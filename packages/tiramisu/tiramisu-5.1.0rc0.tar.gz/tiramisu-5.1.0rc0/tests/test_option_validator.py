from .autopath import do_autopath
do_autopath()

import warnings
import pytest

from tiramisu import BoolOption, StrOption, IPOption, NetmaskOption, NetworkOption, BroadcastOption, \
        IntOption, OptionDescription, Leadership, Config, Params, ParamValue, ParamOption, \
        ParamSelfOption, ParamIndex, ParamInformation, ParamSelfInformation, ParamSelfOption, Calculation, \
        valid_ip_netmask, valid_network_netmask, \
        valid_in_network, valid_broadcast, valid_not_equal
from tiramisu.setting import groups
from tiramisu.error import ValueErrorWarning, ConfigError, PropertiesOptionError
from tiramisu.i18n import _
from .config import config_type, get_config


msg_err = _('attention, "{0}" could be an invalid {1} for "{2}"')


def return_true(value, param=None):
    if value == 'val' and param in [None, 'yes']:
        return True
    raise ValueError('test error')


def return_false(value, param=None):
    if value == 'val' and param in [None, 'yes']:
        raise ValueError('test error return_false')


def return_val(value, param=None):
    return 'val'


def return_if_val(value):
    if value != 'val':
        raise ValueError('test error')


def value_values(value, values):
    if not (value == 'val' and values == ['val'] or
            value == 'val1' and values == ['val'] or
            value == 'val2' and values == ['val'] or
            value == 'val1' and values == ['val1'] or
            value == 'val1' and values == ['val1', 'val2'] or
            value == 'val2' and values == ['val1', 'val2'] or
            value == 'val1' and values == ['val1', None]):
        raise ValueError('error')


def value_values_index(value, values, index):
    value_values(value, values)
    if not (index == 0 or (value == 'val2' and index == 1)):
        raise ValueError('error 2')


def value_values_auto(value, values, auto=False):
    if auto != False:
        raise ValueError('auto should be False')
    if not (value == 'val' and values == ['val'] or
            value == 'val1' and values == ['val1'] or
            value == 'val2' and values == ['val1', 'val2'] or
            value == 'val1' and values == ['val1', None]):
        raise ValueError('error')


def value_values_auto2(value, values, auto=False):
    if auto != False:
        raise ValueError('auto should be False')
    if not (value == 'val1' and values == 'val' or
            value == 'val2' and values == 'val'):
        raise ValueError('error')



def value_empty(value, empty, values):
    if not value == 'val' or empty is not False and not values == ['val']:
        raise ValueError('error')


def test_validator(config_type):
    opt1 = StrOption('opt1', '', validators=[Calculation(return_true, Params(ParamSelfOption()))], default='val')
    opt2 = StrOption('opt2', '', validators=[Calculation(return_false, Params(ParamSelfOption()))])
    od1 = OptionDescription('root', '', [opt1, opt2])
    cfg_ori = Config(od1)
    cfg = get_config(cfg_ori, config_type)
    assert cfg.option('opt1').value.get() == 'val'
    assert cfg.option('opt2').value.valid() is True
    with pytest.raises(ValueError):
        cfg.option('opt2').value.set('val')
    try:
        cfg.option('opt2').value.set('val')
    except ValueError as err:
        msg = _('"{0}" is an invalid {1} for "{2}"').format('val', _('string'), 'opt2') + ', ' + _('test error return_false')
        assert str(err) == msg
        if config_type == 'tiramisu-api':
            msg = _('"{0}" is an invalid {1} for "{2}"').format('val', 'string', 'opt2') + ', ' + _('test error return_false')
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.property.add('demoting_error_warning')
    cfg = get_config(cfg_ori, config_type)
    warnings.simplefilter("always", ValueErrorWarning)
    with warnings.catch_warnings(record=True) as w:
        cfg.option('opt2').value.set('val')
    assert len(w) == 1
    assert str(w[0].message) == msg
    assert cfg.option('opt2').value.valid() is False
    #
    with warnings.catch_warnings(record=True) as w:
        cfg.option('opt2').value.get()
    assert len(w) == 1
    assert str(w[0].message) == msg
    assert cfg.option('opt2').value.valid() is False
    #
    with warnings.catch_warnings(record=True) as w:
        cfg.option('opt2').value.get()
    assert len(w) == 1
    assert str(w[0].message) == msg
    assert cfg.option('opt2').value.valid() is False
#    assert not list_sessions()


def test_validator_not_valid(config_type):
    with pytest.raises(ValueError):
        StrOption('not_a_list', '', validators=Calculation(return_true, Params(ParamSelfOption())), default='val')
    with pytest.raises(ValueError):
        StrOption('not_calculation', '', validators=[str])


def test_validator_params(config_type):
    opt1 = StrOption('opt1', '', validators=[Calculation(return_true, Params((ParamSelfOption(), ParamValue('yes'))))], default='val')
    opt2 = StrOption('opt2', '', validators=[Calculation(return_false, Params((ParamSelfOption(), ParamValue('yes'))))])
    od1 = OptionDescription('root', '', [opt1, opt2])
    cfg_ori = Config(od1)
    cfg = get_config(cfg_ori, config_type)
    assert cfg.option('opt1').value.get() == 'val'
    with pytest.raises(ValueError):
        cfg.option('opt2').value.set('val')
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.property.add('demoting_error_warning')
    cfg = get_config(cfg_ori, config_type)
    warnings.simplefilter("always", ValueErrorWarning)
    with warnings.catch_warnings(record=True) as w:
        cfg.option('opt2').value.set('val')
    assert len(w) == 1
#    assert not list_sessions()


def test_validator_params_value_values(config_type):
    opt1 = StrOption('opt1', '', validators=[Calculation(value_values, Params((ParamSelfOption(whole=False), ParamSelfOption())))], default=['val'], multi=True)
    od1 = OptionDescription('root', '', [opt1])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert cfg.option('opt1').value.get() == ['val']
    cfg.option('opt1').value.set(['val1', 'val2'])
#    assert not list_sessions()


def test_validator_params_value_values_index(config_type):
    opt1 = StrOption('opt1', '', validators=[Calculation(value_values_index, Params((ParamSelfOption(whole=False), ParamSelfOption(), ParamIndex())))], default=['val'], multi=True)
    od1 = OptionDescription('root', '', [opt1])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert cfg.option('opt1').value.get() == ['val']
    cfg.option('opt1').value.set(['val1', 'val2'])
#    assert not list_sessions()


def test_validator_params_value_values_leader(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip reseau autorise", multi=True, validators=[Calculation(value_values, Params((ParamSelfOption(whole=False), ParamSelfOption())))])
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-reseau", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('root', '', [interface1])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['val1', 'val2'])
#    assert not list_sessions()


def test_validator_params_value_values_index_leader(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip reseau autorise", multi=True, validators=[Calculation(value_values_index, Params((ParamSelfOption(whole=False), ParamSelfOption(), ParamIndex())))])
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-reseau", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('root', '', [interface1])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['val1', 'val2'])
#    assert not list_sessions()


def test_validator_params_value_values_follower(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip reseau autorise", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-reseau", multi=True, validators=[Calculation(value_values, Params((ParamSelfOption(), ParamSelfOption(whole=True))))])
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('root', '', [interface1])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['val'])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('val1')
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['val', 'val1'])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.set('val2')
#    assert not list_sessions()


