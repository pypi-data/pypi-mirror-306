# -*- coding: utf-8 -*-
# Copyright (C) 2017-2024 Team tiramisu (see AUTHORS for all contributors)
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
from inspect import getdoc
from typing import List, Set, Any, Optional, Callable, Dict
from warnings import catch_warnings, simplefilter
from functools import wraps
from copy import deepcopy


from .error import (
    ConfigError,
    LeadershipError,
    ValueErrorWarning,
    PropertiesOptionError,
)
from .i18n import _
from .setting import (
    ConfigBag,
    owners,
    groups,
    undefined,
    FORBIDDEN_SET_PROPERTIES,
    SPECIAL_PROPERTIES,
    DEFAULT_PROPERTIES,
)
from .config import (
    KernelConfig,
    KernelGroupConfig,
    KernelMetaConfig,
    KernelMixConfig,
    SubConfig,
)
from .option import RegexpOption, OptionDescription, ChoiceOption, Leadership
from .todict import TiramisuDict
from .autolib import Calculation


TIRAMISU_VERSION = 5


class TiramisuHelp:
    _tmpl_help = "    {0}\t{1}"

    def help(self, _display: bool = True) -> List[str]:
        def display(doc=""):
            if _display:  # pragma: no cover
                print(doc)

        all_modules = dir(self.__class__)
        modules = []
        max_len = 0
        force = False
        for module_name in all_modules:
            if module_name in ["forcepermissive", "unrestraint", "nowarnings"]:
                force = True
                max_len = max(max_len, len("forcepermissive"))
            elif module_name != "help" and not module_name.startswith("_"):
                modules.append(module_name)
                max_len = max(max_len, len(module_name))
        modules.sort()

        display(_(getdoc(self)))
        display()
        if force:
            display(_("Settings:"))
            display(
                self._tmpl_help.format(
                    "forcepermissive",
                    _("Access to option without verifying permissive " "properties"),
                ).expandtabs(max_len + 10)
            )
            display(
                self._tmpl_help.format(
                    "unrestraint", _("Access to option without property restriction")
                ).expandtabs(max_len + 10)
            )
            display(
                self._tmpl_help.format(
                    "nowarnings", _("Do not warnings during validation")
                ).expandtabs(max_len + 10)
            )
            display()
        display(_("Commands:"))
        for module_name in modules:
            module = getattr(self, module_name)
            doc = _(getdoc(module))
            display(self._tmpl_help.format(module_name, doc).expandtabs(max_len + 10))
        display()

    def __dir__(self):
        if "_registers" in super().__dir__():
            return list(self._registers.keys())
        return super().__dir__()

    def __getattr__(self, subfunc):
        raise ConfigError(
            _("please specify a valid sub function ({0}.{1})").format(
                self.__class__.__name__, subfunc
            )
        )


class CommonTiramisu(TiramisuHelp):
    _validate_properties = True
    _allow_dynoption = False

    def _set_subconfig(self) -> None:
        if not self._subconfig:
            self._subconfig = self._config_bag.context.get_sub_config(
                self._config_bag,
                self._path,
                self._index,
                validate_properties=False,
                allow_dynoption=self._allow_dynoption,
            )


def option_type(typ):
    if not isinstance(typ, list):
        types = [typ]
    else:
        types = typ

    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            self = args[0]
            config_bag = self._config_bag
            if self._config_bag.context.impl_type == "group" and "group" in types:
                options_bag = [
                    OptionBag(
                        None,
                        None,
                        self._config_bag,
                        path=self._path,
                    )
                ]
                kwargs["is_group"] = True
                return func(self, options_bag, *args[1:], **kwargs)
            self._set_subconfig()
            option = self._subconfig.option
            error_type = None
            if "dynamic" in types:
                if not self._subconfig.is_dynamic:
                    error_type = "only available for dynamic option"
            elif option.impl_is_optiondescription():
                if "optiondescription" not in types:
                    if option.impl_is_leadership():
                        if "leadership" not in types:
                            error_type = "not available for a Leadership"
                    else:
                        error_type = "not available for an OptionDescription"
            elif option.impl_is_symlinkoption():
                if "symlink" not in types:
                    error_type = "this function is not available for a SymLinkOption"
            elif "option" not in types:
                if "choice" in types:
                    if not isinstance(option, ChoiceOption):
                        error_type = "only available for ChoiceOption"
                elif option.impl_is_leader():
                    if "leader" not in types:
                        error_type = "not available for a Leader"
                elif option.impl_is_follower():
                    if "follower" not in types:
                        error_type = "not available for a Follower"
                else:
                    error_type = "not available for an Option"
            if not error_type:
                if (
                    not option.impl_is_optiondescription()
                    and not option.impl_is_symlinkoption()
                    and option.impl_is_follower()
                ):
                    # default is "without_index"
                    if (
                        "with_index" not in types
                        and "with_or_without_index" not in types
                        and self._index is not None
                    ):
                        msg = _("please do not specify index ({0}.{1})").format(
                            self.__class__.__name__, func.__name__
                        )
                        raise ConfigError(msg)
                    if self._index is None and "with_index" in types:
                        msg = _(
                            "please specify index with a follower option ({0}.{1})"
                        ).format(self.__class__.__name__, func.__name__)
                        raise ConfigError(msg)
                if self._validate_properties and "dont_validate_property" not in types:
                    settings = self._config_bag.context.get_settings()
                    parent = self._subconfig.parent
                    if parent and parent.transitive_properties:
                        while parent:
                            if not parent.parent.transitive_properties:
                                settings.validate_properties(
                                    parent,
                                    need_help=True,
                                )
                                break
                            parent = parent.parent
                    settings.validate_properties(
                        self._subconfig,
                        need_help=True,
                    )
                return func(self, *args[1:], **kwargs)
            msg = _("please specify a valid sub function ({0}.{1}): {2}").format(
                self.__class__.__name__, func.__name__, error_type
            )
            raise ConfigError(msg)

        wrapped.func = func
        return wrapped

    return wrapper


class CommonTiramisuOption(CommonTiramisu):
    _validate_properties = False

    def __init__(
        self,
        path: str,
        index: Optional[int],
        config_bag: ConfigBag,
    ) -> None:
        self._path = path
        self._index = index
        self._config_bag = config_bag
        self._subconfig = None
        self._set_subconfig()


class _TiramisuOptionWalk:
    def _list(
        self,
        subconfig: SubConfig,
        validate_properties: bool,
        *,
        uncalculated: bool = False,
    ):
        options = []
        for sub_subconfig in subconfig.get_children(
            validate_properties, uncalculated=uncalculated
        ):
            options.append(
                TiramisuOption(
                    sub_subconfig.path,
                    sub_subconfig.index,
                    self._config_bag,
                    subconfig=sub_subconfig,
                )
            )
        return options


