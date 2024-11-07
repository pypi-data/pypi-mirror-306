#this test is much more to test that **it's there** and answers attribute access
from .autopath import do_autopath
do_autopath()

import pytest
from tiramisu import BoolOption, OptionDescription, ChoiceOption,\
    IntOption, FloatOption, StrOption, Config
from .config import config_type, get_config


def make_description():
    gcoption = ChoiceOption('name', 'GC name', ['ref', 'framework'], 'ref')
    gcdummy = BoolOption('dummy', 'dummy', default=False)
    gcdummy2 = BoolOption('hide', 'dummy', default=True)
    objspaceoption = ChoiceOption('objspace', 'Object space',
                                  ['std', 'thunk'], 'std')
    booloption = BoolOption('bool', 'Test boolean option', default=True)
    intoption = IntOption('int', 'Test int option', default=0)
    floatoption = FloatOption('float', 'Test float option', default=2.3)
    stroption = StrOption('str', 'Test string option', default="abc")
    boolop = BoolOption('boolop', 'Test boolean option op', default=True)
    wantref_option = BoolOption('wantref', 'Test requires', default=False)
    wantframework_option = BoolOption('wantframework', 'Test requires',
                                      default=False)

    gcgroup = OptionDescription('gc', '', [gcoption, gcdummy, floatoption, gcdummy2])
    descr = OptionDescription('tiram', '', [gcgroup, booloption, objspaceoption,
                                            wantref_option, stroption,
                                            wantframework_option,
                                            intoption, boolop])
    return descr


def test_root_config_answers_ok(config_type):
    "if you hide the root config, the options in this namespace behave normally"
    gcdummy = BoolOption('dummy', 'dummy', default=False)
    boolop = BoolOption('boolop', 'Test boolean option op', default=True)
    od1 = OptionDescription('tiramisu', '', [gcdummy, boolop])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    #settings = cfg.cfgimpl_get_settings()
    #settings.append('hidden')

    assert cfg.option('dummy').value.get() is False
    assert cfg.option('boolop').value.get() is True
#    assert not list_sessions()


def test_option_has_an_api_name(config_type):
    b = BoolOption('impl_has_dependency', 'dummy', default=True)
    od1 = OptionDescription('tiramisu', '', [b])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert cfg.option('impl_has_dependency').value.get() is True
    assert b.impl_has_dependency() is False
#    assert not list_sessions()