def test_validator_params_value_values_index_follower(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip reseau autorise", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-reseau", multi=True, validators=[Calculation(value_values_index, Params((ParamSelfOption(), ParamSelfOption(whole=True), ParamIndex())))])
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('root', '', [interface1])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['val'])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('val1')
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['val', 'val1'])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.set('val2')
#    assert not list_sessions()


def test_validator_params_value_values_kwargs_empty(config_type):
    v = BoolOption('v', '', default=False)
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip reseau autorise", multi=True, default=["ip"])
    netmask_admin_eth0 = StrOption('netmask_admin_eth0',
                                   "masque du sous-reseau",
                                   multi=True,
                                   validators=[Calculation(value_empty, Params((ParamSelfOption(), ParamOption(v))))])
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('root', '', [v, interface1])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['ip']
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['ip', 'val'])
#    assert not list_sessions()


def test_validator_params_value_values_kwargs(config_type):
    v = BoolOption('v', '', default=False)
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip reseau autorise", multi=True, default=["ip"])
    netmask_admin_eth0 = StrOption('netmask_admin_eth0',
                                   "masque du sous-reseau",
                                   multi=True,
                                   validators=[Calculation(value_values_auto, Params((ParamSelfOption(), ParamSelfOption(whole=True)), kwargs={'auto': ParamOption(v)}))])
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('root', '', [v, interface1])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['ip']
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('val1')
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['ip', 'val'])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.set('val2')
#    assert not list_sessions()


def test_validator_params_value_values_kwargs_values(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip reseau autorise", multi=True, properties=('notunique',))
    netmask_admin_eth0 = StrOption('netmask_admin_eth0',
                                   "masque du sous-reseau",
                                   multi=True,
                                   validators=[Calculation(value_values_auto2, Params(ParamSelfOption(), kwargs={'values': ParamOption(ip_admin_eth0)}))])
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('root', '', [interface1])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['val'])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('val1')
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['val', 'val'])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.set('val2')
#    assert not list_sessions()


def test_validator_params_option(config_type):
    opt0 = StrOption('opt0', '', default='yes')
    opt1 = StrOption('opt1', '', validators=[Calculation(return_true, Params((ParamSelfOption(), ParamOption(opt0))))], default='val')
    od1 = OptionDescription('root', '', [opt0, opt1])
    cfg_ori = Config(od1)
    cfg = get_config(cfg_ori, config_type)
    assert cfg.option('opt1').value.get() == 'val'
    cfg.option('opt0').value.set('val')
    with pytest.raises(ValueError):
        cfg.option('opt1').value.get()
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.property.add('demoting_error_warning')
    cfg = get_config(cfg_ori, config_type)
    warnings.simplefilter("always", ValueErrorWarning)
    with warnings.catch_warnings(record=True) as w:
        cfg.option('opt1').value.get()
    assert len(w) == 1
#    assert not list_sessions()


def test_validator_multi(config_type):
    opt1 = StrOption('opt1', '', validators=[Calculation(return_if_val, Params(ParamSelfOption(whole=False)))], multi=True)
    od1 = OptionDescription('root', '', [opt1])
    cfg_ori = Config(od1)
    cfg = get_config(cfg_ori, config_type)
    assert cfg.option('opt1').value.get() == []
    cfg.option('opt1').value.set(['val'])
    assert cfg.option('opt1').value.get() == ['val']
    with pytest.raises(ValueError):
        cfg.option('opt1').value.set(['val', 'val1'])
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.property.add('demoting_error_warning')
    cfg = get_config(cfg_ori, config_type)
    warnings.simplefilter("always", ValueErrorWarning)
    with warnings.catch_warnings(record=True) as w:
        cfg.option('opt1').value.set(['val', 'val1'])
    assert len(w) == 1
#    assert not list_sessions()


def test_validator_warning(config_type):
    opt1 = StrOption('opt1', '', validators=[Calculation(return_true, Params(ParamSelfOption()), warnings_only=True)], default='val')
    opt2 = StrOption('opt2', '', validators=[Calculation(return_false, Params(ParamSelfOption()), warnings_only=True)])
    opt3 = StrOption('opt3', '', validators=[Calculation(return_if_val, Params(ParamSelfOption(whole=False)), warnings_only=True)], multi=True, properties=('notunique',))
    od1 = OptionDescription('root', '', [opt1, opt2, opt3])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert cfg.option('opt1').value.get() == 'val'
    warnings.simplefilter("always", ValueErrorWarning)
    with warnings.catch_warnings(record=True) as w:
        cfg.option('opt1').value.set('val')
    assert w == []
    #
    with warnings.catch_warnings(record=True) as w:
        cfg.option('opt2').value.set('val')
    assert len(w) == 1
    if config_type != 'tiramisu-api':
        assert w[0].message.opt() == opt2
        assert str(w[0].message) == msg_err.format('val', _(opt2.get_type()), 'opt2') + ', ' + 'test error return_false'
    #
    with warnings.catch_warnings(record=True) as w:
        cfg.nowarnings.option('opt2').value.set('val')
    assert len(w) == 0
    with warnings.catch_warnings(record=True) as w:
        cfg.option('opt2').value.set('val')
    assert len(w) == 1
    #
    with warnings.catch_warnings(record=True) as w:
        cfg.option('opt3').value.set(['val'])
    assert w == []
    #
    with warnings.catch_warnings(record=True) as w:
        cfg.option('opt3').value.set(['val', 'val1'])
    assert len(w) == 1
    if config_type != 'tiramisu-api':
        assert w[0].message.opt() == opt3
        assert str(w[0].message) == msg_err.format('val1', _(opt3.get_type()), 'opt3') + ', ' + 'test error'
    #
    with warnings.catch_warnings(record=True) as w:
        with pytest.raises(ValueError):
            cfg.option('opt2').value.set(1)
    assert len(w) == 0
    #
    with warnings.catch_warnings(record=True) as w:
        cfg.option('opt2').value.set('val')
        cfg.option('opt3').value.set(['val', 'val1', 'val'])
    assert len(w) == 2
    if config_type != 'tiramisu-api':
        assert w[0].message.opt() == opt2
        assert str(w[0].message) == msg_err.format('val', _(opt2.get_type()), 'opt2') + ', ' + 'test error return_false'
        assert w[1].message.opt() == opt3
        assert str(w[1].message) == msg_err.format('val1', _(opt3.get_type()), 'opt3') + ', ' + 'test error'
#    assert not list_sessions()


