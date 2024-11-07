# Copyright (C) 2012-2024 Team tiramisu (see AUTHORS for all contributors)
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
"""Configuration management library written in python
"""
from .function import (
    calc_value,
    calc_value_property_help,
    valid_ip_netmask,
    valid_network_netmask,
    valid_in_network,
    valid_broadcast,
    valid_not_equal,
    function_waiting_for_dict,
    function_waiting_for_error,
)
from .autolib import (
    Calculation,
    Params,
    ParamOption,
    ParamDynOption,
    ParamSelfOption,
    ParamValue,
    ParamIndex,
    ParamIdentifier,
    ParamInformation,
    ParamSelfInformation,
)
from .option import *
from .error import ConfigError
from .api import Config, MetaConfig, GroupConfig, MixConfig
from .option import __all__ as all_options
from .setting import owners, groups, undefined


allfuncs = [
    "Calculation",
    "Params",
    "ParamOption",
    "ParamDynOption",
    "ParamSelfOption",
    "ParamValue",
    "ParamIndex",
    "ParamIdentifier",
    "ParamInformation",
    "ParamSelfInformation",
    "MetaConfig",
    "MixConfig",
    "GroupConfig",
    "Config",
    "ConfigError",
    "undefined",
    "owners",
    "groups",
    "calc_value",
    "calc_value_property_help",
    "valid_ip_netmask",
    "valid_network_netmask",
    "valid_in_network",
    "valid_broadcast",
    "function_waiting_for_dict",
    "function_waiting_for_error",
]
allfuncs.extend(all_options)
del all_options
__all__ = tuple(allfuncs)
del allfuncs
__version__ = "4.1.0"
