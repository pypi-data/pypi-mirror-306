# -*- coding: utf-8 -*-
# Copyright (C) 2012-2024 Team tiramisu (see AUTHORS for all contributors)
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
"""options handler global entry point
"""
import weakref
from copy import copy, deepcopy
from typing import Optional, List, Any, Union
from os.path import commonprefix

from .error import PropertiesOptionError, ConfigError, ConflictError, LeadershipError
from .option import DynOptionDescription, Leadership, Option
from .setting import ConfigBag, Settings, undefined, groups
from .value import Values, owners
from .i18n import _
from .cacheobj import Cache
from .autolib import Calculation
from . import autolib


def get_common_path(path1, path2):
    common_path = commonprefix([path1, path2])
    if common_path in [path1, path2]:
        return common_path
    if common_path.endswith("."):
        return common_path[:-1]
    if "." in common_path:
        return common_path.rsplit(".", 1)[0]
    return None


class CCache:
    __slots__ = tuple()

    # =============================================================================
    # CACHE
    def reset_cache(
        self,
        subconfig,
        resetted_opts=None,
    ):
        """reset all settings in cache"""
        if resetted_opts is None:
            resetted_opts = []
        if subconfig is not None:
            if "cache" not in subconfig.config_bag.properties:
                return
            subconfig.config_bag.properties = subconfig.config_bag.properties - {
                "cache"
            }
            self.reset_one_option_cache(
                subconfig,
                resetted_opts,
            )
            subconfig.config_bag.properties = subconfig.config_bag.properties | {
                "cache"
            }
        else:
            self._impl_values_cache.reset_all_cache()  # pylint: disable=no-member
            self.properties_cache.reset_all_cache()  # pylint: disable=no-member

    def reset_one_option_cache(
        self,
        subconfig,
        resetted_opts,
    ):
        """reset cache for one option"""
        if subconfig.path in resetted_opts:
            return
        resetted_opts.append(subconfig.path)
        config_bag = subconfig.config_bag
        for woption in subconfig.option.get_dependencies(subconfig.option):
            option = woption()
            if option.issubdyn():
                # it's an option in dynoptiondescription, remove cache for all generated option
                self.reset_cache_dyn_option(
                    config_bag,
                    option,
                    resetted_opts,
                )
            elif option.impl_is_dynoptiondescription():
                self._reset_cache_dyn_optiondescription(
                    option,
                    config_bag,
                    resetted_opts,
                )
            else:
                option_subconfig = self.get_sub_config(
                    config_bag,
                    option.impl_getpath(),
                    None,
                    properties=None,
                    validate_properties=False,
                )
                self.reset_one_option_cache(
                    option_subconfig,
                    resetted_opts,
                )
            del option
        subconfig.option.reset_cache(
            subconfig.path,
            config_bag,
            resetted_opts,
        )

    def _reset_cache_dyn_optiondescription(
        self,
        option,
        config_bag,
        resetted_opts,
    ):
        # reset cache for all chidren
        path = option.impl_getpath()
        if "." in path:
            parent_path = path.rsplit(".", 1)[0]
            parent_subconfig = self.get_sub_config(
                config_bag,
                parent_path,
                None,
                properties=None,
                validate_properties=False,
            )
        else:
            parent_subconfig = self.get_root(config_bag)
        for subconfig in parent_subconfig.dyn_to_subconfig(
            option,
            False,
        ):
            self.reset_one_option_cache(
                subconfig,
                resetted_opts,
            )
            for walk_subconfig in self.walk(
                subconfig,
                no_value=True,
                validate_properties=False,
            ):
                self.reset_one_option_cache(
                    walk_subconfig,
                    resetted_opts,
                )

    def reset_cache_dyn_option(
        self,
        config_bag,
        option,
        resetted_opts,
    ):
        currents = [self.get_root(config_bag)]
        sub_paths = option.impl_getpath()
        for sub_path in sub_paths.split("."):
            new_currents = []
            for current in currents:
                sub_option = current.option.get_child(
                    sub_path,
                    config_bag,
                    current,
                    allow_dynoption=True,
                )
                if sub_option.impl_is_dynoptiondescription():
                    new_currents.extend(
                        list(
                            current.dyn_to_subconfig(
                                sub_option,
                                False,
                            )
                        )
                    )

                else:
                    new_currents.append(
                        current.get_child(
                            sub_option,
                            None,
                            False,
                            properties=None,
                        ),
                    )
            currents = new_currents
        for dyn_option_subconfig in currents:
            self.reset_one_option_cache(
                dyn_option_subconfig,
                resetted_opts,
            )


