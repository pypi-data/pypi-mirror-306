from .autopath import do_autopath
do_autopath()

import pytest

from tiramisu.setting import owners, groups
from tiramisu import ChoiceOption, BoolOption, IntOption, FloatOption, \
    StrOption, OptionDescription, SymLinkOption, Leadership, Config
from tiramisu.error import ConfigError, ConstError, PropertiesOptionError
from .config import config_type, get_config


owners.addowner("readonly2")
owners.addowner("new2")


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
    wantref_option = BoolOption('wantref', 'Test requires', default=False)
    wantframework_option = BoolOption('wantframework', 'Test requires',
                                      default=False)

    gcgroup = OptionDescription('gc', '', [gcoption, gcdummy, floatoption])
    descr = OptionDescription('tiram', '', [gcgroup, booloption, objspaceoption,
                                            wantref_option, stroption,
                                            wantframework_option,
                                            intoption, boolop])
    return descr


def test_default_owner(config_type):
    gcdummy = BoolOption('dummy', 'dummy', default=False)
    od1 = OptionDescription('tiramisu', '', [gcdummy])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert cfg.option('dummy').value.get() is False
    assert cfg.option('dummy').owner.get() == 'default'
    cfg.option('dummy').value.set(True)
    owner = cfg.owner.get()
    assert cfg.option('dummy').owner.get() == owner
#    assert not list_sessions()


def test_owner_unknown_func(config_type):
    gcdummy = BoolOption('dummy', 'dummy', default=False)
    od1 = OptionDescription('tiramisu', '', [gcdummy])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    with pytest.raises(ConfigError):
        owner = cfg.option('dummy').owner.unknown()
#    assert not list_sessions()


def test_hidden_owner():
    gcdummy = BoolOption('dummy', 'dummy', default=False, properties=('hidden',))
    od1 = OptionDescription('tiramisu', '', [gcdummy])
    cfg = Config(od1)
    cfg.property.read_write()
    #with pytest.raises(PropertiesOptionError):
    #    cfg.forcepermissive.option('dummy').owner.get()
    #with pytest.raises(PropertiesOptionError):
    #    cfg.option('dummy').owner.isdefault()
    #with pytest.raises(PropertiesOptionError):
    #    cfg.forcepermissive.option('dummy').owner.isdefault()
    cfg.permissive.add('hidden')
    cfg.forcepermissive.option('dummy').value.get()
    cfg.forcepermissive.option('dummy').owner.isdefault()
#    assert not list_sessions()


def test_addowner(config_type):
    gcdummy = BoolOption('dummy', 'dummy', default=False)
    od1 = OptionDescription('tiramisu', '', [gcdummy])
    cfg_ori = Config(od1)
    cfg = get_config(cfg_ori, config_type)
    assert cfg.option('dummy').value.get() is False
    assert cfg.option('dummy').owner.get() == 'default'
    assert cfg.option('dummy').owner.isdefault()
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.owner.set('gen_config')
    cfg = get_config(cfg_ori, config_type)
    cfg.option('dummy').value.set(True)
    assert cfg.option('dummy').owner.get() == owners.gen_config
    assert not cfg.option('dummy').owner.isdefault()
#    assert not list_sessions()


def test_addowner_multiple_time():
    owners.addowner("testowner2")
    with pytest.raises(ConstError):
        owners.addowner("testowner2")


def test_delete_owner():
    owners.addowner('deleted2')
    with pytest.raises(ConstError):
        del(owners.deleted2)


def test_owner_is_not_a_string(config_type):
    gcdummy = BoolOption('dummy', 'dummy', default=False)
    od1 = OptionDescription('tiramisu', '', [gcdummy])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert cfg.option('dummy').value.get() is False
    assert cfg.option('dummy').owner.get() == owners.default
    assert cfg.option('dummy').owner.get() == 'default'
    if config_type == 'tiramisu':
        assert isinstance(cfg.option('dummy').owner.get(), owners.Owner)
    cfg.option('dummy').value.set(True)
    assert cfg.option('dummy').owner.get() == 'user'
#    assert not list_sessions()


def test_setowner_without_valid_owner(config_type):
    gcdummy = BoolOption('dummy', 'dummy', default=False)
    od1 = OptionDescription('tiramisu', '', [gcdummy])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert cfg.option('dummy').value.get() is False
    assert cfg.option('dummy').owner.get() == 'default'
#    assert not list_sessions()


