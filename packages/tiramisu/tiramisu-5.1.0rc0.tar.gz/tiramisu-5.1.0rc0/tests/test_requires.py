# coding: utf-8
from .autopath import do_autopath
do_autopath()

from copy import copy
from os import environ
from tiramisu.i18n import _
from tiramisu.setting import groups
from tiramisu import setting
setting.expires_time = 1
from tiramisu import IPOption, OptionDescription, BoolOption, IntOption, StrOption, \
                     Leadership, Config, calc_value, Params, ParamOption, Calculation, ParamValue, ParamSelfOption, ParamIndex, \
                     calc_value_property_help
from tiramisu.error import PropertiesOptionError, ConfigError, display_list
import pytest
from .config import config_type, get_config, parse_od_get


def test_properties(config_type):
    a = BoolOption('activate_service', '', True)
    b = IPOption('ip_address_service', '', properties=('disabled',))
    od1 = OptionDescription('service', '', [a, b])
    cfg_ori = Config(od1)
    cfg_ori.property.read_write()
    cfg = get_config(cfg_ori, config_type)
    props = []
    try:
        cfg.option('ip_address_service').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.unrestraint.option('ip_address_service').permissive.add('disabled')
    cfg = get_config(cfg_ori, config_type)
    cfg.option('ip_address_service').value.get()
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.unrestraint.option('ip_address_service').permissive.remove('disabled')
    cfg = get_config(cfg_ori, config_type)
    props = []
    try:
        cfg.option('ip_address_service').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])
    # pop twice
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.unrestraint.option('ip_address_service').permissive.add('disabled')
    cfg_ori.unrestraint.option('ip_address_service').permissive.remove('disabled')
#    assert not list_sessions()


def test_requires(config_type):
    a = BoolOption('activate_service', '', True)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(a),
                                                   'expected': ParamValue(False)}))
    b = IPOption('ip_address_service', '',
                 properties=(disabled_property,))
    od1 = OptionDescription('service', '', [a, b])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    cfg.option('ip_address_service').value.get()
    cfg.option('activate_service').value.set(False)
    props = []
    try:
        cfg.option('ip_address_service').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])
    cfg.option('activate_service').value.set(True)
    cfg.option('ip_address_service').value.get()
#    assert not list_sessions()


def test_requires_inverse(config_type):
    a = BoolOption('activate_service', '', True)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(a),
                                                   'expected': ParamValue(False),
                                                   'reverse_condition': ParamValue(True)}))
    b = IPOption('ip_address_service', '', properties=(disabled_property,))
    od1 = OptionDescription('service', '', [a, b])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    props = []
    try:
        cfg.option('ip_address_service').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])
    cfg.option('activate_service').value.set(False)
    cfg.option('ip_address_service').value.get()
    cfg.option('activate_service').value.set(True)
    try:
        cfg.option('ip_address_service').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])
#    assert not list_sessions()


def test_requires_self(config_type):
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamSelfOption(),
                                                   'expected': ParamValue('b')}))
    a = StrOption('ip_address_service', '', properties=(disabled_property,))
    od1 = OptionDescription('service', '', [a])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert cfg.option('ip_address_service').value.get() == None
    cfg.option('ip_address_service').value.set('a')
    assert cfg.option('ip_address_service').value.get() == 'a'
    cfg.option('ip_address_service').value.set('b')
    props = []
    try:
        cfg.option('ip_address_service').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])
#    assert not list_sessions()


def test_requires_with_requires(config_type):
    a = BoolOption('activate_service', '', True)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(a),
                                                   'expected': ParamValue(False)}))
    b = IPOption('ip_address_service', '', properties=(disabled_property,))
    od1 = OptionDescription('service', '', [a, b])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.option('ip_address_service').property.add('test')
    cfg = get_config(cfg, config_type)
    cfg.option('ip_address_service').value.get()
    cfg.option('activate_service').value.set(False)
    props = []
    try:
        cfg.option('ip_address_service').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])
    cfg.option('activate_service').value.set(True)
    cfg.option('ip_address_service').value.get()
#    assert not list_sessions()


def test_requires_same_action(config_type):
    activate_service = BoolOption('activate_service', '', True)
    new_property = Calculation(calc_value,
                               Params(ParamValue('new'),
                                      kwargs={'condition': ParamOption(activate_service),
                                              'expected': ParamValue(False)}),
                               calc_value_property_help)
    activate_service_web = BoolOption('activate_service_web', '', True, properties=(new_property,))
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(activate_service_web, notraisepropertyerror=True),
                                                   'expected': ParamValue(False)}),
                                    calc_value_property_help)
    ip_address_service_web = IPOption('ip_address_service_web', '', properties=(disabled_property,))
    od1 = OptionDescription('service', '', [activate_service, activate_service_web, ip_address_service_web])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.property.add('new')
    cfg = get_config(cfg, config_type)
    cfg.option('activate_service').value.get()
    cfg.option('activate_service_web').value.get()
    cfg.option('ip_address_service_web').value.get()
    cfg.option('activate_service').value.set(False)
    #
    props = []
    try:
        cfg.option('activate_service_web').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    if config_type == 'tiramisu':
        assert frozenset(props) == frozenset(['new'])
    else:
        assert frozenset(props) == frozenset(['disabled'])
    #
    props = []
    try:
        cfg.option('ip_address_service_web').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
        submsg = '"disabled" (' + _('the value of "{0}" is {1}').format('activate_service', '"False"') + ')'
        if config_type == 'tiramisu':
            submsg = '"new" (' + _('the value of "{0}" is {1}').format('activate_service', '"False"') + ')'
            submsg = '"disabled" (' + str(_('cannot access to {0} {1} because has {2} {3}').format('option', '"activate_service_web"', _('property'), submsg)) + ')'
            assert str(err) == str(_('cannot access to {0} {1} because has {2} {3}').format('option', '"ip_address_service_web"', _('property'), submsg))
            #access to cache
            assert str(err) == str(_('cannot access to {0} {1} because has {2} {3}').format('option', '"ip_address_service_web"', _('property'), submsg))
        else:
            # FIXME
            assert str(err) == 'error'
    assert frozenset(props) == frozenset(['disabled'])
