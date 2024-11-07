# coding: utf-8
from .autopath import do_autopath
do_autopath()


import pytest
from tiramisu import IntOption, StrOption, OptionDescription, Config
from tiramisu.error import PropertiesOptionError, ConfigError
from .config import config_type, get_config


def make_description():
    u1 = IntOption('u1', '', properties=('frozen', 'mandatory', 'disabled', ))
    u2 = IntOption('u2', '', properties=('frozen', 'mandatory', 'disabled', ))
    return OptionDescription('od1', '', [u1, u2])


def test_forcepermissive_and_unrestraint(config_type):
    od1 = make_description()
    cfg_ori = Config(od1)
    cfg_ori.property.read_write()
    cfg_ori.property.read_write()
    cfg = get_config(cfg_ori, config_type)
    with pytest.raises(ConfigError):
        cfg_ori.forcepermissive.add('disabled')


def test_permissive(config_type):
    od1 = make_description()
    cfg_ori = Config(od1)
    cfg_ori.property.read_write()
    cfg_ori.property.read_write()
    cfg = get_config(cfg_ori, config_type)
    props = frozenset()
    try:
        cfg.option('u1').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert set(props) == {'disabled'}
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.permissive.add('disabled')
    cfg_ori.permissive.remove('hidden')
    assert cfg_ori.permissive.get() == frozenset(['disabled'])
    cfg = get_config(cfg_ori, config_type)
    props = frozenset()
    try:
        cfg.option('u1').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert set(props) == {'disabled'}
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.property.add('permissive')
    cfg = get_config(cfg_ori, config_type)
    cfg.option('u1').value.get()
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.property.remove('permissive')
    cfg = get_config(cfg_ori, config_type)
    props = frozenset()
    try:
        cfg.option('u1').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert set(props) == {'disabled'}
#    assert not list_sessions()


def test_permissive_add(config_type):
    od1 = make_description()
    cfg_ori = Config(od1)
    cfg_ori.property.read_write()
    cfg_ori.property.read_write()
    cfg = get_config(cfg_ori, config_type)
    props = frozenset()
    try:
        cfg.option('u1').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert set(props) == {'disabled'}
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.permissive.add('disabled')
    assert cfg_ori.permissive.get() == frozenset(['hidden', 'disabled'])
    cfg = get_config(cfg_ori, config_type)
    props = frozenset()
    try:
        cfg.option('u1').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert set(props) == {'disabled'}
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.property.add('permissive')
    cfg = get_config(cfg_ori, config_type)
    cfg.option('u1').value.get()
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.property.remove('permissive')
    cfg = get_config(cfg_ori, config_type)
    props = frozenset()
    try:
        cfg.option('u1').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert set(props) == {'disabled'}
#    assert not list_sessions()


def test_permissive_pop():
    od1 = make_description()
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.property.read_write()
    props = frozenset()
    try:
        cfg.forcepermissive.option('u1').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert set(props) == {'disabled'}
    cfg.permissive.add('disabled')
    assert cfg.permissive.get() == frozenset(['hidden', 'disabled'])
    cfg.forcepermissive.option('u1').value.get()
    cfg.permissive.remove('disabled')
    props = frozenset()
    try:
        cfg.forcepermissive.option('u1').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert set(props) == {'disabled'}
#    assert not list_sessions()


def test_permissive_reset():
    od1 = make_description()
    cfg = Config(od1)
    cfg.property.read_write()
    assert cfg.permissive.get() == frozenset(['hidden'])
    #
    cfg.permissive.add('disabled')
    cfg.permissive.remove('hidden')
    assert cfg.permissive.get() == frozenset(['disabled'])
    #
    cfg.permissive.reset()
    assert cfg.permissive.get() == frozenset(['hidden'])
#    assert not list_sessions()


def test_permissive_mandatory():
    od1 = make_description()
    cfg = Config(od1)
    cfg.property.read_only()
    props = frozenset()
    try:
        cfg.option('u1').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])
    cfg.permissive.add('mandatory')
    cfg.permissive.add('disabled')
    assert cfg.permissive.get() == frozenset(['hidden', 'mandatory', 'disabled'])
    cfg.property.add('permissive')
    cfg.option('u1').value.get()
    cfg.property.remove('permissive')
    try:
        cfg.option('u1').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])
#    assert not list_sessions()


def test_permissive_frozen():
    od1 = make_description()
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.permissive.remove('hidden')
    cfg.permissive.add('frozen')
    cfg.permissive.add('disabled')
    assert cfg.permissive.get() == frozenset(['frozen', 'disabled'])
    assert cfg.permissive.get() == frozenset(['frozen', 'disabled'])
    try:
        cfg.option('u1').value.set(1)
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])
    cfg.property.add('permissive')
    cfg.option('u1').value.set(1)
    assert cfg.option('u1').value.get() == 1
    cfg.property.remove('permissive')
    try:
        cfg.option('u1').value.set(1)
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])
#    assert not list_sessions()


def test_forbidden_permissive():
    od1 = make_description()
    cfg = Config(od1)
    cfg.property.read_write()
    with pytest.raises(ConfigError):
        cfg.permissive.add('force_default_on_freeze')
    with pytest.raises(ConfigError):
        cfg.permissive.add('force_metaconfig_on_freeze')
#    assert not list_sessions()


