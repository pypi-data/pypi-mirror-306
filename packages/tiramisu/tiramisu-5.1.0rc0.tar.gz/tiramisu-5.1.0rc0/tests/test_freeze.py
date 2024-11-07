#test_force_store_value coding: utf-8
"frozen and hidden values"
from .autopath import do_autopath
do_autopath()

import pytest

from tiramisu.setting import owners, groups
from tiramisu import ChoiceOption, BoolOption, IntOption, FloatOption, \
    StrOption, OptionDescription, SymLinkOption, Leadership, Config, \
    Calculation, Params, ParamOption, ParamValue, calc_value
from tiramisu.error import PropertiesOptionError, ConfigError


def compare(calculated, expected):
    assert calculated == expected


#____________________________________________________________
#freeze
def make_description_freeze():
    gcoption = ChoiceOption('name', 'GC name', ('ref', 'framework'), 'ref')
    gcdummy = BoolOption('dummy', 'dummy', default=False)
    objspaceoption = ChoiceOption('objspace', 'Object space',
                                  ('std', 'thunk'), 'std')
    booloption = BoolOption('bool', 'Test boolean option', default=True)
    intoption = IntOption('int', 'Test int option', default=0)
    floatoption = FloatOption('float', 'Test float option', default=2.3)
    stroption = StrOption('str', 'Test string option', default="abc")
    boolop = BoolOption('boolop', 'Test boolean option op', default=[True], multi=True)
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(booloption, raisepropertyerror=True),
                                                 'expected': ParamValue(True),
                                                 'default': ParamValue(None)}))
    wantref_option = BoolOption('wantref', 'Test requires', default=False, properties=('force_store_value', hidden_property))
    wantref2_option = BoolOption('wantref2', 'Test requires', default=False, properties=('force_store_value', 'hidden'))
    wantref3_option = BoolOption('wantref3', 'Test requires', default=[False], multi=True, properties=('force_store_value',))
    st2 = SymLinkOption('st2', wantref3_option)
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(booloption, raisepropertyerror=True),
                                                 'expected': ParamValue(True),
                                                 'default': ParamValue(None)}))
    wantframework_option = BoolOption('wantframework', 'Test requires',
                                      default=False,
                                      properties=(hidden_property,))

    gcgroup = OptionDescription('gc', '', [gcoption, gcdummy, floatoption])
    descr = OptionDescription('tiramisu', '', [gcgroup, booloption, objspaceoption,
                              wantref_option, wantref2_option, wantref3_option, st2, stroption,
                              wantframework_option,
                              intoption, boolop])
    return descr


def return_val():
    return 1


def return_val2(value):
    return value


def return_val3(context, value):
    return value


def test_freeze_whole_config():
    od1 = make_description_freeze()
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.property.add('everything_frozen')
    assert cfg.option('gc.dummy').value.get() is False
    prop = []
    try:
        cfg.option('gc.dummy').value.set(True)
    except PropertiesOptionError as err:
        prop = err.proptype
    assert 'frozen' in prop
    assert cfg.option('gc.dummy').value.get() is False
    #
    cfg.property.remove('everything_frozen')
    cfg.option('gc.dummy').value.set(True)
    assert cfg.option('gc.dummy').value.get() is True
    #
    cfg.property.add('everything_frozen')
    owners.addowner("everythingfrozen2")
    prop = []
    try:
        cfg.option('gc.dummy').owner.set('everythingfrozen2')
    except PropertiesOptionError as err:
        prop = err.proptype
    assert 'frozen' in prop
#    assert not list_sessions()


def test_freeze_one_option():
    "freeze an option "
    od1 = make_description_freeze()
    cfg = Config(od1)
    cfg.property.read_write()
    #freeze only one option
    cfg.option('gc.dummy').property.add('frozen')
    assert cfg.option('gc.dummy').value.get() is False
    prop = []
    try:
        cfg.option('gc.dummy').value.set(True)
    except PropertiesOptionError as err:
        prop = err.proptype
    assert 'frozen' in prop
