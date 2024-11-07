"configuration objects global API"
from pytest import raises

from .autopath import do_autopath
do_autopath()
from .config import config_type, get_config, value_list, global_owner, parse_od_get

from tiramisu import Config, IntOption, FloatOption, StrOption, ChoiceOption, \
    BoolOption, FilenameOption, SymLinkOption, IPOption, \
    PortOption, NetworkOption, NetmaskOption, BroadcastOption, \
    DomainnameOption, OptionDescription
from tiramisu.error import PropertiesOptionError, ValueWarning, ConfigError
import warnings


#def teardown_function(function):
#    # test_od_not_list emit a warnings because of doesn't create a Config
#    with warnings.catch_warnings(record=True) as w:
#        assert list_sessions() == [], 'session list is not empty when leaving "{}"'.format(function.__name__)


def make_description():
    gcoption = ChoiceOption('name', 'GC name', ('ref', 'framework'), 'ref')
    gcdummy = BoolOption('dummy', 'dummy', default=False)
    prop = BoolOption('prop', 'prop 1', properties=('disabled',))
    prop2 = StrOption('prop', 'prop 2', properties=('hidden',))
    objspaceoption = ChoiceOption('objspace', 'Object space',
                                  ('std', 'thunk'), 'std')
    booloption = BoolOption('bool', 'Test boolean option', default=True)
    booloption2 = BoolOption('bool', 'Test boolean option', default=False)
    intoption = IntOption('int', 'Test int option', default=0)
    floatoption2 = FloatOption('float', 'Test float option', default=2.3)
    floatoption = FloatOption('float', 'Test float option', default=2.3)
    stroption = StrOption('str', 'Test string option', default="abc")
    boolop = BoolOption('boolop', 'Test boolean option op', default=True)
    wantref_option = BoolOption('wantref', 'Tests', default=False)
    wantframework_option = BoolOption('wantframework', 'Test', default=False)
    gcgroup2 = OptionDescription('gc2', '', [booloption2, prop])
    gcgroup = OptionDescription('gc', '', [gcgroup2, gcoption, gcdummy, floatoption, prop2])
    descr = OptionDescription('tiramisu', '', [gcgroup, booloption, objspaceoption,
                                               wantref_option, stroption,
                                               wantframework_option,
                                               intoption, boolop, floatoption2])
    return descr


def _is_same_opt(opt1, opt2):
    if "id" in dir(opt1):
        assert opt1.id == opt2.id
    else:
        assert opt1 == opt2


def test_od_not_list():
    b = BoolOption('bool', '', multi=True)
    with raises(AssertionError):
        OptionDescription('od', '', b)
#    assert not list_sessions()


def test_str():
    od1 = make_description()
    cfg = Config(od1)
    cfg  # does not crash
#    assert not list_sessions()


def test_make_dict(config_type):
    "serialization of the whole config to a dict"
    od1 = OptionDescription("opt", "", [
        OptionDescription("s1", "", [
            BoolOption("a", "", default=False),
            BoolOption("b", "", default=False, properties=('hidden',))]),
        IntOption("int", "", default=42)])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.permissive.add('hidden')
    cfg = get_config(cfg, config_type)
    assert parse_od_get(cfg.value.get()) == {"s1.a": False, "int": 42}
    cfg.option('int').value.set(43)
    cfg.option('s1.a').value.set(True)
    assert parse_od_get(cfg.value.get()) == {"s1.a": True, "int": 43}
    if config_type == 'tiramisu':
        assert parse_od_get(cfg.forcepermissive.value.get()) == {"s1.a": True, "s1.b": False, "int": 43}
#    assert not list_sessions()


def test_make_dict_sub(config_type):
    "serialization part of config to a dict"
    od1 = OptionDescription("opt", "", [
        OptionDescription("s1", "", [
            BoolOption("a", "", default=False),
            BoolOption("b", "", default=False, properties=('hidden',))]),
        IntOption("int", "", default=42)])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.permissive.add('hidden')
    cfg = get_config(cfg, config_type)
    assert parse_od_get(cfg.option('s1').value.get()) == {'s1.a': False}