class SubConfig:
    __slots__ = (
        "config_bag",
        "option",
        "parent",
        "index",
        "path",
        "true_path",
        "_properties",
        "apply_requires",
        "transitive_properties",
        "is_dynamic",
        "identifiers",
        "_length",
    )

    def __init__(
        self,
        option: Option,
        index: Optional[int],
        path: str,
        config_bag: ConfigBag,
        parent: Optional["SubConfig"],
        identifiers: Optional[list[str]],
        *,
        true_path: Optional[str] = None,
        properties: Union[list[str], undefined] = undefined,
        validate_properties: bool = True,
    ) -> None:
        self.index = index
        self.identifiers = identifiers
        self.option = option
        self.config_bag = config_bag
        self.parent = parent
        self._length = None
        self.path = path
        if true_path is None:
            true_path = path
        is_follower = (
            not option.impl_is_optiondescription() and option.impl_is_follower()
        )
        self.apply_requires = not is_follower or index is not None
        self.true_path = true_path
        if parent and parent.is_dynamic or self.option.impl_is_dynoptiondescription():
            self.is_dynamic = True
        else:
            self.is_dynamic = False
        self._properties = properties
        if validate_properties:
            if self.path and self._properties is undefined:
                settings = config_bag.context.get_settings()
                self._properties = settings.getproperties(
                    self,
                    apply_requires=False,
                )
                self.config_bag.context.get_settings().validate_properties(self)
                self._properties = undefined
            self.config_bag.context.get_settings().validate_properties(self)
        if self.apply_requires and self.option.impl_is_optiondescription():
            if self.path and self.properties is not None:
                settings = config_bag.context.get_settings()
                self.transitive_properties = settings.calc_transitive_properties(
                    self,
                    self.properties,
                )
            else:
                self.transitive_properties = frozenset()

    @property
    def properties(self):
        if self._properties is undefined:
            if self.path is None:
                self._properties = frozenset()
            else:
                settings = self.config_bag.context.get_settings()
                self._properties = frozenset()
                self._properties = settings.getproperties(
                    self,
                    apply_requires=self.apply_requires,
                )
        return self._properties

    @properties.setter
    def properties(self, properties):
        self._properties = properties

    def __repr__(self):
        return f"<SubConfig path={self.path}, index={self.index}>"

    def dyn_to_subconfig(
        self,
        child: Option,
        validate_properties: bool,
        *,
        true_path: Optional[str] = None,
    ) -> List["SubConfig"]:
        config_bag = self.config_bag
        for identifier in child.get_identifiers(self):
            try:
                name = child.impl_getname(identifier)
                if not validate_properties:
                    properties = None
                else:
                    properties = undefined
                yield self.get_child(
                    child,
                    None,
                    validate_properties,
                    identifier=identifier,
                    name=name,
                    properties=properties,
                    true_path=true_path,
                )
            except PropertiesOptionError as err:
                if err.proptype in (["mandatory"], ["empty"]):
                    raise err

    def get_leadership_children(
        self,
        validate_properties,
    ):
        # it's a leadership so walk to leader and follower
        # followers has specific length
        leader, *followers = self.option.get_children()
        yield self.get_child(
            leader,
            None,
            validate_properties,
        )
        for idx in range(self.get_length_leadership()):
            for follower in followers:
                try:
                    yield self.get_child(
                        follower,
                        idx,
                        validate_properties,
                    )
                except PropertiesOptionError as err:
                    if err.proptype in (["mandatory"], ["empty"]):
                        raise err from err

    def get_children(
        self,
        validate_properties,
        *,
        uncalculated: bool = False,
    ):
        if self.option.impl_is_leadership() and not uncalculated:
            yield from self.get_leadership_children(validate_properties)
        else:
            for child in self.option.get_children():
                if child.impl_is_dynoptiondescription() and not uncalculated:
                    yield from self.dyn_to_subconfig(
                        child,
                        validate_properties,
                    )
                else:
                    try:
                        yield self.get_child(
                            child,
                            None,
                            validate_properties,
                        )
                    except PropertiesOptionError as err:
                        if err.proptype in (["mandatory"], ["empty"]):
                            raise err

    def get_child(
        self,
        option: Option,
        index: Optional[int],
        validate_properties: bool,
        *,
        properties=undefined,
        allow_dynoption: bool = False,
        identifier: Optional[str] = None,
        name: Optional[str] = None,
        check_index: bool = True,
        config_bag: ConfigBag = None,
        true_path: Optional[str] = None,
    ) -> "SubConfig":
        # pylint: disable=too-many-branches,too-many-locals,too-many-arguments
        if config_bag is None:
            config_bag = self.config_bag

        if not self.option.impl_is_optiondescription():
            raise TypeError(f'"{self.path}" is not an optiondescription')
        path = self.get_path(
            name,
            option,
        )
        if identifier is None:
            identifiers = self.identifiers
        else:
            if self.identifiers:
                identifiers = self.identifiers + [identifier]
            else:
                identifiers = [identifier]
        subsubconfig = SubConfig(
            option,
            index,
            path,
            self.config_bag,
            self,
            identifiers,
            properties=properties,
            validate_properties=validate_properties,
            true_path=true_path,
        )
        if check_index and index is not None:
            if option.impl_is_optiondescription() or not option.impl_is_follower():
                raise ConfigError("index must be set only with a follower option")
            length = self.get_length_leadership()
            if index >= length:
                raise LeadershipError(
                    _(
                        'index "{0}" is greater than the leadership length "{1}" for option {2}'
                    ).format(
                        index,
                        length,
                        option.impl_get_display_name(subsubconfig, with_quote=True),
                    )
                )
        return subsubconfig

    def get_path(
        self,
        name: str,
        option: Option,
    ) -> str:
        if name is None:
            name = option.impl_getname()
        if self.path is None:
            path = name
        else:
            path = self.path + "." + name
        return path

    def get_length_leadership(self):
        """Get the length of leader option (useful to know follower's length)"""
        if self._length is None:
            cconfig_bag = self.config_bag.copy()
            cconfig_bag.remove_validation()
            leader = self.option.get_leader()
            path = self.get_path(
                None,
                leader,
            )
            subconfig = SubConfig(
                leader,
                None,
                path,
                cconfig_bag,
                self,
                self.identifiers,
                validate_properties=False,
            )
            self._length = len(cconfig_bag.context.get_value(subconfig))
        return self._length

    def get_common_child(
        self,
        search_option: "BaseOption",
        true_path: Optional[str] = None,
        validate_properties: bool = True,
    ):
        current_option_path = self.option.impl_getpath()
        search_option_path = search_option.impl_getpath()
        common_path = get_common_path(current_option_path, search_option_path)
        config_bag = self.config_bag
        index = None
        if (
            not self.option.impl_is_optiondescription()
            and self.option.impl_is_follower()
            and search_option.impl_is_follower()
            and self.parent.option == search_option.impl_get_leadership()
        ):
            index = self.index
            search_child_number = 0
            parents = [self.parent]
        else:
            if common_path:
                parent = self.parent
                common_parent_number = common_path.count(".") + 1
                for idx in range(current_option_path.count(".") - common_parent_number):
                    parent = parent.parent
                parents = [parent]
            else:
                common_parent_number = 0
                parents = [config_bag.context.get_root(config_bag)]
            search_child_number = search_option_path.count(".") - common_parent_number
        subconfigs_is_a_list = False
        if search_child_number:
            if common_parent_number:
                parent_paths = search_option_path.rsplit(".", search_child_number + 1)[
                    1:-1
                ]
            else:
                parent_paths = search_option_path.split(".")[:-1]
            for parent_path in parent_paths:
                new_parents = []
                for parent in parents:
                    sub_option = parent.option.get_child(
                        parent_path,
                        config_bag,
                        parent,
                        allow_dynoption=True,
                    )
                    if sub_option.impl_is_dynoptiondescription():
                        new_parents.extend(
                            parent.dyn_to_subconfig(
                                sub_option,
                                True,
                                true_path=true_path,
                            )
                        )
                        subconfigs_is_a_list = True
                    else:
                        new_parents.append(
                            parent.get_child(
                                sub_option,
                                None,
                                validate_properties,
                                true_path=true_path,
                            )
                        )
                parents = new_parents
        subconfigs = []
        for parent in parents:
            subconfigs.append(
                parent.get_child(
                    search_option,
                    index,
                    validate_properties,
                )
            )
        if subconfigs_is_a_list:
            return subconfigs
        return subconfigs[0]


