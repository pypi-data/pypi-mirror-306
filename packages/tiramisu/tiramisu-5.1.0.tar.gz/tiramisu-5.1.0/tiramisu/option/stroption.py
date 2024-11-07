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
"""StrOption and RegexpOption
"""
from typing import Any

from ..i18n import _
from .option import Option


class StrOption(Option):
    """represents a string"""

    __slots__ = tuple()
    _type = "string"

    def validate(
        self,
        value: str,
    ) -> None:
        """validation"""
        if not isinstance(value, str):
            raise ValueError()


class RegexpOption(StrOption):
    """regexp validation, this is base option use to do a custom's one"""

    __slots__ = tuple()

    def validate(
        self,
        value: Any,
    ) -> None:
        # pylint: disable=no-member
        """validation"""
        super().validate(value)
        match = self._regexp.search(value)
        if not match:
            raise ValueError()