def test_make_dict_with_disabled(config_type):
    od1 = OptionDescription("opt", "", [
        OptionDescription("s1", "", [
            BoolOption("a", "", default=False),
            BoolOption("b", "", default=False, properties=('disabled',))]),
        OptionDescription("s2", "", [
            BoolOption("a", "", default=False),
            BoolOption("b", "", default=False)], properties=('disabled',)),
        IntOption("int", "", default=42)])
    cfg = Config(od1)
    cfg.property.read_only()
    cfg = get_config(cfg, config_type)
    assert parse_od_get(cfg.value.get()) == {"s1.a": False, "int": 42}
    if config_type == 'tiramisu':
        assert parse_od_get(cfg.forcepermissive.value.get()) == {"s1.a": False, "int": 42}
        assert parse_od_get(cfg.unrestraint.value.get()) == {"int": 42, "s1.a": False, "s1.b": False, "s2.a": False, "s2.b": False}
#    assert not list_sessions()


def test_make_dict_with_disabled_in_callback(config_type):
    od1 = OptionDescription("opt", "", [
        OptionDescription("s1", "", [
            BoolOption("a", "", default=False),
            BoolOption("b", "", default=False, properties=('disabled',))]),
        OptionDescription("s2", "", [
            BoolOption("a", "", default=False),
            BoolOption("b", "", default=False)], properties=('disabled',)),
        IntOption("int", "", default=42)])
    cfg = Config(od1)
    cfg.property.read_only()
    cfg = get_config(cfg, config_type)
    assert parse_od_get(cfg.value.get()) == {"s1.a": False, "int": 42}
#    assert not list_sessions()


def test_make_dict_fullpath(config_type):
    od1 = OptionDescription("root", "", [
        OptionDescription("opt", "", [
            OptionDescription("s1", "", [
                BoolOption("a", "", default=False),
                BoolOption("b", "", default=False, properties=('disabled',))]),
            OptionDescription("s2", "", [
                BoolOption("a", "", default=False),
                BoolOption("b", "", default=False)], properties=('disabled',)),
            IntOption("int", "", default=42)]),
        IntOption("introot", "", default=42)])
    cfg = Config(od1)
    cfg.property.read_only()
    cfg = get_config(cfg, config_type)
    assert parse_od_get(cfg.value.get()) == {"opt.s1.a": False, "opt.int": 42, "introot": 42}
    assert parse_od_get(cfg.option('opt').value.get()) == {"opt.s1.a": False, "opt.int": 42}
#    assert not list_sessions()


