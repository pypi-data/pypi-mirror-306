# coding: utf-8
from .autopath import do_autopath
do_autopath()
from .config import parse_od_get
# FIXME from .config import config_type, get_config

import pytest
from tiramisu import Config
from tiramisu import IntOption, StrOption, OptionDescription, DynOptionDescription, PasswordOption, UsernameOption, \
                     SymLinkOption, Leadership, Calculation, Params, \
                     ParamOption, ParamValue, ParamIndex, calc_value
from tiramisu.error import PropertiesOptionError, ConfigError
from tiramisu.setting import groups


#def teardown_function(function):
#    assert list_sessions() == [], 'session list is not empty when leaving "{}"'.format(function.__name__)
def is_mandatory(variable):
    return True


def make_description():
    stro = StrOption('str', '')
    subdescr = OptionDescription('sub', '', [stro], properties=('disabled',))
    stroption = StrOption('str', 'Test string option', default="abc",
                          properties=('mandatory', ))
    stroption1 = StrOption('str1', 'Test string option',
                           properties=('mandatory', ))
    stroption2 = StrOption('unicode2', 'Test string option',
                               properties=('mandatory', ))
    stroption3 = StrOption('str3', 'Test string option', multi=True,
                           properties=('mandatory', ))
    descr = OptionDescription('tiram', '', [subdescr, stroption, stroption1, stroption2, stroption3])
    return descr


def return_value(value):
    return value


def make_description2():
    stroption = StrOption('str', 'str', default="abc",
                          properties=('mandatory', ))
    stroption1 = StrOption('str1', 'str1',
                           properties=('mandatory', ))
    stroption2 = SymLinkOption('unicode2', stroption1)
    stroption3 = StrOption('str3', 'str3', multi=True,
                           properties=('mandatory', ))
    unicode1 = StrOption('unicode1', 'unicode1', Calculation(return_value, Params(ParamOption(stroption))), properties=('mandatory',))
    descr = OptionDescription('tiram', '', [stroption, stroption1, stroption2, stroption3, unicode1])
    return descr


def make_description3():
    stroption = StrOption('str', 'Test string option', default="abc",
                          properties=('mandatory', ))
    stroption1 = StrOption('str1', 'Test string option',
                           properties=('mandatory', ))
    stroption2 = SymLinkOption('unicode2', stroption1)
    stroption3 = StrOption('str3', 'Test string option', multi=True,
                           properties=('mandatory', ))
    unicode1 = StrOption('unicode1', 'Test string option', callback=return_value, callback_params=Params(ParamOption(stroption)),  properties=('mandatory', ))
    int1 = IntOption('int1', '', callback=return_value, callback_params=Params(ParamOption(stroption)),  properties=('mandatory', ))
    descr = OptionDescription('tiram', '', [stroption, stroption1, stroption2, stroption3, unicode1, int1])
    return descr


def test_mandatory_ro():
    od1 = make_description()
    cfg = Config(od1) 
    cfg.property.read_only()
    prop = []
    try:
        cfg.option('str1').value.get()
    except PropertiesOptionError as err:
        prop = err.proptype
    assert 'mandatory' in prop
    cfg.property.read_write()
    cfg.option('str1').value.set('yes')
    cfg.property.read_only()
    assert cfg.option('str1').value.get() == 'yes'
#    assert not list_sessions()


def test_mandatory_ro_dict():
    od1 = make_description()
    cfg = Config(od1) 
    cfg.property.read_only()
    prop = []
    try:
        cfg.value.get()
    except PropertiesOptionError as err:
        prop = err.proptype
    assert 'mandatory' in prop
    cfg.property.read_write()
    cfg.option('str1').value.set('yes')
    cfg.option('unicode2').value.set('yes')
    cfg.property.read_only()
    try:
        cfg.value.get()
    except PropertiesOptionError as err:
        prop = err.proptype
    assert 'mandatory' in prop
    cfg.property.read_write()
    cfg.option('str3').value.set(['yes'])
    cfg.property.read_only()
    assert parse_od_get(cfg.value.get()) == {'str': 'abc', 'str1': 'yes', 'str3': ['yes'], 'unicode2': 'yes'}