#    assert not list_sessions()


def test_multiple_requires(config_type):
    a = StrOption('activate_service', '')
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(a),
                                                   'expected_0': ParamValue('yes'),
                                                   'expected_1': ParamValue('ok')}))
    b = IPOption('ip_address_service', '', properties=(disabled_property,))
    od1 = OptionDescription('service', '', [a, b])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    cfg.option('ip_address_service').value.get()
    cfg.option('activate_service').value.set('yes')
    props = []
    try:
        cfg.option('ip_address_service').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])

    cfg.option('activate_service').value.set('ok')
    props = []
    try:
        cfg.option('ip_address_service').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])

    cfg.option('activate_service').value.set('no')
    cfg.option('ip_address_service').value.get()
#    assert not list_sessions()


def test_multiple_requires_cumulative(config_type):
    a = StrOption('activate_service', '')
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(a),
                                                   'expected': ParamValue('yes')}))
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(a),
                                                 'expected': ParamValue('yes')}))
    b = IPOption('ip_address_service', '', properties=(disabled_property, hidden_property))
    od1 = OptionDescription('service', '', [a, b])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    cfg.option('ip_address_service').value.get()
    cfg.option('activate_service').value.set('yes')
    props = []
    try:
        cfg.option('ip_address_service').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    if config_type == 'tiramisu':
        assert set(props) == {'hidden', 'disabled'}
    else:
        assert set(props) == {'disabled'}

    cfg.option('activate_service').value.set('ok')
    cfg.option('ip_address_service').value.get()

    cfg.option('activate_service').value.set('no')
    cfg.option('ip_address_service').value.get()
#    assert not list_sessions()


def test_multiple_requires_cumulative_inverse(config_type):
    a = StrOption('activate_service', '')
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(a),
                                                   'expected': ParamValue('yes'),
                                                   'reverse_condition': ParamValue(True)}))
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(a),
                                                 'expected': ParamValue('yes'),
                                                 'reverse_condition': ParamValue(True)}))
    b = IPOption('ip_address_service', '', properties=(disabled_property, hidden_property))
    od1 = OptionDescription('service', '', [a, b])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    props = []
    try:
        cfg.option('ip_address_service').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    if config_type == 'tiramisu':
        assert set(props) == {'hidden', 'disabled'}
    else:
        assert set(props) == {'disabled'}
    cfg.option('activate_service').value.set('yes')
    cfg.option('ip_address_service').value.get()

    cfg.option('activate_service').value.set('ok')
    props = []
    try:
        cfg.option('ip_address_service').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    if config_type == 'tiramisu':
        assert set(props) == {'hidden', 'disabled'}
    else:
        assert set(props) == {'disabled'}

    cfg.option('activate_service').value.set('no')
    props = []
    try:
        cfg.option('ip_address_service').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    if config_type == 'tiramisu':
        assert set(props) == {'hidden', 'disabled'}
    else:
        assert set(props) == {'disabled'}
#    assert not list_sessions()


def test_multiple_requires_inverse(config_type):
    a = StrOption('activate_service', '')
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(a),
                                                   'expected_0': ParamValue('yes'),
                                                   'expected_1': ParamValue('ok'),
                                                   'reverse_condition': ParamValue(True)}))
    b = IPOption('ip_address_service', '', properties=(disabled_property,))
    od1 = OptionDescription('service', '', [a, b])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    props = []
    try:
        cfg.option('ip_address_service').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])

    cfg.option('activate_service').value.set('yes')
    cfg.option('ip_address_service').value.get()

    cfg.option('activate_service').value.set('ok')
    cfg.option('ip_address_service').value.get()

    cfg.option('activate_service').value.set('no')
    props = []
    try:
        cfg.option('ip_address_service').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])
#    assert not list_sessions()


def test_requires_transitive(config_type):
    a = BoolOption('activate_service', '', True)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(a, notraisepropertyerror=True),
                                                   'expected': ParamValue(False)}))
    b = BoolOption('activate_service_web', '', True, properties=(disabled_property,))
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(b, raisepropertyerror=True),
                                                   'expected': ParamValue(False)}))

    d = IPOption('ip_address_service_web', '', properties=(disabled_property,))
    od1 = OptionDescription('service', '', [a, b, d])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    cfg.option('activate_service').value.get()
    cfg.option('activate_service_web').value.get()
    cfg.option('ip_address_service_web').value.get()
    cfg.option('activate_service').value.set(False)
    #
    props = []
    try:
        cfg.option('activate_service_web').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])
    #
    props = []
    try:
        cfg.option('ip_address_service_web').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])
#    assert not list_sessions()