#def test_find_in_config():
#    "finds option in config"
#    od1 = make_description()
#    cfg = Config(od1)
#    cfg.property.read_only()
#    cfg.permissive.add('hidden')
#    ret = list(cfg.option.find('dummy'))
#    assert len(ret) == 1
#    _is_same_opt(ret[0].get(), cfg.option('gc.dummy').get())
#    #
#    ret_find = cfg.option.find('dummy', first=True)
#    ret = ret_find.get()
#    _is_same_opt(ret, cfg.option('gc.dummy').get())
#    #
#    ret = list(cfg.option.find('float'))
#    assert len(ret) == 2
#    _is_same_opt(ret[0].get(), cfg.option('gc.float').get())
#    _is_same_opt(ret[1].get(), cfg.option('float').get())
#    #
#    ret = cfg.option.find('bool', first=True)
#    _is_same_opt(ret.get(), cfg.option('gc.gc2.bool').get())
#    ret = cfg.option.find('bool', value=True, first=True)
#    _is_same_opt(ret.get(), cfg.option('bool').get())
#    ret = cfg.option.find('dummy', first=True)
#    _is_same_opt(ret.get(), cfg.option('gc.dummy').get())
#    ret = cfg.option.find('float', first=True)
#    _is_same_opt(ret.get(), cfg.option('gc.float').get())
#    ret = list(cfg.option.find('prop'))
#    assert len(ret) == 1
#    _is_same_opt(ret[0].get(), cfg.option('gc.prop').get())
#    #
#    ret = list(cfg.option.find('prop', value=None))
#    assert len(ret) == 1
#    ret = list(cfg.option.find('prop'))
#    assert len(ret) == 1
#    _is_same_opt(ret[0].get(), cfg.option('gc.prop').get())
#    #
#    cfg.property.read_write()
#    with raises(AttributeError):
#        ret = cfg.option.find('prop')
#        assert ret.get()
#    ret = list(cfg.unrestraint.option.find(name='prop'))
#    assert len(ret) == 2
#    _is_same_opt(ret[0].get(), cfg.unrestraint.option('gc.gc2.prop').get())
#    _is_same_opt(ret[1].get(), cfg.forcepermissive.option('gc.prop').get())
#    #
#    ret = list(cfg.forcepermissive.option.find('prop'))
#    assert len(ret) == 1
#    _is_same_opt(ret[0].get(), cfg.forcepermissive.option('gc.prop').get())
#    #
#    ret = cfg.forcepermissive.option.find('prop', first=True)
#    _is_same_opt(ret.get(), cfg.forcepermissive.option('gc.prop').get())
#    # combinaison of filters
#    ret = list(cfg.unrestraint.option.find('prop', type=BoolOption))
#    assert len(ret) == 1
#    _is_same_opt(ret[0].get(), cfg.unrestraint.option('gc.gc2.prop').get())
#    ret = cfg.unrestraint.option.find('prop', type=BoolOption, first=True)
#    _is_same_opt(ret.get(), cfg.unrestraint.option('gc.gc2.prop').get())
#    #
#    ret = list(cfg.option.find('dummy', value=False))
#    assert len(ret) == 1
#    _is_same_opt(ret[0].get(), cfg.option('gc.dummy').get())
#    #
#    ret = cfg.option.find('dummy', value=False, first=True)
#    _is_same_opt(ret.get(), cfg.option('gc.dummy').get())
#    #subcfgig
#    ret = list(cfg.option('gc').find('dummy'))
#    assert len(ret) == 1
#    _is_same_opt(ret[0].get(), cfg.option('gc.dummy').get())
#    #
#    ret = list(cfg.option('gc').find('float'))
#    assert len(ret) == 1
#    _is_same_opt(ret[0].get(), cfg.option('gc.float').get())
#    #
#    ret = list(cfg.option('gc.gc2').find('bool'))
#    assert len(ret) == 1
#    _is_same_opt(ret[0].get(), cfg.option('gc.gc2.bool').get())
#    ret = cfg.option('gc').find('bool', value=False, first=True)
#    _is_same_opt(ret.get(), cfg.option('gc.gc2.bool').get())
#    #
#    with raises(AttributeError):
#        ret = cfg.option('gc').find('bool', value=True, first=True)
#        assert ret.get()
#    #
#    with raises(AttributeError):
#        ret = cfg.option('gc').find('wantref')
#        ret.get()
#    #
#    ret = list(cfg.unrestraint.option('gc').find('prop'))
#    assert len(ret) == 2
#    _is_same_opt(ret[0].get(), cfg.unrestraint.option('gc.gc2.prop').get())
#    _is_same_opt(ret[1].get(), cfg.forcepermissive.option('gc.prop').get())
#    #
#    cfg.property.read_only()
#    ret = list(cfg.option('gc').find('prop'))
#    assert len(ret) == 1
#    _is_same_opt(ret[0].get(), cfg.option('gc.prop').get())
#    # not OptionDescription
#    with raises(AttributeError):
#        cfg.option.find('gc', first=True)
#    with raises(AttributeError):
#        cfg.option.find('gc2', first=True)
##    assert not list_sessions()
#
#
#def test_find_multi():
#    b = BoolOption('bool', '', multi=True, properties=('notunique',))
#    od1 = OptionDescription('od', '', [b])
#    cfg = Config(od1)
#    #
#    with raises(AttributeError):
#        list(cfg.option.find('bool', value=True))
#    with raises(AttributeError):
#        list(cfg.option.find('bool', value=True, first=True))
#    cfg.option('bool').value.set([False])
#    with raises(AttributeError):
#        list(cfg.option.find('bool', value=True))
#    with raises(AttributeError):
#        list(cfg.option.find('bool', value=True, first=True))
#    cfg.option('bool').value.set([False, False])
#    with raises(AttributeError):
#        list(cfg.option.find('bool', value=True))
#    with raises(AttributeError):
#        list(cfg.option.find('bool', value=True, first=True))
#    cfg.option('bool').value.set([False, False, True])
#    ret = list(cfg.option.find('bool', value=True))
#    assert len(ret) == 1
#    _is_same_opt(ret[0].get(), b)
#    ret = cfg.option.find('bool', value=True, first=True)
#    _is_same_opt(ret.get(), b)
##    assert not list_sessions()
#
#
#def test_does_not_find_in_config():
#    od1 = make_description()
#    cfg = Config(od1)
#    with raises(AttributeError):
#        list(cfg.option.find('IDontExist'))
##    assert not list_sessions()


