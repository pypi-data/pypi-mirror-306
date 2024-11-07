# -*- coding: utf-8 -*-
# Copyright (C) 2023-2024 Team tiramisu (see AUTHORS for all contributors)
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
"""PermissionsOption
"""
import re

from ..i18n import _
from .intoption import IntOption


class PermissionsOption(IntOption):
    """Unix file permissions
    Valid the representing Unix permissions is an octal (base-8) notation.
    This notation consists of at least three digits (owner, group, and others).
    If a fourth digit is present to the setuid bit, the setgid bit and the sticky bit attributes.
    This option is an integer value.
    """

    __slots__ = tuple()
    perm_re = re.compile(r"^[0-7]{3,4}$")
    _type = "unix file permissions"

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        # do not display intoption attributs
        super().__init__(*args, **kwargs)

    def validate(self, value: str) -> None:
        super().validate(value)
        if not self.perm_re.search(str(value)):
            raise ValueError(_("only 3 or 4 octal digits are allowed"))

    def second_level_validation(self, value: str, warnings_only: bool) -> None:
        old_digit = 7
        str_value = str(value)
        if len(str_value) == 4:
            str_value = str_value[1:]
        for idx, digit in enumerate(str_value):
            new_digit = int(digit)
            if old_digit < new_digit:
                if idx == 1:
                    old = _("user")
                    new = _("group")
                else:
                    old = _("group")
                    new = _("other")
                raise ValueError(_("{0} has more right than {1}").format(new, old))
            old_digit = new_digit
        if str_value == "777":
            raise ValueError(_("too weak"))