def test_requires_transitive_unrestraint(config_type):
    a = BoolOption('activate_service', '', True)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(a, notraisepropertyerror=True),
                                                   'expected': ParamValue(False)}))
    b = BoolOption('activate_service_web', '', True, properties=(disabled_property,))
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(b, notraisepropertyerror=True),
                                                   'expected': ParamValue(False)}))
    d = IPOption('ip_address_service_web', '', properties=(disabled_property,))
    od1 = OptionDescription('service', '', [a, b, d])
    cfg_ori = Config(od1)
    cfg_ori.property.read_write()
    cfg = get_config(cfg_ori, config_type)
    cfg.option('activate_service').value.get()
    cfg.option('activate_service_web').value.get()
    cfg.option('ip_address_service_web').value.get()
    cfg.option('activate_service').value.set(False)
    #
    if config_type == 'tiramisu-api':
        cfg.send()
    assert cfg_ori.option('activate_service_web').property.get() == {'disabled'}
    # FIXME assert cfg_ori.unrestraint.option('ip_address_service_web').property.get() == {'disabled'}
    assert cfg_ori.option('ip_address_service_web').property.get() == {'disabled'}
#    assert not list_sessions()


def test_requires_transitive_owner(config_type):
    a = BoolOption('activate_service', '', True)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(a, notraisepropertyerror=True),
                                                   'expected': ParamValue(False)}))
    b = BoolOption('activate_service_web', '', True, properties=(disabled_property,))
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(b, notraisepropertyerror=True),
                                                   'expected': ParamValue(False)}))

    d = IPOption('ip_address_service_web', '', properties=(disabled_property,))
    od1 = OptionDescription('service', '', [a, b, d])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    cfg.option('activate_service').value.get()
    cfg.option('activate_service_web').value.get()
    cfg.option('ip_address_service_web').value.get()
    #no more default value
    cfg.option('ip_address_service_web').value.set('1.1.1.1')
    cfg.option('activate_service').value.set(False)
    props = []
    try:
        cfg.option('ip_address_service_web').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])
#    assert not list_sessions()


def test_requires_transitive_bis(config_type):
    a = BoolOption('activate_service', '', True)
    abis = BoolOption('activate_service_bis', '', True)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(a, notraisepropertyerror=True),
                                                   'expected': ParamValue(True),
                                                   'reverse_condition': ParamValue(True)}))
    b = BoolOption('activate_service_web', '', True, properties=(disabled_property,))
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(b, notraisepropertyerror=True),
                                                   'expected': ParamValue(True),
                                                   'reverse_condition': ParamValue(True)}))
    d = IPOption('ip_address_service_web', '', properties=(disabled_property,))
    od1 = OptionDescription('service', '', [a, abis, b, d])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    #
    cfg.option('activate_service_web').value.get()
    cfg.option('ip_address_service_web').value.get()
    cfg.option('activate_service').value.set(False)
    #
    props = []
    try:
        cfg.option('activate_service_web').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])
    #
    props = []
    try:
        cfg.option('ip_address_service_web').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])
#    assert not list_sessions()


def test_requires_transitive_hidden_permissive():
    a = BoolOption('activate_service', '', True)
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(a, notraisepropertyerror=True),
                                                 'expected': ParamValue(False)}))
    b = BoolOption('activate_service_web', '', True, properties=(hidden_property,))
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(b, notraisepropertyerror=True),
                                                   'expected': ParamValue(False)}))
    d = IPOption('ip_address_service_web', '', properties=(disabled_property,))
    od1 = OptionDescription('service', '', [a, b, d])
    cfg = Config(od1)
    cfg.property.read_write()
    # FIXME permissive cfg = get_config(cfg, config_type)
    cfg.option('activate_service').value.get()
    cfg.option('ip_address_service_web').value.get()
    cfg.option('ip_address_service_web').value.get()
    cfg.option('activate_service').value.set(False)
    #
    cfg.option('ip_address_service_web').value.get()
#    assert not list_sessions()


def test_requires_transitive_hidden_disabled(config_type):
    a = BoolOption('activate_service', '', True)
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(a, notraisepropertyerror=True),
                                                 'expected': ParamValue(False)}))
    b = BoolOption('activate_service_web', '', True, properties=(hidden_property,))
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(b, notraisepropertyerror=True),
                                                   'expected': ParamValue(False)}))
    d = IPOption('ip_address_service_web', '', properties=(disabled_property,))
    od1 = OptionDescription('service', '', [a, b, d])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    cfg.option('activate_service').value.get()
    cfg.option('activate_service_web').value.get()
    cfg.option('ip_address_service_web').value.get()
    cfg.option('activate_service').value.set(False)
    #
    props = []
    try:
        cfg.option('activate_service_web').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    if config_type == 'tiramisu-api':
        assert frozenset(props) == frozenset(['disabled'])
    else:
        assert frozenset(props) == frozenset(['hidden'])
    cfg.option('ip_address_service_web').value.get()
#    assert not list_sessions()


