# coding: utf-8
from .autopath import do_autopath
do_autopath()
import pytest
import warnings


from tiramisu.setting import groups, owners
from tiramisu import StrOption, IntOption, OptionDescription, submulti, Leadership, Config, \
                     MetaConfig, Params, ParamOption, Calculation
from tiramisu.error import LeadershipError, PropertiesOptionError


def return_val(val=None):
    if val is None:
        return 'val'
    else:
        return val


def return_list(value=None):
    return ['val', 'val']


def return_list2(value=None):
    return [['val', 'val']]


def test_unknown_multi():
    with pytest.raises(ValueError):
        StrOption('multi', '', multi='unknown')


def test_submulti():
    multi = StrOption('multi', '', multi=submulti)
    multi2 = StrOption('multi2', '', default_multi=['yes'], multi=submulti)
    multi3 = StrOption('multi3', '', default=[['yes']], multi=submulti)
    od1 = OptionDescription('od', '', [multi, multi2, multi3])
    cfg = Config(od1)
    assert cfg.option('multi').ismulti()
    assert cfg.option('multi').issubmulti()
    assert cfg.option('multi').owner.get() == owners.default
    assert cfg.option('multi').value.get() == []
    assert cfg.option('multi').owner.get() == owners.default
    assert cfg.option('multi').owner.get() == owners.default
    assert cfg.option('multi3').value.get() == [['yes']]
    assert cfg.option('multi').owner.get() == owners.default
#    assert not list_sessions()


def test_submulti_mandatory():
    multi = StrOption('multi', '', multi=submulti, properties=('mandatory',))
    od1 = OptionDescription('od', '', [multi])
    cfg = Config(od1)
    cfg.property.read_only()
    with pytest.raises(PropertiesOptionError):
        cfg.option('multi').value.get()
    #
    cfg.property.read_write()
    cfg.option('multi').value.set([['val']])
    cfg.property.read_only()
    assert cfg.option('multi').value.get() == [['val']]
    #
    cfg.property.read_write()
    cfg.option('multi').value.set([['val'], ['']])
    cfg.property.read_only()
    with pytest.raises(PropertiesOptionError):
        cfg.option('multi').value.get()
    #
    cfg.property.read_write()
    cfg.option('multi').value.set([['val'], [None]])
    cfg.property.read_only()
    with pytest.raises(PropertiesOptionError):
        cfg.option('multi').value.get()
    #
    cfg.property.read_write()
    cfg.option('multi').value.set([['val'], []])
    cfg.property.read_only()
    with pytest.raises(PropertiesOptionError):
        cfg.option('multi').value.get()
    #
    cfg.property.read_write()
    cfg.option('multi').value.set([['val'], ['val1', '']])
    cfg.property.read_only()
    with pytest.raises(PropertiesOptionError):
        cfg.option('multi').value.get()
    #
    cfg.property.read_write()
    cfg.option('multi').value.set([['val'], ['val1', '', 'val2']])
    cfg.property.read_only()
    with pytest.raises(PropertiesOptionError):
        cfg.option('multi').value.get()
#    assert not list_sessions()


def test_submulti_default_multi_not_list():
    with pytest.raises(ValueError):
        StrOption('multi2', '', default_multi='yes', multi=submulti)