class _TiramisuOptionOptionDescription:
    """Manage option"""

    _validate_properties = False

    @option_type(["optiondescription", "option", "with_or_without_index", "symlink"])
    def get(self):
        """Get Tiramisu option"""
        return self._subconfig.option

    @option_type(["optiondescription", "option", "with_or_without_index", "symlink"])
    def isoptiondescription(self):
        """Test if option is an optiondescription"""
        return self._subconfig.option.impl_is_optiondescription()

    @option_type(["optiondescription"])
    def isleadership(self):
        """Test if option is a leader or a follower"""
        return self._subconfig.option.impl_is_leadership()

    @option_type(["optiondescription", "option", "with_or_without_index", "symlink"])
    def description(
        self,
        uncalculated: bool = False,
    ):
        """Get option description"""
        if not uncalculated:
            return self._subconfig.option.impl_get_display_name(self._subconfig)
        return self._subconfig.option._get_information(
            self._subconfig,
            "doc",
            None,
        )

    @option_type(["optiondescription", "option", "symlink", "with_or_without_index"])
    def name(
        self,
        *,
        uncalculated: bool = False,
    ) -> str:
        """Get option name"""
        if uncalculated:
            return self._subconfig.option.impl_getname()
        return self._subconfig.true_path.rsplit(".", 1)[-1]

    @option_type(["optiondescription", "option", "with_or_without_index", "symlink"])
    def path(
        self,
        *,
        uncalculated: bool = False,
    ) -> str:
        """Get option path"""
        if uncalculated:
            return self._subconfig.option.impl_getpath()
        return self._subconfig.true_path

    @option_type(["optiondescription", "option", "symlink", "with_or_without_index"])
    def has_dependency(
        self,
        self_is_dep=True,
    ) -> bool:
        """Test if option has dependency"""
        return self._subconfig.option.impl_has_dependency(self_is_dep)

    @option_type(["optiondescription", "option", "symlink", "with_or_without_index"])
    def dependencies(self):
        """Get dependencies from this option"""
        options = []
        for option in self._subconfig.option.get_dependencies(self._config_bag.context):
            options.append(
                TiramisuOption(
                    option().impl_getpath(),
                    None,
                    self._config_bag,
                    allow_dynoption=True,
                )
            )
        return options

    @option_type(["option", "optiondescription", "symlink", "with_or_without_index"])
    def type(self):
        """Get de option type"""
        option = self._subconfig.option
        if option.impl_is_optiondescription():
            return "optiondescription"
        return option.get_type()

    @option_type(["option", "symlink", "with_or_without_index"])
    def extra(self, extra):
        """Get de option extra"""
        return self._subconfig.option.impl_get_extra(extra)

    @option_type(["option", "optiondescription", "symlink", "with_or_without_index"])
    def isdynamic(self, *, only_self: bool = False):
        """Test if option is a dynamic optiondescription"""
        if not only_self:
            return self._subconfig.is_dynamic
        return (
            self._subconfig.option.impl_is_optiondescription()
            and self._subconfig.option.impl_is_dynoptiondescription()
        )

    @option_type(["option", "leadership"])
    def leader(self):
        """Get the leader option for a leadership or a follower option"""
        option = self._subconfig.option
        if isinstance(option, Leadership):
            leadership = self._subconfig
        else:
            leadership = self._subconfig.parent
        leader_subconfig = leadership.get_child(
            leadership.option.get_leader(),
            None,
            False,
        )
        return TiramisuOption(
            leader_subconfig.path,
            None,
            self._config_bag,
            subconfig=leader_subconfig,
        )

    @option_type(["leadership"])
    def followers(self):
        """Get the followers option for a leadership"""
        option = self._subconfig.option
        if isinstance(option, Leadership):
            leadership = self._subconfig
        else:
            leadership = self._subconfig.parent
        ret = []
        for follower in leadership.option.get_followers():
            follower_subconfig = leadership.get_child(
                follower,
                None,
                False,
            )
            ret.append(
                TiramisuOption(
                    follower_subconfig.path,
                    None,
                    self._config_bag,
                    subconfig=follower_subconfig,
                )
            )
        return ret

    @option_type(["dynamic", "with_or_without_index"])
    def identifiers(
        self,
        only_self: bool = False,
        uncalculated: bool = False,
    ):
        """Get identifiers for dynamic option"""
        if not only_self:
            return self._subconfig.identifiers
        if (
            not self._subconfig.option.impl_is_optiondescription()
            or not self._subconfig.option.impl_is_dynoptiondescription()
        ):
            raise ConfigError(
                _(
                    "the option {0} is not a dynamic option, cannot get identifiers with only_self parameter to True"
                ).format(self._subconfig.path)
            )
        return self._subconfig.option.get_identifiers(
            self._subconfig.parent,
            uncalculated=uncalculated,
        )


class _TiramisuOptionOption(_TiramisuOptionOptionDescription):
    """Manage option"""

    @option_type(["option", "symlink", "with_or_without_index"])
    def ismulti(self):
        """Test if option could have multi value"""
        return self._subconfig.option.impl_is_multi()

    @option_type(["option", "symlink", "with_or_without_index"])
    def issubmulti(self):
        """Test if option could have submulti value"""
        return self._subconfig.option.impl_is_submulti()

    @option_type(["option", "with_or_without_index", "symlink"])
    def isleader(self):
        """Test if option is a leader"""
        return self._subconfig.option.impl_is_leader()

    @option_type(["option", "with_or_without_index", "symlink"])
    def isfollower(self):
        """Test if option is a follower"""
        return self._subconfig.option.impl_is_follower()

    @option_type(["option", "symlink", "with_or_without_index"])
    def issymlinkoption(self) -> bool:
        """Test if option is a symlink option"""
        return self._subconfig.option.impl_is_symlinkoption()

    @option_type(["option", "with_or_without_index"])
    def pattern(self) -> str:
        """Get the option pattern"""
        option = self._subconfig.option
        type = option.get_type()
        if isinstance(option, RegexpOption):
            return option._regexp.pattern
        if type == "integer":
            # FIXME negative too!
            return r"^[0-9]+$"
        if type == "domain name":
            return option.impl_get_extra("_domain_re").pattern
        if type in ["ip", "network", "netmask"]:
            # FIXME only from 0.0.0.0 to 255.255.255.255
            return r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"

    @option_type(["option", "with_or_without_index", "symlink"])
    def index(self):
        """Get index of option"""
        return self._subconfig.index

    @option_type(["symlink", "optiondescription"])
    def option(self, *args, **kwargs):
        """For OptionDescription get sub option, for symlinkoption get the linked option"""
        if self._subconfig.option.impl_is_optiondescription():
            return self._option_description(*args, **kwargs)
        return self._option_symlink(*args, **kwargs)

    def _option_description(
        self,
        path,
        index=None,
    ):
        sub_path = self._path + "." + path
        return TiramisuOption(
            sub_path,
            index,
            self._config_bag,
        )

    def _option_symlink(self):
        subconfig = self._subconfig.config_bag.context._get(
            self._subconfig,
            need_help=True,
            validate_properties=self._validate_properties,
        )
        if isinstance(subconfig, list):
            raise ConfigError(
                _("cannot get option from a follower symlink without index")
            )
        subconfig.true_path = subconfig.path
        return TiramisuOption(
            subconfig.path,
            subconfig.index,
            self._config_bag,
            subconfig=subconfig,
        )