class _Config(CCache):
    """Sub configuration management entry.
    Tree if OptionDescription's responsability. SubConfig are generated
    on-demand. A Config is also a SubConfig.
    Root Config is call context below
    """

    __slots__ = (
        "_impl_context",
        "_impl_descr",
        "_impl_path",
    )

    def __init__(
        self,
        descr,
        context,
        subpath=None,
    ):
        """Configuration option management class

        :param descr: describes the configuration schema
        :type descr: an instance of ``option.OptionDescription``
        :param context: the current root config
        :type context: `Config`
        :type subpath: `str` with the path name
        """
        # main option description
        self._impl_descr = descr
        self._impl_context = context
        self._impl_path = subpath

    def get_description(self):
        """get root description"""
        assert self._impl_descr is not None, _(
            "there is no option description for this config" " (may be GroupConfig)"
        )
        return self._impl_descr

    def get_settings(self):
        """get settings object"""
        return self._impl_settings  # pylint: disable=no-member

    def get_values(self):
        """get values object"""
        return self._impl_values  # pylint: disable=no-member

    def get_values_cache(self):
        """get cache for values"""
        return self._impl_values_cache  # pylint: disable=no-member

    # =============================================================================
    # WALK
    def find(
        self,
        option_bag,
        bytype,
        byname,
        byvalue,
        raise_if_not_found=True,
        only_path=undefined,
        only_option=undefined,
        with_option=False,
    ):
        """
        convenience method for finding an option that lives only in the subtree

        :param first: return only one option if True, a list otherwise
        :return: find list or an exception if nothing has been found
        """

        # pylint: disable=too-many-arguments,too-many-locals
        def _filter_by_value(soption_bag):
            value = self.get_value(soption_bag)
            if isinstance(value, list):
                return byvalue in value
            return value == byvalue

        found = False
        if only_path is not undefined:

            def _fake_iter():
                yield only_option

            options = _fake_iter()
        else:
            options = option_bag.option.get_children_recursively(
                bytype,
                byname,
                option_bag.config_bag,
            )
        for option in options:
            path = option.impl_getpath()
            soption_bag = OptionBag(
                option,
                None,
                option_bag.config_bag,
            )
            if byvalue is not undefined and not _filter_by_value(soption_bag):
                continue
            if option_bag.config_bag.properties:
                # remove option with propertyerror, ...
                try:
                    self.get_sub_config(
                        option_bag.config_bag,  # pylint: disable=no-member
                        path,
                        None,
                        validate_properties=True,
                    )
                except PropertiesOptionError:
                    continue
            found = True
            if not with_option:
                yield path
            else:
                yield path, option
        self._find_return_results(
            found,
            raise_if_not_found,
        )

    def _find_return_results(self, found, raise_if_not_found):
        if not found and raise_if_not_found:
            raise AttributeError(_("no option found in config" " with these criteria"))

    def walk_valid_value(
        self,
        subconfig,
        only_mandatory,
    ):
        value = self.get_value(
            subconfig,
            need_help=False,
        )
        ori_config_bag = subconfig.config_bag
        config_bag = ori_config_bag.copy()
        if only_mandatory:
            config_bag.properties |= {"mandatory", "empty"}
        subconfig.config_bag = config_bag
        self.get_settings().validate_mandatory(
            subconfig,
            value,
        )
        subconfig.config_bag = ori_config_bag
        return value

    def get_root(
        self,
        config_bag: ConfigBag,
    ) -> SubConfig:
        return SubConfig(
            config_bag.context.get_description(),
            None,
            None,
            config_bag,
            None,
            None,
        )

    def get_sub_config(
        self,
        config_bag,
        path,
        index,
        *,
        validate_properties: bool = True,
        properties=undefined,
        true_path: Optional[str] = None,
        allow_dynoption: bool = False,
    ):
        subconfig = self.get_root(config_bag)
        if path is None:
            paths = []
            len_path = 0
        else:
            if "." in path:
                paths = path.split(".")
            else:
                paths = [path]
            len_path = len(paths) - 1
        for idx, name in enumerate(paths):
            if idx != len_path:
                index_ = None
                true_path_ = None
            else:
                index_ = index
                true_path_ = true_path

            if not subconfig.option.impl_is_optiondescription():
                raise TypeError(f'"{subconfig.true_path}" is not an optiondescription')
            option = subconfig.option.get_child(
                name,
                config_bag,
                subconfig,
                with_identifier=True,
                allow_dynoption=allow_dynoption,
            )
            if isinstance(option, tuple):
                identifier, option = option
            else:
                identifier = None
            subconfig = subconfig.get_child(
                option,
                index_,
                validate_properties,
                properties=properties,
                name=name,
                identifier=identifier,
                true_path=true_path_,
            )
        return subconfig

    def walk(
        self,
        root_subconfig: SubConfig,
        *,
        no_value: bool = False,
        only_mandatory: bool = False,
        validate_properties: bool = True,
    ):
        if only_mandatory or no_value:
            ret = []
        else:
            ret = {}
        for subconfig in root_subconfig.get_children(validate_properties):
            # pylint: disable=too-many-branches,too-many-locals,too-many-arguments,
            if only_mandatory and subconfig.option.impl_is_symlinkoption():
                continue
            if subconfig.option.impl_is_optiondescription():
                values = self.walk(
                    subconfig,
                    no_value=no_value,
                    only_mandatory=only_mandatory,
                    validate_properties=validate_properties,
                )
                if only_mandatory or no_value:
                    ret.extend(values)
                else:
                    ret[subconfig] = values
            else:
                if no_value:
                    ret.append(subconfig)
                else:
                    option = self.walk_option(
                        subconfig,
                        only_mandatory,
                    )
                    if only_mandatory:
                        if option:
                            ret.append(subconfig)
                    elif option[0]:
                        ret[subconfig] = option[1]
        return ret

    def walk_option(
        self,
        subconfig: SubConfig,
        only_mandatory: bool,
    ):
        try:
            value = self.walk_valid_value(
                subconfig,
                only_mandatory,
            )
        except PropertiesOptionError as err:
            if err.proptype in (["mandatory"], ["empty"]):
                if only_mandatory:
                    return True
                else:
                    raise err from err
        else:
            if not only_mandatory:
                return True, value
        if only_mandatory:
            return False
        return False, None

    # =============================================================================
    # Manage value
    def get_value(
        self,
        subconfig,
        need_help=True,
    ):
        """
        :return: option's value if name is an option name, OptionDescription
                 otherwise
        """
        original_index = subconfig.index
        subconfig = self._get(
            subconfig,
            need_help,
        )
        if isinstance(subconfig, list):
            value = []
            follower_subconfig = None
            is_follower = not subconfig or subconfig[0].option.impl_is_follower()
            for sconfig in subconfig:
                if not is_follower or follower_subconfig is None:
                    follower_subconfig = self.get_sub_config(
                        sconfig.config_bag,
                        sconfig.path,
                        sconfig.index,
                    )
                else:
                    follower_subconfig = follower_subconfig.parent.get_child(
                        sconfig.option,
                        sconfig.index,
                        False,
                    )
                value.append(
                    self.get_value(
                        follower_subconfig,
                        need_help=need_help,
                    )
                )
        else:
            value = self.get_values().get_cached_value(subconfig)
            if subconfig.option.impl_is_follower():
                length = subconfig.parent.get_length_leadership()
                follower_len = self.get_values().get_max_length(subconfig.path)
                if follower_len > length:
                    option_name = subconfig.option.impl_get_display_name(
                        subconfig, with_quote=True
                    )
                    raise LeadershipError(
                        _(
                            "the follower option {0} has greater length ({1}) than the leader length ({2})"
                        ).format(option_name, follower_len, length)
                    )
            self.get_settings().validate_mandatory(
                subconfig,
                value,
            )
            if original_index != subconfig.index:
                value = value[original_index]
        return value

    def _get(
        self,
        subconfig: "SubConfig",
        need_help: bool,
        validate_properties: bool = True,
    ) -> "OptionBag":
        # pylint: disable=too-many-locals
        option = subconfig.option
        if not option.impl_is_symlinkoption():
            return subconfig
        suboption = option.impl_getopt()
        if suboption.issubdyn():
            dynopt = suboption.getsubdyn()
            return subconfig.get_common_child(
                suboption,
                true_path=subconfig.path,
                validate_properties=validate_properties,
            )
        if suboption.impl_is_follower() and subconfig.index is None:
            subconfig = self.get_sub_config(
                subconfig.config_bag,  # pylint: disable=no-member
                suboption.impl_getpath(),
                None,
                validate_properties=validate_properties,
                true_path=subconfig.path,
            )
            leadership_length = subconfig.parent.get_length_leadership()
            ret = []
            follower = subconfig.option
            parent = subconfig.parent
            for idx in range(leadership_length):
                ret.append(
                    parent.get_child(
                        follower,
                        idx,
                        True,
                    )
                )
            return ret

        if suboption.impl_is_leader():
            index = None
        else:
            index = subconfig.index
        s_subconfig = self.get_sub_config(
            subconfig.config_bag,  # pylint: disable=no-member
            suboption.impl_getpath(),
            index,
            validate_properties=validate_properties,
            true_path=subconfig.path,
        )
        return self._get(
            s_subconfig,
            need_help,
        )

    def get_owner(
        self,
        subconfig: "SubConfig",
    ):
        """get owner"""
        subconfigs = self._get(
            subconfig,
            need_help=True,
        )
        if isinstance(subconfigs, list):
            for sc in subconfigs:
                owner = self.get_owner(
                    sc,
                )
                if owner != owners.default:
                    break
            else:
                owner = owners.default
        else:
            owner = self.get_values().getowner(subconfigs)
        return owner


