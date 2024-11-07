# Copyright (C) 2018-2024 Team tiramisu (see AUTHORS for all contributors)
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
"""some functions to validates or calculates value
"""
from typing import Any, List, Optional
from operator import add, mul, sub, truediv
from ipaddress import ip_address, ip_interface, ip_network
from .i18n import _
from .setting import undefined
from .error import display_list


FUNCTION_WAITING_FOR_DICT = []
FUNCTION_WAITING_FOR_ERROR = []


def function_waiting_for_dict(function):
    """functions (calculation or validation) receive by default only the value of other options
    all functions declared with this function recieve a dict with option informations
    (value, name, ...)
    """
    name = function.__name__
    if name not in FUNCTION_WAITING_FOR_DICT:
        FUNCTION_WAITING_FOR_DICT.append(name)
    return function


def function_waiting_for_error(function):
    """functions (calculation or validation) receive by default only the value of other options
    set PropertyError too
    """
    name = function.__name__
    if name not in FUNCTION_WAITING_FOR_ERROR:
        FUNCTION_WAITING_FOR_ERROR.append(name)
    return function


@function_waiting_for_dict
def valid_network_netmask(
    network: dict,
    netmask: dict,
):
    """
    validates if network and netmask are coherent
    this validator must be set to netmask option
    """
    if None in [network["value"], netmask["value"]]:
        return
    try:
        ip_network(f'{network["value"]}/{netmask["value"]}')
    except ValueError as err:
        raise ValueError(
            _('network "{0}" ({1}) does not match with this netmask').format(
                network["value"], network["name"]
            )
        ) from err


@function_waiting_for_dict
def valid_ip_netmask(
    ip: dict,  # pylint: disable=invalid-name
    netmask: dict,
):
    """validates if ip and netmask are coherent
    this validator must be set to netmask option
    """
    if None in [ip["value"], netmask["value"]]:
        return
    ip_netmask = ip_interface(f'{ip["value"]}/{netmask["value"]}')
    if ip_netmask.ip == ip_netmask.network.network_address:
        msg = _('IP "{0}" ({1}) with this netmask is in fact a network address').format(
            ip["value"], ip["name"]
        )
        raise ValueError(msg)
    if ip_netmask.ip == ip_netmask.network.broadcast_address:
        msg = _(
            'IP "{0}" ({1}) with this netmask is in fact a broadcast address'
        ).format(ip["value"], ip["name"])
        raise ValueError(msg)


@function_waiting_for_dict
def valid_broadcast(
    network: dict,
    netmask: dict,
    broadcast: dict,
):
    """validates if the broadcast is coherent with network and netmask"""
    if None in [network["value"], netmask["value"], broadcast["value"]]:
        return
    if ip_network(
        f'{network["value"]}/{netmask["value"]}'
    ).broadcast_address != ip_address(broadcast["value"]):
        msg = _(
            "broadcast invalid with network {0} ({1}) and netmask {2} ({3})"
        ).format(network["value"], network["name"], netmask["value"], netmask["name"])
        raise ValueError(msg)


@function_waiting_for_dict
def valid_in_network(
    ip: dict,  # pylint: disable=invalid-name
    network: dict,
    netmask=Optional[dict],
):
    """validates if an IP is in a network
    this validator must be set to ip option
    """
    if None in [ip["value"], network["value"]]:
        return
    if "/" in network["value"]:
        # it's a CIDR network
        network_value = network["value"]
    else:
        if netmask is None or netmask["value"] is None:
            return
        network_value = f'{network["value"]}/{netmask["value"]}'
    network_obj = ip_network(network_value)
    ip_netmask = ip_interface(f'{ip["value"]}/{network_obj.netmask}')
    if ip_netmask not in network_obj:
        if netmask is None:
            msg = _('this IP is not in network {network["value"]} ({network["name"]})')
        else:
            msg = _(
                'this IP is not in network {network["value"]} ({network["name"]}) '
                'with netmask {netmask["value"]} ({netmask["name"]})'
            )
        raise ValueError(msg)
    # test if ip is not network/broadcast IP
    if ip_netmask.ip == ip_netmask.network.network_address:
        msg = _(
            "this IP with the network {0} ({1}) is in fact a network address"
        ).format(network["value"], network["name"])
        raise ValueError(msg)
    if ip_netmask.ip == ip_netmask.network.broadcast_address:
        msg = _(
            "this IP with the network {0} ({1}) is in fact a broadcast address"
        ).format(network["value"], network["value"])
        raise ValueError(msg)