#    assert not list_sessions()


def test_mandatory_rw():
    od1 = make_description()
    cfg = Config(od1) 
    cfg.property.read_write()
    # not mandatory in rw
    cfg.option('str1').value.get()
    cfg.option('str1').value.set('yes')
    assert cfg.option('str1').value.get() == 'yes'
#    assert not list_sessions()


def test_mandatory_default():
    od1 = make_description()
    cfg = Config(od1) 
    cfg.property.read_only()
    #not mandatory in rw
    cfg.option('str').value.get()
    cfg.property.read_write()
    cfg.option('str').value.set('yes')
    cfg.property.read_only()
    cfg.option('str').value.get()
    cfg.property.read_write()
    cfg.option('str').value.set(None)
    cfg.property.read_only()
    prop = []
    try:
        cfg.option('str').value.get()
    except PropertiesOptionError as err:
        prop = err.proptype
    assert 'mandatory' in prop
#    assert not list_sessions()


def test_mandatory_delete():
    od1 = make_description()
    cfg = Config(od1) 
    cfg.property.read_only()
    cfg.option('str').value.get()
    try:
        cfg.option('str1').value.get()
    except PropertiesOptionError as err:
        prop = err.proptype
    assert 'mandatory' in prop
    cfg.property.read_write()
    cfg.option('str1').value.set('yes')
    cfg.property.read_only()
    assert cfg.option('str1').value.get() == 'yes'
    cfg.property.remove('everything_frozen')
    prop = []
    try:
        cfg.option('str1').value.reset()
    except PropertiesOptionError as err:
        prop = err.proptype
    assert 'mandatory' in prop
    cfg.option('str').value.reset()

    assert cfg.option('str1').value.get() == 'yes'
#    assert not list_sessions()


#valeur vide : None, '', u'', ...
def test_mandatory_none():
    od1 = make_description()
    cfg = Config(od1) 
    cfg.option('str1').value.set(None)
    assert cfg.option('str1').owner.get() == 'user'
    cfg.property.read_only()
    prop = []
    try:
        cfg.option('str1').value.get()
    except PropertiesOptionError as err:
        prop = err.proptype
    assert 'mandatory' in prop
#    assert not list_sessions()


def test_mandatory_empty():
    od1 = make_description()
    cfg = Config(od1) 
    cfg.option('str1').value.set('')
    assert cfg.option('str1').owner.get() == 'user'
    cfg.property.read_only()
    prop = []
    try:
        cfg.option('str1').value.get()
    except PropertiesOptionError as err:
        prop = err.proptype
    assert 'mandatory' in prop
#    assert not list_sessions()


def test_mandatory_multi_none():
    od1 = make_description()
    cfg = Config(od1) 
    cfg.option('str3').value.set([None])
    assert cfg.option('str3').owner.get() == 'user'
    cfg.property.read_only()
    prop = []
    try:
        cfg.option('str3').value.get()
    except PropertiesOptionError as err:
        prop = err.proptype
    assert 'mandatory' in prop
    cfg.property.read_write()
    cfg.option('str3').value.set(['yes', None])
    assert cfg.option('str3').owner.get() == 'user'
    cfg.property.read_only()
    prop = []
    try:
        cfg.option('str3').value.get()
    except PropertiesOptionError as err:
        prop = err.proptype
    assert 'mandatory' in prop
#    assert not list_sessions()


def test_mandatory_multi_empty():
    od1 = make_description()
    cfg = Config(od1) 
    cfg.option('str3').value.set([])
    assert cfg.option('str3').owner.get() == 'user'
    cfg.property.read_only()
    prop = []
    try:
        cfg.option('str3').value.get()
    except PropertiesOptionError as err:
        prop = err.proptype
    assert 'mandatory' in prop
    #
    cfg.property.read_write()
    cfg.option('str3').value.set([''])
    assert cfg.option('str3').owner.get() == 'user'
    cfg.property.read_only()
    prop = []
    try:
        cfg.option('str3').value.get()
    except PropertiesOptionError as err:
        prop = err.proptype
    assert 'mandatory' in prop
    #
    cfg.property.read_write()
    cfg.option('str3').value.set(['yes', ''])
    assert cfg.option('str3').owner.get() == 'user'
    cfg.property.read_only()
    prop = []
    try:
        cfg.option('str3').value.get()
    except PropertiesOptionError as err:
        prop = err.proptype
    assert 'mandatory' in prop
