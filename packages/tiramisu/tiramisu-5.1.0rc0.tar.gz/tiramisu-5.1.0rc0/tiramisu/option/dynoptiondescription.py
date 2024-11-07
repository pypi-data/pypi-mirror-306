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
#
# The original `Config` design model is unproudly borrowed from
# the rough pypy's guys: http://codespeak.net/svn/pypy/dist/pypy/config/
# the whole pypy projet is under MIT licence
# ____________________________________________________________
"""DynOptionDescription
"""
import re
import weakref
from typing import List, Any, Optional, Dict
from itertools import chain
from ..autolib import ParamOption


from ..i18n import _
from .optiondescription import OptionDescription
from .baseoption import BaseOption
from ..setting import ConfigBag, undefined
from ..error import ConfigError
from ..autolib import Calculation, get_calculated_value


NAME_REGEXP = re.compile(r"^[a-zA-Z\d\-_]*$")


class DynOptionDescription(OptionDescription):
    """dyn option description"""

    __slots__ = (
        "_identifiers",
        "_subdyns",
    )

    def __init__(
        self,
        name: str,
        doc: str,
        children: List[BaseOption],
        identifiers: Calculation,
        **kwargs,
    ) -> None:
        # pylint: disable=too-many-arguments
        super().__init__(
            name,
            doc,
            children,
            **kwargs,
        )
        # check children + set relation to this dynoptiondescription
        wself = weakref.ref(self)
        for child in children:
            child._setsubdyn(wself)
        # add identifiers
        self.value_dependencies(identifiers, is_identifier=True)
        self._identifiers = identifiers

    def convert_identifier_to_path(
        self,
        identifier: Any,
    ) -> str:
        """convert identifier to use it to a path"""
        if identifier is None:
            return None
        if not isinstance(identifier, str):
            identifier = str(identifier)
        if "." in identifier:
            identifier = identifier.replace(".", "_")
        return identifier

    def impl_is_dynoptiondescription(self) -> bool:
        return True

    def option_is_self(
        self,
        option,
    ) -> bool:
        return option == self

    def impl_getname(self, identifier=None) -> str:
        """get name"""
        name = super().impl_getname()
        if identifier is None:
            return name
        path_identifier = self.convert_identifier_to_path(identifier)
        return name + path_identifier

    def get_identifiers(
        self,
        parent: "SubConfig",
        *,
        uncalculated: bool = False,
    ) -> List[str]:
        """get dynamic identifiers"""
        subconfig = parent.get_child(
            self,
            None,
            False,
            properties=None,
        )
        identifiers = self._identifiers
        if isinstance(identifiers, list):
            identifiers = identifiers.copy()
        if uncalculated:
            return identifiers
        values = get_calculated_value(
            subconfig,
            identifiers,
            validate_properties=False,
        )[0]
        if values is None:
            values = []
        values_ = []
        if __debug__:
            if not isinstance(values, list):
                raise ValueError(
                    _(
                        "DynOptionDescription identifiers for option {0}, is not a list ({1})"
                    ).format(
                        self.impl_get_display_name(subconfig, with_quote=True), values
                    )
                )
        for val in values:
            cval = self.convert_identifier_to_path(val)
            if not isinstance(cval, str) or re.match(NAME_REGEXP, cval) is None:
                if __debug__ and cval is not None:
                    raise ValueError(
                        _('invalid identifier "{}" for option {}' "").format(
                            cval, self.impl_get_display_name(subconfig, with_quote=True)
                        )
                    )
            else:
                values_.append(val)
        if __debug__ and len(values_) > len(set(values_)):
            raise ValueError(
                _(
                    'DynOptionDescription "{0}" identifiers return a list with same values "{1}"'
                ).format(self._name, values_)
            )
        return values_
