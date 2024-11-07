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
"""ChoiceOption
"""
from typing import Any

from ..setting import undefined
from ..i18n import _
from .option import Option
from ..autolib import Calculation, get_calculated_value
from ..error import ConfigError, display_list


class ChoiceOption(Option):
    """represents a choice out of several objects.

    The option can also have the value ``None``
    """

    __slots__ = tuple()
    _type = "choice"

    def __init__(self, name, doc, values, *args, **kwargs):
        """
        :param values: is a list of values the option can possibly take
        """
        if not isinstance(values, (Calculation, tuple)):
            raise TypeError(
                _("values must be a tuple or a calculation for {0}").format(name)
            )
        self._choice_values = values
        super().__init__(name, doc, *args, **kwargs)

    def impl_get_values(
        self,
        subconfig: "SubConfig",
        uncalculated: bool = False,
    ):
        """get values allowed by option"""
        choices = self._choice_values
        if isinstance(choices, tuple):
            choices = list(choices)
        if uncalculated:
            return choices
        values = get_calculated_value(
            subconfig,
            choices,
        )[0]

        if values != undefined and not isinstance(values, (list, tuple)):
            raise ConfigError(
                _('the calculated values "{0}" for "{1}" is not a list' "").format(
                    values, self.impl_getname()
                )
            )
        return values

    def validate(
        self,
        value: Any,
    ) -> None:
        """nothing to valide"""

    def validate_with_option(
        self,
        value: Any,
        subconfig: "SubConfig",
        loaded: bool,
    ) -> None:
        if loaded and isinstance(self._choice_values, Calculation):
            return
        values = self.impl_get_values(subconfig)
        self.validate_values(value, values)

    def validate_values(
        self,
        value,
        values,
    ) -> None:
        """validate values"""
        if values is not undefined and value not in values:
            if len(values) == 1:
                raise ValueError(_('only "{0}" is allowed' "").format(values[0]))
            raise ValueError(
                _("only {0} are allowed" "").format(
                    display_list(values, add_quote=True)
                )
            )