#    assert not list_sessions()


def test_mandatory_multi_append():
    od1 = make_description()
    cfg = Config(od1) 
    cfg.option('str3').value.set(['yes'])
    cfg.property.read_write()
    ret = cfg.option('str3').value.get()
    ret.append(None)
#    assert not list_sessions()


def test_mandatory_disabled():
    od1 = make_description()
    cfg = Config(od1) 
    cfg.option('str1').value.get()
    cfg.option('str1').property.add('disabled')
    cfg.property.read_only()
    pop = []
    try:
        cfg.option('str1').value.get()
    except PropertiesOptionError as err:
        prop = err.proptype
    search_prop = {'disabled'}
    assert set(prop) == search_prop
#    assert not list_sessions()


def test_mandatory_unicode():
    od1 = make_description()
    cfg = Config(od1) 
    cfg.option('unicode2').value.get()
    cfg.property.read_only()
    prop = []
    try:
        cfg.option('unicode2').value.get()
    except PropertiesOptionError as err:
        prop = err.proptype
    assert 'mandatory' in prop
    cfg.property.read_write()
    cfg.option('unicode2').value.set(u'')
    cfg.property.read_only()
    prop = []
    try:
        cfg.option('unicode2').value.get()
    except PropertiesOptionError as err:
        prop = err.proptype
    assert 'mandatory' in prop
#    assert not list_sessions()


def compare(ret, expected):
    assert(len(ret) == len(expected))
    for index, opt in enumerate(ret):
        exp = expected[index]
        if isinstance(exp, list):
            assert opt.path() == exp[0]
            assert opt.index() == exp[1]
        else:
            assert opt.path() == exp
            assert opt.index() == None


def test_mandatory_warnings_ro():
    od1 = make_description()
    cfg = Config(od1) 
    cfg.option('str').value.set('')
    cfg.property.read_only()
    proc = []
    try:
        cfg.option('str').value.get()
    except PropertiesOptionError as err:
        prop = err.proptype
    assert 'mandatory' in prop
    compare(cfg.value.mandatory(), ['str', 'str1', 'unicode2', 'str3'])
    cfg.property.read_write()
    cfg.option('str').value.set('a')
    cfg.property.read_only()
    compare(cfg.value.mandatory(), ['str1', 'unicode2', 'str3'])
#    assert not list_sessions()


def test_mandatory_warnings_rw():
    od1 = make_description()
    cfg = Config(od1) 
    cfg.option('str').value.set('')
    cfg.property.read_write()
    cfg.option('str').value.get()
    compare(cfg.value.mandatory(), ['str', 'str1', 'unicode2', 'str3'])
    cfg.option('str').value.set('a')
    compare(cfg.value.mandatory(), ['str1', 'unicode2', 'str3'])
#    assert not list_sessions()


def test_mandatory_warnings_disabled():
    od1 = make_description()
    cfg = Config(od1) 
    cfg.option('str').value.set('')
    cfg.property.read_write()
    cfg.option('str').value.get()
    compare(cfg.value.mandatory(), ['str', 'str1', 'unicode2', 'str3'])
    cfg.option('str').property.add('disabled')
    compare(cfg.value.mandatory(), ['str1', 'unicode2', 'str3'])
#    assert not list_sessions()


def test_mandatory_warnings_hidden():
    od1 = make_description()
    cfg = Config(od1) 
    cfg.option('str').value.set('')
    cfg.property.read_write()
    cfg.permissive.add('hidden')
    cfg.option('str').value.get()
    compare(cfg.value.mandatory(), ['str', 'str1', 'unicode2', 'str3'])
    cfg.option('str').property.add('hidden')
    compare(cfg.value.mandatory(), ['str', 'str1', 'unicode2', 'str3'])
#    assert not list_sessions()


