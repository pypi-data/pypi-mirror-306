"config.set() or config.setoption() or option.setoption()"
from .autopath import do_autopath
do_autopath()

import pytest
from os import environ

from tiramisu.i18n import _
from tiramisu.error import display_list, ConfigError
from tiramisu.setting import owners, groups
from tiramisu import ChoiceOption, BoolOption, IntOption, FloatOption, \
    StrOption, OptionDescription, Leadership, Config, undefined, \
    Calculation, Params, ParamOption, ParamValue, ParamIndex, \
    calc_value, calc_value_property_help, ParamInformation
from tiramisu.error import PropertiesOptionError
import warnings
from .config import config_type, get_config, parse_od_get


def make_description():
    gcoption = ChoiceOption('name', 'GC name', ('ref', 'framework'), 'ref')
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
    gcgroup = OptionDescription('gc', '', [gcoption, gcdummy, floatoption])
    descr = OptionDescription('tiramisu', '', [gcgroup, booloption, objspaceoption,
                                               wantref_option, stroption,
                                               wantframework_option,
                                               intoption, boolop])
    return descr


#____________________________________________________________
# change with __setattr__
def test_attribute_access(config_type):
    "Once set, option values can't be changed again by attribute access"
    s = StrOption("string", "", default="string")
    od1 = OptionDescription("options", "", [s])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    # let's try to change it again
    cfg.option('string').value.set('foo')
    assert cfg.option('string').value.get() == 'foo'
#    assert not list_sessions()


def test_mod_read_only_write():
    "default with multi is a list"
    s = StrOption("string", "", default=[], default_multi="string", multi=True)
    od1 = OptionDescription("options", "", [s])
    config = Config(od1)
    config2 = Config(od1)
    assert config.property.default() == {'cache', 'validator', 'warnings'}
    assert config.property.default('read_only', 'append') == {'frozen',
                                                              'disabled',
                                                              'validator',
                                                              'everything_frozen',
                                                              'mandatory',
                                                              'empty',
                                                              'force_store_value',
                                                              }
    assert config.property.default('read_only', 'remove') == {'permissive',
                                                              'hidden',
                                                              }
    assert config.property.default('read_write', 'append') == {'frozen',
                                                               'disabled',
                                                               'validator',
                                                               'hidden',
                                                               'force_store_value',
                                                               }
    assert config.property.default('read_write', 'remove') == {'permissive',
                                                               'everything_frozen',
                                                               'mandatory',
                                                               'empty',
                                                               }
    #
#    config.property.setdefault(frozenset(['cache']))
    config.property.setdefault(type='read_only', when='append', properties=frozenset(['disabled']))
    config.property.setdefault(type='read_only', when='remove', properties=frozenset(['hidden']))
    config.property.setdefault(type='read_write', when='append', properties=frozenset(['disabled', 'hidden']))
    config.property.setdefault(type='read_write', when='remove', properties=frozenset([]))
    with pytest.raises(ValueError):
        config.property.setdefault(type='unknown', when='append', properties=frozenset(['disabled']))
    with pytest.raises(ValueError):
        config.property.setdefault(type='read_only', when='unknown', properties=frozenset(['disabled']))
    with pytest.raises(TypeError):
        config.property.setdefault(type='read_only', when='append', properties=['disabled'])

    assert config.property.default() == {'warnings', 'validator', 'cache'}
    assert config.property.default('read_only', 'append') == {'disabled'}
    assert config.property.default('read_only', 'remove') == {'hidden'}
    assert config.property.default('read_write', 'append') == {'disabled',
                                                               'hidden'}
    assert config.property.default('read_write', 'remove') == set([])
    #
    config.property.read_only()
    assert config.property.get() == {'warnings', 'validator', 'cache', 'disabled'}
    config.property.read_write()
    assert config.property.get() == {'warnings', 'validator', 'cache', 'disabled', 'hidden'}
    config.property.read_only()
    assert config.property.get() == {'warnings', 'validator', 'cache', 'disabled'}
    #
    assert config2.property.default() == {'cache', 'validator', 'warnings'}
    assert config2.property.default('read_only', 'append') == {'frozen',
                                                               'disabled',
                                                               'validator',
                                                               'everything_frozen',
                                                               'mandatory',
                                                               'empty',
                                                               'force_store_value',
                                                               }
    assert config2.property.default('read_only', 'remove') == {'permissive',
                                                               'hidden',
                                                               }
    assert config2.property.default('read_write', 'append') == {'frozen',
                                                                'disabled',
                                                                'validator',
                                                                'hidden',
                                                                'force_store_value',
                                                                }
    assert config2.property.default('read_write', 'remove') == {'permissive',
                                                                'everything_frozen',
                                                                'mandatory',
                                                                'empty',
                                                                }
    with pytest.raises(ValueError):
        config2.property.default('unknown', 'remove')
    with pytest.raises(ValueError):
        config2.property.default('read_write', 'unknown')
#    assert not list_sessions()


def test_setting_tree(config_type):
    s = StrOption("string", "", default=["string", "sdfsdf"], default_multi="prout", multi=True)
    od4 = OptionDescription("option4", "", [s])
    od3 = OptionDescription("option3", "", [od4])
    od2 = OptionDescription("option2", "", [od3], properties=('hidden',))
    od1 = OptionDescription("root", "", [od2])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    cfg.property.read_write()
    with pytest.raises(PropertiesOptionError):
        cfg.option('option2.option3.option4.string').value.get()


