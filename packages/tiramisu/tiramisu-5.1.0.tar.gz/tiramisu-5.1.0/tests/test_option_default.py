"test all types of option default values for options, add new option in a descr"
from .autopath import do_autopath
do_autopath()

import pytest
from tiramisu.setting import owners
from tiramisu.error import PropertiesOptionError, ConfigError, LeadershipError
from tiramisu import IntOption, FloatOption, StrOption, ChoiceOption, \
    BoolOption, OptionDescription, Leadership, Config, undefined
from .config import config_type, get_config


owners.addowner("frozenmultifollower")


def make_description():
    gcoption = ChoiceOption('name', 'GC name', ['ref', 'framework'], 'ref')
    gcdummy = BoolOption('dummy', 'dummy', default=False)
    objspaceoption = ChoiceOption('objspace', 'Object space',
                                  ['std', 'thunk'], 'std')
    booloption = BoolOption('bool', 'Test boolean option', default=True)
    intoption = IntOption('int', 'Test int option', default=0)
    floatoption = FloatOption('float', 'Test float option', default=2.3)
    stroption = StrOption('str', 'Test string option', default="abc")
    boolop = BoolOption('boolop', 'Test boolean option op', default=True)
    wantref_option = BoolOption('wantref', 'Test requires', default=False,
                                requires=['boolop'])
    wantframework_option = BoolOption('wantframework', 'Test requires',
                                      default=False,
                                      requires=['boolop'])

    gcgroup = OptionDescription('gc', '', [gcoption, gcdummy, floatoption])
    descr = OptionDescription('tiramisu', '', [gcgroup, booloption, objspaceoption,
                                               wantref_option, stroption,
                                               wantframework_option,
                                               intoption, boolop])
    return descr


#____________________________________________________________
# default values
def test_default_is_none(config_type):
    """
    Most constructors take a ``default`` argument that specifies the default
    value of the option. If this argument is not supplied the default value is
    assumed to be ``None``.
    """
    dummy1 = BoolOption('dummy1', 'doc dummy')
    dummy2 = BoolOption('dummy2', 'doc dummy')
    od1 = OptionDescription('group', '', [dummy1, dummy2])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    # so when the default value is not set, there is actually a default value
    assert cfg.option('dummy1').value.get() is None
    assert cfg.option('dummy2').value.get() is None
#    assert not list_sessions()


def test_set_defaut_value_from_option_object():
    """Options have an available default setting and can give it back"""
    b = BoolOption("boolean", "", default=False)
    assert b.impl_getdefault() is False
#    assert not list_sessions()


def test_force_default_on_freeze():
    "a frozen option wich is forced returns his default"
    dummy1 = BoolOption('dummy1', 'doc dummy', default=False, properties=('force_default_on_freeze',))
    dummy2 = BoolOption('dummy2', 'doc dummy', default=True)
    od1 = OptionDescription('group', '', [dummy1, dummy2])
    cfg_ori = Config(od1)
    cfg_ori.property.read_write()
    cfg = cfg_ori
    # FIXME cfg = get_config(cfg_ori, config_type)
    owner = cfg.owner.get()
    cfg.option('dummy1').value.set(True)
    cfg.option('dummy2').value.set(False)
    assert cfg.option('dummy1').owner.get() == owner
    assert cfg.option('dummy2').owner.get() == owner
    # if config_type == 'tiramisu-api':
    #     cfg.send()
    cfg_ori.option('dummy1').property.add('frozen')
    cfg_ori.option('dummy2').property.add('frozen')
    # cfg = get_config(cfg_ori, config_type)
    assert cfg.option('dummy1').value.get() is False
    assert cfg.option('dummy2').value.get() is False
    assert cfg.option('dummy1').owner.isdefault()
    assert cfg.option('dummy2').owner.get() == owner
    # if config_type == 'tiramisu-api':
    #     cfg.send()
    with pytest.raises(PropertiesOptionError):
        cfg_ori.option('dummy2').owner.set('frozen')
    # cfg = get_config(cfg_ori, config_type)
    with pytest.raises(PropertiesOptionError):
        cfg.option('dummy1').value.reset()
    # if config_type == 'tiramisu-api':
    #     cfg.send()
    cfg_ori.option('dummy1').property.remove('frozen')
    # cfg = get_config(cfg_ori, config_type)
    cfg.option('dummy1').value.reset()
    # if config_type == 'tiramisu-api':
    #     cfg.send()
    cfg.option('dummy1').property.add('frozen')
    # cfg = get_config(cfg_ori, config_type)
    with pytest.raises(PropertiesOptionError):
        cfg.option('dummy2').owner.set('frozen')
#    assert not list_sessions()


def test_force_default_on_freeze_multi():
    dummy1 = BoolOption('dummy1', 'doc dummy', default=[False], properties=('force_default_on_freeze',), multi=True)
    dummy2 = BoolOption('dummy2', 'doc dummy', default=[True], multi=True)
    od1 = OptionDescription('group', '', [dummy1, dummy2])
    cfg_ori = Config(od1)
    cfg_ori.property.read_write()
    cfg = cfg_ori
    # FIXME cfg = get_config(cfg_ori, config_type)
    default = cfg.option('dummy1').value.default()[0]
    cfg.option('dummy1').value.set([default, True])
    default = cfg.option('dummy2').value.default()[0]
    cfg.option('dummy2').value.set([default, False])
    owner = cfg.owner.get()
    assert cfg.option('dummy1').owner.get() == owner
    assert cfg.option('dummy2').owner.get() == owner
    # if config_type == 'tiramisu-api':
    #     cfg.send()
    cfg_ori.option('dummy1').property.add('frozen')
    cfg_ori.option('dummy2').property.add('frozen')
    # cfg = get_config(cfg_ori, config_type)
    assert cfg.option('dummy1').value.get() == [False]
    assert cfg.option('dummy2').value.get() == [True, False]
    assert cfg.option('dummy1').owner.isdefault()
    assert cfg.option('dummy2').owner.get() == owner
    # if config_type == 'tiramisu-api':
    #     cfg.send()
    with pytest.raises(PropertiesOptionError):
        cfg_ori.option('dummy2').owner.set('owner')
    # cfg = get_config(cfg_ori, config_type)
    with pytest.raises(PropertiesOptionError):
        cfg.option('dummy2').value.reset()
    # if config_type == 'tiramisu-api':
    #     cfg.send()
    cfg_ori.option('dummy1').property.remove('frozen')
    # cfg = get_config(cfg_ori, config_type)
    cfg.option('dummy1').value.reset()
