from .autopath import do_autopath
do_autopath()

import pytest
import warnings

from tiramisu import Config
from tiramisu.config import KernelConfig
from tiramisu.setting import groups, owners
from tiramisu import ChoiceOption, BoolOption, IntOption, FloatOption, \
    StrOption, OptionDescription, SymLinkOption, IPOption, NetmaskOption, Leadership, \
    undefined, Calculation, Params, ParamOption, ParamValue, ParamIndex, calc_value, \
    valid_ip_netmask, ParamSelfOption, ParamInformation, ParamSelfInformation
from tiramisu.error import PropertiesOptionError, ConflictError, LeadershipError, ConfigError
from tiramisu.i18n import _
from .config import config_type, get_config, parse_od_get


def return_val():
    return 'val'


def return_concat(*args):
    return '.'.join(list(args))


def return_list(value=None):
    return ['val', 'val']


def return_list2(*args):
    l = []
    for arg in args:
        if isinstance(arg, list):
            l.extend(arg)
        else:
            l.append(arg)
    return l


def return_value(value=None):
    return value


def return_async_value(value=None):
    return value


def return_value2(*args, **kwargs):
    value = list(args)
    value.extend(kwargs.values())
    return value


def return_value3(value=None, index=None):
    if index is not None and isinstance(value, list):
        if len(value) > index:
            return value[index]
        return None
    return value


def return_index(val1, val2=None, index=None, self=None):
    if index is None:
        return [val1, val2]
    if index == 0:
        return val1
    if index == 1:
        return val2

def return_calc(i, j, k):
    return i + j + k


def is_config(config, **kwargs):
    if isinstance(config, KernelConfig):
        return 'yes'
    return 'no'


def return_raise(*arg):
    raise Exception('test')


def return_valueerror(*arg):
    raise ValueError('test')


def make_description_duplicates():
    gcoption = ChoiceOption('name', 'GC name', ('ref', 'framework'), 'ref')
    ## dummy 1
    gcdummy = BoolOption('dummy', 'dummy', default=False)
    objspaceoption = ChoiceOption('objspace', 'Object space',
                                  ('std', 'thunk'), 'std')
    booloption = BoolOption('bool', 'Test boolean option', default=True)
    intoption = IntOption('int', 'Test int option', default=0)
    floatoption = FloatOption('float', 'Test float option', default=2.3)
    stroption = StrOption('str', 'Test string option', default="abc")
    boolop = BoolOption('boolop', 'Test boolean option op', default=True)
    wantref_option = BoolOption('wantref', 'Test requires', default=False)
    wantframework_option = BoolOption('wantframework', 'Test requires',
                                      default=False)
    # dummy2 (same path)
    gcdummy2 = BoolOption('dummy', 'dummy2', default=True)
    # dummy3 (same name)
    gcdummy3 = BoolOption('dummy', 'dummy2', default=True)
    gcgroup = OptionDescription('gc', '', [gcoption, gcdummy, gcdummy2, floatoption])
    descr = OptionDescription('constraints', '', [gcgroup, booloption, objspaceoption,
                              wantref_option, stroption,
                              wantframework_option,
                              intoption, boolop, gcdummy3])
    return descr


def test_identical_paths():
    """If in the schema (the option description) there is something that
    have the same name, an exection is raised
    """
    with warnings.catch_warnings(record=True) as w:
        with pytest.raises(ConflictError):
            make_description_duplicates()


def test_hidden_if_in2(config_type):
    intoption = IntOption('int', 'Test int option', default=0)
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(intoption),
                                                 'expected': ParamValue(1),
                                                 'default': ParamValue(None)}))
    stroption = StrOption('str', 'Test string option', default="abc", properties=(hidden_property,))
    od1 = OptionDescription('constraints', '', [stroption, intoption])
    cfg_ori = Config(od1)
    cfg_ori.property.read_write()
    cfg = get_config(cfg_ori, config_type)
    assert not 'hidden' in cfg.option('str').property.get()
    cfg.option('int').value.set(1)
    with pytest.raises(PropertiesOptionError):
        cfg.option('str').value.get()
    with pytest.raises(PropertiesOptionError):
        cfg.option('str').value.set('uvw')
    if config_type == 'tiramisu-api':
        cfg.send()
    assert 'hidden' in cfg_ori.unrestraint.option('str').property.get()
#    assert not list_sessions()


def test_hidden_if_in3(config_type):
    intoption = IntOption('int', 'Test int option', default=0)
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(intoption),
                                                 'expected': ParamValue(1),
                                                 'default_0': ParamValue(None)}))
    stroption = StrOption('str', 'Test string option', default="abc", properties=(hidden_property,))
    od1 = OptionDescription('constraints', '', [stroption, intoption])
    cfg_ori = Config(od1)
    cfg_ori.property.read_write()
    cfg = get_config(cfg_ori, config_type)
    assert not 'hidden' in cfg.option('str').property.get()
    cfg.option('int').value.set(1)
    with pytest.raises(PropertiesOptionError):
        cfg.option('str').value.get()
    with pytest.raises(PropertiesOptionError):
        cfg.option('str').value.set('uvw')
    if config_type == 'tiramisu-api':
        cfg.send()
    assert 'hidden' in cfg_ori.unrestraint.option('str').property.get()
#    assert not list_sessions()


def test_hidden_if_in_with_group(config_type):
    gcoption = ChoiceOption('name', 'GC name', ('ref', 'framework'), 'ref')
    gcdummy = BoolOption('dummy', 'dummy', default=False)

    floatoption = FloatOption('float', 'Test float option', default=2.3)

    objspaceoption = ChoiceOption('objspace', 'Object space',
                                  ('std', 'thunk'), 'std')
    booloption = BoolOption('bool', 'Test boolean option', default=True)
    intoption = IntOption('int', 'Test int option', default=0)
    stroption = StrOption('str', 'Test string option', default="abc")
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(intoption),
                                                 'expected': ParamValue(1),
                                                 'default': ParamValue(None)}))
    gcgroup = OptionDescription('gc', '', [gcoption, gcdummy, floatoption], properties=(hidden_property,))
    od1 = OptionDescription('constraints', '', [gcgroup, booloption,
                              objspaceoption, stroption, intoption])
    cfg_ori = Config(od1)
    cfg_ori.property.read_write()
    cfg = get_config(cfg_ori, config_type)
    assert not 'hidden' in cfg_ori.option('str').property.get()
    cfg.option('int').value.set(1)
    if config_type == 'tiramisu-api':
        cfg.send()
    with pytest.raises(PropertiesOptionError):
        cfg_ori.option('gc.name').value.get()
#    assert not list_sessions()


def test_disabled_with_group():
    gcoption = ChoiceOption('name', 'GC name', ('ref', 'framework'), 'ref')
    gcdummy = BoolOption('dummy', 'dummy', default=False)

    floatoption = FloatOption('float', 'Test float option', default=2.3)

    objspaceoption = ChoiceOption('objspace', 'Object space',
                                  ('std', 'thunk'), 'std')
    booloption = BoolOption('bool', 'Test boolean option', default=True)
    intoption = IntOption('int', 'Test int option', default=0)
    stroption = StrOption('str', 'Test string option', default="abc")
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(intoption),
                                                   'expected': ParamValue(1),
                                                   'default': ParamValue(None)}))
    gcgroup = OptionDescription('gc', '', [gcoption, gcdummy, floatoption], properties=(disabled_property,))
    od1 = OptionDescription('constraints', '', [gcgroup, booloption,
                                                  objspaceoption, stroption, intoption])
    cfg = Config(od1)
    cfg.property.read_write()
    assert cfg.option('gc.name').value.get()
    cfg.option('int').value.set(1)
    with pytest.raises(PropertiesOptionError):
        cfg.option('gc.name').value.get()
#    assert not list_sessions()
#____________________________________________________________


def make_description_callback():
    gcoption = ChoiceOption('name', 'GC name', ('ref', 'framework'), 'ref')
    gcdummy = BoolOption('dummy', 'dummy')
    objspaceoption = ChoiceOption('objspace', 'Object space',
                                  ('std', 'thunk'), 'std')
    booloption = BoolOption('bool', 'Test boolean option', default=True)
    intoption = IntOption('int', 'Test int option', default=0)
    floatoption = FloatOption('float', 'Test float option', default=2.3)
    stroption = StrOption('str', 'Test string option', default="abc")
    boolop = BoolOption('boolop', 'Test boolean option op', default=True)
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(boolop),
                                                 'expected': ParamValue(True),
                                                 'default': ParamValue(None)}))
    wantref_option = BoolOption('wantref', 'Test requires', default=False, properties=(hidden_property,))
    wantframework_option = BoolOption('wantframework', 'Test requires',
                                      default=False,
                                      properties=(hidden_property,))
    gcgroup = OptionDescription('gc', '', [gcoption, gcdummy, floatoption])
    descr = OptionDescription('constraints', '', [gcgroup, booloption, objspaceoption,
                              wantref_option, stroption,
                              wantframework_option,
                              intoption, boolop])
    return descr


def test_has_callback():
    od1 = make_description_callback()
    # here the owner is 'default'
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.option('bool').value.set(False)
    # because dummy has a callback
    cfg.property.add('freeze')
    cfg.option('gc.dummy').property.add('frozen')
    with pytest.raises(PropertiesOptionError):
        cfg.option('gc.dummy').value.set(True)
#    assert not list_sessions()


def test_freeze_and_has_callback():
    od1 = make_description_callback()
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.option('bool').value.set(False)
    cfg.property.add('freeze')
    cfg.option('gc.dummy').property.add('frozen')
    with pytest.raises(PropertiesOptionError):
        cfg.option('gc.dummy').value.set(True)
#    assert not list_sessions()