class TiramisuOptionOwner(CommonTiramisuOption):
    """Manage option's owner"""

    _validate_properties = True

    @option_type(["symlink", "option", "with_index"])
    def get(self):
        """Get owner for a specified option"""
        return self._config_bag.context.get_owner(self._subconfig)

    @option_type(["symlink", "option", "with_index"])
    def isdefault(self):
        """Is option has defaut value"""
        return self._config_bag.context.get_owner(self._subconfig) == owners.default

    @option_type(["option", "with_index"])
    def set(
        self,
        owner: str,
    ) -> None:
        """Get owner for a specified option"""
        try:
            obj_owner = getattr(owners, owner)
        except AttributeError:
            owners.addowner(owner)
            obj_owner = getattr(owners, owner)
        self._config_bag.context.get_values().set_owner(
            self._subconfig,
            obj_owner,
        )


class TiramisuOptionProperty(CommonTiramisuOption):
    """Manage option's property"""

    _validate_properties = False

    @option_type(["option", "optiondescription", "with_index", "symlink"])
    def get(
        self,
        *,
        only_raises: bool = False,
        apply_requires: bool = True,
        uncalculated: bool = False,
    ):
        """Get properties for an option"""
        settings = self._config_bag.context.get_settings()
        if not only_raises:
            return settings.getproperties(
                self._subconfig,
                uncalculated=uncalculated,
                apply_requires=apply_requires,
            )
        return settings.calc_raises_properties(
            self._subconfig,
            uncalculated=uncalculated,
            apply_requires=apply_requires,
        )

    @option_type(["option", "optiondescription", "with_or_without_index"])
    def add(self, prop):
        """Add new property for an option"""
        if prop in FORBIDDEN_SET_PROPERTIES:
            raise ConfigError(
                _('cannot add this property: "{0}"').format(" ".join(prop))
            )
        settings = self._config_bag.context.get_settings()
        props = settings.get_personalize_properties(
            self._path,
            self._index,
        )
        settings.setproperties(
            self._subconfig,
            props | {prop},
        )

    @option_type(["option", "optiondescription", "with_or_without_index"])
    def remove(
        self,
        prop,
    ):
        """Remove new property for an option"""
        settings = self._config_bag.context.get_settings()
        props = settings.get_personalize_properties(
            self._path,
            self._index,
        )

        if prop not in props:
            if self._index is None:
                if prop in settings.getproperties(self._subconfig):
                    msg = _(
                        'cannot remove option\'s property "{0}", use permissive instead in option "{1}"'
                    ).format(prop, self._path)
                else:
                    msg = _('cannot find "{0}" in option "{1}"').format(
                        prop, self._path
                    )
            else:
                if prop in settings.getproperties(self._subconfig):
                    msg = _(
                        'cannot remove option\'s property "{0}", use permissive instead in option "{1}" at index "{2}"'
                    ).format(prop, self._path, self._index)
                else:
                    msg = _('cannot find "{0}" in option "{1}" at index "{2}"').format(
                        prop, self._path, self._index
                    )
            raise ConfigError(msg)
        settings.setproperties(
            self._subconfig,
            props - {prop},
        )

    @option_type(["option", "optiondescription", "with_or_without_index"])
    def reset(self):
        """Reset all personalised properties"""
        self._config_bag.context.get_settings().reset(self._subconfig)


class TiramisuOptionPermissive(CommonTiramisuOption):
    """Manage option's permissive"""

    _validate_properties = False

    @option_type(["option", "optiondescription", "symlink", "with_or_without_index"])
    def get(self):
        """Get permissives value"""
        return self._config_bag.context.get_settings().getpermissives(self._subconfig)

    @option_type(["option", "optiondescription", "with_or_without_index"])
    def add(
        self,
        permissive,
    ):
        """Set permissives value"""
        permissives = self._config_bag.context.get_settings().getpermissives(
            self._subconfig
        )
        self._config_bag.context.get_settings().setpermissives(
            self._subconfig,
            frozenset(permissives | {permissive}),
        )

    @option_type(["option", "optiondescription", "with_or_without_index"])
    def remove(self, permissive):
        """Remove a config property"""
        permissives = set(self.get())
        if permissive not in permissives:
            msg = _('cannot find "{0}"').format(permissive)
            raise ConfigError(msg)
        self._config_bag.context.get_settings().setpermissives(
            self._subconfig,
            frozenset(permissives - {permissive}),
        )

    @option_type(["option", "optiondescription", "with_or_without_index"])
    def reset(self):
        """Reset all personalised permissive"""
        self._config_bag.context.get_settings().reset_permissives(self._subconfig)


class TiramisuOptionInformation(CommonTiramisuOption):
    """Manage option's informations"""

    _validate_properties = False
    _allow_dynoption = True

    @option_type(["option", "optiondescription", "with_or_without_index", "symlink"])
    def get(
        self,
        name: str,
        default=undefined,
    ) -> Any:
        """Get information"""
        return self._config_bag.context.get_values().get_information(
            self._subconfig,
            name,
            default,
        )

    @option_type(["option", "optiondescription"])
    def set(self, key: str, value: Any) -> None:
        """Set information"""
        self._config_bag.context.get_values().set_information(
            self._subconfig,
            key,
            value,
        )

    @option_type(["option", "optiondescription"])
    def remove(
        self,
        key: str,
    ) -> None:
        """Remove information"""
        self._config_bag.context.get_values().del_information(
            key,
            path=self._path,
        )

    @option_type(["option", "optiondescription", "with_or_without_index", "symlink"])
    def list(self) -> list:
        """List information's keys"""
        lst1 = set(self._subconfig.option._list_information())
        lst2 = set(self._config_bag.context.get_values().list_information(self._path))
        return lst1 | lst2


