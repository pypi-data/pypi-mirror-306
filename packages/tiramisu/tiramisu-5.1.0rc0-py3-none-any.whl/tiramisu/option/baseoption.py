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
"""base option
"""
from typing import FrozenSet, Set, Any, List, Optional, Dict
import weakref
from itertools import chain


from ..i18n import _
from ..setting import undefined
from ..autolib import Calculation, ParamOption, ParamInformation, ParamSelfInformation

STATIC_TUPLE = frozenset()


submulti = 2


def valid_name(name):
    """valid option name"""
    if not isinstance(name, str):
        return False
    if "." in name:
        return False
    return True


# ____________________________________________________________
#
class Base:
    """Base use by all *Option* classes (Option, OptionDescription, SymLinkOption, ...)"""

    __slots__ = (
        "_name",
        "_path",
        "_informations",
        "_subdyns",
        "_properties",
        "_has_dependency",
        "_dependencies",
        "_dependencies_information",
        "_identifiers_dependencies",
        "__weakref__",
    )

    def __init__(
        self,
        name: str,
        doc: str,
        informations: Optional[Dict],
        *,
        properties=None,
        is_multi: bool = False,
    ) -> None:
        if not valid_name(name):
            raise ValueError(_('"{0}" is an invalid name for an option').format(name))
        if properties is None:
            properties = frozenset()
        elif isinstance(properties, tuple):
            properties = frozenset(properties)
        if is_multi:
            # if option is a multi, it cannot be 'empty' (None not allowed in the list)
            # and cannot have multiple time the same value
            # 'empty' and 'unique' are removed for follower's option
            if "notunique" not in properties:
                properties = properties | {"unique"}
            if "notempty" not in properties:
                properties = properties | {"empty"}
        assert isinstance(properties, frozenset), _(
            "invalid properties type {0} for {1}," " must be a frozenset"
        ).format(type(properties), name)
        _setattr = object.__setattr__
        _setattr(self, "_name", name)
        _setattr(self, "_informations", {"doc": doc})
        for prop in properties:
            if not isinstance(prop, str):
                if not isinstance(prop, Calculation):
                    raise ValueError(
                        _(
                            "invalid property type {0} for {1}, must be a string or a "
                            "Calculation"
                        ).format(type(prop), name)
                    )
                for param in chain(prop.params.args, prop.params.kwargs.values()):
                    if isinstance(param, ParamOption):
                        param.option._add_dependency(self)
        if properties:
            _setattr(self, "_properties", properties)
        self.set_informations(informations)

    def set_informations(
        self,
        informations: Optional[Dict],
    ) -> None:
        if not informations:
            return
        for key, value in informations.items():
            self._set_information(
                key,
                value,
            )

    def impl_has_dependency(
        self,
        self_is_dep: bool = True,
    ) -> bool:
        """this has dependency"""
        if self_is_dep is True:
            return getattr(self, "_has_dependency", False)
        return hasattr(self, "_dependencies")

    def get_dependencies(
        self,
        context_od,
    ) -> Set[str]:
        ret = set(getattr(self, "_dependencies", STATIC_TUPLE))
        if context_od and hasattr(context_od, "_dependencies"):
            # add options that have context is set in calculation
            return (
                set(context_od._dependencies) | ret
            )  # pylint: disable=protected-access
        return ret

    def _get_identifiers_dependencies(self) -> Set[str]:
        return getattr(self, "_identifiers_dependencies", STATIC_TUPLE)

    def _add_dependency(
        self,
        option,
        is_identifier: bool = False,
    ) -> None:
        woption = weakref.ref(option)
        options = self.get_dependencies(None)
        options.add(woption)
        self._dependencies = tuple(
            options
        )  # pylint: disable=attribute-defined-outside-init
        if is_identifier:
            options = list(self._get_identifiers_dependencies())
            options.append(woption)
            self._identifiers_dependencies = tuple(
                options
            )  # pylint: disable=attribute-defined-outside-init

    def impl_is_optiondescription(self) -> bool:
        """option is an option description"""
        return False

    def impl_is_dynoptiondescription(self) -> bool:
        """option is not a dyn option description"""
        return False

    def impl_is_sub_dyn_optiondescription(self):
        return False

    def impl_getname(self) -> str:
        """get name"""
        return self._name  # pylint: disable=no-member

    def _set_readonly(self) -> None:
        if isinstance(self._informations, dict):  # pylint: disable=no-member
            _setattr = object.__setattr__
            dico = self._informations  # pylint: disable=no-member
            keys = tuple(dico.keys())
            if len(keys) == 1:
                dico = dico["doc"]
            else:
                dico = tuple([keys, tuple(dico.values())])
            _setattr(self, "_informations", dico)
            extra = getattr(self, "_extra", None)
            if extra is not None:
                _setattr(
                    self, "_extra", tuple([tuple(extra.keys()), tuple(extra.values())])
                )

    def impl_is_readonly(self) -> str:
        """the option is readonly"""
        return hasattr(self, "_path")

    def impl_getproperties(self) -> FrozenSet[str]:
        """get properties"""
        return getattr(self, "_properties", frozenset())

    def _setsubdyn(
        self,
        subdyn,
    ) -> None:
        # pylint: disable=attribute-defined-outside-init
        if getattr(self, "_subdyns", None) is None:
            self._subdyns = []
        self._subdyns.append(subdyn)

    def issubdyn(self) -> bool:
        """is sub dynoption"""
        return getattr(self, "_subdyns", None) is not None

    def getsubdyn(self):
        """get sub dynoption"""
        return self._subdyns[0]()

    def get_sub_dyns(self):
        return self._subdyns

    # ____________________________________________________________
    # information
    def _get_information(
        self,
        subconfig: "SubConfig",
        key: str,
        default: Any = undefined,
    ) -> Any:
        """retrieves one information's item

        :param key: the item string (ex: "help")
        """
        dico = self._informations  # pylint: disable=no-member
        if isinstance(dico, tuple):
            if key in dico[0]:
                return dico[1][dico[0].index(key)]
        elif isinstance(dico, str):
            if key == "doc":
                return dico
        elif isinstance(dico, dict):
            if key in dico:
                return dico[key]
        if default is not undefined:
            return default
        # pylint: disable=no-member
        raise ValueError(
            _('information\'s item for {0} not found: "{1}"').format(
                self.impl_get_display_name(subconfig, with_quote=True), key
            )
        )

    def _set_information(
        self,
        key: str,
        value: Any,
    ) -> None:
        """updates the information's attribute
        (which is a dictionary)

        :param key: information's key (ex: "help", "doc"
        :param value: information's value (ex: "the help string")
        """
        if self.impl_is_readonly():
            raise AttributeError(
                _("'{0}' ({1}) object attribute '{2}' is" " read-only").format(
                    self.__class__.__name__, self, key
                )
            )
        self._informations[key] = value  # pylint: disable=no-member

    def _list_information(self) -> Any:
        """get the list of information keys"""
        dico = self._informations  # pylint: disable=no-member
        if isinstance(dico, tuple):
            return list(dico[0])
        if not isinstance(dico, dict):
            return ["doc"]
        # it's a dict
        return list(dico.keys())