def test_mandatory_warnings_frozen():
    od1 = make_description()
    cfg = Config(od1) 
    cfg.option('str').value.set('')
    cfg.property.read_write()
    cfg.option('str').value.get()
    compare(cfg.value.mandatory(), ['str', 'str1', 'unicode2', 'str3'])
    cfg.option('str').property.add('frozen')
    cfg.property.read_only()
    compare(cfg.value.mandatory(), ['str', 'str1', 'unicode2', 'str3'])
#    assert not list_sessions()


def test_mandatory_leader():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True,
                              properties=('mandatory', ))
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau",
                                   multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('o', '', [interface1])
    cfg = Config(od1) 
    cfg.property.read_only()
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_admin_eth0.ip_admin_eth0').value.get()
    with pytest.raises(PropertiesOptionError):
        cfg.value.get()
#    assert not list_sessions()


def test_mandatory_leader_sub():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True,
                              properties=('mandatory', ))
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau",
                                   multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('o', '', [interface1])
    od2 = OptionDescription('o', '', [od1])
    cfg = Config(od2)
    cfg.property.read_only()
    with pytest.raises(PropertiesOptionError):
        cfg.option('o.ip_admin_eth0.ip_admin_eth0').value.get()
    with pytest.raises(PropertiesOptionError):
        cfg.value.get()
#    assert not list_sessions()


def test_mandatory_warnings_leader():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True,
                              properties=('mandatory', ))
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau",
                                   multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('o', '', [interface1])
    cfg = Config(od1) 
    compare(cfg.value.mandatory(), ['ip_admin_eth0.ip_admin_eth0'])
#    assert not list_sessions()


def test_mandatory_leader_empty():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau",
                                   multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('o', '', [interface1])
    cfg = Config(od1) 
    cfg.property.read_write()
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
    #
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set([None])
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == [None]
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == None
    cfg.property.read_only()
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_admin_eth0.ip_admin_eth0').value.get()
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get()
    cfg.property.read_write()
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.reset()
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
    #
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set([''])
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['']
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == None
    cfg.property.read_only()
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_admin_eth0.ip_admin_eth0').value.get()
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get()
    cfg.property.read_write()
    #
    cfg.property.read_write()
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['ip'])
    cfg.property.read_only()
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['ip']
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == None
    #
    cfg.property.read_write()
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['ip2'])
    cfg.property.read_only()
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_admin_eth0.ip_admin_eth0').value.reset()
    cfg.property.read_write()
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.reset()
#    assert not list_sessions()


def test_mandatory_warnings_leader_empty():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau",
                                   multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('o', '', [interface1])
    cfg = Config(od1) 
    cfg.property.read_write()
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set([None])
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == [None]
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == None
    compare(cfg.value.mandatory(), ['ip_admin_eth0.ip_admin_eth0'])
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.reset()
    #
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set([''])
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['']
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == None
    compare(cfg.value.mandatory(), ['ip_admin_eth0.ip_admin_eth0'])
    #
    cfg.property.read_write()
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['ip'])
    compare(cfg.value.mandatory(), [])
#    assert not list_sessions()


def test_mandatory_follower():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau",
                                   multi=True, properties=('mandatory', ))
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('o', '', [interface1])
    cfg = Config(od1) 
    cfg.property.read_only()
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
    assert parse_od_get(cfg.value.get()) == {'ip_admin_eth0.ip_admin_eth0': []}
    #
    cfg.property.read_write()
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['ip'])
    cfg.property.read_only()
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['ip']
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get()
    #
    cfg.property.read_write()
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('')
    cfg.property.read_only()
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['ip']
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get()
    #
    cfg.property.read_write()
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('ip')
    cfg.property.read_only()
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['ip']
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == 'ip'
    assert parse_od_get(cfg.value.get()) == {'ip_admin_eth0.ip_admin_eth0': [{'ip_admin_eth0.ip_admin_eth0': 'ip', 'ip_admin_eth0.netmask_admin_eth0': 'ip'}]}
#    assert not list_sessions()