def test_setitem(config_type):
    s = StrOption("string", "", default=["string", "sdfsdf"], default_multi="prout", multi=True)
    od1 = OptionDescription("options", "", [s])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    cfg.option('string').value.set(['string', 'foo'])
    assert cfg.option('string').value.get() == ['string', 'foo']
#    assert not list_sessions()


def test_reset(config_type):
    "if value is None, resets to default owner"
    s = StrOption("string", "", default="string")
    od1 = OptionDescription("options", "", [s])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    cfg.option('string').value.set('foo')
    assert cfg.option('string').value.get() == "foo"
    assert cfg.option('string').owner.get() ==owners.user
    cfg.option('string').value.reset()
    assert cfg.option('string').value.get() == 'string'
    assert cfg.option('string').owner.get() ==owners.default
#    assert not list_sessions()


def test_reset_with_multi(config_type):
    s = StrOption("string", "", default=["string"], default_multi="string", multi=True)
    od1 = OptionDescription("options", "", [s])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    cfg.option('string').value.reset()
    assert cfg.option('string').value.get() == ["string"]
    assert cfg.option('string').owner.get() =='default'
    cfg.option('string').value.set(["eggs", "spam", "foo"])
    assert cfg.option('string').owner.get() =='user'
    cfg.option('string').value.set([])
    cfg.option('string').value.reset()
    assert cfg.option('string').owner.get() =='default'
    with pytest.raises(ValueError):
        cfg.option('string').value.set(None)
#    assert not list_sessions()


def test_property_get_unique_empty():
    s = StrOption("string", "", default=["string"], default_multi="string", multi=True)
    s2 = StrOption("string2", "", default=["string"], default_multi="string", multi=True, properties=('notunique',))
    s3 = StrOption("string3", "", default=["string"], default_multi="string", multi=True, properties=('notempty',))
    s4 = StrOption("string4", "", default=["string"], default_multi="string", multi=True, properties=('notunique', 'notempty'))
    od1 = OptionDescription("options", "", [s, s2, s3, s4])
    cfg = Config(od1)
    cfg.property.read_write()
    assert cfg.option('string').property.get() == {'empty', 'unique'}
    assert cfg.option('string2').property.get() == {'empty', 'notunique'}
    assert cfg.option('string3').property.get() == {'unique', 'notempty'}
    assert cfg.option('string4').property.get() == {'notunique', 'notempty'}
#    assert not list_sessions()


def test_property_only_raises():
    s = StrOption("string", "", default=["string"], default_multi="string", multi=True)
    intoption = IntOption('int', 'Test int option', default=0)
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(intoption),
                                                 'expected': ParamValue(1)}))
    stroption = StrOption('str', 'Test string option', default=["abc"], default_multi="abc", properties=(hidden_property,), multi=True)
    od1 = OptionDescription("options", "", [s, intoption, stroption])
    cfg = Config(od1)
    cfg.property.read_write()
    assert cfg.option('str').property.get() == {'empty', 'unique'}
    assert cfg.option('str').property.get(only_raises=True) == set()
#    assert not list_sessions()


def test_default_with_multi():
    "default with multi is a list"
    s = StrOption("string", "", default=[], default_multi="string", multi=True)
    od1 = OptionDescription("options", "", [s])
    cfg = Config(od1)
    assert cfg.option('string').value.get() == []
    s = StrOption("string", "", default=None, default_multi="string", multi=True)
    descr = OptionDescription("options", "", [s])
    cfg = Config(descr)
    assert cfg.option('string').value.get() == []
#    assert not list_sessions()


def test_idontexist():
    od1 = make_description()
    cfg = Config(od1)
    cfg.value.get()
    with pytest.raises(AttributeError):
        cfg.option('idontexist').value.get()
#    assert not list_sessions()


# ____________________________________________________________
def test_attribute_access_with_multi(config_type):
    s = StrOption("string", "", default=["string"], default_multi="string", multi=True)
    od1 = OptionDescription("options", "", [s])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    cfg.option('string').value.set(["foo", "bar"])
    assert cfg.option('string').value.get() == ["foo", "bar"]
#    assert not list_sessions()


def test_item_access_with_multi(config_type):
    s = StrOption("string", "", default=["string"], multi=True)
    od1 = OptionDescription("options", "", [s])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    cfg.option('string').value.set(["foo", "bar"])
    assert cfg.option('string').value.get() == ["foo", "bar"]
    cfg.option('string').value.set(["changetest", "bar"])
    assert cfg.option('string').value.get() == ["changetest", "bar"]
#    assert not list_sessions()


def test_access_with_multi_default(config_type):
    s = StrOption("string", "", default=["string"], multi=True)
    od1 = OptionDescription("options", "", [s])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert cfg.option('string').owner.get() =='default'
    cfg.option('string').value.set(["foo", "bar"])
    assert cfg.option('string').value.get() == ["foo", "bar"]
    assert cfg.option('string').owner.get() =='user'
#    assert not list_sessions()


def test_multi_with_requires():
    s = StrOption("string", "", default=["string"], default_multi="string", multi=True)
    intoption = IntOption('int', 'Test int option', default=0)
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(intoption),
                                                 'expected': ParamValue(1)}))
    stroption = StrOption('str', 'Test string option', default=["abc"], default_multi="abc", properties=(hidden_property,), multi=True)
    od1 = OptionDescription("options", "", [s, intoption, stroption])
    cfg = Config(od1)
    cfg.property.read_write()
    assert not 'hidden' in cfg.option('str').property.get()
    cfg.option('int').value.set(1)
    with pytest.raises(PropertiesOptionError):
        cfg.option('str').value.set(['a', 'b'])
    assert 'hidden' in cfg.forcepermissive.option('str').property.get()
