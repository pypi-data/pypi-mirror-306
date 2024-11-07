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
"""DomainnameOption
"""
import re
from ipaddress import ip_interface
from typing import Any, Optional, List

from ..i18n import _
from ..setting import undefined
from .ipoption import IPOption
from .stroption import StrOption
from .networkoption import NetworkOption
from .option import Calculation


class DomainnameOption(StrOption):
    """represents the choice of a domain name
    netbios: for MS domain
    hostname: to identify the device
    domainname:
    fqdn: with tld, not supported yet
    """

    __slots__ = tuple()
    _type = "domain name"

    def __init__(
        self,
        name: str,
        doc: str,
        *args,
        allow_ip: bool = False,
        allow_cidr_network: bool = False,
        type: str = "domainname",
        allow_without_dot: bool = False,
        allow_startswith_dot: bool = False,
        **kwargs,
    ) -> None:
        # pylint: disable=too-many-branches,too-many-locals,too-many-arguments
        if type not in ["netbios", "hostname", "domainname"]:
            raise ValueError(_("unknown type {0} for hostname").format(type))
        extra = {"_dom_type": type}
        if not isinstance(allow_ip, bool):
            raise ValueError(_("allow_ip must be a boolean"))
        if not isinstance(allow_cidr_network, bool):
            raise ValueError(_("allow_cidr_network must be a boolean"))
        if not isinstance(allow_without_dot, bool):
            raise ValueError(_("allow_without_dot must be a boolean"))
        if not isinstance(allow_startswith_dot, bool):
            raise ValueError(_("allow_startswith_dot must be a boolean"))
        extra["_allow_without_dot"] = allow_without_dot
        if type == "domainname":
            if allow_without_dot:
                min_time = 0
            else:
                min_time = 1
            regexp = r"((?!-)[a-z0-9-]{{{1},{0}}}\.){{{1},}}[a-z0-9-]{{1,{0}}}".format(
                self._get_len(type), min_time
            )
        else:
            regexp = r"((?!-)[a-z0-9-]{{1,{0}}})".format(self._get_len(type))
        msg = _(
            'must start with lowercase characters followed by lowercase characters, number, "-" and "." characters are allowed'
        )
        msg_warning = _(
            'must start with lowercase characters followed by lowercase characters, number, "-" and "." characters are recommanded'
        )
        if allow_ip:
            msg = _("could be a IP, otherwise {}").format(msg)
            msg_warning = _("could be a IP, otherwise {}").format(msg_warning)
            if not allow_cidr_network:
                regexp = r"(?:{0}|(?:(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){{3}}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)))".format(
                    regexp
                )
            else:
                regexp = r"(?:{0}|(?:(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){{3}}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)/[0-9][0-9]))".format(
                    regexp
                )
        regexp = r"^{0}$".format(regexp)
        extra["_domain_re"] = re.compile(regexp)
        extra["_domain_re_message"] = msg
        extra["_domain_re_message_warning"] = msg_warning
        extra["_has_upper"] = re.compile("[A-Z]")
        if allow_ip:
            extra["_ip"] = IPOption(
                name,
                doc,
            )
        extra["_allow_ip"] = allow_ip
        if allow_cidr_network:
            extra["_network"] = NetworkOption(
                name,
                doc,
                cidr=True,
            )
        extra["_allow_cidr_network"] = allow_cidr_network
        extra["_allow_startswith_dot"] = allow_startswith_dot

        super().__init__(
            name,
            doc,
            *args,
            extra=extra,
            **kwargs,
        )

    def _get_len(self, type_):
        if type_ == "netbios":
            return 15
        return 63

    def _validate_domain(self, value: str) -> None:
        def _valid_length(val):
            if len(val) < 1:
                raise ValueError(_("invalid length (min 1)"))
            if len(val) > part_name_length:
                raise ValueError(
                    _("invalid length (max {0})" "").format(part_name_length)
                )

        part_name_length = self._get_len(self.impl_get_extra("_dom_type"))
        if self.impl_get_extra("_dom_type") == "domainname":
            if not self.impl_get_extra("_allow_without_dot") and not "." in value:
                raise ValueError(_("must have dot"))
            if len(value) > 255:
                raise ValueError(_("invalid length (max 255)"))
            if self.impl_get_extra("_allow_startswith_dot") and value.startswith("."):
                val = value[1:]
            else:
                val = value
            if val.endswith("."):
                nval = val[:-1]
            else:
                nval = val
            for dom in nval.split("."):
                _valid_length(dom)
        else:
            _valid_length(value)

    def _validate_ip_network(self, value: str) -> None:
        allow_ip = self.impl_get_extra("_allow_ip")
        allow_cidr_network = self.impl_get_extra("_allow_cidr_network")
        if allow_ip is False and allow_cidr_network is False:
            raise ValueError(_("must not be an IP"))
        if allow_ip is True:
            try:
                self.impl_get_extra("_ip").validate(value)
                return
            except ValueError as err:
                if allow_cidr_network is False:
                    raise err
        if allow_cidr_network is True:
            self.impl_get_extra("_network").validate(value)

    def validate(self, value: str) -> None:
        super().validate(value)
        try:
            # check if it's an IP or network
            ip_interface(value)
        except ValueError:
            self._validate_domain(value)
        else:
            self._validate_ip_network(value)

    def _second_level_validation_domain(self, value: str, warnings_only: bool) -> None:
        if self.impl_get_extra("_has_upper").search(value):
            raise ValueError(_("some characters are uppercase"))
        if self.impl_get_extra("_allow_startswith_dot") and value.startswith("."):
            val = value[1:]
        else:
            val = value
        if val.endswith("."):
            nval = val[:-1]
        else:
            nval = val
        if not self.impl_get_extra("_domain_re").search(nval):
            if warnings_only:
                raise ValueError(self.impl_get_extra("_domain_re_message_warning"))
            raise ValueError(self.impl_get_extra("_domain_re_message"))

    def _second_level_validation_ip_network(
        self, value: str, warnings_only: bool
    ) -> None:
        allow_ip = self.impl_get_extra("_allow_ip")
        allow_cidr_network = self.impl_get_extra("_allow_cidr_network")
        # it's an IP so validate with IPOption
        if allow_ip is True and allow_cidr_network is False:
            try:
                self.impl_get_extra("_ip").second_level_validation(value, warnings_only)
                return
            except ValueError as err:
                raise err
        if allow_cidr_network is True:
            self.impl_get_extra("_network").second_level_validation(
                value, warnings_only
            )

    def second_level_validation(self, value: str, warnings_only: bool) -> None:
        try:
            # check if it's an IP or network
            ip_interface(value)
        except ValueError:
            self._second_level_validation_domain(value, warnings_only)
        else:
            self._second_level_validation_ip_network(value, warnings_only)
