# coding: utf-8

from time import sleep, time
from .autopath import do_autopath
do_autopath()

from tiramisu import BoolOption, IPOption, IntOption, StrOption, OptionDescription, Leadership, Config, \
                     undefined, Calculation, Params, ParamValue, ParamOption, calc_value
from tiramisu.error import ConfigError, PropertiesOptionError
from tiramisu.setting import groups


global incr
incr = -1
def return_incr():
    global incr
    incr += 1
    return int(incr/2) + 1


def make_description():
    u1 = IntOption('u1', '', multi=True)
    u2 = IntOption('u2', '')
    u3 = IntOption('u3', '', multi=True)
    return OptionDescription('od1', '', [u1, u2, u3])


def test_cache_config():
    od1 = make_description()
    assert od1.impl_already_build_caches() is False
    cfg = Config(od1)
    assert od1.impl_already_build_caches() is True
    cfg
#    assert not list_sessions()


def test_cache():
    od1 = make_description()
    cfg = Config(od1)
    values = cfg._config_bag.context._impl_values_cache
    settings = cfg._config_bag.context.properties_cache
    cfg.option('u1').value.get()
    assert 'u1' in values.get_cached()
    assert 'u1' in settings.get_cached()
    cfg.option('u2').value.get()
    assert 'u1' in values.get_cached()
    assert 'u1' in settings.get_cached()
    assert 'u2' in values.get_cached()
    assert 'u2' in settings.get_cached()
#    assert not list_sessions()


def test_cache_importation():
    od1 = make_description()
    cfg = Config(od1)
    cfg.option('u2').value.set(1)
    values = cfg._config_bag.context._impl_values_cache
    export = cfg.value.exportation()
    compare(values.get_cached(), {'u2': {None: (1, None)}})
    cfg.option('u2').value.set(2)
    compare(values.get_cached(), {'u2': {None: (2, None)}})
    cfg.value.importation(export)
    compare(values.get_cached(), {})
#    assert not list_sessions()


def test_cache_importation_property():
    od1 = make_description()
    cfg = Config(od1)
    cfg.option('u2').property.add('prop')
    export = cfg.property.exportation()
    assert cfg.option('u2').property.get() == {'prop'}
    cfg.option('u2').property.add('prop2')
    assert cfg.option('u2').property.get() == {'prop', 'prop2'}
    cfg.property.importation(export)
    assert cfg.option('u2').property.get() == {'prop'}
    cfg = Config(od1)
#    assert not list_sessions()


def test_cache_importation_permissive():
    od1 = make_description()
    cfg = Config(od1)
    cfg.option('u2').permissive.add('prop')
    export = cfg.permissive.exportation()
    assert cfg.option('u2').permissive.get() == {'prop'}
    cfg.option('u2').permissive.add('prop2')
    assert cfg.option('u2').permissive.get() == {'prop', 'prop2'}
    cfg.permissive.importation(export)
    assert cfg.option('u2').permissive.get() == {'prop'}
#    assert not list_sessions()


