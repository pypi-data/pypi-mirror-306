from .autopath import do_autopath
do_autopath()

import pytest

from tiramisu.setting import groups, owners
from tiramisu import IntOption, StrOption, NetworkOption, NetmaskOption, \
                     OptionDescription, Leadership, Config, GroupConfig, MixConfig, \
                     MetaConfig, Params, ParamOption, ParamValue, ParamSelfOption, Calculation, \
                     valid_network_netmask
from tiramisu.error import ConfigError, ConflictError, PropertiesOptionError, LeadershipError

owners.addowner('mix1')
owners.addowner('mix2')


def return_value(value=None):
    return value


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


def make_description1():
    i1 = IntOption('i1', '')
    i2 = IntOption('i2', '', default=1)
    i3 = IntOption('i3', '')
    i4 = IntOption('i4', '', default=2)
    i5 = IntOption('i5', '', default=[2], multi=True)
    i6 = IntOption('i6', '', properties=('disabled',))
    od1 = OptionDescription('od1', '', [i1, i2, i3, i4, i5, i6])
    od2 = OptionDescription('od2', '', [od1])
    return od2


def make_description2():
    i1 = IntOption('i1', '')
    i2 = IntOption('i2', '', default=1)
    i3 = IntOption('i3', '')
    i4 = IntOption('i4', '', default=2)
    i5 = IntOption('i5', '', default=[2], multi=True)
    i6 = IntOption('i6', '', properties=('disabled',))
    od1 = OptionDescription('od1', '', [i1, i2, i3, i4, i5, i6])
    od2 = OptionDescription('od2', '', [od1])
    return od2


def make_description3():
    i1 = IntOption('i1', '')
    i2 = IntOption('i2', '', default=1)
    i3 = IntOption('i3', '')
    i4 = IntOption('i4', '', default=2)
    i5 = IntOption('i5', '', default=[2], multi=True)
    i6 = IntOption('i6', '', properties=('disabled',))
    od1 = OptionDescription('od1', '', [i1, i2, i3, i4, i5, i6])
    od2 = OptionDescription('od2', '', [od1])
    return od2


def make_mixconfig(double=False):
    od1 = make_description()
    od2 = make_description1()
    od3 = make_description2()
    conf1 = Config(od1, name='conf1')
    conf1.property.read_write()
    conf2 = Config(od2, name='conf2')
    conf2.property.read_write()
    mix = MixConfig(od3, [conf1, conf2], name='mix')
    assert mix.config.type() == 'mixconfig'
    if double:
        od4 = make_description3()
        mix.owner.set(owners.mix2)
        mix = MixConfig(od4, [mix], name='doublemix')
    mix.property.read_write()
    mix.owner.set(owners.mix1)
    return mix