def test_requires_transitive_hidden_disabled_multiple(config_type):
    a = BoolOption('activate_service', '', True)
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(a, notraisepropertyerror=True),
                                                 'expected': ParamValue(False)}))
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(a, notraisepropertyerror=True),
                                                   'expected': ParamValue(False)}))
    b = BoolOption('activate_service_web', '', True, properties=(hidden_property, disabled_property))
    mandatory_property = Calculation(calc_value,
                                     Params(ParamValue('mandatory'),
                                            kwargs={'condition': ParamOption(b),
                                                    'expected': ParamValue(False)}))
    d = IPOption('ip_address_service_web', '', properties=(mandatory_property,))
    od1 = OptionDescription('service', '', [a, b, d])
    cfg_ori = Config(od1)
    cfg_ori.property.read_write()
    cfg = get_config(cfg_ori, config_type)
    cfg.option('activate_service').value.get()
    cfg.option('activate_service_web').value.get()
    cfg.option('ip_address_service_web').value.get()
    req = None
    if config_type == 'tiramisu-api':
        try:
            cfg.option('activate_service').value.set(False)
        except ConfigError as err:
            req = err
        error_msg = str(_('unable to transform tiramisu object to dict: {}').format(_('cannot access to option {0} because required option {1} has {2} {3}').format('ip_address_service_web', '"activate_service_web"', _('property'), '"disabled"')))
    else:
        cfg.option('activate_service').value.set(False)
        #
        props = []
        try:
            cfg.option('activate_service_web').value.get()
        except PropertiesOptionError as err:
            props = err.proptype
        assert set(props) == {'disabled', 'hidden'}
        del props
        #
        try:
            cfg.option('ip_address_service_web').value.get()
        except ConfigError as err:
            req = err
        error_msg = str(_('unable to carry out a calculation for {}, {}').format('"ip_address_service_web"', _('cannot access to {0} {1} because has {2} {3}').format('option', '"activate_service_web"', _('property'), display_list(['disabled'], add_quote=True))))
    assert req, "ip_address_service_web should raise ConfigError"
    assert str(req) == error_msg
    del req
    #
    cfg_ori.permissive.reset()
    cfg_ori.permissive.remove('hidden')
    if config_type == 'tiramisu-api':
        try:
            cfg = get_config(cfg_ori, config_type)
        except ConfigError as err:
            req = err
        error_msg = str(_('unable to transform tiramisu object to dict: {}').format(_('cannot access to option "{0}" because required option {1} has {2} {3}').format('ip_address_service_web', '"activate_service_web"', _('properties'), '"disabled" {} "hidden"'.format(_('and')))))
    else:
        cfg = get_config(cfg_ori, config_type)
        try:
            cfg.option('ip_address_service_web').value.get()
        except ConfigError as err:
            req = err
        error_msg = str(_('unable to carry out a calculation for {}, {}').format('"ip_address_service_web"', _('cannot access to {0} {1} because has {2} {3}').format('option', '"activate_service_web"', _('properties'), display_list(['hidden', 'disabled'], add_quote=True))))
    assert req, "ip_address_service_web should raise ConfigError"
    assert str(req) == error_msg
    del req
#    assert not list_sessions()


def test_requires_not_transitive(config_type):
    a = BoolOption('activate_service', '', True)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(a, notraisepropertyerror=True),
                                                   'expected': ParamValue(False)}))
    b = BoolOption('activate_service_web', '', True, properties=(disabled_property,))
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(b, notraisepropertyerror=True),
                                                   'no_condition_is_invalid': ParamValue(True),
                                                   'expected': ParamValue(False)}))
    d = IPOption('ip_address_service_web', '', properties=(disabled_property,))
    od1 = OptionDescription('service', '', [a, b, d])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    cfg.option('activate_service').value.get()
    cfg.option('activate_service_web').value.get()
    cfg.option('ip_address_service_web').value.get()
    cfg.option('activate_service').value.set(False)
    #
    props = []
    try:
        cfg.option('activate_service_web').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])
    #
    cfg.option('ip_address_service_web').value.get()
#    assert not list_sessions()


def test_requires_not_transitive_not_same_action(config_type):
    a = BoolOption('activate_service', '', True)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(a, notraisepropertyerror=True),
                                                   'expected': ParamValue(False)}))
    b = BoolOption('activate_service_web', '', True, properties=(disabled_property,))
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(b),
                                                 'expected': ParamValue(False)}))
    d = IPOption('ip_address_service_web', '', properties=(hidden_property,))
    od1 = OptionDescription('service', '', [a, b, d])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    cfg.option('activate_service').value.get()
    cfg.option('activate_service_web').value.get()
    cfg.option('ip_address_service_web').value.get()
    if config_type == 'tiramisu-api':
        with pytest.raises(ConfigError):
            cfg.option('activate_service').value.set(False)
    else:
        cfg.option('activate_service').value.set(False)
        #
        props = []
        try:
            cfg.option('activate_service_web').value.get()
        except PropertiesOptionError as err:
            props = err.proptype
        assert frozenset(props) == frozenset(['disabled'])
        #
        with pytest.raises(ConfigError):
            cfg.option('ip_address_service_web').value.get()
#    assert not list_sessions()


def test_requires_none(config_type):
    a = BoolOption('activate_service', '')
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(a, notraisepropertyerror=True),
                                                   'expected': ParamValue(None)}))
    b = IPOption('ip_address_service', '', properties=(disabled_property,))
    od1 = OptionDescription('service', '', [a, b])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    props = []
    try:
        cfg.option('ip_address_service').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])
    cfg.option('activate_service').value.set(False)
    cfg.option('ip_address_service').value.get()
#    assert not list_sessions()


def test_requires_multi_disabled(config_type):
    a = BoolOption('activate_service', '')
    b = IntOption('num_service', '')
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition_0': ParamOption(a, notraisepropertyerror=True),
                                                   'condition_1': ParamOption(b, notraisepropertyerror=True),
                                                   'expected_0': ParamValue(True),
                                                   'expected_1': ParamValue(1),
                                                   'condition_operator': ParamValue('OR')}))
    c = IPOption('ip_address_service', '', properties=(disabled_property,))
    od1 = OptionDescription('service', '', [a, b, c])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)

    cfg.option('ip_address_service').value.get()

    cfg.option('activate_service').value.set(True)
    props = []
    try:
        cfg.option('ip_address_service').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])

    cfg.option('activate_service').value.set(False)
    cfg.option('ip_address_service').value.get()

    cfg.option('num_service').value.set(1)
    props = []
    try:
        cfg.option('ip_address_service').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])

    cfg.option('activate_service').value.set(True)
    props = []
    try:
        cfg.option('ip_address_service').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])
#    assert not list_sessions()