#    assert not list_sessions()


#def test_force_default_on_freeze_leader():
#    dummy1 = BoolOption('dummy1', 'Test int option', multi=True, properties=('force_default_on_freeze',))
#    dummy2 = BoolOption('dummy2', 'Test string option', multi=True)
#    descr = Leadership("dummy1", "", [dummy1, dummy2])
#    od1 = OptionDescription("root", "", [descr])
#    with pytest.raises(ConfigError):
#        Config(od1)
#    assert not list_sessions()


#def test_force_metaconfig_on_freeze_leader():
#    dummy1 = BoolOption('dummy1', 'Test int option', multi=True, properties=('force_metaconfig_on_freeze',))
#    dummy2 = BoolOption('dummy2', 'Test string option', multi=True)
#    descr = Leadership("dummy1", "", [dummy1, dummy2])
#    od1 = OptionDescription("root", "", [descr])
#    with pytest.raises(ConfigError):
#        Config(od1)
#    assert not list_sessions()


def test_force_default_on_freeze_follower(config_type):
    dummy1 = BoolOption('dummy1', 'Test int option', multi=True, properties=('notunique',))
    dummy2 = BoolOption('dummy2', 'Test string option', multi=True, properties=('force_default_on_freeze',))
    descr = Leadership("dummy1", "", [dummy1, dummy2])
    od1 = OptionDescription("root", "", [descr])
    cfg_ori = Config(od1)
    cfg_ori.property.read_write()
    cfg = get_config(cfg_ori, config_type)
    cfg.option('dummy1.dummy1').value.set([True])
    cfg.option('dummy1.dummy2', 0).value.set(False)
    assert cfg.option('dummy1.dummy1').value.get() == [True]
    assert cfg.option('dummy1.dummy2', 0).value.get() == False
    assert cfg.option('dummy1.dummy1').owner.get() == 'user'
    assert cfg.option('dummy1.dummy2', 0).owner.get() == 'user'
    #
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.option('dummy1.dummy2').property.add('frozen')
    cfg = get_config(cfg_ori, config_type)
    assert cfg.option('dummy1.dummy1').value.get() == [True]
    assert cfg.option('dummy1.dummy2', 0).value.get() == None
    assert cfg.option('dummy1.dummy1').owner.get() == 'user'
    assert cfg.option('dummy1.dummy2', 0).owner.isdefault()
    if config_type == 'tiramisu-api':
        cfg.send()
    with pytest.raises(PropertiesOptionError):
        cfg_ori.option('dummy1.dummy2', 0).owner.set('frozenmultifollower')
    cfg = get_config(cfg_ori, config_type)
    #
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.option('dummy1.dummy2').property.remove('frozen')
    cfg = get_config(cfg_ori, config_type)
    cfg.option('dummy1.dummy1').value.set([True, True])
    cfg.option('dummy1.dummy2', 1).value.set(False)
    assert cfg.option('dummy1.dummy1').value.get() == [True, True]
    assert cfg.option('dummy1.dummy2', 0).value.get() == False
    assert cfg.option('dummy1.dummy2', 1).value.get() == False
    #
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.option('dummy1.dummy2').property.add('frozen')
    cfg = get_config(cfg_ori, config_type)
    assert cfg.option('dummy1.dummy1').value.get() == [True, True]
    assert cfg.option('dummy1.dummy2', 0).value.get() == None
    assert cfg.option('dummy1.dummy2', 1).value.get() == None
    #
    cfg.option('dummy1.dummy1').value.pop(1)
    assert cfg.option('dummy1.dummy1').value.get() == [True]
    assert cfg.option('dummy1.dummy2', 0).value.get() == None
    #
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.option('dummy1.dummy2').property.remove('frozen')
    cfg = get_config(cfg_ori, config_type)
    assert cfg.option('dummy1.dummy1').value.get() == [True]
    assert cfg.option('dummy1.dummy2', 0).value.get() == False
    #
    cfg.option('dummy1.dummy1').value.set([True, True])
    assert cfg.option('dummy1.dummy2', 0).value.get() == False
    assert cfg.option('dummy1.dummy2', 1).value.get() == None
#    assert not list_sessions()


def test_overrides_changes_option_value(config_type):
    "with config.override(), the default is changed and the value is changed"
    od1 = OptionDescription("test", "", [
        BoolOption("b", "", default=False)])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    cfg.option('b').value.set(True)
#    assert not list_sessions()


def test_choice_with_no_default(config_type):
    od1 = OptionDescription("test", "", [
        ChoiceOption("backend", "", ("c", "cli"))])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert cfg.option('backend').value.get() is None
    cfg.option('backend').value.set('c')
#    assert not list_sessions()


def test_choice_with_default(config_type):
    od1 = OptionDescription("test", "", [
        ChoiceOption("backend", "", ("c", "cli"), default="cli")])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert cfg.option('backend').value.get() == 'cli'
#    assert not list_sessions()