class _TiramisuODGet:
    def _od_get(
        self,
        root_subconfig: SubConfig,
    ) -> dict:
        """exports the whole config into a `dict`
        :returns: dict of Option's name (or path) and values
        """

        def parse_od_get(values):
            ret_ = {}
            for subconfig, value in values.items():
                option = TiramisuOption(
                    subconfig.path,
                    subconfig.index,
                    self._config_bag,
                    subconfig=subconfig,
                )
                if option.isoptiondescription():
                    value = parse_od_get(value)
                ret_[option] = value
            return ret_

        return parse_od_get(self._config_bag.context.walk(root_subconfig))


class TiramisuOptionValue(CommonTiramisuOption, _TiramisuODGet):
    """Manage option's value"""

    _validate_properties = True

    @option_type(["option", "symlink", "with_index", "optiondescription"])
    def get(
        self,
        *,
        uncalculated: bool = False,
    ):
        """Get value for an option or option and sub option with values with optiondescription"""
        if self._subconfig.option.impl_is_optiondescription():
            if uncalculated:
                raise ConfigError("uncalculated is not allowed for optiondescription")
            return self._od_get(self._subconfig)
        if uncalculated:
            value = self._subconfig.option.impl_getdefault()
            index = self._subconfig.index
            if not isinstance(value, list) or index is None:
                return value
            if index >= len(value):
                return self._subconfig.option.impl_getdefault_multi()
            return value[index]
        return self._get(uncalculated)

    def _get(
        self,
        need_help: bool = True,
    ):
        """Get option's value"""
        return self._config_bag.context.get_value(self._subconfig, need_help)

    @option_type(["option", "with_index"])
    def set(
        self,
        value,
    ):
        """Change option's value"""
        option = self._subconfig.option
        if (
            not isinstance(value, Calculation)
            and option.impl_is_leader()
            and len(value) < self._subconfig.parent.get_length_leadership()
        ):
            raise LeadershipError(
                _("cannot reduce length of the leader {}" "").format(
                    option.impl_get_display_name(self._subconfig, with_quote=True)
                )
            )
        values = self._config_bag.context.get_values()
        return values.set_value(self._subconfig, value)

    @option_type(["group", "option", "with_index"])
    def reset(
        self,
        is_group: bool = False,
    ) -> None:
        """Reset value for an option"""
        if is_group:
            self._config_bag.context.reset(
                self._subconfig.path,
                self._config_bag,
            )
        else:
            values = self._config_bag.context.get_values()
            if self._subconfig.index is not None:
                values.reset_follower(self._subconfig)
            else:
                values.reset(self._subconfig)

    @option_type(
        ["option", "with_or_without_index", "symlink", "dont_validate_property"]
    )
    def default(
        self,
        uncalculated: bool = False,
    ) -> Any:
        """Get default value (default of option or calculated value)"""
        if uncalculated:
            return self._subconfig.option.impl_getdefault()
        if self._subconfig.option.impl_is_follower() and self._subconfig.index is None:
            msg = _("please specify index with a follower option ({0}.{1})").format(
                self.__class__.__name__, func.__name__
            )
            raise ConfigError(msg)
        if (
            "force_store_value" in self._subconfig.properties
            and "force_store_value" in self._config_bag.properties
        ):
            return self._get(self._subconfig)
        return self._config_bag.context.get_values().get_default_value(self._subconfig)

    @option_type(
        ["option", "with_or_without_index", "symlink", "dont_validate_property"]
    )
    def defaultmulti(self):
        """Get default value when added a value for a multi option (not for optiondescription)"""
        if not self._subconfig.option.impl_is_multi():
            raise ConfigError(_("only multi value has defaultmulti"))
        return self._subconfig.option.impl_getdefault_multi()

    @option_type(["option", "with_index"])
    def valid(self):
        """The if the option's value is valid"""
        try:
            with catch_warnings(record=True) as warns:
                simplefilter("always", ValueErrorWarning)
                self._get(self._subconfig)
                for warn in warns:
                    if isinstance(warn.message, ValueErrorWarning):
                        return False
        except ValueError:
            return False
        return True

    @option_type(["choice", "with_index"])
    def list(
        self,
        *,
        uncalculated: bool = False,
    ):
        """All values available for a ChoiceOption"""
        return self._subconfig.option.impl_get_values(
            self._subconfig,
            uncalculated,
        )

    @option_type("leader")
    def pop(
        self,
        index: int,
    ):
        """Pop a value"""
        self._config_bag.context.get_values().reset_leadership(
            self._subconfig,
            index,
        )

    @option_type(["leader", "follower", "with_or_without_index"])
    def len(self):
        """Length for a leadership"""
        return self._subconfig.parent.get_length_leadership()

    def mandatory(self):
        """Return path of options with mandatory property without any value"""
        subconfig = self._subconfig
        if subconfig.option.impl_is_optiondescription():
            ori_config_bag = self._subconfig.config_bag
            config_bag = ori_config_bag.copy()
            config_bag.properties -= {"mandatory", "empty", "warnings"}
            config_bag.set_permissive()
            self._subconfig.config_bag = config_bag
            options = []
            for subconfig in self._config_bag.context.walk(
                self._subconfig,
                only_mandatory=True,
            ):
                options.append(
                    TiramisuOption(
                        subconfig.path,
                        subconfig.index,
                        ori_config_bag,
                        subconfig=subconfig,
                    )
                )
            self._subconfig.config_bag = ori_config_bag
            return options
        try:
            self._config_bag.context.walk_valid_value(
                self._subconfig, only_mandatory=True
            )
        except PropertiesOptionError as err:
            return err.proptype == ["mandatory"] or err.proptype == ["empty"]
        return False


def _registers(
    _registers: Dict[str, type],
    prefix: str,
):
    for module_name in globals().keys():
        if module_name != prefix and module_name.startswith(prefix):
            module = globals()[module_name]
            func_name = module_name[len(prefix) :].lower()
            _registers[func_name] = module


# __________________________________________________________________________________________________
#


class TiramisuConfig(TiramisuHelp, _TiramisuOptionWalk):
    def __init__(
        self,
        config_bag: ConfigBag,
        orig_config_bags: Optional[List["OptionBag"]],
    ) -> None:
        self._config_bag = config_bag
        self._orig_config_bags = orig_config_bags

    def _return_config(self, config):
        if isinstance(config, KernelConfig):
            return Config(config)
        if isinstance(config, KernelMetaConfig):
            return MetaConfig(config)
        if isinstance(config, KernelMixConfig):
            return MixConfig([], config)
        if isinstance(config, KernelGroupConfig):
            return GroupConfig(config)

    def name(self):
        """get the name"""
        return self._config_bag.context.impl_getname()


