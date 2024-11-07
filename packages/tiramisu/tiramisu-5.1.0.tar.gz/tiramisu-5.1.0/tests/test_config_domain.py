from .autopath import do_autopath
do_autopath()
from .config import config_type, get_config, value_list, global_owner

import warnings, sys
import pytest

from tiramisu import Config, DomainnameOption, EmailOption, URLOption, OptionDescription
from tiramisu.error import ValueWarning
from tiramisu.i18n import _


def test_domainname(config_type):
    d = DomainnameOption('d', '')
    f = DomainnameOption('f', '', allow_without_dot=True)
    g = DomainnameOption('g', '', allow_ip=True)
    h = DomainnameOption('h', '', allow_cidr_network=True)
    i = DomainnameOption('i', '', allow_ip=True, allow_cidr_network=True)
    j = DomainnameOption('j', '', allow_startswith_dot=True)
    od1 = OptionDescription('a', '', [d, f, g, h, i, j])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    #
    cfg.option('d').value.set('toto.com')
    with pytest.raises(ValueError):
        cfg.option('d').value.set('.toto.com')
    with pytest.raises(ValueError):
        cfg.option('d').value.set('toto')
    cfg.option('d').value.set('toto3.com')
    with pytest.raises(ValueError):
        cfg.option('d').value.set('toto_super.com')
    cfg.option('d').value.set('toto-.com')
    with pytest.raises(ValueError):
        cfg.option('d').value.set('toto..com')
    #
    cfg.option('f').value.set('toto.com')
    cfg.option('f').value.set('toto')
    cfg.option('f').value.set('domainnametoolongthathavemorethanmaximumsizeforatruedomainnamea')
    with pytest.raises(ValueError):
        cfg.option('f').value.set('domainnametoolongthathavemorethanmaximumsizeforatruedomainnamean')
    cfg.option('f').value.set('domainnametoolongthathavemorethanmaximumsizeforatruedomainnamea.nd')
    cfg.option('f').value.set('domainnametoolongthathavemorethanmaximumsizeforatruedomainnamea.nditsnoteasytogeneratesolongdomainnamewithoutrepeatdomainnameto.olongthathavemorethanmaximumsizeforatruedomainnameanditsnoteas.ytogeneratesolongdomainnamewithoutrepeatbutimnotabletodoitnowie')
    with pytest.raises(ValueError):
        cfg.option('d').value.set('domainnametoolongthathavemorethanmaximumsizeforatruedomainnamea.nditsnoteasytogeneratesolongdomainnamewithoutrepeatdomainnameto.olongthathavemorethanmaximumsizeforatruedomainnameanditsnoteas.ytogeneratesolongdomainnamewithoutrepeatbutimnotabletodoitnowien')
    cfg.option('f').value.set('d')
    cfg.option('f').value.set('d.t')
    #
    if config_type != 'tiramisu-api':
        # FIXME
        with pytest.raises(ValueError):
            cfg.option('f').value.set('192.168.1.1')
    with pytest.raises(ValueError):
        cfg.option('f').value.set('192.168.1.0/24')
    #
    cfg.option('g').value.set('toto.com')
    cfg.option('g').value.set('192.168.1.0')
    cfg.option('g').value.set('192.168.1.29')
    with pytest.raises(ValueError):
        cfg.option('g').value.set('192.168.1.0/24')
    with pytest.raises(ValueError):
        cfg.option('g').value.set('240.94.1.1')
    #
    cfg.option('h').value.set('toto.com')
    if config_type != 'tiramisu-api':
        # FIXME
        with pytest.raises(ValueError):
            cfg.option('h').value.set('192.168.1.0')
        with pytest.raises(ValueError):
            cfg.option('h').value.set('192.168.1.29')
    # it's a network address
    cfg.option('h').value.set('192.168.1.0/24')
    # but not here
    with pytest.raises(ValueError):
        cfg.option('h').value.set('192.168.1.1/24')
    #
    cfg.option('i').value.set('toto.com')
    cfg.option('i').value.set('192.168.1.0')
    cfg.option('i').value.set('192.168.1.1')
    cfg.option('i').value.set('192.168.1.0/24')
    with pytest.raises(ValueError):
        cfg.option('i').value.set('192.168.1.1/24')
    with pytest.raises(ValueError):
        cfg.option('i').value.set('240.94.1.1')
    #
    cfg.option('j').value.set('toto.com')
    cfg.option('j').value.set('.toto.com')