#def test_mix_name():
#    mix = make_mixconfig(True)
#    assert mix.config.path() == 'doublemix'
#    ret = mix.config('mix')
#    assert ret.config.path() == 'doublemix.mix'
#    ret = mix.config('mix.conf1')
#    assert ret.config.path() == 'doublemix.mix.conf1'
#    ret = mix.config('mix.conf2')
#    assert ret.config.path() == 'doublemix.mix.conf2'
#
#
#def test_mix_not_group():
#    i1 = IntOption('i1', '')
#    od1 = OptionDescription('od1', '', [i1])
#    od2 = OptionDescription('od2', '', [od1])
#    cfg = Config(od2, name='conf1')
#    grp = GroupConfig([cfg])
#    with pytest.raises(TypeError):
#        MixConfig(od2, [grp], name='error')
##    assert not list_sessions()
#
#
#def test_unknown_config():
#    mix = make_mixconfig()
#    with pytest.raises(ConfigError):
#        mix.config('unknown')
#
#
#def test_none():
#    mix = make_mixconfig()
#    newconf1 = mix.config('conf1')
#    newconf2 = mix.config('conf2')
#    assert mix.option('od1.i3').value.get() is newconf1.option('od1.i3').value.get() is newconf2.option('od1.i3').value.get() is None
#    assert mix.option('od1.i3').owner.get() is newconf1.option('od1.i3').owner.get() is newconf2.option('od1.i3').owner.get() is owners.default
#    #
#    mix.option('od1.i3').value.set(3)
#    assert mix.option('od1.i3').value.get() == newconf1.option('od1.i3').value.get() == newconf2.option('od1.i3').value.get() == 3
#    assert mix.option('od1.i3').owner.get() is newconf1.option('od1.i3').owner.get() is newconf2.option('od1.i3').owner.get() is owners.mix1
#    #
#    newconf1.option('od1.i3').value.set(2)
#    assert mix.option('od1.i3').value.get() == newconf2.option('od1.i3').value.get() == 3
#    assert newconf1.option('od1.i3').value.get() == 2
#    assert mix.option('od1.i3').owner.get() is newconf2.option('od1.i3').owner.get() is owners.mix1
#    assert newconf1.option('od1.i3').owner.get() is owners.user
#    #
#    mix.option('od1.i3').value.set(4)
#    assert mix.option('od1.i3').value.get() == newconf2.option('od1.i3').value.get() == 4
#    assert newconf1.option('od1.i3').value.get() == 2
#    assert mix.option('od1.i3').owner.get() is newconf2.option('od1.i3').owner.get() is owners.mix1
#    assert newconf1.option('od1.i3').owner.get() is owners.user
#    #
#    mix.option('od1.i3').value.reset()
#    assert mix.option('od1.i3').value.get() is newconf2.option('od1.i3').value.get() is None
#    assert newconf1.option('od1.i3').value.get() == 2
#    assert mix.option('od1.i3').owner.get() is newconf2.option('od1.i3').owner.get() is owners.default
#    assert newconf1.option('od1.i3').owner.get() is owners.user
#    #
#    newconf1.option('od1.i3').value.reset()
#    assert mix.option('od1.i3').value.get() is newconf1.option('od1.i3').value.get() is newconf2.option('od1.i3').value.get() is None
#    assert mix.option('od1.i3').owner.get() is newconf1.option('od1.i3').owner.get() is newconf2.option('od1.i3').owner.get() is owners.default
#    #
#    assert mix.config.name() == mix.config.name()
#
#
#def test_reset():
#    mix = make_mixconfig()
#    assert mix.option('od1.i2').value.get() == 1
#    mix.option('od1.i2').value.set(2)
#    newconf1 = mix.config('conf1')
#    newconf2 = mix.config('conf2')
#    newconf1.option('od1.i2').value.set(3)
#    assert mix.option('od1.i2').value.get() == 2
#    assert newconf1.option('od1.i2').value.get() == 3
#    assert newconf2.option('od1.i2').value.get() == 2
#    mix.config.reset()
#    assert mix.option('od1.i2').value.get() == 1
#    assert newconf1.option('od1.i2').value.get() == 3
#    assert newconf2.option('od1.i2').value.get() == 1
#
#
#def test_default():
#    mix = make_mixconfig()
#    newconf1 = mix.config('conf1')
#    newconf2 = mix.config('conf2')
#    assert mix.option('od1.i2').value.get() == newconf1.option('od1.i2').value.get() == newconf2.option('od1.i2').value.get() == 1
#    assert mix.option('od1.i2').owner.get() is newconf1.option('od1.i2').owner.get() is newconf2.option('od1.i2').owner.get() is owners.default
#    #
#    mix.option('od1.i2').value.set(3)
#    assert mix.option('od1.i2').value.get() == newconf1.option('od1.i2').value.get() == newconf2.option('od1.i2').value.get() == 3
#    assert mix.option('od1.i2').owner.get() is newconf1.option('od1.i2').owner.get() is newconf2.option('od1.i2').owner.get() is owners.mix1
#    #
#    newconf1.option('od1.i2').value.set(2)
#    assert mix.option('od1.i2').value.get() == newconf2.option('od1.i2').value.get() == 3
#    assert newconf1.option('od1.i2').value.get() == 2
#    assert mix.option('od1.i2').owner.get() is newconf2.option('od1.i2').owner.get() is owners.mix1
#    assert newconf1.option('od1.i2').owner.get() is owners.user
#    #
#    mix.option('od1.i2').value.set(4)
#    assert mix.option('od1.i2').value.get() == newconf2.option('od1.i2').value.get() == 4
#    assert newconf1.option('od1.i2').value.get() == 2
#    assert mix.option('od1.i2').owner.get() is newconf2.option('od1.i2').owner.get() is owners.mix1
#    assert newconf1.option('od1.i2').owner.get() is owners.user
#    #
#    mix.option('od1.i2').value.reset()
#    assert mix.option('od1.i2').value.get() == newconf2.option('od1.i2').value.get() == 1
#    assert newconf1.option('od1.i2').value.get() == 2
#    assert mix.option('od1.i2').owner.get() is newconf2.option('od1.i2').owner.get() is owners.default
#    assert newconf1.option('od1.i2').owner.get() is owners.user
#    #
#    newconf1.option('od1.i2').value.reset()
#    assert mix.option('od1.i2').value.get() == newconf1.option('od1.i2').value.get() == newconf2.option('od1.i2').value.get() == 1
#    assert mix.option('od1.i2').owner.get() is newconf1.option('od1.i2').owner.get() is newconf2.option('od1.i2').owner.get() is owners.default
#
#
#def test_contexts():
#    mix = make_mixconfig()
#    errors = mix.value.set('od1.i2', 6, only_config=True)
#    newconf1 = mix.config('conf1')
#    assert mix.option('od1.i2').value.get() == 1
#    assert mix.option('od1.i2').owner.get() == owners.default
#    assert newconf1.option('od1.i2').value.get() == newconf1.option('od1.i2').value.get() == 6
#    assert newconf1.option('od1.i2').owner.get() == newconf1.option('od1.i2').owner.get() is owners.user
#    assert len(errors) == 0
#
#
#
#def test_find():
#    mix = make_mixconfig()
#    ret = list(mix.option.find('i2'))
#    assert len(ret) == 1
#    assert 1 == ret[0].value.get()
#    ret = mix.option.find('i2', first=True)
#    assert 1 == ret.value.get()
#    assert mix.value.dict() == {'od1.i4': 2, 'od1.i1': None, 'od1.i3': None,
#                                 'od1.i2': 1, 'od1.i5': [2]}
#
#
#def test_mix_mix():
#    mix = make_mixconfig(double=True)
#    newmix = mix.config('mix')
#    newconf1 = mix.config('mix.conf1')
#    newconf2 = mix.config('mix.conf2')
#    assert mix.option('od1.i2').value.get() == newmix.option('od1.i2').value.get() == newconf1.option('od1.i2').value.get() == newconf2.option('od1.i2').value.get() == 1
#    assert mix.option('od1.i2').owner.get() is newmix.option('od1.i2').owner.get() is newconf1.option('od1.i2').owner.get() is newconf2.option('od1.i2').owner.get() is owners.default
#    #
#    mix.option('od1.i2').value.set(3)
#    assert mix.option('od1.i2').value.get() == newmix.option('od1.i2').value.get() == newconf1.option('od1.i2').value.get() == newconf2.option('od1.i2').value.get() == 3
#    assert mix.option('od1.i2').owner.get() is newmix.option('od1.i2').owner.get() is newconf1.option('od1.i2').owner.get() is newconf2.option('od1.i2').owner.get() is owners.mix1
#    #
#    newconf1.option('od1.i2').value.set(2)
#    assert mix.option('od1.i2').value.get() == newmix.option('od1.i2').value.get() == newconf2.option('od1.i2').value.get() == 3
#    assert newconf1.option('od1.i2').value.get() == 2
#    assert mix.option('od1.i2').owner.get() is newmix.option('od1.i2').owner.get() is newconf2.option('od1.i2').owner.get() is owners.mix1
#    assert newconf1.option('od1.i2').owner.get() is owners.user
#    #
#    newmix.option('od1.i2').value.set(4)
#    assert mix.option('od1.i2').value.get() == 3
#    assert newmix.option('od1.i2').value.get() == newconf2.option('od1.i2').value.get() == 4
#    assert newconf1.option('od1.i2').value.get() == 2
#    assert mix.option('od1.i2').owner.get() is owners.mix1
#    assert newmix.option('od1.i2').owner.get() is newconf2.option('od1.i2').owner.get() is owners.mix2
#    assert newconf1.option('od1.i2').owner.get() is owners.user
#    #
#    newmix.option('od1.i2').value.reset()
#    assert mix.option('od1.i2').value.get() == newmix.option('od1.i2').value.get() == newconf2.option('od1.i2').value.get() == 3
#    assert newconf1.option('od1.i2').value.get() == 2
#    assert mix.option('od1.i2').owner.get() is newmix.option('od1.i2').owner.get() is newconf2.option('od1.i2').owner.get() is owners.mix1
#    assert newconf1.option('od1.i2').owner.get() is owners.user
#    #
#    mix.option('od1.i2').value.reset()
#    assert mix.option('od1.i2').value.get() == newmix.option('od1.i2').value.get() == newconf2.option('od1.i2').value.get() == 1
#    assert newconf1.option('od1.i2').value.get() == 2
#    assert mix.option('od1.i2').owner.get() is newmix.option('od1.i2').owner.get() is newconf2.option('od1.i2').owner.get() is owners.default
#    assert newconf1.option('od1.i2').owner.get() is owners.user
#    #
#    newconf1.option('od1.i2').value.reset()
#    assert mix.option('od1.i2').value.get() == newmix.option('od1.i2').value.get() == newconf1.option('od1.i2').value.get() == newconf2.option('od1.i2').value.get() == 1
#    assert mix.option('od1.i2').owner.get() is newmix.option('od1.i2').owner.get() is newconf1.option('od1.i2').owner.get() is newconf2.option('od1.i2').owner.get() is owners.default
#
#
#def test_mix_mix_set():
#    mix = make_mixconfig(double=True)
#    errors1 = mix.value.set('od1.i1', 7, only_config=True)
#    errors2 = mix.value.set('od1.i6', 7, only_config=True)
#    assert len(errors1) == 0
#    assert len(errors2) == 2
#    ret = mix.config('mix.conf1')
#    conf1 = ret._config_bag.context
#    ret = mix.config('mix.conf2')
#    conf2 = ret._config_bag.context
#    newconf1 = mix.config('mix.conf1')
#    newconf2 = mix.config('mix.conf2')
#    assert newconf1.option('od1.i1').value.get() == newconf2.option('od1.i1').value.get() == 7
#    #
#    dconfigs = []
#    ret = mix.config.find('i1', value=7)
#    for conf in ret.config.list():
#        dconfigs.append(conf._config_bag.context)
#    assert [conf1, conf2] == dconfigs
#    newconf1.option('od1.i1').value.set(8)
#    #
#    dconfigs = []
#    ret = mix.config.find('i1')
#    for conf in ret.config.list():
#        dconfigs.append(conf._config_bag.context)
#    assert [conf1, conf2] == dconfigs
#    ret = mix.config.find('i1', value=7)
#    assert conf2 == list(ret.config.list())[0]._config_bag.context
#    ret = mix.config.find('i1', value=8)
#    assert conf1 == list(ret.config.list())[0]._config_bag.context
#    #
#    dconfigs = []
#    ret = mix.config.find('i5', value=2)
#    for conf in ret.config.list():
#        dconfigs.append(conf._config_bag.context)
#    assert [conf1, conf2] == dconfigs
#    #
#    with pytest.raises(AttributeError):
#        mix.config.find('i1', value=10)
#    with pytest.raises(AttributeError):
#        mix.config.find('not', value=10)
#    with pytest.raises(AttributeError):
#        mix.config.find('i6')
#    with pytest.raises(ValueError):
#        mix.value.set('od1.i6', 7, only_config=True, force_default=True)
#    with pytest.raises(ValueError):
#        mix.value.set('od1.i6', 7, only_config=True, force_default_if_same=True)
#    with pytest.raises(ValueError):
#        mix.value.set('od1.i6', 7, only_config=True, force_dont_change_value=True)
#
#
#def test_mix_unconsistent():
#    i1 = IntOption('i1', '')
#    i2 = IntOption('i2', '', default=1)
#    i3 = IntOption('i3', '')
#    i4 = IntOption('i4', '', default=2)
#    od1 = OptionDescription('od1', '', [i1, i2, i3, i4])
#    od2 = OptionDescription('od2', '', [od1])
#    od3 = OptionDescription('od3', '', [od1])
#    conf1 = Config(od2, name='conf1')
#    conf2 = Config(od2, name='conf2')
#    conf3 = Config(od2, name='conf3')
#    i5 = IntOption('i5', '')
#    od4 = OptionDescription('od4', '', [i5])
#    conf4 = Config(od4, name='conf4')
#    mix = MixConfig(od2, [conf1, conf2])
#    mix.owner.set(owners.mix1)
#    with pytest.raises(TypeError):
#        MixConfig(od2, "string", name='error')
#    # same descr but conf1 already in mix
#    assert len(list(conf1.config.parents())) == 1
#    assert len(list(conf3.config.parents())) == 0
#    new_mix = MixConfig(od2, [conf1, conf3])
#    assert len(list(conf1.config.parents())) == 2
#    assert len(list(conf3.config.parents())) == 1
#    # not same descr
#    tmix = MixConfig(od2, [conf3, conf4])
#
#
#def test_mix_leadership():
#    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip", multi=True)
#    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "mask", multi=True, properties=('hidden',))
#    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    od = OptionDescription('root', '', [interface1])
#    conf1 = Config(od, name='conf1')
#    conf2 = Config(od, name='conf2')
#    mix = MixConfig(od, [conf1, conf2])
#    mix.property.read_only()
#    ret = mix.config.find('ip_admin_eth0')
#    configs = ret.config.list()
#    assert len(configs) == 2
#    assert conf1._config_bag.context == configs[0]._config_bag.context
#    assert conf2._config_bag.context == configs[1]._config_bag.context
#    ret = mix.config.find('netmask_admin_eth0')
#    configs = ret.config.list()
#    assert len(configs) == 2
#    assert conf1._config_bag.context == configs[0]._config_bag.context
#    assert conf2._config_bag.context == configs[1]._config_bag.context
#    mix.property.read_write()
#    with pytest.raises(AttributeError):
#        mix.config.find('netmask_admin_eth0')
#    ret = mix.unrestraint.config.find('netmask_admin_eth0')
#    configs = ret.config.list()
#    assert len(configs) == 2
#    assert conf1._config_bag.context == configs[0]._config_bag.context
#    assert conf2._config_bag.context == configs[1]._config_bag.context
#    mix.property.read_only()
#    ret = mix.config.find('netmask_admin_eth0')
#    configs = ret.config.list()
#    assert len(configs) == 2
#    assert conf1._config_bag.context == configs[0]._config_bag.context
#    assert conf2._config_bag.context == configs[1]._config_bag.context
#
#
#def test_mix_leadership_value2():
#    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip", multi=True)
#    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "mask", multi=True, properties=('hidden',))
#    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    od = OptionDescription('root', '', [interface1])
#    conf1 = Config(od, name='conf1')
#    conf2 = Config(od, name='conf2')
#    mix = MixConfig(od, [conf1, conf2], name="mix")
#    newconf1 = mix.config('conf1')
#    newconf1.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.8'])
#    assert newconf1.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == None
#    #FIXME devrait raise ! assert newconf1.option('ip_admin_eth0.ip_admin_eth0', 0).value.get() == None
#    #
#    newconf1.option('ip_admin_eth0.ip_admin_eth0').value.reset()
#    #
#    mix.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.1'])
#    assert newconf1.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == None
#    mix.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('255.255.255.0')
#    assert newconf1.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == '255.255.255.0'
#    mix.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('255.255.0.0')
#    assert newconf1.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == '255.255.0.0'
#    #
#    newconf1.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.1'])
#    assert newconf1.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == '255.255.0.0'
#
#
#def test_mix_leadership_value_default():
#    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip", multi=True, default=['192.168.1.1'])
#    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "mask", multi=True)
#    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    od = OptionDescription('root', '', [interface1])
#    conf1 = Config(od, name='conf1')
#    conf2 = Config(od, name='conf2')
#    mix = MixConfig(od, [conf1, conf2])
#    newconf1 = mix.config('conf1')
#    assert newconf1.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == None
#    #
#    mix.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.1'])
#    assert newconf1.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == None
#    #
#    mix.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('255.255.255.0')
#    assert newconf1.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == '255.255.255.0'
#    #
#    mix.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('255.255.0.0')
#    assert newconf1.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == '255.255.0.0'
#    #
#    newconf1.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.1'])
#    assert newconf1.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == '255.255.0.0'
#
#
#def test_mix_leadership_owners():
#    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip", multi=True)
#    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "mask", multi=True, properties=('hidden',))
#    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    od = OptionDescription('root', '', [interface1])
#    conf1 = Config(od, name='conf1')
#    conf2 = Config(od, name='conf2')
#    mix = MixConfig(od, [conf1, conf2])
#    mix.owner.set(owners.mix1)
#    newconf1 = mix.config('conf1')
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
#    mix.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.1'])
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').owner.get() == owners.mix1
#    assert newconf1.option('ip_admin_eth0.netmask_admin_eth0', 0).owner.isdefault()
#    #
#    mix.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('255.255.255.0')
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').owner.get() == owners.mix1
#    assert newconf1.option('ip_admin_eth0.netmask_admin_eth0', 0).owner.get() == owners.mix1
#    #
#    mix.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('255.255.0.0')
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').owner.get() == owners.mix1
#    assert newconf1.option('ip_admin_eth0.netmask_admin_eth0', 0).owner.get() == owners.mix1
#    #
#    newconf1.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.1'])
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').owner.get() == owners.user
#    assert newconf1.option('ip_admin_eth0.netmask_admin_eth0', 0).owner.get() == owners.mix1
#
#
#def test_mix_force_default():
#    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip", multi=True)
#    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "mask", multi=True, properties=('hidden',))
#    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    od = OptionDescription('root', '', [interface1])
#    conf1 = Config(od, name='conf1')
#    conf2 = Config(od, name='conf2')
#    mix = MixConfig(od, [conf1, conf2])
#    mix.property.read_write()
#    mix.owner.set('mix1')
#    assert mix.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    newconf1 = mix.config('conf1')
#    newconf2 = mix.config('conf2')
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    #
#    errors = mix.value.set('ip_admin_eth0.ip_admin_eth0', ['192.168.1.1'])
#    assert len(errors) == 0
#    assert mix.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.1']
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.1']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.1']
#    #
#    newconf1.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.2'])
#    assert mix.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.1']
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.2']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.1']
#    #
#    errors = mix.value.set('ip_admin_eth0.ip_admin_eth0', ['192.168.1.3'])
#    assert len(errors) == 0
#    assert mix.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.3']
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.2']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.3']
#    #
#    errors = mix.value.set('ip_admin_eth0.ip_admin_eth0', ['192.168.1.4'], force_default=True)
#    assert len(errors) == 0
#    assert mix.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.4']
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.4']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.4']
#
#
#def test_mix_force_dont_change_value():
#    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip", multi=True)
#    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "mask", multi=True, properties=('hidden',))
#    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    od = OptionDescription('root', '', [interface1])
#    conf1 = Config(od, name='conf1')
#    conf2 = Config(od, name='conf2')
#    mix = MixConfig(od, [conf1, conf2])
#    mix.property.read_write()
#    mix.owner.set('mix1')
#    assert mix.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    newconf1 = mix.config('conf1')
#    newconf2 = mix.config('conf2')
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    newconf1.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.4'])
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.4']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.user
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').owner.isdefault()
#    errors = mix.value.set('ip_admin_eth0.ip_admin_eth0', ['192.168.1.4'], force_dont_change_value=True)
#    assert len(errors) == 0
#    assert mix.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.4']
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.4']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.user
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.user
#
#
#def test_mix_force_default_if_same():
#    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip", multi=True)
#    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "mask", multi=True, properties=('hidden',))
#    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    od = OptionDescription('root', '', [interface1])
#    conf1 = Config(od, name='conf1')
#    conf2 = Config(od, name='conf2')
#    mix = MixConfig(od, [conf1, conf2])
#    mix.property.read_write()
#    mix.owner.set('mix1')
#    #
#    assert mix.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    newconf1 = mix.config('conf1')
#    newconf2 = mix.config('conf2')
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    #
#    newconf1.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.4'])
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.4']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.user
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').owner.isdefault()
#    errors = mix.value.set('ip_admin_eth0.ip_admin_eth0', ['192.168.1.4'], force_default_if_same=True)
#    assert len(errors) == 0
#    assert mix.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.4']
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.4']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.4']
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.mix1
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.mix1
#    #
#    newconf1.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.3'])
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.3']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.4']
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.user
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.mix1
#    errors = mix.value.set('ip_admin_eth0.ip_admin_eth0', ['192.168.1.5'], force_default_if_same=True)
#    assert len(errors) == 0
#    assert mix.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.5']
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.3']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.5']
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.user
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.mix1
#
#
#def test_mix_force_default_if_same_and_dont_change():
#    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip", multi=True)
#    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "mask", multi=True, properties=('hidden',))
#    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    od = OptionDescription('root', '', [interface1])
#    conf1 = Config(od, name='conf1')
#    conf2 = Config(od, name='conf2')
#    mix = MixConfig(od, [conf1, conf2])
#    mix.property.read_write()
#    mix.owner.set('mix1')
#    #
#    assert mix.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    newconf1 = mix.config('conf1')
#    newconf2 = mix.config('conf2')
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    #
#    newconf1.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.4'])
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.4']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.user
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').owner.isdefault()
#    errors = mix.value.set('ip_admin_eth0.ip_admin_eth0', ['192.168.1.4'], force_default_if_same=True, force_dont_change_value=True)
#    assert len(errors) == 0
#    assert mix.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.4']
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.4']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.mix1
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.user
#    #
#    newconf1.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.3'])
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.3']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.user
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.user
#    errors = mix.value.set('ip_admin_eth0.ip_admin_eth0', ['192.168.1.5'], force_default_if_same=True, force_dont_change_value=True)
#    assert len(errors) == 0
#    assert mix.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.5']
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.3']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.user
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').owner.get() is owners.user
#
#
#
#def test_mix_force_default_and_dont_change():
#    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip", multi=True)
#    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "mask", multi=True, properties=('hidden',))
#    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    od = OptionDescription('root', '', [interface1])
#    conf1 = Config(od, name='rconf1')
#    conf2 = Config(od, name='rconf2')
#    mix = MixConfig(od, [conf1, conf2])
#    mix.property.read_write()
#    mix.owner.set('mix1')
#    with pytest.raises(ValueError):
#        mix.value.set('ip_admin_eth0.ip_admin_eth0', ['192.168.1.4'], force_default=True, force_dont_change_value=True)
#
#
#def test_mix_properties_mix():
#    ip_admin_eth0 = NetworkOption('ip_admin_eth0', "ip", multi=True, default=['192.168.1.1'])
#    netmask_admin_eth0 = NetmaskOption('netmask_admin_eth0', "mask", multi=True, validators=[Calculation(valid_network_netmask, Params((ParamOption(ip_admin_eth0), ParamSelfOption())))])
#    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0], properties=('disabled',))
#    od = OptionDescription('root', '', [interface1])
#    conf1 = Config(od, name='conf1')
#    conf2 = Config(od, name='conf2')
#    conf1.property.read_write()
#    conf2.property.read_write()
#    mix = MixConfig(od, [conf1, conf2])
#    mix.property.read_write()
#    newconf1 = mix.config('conf1')
#    assert newconf1.value.dict() == {}
#
#
#def test_mix_exception_mix():
#    ip_admin_eth0 = NetworkOption('ip_admin_eth0', "ip", multi=True, default=['192.168.1.1'])
#    netmask_admin_eth0 = NetmaskOption('netmask_admin_eth0', "mask", Calculation(raise_exception), multi=True, validators=[Calculation(valid_network_netmask, Params((ParamOption(ip_admin_eth0), ParamSelfOption())))])
#    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    od = OptionDescription('root', '', [interface1])
#    conf1 = Config(od, name='conf1')
#    conf2 = Config(od, name='conf2')
#    mix = MixConfig(od, [conf1, conf2])
#    mix.property.read_write()
#    with pytest.raises(ConfigError):
#        conf1.value.dict()
#
#
#
#def test_mix_callback():
#    val1 = StrOption('val1', "", 'val')
#    val2 = StrOption('val2', "", Calculation(return_value, Params(ParamOption(val1))))
#    val3 = StrOption('val3', "", Calculation(return_value, Params(ParamValue('yes'))))
#    val4 = StrOption('val4', "", Calculation(return_value, Params(kwargs={'value': ParamOption(val1)})))
#    val5 = StrOption('val5', "", Calculation(return_value, Params(kwargs={'value': ParamValue('yes')})))
#    maconfig = OptionDescription('rootconfig', '', [val1, val2, val3, val4, val5])
#    cfg = Config(maconfig, name='cfg')
#    mix = MixConfig(maconfig, [cfg])
#    mix.property.read_write()
#    newcfg = mix.config('cfg')
#    assert newcfg.value.dict() == {'val3': 'yes', 'val2': 'val', 'val1': 'val', 'val5': 'yes', 'val4': 'val'}
#    newcfg.option('val1').value.set('new')
#    assert newcfg.value.dict() == {'val3': 'yes', 'val2': 'new', 'val1': 'new', 'val5': 'yes', 'val4': 'new'}
#    newcfg.option('val1').value.reset()
#    mix.option('val1').value.set('new')
#    assert newcfg.value.dict() == {'val3': 'yes', 'val2': 'new', 'val1': 'new', 'val5': 'yes', 'val4': 'new'}
#    newcfg.option('val4').value.set('new1')
#    assert newcfg.value.dict() == {'val3': 'yes', 'val2': 'new', 'val1': 'new', 'val5': 'yes', 'val4': 'new1'}
#    newcfg.option('val4').value.reset()
#    mix.option('val4').value.set('new1')
#    assert newcfg.value.dict() == {'val3': 'yes', 'val2': 'new', 'val1': 'new', 'val5': 'yes', 'val4': 'new1'}
#    mix.option('val4').value.reset()
#
#
#def test_mix_callback_follower():
#    val = StrOption('val', "", default='val')
#    val1 = StrOption('val1', "", [Calculation(return_value, Params(ParamOption(val)))], multi=True)
#    val3 = StrOption('val2', "", Calculation(return_value, Params(ParamOption(val1))), multi=True)
#    val4 = StrOption('val3', "", Calculation(return_value, Params(ParamOption(val1))), multi=True)
#    interface1 = Leadership('val1', '', [val1, val3, val4])
#    od = OptionDescription('root', '', [interface1])
#    maconfig = OptionDescription('rootconfig', '', [val, interface1])
#    cfg = Config(maconfig, name='cfg1')
#    mix = MixConfig(maconfig, [cfg])
#    mix.property.read_write()
#    newcfg1 = mix.config('cfg1')
#    assert newcfg1.value.dict() == {'val': 'val', 'val1.val1': [{'val1.val1': 'val', 'val1.val2': 'val', 'val1.val3': 'val'}]}
#    #
#    newcfg1.option('val').value.set('val1')
#    assert newcfg1.value.dict() == {'val': 'val1', 'val1.val1': [{'val1.val1': 'val1', 'val1.val2': 'val1', 'val1.val3': 'val1'}]}
#    #
#    newcfg1.option('val').value.reset()
#    mix.option('val').value.set('val1')
#    assert newcfg1.value.dict() == {'val': 'val1', 'val1.val1': [{'val1.val1': 'val1', 'val1.val2': 'val1', 'val1.val3': 'val1'}]}
#    #
#    mix.option('val').value.reset()
#    newcfg1.option('val1.val2', 0).value.set('val2')
#    assert newcfg1.value.dict() == {'val': 'val', 'val1.val1': [{'val1.val1': 'val', 'val1.val2': 'val2', 'val1.val3': 'val'}]}
#    #
#    newcfg1.option('val1.val2', 0).value.reset()
#    assert newcfg1.value.dict() == {'val': 'val', 'val1.val1': [{'val1.val1': 'val', 'val1.val2': 'val', 'val1.val3': 'val'}]}
#    #
#    mix.option('val1.val2', 0).value.set('val2')
#    assert newcfg1.value.dict() == {'val': 'val', 'val1.val1': [{'val1.val1': 'val', 'val1.val2': 'val2', 'val1.val3': 'val'}]}
#    #
#    mix.option('val1.val1').value.set(['val'])
#    assert newcfg1.value.dict() == {'val': 'val', 'val1.val1': [{'val1.val1': 'val', 'val1.val2': 'val2', 'val1.val3': 'val'}]}
#    #
#    newcfg1.option('val1.val3', 0).value.set('val6')
#    assert newcfg1.value.dict() == {'val': 'val', 'val1.val1': [{'val1.val1': 'val', 'val1.val2': 'val2', 'val1.val3': 'val6'}]}
#    #
#    mix.option('val1.val2', 0).value.reset()
#    newcfg1.option('val1.val3', 0).value.reset()
#    newcfg1.option('val1.val1').value.set(['val3'])
#    assert newcfg1.value.dict() == {'val': 'val', 'val1.val1': [{'val1.val1': 'val3', 'val1.val2': 'val3', 'val1.val3': 'val3'}]}
#    #
#    newcfg1.option('val1.val1').value.reset()
#    assert newcfg1.value.dict() == {'val': 'val', 'val1.val1': [{'val1.val1': 'val', 'val1.val2': 'val', 'val1.val3': 'val'}]}
#    #
#    mix.option('val1.val1').value.set(['val3'])
#    assert newcfg1.value.dict() == {'val': 'val', 'val1.val1': [{'val1.val1': 'val3', 'val1.val2': 'val3', 'val1.val3': 'val3'}]}
#    #
#    newcfg1.option('val1.val2', 0).value.set('val2')
#    assert newcfg1.value.dict() == {'val': 'val', 'val1.val1': [{'val1.val1': 'val3', 'val1.val2': 'val2', 'val1.val3': 'val3'}]}
#    #
#    mix.option('val1.val1').value.set(['val3', 'rah'])
#    assert newcfg1.value.dict() == {'val': 'val', 'val1.val1': [{'val1.val1': 'val3', 'val1.val2': 'val2', 'val1.val3': 'val3'}, {'val1.val1': 'rah', 'val1.val2': 'rah', 'val1.val3': 'rah'}]}
#    #
#    mix.option('val1.val1').value.pop(1)
#    mix.option('val1.val1').value.set(['val4'])
#    assert newcfg1.value.dict() == {'val': 'val', 'val1.val1': [{'val1.val1': 'val4', 'val1.val2': 'val2', 'val1.val3': 'val4'}]}
#
#
#def test_meta_reset():
#    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip", multi=True)
#    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "mask", multi=True, properties=('hidden',))
#    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    od0 = OptionDescription('root', '', [interface1])
#    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip", multi=True)
#    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "mask", multi=True, properties=('hidden',))
#    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    od1 = OptionDescription('root', '', [interface1])
#    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip", multi=True)
#    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "mask", multi=True, properties=('hidden',))
#    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    od2 = OptionDescription('root', '', [interface1])
#    conf1 = Config(od0, name='conf1')
#    conf2 = Config(od1, name='conf2')
#    mix = MixConfig(od2, [conf1, conf2])
#    mix.property.read_write()
#    mix.owner.set('mix1')
#    assert mix.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    newconf1 = mix.config('conf1')
#    newconf2 = mix.config('conf2')
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    errors = mix.value.set('ip_admin_eth0.ip_admin_eth0', ['192.168.1.1'])
#    assert len(errors) == 0
#    assert mix.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.1']
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.1']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.1']
#    newconf1.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.2'])
#    assert mix.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.1']
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.2']
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.1']
#    mix.value.reset('ip_admin_eth0.ip_admin_eth0')
#    assert mix.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf1.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert newconf2.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#
#
#def test_mix_properties_mix_copy():
#    ip_admin_eth0 = NetworkOption('ip_admin_eth0', "ip", multi=True, default=['192.168.1.1'])
#    netmask_admin_eth0 = NetmaskOption('netmask_admin_eth0', "mask", multi=True, properties=('disabled',))
#    interface0 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    ip_admin_eth0 = NetworkOption('ip_admin_eth0', "ip", multi=True, default=['192.168.1.1'])
#    netmask_admin_eth0 = NetmaskOption('netmask_admin_eth0', "mask", multi=True, properties=('disabled',))
#    interface1 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    ip_admin_eth0 = NetworkOption('ip_admin_eth0', "ip", multi=True, default=['192.168.1.1'])
#    netmask_admin_eth0 = NetmaskOption('netmask_admin_eth0', "mask", multi=True, properties=('disabled',))
#    interface2 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    conf1 = Config(interface0, name='conf1')
#    conf2 = Config(interface1, name='conf2')
#    conf1.property.read_write()
#    conf2.property.read_write()
#    mix = MixConfig(interface2, [conf1, conf2], name='mix1')
#    mix.property.read_write()
#
#    newconf1 = mix.config('conf1')
#    conf3 = newconf1.config.copy(name='conf3')
#    newconf3 = mix.config('conf3')
#    mix2 = list(conf3.config.parents())
#    assert len(mix2) == 1
#    assert mix.config.name() == mix2[0].config.name()
#
#    newconf2 = mix.config('conf2')
#    assert newconf1.value.dict() == {'ip_admin_eth0': ['192.168.1.1']}
#    assert conf2.value.dict() == {'ip_admin_eth0': ['192.168.1.1']}
#    assert newconf3.value.dict() == {'ip_admin_eth0': ['192.168.1.1']}
#    mix.option('ip_admin_eth0').value.set(['192.168.1.2'])
#    assert newconf1.value.dict() == {'ip_admin_eth0': ['192.168.1.2']}
#    assert conf2.value.dict() == {'ip_admin_eth0': ['192.168.1.2']}
#    assert newconf3.value.dict() == {'ip_admin_eth0': ['192.168.1.2']}
#    ret = mix.value.set('ip_admin_eth0', ['192.168.1.3'], force_default_if_same=True)
#    assert newconf1.value.dict() == {'ip_admin_eth0': ['192.168.1.3']}
#    assert conf2.value.dict() == {'ip_admin_eth0': ['192.168.1.3']}
#    assert newconf3.value.dict() == {'ip_admin_eth0': ['192.168.1.3']}
#
#
#def test_mix_properties_mix_deepcopy():
#    ip_admin_eth0 = NetworkOption('ip_admin_eth0', "ip", multi=True, default=['192.168.1.1'])
#    netmask_admin_eth0 = NetmaskOption('netmask_admin_eth0', "mask", multi=True,
#                                       properties=('disabled',))
#    interface0 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    ip_admin_eth0 = NetworkOption('ip_admin_eth0', "ip", multi=True, default=['192.168.1.1'])
#    netmask_admin_eth0 = NetmaskOption('netmask_admin_eth0', "mask", multi=True,
#                                       properties=('disabled',))
#    interface1 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    ip_admin_eth0 = NetworkOption('ip_admin_eth0', "ip", multi=True, default=['192.168.1.1'])
#    netmask_admin_eth0 = NetmaskOption('netmask_admin_eth0', "mask", multi=True,
#                                       properties=('disabled',))
#    interface2 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    conf1 = Config(interface0, name='conf1')
#    conf2 = Config(interface1, name='conf2')
#    conf1.property.read_write()
#    conf2.property.read_write()
#    mix = MixConfig(interface2, [conf1, conf2])
#    mix.permissive.add('hidden')
#    mix.property.read_write()
#
#    newconf1 = mix.config('conf1')
#    newconf2 = mix.config('conf2')
#    mix2 = newconf1.config.deepcopy(name='conf3')
#    newconf3 = mix2.config('conf3')
#    assert mix != mix2
#    assert mix.permissive.get() == mix2.permissive.get()
#
#    assert newconf1.value.dict() == {'ip_admin_eth0': ['192.168.1.1']}
#    assert newconf2.value.dict() == {'ip_admin_eth0': ['192.168.1.1']}
#    assert newconf3.value.dict() == {'ip_admin_eth0': ['192.168.1.1']}
#    mix.option('ip_admin_eth0').value.set(['192.168.1.2'])
#    assert newconf1.value.dict() == {'ip_admin_eth0': ['192.168.1.2']}
#    assert newconf2.value.dict() == {'ip_admin_eth0': ['192.168.1.2']}
#    assert newconf3.value.dict() == {'ip_admin_eth0': ['192.168.1.1']}
#    mix.value.set('ip_admin_eth0', ['192.168.1.3'], force_default_if_same=True)
#    assert newconf1.value.dict() == {'ip_admin_eth0': ['192.168.1.3']}
#    assert newconf2.value.dict() == {'ip_admin_eth0': ['192.168.1.3']}
#    assert newconf3.value.dict() == {'ip_admin_eth0': ['192.168.1.1']}
#
#
#def test_mix_properties_submix_deepcopy():
#    ip_admin_eth0 = NetworkOption('ip_admin_eth0', "ip", multi=True, default=['192.168.1.1'])
#    netmask_admin_eth0 = NetmaskOption('netmask_admin_eth0', "mask", multi=True,
#                                       properties=('disabled',))
#    interface0 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    ip_admin_eth0 = NetworkOption('ip_admin_eth0', "ip", multi=True, default=['192.168.1.1'])
#    netmask_admin_eth0 = NetmaskOption('netmask_admin_eth0', "mask", multi=True,
#                                       properties=('disabled',))
#    interface1 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    ip_admin_eth0 = NetworkOption('ip_admin_eth0', "ip", multi=True, default=['192.168.1.1'])
#    netmask_admin_eth0 = NetmaskOption('netmask_admin_eth0', "mask", multi=True,
#                                       properties=('disabled',))
#    interface2 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    conf1 = Config(interface0, name='conf1')
#    conf1.property.read_write()
#    mix1 = MixConfig(interface1, [conf1], name='mix1')
#    mix2 = MixConfig(interface2, [mix1], name='mix2')
#    mix_copy = conf1.config.deepcopy(name='conf2',
#                                           metaconfig_prefix='copy_')
#    assert mix_copy.config.name() == 'copy_mix2'
#    ret1 = mix_copy.config('copy_mix1')
#    assert ret1.config.name() == 'copy_mix1'
#    ret2 = mix_copy.config('copy_mix1.conf2')
#    assert ret2.config.name() == 'conf2'
#
#
#def test_mix_properties_submix_deepcopy_owner():
#    ip_admin_eth0 = NetworkOption('ip_admin_eth0', "ip")
#    netmask_admin_eth0 = NetmaskOption('netmask_admin_eth1', "mask")
#    interface0 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    ip_admin_eth0 = NetworkOption('ip_admin_eth1', "ip")
#    netmask_admin_eth0 = NetmaskOption('netmask_admin_eth0', "mask")
#    interface1 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    ip_admin_eth0 = NetworkOption('ip_admin_eth0', "ip")
#    netmask_admin_eth0 = NetmaskOption('netmask_admin_eth0', "mask")
#    interface2 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    conf1 = Config(interface0, name='conf1')
#    conf1.owner.set('conf1_user')
#    conf1.property.read_write()
#    mix1 = MixConfig(interface1, [conf1], name='mix1')
#    mix1.owner.set('mix1_user')
#    mix2 = MixConfig(interface2, [mix1], name='mix2')
#    mix2.owner.set('mix2_user')
#    #
#    conf1.option('ip_admin_eth0').value.set('192.168.0.1')
#    assert conf1.option('ip_admin_eth0').owner.get() == 'conf1_user'
#    mix2.option('ip_admin_eth0').value.set('192.168.0.3')
#    assert mix2.option('ip_admin_eth0').owner.get() == 'mix2_user'
#    #
#    mix2_copy = conf1.config.deepcopy(name='conf2',
#                                            metaconfig_prefix='copy_')
#    mix2_copy.option('netmask_admin_eth0').value.set('255.255.255.255')
#    assert mix2_copy.option('ip_admin_eth0').value.get() == '192.168.0.3'
#    assert mix2_copy.option('ip_admin_eth0').owner.get() == 'mix2_user'
#    assert mix2_copy.option('netmask_admin_eth0').owner.get() == 'mix2_user'
#    #
#    mix1_copy = mix2_copy.config('copy_mix1')
#    mix1_copy.option('netmask_admin_eth0').value.set('255.255.255.255')
#    #
#    conf2 = mix1_copy.config('conf2')
#    conf2.owner.set('conf2_user')
#    conf2.option('netmask_admin_eth1').value.set('255.255.255.255')
#    assert conf2.option('netmask_admin_eth1').owner.get() == 'conf2_user'
#    assert conf2.option('ip_admin_eth0').value.get() == '192.168.0.1'
#    assert conf2.option('ip_admin_eth0').owner.get() == 'conf1_user'
#
#
#def test_mix_properties_mix_set_value():
#    ip_admin_eth0 = NetworkOption('ip_admin_eth1', "ip", multi=True, default=['192.168.1.1'])
#    netmask_admin_eth0 = NetmaskOption('netmask_admin_eth0', "mask", multi=True, properties=('disabled',))
#    interface0 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    ip_admin_eth0 = NetworkOption('ip_admin_eth0', "ip", multi=True, default=['192.168.1.1'])
#    netmask_admin_eth0 = NetmaskOption('netmask_admin_eth1', "mask", multi=True, properties=('disabled',))
#    interface1 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    ip_admin_eth0 = NetworkOption('ip_admin_eth0', "ip", multi=True, default=['192.168.1.1'])
#    netmask_admin_eth0 = NetmaskOption('netmask_admin_eth0', "mask", multi=True, properties=('disabled',))
#    interface2 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    conf1 = Config(interface0, name='conf1')
#    conf2 = Config(interface1, name='conf2')
#    conf1.property.read_write()
#    conf2.property.read_write()
#    mix = MixConfig(interface2, [conf1, conf2])
#    mix.property.read_write()
#    newconf2 = mix.config('conf2')
#    assert newconf2.value.dict() == {'ip_admin_eth0': ['192.168.1.1']}
#    ret = mix.value.set('netmask_admin_eth0', ['255.255.255.255'], only_config=True)
#    assert len(ret) == 2
#    assert isinstance(ret[0], PropertiesOptionError)
#    assert isinstance(ret[1], AttributeError)
#    del ret[1]
#    del ret[0]
#    del ret
#    ret = mix.value.set('netmask_admin_eth0', ['255.255.255.255'], force_default=True)
#    assert len(ret) == 2
#    assert isinstance(ret[0], AttributeError)
#    assert isinstance(ret[1], PropertiesOptionError)
#    del ret[1]
#    del ret[0]
#    del ret
#    ret = mix.value.set('netmask_admin_eth0', ['255.255.255.255'], force_dont_change_value=True)
#    assert len(ret) == 3
#    assert isinstance(ret[0], PropertiesOptionError)
#    assert isinstance(ret[1], AttributeError)
#    assert isinstance(ret[2], PropertiesOptionError)
#    del ret[2]
#    del ret[1]
#    del ret[0]
#    del ret
#    ret = mix.value.set('netmask_admin_eth0', ['255.255.255.255'], force_default_if_same=True)
#    assert len(ret) == 2
#    assert isinstance(ret[0], AttributeError)
#    assert isinstance(ret[1], PropertiesOptionError)
#    del ret[1]
#    del ret[0]
#    del ret
#    ret = mix.value.set('ip_admin_eth0', '255.255.255.255', only_config=True)
#    assert len(ret) == 2
#    assert isinstance(ret[0], AttributeError)
#    assert isinstance(ret[1], ValueError)
#    del ret[1]
#    del ret[0]
#    del ret
#    ret = mix.value.set('ip_admin_eth0', '255.255.255.255', force_default=True)
#    assert len(ret) == 2
#    assert isinstance(ret[0], AttributeError)
#    assert isinstance(ret[1], ValueError)
#    del ret[1]
#    del ret[0]
#    del ret
#    ret = mix.value.set('ip_admin_eth0', '255.255.255.255', force_dont_change_value=True)
#    assert len(ret) == 2
#    assert isinstance(ret[0], AttributeError)
#    assert isinstance(ret[1], ValueError)
#    del ret[1]
#    del ret[0]
#    del ret
#    ret = mix.value.set('ip_admin_eth0', '255.255.255.255', force_default_if_same=True)
#    assert len(ret) == 2
#    assert isinstance(ret[0], AttributeError)
#    assert isinstance(ret[1], ValueError)
#    del ret[1]
#    del ret[0]
#    del ret
#
#
#def test_mix_different_default():
#    ip_admin_eth0 = NetworkOption('ip_admin_eth0', "ip", multi=True, default=['192.168.1.1'])
#    interface0 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0])
#    ip_admin_eth0 = NetworkOption('ip_admin_eth1', "ip", multi=True, default=['192.168.1.2'])
#    interface1 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0])
#    ip_admin_eth0 = NetworkOption('ip_admin_eth1', "ip", multi=True, default=['192.168.1.3'])
#    interface2 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0])
#    ip_admin_eth0 = NetworkOption('ip_admin_eth0', "ip", multi=True, default=['192.168.1.4'])
#    ip_admin_eth1 = NetworkOption('ip_admin_eth1', "ip", multi=True, default=['192.168.1.5'])
#    interface3 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0, ip_admin_eth1])
#    ip_admin_eth0 = NetworkOption('ip_admin_eth0', "ip", multi=True, default=['192.168.1.6'])
#    interface4 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0])
#    conf1 = Config(interface0, name='conf1')
#    conf1.property.read_write()
#    conf2 = Config(interface1, name='conf2')
#    conf2.property.read_write()
#    mix = MixConfig(interface2, [conf1, conf2], name='submix1')
#    mix = MixConfig(interface3, [mix], name='submix2')
#    mix = MixConfig(interface4, [mix])
#    mix.property.read_write()
#    #
#    assert mix.value.dict() == {'ip_admin_eth0': ['192.168.1.6']}
#    newsubmix2 = mix.config('submix2')
#    newsubmix1 = mix.config('submix2.submix1')
#    newconf1 = mix.config('submix2.submix1.conf1')
#    newconf2 = mix.config('submix2.submix1.conf2')
#    assert newsubmix2.value.dict() == {'ip_admin_eth0': ['192.168.1.4'], 'ip_admin_eth1': ['192.168.1.5']}
#    assert newsubmix1.value.dict() == {'ip_admin_eth1': ['192.168.1.3']}
#    assert newconf2.value.dict() == {'ip_admin_eth1': ['192.168.1.2']}
#    assert newconf1.value.dict() == {'ip_admin_eth0': ['192.168.1.1']}
#    #
#    mix.option('ip_admin_eth0').value.set(['192.168.1.7'])
#    assert mix.value.dict() == {'ip_admin_eth0': ['192.168.1.7']}
#    assert newsubmix2.value.dict() == {'ip_admin_eth0': ['192.168.1.7'], 'ip_admin_eth1': ['192.168.1.5']}
#    assert newsubmix1.value.dict() == {'ip_admin_eth1': ['192.168.1.3']}
#    assert newconf2.value.dict() == {'ip_admin_eth1': ['192.168.1.2']}
#    assert newconf1.value.dict() == {'ip_admin_eth0': ['192.168.1.7']}
#    #
#    newsubmix2.option('ip_admin_eth0').value.set(['192.168.1.8'])
#    assert mix.value.dict() == {'ip_admin_eth0': ['192.168.1.7']}
#    assert newsubmix2.value.dict() == {'ip_admin_eth0': ['192.168.1.8'], 'ip_admin_eth1': ['192.168.1.5']}
#    assert newsubmix1.value.dict() == {'ip_admin_eth1': ['192.168.1.3']}
#    assert newconf2.value.dict() == {'ip_admin_eth1': ['192.168.1.2']}
#    assert newconf1.value.dict() == {'ip_admin_eth0': ['192.168.1.8']}
#    #
#    with pytest.raises(AttributeError):
#        newsubmix1.option('ip_admin_eth0').value.set(['192.168.1.9'])
#    assert mix.value.dict() == {'ip_admin_eth0': ['192.168.1.7']}
#    assert newsubmix2.value.dict() == {'ip_admin_eth0': ['192.168.1.8'], 'ip_admin_eth1': ['192.168.1.5']}
#    assert newsubmix1.value.dict() == {'ip_admin_eth1': ['192.168.1.3']}
#    assert newconf2.value.dict() == {'ip_admin_eth1': ['192.168.1.2']}
#    assert newconf1.value.dict() == {'ip_admin_eth0': ['192.168.1.8']}
#    #
#    with pytest.raises(AttributeError):
#        newconf2.option('ip_admin_eth0').value.set(['192.168.1.9'])
#    assert mix.value.dict() == {'ip_admin_eth0': ['192.168.1.7']}
#    assert newsubmix2.value.dict() == {'ip_admin_eth0': ['192.168.1.8'], 'ip_admin_eth1': ['192.168.1.5']}
#    assert newsubmix1.value.dict() == {'ip_admin_eth1': ['192.168.1.3']}
#    assert newconf2.value.dict() == {'ip_admin_eth1': ['192.168.1.2']}
#    assert newconf1.value.dict() == {'ip_admin_eth0': ['192.168.1.8']}
#    #
#    newconf1.option('ip_admin_eth0').value.set(['192.168.1.9'])
#    assert mix.value.dict() == {'ip_admin_eth0': ['192.168.1.7']}
#    assert newsubmix2.value.dict() == {'ip_admin_eth0': ['192.168.1.8'], 'ip_admin_eth1': ['192.168.1.5']}
#    assert newsubmix1.value.dict() == {'ip_admin_eth1': ['192.168.1.3']}
#    assert newconf2.value.dict() == {'ip_admin_eth1': ['192.168.1.2']}
#    assert newconf1.value.dict() == {'ip_admin_eth0': ['192.168.1.9']}
#    #
#    with pytest.raises(AttributeError):
#        mix.option('ip_admin_eth1').value.set(['192.168.1.10'])
#    assert mix.value.dict() == {'ip_admin_eth0': ['192.168.1.7']}
#    assert newsubmix2.value.dict() == {'ip_admin_eth0': ['192.168.1.8'], 'ip_admin_eth1': ['192.168.1.5']}
#    assert newsubmix1.value.dict() == {'ip_admin_eth1': ['192.168.1.3']}
#    assert newconf2.value.dict() == {'ip_admin_eth1': ['192.168.1.2']}
#    assert newconf1.value.dict() == {'ip_admin_eth0': ['192.168.1.9']}
#    #
#    newsubmix2.option('ip_admin_eth1').value.set(['192.168.1.10'])
#    assert mix.value.dict() == {'ip_admin_eth0': ['192.168.1.7']}
#    assert newsubmix2.value.dict() == {'ip_admin_eth0': ['192.168.1.8'], 'ip_admin_eth1': ['192.168.1.10']}
#    assert newsubmix1.value.dict() == {'ip_admin_eth1': ['192.168.1.10']}
#    assert newconf2.value.dict() == {'ip_admin_eth1': ['192.168.1.10']}
#    assert newconf1.value.dict() == {'ip_admin_eth0': ['192.168.1.9']}
#    #
#    newsubmix1.option('ip_admin_eth1').value.set(['192.168.1.11'])
#    assert mix.value.dict() == {'ip_admin_eth0': ['192.168.1.7']}
#    assert newsubmix2.value.dict() == {'ip_admin_eth0': ['192.168.1.8'], 'ip_admin_eth1': ['192.168.1.10']}
#    assert newsubmix1.value.dict() == {'ip_admin_eth1': ['192.168.1.11']}
#    assert newconf2.value.dict() == {'ip_admin_eth1': ['192.168.1.11']}
#    assert newconf1.value.dict() == {'ip_admin_eth0': ['192.168.1.9']}
#    #
#    newconf2.option('ip_admin_eth1').value.set(['192.168.1.12'])
#    assert mix.value.dict() == {'ip_admin_eth0': ['192.168.1.7']}
#    assert newsubmix2.value.dict() == {'ip_admin_eth0': ['192.168.1.8'], 'ip_admin_eth1': ['192.168.1.10']}
#    assert newsubmix1.value.dict() == {'ip_admin_eth1': ['192.168.1.11']}
#    assert newconf2.value.dict() == {'ip_admin_eth1': ['192.168.1.12']}
#    assert newconf1.value.dict() == {'ip_admin_eth0': ['192.168.1.9']}
#    #
#    with pytest.raises(AttributeError):
#        newconf1.option('ip_admin_eth1').value.set(['192.168.1.13'])
#    assert mix.value.dict() == {'ip_admin_eth0': ['192.168.1.7']}
#    assert newsubmix2.value.dict() == {'ip_admin_eth0': ['192.168.1.8'], 'ip_admin_eth1': ['192.168.1.10']}
#    assert newsubmix1.value.dict() == {'ip_admin_eth1': ['192.168.1.11']}
#    assert newconf2.value.dict() == {'ip_admin_eth1': ['192.168.1.12']}
#    assert newconf1.value.dict() == {'ip_admin_eth0': ['192.168.1.9']}
#
#
#def test_mix_different_default_reset():
#    ip_admin_eth0 = NetworkOption('ip_admin_eth0', "ip", multi=True, default=['192.168.1.1'])
#    interface0 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0])
#    ip_admin_eth0 = NetworkOption('ip_admin_eth1', "ip", multi=True, default=['192.168.1.2'])
#    interface1 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0])
#    ip_admin_eth0 = NetworkOption('ip_admin_eth1', "ip", multi=True, default=['192.168.1.3'])
#    interface2 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0])
#    ip_admin_eth0 = NetworkOption('ip_admin_eth0', "ip", multi=True, default=['192.168.1.4'])
#    ip_admin_eth1 = NetworkOption('ip_admin_eth1', "ip", multi=True, default=['192.168.1.5'])
#    interface3 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0, ip_admin_eth1])
#    ip_admin_eth0 = NetworkOption('ip_admin_eth0', "ip", multi=True, default=['192.168.1.6'])
#    interface4 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0])
#    conf1 = Config(interface0, name='conf1')
#    conf1.property.read_write()
#    conf2 = Config(interface1, name='conf2')
#    conf2.property.read_write()
#    mix = MixConfig(interface2, [conf1, conf2], name='submix1')
#    mix = MixConfig(interface3, [mix], name='submix2')
#    mix = MixConfig(interface4, [mix])
#    mix.property.read_write()
#    #
#    mix.option('ip_admin_eth0').value.set(['192.168.1.7'])
#    submix2 = mix.config('submix2')
#    submix1 = mix.config('submix2.submix1')
#    conf1 = mix.config('submix2.submix1.conf1')
#    conf2 = mix.config('submix2.submix1.conf2')
#    submix2.option('ip_admin_eth0').value.set(['192.168.1.8'])
#    submix2.option('ip_admin_eth1').value.set(['192.168.1.10'])
#    submix1.option('ip_admin_eth1').value.set(['192.168.1.11'])
#    conf2.option('ip_admin_eth1').value.set(['192.168.1.12'])
#    conf1.option('ip_admin_eth0').value.set(['192.168.1.9'])
#    assert mix.value.dict() == {'ip_admin_eth0': ['192.168.1.7']}
#    assert submix2.value.dict() == {'ip_admin_eth0': ['192.168.1.8'], 'ip_admin_eth1': ['192.168.1.10']}
#    assert submix1.value.dict() == {'ip_admin_eth1': ['192.168.1.11']}
#    assert conf2.value.dict() == {'ip_admin_eth1': ['192.168.1.12']}
#    assert conf1.value.dict() == {'ip_admin_eth0': ['192.168.1.9']}
#    #
#    mix.value.reset('ip_admin_eth0')
#    assert mix.value.dict() == {'ip_admin_eth0': ['192.168.1.6']}
#    assert submix2.value.dict() == {'ip_admin_eth0': ['192.168.1.4'], 'ip_admin_eth1': ['192.168.1.10']}
#    assert submix1.value.dict() == {'ip_admin_eth1': ['192.168.1.11']}
#    assert conf2.value.dict() == {'ip_admin_eth1': ['192.168.1.12']}
#    assert conf1.value.dict() == {'ip_admin_eth0': ['192.168.1.1']}
#    #
#    mix.value.reset('ip_admin_eth1')
#    assert mix.value.dict() == {'ip_admin_eth0': ['192.168.1.6']}
#    assert submix2.value.dict() == {'ip_admin_eth0': ['192.168.1.4'], 'ip_admin_eth1': ['192.168.1.5']}
#    assert submix1.value.dict() == {'ip_admin_eth1': ['192.168.1.3']}
#    assert conf2.value.dict() == {'ip_admin_eth1': ['192.168.1.2']}
#    assert conf1.value.dict() == {'ip_admin_eth0': ['192.168.1.1']}
#
#
#def test_mix_pop_config():
#    od = make_description()
#    config1 = Config(od, name='config1')
#    config2 = Config(od, name='config2')
#    mix = MixConfig(od, [config1, config2])
#    mix.option('od1.i1').value.set(2)
#    #
#    assert len(list(mix.config.list())) == 2
#    newconfig1 = mix.config('config1')
#    assert newconfig1.value.dict() == {'od1.i1': 2, 'od1.i2': 1, 'od1.i3': None, 'od1.i4': 2, 'od1.i5': [2], 'od1.i6': None}
#    newconf1 = mix.config.remove('config1')
#    try:
#        mix.config('config1')
#    except ConfigError:
#        pass
#    else:
#        raise Exception('must raise')
#    assert newconf1.value.dict() == {'od1.i1': None, 'od1.i2': 1, 'od1.i3': None, 'od1.i4': 2, 'od1.i5': [2], 'od1.i6': None}
#    #
#    assert len(list(mix.config.list())) == 1
#    with pytest.raises(ConfigError):
#        mix.config.remove('newconf1')
#
#
#def test_mix_add_config():
#    od = make_description()
#    config1 = Config(od, name='config1')
#    config2 = Config(od, name='config2')
#    mix = MixConfig(od, [config1, config2])
#    mix.option('od1.i1').value.set(2)
#    #
#    assert len(list(mix.config.list())) == 2
#    config = Config(od, name='new')
#    assert config.value.dict() == {'od1.i1': None, 'od1.i2': 1, 'od1.i3': None, 'od1.i4': 2, 'od1.i5': [2], 'od1.i6': None}
#    mix.config.add(config)
#    #
#    assert len(list(mix.config.list())) == 3
#    assert config.value.dict() == {'od1.i1': 2, 'od1.i2': 1, 'od1.i3': None, 'od1.i4': 2, 'od1.i5': [2], 'od1.i6': None}
#    #
#    with pytest.raises(ConflictError):
#        mix.config.add(config)
#
#
#def test_mix_add_config_readd():
#    od = make_description()
#    mix = MixConfig(od, [])
#    mix2 = MixConfig(od, [])
#    #
#    config = Config(od, name='new')
#    mix.config.add(config)
#    mix2.config.add(config)
#    assert len(list(config.config.parents())) == 2
#
#
#def test_mix_new_config_readd():
#    od = make_description()
#    mix = MixConfig(od, [])
#    assert len(list(mix.config.list())) == 0
#    mix2 = mix.config.new('mix2')
#    assert len(list(mix.config.list())) == 1
#
#
#def test_meta_new_mixconfig():
#    od = make_description()
#    cfg = Config(od, name='cfg1')
#    meta = MetaConfig([cfg])
#    mix = meta.config.new('mixconfig', type="mixconfig")
#    assert isinstance(mix, MixConfig)
#
#
#def test_meta_mixconfig_parents():
#    od = make_description()
#    cfg = Config(od, name='cfg1')
#    meta = MetaConfig([cfg])
#    mix = meta.config.new('mixconfig', type="mixconfig")
#    parents = mix.config.parents()
#    assert len(parents) == 1
##    assert parents[0].config.get() == meta
