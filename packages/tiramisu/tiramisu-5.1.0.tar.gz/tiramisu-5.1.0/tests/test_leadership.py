# coding: utf-8
from .autopath import do_autopath
do_autopath()
from .config import config_type, get_config, value_list, global_owner, parse_od_get
import pytest

from tiramisu.setting import groups, owners
from tiramisu import ChoiceOption, BoolOption, IntOption, IPOption, NetworkOption, NetmaskOption, \
    StrOption, OptionDescription, Leadership, Config, Calculation, ParamValue, calc_value, Params
from tiramisu.error import LeadershipError, PropertiesOptionError, ConfigError


groups.addgroup('family')


def compare(calculated, expected):
    assert calculated == expected


def make_description():
    numero_etab = StrOption('numero_etab', "identifiant de l'établissement")
    nom_machine = StrOption('nom_machine', "nom de la machine", default="eoleng")
    nombre_interfaces = IntOption('nombre_interfaces', "nombre d'interfaces à activer",
                                  default=1)
    activer_proxy_client = BoolOption('activer_proxy_client', "utiliser un proxy",
                                      default=False)
    mode_conteneur_actif = BoolOption('mode_conteneur_actif', "le serveur est en mode conteneur",
                                      default=False)
    mode_conteneur_actif2 = BoolOption('mode_conteneur_actif2', "le serveur est en mode conteneur2",
                                       default=False, properties=('hidden',))

    adresse_serveur_ntp = StrOption('serveur_ntp', "adresse serveur ntp", multi=True)
    time_zone = ChoiceOption('time_zone', 'fuseau horaire du serveur',
                             ('Paris', 'Londres'), 'Paris')

    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé")
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau")

    leader = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    interface1 = OptionDescription('interface1', '', [leader])
    interface1.impl_set_group_type(groups.family)

    general = OptionDescription('general', '', [numero_etab, nom_machine,
                                nombre_interfaces, activer_proxy_client,
                                mode_conteneur_actif, mode_conteneur_actif2,
                                adresse_serveur_ntp, time_zone])
    general.impl_set_group_type(groups.family)
    new = OptionDescription('new', '', [], properties=('hidden',))
    new.impl_set_group_type(groups.family)
    creole = OptionDescription('creole', 'first tiramisu configuration', [general, interface1, new])
    descr = OptionDescription('baseconfig', 'baseconifgdescr', [creole])
    return descr


def test_base_config(config_type):
    od1 = make_description()
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    assert cfg.option('creole.general.activer_proxy_client').value.get() is False
    assert cfg.option('creole.general.nom_machine').value.get() == "eoleng"
#    if config_type != 'tiramisu-api':
#        ret = cfg.option.find('nom_machine', first=True)
#        assert ret.value.get() == "eoleng"
    assert parse_od_get(cfg.option('creole').value.get()) == {'creole.general.numero_etab': None, 'creole.general.nom_machine': 'eoleng', 'creole.general.nombre_interfaces': 1, 'creole.general.activer_proxy_client': False, 'creole.general.mode_conteneur_actif': False, 'creole.general.serveur_ntp': [], 'creole.general.time_zone': 'Paris', 'creole.interface1.ip_admin_eth0.ip_admin_eth0': None, 'creole.interface1.ip_admin_eth0.netmask_admin_eth0': None}
    if config_type == 'tiramisu-api':
        cfg.send()
#    assert not list_sessions()


def test_get_group_type():
    od1 = make_description()
    cfg = Config(od1)
    cfg.property.read_write()
    grp = cfg.option('creole.general')
    assert grp.group_type() == groups.family
    assert grp.group_type() == 'family'
    assert isinstance(grp.group_type(), groups.GroupType)
#    assert not list_sessions()
#
#
#def test_iter_on_groups():
#    od1 = make_description()
#    cfg = Config(od1)
#    cfg.property.read_write()
#    result = cfg.option('creole').list('optiondescription',
#                                       group_type=groups.family,
#                                       )
#    group_names = [res.name() for res in result]
#    assert group_names == ['general', 'interface1']
#    for i in cfg.option('creole').list('optiondescription',
#                                       group_type=groups.family,
#                                       ):
#        #test StopIteration
#        break
#    result = cfg.option('creole').list('option',
#                                       group_type=groups.family,
#                                       )
#    assert list(result) == []
#    result = cfg.option('creole.general').list('optiondescription',
#                                                group_type=groups.family,
#                                               )
#    assert list(result) == []
##    assert not list_sessions()

