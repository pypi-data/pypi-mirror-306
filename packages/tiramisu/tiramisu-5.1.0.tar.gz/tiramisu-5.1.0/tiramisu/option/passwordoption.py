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
"""PasswordOption
"""

from ..i18n import _
from ..error import display_list
from .stroption import StrOption


class PasswordOption(StrOption):
    """represents the choice of a password"""

    __slots__ = tuple()
    _type = "password"

    def __init__(self, *args, min_len=None, max_len=None, forbidden_char=[], **kwargs):
        extra = {}
        if min_len is not None:
            extra["min_len"] = min_len
        if max_len is not None:
            extra["max_len"] = max_len
        if forbidden_char:
            extra["forbidden_char"] = set(forbidden_char)
        super().__init__(*args, extra=extra, **kwargs)

    def validate(self, value: str) -> None:
        super().validate(value)
        min_len = self.impl_get_extra("min_len")
        if min_len and len(value) < min_len:
            raise ValueError(_("at least {0} characters are required").format(min_len))
        max_len = self.impl_get_extra("max_len")
        if max_len and len(value) > max_len:
            raise ValueError(_("maximum {0} characters required").format(max_len))
        if self.impl_get_extra("forbidden_char"):
            forbidden_char = set(value) & self.impl_get_extra("forbidden_char")
            if forbidden_char:
                raise ValueError(
                    _("must not have the characters {0}").format(
                        display_list(list(forbidden_char), add_quote=True)
                    )
                )