@function_waiting_for_dict
def valid_not_equal(*values):
    """valid that two options have not same value"""
    equal = set()
    for val in values[1:]:
        if "propertyerror" in val:
            continue
        if values[0]["value"] == val["value"] is not None:
            equal.add(val["name"])
    if not equal:
        return
    msg = _("value is identical to {0}").format(
        display_list(list(equal), add_quote=True)
    )
    raise ValueError(msg)


class CalcValue:
    """class to calc_value with different functions"""

    # pylint: disable=too-many-instance-attributes
    def __call__(
        self,
        *args: List[Any],
        multi: bool = False,
        default: Any = undefined,
        condition: Any = undefined,
        no_condition_is_invalid: bool = False,
        expected: Any = undefined,
        condition_operator: str = "AND",
        reverse_condition: bool = False,
        allow_none: bool = False,
        remove_duplicate_value: bool = False,
        join: Optional[str] = None,
        min_args_len: Optional[int] = None,
        operator: Optional[str] = None,
        index: Optional[int] = None,
        **kwargs,
    ) -> Any:
        # pylint: disable=too-many-statements,too-many-branches,too-many-nested-blocks,too-many-locals
        """calculate value
        :param args: list of value
        :param multi: value returns must be a list of value
        :param default: default value if condition is not matched or if args is empty
                        if there is more than one default value, set default_0, default_1, ...
        :param condition: test if condition is equal to expected value
                          if there is more than one condition, set condition_0, condition_1, ...
        :param expected: value expected for all conditions
                         if expected value is different between condition, set expected_0,
                         expected_1, ...
        :param no_condition_is_invalid: if no condition and not condition_0, condition_1, ... (for
                                        example if option is disabled) consider that condition not
                                        matching
        :param condition_operator: OR or AND operator for condition
        :param allow_none: if False, do not return list in None is present in list
        :param remove_duplicate_value: if True, remote duplicated value
        :param join: join all args with specified characters
        :param min_args_len: if number of arguments is smaller than this value, return default value
        :param operator: 'add', 'mul', 'div' or 'sub' all args (args must be integer value)
        :param index: index for follower

        examples:
        * you want to copy value from an option to an other option:
        >>> from tiramisu import calc_value, StrOption, OptionDescription, Config, \
        ...                      Params, ParamOption
        >>> val1 = StrOption('val1', '', 'val1')
        >>> val2 = StrOption('val2', '', callback=calc_value,
        ...                  callback_params=Params(ParamOption(val1)))
        >>> od = OptionDescription('root', '', [val1, val2])
        >>> cfg = Config(od)
        >>> cfg.value.dict()
        {'val1': 'val1', 'val2': 'val1'}

        * you want to copy values from two options in one multi option
        >>> from tiramisu import calc_value, StrOption, OptionDescription, Config, Params, \
        ...                      ParamOption, ParamValue
        >>> val1 = StrOption('val1', "", 'val1')
        >>> val2 = StrOption('val2', "", 'val2')
        >>> val3 = StrOption('val3', "", multi=True, callback=calc_value,
        ...                  callback_params=Params((ParamOption(val1), ParamOption(val2)),
        ...                  multi=ParamValue(True)))
        >>> od = OptionDescription('root', '', [val1, val2, val3])
        >>> cfg = Config(od)
        >>> cfg.value.dict()
        {'val1': 'val1', 'val2': 'val2', 'val3': ['val1', 'val2']}

        * you want to copy a value from an option if it not disabled, otherwise set 'default_value'
        >>> from tiramisu import calc_value, StrOption, OptionDescription, Config, Params, \
        ...                      ParamOption, ParamValue
        >>> val1 = StrOption('val1', '', 'val1')
        >>> val2 = StrOption('val2', '', callback=calc_value,
        ...                  callback_params=Params(ParamOption(val1, True),
        ...                  default=ParamValue('default_value')))
        >>> od = OptionDescription('root', '', [val1, val2])
        >>> cfg = Config(od)
        >>> cfg.property.read_write()
        >>> cfg.value.dict()
        {'val1': 'val1', 'val2': 'val1'}
        >>> cfg.option('val1').property.add('disabled')
        >>> cfg.value.dict()
        {'val2': 'default_value'}

        * you want to copy value from an option if an other is True, otherwise set 'default_value'
        >>> from tiramisu import calc_value, BoolOption, StrOption, OptionDescription, Config, \
        ...                      Params, ParamOption, ParamValue
        >>> boolean = BoolOption('boolean', '', True)
        >>> val1 = StrOption('val1', '', 'val1')
        >>> val2 = StrOption('val2', '', callback=calc_value,
        ...                  callback_params=Params(ParamOption(val1, True),
        ...                                         default=ParamValue('default_value'),
        ...                                         condition=ParamOption(boolean),
        ...                                         expected=ParamValue(True)))
        >>> od = OptionDescription('root', '', [boolean, val1, val2])
        >>> cfg = Config(od)
        >>> cfg.property.read_write()
        >>> cfg.value.dict()
        {'boolean': True, 'val1': 'val1', 'val2': 'val1'}
        >>> cfg.option('boolean').value.set(False)
        >>> cfg.value.dict()
        {'boolean': False, 'val1': 'val1', 'val2': 'default_value'}

        * you want to copy option even if None is present
        >>> from tiramisu import calc_value, StrOption, OptionDescription, Config, Params, \
        ...                      ParamOption, ParamValue
        >>> val1 = StrOption('val1', "", 'val1')
        >>> val2 = StrOption('val2', "")
        >>> val3 = StrOption('val3', "", multi=True, callback=calc_value,
        ...                  callback_params=Params((ParamOption(val1), ParamOption(val2)),
        ...                  multi=ParamValue(True), allow_none=ParamValue(True)))
        >>> od = OptionDescription('root', '', [val1, val2, val3])
        >>> cfg = Config(od)
        >>> cfg.value.dict()
        {'val1': 'val1', 'val2': None, 'val3': ['val1', None]}

        * you want uniq value
        >>> from tiramisu import calc_value, StrOption, OptionDescription, Config, Params, \
        ...                      ParamOption, ParamValue
        >>> val1 = StrOption('val1', "", 'val1')
        >>> val2 = StrOption('val2', "", 'val1')
        >>> val3 = StrOption('val3', "", multi=True, callback=calc_value,
        ...                  callback_params=Params((ParamOption(val1), ParamOption(val2)),
        ...                  multi=ParamValue(True), remove_duplicate_value=ParamValue(True)))
        >>> od = OptionDescription('root', '', [val1, val2, val3])
        >>> cfg = Config(od)
        >>> cfg.value.dict()
        {'val1': 'val1', 'val2': 'val1', 'val3': ['val1']}

        * you want to join two values with '.'
        >>> from tiramisu import calc_value, StrOption, OptionDescription, Config, Params, \
        ...                      ParamOption, ParamValue
        >>> val1 = StrOption('val1', "", 'val1')
        >>> val2 = StrOption('val2', "", 'val2')
        >>> val3 = StrOption('val3', "", callback=calc_value,
        ...                  callback_params=Params((ParamOption(val1),
        ...                  ParamOption(val2)), join=ParamValue('.')))
        >>> od = OptionDescription('root', '', [val1, val2, val3])
        >>> cfg = Config(od)
        >>> cfg.value.dict()
        {'val1': 'val1', 'val2': 'val2', 'val3': 'val1.val2'}

        * you want join three values, only if almost three values are set
        >>> from tiramisu import calc_value, StrOption, OptionDescription, Config, Params, \
        ...                      ParamOption, ParamValue
        >>> val1 = StrOption('val1', "", 'val1')
        >>> val2 = StrOption('val2', "", 'val2')
        >>> val3 = StrOption('val3', "", 'val3')
        >>> val4 = StrOption('val4', "", callback=calc_value,
        ...                              callback_params=Params((ParamOption(val1),
        ...                                                      ParamOption(val2),
        ...                                                      ParamOption(val3, True)),
        ...                              join=ParamValue('.'), min_args_len=ParamValue(3)))
        >>> od = OptionDescription('root', '', [val1, val2, val3, val4])
        >>> cfg = Config(od)
        >>> cfg.property.read_write()
        >>> cfg.value.dict()
        {'val1': 'val1', 'val2': 'val2', 'val3': 'val3', 'val4': 'val1.val2.val3'}
        >>> cfg.option('val3').property.add('disabled')
        >>> cfg.value.dict()
        {'val1': 'val1', 'val2': 'val2', 'val4': ''}

        * you want to add all values
        >>> from tiramisu import calc_value, IntOption, OptionDescription, Config, Params, \
        ...                      ParamOption, ParamValue
        >>> val1 = IntOption('val1', "", 1)
        >>> val2 = IntOption('val2', "", 2)
        >>> val3 = IntOption('val3', "", callback=calc_value,
        ...                              callback_params=Params((ParamOption(val1),
                                                                 ParamOption(val2)),
        ...                              operator=ParamValue('add')))
        >>> od = OptionDescription('root', '', [val1, val2, val3])
        >>> cfg = Config(od)
        >>> cfg.value.dict()
        {'val1': 1, 'val2': 2, 'val3': 3}

        """
        # pylint: disable=attribute-defined-outside-init
        self.args = args
        self.condition = condition
        self.expected = expected
        self.condition_operator = condition_operator
        self.reverse_condition = reverse_condition
        self.kwargs = kwargs
        self.no_condition_is_invalid = (
            no_condition_is_invalid  # pylint: disable=attribute-defined-outside-init
        )
        value = self.get_value(
            default,
            min_args_len,
        )
        if not multi:
            if join is not None:
                if None not in value:
                    value = join.join(value)
                else:
                    value = None
            elif value and operator:
                new_value = value[0]
                oper = {
                    "mul": mul,
                    "add": add,
                    "div": truediv,
                    "sub": sub,
                }[operator]
                for val in value[1:]:
                    new_value = oper(new_value, val)
                value = new_value
            elif value == []:
                value = None
            else:
                value = value[0]
                if isinstance(value, list) and index is not None:
                    if len(value) > index:
                        value = value[index]
                    else:
                        value = None
        else:
            if join is not None:
                if None not in value:
                    length_val = None
                    for val in value:
                        if isinstance(val, list):
                            if None in val:
                                length_val = None
                                break
                            lval = len(val)
                            if length_val is not None and length_val != lval:
                                msg = _(
                                    'unexpected value in calc_value with join attribute "{0}" with invalid length "{1}"'
                                ).format(val, length_val)
                                raise ValueError(msg)
                            length_val = lval
                    new_value = []
                    if length_val is not None:
                        for idx in range(length_val):
                            idx_val = []
                            for val in value:
                                if isinstance(val, list):
                                    idx_val.append(val[idx])
                                else:
                                    idx_val.append(val)
                            new_value.append(join.join(idx_val))
                    value = new_value
                else:
                    value = []
            elif None in value and not allow_none:
                value = []
            if remove_duplicate_value:
                new_value = []
                for val in value:
                    if val not in new_value:
                        new_value.append(val)
                value = new_value
        return value

    def value_from_kwargs(
        self, value: Any, pattern: str, to_dict: bool = False, empty_test=undefined
    ) -> Any:
        """get value from kwargs"""
        # pylint: disable=too-many-branches
        # if value attribute exist return it's value
        # otherwise pattern_0, pattern_1, ...
        # otherwise undefined
        if value is not empty_test:
            if to_dict == "all":
                returns = {None: value}
            else:
                returns = value
        else:
            kwargs_matches = {}
            len_pattern = len(pattern)
            for key, pattern_value in self.kwargs.items():
                if key.startswith(pattern):
                    index = int(key[len_pattern:])
                    if isinstance(pattern_value, dict):
                        pattern_value = pattern_value["value"]
                    kwargs_matches[index] = pattern_value
            if not kwargs_matches:
                returns = undefined
            else:
                keys = sorted(kwargs_matches)
                if to_dict:
                    returns = {}
                else:
                    returns = []
                for key in keys:
                    if to_dict:
                        returns[key] = kwargs_matches[key]
                    else:
                        returns.append(kwargs_matches[key])
        return returns

    def is_condition_matches(
        self,
        condition_value,
    ):
        """verify the condition"""
        # pylint: disable=too-many-branches
        calculated_conditions = self.value_from_kwargs(
            condition_value,
            "condition_",
            to_dict="all",
        )
        if calculated_conditions is undefined:
            is_matches = not self.no_condition_is_invalid
        else:
            is_matches = None
            calculated_expected = self.value_from_kwargs(
                self.expected,
                "expected_",
                to_dict=True,
            )
            calculated_reverse = self.value_from_kwargs(
                self.reverse_condition,
                "reverse_condition_",
                to_dict=True,
                empty_test=False,
            )
            for idx, calculated_condition in calculated_conditions.items():
                if isinstance(calculated_expected, dict):
                    if idx is not None:
                        if isinstance(calculated_expected[idx], list):
                            current_matches = (
                                calculated_condition in calculated_expected[idx]
                            )
                        else:
                            current_matches = (
                                calculated_condition == calculated_expected[idx]
                            )
                    else:
                        current_matches = (
                            calculated_condition in calculated_expected.values()
                        )
                else:
                    current_matches = calculated_condition == calculated_expected
                if isinstance(calculated_reverse, dict) and idx in calculated_reverse:
                    reverse_condition = calculated_reverse[idx]
                else:
                    reverse_condition = False
                if is_matches is None:
                    is_matches = current_matches
                if self.condition_operator == "AND":
                    is_matches = is_matches and current_matches
                    if reverse_condition:
                        is_matches = not is_matches
                    if not is_matches:
                        break
                elif self.condition_operator == "OR":
                    is_matches = is_matches or current_matches
                    if reverse_condition:
                        is_matches = not is_matches
                    if is_matches:
                        break
                else:
                    msg = _(
                        "unexpected {0} condition_operator " "in calc_value"
                    ).format(self.condition_operator)
                    raise ValueError(msg)
            is_matches = (
                is_matches
                and not self.reverse_condition
                or not is_matches
                and self.reverse_condition
            )
        return is_matches

    def get_value(
        self,
        default,
        min_args_len,
    ):
        """get the value from arguments"""
        # retrieve the condition
        if isinstance(self.condition, dict):
            if "value" in self.condition:
                condition_value = self.condition["value"]
            else:
                condition_value = undefined
        else:
            condition_value = self.condition
        # value is empty if condition doesn't match
        # otherwise value is arg
        if not self.is_condition_matches(condition_value):
            value = []
        else:
            value = self.get_args()
        if min_args_len and not len(value) >= min_args_len:
            value = []
        if not value:
            # default value
            new_default = self.value_from_kwargs(
                default,
                "default_",
            )
            if new_default is not undefined:
                if not isinstance(new_default, list):
                    value = [new_default]
                else:
                    value = new_default
        return value

    def get_args(self):
        """get all arguments"""
        return list(self.args)