#    assert not list_sessions()


def test_requires_with_inverted():
    s = StrOption("string", "", default=["string"], multi=True)
    intoption = IntOption('int', 'Test int option', default=0)
    hide_property = Calculation(calc_value,
                                Params(ParamValue('hide'),
                                       kwargs={'condition': ParamOption(intoption),
                                               'expected': ParamValue(1),
                                               'reverse_condition': ParamValue(True)}))
    stroption = StrOption('str', 'Test string option', default=["abc"], default_multi="abc", properties=(hide_property,), multi=True)
    od1 = OptionDescription("options", "", [s, intoption, stroption])
    cfg = Config(od1)
    assert not 'hidden' in cfg.option('str').property.get()
    assert 'hide' in cfg.option('str').property.get()
    cfg.option('int').value.set(1)
    assert not 'hidden' in cfg.option('str').property.get()
    assert not 'hide' in cfg.option('str').property.get()
#    assert not list_sessions()


def test_multi_with_requires_in_another_group():
    s = StrOption("string", "", default=["string"], multi=True)
    intoption = IntOption('int', 'Test int option', default=0)
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(intoption),
                                                 'expected': ParamValue(1)}))
    stroption = StrOption('str', 'Test string option', default=["abc"], properties=(hidden_property,), multi=True)
    descr = OptionDescription("opt", "", [stroption])
    od1 = OptionDescription("opt2", "", [intoption, s, descr])
    cfg = Config(od1)
    cfg.property.read_write()
    assert not 'hidden' in cfg.option('opt.str').property.get()
    cfg.option('int').value.set(1)
    with pytest.raises(PropertiesOptionError):
        cfg.option('opt.str').value.set(['a', 'b'])
    assert 'hidden' in cfg.forcepermissive.option('opt.str').property.get()
#    assert not list_sessions()


def test_multi_with_requires_in_another_group_inverse():
    s = StrOption("string", "", default=["string"], multi=True)
    intoption = IntOption('int', 'Test int option', default=0)
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(intoption),
                                                 'expected': ParamValue(1)}))
#                          requires=[{'option': intoption, 'expected': 1, 'action': 'hidden'}], multi=True)
    stroption = StrOption('str', 'Test string option', default=["abc"], properties=(hidden_property,), multi=True)
    descr = OptionDescription("opt", "", [stroption])
    od1 = OptionDescription("opt2", "", [intoption, s, descr])
    cfg = Config(od1)
    cfg.property.read_write()
    assert not 'hidden' in cfg.option('opt.str').property.get()
    cfg.option('int').value.set(1)
    with pytest.raises(PropertiesOptionError):
        cfg.option('opt.str').value.set(['a', 'b'])
    assert 'hidden' in cfg.forcepermissive.option('opt.str').property.get()
#    assert not list_sessions()


def test_apply_requires_from_config():
    s = StrOption("string", "", default=["string"], multi=True)
    intoption = IntOption('int', 'Test int option', default=0)
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(intoption),
                                                 'expected': ParamValue(1)}))
    stroption = StrOption('str', 'Test string option', default=["abc"], properties=(hidden_property,), multi=True)
    descr = OptionDescription("opt", "", [stroption])
    od1 = OptionDescription("opt2", "", [intoption, s, descr])
    cfg = Config(od1)
    cfg.property.read_write()
    assert not 'hidden' in cfg.option('opt.str').property.get()
    cfg.option('int').value.set(1)
    with pytest.raises(PropertiesOptionError):
        cfg.option('opt.str').value.get()
    assert 'hidden' in cfg.forcepermissive.option('opt.str').property.get()
    assert 'hidden' not in cfg.forcepermissive.option('opt.str').property.get(only_raises=True)
#    assert not list_sessions()


def test_apply_requires_with_disabled():
    s = StrOption("string", "", default=["string"], multi=True)
    intoption = IntOption('int', 'Test int option', default=0)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(intoption),
                                                   'expected': ParamValue(1)}))
    stroption = StrOption('str', 'Test string option', default=["abc"], properties=(disabled_property,), multi=True)
    descr = OptionDescription("opt", "", [stroption])
    od1 = OptionDescription("opt2", "", [intoption, s, descr])
    cfg = Config(od1)
    cfg.property.read_write()
    assert not 'disabled' in cfg.option('opt.str').property.get()
    cfg.option('int').value.set(1)
    with pytest.raises(PropertiesOptionError):
        cfg.option('opt.str').value.get()
    assert 'disabled' not in cfg.unrestraint.option('opt.str').property.get(only_raises=True, apply_requires=False)
    assert 'disabled' in cfg.unrestraint.option('opt.str').property.get()
#    assert not list_sessions()


def test_multi_with_requires_with_disabled_in_another_group():
    s = StrOption("string", "", default=["string"], multi=True)
    intoption = IntOption('int', 'Test int option', default=0)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(intoption),
                                                   'expected': ParamValue(1)}))
    stroption = StrOption('str', 'Test string option', default=["abc"], properties=(disabled_property,), multi=True)
    descr = OptionDescription("opt", "", [stroption])
    od1 = OptionDescription("opt2", "", [intoption, s, descr])
    cfg = Config(od1)
    cfg.property.read_write()
    assert not 'disabled' in cfg.option('opt.str').property.get()
    cfg.option('int').value.set(1)
    with pytest.raises(PropertiesOptionError):
        cfg.option('opt.str').value.set(['a', 'b'])
    assert 'disabled' in cfg.unrestraint.option('opt.str').property.get()
