# coding: utf-8
from .autopath import do_autopath
do_autopath()
import pytest

from tiramisu.setting import groups
from tiramisu import Config, MetaConfig, ChoiceOption, BoolOption, IntOption, \
    StrOption, OptionDescription, groups


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
    wantref_option = BoolOption('wantref', 'Test requires', default=False, properties=('force_store_value',))

    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé")
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau")

    leader = OptionDescription('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    interface1 = OptionDescription('interface1', '', [leader])

    general = OptionDescription('general', '', [numero_etab, nom_machine,
                                nombre_interfaces, activer_proxy_client,
                                mode_conteneur_actif, mode_conteneur_actif2,
                                adresse_serveur_ntp, time_zone, wantref_option])
    new = OptionDescription('new', '', [], properties=('hidden',))
    creole = OptionDescription('creole', 'first tiramisu configuration', [general, interface1, new])
    descr = OptionDescription('baseconfig', 'baseconifgdescr', [creole])
    return descr


def test_copy():
    od1 = make_description()
    cfg = Config(od1)
    ncfg = cfg.config.copy()
    assert cfg.option('creole.general.numero_etab').value.get() == None
    cfg.option('creole.general.numero_etab').value.set('oui')
    assert cfg.option('creole.general.numero_etab').value.get() == 'oui'
    assert ncfg.option('creole.general.numero_etab').value.get() == None
#    assert not list_sessions()


def test_copy_information():
    od1 = make_description()
    cfg = Config(od1)
    cfg.information.set('key', 'value')
    ncfg = cfg.config.copy()
    assert ncfg.information.get('key') == 'value'
#    assert not list_sessions()


def test_copy_force_store_value():
    od1 = make_description()
    conf = Config(od1)
    conf2 = Config(od1)
    assert conf.value.exportation() == {}
    assert conf2.value.exportation() == {}
    #
    conf.property.read_write()
    assert conf.value.exportation() == {'creole.general.wantref': {None: [False, 'forced']}}
    assert conf2.value.exportation() == {}
    #
    conf2.property.read_only()
    assert conf.value.exportation() == {'creole.general.wantref': {None: [False, 'forced']}}
    assert conf2.value.exportation() == {'creole.general.wantref': {None: [False, 'forced']}}
    #
    conf.option('creole.general.wantref').value.set(True)
    assert conf.value.exportation() == {'creole.general.wantref': {None: [True, 'user']}}
    assert conf2.value.exportation() == {'creole.general.wantref': {None: [False, 'forced']}}
#    assert not list_sessions()
#
#
#def test_copy_force_store_value_metaconfig():
#    od1 = make_description()
#    meta = MetaConfig([], optiondescription=od1)
#    conf = meta.config.new()
#    assert meta.property.get() == conf.property.get()
#    assert meta.permissive.get() == conf.permissive.get()
#    conf.property.read_write()
#    assert conf.value.exportation() == {'creole.general.wantref': {None: [False, 'forced']}}
#    assert meta.value.exportation() == {}
##    assert not list_sessions()