def test_filename(config_type):
    a = FilenameOption('a', '')
    od1 = OptionDescription('o', '', [a])
    cfg = Config(od1)
    # FIXME cfg = get_config(cfg, config_type)
    cfg.option('a').value.set('/')
    cfg.option('a').value.set('/tmp')
    cfg.option('a').value.set('/tmp/')
    cfg.option('a').value.set('/tmp/text.txt')
    cfg.option('a').value.set('/tmp/with space.txt')
    cfg.option('a').value.set('/tmp/with$.txt')
    with raises(ValueError):
        cfg.option('a').value.set('not starts with /')
#    assert not list_sessions()


def test_invalid_option():
    ChoiceOption('a', '', ('1', '2'))
    with raises(TypeError):
        ChoiceOption('a', '', [1, 2])
    with raises(TypeError):
        ChoiceOption('a', '', 1)
    with raises(ValueError):
        ChoiceOption('a', '', (1,), 3)
    FloatOption('a', '')
    with raises(ValueError):
        FloatOption('a', '', 'string')
    StrOption('a', '')
    with raises(ValueError):
        StrOption('a', '', 1)
    u = StrOption('a', '')
    SymLinkOption('a', u)
    with raises(ValueError):
        SymLinkOption('a', 'string')
    IPOption('a', '')
    with raises(ValueError):
        IPOption('a', '', 1)
    with raises(ValueError):
        IPOption('a', '', 'string')
    PortOption('a', '')
    with raises(ValueError):
        PortOption('a', '', 'string')
    with raises(ValueError):
        PortOption('a', '', '11:12:13', allow_range=True)
    with raises(ValueError):
        PortOption('a', '', 11111111111111111111)
    with raises(ValueError):
        PortOption('a', '', allow_zero=True, allow_wellknown=False, allow_registred=True, allow_private=False)
    with raises(ValueError):
        PortOption('a', '', allow_zero=True, allow_wellknown=True, allow_registred=False, allow_private=True)
    with raises(ValueError):
        PortOption('a', '', allow_zero=True, allow_wellknown=False, allow_registred=False, allow_private=True)
    with raises(ValueError):
        PortOption('a', '', allow_zero=True, allow_wellknown=False, allow_registred=True, allow_private=True)
    with raises(ValueError):
        PortOption('a', '', allow_zero=False, allow_wellknown=False, allow_registred=False, allow_private=False)
    with raises(ValueError):
        PortOption('a', '', 'tcp:80')
    NetworkOption('a', '')
    with raises(ValueError):
        NetworkOption('a', '', 'string')
    NetmaskOption('a', '')
    with raises(ValueError):
        NetmaskOption('a', '', 'string')
    BroadcastOption('a', '')
    with raises(ValueError):
        BroadcastOption('a', '', 'string')
    DomainnameOption('a', '')
    with raises(ValueError):
        DomainnameOption('a', '', 'string')
    with raises(ValueError):
        DomainnameOption('a', '', type='string')
    with raises(ValueError):
        DomainnameOption('a', '', allow_ip='string')
    with raises(ValueError):
        DomainnameOption('a', '', allow_without_dot='string')
    with raises(ValueError):
        DomainnameOption('a', '', 1)
    #
    ChoiceOption('a', '', (1,), multi=True, default_multi=1)
    with raises(ValueError):
        ChoiceOption('a', '', (1,), default_multi=1)
    with raises(ValueError):
        ChoiceOption('a', '', (1,), multi=True, default=[1,], default_multi=2)
    with raises(ValueError):
        FloatOption('a', '', multi=True, default_multi='string')
    with raises(ValueError):
        StrOption('a', '', multi=True, default_multi=1)
    with raises(ValueError):
        IPOption('a', '', multi=True, default_multi=1)
    with raises(ValueError):
        IPOption('a', '', multi=True, default_multi='string')
    with raises(ValueError):
        PortOption('a', '', multi=True, default_multi='string')
    with raises(ValueError):
        PortOption('a', '', multi=True, default_multi='11:12:13', allow_range=True)
    with raises(ValueError):
        PortOption('a', '', multi=True, default_multi=11111111111111111111)
    with raises(ValueError):
        NetworkOption('a', '', multi=True, default_multi='string')
    with raises(ValueError):
        NetmaskOption('a', '', multi=True, default_multi='string')
    with raises(ValueError):
        BroadcastOption('a', '', multi=True, default_multi='string')
    with raises(ValueError):
        DomainnameOption('a', '', multi=True, default_multi='string')
    with raises(ValueError):
        DomainnameOption('a', '', multi=True, default_multi=1)
