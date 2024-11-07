# coding: utf-8
"frozen and hidden values"
from .autopath import do_autopath
do_autopath()

import pytest

from tiramisu import ChoiceOption, BoolOption, IntOption, FloatOption, \
    PasswordOption, StrOption, DateOption, OptionDescription, Config, \
    Calculation, Params, ParamOption, ParamValue, calc_value
from tiramisu.error import PropertiesOptionError
from .config import config_type, get_config


def make_description():
    gcoption = ChoiceOption('name', 'GC name', ('ref', 'framework'), 'ref')
    gcdummy = BoolOption('dummy', 'dummy', default=False, properties=(('hidden'),))
    objspaceoption = ChoiceOption('objspace', 'Object space',
                                  ('std', 'thunk'), ['std'], multi=True)
    booloption = BoolOption('bool', 'Test boolean option', default=True)
    intoption = IntOption('int', 'Test int option', default=0)
    floatoption = FloatOption('float', 'Test float option', default=2.3)
    stroption = StrOption('str', 'Test string option', default="abc")

    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(gcoption),
                                                 'expected': ParamValue('ref')}))
    wantref_option = BoolOption('wantref', 'Test requires', default=False, properties=(hidden_property,))
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(gcoption),
                                                 'expected': ParamValue('framework')}))
    wantframework_option = BoolOption('wantframework', 'Test requires',
                                      default=False, properties=(hidden_property,))

    # ____________________________________________________________
    booloptiontwo = BoolOption('booltwo', 'Test boolean option two', default=False)
    subgroup = OptionDescription('subgroup', '', [booloptiontwo])
    # ____________________________________________________________

    gcgroup = OptionDescription('gc', '', [subgroup, gcoption, gcdummy, floatoption])
    descr = OptionDescription('trs', '', [gcgroup, booloption, objspaceoption,
                                          wantref_option, stroption,
                                          wantframework_option,
                                          intoption])
    return descr


# ____________________________________________________________
def test_is_hidden(config_type):
    od1 = make_description()
    cfg = Config(od1)
    cfg.property.read_write()
    assert not 'frozen' in cfg.forcepermissive.option('gc.dummy').property.get()
    cfg = get_config(cfg, config_type)
    # setattr
    with pytest.raises(PropertiesOptionError):
        cfg.option('gc.dummy').value.get() == False
    # getattr
    with pytest.raises(PropertiesOptionError):
        cfg.option('gc.dummy').value.get()
#    assert not list_sessions()


def test_group_is_hidden(config_type):
    gcdummy = BoolOption('dummy', 'dummy', default=False, properties=(('hidden'),))
    floatoption = FloatOption('float', 'Test float option', default=2.3)
    gcgroup = OptionDescription('gc', '', [gcdummy, floatoption])
    od1 = OptionDescription('trs', '', [gcgroup])
    cfg_ori = Config(od1)
    cfg_ori.property.read_write()
    cfg_ori.option('gc').property.add('hidden')
    cfg = get_config(cfg_ori, config_type)
    with pytest.raises(PropertiesOptionError):
        cfg.option('gc.dummy').value.get()
    if config_type == 'tiramisu-api':
        cfg.send()
    assert 'hidden' in cfg_ori.option('gc').property.get()
    cfg = get_config(cfg_ori, config_type)
    with pytest.raises(PropertiesOptionError):
        cfg.option('gc.float').value.get()
    # manually set the subconfigs to "show"
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.option('gc').property.remove('hidden')
    cfg = get_config(cfg_ori, config_type)
    assert not 'hidden' in cfg.option('gc').property.get()
    assert cfg.option('gc.float').value.get() == 2.3
    #dummy est en hide
    prop = []
    try:
        cfg.option('gc.dummy').value.set(False)
    except PropertiesOptionError as err:
        prop = err.proptype
    if config_type == 'tiramisu-api':
        assert 'disabled' in prop
    else:
        assert 'hidden' in prop
#    assert not list_sessions()