#    assert not list_sessions()


def test_multi_with_requires_that_is_leadership_follower():
    b = IntOption('int', 'Test int option', default=[0], multi=True)
    c = StrOption('str', 'Test string option', multi=True)
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(c),
                                                 'index': ParamIndex(),
                                                 'expected': ParamValue('1')}))
    d = StrOption('str1', 'Test string option', properties=(hidden_property,), multi=True)
    descr = Leadership("int", "", [b, c, d])
    od1 = OptionDescription('od', '', [descr])
    cfg = Config(od1)
    cfg.property.read_write()
    assert cfg.option('int.int').value.get() == [0]
    assert cfg.option('int.str', 0).value.get() == None
    assert cfg.option('int.str1', 0).value.get() == None
    cfg.option('int.int').value.set([0, 1])
    assert cfg.option('int.int').value.get() == [0, 1]
    assert cfg.option('int.str', 0).value.get() == None
    assert cfg.option('int.str', 1).value.get() == None
    assert cfg.option('int.str1', 0).value.get() == None
    assert cfg.option('int.str1', 1).value.get() == None
    cfg.option('int.str', 1).value.set('1')
    cfg.property.read_only()
    assert cfg.option('int.str1', 0).value.get() == None
    assert cfg.option('int.str1', 1).value.get() == None
    cfg.property.read_write()
    assert cfg.option('int.str1', 0).value.get() == None
    with pytest.raises(PropertiesOptionError):
        cfg.option('int.str1', 1).value.get()
#    assert not list_sessions()


def test_multi_with_requires_that_is_leadership_follower_inverse():
    b = IntOption('int', 'Test int option', default=[0], multi=True)
    c = StrOption('str', 'Test string option', multi=True)
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(c),
                                                 'index': ParamIndex(),
                                                 'reverse_condition': ParamValue(True),
                                                 'expected': ParamValue(None)}))
    d = StrOption('str1', 'Test string option', properties=(hidden_property,), multi=True)
    descr = Leadership("int", "", [b, c, d])
    od1 = OptionDescription('od', '', [descr])
    cfg = Config(od1)
    cfg.property.read_write()
    assert cfg.option('int.int').value.get() == [0]
    assert cfg.option('int.str', 0).value.get() is None
    assert cfg.option('int.str1', 0).value.get() is None
    cfg.option('int.int').value.set([0, 1])
    assert cfg.option('int.int').value.get() == [0, 1]
    assert cfg.option('int.str', 0).value.get() is None
    assert cfg.option('int.str', 1).value.get() is None
    assert cfg.option('int.str1', 0).value.get() is None
    assert cfg.option('int.str1', 1).value.get() is None
    cfg.option('int.str', 1).value.set('1')
    cfg.property.read_only()
    assert cfg.option('int.str1', 0).value.get() is None
    assert cfg.option('int.str1', 1).value.get() is None
    cfg.property.read_write()
    assert cfg.option('int.str1', 0).value.get() is None
    with pytest.raises(PropertiesOptionError):
        cfg.option('int.str1', 1).value.get()
#    assert not list_sessions()


def test_multi_with_bool():
    s = BoolOption("bool", "", default=[False], multi=True)
    od1 = OptionDescription("options", "", [s])
    cfg = Config(od1)
    cfg.option('bool').value.set([True, False])
    assert cfg.option('bool').value.get() == [True, False]
#    assert not list_sessions()


def test_choice_access_with_multi():
    ch = ChoiceOption("t1", "", ("a", "b"), default=["a"], multi=True, properties=('notunique',))
    od1 = OptionDescription("options", "", [ch])
    cfg = Config(od1)
    cfg.option('t1').value.set(["a", "b", "a", "b"])
    assert cfg.option('t1').value.get() == ["a", "b", "a", "b"]
#    assert not list_sessions()


#____________________________________________________________
def test_accepts_multiple_changes_from_option():
    s = StrOption("string", "", default="string")
    od1 = OptionDescription("options", "", [s])
    cfg = Config(od1)
    cfg.option('string').value.set("egg")
    assert cfg.option('string').value.default() == "string"
    assert cfg.option('string').value.get() == "egg"
    cfg.option('string').value.set('blah')
    assert cfg.option('string').value.default() == "string"
    assert cfg.option('string').value.get() == "blah"
    cfg.option('string').value.set('bol')
    assert cfg.option('string').value.get() == 'bol'
#    assert not list_sessions()


def test_allow_multiple_changes_from_config():
    """
    a `setoption` from the config object is much like the attribute access,
    except the fact that value owner can bet set
    """
    s = StrOption("string", "", default="string")
    s2 = StrOption("string2", "", default="string")
    suboption = OptionDescription("bip", "", [s2])
    od1 = OptionDescription("options", "", [s, suboption])
    cfg = Config(od1)
    cfg.option('string').value.set("oh")
    assert cfg.option('string').value.get() == "oh"
    cfg.option('string').value.set("blah")
    assert cfg.option('string').value.get() == "blah"
#    assert not list_sessions()


# ____________________________________________________________
# accessing a value by the get method
def test_access_by_get():
    od1 = make_description()
    cfg = Config(od1)
    assert cfg.option('wantref').value.get() is False
    assert cfg.option('gc.dummy').value.get() is False