def test_append_submulti():
    multi = StrOption('multi', '', multi=submulti)
    multi2 = StrOption('multi2', '', default_multi=['yes'], multi=submulti)
    multi3 = StrOption('multi3', '', default=[['yes']], multi=submulti)
    od1 = OptionDescription('od', '', [multi, multi2, multi3])
    cfg = Config(od1)
    owner = cfg.owner.get()
    assert cfg.option('multi').value.get() == []
    assert cfg.option('multi').owner.get() == owners.default
    cfg.option('multi').value.set([[]])
    assert cfg.option('multi').owner.get() == owner
    assert cfg.option('multi').value.get() == [[]]
    cfg.option('multi').value.set([[], ['no']])
    assert cfg.option('multi').value.get() == [[], ['no']]
    #
    assert cfg.option('multi2').value.get() == []
    assert cfg.option('multi2').owner.get() == owners.default
    cfg.option('multi2').value.set([cfg.option('multi2').value.defaultmulti()])
    assert cfg.option('multi2').owner.get() == owner
    assert cfg.option('multi2').value.get() == [['yes']]
    cfg.option('multi2').value.set([cfg.option('multi2').value.defaultmulti(), ['no']])
    assert cfg.option('multi2').value.get() == [['yes'], ['no']]
    #
    assert cfg.option('multi3').value.get() == [['yes']]
    assert cfg.option('multi3').owner.get() == owners.default
    cfg.option('multi3').value.set([cfg.option('multi2').value.defaultmulti(), []])
    assert cfg.option('multi3').owner.get() == owner
    assert cfg.option('multi3').value.get() == [['yes'], []]
    cfg.option('multi3').value.set([cfg.option('multi2').value.defaultmulti(), [], ['no']])
    assert cfg.option('multi3').value.get() == [['yes'], [], ['no']]
#    assert not list_sessions()


def test_append_unvalide_submulti():
    multi = StrOption('multi', '', multi=submulti)
    multi2 = StrOption('multi2', '', default_multi=['yes'], multi=submulti)
    multi3 = StrOption('multi3', '', default=[['yes']], multi=submulti)
    od1 = OptionDescription('od', '', [multi, multi2, multi3])
    cfg = Config(od1)
    assert cfg.option('multi').value.get() == []
    assert cfg.option('multi').owner.get() == owners.default
    with pytest.raises(ValueError):
        cfg.option('multi').value.set([[1]])
    assert cfg.option('multi').value.get() == []
    assert cfg.option('multi').owner.get() == owners.default
    #
    assert cfg.option('multi2').value.get() == []
    with pytest.raises(ValueError):
        cfg.option('multi2').value.set(['no'])
    assert cfg.option('multi').owner.get() == owners.default
    assert cfg.option('multi2').value.get() == []
    #
    assert cfg.option('multi3').value.get() == [['yes']]
    assert cfg.option('multi3').owner.get() == owners.default
    with pytest.raises(ValueError):
        cfg.option('multi3').value.set([[1]])
    assert cfg.option('multi3').value.get() == [['yes']]
    assert cfg.option('multi3').owner.get() == owners.default
#    assert not list_sessions()


def test_pop_submulti():
    multi = StrOption('multi', '', multi=submulti)
    multi2 = StrOption('multi2', '', default_multi=['yes'], multi=submulti)
    multi3 = StrOption('multi3', '', default=[['yes']], multi=submulti)
    od1 = OptionDescription('od', '', [multi, multi2, multi3])
    cfg = Config(od1)
    owner = cfg.owner.get()
    assert cfg.option('multi').value.get() == []
    assert cfg.option('multi3').owner.get() == owners.default
    cfg.option('multi').value.set([['no', 'yes'], ['peharps']])
    assert cfg.option('multi').owner.get() == owner
    assert cfg.option('multi').value.get() == [['no', 'yes'], ['peharps']]
    #
    assert cfg.option('multi3').value.get() == [['yes']]
    assert cfg.option('multi3').owner.get() == owners.default
    cfg.option('multi3').value.set([])
    assert cfg.option('multi').owner.get() == owner
    assert cfg.option('multi3').value.get() == []
    cfg.option('multi3').value.reset()
    assert cfg.option('multi3').owner.get() == owners.default
    cfg.option('multi3').value.set([[]])
    assert cfg.option('multi3').owner.get() == owner
    assert cfg.option('multi3').value.get() == [[]]
#    assert not list_sessions()


def test_callback_submulti_str():
    multi = StrOption('multi', '', [[Calculation(return_val)]], multi=submulti, default_multi=[Calculation(return_val)])
    od1 = OptionDescription('od', '', [multi])
    cfg = Config(od1)
    cfg.property.read_write()
    owner = cfg.owner.get()
    assert cfg.option('multi').owner.get() == owners.default
    assert cfg.option('multi').value.get() == [['val']]
    cfg.option('multi').value.set([['val'], cfg.option('multi').value.defaultmulti()])
    assert cfg.option('multi').owner.get() == owner
    assert cfg.option('multi').value.get() == [['val'], ['val']]
    cfg.option('multi').value.reset()
    assert cfg.option('multi').owner.get() == owners.default
