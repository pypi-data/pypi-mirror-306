from .autopath import do_autopath
do_autopath()
from .config import config_type, get_config, value_list, global_owner

import warnings
import pytest
from tiramisu import Config, IPOption, NetworkOption, NetmaskOption, \
                     PortOption, BroadcastOption, OptionDescription
from tiramisu.error import ValueWarning


def test_ip(config_type):
    a = IPOption('a', '')
    b = IPOption('b', '', private_only=True)
    d = IPOption('d', '', warnings_only=True, private_only=True)
    warnings.simplefilter("always", ValueWarning)
    od1 = OptionDescription('od', '', [a, b, d])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    cfg.option('a').value.set('192.168.1.1')
    cfg.option('a').value.set('192.168.1.0')
    cfg.option('a').value.set('88.88.88.88')
    cfg.option('a').value.set('0.0.0.0')
    if config_type != 'tiramisu-api':
        # FIXME
        with pytest.raises(ValueError):
            cfg.option('a').value.set('255.255.255.0')
    cfg.option('b').value.set('192.168.1.1')
    cfg.option('b').value.set('192.168.1.0')
    if config_type != 'tiramisu-api':
        # FIXME
        with pytest.raises(ValueError):
            cfg.option('b').value.set('88.88.88.88')
    cfg.option('b').value.set('0.0.0.0')
    if config_type != 'tiramisu-api':
        # FIXME
        with pytest.raises(ValueError):
            cfg.option('b').value.set('255.255.255.0')
    with pytest.raises(ValueError):
        cfg.option('a').value.set('333.0.1.20')

    if config_type != 'tiramisu-api':
        # FIXME
        with pytest.raises(ValueError):
            IPOption('a', 'ip', default='192.000.023.01')
        with warnings.catch_warnings(record=True) as w:
            cfg.option('d').value.set('88.88.88.88')
        assert len(w) == 1
#    assert not list_sessions()


def test_ip_cidr():
    b = IPOption('b', '', private_only=True, cidr=True)
    c = IPOption('c', '', private_only=True)
    warnings.simplefilter("always", ValueWarning)
    od1 = OptionDescription('od', '', [b, c])
    cfg = Config(od1)
    with pytest.raises(ValueError):
        cfg.option('b').value.set('192.168.1.1')
    cfg.option('b').value.set('192.168.1.1/24')
    with pytest.raises(ValueError):
        cfg.option('b').value.set('192.168.1.0/24')
    with pytest.raises(ValueError):
        cfg.option('b').value.set('192.168.1.255/24')
    with pytest.raises(ValueError):
        cfg.option('b').value.set('192.168.1.1/32')
    with pytest.raises(ValueError):
        cfg.option('b').value.set('192.168.1.1/33')
    #
    cfg.option('c').value.set('192.168.1.1')
    with pytest.raises(ValueError):
        cfg.option('c').value.set('192.168.1.1/24')
    with pytest.raises(ValueError):
        cfg.option('c').value.set('192.168.1.1/32')
#    assert not list_sessions()


def test_ip_default():
    a = IPOption('a', '', '88.88.88.88')
    od1 = OptionDescription('od', '', [a])
    cfg = Config(od1)
    cfg.option('a').value.get() == '88.88.88.88'
#    assert not list_sessions()


def test_ip_reserved(config_type):
    a = IPOption('a', '')
    b = IPOption('b', '', allow_reserved=True)
    c = IPOption('c', '', warnings_only=True)
    od1 = OptionDescription('od', '', [a, b, c])
    warnings.simplefilter("always", ValueWarning)
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    if config_type != 'tiramisu-api':
        # FIXME
        with pytest.raises(ValueError):
            cfg.option('a').value.set('240.94.1.1')
    cfg.option('b').value.set('240.94.1.1')
    if config_type != 'tiramisu-api':
        # FIXME
        with warnings.catch_warnings(record=True) as w:
            cfg.option('c').value.set('240.94.1.1')
        assert len(w) == 1
#    assert not list_sessions()