class _CommonConfig(_Config):
    "abstract base class for the Config, KernelGroupConfig and the KernelMetaConfig"
    __slots__ = (
        "_impl_values",
        "_impl_values_cache",
        "_impl_settings",
        "properties_cache",
        "_impl_permissives_cache",
        "parents",
        "impl_type",
    )

    def _impl_build_all_caches(self, descr):
        if not descr.impl_already_build_caches():
            descr._group_type = groups.root  # pylint: disable=protected-access
            descr._build_cache(
                self._display_name
            )  # pylint: disable=no-member,protected-access
        if not hasattr(descr, "_cache_force_store_values"):
            raise ConfigError(
                _("option description seems to be part of an other " "config")
            )

    def get_parents(self):
        """get parents"""
        for parent in self.parents:  # pylint: disable=no-member
            yield parent()

    # information
    def impl_set_information(
        self,
        config_bag,
        key,
        value,
    ):
        """updates the information's attribute

        :param key: information's key (ex: "help", "doc"
        :param value: information's value (ex: "the help string")
        """
        self._impl_values.set_information(
            None,  # pylint: disable=no-member
            key,
            value,
        )
        for option in self.get_description()._cache_dependencies_information.get(
            key, []
        ):  # pylint: disable=protected-access
            # option_bag = OptionBag(option,
            #                       None,
            #                       config_bag,
            #                       properties=None,
            #                       )
            option_bag = None
            self.reset_cache(option_bag)

    def impl_get_information(
        self,
        subconfig,
        key,
        default,
    ):
        """retrieves one information's item

        :param key: the item string (ex: "help")
        """
        return self._impl_values.get_information(
            None,  # pylint: disable=no-member
            key,
            default,
        )

    def impl_del_information(
        self,
        key,
        raises=True,
    ):
        """delete an information"""
        self._impl_values.del_information(
            key,  # pylint: disable=no-member
            raises,
        )

    def impl_list_information(self):
        """list information keys for context"""
        return self._impl_values.list_information()  # pylint: disable=no-member

    def gen_fake_context(self) -> "KernelConfig":
        """generate a fake values to improve validation when assign a new value"""
        export = deepcopy(self.get_values()._values)  # pylint: disable=protected-access
        fake_context = KernelConfig(
            self._impl_descr,
            force_values=export,
            force_settings=self.get_settings(),
            name=self._impl_name,  # pylint: disable=no-member
        )
        fake_context.parents = self.parents  # pylint: disable=no-member
        return fake_context

    def duplicate(
        self,
        force_values=None,
        force_settings=None,
        metaconfig_prefix=None,
        child=None,
        deep=None,
        name=None,
    ):
        """duplication config"""
        # pylint: disable=too-many-arguments
        if name is None:
            name = self._impl_name  # pylint: disable=no-member
        if isinstance(self, KernelConfig):
            duplicated_config = KernelConfig(
                self._impl_descr,
                _duplicate=True,
                force_values=force_values,
                force_settings=force_settings,
                name=name,
            )
        else:
            duplicated_config = KernelMetaConfig(
                [],
                _duplicate=True,
                optiondescription=self._impl_descr,
                name=name,
            )
        duplicated_values = duplicated_config.get_values()
        duplicated_settings = duplicated_config.get_settings()
        duplicated_values._values = deepcopy(
            self.get_values()._values
        )  # pylint: disable=protected-access
        duplicated_values._informations = deepcopy(
            self.get_values()._informations
        )  # pylint: disable=protected-access
        duplicated_settings._properties = deepcopy(
            self.get_settings()._properties
        )  # pylint: disable=protected-access
        duplicated_settings._permissives = deepcopy(
            self.get_settings()._permissives
        )  # pylint: disable=protected-access
        duplicated_settings.ro_append = self.get_settings().ro_append
        duplicated_settings.rw_append = self.get_settings().rw_append
        duplicated_settings.ro_remove = self.get_settings().ro_remove
        duplicated_settings.rw_remove = self.get_settings().rw_remove
        #        duplicated_settings.default_properties = self.get_settings().default_properties
        duplicated_config.reset_cache(None, None)
        if child is not None:
            duplicated_config._impl_children.append(
                child
            )  # pylint: disable=protected-access
            child.parents.append(weakref.ref(duplicated_config))
        if self.parents:  # pylint: disable=no-member
            if deep is not None:
                for parent in self.parents:  # pylint: disable=no-member
                    wparent = parent()
                    if wparent not in deep:
                        deep.append(wparent)
                        subname = wparent.impl_getname()
                        if metaconfig_prefix:
                            subname = metaconfig_prefix + subname
                        duplicated_config = wparent.duplicate(
                            deep=deep,
                            metaconfig_prefix=metaconfig_prefix,
                            child=duplicated_config,
                            name=subname,
                        )
            else:
                duplicated_config.parents = self.parents  # pylint: disable=no-member
                for parent in self.parents:  # pylint: disable=no-member
                    parent()._impl_children.append(
                        duplicated_config
                    )  # pylint: disable=protected-access
        return duplicated_config

    def get_config_path(self):
        """get config path"""
        path = self.impl_getname()
        for parent in self.parents:  # pylint: disable=no-member
            wparent = parent()
            if wparent is None:  # pragma: no cover
                raise ConfigError(
                    _("parent of {0} not already exists").format(self._impl_name)
                )  # pylint: disable=no-member
            path = parent().get_config_path() + "." + path
        return path

    def impl_getname(self):
        """get config name"""
        return self._impl_name  # pylint: disable=no-member


