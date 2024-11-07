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
"""PortOption
"""
import re

from ..i18n import _
from .stroption import StrOption


class PortOption(StrOption):
    """represents the choice of a port
    The port numbers are divided into three ranges:
    the well-known ports,
    the registered ports,
    and the dynamic or private ports.
    You can actived this three range.
    Port number 0 is reserved and can't be used.
    see: http://en.wikipedia.org/wiki/Port_numbers
    """

    __slots__ = tuple()
    port_re = re.compile(r"^[0-9]*$")
    _type = "port"

    def __init__(
        self,
        *args,
        allow_range: bool = False,
        allow_zero: bool = False,
        allow_wellknown: bool = True,
        allow_registred: bool = True,
        allow_protocol: bool = False,
        allow_private: bool = False,
        **kwargs,
    ) -> None:

        extra = {
            "_allow_range": allow_range,
            "_allow_protocol": allow_protocol,
            "_min_value": None,
            "_max_value": None,
        }
        ports_min = [0, 1, 1024, 49152]
        ports_max = [0, 1023, 49151, 65535]
        is_finally = False
        for index, allowed in enumerate(
            [allow_zero, allow_wellknown, allow_registred, allow_private]
        ):
            if extra["_min_value"] is None:
                if allowed:
                    extra["_min_value"] = ports_min[index]
            elif not allowed:
                is_finally = True
            elif allowed and is_finally:
                raise ValueError(_("inconsistency in allowed range"))
            if allowed:
                extra["_max_value"] = ports_max[index]

        if extra["_max_value"] is None:
            raise ValueError(_("max value is empty"))

        super().__init__(*args, extra=extra, **kwargs)

    def validate(self, value: str) -> None:
        super().validate(value)
        if self.impl_get_extra("_allow_protocol") and (
            value.startswith("tcp:") or value.startswith("udp:")
        ):
            value = [value[4:]]
        elif self.impl_get_extra("_allow_range") and ":" in str(value):
            value = value.split(":")
            if len(value) != 2:
                raise ValueError(_("range must have two values only"))
            if not value[0] < value[1]:
                raise ValueError(
                    _("first port in range must be" " smaller than the second one")
                )
        else:
            value = [value]

        for val in value:
            if not self.port_re.search(val):
                raise ValueError()

    def second_level_validation(self, value: str, warnings_only: bool) -> None:
        if self.impl_get_extra("_allow_protocol") and (
            value.startswith("tcp:") or value.startswith("udp:")
        ):
            value = [value[4:]]
        elif ":" in value:
            value = value.split(":")
        else:
            value = [value]
        for val in value:
            val = int(val)
            if (
                not self.impl_get_extra("_min_value")
                <= val
                <= self.impl_get_extra("_max_value")
            ):
                if warnings_only:
                    msg = _("should be between {0} and {1}")
                else:
                    msg = _("must be between {0} and {1}")
                raise ValueError(
                    msg.format(
                        self.impl_get_extra("_min_value"),
                        self.impl_get_extra("_max_value"),
                    )
                )