def test_permissive_option(config_type):
    od1 = make_description()
    cfg_ori = Config(od1)
    cfg_ori.property.read_write()
    cfg = get_config(cfg_ori, config_type)

    props = frozenset()
    try:
        cfg.option('u1').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert set(props) == {'disabled'}
    props = frozenset()
    try:
        cfg.option('u2').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert set(props) == {'disabled'}

    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.option('u1').permissive.add('disabled')
    cfg = get_config(cfg_ori, config_type)
    props = frozenset()
    try:
        cfg.option('u1').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset()
    props = frozenset()
    try:
        cfg.option('u2').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert set(props) == {'disabled'}

    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.property.add('permissive')
    cfg = get_config(cfg_ori, config_type)
    cfg.option('u1').value.get()
    props = frozenset()
    try:
        cfg.option('u2').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert set(props) == {'disabled'}

    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.property.remove('permissive')
    cfg = get_config(cfg_ori, config_type)
    props = frozenset()
    try:
        cfg.option('u1').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset()
    props = frozenset()
    try:
        cfg.option('u2').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert set(props) == {'disabled'}
#    assert not list_sessions()


def test_permissive_option_cache():
    od1 = make_description()
    cfg = Config(od1)
    cfg.property.read_write()

    props = frozenset()
    try:
        cfg.option('u1').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert set(props) == {'disabled'}
    props = frozenset()
    try:
        cfg.option('u2').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert set(props) == {'disabled'}

    cfg.option('u1').permissive.add('disabled')
    props = frozenset()
    try:
        cfg.option('u1').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset()
    props = frozenset()
    try:
        cfg.option('u2').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert set(props) == {'disabled'}

    cfg.property.add('permissive')
    cfg.option('u1').value.get()
    props = frozenset()
    try:
        cfg.option('u2').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert set(props) == {'disabled'}

    cfg.property.remove('permissive')
    props = frozenset()
    try:
        cfg.option('u1').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset()
    props = frozenset()
    try:
        cfg.option('u2').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert set(props) == {'disabled'}
#    assert not list_sessions()


def test_permissive_option_mandatory():
    od1 = make_description()
    cfg = Config(od1)
    cfg.property.read_only()
    props = frozenset()
    try:
        cfg.option('u1').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])
    cfg.option('u1').permissive.add('mandatory')
    cfg.option('u1').permissive.add('disabled')
    assert cfg.option('u1').permissive.get() == frozenset(['mandatory', 'disabled'])
    cfg.property.add('permissive')
    cfg.option('u1').value.get()
    cfg.property.remove('permissive')
    try:
        cfg.option('u1').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])
#    assert not list_sessions()


def test_permissive_option_frozen():
    od1 = make_description()
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.option('u1').permissive.add('disabled')
    cfg.option('u1').permissive.add('frozen')
    cfg.option('u1').value.set(1)
    assert cfg.option('u1').value.get() == 1
    cfg.property.add('permissive')
    assert cfg.option('u1').value.get() == 1
    cfg.property.remove('permissive')
    assert cfg.option('u1').value.get() == 1
#    assert not list_sessions()


def test_remove_option_permissive(config_type):
    var1 = StrOption('var1', '', u'value', properties=('hidden',))
    od1 = OptionDescription('od1', '', [var1])
    od2 = OptionDescription('rootod', '', [od1])
    cfg_ori = Config(od2)
    cfg_ori.property.read_write()
    cfg = get_config(cfg_ori, config_type)
    with pytest.raises(PropertiesOptionError):
        cfg.option('od1.var1').value.get()
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.forcepermissive.option('od1.var1').permissive.add('hidden')
    assert cfg_ori.forcepermissive.option('od1.var1').permissive.get() == frozenset(['hidden'])
    cfg = get_config(cfg_ori, config_type)
    assert cfg.option('od1.var1').value.get() == 'value'
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.forcepermissive.option('od1.var1').permissive.reset()
    assert cfg_ori.forcepermissive.option('od1.var1').permissive.get() == frozenset()
    cfg = get_config(cfg_ori, config_type)
    with pytest.raises(PropertiesOptionError):
        cfg.option('od1.var1').value.get()
#    assert not list_sessions()


def test_reset_option_permissive(config_type):
    var1 = StrOption('var1', '', u'value', properties=('hidden',))
    od1 = OptionDescription('od1', '', [var1])
    od2 = OptionDescription('rootod', '', [od1])
    cfg_ori = Config(od2)
    cfg_ori.property.read_write()
    cfg = get_config(cfg_ori, config_type)
    with pytest.raises(PropertiesOptionError):
        cfg.option('od1.var1').value.get()
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.forcepermissive.option('od1.var1').permissive.add('hidden')
    assert cfg_ori.forcepermissive.option('od1.var1').permissive.get() == frozenset(['hidden'])
    cfg = get_config(cfg_ori, config_type)
    assert cfg.option('od1.var1').value.get() == 'value'
    if config_type == 'tiramisu-api':
        cfg.send()
    cfg_ori.forcepermissive.option('od1.var1').permissive.reset()
    assert cfg_ori.forcepermissive.option('od1.var1').permissive.get() == frozenset()
    cfg = get_config(cfg_ori, config_type)
    with pytest.raises(PropertiesOptionError):
        cfg.option('od1.var1').value.get()
#    assert not list_sessions()
