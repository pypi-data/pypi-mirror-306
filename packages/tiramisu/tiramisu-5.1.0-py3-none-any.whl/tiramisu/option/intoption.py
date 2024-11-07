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
"""IntOption
"""

from ..i18n import _
from .option import Option


class IntOption(Option):
    "represents a choice of an integer"
    __slots__ = tuple()
    _type = "integer"

    def __init__(self, *args, min_number=None, max_number=None, **kwargs):
        extra = {}
        if min_number is not None:
            extra["min_number"] = min_number
        if max_number is not None:
            extra["max_number"] = max_number
        super().__init__(*args, extra=extra, **kwargs)

    def validate(
        self,
        value: int,
    ) -> None:
        if not isinstance(value, int):
            raise ValueError()

    def second_level_validation(self, value, warnings_only):
        min_number = self.impl_get_extra("min_number")
        if min_number is not None and value < min_number:
            if warnings_only:
                msg = _('value should be equal or greater than "{0}"')
            else:
                msg = _('value must be equal or greater than "{0}"')
            raise ValueError(msg.format(min_number))
        max_number = self.impl_get_extra("max_number")
        if max_number is not None and value > max_number:
            if warnings_only:
                msg = _('value should be less than "{0}"')
            else:
                msg = _('value must be less than "{0}"')
            raise ValueError(msg.format(max_number))