def test_group_is_hidden_multi(config_type):
    od1 = make_description()
    cfg_ori = Config(od1)
    cfg_ori.property.read_write()
    cfg_ori.option('objspace').property.add('hidden')
    cfg = get_config(cfg_ori, config_type)
    with pytest.raises(PropertiesOptionError):
        cfg.option('objspace').value.get()
    if config_type == 'tiramisu-api':
        cfg.send()
    assert 'hidden' in cfg_ori.forcepermissive.option('objspace').property.get()
    cfg = get_config(cfg_ori, config_type)
    prop = []
    try:
        cfg.option('objspace').value.set(['std'])
    except PropertiesOptionError as err:
        prop = err.proptype
    if config_type == 'tiramisu-api':
        assert 'disabled' in prop
    else:
        assert 'hidden' in prop
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.forcepermissive.option('objspace').property.remove('hidden')
    cfg = get_config(cfg_ori, config_type)
    assert not 'hidden' in cfg.option('objspace').property.get()
    cfg.option('objspace').value.set(['std', 'thunk'])
#    assert not list_sessions()


def test_global_show(config_type):
    od1 = make_description()
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.forcepermissive.option('gc.dummy').property.add('hidden')
    assert 'hidden' in cfg.forcepermissive.option('gc.dummy').property.get()
    cfg = get_config(cfg, config_type)
    with pytest.raises(PropertiesOptionError):
        cfg.option('gc.dummy').value.get() == False
#    assert not list_sessions()


def test_with_many_subgroups(config_type):
    od1 = make_description()
    cfg_ori = Config(od1)
    #booltwo = config.unwrap_from_path('gc.subgroup.booltwo')
    #setting = config.cfgimpl_get_settings()
    cfg = get_config(cfg_ori, config_type)
    assert not 'hidden' in cfg.option('gc.subgroup.booltwo').property.get()
    assert cfg.option('gc.subgroup.booltwo').value.get() is False
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.option('gc.subgroup.booltwo').property.add('hidden')
#    assert not list_sessions()


def test_password_option(config_type):
    o = PasswordOption('o', '')
    o1 = PasswordOption('o1', '', min_len=4)
    o2 = PasswordOption('o2', '', max_len=4)
    o3 = PasswordOption('o3', '', forbidden_char=['p'])
    od1 = OptionDescription('d', '', [o, o1, o2, o3])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)

    cfg.option('o').value.set('a_valid_password')
    with pytest.raises(ValueError):
        cfg.option('o').value.set(1)
    #
    assert cfg.option('o1').value.get() is None
    with pytest.raises(ValueError):
        cfg.option('o1').value.set("1")
    with pytest.raises(ValueError):
        cfg.option('o1').value.set("12")
    with pytest.raises(ValueError):
        cfg.option('o1').value.set("123")
    cfg.option('o1').value.set("1234")
    cfg.option('o1').value.set("12345")
    #
    assert cfg.option('o2').value.get() is None
    with pytest.raises(ValueError):
        cfg.option('o2').value.set("12345")
    cfg.option('o2').value.set("1")
    cfg.option('o2').value.set("12")
    cfg.option('o2').value.set("123")
    cfg.option('o2').value.set("1234")
    #
    with pytest.raises(ValueError):
        cfg.option('o3').value.set("password")
    cfg.option('o3').value.set("assword")
#    assert not list_sessions()


def test_date_option(config_type):
    o = DateOption('o', '')
    od1 = OptionDescription('d', '', [o])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)

    cfg.option('o').value.set('2017-02-04')
    cfg.option('o').value.set('2017-2-4')
    with pytest.raises(ValueError):
        cfg.option('o').value.set(1)
    with pytest.raises(ValueError):
        cfg.option('o').value.set('2017-13-20')
    with pytest.raises(ValueError):
        cfg.option('o').value.set('2017-11-31')
    with pytest.raises(ValueError):
        cfg.option('o').value.set('2017-12-32')
    with pytest.raises(ValueError):
        cfg.option('o').value.set('2017-2-29')
    with pytest.raises(ValueError):
        cfg.option('o').value.set('2-2-2017')
    with pytest.raises(ValueError):
        cfg.option('o').value.set('2017/2/2')
#    assert not list_sessions()