#    assert not list_sessions()


def test_access_by_get_whith_hide():
    b1 = BoolOption("b1", "", properties=(('hidden'),))
    od1 = OptionDescription("opt", "",
                            [OptionDescription("sub", "",
                                               [b1, ChoiceOption("c1", "", ('a', 'b', 'c'), 'a'),
                                                BoolOption("d1", "")]),
                             BoolOption("b2", ""),
                             BoolOption("d1", "")])
    cfg = Config(od1)
    cfg.property.read_write()
    with pytest.raises(AttributeError):
        cfg.option('b1').value.get()
#    assert not list_sessions()


def test_append_properties():
    od1 = make_description()
    cfg = Config(od1)
    assert cfg.option('gc.dummy').property.get() == set()
    cfg.option('gc.dummy').property.add('test')
    assert cfg.option('gc.dummy').property.get() == {'test'}
    with pytest.raises(ConfigError):
        cfg.option('gc.dummy').property.add('force_store_value')
    assert cfg.option('gc.dummy').property.get() == {'test'}
#    assert not list_sessions()


def test_reset_properties():
    od1 = make_description()
    cfg = Config(od1)
    assert cfg.option('gc.dummy').property.get() == set()
    cfg.option('gc.dummy').property.add('frozen')
    assert cfg.option('gc.dummy').property.get() == {'frozen'}
    cfg.option('gc.dummy').property.reset()
    assert cfg.option('gc.dummy').property.get() == set()
#    assert not list_sessions()


def test_properties_cached():
    b1 = BoolOption("b1", "", properties=('test',))
    od1 = OptionDescription("opt", "", [OptionDescription("sub", "", [b1])])
    cfg = Config(od1)
    cfg.property.read_write()
    assert cfg.option('sub.b1').property.get() == {'test'}
#    assert not list_sessions()


def test_append_properties_force_store_value():
    gcdummy = BoolOption('dummy', 'dummy', default=False, properties=('force_store_value',))
    gcgroup = OptionDescription('gc', '', [gcdummy])
    od1 = OptionDescription('tiramisu', '', [gcgroup])
    cfg = Config(od1)
    assert cfg.option('gc.dummy').property.get() == {'force_store_value'}
    cfg.option('gc.dummy').property.add('test')
    assert cfg.option('gc.dummy').property.get() == {'force_store_value', 'test'}
#    assert not list_sessions()


def test_properties_get_add_reset():
    gcdummy = BoolOption('dummy', 'dummy', default=False, properties=('force_store_value',))
    gcgroup = OptionDescription('gc', '', [gcdummy])
    od1 = OptionDescription('tiramisu', '', [gcgroup])
    cfg = Config(od1)
    assert cfg.property.get() == {'validator', 'warnings', 'cache'}
    cfg.property.add('frozen')
    assert cfg.property.get() == {'validator', 'warnings', 'cache', 'frozen'}
    cfg.property.reset()
    assert cfg.property.get() == frozenset()


