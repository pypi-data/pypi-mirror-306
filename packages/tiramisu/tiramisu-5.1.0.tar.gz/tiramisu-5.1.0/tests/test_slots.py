## coding: utf-8
from .autopath import do_autopath
do_autopath()

import pytest
import warnings

try:
    from tiramisu.setting import OptionBag, ConfigBag
    tiramisu_version = 3
except:
    tiramisu_version = 2
from tiramisu import Config
from tiramisu.option import ChoiceOption, BoolOption, IntOption, FloatOption,\
    StrOption, SymLinkOption, StrOption, IPOption, OptionDescription, \
    PortOption, NetworkOption, NetmaskOption, DomainnameOption, EmailOption, \
    URLOption, FilenameOption


def test_slots_option():
    c = ChoiceOption('a', '', ('a',))
    with pytest.raises(AttributeError):
        c.x = 1
    del c
    c = BoolOption('a', '')
    with pytest.raises(AttributeError):
        c.x = 1
    del c
    c = IntOption('a', '')
    with pytest.raises(AttributeError):
        c.x = 1
    del c
    c = FloatOption('a', '')
    with pytest.raises(AttributeError):
        c.x = 1
    del c
    c = StrOption('a', '')
    with pytest.raises(AttributeError):
        c.x = 1
    c = SymLinkOption('b', c)
    with pytest.raises(AttributeError):
        c.x = 1
    del c
    c = StrOption('a', '')
    with pytest.raises(AttributeError):
        c.x = 1
    del c
    c = IPOption('a', '')
    with pytest.raises(AttributeError):
        c.x = 1
    del c
    c = OptionDescription('a', '', [])
    with pytest.raises(AttributeError):
        c.x = 1
    del c
    c = PortOption('a', '')
    with pytest.raises(AttributeError):
        c.x = 1
    del c
    c = NetworkOption('a', '')
    with pytest.raises(AttributeError):
        c.x = 1
    del c
    c = NetmaskOption('a', '')
    with pytest.raises(AttributeError):
        c.x = 1
    del c
    c = DomainnameOption('a', '')
    with pytest.raises(AttributeError):
        c.x = 1
    del c
    c = EmailOption('a', '')
    with pytest.raises(AttributeError):
        c.x = 1
    del c
    c = URLOption('a', '')
    with pytest.raises(AttributeError):
        c.x = 1
    del c
    c = FilenameOption('a', '')
    with pytest.raises(AttributeError):
        c.x = 1
    del c


def test_slots_option_readonly():
    a = ChoiceOption('a', '', ('a',))
    b = BoolOption('b', '')
    c = IntOption('c', '')
    d = FloatOption('d', '')
    e = StrOption('e', '')
    g = StrOption('g', '')
    h = IPOption('h', '')
    i = PortOption('i', '')
    j = NetworkOption('j', '')
    k = NetmaskOption('k', '')
    l = DomainnameOption('l', '')
    o = EmailOption('o', '')
    p = URLOption('p', '')
    q = FilenameOption('q', '')
    m = OptionDescription('m', '', [a, b, c, d, e, g, h, i, j, k, l, o, p, q])
    a._name = 'a'
    b._name = 'b'
    c._name = 'c'
    d._name = 'd'
    e._name = 'e'
    g._name = 'g'
    h._name = 'h'
    i._name = 'i'
    j._name = 'j'
    k._name = 'k'
    l._name = 'l'
    m._name = 'm'
    o._name = 'o'
    p._name = 'p'
    q._name = 'q'
    Config(m)
    with pytest.raises(AttributeError):
        a._requires = 'a'
    with pytest.raises(AttributeError):
        b._requires = 'b'
    with pytest.raises(AttributeError):
        c._requires = 'c'
    with pytest.raises(AttributeError):
        d._requires = 'd'
    with pytest.raises(AttributeError):
        e._requires = 'e'
    with pytest.raises(AttributeError):
        g._requires = 'g'
    with pytest.raises(AttributeError):
        h._requires = 'h'
    with pytest.raises(AttributeError):
        i._requires = 'i'
    with pytest.raises(AttributeError):
        j._requires = 'j'
    with pytest.raises(AttributeError):
        k._requires = 'k'
    with pytest.raises(AttributeError):
        l._requires = 'l'
    with pytest.raises(AttributeError):
        m._requires = 'm'
    with pytest.raises(AttributeError):
        o._requires = 'o'
    with pytest.raises(AttributeError):
        p._requires = 'p'
    with pytest.raises(AttributeError):
        q._requires = 'q'
#    assert not list_sessions()


#def test_slots_description():
#    # __slots__ for OptionDescription should be complete for __getattr__
#    slots = set()
#    for subclass in OptionDescription.__mro__:
#        if subclass is not object:
#            slots.update(subclass.__slots__)
#    assert slots == set(OptionDescription.__slots__)


def test_slots_setting():
    od1 = OptionDescription('a', '', [])
    od2 = OptionDescription('a', '', [od1])
    cfg = Config(od2)
    s = cfg._config_bag.context.get_settings()
    s
    with pytest.raises(AttributeError):
        s.x = 1
#    assert not list_sessions()


def test_slots_value():
    od1 = OptionDescription('a', '', [])
    od2 = OptionDescription('a', '', [od1])
    cfg = Config(od2)
    v = cfg._config_bag.context.get_values()
    v
    with pytest.raises(AttributeError):
        v.x = 1
#    assert not list_sessions()