#    assert not list_sessions()


def test_domainname_invalid(config_type):
    with pytest.raises(ValueError):
        DomainnameOption('a', '', allow_cidr_network='str')
    with pytest.raises(ValueError):
        DomainnameOption('a', '', allow_startswith_dot='str')

def test_domainname_upper(config_type):
    d = DomainnameOption('d', '')
    od1 = OptionDescription('a', '', [d])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    cfg.option('d').value.set('toto.com')
    msg = _('some characters are uppercase')
    has_error = False
    try:
        cfg.option('d').value.set('TOTO.COM')
    except ValueError as err:
        if config_type != 'tiramisu-api':
            # FIXME
            assert msg in str(err)
        has_error = True
    assert has_error is True
    has_error = False
    try:
        cfg.option('d').value.set('toTo.com')
    except ValueError as err:
        if config_type != 'tiramisu-api':
            # FIXME
            assert msg in str(err)
        has_error = True
    assert has_error is True
#    assert not list_sessions()


def test_domainname_warning(config_type):
    d = DomainnameOption('d', '', warnings_only=True)
    f = DomainnameOption('f', '', allow_without_dot=True, warnings_only=True)
    g = DomainnameOption('g', '', allow_ip=True, warnings_only=True)
    od1 = OptionDescription('a', '', [d, f, g])
    warnings.simplefilter("always", ValueWarning)
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    cfg.option('d').value.set('toto.com')
    cfg.option('d').value.set('toto.com.')
    with pytest.raises(ValueError):
        cfg.option('d').value.set('toto')
    cfg.option('d').value.set('toto3.com')
    if config_type != 'tiramisu-api':
        # FIXME
        with warnings.catch_warnings(record=True) as w:
            cfg.option('d').value.set('toto_super.com')
        assert len(w) == 1
    with warnings.catch_warnings(record=True) as w:
        cfg.option('d').value.set('toto-.com')
    assert len(w) == 0
    with pytest.raises(ValueError):
        cfg.option('d').value.set('toto..com')
    #
    cfg.option('f').value.set('toto.com')
    cfg.option('f').value.set('toto')
    cfg.option('f').value.set('domainnametoolongthathavemorethanmaximumsizeforatruedomainnamea')
    with pytest.raises(ValueError):
        cfg.option('f').value.set('domainnametoolongthathavemorethanmaximumsizeforatruedomainnamean')
    cfg.option('f').value.set('domainnametoolongthathavemorethanmaximumsizeforatruedomainnamea.nd')
    cfg.option('f').value.set('domainnametoolongthathavemorethanmaximumsizeforatruedomainnamea.nditsnoteasytogeneratesolongdomainnamewithoutrepeatdomainnameto.olongthathavemorethanmaximumsizeforatruedomainnameanditsnoteas.ytogeneratesolongdomainnamewithoutrepeatbutimnotabletodoitnowie')
    if config_type != 'tiramisu-api':
        # FIXME
        with pytest.raises(ValueError):
            cfg.option('f').value.set('domainnametoolongthathavemorethanmaximumsizeforatruedomainname.nditsnoteasytogeneratesolongdomainnamewithoutrepeatdomainnamet.olongthathavemorethanmaximumsizeforatruedomainnameanditsnotea.ytogeneratesolongdomainnamewithoutrepeatbutimnotabletodoitnowie.xxxx')
    cfg.option('f').value.set('d')
    cfg.option('f').value.set('d.t')
    #
    if config_type != 'tiramisu-api':
        # FIXME
        with pytest.raises(ValueError):
            cfg.option('f').value.set('192.168.1.1')
    cfg.option('g').value.set('toto.com')
    cfg.option('g').value.set('192.168.1.0')
    cfg.option('g').value.set('192.168.1.29')