def test_mandatory_warnings_follower():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau",
                                   multi=True, properties=('mandatory', ))
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('o', '', [interface1])
    cfg = Config(od1) 
    cfg.property.read_only()
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
    #
    cfg.property.read_write()
    compare(cfg.value.mandatory(), [])
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['ip'])
    compare(cfg.value.mandatory(), [['ip_admin_eth0.netmask_admin_eth0', 0]])
#    assert not list_sessions()


def test_mandatory_warnings_symlink():
    stroption = StrOption('str', 'Test string option', default="abc",
                          properties=('mandatory', ))
    stroption1 = StrOption('str1', 'Test string option',
                           properties=('mandatory', ))
    stroption2 = SymLinkOption('unicode2', stroption1)
    stroption3 = StrOption('str3', 'Test string option', multi=True,
                           properties=('mandatory', ))
    od1 = OptionDescription('tiram', '', [stroption, stroption1, stroption2, stroption3])
    cfg = Config(od1) 
    cfg.option('str').value.set('')
    cfg.property.read_write()
    cfg.option('str').value.get()
    compare(cfg.value.mandatory(), ['str', 'str1', 'str3'])
    cfg.option('str').property.add('frozen')
    cfg.property.read_only()
    compare(cfg.value.mandatory(), ['str', 'str1', 'str3'])
#    assert not list_sessions()


def test_mandatory_warnings_validate_empty():
    od1 = make_description2()
    cfg = Config(od1) 
    cfg.option('str').value.set('')
    cfg.property.read_only()
    compare(cfg.value.mandatory(), ['str', 'str1', 'str3', 'unicode1'])
#    assert not list_sessions()


def test_mandatory_warnings_requires():
    stroption = StrOption('str', 'Test string option', default="abc",
                          properties=('mandatory', ))
    stroption1 = StrOption('str1', 'Test string option',
                           properties=('mandatory', ))
    stroption2 = StrOption('unicode2', 'Test string option',
                               properties=('mandatory', ))
    mandatory_property = Calculation(calc_value,
                                     Params(ParamValue('mandatory'),
                                            kwargs={'condition': ParamOption(stroption, notraisepropertyerror=True),
                                                    'expected': ParamValue('yes'),
                                                    'no_condition_is_invalid': ParamValue(True)}))
    stroption3 = StrOption('str3', 'Test string option', multi=True, properties=(mandatory_property,))
    od1 = OptionDescription('tiram', '', [stroption, stroption1, stroption2, stroption3])
    cfg = Config(od1) 
    cfg.option('str').value.set('')
    cfg.property.read_write()
    cfg.option('str').value.get()
    compare(cfg.value.mandatory(), ['str', 'str1', 'unicode2'])
    cfg.property.read_only()
    compare(cfg.value.mandatory(), ['str', 'str1', 'unicode2'])
    cfg.property.read_write()
    cfg.option('str').value.set('yes')
    compare(cfg.value.mandatory(), ['str1', 'unicode2', 'str3'])
#    assert not list_sessions()


def test_mandatory_warnings_requires_leadership():
    stroption = StrOption('str', 'Test string option', default="abc",
                          properties=('mandatory', ))
    stroption1 = StrOption('str1', 'Test string option', multi=True)
    mandatory_property = Calculation(calc_value,
                                     Params(ParamValue(None),
                                            kwargs={'condition': ParamOption(stroption),
                                                    'expected': ParamValue('yes'),
                                                    'reverse_condition': ParamValue(True),
                                                    'default': ParamValue('mandatory')}))
    stroption2 = StrOption('str2', 'Test string option', multi=True, properties=(mandatory_property,))
    leadership = Leadership('leader', 'leadership', [stroption1, stroption2])
    od1 = OptionDescription('tiram', '', [stroption, leadership])
    cfg = Config(od1) 
    cfg.option('str').value.set('')
    cfg.option('leader.str1').value.set(['str'])
    compare(cfg.value.mandatory(), ['str'])
    cfg.option('str').value.set('yes')
    compare(cfg.value.mandatory(), [['leader.str2', 0]])
#    assert not list_sessions()