def test_reset_properties_force_store_value():
    gcdummy = BoolOption('dummy', 'dummy', default=False, properties=('force_store_value',))
    gcgroup = OptionDescription('gc', '', [gcdummy])
    od1 = OptionDescription('tiramisu', '', [gcgroup])
    cfg = Config(od1)
    assert cfg.property.exportation() == {'properties': {None: {None: frozenset({'cache',
                                                                                 'validator',
                                                                                 'warnings'})}},
                                          'ro_append': frozenset({'disabled',
                                                                  'empty',
                                                                  'everything_frozen',
                                                                  'force_store_value',
                                                                  'frozen',
                                                                  'mandatory',
                                                                  'validator'}),
                                          'ro_remove': frozenset({'hidden',
                                                                  'permissive'}),
                                          'rw_append': frozenset({'disabled',
                                                                  'force_store_value',
                                                                  'frozen',
                                                                  'hidden',
                                                                  'validator'}),
                                          'rw_remove': frozenset({'empty',
                                                                  'everything_frozen',
                                                                  'mandatory',
                                                                  'permissive'}),
                                         }

    cfg.property.add('frozen')
    assert cfg.property.exportation() == \
           {
            'properties': {None: {None: frozenset({'cache',
                                                   'frozen',
                                                   'validator',
                                                   'warnings'})}},
            'ro_append': frozenset({'disabled',
                                    'empty',
                                    'everything_frozen',
                                    'force_store_value',
                                    'frozen',
                                    'mandatory',
                                    'validator'}),
            'ro_remove': frozenset({'hidden',
                                    'permissive'}),
            'rw_append': frozenset({'disabled',
                                    'force_store_value',
                                    'frozen',
                                    'hidden',
                                    'validator'}),
            'rw_remove': frozenset({'empty',
                                    'everything_frozen',
                                    'mandatory',
                                    'permissive'}),
           }
    cfg.property.reset()
    assert cfg.property.exportation() == {'properties': {None: {}},
                                          'ro_append': frozenset({'disabled',
                                                                  'empty',
                                                                  'everything_frozen',
                                                                  'force_store_value',
                                                                  'frozen',
                                                                  'mandatory',
                                                                  'validator'}),
                                          'ro_remove': frozenset({'hidden',
                                                                  'permissive'}),
                                          'rw_append': frozenset({'disabled',
                                                                  'force_store_value',
                                                                  'frozen',
                                                                  'hidden',
                                                                  'validator'}),
                                          'rw_remove': frozenset({'empty',
                                                                  'everything_frozen',
                                                                  'mandatory',
                                                                  'permissive'}),
                                         }

    cfg.option('gc.dummy').property.add('test')
    assert cfg.property.exportation() == {
                                          'properties': {None: {},
                                                         'gc.dummy': {None: frozenset({'test'})}},
                                          'ro_append': frozenset({'disabled',
                                                                  'empty',
                                                                  'everything_frozen',
                                                                  'force_store_value',
                                                                  'frozen',
                                                                  'mandatory',
                                                                  'validator'}),
                                          'ro_remove': frozenset({'hidden',
                                                                  'permissive'}),
                                          'rw_append': frozenset({'disabled',
                                                                  'force_store_value',
                                                                  'frozen',
                                                                  'hidden',
                                                                  'validator'}),
                                          'rw_remove': frozenset({'empty',
                                                                  'everything_frozen',
                                                                  'mandatory',
                                                                  'permissive'}),
                                         }

    cfg.property.reset()
    assert cfg.property.exportation() == {
                                          'properties': {None: {},
                                                         'gc.dummy': {None: frozenset({'test'})}},
                                          'ro_append': frozenset({'disabled',
                                                                  'empty',
                                                                  'everything_frozen',
                                                                  'force_store_value',
                                                                  'frozen',
                                                                  'mandatory',
                                                                  'validator'}),
                                          'ro_remove': frozenset({'hidden',
                                                                  'permissive'}),
                                          'rw_append': frozenset({'disabled',
                                                                  'force_store_value',
                                                                  'frozen',
                                                                  'hidden',
                                                                  'validator'}),
                                          'rw_remove': frozenset({'empty',
                                                                  'everything_frozen',
                                                                  'mandatory',
                                                                  'permissive'}),
                                         }

    cfg.property.add('frozen')
    assert cfg.property.exportation() == \
            {
             'properties': {None: {None: frozenset({'frozen'})},
                            'gc.dummy': {None: frozenset({'test'})}},
             'ro_append': frozenset({'disabled',
                                     'empty',
                                     'everything_frozen',
                                     'force_store_value',
                                     'frozen',
                                     'mandatory',
                                     'validator'}),
             'ro_remove': frozenset({'hidden',
                                     'permissive'}),
             'rw_append': frozenset({'disabled',
                                     'force_store_value',
                                     'frozen',
                                     'hidden',
                                     'validator'}),
             'rw_remove': frozenset({'empty',
                                     'everything_frozen',
                                     'mandatory',
                                     'permissive'}),
            }
    cfg.property.add('frozen')
    assert cfg.property.exportation() == \
            {
             'properties': {None: {None: frozenset({'frozen'})}, 'gc.dummy': {None: frozenset({'test'})}},
             'ro_append': frozenset({'disabled',
                                     'empty',
                                     'everything_frozen',
                                     'force_store_value',
                                     'frozen',
                                     'mandatory',
                                     'validator'}),
             'ro_remove': frozenset({'hidden',
                                     'permissive'}),
             'rw_append': frozenset({'disabled',
                                     'force_store_value',
                                     'frozen',
                                     'hidden',
                                     'validator'}),
             'rw_remove': frozenset({'empty',
                                     'everything_frozen',
                                     'mandatory',
                                     'permissive'}),
            }
    cfg.option('gc.dummy').property.add('test')
    assert cfg.property.exportation() == \
            {
             'properties': {None: {None: frozenset({'frozen'})}, 'gc.dummy': {None: frozenset({'test'})}},
             'ro_append': frozenset({'disabled',
                                     'empty',
                                     'everything_frozen',
                                     'force_store_value',
                                     'frozen',
                                     'mandatory',
                                     'validator'}),
             'ro_remove': frozenset({'hidden',
                                     'permissive'}),
             'rw_append': frozenset({'disabled',
                                     'force_store_value',
                                     'frozen',
                                     'hidden',
                                     'validator'}),
             'rw_remove': frozenset({'empty',
                                     'everything_frozen',
                                     'mandatory',
                                     'permissive'}),
            }
#    assert not list_sessions()