# ____________________________________________________________
class KernelConfig(_CommonConfig):
    """main configuration management entry"""

    # pylint: disable=too-many-instance-attributes
    __slots__ = (
        "__weakref__",
        "_impl_name",
        "_display_name",
        "_impl_symlink",
        "_storage",
    )
    impl_type = "config"

    def __init__(
        self,
        descr,
        force_values=None,
        force_settings=None,
        name=None,
        display_name=None,
        _duplicate=False,
    ):
        """Configuration option management class

        :param descr: describes the configuration schema
        :type descr: an instance of ``option.OptionDescription``
        :param context: the current root config
        :type context: `Config`
        """
        # pylint: disable=too-many-arguments,too-many-arguments
        self._display_name = display_name
        self.parents = []
        self._impl_symlink = []
        self._impl_name = name
        if isinstance(descr, Leadership):
            raise ConfigError(
                _("cannot set leadership object has root optiondescription")
            )
        if isinstance(descr, DynOptionDescription):
            msg = _("cannot set dynoptiondescription object has root optiondescription")
            raise ConfigError(msg)
        if force_settings is not None and force_values is not None:
            self._impl_settings = force_settings
            self._impl_permissives_cache = Cache()
            self.properties_cache = Cache()
            self._impl_values = Values(force_values)
            self._impl_values_cache = Cache()
        else:
            self._impl_settings = Settings()
            self._impl_permissives_cache = Cache()
            self.properties_cache = Cache()
            self._impl_values = Values()
            self._impl_values_cache = Cache()
        self._impl_context = weakref.ref(self)
        if None in [force_settings, force_values]:
            self._impl_build_all_caches(descr)
        super().__init__(
            descr,
            self._impl_context,
            None,
        )


