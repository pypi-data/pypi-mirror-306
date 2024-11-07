# -*- coding: utf-8 -*-
# Copyright (C) 2014-2024 Team tiramisu (see AUTHORS for all contributors)
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
"""all official option
"""
from .optiondescription import OptionDescription
from .dynoptiondescription import DynOptionDescription
from .leadership import Leadership
from .baseoption import submulti
from .symlinkoption import SymLinkOption

# from .syndynoption import SynDynOption, SynDynOptionDescription, SynDynLeadership
from .option import Option
from .choiceoption import ChoiceOption
from .booloption import BoolOption
from .intoption import IntOption
from .floatoption import FloatOption
from .stroption import StrOption, RegexpOption
from .ipoption import IPOption
from .portoption import PortOption
from .networkoption import NetworkOption
from .netmaskoption import NetmaskOption
from .broadcastoption import BroadcastOption
from .domainnameoption import DomainnameOption
from .emailoption import EmailOption
from .urloption import URLOption
from .usernameoption import UsernameOption, GroupnameOption
from .dateoption import DateOption
from .filenameoption import FilenameOption
from .passwordoption import PasswordOption
from .macoption import MACOption
from .permissionsoption import PermissionsOption


__all__ = (
    "Leadership",
    "OptionDescription",
    "DynOptionDescription",
    #           'SynDynOptionDescription', 'SynDynLeadership','SynDynOption',
    "Option",
    "SymLinkOption",
    "ChoiceOption",
    "BoolOption",
    "DateOption",
    "IntOption",
    "FloatOption",
    "StrOption",
    "IPOption",
    "PortOption",
    "NetworkOption",
    "NetmaskOption",
    "BroadcastOption",
    "DomainnameOption",
    "EmailOption",
    "URLOption",
    "UsernameOption",
    "GroupnameOption",
    "FilenameOption",
    "PasswordOption",
    "submulti",
    "RegexpOption",
    "MACOption",
    "PermissionsOption",
)
