# -*- coding: utf-8 -*-
"sets the options of the configuration objects Config object itself"
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
# ____________________________________________________________
from typing import Union, Set
from itertools import chain
from .error import (
    PropertiesOptionError,
    ConstError,
    ConfigError,
    LeadershipError,
    display_list,
)
from .i18n import _


# If cache and expire is enable, time before cache is expired.
# This delay start first time value/setting is set in cache, even if
# user access several time to value/setting
EXPIRATION_TIME = 5

# List of default properties (you can add new one if needed).
#
# For common properties and personalise properties, if a propery is set for
# an Option and for the Config together, Setting raise a PropertiesOptionError
#
# * Common properties:
#
# hidden
#    option with this property can only get value in read only mode. This
#    option is not available in read write mode.
#
# disabled
#    option with this property cannot be set/get
#
# frozen
#    cannot set value for option with this properties if 'frozen' is set in
#    config
#
# * Special property:
#
# permissive
#    option with 'permissive' cannot raise PropertiesOptionError for properties
#    set in permissive
#    config with 'permissive', whole option in this config cannot raise
#    PropertiesOptionError for properties set in permissive
#
# mandatory
#    should set value for option with this properties if 'mandatory' is set in
#    config
#    example: 'a', ['a'], [None] are valid
#             None, [] are not valid
#
# empty
#    raise mandatory PropertiesOptionError if multi or leader have empty value
#    example: ['a'] is valid
#             [None] is not valid
#
# unique
#    raise ValueError if a value is set twice or more in a multi Option
#
# * Special Config properties:
#
# cache
#    if set, enable cache settings and values
#
# expire
#    if set, settings and values in cache expire after ``expiration_time``
#
# everything_frozen
#    whole option in config are frozen (even if option have not frozen
#    property)
#
# validator
#    launch validator set by user in option (this property has no effect
#    for internal validator)
#
# warnings
#    display warnings during validation
#
# demoting_error_warning
#    all value errors are convert to warning (ValueErrorWarning)
DEFAULT_PROPERTIES = frozenset(["cache", "validator", "warnings"])
SPECIAL_PROPERTIES = {"frozen", "mandatory", "empty", "force_store_value"}

# Config can be in two defaut mode:
#
# read_only
#    you can get all variables not disabled but you cannot set any variables
#    if a value has a callback without any value, callback is launch and value
#    of this variable can change
#    you cannot access to mandatory variable without values
#
# read_write
#    you can get all variables not disabled and not hidden
#    you can set all variables not frozen
RO_APPEND = frozenset(
    [
        "frozen",
        "disabled",
        "validator",
        "everything_frozen",
        "mandatory",
        "empty",
        "force_store_value",
    ]
)
RO_REMOVE = frozenset(
    [
        "permissive",
        "hidden",
    ]
)
RW_APPEND = frozenset(
    [
        "frozen",
        "disabled",
        "validator",
        "hidden",
        "force_store_value",
    ]
)
RW_REMOVE = frozenset(
    [
        "permissive",
        "everything_frozen",
        "mandatory",
        "empty",
    ]
)


FORBIDDEN_SET_PROPERTIES = frozenset(["force_store_value"])
FORBIDDEN_SET_PERMISSIVES = frozenset(
    [
        "force_default_on_freeze",
        "force_metaconfig_on_freeze",
        "force_store_value",
    ]
)
ALLOWED_LEADER_PROPERTIES = {
    "empty",
    "notempty",
    "notunique",
    "unique",
    "force_store_value",
    "mandatory",
    "force_default_on_freeze",
    "force_metaconfig_on_freeze",
    "frozen",
}

static_set = frozenset()


# ____________________________________________________________
class Undefined:
    """Object undefined, means that there is not value"""

    # pylint: disable=too-few-public-methods
    def __str__(self):  # pragma: no cover
        return "Undefined"

    __repr__ = __str__


undefined = Undefined()


