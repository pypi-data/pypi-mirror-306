# -*- coding: utf-8 -*-

"""theses tests are much more to test that config, option description, vs...
**it's there** and answers via attribute access"""
import weakref

from .autopath import do_autopath
do_autopath()
from .config import config_type, get_config, value_list, global_owner

import pytest
from tiramisu import Config, Calculation, Params, ParamSelfInformation, calc_value
from tiramisu.i18n import _
from tiramisu import Config, IntOption, FloatOption, ChoiceOption, \
    BoolOption, StrOption, SymLinkOption, OptionDescription, undefined, \
    DomainnameOption, EmailOption, URLOption, RegexpOption, IPOption, \
    PortOption, NetworkOption, NetmaskOption, BroadcastOption, UsernameOption, \
    GroupnameOption, DateOption, FilenameOption, PasswordOption, MACOption, \
    PermissionsOption
from tiramisu.error import ConflictError, ConfigError, PropertiesOptionError


def make_description():
    gcoption = ChoiceOption('name', 'GC name', ('ref', 'framework'), 'ref')
    gcdummy = BoolOption('dummy', 'dummy', default=False)
    objspaceoption = ChoiceOption('objspace', 'Object space',
                                  ('std', 'thunk'), 'std')
    booloption = BoolOption('bool', 'Test boolean option', default=True)
    intoption = IntOption('int', 'Test int option', default=0)
    floatoption = FloatOption('float', 'Test float option', default=2.3)
    stroption = StrOption('str', 'Test string option', default="abc", properties=('mandatory', ))
    boolop = BoolOption('boolop', 'Test boolean option op', default=True, properties=('hidden',))
    wantref_option = BoolOption('wantref', 'Test requires', default=False, informations={'info': 'default value'})
    wantframework_option = BoolOption('wantframework', 'Test requires',
                                      default=False)

    gcgroup = OptionDescription('gc', '', [gcoption, gcdummy, floatoption])
    descr = OptionDescription('tiram', '', [gcgroup, booloption, objspaceoption,
                                            wantref_option, stroption,
                                            wantframework_option,
                                            intoption, boolop])
    return descr


def test_base_config(config_type):
    """making a :class:`tiramisu.config.Config()` object
    and a :class:`tiramisu.option.OptionDescription()` object
    """
    gcdummy = BoolOption('dummy', 'dummy', default=False)
    od1 = OptionDescription('tiramisu', '', [gcdummy])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert cfg.config.type() == 'config'


def test_base_config_name():
    gcdummy = BoolOption('dummy', 'dummy', default=False)
    od1 = OptionDescription('tiramisu', '', [gcdummy])
    cfg = Config(od1)
    #raises(ValueError, "Config(descr, session_id='unvalid name')")
#    assert not list_sessions()


def test_base_path():
    gcdummy = BoolOption('dummy', 'dummy', default=False)
    od1 = OptionDescription('tiramisu', '', [gcdummy])
    cfg = Config(od1)
    base = OptionDescription('config', '', [od1])
    with pytest.raises(ConfigError):
        with Config(base):
            pass
#    assert not list_sessions()


def test_base_config_force_permissive():
    od1 = make_description()
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.permissive.add('hidden')
    with pytest.raises(PropertiesOptionError):
        cfg.option('boolop').value.get()
    assert cfg.forcepermissive.option('boolop').value.get() is True
#    assert not list_sessions()


def test_base_config_in_a_tree():
    # FIXME
    config_type = 'tiramisu'
    "how options are organized into a tree, see :ref:`tree`"
    od1 = make_description()
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    #
    cfg.option('bool').value.set(False)
    #
    assert cfg.option('gc.name').value.get() == 'ref'
    cfg.option('gc.name').value.set('framework')
    assert cfg.option('gc.name').value.get() == 'framework'
    #
    assert cfg.option('objspace').value.get() == 'std'
    cfg.option('objspace').value.set('thunk')
    assert cfg.option('objspace').value.get() == 'thunk'
    #
    assert cfg.option('gc.float').value.get() == 2.3
    cfg.option('gc.float').value.set(3.4)
    assert cfg.option('gc.float').value.get() == 3.4
    #
    assert cfg.option('int').value.get() == 0
    cfg.option('int').value.set(123)
    assert cfg.option('int').value.get() == 123
    #
    assert cfg.option('wantref').value.get() is False
    cfg.option('wantref').value.set(True)
    assert cfg.option('wantref').value.get() is True
    #
    assert cfg.option('str').value.get() == 'abc'
    cfg.option('str').value.set('def')
    assert cfg.option('str').value.get() == 'def'
    #
    with pytest.raises(AttributeError):
        cfg.option('gc.foo').value.get()
    ##
    cfg = Config(od1)
    assert cfg.option('bool').value.get() is True
    assert cfg.option('gc.name').value.get() == 'ref'
    assert cfg.option('wantframework').value.get() is False