def test_requires_multi_disabled_inverse(config_type):
    a = BoolOption('activate_service', '')
    b = IntOption('num_service', '')
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition_0': ParamOption(a, notraisepropertyerror=True),
                                                   'condition_1': ParamOption(b, notraisepropertyerror=True),
                                                   'expected_0': ParamValue(True),
                                                   'expected_1': ParamValue(1),
                                                   'condition_operator': ParamValue('OR'),
                                                   'reverse_condition_0': ParamValue(True),
                                                   'reverse_condition_1': ParamValue(True)}))
    c = IPOption('ip_address_service', '', properties=(disabled_property,))
    od1 = OptionDescription('service', '', [a, b, c])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)

    props = []
    try:
        cfg.option('ip_address_service').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])

    cfg.option('activate_service').value.set(True)
    props = []
    try:
        cfg.option('ip_address_service').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])

    cfg.option('activate_service').value.set(False)
    props = []
    try:
        cfg.option('ip_address_service').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])

    cfg.option('num_service').value.set(1)
    props = []
    try:
        cfg.option('ip_address_service').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])

    cfg.option('activate_service').value.set(True)
    cfg.option('ip_address_service').value.get()
#    assert not list_sessions()


def test_requires_multi_disabled_2(config_type):
    a = BoolOption('a', '')
    b = BoolOption('b', '')
    c = BoolOption('c', '')
    d = BoolOption('d', '')
    e = BoolOption('e', '')
    f = BoolOption('f', '')
    g = BoolOption('g', '')
    h = BoolOption('h', '')
    i = BoolOption('i', '')
    j = BoolOption('j', '')
    k = BoolOption('k', '')
    l = BoolOption('l', '')
    m = BoolOption('m', '')
    list_bools = [a, b, c, d, e, f, g, h, i, j, k, l, m]
    requires = []
    kwargs={'expected': ParamValue(True),
            'condition_operator': ParamValue('OR')}
    for idx, boo in enumerate(list_bools):
        kwargs['condition_{}'.format(idx)] = ParamOption(boo, notraisepropertyerror=True)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs=kwargs))
    z = IPOption('z', '', properties=(disabled_property,))
    y = copy(list_bools)
    y.append(z)
    od1 = OptionDescription('service', '', y)
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)

    cfg.option('z').value.get()
    for boo in list_bools:
        cfg.option(boo.impl_getname()).value.set(True)
        props = []
        try:
            cfg.option('z').value.get()
        except PropertiesOptionError as err:
            props = err.proptype
        assert frozenset(props) == frozenset(['disabled'])
    for boo in list_bools:
        cfg.option(boo.impl_getname()).value.set(False)
        if boo == m:
            cfg.option('z').value.get()
        else:
            props = []
            try:
                cfg.option('z').value.get()
            except PropertiesOptionError as err:
                props = err.proptype
            assert frozenset(props) == frozenset(['disabled'])
#    assert not list_sessions()


def test_requires_multi_disabled_inverse_2(config_type):
    a = BoolOption('a', '')
    b = BoolOption('b', '')
    c = BoolOption('c', '')
    d = BoolOption('d', '')
    e = BoolOption('e', '')
    f = BoolOption('f', '')
    g = BoolOption('g', '')
    h = BoolOption('h', '')
    i = BoolOption('i', '')
    j = BoolOption('j', '')
    k = BoolOption('k', '')
    l = BoolOption('l', '')
    m = BoolOption('m', '')
    list_bools = [a, b, c, d, e, f, g, h, i, j, k, l, m]
    requires = []
    kwargs={'expected': ParamValue(True),
            'condition_operator': ParamValue('OR')}
    for idx, boo in enumerate(list_bools):
        kwargs['condition_{}'.format(idx)] = ParamOption(boo, notraisepropertyerror=True)
        kwargs['reverse_condition_{}'.format(idx)] = ParamValue(True)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs=kwargs))
    #for boo in list_bools:
    #    requires.append({'option': boo, 'expected': True, 'action': 'disabled',
    #                     'inverse': True})
    z = IPOption('z', '', properties=(disabled_property,))
    y = copy(list_bools)
    y.append(z)
    od1 = OptionDescription('service', '', y)
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)

    props = []
    try:
        cfg.option('z').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])
    for boo in list_bools:
        cfg.option(boo.impl_getname()).value.set(True)
        if boo != m:
            # it's disabled until last option is modified
            props = []
            try:
                cfg.option('z').value.get()
            except PropertiesOptionError as err:
                props = err.proptype
            assert frozenset(props) == frozenset(['disabled'])
    cfg.option('z').value.get()
    for boo in list_bools:
        cfg.option(boo.impl_getname()).value.set(False)
        props = []
        try:
            cfg.option('z').value.get()
        except PropertiesOptionError as err:
            props = err.proptype
        assert frozenset(props) == frozenset(['disabled'])
    try:
        cfg.option('z').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    for boo in reversed(list_bools):
        cfg.option(boo.impl_getname()).value.set(True)
        if boo != a:
            # it's disabled until last option is modified
            props = []
            try:
                cfg.option('z').value.get()
            except PropertiesOptionError as err:
                props = err.proptype
            assert frozenset(props) == frozenset(['disabled'])
    cfg.option('z').value.get()
#    assert not list_sessions()


def test_requires_requirement_append(config_type):
    a = BoolOption('activate_service', '', True)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(a, notraisepropertyerror=True),
                                                   'expected': ParamValue(False)}))
    b = IPOption('ip_address_service', '', properties=(disabled_property,))
    od1 = OptionDescription('service', '', [a, b])
    cfg_ori = Config(od1)
    cfg_ori.property.read_write()
    cfg = get_config(cfg_ori, config_type)
    cfg.property.get()
    cfg.option('ip_address_service').property.get()
    if config_type == 'tiramisu-api':
        cfg.send()
    #raises(ValueError, "cfg_ori.option('ip_address_service').property.add('disabled')")
    cfg = get_config(cfg_ori, config_type)
    cfg.option('activate_service').value.set(False)
    # disabled is now set, test to remove disabled before store in storage
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.unrestraint.option('ip_address_service').property.add("test")
#    assert not list_sessions()


