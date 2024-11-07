# -*- coding: utf-8 -*-
# Copyright (C) 2014-2024 Team tiramisu (see AUTHORS for all contributors)
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# The original `Config` design model is unproudly borrowed from
# the rough pypy's guys: http://codespeak.net/svn/pypy/dist/pypy/config/
# the whole pypy projet is under MIT licence
# ____________________________________________________________
"""OptionDescription
"""
import weakref
from typing import Optional, Iterator, Union, List, Dict


from ..i18n import _
from ..setting import ConfigBag, groups, undefined, owners, Undefined
from .baseoption import BaseOption

# from .syndynoption import SubDynOptionDescription, SynDynOptionDescription
from ..error import ConfigError, ConflictError


class CacheOptionDescription(BaseOption):
    """manage cache for option description"""

    __slots__ = (
        "_cache_force_store_values",
        "_cache_dependencies_information",
    )

    def impl_already_build_caches(self) -> bool:
        """is a readonly option?"""
        return self.impl_is_readonly()

    def _build_cache(
        self,
        display_name,
        _consistencies=None,
        _consistencies_id=0,
        currpath: List[str] = None,
        cache_option=None,
        force_store_values=None,
        dependencies_information=None,
    ) -> None:
        """validate options and set option has readonly option"""
        # pylint: disable=too-many-branches,too-many-arguments
        # _consistencies is None only when we start to build cache
        if _consistencies is None:
            init = True
            _consistencies = {}
            if __debug__:
                cache_option = []
            force_store_values = []
            dependencies_information = {}
            currpath = []
        else:
            init = False

        if self.impl_is_readonly():
            # cache already set
            raise ConfigError(
                _("option description seems to be part of an other " "config")
            )
        for option in self.get_children():
            if __debug__:
                cache_option.append(option)
            sub_currpath = currpath + [option.impl_getname()]
            subpath = ".".join(sub_currpath)
            if isinstance(option, OptionDescription):
                # pylint: disable=protected-access
                option._build_cache(
                    display_name,
                    _consistencies,
                    _consistencies_id,
                    sub_currpath,
                    cache_option,
                    force_store_values,
                    dependencies_information,
                )
            elif not option.impl_is_symlinkoption():
                informations = option.get_dependencies_information()
                if informations:
                    for param in informations.pop(None):
                        del param.self_option
                for (
                    information,
                    options,
                ) in option.get_dependencies_information().items():
                    if None in options:
                        dependencies_information.setdefault(information, []).append(
                            option
                        )
                properties = option.impl_getproperties()
                if "force_store_value" in properties:
                    force_store_values.append(option)
            if option.impl_is_readonly():
                raise ConflictError(_("duplicate option: {0}").format(option))
            if not self.impl_is_readonly() and display_name:
                option._display_name_function = (
                    display_name  # pylint: disable=protected-access
                )
            option._path = subpath  # pylint: disable=protected-access
            option._set_readonly()  # pylint: disable=protected-access
        if init:
            self._cache_force_store_values = (
                force_store_values  # pylint: disable=attribute-defined-outside-init
            )
            self._cache_dependencies_information = dependencies_information  # pylint: disable=attribute-defined-outside-init
            self._path = (
                None  # pylint: disable=attribute-defined-outside-init,no-member
            )
            self._set_readonly()

    def impl_build_force_store_values(
        self,
        config_bag: ConfigBag,
    ) -> None:
        """set value to force_store_values option"""
        # pylint: disable=too-many-branches
        context = config_bag.context
        if "force_store_value" not in config_bag.properties:
            return

        values = config_bag.context.get_values()
        for option in self._cache_force_store_values:
            if option.issubdyn():
                paths = option.impl_getpath().split(".")
                parents = [config_bag.context.get_root(config_bag)]
                for name in paths:
                    new_parents = []
                    for parent in parents:
                        doption = parent.option.get_child(
                            name,
                            config_bag,
                            parent,
                            allow_dynoption=True,
                        )
                        if doption.impl_is_dynoptiondescription():
                            new_parents.extend(
                                parent.dyn_to_subconfig(
                                    doption,
                                    True,
                                )
                            )
                        else:
                            new_parents.append(
                                parent.get_child(
                                    doption,
                                    None,
                                    True,
                                    name=name,
                                )
                            )
                    parents = new_parents
                subconfigs = new_parents
            else:
                subconfigs = [
                    context.get_sub_config(
                        config_bag,
                        option.impl_getpath(),
                        None,
                        properties=None,
                        validate_properties=False,
                    )
                ]

            if option.impl_is_follower():
                for follower_subconfig in subconfigs:
                    parent = follower_subconfig.parent
                    follower_len = parent.get_length_leadership()
                    for index in range(follower_len):
                        if values.hasvalue(
                            follower_subconfig.path,
                            index=index,
                        ):
                            continue
                        idx_follower_subconfig = parent.get_child(
                            follower_subconfig.option,
                            index,
                            validate_properties=False,
                        )

                        value = values.get_value(idx_follower_subconfig)[0]
                        if value is None:
                            continue
                        values.set_storage_value(
                            follower_subconfig.path,
                            index,
                            value,
                            owners.forced,
                        )
            else:
                for subconfig in subconfigs:
                    subconfig.properties = frozenset()
                    value = values.get_value(subconfig)[0]
                    if value is None:
                        continue
                    if values.hasvalue(subconfig.path):
                        continue
                    values.set_storage_value(
                        subconfig.path,
                        None,
                        value,
                        owners.forced,
                    )