class CalcValuePropertyHelp(CalcValue):
    """special class to display property error"""

    def get_name(self):
        """get the condition name"""
        return self.condition["name"]

    def get_indexed_name(self, index: int) -> str:
        """get name for a specified index"""
        condition_index = self.kwargs.get(f"condition_{index}")
        if condition_index is not None and not isinstance(condition_index, dict):
            raise ValueError(
                _('unexpected condition_{0} must have "todict" argument').format(index)
            )
        return condition_index["name"]

    def build_property_message(
        self,
        name: str,
        value: Any,
    ) -> str:
        """prepare message to display error message if needed"""
        if not self.reverse_condition:
            msg = _('the value of "{0}" is {1}').format(name, value)
        else:
            msg = _('the value of "{0}" is not {1}').format(name, value)
        return msg

    def get_args(self):
        args = super().get_args()
        action = args[0]
        calculated_expected = self.value_from_kwargs(
            self.expected, "expected_", to_dict=True
        )
        if self.condition is not undefined:
            if "propertyerror" in self.condition:
                msg = self.condition["propertyerror"]
            else:
                name = self.get_name()
                if isinstance(calculated_expected, dict):
                    calc_values = calculated_expected.values()
                else:
                    calc_values = [calculated_expected]
                display_value = display_list(
                    [str(val) for val in calc_values], separator="or", add_quote=True
                )
                msg = self.build_property_message(name, display_value)
        else:
            msgs = []
            for key, value in calculated_expected.items():
                name = self.get_indexed_name(key)
                msgs.append(self.build_property_message(name, f'"{value}"'))
            msg = display_list(msgs, separator=self.condition_operator.lower())
        return [(action, f'"{action}" ({msg})')]


calc_value = CalcValue()
calc_value.__name__ = "calc_value"  # pylint: disable=attribute-defined-outside-init
# function_waiting_for_dict(calc_value)
calc_value_property_help = CalcValuePropertyHelp()
calc_value_property_help.__name__ = (
    "calc_value_property_help"  # pylint: disable=attribute-defined-outside-init
)
function_waiting_for_dict(calc_value_property_help)