#def test_importation_force_store_value():
#    gcdummy = BoolOption('dummy', 'dummy', default=False,
#                         properties=('force_store_value',))
#    gcgroup = OptionDescription('gc', '', [gcdummy])
#    od1 = OptionDescription('tiramisu', '', [gcgroup])
#    config1 = Config(od1)
#    assert config1.value.exportation() == {}
#    config1.property.add('frozen')
#    assert config1.value.exportation() == {}
#    config1.property.add('force_store_value')
#    assert config1.value.exportation() == {'gc.dummy': {None: [False, 'forced']}}
#    exportation = config1.property.exportation()
#    config2 = Config(od1)
#    assert config2.value.exportation() == {}
#    config2.property.importation(exportation)
#    assert config2.value.exportation() == {'gc.dummy': {None: [False, 'forced']}}
#    config2.property.importation(exportation)
#    assert config2.value.exportation() == {'gc.dummy': {None: [False, 'forced']}}
##    assert not list_sessions()
#
#
def test_set_modified_value():
    gcdummy = BoolOption('dummy', 'dummy', default=False, properties=('force_store_value',))
    gcgroup = OptionDescription('gc', '', [gcdummy])
    od1 = OptionDescription('tiramisu', '', [gcgroup])
    cfg = Config(od1)
    assert cfg.property.exportation() == {
                                          'properties': {None: {None: frozenset({'cache',
                                                                                 'validator',
                                                                                 'warnings'})}},
                                          'ro_append': frozenset({'disabled',
                                                                  'empty',
                                                                  'everything_frozen',
                                                                  'force_store_value',
                                                                  'frozen',
                                                                  'mandatory',
                                                                  'validator'}),
                                          'ro_remove': frozenset({'hidden',
                                                                  'permissive'}),
                                          'rw_append': frozenset({'disabled',
                                                                  'force_store_value',
                                                                  'frozen',
                                                                  'hidden',
                                                                  'validator'}),
                                          'rw_remove': frozenset({'empty',
                                                                  'everything_frozen',
                                                                  'mandatory',
                                                                  'permissive'}),
                                         }

    cfg.property.importation({
                              'properties': {None: {None: frozenset({'cache',
                                                                     'frozen',
                                                                     'validator',
                                                                     'warnings'})}},
                              'ro_append': frozenset({'disabled',
                                                      'empty',
                                                      'everything_frozen',
                                                      'force_store_value',
                                                      'frozen',
                                                      'mandatory',
                                                      'validator'}),
                              'ro_remove': frozenset({'hidden',
                                                      'permissive'}),
                              'rw_append': frozenset({'disabled',
                                                      'force_store_value',
                                                      'frozen',
                                                      'hidden',
                                                      'validator'}),
                              'rw_remove': frozenset({'empty',
                                                      'everything_frozen',
                                                      'mandatory',
                                                      'permissive'}),
                             })
    assert cfg.property.exportation() == \
            {
             'properties': {None: {None: frozenset({'cache',
                                                    'frozen',
                                                    'validator',
                                                    'warnings'})}},
             'ro_append': frozenset({'disabled',
                                     'empty',
                                     'everything_frozen',
                                     'force_store_value',
                                     'frozen',
                                     'mandatory',
                                     'validator'}),
             'ro_remove': frozenset({'hidden',
                                     'permissive'}),
             'rw_append': frozenset({'disabled',
                                     'force_store_value',
                                     'frozen',
                                     'hidden',
                                     'validator'}),
             'rw_remove': frozenset({'empty',
                                     'everything_frozen',
                                     'mandatory',
                                     'permissive'}),
            }
#    assert not list_sessions()


#def test_none_is_not_modified():
#    gcdummy = StrOption('dummy', 'dummy', properties=('force_store_value',))
#    gcdummy1 = StrOption('dummy1', 'dummy1', default="str", properties=('force_store_value',))
#    gcgroup = OptionDescription('gc', '', [gcdummy, gcdummy1])
#    od1 = OptionDescription('tiramisu', '', [gcgroup])
#    cfg = Config(od1)
#    assert cfg.value.exportation() == {}
#    cfg.property.read_write()
#    assert cfg.value.exportation() == {'gc.dummy1': {None: ['str', 'forced']}}
##    assert not list_sessions()
#
#
def test_pprint():
    msg_error = _("cannot access to {0} {1} because has {2} {3}")
    msg_is_not = _('the value of "{0}" is not {1}')
    msg_is = _('the value of "{0}" is {1}')
    properties = _('properties')
    prop = _('property')

    s = StrOption("string", "", default=["string"], default_multi="string", multi=True, properties=('hidden', 'disabled'))
    s2 = StrOption("string2", "", default="string")
    s3 = StrOption("string3", "", default=["string"], default_multi="string", multi=True, properties=('hidden',))
    intoption = IntOption('int', 'Test int option', default=0)
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(intoption),
                                                 'expected_0': ParamValue(2),
                                                 'expected_1': ParamValue(3),
                                                 'expected_2': ParamValue(4),
                                                 'reverse_condition': ParamValue(True)}),
                                  calc_value_property_help)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition_0': ParamOption(intoption),
                                                   'expected_0': ParamValue(1),
                                                   'condition_1': ParamOption(s2),
                                                   'expected_1': ParamValue('string')}),
                                    calc_value_property_help)
    stroption = StrOption('str', 'Test string option', default="abc", properties=(hidden_property, disabled_property))

    val2 = StrOption('val2', "")
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(intoption),
                                                 'expected': ParamValue(1)}),
                                  calc_value_property_help)
    descr2 = OptionDescription("options", "options", [val2], properties=(hidden_property,))

    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(stroption),
                                                 'expected': ParamValue('2'),
                                                 'reverse_condition': ParamValue(True)}),
                                  calc_value_property_help)
    val3 = StrOption('val3', "", properties=(hidden_property,))

    od1 = OptionDescription("options", "root option", [s, s2, s3, intoption, stroption, descr2, val3])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.option('int').value.set(1)
    err = None
    try:
        cfg.option('str').value.get()
    except PropertiesOptionError as error:
        err = error

    list_disabled = '"disabled" (' + display_list([msg_is.format('Test int option', '"1"'), msg_is.format('string2', '"string"')], add_quote=False) + ')'
    list_hidden = '"hidden" (' + msg_is_not.format('Test int option', display_list([2, 3, 4], separator='or', add_quote=True)) + ')'
    assert str(err) == _(msg_error.format('option', '"Test string option"', properties, display_list([list_disabled, list_hidden], add_quote=False)))
    del err

    err = None
    try:
        cfg.option('options.val2').value.get()
    except PropertiesOptionError as error:
        err = error

    assert str(err) == msg_error.format('optiondescription', '"options"', prop, '"hidden" (' + msg_is.format('Test int option', '"1"') + ')')

    #err = None
    #try:
    #    cfg.option('val3').value.get()
    #except PropertiesOptionError as error:
    #    err = error

    #msg_1 = msg_is.format('string2', 'string')
    #msg_2 = msg_is.format('Test int option', 1)
    #msg_3 = msg_is_not.format('Test int option', display_list([2, 3, 4], 'or', add_quote=True))
    #list_hidden = '"hidden" (' + display_list([msg_2, msg_3, msg_1]) + ')'

    #assert str(err) == msg_error.format('option', 'val3', prop, list_hidden)

    err = None
    try:
        cfg.option('string').value.get()
    except Exception as error:
        err = error

    assert str(err) == msg_error.format('option', '"string"', properties, display_list(['disabled', 'hidden'], add_quote=True))
    del err

    err = None
    try:
        cfg.option('string3').value.get()
    except Exception as error:
        err = error

    assert str(err) == msg_error.format('option', '"string3"', prop, '"hidden"')
    del err