def test_validator_warning_disabled(config_type):
    opt1 = StrOption('opt1', '', validators=[Calculation(return_true, Params(ParamSelfOption()), warnings_only=True)], default='val')
    opt2 = StrOption('opt2', '', validators=[Calculation(return_false, Params(ParamSelfOption()), warnings_only=True)])
    opt3 = StrOption('opt3', '', validators=[Calculation(return_if_val, Params(ParamSelfOption(whole=False)), warnings_only=True)], multi=True, properties=('notunique',))
    od1 = OptionDescription('root', '', [opt1, opt2, opt3])
    cfg_ori = Config(od1)
    cfg_ori.property.remove('warnings')
    cfg = get_config(cfg_ori, config_type)
    assert cfg.option('opt1').value.get() == 'val'
    warnings.simplefilter("always", ValueErrorWarning)
    with warnings.catch_warnings(record=True) as w:
        cfg.option('opt1').value.set('val')
    assert w == []
    #
    with warnings.catch_warnings(record=True) as w:
        cfg.option('opt2').value.set('val')
    assert w == []
    #
    with warnings.catch_warnings(record=True) as w:
        cfg.option('opt3').value.set(['val'])
    assert w == []
    #
    with warnings.catch_warnings(record=True) as w:
        cfg.option('opt3').value.set(['val', 'val1'])
    assert w == []
    with pytest.raises(ValueError):
        cfg.option('opt2').value.set(1)
    #
    with warnings.catch_warnings(record=True) as w:
        cfg.option('opt2').value.set('val')
        cfg.option('opt3').value.set(['val', 'val1', 'val'])
    assert w == []
    #
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.property.add('demoting_error_warning')
    cfg = get_config(cfg_ori, config_type)
    if config_type != 'tiramisu-api':
        warnings.simplefilter("always", ValueErrorWarning)
        with warnings.catch_warnings(record=True) as w:
            cfg.option('opt2').value.set(1)
        assert len(w) == 1
#    assert not list_sessions()


def test_validator_warning_leadership(config_type):
    display_name_ip = "ip reseau autorise"
    display_name_netmask = "masque du sous-reseau"
    ip_admin_eth0 = StrOption('ip_admin_eth0', display_name_ip, multi=True, validators=[Calculation(return_false, Params(ParamSelfOption(whole=False)), warnings_only=True)], properties=('notunique',))
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', display_name_netmask, multi=True, validators=[Calculation(return_if_val, Params(ParamSelfOption()), warnings_only=True)])
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    assert interface1.impl_get_group_type() == groups.leadership
    od1 = OptionDescription('root', '', [interface1])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    warnings.simplefilter("always", ValueErrorWarning)
    with warnings.catch_warnings(record=True) as w:
        cfg.option('ip_admin_eth0.ip_admin_eth0').value.set([None])
    assert w == []
    #
    with warnings.catch_warnings(record=True) as w:
        cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('val1')
    assert len(w) == 1
    if config_type != 'tiramisu-api':
        assert w[0].message.opt() == netmask_admin_eth0
        assert str(w[0].message) == msg_err.format('val1', _(netmask_admin_eth0.get_type()), display_name_netmask) + ', test error'
    #
    with warnings.catch_warnings(record=True) as w:
        cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['val'])
    if config_type != 'tiramisu-api':
        assert w and w[0].message.opt() == ip_admin_eth0
        assert str(w[0].message) == msg_err.format('val', _(ip_admin_eth0.get_type()), display_name_ip) + ', test error return_false'
    else:
        assert len(w) == 2
    #
    with warnings.catch_warnings(record=True) as w:
        cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['val', 'val1', 'val1'])
    if config_type != 'tiramisu-api':
        assert w[0].message.opt() == ip_admin_eth0
        assert str(w[0].message) == msg_err.format('val', _(ip_admin_eth0.get_type()), display_name_ip) + ', test error return_false'
    else:
        assert len(w) == 3
    #
    with warnings.catch_warnings(record=True) as w:
        cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['val1', 'val', 'val1'])
    if config_type != 'tiramisu-api':
        assert w[0].message.opt() == ip_admin_eth0
        assert str(w[0].message) == msg_err.format('val', _(ip_admin_eth0.get_type()), display_name_ip) + ', test error return_false'
    else:
        assert len(w) == 3
    #
    warnings.resetwarnings()
    with warnings.catch_warnings(record=True) as w:
        cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['val1', 'val1', 'val'])
    if config_type != 'tiramisu-api':
        assert w[0].message.opt() == ip_admin_eth0
        assert str(w[0].message) == msg_err.format('val', _(ip_admin_eth0.get_type()), display_name_ip) + ', test error return_false'
    else:
        assert len(w) == 3
#    assert not list_sessions()


def test_validator_follower_param(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip reseau autorise", multi=True, properties=('notunique',))
    netmask_admin_eth0 = StrOption('netmask_admin_eth0',
                                   "masque du sous-reseau",
                                   multi=True,
                                   validators=[Calculation(return_true, Params(ParamSelfOption(), kwargs={'param': ParamOption(ip_admin_eth0)}))])
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('root', '', [interface1])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['yes'])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('val')
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['yes', 'yes'])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.set('val')
#    assert not list_sessions()


def test_validator_dependencies():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip reseau autorise")
    netmask_admin_eth0 = StrOption('netmask_admin_eth0',
                                   "masque du sous-reseau",
                                   validators=[Calculation(return_true, Params(ParamSelfOption(whole=False), kwargs={'param': ParamOption(ip_admin_eth0)}))])
    opt2 = StrOption('opt2', '', validators=[Calculation(return_false, Params(ParamSelfOption(whole=False)))])
    od1 = OptionDescription('root', '', [ip_admin_eth0, netmask_admin_eth0, opt2])
    cfg = Config(od1)
    assert cfg.option('ip_admin_eth0').has_dependency() is False
    assert cfg.option('netmask_admin_eth0').has_dependency() is True
    assert cfg.option('opt2').has_dependency() is False
    #
    assert cfg.option('ip_admin_eth0').has_dependency(False) is True
    assert cfg.option('netmask_admin_eth0').has_dependency(False) is False
    assert cfg.option('opt2').has_dependency(False) is False
#    assert not list_sessions()


def test_validator_ip_netmask(config_type):
    a = IPOption('a', '')
    b = NetmaskOption('b', '', validators=[Calculation(valid_ip_netmask, Params((ParamOption(a), ParamSelfOption())))])
    od1 = OptionDescription('od', '', [a, b])
    cfg_ori = Config(od1)
    cfg = cfg_ori
    cfg = get_config(cfg_ori, config_type)
    cfg.option('b').value.set('255.255.255.0')
    cfg.option('a').value.set('192.168.1.1')
    cfg.option('b').value.set('255.255.255.0')
    cfg.option('a').value.set('192.168.1.2')
    cfg.option('b').value.set('255.255.255.128')
    cfg.option('b').value.set('255.255.255.0')
    cfg.option('a').value.set('192.168.1.0')
    with pytest.raises(ValueError):
        cfg.option('b').value.get()
    cfg.option('a').value.set('192.168.1.255')
    with pytest.raises(ValueError):
        cfg.option('b').value.get()
    cfg.option('a').value.reset()
    cfg.option('b').value.reset()
    cfg.option('a').value.set('192.168.1.255')
    with pytest.raises(ValueError):
        cfg.option('b').value.set('255.255.255.0')
    #
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.property.add('demoting_error_warning')
    cfg = get_config(cfg_ori, config_type)
    with warnings.catch_warnings(record=True) as w:
        cfg.option('b').value.set('255.255.255.0')
    assert len(w) == 1