#    assert not list_sessions()


def test_callback_submulti_list():
    multi = StrOption('multi', '', [Calculation(return_list)], multi=submulti, default_multi=Calculation(return_list), properties=('notunique',))
    od1 = OptionDescription('od', '', [multi])
    cfg = Config(od1)
    cfg.property.read_write()
    owner = cfg.owner.get()
    assert cfg.option('multi').value.get() == [['val', 'val']]
    assert cfg.option('multi').owner.get() == owners.default
    cfg.option('multi').value.set([['val', 'val'], cfg.option('multi').value.defaultmulti()])
    assert cfg.option('multi').owner.get() == owner
    assert cfg.option('multi').value.get() == [['val', 'val'], ['val', 'val']]
    cfg.option('multi').value.set([['val', 'val'], cfg.option('multi').value.defaultmulti(), cfg.option('multi').value.defaultmulti()])
    assert cfg.option('multi').value.get() == [['val', 'val'], ['val', 'val'], ['val', 'val']]
    cfg.option('multi').value.reset()
    assert cfg.option('multi').owner.get() == owners.default
#    assert not list_sessions()


def test_callback_submulti_list_list():
    multi = StrOption('multi', '', Calculation(return_list2), multi=submulti, properties=('notunique',))
    od1 = OptionDescription('od', '', [multi])
    cfg = Config(od1)
    cfg.property.read_write()
    owner = cfg.owner.get()
    assert cfg.option('multi').value.get() == [['val', 'val']]
    assert cfg.option('multi').owner.get() == owners.default
    cfg.option('multi').value.set([['val', 'val'], cfg.option('multi').value.defaultmulti()])
    assert cfg.option('multi').owner.get() == owner
    assert cfg.option('multi').value.get() == [['val', 'val'], []]
    cfg.option('multi').value.reset()
    assert cfg.option('multi').owner.get() == owners.default
#    assert not list_sessions()


def test_groups_with_leader_submulti():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=submulti)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    assert interface1.impl_get_group_type() == groups.leadership


def test_groups_with_leader_in_config_submulti():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=submulti)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('root', '', [interface1])
    cfg = Config(od1)
    assert interface1.impl_get_group_type() == groups.leadership
#    assert not list_sessions()


def test_values_with_leader_and_followers_submulti():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=submulti)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('toto', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    owner = cfg.owner.get()
    assert interface1.impl_get_group_type() == groups.leadership
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').owner.get() == owners.default
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(["192.168.230.145"])
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ["192.168.230.145"]
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == []
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').owner.get() == owner
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).owner.get() == owners.default
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(["192.168.230.145", "192.168.230.147"])
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == []
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.get() == []
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set(['255.255.255.0'])
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == ['255.255.255.0']
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.get() == []
    with pytest.raises(ValueError):
        cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('255.255.255.0')
    with pytest.raises(ValueError):
        cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set([['255.255.255.0']])
#    assert not list_sessions()