#    assert not list_sessions()


def test_not_valid_properties():
    with pytest.raises(AssertionError):
        stroption = StrOption('str', 'Test string option', default='abc', properties='mandatory')
#    assert not list_sessions()


def test_information_load():
    ChoiceOption('a', '', ('a', 'b'), informations={'info': 'value'})
    BoolOption('a', '', informations={'info': 'value'})
    IntOption('a', '', informations={'info': 'value'})
    FloatOption('a', '', informations={'info': 'value'})
    StrOption('a', '', informations={'info': 'value'})
    RegexpOption('a', '', informations={'info': 'value'})
    IPOption('a', '', informations={'info': 'value'})
    PortOption('a', '', informations={'info': 'value'})
    NetworkOption('a', '', informations={'info': 'value'})
    NetmaskOption('a', '', informations={'info': 'value'})
    BroadcastOption('a', '', informations={'info': 'value'})
    DomainnameOption('a', '', informations={'info': 'value'})
    EmailOption('a', '', informations={'info': 'value'})
    URLOption('a', '', informations={'info': 'value'})
    UsernameOption('a', '', informations={'info': 'value'})
    GroupnameOption('a', '', informations={'info': 'value'})
    DateOption('a', '', informations={'info': 'value'})
    FilenameOption('a', '', informations={'info': 'value'})
    PasswordOption('a', '', informations={'info': 'value'})
    MACOption('a', '', informations={'info': 'value'})
    PermissionsOption('a', '', informations={'info': 'value'})

def test_information_config():
    od1 = make_description()
    cfg = Config(od1)
    string = 'some informations'
    #
    assert list(cfg.information.list()) == ['doc']
    cfg.information.set('info', string)
    assert cfg.information.get('info') == string
    assert set(cfg.information.list()) == {'doc', 'info'}
    #
    with pytest.raises(ValueError):
        cfg.information.get('noinfo')
    assert cfg.information.get('noinfo', 'default') == 'default'
    cfg.information.remove('info')
    with pytest.raises(ValueError):
        cfg.information.remove('info')
    with pytest.raises(ValueError):
        cfg.information.remove('noinfo')
    assert list(cfg.information.list()) == ['doc']
#    assert not list_sessions()


def test_information_config_list():
    od1 = make_description()
    cfg = Config(od1)
    string = 'some informations'
    cfg.information.set('info', string)
    #
    assert cfg.information.exportation() == {None: {'info': string}}
    assert set(cfg.information.list()) == {'info', 'doc'}


def test_information_exportation():
    od1 = make_description()
    cfg = Config(od1)
    string = 'some informations'
    cfg.information.set('info', string)
    #
    assert cfg.information.exportation() == {None: {'info': string}}


def test_information_importation():
    od1 = make_description()
    cfg = Config(od1)
    string = 'some informations'
    assert cfg.information.exportation() == {}
    #
    cfg.information.importation({None: {'info': string}})
    assert cfg.information.exportation() == {None: {'info': string}}


def test_information_option():
    od1 = make_description()
    cfg = Config(od1)
    string = 'some informations'
    #
    assert list(cfg.option('gc.name').information.list()) == ['doc']
    cfg.option('gc.name').information.set('info', string)
    assert cfg.option('gc.name').information.get('info') == string
    assert set(cfg.option('gc.name').information.list()) == {'doc', 'info'}
    #
    with pytest.raises(ValueError):
        cfg.option('gc.name').information.get('noinfo')
    assert cfg.option('gc.name').information.get('noinfo', 'default') == 'default'
    cfg.option('gc.name').information.remove('info')
    with pytest.raises(ValueError):
        cfg.option('gc.name').information.get('info')
    with pytest.raises(ValueError):
        cfg.option('gc.name').information.remove('noinfo')
    assert list(cfg.option('gc.name').information.list()) == ['doc']
    #
    assert cfg.option('wantref').information.get('info') == 'default value'
    cfg.option('wantref').information.set('info', 'default value')
    assert cfg.option('wantref').information.get('info') == 'default value'
    cfg.option('wantref').information.remove('info')
    assert cfg.option('wantref').information.get('info') == 'default value'
#    assert not list_sessions()