#    assert not list_sessions()


def test_validator_network_netmask(config_type):
    a = NetworkOption('a', '')
    b = NetmaskOption('b', '', validators=[Calculation(valid_network_netmask, Params((ParamOption(a), ParamSelfOption())))])
    od1 = OptionDescription('od', '', [a, b])
    cfg_ori = Config(od1)
    cfg = get_config(cfg_ori, config_type)
    cfg.option('a').value.set('192.168.1.1')
    cfg.option('b').value.set('255.255.255.255')
    cfg.option('b').value.reset()
    cfg.option('a').value.set('192.168.1.0')
    cfg.option('b').value.set('255.255.255.0')
    cfg.option('a').value.set('192.168.1.1')
    with pytest.raises(ValueError):
        cfg.option('b').value.get()
    #
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.property.add('demoting_error_warning')
    cfg = get_config(cfg_ori, config_type)
    with warnings.catch_warnings(record=True) as w:
        cfg.option('a').value.set('192.168.1.1')
    assert len(w) == 0
    with warnings.catch_warnings(record=True) as w:
        cfg.option('b').value.get()
    assert len(w) == 1
#    assert not list_sessions()


def test_validator_ip_in_network(config_type):
    a = NetworkOption('a', '')
    b = NetmaskOption('b', '')
    c = IPOption('c', '', validators=[Calculation(valid_in_network, Params((ParamSelfOption(), ParamOption(a), ParamOption(b))))])
    d = IPOption('d', '', validators=[Calculation(valid_in_network, Params((ParamSelfOption(), ParamOption(a), ParamOption(b))), warnings_only=True)])
    od1 = OptionDescription('od', '', [a, b, c, d])
    warnings.simplefilter("always", ValueErrorWarning)
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    cfg.option('a').value.set('192.168.1.0')
    cfg.option('b').value.set('255.255.255.0')
    cfg.option('c').value.set('192.168.1.1')
    with pytest.raises(ValueError):
        cfg.option('c').value.set('192.168.2.1')
    with pytest.raises(ValueError):
        cfg.option('c').value.set('192.168.1.0')
    with pytest.raises(ValueError):
        cfg.option('c').value.set('192.168.1.255')
    with warnings.catch_warnings(record=True) as w:
        cfg.option('d').value.set('192.168.2.1')
    assert len(w) == 1
#    assert not list_sessions()


def test_validator_ip_in_network_incomplete(config_type):
    a = NetworkOption('a', '')
    b = NetmaskOption('b', '')
    c = IPOption('c', '', validators=[Calculation(valid_in_network, Params((ParamSelfOption(), ParamOption(a), ParamOption(b))))])
    d = IPOption('d', '', validators=[Calculation(valid_in_network, Params((ParamSelfOption(), ParamOption(a), ParamOption(b))), warnings_only=True)])
    od1 = OptionDescription('od', '', [a, b, c, d])
    warnings.simplefilter("always", ValueErrorWarning)
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    #
    cfg.option('c').value.set('192.168.1.1')
    #
    cfg.option('a').value.set('192.168.1.0')
    cfg.option('c').value.set('192.168.1.2')
    cfg.option('c').value.set('192.168.2.1')
    #
    cfg.option('b').value.set('255.255.255.0')
    cfg.option('c').value.set('192.168.1.3')
    with pytest.raises(ValueError):
        cfg.option('c').value.set('192.168.2.1')
#    assert not list_sessions()


def test_validator_ip_in_network_cidr(config_type):
    a = NetworkOption('a', '', cidr=True)
    c = IPOption('c', '', validators=[Calculation(valid_in_network, Params((ParamSelfOption(), ParamOption(a))))])
    d = IPOption('d', '', validators=[Calculation(valid_in_network, Params((ParamSelfOption(), ParamOption(a))), warnings_only=True)])
    od1 = OptionDescription('od', '', [a, c, d])
    warnings.simplefilter("always", ValueErrorWarning)
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    cfg.option('a').value.set('192.168.1.0/24')
    cfg.option('c').value.set('192.168.1.1')
    with pytest.raises(ValueError):
        cfg.option('c').value.set('192.168.2.1')
    with pytest.raises(ValueError):
        cfg.option('c').value.set('192.168.1.0')
    with pytest.raises(ValueError):
        cfg.option('c').value.set('192.168.1.255')
    with warnings.catch_warnings(record=True) as w:
        cfg.option('d').value.set('192.168.2.1')
    assert len(w) == 1
#    assert not list_sessions()


def test_validator_ip_in_network_cidr_incomplete(config_type):
    a = NetworkOption('a', '', cidr=True)
    c = IPOption('c', '', validators=[Calculation(valid_in_network, Params((ParamSelfOption(), ParamOption(a))))])
    d = IPOption('d', '', validators=[Calculation(valid_in_network, Params((ParamSelfOption(), ParamOption(a))), warnings_only=True)])
    od1 = OptionDescription('od', '', [a, c, d])
    warnings.simplefilter("always", ValueErrorWarning)
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    #
    cfg.option('c').value.set('192.168.1.1')
    #
    cfg.option('a').value.set('192.168.1.0/24')
    cfg.option('c').value.set('192.168.1.2')
    with pytest.raises(ValueError):
        cfg.option('c').value.set('192.168.2.1')
#    assert not list_sessions()


def test_validator_ip_netmask_multi(config_type):
    a = IPOption('a', '', multi=True)
    b = NetmaskOption('b', '', multi=True, validators=[Calculation(valid_ip_netmask, Params((ParamOption(a), ParamSelfOption())))])
    od = Leadership('a', '', [a, b])
    od2 = OptionDescription('od2', '', [od])
    cfg_ori = Config(od2)
    cfg = get_config(cfg_ori, config_type)
    cfg.option('a.a').value.set(['192.168.1.1'])
    cfg.option('a.b', 0).value.set('255.255.255.0')
    cfg.option('a.a').value.set(['192.168.1.2'])
    cfg.option('a.b', 0).value.set('255.255.255.128')
    cfg.option('a.b', 0).value.set('255.255.255.0')
    cfg.option('a.a').value.set(['192.168.1.0'])
    with pytest.raises(ValueError):
        cfg.option('a.b', 0).value.get()
    #
    cfg.option('a.a').value.set(['192.168.1.2'])
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.property.add('demoting_error_warning')
    cfg = get_config(cfg_ori, config_type)
    cfg.option('a.a').value.set(['192.168.1.0'])
    with warnings.catch_warnings(record=True) as w:
        cfg.option('a.b', 0).value.get()
    assert len(w) == 1
