"""these tests are here to create some :class:`tiramisu.option.Option`'s
and to compare them
"""
from .autopath import do_autopath
do_autopath()

import pytest
import warnings
from tiramisu.error import ConfigError, ValueWarning
from tiramisu import IntOption, SymLinkOption, OptionDescription, Config, Calculation, groups
from tiramisu.i18n import _

try:
    groups.family
except:
    groups.addgroup('family')


def a_func():
    return None


def display_name(*args, with_quote=False):
    return 'display_name'


def test_option_valid_name():
    IntOption('test', '')
    with pytest.raises(ValueError):
        IntOption(1, "")
    i = IntOption("test1", "")
    with pytest.raises(ValueError):
        SymLinkOption(1, i)
    i = SymLinkOption("test1", i)


def test_option_get_information_config():
    description = "it's ok"
    string = 'some informations'
    i = IntOption('test', description)
    od = OptionDescription('od', '', [i])
    cfg = Config(od)
    with pytest.raises(ValueError):
        cfg.option('test').information.get('noinfo')
    assert cfg.option('test').information.get('noinfo', 'default') == 'default'
    assert cfg.option('test').information.get('doc') == description
#    assert not list_sessions()


def test_option_unknown():
    description = "it's ok"
    string = 'some informations'
    i = IntOption('test', description, informations={'noinfo': 'optdefault'})
    od = OptionDescription('od', '', [i])
    cfg = Config(od)
    #
    with pytest.raises(ConfigError):
        cfg.option('test').unknown.get()
    with pytest.raises(ConfigError):
        # only choice
        cfg.option('test').value.list()


def test_option_description():
    description = "it's ok"
    i = IntOption('test', description)
    od = OptionDescription('od', 'od', [i])
    od2 = OptionDescription('od', '', [od])
    cfg = Config(od2)
    assert cfg.option('od').description() == 'od'
    assert cfg.option('od.test').description() == description


def test_option_get_information_default():
    description = "it's ok"
    string = 'some informations'
    i = IntOption('test', description, informations={'noinfo': 'optdefault'})
    od = OptionDescription('od', '', [i])
    cfg = Config(od)
    #
    assert cfg.option('test').information.get('noinfo', 'falsedefault') == 'optdefault'
    #
    cfg.option('test').information.set('noinfo', 'notdefault')
    assert cfg.option('test').information.get('noinfo', 'falsedefault') == 'notdefault'
#    assert not list_sessions()


def test_option_get_information_config2():
    description = "it's ok"
    string = 'some informations'
    i = IntOption('test', description, informations={'info': string})
    od = OptionDescription('od', '', [i])
    cfg = Config(od)
    with pytest.raises(ValueError):
        cfg.option('test').information.get('noinfo')
    assert cfg.option('test').information.get('info') == string
    with pytest.raises(ValueError):
        cfg.option('test').information.get('noinfo')
    assert cfg.option('test').information.get('noinfo', 'default') == 'default'
    assert cfg.option('test').information.get('doc') == description
#    assert not list_sessions()


def test_optiondescription_get_information():
    description = "it's ok"
    string = 'some informations'
    o = OptionDescription('test', description, [], informations={'info': string})
    od = OptionDescription('od', '', [o])
    cfg = Config(od)
    assert cfg.option('test').information.get('info') == string
    with pytest.raises(ValueError):
        cfg.option('test').information.get('noinfo')
    assert cfg.option('test').information.get('noinfo', 'default') == 'default'
    assert cfg.option('test').information.get('doc') == description
#    assert not list_sessions()


def test_option_isoptiondescription():
    i = IntOption('test', '')
    od = OptionDescription('od', '', [i])
    od = OptionDescription('od', '', [od])
    cfg = Config(od)
    assert cfg.option('od').isoptiondescription()
    assert not cfg.option('od.test').isoptiondescription()
#    assert not list_sessions()


def test_option_double():
    i = IntOption('test', '')
    od = OptionDescription('od1', '', [i])
    od = OptionDescription('od2', '', [od])
    od = OptionDescription('od3', '', [od])
    cfg = Config(od)
    assert cfg.option('od2.od1.test').value.get() is None
    assert cfg.option('od2').option('od1').option('test').value.get() is None
#    assert not list_sessions()


def test_option_multi():
    IntOption('test', '', multi=True)
    IntOption('test', '', multi=True, default_multi=1)
    IntOption('test', '', default=[1], multi=True, default_multi=1)
    #add default_multi to not multi's option
    with pytest.raises(ValueError):
        IntOption('test', '', default_multi=1)
    #unvalid default_multi
    with pytest.raises(ValueError):
        IntOption('test', '', multi=True, default_multi='yes')
#    assert not list_sessions()


def test_unknown_option():
    i = IntOption('test', '')
    od1 = OptionDescription('od', '', [i])
    od2 = OptionDescription('od', '', [od1])
    cfg = Config(od2)
    # test is an option, not an optiondescription
    with pytest.raises(TypeError):
        cfg.option('od.test.unknown').value.get()
    # unknown is an unknown option
    with pytest.raises(AttributeError):
        cfg.option('unknown').value.get()
    # unknown is an unknown option
    with pytest.raises(AttributeError):
        cfg.option('od.unknown').value.get()
    # unknown is an unknown optiondescription
    with pytest.raises(AttributeError):
        cfg.option('od.unknown.suboption').value.get()