class TiramisuOption(
    CommonTiramisu,
    _TiramisuOptionOption,
    TiramisuConfig,
):
    """Manage selected option"""

    _validate_properties = False
    _registers = {}

    def __init__(
        self,
        path: Optional[str] = None,
        index: Optional[int] = None,
        config_bag: Optional[ConfigBag] = None,
        *,
        subconfig: Optional[SubConfig] = None,
        allow_dynoption: bool = False,
    ) -> None:
        self._path = path
        self._index = index
        self._config_bag = config_bag
        self._allow_dynoption = allow_dynoption
        self._subconfig = subconfig
        if not self._registers:
            _registers(self._registers, "TiramisuOption")

    def __repr__(self):
        msg = f'<TiramisuOption path="{self._path}"'
        if self._index is not None:
            msg += f", index={self._index}"
        msg += ">"
        return msg

    def __getattr__(self, subfunc: str) -> Any:
        if subfunc in self._registers:
            return self._registers[subfunc](
                self._path,
                self._index,
                self._config_bag,
            )
        raise ConfigError(
            _("please specify a valid sub function ({0}.{1}) for {2}").format(
                self.__class__.__name__, subfunc, self._path
            )
        )

    #
    def __iter__(self):
        self._set_subconfig()
        for sub_subconfig in self._subconfig.get_children(True):
            yield TiramisuOption(
                sub_subconfig.path,
                sub_subconfig.index,
                self._config_bag,
                subconfig=sub_subconfig,
            )

    @option_type("optiondescription")
    def group_type(self):
        """Get type for an optiondescription (only for optiondescription)"""
        self._set_subconfig()
        return self._subconfig.option.impl_get_group_type()

    @option_type("optiondescription")
    def list(
        self,
        *,
        validate_properties: bool = True,
        uncalculated: bool = False,
    ):
        """List options inside an option description (by default list only option)"""
        self._set_subconfig()
        return self._list(
            self._subconfig,
            validate_properties,
            uncalculated=uncalculated,
        )

    def _load_dict(
        self,
        clearable: str = "all",
        remotable: str = "minimum",
    ):
        config = self._config_bag.context
        self._tiramisu_dict = TiramisuDict(
            self._return_config(config),
            root=self._path,
            clearable=clearable,
            remotable=remotable,
        )

    @option_type("optiondescription")
    def dict(
        self,
        clearable: str = "all",
        remotable: str = "minimum",
        form: List = [],
        force: bool = False,
    ) -> Dict:
        """Convert config and option to tiramisu format"""
        if force or self._tiramisu_dict is None:
            self._load_dict(clearable, remotable)
        return self._tiramisu_dict.todict(form)

    @option_type("optiondescription")
    def updates(
        self,
        body: List,
    ) -> Dict:
        """Updates value with tiramisu format"""
        if self._tiramisu_dict is None:  # pragma: no cover
            self._load_dict()
        return self._tiramisu_dict.set_updates(body)


class TiramisuContextInformation(TiramisuConfig):
    """Manage config informations"""

    def get(
        self,
        name,
        default=undefined,
    ):
        """Get an information"""
        context = self._config_bag.context
        values = context.get_values()
        subconfig = context.get_root(self._config_bag)
        return values.get_information(
            subconfig,
            name,
            default,
        )

    def set(
        self,
        name,
        value,
    ):
        """Set an information"""
        self._config_bag.context.impl_set_information(
            self._config_bag,
            name,
            value,
        )

    def remove(
        self,
        name,
    ):
        """Remove an information"""
        self._config_bag.context.impl_del_information(name)

    def list(self):
        """List information's keys"""
        lst1 = set(self._config_bag.context.get_description()._list_information())
        lst2 = set(self._config_bag.context.impl_list_information())
        return lst1 | lst2

    def exportation(self):
        """Export all informations"""
        return deepcopy(self._config_bag.context.get_values()._informations)

    def importation(self, informations):
        """Import informations"""
        self._config_bag.context.get_values()._informations = deepcopy(informations)


class TiramisuContextValue(TiramisuConfig, _TiramisuODGet):
    """Manage config value"""

    def mandatory(self):
        """Return path of options with mandatory property without any value"""
        config_bag = self._config_bag.copy()
        config_bag.properties -= {"mandatory", "empty", "warnings"}
        config_bag.set_permissive()
        root = self._config_bag.context.get_root(config_bag)
        options = []
        for subconfig in self._config_bag.context.walk(
            root,
            only_mandatory=True,
        ):
            options.append(
                TiramisuOption(
                    subconfig.path,
                    subconfig.index,
                    self._config_bag,
                    subconfig=subconfig,
                )
            )
        return options

    # FIXME should be only for group/meta
    def set(
        self,
        path: str,
        value: Any,
        only_config=undefined,
        force_default=undefined,
        force_default_if_same=undefined,
        force_dont_change_value=undefined,
    ):
        """Set a value in config or children for a path"""
        kwargs = {}
        if only_config is not undefined:
            kwargs["only_config"] = only_config
        if force_default is not undefined:
            kwargs["force_default"] = force_default
        if force_default_if_same is not undefined:
            kwargs["force_default_if_same"] = force_default_if_same
        if force_dont_change_value is not undefined:
            kwargs["force_dont_change_value"] = force_dont_change_value
        option_bag = OptionBag(
            None,
            None,
            self._config_bag,
            path=path,
        )
        return self._config_bag.context.set_value(
            option_bag,
            value,
            **kwargs,
        )

    # FIXME should be only for group/meta
    def reset(self, path: str, only_children: bool = False):
        """Reset value"""
        self._config_bag.context.reset(
            path,
            only_children,
            self._config_bag,
        )

    def get(self):
        """Get option and sub option with values"""
        root = self._config_bag.context.get_root(self._config_bag)
        return self._od_get(root)

    def exportation(
        self,
        with_default_owner: bool = False,
    ):
        """Export all values"""
        exportation = deepcopy(self._config_bag.context.get_values()._values)
        if not with_default_owner:
            del exportation[None]
        return exportation

    def importation(self, values):
        """Import values"""
        cvalues = self._config_bag.context.get_values()
        if None not in values:
            current_owner = cvalues.get_context_owner()
        cvalues._values = deepcopy(values)
        self._config_bag.context.reset_cache(None, None)
        if None not in values:
            cvalues._values[None] = {None: [None, current_owner]}


class TiramisuContextOwner(TiramisuConfig):
    """Global owner"""

    def get(self):
        """Get owner"""
        return self._config_bag.context.get_values().get_context_owner()

    def set(self, owner):
        """Set owner"""
        try:
            obj_owner = getattr(owners, owner)
        except AttributeError:
            owners.addowner(owner)
            obj_owner = getattr(owners, owner)
        values = self._config_bag.context.get_values()
        values.set_context_owner(obj_owner)