def test_list_recursive():
    od1 = make_description()
    cfg = Config(od1)
    cfg.property.read_write()
    result = cfg.option('creole').list()
    group_names = [res.name() for res in result]
    assert group_names == ['general', 'interface1']
    #
#    assert not list_sessions()


def test_iter_on_groups_force_permissive():
    od1 = make_description()
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.permissive.add('hidden')
    result = cfg.forcepermissive.option('creole.general').list()
    group_names = [res.name() for res in result]
    ass = ['numero_etab', 'nom_machine', 'nombre_interfaces',
           'activer_proxy_client', 'mode_conteneur_actif',
           'mode_conteneur_actif2', 'serveur_ntp', 'time_zone']
    assert group_names == ass
    # mode_conteneur_actif2 is not visible is not forcepermissive
    result = cfg.option('creole.general').list()
    group_names = [res.name() for res in result]
    ass.remove('mode_conteneur_actif2')
    assert group_names == ass
#    assert not list_sessions()


def test_iter_group_on_groups_force_permissive():
    od1 = make_description()
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.permissive.add('hidden')
    result = cfg.forcepermissive.option('creole').list()
    group_names = [res.name() for res in result]
    assert group_names == ['general', 'interface1', 'new']
#    assert not list_sessions()


def test_iter_on_groups_props():
    od1 = make_description()
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.option('creole.interface1').property.add('disabled')
    result = cfg.option('creole').list()
    group_names = [res.name() for res in result]
    assert group_names == ['general']
#    assert not list_sessions()


def test_iter_on_empty_group():
    od1 = OptionDescription("name", "descr", [])
    cfg = Config(od1)
    cfg.property.read_write()
    result = list(cfg.list())
    assert result == []
#    assert not list_sessions()


def test_groups_with_leader():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    assert interface1.impl_get_group_type() == groups.leadership
#    assert not list_sessions()


def test_groups_is_leader(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True, default_multi='value')
    interface1 = Leadership('leadership', '', [ip_admin_eth0, netmask_admin_eth0])
    var = StrOption('var', "ip réseau autorisé", multi=True)
    od2 = OptionDescription('od2', '', [var])
    od1 = OptionDescription('od', '', [interface1, od2])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert not cfg.option('od2').isleadership()
    assert cfg.option('leadership').isleadership()
    assert not cfg.option('od2.var').isleader()
    assert not cfg.option('od2.var').isfollower()
    assert cfg.option('leadership.ip_admin_eth0').ismulti()
    assert cfg.option('leadership.netmask_admin_eth0').ismulti()
    assert not cfg.option('leadership.ip_admin_eth0').issubmulti()
    assert not cfg.option('leadership.netmask_admin_eth0').issubmulti()
    assert cfg.option('leadership.ip_admin_eth0').isleader()
    assert not cfg.option('leadership.ip_admin_eth0').isfollower()
    assert not cfg.option('leadership.netmask_admin_eth0').isleader()
    assert cfg.option('leadership.netmask_admin_eth0').isfollower()
    assert cfg.option('leadership.netmask_admin_eth0').path() == 'leadership.netmask_admin_eth0'
    assert cfg.option('leadership.netmask_admin_eth0').value.defaultmulti() == 'value'
    if config_type == 'tiramisu-api':
        cfg.send()
#    assert not list_sessions()