#    assert not list_sessions()


def test_help():
    stro = StrOption('s', '', multi=True)
    od1 = OptionDescription('o', '', [stro])
    od2 = OptionDescription('o', '', [od1])
    cfg = Config(od2)
    cfg.help(_display=False)
    cfg.config.help(_display=False)
    cfg.option('o').help(_display=False)
    cfg.option('o.s').help(_display=False)
#    assert not list_sessions()


def test_config_reset():
    od1 = make_description()
    cfg = Config(od1)
    cfg.owner.set('test')
    assert cfg.owner.get() == 'test'
    assert not cfg.option('gc.gc2.bool').value.get()
    assert not cfg.option('boolop').property.get()
    assert not cfg.option('boolop').permissive.get()
    assert not cfg.option('wantref').information.get('info', None)
    #
    cfg.option('gc.gc2.bool').value.set(True)
    cfg.option('boolop').property.add('test')
    cfg.option('float').permissive.add('test')
    cfg.option('wantref').information.set('info', 'info')
    assert cfg.option('gc.gc2.bool').value.get()
    assert cfg.option('boolop').property.get()
    assert cfg.option('float').permissive.get()
    assert cfg.option('wantref').information.get('info', None)
    #
    assert cfg.owner.get() == 'test'
    cfg.config.reset()
    assert cfg.owner.get() == 'test'
    assert not cfg.option('gc.gc2.bool').value.get()
    assert not cfg.option('boolop').property.get()
    assert not cfg.option('float').permissive.get()
    assert not cfg.option('wantref').information.get('info', None)
#    assert not list_sessions()
