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
"""URLOption to check url value
"""
import re
from typing import Any, Optional, List, Dict

from ..setting import undefined
from ..i18n import _
from .option import Calculation
from .stroption import StrOption
from .domainnameoption import DomainnameOption
from .portoption import PortOption


class URLOption(StrOption):
    """URLOption to check url value"""

    __slots__ = tuple()
    path_re = re.compile(r"^[A-Za-z0-9\-\._~:/\?#\[\]@!%\$&\'\(\)\*\+,;=]+$")
    _type = "URL"

    def __init__(
        self,
        name: str,
        doc: str,
        *args,
        allow_ip: bool = False,
        type: str = "domainname",
        allow_without_dot=False,
        allow_range: bool = False,
        allow_zero: bool = False,
        allow_wellknown: bool = True,
        allow_registred: bool = True,
        allow_private: bool = False,
        **kwargs,
    ) -> None:
        # pylint: disable=too-many-arguments,too-many-locals,redefined-builtin
        extra = {
            "_domainname": DomainnameOption(
                name,
                doc,
                allow_ip=allow_ip,
                type=type,
                allow_without_dot=allow_without_dot,
            ),
            "_port": PortOption(
                name,
                doc,
                allow_range=allow_range,
                allow_zero=allow_zero,
                allow_wellknown=allow_wellknown,
                allow_registred=allow_registred,
                allow_private=allow_private,
            ),
        }
        super().__init__(
            name,
            doc,
            extra=extra,
            *args,
            **kwargs,
        )

    def _get_domain_port_files(self, value: str) -> (str, str):
        if value.startswith("http://"):
            type_ = "http"
            value = value[7:]
        elif value.startswith("https://"):
            type_ = "https"
            value = value[8:]
        else:
            raise ValueError(_("must start with http:// or " "https://"))
        # get domain/files
        splitted = value.split("/", 1)
        if len(splitted) == 1:
            domain = value
            files = None
        else:
            domain, files = splitted
        # if port in domain
        splitted = domain.split(":", 1)
        if len(splitted) == 1:
            domain = splitted[0]
            port = {"http": "80", "https": "443"}[type_]
        else:
            domain, port = splitted
        return domain, port, files

    def validate(self, value: str) -> None:
        super().validate(value)
        domain, port, files = self._get_domain_port_files(value)
        # validate port
        portoption = self.impl_get_extra("_port")
        portoption.validate(port)
        # validate domainname
        domainnameoption = self.impl_get_extra("_domainname")
        domainnameoption.validate(domain)
        # validate files
        if files is not None and files != "" and not self.path_re.search(files):
            raise ValueError(_("must ends with a valid resource name"))

    def second_level_validation(self, value, warnings_only):
        domain, port, _ = self._get_domain_port_files(value)
        # validate port
        portoption = self.impl_get_extra("_port")
        portoption.second_level_validation(port, warnings_only)
        # validate domainname
        domainnameoption = self.impl_get_extra("_domainname")
        domainnameoption.second_level_validation(domain, warnings_only)