def test_network(config_type):
    a = NetworkOption('a', '')
    b = NetworkOption('b', '', warnings_only=True)
    od1 = OptionDescription('od', '', [a, b])
    warnings.simplefilter("always", ValueWarning)
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    cfg.option('a').value.set('192.168.1.1')
    cfg.option('a').value.set('192.168.1.0')
    cfg.option('a').value.set('88.88.88.88')
    cfg.option('a').value.set('0.0.0.0')
    with pytest.raises(ValueError):
        cfg.option('a').value.set(1)
    with pytest.raises(ValueError):
        cfg.option('a').value.set('1.1.1.1.1')
    if config_type != 'tiramisu-api':
        # FIXME
        with pytest.raises(ValueError):
            cfg.option('a').value.set('255.255.255.0')
        with pytest.raises(ValueError):
            cfg.option('a').value.set('192.168.001.0')
    with pytest.raises(ValueError):
        cfg.option('a').value.set('333.168.1.1')
    if config_type != 'tiramisu-api':
        # FIXME
        with warnings.catch_warnings(record=True) as w:
            cfg.option('b').value.set('255.255.255.0')
        assert len(w) == 1
#    assert not list_sessions()


def test_network_cidr(config_type):
    a = NetworkOption('a', '', cidr=True)
    od1 = OptionDescription('od', '', [a])
    cfg = Config(od1)
    # FIXME cfg = get_config(cfg, config_type)
    cfg.option('a').value.set('192.168.1.1/32')
    cfg.option('a').value.set('192.168.1.0/24')
    cfg.option('a').value.set('88.88.88.88/32')
    cfg.option('a').value.set('0.0.0.0/0')
    with pytest.raises(ValueError):
        cfg.option('a').value.set('192.168.1.1')
    with pytest.raises(ValueError):
        cfg.option('a').value.set('192.168.1.1/24')
    with pytest.raises(ValueError):
        cfg.option('a').value.set('2001:db00::0/24')
#    assert not list_sessions()


def test_network_invalid():
    with pytest.raises(ValueError):
        NetworkOption('a', '', default='toto')


def test_netmask(config_type):
    a = NetmaskOption('a', '')
    od1 = OptionDescription('od', '', [a])
    cfg = Config(od1)
    cfg = get_config(cfg, config_type)
    with pytest.raises(ValueError):
        cfg.option('a').value.set('192.168.1.1.1')
    if config_type != 'tiramisu-api':
        # FIXME
        with pytest.raises(ValueError):
            cfg.option('a').value.set('192.168.1.1')
        with pytest.raises(ValueError):
            cfg.option('a').value.set('192.168.1.0')
        with pytest.raises(ValueError):
            cfg.option('a').value.set('88.88.88.88')
        with pytest.raises(ValueError):
            cfg.option('a').value.set('255.255.255.000')
    with pytest.raises(ValueError):
        cfg.option('a').value.set(2)
    cfg.option('a').value.set('0.0.0.0')
    cfg.option('a').value.set('255.255.255.0')
#    assert not list_sessions()


def test_broadcast(config_type):
    a = BroadcastOption('a', '')
    od1 = OptionDescription('od', '', [a])
    cfg = Config(od1)
    # FIXME cfg = get_config(cfg, config_type)
    with pytest.raises(ValueError):
        cfg.option('a').value.set('192.168.1.255.1')
    with pytest.raises(ValueError):
        cfg.option('a').value.set('192.168.001.255')
    with pytest.raises(ValueError):
        cfg.option('a').value.set('192.168.0.300')
    with pytest.raises(ValueError):
        cfg.option('a').value.set(1)
    with pytest.raises(ValueError):
        cfg.option('a').value.set(2)
    with pytest.raises(ValueError):
        cfg.option('a').value.set('2001:db8::1')
    cfg.option('a').value.set('0.0.0.0')
    cfg.option('a').value.set('255.255.255.0')
#    assert not list_sessions()