def test_values_with_leader_and_followers_submulti_mandatory():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=submulti, properties=('mandatory',))
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('toto', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_only()
    owner = cfg.owner.get()
    assert interface1.impl_get_group_type() == groups.leadership
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').owner.get() == owners.default
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
    #
    cfg.property.read_write()
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(["192.168.230.145"])
    cfg.property.read_only()
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ["192.168.230.145"]
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get()
    #
    cfg.property.read_write()
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set(["255.255.255.0"])
    cfg.property.read_only()
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == ["255.255.255.0"]
    #
    cfg.property.read_write()
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set(["255.255.255.0", None])
    cfg.property.read_only()
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get()
    #
    cfg.property.read_write()
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set(["255.255.255.0", ''])
    cfg.property.read_only()
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get()
    #
    cfg.property.read_write()
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set(["255.255.255.0", '', "255.255.255.0"])
    cfg.property.read_only()
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get()
#    assert not list_sessions()


def test_values_with_leader_and_followers_submulti_default_multi():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=submulti, default_multi=['255.255.0.0', '0.0.0.0'])
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('toto', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    owner = cfg.owner.get()
    assert interface1.impl_get_group_type() == groups.leadership
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').owner.get() == owners.default
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(["192.168.230.145"])
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ["192.168.230.145"]
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == ['255.255.0.0', '0.0.0.0']
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(["192.168.230.145", "192.168.230.147"])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set(['255.255.255.0'])
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == ['255.255.255.0']
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.get() == ['255.255.0.0', '0.0.0.0']
#    assert not list_sessions()


def test_reset_values_with_leader_and_followers_submulti():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=submulti)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('toto', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    owner = cfg.owner.get()
    assert interface1.impl_get_group_type() == groups.leadership
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').owner.get() == owners.default
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.230.145'])
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').owner.get() == owner
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).owner.get() == owners.default
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.reset()
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').owner.get() == owners.default
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
    #
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.230.145'])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set(['255.255.255.0'])
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').owner.get() == owner
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).owner.get() == owner
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.reset()
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').owner.get() == owners.default
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert not list_sessions()


def test_values_with_leader_and_followers_follower_submulti():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True, properties=('notunique',))
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=submulti)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('toto', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    with pytest.raises(LeadershipError):
        cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set(['255.255.255.0'])
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.230.145'])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set(['255.255.255.0'])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set(['255.255.255.0', '255.255.255.0'])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.reset()
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set(['255.255.255.0'])
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.230.145', '192.168.230.145'])
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == ['255.255.255.0']
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.get() == []
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set(['255.255.255.0'])
#    assert not list_sessions()


def test_values_with_leader_and_leadership_submulti():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True, properties=('notunique',))
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=submulti)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('toto', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(["192.168.230.145"])
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(["192.168.230.145", "192.168.230.145"])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set(['255.255.255.0'])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.set(['255.255.255.0'])
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == ['255.255.255.0']
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.get() == ['255.255.255.0']
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.pop(1)
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ["192.168.230.145"]
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == ['255.255.255.0']
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.reset()
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert not list_sessions()


def test_values_with_leader_owner_submulti():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=submulti)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('toto', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    owner = cfg.owner.get()
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').owner.get() == owners.default
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.230.145'])
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').owner.get() == owner
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).owner.get() == owners.default
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.reset()
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').owner.get() == owners.default
#    assert not list_sessions()


def test_values_with_leader_disabled_submulti():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True, properties=('notunique',))
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=submulti)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('toto', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.230.145'])
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.pop(0)
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.230.145'])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set(['192.168.230.145'])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.reset()
    cfg.option('ip_admin_eth0.netmask_admin_eth0').property.add('disabled')
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.230.145', '192.168.230.145'])
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.pop(1)
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.pop(0)

    #delete with value in disabled var
    cfg.unrestraint.option('ip_admin_eth0.netmask_admin_eth0').property.remove('disabled')
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.230.145'])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set(['192.168.230.145'])
    cfg.unrestraint.option('ip_admin_eth0.netmask_admin_eth0').property.add('disabled')
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.pop(0)
#    assert not list_sessions()


def test_leader_is_submulti():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=submulti)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('toto', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    owner = cfg.owner.get()
    assert interface1.impl_get_group_type() == groups.leadership
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').owner.isdefault()
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set([["192.168.230.145"]])
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == [["192.168.230.145"]]
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == None
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').owner.get() == owner
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).owner.isdefault()
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set([["192.168.230.145"], ["192.168.230.147"]])
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == None
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.get() == None
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set([["192.168.230.145", '192.168.1.1'], ["192.168.230.147"]])
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == [["192.168.230.145", '192.168.1.1'], ["192.168.230.147"]]
    with pytest.raises(ValueError):
        cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.1', '192.168.1.1'])
