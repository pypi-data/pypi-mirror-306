import pytest
from .autopath import do_autopath
do_autopath()

from tiramisu.setting import groups, owners
from tiramisu import IntOption, StrOption, NetworkOption, NetmaskOption, BoolOption, ChoiceOption, \
                     IPOption, OptionDescription, Leadership, Config, GroupConfig, MetaConfig, \
                     Calculation, Params, ParamOption, ParamValue, calc_value, ParamSelfOption, \
                     valid_network_netmask, valid_not_equal
from tiramisu.error import ConfigError, ConflictError, PropertiesOptionError, LeadershipError
from .config import config_type, get_config


owners.addowner('config')
owners.addowner('meta1')
owners.addowner('meta2')


def return_value(value=None):
    return value


def return_condition(val, condition, expected):
    if condition == expected:
        return val
    return None


def raise_exception():
    raise Exception('test')


def make_description():
    i1 = IntOption('i1', '')
    i2 = IntOption('i2', '', default=1)
    i3 = IntOption('i3', '')
    i4 = IntOption('i4', '', default=2)
    i5 = IntOption('i5', '', default=[2], multi=True)
    i6 = IntOption('i6', '', properties=('disabled',))
    od1 = OptionDescription('od1', '', [i1, i2, i3, i4, i5, i6])
    od2 = OptionDescription('od2', '', [od1])
    return od2


def make_metaconfig(double=False):
    od2 = make_description()
    conf1 = Config(od2, name='conf1')
    conf1.property.read_write()
    conf2 = Config(od2, name='conf2')
    conf2.property.read_write()
    meta = MetaConfig([conf1, conf2], name='meta')
    assert meta.config.type() == 'metaconfig'
    assert meta.config.name() == 'meta'
    if double:
        meta.owner.set(owners.meta2)
        meta = MetaConfig([meta], name='doublemeta')
    meta.property.read_write()
    meta.owner.set(owners.meta1)
    return meta