def test_callback(config_type):
    val1 = StrOption('val1', "", Calculation(return_val))
    val2 = StrOption('val2', "")
    od1 = OptionDescription('rootconfig', '', [val1, val2])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert isinstance(cfg.option('val1').value.get(uncalculated=True), Calculation)
    assert cfg.option('val1').value.get() == 'val'
    cfg.option('val1').value.set('new-val')
    assert cfg.option('val1').value.get() == 'new-val'
    with pytest.raises(ConfigError):
        assert cfg.option('val1').value.defaultmulti() == None
    cfg.option('val1').value.reset()
    assert cfg.option('val1').value.get() == 'val'
#    assert not list_sessions()


def test_callback_set(config_type):
    val1 = StrOption('val1', "")
    val2 = StrOption('val2', "")
    od1 = OptionDescription('rootconfig', '', [val1, val2])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    cfg.option('val2').value.set(Calculation(return_value, Params(ParamOption(val1))))
    assert cfg.option('val2').value.get() == None
    #
    cfg.option('val1').value.set('new-val')
    assert cfg.option('val2').value.get() == 'new-val'
    #
    cfg.option('val1').value.reset()
    assert cfg.option('val2').value.get() == None


def test_params():
    with pytest.raises(ValueError):
        Params('str')
    with pytest.raises(ValueError):
        Params(('str',))
    with pytest.raises(ValueError):
        Params(kwargs={'a': 'str'})


def test_param_option():
    val1 = StrOption('val1', "")
    with pytest.raises(ValueError):
        ParamOption('str')
    with pytest.raises(AssertionError):
        ParamOption(val1, 'str')


def test_callback_with_error(config_type):
    val1 = StrOption("val1", "", Calculation(is_config, Params(ParamValue('string'), kwargs={'value': ParamValue('string')})))
    od1 = OptionDescription('rootconfig', '', [val1])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert cfg.option('val1').value.get() == 'no'
#    assert not list_sessions()


def test_callback_value(config_type):
    val1 = StrOption('val1', "", 'val')
    val2 = StrOption('val2', "", Calculation(return_value, Params(ParamOption(val1))))
    val3 = StrOption('val3', "", Calculation(return_value, Params(ParamValue('yes'))))
    val4 = StrOption('val4', "", Calculation(return_value, Params(kwargs={'value': ParamOption(val1)})))
    val5 = StrOption('val5', "", Calculation(return_value, Params(ParamValue('yes'))))
    od1 = OptionDescription('rootconfig', '', [val1, val2, val3, val4, val5])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert cfg.option('val1').value.get() == 'val'
    assert cfg.option('val2').value.get() == 'val'
    assert cfg.option('val4').value.get() == 'val'
    cfg.option('val1').value.set('new-val')
    assert cfg.option('val1').value.get() == 'new-val'
    assert cfg.option('val2').value.get() == 'new-val'
    assert cfg.option('val4').value.get() == 'new-val'
    cfg.option('val1').value.reset()
    assert cfg.option('val1').value.get() == 'val'
    assert cfg.option('val2').value.get() == 'val'
    assert cfg.option('val3').value.get() == 'yes'
    assert cfg.option('val4').value.get() == 'val'
    assert cfg.option('val5').value.get() == 'yes'
#    assert not list_sessions()


def test_callback_async_value(config_type):
    val1 = StrOption('val1', "", 'val')
    val2 = StrOption('val2', "", Calculation(return_async_value, Params(ParamOption(val1))))
    val3 = StrOption('val3', "", Calculation(return_async_value, Params(ParamValue('yes'))))
    val4 = StrOption('val4', "", Calculation(return_async_value, Params(kwargs={'value': ParamOption(val1)})))
    val5 = StrOption('val5', "", Calculation(return_async_value, Params(ParamValue('yes'))))
    od1 = OptionDescription('rootconfig', '', [val1, val2, val3, val4, val5])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert cfg.option('val1').value.get() == 'val'
    assert cfg.option('val2').value.get() == 'val'
    assert cfg.option('val4').value.get() == 'val'
    cfg.option('val1').value.set('new-val')
    assert cfg.option('val1').value.get() == 'new-val'
    assert cfg.option('val2').value.get() == 'new-val'
    assert cfg.option('val4').value.get() == 'new-val'
    cfg.option('val1').value.reset()
    assert cfg.option('val1').value.get() == 'val'
    assert cfg.option('val2').value.get() == 'val'
    assert cfg.option('val3').value.get() == 'yes'
    assert cfg.option('val4').value.get() == 'val'
    assert cfg.option('val5').value.get() == 'yes'
#    assert not list_sessions()


def test_callback_information(config_type):
    val1 = StrOption('val1', "", Calculation(return_value, Params(ParamInformation('information', 'no_value'))))
    val2 = StrOption('val2', "", Calculation(return_value, Params(ParamInformation('information'))))
    od1 = OptionDescription('rootconfig', '', [val1, val2])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert cfg.option('val1').value.get() == 'no_value'
    with pytest.raises(ConfigError):
        cfg.option('val2').value.get()
    cfg.information.set('information', 'new_value')
    assert cfg.option('val1').value.get() == 'new_value'
    assert cfg.option('val2').value.get() == 'new_value'
    cfg.information.set('information', 'new_value2')
    assert cfg.option('val1').value.get() == 'new_value2'
    assert cfg.option('val2').value.get() == 'new_value2'
#    assert not list_sessions()


def test_callback_information2(config_type):
    val1 = StrOption('val1', "", Calculation(return_value, Params(ParamSelfInformation('information', 'no_value'))))
    val2 = StrOption('val2', "", Calculation(return_value, Params(ParamSelfInformation('information'))), informations={'information': 'new_value'})
    val3 = StrOption('val3', "", Calculation(return_value, Params(ParamSelfInformation('information'))))
    od1 = OptionDescription('rootconfig', '', [val1, val2, val3])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert cfg.option('val1').value.get() == 'no_value'
    assert cfg.option('val2').value.get() == 'new_value'
    with pytest.raises(ConfigError):
        cfg.option('val3').value.get()
    cfg.option('val2').information.set('information', 'new_value2')
    assert cfg.option('val2').value.get() == 'new_value2'
#    assert not list_sessions()


def test_callback_information3(config_type):
    val1 = StrOption('val1', "", informations={'information': 'new_value'})
    val2 = StrOption('val2', "", Calculation(return_value, Params(ParamInformation('information', option=val1))))
    od1 = OptionDescription('rootconfig', '', [val1, val2])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert cfg.option('val2').value.get() == 'new_value'
    cfg.option('val1').information.set('information', 'new_value2')
    assert cfg.option('val2').value.get() == 'new_value2'


def test_callback_value_tuple(config_type):
    val1 = StrOption('val1', "", 'val1')
    val2 = StrOption('val2', "", 'val2')
    val3 = StrOption('val3', "", Calculation(return_concat, Params((ParamOption(val1), ParamOption(val2)))))
    val4 = StrOption('val4', "", Calculation(return_concat, Params((ParamValue('yes'), ParamValue('no')))))
    od1 = OptionDescription('rootconfig', '', [val1, val2, val3, val4])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert cfg.option('val1').value.get() == 'val1'
    assert cfg.option('val2').value.get() == 'val2'
    assert cfg.option('val3').value.get() == 'val1.val2'
    assert cfg.option('val4').value.get() == 'yes.no'
    cfg.option('val1').value.set('new-val')
    assert cfg.option('val3').value.get() == 'new-val.val2'
    cfg.option('val1').value.reset()
    assert cfg.option('val3').value.get() == 'val1.val2'
#    assert not list_sessions()


def test_callback_value_force_permissive2(config_type):
    val1 = StrOption('val1', "", 'val', properties=('disabled',))
    val2 = StrOption('val2', "", Calculation(return_value, Params(ParamOption(val1))))
    val3 = StrOption('val3', "", Calculation(return_value, Params(ParamOption(val1, True))))
    od1 = OptionDescription('rootconfig', '', [val1, val2, val3])
    cfg = Config(od1)
    cfg.property.read_only()
    if config_type != 'tiramisu-api':
        with pytest.raises(ConfigError):
            cfg.option('val2').value.get()
        cfg.option('val3').value.get() is None
    else:
        with pytest.raises(ConfigError):
            get_config(cfg, config_type)
#    assert not list_sessions()


def test_callback_value_force_permissive_kwargs():
    val1 = StrOption('val1', "", 'val', properties=('disabled',))
    val2 = StrOption('val2', "", Calculation(return_value, Params(value=ParamOption(val1))))
    val3 = StrOption('val3', "", Calculation(return_value, Params(value=ParamOption(val1, True))))
    od1 = OptionDescription('rootconfig', '', [val1, val2, val3])
    cfg = Config(od1)
    cfg.property.read_only()
    with pytest.raises(ConfigError):
        cfg.option('val2').value.get()
    cfg.option('val3').value.get() is None
#    assert not list_sessions()


def test_callback_symlink(config_type):
    val1 = StrOption('val1', "", 'val')
    val2 = SymLinkOption('val2', val1)
    val3 = StrOption('val3', "", Calculation(return_value, Params(ParamOption(val2))))
    od1 = OptionDescription('rootconfig', '', [val1, val2, val3])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert cfg.option('val1').value.get() == 'val'
    assert cfg.option('val2').value.get() == 'val'
    assert cfg.option('val3').value.get() == 'val'
    cfg.option('val1').value.set('new-val')
    assert cfg.option('val1').value.get() == 'new-val'
    assert cfg.option('val3').value.get() == 'new-val'
    cfg.option('val1').value.reset()
    assert cfg.option('val1').value.get() == 'val'
    assert cfg.option('val3').value.get() == 'val'
#    assert not list_sessions()