def test_cache_reset():
    od1 = make_description()
    cfg = Config(od1)
    values = cfg._config_bag.context._impl_values_cache
    settings = cfg._config_bag.context.properties_cache
    #when change a value
    cfg.option('u1').value.get()
    cfg.option('u2').value.get()
    assert 'u1' in values.get_cached()
    assert 'u1' in settings.get_cached()
    assert 'u2' in values.get_cached()
    assert 'u2' in settings.get_cached()
    assert 'u1' in values.get_cached()
    settings.get_cached()
    cfg.option('u2').value.set(1)
    assert 'u1' in values.get_cached()
    assert 'u1' in settings.get_cached()
    assert 'u2' in values.get_cached()
    assert 'u2' not in settings.get_cached()
    #when remove a value
    cfg.option('u1').value.get()
    assert 'u1' in values.get_cached()
    assert 'u1' in settings.get_cached()
    cfg.option('u2').value.reset()
    assert 'u1' in values.get_cached()
    assert 'u1' in settings.get_cached()
    assert 'u2' not in values.get_cached()
    assert 'u2' not in settings.get_cached()
    #when add/del property
    cfg.option('u1').value.get()
    assert 'u1' in values.get_cached()
    assert 'u1' in settings.get_cached()
    cfg.option('u2').property.add('test')
    assert 'u1' in values.get_cached()
    assert 'u1' in settings.get_cached()
    assert 'u2' not in values.get_cached()
    assert 'u2' not in settings.get_cached()
    cfg.option('u1').value.get()
    assert 'u1' in values.get_cached()
    assert 'u1' in settings.get_cached()
    cfg.option('u2').property.remove('test')
    assert 'u1' in values.get_cached()
    assert 'u1' in settings.get_cached()
    assert 'u2' not in values.get_cached()
    assert 'u2' not in settings.get_cached()
    #when enable/disabled property
    cfg.option('u1').value.get()
    assert 'u1' in values.get_cached()
    assert 'u1' in settings.get_cached()
    cfg.property.add('test')
    assert 'u1' not in values.get_cached()
    assert 'u1' not in settings.get_cached()
    cfg.option('u1').value.get()
    assert 'u1' in values.get_cached()
    assert 'u1' in values.get_cached()
    assert 'u1' in settings.get_cached()
    cfg.property.remove('test')
    assert 'u1' not in values.get_cached()
    assert 'u1' not in settings.get_cached()
#    assert not list_sessions()


def test_cache_reset_multi():
    od1 = make_description()
    cfg = Config(od1)
    values = cfg._config_bag.context._impl_values_cache
    settings = cfg._config_bag.context.properties_cache
    cfg.option('u1').value.get()
    cfg.option('u3').value.get()
    assert 'u1' in values.get_cached()
    assert 'u1' in settings.get_cached()
    assert 'u3' in values.get_cached()
    assert 'u3' in settings.get_cached()
    #when change a value
    cfg.option('u3').value.set([1])
    assert 'u1' in values.get_cached()
    assert 'u1' in settings.get_cached()
    assert 'u3' in values.get_cached()
    assert 'u3' not in settings.get_cached()
    #when append value
    cfg.option('u1').value.get()
    cfg.option('u3').value.get()
    assert 'u1' in values.get_cached()
    assert 'u1' in settings.get_cached()
    assert 'u3' in values.get_cached()
    assert 'u3' in settings.get_cached()
    cfg.option('u3').value.set([1, 2])
    assert 'u1' in values.get_cached()
    assert 'u1' in settings.get_cached()
    assert 'u3' in values.get_cached()
    assert 'u3' not in settings.get_cached()
    #when pop value
    cfg.option('u1').value.get()
    cfg.option('u3').value.get()
    assert 'u1' in values.get_cached()
    assert 'u1' in settings.get_cached()
    assert 'u3' in values.get_cached()
    assert 'u3' in settings.get_cached()
    cfg.option('u3').value.set([1])
    assert 'u1' in values.get_cached()
    assert 'u1' in settings.get_cached()
    assert 'u3' in values.get_cached()
    assert 'u3' not in settings.get_cached()
    #when remove a value
    cfg.option('u1').value.get()
    assert 'u1' in values.get_cached()
    assert 'u1' in settings.get_cached()
    cfg.option('u3').value.reset()
    assert 'u1' in values.get_cached()
    assert 'u1' in settings.get_cached()
    assert 'u3' not in values.get_cached()
    assert 'u3' not in settings.get_cached()
#    assert not list_sessions()


def test_reset_cache():
    od1 = make_description()
    cfg = Config(od1)
    values = cfg._config_bag.context._impl_values_cache
    settings = cfg._config_bag.context.properties_cache
    cfg.option('u1').value.get()
    assert 'u1' in values.get_cached()
    assert 'u1' in settings.get_cached()
    cfg.cache.reset()
    assert 'u1' not in values.get_cached()
    assert 'u1' not in settings.get_cached()
    cfg.option('u1').value.get()
    cfg.option('u2').value.get()
    assert 'u1' in values.get_cached()
    assert 'u1' in settings.get_cached()
    assert 'u2' in values.get_cached()
    assert 'u2' in settings.get_cached()
    cfg.cache.reset()
    assert 'u1' not in values.get_cached()
    assert 'u1' not in settings.get_cached()
    assert 'u2' not in values.get_cached()
    assert 'u2' not in settings.get_cached()