class PropertyPermissive:
    def _set_default_permissive(
        self,
        settings,
    ):
        or_properties = settings.rw_append - settings.ro_append - SPECIAL_PROPERTIES
        permissives = frozenset(settings.get_context_permissives() | or_properties)
        settings.set_context_permissives(permissives)

    def _reset_config_properties(
        self,
        settings,
    ):
        properties = settings.get_context_properties()
        permissives = settings.get_context_permissives()
        self._config_bag.properties = properties
        self._config_bag.permissives = permissives
        if self._orig_config_bags:
            for config_bag in self._orig_config_bags:
                config_bag.properties = properties
                config_bag.permissives = permissives


class TiramisuContextProperty(TiramisuConfig, PropertyPermissive):
    """Manage config properties"""

    def read_only(self):
        """Set config to read only mode"""
        if self._config_bag.is_unrestraint:
            raise ConfigError("cannot change context property in unrestraint mode")
        old_props = self._config_bag.properties
        settings = self._config_bag.context.get_settings()
        settings.read_only(self._config_bag)
        self._set_default_permissive(settings)
        self._reset_config_properties(settings)
        if (
            "force_store_value" not in old_props
            and "force_store_value" in self._config_bag.properties
        ):
            self._force_store_value()

    def read_write(self):
        """Set config to read and write mode"""
        if self._config_bag.is_unrestraint:
            raise ConfigError("cannot change context property in unrestraint mode")
        old_props = self._config_bag.properties
        settings = self._config_bag.context.get_settings()
        settings.read_write(self._config_bag)
        self._set_default_permissive(settings)
        self._reset_config_properties(settings)
        if (
            "force_store_value" not in old_props
            and "force_store_value" in self._config_bag.properties
        ):
            self._force_store_value()

    def add(self, prop):
        """Add a config property"""
        props = set(self.get())
        if prop not in props:
            props.add(prop)
            self._set(frozenset(props))

    def remove(self, prop):
        """Remove a config property"""
        props = set(self.get())
        if prop not in props:
            msg = f'cannot find "{prop}"'
            raise ConfigError(msg)
        props.remove(prop)
        self._set(frozenset(props))

    def get(
        self,
        *,
        only_raises: bool = False,
        apply_requires: bool = True,
        uncalculated: bool = False,
    ) -> Set:
        """Get all config properties"""
        if only_raises:
            return set()
        return self._config_bag.properties

    def _set(
        self,
        props,
    ):
        """Personalise config properties"""
        if self._config_bag.is_unrestraint:
            raise ConfigError("cannot change context property in unrestraint mode")
        if "force_store_value" in props:
            force_store_value = "force_store_value" not in self._config_bag.properties
        else:
            force_store_value = False
        settings = self._config_bag.context.get_settings()
        settings.set_context_properties(
            props,
            self._config_bag.context,
        )
        self._reset_config_properties(settings)
        if force_store_value:
            self._force_store_value()

    def reset(self):
        """Remove config properties"""
        if self._config_bag.is_unrestraint:
            raise ConfigError("cannot change context property in unrestraint mode")
        settings = self._config_bag.context.get_settings()
        settings.reset(self._config_bag)
        self._reset_config_properties(settings)

    def exportation(self):
        """Export config properties"""
        settings = self._config_bag.context.get_settings()
        return {
            "properties": deepcopy(settings._properties),
            "ro_append": settings.ro_append.copy(),
            "ro_remove": settings.ro_remove.copy(),
            "rw_append": settings.rw_append.copy(),
            "rw_remove": settings.rw_remove.copy(),
        }

    def importation(self, data):
        """Import config properties"""
        if self._config_bag.is_unrestraint:
            raise ConfigError("cannot change context property in unrestraint mode")
        properties = data["properties"]
        if "force_store_value" in properties.get(None, {}).get(None, []):
            force_store_value = "force_store_value" not in self._config_bag.properties
        else:
            force_store_value = False
        context = self._config_bag.context
        settings = context.get_settings()
        settings._properties = deepcopy(properties)
        settings.ro_append = data["ro_append"].copy()
        settings.ro_remove = data["ro_remove"].copy()
        settings.rw_append = data["rw_append"].copy()
        settings.rw_remove = data["rw_remove"].copy()
        context.reset_cache(None, None)
        self._reset_config_properties(settings)
        if force_store_value:
            self._force_store_value()

    def _force_store_value(self):
        descr = self._config_bag.context.get_description()
        descr.impl_build_force_store_values(self._config_bag)

    def setdefault(
        self, properties: Set[str], type: Optional[str], when: Optional[str] = None
    ) -> None:
        if not isinstance(properties, frozenset):
            raise TypeError(_("properties must be a frozenset"))
        setting = self._config_bag.context.get_settings()
        if when not in ["append", "remove"]:
            raise ValueError(
                _("unknown when {} (must be in append or remove)").format(when)
            )
        if type == "read_only":
            if when == "append":
                setting.ro_append = properties
            else:
                setting.ro_remove = properties
        elif type == "read_write":
            if when == "append":
                setting.rw_append = properties
            else:
                setting.rw_remove = properties
        else:
            raise ValueError(_("unknown type {}").format(type))

    def default(
        self,
        type: Optional[str] = None,
        when: Optional[str] = None,
    ) -> Set[str]:
        setting = self._config_bag.context.get_settings()
        if type is None and when is None:
            return DEFAULT_PROPERTIES
        if type == "current":
            return setting.get_context_properties()
        if when not in ["append", "remove"]:
            raise ValueError(
                _("unknown when {} (must be in append or remove)").format(when)
            )
        if type == "read_only":
            if when == "append":
                return setting.ro_append
            return setting.ro_remove
        if type == "read_write":
            if when == "append":
                return setting.rw_append
            return setting.rw_remove
        raise ValueError(_("unknown type {}").format(type))