class OptionDescriptionWalk(CacheOptionDescription):
    """get child of option description"""

    __slots__ = ("_children",)

    def get_path(
        self,
        config_bag,
    ):
        if config_bag is undefined or config_bag.context.get_description() == self:
            return ""
        return self.impl_getpath()

    def get_child_not_dynamic(
        self,
        name,
        allow_dynoption,
    ):
        if name in self._children[0]:  # pylint: disable=no-member
            option = self._children[1][
                self._children[0].index(name)
            ]  # pylint: disable=no-member
            if option.impl_is_dynoptiondescription() and not allow_dynoption:
                raise AttributeError(
                    _(
                        'unknown option "{0}" in root optiondescription (it\'s a dynamic option)'
                    ).format(name)
                )
            return option

    def get_child(
        self,
        name: str,
        config_bag: ConfigBag,
        parent: "SubConfig",
        *,
        with_identifier: bool = False,
        allow_dynoption: bool = False,
    ) -> Union[BaseOption]:
        """get a child"""
        # if not dyn
        option = self.get_child_not_dynamic(
            name,
            allow_dynoption,
        )
        if option:
            return option
        # if dyn
        for child in self._children[1]:  # pylint: disable=no-member
            if not child.impl_is_dynoptiondescription():
                continue
            for identifier in child.get_identifiers(parent):
                if name != child.impl_getname(identifier):
                    continue
                if not with_identifier:
                    return child
                return identifier, child
        if self.impl_get_group_type() == groups.root:  # pylint: disable=no-member
            raise AttributeError(
                _('unknown option "{0}" in root optiondescription').format(name)
            )
        raise AttributeError(
            _('unknown option "{0}" in optiondescription {1}').format(
                name, self.impl_get_display_name(parent, with_quote=True)
            )
        )

    def get_children(self) -> List[BaseOption]:
        """get children"""
        return self._children[1]

    def get_children_recursively(
        self,
        bytype: Optional[BaseOption],
        byname: Optional[str],
        config_bag: ConfigBag,
        self_opt: BaseOption = None,
        *,
        option_identifiers: Optional[list] = None,
    ) -> Iterator[Union[BaseOption]]:
        """get children recursively"""
        if self_opt is None:
            self_opt = self
        for option in self_opt.get_children():
            if option.impl_is_optiondescription():
                for subopt in option.get_children_recursively(
                    bytype,
                    byname,
                    config_bag,
                ):
                    yield subopt
            elif (byname is None or option.impl_getname() == byname) and (
                bytype is None or isinstance(option, bytype)
            ):
                yield option


class OptionDescription(OptionDescriptionWalk):
    """Config's schema (organisation, group) and container of Options
    The `OptionsDescription` objects lives in the `tiramisu.config.Config`.
    """

    __slots__ = ("_group_type",)

    def __init__(
        self,
        name: str,
        doc: str,
        children: List[BaseOption],
        *,
        properties=None,
        informations: Optional[Dict] = None,
        group_type: Optional[groups.GroupType] = groups.default,
    ) -> None:
        """
        :param children: a list of options (including optiondescriptions)

        """
        assert isinstance(children, list), _(
            'children in optiondescription "{}" ' "must be a list"
        ).format(name)
        super().__init__(
            name,
            doc,
            informations,
            properties=properties,
        )
        child_names = []
        if __debug__:
            dynopt_names = []
        for child in children:
            name = child.impl_getname()
            child_names.append(name)
            if __debug__ and child.impl_is_dynoptiondescription():
                dynopt_names.append(name)

        # before sorting
        children_ = (tuple(child_names), tuple(children))

        if __debug__:
            # better performance like this
            child_names.sort()
            old = None
            for child in child_names:
                if child == old:
                    raise ConflictError(
                        _("duplicate option name: " '"{0}"').format(child)
                    )
                if dynopt_names:
                    for dynopt in dynopt_names:
                        if child != dynopt and child.startswith(dynopt):
                            raise ConflictError(
                                _(
                                    'the option\'s name "{0}" start as the dynoptiondescription\'s name "{1}"'
                                ).format(child, dynopt)
                            )
                old = child
        self._children = children_
        # the group_type is useful for filtering OptionDescriptions in a config
        self._group_type = None
        self.impl_set_group_type(group_type)

    def _setsubdyn(
        self,
        subdyn,
    ) -> None:
        for child in self._children[1]:
            child._setsubdyn(subdyn)
        super()._setsubdyn(subdyn)

    def impl_is_optiondescription(self) -> bool:
        """the option is an option description"""
        return True

    def impl_is_dynoptiondescription(self) -> bool:
        """the option is not dynamic"""
        return False

    def impl_is_leadership(self) -> bool:
        """the option is not a leadership"""
        return False

    # ____________________________________________________________
    def impl_set_group_type(
        self,
        group_type: groups.GroupType,
    ) -> None:
        """sets a given group object to an OptionDescription

        :param group_type: an instance of `GroupType` or `LeadershipGroupType`
                              that lives in `setting.groups`
        """
        if __debug__:
            if self._group_type is not None and self._group_type != groups.default:
                raise ValueError(
                    _(
                        "cannot change group_type if already set " "(old {0}, new {1})"
                    ).format(self._group_type, group_type)
                )
            if not isinstance(group_type, groups.GroupType):
                raise ValueError(_("group_type: {0}" " not allowed").format(group_type))
            if isinstance(group_type, groups.LeadershipGroupType):
                raise ConfigError(
                    "please use Leadership object instead of OptionDescription"
                )
        self._group_type = group_type

    def impl_get_group_type(self) -> groups.GroupType:
        """get the group type of option description"""
        return self._group_type

    def impl_is_dynsymlinkoption(self) -> bool:
        """option is not a dyn symlink option"""
        return False