class KernelGroupConfig(_CommonConfig):
    """Group a config with same optiondescription tree"""

    __slots__ = (
        "__weakref__",
        "_impl_children",
        "_impl_name",
        "_display_name",
    )
    impl_type = "group"

    def __init__(
        self,
        children,
        display_name=None,
        name=None,
        _descr=None,
    ):
        # pylint: disable=super-init-not-called
        names = []
        for child in children:
            name_ = child._impl_name
            names.append(name_)
        if len(names) != len(set(names)):
            while range(1, len(names) + 1):
                name = names.pop(0)
                if name in names:
                    raise ConflictError(
                        _(
                            "config name must be uniq in " 'groupconfig for "{0}"'
                        ).format(name)
                    )

        self._impl_children = children
        self.parents = []
        self._display_name = display_name
        if name:
            self._impl_name = name
        self._impl_context = weakref.ref(self)
        self._impl_descr = _descr
        self._impl_path = None

    def get_children(self):
        """get all children"""
        return self._impl_children

    def reset_cache(
        self,
        option_bag,
        resetted_opts=None,
    ):
        if resetted_opts is None:
            resetted_opts = []
        if isinstance(self, KernelMixConfig):
            super().reset_cache(
                option_bag,
                resetted_opts=copy(resetted_opts),
            )
        for child in self._impl_children:
            if option_bag is not None:
                coption_bag = option_bag.copy()
                cconfig_bag = coption_bag.config_bag.copy()
                cconfig_bag.context = child
                coption_bag.config_bag = cconfig_bag
            else:
                coption_bag = None
            child.reset_cache(
                coption_bag,
                resetted_opts=copy(resetted_opts),
            )

    def set_value(
        self,
        option_bag,
        value,
        only_config=False,
    ):
        """Setattr not in current KernelGroupConfig, but in each children"""
        ret = []
        for child in self._impl_children:
            cconfig_bag = option_bag.config_bag.copy()
            cconfig_bag.context = child
            if isinstance(child, KernelGroupConfig):
                ret.extend(
                    child.set_value(
                        option_bag,
                        value,
                        only_config=only_config,
                    )
                )
            else:
                settings = child.get_settings()
                properties = settings.get_context_properties(child.properties_cache)
                permissives = settings.get_context_permissives()
                cconfig_bag.properties = properties
                cconfig_bag.permissives = permissives
                try:
                    # GROUP
                    coption_bag = child.get_sub_option_bag(
                        cconfig_bag,
                        option_bag.path,
                        option_bag.index,
                        False,
                    )
                    child.set_value(
                        coption_bag,
                        value,
                    )
                except PropertiesOptionError as err:
                    # pylint: disable=protected-access
                    ret.append(
                        PropertiesOptionError(
                            err._option_bag,
                            err.proptype,
                            err._settings,
                            err._opt_type,
                            err._name,
                            err._orig_opt,
                        )
                    )
                except (ValueError, LeadershipError, AttributeError) as err:
                    ret.append(err)
        return ret

    def find_group(
        self,
        config_bag,
        byname=None,
        bypath=undefined,
        byoption=undefined,
        byvalue=undefined,
        raise_if_not_found=True,
        _sub=False,
    ):
        """Find first not in current KernelGroupConfig, but in each children"""
        # pylint: disable=too-many-arguments
        # if KernelMetaConfig, all children have same OptionDescription in
        # context so search only one time the option for all children
        if bypath is undefined and byname is not None and self.impl_type == "meta":
            root_option_bag = OptionBag(
                self.get_description(),
                None,
                config_bag,
            )
            next(
                self.find(
                    root_option_bag,
                    bytype=None,
                    byname=byname,
                    byvalue=undefined,
                    raise_if_not_found=raise_if_not_found,
                    with_option=True,
                )
            )
            byname = None

        ret = []
        for child in self._impl_children:
            if isinstance(child, KernelGroupConfig):
                ret.extend(
                    child.find_group(
                        byname=byname,
                        bypath=bypath,
                        byoption=byoption,
                        byvalue=byvalue,
                        config_bag=config_bag,
                        raise_if_not_found=False,
                        _sub=True,
                    )
                )
            else:
                cconfig_bag = config_bag.copy()
                cconfig_bag.context = child
                if cconfig_bag.properties is None:
                    settings = child.get_settings()
                    properties = settings.get_context_properties(child.properties_cache)
                    permissives = settings.get_context_permissives()
                    cconfig_bag.properties = properties
                    cconfig_bag.permissives = permissives
                root_option_bag = OptionBag(
                    child.get_description(),
                    None,
                    cconfig_bag,
                )
                try:
                    next(
                        child.find(
                            root_option_bag,
                            None,
                            byname,
                            byvalue,
                            raise_if_not_found=False,
                            only_path=bypath,
                            only_option=byoption,
                        )
                    )
                    ret.append(child)
                except StopIteration:
                    pass
        if not _sub:
            self._find_return_results(
                ret != [],  # pylint: disable=use-implicit-booleaness-not-comparison
                raise_if_not_found,
            )
        return ret

    def reset(
        self,
        path: str,
        config_bag: ConfigBag,
    ) -> None:
        """reset value for specified path"""
        for child in self._impl_children:
            settings = child.get_settings()
            cconfig_bag = config_bag.copy()
            cconfig_bag.context = child
            settings = child.get_settings()
            properties = settings.get_context_properties(child.properties_cache)
            permissives = settings.get_context_permissives()
            cconfig_bag.properties = properties
            cconfig_bag.permissives = permissives
            cconfig_bag.remove_validation()
            # GROUP
            option_bag = child.get_sub_option_bag(
                cconfig_bag,
                path,
                None,
                False,
            )[-1]
            child.get_values().reset(option_bag)

    def getconfig(
        self,
        name: str,
    ) -> KernelConfig:
        """get a child from a config name"""
        for child in self._impl_children:
            if name == child.impl_getname():
                return child
        raise ConfigError(_('unknown config "{}"').format(name))