#    assert not list_sessions()


def test_cache_not_cache():
    od1 = make_description()
    cfg = Config(od1)
    values = cfg._config_bag.context._impl_values_cache
    settings = cfg._config_bag.context.properties_cache
    cfg.property.remove('cache')
    cfg.option('u1').value.get()
    assert 'u1' not in values.get_cached()
    assert 'u1' not in settings.get_cached()
#    assert not list_sessions()


def test_cache_leadership():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True)
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    od1 = OptionDescription('toto', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    values = cfg._config_bag.context._impl_values_cache
    settings = cfg._config_bag.context.properties_cache
    assert values.get_cached() == {}
    #assert settings.get_cached() == {}
    #
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.2'])
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.get()
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get()
    cache = values.get_cached()
    assert set(cache.keys()) == set(['ip_admin_eth0.ip_admin_eth0', 'ip_admin_eth0.netmask_admin_eth0'])
    assert set(cache['ip_admin_eth0.ip_admin_eth0'].keys()) == set([None])
    assert cache['ip_admin_eth0.ip_admin_eth0'][None][0] == ['192.168.1.2']
    #assert set(cache['ip_admin_eth0.netmask_admin_eth0'].keys()) == set([None])
    #assert cache['ip_admin_eth0.netmask_admin_eth0'][None][0] == [None]
    #assert cache['ip_admin_eth0.netmask_admin_eth0'][0][0] is None
    cache = settings.get_cached()
    assert set(cache.keys()) == set(['ip_admin_eth0', 'ip_admin_eth0.ip_admin_eth0', 'ip_admin_eth0.netmask_admin_eth0'])
    assert set(cache['ip_admin_eth0'].keys()) == set([None])
    assert set(cache['ip_admin_eth0.ip_admin_eth0'].keys()) == set([None])
    assert set(cache['ip_admin_eth0.netmask_admin_eth0'].keys()) == {0}
    #
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.2', '192.168.1.1'])
    cfg.option('ip_admin_eth0.ip_admin_eth0').value.get()
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 0).value.get()
    cfg.option('ip_admin_eth0.netmask_admin_eth0', 1).value.get()
    cache = values.get_cached()
    assert set(cache.keys()) == set(['ip_admin_eth0.ip_admin_eth0', 'ip_admin_eth0.netmask_admin_eth0'])
    assert set(cache['ip_admin_eth0.ip_admin_eth0'].keys()) == set([None])
    assert cache['ip_admin_eth0.ip_admin_eth0'][None][0] == ['192.168.1.2', '192.168.1.1']
    #assert set(cache['ip_admin_eth0.netmask_admin_eth0'].keys()) == set([None])
    #assert cache['ip_admin_eth0.netmask_admin_eth0'][None][0] == [None, None]
    #assert cache['ip_admin_eth0.netmask_admin_eth0'][0][0] is None
    #assert cache['ip_admin_eth0.netmask_admin_eth0'][1][0] is None
    cache = settings.get_cached()
    assert set(cache.keys()) == set(['ip_admin_eth0', 'ip_admin_eth0.ip_admin_eth0', 'ip_admin_eth0.netmask_admin_eth0'])
    assert set(cache['ip_admin_eth0'].keys()) == set([None])
    assert set(cache['ip_admin_eth0.ip_admin_eth0'].keys()) == set([None])
    assert set(cache['ip_admin_eth0.netmask_admin_eth0'].keys()) == set([0, 1])
    #DEL, insert, ...
#    assert not list_sessions()


def compare(calculated, expected):
    assert set(calculated.keys()) == set(expected.keys())
    for calculated_key in calculated:
        assert set(calculated[calculated_key].keys()) == set(expected[calculated_key].keys())
        for calculated_subkey in calculated[calculated_key]:
            # do not check timestamp
            assert calculated[calculated_key][calculated_subkey][0] == expected[calculated_key][calculated_subkey][0]