def test_requires_different_inverse(config_type):
    a = BoolOption('activate_service', '', True)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition_0': ParamOption(a, notraisepropertyerror=True),
                                                   'condition_1': ParamOption(a, notraisepropertyerror=True),
                                                   'expected_0': ParamValue(True),
                                                   'expected_1': ParamValue(True),
                                                   'condition_operator': ParamValue('OR'),
                                                   'reverse_condition_0': ParamValue(True)}))
    b = IPOption('ip_address_service', '', properties=(disabled_property,))
    od1 = OptionDescription('service', '', [a, b])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    #with pytest.raises(PropertiesOptionError):
    #    cfg.option('ip_address_service').value.get()
    cfg.option('activate_service').value.set(False)
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_address_service').value.get()
#    assert not list_sessions()


def test_requires_different_inverse_unicode(config_type):
    a = BoolOption('activate_service', '', True)
    d = StrOption('activate_other_service', '', 'val2')
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition_0': ParamOption(a, notraisepropertyerror=True),
                                                   'condition_1': ParamOption(d, notraisepropertyerror=True),
                                                   'expected_0': ParamValue(True),
                                                   'expected_1': ParamValue('val1'),
                                                   'condition_operator': ParamValue('OR'),
                                                   'reverse_condition_0': ParamValue(True)}))
    b = IPOption('ip_address_service', '', properties=(disabled_property,))
    od1 = OptionDescription('service', '', [a, d, b])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert cfg.option('ip_address_service').value.get() == None
    cfg.option('activate_service').value.set(False)
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_address_service').value.get()
    cfg.option('activate_service').value.set(True)
    assert cfg.option('ip_address_service').value.get() == None
    cfg.option('activate_other_service').value.set('val1')
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_address_service').value.get()
    cfg.option('activate_service').value.set(False)
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_address_service').value.get()
#    assert not list_sessions()


def test_requires_different_inverse_unicode2(config_type):
    a = BoolOption('activate_service', '', False)
    d = StrOption('activate_other_service', '', 'val2')
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition_0': ParamOption(a),
                                                   'condition_1': ParamOption(d),
                                                   'expected_0': ParamValue(True),
                                                   'expected_1': ParamValue(['val2', 'val3']),
                                                   'condition_operator': ParamValue('OR'),
                                                   'reverse_condition_1': ParamValue(True)}))
    b = IPOption('ip_address_service', '', properties=(disabled_property,))
    od1 = OptionDescription('service', '', [a, d, b])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert cfg.option('ip_address_service').value.get() == None
    cfg.option('activate_service').value.set(True)
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_address_service').value.get()
    cfg.option('activate_service').value.set(False)
    assert cfg.option('ip_address_service').value.get() == None
    cfg.option('activate_other_service').value.set('val1')
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_address_service').value.get()
    cfg.option('activate_service').value.set(True)
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_address_service').value.get()
#    assert not list_sessions()


def test_optiondescription_requires():
    a = BoolOption('activate_service', '', True)
    b = BoolOption('ip_address_service', '', multi=True)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(a, notraisepropertyerror=True),
                                                   'expected': ParamValue(False)}))
    OptionDescription('service', '', [b], properties=(disabled_property,))


def test_leadership_requires(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True, properties=('notunique',))
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(ip_admin_eth0, notraisepropertyerror=True),
                                                   'expected': ParamValue('192.168.1.1'),
                                                   'no_condition_is_invalid': ParamValue(True),
                                                   'index': ParamIndex()}))
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True, properties=(disabled_property,))
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('toto', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.2'])
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() is None
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.2']
    #
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.2', '192.168.1.1'])
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() is None
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.get()
    #
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.2', '192.168.1.2'])
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() is None
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.get() is None
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.set('255.255.255.255')
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.get() == '255.255.255.255'
    assert parse_od_get(cfg.value.get()) == {'ip_admin_eth0.ip_admin_eth0': [{'ip_admin_eth0.ip_admin_eth0': '192.168.1.2', 'ip_admin_eth0.netmask_admin_eth0': None},
                                                                      {'ip_admin_eth0.ip_admin_eth0': '192.168.1.2', 'ip_admin_eth0.netmask_admin_eth0': '255.255.255.255'}]}
    #
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.2', '192.168.1.1'])
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() is None
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.get()
    assert parse_od_get(cfg.value.get()) == {'ip_admin_eth0.ip_admin_eth0': [{'ip_admin_eth0.ip_admin_eth0': '192.168.1.2',
                                                                       'ip_admin_eth0.netmask_admin_eth0': None},
                                                                      {'ip_admin_eth0.ip_admin_eth0': '192.168.1.1'}]}
    #
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('255.255.255.255')
    assert parse_od_get(cfg.value.get()) == {'ip_admin_eth0.ip_admin_eth0': [{'ip_admin_eth0.ip_admin_eth0': '192.168.1.2',
                                                                       'ip_admin_eth0.netmask_admin_eth0': '255.255.255.255'},
                                                                      {'ip_admin_eth0.ip_admin_eth0': '192.168.1.1'}]}
#    assert not list_sessions()


def test_leadership_requires_leader(config_type):
    activate = BoolOption('activate', "Activer l'accès au réseau", True)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(activate, notraisepropertyerror=True),
                                                   'expected': ParamValue(False),
                                                   'index': ParamIndex()}))
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0], properties=(disabled_property,))
    od1 = OptionDescription('toto', '', [activate, interface1])
    cfg = Config(od1)
    cfg.property.read_write()

    #
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.2'])
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() is None
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.2']
    #
    cfg.option('activate').value.set(False)
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_admin_eth0.ip_admin_eth0').value.get()
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get()
    #
    cfg.option('activate').value.set(True)
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() is None
    #
    cfg.option('activate').value.set(False)
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_admin_eth0.ip_admin_eth0').value.get()
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get()
    assert parse_od_get(cfg.value.get()) == {'activate': False}