def test_information_option_2():
    i1 = IntOption('test1', '', informations={'info': 'value'})
    od1 = OptionDescription('test', '', [i1])
    cfg = Config(od1)
    # it's tuples
    assert set(cfg.option('test1').information.list()) == {'info', 'doc'}
#    assert not list_sessions()


def test_information_option_symlink():
    i1 = IntOption('test1', '', Calculation(calc_value, Params(ParamSelfInformation('info'))), informations={'info': 'value'})
    i2 = SymLinkOption('test2', i1)
    od1 = OptionDescription('test', '', [i2, i1])
    cfg = Config(od1)
    # it's tuples
    assert set(cfg.option('test1').information.list()) == {'info', 'doc'}
    assert set(cfg.option('test2').information.list()) == {'info', 'doc'}
#    assert not list_sessions()


def test_information_optiondescription():
    od1 = make_description()
    cfg = Config(od1)
    string = 'some informations'
    #
    assert list(cfg.option('gc').information.list()) == ['doc']
    cfg.option('gc').information.set('info', string)
    assert cfg.option('gc').information.get('info') == string
    assert set(cfg.option('gc').information.list()) == {'doc', 'info'}
    #
    with pytest.raises(ValueError):
        cfg.option('gc').information.get('noinfo')
    assert cfg.option('gc').information.get('noinfo', 'default') == 'default'
    cfg.option('gc').information.remove('info')
    with pytest.raises(ValueError):
        cfg.option('gc').information.get('info')
    with pytest.raises(ValueError):
        cfg.option('gc').information.remove('noinfo')
    assert list(cfg.option('gc').information.list()) == ['doc']
#    assert not list_sessions()


def compare(val1, val2):
    assert val1 == val2


def test_get_modified_values():
    g1 = IntOption('g1', '', 1)
    g2 = StrOption('g2', '', 'héhé')
    g3 = StrOption('g3', '', 'héhé')
    g4 = BoolOption('g4', '', True)
    g5 = StrOption('g5', '')
    g6 = StrOption('g6', '', multi=True)
    d1 = OptionDescription('od', '', [g1, g2, g3, g4, g5, g6])
    od1 = OptionDescription('root', '', [d1])
    cfg = Config(od1)
    compare(cfg.value.exportation(), {})
    assert not cfg.option('od.g5').ismulti()
    assert not cfg.option('od.g5').issubmulti()
    cfg.option('od.g5').value.set('yes')
    compare(cfg.value.exportation(), {'od.g5': {None: ['yes', 'user']}})
    cfg.option('od.g4').value.set(False)
    compare(cfg.value.exportation(), {'od.g5': {None: ['yes', 'user']}, 'od.g4': {None: [False, 'user']}})
    cfg.option('od.g4').value.set(True)
    compare(cfg.value.exportation(), {'od.g5': {None: ['yes', 'user']}, 'od.g4': {None: [True, 'user']}})
    cfg.option('od.g4').value.reset()
    compare(cfg.value.exportation(), {'od.g5': {None: ['yes', 'user']}})
    assert cfg.option('od.g6').ismulti()
    cfg.option('od.g6').value.set([None])
    compare(cfg.value.exportation(), {'od.g5': {None: ['yes', 'user']}, 'od.g6': {None: [[None], 'user']}})
    cfg.option('od.g6').value.set([])
    compare(cfg.value.exportation(), {'od.g5': {None: ['yes', 'user']}, 'od.g6': {None: [[], 'user']}})
    cfg.option('od.g6').value.set(['3'])
    compare(cfg.value.exportation(), {'od.g5': {None: ['yes', 'user']}, 'od.g6': {None: [['3'], 'user']}})
    cfg.option('od.g6').value.set([])
    compare(cfg.value.exportation(), {'od.g5': {None: ['yes', 'user']}, 'od.g6': {None: [[], 'user']}})
#    assert not list_sessions()


def test_get_modified_values_not_modif(config_type):
    g1 = StrOption('g1', '', multi=True)
    d1 = OptionDescription('od', '', [g1])
    od1 = OptionDescription('root', '', [d1])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert cfg.option('od.g1').value.get() == []
    value = cfg.option('od.g1').value.get()
    value.append('val')
    assert cfg.option('od.g1').value.get() == []
#    assert not list_sessions()


def test_duplicated_option():
    g1 = IntOption('g1', '', 1)
    g1
    #in same OptionDescription
    with pytest.raises(ConflictError):
        d1 = OptionDescription('od', '', [g1, g1])
#    assert not list_sessions()