def test_cache_callback():
    val1 = StrOption('val1', "", 'val')
    val2 = StrOption('val2', "", Calculation(calc_value, Params(ParamOption(val1))), properties=('mandatory',))
    val3 = StrOption('val3', "", Calculation(calc_value, Params(ParamValue('yes'))))
    val4 = StrOption('val4', "", Calculation(calc_value, Params(ParamOption(val1))))
    val5 = StrOption('val5', "", [Calculation(calc_value, Params(ParamValue('yes')))], multi=True)
    od1 = OptionDescription('rootconfig', '', [val1, val2, val3, val4, val5])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.value.get()
    values = cfg._config_bag.context._impl_values_cache
    settings = cfg._config_bag.context.properties_cache
    compare(values.get_cached(), {'val1': {None: ('val', None)},
                                  'val2': {None: ('val', None)},
                                  'val3': {None: ('yes', None)},
                                  'val4': {None: ('val', None)},
                                  'val5': {None: (['yes'], None)}})
    cfg.option('val1').value.set('new')
    compare(values.get_cached(), {'val3': {None: ('yes', None)},
                                  'val1': {None: ('new', None)},
                                  'val5': {None: (['yes'], None)}})
    cfg.value.get()
    compare(values.get_cached(), {'val1': {None: ('new', None)},
                                  'val2': {None: ('new', None)},
                                  'val3': {None: ('yes', None)},
                                  'val4': {None: ('new', None)},
                                  'val5': {None: (['yes'], None)}})
    cfg.option('val3').value.set('new2')
    compare(values.get_cached(), {'val1': {None: ('new', None)},
                                  'val2': {None: ('new', None)},
                                  'val4': {None: ('new', None)},
                                  'val1': {None: ('new', None)},
                                  'val3': {None: ('new2', None, True)},
                                  'val5': {None: (['yes'], None)}})
    cfg.value.get()
    compare(values.get_cached(), {'val1': {None: ('new', None)},
                                  'val2': {None: ('new', None)},
                                  'val3': {None: ('new2', None)},
                                  'val4': {None: ('new', None)},
                                  'val5': {None: (['yes'], None)}})
    cfg.option('val4').value.set('new3')
    compare(values.get_cached(), {'val1': {None: ('new', None)},
                                  'val2': {None: ('new', None)},
                                  'val3': {None: ('new2', None)},
                                  'val4': {None: ('new3', None, True)},
                                  'val5': {None: (['yes'], None)}})
    cfg.value.get()
    compare(values.get_cached(), {'val1': {None: ('new', None)},
                                  'val2': {None: ('new', None)},
                                  'val3': {None: ('new2', None)},
                                  'val4': {None: ('new3', None)},
                                  'val5': {None: (['yes'], None)}})
#    assert not list_sessions()