#    assert not list_sessions()


def test_leadership_requires_leadership(config_type):
    activate = BoolOption('activate', "Activer l'accès au réseau", True)
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(activate, notraisepropertyerror=True),
                                                   'expected': ParamValue(False),
                                                   'index': ParamIndex()}))
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0], properties=(disabled_property,))
    od1 = OptionDescription('toto', '', [activate, interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    #
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.2'])
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() is None
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.2']
    #
    cfg.option('activate').value.set(False)
    if config_type != 'tiramisu-api':
        # FIXME
        with pytest.raises(PropertiesOptionError):
            cfg.option('ip_admin_eth0.ip_admin_eth0').value.get()
        with pytest.raises(PropertiesOptionError):
            cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get()
    #
    cfg.option('activate').value.set(True)
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() is None
    #
    cfg.option('activate').value.set(False)
    if config_type != 'tiramisu-api':
        # FIXME
        with pytest.raises(PropertiesOptionError):
            cfg.option('ip_admin_eth0.ip_admin_eth0').value.get()
        with pytest.raises(PropertiesOptionError):
            cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get()
    assert parse_od_get(cfg.value.get()) == {'activate': False}
#    assert not list_sessions()


def test_leadership_requires_no_leader(config_type):
    activate = BoolOption('activate', "Activer l'accès au réseau", True)
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(activate, notraisepropertyerror=True),
                                                   'expected': ParamValue(False)}))
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True, properties=(disabled_property,))
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('toto', '', [activate, interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.2'])
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() is None
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.2']
    cfg.option('activate').value.set(False)
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.2', '192.168.1.1'])
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.2', '192.168.1.1']
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get()
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.get()
    cfg.option('activate').value.set(True)
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() is None
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.get() is None
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.set('255.255.255.255')
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.get() == '255.255.255.255'
    cfg.option('activate').value.set(False)
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get()
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.get()
    assert parse_od_get(cfg.value.get()) == {'activate': False, 'ip_admin_eth0.ip_admin_eth0': [{'ip_admin_eth0.ip_admin_eth0': '192.168.1.2'}, {'ip_admin_eth0.ip_admin_eth0': '192.168.1.1'}]}
#    assert not list_sessions()


def test_leadership_requires_complet(config_type):
    optiontoto = StrOption('unicodetoto', "Unicode")
    option = StrOption('unicode', "Unicode leader", multi=True)
    option1 = StrOption('unicode1', "Unicode follower 1", multi=True)
    option2 = StrOption('unicode2', "Values 'test' must show 'Unicode follower 3'", multi=True)
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(option, notraisepropertyerror=True),
                                                 'expected': ParamValue('test'),
                                                 'index': ParamIndex(),
                                                 'no_condition_is_invalid': ParamValue(True),
                                                 'reverse_condition': ParamValue(True)}))
    option3 = StrOption('unicode3', "Unicode follower 3", properties=(hidden_property,), multi=True)
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(option2, notraisepropertyerror=True),
                                                 'expected': ParamValue('test'),
                                                 'no_condition_is_invalid': ParamValue(True),
                                                 'index': ParamIndex(),
                                                 'reverse_condition': ParamValue(True)}))
    option4 = StrOption('unicode4', "Unicode follower 4", properties=(hidden_property,), multi=True)
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(optiontoto, notraisepropertyerror=True),
                                                 'expected': ParamValue('test'),
                                                 'no_condition_is_invalid': ParamValue(True),
                                                 'reverse_condition': ParamValue(True)}))
    option5 = StrOption('unicode5', "Unicode follower 5", properties=(hidden_property,), multi=True)
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition_0': ParamOption(optiontoto, notraisepropertyerror=True),
                                                 'expected_0': ParamValue('test'),
                                                 'condition_1': ParamOption(option2, notraisepropertyerror=True),
                                                 'expected_1': ParamValue('test'),
                                                 'no_condition_is_invalid': ParamValue(True),
                                                 'condition_operator': ParamValue('OR'),
                                                 'reverse_condition_0': ParamValue(True),
                                                 'reverse_condition_1': ParamValue(True)}))
    option6 = StrOption('unicode6', "Unicode follower 6", properties=(hidden_property,), multi=True)
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition_0': ParamOption(option2, notraisepropertyerror=True),
                                                 'expected_0': ParamValue('test'),
                                                 'condition_1': ParamOption(optiontoto, notraisepropertyerror=True),
                                                 'expected_1': ParamValue('test'),
                                                 'no_condition_is_invalid': ParamValue(True),
                                                 'reverse_condition': ParamValue(True)}))
    option7 = StrOption('unicode7', "Unicode follower 7", properties=(hidden_property,), multi=True)
    descr1 = Leadership("unicode", "Common configuration 1",
                        [option, option1, option2, option3, option4, option5, option6, option7])
    descr = OptionDescription("options", "Common configuration 2", [descr1, optiontoto])
    od1 = OptionDescription("unicode1_leadership_requires", "Leader followers with Unicode follower 3 hidden when Unicode follower 2 is test", [descr])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    cfg.option('options.unicode.unicode').value.set(['test', 'trah'])
    cfg.option('options.unicode.unicode2', 0).value.set('test')
    assert parse_od_get(cfg.value.get()) == {'options.unicode.unicode': [{'options.unicode.unicode': 'test', 'options.unicode.unicode1': None, 'options.unicode.unicode2': 'test', 'options.unicode.unicode3': None, 'options.unicode.unicode4': None}, {'options.unicode.unicode': 'trah', 'options.unicode.unicode1': None, 'options.unicode.unicode2': None}], 'options.unicodetoto': None}
    #
    cfg.option('options.unicodetoto').value.set('test')
    assert parse_od_get(cfg.value.get()) == {'options.unicode.unicode': [{'options.unicode.unicode': 'test', 'options.unicode.unicode1': None, 'options.unicode.unicode2': 'test', 'options.unicode.unicode3': None, 'options.unicode.unicode4': None, 'options.unicode.unicode5': None, 'options.unicode.unicode6': None, 'options.unicode.unicode7': None}, {'options.unicode.unicode': 'trah', 'options.unicode.unicode1': None, 'options.unicode.unicode2': None, 'options.unicode.unicode5': None}], 'options.unicodetoto': 'test'}