#    assert not list_sessions()


def test_pprint_not_todict():
    msg_error = _("cannot access to {0} {1} because has {2} {3}")
    msg_is_not = _('the value of "{0}" is not {1}')
    msg_is = _('the value of "{0}" is {1}')
    properties = _('properties')
    prop = _('property')

    s = StrOption("string", "", default=["string"], default_multi="string", multi=True, properties=('hidden', 'disabled'))
    s2 = StrOption("string2", "", default="string")
    s3 = StrOption("string3", "", default=["string"], default_multi="string", multi=True, properties=('hidden',))
    intoption = IntOption('int', 'Test int option', default=0)
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(intoption),
                                                 'expected_0': ParamValue(2),
                                                 'expected_1': ParamValue(3),
                                                 'expected_2': ParamValue(4),
                                                 'reverse_condition': ParamValue(True)}),
                                  )
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition_0': ParamOption(intoption),
                                                   'expected_0': ParamValue(1),
                                                   'condition_1': ParamOption(s2),
                                                   'expected_1': ParamValue('string')}),
                                    )
    stroption = StrOption('str', 'Test string option', default="abc", properties=(hidden_property, disabled_property))

    val2 = StrOption('val2', "")
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(intoption),
                                                 'expected': ParamValue(1)}),
                                  )
    descr2 = OptionDescription("options", "options", [val2], properties=(hidden_property,))

    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(stroption),
                                                 'expected': ParamValue('2'),
                                                 'reverse_condition': ParamValue(True)}),
                                  )
    val3 = StrOption('val3', "", properties=(hidden_property,))

    od1 = OptionDescription("options", "root option", [s, s2, s3, intoption, stroption, descr2, val3])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.option('int').value.set(1)
    err = None
    try:
        cfg.option('str').value.get()
    except PropertiesOptionError as error:
        err = error

    list_disabled = '"disabled"'
    list_hidden = '"hidden"'
    assert str(err) == _(msg_error.format('option', '"Test string option"', properties, display_list([list_disabled, list_hidden], add_quote=False)))
    del err

    err = None
    try:
        cfg.option('options.val2').value.get()
    except PropertiesOptionError as error:
        err = error

    assert str(err) == msg_error.format('optiondescription', '"options"', prop, '"hidden"')

    err = None
    try:
        cfg.option('string').value.get()
    except Exception as error:
        err = error

    assert str(err) == msg_error.format('option', '"string"', properties, display_list(['disabled', 'hidden'], add_quote=True))
    del err

    err = None
    try:
        cfg.option('string3').value.get()
    except Exception as error:
        err = error

    assert str(err) == msg_error.format('option', '"string3"', prop, '"hidden"')
    del err
#    assert not list_sessions()


def test_property_invalid_type():
    with pytest.raises(ValueError):
        s3 = StrOption("string3", "", default=["string"], default_multi="string", multi=True, properties=(1,))


def test_settings_list_with_follower():
    leader = StrOption("leader", "leader", default=['leader'], multi=True)
    option = StrOption("str", "str", default_multi="dhcp", multi=True, properties=frozenset({'disabled'}))
    ip = StrOption(name="ip",
                   doc="ip",
                   multi=True,
                   properties=frozenset({"basic", "mandatory", Calculation(calc_value, Params(ParamValue('disabled'), kwargs={'condition': ParamOption(option, notraisepropertyerror=True), 'expected': ParamValue("ipv4"), 'reverse_condition': ParamValue(True)}), calc_value_property_help)}),
                   )
    descr = Leadership("root", "", [leader, option, ip])
    cfg = Config(OptionDescription('root', 'root', [descr]))
    cfg.property.read_write()
    assert parse_od_get(cfg.option('root').value.get()) == {'root.leader': ['leader']}
    assert len(cfg.option('root').list()) == 1
    assert len(cfg.option('root').list(validate_properties=False)) == 3


def return_none(*args):
    return


def test_settings_disable_set_information(config_type):
    opt1 = StrOption('opt1', '', ['val'], multi=True)
    opt2 = StrOption('opt2', '', default_multi='test', validators=[Calculation(return_none, Params((ParamInformation('key'))))], properties=frozenset([Calculation(return_none, Params((ParamInformation('key'))))]), multi=True)
    od2 = Leadership('leadership', '', [opt1, opt2])
    od1 = OptionDescription('root', '', [od2])
    cfg = Config(od1)
    cfg.property.read_only()
    cfg.information.set('key', 'val')
    assert parse_od_get(cfg.value.get()) == {'leadership.opt1': [{'leadership.opt1': 'val', 'leadership.opt2': 'test'}]}