def test_duplicated_option_diff_od():
    g1 = IntOption('g1', '', 1)
    d1 = OptionDescription('od1', '', [g1])
    #in different OptionDescription
    d2 = OptionDescription('od2', '', [g1, d1])
    d2
    with pytest.raises(ConflictError):
        Config(d2)


def test_cannot_assign_value_to_option_description():
    od1 = make_description()
    cfg = Config(od1)
    with pytest.raises(ConfigError):
        cfg.option('gc').value.set(3)
#    assert not list_sessions()


def test_config_multi(config_type):
    i1 = IntOption('test1', '', multi=True)
    i2 = IntOption('test2', '', multi=True, default_multi=1)
    i3 = IntOption('test3', '', default=[2], multi=True, default_multi=1)
    od1 = OptionDescription('test', '', [i1, i2, i3])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert cfg.option('test1').value.get() == []
    assert cfg.option('test2').value.get() == []
    cfg.option('test2').value.set([1])
    assert cfg.option('test2').value.get() == [1]
    assert cfg.option('test3').value.get() == [2]
    cfg.option('test3').value.set([2, 1])
    assert cfg.option('test3').value.get() == [2, 1]
#    assert not list_sessions()


def test_prefix_error():
    i1 = IntOption('test1', '')
    od1 = OptionDescription('test', '', [i1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.option('test1').value.set(1)
    try:
        cfg.option('test1').value.set('yes')
    except Exception as err:
        assert str(err) == _('"{0}" is an invalid {1} for "{2}"').format('yes', _('integer'), 'test1')
    try:
        cfg.option('test1').value.set('yes')
    except Exception as err:
        err.prefix = ''
        assert str(err) == _('invalid value')
#    assert not list_sessions()


def test_no_validation():
    # FIXME
    config_type = 'tiramisu'
    i1 = IntOption('test1', '')
    od1 = OptionDescription('test', '', [i1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    cfg.option('test1').value.set(1)
    with pytest.raises(ValueError):
        cfg.option('test1').value.set('yes')
    assert cfg.option('test1').value.get() == 1
    cfg.property.remove('validator')
    cfg = get_config(cfg, config_type)
    cfg.option('test1').value.set('yes')
    assert cfg.option('test1').value.get() == 'yes'
    cfg.property.add('validator')
    with pytest.raises(ValueError):
        cfg.option('test1').value.get()
    cfg.option('test1').value.reset()
    assert cfg.option('test1').value.get() is None
#    assert not list_sessions()


#def test_subconfig():
#    i = IntOption('i', '')
#    o = OptionDescription('val', '', [i])
#    od1 = OptionDescription('val', '', [o])
#    cfg = Config(od1)
#    cfg
#    with pytest.raises(TypeError):
#        SubConfig(i, weakref.ref(cfg))
#    assert not list_sessions()


def test_config_subconfig():
    i1 = IntOption('i1', '')
    i2 = IntOption('i2', '', default=1)
    i3 = IntOption('i3', '')
    i4 = IntOption('i4', '', default=2)
    od1 = OptionDescription('od1', '', [i1, i2, i3, i4])
    od2 = OptionDescription('od2', '', [od1])
    cfg = Config(od2)
    with pytest.raises(ConfigError):
        cfg2 = Config(od1)
#    assert not list_sessions()


def test_config_od_name(config_type):
    i = IntOption('i', '')
    s = SymLinkOption('s', i)
    o = OptionDescription('val', '', [i, s])
    o2 = OptionDescription('val', '', [o])
    cfg = Config(o2)
    cfg = get_config(cfg, config_type)
    assert cfg.option('val.i').name() == 'i'
    assert cfg.option('val.s').name() == 's'
    assert cfg.option('val.s').type() == 'integer'
    assert cfg.option('val').type() == 'optiondescription'
#    assert not list_sessions()


def test_config_od_type(config_type):
    i = IntOption('i', '')
    o = OptionDescription('val', '', [i])
    o2 = OptionDescription('val', '', [o])
    cfg = Config(o2)
    cfg = get_config(cfg, config_type)
    assert cfg.option('val').type() == 'optiondescription'
    assert cfg.option('val.i').type() == 'integer'
#    assert not list_sessions()


def test_config_default(config_type):
    i = IntOption('i', '', 8)
    o = OptionDescription('val', '', [i])
    o2 = OptionDescription('val', '', [o])
    cfg = Config(o2)
    cfg = get_config(cfg, config_type)
    assert cfg.option('val.i').value.default() == 8
    cfg.option('val.i').value.set(9)
    assert cfg.option('val.i').value.get() == 9
    assert cfg.option('val.i').value.default() == 8
#    assert not list_sessions()