#    assert not list_sessions()


def test_special_domain_name(config_type):
    """domain name option that starts with a number or not
    """
    d = DomainnameOption('d', '')
    e = DomainnameOption('e', '', type='netbios')
    od1 = OptionDescription('a', '', [d, e])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    cfg.option('d').value.set('1toto.com')
    cfg.option('d').value.set('123toto.com')
    cfg.option('e').value.set('toto')
    cfg.option('e').value.set('1toto')
#    assert not list_sessions()


def test_domainname_netbios(config_type):
    d = DomainnameOption('d', '', type='netbios')
    e = DomainnameOption('e', '', "toto", type='netbios')
    od1 = OptionDescription('a', '', [d, e])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    with pytest.raises(ValueError):
        cfg.option('d').value.set('toto.com')
    cfg.option('d').value.set('toto')
    with pytest.raises(ValueError):
        cfg.option('d').value.set('domainnametoolong')
#    assert not list_sessions()


def test_domainname_hostname(config_type):
    d = DomainnameOption('d', '', type='hostname')
    e = DomainnameOption('e', '', "toto", type='hostname')
    od1 = OptionDescription('a', '', [d, e])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    with pytest.raises(ValueError):
        cfg.option('d').value.set('toto.com')
    cfg.option('d').value.set('toto')
    cfg.option('d').value.set('domainnametoolong')
#    assert not list_sessions()


def test_email(config_type):
    e = EmailOption('e', '')
    od1 = OptionDescription('a', '', [e])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    cfg.option('e').value.set('foo-bar.baz@example.com')
    cfg.option('e').value.set('root@foo.com')
    cfg.option('e').value.set('root@domain')
    with pytest.raises(ValueError):
        cfg.option('e').value.set(1)
    with pytest.raises(ValueError):
        cfg.option('e').value.set('root')
    with pytest.raises(ValueError):
        cfg.option('e').value.set('root[]@domain')
#    assert not list_sessions()


def test_url(config_type):
    u = URLOption('u', '')
    od1 = OptionDescription('a', '', [u])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    cfg.option('u').value.set('http://foo.com')
    cfg.option('u').value.set('https://foo.com')
    cfg.option('u').value.set('https://foo.com/')
    with pytest.raises(ValueError):
        cfg.option('u').value.set(1)
    if config_type != 'tiramisu-api':
        # FIXME
        with pytest.raises(ValueError):
            cfg.option('u').value.set('ftp://foo.com')
        with pytest.raises(ValueError):
            cfg.option('u').value.set('foo.com')
        with pytest.raises(ValueError):
            cfg.option('u').value.set(':/foo.com')
        with pytest.raises(ValueError):
            cfg.option('u').value.set('foo.com/http://')
    cfg.option('u').value.set('https://foo.com/index.html')
    cfg.option('u').value.set('https://foo.com/index.html?var=value&var2=val2')
    if config_type != 'tiramisu-api':
        # FIXME
        with pytest.raises(ValueError):
            cfg.option('u').value.set('https://foo.com/index\\n.html')
    cfg.option('u').value.set('https://foo.com:8443')
    cfg.option('u').value.set('https://foo.com:8443/')
    cfg.option('u').value.set('https://foo.com:8443/index.html')
    if config_type != 'tiramisu-api':
        # FIXME
        with pytest.raises(ValueError):
            cfg.option('u').value.set('https://foo.com:84438989')
    cfg.option('u').value.set('https://foo.com:8443/INDEX')
    if config_type != 'tiramisu-api':
        # FIXME
        with pytest.raises(ValueError):
            cfg.option('u').value.set('https://FOO.COM:8443')
#    assert not list_sessions()