#    assert not list_sessions()


def test_callback_submulti():
    multi = StrOption('multi', '', multi=submulti)
    multi2 = StrOption('multi2', '', Calculation(return_val, Params(ParamOption(multi))), multi=submulti)
    od1 = OptionDescription('multi', '', [multi, multi2])
    cfg = Config(od1)
    cfg.property.read_write()
    owner = cfg.owner.get()
    assert cfg.option('multi').owner.get() == owners.default
    assert cfg.option('multi').value.get() == []
    assert cfg.option('multi2').value.get() == []
    cfg.option('multi').value.set([['val']])
    assert cfg.option('multi').owner.get() == owner
    assert cfg.option('multi2').owner.get() == owners.default
    assert cfg.option('multi').value.get() == [['val']]
    assert cfg.option('multi2').value.get() == [['val']]
#    assert not list_sessions()


def test_callback_submulti_follower():
    multi = StrOption('multi', '', multi=True)
    multi2 = StrOption('multi2', '', Calculation(return_list), multi=submulti)
    od = Leadership('multi', '', [multi, multi2])
    od1 = OptionDescription('multi', '', [od])
    cfg = Config(od1)
    cfg.property.read_write()
    assert cfg.option('multi.multi').value.get() == []
    cfg.option('multi.multi').value.set(['val'])
    assert cfg.option('multi.multi2', 0).value.get() == ['val', 'val']
#    assert not list_sessions()


def test_submulti_unique():
    i = IntOption('int', '', multi=submulti, properties=('unique',))
    od1 = OptionDescription('od', '', [i])
    cfg = Config(od1)
    assert cfg.option('int').value.get() == []
    cfg.option('int').value.set([[0]])
    assert cfg.option('int').value.get() == [[0]]
    with pytest.raises(ValueError):
        cfg.option('int').value.set([[0, 0]])
    cfg.option('int').value.set([[0], [0]])
    with pytest.raises(ValueError):
        cfg.option('int').value.set([[1, 0, 2, 3, 4, 5, 6, 0, 7], [0]])
    cfg.option('int').value.set([[0, 4, 5, 6], [0]])
#    assert not list_sessions()


#def test_multi_submulti_meta():
#    multi = StrOption('multi', '', multi=submulti)
#    od1 = OptionDescription('od', '', [multi])
#    cfg = Config(od1, name='cfg')
#    cfg.property.read_write()
#    cfg2 = Config(od1)
#    cfg2.property.read_write()
#    meta = MetaConfig([cfg, cfg2])
#    meta.property.read_write()
#    meta.option('multi').value.set([['val']])
#    assert meta.option('multi').value.get() == [['val']]
#    newcfg = meta.config('cfg')
#    newcfg.option('multi').value.set([['val', None]])
#    assert cfg.option('multi').value.get() == [['val', None]]
#    newcfg = meta.config('cfg')
#    assert newcfg.option('multi').value.get() == [['val', None]]
#    assert meta.option('multi').value.get() == [['val']]
##    assert not list_sessions()
#
#
#def test_multi_submulti_meta_no_cache():
#    multi = StrOption('multi', '', multi=submulti)
#    multi = StrOption('multi', '', multi=submulti)
#    od1 = OptionDescription('od', '', [multi])
#    cfg = Config(od1, name='cfg')
#    cfg.property.read_write()
#    cfg2 = Config(od1)
#    cfg.property.read_write()
#    meta = MetaConfig([cfg, cfg2])
#    meta.property.read_write()
#    meta.property.remove('cache')
#    meta.option('multi').value.set([['val']])
#    assert meta.option('multi').value.get() == [['val']]
#    newcfg = meta.config('cfg')
#    newcfg.option('multi').value.set([['val', None]])
#    assert cfg.option('multi').value.get() == [['val', None]]
#    newcfg = meta.config('cfg')
#    assert newcfg.option('multi').value.get() == [['val', None]]
#    assert meta.option('multi').value.get() == [['val']]
##    assert not list_sessions()