class KernelMixConfig(KernelGroupConfig):
    """Kernel mixconfig: this config can have differents optiondescription tree"""

    # pylint: disable=too-many-instance-attributes
    __slots__ = (
        "_impl_symlink",
        "_storage",
    )
    impl_type = "mix"

    def __init__(
        self,
        optiondescription,
        children,
        name=None,
        display_name=None,
        _duplicate=False,
    ):
        self._impl_name = name
        self._impl_symlink = []
        for child in children:
            if not isinstance(child, (KernelConfig, KernelMixConfig)):
                raise TypeError(_("child must be a Config, MixConfig or MetaConfig"))
            child.parents.append(weakref.ref(self))
        self._impl_settings = Settings()
        self._impl_settings._properties = deepcopy(self._impl_settings._properties)
        self._impl_settings._permissives = deepcopy(self._impl_settings._permissives)
        self._impl_permissives_cache = Cache()
        self.properties_cache = Cache()
        self._impl_values = Values()
        self._impl_values._values = deepcopy(self._impl_values._values)
        self._impl_values_cache = Cache()
        self._display_name = display_name
        self._impl_build_all_caches(optiondescription)
        super().__init__(
            children,
            _descr=optiondescription,
            display_name=display_name,
        )

    def set_value(
        self,
        option_bag,
        value,
        only_config=False,
        force_default=False,
        force_dont_change_value=False,
        force_default_if_same=False,
    ):
        """only_config: could be set if you want modify value in all Config included in
        this KernelMetaConfig
        """
        # pylint: disable=too-many-branches,too-many-nested-blocks,too-many-locals,too-many-arguments
        ret = []
        if only_config:
            if force_default or force_default_if_same or force_dont_change_value:
                raise ValueError(
                    _(
                        "force_default, force_default_if_same or "
                        "force_dont_change_value cannot be set with"
                        " only_config"
                    )
                )
        else:
            if force_default or force_default_if_same or force_dont_change_value:
                if force_default and force_dont_change_value:
                    raise ValueError(
                        _(
                            "force_default and force_dont_change_value"
                            " cannot be set together"
                        )
                    )
                for child in self._impl_children:
                    cconfig_bag = option_bag.config_bag.copy()
                    cconfig_bag.context = child
                    settings = child.get_settings()
                    properties = settings.get_context_properties(child.properties_cache)
                    cconfig_bag.properties = properties
                    cconfig_bag.permissives = settings.get_context_permissives()
                    try:
                        if self.impl_type == "meta":
                            obj = self
                        else:
                            obj = child
                        validate_properties = (
                            not force_default and not force_default_if_same
                        )
                        # MIX
                        moption_bag = obj.get_sub_option_bag(
                            cconfig_bag,
                            option_bag.path,
                            option_bag.index,
                            validate_properties,
                        )[-1]
                        if force_default_if_same:
                            if not child.get_values().hasvalue(option_bag.path):
                                child_value = undefined
                            else:
                                child_value = child.get_value(moption_bag)
                        if force_default or (
                            force_default_if_same and value == child_value
                        ):
                            child.get_values().reset(moption_bag)
                            continue
                        if force_dont_change_value:
                            child_value = child.get_value(moption_bag)
                            if value != child_value:
                                child.set_value(
                                    moption_bag,
                                    child_value,
                                )
                    except PropertiesOptionError as err:
                        # pylint: disable=protected-access
                        ret.append(
                            PropertiesOptionError(
                                err._option_bag,
                                err.proptype,
                                err._settings,
                                err._opt_type,
                                err._name,
                                err._orig_opt,
                            )
                        )
                    except (ValueError, LeadershipError, AttributeError) as err:
                        ret.append(err)

        try:
            # MIX
            moption_bag = self.get_sub_option_bag(
                option_bag.config_bag,
                option_bag.path,
                option_bag.index,
                not only_config,
            )[-1]
            if only_config:
                ret = super().set_value(
                    moption_bag,
                    value,
                    only_config=only_config,
                )
            else:
                _CommonConfig.set_value(
                    self,
                    moption_bag,
                    value,
                )
        except (PropertiesOptionError, ValueError, LeadershipError) as err:
            ret.append(err)
        return ret

    def reset(
        self,
        path: str,
        only_children: bool,
        config_bag: ConfigBag,
    ) -> None:
        """reset value for a specified path"""
        # pylint: disable=arguments-differ
        rconfig_bag = config_bag.copy()
        rconfig_bag.remove_validation()
        if self.impl_type == "meta":
            # MIX
            option_bag = self.get_sub_option_bag(
                config_bag,
                path,
                None,
                True,
            )[-1]
        elif not only_children:
            try:
                # MIX
                option_bag = self.get_sub_option_bag(
                    rconfig_bag,
                    path,
                    None,
                    True,
                )[-1]
            except AttributeError:
                only_children = True
        for child in self._impl_children:
            rconfig_bag.context = child
            try:
                if self.impl_type == "meta":
                    moption_bag = option_bag
                    moption_bag.config_bag = rconfig_bag
                else:
                    # MIX
                    moption_bag = child.get_sub_option_bag(
                        rconfig_bag,
                        path,
                        None,
                        True,
                    )[-1]
                child.get_values().reset(moption_bag)
            except AttributeError:
                pass
            if isinstance(child, KernelMixConfig):
                child.reset(
                    path,
                    False,
                    rconfig_bag,
                )
        if not only_children:
            option_bag.config_bag = config_bag
            self.get_values().reset(option_bag)

    def new_config(
        self,
        name=None,
        type_="config",
    ):
        """Create a new config/metaconfig/mixconfig and add it to this MixConfig"""
        if name:
            for child in self._impl_children:
                if child.impl_getname() == name:
                    raise ConflictError(
                        _("config name must be uniq in " "groupconfig for {0}").format(
                            child
                        )
                    )
        assert type_ in ("config", "metaconfig", "mixconfig"), _(
            "unknown type {}"
        ).format(type_)
        if type_ == "config":
            config = KernelConfig(self._impl_descr, name=name)
        elif type_ == "metaconfig":
            config = KernelMetaConfig(
                [],
                optiondescription=self._impl_descr,
                name=name,
            )
        elif type_ == "mixconfig":
            config = KernelMixConfig(
                children=[],
                optiondescription=self._impl_descr,
                name=name,
            )
        # Copy context properties/permissives
        settings = config.get_settings()
        properties = settings.get_context_properties()
        settings.set_context_properties(
            properties,
            config,
        )
        settings.set_context_permissives(settings.get_context_permissives())
        settings.ro_append = settings.ro_append
        settings.rw_append = settings.rw_append
        settings.ro_remove = settings.ro_remove
        settings.rw_remove = settings.rw_remove
        #        settings.default_properties = settings.default_properties

        config.parents.append(weakref.ref(self))
        self._impl_children.append(config)
        return config

    def add_config(
        self,
        config,
    ):
        """Add a child config to a mix config"""
        if not config.impl_getname():
            raise ConfigError(_("config added has no name, the name is mandatory"))
        if config.impl_getname() in [
            child.impl_getname() for child in self._impl_children
        ]:
            raise ConflictError(
                _('config name "{0}" is not uniq in ' 'groupconfig "{1}"').format(
                    config.impl_getname(), self.impl_getname()
                ),
            )
        config.parents.append(weakref.ref(self))
        self._impl_children.append(config)
        config.reset_cache(None, None)

    def remove_config(
        self,
        name,
    ):
        """Remove a child config to a mix config by it's name"""
        for current_index, child in enumerate(self._impl_children):
            if name == child.impl_getname():
                child.reset_cache(None, None)
                break
        else:
            raise ConfigError(_("cannot find the config {0}").format(name))
        for child_index, parent in enumerate(child.parents):
            if parent() == self:
                break
        else:  # pragma: no cover
            raise ConfigError(
                _("cannot find the config {0}").format(self.impl_getname())
            )
        self._impl_children.pop(current_index)
        child.parents.pop(child_index)
        return child