#    assert not list_sessions()


def test_leadership_requires_transitive1(config_type):
    optiontoto = StrOption('unicodetoto', "Simple unicode")
    option = StrOption('unicode', "Unicode leader", multi=True)
    option1 = StrOption('unicode1', "Unicode follower 1", multi=True)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(optiontoto, raisepropertyerror=True),
                                                   'expected': ParamValue('test'),
                                                   'reverse_condition': ParamValue(True)}))
    option2 = StrOption('unicode2', "Unicode follower 2", properties=(disabled_property,), multi=True)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(option2, raisepropertyerror=True),
                                                   'expected': ParamValue('test'),
                                                   'index': ParamIndex(),
                                                   'no_condition_is_invalid': ParamValue(True),
                                                   'reverse_condition': ParamValue(True)}))
    option3 = StrOption('unicode3', "Unicode follower 3", properties=(disabled_property,), multi=True)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(option3, raisepropertyerror=True),
                                                   'expected': ParamValue('test'),
                                                   'index': ParamIndex(),
                                                   'no_condition_is_invalid': ParamValue(True),
                                                   'reverse_condition': ParamValue(True)}))
    option4 = StrOption('unicode4', "Unicode follower 4", properties=(disabled_property,), multi=True)
    descr1 = Leadership("unicode", "Common configuration 1",
                        [option, option1, option2, option3, option4])
    descr = OptionDescription("options", "Common configuration 2", [descr1, optiontoto])
    od1 = OptionDescription("unicode1", "", [descr])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert parse_od_get(cfg.value.get()) == {'options.unicode.unicode': [], 'options.unicodetoto': None}
    #
    cfg.option('options.unicodetoto').value.set('test')
    assert parse_od_get(cfg.value.get()) == {'options.unicode.unicode': [], 'options.unicodetoto': 'test'}
    #
    cfg.option('options.unicode.unicode').value.set(['a', 'b', 'c'])
    assert parse_od_get(cfg.value.get()) == {'options.unicode.unicode': [{'options.unicode.unicode': 'a', 'options.unicode.unicode1': None, 'options.unicode.unicode2': None}, {'options.unicode.unicode': 'b', 'options.unicode.unicode1': None, 'options.unicode.unicode2': None}, {'options.unicode.unicode': 'c', 'options.unicode.unicode1': None, 'options.unicode.unicode2': None}], 'options.unicodetoto': 'test'}

    cfg.option('options.unicode.unicode2', 1).value.set('test')
    cfg.option('options.unicode.unicode3', 1).value.set('test')
    assert parse_od_get(cfg.value.get()) == {'options.unicode.unicode': [{'options.unicode.unicode': 'a', 'options.unicode.unicode1': None, 'options.unicode.unicode2': None}, {'options.unicode.unicode': 'b', 'options.unicode.unicode1': None, 'options.unicode.unicode2': 'test', 'options.unicode.unicode3': 'test', 'options.unicode.unicode4': None}, {'options.unicode.unicode': 'c', 'options.unicode.unicode1': None, 'options.unicode.unicode2': None}], 'options.unicodetoto': 'test'}
    #
    cfg.option('options.unicode.unicode2', 1).value.set('rah')
    assert parse_od_get(cfg.value.get()) == {'options.unicode.unicode': [{'options.unicode.unicode': 'a', 'options.unicode.unicode1': None, 'options.unicode.unicode2': None}, {'options.unicode.unicode': 'b', 'options.unicode.unicode1': None, 'options.unicode.unicode2': 'rah'}, {'options.unicode.unicode': 'c', 'options.unicode.unicode1': None, 'options.unicode.unicode2': None}], 'options.unicodetoto': 'test'}
    #
    cfg.option('options.unicode.unicode2', 1).value.set('test')
    cfg.option('options.unicodetoto').value.set('rah')
    assert parse_od_get(cfg.value.get()) == {'options.unicode.unicode': [{'options.unicode.unicode': 'a', 'options.unicode.unicode1': None}, {'options.unicode.unicode': 'b', 'options.unicode.unicode1': None}, {'options.unicode.unicode': 'c', 'options.unicode.unicode1': None}], 'options.unicodetoto': 'rah'}
#    assert not list_sessions()


# FIXME tester l'ajout d'un Calculation
# FIXME permissive peut etre in calcul !
# FIXME Calculation sur des multis ...