#    assert not list_sessions()


def test_validator_network_netmask_multi(config_type):
    a = NetworkOption('a', '', multi=True)
    b = NetmaskOption('b', '', multi=True, validators=[Calculation(valid_network_netmask, Params((ParamOption(a), ParamSelfOption())))])
    od = Leadership('a', '', [a, b])
    od2 = OptionDescription('od', '', [od])
    cfg = Config(od2)
    cfg = get_config(cfg, config_type)
    cfg.option('a.a').value.set(['192.168.1.1'])
    cfg.option('a.b', 0).value.set('255.255.255.255')
    cfg.option('a.b', 0).value.reset()
    cfg.option('a.a').value.set(['192.168.1.0'])
    cfg.option('a.b', 0).value.set('255.255.255.0')
    cfg.option('a.a').value.set(['192.168.1.1'])
    with pytest.raises(ValueError):
        cfg.option('a.b', 0).value.get()
#    assert not list_sessions()


def test_validator_network_netmask_multi_follower_default_multi(config_type):
    a = NetworkOption('a', '', default_multi=u'192.168.1.0', multi=True, properties=('mandatory',))
    b = NetmaskOption('b', '', default_multi=u'255.255.255.0', multi=True, properties=('mandatory',), validators=[Calculation(valid_network_netmask, Params((ParamOption(a), ParamSelfOption())))])
    od = Leadership('a', '', [a, b])
    od2 = OptionDescription('od2', '', [od])
    cfg = Config(od2)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    cfg.option('a.a').value.set(['192.168.1.0'])
    assert cfg.option('a.a').value.get() == ['192.168.1.0']
    assert cfg.option('a.b', 0).value.get() == '255.255.255.0'
#    assert not list_sessions()


def test_validator_network_netmask_multi_follower_default(config_type):
    a = NetworkOption('a', '', multi=True, properties=('mandatory',))
    b = NetmaskOption('b', '', default_multi=u'255.255.255.0', multi=True, properties=('mandatory',), validators=[Calculation(valid_network_netmask, Params((ParamOption(a), ParamSelfOption())))])
    od = Leadership('a', '', [a, b])
    od2 = OptionDescription('od2', '', [od])
    cfg_ori = Config(od2)
    cfg_ori.property.read_write()
    cfg_ori.property.remove('cache')
    cfg = get_config(cfg_ori, config_type)
    assert cfg.option('a.a').value.get() == []
    cfg.option('a.a').value.set(['192.168.1.0'])
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.property.read_only()
    cfg = get_config(cfg_ori, config_type)
    assert cfg.option('a.a').value.get() == [u'192.168.1.0']
    assert cfg.option('a.b', 0).value.get() == u'255.255.255.0'
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.property.read_write()
    cfg = get_config(cfg_ori, config_type)
    cfg.option('a.a').value.set([u'192.168.1.0', u'192.168.1.1'])
    with pytest.raises(ValueError):
        cfg.option('a.b', 0).value.set([u'192.168.1.0'])
    with pytest.raises(ValueError):
        cfg.option('a.b', 1).value.set([u'192.168.1.1'])
    cfg.option('a.a').value.set(['192.168.1.0', '192.168.1.1'])
    cfg.option('a.b', 0).value.set('255.255.255.0')
    cfg.option('a.b', 1).value.set('255.255.255.255')
    cfg.option('a.a').value.set(['192.168.1.0', '192.168.1.1'])
#    assert not list_sessions()


def return_netmask(*args, **kwargs):
    return u'255.255.255.0'


def return_netmask2(leader):
    if leader is not None:
        if leader.endswith('2.1'):
            return u'255.255.255.0'
        if not leader.endswith('.0'):
            return u'255.255.255.255'
    return u'255.255.255.0'


def test_validator_network_netmask_multi_follower_callback(config_type):
    a = NetworkOption('a', '', multi=True, properties=('mandatory',))
    b = NetmaskOption('b', '', Calculation(return_netmask, Params(kwargs={'index': ParamIndex()})), multi=True, properties=('mandatory',), validators=[Calculation(valid_network_netmask, Params((ParamOption(a), ParamSelfOption())))])
    od = Leadership('a', '', [a, b])
    od2 = OptionDescription('od2', '', [od])
    cfg_ori = Config(od2)
    cfg_ori.property.read_write()
    cfg_ori.property.remove('cache')
    cfg = get_config(cfg_ori, config_type)
    assert cfg.option('a.a').value.get() == []
    cfg.option('a.a').value.set(['192.168.1.0'])
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.property.read_only()
    cfg = get_config(cfg_ori, config_type)
    assert cfg.option('a.a').value.get() == [u'192.168.1.0']
    assert cfg.option('a.b', 0).value.get() == '255.255.255.0'
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.property.read_write()
    cfg = get_config(cfg_ori, config_type)
    cfg.option('a.a').value.set([u'192.168.1.0', u'192.168.1.1'])
    cfg.option('a.b', 0).value.get()
    with pytest.raises(ValueError):
        cfg.option('a.b', 1).value.get()
    cfg.option('a.a').value.set(['192.168.1.0', '192.168.1.1'])
    cfg.option('a.b', 0).value.set('255.255.255.0')
    cfg.option('a.b', 1).value.set('255.255.255.255')
    cfg.option('a.a').value.set(['192.168.1.0', '192.168.1.1'])
#    assert not list_sessions()


def test_validator_network_netmask_multi_follower_callback_value(config_type):
    a = NetworkOption('a', '', multi=True, properties=('mandatory',))
    b = NetmaskOption('b', '', Calculation(return_netmask2, Params(ParamOption(a))), multi=True, properties=('mandatory',), validators=[Calculation(valid_network_netmask, Params((ParamOption(a), ParamSelfOption())))])
    od = Leadership('a', '', [a, b])
    od2 = OptionDescription('od2', '', [od])
    cfg = Config(od2)
    cfg.property.read_write()
    cfg.property.remove('cache')
    cfg = get_config(cfg, config_type)
    assert cfg.option('a.a').value.get() == []
    cfg.option('a.a').value.set(['192.168.1.0'])
    assert cfg.option('a.a').value.get() == ['192.168.1.0']
    assert cfg.option('a.b', 0).value.get() == '255.255.255.0'
    cfg.option('a.a').value.set(['192.168.1.0', '192.168.2.1'])
    assert cfg.option('a.b', 0).value.get() == '255.255.255.0'
    with pytest.raises(ValueError):
        cfg.option('a.b', 1).value.get()
    cfg.option('a.a').value.pop(1)
    #
    assert cfg.option('a.a').value.get() == [u'192.168.1.0']
    assert cfg.option('a.b', 0).value.get() == '255.255.255.0'
    cfg.option('a.a').value.set(['192.168.2.1'])
    with pytest.raises(ValueError):
        cfg.option('a.b', 0).value.get()
    cfg.option('a.a').value.set(['192.168.1.0'])
    #
    assert cfg.option('a.a').value.get() == [u'192.168.1.0']
    assert cfg.option('a.b', 0).value.get() == '255.255.255.0'
    cfg.option('a.a').value.set(['192.168.1.0', '192.168.1.1'])
    cfg.option('a.b', 0).value.set('255.255.255.0')
    cfg.option('a.b', 1).value.set('255.255.255.255')