class BaseOption(Base):
    """This abstract base class stands for attribute access
    in options that have to be set only once, it is of course done in the
    __setattr__ method
    """

    __slots__ = ("_display_name_function",)

    def __setattr__(
        self,
        name: str,
        value: Any,
    ) -> Any:
        """set once and only once some attributes in the option,
        like `_name`. `_name` cannot be changed once the option is
        pushed in the :class:`tiramisu.option.OptionDescription`.

        if the attribute `_readonly` is set to `True`, the option is
        "frozen" (which has nothing to do with the high level "freeze"
        propertie or "read_only" property)
        """
        # never change _name in an option or attribute when object is readonly
        if self.impl_is_readonly():
            raise AttributeError(
                _('"{}" ({}) object attribute "{}" is' " read-only").format(
                    self.__class__.__name__, self.impl_get_display_name(None), name
                )
            )
        super().__setattr__(name, value)

    def impl_getpath(self) -> str:
        """get the path of the option"""
        try:
            return self._path
        except AttributeError as err:
            raise AttributeError(
                _("{0} not part of any Config").format(
                    self.impl_get_display_name(None, with_quote=True)
                )
            ) from err

    def impl_get_display_name(
        self,
        subconfig: "SubConfig",
        *,
        with_quote: bool = False,
    ) -> str:
        """get display name"""
        if hasattr(self, "_display_name_function"):
            return self._display_name_function(
                self,
                subconfig,
                with_quote=with_quote,
            )
        name = self._get_information(subconfig, "doc", None)
        if name is None or name == "":
            if subconfig and subconfig.path:
                name = subconfig.path.rsplit(".", 1)[-1]
            else:
                name = self._name
        if with_quote:
            return f'"{name}"'
        return name

    def reset_cache(
        self,
        path: str,
        config_bag: "OptionBag",
        resetted_opts: List[Base],  # pylint: disable=unused-argument
    ) -> None:
        """reset cache"""
        context = config_bag.context
        context.properties_cache.delcache(path)
        context._impl_permissives_cache.delcache(
            path
        )  # pylint: disable=protected-access
        if not self.impl_is_optiondescription():
            context.get_values_cache().delcache(
                path
            )  # pylint: disable=protected-access

    def impl_is_symlinkoption(self) -> bool:
        """the option is not a symlinkoption"""
        return False

    def get_dependencies_information(self) -> List[str]:
        """get dependencies information"""
        return getattr(self, "_dependencies_information", {})

    def value_dependencies(
        self,
        value: Any,
        is_identifier: bool = False,
    ) -> Any:
        """parse dependancies to add dependencies"""
        if isinstance(value, list):
            for val in value:
                if isinstance(value, list):
                    self.value_dependencies(val, is_identifier)
                elif isinstance(value, Calculation):
                    self.value_dependency(val, is_identifier)
        elif isinstance(value, Calculation):
            self.value_dependency(value, is_identifier)

    def value_dependency(
        self,
        value: Any,
        is_identifier: bool = False,
    ) -> Any:
        """parse dependancy to add dependencies"""
        for param in chain(value.params.args, value.params.kwargs.values()):
            if isinstance(param, ParamOption):
                # pylint: disable=protected-access
                param.option._add_dependency(self, is_identifier=is_identifier)
                self._has_dependency = True
            elif isinstance(param, ParamInformation):
                dest = self
                if isinstance(param, ParamSelfInformation):
                    opt = weakref.ref(self)
                elif param.option:
                    dest = param.option
                    opt = weakref.ref(self)
                else:
                    param.set_self_option(self)
                    opt = None
                if not getattr(dest, "_dependencies_information", {}):
                    dest._dependencies_information = {None: []}
                dest._dependencies_information[None].append(param)
                dest._dependencies_information.setdefault(
                    param.information_name, []
                ).append(opt)
