# -*- coding: utf-8 -*-
"takes care of the option's values and multi values"
# Copyright (C) 2013-2024 Team tiramisu (see AUTHORS for all contributors)
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
# ____________________________________________________________
from typing import Union, Optional, List, Any
from .error import ConfigError
from .setting import owners, undefined, forbidden_owners
from .autolib import Calculation, get_calculated_value
from .i18n import _


class Values:
    """This class manage value (default value, stored value or calculated value
    It's also responsible of a caching utility.
    """

    # pylint: disable=too-many-public-methods
    __slots__ = (
        "_values",
        "_informations",
        "__weakref__",
    )

    def __init__(
        self,
        default_values: Union[None, dict] = None,
    ) -> None:
        """
        Initializes the values's dict.

        :param default_values: values stored by default for this object

        """
        self._informations = {}
        # set default owner
        if not default_values:
            default_values = {None: {None: [None, owners.user]}}
        self._values = default_values

    # ______________________________________________________________________
    # get value
    def get_cached_value(
        self,
        subconfig: "SubConfig",
    ) -> Any:
        """get value directly in cache if set
        otherwise calculated value and set it in cache

        :returns: value
        """
        # try to retrive value in cache
        setting_properties = subconfig.config_bag.properties
        cache = subconfig.config_bag.context.get_values_cache()
        is_cached, value, validated = cache.getcache(
            subconfig,
            "values",
        )
        # no cached value so get value
        if not is_cached:
            value, has_calculation = self.get_value(subconfig)
        # validates and warns value
        if not validated:
            validate = subconfig.option.impl_validate(
                subconfig,
                value,
                check_error=True,
            )
        if "warnings" in setting_properties:
            subconfig.option.impl_validate(
                subconfig,
                value,
                check_error=False,
            )
        # set value to cache
        if not is_cached and not has_calculation:
            cache.setcache(
                subconfig,
                value,
                validated=validate,
            )
        if isinstance(value, list):
            # return a copy, so value cannot be modified
            value = value.copy()
        # and return it
        return value

    def get_value(
        self,
        subconfig: "SubConfig",
    ) -> Any:
        """actually retrieves the stored value or the default value (value modified by user)

        :returns: value
        """
        # get owner and value from store
        default_value = [undefined, owners.default]
        value, owner = self._values.get(subconfig.path, {}).get(
            subconfig.index, default_value
        )
        if owner == owners.default or (
            "frozen" in subconfig.properties
            and (
                "force_default_on_freeze" in subconfig.properties
                or self.check_force_to_metaconfig(subconfig)
            )
        ):
            # the value is a default value
            # get it
            value = self.get_default_value(subconfig)
        value, has_calculation = get_calculated_value(
            subconfig,
            value,
        )
        return value, has_calculation

    def get_default_value(
        self,
        subconfig: "SubConfig",
    ) -> Any:
        """get default value:
        - get parents config value or
        - get calculated value or
        - get default value
        """
        msubconfig = self._get_modified_parent(subconfig)
        if msubconfig is not None:
            # retrieved value from parent config
            return msubconfig.config_bag.context.get_values().get_cached_value(
                msubconfig
            )

        # now try to get calculated value:
        value, _has_calculation = get_calculated_value(
            subconfig,
            subconfig.option.impl_getdefault(),
        )
        if (
            subconfig.index is not None
            and isinstance(value, (list, tuple))
            and (
                not subconfig.option.impl_is_submulti()
                or not value
                or isinstance(value[0], list)
            )
        ):
            # if index (so slave), must return good value for this index
            # for submulti, first index is a list, assume other data are list too
            index = subconfig.index
            if len(value) > index:
                value = value[index]
            else:
                # no value for this index, retrieve default multi value
                # default_multi is already a list for submulti
                value, _has_calculation = get_calculated_value(
                    subconfig,
                    subconfig.option.impl_getdefault_multi(),
                )
        self.reset_cache_after_calculation(
            subconfig,
            value,
        )
        return value

    # ______________________________________________________________________
    def check_force_to_metaconfig(
        self,
        subconfig: "OptionBag",
    ) -> bool:
        """Check if the value must be retrieve from parent metaconfig or not"""
        # force_metaconfig_on_freeze is set to an option and context is a kernelconfig
        #   => to metaconfig
        # force_metaconfig_on_freeze is set *explicitly* to an option and context is a
        #   kernelmetaconfig => to sub metaconfig
        if "force_metaconfig_on_freeze" in subconfig.properties:
            settings = subconfig.config_bag.context.get_settings()
            if subconfig.config_bag.context.impl_type == "config":
                return True
            # it's a not a config, force to metaconfig only in *explicitly* set
            return "force_metaconfig_on_freeze" in settings.get_stored_properties(
                subconfig.path,
                subconfig.index,
                frozenset(),
            )
        return False

    def reset_cache_after_calculation(
        self,
        subconfig,
        value,
    ):
        """if value is modification after calculation, invalid cache"""
        cache = subconfig.config_bag.context.get_values_cache()
        is_cache, cache_value, _ = cache.getcache(
            subconfig,
            "values",
            expiration=False,
        )
        if not is_cache or cache_value == value:
            # calculation return same value as previous value,
            # so do not invalidate cache
            return
        # calculated value is a new value, so reset cache
        subconfig.config_bag.context.reset_cache(subconfig)
        # and manage force_store_value
        self._set_force_value_identifier(
            subconfig,
            value,
        )

    def isempty(
        self,
        subconfig: "SubConfig",
        value: Any,
        force_allow_empty_list: bool,
    ) -> bool:
        """convenience method to know if an option is empty"""
        index = subconfig.index
        option = subconfig.option
        if index is None and option.impl_is_submulti():
            # index is not set
            isempty = True
            for val in value:
                isempty = self._isempty_multi(val, force_allow_empty_list)
                if isempty:
                    break
        elif (
            index is None or (index is not None and option.impl_is_submulti())
        ) and option.impl_is_multi():
            # it's a single list
            isempty = self._isempty_multi(value, force_allow_empty_list)
        else:
            isempty = value is None or value == ""
        return isempty

    def _isempty_multi(
        self,
        value: Any,
        force_allow_empty_list: bool,
    ) -> bool:
        if not isinstance(value, list):
            return False
        return (
            (not force_allow_empty_list and value == []) or None in value or "" in value
        )

    # ______________________________________________________________________
    # set value
    def set_value(
        self,
        subconfig: "SubConfig",
        value: Any,
    ) -> None:
        """set value to option"""
        owner = self.get_context_owner()
        setting_properties = subconfig.config_bag.properties
        ori_value = value
        if "validator" in setting_properties:
            value, has_calculation = self.setvalue_validation(
                subconfig,
                value,
            )

        elif isinstance(value, list):
            # copy
            value = value.copy()
        self._setvalue(
            subconfig,
            ori_value,
            owner,
        )
        if (
            "force_store_value" in setting_properties
            and subconfig.option.impl_is_leader()
        ):
            leader = subconfig.option.impl_get_leadership()
            parent = subconfig.parent
            parent._length = len(value)
            leader.follower_force_store_value(
                value,
                parent,
                owners.forced,
            )
        validator = (
            "validator" in setting_properties
            and "demoting_error_warning" not in setting_properties
        )
        if validator and not has_calculation:
            cache = subconfig.config_bag.context.get_values_cache()
            cache.setcache(
                subconfig,
                value,
                validated=validator,
            )
        elif "validator" in setting_properties and has_calculation:
            cache = subconfig.config_bag.context.get_values_cache()
            cache.delcache(subconfig.path)

    def setvalue_validation(
        self,
        subconfig: "SubConfig",
        value: Any,
    ):
        """validate value before set value"""
        settings = subconfig.config_bag.context.get_settings()
        # First validate properties with this value
        opt = subconfig.option
        settings.validate_frozen(subconfig)
        val, has_calculation = get_calculated_value(
            subconfig,
            value,
        )
        settings.validate_mandatory(
            subconfig,
            val,
        )
        # Value must be valid for option
        opt.impl_validate(
            subconfig,
            val,
            check_error=True,
        )
        if "warnings" in subconfig.config_bag.properties:
            # No error found so emit warnings
            opt.impl_validate(
                subconfig,
                val,
                check_error=False,
            )
        return val, has_calculation

    def _setvalue(
        self,
        subconfig: "SubConfig",
        value: Any,
        owner: str,
    ) -> None:
        subconfig.config_bag.context.reset_cache(subconfig)
        self.set_storage_value(
            subconfig.path,
            subconfig.index,
            value,
            owner,
        )
        self._set_force_value_identifier(
            subconfig,
            value,
        )

    def set_storage_value(
        self,
        path,
        index,
        value,
        owner,
    ):
        """set a value"""
        self._values.setdefault(path, {})[index] = [value, owner]

    def _set_force_value_identifier(
        self,
        subconfig: "SubConfig",
        identifier_values,
    ) -> None:
        """force store value for an option for identifiers"""
        # pylint: disable=too-many-locals
        if "force_store_value" not in subconfig.config_bag.properties:
            return

        config_bag = subconfig.config_bag
        context = config_bag.context
        for (
            woption
        ) in (
            subconfig.option._get_identifiers_dependencies()
        ):  # pylint: disable=protected-access
            options = subconfig.get_common_child(
                woption(),
                true_path=subconfig.path,
                validate_properties=False,
            )
            if not isinstance(options, list):
                options = [options]
            for option in options:
                parent = option.parent
                for identifier in identifier_values:
                    name = option.option.impl_getname(identifier)
                    opt_subconfig = parent.get_child(
                        option.option,
                        None,
                        False,
                        identifier=identifier,
                        name=name,
                    )

                    for walk_subconfig in context.walk(
                        opt_subconfig,
                        no_value=True,
                        validate_properties=False,
                    ):
                        if "force_store_value" not in walk_subconfig.properties:
                            continue
                        default_value = [
                            self.get_value(walk_subconfig)[0],
                            owners.forced,
                        ]
                        self._values.setdefault(walk_subconfig.path, {})[
                            walk_subconfig.index
                        ] = default_value

    def _get_modified_parent(
        self,
        subconfig: "SubConfig",
    ) -> Optional["SubConfig"]:
        """Search in differents parents a Config with a modified value
        If not found, return None
        For follower option, return the Config where leader is modified
        """

        def build_option_bag(subconfig, parent):
            doption_bag = subconfig.copy()
            config_bag = subconfig.config_bag.copy()
            config_bag.context = parent
            config_bag.unrestraint()
            doption_bag.config_bag = config_bag
            return doption_bag

        for parent in subconfig.config_bag.context.get_parents():
            doption_bag = build_option_bag(subconfig, parent)
            if "force_metaconfig_on_freeze" in subconfig.properties:
                # remove force_metaconfig_on_freeze only if option in metaconfig
                # hasn't force_metaconfig_on_freeze properties
                ori_properties = doption_bag.properties
                settings = doption_bag.config_bag.context.get_settings()
                doption_bag.properties = settings.getproperties(doption_bag)
                if not self.check_force_to_metaconfig(doption_bag):
                    doption_bag.properties = ori_properties - {
                        "force_metaconfig_on_freeze"
                    }
                else:
                    doption_bag.properties = ori_properties
            parent_owner = parent.get_values().getowner(
                doption_bag,
                parent,
                only_default=True,
            )
            if parent_owner != owners.default:
                return doption_bag

        return None

    # ______________________________________________________________________
    # owner

    def is_default_owner(
        self,
        subconfig: "SubConfig",
        *,
        validate_meta: bool = True,
    ) -> bool:
        """is default owner for an option"""
        return (
            self.getowner(
                subconfig,
                validate_meta=validate_meta,
                only_default=True,
            )
            == owners.default
        )

    def hasvalue(
        self,
        path,
        *,
        index=None,
    ):
        """if path has a value
        return: boolean
        """
        has_path = path in self._values
        if index is None:
            return has_path
        if has_path:
            return index in self._values[path]
        return False

    def getowner(
        self,
        subconfig: "SubConfig",
        *,
        validate_meta=True,
        only_default=False,
    ):
        """
        retrieves the option's owner

        :param opt: the `option.Option` object
        :param force_permissive: behaves as if the permissive property
                                 was present
        :returns: a `setting.owners.Owner` object
        """
        #        context = subconfig.config_bag.context
        #        settings = context.get_settings()
        #        settings.validate_properties(subconfig)
        if (
            "frozen" in subconfig.properties
            and "force_default_on_freeze" in subconfig.properties
        ):
            return owners.default
        if only_default:
            if self.hasvalue(
                subconfig.path,
                index=subconfig.index,
            ):
                owner = "not_default"
            else:
                owner = owners.default
        else:
            owner = self._values.get(subconfig.path, {}).get(
                subconfig.index,
                [undefined, owners.default],
            )[1]
        if validate_meta is not False and (
            owner is owners.default
            or "frozen" in subconfig.properties
            and "force_metaconfig_on_freeze" in subconfig.properties
        ):
            msubconfig = self._get_modified_parent(subconfig)
            if msubconfig is not None:
                values = msubconfig.config_bag.context.get_values()
                owner = values.getowner(
                    msubconfig,
                    parent,
                    only_default=only_default,
                )
            elif "force_metaconfig_on_freeze" in subconfig.properties:
                return owners.default
        return owner

    def set_owner(
        self,
        subconfig,
        owner,
    ):
        """
        sets a owner to an option

        :param subconfig: the `OptionBag` object
        :param owner: a valid owner, that is a `setting.owners.Owner` object
        """
        if owner in forbidden_owners:
            raise ValueError(_('set owner "{0}" is forbidden').format(str(owner)))

        if not self.hasvalue(
            subconfig.path,
            index=subconfig.index,
        ):
            raise ConfigError(
                _(
                    '"{0}" is a default value, so we cannot change owner to "{1}"'
                ).format(subconfig.path, owner)
            )
        subconfig.config_bag.context.get_settings().validate_frozen(subconfig)
        self._values[subconfig.path][subconfig.index][1] = owner

    # ______________________________________________________________________
    # reset

    def reset(
        self,
        subconfig: "SubConfig",
        *,
        validate: bool = True,
    ) -> None:
        """reset value for an option"""
        config_bag = subconfig.config_bag
        hasvalue = self.hasvalue(subconfig.path)
        context = config_bag.context
        setting_properties = config_bag.properties
        if validate:
            if hasvalue and "validator" in setting_properties:
                fake_context = context.gen_fake_context()
                fake_config_bag = config_bag.copy()
                fake_config_bag.remove_validation()
                fake_config_bag.context = fake_context
                fake_subconfig = fake_context.get_sub_config(
                    fake_config_bag,
                    subconfig.path,
                    subconfig.index,
                    validate_properties=False,
                )
                fake_values = fake_context.get_values()
                fake_values.reset(fake_subconfig)
                fake_subconfig.config_bag.properties = setting_properties
                value = fake_values.get_default_value(fake_subconfig)
                fake_values.setvalue_validation(
                    fake_subconfig,
                    value,
                )
        #        if hasvalue:
        opt = subconfig.option
        if opt.impl_is_leader():
            opt.impl_get_leadership().reset(subconfig.parent)
        if (
            "force_store_value" in setting_properties
            and "force_store_value" in subconfig.properties
        ):
            value = self.get_default_value(subconfig)

            self._setvalue(
                subconfig,
                value,
                owners.forced,
            )
        else:
            value = None
            if subconfig.path in self._values:
                del self._values[subconfig.path]
            if (
                "force_store_value" in setting_properties
                and subconfig.option.impl_is_leader()
            ):
                if value is None:
                    value = self.get_default_value(subconfig)
                leader = subconfig.option.impl_get_leadership()
                leader.follower_force_store_value(
                    value,
                    subconfig.parent,
                    owners.forced,
                )
        context.reset_cache(subconfig)

    # ______________________________________________________________________
    # Follower

    def get_max_length(self, path: str) -> int:
        """get max index for a follower and determine the length of the follower"""
        values = self._values.get(path, {})
        if values:
            return max(values) + 1
        return 0

    def reset_follower(
        self,
        subconfig: "SubConfig",
    ) -> None:
        """reset value for a follower"""
        if not self.hasvalue(
            subconfig.path,
            index=subconfig.index,
        ):
            return
        config_bag = subconfig.config_bag
        context = config_bag.context
        setting_properties = config_bag.properties
        if "validator" in setting_properties:
            fake_context = context.gen_fake_context()
            fake_config_bag = config_bag.copy()
            fake_config_bag.remove_validation()
            fake_config_bag.context = fake_context
            fake_subconfig = fake_context.get_sub_config(
                fake_config_bag,
                subconfig.path,
                subconfig.index,
                validate_properties=False,
            )
            fake_values = fake_context.get_values()
            fake_values.reset_follower(fake_subconfig)
            fake_subconfig.config_bag.properties = setting_properties
            value = fake_values.get_default_value(fake_subconfig)
            fake_values.setvalue_validation(
                fake_subconfig,
                value,
            )
        if (
            "force_store_value" in setting_properties
            and "force_store_value" in subconfig.properties
        ):
            value = self.get_default_value(
                subconfig,
            )

            self._setvalue(
                subconfig,
                value,
                owners.forced,
            )
        else:
            self.resetvalue_index(subconfig)
            context.reset_cache(subconfig)

    def resetvalue_index(
        self,
        subconfig: "SubConfig",
    ) -> None:
        """reset a value for a follower at an index"""
        if (
            subconfig.path in self._values
            and subconfig.index in self._values[subconfig.path]
        ):
            del self._values[subconfig.path][subconfig.index]

    def reduce_index(
        self,
        subconfig: "SubConfig",
    ) -> None:
        """reduce follower's value from a specified index"""
        self.resetvalue_index(subconfig)
        for index in range(subconfig.index + 1, self.get_max_length(subconfig.path)):
            if self.hasvalue(
                subconfig.path,
                index=index,
            ):
                self._values[subconfig.path][index - 1] = self._values[
                    subconfig.path
                ].pop(index)

    def reset_leadership(
        self,
        subconfig: "SubConfig",
        index: int,
    ) -> None:
        """reset leadership from an index"""
        current_value = self.get_cached_value(subconfig)
        length = len(current_value)
        if index >= length:
            raise IndexError(
                _(
                    "index {index} is greater than the length {length} "
                    "for option {subconfig.option.impl_get_display_name(with_quote=True)}"
                )
            )
        current_value.pop(index)
        leadership_subconfig = subconfig.parent
        leadership_subconfig.option.pop(
            subconfig,
            index,
        )
        self.set_value(
            subconfig,
            current_value,
        )

    # ______________________________________________________________________
    # information

    def set_information(
        self,
        subconfig,
        key,
        value,
    ):
        """updates the information's attribute

        :param key: information's key (ex: "help", "doc"
        :param value: information's value (ex: "the help string")
        """
        if subconfig is None:
            path = None
        else:
            path = subconfig.path
        self._informations.setdefault(path, {})[key] = value
        if path is None:
            return
        config_bag = subconfig.config_bag
        context = config_bag.context
        for key, options in subconfig.option.get_dependencies_information().items():
            if key is None:
                continue
            for woption in options:
                if woption is None:
                    continue
                option = woption()
                if option.issubdyn():
                    option_subconfigs = subconfig.get_common_child(
                        option,
                        validate_properties=False,
                    )
                    if not isinstance(option_subconfigs, list):
                        option_subconfigs = [option_subconfigs]
                else:
                    option_subconfigs = [
                        context.get_sub_config(
                            config_bag,
                            option.impl_getpath(),
                            None,
                            validate_properties=False,
                        )
                    ]
                for option_subconfig in option_subconfigs:
                    context.reset_cache(option_subconfig)

    def get_information(
        self,
        subconfig,
        name,
        default,
    ):
        """retrieves one information's item

        :param name: the item string (ex: "help")
        """
        if subconfig.option.impl_is_symlinkoption():
            option = subconfig.option.impl_getopt()
            path = option.impl_getpath()
        else:
            option = subconfig.option
            path = subconfig.path
        try:
            return self._informations[path][name]
        except KeyError as err:
            pass
        if option is not None:
            return option._get_information(
                subconfig,
                name,
                default,
            )
        return subconfig.config_bag.context.get_description()._get_information(
            subconfig,
            name,
            default,
        )

    def del_information(
        self,
        key: Any,
        raises: bool = True,
        path: str = None,
    ):
        """delete information for a specified key"""
        if path in self._informations and key in self._informations[path]:
            del self._informations[path][key]
        elif raises:
            raise ValueError(_('information\'s item not found "{}"').format(key))

    def list_information(
        self,
        path: str = None,
    ) -> List[str]:
        """list all informations keys for a specified path"""
        return list(self._informations.get(path, {}).keys())

    # ____________________________________________________________
    # default owner methods
    def set_context_owner(self, owner: str) -> None:
        """set the context owner"""
        if owner in forbidden_owners:
            raise ValueError(_('set owner "{0}" is forbidden').format(str(owner)))
        self._values[None][None][1] = owner

    def get_context_owner(self) -> str:
        """get the context owner"""
        return self._values[None][None][1]