#    assert not list_sessions()


def test_optiondescription_list():
    groups.addgroup('notfamily1')
    i = IntOption('test', '')
    i2 = IntOption('test', '')
    od1 = OptionDescription('od', '', [i])
    od1.impl_set_group_type(groups.family)
    od3 = OptionDescription('od2', '', [i2])
    od3.impl_set_group_type(groups.notfamily1)
    od2 = OptionDescription('od', '', [od1, od3])
    od4 = OptionDescription('od', '', [od2])
    cfg = Config(od4)
    assert len(list(cfg.option('od').list())) == 2
    assert len(list(cfg.option('od.od').list())) == 1
    assert len(list(cfg.option('od.od2').list())) == 1
#    assert not list_sessions()


def test_optiondescription_group():
    groups.addgroup('notfamily')
    i = IntOption('test', '')
    i2 = IntOption('test', '')
    od1 = OptionDescription('od', '', [i])
    od1.impl_set_group_type(groups.family)
    od3 = OptionDescription('od2', '', [i2])
    od3.impl_set_group_type(groups.notfamily)
    od2 = OptionDescription('od', '', [od1, od3])
    cfg = Config(od2)
    assert len(list(cfg.list())) == 2
#    assert not list_sessions()


def test_optiondescription_group_redefined():
    try:
        groups.addgroup('notfamily')
    except:
        pass
    i = IntOption('test', '')
    od1 = OptionDescription('od', '', [i])
    od1.impl_set_group_type(groups.family)
    with pytest.raises(ValueError):
        od1.impl_set_group_type(groups.notfamily)
#    assert not list_sessions()


def test_optiondescription_group_leadership():
    i = IntOption('test', '')
    od1 = OptionDescription('od', '', [i])
    with pytest.raises(ConfigError):
        od1.impl_set_group_type(groups.leadership)
#    assert not list_sessions()



def test_asign_optiondescription():
    i = IntOption('test', '')
    od1 = OptionDescription('od', '', [i])
    od2 = OptionDescription('od', '', [od1])
    cfg = Config(od2)
    with pytest.raises(ConfigError):
        cfg.option('od').value.set('test')
    with pytest.raises(ConfigError):
        cfg.option('od').value.reset()
#    assert not list_sessions()


def test_intoption():
    i1 = IntOption('test1', 'description', min_number=3)
    i2 = IntOption('test2', 'description', max_number=3)
    i3 = IntOption('test3', 'description', min_number=3, max_number=6, warnings_only=True)
    od = OptionDescription('od', '', [i1, i2, i3])
    cfg = Config(od)
    with pytest.raises(ValueError):
        cfg.option('test1').value.set(2)
    cfg.option('test1').value.set(3)
    assert cfg.option('test1').value.valid() is True
    cfg.option('test1').value.set(4)
    cfg.option('test2').value.set(2)
    cfg.option('test2').value.set(3)
    with pytest.raises(ValueError):
        cfg.option('test2').value.set(4)
    warnings.simplefilter("always", ValueWarning)
    with warnings.catch_warnings(record=True) as w:
        cfg.option('test3').value.set(2)
    assert cfg.option('test3').value.valid() is True
    assert len(w) == 1
    with warnings.catch_warnings(record=True) as w:
        cfg.option('test3').value.set(7)
    assert cfg.option('test3').value.valid() is True
    cfg.option('test3').value.set(4)
    assert cfg.option('test3').value.valid() is True
    assert len(w) == 1
#    assert not list_sessions()


def test_option_not_in_config():
    i1 = IntOption('test1', 'description', min_number=3)
    with pytest.raises(AttributeError):
        i1.impl_getpath()
#    assert not list_sessions()


def test_option_unknown_func():
    i1 = IntOption('test1', 'description', min_number=3)
    i2 = IntOption('test2', 'description', max_number=3)
    i3 = IntOption('test3', 'description', min_number=3, max_number=6, warnings_only=True)
    od = OptionDescription('od', '', [i1, i2, i3])
    cfg = Config(od)
    with pytest.raises(ConfigError):
        cfg.option('test1').value.unknown()


def test_option_with_index():
    i1 = IntOption('test1', 'description', [4, 5], min_number=3, multi=True)
    i2 = IntOption('test2', 'description', max_number=3)
    i3 = IntOption('test3', 'description', min_number=3, max_number=6, warnings_only=True)
    od = OptionDescription('od', '', [i1, i2, i3])
    cfg = Config(od)
    with pytest.raises(ConfigError):
        cfg.option('test1', 0).value.get()


def test_option_display_name():
    i1 = IntOption('test1', 'description', min_number=3)
    i2 = IntOption('test2', 'description', max_number=3)
    i3 = IntOption('test3', 'description', min_number=3, max_number=6, warnings_only=True)
    od = OptionDescription('od', '', [i1, i2, i3])
    cfg = Config(od,
                 display_name=display_name,
                 )
    assert cfg.option('test1').name() == 'test1'
    assert cfg.option('test1').description() == 'display_name'