def test_mandatory_warnings_requires_leadership_follower():
    stroption = StrOption('str', 'Test string option', multi=True)
    stroption1 = StrOption('str1', 'Test string option', multi=True)
    mandatory_property = Calculation(calc_value,
                                     Params(ParamValue(None),
                                            kwargs={'condition': ParamOption(stroption1),
                                                    'expected': ParamValue('yes'),
                                                    'reverse_condition': ParamValue(True),
                                                    'default': ParamValue('mandatory')}))
    stroption2 = StrOption('str2', 'Test string option', multi=True, properties=(mandatory_property,))
    leadership = Leadership('leader', 'leadership', [stroption, stroption1, stroption2])
    od1 = OptionDescription('tiram', '', [leadership])
    cfg = Config(od1) 
    cfg.option('leader.str').value.set(['str'])
    compare(cfg.value.mandatory(), [])
    cfg.option('leader.str1', 0).value.set('yes')
    compare(cfg.value.mandatory(), [['leader.str2', 0]])
    cfg.option('leader.str2', 0).value.set('yes')
    compare(cfg.value.mandatory(), [])
    #
    cfg.option('leader.str').value.set(['str', 'str1'])
    compare(cfg.value.mandatory(), [])
    cfg.option('leader.str1', 1).value.set('yes')
    compare(cfg.value.mandatory(), [['leader.str2', 1]])
    cfg.option('leader.str2', 1).value.set('yes')
    compare(cfg.value.mandatory(), [])
    cfg.option('leader.str2', 0).value.reset()
    cfg.option('leader.str2', 1).value.reset()
    compare(cfg.value.mandatory(), [['leader.str2', 0], ['leader.str2', 1]])
#    assert not list_sessions()


def test_mandatory_od_disabled():
    descr = make_description()
    od1 = OptionDescription('od', '', [descr])
    cfg = Config(od1) 
    cfg.property.read_only()
    compare(cfg.value.mandatory(), ['tiram.str1', 'tiram.unicode2', 'tiram.str3'])
    cfg.option('tiram').property.add('disabled')
    compare(cfg.value.mandatory(), [])
#    assert not list_sessions()


def return_list(val=None, identifier=None):
    if val:
        return val
    else:
        return ['val1', 'val2']


#def test_mandatory_dyndescription():
#    st = StrOption('st', '', properties=('mandatory',))
#    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list))
#    od = OptionDescription('od', '', [dod])
#    od2 = OptionDescription('od', '', [od])
#    cfg = Config(od2)
#    cfg.property.read_only()
#    compare(cfg.value.mandatory(), ['od.dodval1.st', 'od.dodval2.st'])
#
#
#def test_mandatory_dyndescription_context():
#    val1 = StrOption('val1', '', ['val1', 'val2'], multi=True)
#    st = StrOption('st', '', properties=('mandatory',))
#    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list, Params(ParamOption(val1))))
#    od = OptionDescription('od', '', [dod, val1])
#    od2 = OptionDescription('od', '', [od])
#    cfg = Config(od2)
#    cfg.property.read_only()
#    compare(cfg.value.mandatory(), ['od.dodval1.st', 'od.dodval2.st'])


def test_mandatory_callback_leader_and_followers_leader():
    val1 = StrOption('val1', "", multi=True, properties=('mandatory', 'empty'))
    val2 = StrOption('val2', "", multi=True, default_multi='val2', properties=('expert',))
    val3 = StrOption('val3', "", Calculation(calc_value, Params(ParamOption(val2), {'index': ParamIndex()})), multi=True)
    val4 = StrOption('val4', "", Calculation(calc_value, Params(ParamOption(val3), {'index': ParamIndex()})), multi=True)
    interface1 = Leadership('val1', '', [val1, val2, val3, val4])
    od1 = OptionDescription('rootconfig', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    # FIXME cfg = get_config(cfg, config_type)
    compare(cfg.value.mandatory(), ['val1.val1'])
#    assert not list_sessions()


def test_mandatory_and_disabled():
    password = PasswordOption(name="password", doc="Password", properties=frozenset({"disabled"}))
    username = UsernameOption(name="username", doc="Username", properties=frozenset({"normal", Calculation(is_mandatory, Params((ParamOption(password)))), "disabled"}))
    od1 = OptionDescription('rootconfig', '', [username, password])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.value.get()