def test_port(config_type):
    a = PortOption('a', '')
    b = PortOption('b', '', allow_zero=True)
    c = PortOption('c', '', allow_zero=True, allow_registred=False)
    d = PortOption('d', '', allow_zero=True, allow_wellknown=False, allow_registred=False)
    e = PortOption('e', '', allow_zero=True, allow_private=True)
    f = PortOption('f', '', allow_private=True)
    g = PortOption('g', '', warnings_only=True)
    od1 = OptionDescription('od', '', [a, b, c, d, e, f, g])
    cfg = Config(od1)
    # FIXME cfg = get_config(cfg, config_type)
    with pytest.raises(ValueError):
        cfg.option('a').value.set('0')
    with warnings.catch_warnings(record=True) as w:
        cfg.option('g').value.set('0')
    assert len(w) == 1
    cfg.option('a').value.set('1')
    cfg.option('a').value.set('1023')
    cfg.option('a').value.set('1024')
    cfg.option('a').value.set('49151')
    with pytest.raises(ValueError):
        cfg.option('a').value.set('49152')
    with pytest.raises(ValueError):
        cfg.option('a').value.set('65535')
    with pytest.raises(ValueError):
        cfg.option('a').value.set('65536')

    cfg.option('b').value.set('0')
    cfg.option('b').value.set('1')
    cfg.option('b').value.set('1023')
    cfg.option('b').value.set('1024')
    cfg.option('b').value.set('49151')
    with pytest.raises(ValueError):
        cfg.option('b').value.set('49152')
    with pytest.raises(ValueError):
        cfg.option('b').value.set('65535')
    with pytest.raises(ValueError):
        cfg.option('b').value.set('65536')

    cfg.option('c').value.set('0')
    cfg.option('c').value.set('1')
    cfg.option('c').value.set('1023')
    with pytest.raises(ValueError):
        cfg.option('c').value.set('1024')
    with pytest.raises(ValueError):
        cfg.option('c').value.set('49151')
    with pytest.raises(ValueError):
        cfg.option('c').value.set('49152')
    with pytest.raises(ValueError):
        cfg.option('c').value.set('65535')
    with pytest.raises(ValueError):
        cfg.option('c').value.set('65536')

    cfg.option('d').value.set('0')
    with pytest.raises(ValueError):
        cfg.option('d').value.set('1')
    with pytest.raises(ValueError):
        cfg.option('d').value.set('1023')
    with pytest.raises(ValueError):
        cfg.option('d').value.set('1024')
    with pytest.raises(ValueError):
        cfg.option('d').value.set('49151')
    with pytest.raises(ValueError):
        cfg.option('d').value.set('49152')
    with pytest.raises(ValueError):
        cfg.option('d').value.set('65535')
    with pytest.raises(ValueError):
        cfg.option('d').value.set('65536')

    cfg.option('e').value.set('0')
    cfg.option('e').value.set('1')
    cfg.option('e').value.set('1023')
    cfg.option('e').value.set('1024')
    cfg.option('e').value.set('49151')
    cfg.option('e').value.set('49152')
    cfg.option('e').value.set('65535')

    with pytest.raises(ValueError):
        cfg.option('f').value.set('0')
    cfg.option('f').value.set('1')
    cfg.option('f').value.set('1023')
    cfg.option('f').value.set('1024')
    cfg.option('f').value.set('49151')
    cfg.option('f').value.set('49152')
    cfg.option('f').value.set('65535')
    with pytest.raises(ValueError):
        cfg.option('f').value.set('65536')
#    assert not list_sessions()


def test_port_protocol(config_type):
    a = PortOption('a', '', allow_protocol=True)
    od1 = OptionDescription('od', '', [a])
    cfg = Config(od1)
    cfg.option('a').value.set('80')
    cfg.option('a').value.set('tcp:80')
#    assert not list_sessions()