#    assert not list_sessions()


def test_validator_ip_netmask_multi_leader(config_type):
    a = IPOption('a', '', multi=True)
    b = NetmaskOption('b', '', multi=True, validators=[Calculation(valid_ip_netmask, Params((ParamOption(a), ParamSelfOption())))])
    od = Leadership('a', '', [a, b])
    od2 = OptionDescription('od2', '', [od])
    cfg = Config(od2)
    cfg = get_config(cfg, config_type)
    cfg.option('a.a').value.set(['192.168.1.1'])
    cfg.option('a.b', 0).value.set('255.255.255.0')
    cfg.option('a.a').value.set(['192.168.1.2'])
    cfg.option('a.b', 0).value.set('255.255.255.128')
    cfg.option('a.b', 0).value.set('255.255.255.0')
    cfg.option('a.a').value.set(['192.168.1.0'])
    with pytest.raises(ValueError):
        cfg.option('a.b', 0).value.get()
    cfg.option('a.a').value.set(['192.168.1.128'])
    with pytest.raises(ValueError):
        cfg.option('a.b', 0).value.set('255.255.255.128')
    cfg.option('a.a').value.set(['192.168.1.2', '192.168.1.3'])
#    assert not list_sessions()


def test_validator_network_netmask_multi_leader(config_type):
    a = NetworkOption('a', '', multi=True)
    b = NetmaskOption('b', '', multi=True, validators=[Calculation(valid_network_netmask, Params((ParamOption(a), ParamSelfOption())))])
    od = Leadership('a', '', [a, b])
    od2 = OptionDescription('od2', '', [od])
    cfg = Config(od2)
    cfg = get_config(cfg, config_type)
    cfg.option('a.a').value.set(['192.168.1.1'])
    cfg.option('a.b', 0).value.set('255.255.255.255')
    cfg.option('a.b', 0).value.reset()
    cfg.option('a.a').value.set(['192.168.1.0'])
    cfg.option('a.b', 0).value.set('255.255.255.0')
    cfg.option('a.a').value.set(['192.168.1.1'])
    with pytest.raises(ValueError):
        cfg.option('a.b', 0).value.get()
#    assert not list_sessions()


def test_validator_broadcast(config_type):
    a = NetworkOption('a', '', multi=True)
    b = NetmaskOption('b', '', multi=True, validators=[Calculation(valid_network_netmask, Params((ParamOption(a), ParamSelfOption())))])
    c = BroadcastOption('c', '', multi=True, validators=[Calculation(valid_broadcast, Params((ParamOption(a), ParamOption(b), ParamSelfOption())))])
    od = Leadership('a', '', [a, b, c])
    od2 = OptionDescription('od2', '', [od])
    cfg = Config(od2)
    cfg = get_config(cfg, config_type)
    #first, test network_netmask
    cfg.option('a.a').value.set(['192.168.1.128'])
    with pytest.raises(ValueError):
        cfg.option('a.a').value.set(['255.255.255.0'])
    #
    cfg.option('a.a').value.set(['192.168.1.0'])
    cfg.option('a.b', 0).value.set('255.255.255.0')
    cfg.option('a.c', 0).value.set('192.168.1.255')
    cfg.option('a.a').value.set(['192.168.1.1'])
    with pytest.raises(ValueError):
        cfg.option('a.b', 0).value.get()
    with pytest.raises(ValueError):
        cfg.option('a.c', 0).value.get()
    #
    cfg.option('a.a').value.set(['192.168.1.0', '192.168.2.128'])
    cfg.option('a.b', 0).value.set('255.255.255.0')
    cfg.option('a.b', 1).value.set('255.255.255.128')
    cfg.option('a.c', 0).value.set('192.168.1.255')
    cfg.option('a.c', 1).value.set('192.168.2.255')
    with pytest.raises(ValueError):
        cfg.option('a.c', 1).value.set('192.168.2.128')
    cfg.option('a.c', 1).value.set('192.168.2.255')
#    assert not list_sessions()


def test_validator_broadcast_todict(config_type):
    a = NetworkOption('a', '', multi=True)
    b = NetmaskOption('b', '', multi=True, validators=[Calculation(valid_network_netmask, Params((ParamOption(a), ParamSelfOption())))])
    c = BroadcastOption('c', '', multi=True, validators=[Calculation(valid_broadcast, Params((ParamOption(a), ParamOption(b), ParamSelfOption())))])
    od = Leadership('a', '', [a, b, c])
    od2 = OptionDescription('od2', '', [od])
    cfg = Config(od2)
    cfg = get_config(cfg, config_type)
    #first, test network_netmask
    cfg.option('a.a').value.set(['192.168.1.128'])
    with pytest.raises(ValueError):
        cfg.option('a.a').value.set(['255.255.255.0'])
    #
    cfg.option('a.a').value.set(['192.168.1.0'])
    cfg.option('a.b', 0).value.set('255.255.255.0')
    cfg.option('a.c', 0).value.set('192.168.1.255')
    cfg.option('a.a').value.set(['192.168.1.1'])
    with pytest.raises(ValueError):
        cfg.option('a.b', 0).value.get()
    with pytest.raises(ValueError):
        cfg.option('a.c', 0).value.get()
    #
    cfg.option('a.a').value.set(['192.168.1.0', '192.168.2.128'])
    cfg.option('a.b', 0).value.set('255.255.255.0')
    cfg.option('a.b', 1).value.set('255.255.255.128')
    cfg.option('a.c', 0).value.set('192.168.1.255')
    cfg.option('a.c', 1).value.set('192.168.2.255')
    with pytest.raises(ValueError):
        cfg.option('a.c', 1).value.set('192.168.2.128')
    cfg.option('a.c', 1).value.set('192.168.2.255')
#    assert not list_sessions()


def test_validator_broadcast_warnings(config_type):
    warnings.simplefilter("always", ValueErrorWarning)
    a = NetworkOption('a', '', properties=('mandatory', 'disabled'))
    b = NetmaskOption('b', '', properties=('mandatory', 'disabled'), validators=[Calculation(valid_network_netmask, Params((ParamOption(a), ParamSelfOption())), warnings_only=True)])
    od1 = OptionDescription('a', '', [a, b])
    cfg_ori = Config(od1)
    cfg = get_config(cfg_ori, config_type)
    with warnings.catch_warnings(record=True) as w:
        cfg.option('a').value.set('192.168.1.4')
        cfg.option('b').value.set('255.255.255.0')
    assert len(w) == 1
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.property.read_write()
    cfg = get_config(cfg_ori, config_type)
    with warnings.catch_warnings(record=True) as w:
        list(cfg.value.mandatory())
    assert len(w) == 0
