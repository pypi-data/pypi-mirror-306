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
"""IPOption
"""
from ipaddress import ip_address, ip_interface

from ..i18n import _
from .stroption import StrOption


class IPOption(StrOption):
    """represents the choice of an ip"""

    __slots__ = tuple()
    _type = "IP"

    def __init__(
        self,
        *args,
        private_only=False,
        allow_reserved=False,
        cidr=False,
        extra=None,
        **kwargs,
    ):
        if extra is None:
            extra = {}
        extra["_private_only"] = private_only
        extra["_allow_reserved"] = allow_reserved
        extra["_cidr"] = cidr
        super().__init__(*args, extra=extra, **kwargs)

    def _validate_cidr(self, value):
        try:
            ip_obj = ip_interface(value)
        except ValueError as err:
            raise ValueError() from err
        if ip_obj.ip == ip_obj.network.network_address:
            raise ValueError(_("it's in fact a network address"))
        if ip_obj.ip == ip_obj.network.broadcast_address:
            raise ValueError(_("it's in fact a broacast address"))

    def _validate_ip(self, value):
        try:
            str(ip_address(value))
        except ValueError as err:
            raise ValueError() from err

    def validate(self, value: str) -> None:
        super().validate(value)
        if self.impl_get_extra("_cidr"):
            if "/" not in value:
                raise ValueError(_('CIDR address must have a "/"'))
            self._validate_cidr(value)
        else:
            self._validate_ip(value)

    def second_level_validation(self, value: str, warnings_only: bool) -> None:
        ip_obj = ip_interface(value)
        if not self.impl_get_extra("_allow_reserved") and ip_obj.is_reserved:
            if warnings_only:
                msg = _("shouldn't be reserved IP")
            else:
                msg = _("mustn't be reserved IP")
            raise ValueError(msg)
        if self.impl_get_extra("_private_only") and not ip_obj.is_private:
            if warnings_only:
                msg = _("should be private IP")
            else:
                msg = _("must be private IP")
            raise ValueError(msg)