def test_port_range(config_type):
    a = PortOption('a', '', allow_range=True)
    b = PortOption('b', '', allow_range=True, allow_zero=True)
    c = PortOption('c', '', allow_range=True, allow_zero=True, allow_registred=False)
    d = PortOption('d', '', allow_range=True, allow_zero=True, allow_wellknown=False, allow_registred=False)
    e = PortOption('e', '', allow_range=True, allow_zero=True, allow_private=True)
    f = PortOption('f', '', allow_range=True, allow_private=True)
    od1 = OptionDescription('od', '', [a, b, c, d, e, f])
    cfg = Config(od1)
    # FIXME cfg = get_config(cfg, config_type)
    with pytest.raises(ValueError):
        cfg.option('a').value.set('0')
    cfg.option('a').value.set('1')
    cfg.option('a').value.set('1023')
    cfg.option('a').value.set('1024')
    cfg.option('a').value.set('49151')
    with pytest.raises(ValueError):
        cfg.option('a').value.set('49152')
    with pytest.raises(ValueError):
        cfg.option('a').value.set('65535')
    with pytest.raises(ValueError):
        cfg.option('a').value.set('65536')
    cfg.option('a').value.set('1:49151')
    with pytest.raises(ValueError):
        cfg.option('a').value.set('0:49151')
    with pytest.raises(ValueError):
        cfg.option('a').value.set('1:49152')

    cfg.option('b').value.set('0')
    cfg.option('b').value.set('1')
    cfg.option('b').value.set('1023')
    cfg.option('b').value.set('1024')
    cfg.option('b').value.set('49151')
    with pytest.raises(ValueError):
        cfg.option('b').value.set('49152')
    with pytest.raises(ValueError):
        cfg.option('b').value.set('65535')
    with pytest.raises(ValueError):
        cfg.option('b').value.set('65536')
    cfg.option('b').value.set('0:49151')
    with pytest.raises(ValueError):
        cfg.option('b').value.set('0:49152')

    cfg.option('c').value.set('0')
    cfg.option('c').value.set('1')
    cfg.option('c').value.set('1023')
    with pytest.raises(ValueError):
        cfg.option('c').value.set('1024')
    with pytest.raises(ValueError):
        cfg.option('c').value.set('49151')
    with pytest.raises(ValueError):
        cfg.option('c').value.set('49152')
    with pytest.raises(ValueError):
        cfg.option('c').value.set('65535')
    with pytest.raises(ValueError):
        cfg.option('c').value.set('65536')
    cfg.option('c').value.set('0:1023')
    with pytest.raises(ValueError):
        cfg.option('c').value.set('0:1024')

    cfg.option('d').value.set('0')
    with pytest.raises(ValueError):
        cfg.option('d').value.set('1')
    with pytest.raises(ValueError):
        cfg.option('d').value.set('1023')
    with pytest.raises(ValueError):
        cfg.option('d').value.set('1024')
    with pytest.raises(ValueError):
        cfg.option('d').value.set('49151')
    with pytest.raises(ValueError):
        cfg.option('d').value.set('49152')
    with pytest.raises(ValueError):
        cfg.option('d').value.set('65535')
    with pytest.raises(ValueError):
        cfg.option('d').value.set('65536')
    with pytest.raises(ValueError):
        cfg.option('d').value.set('0:0')
    with pytest.raises(ValueError):
        cfg.option('d').value.set('0:1')

    cfg.option('e').value.set('0')
    cfg.option('e').value.set('1')
    cfg.option('e').value.set('1023')
    cfg.option('e').value.set('1024')
    cfg.option('e').value.set('49151')
    cfg.option('e').value.set('49152')
    cfg.option('e').value.set('65535')
    cfg.option('e').value.set('0:65535')
    with pytest.raises(ValueError):
        cfg.option('e').value.set('0:65536')

    with pytest.raises(ValueError):
        cfg.option('f').value.set('0')
    cfg.option('f').value.set('1')
    cfg.option('f').value.set('1023')
    cfg.option('f').value.set('1024')
    cfg.option('f').value.set('49151')
    cfg.option('f').value.set('49152')
    cfg.option('f').value.set('65535')
    with pytest.raises(ValueError):
        cfg.option('f').value.set('65536')
    cfg.option('f').value.set('1:65535')
    cfg.option('f').value.set('3:4')
    with pytest.raises(ValueError):
        cfg.option('f').value.set('0:65535')
    with pytest.raises(ValueError):
        cfg.option('f').value.set('4:3')
#    assert not list_sessions()