#    assert not list_sessions()


def test_validator_broadcast_default_1():
    a = NetworkOption('a', '', '192.168.1.0')
    b = NetmaskOption('b', '', '255.255.255.128')
    c = BroadcastOption('c', '', '192.168.2.127', validators=[Calculation(valid_broadcast, Params((ParamOption(a), ParamOption(b), ParamSelfOption())))])
    od1 = OptionDescription('a', '', [a, b, c])
    cfg = Config(od1)
    with pytest.raises(ValueError):
        cfg.value.get()
#    assert not list_sessions()


def test_validator_broadcast_default_2():
    a = NetworkOption('a', '', '192.168.1.0')
    b = NetmaskOption('b', '', '255.255.255.128')
    d = BroadcastOption('d', '', '192.168.1.127', validators=[Calculation(valid_broadcast, Params((ParamOption(a), ParamOption(b), ParamSelfOption())))])
    od1 = OptionDescription('a', '', [a, b, d])
    cfg = Config(od1)
    assert cfg.value.get()
#    assert not list_sessions()


def test_validator_not_all(config_type):
    a = NetworkOption('a', '', multi=True)
    b = NetmaskOption('b', '', multi=True, validators=[Calculation(valid_network_netmask, Params((ParamOption(a), ParamSelfOption())))])
    c = BroadcastOption('c', '', multi=True)
    od = Leadership('a', '', [a, b, c])
    od1 = OptionDescription('od2', '', [od])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    cfg.option('a.a').value.set(['192.168.1.0'])
    cfg.option('a.b', 0).value.set('255.255.255.0')
    cfg.option('a.c', 0).value.set('192.168.1.255')
#    assert not list_sessions()


def test_validator_network_netmask_mandatory(config_type):
    a = NetworkOption('a', '', multi=True, properties=('mandatory',), default=[u'0.0.0.0'])
    b = NetmaskOption('b', '', multi=True, properties=('mandatory',), default_multi=u'0.0.0.0', validators=[Calculation(valid_network_netmask, Params((ParamOption(a), ParamSelfOption())))])
    od = Leadership('a', '', [a, b])
    od1 = OptionDescription('od2', '', [od])
    cfg = Config(od1)
    cfg.property.read_only()
    cfg = get_config(cfg, config_type)
    cfg.value.get()
#    assert not list_sessions()


def test_validator_has_dependency():
    a = IPOption('a', '')
    b = NetmaskOption('b', '', validators=[Calculation(valid_ip_netmask, Params((ParamOption(a), ParamSelfOption())))])
    od1 = OptionDescription('od', '', [a, b])
    cfg = Config(od1)
    assert cfg.option('a').has_dependency() is False
    assert cfg.option('b').has_dependency() is True
    assert cfg.option('a').has_dependency(False) is True
    assert cfg.option('b').has_dependency(False) is False
#    assert not list_sessions()


def test_validator_warnings_only_more_option(config_type):
    a = IntOption('a', '')
    b = IntOption('b', '')
    d = IntOption('d', '', validators=[Calculation(valid_not_equal, Params((ParamSelfOption(), ParamOption(a), ParamOption(b))), warnings_only=True)])
    od1 = OptionDescription('od', '', [a, b, d])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    cfg.option('a').value.set(1)
    cfg.option('b').value.set(1)
    warnings.simplefilter("always", ValueErrorWarning)
    with warnings.catch_warnings(record=True) as w:
        cfg.option('d').value.get()
    assert w == []
    with warnings.catch_warnings(record=True) as w:
        cfg.option('d').value.set(1)
    assert w != []
    assert len(w) == 1
#    assert not list_sessions()


def test_validator_error_prefix():
    a = IntOption('a', '')
    b = IntOption('b', '', validators=[Calculation(valid_not_equal, Params((ParamSelfOption(), ParamOption(a))))])
    od1 = OptionDescription('od', '', [a, b])
    cfg = Config(od1)
    cfg.option('a').value.set(1)
    try:
        cfg.option('b').value.set(1)
    except Exception as err:
        assert str(err) == _('"{0}" is an invalid {1} for "{2}"').format('1', _('integer'), 'b') + ', ' +  _('value is identical to {0}').format('"a"')
    try:
        cfg.option('b').value.set(1)
    except Exception as err:
        err.prefix = ''
        assert str(err) == _('value is identical to {0}').format('"a"')
#    assert not list_sessions()


def test_validator_warnings_only_option(config_type):
    a = IntOption('a', '')
    b = IntOption('b', '', warnings_only=True, validators=[Calculation(valid_not_equal, Params((ParamSelfOption(), ParamOption(a))))])
    od1 = OptionDescription('od', '', [a, b])
    cfg_ori = Config(od1)
    cfg = get_config(cfg_ori, config_type)
    cfg.option('a').value.set(1)
    with pytest.raises(ValueError):
        cfg.option('b').value.set(1)
#    assert not list_sessions()


def test_validator_not_equal(config_type):
    a = IntOption('a', '')
    b = IntOption('b', '', validators=[Calculation(valid_not_equal, Params((ParamSelfOption(), ParamOption(a))))])
    od1 = OptionDescription('od', '', [a, b])
    cfg_ori = Config(od1)
    cfg = get_config(cfg_ori, config_type)
    assert cfg.option('a').value.get() is None
    assert cfg.option('b').value.get() is None
    cfg.option('a').value.set(1)
    cfg.option('a').value.reset()
    cfg.option('a').value.set(1)
    with pytest.raises(ValueError):
        cfg.option('b').value.set(1)
    cfg.option('b').value.set(2)
    #
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.property.add('demoting_error_warning')
    cfg = get_config(cfg_ori, config_type)
    warnings.simplefilter("always", ValueErrorWarning)
    with warnings.catch_warnings(record=True) as w:
        cfg.option('b').value.set(1)
    assert len(w) == 1
#    assert not list_sessions()


def test_validator_not_equal_leadership(config_type):
    a = IntOption('a', '', multi=True)
    b = IntOption('b', '', multi=True, validators=[Calculation(valid_not_equal, Params((ParamSelfOption(), ParamOption(a))))])
    od = Leadership('a', '', [a, b])
    od1 = OptionDescription('b', '', [od])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert cfg.option('a.a').value.get() == []
    cfg.option('a.a').value.set([1])
    cfg.option('a.a').value.reset()
    cfg.option('a.a').value.set([1])
    with pytest.raises(ValueError):
        cfg.option('a.b', 0).value.set(1)
    cfg.option('a.b', 0).value.set(2)
    cfg.option('a.a').value.reset()
    cfg.option('a.a').value.set([1])
    cfg.value.get()
#    assert not list_sessions()


