# coding: utf-8
from .autopath import do_autopath
do_autopath()
import weakref
import pytest

from tiramisu import BoolOption, IntOption, StrOption, IPOption, NetmaskOption, \
                     SymLinkOption, OptionDescription, DynOptionDescription, submulti, \
                     Config, GroupConfig, MetaConfig, Params, ParamOption, Calculation


def funcname(*args, **kwargs):
    return value


def test_deref_value():
    b = BoolOption('b', '')
    o = OptionDescription('od', '', [b])
    cfg = Config(o)
    w = weakref.ref(cfg._config_bag.context.get_values())
    del cfg
    assert w() is None


def test_deref_setting():
    b = BoolOption('b', '')
    o = OptionDescription('od', '', [b])
    cfg = Config(o)
    w = weakref.ref(cfg._config_bag.context.get_settings())
    del cfg
    assert w() is None


def test_deref_config():
    b = BoolOption('b', '')
    o = OptionDescription('od', '', [b])
    cfg = Config(o)
    w = weakref.ref(cfg)
    del cfg
    assert w() is None


def test_deref_option():
    b = BoolOption('b', '')
    o = OptionDescription('od', '', [b])
    w = weakref.ref(b)
    del(b)
    try:
        assert w() is not None
    except AssertionError:
        return
    del(o)
    assert w() is None


def test_deref_optiondescription():
    b = BoolOption('b', '')
    o = OptionDescription('od', '', [b])
    w = weakref.ref(o)
    del(b)
    assert w() is not None
    del(o)
    assert w() is None


def test_deref_option_cache():
    b = BoolOption('b', '')
    o = OptionDescription('od', '', [b])
    o._build_cache(None)
    w = weakref.ref(b)
    del(b)
    assert w() is not None
    del(o)
    assert w() is None


def test_deref_optiondescription_cache():
    b = BoolOption('b', '')
    o = OptionDescription('od', '', [b])
    o._build_cache(None)
    w = weakref.ref(o)
    del(b)
    assert w() is not None
    del(o)
    assert w() is None


def test_deref_option_config():
    b = BoolOption('b', '')
    o = OptionDescription('od', '', [b])
    cfg = Config(o)
    w = weakref.ref(b)
    del(b)
    assert w() is not None
    del(o)
    assert w() is not None
    del cfg
    assert w() is None


def test_deref_optiondescription_config():
    b = BoolOption('b', '')
    o = OptionDescription('od', '', [b])
    cfg = Config(o)
    w = weakref.ref(o)
    del(b)
    assert w() is not None
    del(o)
    assert w() is not None
    del cfg
    assert w() is None


def test_deref_validator():
    a = StrOption('a', '', default='yes')
    b = StrOption('b', '', validators=[Calculation(funcname, Params(ParamOption(a)))], default='val')
    o = OptionDescription('root', '', [a, b])
    cfg = Config(o)
    w = weakref.ref(a)
    x = weakref.ref(b)
    y = weakref.ref(o)
    z = weakref.ref(cfg)
    assert w() is not None
    assert x() is not None
    assert w() is not None
    assert x() is not None
    del(a)
    del(b)
    assert w() is not None
    assert x() is not None
    assert w() is not None
    assert x() is not None
    del(o)
    assert w() is not None
    assert x() is not None
    assert w() is not None
    assert x() is not None
    del cfg
    assert y() is None
    assert z() is None


def test_deref_callback():
    a = StrOption('a', "", 'val')
    b = StrOption('b', "", Calculation(funcname, Params((ParamOption(a),))))
    o = OptionDescription('root', '', [a, b])
    cfg = Config(o)
    w = weakref.ref(a)
    x = weakref.ref(b)
    y = weakref.ref(o)
    z = weakref.ref(cfg)
    assert w() is not None
    assert x() is not None
    assert w() is not None
    assert x() is not None
    del(a)
    del(b)
    assert w() is not None
    assert x() is not None
    assert w() is not None
    assert x() is not None
    del(o)
    assert w() is not None
    assert x() is not None
    assert w() is not None
    assert x() is not None
    del cfg
    assert y() is None
    assert z() is None


def test_deref_symlink():
    a = BoolOption("a", "", default=False)
    b = SymLinkOption("b", a)
    o = OptionDescription('root', '', [a, b])
    cfg = Config(o)
    w = weakref.ref(a)
    x = weakref.ref(b)
    y = weakref.ref(o)
    z = weakref.ref(cfg)
    assert w() is not None
    assert x() is not None
    assert w() is not None
    assert x() is not None
    del(a)
    del(b)
    assert w() is not None
    assert x() is not None
    assert w() is not None
    assert x() is not None
    del(o)
    assert w() is not None
    assert x() is not None
    assert w() is not None
    assert x() is not None
    del cfg
    assert y() is None
    assert z() is None


def test_deref_dyn():
    a = StrOption('a', '', ['val1', 'val2'], multi=True)
    b = StrOption('b', '')
    dod = DynOptionDescription('dod', '', [b], identifiers=Calculation(funcname, Params((ParamOption(a),))))
    o = OptionDescription('od', '', [dod, a])
    cfg = Config(o)
    w = weakref.ref(a)
    x = weakref.ref(b)
    y = weakref.ref(o)
    z = weakref.ref(cfg)
    assert w() is not None
    assert x() is not None
    assert w() is not None
    assert x() is not None
    del(a)
    del(b)
    assert w() is not None
    assert x() is not None
    assert w() is not None
    assert x() is not None
    del(o)
    del(dod)
    assert w() is not None
    assert x() is not None
    assert w() is not None
    assert x() is not None
    del cfg
    assert y() is None
    assert z() is None