class ConfigBag:
    """Object to store information for context"""

    __slots__ = (
        "context",  # link to the current context
        "properties",  # properties for current context
        "true_properties",  # properties for current context
        "is_unrestraint",
        "permissives",  # permissives for current context
        "expiration_time",  # EXPIRATION_TIME
    )

    def __init__(self, context, properties: set, permissives: frozenset, **kwargs):
        self.context = context
        self.properties = properties
        self.permissives = permissives
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __getattr__(self, key):
        if key == "true_properties":
            return self.properties
        if key == "expiration_time":
            self.expiration_time = (
                EXPIRATION_TIME  # pylint: disable=attribute-defined-outside-init
            )
            return self.expiration_time
        if key == "is_unrestraint":
            return False
        raise KeyError(f'unknown key "{key}" for ConfigBag')  # pragma: no cover

    def nowarnings(self):
        """do not warnings"""
        self.properties = frozenset(self.properties - {"warnings"})

    def remove_validation(self):
        """do not validate option"""
        self.properties = frozenset(self.properties - {"validator"})

    def unrestraint(self):
        """do not restraint access to option"""
        self.is_unrestraint = True  # pylint: disable=attribute-defined-outside-init
        self.true_properties = (
            self.properties
        )  # pylint: disable=attribute-defined-outside-init
        self.properties = frozenset(["cache"])

    def set_permissive(self):
        """set permissive"""
        self.properties = frozenset(self.properties | {"permissive"})

    def copy(self):
        """copy the config"""
        kwargs = {}
        for key in self.__slots__:
            kwargs[key] = getattr(self, key)
        return ConfigBag(**kwargs)


# ____________________________________________________________
class _NameSpace:
    """convenient class that emulates a module
    and builds constants (that is, unique names)
    when attribute is added, we cannot delete it
    """

    def __setattr__(
        self,
        name,
        value,
    ):
        if name in self.__dict__:
            raise ConstError(_("can't rebind {0}").format(name))
        self.__dict__[name] = value

    def __delattr__(
        self,
        name,
    ):
        raise ConstError(_("can't unbind {0}").format(name))


class GroupModule(_NameSpace):
    "emulates a module to manage unique group (OptionDescription) names"

    # pylint: disable=too-few-public-methods
    class GroupType(str):
        """allowed normal group (OptionDescription) names
        *normal* means : groups that are not leader
        """

    class DefaultGroupType(GroupType):
        """groups that are default (typically 'default')"""

    class LeadershipGroupType(GroupType):
        """allowed normal group (OptionDescription) names
        *leadership* means : groups that have the 'leadership' attribute set
        """

    class RootGroupType(GroupType):
        """root means this is the root optiondescription of whole config"""

    def addgroup(self, name):
        """add a new group type"""
        setattr(groups, name, groups.GroupType(name))


class OwnerModule(_NameSpace):
    """emulates a module to manage unique owner names.

    owners are living in `Config._value_owners`
    """

    # pylint: disable=too-few-public-methods
    class Owner(str):
        """allowed owner names"""

    class DefaultOwner(Owner):
        """groups that are default (typically 'default')"""

    def addowner(self, name):
        """
        :param name: the name of the new owner
        """
        setattr(owners, name, owners.Owner(name))


# ____________________________________________________________
# populate groups
groups = GroupModule()

# groups.default: default group set when creating a new optiondescription
groups.default = groups.DefaultGroupType(
    "default"
)  # pylint: disable=attribute-defined-outside-init

# groups.leadership: leadership group is a special optiondescription, all suboptions should
#                    be multi option and all values should have same length, to find
#                    leader's option, the optiondescription's name should be same than de
#                    leader's option"""
groups.leadership = groups.LeadershipGroupType(
    "leadership"
)  # pylint: disable=attribute-defined-outside-init

# groups.root: this group is the root optiondescription of whole config
groups.root = groups.RootGroupType(
    "root"
)  # pylint: disable=attribute-defined-outside-init


# ____________________________________________________________
# populate owners with default attributes
owners = OwnerModule()

# default: is the config owner after init time
owners.default = owners.DefaultOwner(
    "default"
)  # pylint: disable=attribute-defined-outside-init

# user: is the generic is the generic owner
owners.addowner("user")

# forced: special owner when value is forced
owners.addowner("forced")


forbidden_owners = (owners.default, owners.forced)  # pylint: disable=no-member