def test_validator_not_equal_leadership_default():
    a = IntOption('a', '', multi=True)
    b = IntOption('b', '', multi=True, default_multi=1, validators=[Calculation(valid_not_equal, Params((ParamSelfOption(), ParamOption(a))))])
    od = Leadership('a', '', [a, b])
    od1 = OptionDescription('a', '', [od])
    cfg = Config(od1)
    # FIXME cfg = get_config(cfg, config_type)
    assert cfg.option('a.a').value.get() == []
    cfg.option('a.a').value.set([1])
    with pytest.raises(ValueError):
        cfg.option('a.b', 0).value.get()
    cfg.option('a.a').value.set([2])
    cfg.option('a.a').value.reset()
    cfg.option('a.a').value.set([2])
    #
    cfg.property.add('demoting_error_warning')
    with warnings.catch_warnings(record=True) as w:
        cfg.option('a.b', 0).value.set(2)
    assert len(w) == 1
#    assert not list_sessions()


def test_validator_default_diff():
    a = IntOption('a', '', 3)
    b = IntOption('b', '', 1, validators=[Calculation(valid_not_equal, Params((ParamSelfOption(), ParamOption(a))))])
    od1 = OptionDescription('od', '', [a, b])
    cfg = Config(od1)
    # FIXME cfg = get_config(cfg, config_type)
    cfg.option('b').value.set(2)
    cfg.option('a').value.set(1)
    owner = cfg.owner.get()
    assert cfg.option('b').owner.get() == owner
    with pytest.raises(ValueError):
        cfg.option('b').value.reset()
    assert cfg.option('b').owner.get() == owner
    #
    cfg.property.add('demoting_error_warning')
    with warnings.catch_warnings(record=True) as w:
        cfg.option('b').value.reset()
    assert len(w) == 1
#    assert not list_sessions()


def test_validator_permissive(config_type):
    a = IntOption('a', '', 1, properties=('hidden',))
    b = IntOption('b', '', 2, validators=[Calculation(valid_not_equal, Params((ParamSelfOption(), ParamOption(a))))])
    od1 = OptionDescription('od', '', [a, b])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.permissive.add('hidden')
    cfg = get_config(cfg, config_type)
    with pytest.raises(ValueError):
        cfg.option('b').value.set(1)
    cfg.option('b').value.set(2)
#    assert not list_sessions()


def test_validator_disabled(config_type):
    a = IntOption('a', '', 1, properties=('disabled',))
    b = IntOption('b', '', 2, validators=[Calculation(valid_not_equal, Params((ParamSelfOption(), ParamOption(a, raisepropertyerror=True))))])
    od1 = OptionDescription('od', '', [a, b])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    with pytest.raises(PropertiesOptionError):
        cfg.option('b').value.set(1)
#    assert not list_sessions()


def test_consistency_disabled_transitive(config_type):
    a = IntOption('a', '', 1, properties=('disabled',))
    b = IntOption('b', '', 2, validators=[Calculation(valid_not_equal, Params((ParamSelfOption(), ParamOption(a, notraisepropertyerror=True))))])
    od1 = OptionDescription('od', '', [a, b])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    cfg.option('b').value.set(1)
#    assert not list_sessions()


def test_consistency_double_warnings(config_type):
    a = IntOption('a', '', 1)
    b = IntOption('b', '', 1)
    c = IntOption('c', '', validators=[Calculation(valid_not_equal, Params((ParamSelfOption(), ParamOption(a))), warnings_only=True), Calculation(valid_not_equal, Params((ParamSelfOption(), ParamOption(b))), warnings_only=True)])
    od = OptionDescription('od', '', [a, b, c])
    warnings.simplefilter("always", ValueErrorWarning)
    od1 = OptionDescription('od2', '', [od])
    cfg_ori = Config(od1)
    cfg = get_config(cfg_ori, config_type)
    with warnings.catch_warnings(record=True) as w:
        cfg.option('od.c').value.set(1)
    assert w != []
    if config_type == 'tiramisu-api':
        # in this case warnings is for '"a" and "b"'
        assert len(w) == 1
    else:
        # in this cas one warnings is for "a" and the second for "b"
        assert len(w) == 2
    cfg.option('od.a').value.set(2)
    with warnings.catch_warnings(record=True) as w:
        cfg.option('od.c').value.get()
    assert len(w) == 1
    #
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.property.remove('warnings')
    cfg = get_config(cfg_ori, config_type)
    with warnings.catch_warnings(record=True) as w:
        cfg.option('od.c').value.set(1)
    assert w == []
#    assert not list_sessions()


def test_consistency_warnings_error(config_type):
    a = IntOption('a', '', 1)
    b = IntOption('b', '', 1)
    c = IntOption('c', '', validators=[
            Calculation(valid_not_equal, Params((ParamSelfOption(), ParamOption(a))), warnings_only=True),
            Calculation(valid_not_equal, Params((ParamSelfOption(), ParamOption(b))))
        ])
    od1 = OptionDescription('od', '', [a, b, c])
    warnings.simplefilter("always", ValueErrorWarning)
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    with warnings.catch_warnings(record=True) as w:
        with pytest.raises(ValueError):
            cfg.option('c').value.set(1)
    assert w == []
#    assert not list_sessions()


def test_consistency_not_equal_has_dependency():
    a = IntOption('a', '')
    b = IntOption('b', '', )
    b = IntOption('b', '', validators=[Calculation(valid_not_equal, Params((ParamSelfOption(), ParamOption(a))))])
    od1 = OptionDescription('od', '', [a, b])
    cfg = Config(od1)
    assert cfg.option('a').has_dependency() is False
    assert cfg.option('b').has_dependency() is True
    assert cfg.option('a').has_dependency(False) is True
    assert cfg.option('b').has_dependency(False) is False
#    assert not list_sessions()


def test_validator_information(config_type):
    opt1 = StrOption('opt1', '', validators=[Calculation(return_true, Params((ParamSelfInformation('key'), ParamValue('yes'))))], default='val')
    opt2 = StrOption('opt2', '', validators=[Calculation(return_true, Params((ParamInformation('key'), ParamValue('yes'))))], default='val')
    opt3 = StrOption('opt3', '', validators=[Calculation(return_true, Params((ParamInformation('key', option=opt1), ParamValue('yes'))))], default='val')
    od1 = OptionDescription('root', '', [opt1, opt2, opt3])
    cfg = Config(od1)
    with pytest.raises(ConfigError):
        cfg.option('opt1').value.get()
    with pytest.raises(ConfigError):
        cfg.option('opt3').value.get()
    cfg.option('opt1').information.set('key', 'val')
    assert cfg.option('opt1').value.get() == 'val'
    assert cfg.option('opt3').value.get() == 'val'
    cfg.option('opt1').information.set('key', 'val1')
    with pytest.raises(ValueError):
        cfg.option('opt1').value.get()
    with pytest.raises(ValueError):
        cfg.option('opt3').value.get()
    #
    with pytest.raises(ConfigError):
        cfg.option('opt2').value.get()
    cfg.information.set('key', 'val')
    assert cfg.option('opt2').value.get() == 'val'
    cfg.information.set('key', 'val1')
    with pytest.raises(ValueError):
        cfg.option('opt2').value.get()