class KernelMetaConfig(KernelMixConfig):
    """Meta config"""

    __slots__ = tuple()
    impl_type = "meta"

    def __init__(
        self,
        children,
        optiondescription=None,
        name=None,
        display_name=None,
        _duplicate=False,
    ):
        descr = None
        if optiondescription is not None:
            if not _duplicate:
                new_children = []
                for child_name in children:
                    assert isinstance(child_name, str), _(
                        "MetaConfig with optiondescription"
                        " must have string has child, "
                        "not {}"
                    ).format(child_name)
                    new_children.append(
                        KernelConfig(optiondescription, name=child_name)
                    )
                children = new_children
            descr = optiondescription
        for child in children:
            if __debug__ and not isinstance(child, (KernelConfig, KernelMetaConfig)):
                raise TypeError(_("child must be a Config or MetaConfig"))
            if descr is None:
                descr = child.get_description()
            elif descr is not child.get_description():
                raise ValueError(
                    _(
                        "all config in metaconfig must "
                        "have the same optiondescription"
                    )
                )
        super().__init__(
            descr,
            children,
            name=name,
            display_name=display_name,
        )

    def add_config(
        self,
        config,
    ):
        if self._impl_descr is not config.get_description():
            raise ValueError(_("metaconfig must " "have the same optiondescription"))
        super().add_config(config)