class TiramisuContextPermissive(TiramisuConfig, PropertyPermissive):
    """Manage config permissives"""

    def get(self):
        """Get config permissives"""
        return self._get()

    def _get(self):
        return self._config_bag.context.get_settings().get_context_permissives()

    def _set(
        self,
        permissives,
    ):
        """Set config permissives"""
        if self._config_bag.is_unrestraint:
            raise ConfigError("cannot change context permissive in unrestraint mode")
        settings = self._config_bag.context.get_settings()
        settings.set_context_permissives(permissives)
        self._reset_config_properties(settings)

    def exportation(self):
        """Export config permissives"""
        return deepcopy(self._config_bag.context.get_settings()._permissives)

    def importation(self, permissives):
        """Import config permissives"""
        if self._config_bag.is_unrestraint:
            raise ConfigError("cannot change context permissive in unrestraint mode")
        context = self._config_bag.context
        settings = context.get_settings()
        settings._permissives = deepcopy(permissives)
        context.reset_cache(
            None,
            None,
        )
        self._reset_config_properties(settings)

    def reset(self):
        """Remove config permissives"""
        if self._config_bag.is_unrestraint:
            raise ConfigError("cannot change context permissive in unrestraint mode")
        settings = self._config_bag.context.get_settings()
        settings.reset_permissives(self._config_bag)
        self._set_default_permissive(settings)
        self._reset_config_properties(settings)

    def add(self, permissive):
        """Add a config permissive"""
        permissives = set(self._get())
        permissives.add(permissive)
        self._set(frozenset(permissives))

    def remove(self, permissive):
        """Remove a config permissive"""
        permissives = set(self._get())
        if permissive not in permissives:
            msg = f'cannot find "{permissive}"'
            raise ConfigError(msg)
        permissives.remove(permissive)
        self._set(frozenset(permissives))


class TiramisuContextOption(TiramisuConfig, _TiramisuOptionWalk):
    def __init__(self) -> None:
        self._tiramisu_dict = None

    def __iter__(self):
        root = self._config_bag.context.get_root(self._config_bag)
        for sub_subconfig in root.get_children(True):
            yield TiramisuOption(
                sub_subconfig.path,
                sub_subconfig.index,
                self._config_bag,
                subconfig=sub_subconfig,
            )

    def get(self):
        """Get Tiramisu option"""
        return None

    def isleadership(self):
        """Test if option is a leader or a follower"""
        return False

    def description(
        self,
        uncalculated: bool = False,
    ) -> str:
        """Get option description"""
        if not uncalculated:
            return self._config_bag.context.get_description().impl_get_display_name(
                None
            )
        return self._config_bag.context.get_description()._get_information(
            None,
            "doc",
            None,
        )

    def name(self):
        """Get option name"""
        return None

    def path(
        self,
    ):
        """Get option path"""
        return None

    def has_dependency(
        self,
        self_is_dep=True,
    ) -> bool:
        """Test if option has dependency"""
        return False

    def isoptiondescription(self):
        """Test if option is an optiondescription"""
        return True

    def isdynamic(self):
        """Test if option is a dynamic optiondescription"""
        return False

    def type(self):
        """Get de option type"""
        return "optiondescription"

    def list(
        self,
        *,
        validate_properties: bool = True,
        uncalculated: bool = False,
    ):
        """List options (by default list only option)"""
        root = self._config_bag.context.get_root(self._config_bag)
        return self._list(
            root,
            validate_properties,
            uncalculated=uncalculated,
        )

    def _load_dict(self, clearable="all", remotable="minimum"):
        self._tiramisu_dict = TiramisuDict(
            self._return_config(self._config_bag.context),
            root=None,
            clearable=clearable,
            remotable=remotable,
        )

    def dict(
        self,
        clearable="all",
        remotable="minimum",
        form=None,
        force=False,
    ):
        """Convert config and option to tiramisu format"""
        if form is None:
            form = []
        if force or self._tiramisu_dict is None:
            self._load_dict(clearable, remotable)
        return self._tiramisu_dict.todict(form)

    def updates(self, body: List) -> Dict:
        """Updates value with tiramisu format"""
        if self._tiramisu_dict is None:  # pragma: no cover
            self._load_dict()
        return self._tiramisu_dict.set_updates(body)


class _TiramisuContextConfigReset:
    def reset(self):
        """Remove all datas to current config (informations, values, properties, ...)"""
        # Option's values
        context_owner = self._config_bag.context.get_values().get_context_owner()
        self._config_bag.context.get_values()._values = {
            None: {None: [None, context_owner]}
        }
        # Option's informations
        self._config_bag.context.get_values()._informations = {}
        # Option's properties
        self._config_bag.context.get_settings()._properties = {}
        # Option's permissives
        self._config_bag.context.get_settings()._permissives = {}
        # Remove cache
        self._config_bag.context.reset_cache(None, None)


class _TiramisuContextConfig(TiramisuConfig, _TiramisuContextConfigReset):
    """Actions to Config"""

    def type(self):
        """Type a Config"""
        return "config"

    def copy(self, name=None):
        """Copy current config"""
        config = self._config_bag.context.duplicate(name=name)
        return self._return_config(config)

    def deepcopy(self, metaconfig_prefix=None, name=None):
        """Copy current config with all parents"""
        config = self._config_bag.context.duplicate(
            metaconfig_prefix=metaconfig_prefix,
            deep=[],
            name=name,
        )
        return self._return_config(config)

    def parents(self):
        """Get all parents of current config"""
        ret = []
        for parent in self._config_bag.context.get_parents():
            ret.append(self._return_config(parent))
        return ret

    def path(self):
        """Get path from config (all parents name)"""
        return self._config_bag.context.get_config_path()


class _TiramisuContextGroupConfig(TiramisuConfig):
    """Actions to GroupConfig"""

    def type(self):
        """Type a Config"""
        return "groupconfig"

    def list(self):
        """List children's config"""
        return [
            self._return_config(child)
            for child in self._config_bag.context.get_children()
        ]

    #
    #    def find(self,
    #             name: str,
    #             value=undefined,
    #             ):
    #        """Find an or a list of config with finding option"""
    #        return GroupConfig(self._config_bag.context.find_group(byname=name,
    #                                                               byvalue=value,
    #                                                               config_bag=self._config_bag,
    #                                                               ))

    def __call__(self, path: Optional[str]):
        """Select a child Tiramisu config"""
        spaths = path.split(".")
        config = self._config_bag.context
        for spath in spaths:
            config = config.getconfig(spath)
        if isinstance(config, KernelGroupConfig):
            return self._return_config(config)
        return self._return_config(config)

    def copy(self, name=None):
        config = self._config_bag.context.duplicate(name=name)
        return self._return_config(config)

    def deepcopy(self, name=None, metaconfig_prefix=None):
        config = self._config_bag.context.duplicate(
            metaconfig_prefix=metaconfig_prefix,
            deep=[],
            name=name,
        )
        return self._return_config(config)

    def path(self):
        return self._config_bag.context.get_config_path()