# ____________________________________________________________
class Settings:
    "``config.Config()``'s configuration options settings"
    __slots__ = (
        "_properties",
        "_permissives",
        "_permissives",
        "__weakref__",
        "ro_append",
        "ro_remove",
        "rw_append",
        "rw_remove",
    )

    def __init__(self):
        """
        initializer

        :param context: the root config
        :param storage: the storage type
        """
        # generic owner
        self._properties = {None: {None: DEFAULT_PROPERTIES}}
        self._permissives = {}
        self.ro_append = RO_APPEND
        self.ro_remove = RO_REMOVE
        self.rw_append = RW_APPEND
        self.rw_remove = RW_REMOVE

    # ____________________________________________________________
    # get properties and permissive methods

    def get_context_properties(self):
        """get context properties"""
        return self.get_personalize_properties()

    def get_personalize_properties(
        self,
        path: Union[None, str] = None,
        index: Union[None, int] = None,
    ) -> Set[str]:
        """Get the properties modified by user for a path or index"""
        if path not in self._properties or index not in self._properties[path]:
            return frozenset()
        return self._properties[path][index]

    def getproperties(
        self,
        subconfig: "SubConfig",
        *,
        apply_requires=True,
        uncalculated=False,
        help_property=False,
        transitive_raise=True,
    ):
        """get properties"""
        # pylint: disable=too-many-branches
        option = subconfig.option
        if option.impl_is_symlinkoption():
            option = option.impl_getopt()
        if apply_requires and not uncalculated and not help_property:
            cache = subconfig.config_bag.context.properties_cache
            is_cached, props, validated = cache.getcache(
                subconfig,  # pylint: disable=unused-variable
                "self_props",
            )
        else:
            is_cached = False
        if not is_cached:
            props = set()
            # if index, get option's properties (without index) too
            p_props = [option.impl_getproperties()]
            props_config = self.get_personalize_properties(subconfig.path)
            if props_config:
                p_props.append(props_config)
            if subconfig.index is not None:
                props_config = self.get_personalize_properties(
                    subconfig.path,
                    subconfig.index,
                )
                if props_config:
                    p_props.append(props_config)
            for prop in chain(*p_props):
                if uncalculated or isinstance(prop, str):
                    if not help_property:
                        props.add(prop)
                    else:
                        props.add((prop, prop))
                elif apply_requires:
                    try:
                        if not help_property:
                            new_prop = prop.execute(
                                subconfig,
                                for_settings=True,
                            )
                        else:
                            new_prop = prop.help(
                                subconfig,
                                for_settings=True,
                            )
                            if isinstance(new_prop, str):
                                new_prop = (new_prop, new_prop)
                        if new_prop is None:
                            continue
                    except ConfigError as err:
                        if transitive_raise:
                            raise err from err
                        continue
                    if (not help_property and not isinstance(new_prop, str)) or (
                        help_property and not isinstance(new_prop, tuple)
                    ):
                        raise ValueError(
                            _(
                                "invalid property type {type(new_prop)} for "
                                "{subconfig.option.impl_getname()} with "
                                "{prop.function.__name__} function"
                            )
                        )
                    if (
                        not option.impl_is_optiondescription()
                        and option.impl_is_leader()
                        and new_prop not in ALLOWED_LEADER_PROPERTIES
                    ):
                        raise LeadershipError(
                            _('leader cannot have "{new_prop}" property')
                        )
                    props.add(new_prop)
            props -= self.getpermissives(subconfig)
            if (
                not uncalculated
                and apply_requires
                and not subconfig.config_bag.is_unrestraint
                and not help_property
                and transitive_raise
            ):
                cache.setcache(
                    subconfig,
                    props,
                    type_="properties",
                )
        if (
            not uncalculated
            and subconfig.parent
            and subconfig.parent.transitive_properties
        ):
            parent_properties = subconfig.parent.transitive_properties
            parent_properties -= self.getpermissives(subconfig)
            if help_property:
                parent_properties = {(prop, prop) for prop in parent_properties}
            return props | parent_properties
        return props

    def get_context_permissives(self):
        """get context permissives"""
        return self.getpermissives(None)

    def _getpermissives(
        self,
        path,
        index,
    ):
        if not path in self._permissives:
            ret = frozenset()
        else:
            ret = self._permissives[path].get(index, frozenset())
        return ret

    def getpermissives(
        self,
        subconfig: "SubConfig",
    ):
        """get permissive"""
        if subconfig is None:
            path = None
            index = None
        else:
            opt = subconfig.option
            if opt.impl_is_symlinkoption():
                opt = opt.impl_getopt()
                path = opt.impl_getpath()
            else:
                path = subconfig.path
            index = subconfig.index
        permissives = self._getpermissives(
            path,
            None,
        )
        if index is not None:
            option_permissives = self._permissives.get(path, {}).get(index, set())
            permissives = frozenset(option_permissives | permissives)
        return permissives

    # ____________________________________________________________
    # set methods
    def set_context_properties(self, properties, context):
        """set context properties"""
        self._properties[None][None] = properties
        context.reset_cache(None)

    def setproperties(
        self,
        subconfig,
        properties,
    ):
        """save properties for specified path
        (never save properties if same has option properties)
        """
        opt = subconfig.option
        if not opt.impl_is_optiondescription() and opt.impl_is_leader():
            not_allowed_properties = properties - ALLOWED_LEADER_PROPERTIES
            if not_allowed_properties:
                raise LeadershipError(
                    _('leader cannot have "{0}" property').format(
                        display_list(not_allowed_properties)
                    )
                )
            if (
                "force_default_on_freeze" in properties
                or "force_metaconfig_on_freeze" in properties
            ) and "frozen" not in properties:
                raise LeadershipError(
                    _(
                        'a leader ({0}) cannot have "force_default_on_freeze" or "force_metaconfig_on_freeze" property without "frozen"'
                    ).format(opt.impl_get_display_name())
                )
        self._properties.setdefault(subconfig.path, {})[subconfig.index] = properties
        # values too because of follower values could have a PropertiesOptionError has value
        subconfig.config_bag.context.reset_cache(subconfig)
        subconfig.properties = properties

    def set_context_permissives(
        self,
        permissives,
    ):
        """set context permissive"""
        self.setpermissives(
            None,
            permissives,
        )

    def setpermissives(
        self,
        subconfig,
        permissives,
    ):
        """
        enables us to put the permissives in the storage

        :param path: the option's path
        :param type: str
        :param opt: if an option object is set, the path is extracted.
                    it is better (faster) to set the path parameter
                    instead of passing a :class:`tiramisu.option.Option()` object.
        """
        if not isinstance(permissives, frozenset):
            raise TypeError(_("permissive must be a frozenset"))
        if subconfig is not None:
            path = subconfig.path
            index = subconfig.index
        else:
            path = None
            index = None
        forbidden_permissives = FORBIDDEN_SET_PERMISSIVES & permissives
        if forbidden_permissives:
            raise ConfigError(
                _("cannot add those permissives: {0}").format(
                    " ".join(forbidden_permissives)
                )
            )
        self._permissives.setdefault(path, {})[index] = permissives
        if subconfig is not None:
            subconfig.config_bag.context.reset_cache(subconfig)

    # ____________________________________________________________
    # reset methods
    def _get_path_index_config_option(
        self,
        bag: Union["SubConfig", ConfigBag],
        msg: str,
    ):
        if isinstance(bag, ConfigBag):
            path = None
            index = None
            config_bag = bag
            subconfig = None
        else:
            assert not bag.option.impl_is_symlinkoption(), msg.format(
                bag.option.impl_get_display_name()
            )
            path = bag.path
            index = bag.index
            config_bag = bag.config_bag
            subconfig = bag
        return path, index, config_bag, subconfig

    def reset(
        self,
        bag: Union["SubConfig", ConfigBag],
    ):
        """reset property"""
        path, index, config_bag, subconfig = self._get_path_index_config_option(
            bag,
            _("can't reset properties to " 'the symlinkoption "{}"'),
        )
        if path in self._properties and index in self._properties[path]:
            del self._properties[path][index]
        config_bag.context.reset_cache(subconfig)

    def reset_permissives(
        self,
        bag: Union["SubConfig", ConfigBag],
    ):
        """reset permission"""
        path, index, config_bag, subconfig = self._get_path_index_config_option(
            bag,
            _("can't reset permissives to " 'the symlinkoption "{}"'),
        )
        if path in self._permissives and index in self._permissives[path]:
            del self._permissives[path][index]
        config_bag.context.reset_cache(subconfig)

    # ____________________________________________________________
    # validate properties
    def calc_raises_properties(
        self,
        subconfig,
        *,
        apply_requires=True,
        uncalculated=False,
        transitive_raise=True,
        not_unrestraint: bool = False,
    ):
        """raise if needed"""
        if not uncalculated and apply_requires and subconfig.properties is not None:
            option_properties = subconfig.properties
        else:
            option_properties = self.getproperties(
                subconfig,
                apply_requires=apply_requires,
                uncalculated=uncalculated,
                transitive_raise=transitive_raise,
            )
        return self._calc_raises_properties(
            subconfig,
            option_properties,
            not_unrestraint,
        )

    def calc_transitive_properties(
        self,
        subconfig,
        option_properties,
    ):
        config_bag = subconfig.config_bag
        modified, context_properties = self.calc_read(
            self.rw_remove,
            self.rw_append,
            config_bag,
        )
        raises_properties = context_properties - SPECIAL_PROPERTIES
        # remove global permissive properties
        if raises_properties and "permissive" in raises_properties:
            raises_properties -= config_bag.permissives
        properties = option_properties & raises_properties
        # at this point it should not remain any property for the option
        return properties

    def _calc_raises_properties(
        self,
        subconfig,
        option_properties,
        not_unrestraint: bool,
    ):
        config_bag = subconfig.config_bag
        if not_unrestraint and config_bag.is_unrestraint:
            context_properties = config_bag.true_properties
        else:
            context_properties = config_bag.properties
        raises_properties = context_properties - SPECIAL_PROPERTIES
        # remove global permissive properties
        if raises_properties and "permissive" in raises_properties:
            raises_properties -= config_bag.permissives
        properties = option_properties & raises_properties
        # at this point it should not remain any property for the option
        return properties

    def validate_properties(
        self,
        subconfig,
        *,
        need_help=True,
    ):
        """check properties"""
        config_properties = subconfig.config_bag.properties
        if not config_properties or config_properties == frozenset(["cache"]):
            # if no global property
            return
        for transitive_raise in [False, True]:
            properties = self.calc_raises_properties(
                subconfig,
                transitive_raise=transitive_raise,
            )
            if properties != frozenset():
                if need_help:
                    help_properties = dict(
                        self.getproperties(
                            subconfig,
                            help_property=True,
                            transitive_raise=transitive_raise,
                        )
                    )
                    calc_properties = []
                    for property_ in self._calc_raises_properties(
                        subconfig,
                        set(help_properties.keys()),
                        False,
                    ):
                        calc_properties.append(help_properties[property_])
                    calc_properties = frozenset(calc_properties)
                else:
                    calc_properties = properties
                raise PropertiesOptionError(
                    subconfig,
                    properties,
                    self,
                    help_properties=calc_properties,
                )

    def validate_mandatory(
        self,
        subconfig,
        value,
    ):
        """verify if option is mandatory without value"""
        if "mandatory" not in subconfig.config_bag.properties:
            return
        values = subconfig.config_bag.context.get_values()
        if (
            not (
                "permissive" in subconfig.config_bag.properties
                and "mandatory" in subconfig.config_bag.permissives
            )
            and "mandatory" in subconfig.properties
            and values.isempty(
                subconfig,
                value,
                False,
            )
        ):
            raise PropertiesOptionError(
                subconfig,
                ["mandatory"],
                self,
            )
        if "empty" in subconfig.properties and values.isempty(
            subconfig,
            value,
            True,
        ):
            raise PropertiesOptionError(
                subconfig,
                ["empty"],
                self,
            )

    def validate_frozen(
        self,
        subconfig,
    ):
        """verify if option is frozen"""
        if (
            subconfig.config_bag.properties
            and (
                "everything_frozen" in subconfig.config_bag.properties
                or (
                    "frozen" in subconfig.config_bag.properties
                    and "frozen" in subconfig.properties
                )
            )
            and not (
                ("permissive" in subconfig.config_bag.properties)
                and "frozen" in subconfig.config_bag.permissives
            )
        ):
            raise PropertiesOptionError(
                subconfig,
                ["frozen"],
                self,
            )
        return False

    # ____________________________________________________________
    # read only/read write

    def calc_read(
        self,
        remove,
        append,
        config_bag,
    ):
        props = self.get_personalize_properties()
        modified = False
        if remove & props:
            props = props - remove
            modified = True
        if append & props != append:
            props = props | append
            modified = True
        return modified, frozenset(props)

    def _read(
        self,
        remove,
        append,
        config_bag,
    ):
        modified, props = self.calc_read(
            remove,
            append,
            config_bag,
        )
        if modified:
            self.set_context_properties(
                props,
                config_bag.context,
            )

    def read_only(
        self,
        config_bag,
    ):
        "convenience method to freeze, hide and disable"
        self._read(
            self.ro_remove,
            self.ro_append,
            config_bag,
        )

    def read_write(
        self,
        config_bag,
    ):
        "convenience method to freeze, hide and disable"
        self._read(
            self.rw_remove,
            self.rw_append,
            config_bag,
        )