def test_leader_list(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", ['val1'], multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True, default_multi='value')
    interface1 = Leadership('leadership', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('od', '', [interface1])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    ret = cfg.list()
    assert len(ret) == 1
    assert ret[0].name() == 'leadership'
    #
    ret = cfg.option('leadership').list()
    assert len(ret) == 2
    assert ret[0].name() == 'ip_admin_eth0'
    assert ret[1].name() == 'netmask_admin_eth0'
    assert ret[1].index() == 0
    #
    cfg.option('leadership.ip_admin_eth0').value.set(['a', 'b'])
    cfg.option('leadership.netmask_admin_eth0', 0).value.set('c')
    cfg.option('leadership.netmask_admin_eth0', 1).value.set('d')
    ret = cfg.option('leadership').list()
    assert ret[0].name() == 'ip_admin_eth0'
    assert ret[1].name() == 'netmask_admin_eth0'
#    assert ret[1].option.index() == 0
#    assert ret[2].option.name() == 'netmask_admin_eth0'
#    assert ret[2].option.index() == 1
#    assert len(ret) == 3
#    if config_type == 'tiramisu-api':
#        cfg.send()
##    assert not list_sessions()


def test_groups_is_multi_with_index(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", ['val'], multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True, default_multi='value')
    interface1 = Leadership('leadership', '', [ip_admin_eth0, netmask_admin_eth0])
    var = StrOption('var', "ip réseau autorisé", multi=True)
    od2 = OptionDescription('od2', '', [var])
    od1 = OptionDescription('od', '', [interface1, od2])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert cfg.option('leadership.netmask_admin_eth0', 0).ismulti()


def test_groups_is_information_with_index(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", ['val'], multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True, default_multi='value')
    interface1 = Leadership('leadership', '', [ip_admin_eth0, netmask_admin_eth0])
    var = StrOption('var', "ip réseau autorisé", multi=True)
    od2 = OptionDescription('od2', '', [var])
    od1 = OptionDescription('od', '', [interface1, od2])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    with pytest.raises(ConfigError):
        assert cfg.option('leadership.netmask_admin_eth0', 0).information.set('key', 'value')


def test_groups_with_leader_in_root():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    interface1
    with pytest.raises(ConfigError):
        Config(interface1)
#    assert not list_sessions()


def test_groups_with_leader_in_config():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('root', '', [interface1])
    cfg = Config(od1)
    assert interface1.impl_get_group_type() == groups.leadership
#    assert not list_sessions()


def test_groups_with_leader_make_dict(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('root', '', [interface1])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert parse_od_get(cfg.value.get()) == {'ip_admin_eth0.ip_admin_eth0': []}
    if config_type != 'tiramisu-api':
        # FIXME useful? already in leadership
        assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.len() == 0
        assert cfg.option('ip_admin_eth0.netmask_admin_eth0').value.len() == 0
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['ip1', 'ip2'])
    if config_type != 'tiramisu-api':
        # FIXME
        assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.len() == 2
        assert cfg.option('ip_admin_eth0.netmask_admin_eth0').value.len() == 2
    assert parse_od_get(cfg.value.get()) == {'ip_admin_eth0.ip_admin_eth0': [{'ip_admin_eth0.ip_admin_eth0': 'ip1', 'ip_admin_eth0.netmask_admin_eth0': None}, {'ip_admin_eth0.ip_admin_eth0': 'ip2', 'ip_admin_eth0.netmask_admin_eth0': None}]}
    if config_type == 'tiramisu-api':
        cfg.send()
#    assert not list_sessions()

def test_not_groups_len(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('root', '', [interface1])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    with pytest.raises(ConfigError):
        cfg.option('ip_admin_eth0.ip_admin_eth0').value.len()


def test_groups_with_leader_make_dict2(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = Leadership('other', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('root', '', [interface1])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert parse_od_get(cfg.value.get()) == {'other.ip_admin_eth0': []}
    if config_type != 'tiramisu-api':
        # FIXME useful? already in leadership
        assert cfg.option('other.ip_admin_eth0').value.len() == 0
        assert cfg.option('other.netmask_admin_eth0').value.len() == 0
    cfg.option('other.ip_admin_eth0').value.set(['ip1', 'ip2'])
    if config_type != 'tiramisu-api':
        # FIXME
        assert cfg.option('other.ip_admin_eth0').value.len() == 2
        assert cfg.option('other.netmask_admin_eth0').value.len() == 2
    assert parse_od_get(cfg.value.get()) == {'other.ip_admin_eth0': [{'other.ip_admin_eth0': 'ip1', 'other.netmask_admin_eth0': None}, {'other.ip_admin_eth0': 'ip2', 'other.netmask_admin_eth0': None}]}
    if config_type == 'tiramisu-api':
        cfg.send()
#    assert not list_sessions()


def test_groups_with_leader_default_value(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('root', '', [interface1])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.default() == []
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['ip1', 'ip2'])
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['ip1', 'ip2']
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.default() == []
    if config_type == 'tiramisu-api':
        cfg.send()
#    assert not list_sessions()


def test_groups_with_leader_default_value_2(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", ['ip1', 'ip2'], multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", default_multi='netmask1', multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('root', '', [interface1])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['ip1', 'ip2']
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.default() == ['ip1', 'ip2']
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['ip3', 'ip4'])
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['ip3', 'ip4']
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.default() == ['ip1', 'ip2']
    #
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == 'netmask1'
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.get() == 'netmask1'
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.default() == 'netmask1'
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.default() == 'netmask1'
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.set('netmask2')
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == 'netmask1'
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.get() == 'netmask2'
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.default() == 'netmask1'
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.default() == 'netmask1'
    if config_type == 'tiramisu-api':
        cfg.send()
#    assert not list_sessions()


def test_groups_with_leader_hidden_in_config():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True, properties=('hidden',))
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0], properties=('hidden',))
    od1 = OptionDescription('root', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.permissive.add('hidden')
    assert cfg.forcepermissive.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
    cfg.forcepermissive.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.1'])
    assert cfg.forcepermissive.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() is None
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_admin_eth0.ip_admin_eth0').value.get()
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get()
    assert parse_od_get(cfg.value.get()) == {}
#    assert not list_sessions()


def test_groups_with_leader_hidden_in_config2():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True, properties=('hidden',))
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('root', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.permissive.add('hidden')
    assert cfg.forcepermissive.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
    cfg.forcepermissive.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.1'])
    assert cfg.forcepermissive.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() is None
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.1']
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get()
#    assert not list_sessions()


def test_groups_with_leader_hidden_in_config3():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True, properties=('hidden',))
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('root', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.permissive.add('hidden')
    assert cfg.forcepermissive.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
    cfg.forcepermissive.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.1'])
    with pytest.raises(PropertiesOptionError):
        cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get()
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.reset()
    assert cfg.forcepermissive.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
    #del
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.1'])
    cfg.property.remove('hidden')
    assert cfg.forcepermissive.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() is None
    cfg.forcepermissive.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('255.255.255.0')
    assert cfg.forcepermissive.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == '255.255.255.0'
    cfg.property.add('hidden')
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.reset()
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.1'])
    cfg.property.remove('hidden')
    assert cfg.forcepermissive.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() is None
#    assert not list_sessions()


def test_groups_with_leader_reset_empty(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('root', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.reset()
    if config_type != 'tiramisu-api':
        with pytest.raises(LeadershipError):
            cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.reset()
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.1'])
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == None
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.reset()
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == None
    if config_type == 'tiramisu-api':
        cfg.send()
#    assert not list_sessions()


def test_groups_with_leader_index_mandatory(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('root', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.1'])
    # index not allowed for leader
    with pytest.raises(ConfigError):
        cfg.option('ip_admin_eth0.ip_admin_eth0', 0).value.get()
    # index is mandatory
    with pytest.raises(ConfigError):
        cfg.option('ip_admin_eth0.netmask_admin_eth0').value.reset()
    with pytest.raises(ConfigError):
        cfg.option('ip_admin_eth0.netmask_admin_eth0').value.get()


def test_groups_with_leader_reset_out_of_range(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('root', '', [interface1])
    cfg_ori = Config(od1)
    cfg_ori.property.read_write()
    cfg = get_config(cfg_ori, config_type)
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.1'])
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.forcepermissive.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('255.255.255.0')
    cfg = get_config(cfg_ori, config_type)
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.reset()
    if config_type != 'tiramisu-api':
        # FIXME
        with pytest.raises(LeadershipError):
            cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.reset()
        with pytest.raises(IndexError):
            cfg.option('ip_admin_eth0.ip_admin_eth0').value.pop(1)
    if config_type == 'tiramisu-api':
        cfg.send()
#    assert not list_sessions()


def test_allowed_groups():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    interface1
    with pytest.raises(ValueError):
        interface1.impl_set_group_type('toto')
#    assert not list_sessions()


def test_values_with_leader_disabled_leader(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('toto', '', [interface1])
    cfg_ori = Config(od1)
    cfg_ori.property.read_write()
    cfg = get_config(cfg_ori, config_type)
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.230.145'])
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.pop(0)
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.230.145'])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set("192.168.230.145")
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.reset()
    with pytest.raises(LeadershipError):
        cfg_ori.option('ip_admin_eth0.ip_admin_eth0').property.add('disabled')
    cfg_ori.option('ip_admin_eth0').property.add('disabled')
    cfg = get_config(cfg_ori, config_type)
    if config_type != 'tiramisu-api':
        # FIXME
        with pytest.raises(PropertiesOptionError):
            cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('192.168.230.145')
    if config_type == 'tiramisu-api':
        cfg.send()
#    assert not list_sessions()


def test_sub_group_in_leader_group():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    subgroup = OptionDescription("subgroup", '', [])
    with pytest.raises(ValueError):
        Leadership('ip_admin_eth0', '', [subgroup, ip_admin_eth0, netmask_admin_eth0])
#    assert not list_sessions()


def test_group_always_has_multis():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau")
    with pytest.raises(ValueError):
        Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    assert not list_sessions()


#____________________________________________________________
def test_values_with_leader_and_followers1(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('toto', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    owner = global_owner(cfg, config_type)
    cfg = get_config(cfg, config_type)
    assert interface1.impl_get_group_type() == groups.leadership
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').owner.isdefault()
    #
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(["192.168.230.145"])
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ["192.168.230.145"]
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() is None
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').owner.get() == owner
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).owner.isdefault()
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(["192.168.230.145", "192.168.230.147"])
    if config_type != 'tiramisu-api':
        # FIXME
        with pytest.raises(ConfigError):
            cfg.option('ip_admin_eth0.netmask_admin_eth0').value.set([None])
        with pytest.raises(ConfigError):
            cfg.option('ip_admin_eth0.netmask_admin_eth0').value.pop(0)
    if config_type == 'tiramisu-api':
        cfg.send()
#    assert not list_sessions()


def test_reset_values_with_leader_and_followers(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('toto', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    owner = global_owner(cfg, config_type)
    assert interface1.impl_get_group_type() == groups.leadership
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').owner.isdefault()
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(["192.168.230.145"])
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').owner.get() == owner
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).owner.isdefault()
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.reset()
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').owner.isdefault()
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
    #reset
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(["192.168.230.145"])
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.reset()
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').owner.isdefault()
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
#    assert not list_sessions()


def test_reset_values_with_leader_and_followers_default_value():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True, default=['192.168.230.145'])
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True, default=['255.255.255.0'])
    with pytest.raises(ValueError):
        Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    assert not list_sessions()


def test_reset_values_with_leader_and_followers_default(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True, default=['192.168.230.145'])
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('toto', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    owner = global_owner(cfg, config_type)
    cfg = get_config(cfg, config_type)
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').owner.isdefault()
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).owner.isdefault()

    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.230.146'])
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').owner.get() == owner
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).owner.isdefault()
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.reset()
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').owner.isdefault()
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).owner.isdefault()
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.230.145']
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set(None)

    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.230.146'])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('255.255.255.0')
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').owner.get() == owner
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).owner.get() == owner
    with pytest.raises(ConfigError):
        # index is mandatory
        cfg.option('ip_admin_eth0.netmask_admin_eth0').owner.get()
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.reset()
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').owner.isdefault()
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).owner.get() == owners.default
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.230.145']
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set(None)

    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('255.255.255.0')
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').owner.isdefault()
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).owner.get() == owner
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.reset()
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').owner.isdefault()
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).owner.isdefault()
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.230.145']
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set(None)
    if config_type == 'tiramisu-api':
        cfg.send()
#    assert not list_sessions()


def test_values_with_leader_and_followers_follower(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True, properties=('notunique',))
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('toto', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    if config_type != 'tiramisu-api':
        with pytest.raises(LeadershipError):
           cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('255.255.255.0')
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.230.145'])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('255.255.255.0')
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.reset()
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('255.255.255.0')
    #
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.230.145', '192.168.230.145'])
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == '255.255.255.0'
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.get() is None
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('255.255.255.0')
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.set('255.255.255.0')
    if config_type != 'tiramisu-api':
        # FIXME
        with pytest.raises(ConfigError):
            cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.pop(1)
    #reset
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.230.145',
                                                         '192.168.230.145',
                                                         '192.168.230.145'])
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.reset()
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
    if config_type == 'tiramisu-api':
        cfg.send()
#    assert not list_sessions()


def test_values_with_leader_and_followers_pop(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('toto', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.230.145'])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('255.255.255.0')
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.230.145', '192.168.230.146'])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.set('255.255.0.0')
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.230.145', '192.168.230.146']
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == '255.255.255.0'
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.get() == '255.255.0.0'
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.pop(0)
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.230.146']
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == '255.255.0.0'
    if config_type == 'tiramisu-api':
        cfg.send()
#    assert not list_sessions()


def test_values_with_leader_and_followers_leader(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True, properties=('notunique',))
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('toto', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(["192.168.230.145"])
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(["192.168.230.145"])
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(["192.168.230.145", "192.168.230.145"])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('255.255.255.0')
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.set('255.255.255.0')
    if config_type != 'tiramisu-api':
        with pytest.raises(LeadershipError):
            cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.230.145'])
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == '255.255.255.0'
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.get() == '255.255.255.0'
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.pop(1)
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ["192.168.230.145"]
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == '255.255.255.0'
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.reset()
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == []
    if config_type == 'tiramisu-api':
        cfg.send()
#    assert not list_sessions()


def test_values_with_leader_and_followers_leader_pop():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True, properties=('notunique',))
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('toto', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(["192.168.230.145", "192.168.230.146"])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.set('255.255.0.0')
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ["192.168.230.145", "192.168.230.146"]
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == None
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.get() == '255.255.0.0'
    compare(cfg.value.exportation(), {'ip_admin_eth0.ip_admin_eth0': {None: [['192.168.230.145', '192.168.230.146'], 'user']}, 'ip_admin_eth0.netmask_admin_eth0': {1: ['255.255.0.0', 'user']}})
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.pop(0)
    compare(cfg.value.exportation(), {'ip_admin_eth0.ip_admin_eth0': {None: [['192.168.230.146'], 'user']}, 'ip_admin_eth0.netmask_admin_eth0': {0: ['255.255.0.0', 'user']}})
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ["192.168.230.146"]
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == '255.255.0.0'
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.230.146', "192.168.230.145", "192.168.230.146", "192.168.230.147", "192.168.230.148", "192.168.230.149"])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 3).value.set('255.255.0.0')
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 4).value.set('255.255.0.0')
    compare(cfg.value.exportation(), {'ip_admin_eth0.ip_admin_eth0': {None: [['192.168.230.146', '192.168.230.145', '192.168.230.146', '192.168.230.147', '192.168.230.148', '192.168.230.149'], 'user']}, 'ip_admin_eth0.netmask_admin_eth0': {0: ['255.255.0.0', 'user'], 3: ['255.255.0.0', 'user'], 4: ['255.255.0.0', 'user']}})
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.pop(5)
    compare(cfg.value.exportation(), {'ip_admin_eth0.ip_admin_eth0': {None: [['192.168.230.146', '192.168.230.145', '192.168.230.146', '192.168.230.147', '192.168.230.148'], 'user']}, 'ip_admin_eth0.netmask_admin_eth0': {0: ['255.255.0.0', 'user'], 3: ['255.255.0.0', 'user'], 4: ['255.255.0.0', 'user']}})
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.pop(2)
    compare(cfg.value.exportation(), {'ip_admin_eth0.ip_admin_eth0': {None: [['192.168.230.146', '192.168.230.145', '192.168.230.147', '192.168.230.148'], 'user']}, 'ip_admin_eth0.netmask_admin_eth0': {0: ['255.255.0.0', 'user'], 2: ['255.255.0.0', 'user'], 3: ['255.255.0.0', 'user']}})
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.pop(2)
    compare(cfg.value.exportation(), {'ip_admin_eth0.ip_admin_eth0': {None: [['192.168.230.146', '192.168.230.145', '192.168.230.148'], 'user']}, 'ip_admin_eth0.netmask_admin_eth0': {0: ['255.255.0.0', 'user'], 2: ['255.255.0.0', 'user']}})
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.pop(2)
    compare(cfg.value.exportation(), {'ip_admin_eth0.ip_admin_eth0': {None: [['192.168.230.146', '192.168.230.145'], 'user']}, 'ip_admin_eth0.netmask_admin_eth0': {0: ['255.255.0.0', 'user']}})
#    assert not list_sessions()


def test_follower_unique():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True, properties=('unique',))
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('toto', '', [interface1])
    cfg = Config(od1)
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(["192.168.230.145", "192.168.230.146"])
    # unique property is removed for a follower
    assert not cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).property.get()
#    assert not list_sessions()


def test_values_with_leader_owner(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('toto', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    owner = cfg.owner.get()
    cfg = get_config(cfg, config_type)
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').owner.isdefault()
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(["192.168.230.145"])
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').owner.get() == owner
    assert cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).owner.isdefault()
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.pop(0)
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').owner.get() == owner
#    assert not list_sessions()


def test_values_with_leader_disabled(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('toto', '', [interface1])
    cfg_ori = Config(od1)
    cfg_ori.property.read_write()
    cfg = get_config(cfg_ori, config_type)
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(["192.168.230.145"])
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.pop(0)
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(["192.168.230.145"])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set("192.168.230.145")
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.pop(0)
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.option('ip_admin_eth0.netmask_admin_eth0').property.add('disabled')
    cfg = get_config(cfg_ori, config_type)
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(["192.168.230.145"])
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.pop(0)

    if config_type == 'tiramisu-api':
        cfg.send()
    #delete with value in disabled var
    cfg_ori.unrestraint.option('ip_admin_eth0.netmask_admin_eth0').property.remove('disabled')
    cfg = get_config(cfg_ori, config_type)
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(["192.168.230.145"])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set("192.168.230.145")
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.unrestraint.option('ip_admin_eth0.netmask_admin_eth0').property.add('disabled')
    cfg = get_config(cfg_ori, config_type)
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.pop(0)

    ##append with value in disabled var
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.unrestraint.option('ip_admin_eth0.netmask_admin_eth0').property.remove('disabled')
    cfg = get_config(cfg_ori, config_type)
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(["192.168.230.145"])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set("192.168.230.145")
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.unrestraint.option('ip_admin_eth0.netmask_admin_eth0').property.add('disabled')
    cfg = get_config(cfg_ori, config_type)
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(["192.168.230.145", '192.168.230.43'])
    if config_type == 'tiramisu-api':
        cfg.send()
#    assert not list_sessions()


def test_multi_non_valid_value(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    od1 = OptionDescription('toto', '', [ip_admin_eth0])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    cfg.option('ip_admin_eth0').value.set(['a'])
    with pytest.raises(ValueError):
        cfg.option('ip_admin_eth0').value.set([1])
    if config_type == 'tiramisu-api':
        cfg.send()
#    assert not list_sessions()


def test_multi_leader_default_follower(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", default_multi="255.255.255.0", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('toto', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.1'])
    assert cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.1']
    if config_type == 'tiramisu-api':
        cfg.send()
#    assert not list_sessions()


def test_groups_with_leader_get_modified_value():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True, properties=('notunique',))
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('toto', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    compare(cfg.value.exportation(), {})
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.1'])
    compare(cfg.value.exportation(), {'ip_admin_eth0.ip_admin_eth0': {None: [['192.168.1.1'], 'user']}})
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.set('255.255.255.255')
    compare(cfg.value.exportation(), {'ip_admin_eth0.ip_admin_eth0': {None: [['192.168.1.1'], 'user']}, 'ip_admin_eth0.netmask_admin_eth0': {0: ['255.255.255.255', 'user']}})
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.1', '192.168.1.1'])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.set('255.255.255.255')
    compare(cfg.value.exportation(), {'ip_admin_eth0.ip_admin_eth0': {None: [['192.168.1.1', '192.168.1.1'], 'user']}, 'ip_admin_eth0.netmask_admin_eth0': {0: ['255.255.255.255', 'user'], 1: ['255.255.255.255', 'user']}})
#    assert not list_sessions()


def test_groups_with_leader_importation(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('toto', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.value.importation({'ip_admin_eth0.ip_admin_eth0': {None: [['192.168.1.1', '192.168.1.0'], 'user']}, 'ip_admin_eth0.netmask_admin_eth0': {0: ['255.255.255.255', 'user'], 1: ['255.255.255.0', 'user']}})
    cfg = get_config(cfg, config_type)
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.1', '192.168.1.0']
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get() == '255.255.255.255'
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.get() == '255.255.255.0'
    cfg.option('ip_admin_eth0.ip_admin_eth0').owner.get() == 'user'
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).owner.get() == 'user'
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).owner.get() == 'user'
    if config_type == 'tiramisu-api':
        cfg.send()
#    assert not list_sessions()


def test_wrong_index():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True, default=['1.1.1.1'])
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od2 = OptionDescription('od', '', [interface1])
    od1 = OptionDescription('toto', '', [od2])
    cfg = Config(od1)
    cfg.property.read_write()
    assert cfg.option('od.ip_admin_eth0.ip_admin_eth0').get()
    with pytest.raises(ConfigError):
        cfg.option('od.ip_admin_eth0.ip_admin_eth0', 0).get()
    assert cfg.option('od.ip_admin_eth0.netmask_admin_eth0').get()
    assert cfg.option('od.ip_admin_eth0').get()
    with pytest.raises(ConfigError):
        cfg.option('od.ip_admin_eth0', 0).get()
    assert cfg.option('od').get()
    with pytest.raises(ConfigError):
        cfg.option('od', 0).get()
#    assert not list_sessions()


def test_without_leader_or_follower():
    with pytest.raises(ValueError):
        Leadership('ip_admin_eth0', '', [])
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True, default=['1.1.1.1'])
    with pytest.raises(ValueError):
        Leadership('ip_admin_eth0', '', [ip_admin_eth0])
    #empty optiondescription is allowed
    OptionDescription('ip_admin_eth0', '', [])
#    assert not list_sessions()


def test_leader_not_multi():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé")
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    with pytest.raises(ValueError):
        Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    assert not list_sessions()


def test_follower_not_multi():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau")
    with pytest.raises(ValueError):
        Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
#    assert not list_sessions()


def test_follower_force_store_value_none():
    ip_admin_eth0 = IPOption('ip_admin_eth0', "ip réseau autorisé", multi=True, default=['1.1.1.1'])
    netmask_admin_eth0 = NetmaskOption('netmask_admin_eth0', "masque du sous-réseau",  multi=True, properties=('force_store_value',))
    interface0 = Leadership('interface0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('od', '', [interface0])
    od2 = OptionDescription('toto', '', [od1])
    cfg = Config(od2)
    cfg.property.read_write()
    assert cfg.option('od.interface0.netmask_admin_eth0', 0).owner.isdefault()
#    assert not list_sessions()


def test_follower_force_store_value():
    ip_admin_eth0 = IPOption('ip_admin_eth0', "ip réseau autorisé", multi=True, default=['1.1.1.1'])
    netmask_admin_eth0 = NetmaskOption('netmask_admin_eth0', "masque du sous-réseau", default_multi='255.255.255.0', multi=True, properties=('force_store_value',))
    interface0 = Leadership('interface0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('od', '', [interface0])
    od2 = OptionDescription('toto', '', [od1])
    cfg = Config(od2)
    cfg.property.read_write()
    assert not cfg.option('od.interface0.netmask_admin_eth0', 0).owner.isdefault()
#    assert not list_sessions()


def test_follower_force_store_value_read_only():
    ip_admin_eth0 = IPOption('ip_admin_eth0', "ip réseau autorisé", multi=True, default=['1.1.1.1'])
    netmask_admin_eth0 = NetmaskOption('netmask_admin_eth0', "masque du sous-réseau", default_multi='255.255.255.0', multi=True, properties=('force_store_value',))
    interface0 = Leadership('interface0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('od', '', [interface0])
    od2 = OptionDescription('toto', '', [od1])
    cfg = Config(od2)
    cfg.property.read_only()
    assert not cfg.option('od.interface0.netmask_admin_eth0', 0).owner.isdefault()
#    assert not list_sessions()


def test_follower_force_store_value_reset():
    ip_admin_eth0 = IPOption('ip_admin_eth0', "ip réseau autorisé", multi=True, default=['1.1.1.1'])
    netmask_admin_eth0 = NetmaskOption('netmask_admin_eth0', "masque du sous-réseau", default_multi='255.255.255.0', multi=True, properties=('force_store_value',))
    interface0 = Leadership('interface0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('od', '', [interface0])
    od2 = OptionDescription('toto', '', [od1])
    cfg = Config(od2)
    cfg.property.read_write()
    cfg.option('od.interface0.ip_admin_eth0').value.set(['1.1.1.1', '192.168.0.0'])
    assert not cfg.option('od.interface0.netmask_admin_eth0', 0).owner.isdefault()
    assert not cfg.option('od.interface0.netmask_admin_eth0', 1).owner.isdefault()
    #
    cfg.option('od.interface0.netmask_admin_eth0', 1).value.reset()
    assert not cfg.option('od.interface0.netmask_admin_eth0', 1).owner.isdefault()
    #
    cfg.option('od.interface0.ip_admin_eth0').value.pop(0)
    cfg.option('od.interface0.ip_admin_eth0').value.pop(0)
    assert cfg.option('od.interface0.ip_admin_eth0').value.get() == []
    cfg.option('od.interface0.ip_admin_eth0').value.reset()
    assert not cfg.option('od.interface0.netmask_admin_eth0', 0).owner.isdefault()
#    assert not list_sessions()


#def test_follower_properties():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True, properties=('aproperty',))
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('toto', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['1.1.1.1', '192.168.0.0'])
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).property.get() == ('aproperty',)
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).property.get() == ('aproperty',)
    #
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).property.add('newproperty')
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).property.get() == ('aproperty', 'newproperty')
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).property.get() == ('aproperty',)
    #
    cfg.option('ip_admin_eth0.netmask_admin_eth0').property.add('newproperty1')
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).property.get() == ('aproperty', 'newproperty', 'newproperty1')
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).property.get() == ('aproperty', 'newproperty1')
#    assert not list_sessions()


def test_api_get_leader(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('conf', '', [interface1])
    cfg = Config(od1)
    option = cfg.option('ip_admin_eth0.netmask_admin_eth0').leader()
    assert option.get() == ip_admin_eth0
#    assert not list_sessions()


def test_leader_forbidden_properties(config_type):
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('conf', '', [interface1])
    cfg = Config(od1)
    with pytest.raises(LeadershipError):
        cfg.option('ip_admin_eth0.ip_admin_eth0').property.add('permissive')


def test_leader_forbidden_properties_callback(config_type):
    calc_property = Calculation(calc_value, Params(ParamValue('permissive')))
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True, properties=(calc_property,))
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('conf', '', [interface1])
    cfg = Config(od1)
    with pytest.raises(LeadershipError):
        cfg.option('ip_admin_eth0.ip_admin_eth0').value.get()