class _TiramisuContextMixConfig(
    _TiramisuContextGroupConfig, _TiramisuContextConfigReset
):
    """Actions to MixConfig"""

    def type(self):
        """Type a Config"""
        return "mixconfig"

    def new(self, name=None, type="config"):
        """Create and add a new config"""
        config = self._config_bag.context
        new_config = config.new_config(type_=type, name=name)
        return self._return_config(new_config)

    def remove(self, name):
        """Remove config from MetaConfig"""
        config = self._config_bag.context.remove_config(name)
        return self._return_config(config)

    def add(self, config):
        """Add config from MetaConfig"""
        # pylint: disable=protected-access
        self._config_bag.context.add_config(config._config_bag.context)

    def parents(self):
        """Get all parents of current config"""
        ret = []
        for parent in self._config_bag.context.get_parents():
            ret.append(self._return_config(parent))
        return ret


class _TiramisuContextMetaConfig(_TiramisuContextMixConfig):
    """Actions to MetaConfig"""

    def type(self):
        """Type a Config"""
        return "metaconfig"


class TiramisuContextCache(TiramisuConfig):
    """Manage config cache"""

    def reset(self):
        """Reset cache"""
        self._config_bag.context.reset_cache(None, None)

    def set_expiration_time(
        self,
        time: int,
    ) -> None:
        """Change expiration time value"""
        self._config_bag.expiration_time = time

    def get_expiration_time(self) -> int:
        """Get expiration time value"""
        return self._config_bag.expiration_time


class TiramisuAPI(TiramisuHelp):
    """TiramisuAPI common class"""

    _registers = {}

    def __init__(self, config_bag, orig_config_bags=None) -> None:
        self._config_bag = config_bag
        self._orig_config_bags = orig_config_bags
        if not self._registers:
            _registers(self._registers, "TiramisuContext")
        super().__init__()

    def option(
        self,
        path: str,
        index: Optional[int] = None,
    ) -> TiramisuOption:
        """Select an option by path"""
        return TiramisuOption(
            path,
            index,
            self._config_bag,
        )

    def __getattr__(self, subfunc: str) -> Any:
        if subfunc in ["forcepermissive", "unrestraint", "nowarnings"]:
            if self._orig_config_bags:
                msg = _(
                    "do not use unrestraint, nowarnings or forcepermissive together"
                )
                raise ConfigError(msg)
            config_bag = self._config_bag.copy()
            if subfunc == "unrestraint":
                config_bag.unrestraint()
            elif subfunc == "nowarnings":
                config_bag.nowarnings()
            else:
                config_bag.set_permissive()
            return ConfigProp(config_bag, [self._config_bag])
        if subfunc == "config":
            config_type = self._config_bag.context.impl_type
            if config_type == "group":
                config = _TiramisuContextGroupConfig
            elif config_type == "meta":
                config = _TiramisuContextMetaConfig
            elif config_type == "mix":
                config = _TiramisuContextMixConfig
            else:
                config = _TiramisuContextConfig
            return config(self._config_bag, self._orig_config_bags)
        if subfunc in self._registers:
            config_bag = self._config_bag
            # del config_bag.permissives
            return self._registers[subfunc](config_bag, self._orig_config_bags)
        raise ConfigError(
            _("please specify a valid sub function ({0}.{1})").format(
                self.__class__.__name__, subfunc
            )
        )

    def __dir__(self):
        return list(self._registers.keys()) + [
            "unrestraint",
            "forcepermissive",
            "nowarnings",
            "config",
        ]


class ConfigProp(TiramisuAPI, TiramisuContextOption):
    def __repr__(self):
        return f"<Config path=None>"


class Config(TiramisuAPI, TiramisuContextOption):
    """Root config object that enables us to handle the configuration options"""

    def __init__(
        self,
        descr: OptionDescription,
        name=None,
        display_name=None,
    ) -> None:
        if isinstance(descr, KernelConfig):
            config = descr
        else:
            config = KernelConfig(
                descr,
                name=name,
                display_name=display_name,
            )
        settings = config.get_settings()
        properties = settings.get_context_properties()
        permissives = settings.get_context_permissives()
        config_bag = ConfigBag(
            config,
            properties=properties,
            permissives=permissives,
        )
        super().__init__(config_bag)

    def __del__(self):
        try:
            del self._config_bag.context
            del self._config_bag
            del self._orig_config_bags
        except ConfigError:
            pass

    def __repr__(self):
        return f"<Config path=None>"


class MetaConfig(TiramisuAPI):
    """MetaConfig object that enables us to handle the sub configuration's options
    with common root optiondescription
    """

    # pylint: disable=too-few-public-methods
    def __init__(
        self,
        children: "Config" = None,
        name=None,
        optiondescription: Optional[OptionDescription] = None,
        display_name=None,
    ) -> None:
        if children is None:
            children = []
        if isinstance(children, KernelMetaConfig):
            config = children
        else:
            _children = []
            for child in children:
                if isinstance(child, TiramisuAPI):
                    _children.append(child._config_bag.context)
                else:
                    _children.append(child)

            config = KernelMetaConfig(
                _children,
                optiondescription=optiondescription,
                name=name,
                display_name=display_name,
            )
        settings = config.get_settings()
        properties = settings.get_context_properties()
        permissives = settings.get_context_permissives()
        config_bag = ConfigBag(config, properties=properties, permissives=permissives)
        super().__init__(config_bag)


class MixConfig(TiramisuAPI):
    """MixConfig object that enables us to handle the sub configuration's options
    with differents root optiondescription
    """

    # pylint: disable=too-few-public-methods
    def __init__(
        self,
        optiondescription: OptionDescription,
        children: List[Config],
        name: Callable = None,
        display_name=None,
    ) -> None:
        if isinstance(children, KernelMixConfig):
            config = children
        else:
            _children = []
            for child in children:
                if isinstance(child, TiramisuAPI):
                    _children.append(child._config_bag.context)
                else:
                    _children.append(child)

            config = KernelMixConfig(
                optiondescription,
                _children,
                name=name,
                display_name=display_name,
            )
        settings = config.get_settings()
        properties = settings.get_context_properties(config.properties_cache)
        permissives = settings.get_context_permissives()
        config_bag = ConfigBag(
            config,
            properties=properties,
            permissives=permissives,
        )
        super().__init__(config_bag)


class GroupConfig(TiramisuAPI):
    """GroupConfig that enables us to access the sub configuration's options"""

    # pylint: disable=too-few-public-methods
    def __init__(
        self,
        children,
        name=None,
    ) -> None:
        if isinstance(children, KernelGroupConfig):
            config = children
        else:
            _children = []
            for child in children:
                if isinstance(child, TiramisuAPI):
                    _children.append(child._config_bag.context)
                else:
                    _children.append(child)

            config = KernelGroupConfig(_children, name=name)
        config_bag = ConfigBag(config, properties=None, permissives=None)
        super().__init__(config_bag)