#    assert not list_sessions()


def test_frozen_value():
    "setattr a frozen value at the config level"
    s = StrOption("string", "", default="string")
    od1 = OptionDescription("options", "", [s])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.property.add('frozen')
    cfg.option('string').property.add('frozen')
    prop = []
    try:
        cfg.option('string').value.set('egg')
    except PropertiesOptionError as err:
        prop = err.proptype
    assert 'frozen' in prop
#    assert not list_sessions()


def test_freeze():
    "freeze a whole configuration object"
    od1 = make_description_freeze()
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.property.add('frozen')
    cfg.option('gc.name').property.add('frozen')
    prop = []
    try:
        cfg.option('gc.name').value.set('framework')
    except PropertiesOptionError as err:
        prop = err.proptype
    assert 'frozen' in prop
#    assert not list_sessions()


def test_freeze_multi():
    od1 = make_description_freeze()
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.property.add('frozen')
    cfg.option('boolop').property.add('frozen')
    prop = []
    try:
        cfg.option('boolop').value.set([True])
    except PropertiesOptionError as err:
        prop = err.proptype
    assert 'frozen' in prop
#    assert not list_sessions()


def test_force_store_value():
    od1 = make_description_freeze()
    cfg = Config(od1)
    compare(cfg.value.exportation(), {})
    cfg.property.read_write()
    compare(cfg.value.exportation(), {'wantref': {None: [False, 'forced']}, 'wantref2': {None: [False, 'forced']}, 'wantref3': {None: [[False], 'forced']}})
    cfg.option('bool').value.set(False)
    cfg.option('wantref').value.set(True)
    cfg.option('bool').value.reset()
    compare(cfg.value.exportation(), {'wantref': {None: [True, 'user']}, 'wantref2': {None: [False, 'forced']}, 'wantref3': {None: [[False], 'forced']}})
    cfg.option('bool').value.set(False)
    cfg.option('wantref').value.reset()
    cfg.option('bool').value.reset()
    compare(cfg.value.exportation(), {'wantref': {None: [False, 'forced']}, 'wantref2': {None: [False, 'forced']}, 'wantref3': {None: [[False], 'forced']}})
#    assert not list_sessions()


def test_force_store_value_leadership_sub():
    b = IntOption('int', 'Test int option', multi=True, properties=('force_store_value',))
    c = StrOption('str', 'Test string option', multi=True)
    descr = Leadership("int", "", [b, c])
    od1 = OptionDescription('odr', '', [descr])
    cfg = Config(od1)
    cfg.property.read_only()
    compare(cfg.value.exportation(), {'int.int': {None: [[], 'forced']}})
#    assert not list_sessions()


def test_force_store_value_callback():
    b = IntOption('int', 'Test int option', Calculation(return_val), properties=('force_store_value',))
    od1 = OptionDescription("int", "", [b])
    cfg = Config(od1)
    cfg.property.read_only()
    compare(cfg.value.exportation(), {'int': {None: [1, 'forced']}})
#    assert not list_sessions()


def test_force_store_value_callback_params():
    b = IntOption('int', 'Test int option', Calculation(return_val2, Params(kwargs={'value': ParamValue(2)})), properties=('force_store_value',))
    od1 = OptionDescription("int", "", [b])
    cfg = Config(od1)
    cfg.property.read_only()
    compare(cfg.value.exportation(), {'int': {None: [2, 'forced']}})
#    assert not list_sessions()


def test_force_store_value_callback_params_with_opt():
    a = IntOption('val1', "", 2)
    b = IntOption('int', 'Test int option', Calculation(return_val2, Params(kwargs={'value': ParamOption(a)})), properties=('force_store_value',))
    od1 = OptionDescription("int", "", [a, b])
    cfg = Config(od1)
    cfg.property.read_only()
    compare(cfg.value.exportation(), {'int': {None: [2, 'forced']}})
#    assert not list_sessions()