def test_callback_list():
    val1 = StrOption('val1', "", Calculation(return_list))
    od1 = OptionDescription('rootconfig', '', [val1])
    cfg = Config(od1)
    cfg.property.read_write()
    with pytest.raises(ValueError):
        cfg.option('val1').value.get()
    assert cfg.option('val1').value.valid() is False
#    assert not list_sessions()


def test_callback_list2():
    val1 = StrOption('val1', "", Calculation(return_list))
    val2 = StrOption('val2', "", Calculation(return_value, Params(ParamOption(val1))))
    od1 = OptionDescription('rootconfig', '', [val1, val2])
    cfg = Config(od1)
    cfg.property.read_write()
    with pytest.raises(ValueError):
        cfg.option('val1').value.get()
    assert cfg.option('val1').value.valid() is False
    #cfg.val2
    with pytest.raises(ValueError):
        cfg.option('val2').value.get()
    assert cfg.option('val2').value.valid() is False
#    assert not list_sessions()


def test_callback_multi(config_type):
    val1 = StrOption('val1', "", [Calculation(return_val)], multi=True)
    od1 = OptionDescription('rootconfig', '', [val1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert cfg.option('val1').value.get() == ['val']
    cfg.option('val1').value.set(['new-val'])
    assert cfg.option('val1').value.defaultmulti() == None
    assert cfg.option('val1').value.get() == ['new-val']
    cfg.option('val1').value.set(['new-val', 'new-val2'])
    assert cfg.option('val1').value.get() == ['new-val', 'new-val2']
    cfg.option('val1').value.reset()
    assert cfg.option('val1').value.get() == ['val']
#    assert not list_sessions()


def test_callback_multi_set(config_type):
    val1 = StrOption('val1', "", multi=True)
    od1 = OptionDescription('rootconfig', '', [val1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert cfg.option('val1').value.get() == []
    #
    cfg.option('val1').value.set([Calculation(return_val)])
    assert cfg.option('val1').value.get() == ['val']
    cfg.option('val1').value.reset()
    assert cfg.option('val1').value.get() == []
#    assert not list_sessions()


def test_callback_multi_value(config_type):
    val1 = StrOption('val1', "", ['val'], multi=True)
    option = ParamOption(val1)
    params1 = Params((option,))
    value = ParamValue('yes')
    params2 = Params((value,))
    params3 = Params((option, value))
    val2 = StrOption('val2', "", Calculation(return_value, params1), multi=True)
    val3 = StrOption('val3', "", [Calculation(return_value, params2)], multi=True)
    val4 = StrOption('val4', "", Calculation(return_list2, params3), multi=True)
    od1 = OptionDescription('rootconfig', '', [val1, val2, val3, val4])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert cfg.option('val1').value.get() == ['val']
    assert cfg.option('val2').value.get() == ['val']
    assert cfg.option('val4').value.get() == ['val', 'yes']
    cfg.option('val1').value.set(['new-val'])
    assert cfg.option('val1').value.get() == ['new-val']
    assert cfg.option('val2').value.get() == ['new-val']
    assert cfg.option('val4').value.get() == ['new-val', 'yes']
    cfg.option('val1').value.set(['new-val', 'new-val2'])
    assert cfg.option('val1').value.get() == ['new-val', 'new-val2']
    assert cfg.option('val2').value.get() == ['new-val', 'new-val2']
    assert cfg.option('val4').value.get() == ['new-val', 'new-val2', 'yes']
    cfg.option('val1').value.reset()
    assert cfg.option('val1').value.get() == ['val']
    assert cfg.option('val2').value.get() == ['val']
    assert cfg.option('val3').value.get() == ['yes']
    assert cfg.option('val4').value.get() == ['val', 'yes']
    cfg.option('val2').value.set(['val', 'new'])
    assert cfg.option('val1').value.get() == ['val']
    assert cfg.option('val2').value.get() == ['val', 'new']
#    assert not list_sessions()


def test_callback_multi_value_set(config_type):
    val1 = StrOption('val1', "", ['val1'], multi=True)
    val2 = StrOption('val2', "", ['val2'], multi=True)
    od1 = OptionDescription('rootconfig', '', [val1, val2])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert cfg.option('val1').value.get() == ['val1']
    assert cfg.option('val2').value.get() == ['val2']
    #
    cfg.option('val2').value.set(Calculation(return_value, Params(ParamOption(val1))))
    assert cfg.option('val1').value.get() == ['val1']
    assert cfg.option('val2').value.get() == ['val1']
    #
    cfg.option('val1').value.set(['val1', 'yes'])
    assert cfg.option('val2').value.get() == ['val1', 'yes']
    assert cfg.option('val2').value.get() == ['val1', 'yes']
    #
    cfg.option('val2').value.reset()
    assert cfg.option('val1').value.get() == ['val1', 'yes']
    assert cfg.option('val2').value.get() == ['val2']
#    assert not list_sessions()


def test_callback_multi_list(config_type):
    val1 = StrOption('val1', "", Calculation(return_list), multi=True, properties=('notunique',))
    od1 = OptionDescription('rootconfig', '', [val1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert cfg.option('val1').value.get() == ['val', 'val']
    cfg.option('val1').value.set(['new-val'])
    assert cfg.option('val1').value.get() == ['new-val']
    cfg.option('val1').value.set(['new-val', 'new-val2'])
    assert cfg.option('val1').value.get() == ['new-val', 'new-val2']
    cfg.option('val1').value.reset()
    assert cfg.option('val1').value.get() == ['val', 'val']
#    assert not list_sessions()


def test_callback_multi_list_extend(config_type):
    val1 = StrOption('val1', "", Calculation(return_list2, Params((ParamValue(['1', '2', '3']), ParamValue(['4', '5'])))), multi=True)
    od1 = OptionDescription('rootconfig', '', [val1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert cfg.option('val1').value.get() == ['1', '2', '3', '4', '5']
#    assert not list_sessions()


def test_callback_multi_callback(config_type):
    val1 = StrOption('val1', "", [Calculation(return_val)], multi=True)
    interface1 = OptionDescription('val1', '', [val1])
    od1 = OptionDescription('rootconfig', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert cfg.option('val1.val1').value.get() == ['val']
    cfg.option('val1.val1').value.set(['val1', None])
    assert cfg.option('val1.val1').value.get() == ['val1', None]
#    assert not list_sessions()


def test_callback_multi_callback_default(config_type):
    val1 = StrOption('val1', "", default_multi=Calculation(return_val), multi=True)
    interface1 = OptionDescription('val1', '', [val1])
    od1 = OptionDescription('rootconfig', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert cfg.option('val1.val1').value.get() == []
    cfg.option('val1.val1').value.set(['val1', 'val'])
    assert cfg.option('val1.val1').value.get() == ['val1', 'val']
#    assert not list_sessions()


def test_callback_leader_and_followers_leader(config_type):
    val1 = StrOption('val1', "", default=['val'], multi=True)
    val2 = StrOption('val2', "", default=Calculation(return_value, Params(ParamOption(val1))), default_multi=Calculation(return_val), multi=True, properties=('notunique',))
    val3 = StrOption('val3', "", multi=True)
    interface1 = Leadership('val2', '', [val2, val3])
    od1 = OptionDescription('rootconfig', '', [val1, interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert cfg.option('val1').value.get() == ['val']
    assert cfg.option('val2.val2').value.get() == ['val']
    #
    cfg.option('val1').value.set(['val1', 'val2'])
    assert cfg.option('val1').value.get() == ['val1', 'val2']
    assert cfg.option('val2.val2').value.get() == ['val1', 'val2']
    assert cfg.option('val2.val3', 0).value.get() == None
    assert cfg.option('val2.val3', 1).value.get() == None
    #
    cfg.option('val1').value.set(['val'])
    assert cfg.option('val2.val2').value.get() == ['val']
    assert cfg.option('val2.val3', 0).value.get() == None
#    assert not list_sessions()


def test_callback_leader_and_followers_leader_set(config_type):
    val1 = StrOption('val1', "", default=['val1', 'val2'], multi=True)
    val2 = StrOption('val2', "", multi=True)
    val3 = StrOption('val3', "", multi=True)
    interface1 = Leadership('val2', '', [val2, val3])
    od1 = OptionDescription('rootconfig', '', [val1, interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert cfg.option('val1').value.get() == ['val1', 'val2']
    #
    cfg.option('val2.val2').value.set(Calculation(return_value, Params(ParamOption(val1))))
    assert cfg.option('val2.val2').value.get() == ['val1', 'val2']
    assert cfg.option('val2.val3', 0).value.get() == None
    assert cfg.option('val2.val3', 1).value.get() == None
    #assert not list_sessions()


def test_callback_follower(config_type):
    val1 = StrOption('val1', "", multi=True)
    val2 = StrOption('val2', "", Calculation(return_value3, Params(ParamValue(['string', 'new']), {'index': ParamIndex()})), multi=True)
    interface1 = Leadership('val1', '', [val1, val2])
    od1 = OptionDescription('rootconfig', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    cfg.option('val1.val1').value.set(['val'])
    assert cfg.option('val1.val2', 0).value.get() == 'string'
    cfg.option('val1.val1').value.set(['val', 'val1'])
    assert cfg.option('val1.val2', 0).value.get() == 'string'
    assert cfg.option('val1.val2', 1).value.get() == 'new'
    cfg.option('val1.val1').value.set(['val', 'val1', 'val2'])
    assert cfg.option('val1.val2', 0).value.get() == 'string'
    assert cfg.option('val1.val2', 1).value.get() == 'new'
    assert cfg.option('val1.val2', 2).value.get() == None
    cfg.option('val1.val1').value.set(['val', 'val1', 'val2', 'val3'])
    assert cfg.option('val1.val2', 0).value.get() == 'string'
    assert cfg.option('val1.val2', 1).value.get() == 'new'
    assert cfg.option('val1.val2', 2).value.get() == None
    assert cfg.option('val1.val2', 3).value.get() == None
#    assert not list_sessions()


def test_callback_follower_set(config_type):
    val1 = StrOption('val1', "")
    val2 = StrOption('val2', "", default=['val1'], multi=True)
    val3 = StrOption('val3', "", multi=True)
    interface1 = Leadership('val2', '', [val2, val3])
    od1 = OptionDescription('rootconfig', '', [val1, interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    cfg.option('val1').value.set('val')
    assert cfg.option('val1').value.get() == 'val'
    assert cfg.option('val2.val2').value.get() == ['val1']
    assert cfg.option('val2.val3', 0).value.get() == None
    #
    cfg.option('val2.val3', 0).value.set(Calculation(return_value, Params(ParamOption(val1))))
    assert cfg.option('val2.val3', 0).value.get() == 'val'
    #
    cfg.option('val1').value.set('val1')
    assert cfg.option('val2.val3', 0).value.get() == 'val1'
#    assert not list_sessions()


def test_callback_leader_and_followers_leader2(config_type):
    val1 = StrOption('val1', "", multi=True)
    val2 = StrOption('val2', "", multi=True, default_multi='val2')
    val3 = StrOption('val3', "", Calculation(calc_value, Params(ParamOption(val2), {'index': ParamIndex()})), multi=True)
    val4 = StrOption('val4', "", Calculation(calc_value, Params(ParamOption(val3), {'index': ParamIndex()})), multi=True)
    interface1 = Leadership('val1', '', [val1, val2, val3, val4])
    od1 = OptionDescription('rootconfig', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    cfg.option('val1.val1').value.set(['val'])
    assert cfg.option('val1.val4', 0).value.get() == 'val2'
    assert cfg.option('val1.val3', 0).value.get() == 'val2'
    assert cfg.option('val1.val2', 0).value.get() == 'val2'
#    assert not list_sessions()


def test_callback_leader_and_followers_leader_mandatory1(config_type):
    val = StrOption('val', "", default='val')
    val1 = StrOption('val1', "", Calculation(return_value2, Params(ParamOption(val))), properties=('mandatory',), multi=True)
    val3 = StrOption('val3', "", Calculation(return_index, Params(ParamOption(val1), {'index': ParamIndex()})), properties=('mandatory',), multi=True)
    val4 = StrOption('val4', "", Calculation(return_index, Params(ParamOption(val1), {'index': ParamIndex()})), properties=('mandatory',), multi=True)
    interface1 = Leadership('val1', '', [val1, val3, val4])
    od1 = OptionDescription('rootconfig', '', [val, interface1])
    cfg_ori = Config(od1)
    cfg_ori.property.read_only()
    cfg = get_config(cfg_ori, config_type)
    assert cfg.option('val1.val3', 0).value.get() == 'val'
    assert cfg.option('val1.val4', 0).value.get() == 'val'
    assert cfg.option('val1.val1').value.get() == ['val']
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.property.read_write()
    cfg = get_config(cfg_ori, config_type)
    cfg.option('val1.val1').value.set(['val', 'val3'])
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.property.read_only()
    cfg = get_config(cfg_ori, config_type)
    assert cfg.option('val1.val1').value.get() == ['val', 'val3']
    assert cfg.option('val1.val3', 0).value.get() == 'val'
    if config_type != 'tiramisu-api':
        # FIXME
        with pytest.raises(PropertiesOptionError):
            cfg.option('val1.val3', 1).value.get()
        with pytest.raises(PropertiesOptionError):
            cfg.option('val1.val4', 1).value.get()
#    assert not list_sessions()


def test_callback_leader_and_followers_leader_mandatory2(config_type):
    val = StrOption('val', "", default='val')
    val_ = StrOption('val_', "", default='val_')
    val1 = StrOption('val1', "", Calculation(return_index, Params(ParamOption(val), {'val2': ParamOption(val_)})), properties=('mandatory',), multi=True)
    val3 = StrOption('val3', "", Calculation(return_index, Params(ParamOption(val1), {'val2': ParamOption(val_), 'index': ParamIndex()})), properties=('mandatory',), multi=True)
    val4 = StrOption('val4', "", Calculation(return_index, Params(ParamOption(val1), {'val2': ParamOption(val_), 'index': ParamIndex()})), properties=('mandatory',), multi=True)
    interface1 = Leadership('val1', '', [val1, val3, val4])
    od1 = OptionDescription('rootconfig', '', [val, val_, interface1])
    cfg_ori = Config(od1)
    cfg_ori.property.read_only()
    cfg = get_config(cfg_ori, config_type)
    assert cfg.option('val1.val3', 0).value.get() == 'val'
    assert cfg.option('val1.val3', 1).value.get() == 'val_'
    assert cfg.option('val1.val4', 0).value.get() == 'val'
    assert cfg.option('val1.val4', 1).value.get() == 'val_'
    assert cfg.option('val1.val1').value.get() == ['val', 'val_']
    cfg_ori.property.read_write()
    cfg = get_config(cfg_ori, config_type)
    cfg.option('val1.val1').value.set(['val', 'val_', 'val3'])
    assert cfg.option('val1.val1').value.get() == ['val', 'val_', 'val3']
    cfg_ori.property.read_only()
    cfg = get_config(cfg_ori, config_type)
    assert cfg.option('val1.val3', 0).value.get() == 'val'
    assert cfg.option('val1.val3', 1).value.get() == 'val_'
    assert cfg.option('val1.val4', 0).value.get() == 'val'
    assert cfg.option('val1.val4', 1).value.get() == 'val_'
    if config_type != 'tiramisu-api':
        # FIXME
        with pytest.raises(PropertiesOptionError):
            cfg.option('val1.val3', 2).value.get()
        with pytest.raises(PropertiesOptionError):
            cfg.option('val1.val4', 2).value.get()
    assert cfg.option('val1.val1').value.get() == ['val', 'val_', 'val3']
#    assert not list_sessions()


def test_callback_leader_and_followers_leader_mandatory3(config_type):
    val = StrOption('val', "", default='val')
    val_ = StrOption('val_', "", default='val_')
    val1 = StrOption('val1', "", Calculation(return_value2, Params(ParamOption(val), {'val': ParamOption(val_)})), properties=('mandatory',), multi=True)
    val3 = StrOption('val3', "", Calculation(calc_value, Params(ParamOption(val1), {'index': ParamIndex()})), properties=('mandatory',), multi=True)
    val4 = StrOption('val4', "", Calculation(calc_value, Params(ParamOption(val1), {'index': ParamIndex()})), properties=('mandatory',), multi=True)
    interface1 = Leadership('val1', '', [val1, val3, val4])
    od1 = OptionDescription('rootconfig', '', [val, val_, interface1])
    cfg_ori = Config(od1)
    cfg_ori.property.read_only()
    cfg = get_config(cfg_ori, config_type)
    assert cfg.option('val1.val3', 0).value.get() == 'val'
    assert cfg.option('val1.val3', 1).value.get() == 'val_'
    assert cfg.option('val1.val4', 0).value.get() == 'val'
    assert cfg.option('val1.val4', 1).value.get() == 'val_'
    assert cfg.option('val1.val1').value.get() == ['val', 'val_']
    cfg_ori.property.read_write()
    cfg = get_config(cfg_ori, config_type)
    cfg.option('val1.val1').value.set(['val', 'val_', 'val3'])
    cfg_ori.property.read_only()
    cfg = get_config(cfg_ori, config_type)
    assert cfg.option('val1.val3', 0).value.get() == 'val'
    assert cfg.option('val1.val3', 1).value.get() == 'val_'
    assert cfg.option('val1.val3', 2).value.get() == 'val3'
    assert cfg.option('val1.val4', 0).value.get() == 'val'
    assert cfg.option('val1.val4', 1).value.get() == 'val_'
    assert cfg.option('val1.val4', 2).value.get() == 'val3'
    assert cfg.option('val1.val1').value.get() == ['val', 'val_', 'val3']
#    assert not list_sessions()


def test_callback_leader_and_followers_leader_mandatory4(config_type):
    val = StrOption('val', "", default='val')
    val1 = StrOption('val1', "", Calculation(return_value2, Params(ParamOption(val))), properties=('mandatory',), multi=True)
    val3 = StrOption('val3', "", Calculation(calc_value, Params(ParamOption(val1), {'index': ParamIndex()})), properties=('mandatory',), multi=True)
    val4 = StrOption('val4', "", Calculation(calc_value, Params(ParamOption(val1), {'index': ParamIndex()})), properties=('mandatory',), multi=True)
    interface1 = Leadership('val1', '', [val1, val3, val4])
    od1 = OptionDescription('rootconfig', '', [val, interface1])
    cfg_ori = Config(od1)
    cfg_ori.property.read_only()
    cfg = get_config(cfg_ori, config_type)
    #raises(IndexError, "cfg.option('val1.val3').value.get()")
    assert cfg.option('val1.val3', 0).value.get() == 'val'
    assert cfg.option('val1.val4', 0).value.get() == 'val'
    assert cfg.option('val1.val1').value.get() == ['val']
    cfg_ori.property.read_write()
    cfg = get_config(cfg_ori, config_type)
    cfg.option('val1.val1').value.set(['val', 'val3'])
    cfg_ori.property.read_only()
    cfg = get_config(cfg_ori, config_type)
    assert cfg.option('val1.val1').value.get() == ['val', 'val3']
    assert cfg.option('val1.val3', 0).value.get() == 'val'
    assert cfg.option('val1.val3', 1).value.get() == 'val3'
    assert cfg.option('val1.val4', 0).value.get() == 'val'
    assert cfg.option('val1.val4', 1).value.get() == 'val3'
#    assert not list_sessions()


def test_callback_leader_and_followers_leader4():
    val1 = StrOption('val1', "", ['val1'], multi=True, properties=('mandatory',))
    val2 = StrOption('val2', "", multi=True, default_multi='val2', properties=('expert', 'mandatory'))
    val3 = StrOption('val3', "", Calculation(calc_value, Params(ParamOption(val2), {'index': ParamIndex()})), multi=True)
    val4 = StrOption('val4', "", Calculation(calc_value, Params(ParamOption(val3), {'index': ParamIndex()})), multi=True)
    interface1 = Leadership('val1', '', [val1, val2, val3, val4])
    od1 = OptionDescription('rootconfig', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    # FIXME cfg = get_config(cfg, config_type)
    cfg.property.add('expert')
    cfg.permissive.add('expert')
    assert list(cfg.value.mandatory()) == []
#    assert not list_sessions()


def test_consistency_leader_and_followers_leader_mandatory_transitive():
    #default value
    val1 = IPOption('val1', "", ['192.168.0.1'], multi=True, properties=('mandatory',))
    val2 = NetmaskOption('val2', "", multi=True, default_multi='255.255.255.0', properties=('disabled', 'mandatory'), validators=[Calculation(valid_ip_netmask, Params((ParamOption(val1), ParamSelfOption())))])
    interface1 = Leadership('val1', '', [val1, val2])
    od1 = OptionDescription('rootconfig', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    # FIXME cfg = get_config(cfg, config_type)
    try:
        cfg.option('val1.val2', 0).value.get()
    except PropertiesOptionError as error:
        assert str(error) == str(_('cannot access to {0} {1} because has {2} {3}').format('option', '"val2"', _('property'), '"disabled"'))
    else:
        raise Exception('must raises')
    assert list(cfg.value.mandatory()) == []
#    assert not list_sessions()


def test_callback_leader_and_followers_leader_list(config_type):
    val1 = StrOption('val1', "", Calculation(return_list), multi=True, properties=('notunique',))
    val2 = StrOption('val2', "", multi=True)
    interface1 = Leadership('val1', '', [val1, val2])
    od1 = OptionDescription('rootconfig', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert cfg.option('val1.val1').value.get() == ['val', 'val']
    assert cfg.option('val1.val2', 0).value.get() == None
    assert cfg.option('val1.val2', 1).value.get() == None
    default_multi = cfg.option('val1.val1').value.defaultmulti()
    cfg.option('val1.val1').value.set(['val', 'val', default_multi])
    assert cfg.option('val1.val1').value.get() == ['val', 'val', None]
    assert cfg.option('val1.val2', 0).value.get() == None
    assert cfg.option('val1.val2', 1).value.get() == None
    assert cfg.option('val1.val2', 2).value.get() == None
    cfg.option('val1.val1').value.reset()
    assert cfg.option('val1.val1').value.get() == ['val', 'val']
    assert cfg.option('val1.val2', 0).value.get() == None
    assert cfg.option('val1.val2', 1).value.get() == None
    cfg.option('val1.val1').value.pop(1)
    assert cfg.option('val1.val1').value.get() == ['val']
    assert cfg.option('val1.val2', 0).value.get() == None
#    assert not list_sessions()


def test_callback_leader_and_followers_leader_follower_list(config_type):
    val1 = StrOption('val1', "", multi=True)
    val2 = StrOption('val2', "", Calculation(return_list), multi=True)
    interface1 = Leadership('val1', '', [val1, val2])
    od1 = OptionDescription('rootconfig', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert cfg.option('val1.val1').value.get() == []
    if config_type == 'tiramisu-api':
        # when "tiramisu-api", raise when set and not in get function
        with pytest.raises(ConfigError):
            cfg.option('val1.val1').value.set(['val1'])
    else:
        cfg.option('val1.val1').value.set(['val1'])
        with pytest.raises(LeadershipError):
            cfg.option('val1.val2', 0).value.get()
#    assert not list_sessions()


def test_callback_leader_and_followers_follower(config_type):
    val1 = StrOption('val1', "", multi=True)
    val2 = StrOption('val2', "", Calculation(return_val), multi=True)
    interface1 = Leadership('val1', '', [val1, val2])
    od1 = OptionDescription('rootconfig', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert cfg.option('val1.val1').value.get() == []
    #
    cfg.option('val1.val1').value.set(['val1'])
    assert cfg.option('val1.val1').value.get() == ['val1']
    assert cfg.option('val1.val2', 0).value.get() == 'val'
    #
    cfg.option('val1.val1').value.set(['val1', 'val2'])
    assert cfg.option('val1.val1').value.get() == ['val1', 'val2']
    assert cfg.option('val1.val2', 0).value.get() == 'val'
    assert cfg.option('val1.val2', 1).value.get() == 'val'
    #
    cfg.option('val1.val1').value.set(['val1', 'val2', 'val3'])
    assert cfg.option('val1.val1').value.get() == ['val1', 'val2', 'val3']
    assert cfg.option('val1.val2', 0).value.get() == 'val'
    assert cfg.option('val1.val2', 1).value.get() == 'val'
    assert cfg.option('val1.val2', 2).value.get() == 'val'
    #
    cfg.option('val1.val1').value.pop(2)
    assert cfg.option('val1.val1').value.get() == ['val1', 'val2']
    assert cfg.option('val1.val2', 0).value.get() == 'val'
    assert cfg.option('val1.val2', 1).value.get() == 'val'
    #
    cfg.option('val1.val2', 0).value.set('val2')
    cfg.option('val1.val2', 1).value.set('val2')
    assert cfg.option('val1.val2', 0).value.get() == 'val2'
    assert cfg.option('val1.val2', 1).value.get() == 'val2'
    #
    cfg.option('val1.val1').value.set(['val1', 'val2', 'val3'])
    assert cfg.option('val1.val2', 0).value.get() == 'val2'
    assert cfg.option('val1.val2', 1).value.get() == 'val2'
    assert cfg.option('val1.val2', 2).value.get() == 'val'
#    assert not list_sessions()


def test_callback_leader_and_followers():
    val1 = StrOption('val1', "", multi=True)
    val2 = StrOption('val2', "", Calculation(return_val), multi=True)
    interface1 = Leadership('val1', '', [val1, val2])
    od1 = OptionDescription('rootconfig', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
#    assert not list_sessions()


def test_callback_leader_and_followers_follower_cal(config_type):
    val3 = StrOption('val3', "", multi=True)
    val1 = StrOption('val1', "", Calculation(return_value, Params(ParamOption(val3))), multi=True)
    val2 = StrOption('val2', "", Calculation(return_val), multi=True)
    interface1 = Leadership('val1', '', [val1, val2])
    od1 = OptionDescription('rootconfig', '', [interface1, val3])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    #
    assert cfg.option('val3').value.get() == []
    assert cfg.option('val1.val1').value.get() == []
    #
    cfg.option('val1.val1').value.set(['val1'])
    cfg.option('val3').value.set(['val1'])
    assert cfg.option('val1.val1').value.get() == ['val1']
    assert cfg.option('val1.val2', 0).value.get() == 'val'
    #
    cfg.option('val1.val1').value.reset()
    cfg.option('val1.val2', 0).value.set('val')
    #
    cfg.option('val3').value.set(['val1', 'val2'])
    assert cfg.option('val1.val2', 0).value.get() == 'val'
    assert cfg.option('val1.val2', 1).value.get() == 'val'
    assert cfg.option('val1.val1').value.get() == ['val1', 'val2']
    # len of follower is higher than leader's one
    cfg.option('val1.val2', 0).value.set('val1')
    cfg.option('val1.val2', 1).value.set('val2')
    if config_type == 'tiramisu-api':
        # when "tiramisu-api", raise when set and not in get function
        with pytest.raises(ConfigError):
            cfg.option('val3').value.set(['val1'])
    else:
        cfg.option('val3').value.set(['val1'])
        assert cfg.option('val1.val1').value.get() == ['val1']
        with pytest.raises(LeadershipError):
            cfg.option('val1.val2', 0).value.get()
    #
    cfg.option('val3').value.set(['val1', 'val2', 'val3'])
    assert cfg.option('val1.val2', 0).value.get() == 'val1'
    assert cfg.option('val1.val2', 1).value.get() == 'val2'
    assert cfg.option('val1.val2', 2).value.get() == 'val'
#    assert not list_sessions()


def test_callback_leader_and_followers_leader_disabled():
    #properties must be transitive
    val1 = StrOption('val1', "", ['val1'], multi=True)
    val2 = StrOption('val2', "", multi=True)
    interface1 = Leadership('val1', '', [val1, val2], properties=('disabled',))
    od1 = OptionDescription('rootconfig', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    with pytest.raises(PropertiesOptionError):
        cfg.option('val1.val1').value.get()
    with pytest.raises(PropertiesOptionError):
        cfg.option('val1.val1').value.set(['yes'])
    with pytest.raises(PropertiesOptionError):
        cfg.option('val1.val2', 0).value.get()
#    assert not list_sessions()


def test_callback_leader_and_followers_leader_callback_disabled():
    val0 = StrOption('val0', "", multi=True, properties=('disabled',))
    val1 = StrOption('val1', "", Calculation(return_value, Params(ParamOption(val0))), multi=True)
    val2 = StrOption('val2', "", multi=True)
    interface1 = Leadership('val1', '', [val1, val2])
    od1 = OptionDescription('rootconfig', '', [interface1, val0])
    cfg = Config(od1)
    cfg.property.read_write()
    with pytest.raises(ConfigError):
        cfg.option('val1.val1').value.get()
    with pytest.raises(ConfigError):
        cfg.option('val1.val2', 0).value.get()
    cfg.property.remove('disabled')
    cfg.option('val1.val1').value.set([])
    cfg.property.add('disabled')
    assert cfg.option('val1.val1').value.get() == []
#    assert not list_sessions()


def test_callback_leader_and_followers_follower_disabled():
    val1 = StrOption('val1', "", multi=True)
    val2 = StrOption('val2', "", multi=True, properties=('disabled',))
    interface1 = Leadership('val1', '', [val1, val2])
    od1 = OptionDescription('rootconfig', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    assert cfg.option('val1.val1').value.get() == []
    cfg.option('val1.val1').value.set(['yes'])
    assert cfg.option('val1.val1').value.get() == ['yes']
    cfg.property.remove('disabled')
    assert cfg.option('val1.val2', 0).value.get() == None
    cfg.option('val1.val2', 0).value.set('no')
    cfg.option('val1.val1').value.set(['yes', 'yes2', 'yes3'])
    cfg.option('val1.val2', 2).value.set('no1')
    assert cfg.option('val1.val2', 0).value.get() == 'no'
    assert cfg.option('val1.val2', 1).value.get() == None
    assert cfg.option('val1.val2', 2).value.get() == 'no1'
    cfg.property.add('disabled')
    cfg.option('val1.val1').value.pop(0)
    assert cfg.option('val1.val1').value.get() == ['yes2', 'yes3']
    cfg.property.remove('disabled')
    assert cfg.option('val1.val2', 0).value.get() == None
    assert cfg.option('val1.val2', 1).value.get() == 'no1'
#    assert not list_sessions()


def test_callback_leader_and_followers_follower_callback_disabled():
    val0 = StrOption('val0', "", multi=True, properties=('disabled',))
    val1 = StrOption('val1', "", multi=True)
    val2 = StrOption('val2', "", Calculation(return_value, Params(ParamOption(val0))), multi=True)
    interface1 = Leadership('val1', '', [val1, val2])
    od1 = OptionDescription('rootconfig', '', [interface1, val0])
    cfg = Config(od1)
    cfg.property.read_write()
    assert cfg.option('val1.val1').value.get() == []
    cfg.option('val1.val1').value.set(['yes'])
    assert cfg.option('val1.val1').value.get() == ['yes']
    cfg.property.remove('disabled')
    cfg.option('val1.val2', 0).value.set('no')
    cfg.option('val1.val1').value.set(['yes', 'yes1'])
    assert cfg.option('val1.val2', 0).value.get() == 'no'
    cfg.property.add('disabled')
    cfg.option('val1.val1').value.pop(1)
#    assert not list_sessions()


def test_callback_leader_and_followers_value():
    val4 = StrOption('val4', '', multi=True, default=['val10', 'val11'])
    val1 = StrOption('val1', "", multi=True)
    val2 = StrOption('val2', "", Calculation(return_value, Params(ParamOption(val1))), multi=True)
    val3 = StrOption('val3', "", Calculation(return_value, Params(ParamValue('yes'))), multi=True)
    val5 = StrOption('val5', "", Calculation(return_value, Params(ParamOption(val4))), multi=True)
    val6 = StrOption('val6', "", Calculation(return_value, Params(ParamOption(val5))), multi=True)
    interface1 = Leadership('val1', '', [val1, val2, val3, val5, val6])
    od1 = OptionDescription('rootconfig', '', [interface1, val4])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.option('val4').value.get() == ['val10', 'val11']
    assert cfg.option('val1.val1').value.get() == []
    #with pytest.raises(LeadershipError):
    #    cfg.val1.val1")
    #with pytest.raises(LeadershipError):
    #    cfg.val1.val2")
    #with pytest.raises(LeadershipError):
    #    cfg.val1.val3")
    #with pytest.raises(LeadershipError):
    #    cfg.val1.val5")
    #with pytest.raises(LeadershipError):
    #    cfg.val1.val6")
    #
    #default calculation has greater length
    #with pytest.raises(LeadershipError):
    #    cfg.option('val1.val1').value.set(['val1']")
    #
    cfg.option('val1.val1').value.set(['val1', 'val2'])
    assert cfg.option('val1.val1').value.get() == ['val1', 'val2']
    assert cfg.option('val1.val2', 0).value.get() == 'val1'
    assert cfg.option('val1.val2', 1).value.get() == 'val2'
    assert cfg.option('val1.val3', 0).value.get() == 'yes'
    assert cfg.option('val1.val3', 1).value.get() == 'yes'
    with pytest.raises(LeadershipError):
        cfg.option('val1.val5', 0).value.get()
    with pytest.raises(LeadershipError):
        cfg.option('val1.val5', 1).value.get()
    with pytest.raises(LeadershipError):
        cfg.option('val1.val6', 0).value.get()
    with pytest.raises(LeadershipError):
        cfg.option('val1.val6', 1).value.get()
    #
    cfg.option('val1.val1').value.set(['val1', 'val2', 'val3'])
    assert cfg.option('val1.val1').value.get() == ['val1', 'val2', 'val3']
    assert cfg.option('val1.val2', 0).value.get() == 'val1'
    assert cfg.option('val1.val2', 1).value.get() == 'val2'
    assert cfg.option('val1.val2', 2).value.get() == 'val3'
    assert cfg.option('val1.val3', 0).value.get() == 'yes'
    assert cfg.option('val1.val3', 1).value.get() == 'yes'
    assert cfg.option('val1.val3', 2).value.get() == 'yes'
    with pytest.raises(LeadershipError):
        cfg.option('val1.val5', 2).value.get()
    with pytest.raises(LeadershipError):
        cfg.option('val1.val6', 2).value.get()
    #
    cfg.option('val1.val1').value.pop(2)
    assert cfg.option('val1.val1').value.get() == ['val1', 'val2']
    assert cfg.option('val1.val2', 0).value.get() == 'val1'
    assert cfg.option('val1.val2', 1).value.get() == 'val2'
    assert cfg.option('val1.val3', 0).value.get() == 'yes'
    assert cfg.option('val1.val3', 1).value.get() == 'yes'
    #
    cfg.option('val1.val2', 0).value.set('val2')
    cfg.option('val1.val2', 1).value.set('val2')
    cfg.option('val1.val3', 0).value.set('val2')
    cfg.option('val1.val3', 1).value.set('val2')
    cfg.option('val1.val5', 0).value.set('val2')
    cfg.option('val1.val5', 1).value.set('val2')
    assert cfg.option('val1.val2', 0).value.get() == 'val2'
    assert cfg.option('val1.val2', 1).value.get() == 'val2'
    assert cfg.option('val1.val3', 0).value.get() == 'val2'
    assert cfg.option('val1.val3', 1).value.get() == 'val2'
    assert cfg.option('val1.val5', 0).value.get() == 'val2'
    assert cfg.option('val1.val5', 1).value.get() == 'val2'
    assert cfg.option('val1.val6', 0).value.get() == 'val2'
    assert cfg.option('val1.val6', 1).value.get() == 'val2'
    #
    cfg.option('val1.val1').value.set(['val1', 'val2', 'val3'])
    assert cfg.option('val1.val2', 2).value.get() == 'val3'
    assert cfg.option('val1.val3', 2).value.get() == 'yes'
#    assert not list_sessions()


def test_callback_different_type(config_type):
    val = IntOption('val', "", default=2)
    val_ = IntOption('val_', "", default=3)
    val1 = IntOption('val1', "", multi=True)
    val2 = IntOption('val2', "", Calculation(return_calc, Params((ParamOption(val), ParamOption(val1)), {'k': ParamOption(val_)})), multi=True)
    interface1 = Leadership('val1', '', [val1, val2])
    od1 = OptionDescription('rootconfig', '', [interface1, val, val_])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert cfg.option('val1.val1').value.get() == []
    cfg.option('val1.val1').value.set([1])
    assert cfg.option('val1.val1').value.get() == [1]
    assert cfg.option('val1.val2', 0).value.get() == 6
    cfg.option('val1.val1').value.set([1, 3])
    assert cfg.option('val1.val1').value.get() == [1, 3]
    assert cfg.option('val1.val2', 0).value.get() == 6
    assert cfg.option('val1.val2', 1).value.get() == 8
    cfg.option('val1.val1').value.set([1, 3, 5])
    assert cfg.option('val1.val1').value.get() == [1, 3, 5]
    assert cfg.option('val1.val2', 0).value.get() == 6
    assert cfg.option('val1.val2', 1).value.get() == 8
    assert cfg.option('val1.val2', 2).value.get() == 10
#    assert not list_sessions()


def test_callback_hidden():
    opt1 = BoolOption('opt1', '')
    opt2 = BoolOption('opt2', '', Calculation(return_value, Params(ParamOption(opt1))))
    od1 = OptionDescription('od1', '', [opt1], properties=('hidden',))
    od2 = OptionDescription('od2', '', [opt2])
    od1 = OptionDescription('rootconfig', '', [od1, od2])
    cfg = Config(od1)
    cfg.property.read_write()
    with pytest.raises(PropertiesOptionError):
        cfg.option('od1.opt1').value.get()
    # do not raise, forcepermissive
    cfg.option('od2.opt2').value.get()
#    assert not list_sessions()


def test_callback_hidden_permissive():
    opt1 = BoolOption('opt1', '')
    opt2 = BoolOption('opt2', '', Calculation(return_value, Params(ParamOption(opt1))))
    od1 = OptionDescription('od1', '', [opt1], properties=('hidden',))
    od2 = OptionDescription('od2', '', [opt2])
    od3 = OptionDescription('rootconfig', '', [od1, od2])
    cfg = Config(od3)
    cfg.permissive.add('hidden')
    cfg.property.read_write()
    with pytest.raises(PropertiesOptionError):
        cfg.option('od1.opt1').value.get()
    cfg.option('od2.opt2').value.get()
#    assert not list_sessions()


def test_callback_hidden_permissive_callback():
    opt1 = BoolOption('opt1', '')
    opt2 = BoolOption('opt2', '', Calculation(return_value, Params(ParamOption(opt1, True))))
    od1 = OptionDescription('od1', '', [opt1], properties=('hidden',))
    od2 = OptionDescription('od2', '', [opt2])
    od3 = OptionDescription('rootconfig', '', [od1, od2])
    cfg = Config(od3)
    cfg.property.read_write()
    with pytest.raises(PropertiesOptionError):
        cfg.option('od1.opt1').value.get()
    cfg.option('od2.opt2').value.get()
#    assert not list_sessions()


def test_callback_two_disabled():
    opt1 = BoolOption('opt1', '', properties=('disabled',))
    opt2 = BoolOption('opt2', '', Calculation(return_value, Params(ParamOption(opt1))), properties=('disabled',))
    od1 = OptionDescription('od1', '', [opt1])
    od2 = OptionDescription('od2', '', [opt2])
    od3 = OptionDescription('rootconfig', '', [od1, od2])
    cfg = Config(od3)
    cfg.property.read_write()
    with pytest.raises(PropertiesOptionError):
        cfg.option('od2.opt2').value.get()
#    assert not list_sessions()


def test_callback_two_disabled2():
    opt1 = BoolOption('opt1', '', properties=('hidden',))
    opt2 = BoolOption('opt2', '', Calculation(return_value, Params(ParamOption(opt1))), properties=('hidden',))
    od1 = OptionDescription('od1', '', [opt1])
    od2 = OptionDescription('od2', '', [opt2])
    od3 = OptionDescription('rootconfig', '', [od1, od2])
    cfg = Config(od3)
    cfg.property.read_write()
    cfg.permissive.add('hidden')
    with pytest.raises(PropertiesOptionError):
        cfg.option('od2.opt2').value.get()
    assert cfg.forcepermissive.option('od2.opt2').owner.isdefault()
#    assert not list_sessions()


def test_callback_calculating_invalid():
    opt1 = IntOption('opt1', '', 1)
    opt2 = BoolOption('opt2', '', Calculation(return_value, Params(ParamOption(opt1))))
    od1 = OptionDescription('od1', '', [opt1])
    od2 = OptionDescription('od2', '', [opt2])
    od3 = OptionDescription('rootconfig', '', [od1, od2])
    cfg = Config(od3)
    cfg.property.read_write()
    with pytest.raises(ValueError):
        cfg.option('od2.opt2').value.get()
    assert cfg.option('od2.opt2').value.valid() is False
    cfg.unrestraint.option('od2.opt2').property.add('disabled')
    with pytest.raises(PropertiesOptionError):
        cfg.option('od2.opt2').value.get()
#    assert not list_sessions()


def test_callback_unvalid_value(config_type):
    val1 = StrOption('val1', "", multi=True)
    val2 = BoolOption('val2', '', Calculation(return_value, Params(ParamOption(val1))), multi=True)
    interface1 = Leadership('val1', '', [val1, val2])
    od1 = OptionDescription('rootconfig', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    cfg.option('val1.val1').value.set(['val'])
    with pytest.raises(ValueError):
        cfg.option('val1.val2', 0).value.get()
    assert cfg.option('val1.val2', 0).value.valid() is False


def test_callback_unrestraint():
    opt1 = IntOption('opt1', '', 1)
    opt2 = IntOption('opt2', '', Calculation(return_value, Params(ParamOption(opt1))))
    od1 = OptionDescription('od1', '', [opt1], properties=('disabled',))
    od2 = OptionDescription('od2', '', [opt2])
    od3 = OptionDescription('rootconfig', '', [od1, od2])
    cfg = Config(od3)
    cfg.property.read_write()
    with pytest.raises(ConfigError):
        cfg.option('od2.opt2').value.get()
    assert cfg.unrestraint.option('od2.opt2').value.get() == 1
#    assert not list_sessions()


def test_callback_calculating_disabled():
    opt1 = BoolOption('opt1', '', properties=('disabled',))
    opt2 = BoolOption('opt2', '', Calculation(return_value, Params(ParamOption(opt1))))
    od1 = OptionDescription('od1', '', [opt1])
    od2 = OptionDescription('od2', '', [opt2])
    od3 = OptionDescription('rootconfig', '', [od1, od2])
    cfg = Config(od3)
    cfg.property.read_write()
    with pytest.raises(ConfigError):
        cfg.option('od2.opt2').value.get()
#    assert not list_sessions()


def test_callback_calculating_mandatory():
    opt1 = BoolOption('opt1', '', properties=('disabled',))
    opt2 = BoolOption('opt2', '', Calculation(return_value, Params(ParamOption(opt1))), properties=('mandatory',))
    od1 = OptionDescription('od1', '', [opt1])
    od2 = OptionDescription('od2', '', [opt2])
    od3 = OptionDescription('rootconfig', '', [od1, od2])
    cfg = Config(od3)
    cfg.property.read_only()
    with pytest.raises(ConfigError):
        cfg.option('od2.opt2').value.get()
#    assert not list_sessions()


def test_callback_calculating_mandatory_multi():
    opt1 = BoolOption('opt1', '', multi=True, properties=('disabled',))
    opt2 = BoolOption('opt2', '', Calculation(return_value, Params(ParamOption(opt1))), properties=('mandatory',), multi=True)
    od1 = OptionDescription('od1', '', [opt1])
    od2 = OptionDescription('od2', '', [opt2])
    od3 = OptionDescription('rootconfig', '', [od1, od2])
    cfg = Config(od3)
    cfg.property.read_only()
    with pytest.raises(ConfigError):
        cfg.option('od2.opt2').value.get()
#    assert not list_sessions()


def test_callback_two_disabled_multi():
    opt1 = BoolOption('opt1', '', properties=('disabled',))
    opt2 = BoolOption('opt2', '', Calculation(return_value, Params(ParamOption(opt1))), properties=('disabled',), multi=True)
    od1 = OptionDescription('od1', '', [opt1])
    od2 = OptionDescription('od2', '', [opt2])
    od3 = OptionDescription('rootconfig', '', [od1, od2])
    cfg = Config(od3)
    cfg.property.read_write()
    with pytest.raises(PropertiesOptionError):
        cfg.option('od2.opt2').value.get()
#    assert not list_sessions()


def test_callback_multi_list_params(config_type):
    val1 = StrOption('val1', "", multi=True, default=['val1', 'val2'])
    val2 = StrOption('val2', "", Calculation(return_list, Params(ParamOption(val1))), multi=True, properties=('notunique',))
    oval2 = OptionDescription('val2', '', [val2])
    od1 = OptionDescription('rootconfig', '', [val1, oval2])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert cfg.option('val2.val2').value.get() == ['val', 'val']
#    assert not list_sessions()


def test_callback_multi_list_params_key(config_type):
    val1 = StrOption('val1', "", multi=True, default=['val1', 'val2'])
    val2 = StrOption('val2', "", Calculation(return_list, Params(kwargs={'value': ParamOption(val1)})), multi=True, properties=('notunique',))
    oval2 = OptionDescription('val2', '', [val2])
    od1 = OptionDescription('rootconfig', '', [val1, oval2])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert cfg.option('val2.val2').value.get() == ['val', 'val']
#    assert not list_sessions()


def test_leadership_callback_description(config_type):
    st1 = StrOption('st1', "", multi=True)
    st2 = StrOption('st2', "", Calculation(return_value, Params(ParamOption(st1))), multi=True)
    stm = Leadership('st1', '', [st1, st2])
    st = OptionDescription('st', '', [stm])
    od = OptionDescription('od', '', [st])
    od2 = OptionDescription('od', '', [od])
    cfg = Config(od2)
    cfg = get_config(cfg, config_type)
    owner = cfg.owner.get()
    assert cfg.option('od.st.st1.st1').value.get() == []
    assert cfg.option('od.st.st1.st1').owner.isdefault()
    ##
    cfg.option('od.st.st1.st1').value.set(['yes'])
    cfg.option('od.st.st1.st2', 0).value.set('yes')
    assert cfg.option('od.st.st1.st1').owner.get() == owner
    assert cfg.option('od.st.st1.st2', 0).owner.get() == owner
#    assert not list_sessions()


def test_leadership_callback_outside(config_type):
    st1 = StrOption('st1', "", multi=True)
    st2 = StrOption('st2', "", multi=True, default_multi='val2')
    stm = Leadership('st1', '', [st1, st2])
    st3 = StrOption('st3', "", Calculation(return_value, Params(ParamOption(st2))), multi=True)
    st = OptionDescription('st', '', [stm, st3])
    od = OptionDescription('od', '', [st])
    od2 = OptionDescription('od', '', [od])
    cfg = Config(od2)
    cfg = get_config(cfg, config_type)
    owner = cfg.owner.get()
    cfg.option('od.st.st1.st1').value.set(['yes'])
    assert parse_od_get(cfg.value.get()) == {'od.st.st1.st1': [{'od.st.st1.st1': 'yes', 'od.st.st1.st2': 'val2'}], 'od.st.st3': ['val2']}
##    assert not list_sessions()


def test_callback_raise():
    opt1 = BoolOption('opt1', 'Option 1', Calculation(return_raise))
    opt2 = BoolOption('opt2', 'Option 2', Calculation(return_valueerror))
    od1 = OptionDescription('od1', '', [opt1])
    od2 = OptionDescription('od2', '', [opt2])
    od3 = OptionDescription('rootconfig', '', [od1, od2])
    cfg = Config(od3)
    cfg.property.read_write()
    try:
        cfg.option('od1.opt1').value.get()
    except ConfigError as err:
        assert '"Option 1"' in str(err)
    try:
        cfg.option('od2.opt2').value.get()
    except ConfigError as err:
        assert '"Option 2"' in str(err)
#    assert not list_sessions()


def test_calc_value_simple(config_type):
    val1 = StrOption('val1', '', 'val1')
    val2 = StrOption('val2', '', Calculation(calc_value, Params(ParamOption(val1))))
    od1 = OptionDescription('root', '', [val1, val2])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert parse_od_get(cfg.value.get()) == {'val1': 'val1', 'val2': 'val1'}
#    assert not list_sessions()


def test_calc_value_multi(config_type):
    val1 = StrOption('val1', "", 'val1')
    val2 = StrOption('val2', "", 'val2')
    val3 = StrOption('val3', "", Calculation(calc_value, Params((ParamOption(val1), ParamOption(val2)), multi=ParamValue(True))), multi=True)
    od1 = OptionDescription('root', '', [val1, val2, val3])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert parse_od_get(cfg.value.get()) == {'val1': 'val1', 'val2': 'val2', 'val3': ['val1', 'val2']}
#    assert not list_sessions()


def test_calc_value_disabled():
    val1 = StrOption('val1', '', 'val1')
    val2 = StrOption('val2', '', Calculation(calc_value, Params(ParamOption(val1, True), default=ParamValue('default_value'))))
    od1 = OptionDescription('root', '', [val1, val2])
    cfg = Config(od1)
    cfg.property.read_write()
    assert parse_od_get(cfg.value.get()) == {'val1': 'val1', 'val2': 'val1'}
    cfg.option('val1').property.add('disabled')
    assert parse_od_get(cfg.value.get()) == {'val2': 'default_value'}
#    assert not list_sessions()


def test_calc_value_condition(config_type):
    boolean = BoolOption('boolean', '', True)
    val1 = StrOption('val1', '', 'val1')
    val2 = StrOption('val2', '', Calculation(calc_value, Params(ParamOption(val1, True),
                                                         default=ParamValue('default_value'),
                                                         condition=ParamOption(boolean),
                                                         expected=ParamValue(True))))
    od1 = OptionDescription('root', '', [boolean, val1, val2])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert parse_od_get(cfg.value.get()) == {'boolean': True, 'val1': 'val1', 'val2': 'val1'}
    cfg.option('boolean').value.set(False)
    assert parse_od_get(cfg.value.get()) == {'boolean': False, 'val1': 'val1', 'val2': 'default_value'}
#    assert not list_sessions()


def test_calc_value_allow_none(config_type):
    val1 = StrOption('val1', "", 'val1')
    val2 = StrOption('val2', "")
    val3 = StrOption('val3', "", Calculation(calc_value, Params((ParamOption(val1), ParamOption(val2)), multi=ParamValue(True), allow_none=ParamValue(True))), multi=True)
    od1 = OptionDescription('root', '', [val1, val2, val3])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert parse_od_get(cfg.value.get()) == {'val1': 'val1', 'val2': None, 'val3': ['val1', None]}
#    assert not list_sessions()


def test_calc_value_remove_duplicate(config_type):
    val1 = StrOption('val1', "", 'val1')
    val2 = StrOption('val2', "", 'val1')
    val3 = StrOption('val3', "", Calculation(calc_value, Params((ParamOption(val1), ParamOption(val2)), multi=ParamValue(True), remove_duplicate_value=ParamValue(True))), multi=True)
    od1 = OptionDescription('root', '', [val1, val2, val3])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert parse_od_get(cfg.value.get()) == {'val1': 'val1', 'val2': 'val1', 'val3': ['val1']}
#    assert not list_sessions()


def test_calc_value_remove_duplicate2(config_type):
    val1 = StrOption('val1', "", ['val1', 'val1'], multi=True, properties=('notunique',))
    val2 = StrOption('val2', "", ['val1', 'val1'], multi=True, properties=('notunique',))
    val3 = StrOption('val3', "", Calculation(calc_value, Params((ParamOption(val1), ParamOption(val2)), multi=ParamValue(True), remove_duplicate_value=ParamValue(True), join=ParamValue('-'))), multi=True)
    od1 = OptionDescription('root', '', [val1, val2, val3])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert parse_od_get(cfg.value.get()) == {'val1': ['val1', 'val1'], 'val2': ['val1', 'val1'], 'val3': ['val1-val1']}
#    assert not list_sessions()


def test_calc_value_join(config_type):
    val1 = StrOption('val1', "", 'val1')
    val2 = StrOption('val2', "", 'val2')
    val3 = StrOption('val3', "")
    val4 = StrOption('val4', "", Calculation(calc_value, Params((ParamOption(val1), ParamOption(val2), ParamOption(val3)), join=ParamValue('.'))))
    od1 = OptionDescription('root', '', [val1, val2, val3, val4])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert parse_od_get(cfg.value.get()) == {'val1': 'val1', 'val2': 'val2', 'val3': None, 'val4': None}
    cfg.option('val3').value.set('val3')
    assert parse_od_get(cfg.value.get()) == {'val1': 'val1', 'val2': 'val2', 'val3': 'val3', 'val4': 'val1.val2.val3'}
#    assert not list_sessions()


def test_calc_value_join_multi(config_type):
    val1 = StrOption('val1', "", multi=True)
    val4 = StrOption('val4', "", Calculation(calc_value, Params((ParamOption(val1)), join=ParamValue('.'), multi=ParamValue(True))), multi=True)
    od1 = OptionDescription('root', '', [val1, val4])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert parse_od_get(cfg.value.get()) == {'val1': [], 'val4': []}
    cfg.option('val1').value.set(['val1'])
    assert parse_od_get(cfg.value.get()) == {'val1': ['val1'], 'val4': ['val1']}
#    assert not list_sessions()


def test_calc_value_join_multi_value(config_type):
    val1 = StrOption('val1', "", ['val1'], multi=True)
    val2 = StrOption('val2', "", ['val2'], multi=True)
    val3 = StrOption('val3', "", [None], multi=True)
    val4 = StrOption('val4', "", Calculation(calc_value, Params((ParamOption(val1), ParamOption(val2), ParamOption(val3)), join=ParamValue('.'), multi=ParamValue(True))), multi=True)
    od1 = OptionDescription('root', '', [val1, val2, val3, val4])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert parse_od_get(cfg.value.get()) == {'val1': ['val1'], 'val2': ['val2'], 'val3': [None], 'val4': []}
    cfg.option('val3').value.set(['val3'])
    assert parse_od_get(cfg.value.get()) == {'val1': ['val1'], 'val2': ['val2'], 'val3': ['val3'], 'val4': ['val1.val2.val3']}
#    assert not list_sessions()


def test_calc_value_min():
    val1 = StrOption('val1', "", 'val1')
    val2 = StrOption('val2', "", 'val2')
    val3 = StrOption('val3', "", 'val3')
    val4 = StrOption('val4', "", Calculation(calc_value, Params((ParamOption(val1), ParamOption(val2), ParamOption(val3, True)), join=ParamValue('.'), min_args_len=ParamValue(3))))
    od1 = OptionDescription('root', '', [val1, val2, val3, val4])
    cfg = Config(od1)
    cfg.property.read_write()
    assert parse_od_get(cfg.value.get()) == {'val1': 'val1', 'val2': 'val2', 'val3': 'val3', 'val4': 'val1.val2.val3'}
    cfg.option('val3').property.add('disabled')
    assert parse_od_get(cfg.value.get()) == {'val1': 'val1', 'val2': 'val2', 'val4': ''}
#    assert not list_sessions()


def test_calc_value_add(config_type):
    val1 = IntOption('val1', "", 1)
    val2 = IntOption('val2', "", 2)
    val3 = IntOption('val3', "", Calculation(calc_value, Params((ParamOption(val1), ParamOption(val2)), operator=ParamValue('add'))))
    od1 = OptionDescription('root', '', [val1, val2, val3])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert parse_od_get(cfg.value.get()) == {'val1': 1, 'val2': 2, 'val3': 3}
#    assert not list_sessions()


def test_calc_dependencies(config_type):
    val1 = IntOption('val1', "", 1)
    val2 = IntOption('val2', "", 2)
    val3 = IntOption('val3', "", Calculation(calc_value, Params((ParamOption(val1), ParamOption(val2)), operator=ParamValue('add'))))
    od1 = OptionDescription('root', '', [val1, val2, val3])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    dep = cfg.option('val1').dependencies()
    assert len(dep) == 1
    assert dep[0].get() == val3
    #
    dep = cfg.option('val2').dependencies()
    assert len(dep) == 1
    assert dep[0].get() == val3
    #
    assert cfg.option('val3').dependencies() == []


def test_callback__kwargs_wrong(config_type):
    with pytest.raises(ValueError):
        Params(kwargs='string')


def test_callback_information_parent(config_type):
    information = ParamInformation('information')
    val1 = StrOption('val1', "", Calculation(return_value, Params(information)))
    od2 = OptionDescription('od', '', [val1], informations={'information': 'new_value'})
    information.set_option(od2)
    od1 = OptionDescription('rootconfig', '', [od2])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert cfg.option('od.val1').value.get() == 'new_value'
    cfg.option('od').information.set('information', 'new_value2')
    assert cfg.option('od.val1').value.get() == 'new_value2'


def test_callback_information_redefined(config_type):
    val1 = StrOption('val1', "")
    information = ParamInformation('information', option=val1)
    val2 = StrOption('val2', "", Calculation(return_value, Params(information)))
    od2 = OptionDescription('od', '', [val1, val2], informations={'information': 'new_value'})
    with pytest.raises(ConfigError):
        information.set_option(od2)


def test_callback_information_redefined_after(config_type):
    information = ParamInformation('information')
    val1 = StrOption('val1', "", Calculation(return_value, Params(information)))
    od2 = OptionDescription('od', '', [val1], informations={'information': 'new_value'})
    od1 = OptionDescription('rootconfig', '', [od2])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    with pytest.raises(ConfigError):
        information.set_option(od2)