def test_setowner_for_value(config_type):
    gcdummy = BoolOption('dummy', 'dummy', default=False)
    od1 = OptionDescription('tiramisu', '', [gcdummy])
    cfg_ori = Config(od1)
    cfg = get_config(cfg_ori, config_type)
    assert cfg.option('dummy').value.get() is False
    assert cfg.option('dummy').owner.get() == 'default'
    if config_type == 'tiramisu-api':
        cfg.send()
    with pytest.raises(ConfigError):
        cfg_ori.option('dummy').owner.set('new2')
    cfg = get_config(cfg_ori, config_type)
    cfg.option('dummy').value.set(False)
    assert cfg.option('dummy').owner.get() == owners.user
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.option('dummy').owner.set('new2')
    cfg = get_config(cfg_ori, config_type)
    assert cfg.option('dummy').owner.get() == owners.new2
#    assert not list_sessions()


def test_setowner_forbidden(config_type):
    gcdummy = BoolOption('dummy', 'dummy', default=False)
    od1 = OptionDescription('tiramisu', '', [gcdummy])
    cfg_ori = Config(od1)
    cfg = get_config(cfg_ori, config_type)
    assert cfg.option('dummy').value.get() is False
    assert cfg.option('dummy').owner.get() == 'default'
    if config_type == 'tiramisu-api':
        cfg.send()
    with pytest.raises(ValueError):
        cfg_ori.owner.set('default')
    cfg = get_config(cfg_ori, config_type)
    cfg.option('dummy').value.set(False)
    if config_type == 'tiramisu-api':
        cfg.send()
    with pytest.raises(ValueError):
        cfg_ori.option('dummy').owner.set('default')
    cfg = get_config(cfg_ori, config_type)
#    assert not list_sessions()


def test_setowner_read_only(config_type):
    gcdummy = BoolOption('dummy', 'dummy', default=False)
    od1 = OptionDescription('tiramisu', '', [gcdummy])
    cfg_ori = Config(od1)
    cfg_ori.property.read_write()
    cfg = get_config(cfg_ori, config_type)
    assert cfg.option('dummy').value.get() is False
    assert cfg.option('dummy').owner.get() == 'default'
    cfg.option('dummy').value.set(False)
    assert cfg.option('dummy').owner.get() == owners.user
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.property.read_only()
    with pytest.raises(PropertiesOptionError):
        cfg_ori.option('dummy').owner.set('readonly2')
    cfg = get_config(cfg_ori, config_type)
    assert cfg.option('dummy').owner.get() == owners.user
#    assert not list_sessions()


def test_setowner_optiondescription(config_type):
    gcdummy = BoolOption('dummy', 'dummy', default=False)
    descr1 = OptionDescription('tiramisu', '', [gcdummy])
    od1 = OptionDescription('tiramisu', '', [descr1])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    with pytest.raises(ConfigError):
        cfg.option('tiramisu').owner.get()
    with pytest.raises(ConfigError):
        cfg.option('tiramisu').owner.set('user')
#    assert not list_sessions()


def test_setowner_symlinkoption(config_type):
    gcdummy = BoolOption('dummy', 'dummy', default=False)
    s = SymLinkOption('symdummy', gcdummy)
    descr1 = OptionDescription('tiramisu', '', [gcdummy, s])
    od1 = OptionDescription('tiramisu', '', [descr1])
    cfg_ori = Config(od1)
    cfg = get_config(cfg_ori, config_type)
    assert cfg.option('tiramisu.symdummy').owner.isdefault()
    cfg.option('tiramisu.dummy').value.set(True)
    assert not cfg.option('tiramisu.symdummy').owner.isdefault()
    if config_type == 'tiramisu-api':
        cfg.send()
    with pytest.raises(ConfigError):
        cfg_ori.option('tiramisu.symdummy').owner.set('user')
#    assert not list_sessions()


def test_owner_leadership(config_type):
    b = IntOption('int', 'Test int option', default=[0], multi=True)
    c = StrOption('str', 'Test string option', multi=True)
    descr = Leadership("int", "", [b, c])
    od1 = OptionDescription('od', '', [descr])
    cfg_ori = Config(od1)
    with pytest.raises(ConfigError):
        cfg_ori.option('int.str', 0).owner.set('user')
    cfg = get_config(cfg_ori, config_type)

    cfg.option('int.int').value.set([0, 1])
    cfg.option('int.str', 0).value.set('yes')
    assert not cfg.option('int.str', 0).owner.isdefault()
    assert cfg.option('int.str', 1).owner.isdefault()
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.option('int.str', 0).owner.set('user')
    cfg = get_config(cfg_ori, config_type)
    assert cfg.option('int.str', 0).owner.get() == owners.user
    assert cfg.option('int.str', 1).owner.isdefault()
    assert cfg.option('int.str', 0).value.get() == 'yes'
    assert cfg.option('int.str', 1).value.get() == None
#    assert not list_sessions()