#def test_unknown_config():
#    meta = make_metaconfig()
#    with pytest.raises(ConfigError):
#        meta.config('unknown')
#
#
#def test_error_metaconfig():
#    od2 = make_description()
#    conf1 = Config(od2, name='conf1')
#    with pytest.raises(TypeError):
#        MetaConfig([GroupConfig([conf1])], name='meta')
#
#
#def test_path():
#    meta = make_metaconfig()
#    assert meta.config.path() == 'meta'
#    ret = meta.config('conf1')
#    assert ret.config.path() == 'meta.conf1'
#    ret = meta.config('conf2')
#    assert ret.config.path() == 'meta.conf2'
#
#
#def test_none():
#    meta = make_metaconfig()
#    conf1 = meta.config('conf1')
#    conf2 = meta.config('conf2')
#    assert meta.option('od1.i3').value.get() is conf1.option('od1.i3').value.get() is conf2.option('od1.i3').value.get() is None
#    assert meta.option('od1.i3').owner.get() is conf1.option('od1.i3').owner.get() is conf2.option('od1.i3').owner.get() is owners.default
#    #
#    assert meta.option('od1.i3').value.set(3) == []
#    assert meta.option('od1.i3').value.get() == conf1.option('od1.i3').value.get() == conf2.option('od1.i3').value.get() == 3
#    assert meta.option('od1.i3').owner.get() is conf1.option('od1.i3').owner.get() is conf2.option('od1.i3').owner.get() is owners.meta1
#    #
#    conf1.option('od1.i3').value.set(2)
#    assert meta.option('od1.i3').value.get() == conf2.option('od1.i3').value.get() == 3
#    assert conf1.option('od1.i3').value.get() == 2
#    assert meta.option('od1.i3').owner.get() is conf2.option('od1.i3').owner.get() is owners.meta1
#    assert conf1.option('od1.i3').owner.get() is owners.user
#    #
#    meta.option('od1.i3').value.set(4)
#    assert meta.option('od1.i3').value.get() == conf2.option('od1.i3').value.get() == 4
#    assert conf1.option('od1.i3').value.get() == 2
#    assert meta.option('od1.i3').owner.get() is conf2.option('od1.i3').owner.get() is owners.meta1
#    assert conf1.option('od1.i3').owner.get() is owners.user
#    #
#    meta.option('od1.i3').value.reset()
#    assert meta.option('od1.i3').value.get() is conf2.option('od1.i3').value.get() is None
#    assert conf1.option('od1.i3').value.get() == 2
#    assert meta.option('od1.i3').owner.get() is conf2.option('od1.i3').owner.get() is owners.default
#    assert conf1.option('od1.i3').owner.get() is owners.user
#    #
#    conf1.option('od1.i3').value.reset()
#    assert meta.option('od1.i3').value.get() is conf1.option('od1.i3').value.get() is conf2.option('od1.i3').value.get() is None
#    assert meta.option('od1.i3').owner.get() is conf1.option('od1.i3').owner.get() is conf2.option('od1.i3').owner.get() is owners.default
#
#
#def test_metaconfig_reset(config_type):
#    meta = make_metaconfig()
#    meta_api = get_config(meta, config_type)
#    assert meta_api.option('od1.i2').value.get() == 1
#    meta_api.option('od1.i2').value.set(2)
#    if config_type == 'tiramisu-api':
#        meta_api.send()
#    conf1 = meta.config('conf1')
#    conf2 = meta.config('conf2')
#    conf1.option('od1.i2').value.set(3)
#    assert meta.option('od1.i2').value.get() == 2
#    assert conf1.option('od1.i2').value.get() == 3
#    assert conf2.option('od1.i2').value.get() == 2
#    meta.config.reset()
#    assert meta.option('od1.i2').value.get() == 1
#    assert conf1.option('od1.i2').value.get() == 3
#    assert conf2.option('od1.i2').value.get() == 1
#
#
#def test_default():
#    meta = make_metaconfig()
#    conf1 = meta.config('conf1')
#    conf2 = meta.config('conf2')
#    assert meta.option('od1.i2').value.get() == conf1.option('od1.i2').value.get() == conf2.option('od1.i2').value.get() == 1
#    assert meta.option('od1.i2').owner.get() is conf1.option('od1.i2').owner.get() is conf2.option('od1.i2').owner.get() is owners.default
#    #
#    meta.option('od1.i2').value.set(3)
#    assert meta.option('od1.i2').value.get() == conf1.option('od1.i2').value.get() == conf2.option('od1.i2').value.get() == 3
#    assert meta.option('od1.i2').owner.get() is conf1.option('od1.i2').owner.get() is conf2.option('od1.i2').owner.get() is owners.meta1
#    #
#    conf1.option('od1.i2').value.set(2)
#    assert meta.option('od1.i2').value.get() == conf2.option('od1.i2').value.get() == 3
#    assert conf1.option('od1.i2').value.get() == 2
#    assert meta.option('od1.i2').owner.get() is conf2.option('od1.i2').owner.get() is owners.meta1
#    assert conf1.option('od1.i2').owner.get() is owners.user
#    #
#    meta.option('od1.i2').value.set(4)
#    assert meta.option('od1.i2').value.get() == conf2.option('od1.i2').value.get() == 4
#    assert conf1.option('od1.i2').value.get() == 2
#    assert meta.option('od1.i2').owner.get() is conf2.option('od1.i2').owner.get() is owners.meta1
#    assert conf1.option('od1.i2').owner.get() is owners.user
#    #
#    meta.option('od1.i2').value.reset()
#    assert meta.option('od1.i2').value.get() == conf2.option('od1.i2').value.get() == 1
#    assert conf1.option('od1.i2').value.get() == 2
#    assert meta.option('od1.i2').owner.get() is conf2.option('od1.i2').owner.get() is owners.default
#    assert conf1.option('od1.i2').owner.get() is owners.user
#    #
#    conf1.option('od1.i2').value.reset()
#    assert meta.option('od1.i2').value.get() == conf1.option('od1.i2').value.get() == conf2.option('od1.i2').value.get() == 1
#    assert meta.option('od1.i2').owner.get() is conf1.option('od1.i2').owner.get() is conf2.option('od1.i2').owner.get() is owners.default
#
#
#def test_contexts():
#    meta = make_metaconfig()
#    errors = meta.value.set('od1.i2', 6, only_config=True)
#    assert len(errors) == 0
#    conf1 = meta.config('conf1')
#    assert meta.option('od1.i2').value.get() == 1
#    assert meta.option('od1.i2').owner.get() == owners.default
#    assert conf1.option('od1.i2').value.get() == conf1.option('od1.i2').value.get() == 6
#    assert conf1.option('od1.i2').owner.get() == conf1.option('od1.i2').owner.get() is owners.user
#
#
#def test_find():
#    meta = make_metaconfig()
#    ret = list(meta.option.find('i2'))
#    assert len(ret) == 1
#    assert 1 == ret[0].value.get()
#    ret = meta.option.find('i2', first=True)
#    assert 1 == ret.value.get()
#    assert meta.value.dict() == {'od1.i4': 2, 'od1.i1': None, 'od1.i3': None,
#                                      'od1.i2': 1, 'od1.i5': [2]}
#
#
#def test_meta_meta():
#    meta = make_metaconfig(double=True)
#    meta1 = meta.config('meta')
#    conf1 = meta.config('meta.conf1')
#    conf2 = meta.config('meta.conf2')
#    assert meta.option('od1.i2').value.get() == meta1.option('od1.i2').value.get() == conf1.option('od1.i2').value.get() == conf2.option('od1.i2').value.get() == 1
#    assert meta.option('od1.i2').owner.get() is meta1.option('od1.i2').owner.get() is conf1.option('od1.i2').owner.get() is conf2.option('od1.i2').owner.get() is owners.default
#    #
#    meta.option('od1.i2').value.set(3)
#    assert meta.option('od1.i2').value.get() == meta1.option('od1.i2').value.get() == conf1.option('od1.i2').value.get() == conf2.option('od1.i2').value.get() == 3
#    assert meta.option('od1.i2').owner.get() is meta1.option('od1.i2').owner.get() is conf1.option('od1.i2').owner.get() is conf2.option('od1.i2').owner.get() is owners.meta1
#    #
#    conf1.option('od1.i2').value.set(2)
#    assert meta.option('od1.i2').value.get() == meta1.option('od1.i2').value.get() == conf2.option('od1.i2').value.get() == 3
#    assert conf1.option('od1.i2').value.get() == 2
#    assert meta.option('od1.i2').owner.get() is meta1.option('od1.i2').owner.get() is conf2.option('od1.i2').owner.get() is owners.meta1
#    assert conf1.option('od1.i2').owner.get() is owners.user
#    #
#    meta1.option('od1.i2').value.set(4)
#    assert meta.option('od1.i2').value.get() == 3
#    assert meta1.option('od1.i2').value.get() == conf2.option('od1.i2').value.get() == 4
#    assert conf1.option('od1.i2').value.get() == 2
#    assert meta.option('od1.i2').owner.get() is owners.meta1
#    assert meta1.option('od1.i2').owner.get() is conf2.option('od1.i2').owner.get() is owners.meta2
#    assert conf1.option('od1.i2').owner.get() is owners.user
#    #
#    meta1.option('od1.i2').value.reset()
#    assert meta.option('od1.i2').value.get() == meta1.option('od1.i2').value.get() == conf2.option('od1.i2').value.get() == 3
#    assert conf1.option('od1.i2').value.get() == 2
#    assert meta.option('od1.i2').owner.get() is meta1.option('od1.i2').owner.get() is conf2.option('od1.i2').owner.get() is owners.meta1
#    assert conf1.option('od1.i2').owner.get() is owners.user
#    #
#    meta.option('od1.i2').value.reset()
#    assert meta.option('od1.i2').value.get() == meta1.option('od1.i2').value.get() == conf2.option('od1.i2').value.get() == 1
#    assert conf1.option('od1.i2').value.get() == 2
#    assert meta.option('od1.i2').owner.get() is meta1.option('od1.i2').owner.get() is conf2.option('od1.i2').owner.get() is owners.default
#    assert conf1.option('od1.i2').owner.get() is owners.user
#    #
#    conf1.option('od1.i2').value.reset()
#    assert meta.option('od1.i2').value.get() == meta1.option('od1.i2').value.get() == conf1.option('od1.i2').value.get() == conf2.option('od1.i2').value.get() == 1
#    assert meta.option('od1.i2').owner.get() is meta1.option('od1.i2').owner.get() is conf1.option('od1.i2').owner.get() is conf2.option('od1.i2').owner.get() is owners.default
#
#
#def test_meta_new_config():
#    od = make_description()
#    meta = MetaConfig(['name1', 'name2'], optiondescription=od)
#    assert len(list(meta.config.list())) == 2
#    meta.config.new('newconf1')
#    assert len(list(meta.config.list())) == 3
#
#
#def test_meta_new_config_owner():
#    od = make_description()
#    meta = MetaConfig(['name1', 'name2'], optiondescription=od)
#    meta.owner.set('meta')
#    meta.config.new('newconf1')
#    assert meta.owner.get() == 'meta'
#
#
#def test_meta_new_metaconfig():
#    od = make_description()
#    meta = MetaConfig(['name1', 'name2'], optiondescription=od)
#    meta.config.new('newconf1', type='metaconfig')
#    newconf1 = meta.config('newconf1')
#    newconf1.config.new('newconf2', type='metaconfig')
#    newconf2 = newconf1.config('newconf2')
#    newconf2.config.new('newconf3')
#    newconf3 = newconf2.config('newconf3')
#    assert newconf3.config.name() == 'newconf3'
#
#
#def test_meta_pop_config():
#    od = make_description()
#    meta = MetaConfig(['name1', 'name2'], optiondescription=od)
#    meta.option('od1.i1').value.set(2)
#    #
#    assert len(list(meta.config.list())) == 2
#    meta.config.new('newconf1')
#    newconf1 = meta.config('newconf1')
#    assert newconf1.value.dict() == {'od1.i1': 2, 'od1.i2': 1, 'od1.i3': None, 'od1.i4': 2, 'od1.i5': [2], 'od1.i6': None}
#    #
#    assert len(list(meta.config.list())) == 3
#    newconf1 = meta.config.remove('newconf1')
#    try:
#        meta.config('newconf1')
#    except ConfigError:
#        pass
#    else:
#        raise Exception('must raise')
#    assert newconf1.value.dict() == {'od1.i1': None, 'od1.i2': 1, 'od1.i3': None, 'od1.i4': 2, 'od1.i5': [2], 'od1.i6': None}
#    #
#    assert len(list(meta.config.list())) == 2
#    with pytest.raises(ConfigError):
#        meta.config.remove('newconf1')
#
#
#def test_meta_add_config():
#    od = make_description()
#    od2 = make_description()
#    meta = MetaConfig(['name1', 'name2'], optiondescription=od)
#    meta.option('od1.i1').value.set(2)
#    #
#    assert len(list(meta.config.list())) == 2
#    config = Config(od, name='new')
#    assert config.value.dict() == {'od1.i1': None, 'od1.i2': 1, 'od1.i3': None, 'od1.i4': 2, 'od1.i5': [2], 'od1.i6': None}
#    meta.config.add(config)
#    #
#    assert len(list(meta.config.list())) == 3
#    assert config.value.dict() == {'od1.i1': 2, 'od1.i2': 1, 'od1.i3': None, 'od1.i4': 2, 'od1.i5': [2], 'od1.i6': None}
#    #
#    with pytest.raises(ConflictError):
#        meta.config.add(config)
#    newconfig = Config(od2)
#    with pytest.raises(ValueError):
#        meta.config.add(newconfig)
#
#
#def test_meta_add_config_not_name():
#    od = make_description()
#    od2 = make_description()
#    meta = MetaConfig(['name1', 'name2'], optiondescription=od)
#    meta.option('od1.i1').value.set(2)
#    #
#    assert len(list(meta.config.list())) == 2
#    config = Config(od)
#    with pytest.raises(ConfigError):
#        meta.config.add(config)
#
#
#def test_meta_add_config_readd():
#    od = make_description()
#    meta = MetaConfig([], optiondescription=od)
#    meta2 = MetaConfig([], optiondescription=od)
#    config = Config(od, name='new')
#    #
#    meta.config.add(config)
#    meta2.config.add(config)
#    assert len(list(config.config.parents())) == 2
#
#
#def test_meta_new_config_wrong_name():
#    od = make_description()
#    meta = MetaConfig(['name1', 'name2'], optiondescription=od)
#    assert len(list(meta.config.list())) == 2
#    with pytest.raises(ConflictError):
#        meta.config.new('name1')
#    assert len(list(meta.config.list())) == 2
#
#
#def test_meta_load_config():
#    od = make_description()
#    meta = MetaConfig(['name1', 'name2'], optiondescription=od)
#    assert len(list(meta.config.list())) == 2
#    meta.config('name1')
#
#
#def test_meta_load_config_wrong_name():
#    od = make_description()
#    meta = MetaConfig(['name1', 'name2'], optiondescription=od)
#    assert len(list(meta.config.list())) == 2
#    with pytest.raises(ConfigError):
#        meta.config('name3')
#
#
#def test_meta_meta_set():
#    meta = make_metaconfig(double=True)
#    errors1 = meta.value.set('od1.i1', 7, only_config=True)
#    errors2 = meta.value.set('od1.i6', 7, only_config=True)
#    assert len(errors1) == 0
#    assert len(errors2) == 2
#    conf1 = meta.config('meta.conf1')
#    conf2 = meta.config('meta.conf2')
#    assert conf1.option('od1.i1').value.get() == conf2.option('od1.i1').value.get() == 7
#    #
#    dconfigs = []
#    ret = meta.config.find('i1', value=7)
#    for conf in ret.config.list():
#        dconfigs.append(conf._config_bag.context)
#    assert [conf1._config_bag.context, conf2._config_bag.context] == dconfigs
#    conf1.option('od1.i1').value.set(8)
#    #
#    dconfigs = []
#    ret = meta.config.find('i1')
#    for conf in ret.config.list():
#        dconfigs.append(conf._config_bag.context)
#    assert [conf1._config_bag.context, conf2._config_bag.context] == dconfigs
#    ret = meta.config.find('i1', value=7)
#    assert len(ret.config.list()) == 1
#    assert conf2._config_bag.context == list(ret.config.list())[0]._config_bag.context
#
#    ret = meta.config.find('i1', value=8)
#    assert len(ret.config.list()) == 1
#    assert conf1._config_bag.context == list(ret.config.list())[0]._config_bag.context
#    #
#    dconfigs = []
#    ret = meta.config.find('i5', value=2)
#    for conf in ret.config.list():
#        dconfigs.append(conf._config_bag.context)
#    assert [conf1._config_bag.context, conf2._config_bag.context] == dconfigs
#    #
#    with pytest.raises(AttributeError):
#        meta.config.find('i1', value=10)
#    with pytest.raises(AttributeError):
#        meta.config.find('not', value=10)
#    with pytest.raises(AttributeError):
#        meta.config.find('i6')
#    with pytest.raises(ValueError):
#        meta.value.set('od1.i6', 7, only_config=True, force_default=True)
#    with pytest.raises(ValueError):
#        meta.value.set('od1.i6', 7, only_config=True, force_default_if_same=True)
#    with pytest.raises(ValueError):
#        meta.value.set('od1.i6', 7, only_config=True, force_dont_change_value=True)
#
#
#def test_not_meta():
#    i1 = IntOption('i1', '')
#    od1 = OptionDescription('od1', '', [i1])
#    od2 = OptionDescription('od2', '', [od1])
#    conf1 = Config(od2, name='conf1')
#    conf2 = Config(od2, name='conf2')
#    conf3 = Config(od2)
#    conf4 = Config(od2, name='conf4')
#    with pytest.raises(TypeError):
#        GroupConfig(conf1)
#    with pytest.raises(ConflictError):
#        GroupConfig([conf2, conf2], name='conf8')
#    grp = GroupConfig([conf1, conf2])
#    assert grp.config.type() == 'groupconfig'
#    with pytest.raises(ConfigError):
#        grp.option('od1.i1').value.get()
#    conf1, conf2 = grp.config.list()
#    errors = grp.value.set('od1.i1', 7)
#    assert len(errors) == 0
#    conf1 = grp.config('conf1')
#    conf2 = grp.config('conf2')
#    assert conf1.option('od1.i1').value.get() == conf2.option('od1.i1').value.get() == 7
#    assert conf1.option('od1.i1').owner.get() is conf2.option('od1.i1').owner.get() is owners.user
#    grp.option('od1.i1').value.reset()
#    assert conf1.option('od1.i1').owner.get() is conf2.option('od1.i1').owner.get() is owners.default
#
#
#def test_group_find_firsts():
#    i1 = IntOption('i1', '')
#    od1 = OptionDescription('od1', '', [i1])
#    od2 = OptionDescription('od2', '', [od1])
#    conf1 = Config(od2, name='conf1')
#    conf2 = Config(od2, name='conf2')
#    grp = GroupConfig([conf1, conf2])
#    ret = grp.config.find('i1')
#    newconf1, newconf2 = grp.config.list()
#    conf1._config_bag.context == newconf1._config_bag.context
#    conf2._config_bag.context == newconf2._config_bag.context
#
#
#def test_group_group():
#    i1 = IntOption('i1', '')
#    od1 = OptionDescription('od1', '', [i1])
#    od2 = OptionDescription('od2', '', [od1])
#    conf1 = Config(od2, name='conf9')
#    conf2 = Config(od2, name='conf10')
#    grp = GroupConfig([conf1, conf2], 'grp')
#    grp2 = GroupConfig([grp])
#    errors = grp2.value.set('od1.i1', 2)
#    assert len(errors) == 0
#    conf9 = grp2.config('grp.conf9')
#    assert conf9.option('od1.i1').value.get() == 2
#    assert conf9.option('od1.i1').owner.get() is owners.user
#
#
#def test_group_group_path():
#    i1 = IntOption('i1', '')
#    od1 = OptionDescription('od1', '', [i1])
#    od2 = OptionDescription('od2', '', [od1])
#    conf1 = Config(od2, name='conf9')
#    conf2 = Config(od2, name='conf10')
#    grp = GroupConfig([conf1, conf2], 'grp')
#    grp2 = GroupConfig([grp], 'grp2')
#    assert grp2.config.path() == 'grp2'
#    newgrp = grp2.config('grp')
#    assert newgrp.config.path() == 'grp'
#    newgrp = grp2.config('grp.conf9')
#    assert newgrp.config.path() == 'conf9'
#    newgrp = grp2.config('grp.conf10')
#    assert newgrp.config.path() == 'conf10'
#
#
#def test_meta_unconsistent():
#    i1 = IntOption('i1', '')
#    i2 = IntOption('i2', '', default=1)
#    i3 = IntOption('i3', '')
#    i4 = IntOption('i4', '', default=2)
#    od1 = OptionDescription('od1', '', [i1, i2, i3, i4])
#    od2 = OptionDescription('od2', '', [od1])
#    i5 = IntOption('i5', '')
#    od3 = OptionDescription('od3', '', [i5])
#    conf1 = Config(od2, name='conf1')
#    conf2 = Config(od2, name='conf2')
#    conf3 = Config(od2, name='conf3')
#    conf4 = Config(od3, name='conf4')
#    meta = MetaConfig([conf1, conf2])
#    meta.owner.set(owners.meta1)
#    with pytest.raises(TypeError):
#        MetaConfig("string")
#    #same descr but conf1 already in meta
#    assert len(list(conf1.config.parents())) == 1
#    assert len(list(conf3.config.parents())) == 0
#    new_meta = MetaConfig([conf1, conf3])
#    assert len(list(conf1.config.parents())) == 2
#    assert len(list(conf3.config.parents())) == 1
#    #not same descr
#    with pytest.raises(ValueError):
#        MetaConfig([conf3, conf4])
#
#
#def test_meta_leadership():
#    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip", multi=True)
#    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "mask", multi=True, properties=('hidden',))
#    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    od = OptionDescription('root', '', [interface1])
#    conf1 = Config(od, name='conf1')
#    conf2 = Config(od, name='conf2')
#    meta = MetaConfig([conf1, conf2])
#    meta.property.read_only()
#    ret = meta.config.find('ip_admin_eth0')
#    configs = ret.config.list()
#    assert len(configs) == 2
#    assert conf1._config_bag.context == configs[0]._config_bag.context
#    assert conf2._config_bag.context == configs[1]._config_bag.context
#    ret = meta.config.find('netmask_admin_eth0')
#    configs = ret.config.list()
#    assert len(configs) == 2
#    assert conf1._config_bag.context == configs[0]._config_bag.context
#    assert conf2._config_bag.context == configs[1]._config_bag.context
#    meta.property.read_write()
#    with pytest.raises(AttributeError):
#        meta.config.find('netmask_admin_eth0')
#    ret = meta.unrestraint.config.find('netmask_admin_eth0')
#    configs = ret.config.list()
#    assert conf1._config_bag.context == configs[0]._config_bag.context
#    assert conf2._config_bag.context == configs[1]._config_bag.context
#    meta.property.read_only()
#    ret = meta.config.find('netmask_admin_eth0')
#    configs = ret.config.list()
#    assert conf1._config_bag.context == configs[0]._config_bag.context
#    assert conf2._config_bag.context == configs[1]._config_bag.context
#
#
#def test_meta_leadership_value():
#    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip", multi=True)
#    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "mask", multi=True, properties=('hidden',))
#    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    od = OptionDescription('root', '', [interface1])
#    conf1 = Config(od, name='conf1')
#    conf2 = Config(od, name='conf2')
#    meta = MetaConfig([conf1, conf2], name="meta")
#    conf1.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.8'])
#    assert conf1.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == None
#    with pytest.raises(ConfigError):
#        conf1.option('ip_admin_eth0.ip_admin_eth0', 0).value.get()
#    #
#    conf1.option('ip_admin_eth0.ip_admin_eth0').value.reset()
#    #
#    meta.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.1'])
#    assert conf1.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == None
#    meta.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('255.255.255.0')
#    assert conf1.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == '255.255.255.0'
#    meta.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('255.255.0.0')
#    assert conf1.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == '255.255.0.0'
#    #
#    conf1.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.1'])
#    assert conf1.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == '255.255.0.0'
#    #
#    meta.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.2.1', '192.168.3.1'])
#    meta.option('ip_admin_eth0.netmask_admin_eth0', 1).value.set('255.255.255.0')
#    #
#    assert conf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.1']
#    assert conf1.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == '255.255.0.0'
#
#
#def test_meta_leadership_value_default():
#    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip", multi=True, default=['192.168.1.1'])
#    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "mask", multi=True)
#    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    od = OptionDescription('root', '', [interface1])
#    conf1 = Config(od, name='conf1')
#    conf2 = Config(od, name='conf2')
#    meta = MetaConfig([conf1, conf2])
#    newconf1 = meta.config('conf1')
#    assert newconf1.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == None
#    #
#    meta.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.1'])
#    assert newconf1.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == None
#    #
#    meta.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('255.255.255.0')
#    assert newconf1.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == '255.255.255.0'
#    #
#    meta.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('255.255.0.0')
#    assert newconf1.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == '255.255.0.0'
#    #
#    newconf1.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.1'])
#    assert newconf1.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == '255.255.0.0'
#
#
#def test_meta_leadership_owners():
#    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip", multi=True)
#    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "mask", multi=True, properties=('hidden',))
#    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    od = OptionDescription('root', '', [interface1])
#    conf1 = Config(od, name='conf1')
#    conf2 = Config(od, name='conf2')
#    meta = MetaConfig([conf1, conf2])
#    meta.owner.set(owners.meta1)
#    newconf1 = meta.config('conf1')
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').owner.isdefault()
#    with pytest.raises(LeadershipError):
#        newconf1.option('ip_admin_eth0.netmask_admin_eth0', 0).owner.isdefault()
#    #
#    newconf1.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.1'])
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').owner.get() == owners.user
#    assert newconf1.option('ip_admin_eth0.netmask_admin_eth0', 0).owner.isdefault()
#    #
#    newconf1.option('ip_admin_eth0.ip_admin_eth0').value.reset()
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').owner.isdefault()
#    #
#    meta.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.1'])
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').owner.get() == owners.meta1
#    assert newconf1.option('ip_admin_eth0.netmask_admin_eth0', 0).owner.isdefault()
#    #
#    meta.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('255.255.255.0')
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').owner.get() == owners.meta1
#    assert newconf1.option('ip_admin_eth0.netmask_admin_eth0', 0).owner.get() == owners.meta1
#    #
#    meta.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('255.255.0.0')
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').owner.get() == owners.meta1
#    assert newconf1.option('ip_admin_eth0.netmask_admin_eth0', 0).owner.get() == owners.meta1
#    #
#    newconf1.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.1'])
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').owner.get() == owners.user
#    assert newconf1.option('ip_admin_eth0.netmask_admin_eth0', 0).owner.get() == owners.meta1
#
#
#def test_meta_force_default():
#    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip", multi=True)
#    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "mask", multi=True, properties=('hidden',))
#    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    od = OptionDescription('root', '', [interface1])
#    conf1 = Config(od, name='conf1')
#    conf2 = Config(od, name='conf2')
#    meta = MetaConfig([conf1, conf2])
#    meta.property.read_write()
#    meta.owner.set('meta1')
#    newconf1 = meta.config('conf1')
#    newconf2 = meta.config('conf2')
#    assert meta.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    #
#    errors = meta.value.set('ip_admin_eth0.ip_admin_eth0', ['192.168.1.1'])
#    assert len(errors) == 0
#    assert meta.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.1']
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.1']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.1']
#    #
#    newconf1.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.2'])
#    assert meta.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.1']
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.2']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.1']
#    #
#    errors = meta.value.set('ip_admin_eth0.ip_admin_eth0', ['192.168.1.3'])
#    assert len(errors) == 0
#    assert meta.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.3']
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.2']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.3']
#    #
#    errors = meta.value.set('ip_admin_eth0.ip_admin_eth0', ['192.168.1.4'], force_default=True)
#    assert len(errors) == 0
#    assert meta.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.4']
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.4']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.4']
#
#
#def test_meta_force_dont_change_value():
#    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip", multi=True)
#    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "mask", multi=True, properties=('hidden',))
#    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    od = OptionDescription('root', '', [interface1])
#    conf1 = Config(od, name='conf1')
#    conf2 = Config(od, name='conf2')
#    meta = MetaConfig([conf1, conf2])
#    meta.property.read_write()
#    meta.owner.set('meta1')
#    assert meta.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    newconf1 = meta.config('conf1')
#    newconf2 = meta.config('conf2')
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    newconf1.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.4'])
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.4']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.user
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').owner.isdefault()
#    errors = meta.value.set('ip_admin_eth0.ip_admin_eth0', ['192.168.1.4'], force_dont_change_value=True)
#    assert len(errors) == 0
#    assert meta.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.4']
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.4']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.user
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.user
#
#
#def test_meta_force_default_if_same():
#    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip", multi=True)
#    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "mask", multi=True, properties=('hidden',))
#    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    od = OptionDescription('root', '', [interface1])
#    conf1 = Config(od, name='conf1')
#    conf2 = Config(od, name='conf2')
#    meta = MetaConfig([conf1, conf2])
#    meta.property.read_write()
#    meta.owner.set('meta1')
#    #
#    newconf1 = meta.config('conf1')
#    newconf2 = meta.config('conf2')
#    assert meta.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    #
#    newconf1.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.4'])
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.4']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.user
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').owner.isdefault()
#    errors = meta.value.set('ip_admin_eth0.ip_admin_eth0', ['192.168.1.4'], force_default_if_same=True)
#    assert len(errors) == 0
#    assert meta.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.4']
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.4']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.4']
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.meta1
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.meta1
#    #
#    newconf1.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.3'])
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.3']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.4']
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.user
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.meta1
#    errors = meta.value.set('ip_admin_eth0.ip_admin_eth0', ['192.168.1.5'], force_default_if_same=True)
#    assert len(errors) == 0
#    assert meta.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.5']
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.3']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.5']
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.user
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.meta1
#
#
#def test_meta_force_default_if_same_and_dont_change():
#    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip", multi=True)
#    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "mask", multi=True, properties=('hidden',))
#    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    od = OptionDescription('root', '', [interface1])
#    conf1 = Config(od, name='conf1')
#    conf2 = Config(od, name='conf2')
#    meta = MetaConfig([conf1, conf2])
#    meta.property.read_write()
#    meta.owner.set('meta1')
#    #
#    newconf1 = meta.config('conf1')
#    newconf2 = meta.config('conf2')
#    assert meta.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    #
#    newconf1.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.4'])
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.4']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.user
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').owner.isdefault()
#    errors = meta.value.set('ip_admin_eth0.ip_admin_eth0', ['192.168.1.4'], force_default_if_same=True, force_dont_change_value=True)
#    assert len(errors) == 0
#    assert meta.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.4']
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.4']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.meta1
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.user
#    #
#    newconf1.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.3'])
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.3']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.user
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.user
#    errors = meta.value.set('ip_admin_eth0.ip_admin_eth0', ['192.168.1.5'], force_default_if_same=True, force_dont_change_value=True)
#    assert len(errors) == 0
#    assert meta.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.5']
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.3']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.user
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.user
#
#
#def test_meta_force_default_and_dont_change():
#    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip", multi=True)
#    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "mask", multi=True, properties=('hidden',))
#    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    od = OptionDescription('root', '', [interface1])
#    conf1 = Config(od, name='rconf1')
#    conf2 = Config(od, name='rconf2')
#    meta = MetaConfig([conf1, conf2])
#    meta.property.read_write()
#    meta.owner.set('meta1')
#    with pytest.raises(ValueError):
#        meta.value.set('ip_admin_eth0.ip_admin_eth0', ['192.168.1.4'], force_default=True, force_dont_change_value=True)
#
#
#def test_meta_properties_meta():
#    ip_admin_eth0 = NetworkOption('ip_admin_eth0', "ip", multi=True, default=['192.168.1.1'])
#    netmask_admin_eth0 = NetmaskOption('netmask_admin_eth0', "mask", multi=True, validators=[Calculation(valid_network_netmask, Params((ParamOption(ip_admin_eth0), ParamSelfOption())))])
#    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0], properties=('disabled',))
#    od = OptionDescription('root', '', [interface1])
#    conf1 = Config(od, name='conf1')
#    conf2 = Config(od, name='conf2')
#    conf1.property.read_write()
#    conf2.property.read_write()
#    meta = MetaConfig([conf1, conf2])
#    meta.property.read_write()
#    ret = meta.config('conf1')
#    assert ret.value.dict() == {}
#
#
#def test_meta_exception_meta():
#    ip_admin_eth0 = NetworkOption('ip_admin_eth0', "ip", multi=True, default=['192.168.1.1'])
#    netmask_admin_eth0 = NetmaskOption('netmask_admin_eth0', "mask", Calculation(raise_exception), multi=True, validators=[Calculation(valid_network_netmask, Params((ParamOption(ip_admin_eth0), ParamSelfOption())))])
#    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    od = OptionDescription('root', '', [interface1])
#    conf1 = Config(od, name='conf1')
#    conf2 = Config(od, name='conf2')
#    meta = MetaConfig([conf1, conf2])
#    meta.property.read_write()
#    with pytest.raises(Exception):
#        conf1.make_dict()
#
#
#def test_meta_properties_requires1():
#    opt1 = BoolOption('opt1', 'opt1', False)
#    opt2 = BoolOption('opt2', "")
#    disabled_property = Calculation(calc_value,
#                                    Params(ParamValue('disabled'),
#                                           kwargs={'condition': ParamOption(opt1),
#                                                   'expected': ParamValue(False)}))
#    od2 = OptionDescription('od2', "", [opt2], properties=(disabled_property,))
#    opt3 = BoolOption('opt3', '', validators=[Calculation(valid_not_equal, Params((ParamSelfOption(), ParamOption(opt2))))])
#    od = OptionDescription('root', '', [opt1, od2, opt3])
#    conf1 = Config(od, name='conf1')
#    conf1.property.read_write()
#    meta = MetaConfig([conf1], 'meta')
#    meta.property.read_write()
#    meta.option('opt1').value.set(True)
#    #
#    conf1.option('od2.opt2').value.set(False)
#
#
#def test_meta_properties_requires_mandatory():
#    probes = BoolOption('probes', 'probes available', False)
#    eth0_method = ChoiceOption('eth0_method', '', ('static', 'dhcp'), 'static')
#    ip_address = IPOption('ip_address', '')
#    mandatory_property = Calculation(calc_value,
#                                     Params(ParamValue('mandatory'),
#                                            kwargs={'condition': ParamOption(probes),
#                                                    'expected': ParamValue('yes'),
#                                                    'default': ParamValue(None)}))
#    ip_eth0 = IPOption('ip_eth0', "ip", Calculation(return_condition, Params(kwargs={'val': ParamOption(ip_address), 'condition': ParamOption(eth0_method), 'expected': ParamValue('dhcp')})), properties=(mandatory_property,))
#    ip_gw = IPOption('ip_gw', 'gw', validators=[Calculation(valid_not_equal, Params((ParamSelfOption(), ParamOption(ip_eth0))))])
#    od = OptionDescription('root', '', [ip_gw, probes, eth0_method, ip_address, ip_eth0])
#    conf1 = Config(od, name='conf1')
#    conf1.property.read_write()
#    meta = MetaConfig([conf1], 'meta')
#    #
#    meta.option('probes').value.set(True)
#    meta.option('ip_address').value.set('1.1.1.1')
#    meta.option('ip_gw').value.set('1.1.1.2')
#    conf1.option('eth0_method').value.set('dhcp')
#    conf1.property.read_only()
#    assert conf1.value.dict() == {'ip_gw': '1.1.1.2', 'probes': True, 'eth0_method': 'dhcp', 'ip_address': '1.1.1.1', 'ip_eth0': '1.1.1.1'}
#
#
#def test_meta_callback():
#    val1 = StrOption('val1', "", 'val')
#    val2 = StrOption('val2', "", Calculation(return_value, Params(ParamOption(val1))))
#    val3 = StrOption('val3', "", Calculation(return_value, Params(ParamValue('yes'))))
#    val4 = StrOption('val4', "", Calculation(return_value, Params(kwargs={'value': ParamOption(val1)})))
#    val5 = StrOption('val5', "", Calculation(return_value, Params(kwargs={'value': ParamValue('yes')})))
#    maconfig = OptionDescription('rootconfig', '', [val1, val2, val3, val4, val5])
#    cfg = Config(maconfig, name='cfg')
#    meta = MetaConfig([cfg])
#    meta.property.read_write()
#    newcfg = meta.config('cfg')
#    assert newcfg.value.dict() == {'val3': 'yes', 'val2': 'val', 'val1': 'val', 'val5': 'yes', 'val4': 'val'}
#    newcfg.option('val1').value.set('new')
#    assert newcfg.value.dict() == {'val3': 'yes', 'val2': 'new', 'val1': 'new', 'val5': 'yes', 'val4': 'new'}
#    newcfg.option('val1').value.reset()
#    meta.option('val1').value.set('new')
#    assert newcfg.value.dict() == {'val3': 'yes', 'val2': 'new', 'val1': 'new', 'val5': 'yes', 'val4': 'new'}
#    newcfg.option('val4').value.set('new1')
#    assert newcfg.value.dict() == {'val3': 'yes', 'val2': 'new', 'val1': 'new', 'val5': 'yes', 'val4': 'new1'}
#    newcfg.option('val4').value.reset()
#    meta.option('val4').value.set('new1')
#    assert newcfg.value.dict() == {'val3': 'yes', 'val2': 'new', 'val1': 'new', 'val5': 'yes', 'val4': 'new1'}
#    meta.option('val4').value.reset()
#
#
#def test_meta_callback_follower():
#    val = StrOption('val', "", default='val')
#    val1 = StrOption('val1', "", [Calculation(return_value, Params(ParamOption(val)))], multi=True)
#    val3 = StrOption('val2', "", Calculation(return_value, Params(ParamOption(val1))), multi=True)
#    val4 = StrOption('val3', "", Calculation(return_value, Params(ParamOption(val1))), multi=True)
#    interface1 = Leadership('val1', '', [val1, val3, val4])
#    od = OptionDescription('root', '', [interface1])
#    maconfig = OptionDescription('rootconfig', '', [val, interface1])
#    conf1 = Config(maconfig, name='conf1')
#    meta = MetaConfig([conf1])
#    meta.property.read_write()
#    assert conf1.value.dict() == {'val': 'val', 'val1.val1': [{'val1.val1': 'val', 'val1.val2': 'val', 'val1.val3': 'val'}]}
#    #
#    conf1.option('val').value.set('val1')
#    assert conf1.value.dict() == {'val': 'val1', 'val1.val1': [{'val1.val1': 'val1', 'val1.val2': 'val1', 'val1.val3': 'val1'}]}
#    #
#    conf1.option('val').value.reset()
#    meta.option('val').value.set('val1')
#    assert conf1.value.dict() == {'val': 'val1', 'val1.val1': [{'val1.val1': 'val1', 'val1.val2': 'val1', 'val1.val3': 'val1'}]}
#    #
#    meta.option('val').value.reset()
#    conf1.option('val1.val2', 0).value.set('val2')
#    assert conf1.value.dict() == {'val': 'val', 'val1.val1': [{'val1.val1': 'val', 'val1.val2': 'val2', 'val1.val3': 'val'}]}
#    #
#    conf1.option('val1.val2', 0).value.reset()
#    assert conf1.value.dict() == {'val': 'val', 'val1.val1': [{'val1.val1': 'val', 'val1.val2': 'val', 'val1.val3': 'val'}]}
#    #
#    meta.option('val1.val2', 0).value.set('val2')
#    assert conf1.value.dict() == {'val': 'val', 'val1.val1': [{'val1.val1': 'val', 'val1.val2': 'val2', 'val1.val3': 'val'}]}
#    #
#    meta.option('val1.val1').value.set(['val'])
#    assert conf1.value.dict() == {'val': 'val', 'val1.val1': [{'val1.val1': 'val', 'val1.val2': 'val2', 'val1.val3': 'val'}]}
#    #
#    conf1.option('val1.val3', 0).value.set('val6')
#    assert conf1.value.dict() == {'val': 'val', 'val1.val1': [{'val1.val1': 'val', 'val1.val2': 'val2', 'val1.val3': 'val6'}]}
#    #
#    meta.option('val1.val2', 0).value.reset()
#    conf1.option('val1.val3', 0).value.reset()
#    conf1.option('val1.val1').value.set(['val3'])
#    assert conf1.value.dict() == {'val': 'val', 'val1.val1': [{'val1.val1': 'val3', 'val1.val2': 'val3', 'val1.val3': 'val3'}]}
#    #
#    conf1.option('val1.val1').value.reset()
#    assert conf1.value.dict() == {'val': 'val', 'val1.val1': [{'val1.val1': 'val', 'val1.val2': 'val', 'val1.val3': 'val'}]}
#    #
#    meta.option('val1.val1').value.set(['val3'])
#    assert conf1.value.dict() == {'val': 'val', 'val1.val1': [{'val1.val1': 'val3', 'val1.val2': 'val3', 'val1.val3': 'val3'}]}
#    #
#    conf1.option('val1.val2', 0).value.set('val2')
#    assert conf1.value.dict() == {'val': 'val', 'val1.val1': [{'val1.val1': 'val3', 'val1.val2': 'val2', 'val1.val3': 'val3'}]}
#    #
#    meta.option('val1.val1').value.set(['val3', 'rah'])
#    assert conf1.value.dict() == {'val': 'val', 'val1.val1': [{'val1.val1': 'val3', 'val1.val2': 'val2', 'val1.val3': 'val3'}, {'val1.val1': 'rah', 'val1.val2': 'rah', 'val1.val3': 'rah'}]}
#    #
#    meta.option('val1.val1').value.pop(1)
#    meta.option('val1.val1').value.set(['val4'])
#    assert conf1.value.dict() == {'val': 'val', 'val1.val1': [{'val1.val1': 'val4', 'val1.val2': 'val2', 'val1.val3': 'val4'}]}
#
#
#def test_meta_reset():
#    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip", multi=True)
#    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "mask", multi=True, properties=('hidden',))
#    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    od = OptionDescription('root', '', [interface1])
#    conf1 = Config(od, name='conf1')
#    conf2 = Config(od, name='conf2')
#    meta = MetaConfig([conf1, conf2])
#    meta.property.read_write()
#    meta.owner.set('meta1')
#    newconf1 = meta.config('conf1')
#    newconf2 = meta.config('conf2')
#    assert meta.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    errors = meta.value.set('ip_admin_eth0.ip_admin_eth0', ['192.168.1.1'])
#    assert len(errors) == 0
#    assert meta.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.1']
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.1']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.1']
#    newconf1.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.2'])
#    assert meta.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.1']
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.2']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.1']
#    meta.value.reset('ip_admin_eth0.ip_admin_eth0')
#    assert meta.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#
#
#def test_meta_properties_meta_copy():
#    ip_admin_eth0 = NetworkOption('ip_admin_eth0', "ip", multi=True, default=['192.168.1.1'])
#    netmask_admin_eth0 = NetmaskOption('netmask_admin_eth0', "mask", multi=True, properties=('disabled',))
#    interface1 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    conf1 = Config(interface1, name='conf1')
#    conf2 = Config(interface1, name='conf2')
#    conf1.property.read_write()
#    conf2.property.read_write()
#    meta = MetaConfig([conf1, conf2], name='meta1')
#    meta.property.read_write()
#
#    newconf1 = meta.config('conf1')
#    newconf2 = meta.config('conf2')
#    conf3 = newconf1.config.copy(name='conf3')
#    meta2 = list(conf3.config.parents())
#    assert len(meta2) == 1
#    assert meta.config.name() == meta2[0].config.name()
#
#    assert newconf1.value.dict() == {'ip_admin_eth0': ['192.168.1.1']}
#    assert newconf2.value.dict() == {'ip_admin_eth0': ['192.168.1.1']}
#    newconf3 = meta.config('conf3')
#    assert newconf3.value.dict() == {'ip_admin_eth0': ['192.168.1.1']}
#    meta.option('ip_admin_eth0').value.set(['192.168.1.2'])
#    assert newconf1.value.dict() == {'ip_admin_eth0': ['192.168.1.2']}
#    assert newconf2.value.dict() == {'ip_admin_eth0': ['192.168.1.2']}
#    assert newconf3.value.dict() == {'ip_admin_eth0': ['192.168.1.2']}
#    ret = meta.value.set('ip_admin_eth0', ['192.168.1.3'], force_default_if_same=True)
#    assert newconf1.value.dict() == {'ip_admin_eth0': ['192.168.1.3']}
#    assert newconf2.value.dict() == {'ip_admin_eth0': ['192.168.1.3']}
#    assert newconf3.value.dict() == {'ip_admin_eth0': ['192.168.1.3']}
#
#
#def test_meta_properties_meta_deepcopy():
#    ip_admin_eth0 = NetworkOption('ip_admin_eth0', "ip", multi=True, default=['192.168.1.1'])
#    netmask_admin_eth0 = NetmaskOption('netmask_admin_eth0', "mask", multi=True,
#                                       properties=('disabled',))
#    interface1 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    conf1 = Config(interface1, name='conf1')
#    conf2 = Config(interface1, name='conf2')
#    conf1.property.read_write()
#    conf2.property.read_write()
#    meta = MetaConfig([conf1, conf2])
#    meta.permissive.add('hidden')
#    meta.property.read_write()
#
#    newconf1 = meta.config('conf1')
#    newconf2 = meta.config('conf2')
#    meta2 = newconf1.config.deepcopy(name='conf3')
#    newconf3 = meta2.config('conf3')
#    assert meta != meta2
#    assert meta.permissive.get() == meta2.permissive.get()
#
#    assert newconf1.value.dict() == {'ip_admin_eth0': ['192.168.1.1']}
#    assert newconf2.value.dict() == {'ip_admin_eth0': ['192.168.1.1']}
#    assert newconf3.value.dict() == {'ip_admin_eth0': ['192.168.1.1']}
#    meta.option('ip_admin_eth0').value.set(['192.168.1.2'])
#    assert newconf1.value.dict() == {'ip_admin_eth0': ['192.168.1.2']}
#    assert newconf2.value.dict() == {'ip_admin_eth0': ['192.168.1.2']}
#    assert newconf3.value.dict() == {'ip_admin_eth0': ['192.168.1.1']}
#    meta.value.set('ip_admin_eth0', ['192.168.1.3'], force_default_if_same=True)
#    assert newconf1.value.dict() == {'ip_admin_eth0': ['192.168.1.3']}
#    assert newconf2.value.dict() == {'ip_admin_eth0': ['192.168.1.3']}
#    assert newconf3.value.dict() == {'ip_admin_eth0': ['192.168.1.1']}
#
#
#def test_meta_properties_meta_deepcopy_multi_parent():
#    ip_admin_eth0 = NetworkOption('ip_admin_eth0', "ip")
#    netmask_admin_eth0 = NetmaskOption('netmask_admin_eth0', "mask")
#    interface1 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    conf1 = Config(interface1, name='conf1')
#    conf2 = Config(interface1, name='conf2')
#    conf1.property.read_write()
#    conf2.property.read_write()
#    meta1 = MetaConfig([conf1, conf2], name='meta1')
#    meta1.permissive.add('hidden')
#    meta1.property.read_write()
#
#    meta2 = MetaConfig(['name1', 'name2'], optiondescription=interface1, name='meta2')
#    meta2.config.add(conf1)
#
#    meta1.option('ip_admin_eth0').value.set('192.168.1.1')
#    meta2.option('netmask_admin_eth0').value.set('255.255.255.0')
#
#    assert meta1.value.dict() == {'ip_admin_eth0': '192.168.1.1', 'netmask_admin_eth0': None}
#    assert meta2.value.dict() == {'ip_admin_eth0': None, 'netmask_admin_eth0': '255.255.255.0'}
#    assert conf1.value.dict() == {'ip_admin_eth0': '192.168.1.1', 'netmask_admin_eth0': '255.255.255.0'}
#    assert conf2.value.dict() == {'ip_admin_eth0': '192.168.1.1', 'netmask_admin_eth0': None}
#
#    copy_meta2 = conf1.config.deepcopy(name='copy_conf1', metaconfig_prefix='copy_')
#    assert copy_meta2.config.path() == 'copy_meta2'
#    copy_meta1 = copy_meta2.config('copy_meta1')
#    copy_conf1 = copy_meta1.config('copy_conf1')
#    assert copy_meta2.value.dict() == {'ip_admin_eth0': None, 'netmask_admin_eth0': '255.255.255.0'}
#    assert copy_conf1.value.dict() == {'ip_admin_eth0': '192.168.1.1', 'netmask_admin_eth0': '255.255.255.0'}
#
#
#def test_meta_properties_submeta_deepcopy():
#    ip_admin_eth0 = NetworkOption('ip_admin_eth0', "ip", multi=True, default=['192.168.1.1'])
#    netmask_admin_eth0 = NetmaskOption('netmask_admin_eth0', "mask", multi=True,
#                                       properties=('disabled',))
#    interface1 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    conf1 = Config(interface1, name='conf1')
#    conf1.property.read_write()
#    meta1 = MetaConfig([conf1], name='meta1')
#    meta2 = MetaConfig([meta1], name='meta2')
#    meta_copy = conf1.config.deepcopy(name='conf2',
#                                      metaconfig_prefix='copy_')
#    assert meta_copy.config.name() == 'copy_meta2'
#    newcopy = meta_copy.config('copy_meta1')
#    assert newcopy.config.name() == 'copy_meta1'
#    newcopy = newcopy.config('conf2')
#    assert newcopy.config.name() == 'conf2'
#
#
#def test_meta_properties_copy_meta():
#    ip_admin_eth0 = NetworkOption('ip_admin_eth0', "ip", multi=True, default=['192.168.1.1'])
#    netmask_admin_eth0 = NetmaskOption('netmask_admin_eth0', "mask", multi=True,
#                                       properties=('disabled',))
#    interface1 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    conf1 = Config(interface1, name='conf1')
#    conf1.property.read_write()
#    meta1 = MetaConfig([conf1], name='meta1')
#    meta2 = MetaConfig([meta1], name='meta2')
#    meta_copy = meta1.config.copy(name='meta3')
#    assert meta_copy.config.name() == 'meta3'
#    assert list(meta_copy.config.list()) == []
#
#
#def test_meta_properties_deepcopy_meta():
#    ip_admin_eth0 = NetworkOption('ip_admin_eth0', "ip", multi=True, default=['192.168.1.1'])
#    netmask_admin_eth0 = NetmaskOption('netmask_admin_eth0', "mask", multi=True,
#                                       properties=('disabled',))
#    interface1 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    conf1 = Config(interface1, name='conf1')
#    conf1.property.read_write()
#    meta1 = MetaConfig([conf1], name='meta1')
#    meta2 = MetaConfig([meta1], name='meta2')
#    meta_copy = meta1.config.deepcopy(name='meta3',
#                                            metaconfig_prefix='copy_')
#    assert meta_copy.config.name() == 'copy_meta2'
#    newcopy = meta_copy.config('meta3')
#    assert newcopy.config.name() == 'meta3'
#    assert list(newcopy.config.list()) == []
#
#
#def test_meta_properties_submeta_deepcopy_owner():
#    ip_admin_eth0 = NetworkOption('ip_admin_eth0', "ip")
#    netmask_admin_eth0 = NetmaskOption('netmask_admin_eth0', "mask")
#    interface1 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    conf1 = Config(interface1, name='conf1')
#    conf1.owner.set('conf1_user')
#    conf1.property.read_write()
#    meta1 = MetaConfig([conf1], name='meta1')
#    meta1.owner.set('meta1_user')
#    meta2 = MetaConfig([meta1], name='meta2')
#    meta2.owner.set('meta2_user')
#    #
#    conf1.option('ip_admin_eth0').value.set('192.168.0.1')
#    assert conf1.option('ip_admin_eth0').owner.get() == 'conf1_user'
#    meta1.option('ip_admin_eth0').value.set('192.168.0.2')
#    assert meta1.option('ip_admin_eth0').owner.get() == 'meta1_user'
#    meta2.option('ip_admin_eth0').value.set('192.168.0.3')
#    assert meta2.option('ip_admin_eth0').owner.get() == 'meta2_user'
#    #
#    meta2_copy = conf1.config.deepcopy(name='conf2',
#                                       metaconfig_prefix='copy_')
#    meta2_copy.option('netmask_admin_eth0').value.set('255.255.255.255')
#    assert meta2_copy.option('ip_admin_eth0').value.get() == '192.168.0.3'
#    assert meta2_copy.option('ip_admin_eth0').owner.get() == 'meta2_user'
#    assert meta2_copy.option('netmask_admin_eth0').owner.get() == 'meta2_user'
#    #
#    meta1_copy = meta2_copy.config('copy_meta1')
#    meta1_copy.option('netmask_admin_eth0').value.set('255.255.255.255')
#    assert meta1_copy.option('ip_admin_eth0').value.get() == '192.168.0.2'
#    assert meta1_copy.option('ip_admin_eth0').owner.get() == 'meta1_user'
#    assert meta1_copy.option('netmask_admin_eth0').owner.get() == 'meta1_user'
#    #
#    conf2 = meta1_copy.config('conf2')
#    conf2.owner.set('conf2_user')
#    conf2.option('netmask_admin_eth0').value.set('255.255.255.255')
#    assert conf2.option('netmask_admin_eth0').owner.get() == 'conf2_user'
#    assert conf2.option('ip_admin_eth0').value.get() == '192.168.0.1'
#    assert conf2.option('ip_admin_eth0').owner.get() == 'conf1_user'
#
#
#def test_meta_properties_meta_set_value():
#    ip_admin_eth0 = NetworkOption('ip_admin_eth0', "ip", multi=True, default=['192.168.1.1'])
#    netmask_admin_eth0 = NetmaskOption('netmask_admin_eth0', "mask", multi=True, properties=('disabled',))
#    interface1 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    conf1 = Config(interface1, name='conf1')
#    conf2 = Config(interface1, name='conf2')
#    conf1.property.read_write()
#    conf2.property.read_write()
#    meta = MetaConfig([conf1, conf2])
#    meta.property.read_write()
#    ret = meta.config('conf1')
#    assert ret.value.dict() == {'ip_admin_eth0': ['192.168.1.1']}
#    ret = meta.value.set('netmask_admin_eth0', ['255.255.255.255'], only_config=True)
#    assert len(ret) == 2
#    assert isinstance(ret[0], PropertiesOptionError)
#    assert isinstance(ret[1], PropertiesOptionError)
#    del ret[1]
#    del ret[0]
#    del ret
#    ret = meta.value.set('netmask_admin_eth0', ['255.255.255.255'], force_default=True)
#    assert len(ret) == 1
#    assert isinstance(ret[0], PropertiesOptionError)
#    del ret[0]
#    del ret
#    ret = meta.value.set('netmask_admin_eth0', ['255.255.255.255'], force_dont_change_value=True)
#    assert len(ret) == 3
#    assert isinstance(ret[0], PropertiesOptionError)
#    assert isinstance(ret[1], PropertiesOptionError)
#    assert isinstance(ret[2], PropertiesOptionError)
#    del ret[2]
#    del ret[1]
#    del ret[0]
#    del ret
#    ret = meta.value.set('netmask_admin_eth0', ['255.255.255.255'], force_default_if_same=True)
#    assert len(ret) == 1
#    assert isinstance(ret[0], PropertiesOptionError)
#    del ret[0]
#    del ret
#    ret = meta.value.set('ip_admin_eth0', '255.255.255.255', only_config=True)
#    assert len(ret) == 2
#    assert isinstance(ret[0], ValueError)
#    assert isinstance(ret[1], ValueError)
#    del ret[1]
#    del ret[0]
#    del ret
#    ret = meta.value.set('ip_admin_eth0', '255.255.255.255', force_default=True)
#    assert len(ret) == 1
#    assert isinstance(ret[0], ValueError)
#    del ret[0]
#    del ret
#    ret = meta.value.set('ip_admin_eth0', '255.255.255.255', force_dont_change_value=True)
#    assert len(ret) == 1
#    assert isinstance(ret[0], ValueError)
#    del ret[0]
#    del ret
#    ret = meta.value.set('ip_admin_eth0', '255.255.255.255', force_default_if_same=True)
#    assert len(ret) == 1
#    assert isinstance(ret[0], ValueError)
#    del ret[0]
#    del ret
#
#
#def test_metaconfig_force_metaconfig_on_freeze():
#    dummy1 = StrOption('dummy1', 'doc dummy', default='default', properties=('force_metaconfig_on_freeze',))
#    group = OptionDescription('group', '', [dummy1])
#    cfg = Config(group, name='cfg')
#    cfg.owner.set(owners.config)
#    meta1 = MetaConfig([cfg], name='meta1')
#    meta1.owner.set(owners.meta1)
#    meta2 = MetaConfig([meta1], name='meta2')
#    meta2.owner.set(owners.meta2)
#    cfg.property.read_write()
#
#    cfg.option('dummy1').property.add('frozen')
#    #
#    assert cfg.option('dummy1').value.get() == 'default'
#    assert cfg.option('dummy1').owner.get() == 'default'
#    #
#    meta2.option('dummy1').value.set('meta2')
#    #
#    assert cfg.option('dummy1').value.get() == 'meta2'
#    assert cfg.option('dummy1').owner.get() == 'meta2'
#    #
#    cfg.option('dummy1').property.remove('frozen')
#    cfg.option('dummy1').value.set('cfg')
#    cfg.option('dummy1').property.add('frozen')
#    #
#    assert cfg.option('dummy1').value.get() == 'meta2'
#    assert cfg.option('dummy1').owner.get() == 'meta2'
#    #
#    meta1.option('dummy1').value.set('meta1')
#    #
#    assert cfg.option('dummy1').value.get() == 'meta1'
#    assert cfg.option('dummy1').owner.get() == 'meta1'
#    #
#    cfg.option('dummy1').property.remove('frozen')
#    assert cfg.option('dummy1').value.get() == 'cfg'
#    assert cfg.option('dummy1').owner.get() == 'config'
#
#
#def test_metaconfig_force_metaconfig_on_freeze_option():
#    dummy1 = StrOption('dummy1', 'doc dummy', default='default')
#    dummy2 = StrOption('dummy2', 'doc dummy', default='default', properties=('force_default_on_freeze',))
#    group = OptionDescription('group', '', [dummy1, dummy2])
#    cfg = Config(group, name='cfg')
#    cfg.owner.set(owners.config)
#    meta1 = MetaConfig([cfg], name='meta1')
#    meta1.owner.set(owners.meta1)
#    meta2 = MetaConfig([meta1], name='meta2')
#    meta2.owner.set(owners.meta2)
#    cfg.property.read_write()
#
#    cfg.option('dummy1').property.add('frozen')
#    cfg.option('dummy1').property.add('force_metaconfig_on_freeze')
#    cfg.option('dummy2').property.add('frozen')
#    #
#    assert cfg.option('dummy1').value.get() == 'default'
#    assert cfg.option('dummy1').owner.get() == 'default'
#    assert cfg.option('dummy2').value.get() == 'default'
#    assert cfg.option('dummy2').owner.get() == 'default'
#    #
#    meta2.option('dummy1').value.set('meta2')
#    meta2.option('dummy2').value.set('meta2')
#    #
#    assert cfg.option('dummy1').value.get() == 'meta2'
#    assert cfg.option('dummy1').owner.get() == 'meta2'
#    assert cfg.option('dummy2').value.get() == 'default'
#    assert cfg.option('dummy2').owner.get() == 'default'
#    #
#    cfg.option('dummy1').property.remove('frozen')
#    cfg.option('dummy2').property.remove('frozen')
#    cfg.option('dummy1').value.set('cfg')
#    cfg.option('dummy2').value.set('cfg')
#    cfg.option('dummy1').property.add('frozen')
#    cfg.option('dummy2').property.add('frozen')
#    #
#    assert cfg.option('dummy1').value.get() == 'meta2'
#    assert cfg.option('dummy1').owner.get() == 'meta2'
#    assert cfg.option('dummy2').value.get() == 'default'
#    assert cfg.option('dummy2').owner.get() == 'default'
#    #
#    meta1.option('dummy1').value.set('meta1')
#    meta1.option('dummy2').value.set('meta1')
#    #
#    assert cfg.option('dummy1').value.get() == 'meta1'
#    assert cfg.option('dummy1').owner.get() == 'meta1'
#    assert cfg.option('dummy2').value.get() == 'default'
#    assert cfg.option('dummy2').owner.get() == 'default'
#    #
#    meta1.option('dummy1').property.add('force_metaconfig_on_freeze')
#    assert cfg.option('dummy1').value.get() == 'meta2'
#    assert cfg.option('dummy1').owner.get() == 'meta2'
#    #
#    meta2.option('dummy1').property.add('force_metaconfig_on_freeze')
#    assert cfg.option('dummy1').value.get() == 'default'
#    assert cfg.option('dummy1').owner.get() == 'default'
#    #
#    meta1.option('dummy1').property.remove('force_metaconfig_on_freeze')
#    assert cfg.option('dummy1').value.get() == 'meta1'
#    assert cfg.option('dummy1').owner.get() == 'meta1'
#    #
#    cfg.option('dummy1').property.remove('frozen')
#    assert cfg.option('dummy1').value.get() == 'cfg'
#    assert cfg.option('dummy1').owner.get() == 'config'
#
#
#def test_meta_get_config():
#    od = make_description()
#    meta = MetaConfig(['name1', 'name2'], optiondescription=od)
#    meta.config.new('meta1', type='metaconfig')
#    assert isinstance(meta.config('meta1'), MetaConfig)
#    assert isinstance(meta.config('name1'), Config)
#    with pytest.raises(ConfigError):
#        meta.config('unknown')