def test_cache_leader_and_followers():
    val1 = StrOption('val1', "", multi=True)
    val2 = StrOption('val2', "", multi=True)
    interface1 = Leadership('val1', '', [val1, val2])
    od1 = OptionDescription('rootconfig', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.value.get()
    global_props = ['cache', 'disabled', 'frozen', 'hidden', 'validator', 'warnings', 'force_store_value']
    val1_props = []
    val1_val1_props = ['empty', 'unique']
    val1_val2_props = []
    global_props = frozenset(global_props)
    val1_props = frozenset(val1_props)
    val1_val1_props = frozenset(val1_val1_props)
    val1_val2_props = frozenset(val1_val2_props)
    #None because no value
    idx_val2 = None
    values = cfg._config_bag.context._impl_values_cache
    settings = cfg._config_bag.context.properties_cache
    compare(settings.get_cached(), {'val1': {None: (val1_props, None)},
                                    'val1.val1': {None: (val1_val1_props, None)},
                                    })
    # len is 0 so don't get any value
    compare(values.get_cached(), {'val1.val1': {None: ([], None)}})
    #
    cfg.option('val1.val1').value.set([None])
    val_val2_props = {idx_val2: (val1_val2_props, None), None: (set(), None)}
    compare(settings.get_cached(), {'val1.val1': {None: ({'empty', 'unique'}, None, True)}})
    compare(values.get_cached(), {'val1.val1': {None: ([None], None, True)}})
    cfg.value.get()
    #has value
    idx_val2 = 0
    val_val2 = None
    val_val2_props = {idx_val2: (val1_val2_props, None)}
    compare(settings.get_cached(), {'val1': {None: (val1_props, None)},
                                    'val1.val1': {None: (val1_val1_props, None)},
                                    'val1.val2': val_val2_props})
    compare(values.get_cached(), {'val1.val1': {None: ([None], None)},
                                  'val1.val2': {idx_val2: (val_val2, None)},
                                  })
    cfg.option('val1.val1').value.set([None, None])
    cfg.value.get()
    cfg.option('val1.val2', 1).value.set('oui')
    compare(settings.get_cached(), {})
    compare(values.get_cached(), {'val1.val2': {1: ('oui', None, True)}})
    val1_val2_props = {0: (frozenset([]), None), 1: (frozenset([]), None)}
#    assert not list_sessions()


def test_cache_leader_callback():
    val1 = StrOption('val1', "", multi=True)
    val2 = StrOption('val2', "", Calculation(calc_value, Params(kwargs={'value': ParamOption(val1)})), multi=True)
    interface1 = Leadership('val1', '', [val1, val2])
    od1 = OptionDescription('rootconfig', '', [interface1])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.value.get()
    global_props = ['cache', 'disabled', 'frozen', 'hidden', 'validator', 'warnings', 'force_store_value']
    val1_props = []
    val1_val1_props = ['empty', 'unique']
    val1_val2_props = []
    global_props = frozenset(global_props)
    val1_props = frozenset(val1_props)
    val1_val1_props = frozenset(val1_val1_props)
    val1_val2_props = frozenset(val1_val2_props)
    values = cfg._config_bag.context._impl_values_cache
    settings = cfg._config_bag.context.properties_cache
    compare(settings.get_cached(), {'val1': {None: (val1_props, None)},
                                    'val1.val1': {None: (val1_val1_props, None)},
                                    })
    compare(values.get_cached(), {'val1.val1': {None: ([], None)}})
    cfg.option('val1.val1').value.set([None])
    compare(settings.get_cached(), {'val1.val1': {None: ({'unique', 'empty'}, None, True)}})

    compare(values.get_cached(), {'val1.val1': {None: ([None], None, True)}})
    cfg.value.get()
#    assert not list_sessions()


def test_cache_requires():
    a = BoolOption('activate_service', '', True)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(a),
                                                   'expected': ParamValue(False),
                                                   'default': ParamValue(None)}))
    b = IPOption('ip_address_service', '', properties=(disabled_property,))
    od1 = OptionDescription('service', '', [a, b])
    cfg = Config(od1)
    cfg.property.read_write()
    values = cfg._config_bag.context._impl_values_cache
    settings = cfg._config_bag.context.properties_cache
    assert values.get_cached() == {}
    assert cfg.option('ip_address_service').value.get() == None
    compare(settings.get_cached(), {'activate_service': {None: (set([]), None)},
                                    'ip_address_service': {None: (set([]), None)}})

    compare(values.get_cached(), {'ip_address_service': {None: (None, None)},
                                                     'activate_service': {None: (True, None)}})
    cfg.value.get()
    compare(settings.get_cached(), {'activate_service': {None: (set([]), None)},
                                    'ip_address_service': {None: (set([]), None)}})

    compare(values.get_cached(), {'ip_address_service': {None: (None, None)},
                                  'activate_service': {None: (True, None)}})
    cfg.option('ip_address_service').value.set('1.1.1.1')
    compare(settings.get_cached(), {'activate_service': {None: (set([]), None)}})

    compare(values.get_cached(), {'activate_service': {None: (True, None)}, 'ip_address_service': {None: ('1.1.1.1', None, True)}})
    cfg.value.get()
    compare(settings.get_cached(), {'activate_service': {None: (set([]), None)},
                                    'ip_address_service': {None: (set([]), None)}})

    compare(values.get_cached(), {'ip_address_service': {None: ('1.1.1.1', None)},
                                  'activate_service': {None: (True, None)}})
    cfg.option('activate_service').value.set(False)
    compare(settings.get_cached(), {})

    compare(values.get_cached(), {'activate_service': {None: (False, None)}})
    cfg.value.get()
    compare(settings.get_cached(), {'activate_service': {None: (set([]), None)},
                                    'ip_address_service': {None: (set(['disabled']), None)}})

    compare(values.get_cached(), {'activate_service': {None: (False, None)}})
