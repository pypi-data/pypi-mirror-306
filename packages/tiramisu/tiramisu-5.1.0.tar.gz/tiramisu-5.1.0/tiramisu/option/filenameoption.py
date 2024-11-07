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
"""FilenameOption
"""
from pathlib import Path

from ..i18n import _
from ..error import display_list
from .stroption import StrOption


class FilenameOption(StrOption):
    """validate file or directory name"""

    __slots__ = tuple()
    _type = "file name"

    def __init__(
        self,
        name: str,
        *args,
        allow_relative=False,
        test_existence=False,
        types=["file", "directory"],
        **kwargs,
    ):
        if not isinstance(types, list):
            raise ValueError(
                _('types parameter must be a list, not "{0}" for "{1}"').format(
                    types, name
                )
            )
        for typ in types:
            if typ not in ["file", "directory"]:
                raise ValueError(f'unknown type "{typ}" for "{name}"')
        extra = {
            "_allow_relative": allow_relative,
            "_test_existence": test_existence,
            "_types": types,
        }
        super().__init__(name, *args, extra=extra, **kwargs)

    def validate(
        self,
        value: str,
    ) -> None:
        super().validate(value)
        if not self.impl_get_extra("_allow_relative") and not value.startswith("/"):
            raise ValueError(_('must starts with "/"'))
        if value is not None and self.impl_get_extra("_test_existence"):
            types = self.impl_get_extra("_types")
            file = Path(value)
            found = False
            if "file" in types and file.is_file():
                found = True
            if not found and "directory" in types and file.is_dir():
                found = True
            if not found:
                raise ValueError(
                    _('cannot find {0} "{1}"').format(
                        display_list(types, separator="or"), value
                    )
                )