#    assert not list_sessions()


def test_cache_global_properties():
    a = BoolOption('activate_service', '', True)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(a),
                                                   'expected': ParamValue(False),
                                                   'default': ParamValue(None)}))
    b = IPOption('ip_address_service', '', properties=(disabled_property,))
    od1 = OptionDescription('service', '', [a, b])
    cfg = Config(od1)
    cfg.property.read_write()
    values = cfg._config_bag.context._impl_values_cache
    settings = cfg._config_bag.context.properties_cache
    assert values.get_cached() == {}
    assert cfg.option('ip_address_service').value.get() == None
    compare(settings.get_cached(), {'activate_service': {None: (set([]), None)},
                                    'ip_address_service': {None: (set([]), None)}})

    compare(values.get_cached(), {'ip_address_service': {None: (None, None)},
                                                      'activate_service': {None: (True, None)}})
    cfg.property.remove('disabled')
    assert cfg.option('ip_address_service').value.get() == None
    compare(settings.get_cached(), {'activate_service': {None: (set([]), None)},
                                    'ip_address_service': {None: (set([]), None)}})
    cfg.property.add('test')
    assert cfg.option('ip_address_service').value.get() == None
    compare(settings.get_cached(), {'activate_service': {None: (set([]), None)},
                                    'ip_address_service': {None: (set([]), None)}})
#    assert not list_sessions()


def test_callback_value_incr():
    global incr
    incr = -1
    val1 = IntOption('val1', "", Calculation(return_incr), properties=('expire',))
    val2 = IntOption('val2', "", Calculation(calc_value, Params(ParamOption(val1))))
    od1 = OptionDescription('rootconfig', '', [val1, val2])
    cfg = Config(od1)
    assert cfg.cache.get_expiration_time() == 5
    cfg.cache.set_expiration_time(1)
    assert cfg.cache.get_expiration_time() == 1
    cfg.property.read_write()
    assert cfg.option('val1').value.get() == 1
    sleep(1)
    assert cfg.option('val2').value.get() == 1
    sleep(1)
    assert cfg.option('val1').value.get() == 1
    assert cfg.option('val2').value.get() == 1
    sleep(2)
    assert cfg.option('val1').value.get() == 2
    assert cfg.option('val2').value.get() == 2
    assert cfg.option('val1').value.get() == 2
    assert cfg.option('val2').value.get() == 2
#    assert not list_sessions()


def test_callback_value_incr_demoting():
    global incr
    incr = -1
    val1 = IntOption('val1', "", Calculation(return_incr), properties=('expire',))
    val2 = IntOption('val2', "", Calculation(calc_value, Params(ParamOption(val1))))
    od1 = OptionDescription('rootconfig', '', [val1, val2])
    cfg = Config(od1)
    cfg.property.add('demoting_error_warning')
    assert cfg.cache.get_expiration_time() == 5
    cfg.cache.set_expiration_time(1)
    assert cfg.cache.get_expiration_time() == 1
    cfg.property.read_write()
    assert cfg.option('val1').value.get() == 1
    sleep(1)
    assert cfg.option('val2').value.get() == 1
    sleep(1)
    assert cfg.option('val1').value.get() == 1
    assert cfg.option('val2').value.get() == 1
    sleep(2)
    assert cfg.option('val1').value.get() == 2
    assert cfg.option('val2').value.get() == 2
    assert cfg.option('val1').value.get() == 2
    assert cfg.option('val2').value.get() == 2
#    assert not list_sessions()
