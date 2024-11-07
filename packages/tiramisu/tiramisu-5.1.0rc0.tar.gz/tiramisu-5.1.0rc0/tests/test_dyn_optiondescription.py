# coding: utf-8
from .autopath import do_autopath
do_autopath()
from .config import parse_od_get
import pytest

from tiramisu.setting import groups, owners
from tiramisu import BoolOption, StrOption, ChoiceOption, IPOption, \
    NetworkOption, NetmaskOption, IntOption, FloatOption, \
    StrOption, PortOption, BroadcastOption, DomainnameOption, \
    EmailOption, URLOption, UsernameOption, FilenameOption, SymLinkOption, \
    OptionDescription, DynOptionDescription, submulti, Leadership, \
    Config, \
    Params, ParamOption, ParamValue, ParamIdentifier, ParamSelfOption, ParamDynOption, ParamIndex, ParamSelfInformation, ParamInformation, \
    Calculation, calc_value
from tiramisu.error import PropertiesOptionError, ConfigError, ConflictError, ValueOptionError


def display_name(kls, subconfig, with_quote=False) -> str:
    """Replace the Tiramisu display_name function to display path + description"""
    doc = kls._get_information(subconfig, "doc", None)
    comment = f" ({doc})" if doc and doc != subconfig.path.rsplit('.', 1)[-1] else ""
    if with_quote:
        return f'"{subconfig.path}"{comment}'
    return f"{subconfig.path}{comment}"


class ConvertDynOptionDescription(DynOptionDescription):
    def convert_identifier_to_path(self, identifier):
        # remove dot with is illegal
        return identifier.replace('.', '')


def return_true(value, param=None, identifier=None):
    if value == 'val' and param in [None, 'yes']:
        return
    raise ValueError('no value')


def return_dynval(value='val', identifier=None):
    return value


def return_list2(identifier):
    return [str(identifier), 'val2']


def return_list(val=None, identifier=None):
    if val:
        return val
    return ['val1', 'val2']


def return_list_dot(val=None, identifier=None):
    return ['val.1', 'val.2']


def return_same_list(*args, **kwargs):
    return ['val1', 'val1']


def return_wrong_list(*args, **kwargs):
    return ['---', ' ']


def return_raise():
    raise Exception('error')


def return_str(*args, **kwargs):
    return 'str'


def test_build_dyndescription():
    st1 = StrOption('st', '')
    dod = DynOptionDescription('dod', '', [st1], identifiers=Calculation(return_list))
    od1 = OptionDescription('od', '', [dod])
    cfg = Config(od1)
    assert parse_od_get(cfg.value.get()) == {'dodval1.st': None, 'dodval2.st': None}
    assert cfg.option('dodval1').isdynamic()
    assert cfg.option('dodval1.st').isdynamic()
    assert cfg.option('dodval1').isdynamic(only_self=True)
    assert not cfg.option('dodval1.st').isdynamic(only_self=True)
#    assert not list_sessions()


def test_dyndescription_identifiers():
    st1 = StrOption('st', '')
    dod = DynOptionDescription('dod', '', [st1], identifiers=Calculation(return_list))
    od1 = OptionDescription('od', '', [dod])
    cfg = Config(od1)
    assert parse_od_get(cfg.value.get()) == {'dodval1.st': None, 'dodval2.st': None}
    assert cfg.option('dodval1').identifiers() == ['val1']
    assert cfg.option('dodval1.st').identifiers() == ['val1']
    assert cfg.option('dodval1').identifiers(only_self=True) == ['val1', 'val2']
    with pytest.raises(ConfigError):
        cfg.option('dodval1.st').identifiers(only_self=True)
#    assert not list_sessions()


def test_dyndescription_identifiers_2():
    st1 = StrOption('st', '')
    od = OptionDescription('od', '', [st1])
    dod = DynOptionDescription('dod', '', [od], identifiers=Calculation(return_list))
    od1 = OptionDescription('od', '', [dod])
    cfg = Config(od1)
    assert parse_od_get(cfg.value.get()) == {'dodval1.od.st': None, 'dodval2.od.st': None}
    assert cfg.option('dodval1').identifiers() == ['val1']
    assert cfg.option('dodval1.od').identifiers() == ['val1']
    assert cfg.option('dodval1.od.st').identifiers() == ['val1']
    assert cfg.option('dodval1').identifiers(only_self=True) == ['val1', 'val2']
    with pytest.raises(ConfigError):
        cfg.option('dodval1.od').identifiers(only_self=True)
#    assert not list_sessions()


def test_build_dyndescription_with_int():
    int1 = IntOption('int', '', default=Calculation(calc_value, Params(ParamIdentifier())))
    dod = DynOptionDescription('dod', '', [int1], identifiers=Calculation(return_list, Params(ParamValue([1, 2]))))
    od1 = OptionDescription('od', '', [dod])
    cfg = Config(od1)
    assert parse_od_get(cfg.value.get()) == {'dod1.int': 1, 'dod2.int': 2}
#    assert not list_sessions()


def test_build_dyndescription_with_dot():
    st1 = StrOption('st', '', default=Calculation(calc_value, Params(ParamIdentifier())))
    dod = DynOptionDescription('dod', '', [st1], identifiers=Calculation(return_list_dot))
    od1 = OptionDescription('od', '', [dod])
    cfg = Config(od1)
    assert parse_od_get(cfg.value.get()) == {'dodval_1.st': 'val.1', 'dodval_2.st': 'val.2'}
#    assert not list_sessions()


def test_build_dyndescription_raise():
    st1 = StrOption('st', '')
    dod = DynOptionDescription('dod', '', [st1], identifiers=Calculation(return_raise))
    od1 = OptionDescription('od', '', [dod])
    cfg = Config(od1)
    with pytest.raises(ConfigError):
        cfg.value.get()
#    assert not list_sessions()


def test_build_dyndescription_not_list():
    st1 = StrOption('st', '')
    dod = DynOptionDescription('dod', '', [st1], identifiers=Calculation(return_str))
    od1 = OptionDescription('od', '', [dod])
    cfg = Config(od1)
    with pytest.raises(ValueError):
        cfg.value.get()
#    assert not list_sessions()


def test_subpath_dyndescription():
    st1 = StrOption('st', '')
    dod = DynOptionDescription('dod', '', [st1], identifiers=Calculation(return_list))
    od1 = OptionDescription('od', '', [dod])
    od2 = OptionDescription('od', '', [od1])
    cfg = Config(od2)
    assert parse_od_get(cfg.value.get()) == {'od.dodval1.st': None, 'od.dodval2.st': None}
#    assert not list_sessions()


def test_list_dyndescription():
    st = StrOption('st', '')
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list))
    od = OptionDescription('od', '', [dod])
    od2 = OptionDescription('od', '', [od])
    cfg = Config(od2)
    assert cfg.option('od.dodval1.st').value.get() is None
    assert cfg.option('od.dodval2.st').value.get() is None
#    assert not list_sessions()


def test_unknown_dyndescription():
    st = StrOption('st', '')
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list))
    od = OptionDescription('od', '', [dod])
    od2 = OptionDescription('od', '', [od])
    cfg = Config(od2)
    with pytest.raises(AttributeError):
        cfg.option('od.dodval3').value.get()
    with pytest.raises(AttributeError):
        cfg.option('od.dodval1.novalue').value.get()
    with pytest.raises(AttributeError):
        cfg.option('od.dodval1.stnoval1').value.get()
    with pytest.raises(AttributeError):
        cfg.option('od.dod.st').value.get()
#    assert not list_sessions()


def test_getdoc_dyndescription():
    st1 = StrOption('st', 'doc1')
    dod = DynOptionDescription('dod', 'doc2', [st1], identifiers=Calculation(return_list))
    od1 = OptionDescription('od', '', [dod])
    od2 = OptionDescription('od', '', [od1])
    cfg = Config(od2)
    assert cfg.option('od.dodval1.st').name() == 'st'
    assert cfg.option('od.dodval2.st').name() == 'st'
    assert cfg.option('od.dodval1.st').name(uncalculated=True) == cfg.option('od.dodval2.st').name(uncalculated=True) == 'st'
    assert cfg.option('od.dodval1').name() == 'dodval1'
    assert cfg.option('od.dodval2').name() == 'dodval2'
    assert cfg.option('od.dodval1').name(uncalculated=True) == cfg.option('od.dodval2').name(uncalculated=True) == 'dod'
    assert cfg.option('od.dodval1.st').description() == 'doc1'
    assert cfg.option('od.dodval2.st').description() == 'doc1'
    assert cfg.option('od.dodval1').description() == 'doc2'
    assert cfg.option('od.dodval2').description() == 'doc2'
#    assert not list_sessions()


def test_dyndescription_path():
    st1 = StrOption('st', 'doc1')
    dod = DynOptionDescription('dod', 'doc2', [st1], identifiers=Calculation(return_list))
    od1 = OptionDescription('od', '', [dod])
    od2 = OptionDescription('od', '', [od1])
    cfg = Config(od2)
    assert cfg.option('od.dodval1.st').path() == 'od.dodval1.st'
    assert cfg.option('od.dodval2.st').path() == 'od.dodval2.st'
    assert cfg.option('od.dodval1.st').path(uncalculated=True) == cfg.option('od.dodval2.st').path(uncalculated=True) == 'od.dod.st'
    assert cfg.option('od.dodval1').path() == 'od.dodval1'
    assert cfg.option('od.dodval2').path() == 'od.dodval2'
    assert cfg.option('od.dodval1').path(uncalculated=True) == cfg.option('od.dodval2').path(uncalculated=True) == 'od.dod'


def test_mod_dyndescription():
    st = StrOption('st', '')
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list))
    od = OptionDescription('od', '', [dod])
    od2 = OptionDescription('od', '', [od])
    cfg = Config(od2)
    owner = cfg.owner.get()
    #
    assert cfg.option('od.dodval1.st').value.get() is None
    assert cfg.option('od.dodval2.st').value.get() is None
    assert cfg.option('od.dodval1.st').owner.isdefault()
    assert cfg.option('od.dodval2.st').owner.isdefault()
    #
    cfg.option('od.dodval1.st').value.set('yes')
    assert cfg.option('od.dodval1.st').value.get() == 'yes'
    assert cfg.option('od.dodval2.st').value.get() is None
    assert cfg.option('od.dodval1.st').owner.get() == owner
    assert cfg.option('od.dodval2.st').owner.isdefault()
    #
    cfg.option('od.dodval2.st').value.set('no')
    assert cfg.option('od.dodval1.st').value.get() == 'yes'
    assert cfg.option('od.dodval2.st').value.get() == 'no'
    assert cfg.option('od.dodval1.st').owner.get() == owner
    assert cfg.option('od.dodval2.st').owner.get() == owner
#    assert not list_sessions()


def test_del_dyndescription():
    st = StrOption('st', '')
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list))
    od = OptionDescription('od', '', [dod])
    od2 = OptionDescription('od', '', [od])
    cfg = Config(od2)
    owner = cfg.owner.get()
    assert cfg.option('od.dodval1.st').value.get() is None
    assert cfg.option('od.dodval2.st').value.get() is None
    cfg.option('od.dodval1.st').value.set('yes')
    assert cfg.option('od.dodval1.st').owner.get() == owner
    cfg.option('od.dodval1.st').value.reset()
    assert cfg.option('od.dodval1.st').owner.isdefault()
#    assert not list_sessions()


def test_multi_dyndescription():
    st = StrOption('st', '', multi=True)
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list))
    od = OptionDescription('od', '', [dod])
    od2 = OptionDescription('od', '', [od])
    cfg = Config(od2)
    owner = cfg.owner.get()
    assert cfg.option('od.dodval1.st').value.get() == []
    assert cfg.option('od.dodval2.st').value.get() == []
    assert cfg.option('od.dodval1.st').owner.isdefault()
    assert cfg.option('od.dodval2.st').owner.isdefault()
    cfg.option('od.dodval1.st').value.set(['yes'])
    assert cfg.option('od.dodval1.st').value.get() == ['yes']
    assert cfg.option('od.dodval2.st').value.get() == []
    assert cfg.option('od.dodval1.st').owner.get() == owner
    assert cfg.option('od.dodval2.st').owner.isdefault()
    cfg.option('od.dodval2.st').value.set(['no'])
    assert cfg.option('od.dodval1.st').value.get() == ['yes']
    assert cfg.option('od.dodval2.st').value.get() == ['no']
    assert cfg.option('od.dodval1.st').owner.get() == owner
    assert cfg.option('od.dodval2.st').owner.get() == owner
    cfg.option('od.dodval1.st').value.set(['yes', 'no'])
    assert cfg.option('od.dodval1.st').value.get() == ['yes', 'no']
    cfg.option('od.dodval1.st').value.set(['yes'])
    assert cfg.option('od.dodval1.st').value.get() == ['yes']
#    assert not list_sessions()


def test_prop_dyndescription():
    st = StrOption('st', '', properties=('test',))
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list))
    od = OptionDescription('od', '', [dod])
    od2 = OptionDescription('od', '', [od])
    cfg = Config(od2)
    assert set(cfg.option('od.dodval1.st').property.get()) == set(['test'])
    assert set(cfg.option('od.dodval2.st').property.get()) == set(['test'])
    cfg.option('od.dodval2.st').property.add('test2')
    assert set(cfg.option('od.dodval1.st').property.get()) == set(['test'])
    assert set(cfg.option('od.dodval2.st').property.get()) == set(['test', 'test2'])
    #
    assert set(cfg.option('od.dodval1').property.get()) == set([])
    assert set(cfg.option('od.dodval2').property.get()) == set([])
    cfg.option('od.dodval1').property.add('test1')
    assert set(cfg.option('od.dodval1').property.get()) == set(['test1'])
    assert set(cfg.option('od.dodval2').property.get()) == set([])
    cfg.option('od.dodval1').property.remove('test1')
    assert set(cfg.option('od.dodval1').property.get()) == set([])
    assert set(cfg.option('od.dodval2').property.get()) == set([])
#    assert not list_sessions()


def test_prop_dyndescription_force_store_value():
    st = StrOption('st', '', properties=('force_store_value',))
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list))
    od = OptionDescription('od', '', [dod])
    od2 = OptionDescription('od', '', [od])
    cfg = Config(od2)
    cfg.property.read_write()
    assert parse_od_get(cfg.value.get()) == {'od.dodval1.st': None, 'od.dodval2.st': None}
#    assert not list_sessions()


def test_prop_dyndescription_force_store_value_calculation_prefix():
    lst = StrOption('lst', '', ['val1', 'val2'], multi=True)
    st = StrOption('st', '', Calculation(return_list, Params(ParamIdentifier())) , properties=('force_store_value',))
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list, Params(ParamOption(lst))))
    od = OptionDescription('od', '', [dod, lst])
    od2 = OptionDescription('od', '', [od])
    cfg = Config(od2)
    cfg.property.read_write()
    assert cfg.option('od.dodval1.st').owner.isdefault() == False
    assert cfg.option('od.dodval2.st').owner.isdefault() == False
    assert parse_od_get(cfg.value.get()) == {'od.lst': ['val1', 'val2'], 'od.dodval1.st': 'val1', 'od.dodval2.st': 'val2'}
    #
    cfg.option('od.lst').value.set(['val1', 'val2', 'val3'])
    assert cfg.option('od.dodval3.st').owner.isdefault() == False
    assert cfg.option('od.dodval1.st').owner.isdefault() == False
    assert cfg.option('od.dodval2.st').owner.isdefault() == False
    assert parse_od_get(cfg.value.get()) == {'od.lst': ['val1', 'val2', 'val3'], 'od.dodval1.st': 'val1', 'od.dodval2.st': 'val2', 'od.dodval3.st': 'val3'}

#    assert not list_sessions()


def test_callback_dyndescription():
    st = StrOption('st', '', Calculation(return_dynval))
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list))
    od = OptionDescription('od', '', [dod])
    od2 = OptionDescription('od', '', [od])
    cfg = Config(od2)
    owner = cfg.owner.get()
    assert cfg.option('od.dodval1.st').value.get() == 'val'
    assert cfg.option('od.dodval2.st').value.get() == 'val'
    assert cfg.option('od.dodval1.st').owner.isdefault()
    assert cfg.option('od.dodval2.st').owner.isdefault()
    cfg.option('od.dodval1.st').value.set('val2')
    assert cfg.option('od.dodval1.st').value.get() == 'val2'
    assert cfg.option('od.dodval2.st').value.get() == 'val'
    assert cfg.option('od.dodval1.st').owner.get() == owner
    assert cfg.option('od.dodval2.st').owner.isdefault()
    cfg.option('od.dodval1.st').value.reset()
    assert cfg.option('od.dodval1.st').value.get() == 'val'
    assert cfg.option('od.dodval2.st').value.get() == 'val'
    assert cfg.option('od.dodval1.st').owner.isdefault()
    assert cfg.option('od.dodval2.st').owner.isdefault()
#    assert not list_sessions()


def test_callback_dyndescription_outside_wrong_param():
    lst = StrOption('lst', '', ['val1', 'val2'], multi=True)
    st = StrOption('st', '', Calculation(return_dynval))
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list, Params(ParamOption(lst))))
    out = StrOption('out', '', Calculation(return_dynval, Params(ParamOption(st))))
    od = OptionDescription('od', '', [dod, out])
    od2 = OptionDescription('od', '', [od, lst])
    cfg = Config(od2)
    with pytest.raises(ValueOptionError):
        cfg.value.get()
#    assert not list_sessions()


def test_callback_dyndescription_outside1():
    lst = StrOption('lst', '', ['val1', 'val2'], multi=True)
    st = StrOption('st', '', Calculation(return_dynval))
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list, Params(ParamOption(lst))))
    out = StrOption('out', '', Calculation(return_dynval, Params(ParamDynOption(st, ['val1']))))
    od = OptionDescription('od', '', [dod, out])
    od2 = OptionDescription('od', '', [od, lst])
    cfg = Config(od2)
    assert parse_od_get(cfg.value.get()) == {'od.dodval1.st': 'val', 'od.dodval2.st': 'val', 'od.out': 'val', 'lst': ['val1', 'val2']}
    cfg.option('od.dodval1.st').value.set('val1')
    cfg.option('od.dodval2.st').value.set('val2')
    assert parse_od_get(cfg.value.get()) == {'od.dodval1.st': 'val1', 'od.dodval2.st': 'val2', 'od.out': 'val1', 'lst': ['val1', 'val2']}
    cfg.option('lst').value.set(['val2'])
    with pytest.raises(ConfigError):
        cfg.value.get()
    cfg.option('lst').value.set(['val1'])
    assert parse_od_get(cfg.value.get()) == {'od.dodval1.st': 'val1', 'od.out': 'val1', 'lst': ['val1']}
#    assert not list_sessions()


def test_callback_dyndescription_outside2():
    lst = StrOption('lst', '', ['val1', 'val2'], multi=True)
    out = StrOption('out', '')
    st = StrOption('st', '', Calculation(return_dynval, Params(ParamOption(out))))
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list, Params(ParamOption(lst))))
    od = OptionDescription('od', '', [dod, out])
    od2 = OptionDescription('od', '', [od, lst])
    cfg = Config(od2)
    assert parse_od_get(cfg.value.get()) == {'od.dodval1.st': None, 'od.dodval2.st': None, 'od.out': None, 'lst': ['val1', 'val2']}
    cfg.option('od.out').value.set('val1')
    assert parse_od_get(cfg.value.get()) == {'od.dodval1.st': 'val1', 'od.dodval2.st': 'val1', 'od.out': 'val1', 'lst': ['val1', 'val2']}
#    assert not list_sessions()


def test_callback_dyndescription_outside3():
    lst = StrOption('lst', '', ['val1', 'val2'], multi=True)
    st = StrOption('st', '', 'val1')
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list, Params(ParamOption(lst))), properties=('hidden',))
    out = StrOption('out', '', Calculation(return_dynval, Params(ParamDynOption(st, ['val1']))))
    od = OptionDescription('od', '', [dod, out])
    od2 = OptionDescription('od', '', [od, lst])
    cfg = Config(od2)
    cfg.property.read_write()
    assert parse_od_get(cfg.value.get()) == {'od.out': 'val1', 'lst': ['val1', 'val2']}


def test_callback_dyndescription_subdyn():
    lst = StrOption('lst', '', ['val1', 'val2'], multi=True)
    st = StrOption('st', '', 'val1')
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list, Params(ParamOption(lst))))
    out = StrOption('out', '', Calculation(return_dynval, Params(ParamDynOption(st, ['val1', None]))), multi=True, properties=('notunique',))
    dod2 = DynOptionDescription('dod2', '', [dod, out], identifiers=Calculation(return_list, Params(ParamOption(lst))))
    od = OptionDescription('od', '', [dod2])
    od2 = OptionDescription('od', '', [od, lst])
    cfg = Config(od2)
    cfg.property.read_write()
    assert parse_od_get(cfg.value.get()) == {'od.dod2val1.dodval1.st': 'val1', 'od.dod2val1.dodval2.st': 'val1', 'od.dod2val1.out': ['val1', 'val1'], 'od.dod2val2.dodval1.st': 'val1', 'od.dod2val2.dodval2.st': 'val1', 'od.dod2val2.out': ['val1', 'val1'], 'lst': ['val1', 'val2']}


def test_callback_list_dyndescription():
    st = StrOption('st', '', Calculation(return_list2, Params(ParamIdentifier())), multi=True, properties=('notunique',))
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list))
    od = OptionDescription('od', '', [dod])
    od2 = OptionDescription('od', '', [od])
    cfg = Config(od2)
    owner = cfg.owner.get()
    assert cfg.option('od.dodval1.st').value.get() == ['val1', 'val2']
    assert cfg.option('od.dodval2.st').value.get() == ['val2', 'val2']
    assert cfg.option('od.dodval1.st').owner.isdefault()
    assert cfg.option('od.dodval2.st').owner.isdefault()
    cfg.option('od.dodval1.st').value.set(['val3', 'val2'])
    assert cfg.option('od.dodval1.st').value.get() == ['val3', 'val2']
    assert cfg.option('od.dodval2.st').value.get() == ['val2', 'val2']
    assert cfg.option('od.dodval1.st').owner.get() == owner
    assert cfg.option('od.dodval2.st').owner.isdefault()
#    assert not list_sessions()


def test_mandatory_dyndescription():
    st = StrOption('st', '', properties=('mandatory',))
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list))
    od = OptionDescription('od', '', [dod])
    od2 = OptionDescription('od', '', [od])
    cfg = Config(od2)
    cfg.property.read_only()
    with pytest.raises(PropertiesOptionError):
        cfg.option('od.dodval1.st').value.get()
    with pytest.raises(PropertiesOptionError):
        cfg.option('od.dodval2.st').value.get()
    cfg.property.read_write()
    cfg.option('od.dodval1.st').value.set('val')
    cfg.property.read_only()
    assert cfg.option('od.dodval1.st').value.get() == 'val'
    with pytest.raises(PropertiesOptionError):
        cfg.option('od.dodval2.st').value.get()
    cfg.property.read_write()
    cfg.option('od.dodval1.st').value.reset()
    cfg.property.read_only()
    with pytest.raises(PropertiesOptionError):
        cfg.option('od.dodval1.st').value.get()
#    assert not list_sessions()


def test_build_dyndescription_context():
    val1 = StrOption('val1', '', ['val1', 'val2'], multi=True)
    st1 = StrOption('st', '')
    dod = DynOptionDescription('dod', '', [st1], identifiers=Calculation(return_list, Params(ParamOption(val1))))
    od1 = OptionDescription('od', '', [dod, val1])
    cfg = Config(od1)
    assert parse_od_get(cfg.value.get()) == {'dodval1.st': None, 'dodval2.st': None, 'val1': ['val1', 'val2']}
#    assert not list_sessions()


def test_subpath_dyndescription_context():
    val1 = StrOption('val1', '', ['val1', 'val2'], multi=True)
    st1 = StrOption('st', '')
    dod = DynOptionDescription('dod', '', [st1], identifiers=Calculation(return_list, Params(ParamOption(val1))))
    od1 = OptionDescription('od', '', [dod, val1])
    od2 = OptionDescription('od', '', [od1])
    cfg = Config(od2)
    assert parse_od_get(cfg.value.get()) == {'od.dodval1.st': None, 'od.dodval2.st': None, 'od.val1': ['val1', 'val2']}
#    assert not list_sessions()


def test_list_dyndescription_context():
    val1 = StrOption('val1', '', ['val1', 'val2'], multi=True)
    st = StrOption('st', '')
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list, Params(ParamOption(val1))))
    od = OptionDescription('od', '', [dod, val1])
    od2 = OptionDescription('od', '', [od])
    cfg = Config(od2)
    assert cfg.option('od.dodval1.st').value.get() is None
    assert cfg.option('od.dodval2.st').value.get() is None
    with pytest.raises(AttributeError):
        cfg.option('od.dodval3').value.get()
#    assert not list_sessions()


def test_mod_dyndescription_context():
    val1 = StrOption('val1', '', ['val1', 'val2'], multi=True)
    st = StrOption('st', '')
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list, Params(ParamOption(val1))))
    od = OptionDescription('od', '', [dod, val1])
    od2 = OptionDescription('od', '', [od])
    cfg = Config(od2)
    owner = cfg.owner.get()
    assert cfg.option('od.dodval1.st').value.get() is None
    assert cfg.option('od.dodval2.st').value.get() is None
    assert cfg.option('od.dodval1.st').owner.isdefault()
    assert cfg.option('od.dodval2.st').owner.isdefault()
    cfg.option('od.dodval1.st').value.set('yes')
    assert cfg.option('od.dodval1.st').value.get() == 'yes'
    assert cfg.option('od.dodval2.st').value.get() is None
    assert cfg.option('od.dodval1.st').owner.get() == owner
    assert cfg.option('od.dodval2.st').owner.isdefault()
    cfg.option('od.dodval2.st').value.set('no')
    assert cfg.option('od.dodval1.st').value.get() == 'yes'
    assert cfg.option('od.dodval2.st').value.get() == 'no'
    assert cfg.option('od.dodval1.st').owner.get() == owner
    assert cfg.option('od.dodval2.st').owner.get() == owner
#    assert not list_sessions()


def test_del_dyndescription_context():
    val1 = StrOption('val1', '', ['val1', 'val2'], multi=True)
    st = StrOption('st', '')
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list, Params(ParamOption(val1))))
    od = OptionDescription('od', '', [dod, val1])
    od2 = OptionDescription('od', '', [od])
    cfg = Config(od2)
    owner = cfg.owner.get()
    assert cfg.option('od.dodval1.st').value.get() is None
    assert cfg.option('od.dodval2.st').value.get() is None
    cfg.option('od.dodval1.st').value.set('yes')
    assert cfg.option('od.dodval1.st').owner.get() == owner
    cfg.option('od.dodval1.st').value.reset()
    assert cfg.option('od.dodval1.st').owner.isdefault()
#    assert not list_sessions()


def test_multi_dyndescription_context():
    val1 = StrOption('val1', '', ['val1', 'val2'], multi=True)
    st = StrOption('st', '', multi=True, properties=('notunique',))
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list, Params(ParamOption(val1))))
    od = OptionDescription('od', '', [dod, val1])
    od2 = OptionDescription('od', '', [od])
    cfg = Config(od2)
    owner = cfg.owner.get()
    assert cfg.option('od.dodval1.st').value.get() == []
    assert cfg.option('od.dodval2.st').value.get() == []
    assert cfg.option('od.dodval1.st').owner.isdefault()
    assert cfg.option('od.dodval2.st').owner.isdefault()
    cfg.option('od.dodval1.st').value.set(['yes'])
    assert cfg.option('od.dodval1.st').value.get() == ['yes']
    assert cfg.option('od.dodval2.st').value.get() == []
    assert cfg.option('od.dodval1.st').owner.get() == owner
    assert cfg.option('od.dodval2.st').owner.isdefault()
    cfg.option('od.dodval2.st').value.set(['no'])
    assert cfg.option('od.dodval1.st').value.get() == ['yes']
    assert cfg.option('od.dodval2.st').value.get() == ['no']
    assert cfg.option('od.dodval1.st').owner.get() == owner
    assert cfg.option('od.dodval2.st').owner.get() == owner
    cfg.option('od.dodval1.st').value.set(['yes', 'yes'])
    assert cfg.option('od.dodval1.st').value.get() == ['yes', 'yes']
    cfg.option('od.dodval1.st').value.set(['yes'])
    assert cfg.option('od.dodval1.st').value.get() == ['yes']
#    assert not list_sessions()


def test_prop_dyndescription_context():
    val1 = StrOption('val1', '', ['val1', 'val2'], multi=True)
    st = StrOption('st', '', properties=('test',))
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list, Params(ParamOption(val1))))
    od = OptionDescription('od', '', [dod, val1])
    od2 = OptionDescription('od', '', [od])
    cfg = Config(od2)
    assert set(cfg.option('od.dodval1.st').property.get()) == set(['test'])
    assert set(cfg.option('od.dodval2.st').property.get()) == set(['test'])
    cfg.option('od.dodval2.st').property.add('test2')
    assert set(cfg.option('od.dodval1.st').property.get()) == set(['test'])
    assert set(cfg.option('od.dodval2.st').property.get()) == set(['test', 'test2'])
    cfg.option('od.dodval1.st').permissive.add('test')
    assert set(cfg.option('od.dodval1.st').property.get()) == set([])
    assert set(cfg.option('od.dodval2.st').property.get()) == set(['test', 'test2'])
#    assert not list_sessions()


def test_callback_dyndescription_context():
    val1 = StrOption('val1', '', ['val1', 'val2'], multi=True)
    st = StrOption('st', '', Calculation(return_dynval))
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list))
    od = OptionDescription('od', '', [dod, val1])
    od2 = OptionDescription('od', '', [od])
    cfg = Config(od2)
    owner = cfg.owner.get()
    assert cfg.option('od.dodval1.st').value.get() == 'val'
    assert cfg.option('od.dodval2.st').value.get() == 'val'
    assert cfg.option('od.dodval1.st').owner.isdefault()
    assert cfg.option('od.dodval2.st').owner.isdefault()
    cfg.option('od.dodval1.st').value.set('val2')
    assert cfg.option('od.dodval1.st').value.get() == 'val2'
    assert cfg.option('od.dodval2.st').value.get() == 'val'
    assert cfg.option('od.dodval1.st').owner.get() == owner
    assert cfg.option('od.dodval2.st').owner.isdefault()
    cfg.option('od.dodval1.st').value.reset()
    assert cfg.option('od.dodval1.st').value.get() == 'val'
    assert cfg.option('od.dodval2.st').value.get() == 'val'
    assert cfg.option('od.dodval1.st').owner.isdefault()
    assert cfg.option('od.dodval2.st').owner.isdefault()
#    assert not list_sessions()


def test_mandatory_dyndescription_context():
    val1 = StrOption('val1', '', ['val1', 'val2'], multi=True)
    st = StrOption('st', '', properties=('mandatory',))
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list, Params(ParamOption(val1))))
    od = OptionDescription('od', '', [dod, val1])
    od2 = OptionDescription('od', '', [od])
    cfg = Config(od2)
    cfg.property.read_only()
    with pytest.raises(PropertiesOptionError):
        cfg.option('od.dodval1.st').value.get()
    with pytest.raises(PropertiesOptionError):
        cfg.option('od.dodval2.st').value.get()
    cfg.property.read_write()
    cfg.option('od.dodval1.st').value.set('val')
    cfg.property.read_only()
    assert cfg.option('od.dodval1.st').value.get() == 'val'
    with pytest.raises(PropertiesOptionError):
        cfg.option('od.dodval2.st').value.get()
    cfg.property.read_write()
    cfg.option('od.dodval1.st').value.reset()
    cfg.property.read_only()
    with pytest.raises(PropertiesOptionError):
        cfg.option('od.dodval1.st').value.get()
#    assert not list_sessions()


def test_increase_dyndescription_context():
    val1 = StrOption('val1', '', ['val1', 'val2'], multi=True)
    st = StrOption('st', '', properties=('mandatory',))
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list, Params(ParamOption(val1))))
    od = OptionDescription('od', '', [dod, val1])
    od2 = OptionDescription('od', '', [od])
    cfg = Config(od2)
    cfg.property.read_write()
    assert cfg.option('od.dodval1.st').value.get() is None
    assert cfg.option('od.dodval2.st').value.get() is None
    with pytest.raises(AttributeError):
        cfg.option('od.dodval3.st').value.get()
    cfg.option('od.val1').value.set(['val1', 'val2', 'val3'])
    assert cfg.option('od.dodval1.st').value.get() is None
    assert cfg.option('od.dodval2.st').value.get() is None
    assert cfg.option('od.dodval3.st').value.get() is None
#    assert not list_sessions()


def test_decrease_dyndescription_context():
    val1 = StrOption('val1', '', ['val1', 'val2'], multi=True)
    st = StrOption('st', '', properties=('mandatory',))
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list, Params(ParamOption(val1))))
    od = OptionDescription('od', '', [dod, val1])
    od2 = OptionDescription('od', '', [od])
    cfg = Config(od2)
    owner = cfg.owner.get()
    cfg.property.read_write()
    assert cfg.option('od.dodval1.st').value.get() is None
    assert cfg.option('od.dodval2.st').value.get() is None
    cfg.option('od.dodval2.st').value.set('yes')
    assert cfg.option('od.dodval1.st').value.get() is None
    assert cfg.option('od.dodval2.st').value.get() == 'yes'
    assert cfg.option('od.dodval1.st').owner.isdefault()
    assert cfg.option('od.dodval2.st').owner.get() == owner
    with pytest.raises(AttributeError):
        cfg.option('od.dodval3').value.get()
    cfg.option('od.val1').value.set(['val1'])
    assert cfg.option('od.dodval1.st').value.get() is None
    with pytest.raises(AttributeError):
        cfg.option('od.dodval2').value.get()
    with pytest.raises(AttributeError):
        cfg.option('od.dodval3').value.get()
    assert cfg.option('od.dodval1.st').owner.isdefault()
    with pytest.raises(AttributeError):
        cfg.option('od.dodval2.st').owner.get()
    with pytest.raises(AttributeError):
        cfg.option('od.dodval2.st').value.get()
#    assert not list_sessions()


def test_dyndescription_root():
    boolean = BoolOption('boolean', '', True)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(boolean),
                                                   'expected': ParamValue(False),
                                                   'default': ParamValue(None)}))
    st1 = StrOption('st', '', properties=(disabled_property,))
    dod = DynOptionDescription('dod', '', [boolean, st1], identifiers=Calculation(return_list))
    with pytest.raises(ConfigError):
        cfg = Config(dod)
#    assert not list_sessions()


def test_dyndescription_disable_identifier_root():
    boolean = BoolOption('boolean', '', True)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(boolean),
                                                   'expected': ParamValue(False),
                                                   'default': ParamValue(None)}))
    val = StrOption('val', '', ['ext1', 'ext2'], properties=(disabled_property,), multi=True)
    st1 = StrOption('st', '')
    dod = DynOptionDescription('dod', '', [st1], identifiers=Calculation(calc_value, Params(ParamOption(val, notraisepropertyerror=True))), properties=(disabled_property,))
    od1 = OptionDescription('root', 'root', [boolean, val, dod])
    cfg = Config(od1)
    cfg.property.read_write()
    assert parse_od_get(cfg.value.get()) == {'boolean': True, 'val': ['ext1', 'ext2'], 'dodext1.st': None, 'dodext2.st': None}
    #
    cfg.option('boolean').value.set(False)
    assert parse_od_get(cfg.value.get()) == {'boolean': False}
#    assert not list_sessions()


def test_dyndescription_disable_identifier_root_2():
    boolean = BoolOption('boolean', '', False)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(boolean),
                                                   'expected': ParamValue(False),
                                                   'default': ParamValue(None)}))
    val = StrOption('val', '', ['ext1', 'ext2'], properties=(disabled_property,), multi=True)
    st1 = StrOption('st', '')
    dod = DynOptionDescription('dod', '', [st1], identifiers=Calculation(calc_value, Params(ParamOption(val, notraisepropertyerror=True))), properties=(disabled_property,))
    od1 = OptionDescription('root', 'root', [boolean, val, dod])
    cfg = Config(od1)
    cfg.property.read_write()
    assert parse_od_get(cfg.value.get()) == {'boolean': False}
    #
    cfg.option('boolean').value.set(True)
    assert parse_od_get(cfg.value.get()) == {'boolean': True, 'val': ['ext1', 'ext2'], 'dodext1.st': None, 'dodext2.st': None}
#    assert not list_sessions()


def test_dyndescription_disable_identifier():
    boolean = BoolOption('boolean', '', True)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(boolean),
                                                   'expected': ParamValue(False),
                                                   'default': ParamValue(None)}))
    val = StrOption('val', '', ['ext1', 'ext2'], properties=(disabled_property,), multi=True)
    st1 = StrOption('st', '')
    dod = DynOptionDescription('dod', '', [st1], identifiers=Calculation(calc_value, Params(ParamOption(val, notraisepropertyerror=True))), properties=(disabled_property,))
    od = OptionDescription('root', 'root', [boolean, val, dod])
    od1 = OptionDescription('root', 'root', [od])
    cfg = Config(od1)
    cfg.property.read_write()
    assert parse_od_get(cfg.value.get()) == {'root.boolean': True, 'root.val': ['ext1', 'ext2'], 'root.dodext1.st': None, 'root.dodext2.st': None}
    #
    cfg.option('root.boolean').value.set(False)
    assert parse_od_get(cfg.value.get()) == {'root.boolean': False}
#    assert not list_sessions()


def test_requires_dyndescription():
    boolean = BoolOption('boolean', '', True)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(boolean, raisepropertyerror=True),
                                                   'expected': ParamValue(False),
                                                   'default': ParamValue(None)}))
    st1 = StrOption('st', '', properties=(disabled_property,))
    dod = DynOptionDescription('dod', '', [st1], identifiers=Calculation(return_list))
    od1 = OptionDescription('od', '', [dod])
    od2 = OptionDescription('od', '', [od1, boolean])
    cfg = Config(od2)
    cfg.property.read_write()
    assert cfg.option('od.dodval1.st').value.get() is None
    assert cfg.option('od.dodval2.st').value.get() is None
    #
    cfg.option('boolean').value.set(False)
    props = []
    try:
        cfg.option('od.dodval1.st').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])
    props = []
    try:
        cfg.option('od.dodval2.st').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])
    #
    cfg.option('boolean').value.set(True)
    assert cfg.option('od.dodval1.st').value.get() is None
    assert cfg.option('od.dodval2.st').value.get() is None
    #transitive
    cfg.option('boolean').property.add('disabled')
    props = []
    try:
        cfg.option('od.dodval1.st').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])
    props = []
    try:
        cfg.option('od.dodval2.st').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])
#    assert not list_sessions()


def test_requires_dyndescription_boolean():
    boolean1 = BoolOption('boolean1', '', True)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(boolean1, raisepropertyerror=True),
                                                   'expected': ParamValue(False),
                                                   'default': ParamValue(None)}))
    boolean = BoolOption('boolean', '', True, properties=(disabled_property,))
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(boolean, raisepropertyerror=True),
                                                   'expected': ParamValue(False),
                                                   'default': ParamValue(None)}))
    st = StrOption('st', '', properties=(disabled_property,))
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list))
    od = OptionDescription('od', '', [dod])
    od2 = OptionDescription('od', '', [od, boolean1, boolean])
    cfg = Config(od2)
    cfg.property.read_write()
    assert parse_od_get(cfg.value.get()) == {'boolean1': True,
                                             'boolean': True,
                                             'od.dodval1.st': None,
                                             'od.dodval2.st': None}
    #
    cfg.option('boolean').value.set(False)
    assert parse_od_get(cfg.value.get()) == {'boolean1': True,
                                             'boolean': False}
    #
    cfg.option('boolean').value.set(True)
    assert parse_od_get(cfg.value.get()) == {'boolean1': True,
                                             'boolean': True,
                                             'od.dodval1.st': None,
                                             'od.dodval2.st': None}
    #
    cfg.option('boolean1').value.set(False)
    assert parse_od_get(cfg.value.get()) == {'boolean1': False}
#    assert not list_sessions()


def test_requires_dyndescription_in_dyn():
    boolean = BoolOption('boolean', '', True)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(boolean, raisepropertyerror=True),
                                                   'expected': ParamValue(False),
                                                   'default': ParamValue(None)}))
    st = StrOption('st', '', properties=(disabled_property,))
    dod = DynOptionDescription('dod', '', [boolean, st], identifiers=Calculation(return_list))
    od = OptionDescription('od', '', [dod])
    od2 = OptionDescription('od', '', [od])
    cfg = Config(od2)
    cfg.property.read_write()

    assert cfg.option('od.dodval1.st').value.get() is None
    assert cfg.option('od.dodval2.st').value.get() is None
    #
    cfg.option('od.dodval1.boolean').value.set(False)

    props = []
    try:
        cfg.option('od.dodval1.st').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert props == frozenset(['disabled'])
    props = []
    cfg.option('od.dodval2.st').value.get()
    #
    cfg.option('od.dodval1.boolean').value.set(True)
    assert cfg.option('od.dodval1.st').value.get() is None
    assert cfg.option('od.dodval2.st').value.get() is None
#    assert not list_sessions()


def calc_value_not_same(param, condition, expected, default, identifier):
    if identifier == 'val1':
        index = 0
    else:
        index = 1
    return calc_value(param, condition=condition[index], expected=expected, default=default)


def test_requires_dyndescription_in_dyn_not_same():
    boolean = BoolOption('boolean', '', True)
    disabled_property = Calculation(calc_value_not_same,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(boolean, raisepropertyerror=True),
                                                   'expected': ParamValue(False),
                                                   'default': ParamValue(None),
                                                   'identifier': ParamIdentifier()}))
    st = StrOption('st', '', properties=(disabled_property,))
    dod1 = DynOptionDescription('dod1', '', [boolean], identifiers=Calculation(return_list))
    dod2 = DynOptionDescription('dod2', '', [st], identifiers=Calculation(return_list))
    od = OptionDescription('od', '', [dod1, dod2])
    od2 = OptionDescription('od', '', [od])
    cfg = Config(od2)
    cfg.property.read_write()

    assert cfg.option('od.dod2val1.st').value.get() is None
    assert cfg.option('od.dod2val2.st').value.get() is None
    #
    cfg.option('od.dod1val1.boolean').value.set(False)

    props = []
    try:
        cfg.option('od.dod2val1.st').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert props == frozenset(['disabled'])
    props = []
    cfg.option('od.dod2val2.st').value.get()
    #
    cfg.option('od.dod1val1.boolean').value.set(True)
    assert cfg.option('od.dod2val1.st').value.get() is None
    assert cfg.option('od.dod2val2.st').value.get() is None
#    assert not list_sessions()


def test_requires_dyndescription2():
    boolean = BoolOption('boolean', '', True)
    st1 = StrOption('st', '')
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(boolean, raisepropertyerror=True),
                                                   'expected': ParamValue(False),
                                                   'default': ParamValue(None)}))
    dod = DynOptionDescription('dod', '', [st1], identifiers=Calculation(return_list), properties=(disabled_property,))
    od1 = OptionDescription('od', '', [dod])
    od2 = OptionDescription('od', '', [od1, boolean])
    cfg = Config(od2)
    cfg.property.read_write()
    assert cfg.option('od.dodval1.st').value.get() is None
    assert cfg.option('od.dodval2.st').value.get() is None
    #
    cfg.option('boolean').value.set(False)
    props = []
    try:
        cfg.option('od.dodval1.st').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])
    props = []
    try:
        cfg.option('od.dodval2.st').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])
    #
    cfg.option('boolean').value.set(True)
    assert cfg.option('od.dodval1.st').value.get() is None
    assert cfg.option('od.dodval2.st').value.get() is None
    #transitive
    cfg.option('boolean').property.add('disabled')
    props = []
    try:
        cfg.option('od.dodval1.st').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])
    props = []
    try:
        cfg.option('od.dodval2.st').value.get()
    except PropertiesOptionError as err:
        props = err.proptype
    assert frozenset(props) == frozenset(['disabled'])
#    assert not list_sessions()


def test_validator_dyndescription():
    val1 = StrOption('val1', '', ['val1', 'val2'], multi=True)
    st = StrOption('st', '', validators=[Calculation(return_true, Params((ParamSelfOption(), ParamValue('yes'))))], default='val')
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list))
    od = OptionDescription('od', '', [dod, val1])
    od2 = OptionDescription('od', '', [od])
    cfg = Config(od2)
    assert cfg.option('od.dodval1.st').value.get() == 'val'
    with pytest.raises(ValueError):
        cfg.option('od.dodval1.st').value.set('no')
    cfg.option('od.dodval1.st').value.set('val')
#    assert not list_sessions()


def test_makedict_dyndescription_context():
    val1 = StrOption('val1', '', ['val1', 'val2'], multi=True)
    st = StrOption('st', '')
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list))
    od = OptionDescription('od', '', [dod, val1])
    od2 = OptionDescription('od', '', [od])
    cfg = Config(od2)
    cfg.option('od.dodval1.st').value.set('yes')
    assert parse_od_get(cfg.value.get()) == {'od.val1': ['val1', 'val2'], 'od.dodval1.st': 'yes', 'od.dodval2.st': None}
#    assert not list_sessions()


#def test_find_dyndescription_context():
#    val1 = StrOption('val1', '', ['val1', 'val2'], multi=True)
#    st = StrOption('st', '')
#    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list))
#    od = OptionDescription('od', '', [dod, val1])
#    od2 = OptionDescription('od', '', [od])
#    cfg = Config(od2)
#    cfg.option('od.dodval1.st').value.set('yes')
#    ret = cfg.option.find('st', first=True)
#    assert ret.value.get() == "yes"
#    ret = cfg.option.find('st', first=True)
#    assert isinstance(ret.get(), SynDynOption)
#    #assert cfg.option.find(bytype=StrOption, type='path') == ['od.dodval1.st', 'od.dodval2.st', 'od.val1']
#    #opts = cfg.option.find(byvalue='yes')
#    #assert len(opts) == 1
#    #assert isinstance(opts[0], SynDynOption)
#    #assert opts[0].impl_getname() == 'st'
#    with pytest.raises(AttributeError):
#        list(cfg.option.find('strnotexists'))
##    assert not list_sessions()


def test_information_dyndescription_context():
    val1 = StrOption('val1', '', ['val1', 'val2'], multi=True)
    st = StrOption('st', '', informations={'testst': 'val2'})
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list), informations={'testod': 'val1'})
    od = OptionDescription('od', '', [dod, val1])
    od2 = OptionDescription('od', '', [od])
    cfg = Config(od2)
    cfg.information.set('testcfgod', 'val3')
    assert cfg.option('od.dodval1').information.get('testod') == 'val1'
    assert cfg.option('od.dodval2').information.get('testod') == 'val1'
    assert cfg.option('od.dodval1.st').information.get('testst') == 'val2'
    assert cfg.option('od.dodval2.st').information.get('testst') == 'val2'
    assert cfg.information.get('testcfgod') == 'val3'
#    assert not list_sessions()


def test_all_dyndescription():
    st = StrOption('st', '')
    ip = IPOption('ip', '')
    network = NetworkOption('network', '')
    netmask = NetmaskOption('netmask', '')
    ch = ChoiceOption('ch', '', ('val1', 'val2', 'val3'))
    ch1 = ChoiceOption('ch1', '', Calculation(return_list))
    boo = BoolOption('boo', '')
    intr = IntOption('intr', '')
    floa = FloatOption('floa', '')
    uni = StrOption('uni', '')
    port = PortOption('port', '')
    broad = BroadcastOption('broad', '')
    domain = DomainnameOption('domain', '')
    email = EmailOption('email', '')
    url = URLOption('url', '')
    username = UsernameOption('username', '')
    filename = FilenameOption('filename', '')
    dod = DynOptionDescription('dod', '', [st, ip, network, netmask, ch, ch1,
                                           boo, intr, floa, uni, port, broad,
                                           domain, email, url, username,
                                           filename], identifiers=Calculation(return_list))
    od1 = OptionDescription('od', '', [dod])
    cfg = Config(od1)
    assert cfg.option('dodval1.st').value.get() is None
    assert cfg.option('dodval1.ip').value.get() is None
    assert cfg.option('dodval1.network').value.get() is None
    assert cfg.option('dodval1.netmask').value.get() is None
    assert cfg.option('dodval1.ch').value.get() is None
    assert cfg.option('dodval1.ch1').value.get() is None
    assert cfg.option('dodval1.boo').value.get() is None
    assert cfg.option('dodval1.intr').value.get() is None
    assert cfg.option('dodval1.floa').value.get() is None
    assert cfg.option('dodval1.uni').value.get() is None
    assert cfg.option('dodval1.port').value.get() is None
    assert cfg.option('dodval1.broad').value.get() is None
    assert cfg.option('dodval1.domain').value.get() is None
    assert cfg.option('dodval1.email').value.get() is None
    assert cfg.option('dodval1.url').value.get() is None
    assert cfg.option('dodval1.username').value.get() is None
    assert cfg.option('dodval1.filename').value.get() is None
    #
    cfg.option('dodval1.st').value.set("no")
    cfg.option('dodval1.ip').value.set("1.1.1.1")
    cfg.option('dodval1.network').value.set("1.1.1.0")
    cfg.option('dodval1.netmask').value.set("255.255.255.0")
    cfg.option('dodval1.ch').value.set("val1")
    cfg.option('dodval1.ch1').value.set("val2")
    cfg.option('dodval1.boo').value.set(True)
    cfg.option('dodval1.intr').value.set(1)
    cfg.option('dodval1.floa').value.set(0.1)
    cfg.option('dodval1.uni').value.set(u"no")
    cfg.option('dodval1.port').value.set('80')
    cfg.option('dodval1.broad').value.set("1.1.1.255")
    cfg.option('dodval1.domain').value.set("test.com")
    cfg.option('dodval1.email').value.set("test@test.com")
    cfg.option('dodval1.url').value.set("http://test.com")
    cfg.option('dodval1.username').value.set("user1")
    cfg.option('dodval1.filename').value.set("/tmp")
    assert cfg.option('dodval1.st').value.get() == "no"
    assert cfg.option('dodval1.ip').value.get() == "1.1.1.1"
    assert cfg.option('dodval1.network').value.get() == "1.1.1.0"
    assert cfg.option('dodval1.netmask').value.get() == "255.255.255.0"
    assert cfg.option('dodval1.ch').value.get() == "val1"
    assert cfg.option('dodval1.ch1').value.get() == "val2"
    assert cfg.option('dodval1.boo').value.get() is True
    assert cfg.option('dodval1.intr').value.get() == 1
    assert cfg.option('dodval1.floa').value.get() == 0.1
    assert cfg.option('dodval1.uni').value.get() == u"no"
    assert cfg.option('dodval1.port').value.get() == '80'
    assert cfg.option('dodval1.broad').value.get() == "1.1.1.255"
    assert cfg.option('dodval1.domain').value.get() == "test.com"
    assert cfg.option('dodval1.email').value.get() == "test@test.com"
    assert cfg.option('dodval1.url').value.get() == "http://test.com"
    assert cfg.option('dodval1.username').value.get() == "user1"
    assert cfg.option('dodval1.filename').value.get() == "/tmp"
    assert cfg.option('dodval2.st').value.get() is None
    assert cfg.option('dodval2.ip').value.get() is None
    assert cfg.option('dodval2.network').value.get() is None
    assert cfg.option('dodval2.netmask').value.get() is None
    assert cfg.option('dodval2.ch').value.get() is None
    assert cfg.option('dodval2.ch1').value.get() is None
    assert cfg.option('dodval2.boo').value.get() is None
    assert cfg.option('dodval2.intr').value.get() is None
    assert cfg.option('dodval2.floa').value.get() is None
    assert cfg.option('dodval2.uni').value.get() is None
    assert cfg.option('dodval2.port').value.get() is None
    assert cfg.option('dodval2.broad').value.get() is None
    assert cfg.option('dodval2.domain').value.get() is None
    assert cfg.option('dodval2.email').value.get() is None
    assert cfg.option('dodval2.url').value.get() is None
    assert cfg.option('dodval2.username').value.get() is None
    assert cfg.option('dodval2.filename').value.get() is None
#    assert not list_sessions()


def test_leadership_dyndescription():
    st1 = StrOption('st1', "", multi=True)
    st2 = StrOption('st2', "", multi=True)
    stm = Leadership('st1', '', [st1, st2])
    st = DynOptionDescription('st', '', [stm], identifiers=Calculation(return_list))
    od = OptionDescription('od', '', [st])
    od1 = OptionDescription('od', '', [od])
    cfg = Config(od1)
    owner = cfg.owner.get()
    #
    assert parse_od_get(cfg.value.get()) == {'od.stval2.st1.st1': [], 'od.stval1.st1.st1': []}
    assert cfg.option('od.stval1.st1.st1').value.get() == []
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.isdefault()
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
    #
    cfg.option('od.stval1.st1.st1').value.set(['yes'])
    assert parse_od_get(cfg.value.get()) == {'od.stval1.st1.st1': [{'od.stval1.st1.st1': 'yes', 'od.stval1.st1.st2': None}], 'od.stval2.st1.st1': []}
    assert cfg.option('od.stval1.st1.st1').value.get() == ['yes']
    assert cfg.option('od.stval1.st1.st2', 0).value.get() == None
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.st1.st2', 0).owner.isdefault()
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
    #
    cfg.option('od.stval1.st1.st2', 0).value.set('no')
    assert cfg.option('od.stval1.st1.st1').value.get() == ['yes']
    assert cfg.option('od.stval1.st1.st2', 0).value.get() == 'no'
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.st1.st2', 0).owner.get() == owner
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
    #
    cfg.option('od.stval1.st1.st1').value.pop(0)
    assert cfg.option('od.stval1.st1.st1').value.get() == []
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
    #
    cfg.option('od.stval1.st1.st1').value.set(['yes'])
    cfg.option('od.stval1.st1.st2', 0).value.set('yes')
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.st1.st2', 0).owner.get() == owner
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    cfg.option('od.stval1.st1.st2', 0).value.reset()
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.st1.st2', 0).owner.isdefault()
    #
    cfg.option('od.stval1.st1.st1').value.set(['yes'])
    cfg.option('od.stval1.st1.st2', 0).value.set('yes')
    cfg.option('od.stval1.st1.st1').value.reset()
    assert cfg.option('od.stval1.st1.st1').value.get() == []
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.isdefault()
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
#    assert not list_sessions()


def test_leadership_dyndescription_force_store_value_leader():
    st1 = StrOption('st1', "", multi=True, default=Calculation(return_list), properties=('force_store_value',))
    st2 = StrOption('st2', "", multi=True, default=Calculation(return_list, Params(ParamOption(st1))))
    stm = Leadership('st1', '', [st1, st2])
    val1 = StrOption('val1', '', multi=True, default=['val1', 'val2'])
    st = DynOptionDescription('st', '', [stm], identifiers=Calculation(return_list, Params(ParamOption(val1))))
    od = OptionDescription('od', '', [val1, st])
    od1 = OptionDescription('od', '', [od])
    cfg = Config(od1)
    cfg.property.read_write()
    assert cfg.option('od.stval1.st1.st1').owner.isdefault() == False
    assert cfg.option('od.stval2.st1.st1').owner.isdefault() == False
    assert cfg.option('od.stval1.st1.st2', 0).owner.isdefault() == True
    assert cfg.option('od.stval1.st1.st2', 1).owner.isdefault() == True
    assert cfg.option('od.stval2.st1.st2', 0).owner.isdefault() == True
    assert cfg.option('od.stval2.st1.st2', 1).owner.isdefault() == True
    assert parse_od_get(cfg.value.get()) == {'od.val1': ['val1', 'val2'], 'od.stval1.st1.st1': [{'od.stval1.st1.st1': 'val1', 'od.stval1.st1.st2': 'val1'}, {'od.stval1.st1.st1': 'val2', 'od.stval1.st1.st2': 'val2'}], 'od.stval2.st1.st1': [{'od.stval2.st1.st1': 'val1', 'od.stval2.st1.st2': 'val1'}, {'od.stval2.st1.st1': 'val2', 'od.stval2.st1.st2': 'val2'}]}
    #
    cfg.option('od.val1').value.set(['val1', 'val2', 'val3'])
    assert cfg.option('od.stval3.st1.st1').owner.isdefault() == False
    assert cfg.option('od.stval3.st1.st2', 0).owner.isdefault() == True
    assert cfg.option('od.stval3.st1.st2', 1).owner.isdefault() == True
    assert parse_od_get(cfg.value.get()) == {'od.val1': ['val1', 'val2', 'val3'], 'od.stval1.st1.st1': [{'od.stval1.st1.st1': 'val1', 'od.stval1.st1.st2': 'val1'}, {'od.stval1.st1.st1': 'val2', 'od.stval1.st1.st2': 'val2'}], 'od.stval2.st1.st1': [{'od.stval2.st1.st1': 'val1', 'od.stval2.st1.st2': 'val1'}, {'od.stval2.st1.st1': 'val2', 'od.stval2.st1.st2': 'val2'}], 'od.stval3.st1.st1': [{'od.stval3.st1.st1': 'val1', 'od.stval3.st1.st2': 'val1'}, {'od.stval3.st1.st1': 'val2', 'od.stval3.st1.st2': 'val2'}]}
    #
    cfg.option('od.stval3.st1.st1').value.set(['val1', 'val2', 'val3'])
    assert cfg.option('od.stval3.st1.st1').owner.isdefault() == False
    assert cfg.option('od.stval3.st1.st2', 0).owner.isdefault() == True
    assert cfg.option('od.stval3.st1.st2', 1).owner.isdefault() == True
    assert cfg.option('od.stval3.st1.st2', 2).owner.isdefault() == True
    assert parse_od_get(cfg.value.get()) == {'od.val1': ['val1', 'val2', 'val3'], 'od.stval1.st1.st1': [{'od.stval1.st1.st1': 'val1', 'od.stval1.st1.st2': 'val1'}, {'od.stval1.st1.st1': 'val2', 'od.stval1.st1.st2': 'val2'}], 'od.stval2.st1.st1': [{'od.stval2.st1.st1': 'val1', 'od.stval2.st1.st2': 'val1'}, {'od.stval2.st1.st1': 'val2', 'od.stval2.st1.st2': 'val2'}], 'od.stval3.st1.st1': [{'od.stval3.st1.st1': 'val1', 'od.stval3.st1.st2': 'val1'}, {'od.stval3.st1.st1': 'val2', 'od.stval3.st1.st2': 'val2'}, {'od.stval3.st1.st1': 'val3', 'od.stval3.st1.st2': 'val3'}]}
#    assert not list_sessions()


def test_leadership_dyndescription_force_store_value():
    st1 = StrOption('st1', "", multi=True, default=Calculation(return_list))
    st2 = StrOption('st2', "", multi=True, properties=('force_store_value',), default=Calculation(return_list, Params(ParamOption(st1))))
    stm = Leadership('st1', '', [st1, st2])
    val1 = StrOption('val1', '', multi=True, default=['val1', 'val2'])
    st = DynOptionDescription('st', '', [stm], identifiers=Calculation(return_list, Params(ParamOption(val1))))
    od = OptionDescription('od', '', [val1, st])
    od1 = OptionDescription('od', '', [od])
    cfg = Config(od1)
    cfg.property.read_write()
    assert cfg.option('od.stval1.st1.st1').owner.isdefault() == True
    assert cfg.option('od.stval2.st1.st1').owner.isdefault() == True
    assert cfg.option('od.stval1.st1.st2', 0).owner.isdefault() == False
    assert cfg.option('od.stval1.st1.st2', 1).owner.isdefault() == False
    assert cfg.option('od.stval2.st1.st2', 0).owner.isdefault() == False
    assert cfg.option('od.stval2.st1.st2', 1).owner.isdefault() == False
    assert parse_od_get(cfg.value.get()) == {'od.val1': ['val1', 'val2'], 'od.stval1.st1.st1': [{'od.stval1.st1.st1': 'val1', 'od.stval1.st1.st2': 'val1'}, {'od.stval1.st1.st1': 'val2', 'od.stval1.st1.st2': 'val2'}], 'od.stval2.st1.st1': [{'od.stval2.st1.st1': 'val1', 'od.stval2.st1.st2': 'val1'}, {'od.stval2.st1.st1': 'val2', 'od.stval2.st1.st2': 'val2'}]}
    #
    cfg.option('od.val1').value.set(['val1', 'val2', 'val3'])
    assert cfg.option('od.stval3.st1.st1').owner.isdefault() == True
    assert cfg.option('od.stval3.st1.st2', 0).owner.isdefault() == False
    assert cfg.option('od.stval3.st1.st2', 1).owner.isdefault() == False
    assert parse_od_get(cfg.value.get()) == {'od.val1': ['val1', 'val2', 'val3'], 'od.stval1.st1.st1': [{'od.stval1.st1.st1': 'val1', 'od.stval1.st1.st2': 'val1'}, {'od.stval1.st1.st1': 'val2', 'od.stval1.st1.st2': 'val2'}], 'od.stval2.st1.st1': [{'od.stval2.st1.st1': 'val1', 'od.stval2.st1.st2': 'val1'}, {'od.stval2.st1.st1': 'val2', 'od.stval2.st1.st2': 'val2'}], 'od.stval3.st1.st1': [{'od.stval3.st1.st1': 'val1', 'od.stval3.st1.st2': 'val1'}, {'od.stval3.st1.st1': 'val2', 'od.stval3.st1.st2': 'val2'}]}
    #
    cfg.option('od.stval3.st1.st1').value.set(['val1', 'val2', 'val3'])
    assert cfg.option('od.stval3.st1.st1').owner.isdefault() == False
    assert cfg.option('od.stval3.st1.st2', 0).owner.isdefault() == False
    assert cfg.option('od.stval3.st1.st2', 1).owner.isdefault() == False
    assert cfg.option('od.stval3.st1.st2', 2).owner.isdefault() == False
    assert parse_od_get(cfg.value.get()) == {'od.val1': ['val1', 'val2', 'val3'], 'od.stval1.st1.st1': [{'od.stval1.st1.st1': 'val1', 'od.stval1.st1.st2': 'val1'}, {'od.stval1.st1.st1': 'val2', 'od.stval1.st1.st2': 'val2'}], 'od.stval2.st1.st1': [{'od.stval2.st1.st1': 'val1', 'od.stval2.st1.st2': 'val1'}, {'od.stval2.st1.st1': 'val2', 'od.stval2.st1.st2': 'val2'}], 'od.stval3.st1.st1': [{'od.stval3.st1.st1': 'val1', 'od.stval3.st1.st2': 'val1'}, {'od.stval3.st1.st1': 'val2', 'od.stval3.st1.st2': 'val2'}, {'od.stval3.st1.st1': 'val3', 'od.stval3.st1.st2': 'val3'}]}
#    assert not list_sessions()


def test_leadership_default_multi_dyndescription1():
    st1 = StrOption('st1', "", multi=True)
    st2 = StrOption('st2', "", multi=True, default_multi='no')
    stm = Leadership('st1', '', [st1, st2])
    st = DynOptionDescription('st', '', [stm], identifiers=Calculation(return_list))
    od = OptionDescription('od', '', [st])
    od1 = OptionDescription('od', '', [od])
    cfg = Config(od1)
    owner = cfg.owner.get()
    #
    assert cfg.option('od.stval1.st1.st1').value.get() == []
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.isdefault()
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
    #
    cfg.option('od.stval1.st1.st1').value.set(['yes'])
    assert cfg.option('od.stval1.st1.st1').value.get() == ['yes']
    assert cfg.option('od.stval1.st1.st2', 0).value.get() == 'no'
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.st1.st2', 0).owner.isdefault()
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
#    assert not list_sessions()


def test_leadership_dyndescription_param():
    val1 = StrOption('val1', '', ['val1', 'val2'], multi=True)
    odval = OptionDescription('odval1', '', [val1])
    st1 = StrOption('st1', "", multi=True)
    st2 = StrOption('st2', "", multi=True)
    stm = Leadership('st1', '', [st1, st2])
    st = DynOptionDescription('st', '', [stm], identifiers=Calculation(return_list, Params(ParamOption(val1))))
    od = OptionDescription('od', '', [st, odval])
    od1 = OptionDescription('od', '', [od])
    cfg = Config(od1)
    owner = cfg.owner.get()
    assert parse_od_get(cfg.value.get()) == {'od.stval1.st1.st1': [], 'od.stval2.st1.st1': [], 'od.odval1.val1': ['val1', 'val2']}
    assert cfg.option('od.stval1.st1.st1').value.get() == []
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.get() == owners.default
    assert cfg.option('od.stval2.st1.st1').owner.get() == owners.default
    #
    cfg.option('od.stval1.st1.st1').value.set(['yes'])
    assert parse_od_get(cfg.value.get()) == {'od.stval1.st1.st1': [{'od.stval1.st1.st1': 'yes', 'od.stval1.st1.st2': None}], 'od.stval2.st1.st1': [], 'od.odval1.val1': ['val1', 'val2']}
    assert cfg.option('od.stval1.st1.st1').value.get() == ['yes']
    assert cfg.option('od.stval1.st1.st2', 0).value.get() == None
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.st1.st2', 0).owner.get() == owners.default
    assert cfg.option('od.stval2.st1.st1').owner.get() == owners.default
    #
    cfg.option('od.stval1.st1.st2', 0).value.set('no')
    assert cfg.option('od.stval1.st1.st1').value.get() == ['yes']
    assert cfg.option('od.stval1.st1.st2', 0).value.get() == 'no'
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.st1.st2', 0).owner.get() == owner
    assert cfg.option('od.stval2.st1.st1').owner.get() == owners.default
    #
    cfg.option('od.stval1.st1.st1').value.pop(0)
    assert cfg.option('od.stval1.st1.st1').value.get() == []
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval2.st1.st1').owner.get() == owners.default
    #
    cfg.option('od.stval1.st1.st1').value.set(['yes'])
    cfg.option('od.stval1.st1.st2', 0).value.set('yes')
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.st1.st2', 0).owner.get() == owner
    assert cfg.option('od.stval2.st1.st1').owner.get() == owners.default
    #
    cfg.option('od.stval1.st1.st2', 0).value.reset()
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.st1.st2', 0).owner.get() == owners.default
    assert cfg.option('od.stval2.st1.st1').owner.get() == owners.default
    #
    cfg.option('od.stval1.st1.st1').value.set(['yes'])
    cfg.option('od.stval1.st1.st2', 0).value.set('yes')
    cfg.option('od.stval1.st1.st1').value.reset()
    assert cfg.option('od.stval1.st1.st1').value.get() == []
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.get() == owners.default
    assert cfg.option('od.stval2.st1.st1').owner.get() == owners.default
#    assert not list_sessions()


def test_leadership_default_multi_dyndescription2():
    st1 = StrOption('st1', "", multi=True)
    st2 = StrOption('st2', "", multi=True, default_multi='no')
    stm = Leadership('st1', '', [st1, st2])
    st = DynOptionDescription('st', '', [stm], identifiers=Calculation(return_list))
    od = OptionDescription('od', '', [st])
    od1 = OptionDescription('od', '', [od])
    cfg = Config(od1)
    owner = cfg.owner.get()
    #
    assert cfg.option('od.stval1.st1.st1').value.get() == []
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.isdefault()
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
    #
    cfg.option('od.stval1.st1.st1').value.set(['yes'])
    assert cfg.option('od.stval1.st1.st1').value.get() == ['yes']
    assert cfg.option('od.stval1.st1.st2', 0).value.get() == 'no'
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.st1.st2', 0).owner.isdefault()
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
#    assert not list_sessions()


def _test_leadership(cfg):
    owner = cfg.owner.get()
    cfg.option('od.val1.val1').value.set(['val1', 'val2'])
    cfg.option('od.val1.val2', 0).value.set('val1')
    cfg.option('od.val1.val2', 1).value.set('val2')
    assert parse_od_get(cfg.value.get()) == {'od.stval1.st1.st1': [], 'od.stval2.st1.st1': [], 'od.val1.val1': [{'od.val1.val1': 'val1', 'od.val1.val2': 'val1'}, {'od.val1.val1': 'val2', 'od.val1.val2': 'val2'}]}
    assert cfg.option('od.stval1.st1.st1').value.get() == []
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.get() == owners.default
    assert cfg.option('od.stval2.st1.st1').owner.get() == owners.default
    #
    cfg.option('od.stval1.st1.st1').value.set(['yes'])
    assert parse_od_get(cfg.value.get()) == {'od.stval1.st1.st1': [{'od.stval1.st1.st1': 'yes', 'od.stval1.st1.st2': None}], 'od.stval2.st1.st1': [], 'od.val1.val1': [{'od.val1.val1': 'val1', 'od.val1.val2': 'val1'}, {'od.val1.val1': 'val2', 'od.val1.val2': 'val2'}]}
    assert cfg.option('od.stval1.st1.st1').value.get() == ['yes']
    assert cfg.option('od.stval1.st1.st2', 0).value.get() == None
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.st1.st2', 0).owner.get() == owners.default
    assert cfg.option('od.stval2.st1.st1').owner.get() == owners.default
    #
    cfg.option('od.stval1.st1.st2', 0).value.set('no')
    assert cfg.option('od.stval1.st1.st1').value.get() == ['yes']
    assert cfg.option('od.stval1.st1.st2', 0).value.get() == 'no'
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.st1.st2', 0).owner.get() == owner
    assert cfg.option('od.stval2.st1.st1').owner.get() == owners.default
    #
    cfg.option('od.stval1.st1.st1').value.pop(0)
    assert cfg.option('od.stval1.st1.st1').value.get() == []
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval2.st1.st1').owner.get() == owners.default
    #
    cfg.option('od.stval1.st1.st1').value.set(['yes'])
    cfg.option('od.stval1.st1.st2', 0).value.set('yes')
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.st1.st2', 0).owner.get() == owner
    assert cfg.option('od.stval2.st1.st1').owner.get() == owners.default
    #
    cfg.option('od.stval1.st1.st2', 0).value.reset()
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.st1.st2', 0).owner.get() == owners.default
    assert cfg.option('od.stval2.st1.st1').owner.get() == owners.default
    #
    cfg.option('od.stval1.st1.st1').value.set(['yes'])
    cfg.option('od.stval1.st1.st2', 0).value.set('yes')
    cfg.option('od.stval1.st1.st1').value.reset()
    assert cfg.option('od.stval1.st1.st1').value.get() == []
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.get() == owners.default
    assert cfg.option('od.stval2.st1.st1').owner.get() == owners.default


def test_leadership_dyndescription_param_leader():
    val1 = StrOption('val1', "", multi=True)
    val2 = StrOption('val2', "", multi=True)
    odval = Leadership('val1', '', [val1, val2])
    st1 = StrOption('st1', "", multi=True)
    st2 = StrOption('st2', "", multi=True)
    stm = Leadership('st1', '', [st1, st2])
    st = DynOptionDescription('st', '', [stm], identifiers=Calculation(return_list, Params(ParamOption(val1))))
    od = OptionDescription('od', '', [st, odval])
    od1 = OptionDescription('od', '', [od])
    cfg = Config(od1)
    _test_leadership(cfg)
#    assert not list_sessions()


def test_leadership_default_multi_dyndescription3():
    st1 = StrOption('st1', "", multi=True)
    st2 = StrOption('st2', "", multi=True, default_multi='no')
    stm = Leadership('st1', '', [st1, st2])
    st = DynOptionDescription('st', '', [stm], identifiers=Calculation(return_list))
    od = OptionDescription('od', '', [st])
    od2 = OptionDescription('od', '', [od])
    cfg = Config(od2)
    owner = cfg.owner.get()
    #
    assert cfg.option('od.stval1.st1.st1').value.get() == []
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.isdefault()
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
    #
    cfg.option('od.stval1.st1.st1').value.set(['yes'])
    assert cfg.option('od.stval1.st1.st1').value.get() == ['yes']
    assert cfg.option('od.stval1.st1.st2', 0).value.get() == 'no'
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.st1.st2', 0).owner.isdefault()
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
#    assert not list_sessions()


def test_leadership_dyndescription_param_follower():
    val1 = StrOption('val1', "", multi=True)
    val2 = StrOption('val2', "", multi=True)
    odval = Leadership('val1', '', [val1, val2])
    st1 = StrOption('st1', "", multi=True)
    st2 = StrOption('st2', "", multi=True)
    stm = Leadership('st1', '', [st1, st2])
    st = DynOptionDescription('st', '', [stm], identifiers=Calculation(return_list, Params(ParamOption(val2))))
    od = OptionDescription('od', '', [st, odval])
    od1 = OptionDescription('od', '', [od])
    cfg = Config(od1)
    _test_leadership(cfg)
#    assert not list_sessions()


def test_leadership_default_multi_dyndescription_sub():
    st1 = StrOption('st1', "", multi=True)
    st2 = StrOption('st2', "", multi=True, default_multi='no')
    stm = Leadership('st1', '', [st1, st2])
    st = DynOptionDescription('st', '', [stm], identifiers=Calculation(return_list))
    od = OptionDescription('od', '', [st])
    od1 = OptionDescription('od', '', [od])
    cfg = Config(od1)
    owner = cfg.owner.get()
    #
    assert cfg.option('od.stval1.st1.st1').value.get() == []
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.isdefault()
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
    #
    cfg.option('od.stval1.st1.st1').value.set(['yes'])
    assert cfg.option('od.stval1.st1.st1').value.get() == ['yes']
    assert cfg.option('od.stval1.st1.st2', 0).value.get() == 'no'
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.st1.st2', 0).owner.isdefault()
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
#    assert not list_sessions()


def test_leadership_submulti_dyndescription():
    st1 = StrOption('st1', "", multi=True)
    st2 = StrOption('st2', "", multi=submulti)
    stm = Leadership('st1', '', [st1, st2])
    std = DynOptionDescription('st', '', [stm], identifiers=Calculation(return_list))
    od1 = OptionDescription('od', '', [std])
    od2 = OptionDescription('od', '', [od1])
    cfg = Config(od2)
    owner = cfg.owner.get()
    #
    assert cfg.option('od.stval1.st1.st1').value.get() == []
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.isdefault()
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
    #
    cfg.option('od.stval1.st1.st1').value.set(['yes'])
    assert cfg.option('od.stval1.st1.st1').value.get() == ['yes']
    assert cfg.option('od.stval1.st1.st2', 0).value.get() == []
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.st1.st2', 0).owner.isdefault()
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
    #
    cfg.option('od.stval1.st1.st2', 0).value.set(['no'])
    assert cfg.option('od.stval1.st1.st1').value.get() == ['yes']
    assert cfg.option('od.stval1.st1.st2', 0).value.get() == ['no']
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.st1.st2', 0).owner.get() == owner
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
#    assert not list_sessions()


def test_leadership_callback_dyndescription():
    st1 = StrOption('st1', "", multi=True)
    st2 = StrOption('st2', "", Calculation(return_dynval, Params(kwargs={'value': ParamOption(st1)})), multi=True)
    stm = Leadership('st1', '', [st1, st2])
    st1 = DynOptionDescription('st', '', [stm], identifiers=Calculation(return_list))
    od1 = OptionDescription('od', '', [st1])
    od2 = OptionDescription('od', '', [od1])
    cfg = Config(od2)
    owner = cfg.owner.get()
    assert parse_od_get(cfg.value.get()) == {'od.stval1.st1.st1': [], 'od.stval2.st1.st1': []}
    assert cfg.option('od.stval1.st1.st1').value.get() ==[]
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.isdefault()
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
    #
    cfg.option('od.stval1.st1.st1').value.set(['yes'])
    assert parse_od_get(cfg.value.get()) == {'od.stval1.st1.st1': [{'od.stval1.st1.st1': 'yes', 'od.stval1.st1.st2': 'yes'}], 'od.stval2.st1.st1': []}
    assert cfg.option('od.stval1.st1.st1').value.get() == ['yes']
    assert cfg.option('od.stval1.st1.st2', 0).value.get() == 'yes'
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.st1.st2', 0).owner.isdefault()
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
    #
    cfg.option('od.stval1.st1.st2', 0).value.set('no')
    assert cfg.option('od.stval1.st1.st1').value.get() == ['yes']
    assert cfg.option('od.stval1.st1.st2', 0).value.get() == 'no'
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.st1.st2', 0).owner.get() == owner
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
    #
    cfg.option('od.stval1.st1.st1').value.pop(0)
    assert cfg.option('od.stval1.st1.st1').value.get() == []
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
    #
    cfg.option('od.stval1.st1.st1').value.set(['yes'])
    cfg.option('od.stval1.st1.st2', 0).value.set('yes')
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.st1.st2', 0).owner.get() == owner
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
    cfg.option('od.stval1.st1.st2', 0).value.reset()
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.st1.st2', 0).owner.isdefault()
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
    #
    cfg.option('od.stval1.st1.st1').value.set(['yes'])
    cfg.option('od.stval1.st1.st2', 0).value.set('yes')
    cfg.option('od.stval1.st1.st1').value.reset()
    assert cfg.option('od.stval1.st1.st1').value.get() == []
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.isdefault()
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
    #
    cfg.option('od.stval1.st1.st1').value.set(['yes'])
    assert cfg.option('od.stval1.st1.st2', 0).value.get() == 'yes'
#    assert not list_sessions()


def test_leadership_callback_value_dyndescription():
    st1 = StrOption('st1', "", multi=True)
    st2 = StrOption('st2', "", Calculation(return_dynval, Params(kwargs={'value': ParamValue('val')})), multi=True)
    stm = Leadership('st1', '', [st1, st2])
    st = DynOptionDescription('st', '', [stm], identifiers=Calculation(return_list))
    od = OptionDescription('od', '', [st])
    od1 = OptionDescription('od', '', [od])
    cfg = Config(od1)
    assert cfg.option('od.stval1.st1.st1').value.get() == []
    cfg.option('od.stval1.st1.st1').value.set(['yes'])
    assert cfg.option('od.stval1.st1.st1').value.get() == ['yes']
    cfg.option('od.stval1.st1.st2', 0).value.set('val')
    assert cfg.option('od.stval1.st1.st2', 0).value.get() == 'val'
#    assert not list_sessions()


def test_leadership_callback_nomulti_dyndescription():
    v11 = StrOption('v1', '', "val")
    st1 = StrOption('st1', "", multi=True)
    st2 = StrOption('st2', "", Calculation(return_dynval, Params(ParamOption(v11))), multi=True)
    stm = Leadership('st1', '', [st1, st2])
    stt = DynOptionDescription('st', '', [stm], identifiers=Calculation(return_list))
    od1 = OptionDescription('od', '', [stt])
    od2 = OptionDescription('od', '', [od1, v11])
    cfg = Config(od2)
    assert cfg.option('od.stval1.st1.st1').value.get() == []
    cfg.option('od.stval1.st1.st1').value.set(['yes'])
    assert cfg.option('od.stval1.st1.st1').value.get() == ['yes']
    assert cfg.option('od.stval1.st1.st2', 0).value.get() == 'val'
#    assert not list_sessions()


def test_leadership_callback_samegroup_dyndescription():
    st1 = StrOption('st1', "", multi=True)
    st2 = StrOption('st2', "", multi=True)
    st3 = StrOption('st3', "", Calculation(return_dynval, Params(ParamOption(st2))), multi=True)
    stm = Leadership('st1', '', [st1, st2, st3])
    stt = DynOptionDescription('st', '', [stm], identifiers=Calculation(return_list))
    od1 = OptionDescription('od', '', [stt])
    od2 = OptionDescription('od', '', [od1])
    cfg = Config(od2)
    owner = cfg.owner.get()
    assert parse_od_get(cfg.value.get()) == {'od.stval1.st1.st1': [], 'od.stval2.st1.st1': []}
    assert cfg.option('od.stval1.st1.st1').value.get() == []
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.isdefault()
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
    #
    cfg.option('od.stval1.st1.st1').value.set(['yes'])
    assert parse_od_get(cfg.value.get()) == {'od.stval1.st1.st1': [{'od.stval1.st1.st1': 'yes', 'od.stval1.st1.st2': None, 'od.stval1.st1.st3': None}], 'od.stval2.st1.st1': []}
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.st1.st2', 0).owner.isdefault()
    assert cfg.option('od.stval1.st1.st3', 0).owner.isdefault()
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
    #
    cfg.option('od.stval1.st1.st2', 0).value.set('yes')
    assert parse_od_get(cfg.value.get()) == {'od.stval1.st1.st1': [{'od.stval1.st1.st1': 'yes', 'od.stval1.st1.st2': 'yes', 'od.stval1.st1.st3': 'yes'}], 'od.stval2.st1.st1': []}
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.st1.st2', 0).owner.get() == owner
    assert cfg.option('od.stval1.st1.st3', 0).owner.isdefault()
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
#    assert not list_sessions()


def test_invalid_conflict_dyndescription():
    st = StrOption('st', '')
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list))
    dodinvalid = StrOption('dodinvalid', '')
    dod, dodinvalid
    with pytest.raises(ConflictError):
        OptionDescription('od', '', [dod, dodinvalid])
#    assert not list_sessions()


def test_leadership_default_multi_dyndescription4():
    st1 = StrOption('st1', "", multi=True)
    st2 = StrOption('st2', "", multi=True, default_multi='no')
    stm = Leadership('st1', '', [st1, st2])
    od1 = OptionDescription('od1', '', [stm])
    st = DynOptionDescription('st', '', [od1], identifiers=Calculation(return_list))
    od = OptionDescription('od', '', [st])
    od1 = OptionDescription('od', '', [od])
    cfg = Config(od1)
    owner = cfg.owner.get()
    #
    assert parse_od_get(cfg.value.get()) == {'od.stval1.od1.st1.st1': [],
                                             'od.stval2.od1.st1.st1': [],
                                             }
    assert cfg.option('od.stval1.od1.st1.st1').value.get() == []
    assert cfg.option('od.stval2.od1.st1.st1').value.get() == []
    assert cfg.option('od.stval1.od1.st1.st1').owner.isdefault()
    assert cfg.option('od.stval2.od1.st1.st1').owner.isdefault()
    #
    cfg.option('od.stval1.od1.st1.st1').value.set(['yes'])
    assert cfg.option('od.stval1.od1.st1.st1').value.get() == ['yes']
    assert cfg.option('od.stval1.od1.st1.st2', 0).value.get() == 'no'
    assert cfg.option('od.stval2.od1.st1.st1').value.get() == []
    assert cfg.option('od.stval1.od1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.od1.st1.st2', 0).owner.isdefault()
    assert cfg.option('od.stval2.od1.st1.st1').owner.isdefault()
    assert parse_od_get(cfg.value.get()) == {'od.stval1.od1.st1.st1': [{'od.stval1.od1.st1.st1': 'yes',
                                                                        'od.stval1.od1.st1.st2': 'no'}],
                                             'od.stval2.od1.st1.st1': [],
                               }
#    assert not list_sessions()


def test_subdynod_dyndescription_root():
    st2 = StrOption('st2', '')
    dod1 = DynOptionDescription('dod1', '', [st2], identifiers=Calculation(return_list, Params(ParamValue(['a', 'b']))))
    dod = DynOptionDescription('dod', '', [dod1], identifiers=Calculation(return_list))
    st3 = StrOption('st3', '', Calculation(return_dynval, Params(ParamDynOption(st2, ['val1', 'a']))))
    # FIXME st4 = StrOption('st4', '', Calculation(return_dynval, Params(ParamOption(st2))), multi=True)
    od1 = OptionDescription('od', '', [dod, st3])  #, st4])
    cfg = Config(od1)
    assert parse_od_get(cfg.value.get()) == {'dodval1.dod1a.st2': None,
                                             'dodval1.dod1b.st2': None,
                                             'dodval2.dod1a.st2': None,
                                             'dodval2.dod1b.st2': None,
                                             'st3': None,
                                             }
    assert cfg.option('dodval1.dod1a.st2').owner.isdefault()
    assert cfg.option('dodval1.dod1a.st2').value.get() is None
    assert cfg.option('dodval1.dod1b.st2').value.get() is None
    assert cfg.option('dodval2.dod1a.st2').value.get() is None
    assert cfg.option('dodval2.dod1b.st2').value.get() is None
    assert cfg.option('dodval2.dod1b.st2').value.get() is None
    assert cfg.option('st3').value.get() is None
    #
    cfg.option('dodval1.dod1a.st2').value.set('val')
    assert parse_od_get(cfg.value.get()) == {'dodval1.dod1a.st2': 'val',
                                             'dodval1.dod1b.st2': None,
                                             'dodval2.dod1a.st2': None,
                                             'dodval2.dod1b.st2': None,
                                             'st3': 'val',
                                             }
    assert not cfg.option('dodval1.dod1a.st2').owner.isdefault()
    assert cfg.option('dodval1.dod1a.st2').value.get() == 'val'
    assert cfg.option('dodval1.dod1b.st2').value.get() is None
    assert cfg.option('dodval2.dod1a.st2').value.get() is None
    assert cfg.option('dodval2.dod1b.st2').value.get() is None
    assert cfg.option('st3').value.get() == 'val'
    #
    cfg.option('dodval2.dod1a.st2').value.reset()
    assert parse_od_get(cfg.value.get()) == {'dodval1.dod1a.st2': 'val',
                                             'dodval1.dod1b.st2': None,
                                             'dodval2.dod1a.st2': None,
                                             'dodval2.dod1b.st2': None,
                                             'st3': 'val',
                                             }
    assert not cfg.option('dodval1.dod1a.st2').owner.isdefault()
    assert cfg.option('dodval1.dod1a.st2').value.get() == 'val'
    assert cfg.option('dodval1.dod1b.st2').value.get() is None
    assert cfg.option('dodval2.dod1a.st2').value.get() is None
    assert cfg.option('dodval2.dod1b.st2').value.get() is None
    assert cfg.option('st3').value.get() == 'val'
    #
    cfg.option('dodval1.dod1a.st2').value.reset()
    assert parse_od_get(cfg.value.get()) == {'dodval1.dod1a.st2': None,
                                             'dodval1.dod1b.st2': None,
                                             'dodval2.dod1a.st2': None,
                                             'dodval2.dod1b.st2': None,
                                             'st3': None,
                                             }
    assert cfg.option('dodval1.dod1a.st2').owner.isdefault()
    assert cfg.option('dodval1.dod1a.st2').value.get() is None
    assert cfg.option('dodval1.dod1b.st2').value.get() is None
    assert cfg.option('dodval2.dod1a.st2').value.get() is None
    assert cfg.option('dodval2.dod1b.st2').value.get() is None
    assert cfg.option('st3').value.get() is None
#    assert not list_sessions()


def test_subdynod_dyndescription():
    st2 = StrOption('st2', '')
    dod1 = DynOptionDescription('dod1', '', [st2], identifiers=Calculation(return_list, Params(ParamValue(['a', 'b']))))
    dod = DynOptionDescription('dod', '', [dod1], identifiers=Calculation(return_list))
    od1 = OptionDescription('od', '', [dod])
    st3 = StrOption('st3', '', Calculation(return_dynval, Params(ParamDynOption(st2, ['val1', 'a']))))
    od = OptionDescription('od', '', [od1, st3])  #, st4])
    cfg = Config(od)
    assert parse_od_get(cfg.value.get()) == {'od.dodval1.dod1a.st2': None,
                                             'od.dodval1.dod1b.st2': None,
                                             'od.dodval2.dod1a.st2': None,
                                             'od.dodval2.dod1b.st2': None,
                                             'st3': None,
                                             }
    assert cfg.option('od.dodval1.dod1a.st2').owner.isdefault()
    assert cfg.option('od.dodval1.dod1a.st2').value.get() is None
    assert cfg.option('od.dodval1.dod1b.st2').value.get() is None
    assert cfg.option('od.dodval2.dod1a.st2').value.get() is None
    assert cfg.option('od.dodval2.dod1b.st2').value.get() is None
    assert cfg.option('od.dodval2.dod1b.st2').value.get() is None
    assert cfg.option('st3').value.get() is None
    #
    cfg.option('od.dodval1.dod1a.st2').value.set('val')
    assert parse_od_get(cfg.value.get()) == {'od.dodval1.dod1a.st2': 'val',
                                             'od.dodval1.dod1b.st2': None,
                                             'od.dodval2.dod1a.st2': None,
                                             'od.dodval2.dod1b.st2': None,
                                             'st3': 'val',
                                             }
    assert not cfg.option('od.dodval1.dod1a.st2').owner.isdefault()
    assert cfg.option('od.dodval1.dod1a.st2').value.get() == 'val'
    assert cfg.option('od.dodval1.dod1b.st2').value.get() is None
    assert cfg.option('od.dodval2.dod1a.st2').value.get() is None
    assert cfg.option('od.dodval2.dod1b.st2').value.get() is None
    assert cfg.option('st3').value.get() == 'val'
    #
    cfg.option('od.dodval2.dod1a.st2').value.reset()
    assert parse_od_get(cfg.value.get()) == {'od.dodval1.dod1a.st2': 'val',
                                             'od.dodval1.dod1b.st2': None,
                                             'od.dodval2.dod1a.st2': None,
                                             'od.dodval2.dod1b.st2': None,
                                             'st3': 'val',
                                             }
    assert not cfg.option('od.dodval1.dod1a.st2').owner.isdefault()
    assert cfg.option('od.dodval1.dod1a.st2').value.get() == 'val'
    assert cfg.option('od.dodval1.dod1b.st2').value.get() is None
    assert cfg.option('od.dodval2.dod1a.st2').value.get() is None
    assert cfg.option('od.dodval2.dod1b.st2').value.get() is None
    assert cfg.option('st3').value.get() == 'val'
    #
    cfg.option('od.dodval1.dod1a.st2').value.reset()
    assert parse_od_get(cfg.value.get()) == {'od.dodval1.dod1a.st2': None,
                                             'od.dodval1.dod1b.st2': None,
                                             'od.dodval2.dod1a.st2': None,
                                             'od.dodval2.dod1b.st2': None,
                                             'st3': None,
                                             }
    assert cfg.option('od.dodval1.dod1a.st2').owner.isdefault()
    assert cfg.option('od.dodval1.dod1a.st2').value.get() is None
    assert cfg.option('od.dodval1.dod1b.st2').value.get() is None
    assert cfg.option('od.dodval2.dod1a.st2').value.get() is None
    assert cfg.option('od.dodval2.dod1b.st2').value.get() is None
    assert cfg.option('st3').value.get() is None
#    assert not list_sessions()

def test_subdynod_dyndescription_2():
    st2 = StrOption('st2', '')
    st1 = StrOption('st1', '', default=['a', 'b'], multi=True)
    dod1 = DynOptionDescription('dod1', '', [st2], identifiers=Calculation(return_list, Params(ParamOption(st1))))
    dod = DynOptionDescription('dod', '', [dod1, st1], identifiers=Calculation(return_list))
    od1 = OptionDescription('od', '', [dod])
    st3 = StrOption('st3', '', Calculation(return_dynval, Params(ParamDynOption(st2, ['val1', 'a']))))
    od = OptionDescription('od', '', [od1, st3])  #, st4])
    cfg = Config(od)
    assert parse_od_get(cfg.value.get()) == {'od.dodval1.dod1a.st2': None,
                               'od.dodval1.dod1b.st2': None,
                               'od.dodval1.st1': ['a', 'b'],
                               'od.dodval2.dod1a.st2': None,
                               'od.dodval2.dod1b.st2': None,
                               'od.dodval2.st1': ['a', 'b'],
                               'st3': None,
                               }
    cfg.cache.reset()
    assert cfg.option('od.dodval1.dod1a.st2').value.get() is None
    assert cfg.option('od.dodval1.dod1b.st2').value.get() is None
    assert cfg.option('od.dodval1.st1').value.get() == ['a', 'b']
    assert cfg.option('od.dodval2.dod1a.st2').value.get() is None
    assert cfg.option('od.dodval2.dod1b.st2').value.get() is None
    assert cfg.option('od.dodval2.st1').value.get() == ['a', 'b']
    assert cfg.option('st3').value.get() is None
    #
    cfg.option('od.dodval1.st1').value.set(['a'])
    cfg.option('od.dodval2.st1').value.set(['b', 'c'])
    assert parse_od_get(cfg.value.get()) == {'od.dodval1.st1': ['a'],
                               'od.dodval1.dod1a.st2': None,
                               'od.dodval2.st1': ['b', 'c'],
                               'od.dodval2.dod1b.st2': None,
                               'od.dodval2.dod1c.st2': None,
                               'st3': None,
                               }


def test_subdynod_dyndescription_leadership():
    st1 = StrOption('st1', '', multi=True)
    st2 = StrOption('st2', '', multi=True)
    stm = Leadership('stm', '', [st1, st2])
    dod1 = DynOptionDescription('dod1', '', [stm], identifiers=Calculation(return_list, Params(ParamValue(['a', 'b']))))
    dod = DynOptionDescription('dod', '', [dod1], identifiers=Calculation(return_list))
    od1 = OptionDescription('od', '', [dod])
    st3 = StrOption('st3', '', Calculation(return_dynval, Params(ParamDynOption(st1, ['val1', 'a']))), multi=True)
    # FIXME st4 = StrOption('st4', '', Calculation(return_dynval, Params(ParamOption(st2))), multi=True)
    st5 = StrOption('st5', '', Calculation(return_dynval, Params(ParamDynOption(st2, ['val1', 'a']))), multi=True)
    #cfg = Config(od1)
    #FIXME
    od = OptionDescription('od', '', [od1, st3 , st5])  #, st4])
    cfg = Config(od)
    assert parse_od_get(cfg.value.get()) == {'od.dodval1.dod1a.stm.st1': [],
                               'od.dodval1.dod1b.stm.st1': [],
                               'od.dodval2.dod1a.stm.st1': [],
                               'od.dodval2.dod1b.stm.st1': [],
                               'st3': [],
                               'st5': [],
                               }
    assert cfg.option('od.dodval1.dod1a.stm.st1').owner.isdefault()
    assert cfg.option('od.dodval1.dod1a.stm.st1').value.get() == []
    assert cfg.option('od.dodval1.dod1b.stm.st1').value.get() == []
    assert cfg.option('od.dodval2.dod1a.stm.st1').value.get() == []
    assert cfg.option('od.dodval2.dod1b.stm.st1').value.get() == []
    assert cfg.option('od.dodval2.dod1b.stm.st1').value.get() == []
    assert cfg.option('st3').value.get() == []
    assert cfg.option('st5').value.get() == []
    #
    cfg.option('od.dodval1.dod1a.stm.st1').value.set(['val'])
    assert cfg.option('st3').value.get() == ['val']
    assert parse_od_get(cfg.value.get()) == {'od.dodval1.dod1a.stm.st1': [{'od.dodval1.dod1a.stm.st1': 'val',
                                                             'od.dodval1.dod1a.stm.st2': None}],
                               'od.dodval1.dod1b.stm.st1': [],
                               'od.dodval2.dod1a.stm.st1': [],
                               'od.dodval2.dod1b.stm.st1': [],
                               'st3': ['val'],
                               'st5': [],
                               }
    assert not cfg.option('od.dodval1.dod1a.stm.st1').owner.isdefault()
    assert cfg.option('od.dodval1.dod1a.stm.st1').value.get() == ['val']
    assert cfg.option('od.dodval1.dod1b.stm.st1').value.get() == []
    assert cfg.option('od.dodval2.dod1a.stm.st1').value.get() == []
    assert cfg.option('od.dodval2.dod1b.stm.st1').value.get() == []
    #


def test_dyndescription_symlink():
    st = StrOption('st', '')
    st2 = SymLinkOption('st2', st)
#    with pytest.raises(ConfigError):
    dod = DynOptionDescription('dod', '', [st, st2], identifiers=Calculation(return_list))
    od = OptionDescription('od', '', [dod])
    cfg = Config(od)
    assert parse_od_get(cfg.value.get()) == {'dodval1.st': None, 'dodval1.st2': None, 'dodval2.st': None, 'dodval2.st2': None}
    cfg.option('dodval1.st').value.set('j')
    assert parse_od_get(cfg.value.get()) == {'dodval1.st': 'j', 'dodval1.st2': 'j', 'dodval2.st': None, 'dodval2.st2': None}
#    assert not list_sessions()


def test_dyndescription_symlink_not_same():
    st = StrOption('st', '')
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list))
    st2 = SymLinkOption('st2', st)
#    with pytest.raises(ConfigError):
    dod2 = DynOptionDescription('sdod', '', [st2], identifiers=Calculation(return_list))
    od = OptionDescription('od', '', [dod, dod2])
    cfg = Config(od)
    assert parse_od_get(cfg.value.get()) == {'dodval1.st': None, 'dodval2.st': None, 'sdodval1.st2': [None, None], 'sdodval2.st2': [None, None]}
    cfg.option('dodval1.st').value.set('j')
    assert parse_od_get(cfg.value.get()) == {'dodval1.st': 'j', 'dodval2.st': None, 'sdodval1.st2': ['j', None], 'sdodval2.st2': ['j', None]}
#    assert not list_sessions()


def test_dyndescription_symlink_outside():
    st = StrOption('st', '')
#    with pytest.raises(ConfigError):
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list))
    st2 = SymLinkOption('st2', st)
    od = OptionDescription('od', '', [dod, st2])
    cfg = Config(od)
    assert parse_od_get(cfg.value.get()) == {'dodval1.st': None, 'dodval2.st': None, 'st2': [None, None]}
    cfg.option('dodval1.st').value.set('j')
    assert parse_od_get(cfg.value.get()) == {'dodval1.st': 'j', 'dodval2.st': None, 'st2': ['j', None]}
#    assert not list_sessions()


def test_dyndescription_symlink_inside():
    st = StrOption('st', '')
    st2 = SymLinkOption('st2', st)
#    with pytest.raises(ConfigError):
    dod = DynOptionDescription('dod', '', [st2], identifiers=Calculation(return_list))
    od = OptionDescription('od', '', [dod, st])
    cfg = Config(od)
    assert parse_od_get(cfg.value.get()) == {'dodval1.st2': None, 'dodval2.st2': None, 'st': None}
    cfg.option('st').value.set('j')
    assert parse_od_get(cfg.value.get()) == {'dodval1.st2': 'j', 'dodval2.st2': 'j', 'st': 'j'}
#    assert not list_sessions()


def test_nocallback_dyndescription():
    st = StrOption('st', '')
    st2 = StrOption('st2', '')
    with pytest.raises(TypeError):
        DynOptionDescription('dod', '', [st, st2])
#    assert not list_sessions()


def test_invalid_samevalue_dyndescription():
    st1 = StrOption('st', '')
    dod = DynOptionDescription('dod', '', [st1], identifiers=Calculation(return_same_list))
    od1 = OptionDescription('od', '', [dod])
    cfg = Config(od1)
    with pytest.raises(ValueError):
        cfg.value.get()
#    assert not list_sessions()


def test_invalid_name_dyndescription():
    st1 = StrOption('st', '')
    dod = DynOptionDescription('dod', '', [st1], identifiers=Calculation(return_wrong_list))
    od1 = OptionDescription('od', '', [dod])
    cfg = Config(od1)
    with pytest.raises(ValueError):
        cfg.value.get()
#    assert not list_sessions()


def test_leadership_dyndescription_convert():
    st1 = StrOption('st1', "", multi=True)
    st2 = StrOption('st2', "", multi=True)
    stm = Leadership('st1', '', [st1, st2])
    st = ConvertDynOptionDescription('st', '', [stm], identifiers=Calculation(return_list_dot))
    od = OptionDescription('od', '', [st])
    od1 = OptionDescription('od', '', [od])
    cfg = Config(od1)
    owner = cfg.owner.get()
    #
    assert parse_od_get(cfg.value.get()) == {'od.stval1.st1.st1': [], 'od.stval2.st1.st1': []}
    assert cfg.option('od.stval1.st1.st1').value.get() == []
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.isdefault()
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
    #
    cfg.option('od.stval1.st1.st1').value.set(['yes'])
    assert parse_od_get(cfg.value.get()) == {'od.stval1.st1.st1': [{'od.stval1.st1.st1': 'yes', 'od.stval1.st1.st2': None}], 'od.stval2.st1.st1': []}
    assert cfg.option('od.stval1.st1.st1').value.get() == ['yes']
    assert cfg.option('od.stval1.st1.st2', 0).value.get() == None
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.st1.st2', 0).owner.isdefault()
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
    #
    cfg.option('od.stval1.st1.st2', 0).value.set('no')
    assert cfg.option('od.stval1.st1.st1').value.get() == ['yes']
    assert cfg.option('od.stval1.st1.st2', 0).value.get() == 'no'
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.st1.st2', 0).owner.get() == owner
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
    #
    cfg.option('od.stval1.st1.st1').value.pop(0)
    assert cfg.option('od.stval1.st1.st1').value.get() == []
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
    #
    cfg.option('od.stval1.st1.st1').value.set(['yes'])
    cfg.option('od.stval1.st1.st2', 0).value.set('yes')
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.st1.st2', 0).owner.get() == owner
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    cfg.option('od.stval1.st1.st2', 0).value.reset()
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.st1.st2', 0).owner.isdefault()
    #
    cfg.option('od.stval1.st1.st1').value.set(['yes'])
    cfg.option('od.stval1.st1.st2', 0).value.set('yes')
    cfg.option('od.stval1.st1.st1').value.reset()
    assert cfg.option('od.stval1.st1.st1').value.get() == []
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.isdefault()
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
#    assert not list_sessions()


def test_leadership_callback_samegroup_dyndescription_convert():
    st1 = StrOption('st1', "", multi=True)
    st2 = StrOption('st2', "", multi=True)
    st3 = StrOption('st3', "", Calculation(return_dynval, Params(ParamOption(st2))), multi=True)
    stm = Leadership('st1', '', [st1, st2, st3])
    stt = ConvertDynOptionDescription('st', '', [stm], identifiers=Calculation(return_list_dot))
    od1 = OptionDescription('od', '', [stt])
    od2 = OptionDescription('od', '', [od1])
    cfg = Config(od2)
    owner = cfg.owner.get()
    assert parse_od_get(cfg.value.get()) == {'od.stval1.st1.st1': [], 'od.stval2.st1.st1': []}
    assert cfg.option('od.stval1.st1.st1').value.get() == []
    assert cfg.option('od.stval2.st1.st1').value.get() == []
    assert cfg.option('od.stval1.st1.st1').owner.isdefault()
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
    #
    cfg.option('od.stval1.st1.st1').value.set(['yes'])
    assert parse_od_get(cfg.value.get()) == {'od.stval1.st1.st1': [{'od.stval1.st1.st1': 'yes', 'od.stval1.st1.st2': None, 'od.stval1.st1.st3': None}], 'od.stval2.st1.st1': []}
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.st1.st2', 0).owner.isdefault()
    assert cfg.option('od.stval1.st1.st3', 0).owner.isdefault()
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
    #
    cfg.option('od.stval1.st1.st2', 0).value.set('yes')
    assert parse_od_get(cfg.value.get()) == {'od.stval1.st1.st1': [{'od.stval1.st1.st1': 'yes', 'od.stval1.st1.st2': 'yes', 'od.stval1.st1.st3': 'yes'}], 'od.stval2.st1.st1': []}
    assert cfg.option('od.stval1.st1.st1').owner.get() == owner
    assert cfg.option('od.stval1.st1.st2', 0).owner.get() == owner
    assert cfg.option('od.stval1.st1.st3', 0).owner.isdefault()
    assert cfg.option('od.stval2.st1.st1').owner.isdefault()
#    assert not list_sessions()


def test_dyn_with_leader_hidden_in_config():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True, properties=('hidden',))
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0], properties=('hidden',))
    dyn = DynOptionDescription('leader', '', [interface1], identifiers=Calculation(return_list))
    od1 = OptionDescription('root', '', [dyn])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.permissive.add('hidden')
    assert cfg.forcepermissive.option('leaderval1.ip_admin_eth0.ip_admin_eth0').value.get() == []
    cfg.forcepermissive.option('leaderval1.ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.1'])
    assert cfg.forcepermissive.option('leaderval1.ip_admin_eth0.netmask_admin_eth0', 0).value.get() is None
    with pytest.raises(PropertiesOptionError):
        cfg.option('leaderval1.ip_admin_eth0.ip_admin_eth0').value.get()
    with pytest.raises(PropertiesOptionError):
        cfg.option('leaderval1.ip_admin_eth0.netmask_admin_eth0', 0).value.get()
    assert parse_od_get(cfg.value.get()) == {}
    assert parse_od_get(cfg.forcepermissive.value.get()) == {'leaderval1.ip_admin_eth0.ip_admin_eth0': [{'leaderval1.ip_admin_eth0.ip_admin_eth0': '192.168.1.1', 'leaderval1.ip_admin_eth0.netmask_admin_eth0': None}],
                                                             'leaderval2.ip_admin_eth0.ip_admin_eth0': []}
#    assert not list_sessions()


def test_dyn_with_leader_hidden_in_config2():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True)
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True, properties=('hidden',))
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    dyn = DynOptionDescription('leader', '', [interface1], identifiers=Calculation(return_list))
    od1 = OptionDescription('root', '', [dyn])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg.permissive.add('hidden')
    assert cfg.forcepermissive.option('leaderval1.ip_admin_eth0.ip_admin_eth0').value.get() == []
    cfg.forcepermissive.option('leaderval1.ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.1'])
    assert cfg.forcepermissive.option('leaderval1.ip_admin_eth0.netmask_admin_eth0', 0).value.get() is None
    with pytest.raises(PropertiesOptionError):
        cfg.option('leaderval1.ip_admin_eth0.netmask_admin_eth0', 0).value.get()
    assert parse_od_get(cfg.value.get()) == {'leaderval1.ip_admin_eth0.ip_admin_eth0': [{'leaderval1.ip_admin_eth0.ip_admin_eth0': '192.168.1.1'}],
                                             'leaderval2.ip_admin_eth0.ip_admin_eth0': []}
#    assert not list_sessions()


def test_dyn_leadership_requires():
    ip_admin_eth0 = StrOption('ip_admin_eth0', "ip réseau autorisé", multi=True, properties=('notunique',))
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(ip_admin_eth0, notraisepropertyerror=True),
                                                   'expected': ParamValue('192.168.1.1'),
                                                   'no_condition_is_invalid': ParamValue(True),
                                                   'index': ParamIndex()}))
    netmask_admin_eth0 = StrOption('netmask_admin_eth0', "masque du sous-réseau", multi=True, properties=(disabled_property,))
    interface1 = Leadership('ip_admin_eth0', '', [ip_admin_eth0, netmask_admin_eth0])
    dyn = DynOptionDescription('leader', '', [interface1], identifiers=Calculation(return_list))
    od1 = OptionDescription('toto', '', [dyn])
    cfg = Config(od1)
    cfg.property.read_write()
    assert cfg.option('leaderval1.ip_admin_eth0.ip_admin_eth0').value.get() == []
    cfg.option('leaderval1.ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.2'])
    assert cfg.option('leaderval1.ip_admin_eth0.netmask_admin_eth0', 0).value.get() is None
    assert cfg.option('leaderval1.ip_admin_eth0.ip_admin_eth0').value.get() == ['192.168.1.2']
    #
    cfg.option('leaderval1.ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.2', '192.168.1.1'])
    assert cfg.option('leaderval1.ip_admin_eth0.netmask_admin_eth0', 0).value.get() is None
    with pytest.raises(PropertiesOptionError):
        cfg.option('leaderval1.ip_admin_eth0.netmask_admin_eth0', 1).value.get()
    #
    cfg.option('leaderval1.ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.2', '192.168.1.2'])
    assert cfg.option('leaderval1.ip_admin_eth0.netmask_admin_eth0', 0).value.get() is None
    assert cfg.option('leaderval1.ip_admin_eth0.netmask_admin_eth0', 1).value.get() is None
    cfg.option('leaderval1.ip_admin_eth0.netmask_admin_eth0', 1).value.set('255.255.255.255')
    assert cfg.option('leaderval1.ip_admin_eth0.netmask_admin_eth0', 1).value.get() == '255.255.255.255'
    ret = parse_od_get(cfg.value.get())
    assert ret == {'leaderval1.ip_admin_eth0.ip_admin_eth0': [{'leaderval1.ip_admin_eth0.ip_admin_eth0': '192.168.1.2', 'leaderval1.ip_admin_eth0.netmask_admin_eth0': None},
                                                              {'leaderval1.ip_admin_eth0.ip_admin_eth0': '192.168.1.2', 'leaderval1.ip_admin_eth0.netmask_admin_eth0': '255.255.255.255'}],
                   'leaderval2.ip_admin_eth0.ip_admin_eth0': []}

    #
    cfg.option('leaderval1.ip_admin_eth0.ip_admin_eth0').value.set(['192.168.1.2', '192.168.1.1'])
    assert cfg.option('leaderval1.ip_admin_eth0.netmask_admin_eth0', 0).value.get() is None
    with pytest.raises(PropertiesOptionError):
        cfg.option('leaderval1.ip_admin_eth0.netmask_admin_eth0', 1).value.get()
    assert parse_od_get(cfg.value.get()) == {'leaderval1.ip_admin_eth0.ip_admin_eth0': [{'leaderval1.ip_admin_eth0.ip_admin_eth0': '192.168.1.2', 'leaderval1.ip_admin_eth0.netmask_admin_eth0': None}, {'leaderval1.ip_admin_eth0.ip_admin_eth0': '192.168.1.1'}], 'leaderval2.ip_admin_eth0.ip_admin_eth0': []}
    #
#    assert not list_sessions()


def test_dyn_leadership_mandatory():
    nsd_zones_all = StrOption(name="nsd_zones_all", doc="nsd_zones_all", multi=True, default=['val1', 'val2'])
    is_auto = BoolOption(name="is_auto_", doc="is auto")
    hostname = DomainnameOption(name="hostname_", doc="hostname_", multi=True, type='hostname')
    choice = ChoiceOption(name="type_", doc="type_", values=('A', 'CNAME'), multi=True, default_multi="A")
    leadership = Leadership(name="hostname_", doc="hostname_", children=[hostname, choice], properties=frozenset({Calculation(calc_value, Params(ParamValue('hidden'), kwargs={'condition': ParamOption(is_auto, notraisepropertyerror=True), 'expected': ParamValue(True)}))}))
    dyn = DynOptionDescription(name="nsd_zone_", doc="Zone ", identifiers=Calculation(calc_value, Params((ParamOption(nsd_zones_all, notraisepropertyerror=True)))), children=[is_auto, leadership], properties=frozenset({"normal"}))
    od1 = OptionDescription(name="nsd", doc="nsd", children=[nsd_zones_all, dyn])
    cfg = Config(od1)
    assert cfg.value.mandatory() == []
#    assert not list_sessions()


def test_dyn_symlink():
    remotes = StrOption("remotes", "Remotes", ['a', 'b', 'c'], multi=True)
    remote_ip = StrOption("remote_ip_", "Remote IP", Calculation(calc_value, Params(ParamIdentifier())))
    dyn_remote = DynOptionDescription("remote_", "Account for ", identifiers=Calculation(calc_value, Params((ParamOption(remotes)))), children=[remote_ip])
    name = SymLinkOption("name", opt=remote_ip)
    od1 = OptionDescription(name="accounts", doc="accounts.remote_.remote_ip_", children=[remotes, dyn_remote, name])
    cfg = Config(od1)
    assert cfg.option('name').value.get() == ['a', 'b', 'c']
    assert cfg.option('name').ismulti() == True
    assert cfg.option('name').issubmulti() == False
    assert parse_od_get(cfg.value.get()) == {'remotes': ['a', 'b', 'c'], 'remote_a.remote_ip_': 'a', 'remote_b.remote_ip_': 'b', 'remote_c.remote_ip_': 'c', 'name': ['a', 'b', 'c']}
#    assert not list_sessions()


def test_dyn_callback_with_not_dyn():
    remotes = StrOption("remotes", "Remotes", ['a', 'b', 'c'], multi=True)
    remote_ip = StrOption("remote_ip_", "Remote IP", Calculation(calc_value, Params(ParamIdentifier())))
    dyn_remote = DynOptionDescription("remote_", "Account for ", identifiers=Calculation(calc_value, Params((ParamOption(remotes)))), children=[remote_ip])
    names = StrOption('names', '', Calculation(calc_value, Params(ParamOption(remote_ip))), multi=True)
    od1 = OptionDescription(name="accounts", doc="accounts.remote_.remote_ip_", children=[remotes, dyn_remote, names])
    cfg = Config(od1)
    assert cfg.option('names').value.get() == ['a', 'b', 'c']
    assert cfg.option('names').ismulti() == True
    assert cfg.option('names').issubmulti() == False
    assert parse_od_get(cfg.value.get()) == {'remotes': ['a', 'b', 'c'], 'remote_a.remote_ip_': 'a', 'remote_b.remote_ip_': 'b', 'remote_c.remote_ip_': 'c', 'names': ['a', 'b', 'c']}
#    assert not list_sessions()


def test_dyn_link_subdyn():
    database_names = StrOption(name="database_names", doc="database_names", multi=True, default=["srep", "snom", "srem"])
    password = StrOption(name="password", doc="password", properties=('mandatory',))
    name = StrOption(name="name", doc="name", properties=('mandatory',))
    password2 = StrOption(name="password", doc="password", default=Calculation(calc_value, Params((ParamOption(password)))), properties=('mandatory',))
    user = OptionDescription(name="user", doc="user", children=[name, password2])
    sub = OptionDescription(name="sub", doc="sub", children=[user])
    user_database = DynOptionDescription(name="user_database_", doc="user database", identifiers=Calculation(calc_value, Params((ParamOption(database_names, notraisepropertyerror=True)))), children=[password, sub])
    socle = OptionDescription(name="socle", doc="socle", children=[user_database, database_names])
    root = OptionDescription(name="baseoption", doc="baseoption", children=[socle])
    cfg = Config(root)
    assert cfg.option('socle.database_names').value.get() == ["srep", "snom", "srem"]
    assert cfg.option('socle.user_database_srep.password').value.get() is None
    assert cfg.option('socle.user_database_srep.sub.user.name').value.get() is None
    assert cfg.option('socle.user_database_srep.sub.user.password').value.get() is None
    assert [opt.path() for opt in cfg.value.mandatory()] == ['socle.user_database_srep.password',
                                                             'socle.user_database_srep.sub.user.name',
                                                             'socle.user_database_srep.sub.user.password',
                                                             'socle.user_database_snom.password',
                                                             'socle.user_database_snom.sub.user.name',
                                                             'socle.user_database_snom.sub.user.password',
                                                             'socle.user_database_srem.password',
                                                             'socle.user_database_srem.sub.user.name',
                                                             'socle.user_database_srem.sub.user.password',
                                                             ]
    #
    cfg.option('socle.user_database_srep.password').value.set('pass')
    cfg.option('socle.user_database_snom.sub.user.password').value.set('pass')
    assert cfg.option('socle.user_database_srep.password').value.get() is 'pass'
    assert cfg.option('socle.user_database_srep.sub.user.name').value.get() is None
    assert cfg.option('socle.user_database_srep.sub.user.password').value.get() is 'pass'
    assert [opt.path() for opt in cfg.value.mandatory()] == ['socle.user_database_srep.sub.user.name',
                                                             'socle.user_database_snom.password',
                                                             'socle.user_database_snom.sub.user.name',
                                                             'socle.user_database_srem.password',
                                                             'socle.user_database_srem.sub.user.name',
                                                             'socle.user_database_srem.sub.user.password',
                                                             ]
    #
    cfg.option('socle.user_database_snom.password').value.set('pass2')
    cfg.option('socle.user_database_srem.password').value.set('pass3')
    cfg.option('socle.user_database_srep.sub.user.name').value.set('name1')
    cfg.option('socle.user_database_snom.sub.user.name').value.set('name2')
    cfg.option('socle.user_database_srem.sub.user.name').value.set('name3')
    assert [opt.path() for opt in cfg.value.mandatory()] == []
    assert parse_od_get(cfg.value.get()) == {'socle.database_names': ['srep',
                                                        'snom',
                                                        'srem'],
                               'socle.user_database_snom.password': 'pass2',
                               'socle.user_database_snom.sub.user.name': 'name2',
                               'socle.user_database_snom.sub.user.password': 'pass',
                               'socle.user_database_srem.password': 'pass3',
                               'socle.user_database_srem.sub.user.name': 'name3',
                               'socle.user_database_srem.sub.user.password': 'pass3',
                               'socle.user_database_srep.password': 'pass',
                               'socle.user_database_srep.sub.user.name': 'name1',
                               'socle.user_database_srep.sub.user.password': 'pass',
                               }
    #
    assert [opt.path() for opt in cfg.value.mandatory()] == []


def test_dyn_link_subdyn_2():
    database_names = StrOption(name="database_names", doc="database_names", multi=True, default=["srep", "snom", "srem"])
    password2 = StrOption(name="password", doc="password", properties=('mandatory',))
    password = StrOption(name="password", doc="password", default=Calculation(calc_value, Params((ParamOption(password2)))), properties=('mandatory',))
    name = StrOption(name="name", doc="name", properties=('mandatory',))
    user = OptionDescription(name="user", doc="user", children=[name, password2])
    sub = OptionDescription(name="sub", doc="sub", children=[user])
    user_database = DynOptionDescription(name="user_database_", doc="user database", identifiers=Calculation(calc_value, Params((ParamOption(database_names, notraisepropertyerror=True)))), children=[password, sub])
    socle = OptionDescription(name="socle", doc="socle", children=[user_database, database_names])
    root = OptionDescription(name="baseoption", doc="baseoption", children=[socle])
    cfg = Config(root)
    assert cfg.option('socle.database_names').value.get() == ["srep", "snom", "srem"]
    assert cfg.option('socle.user_database_srep.password').value.get() is None
    assert cfg.option('socle.user_database_srep.sub.user.name').value.get() is None

    assert cfg.option('socle.user_database_srep.sub.user.password').value.get() is None
    assert [opt.path() for opt in cfg.value.mandatory()] == ['socle.user_database_srep.password',
                                                             'socle.user_database_srep.sub.user.name',
                                                             'socle.user_database_srep.sub.user.password',
                                                             'socle.user_database_snom.password',
                                                             'socle.user_database_snom.sub.user.name',
                                                             'socle.user_database_snom.sub.user.password',
                                                             'socle.user_database_srem.password',
                                                             'socle.user_database_srem.sub.user.name',
                                                             'socle.user_database_srem.sub.user.password',
                                                             ]
    #
    cfg.option('socle.user_database_srep.password').value.set('pass')
    cfg.option('socle.user_database_snom.sub.user.password').value.set('pass')
    assert cfg.option('socle.user_database_srep.password').value.get() is 'pass'
    assert cfg.option('socle.user_database_srep.sub.user.name').value.get() is None
    assert cfg.option('socle.user_database_srep.sub.user.password').value.get() is None
    assert cfg.option('socle.user_database_snom.password').value.get() is 'pass'
    assert [opt.path() for opt in cfg.value.mandatory()] == ['socle.user_database_srep.sub.user.name',
                                                             'socle.user_database_srep.sub.user.password',
                                                             'socle.user_database_snom.sub.user.name',
                                                             'socle.user_database_srem.password',
                                                             'socle.user_database_srem.sub.user.name',
                                                             'socle.user_database_srem.sub.user.password',
                                                             ]
    #
    cfg.option('socle.user_database_srep.sub.user.password').value.set('pass2')
    cfg.option('socle.user_database_srem.sub.user.password').value.set('pass3')
    cfg.option('socle.user_database_srep.sub.user.name').value.set('name1')
    cfg.option('socle.user_database_snom.sub.user.name').value.set('name2')
    cfg.option('socle.user_database_srem.sub.user.name').value.set('name3')
    assert [opt.path() for opt in cfg.value.mandatory()] == []
    assert parse_od_get(cfg.value.get()) == {'socle.database_names': ['srep',
                                                        'snom',
                                                        'srem'],
                               'socle.user_database_snom.password': 'pass',
                               'socle.user_database_snom.sub.user.name': 'name2',
                               'socle.user_database_snom.sub.user.password': 'pass',
                               'socle.user_database_srem.password': 'pass3',
                               'socle.user_database_srem.sub.user.name': 'name3',
                               'socle.user_database_srem.sub.user.password': 'pass3',
                               'socle.user_database_srep.password': 'pass',
                               'socle.user_database_srep.sub.user.name': 'name1',
                               'socle.user_database_srep.sub.user.password': 'pass2',
                               }
    #
    assert [opt.path() for opt in cfg.value.mandatory()] == []


def test_dyn_link_subdyn_twice():
    password = StrOption(name="password", doc="password", properties=('mandatory',))
    name = StrOption(name="name", doc="name", properties=('mandatory',))
    login = StrOption(name="login", doc="login", default=Calculation(calc_value, Params((ParamOption(name)))), properties=('mandatory',))
    password2 = StrOption(name="password2", doc="password2", default=Calculation(calc_value, Params((ParamOption(password)))), properties=('mandatory',))
    database_names = StrOption(name="database_names", doc="database_names", multi=True, default=["srep", "snom", "srem"])
    user_database = DynOptionDescription(name="user_database_", doc="user database", identifiers=Calculation(calc_value, Params((ParamOption(database_names, notraisepropertyerror=True)))), children=[name, login, password2])
    databases = OptionDescription(name="databases", doc="database", children=[password, user_database])
    schema_names = StrOption(name="database_schemas", doc="database_schemas", multi=True, default=["schema1", "schema2", "schema3"])
    schema = DynOptionDescription(name="schema_", doc="schema_", identifiers=Calculation(calc_value, Params((ParamOption(schema_names, notraisepropertyerror=True)))), children=[database_names, databases])
    socle = OptionDescription(name="socle", doc="socle", children=[schema, schema_names])
    root = OptionDescription(name="baseoption", doc="baseoption", children=[socle])
    cfg = Config(root)
    assert parse_od_get(cfg.value.get()) == {'socle.database_schemas': ['schema1',
                                                          'schema2',
                                                          'schema3'],
                               'socle.schema_schema1.database_names': ['srep',
                                                                       'snom',
                                                                       'srem'],
                               'socle.schema_schema1.databases.password': None,
                               'socle.schema_schema1.databases.user_database_snom.name': None,
                               'socle.schema_schema1.databases.user_database_snom.login': None,
                               'socle.schema_schema1.databases.user_database_snom.password2': None,
                               'socle.schema_schema1.databases.user_database_srem.name': None,
                               'socle.schema_schema1.databases.user_database_srem.login': None,
                               'socle.schema_schema1.databases.user_database_srem.password2': None,
                               'socle.schema_schema1.databases.user_database_srep.name': None,
                               'socle.schema_schema1.databases.user_database_srep.login': None,
                               'socle.schema_schema1.databases.user_database_srep.password2': None,
                               'socle.schema_schema2.database_names': ['srep',
                                                                       'snom',
                                                                       'srem'],
                               'socle.schema_schema2.databases.password': None,
                               'socle.schema_schema2.databases.user_database_snom.name': None,
                               'socle.schema_schema2.databases.user_database_snom.login': None,
                               'socle.schema_schema2.databases.user_database_snom.password2': None,
                               'socle.schema_schema2.databases.user_database_srem.name': None,
                               'socle.schema_schema2.databases.user_database_srem.login': None,
                               'socle.schema_schema2.databases.user_database_srem.password2': None,
                               'socle.schema_schema2.databases.user_database_srep.name': None,
                               'socle.schema_schema2.databases.user_database_srep.login': None,
                               'socle.schema_schema2.databases.user_database_srep.password2': None,
                               'socle.schema_schema3.database_names': ['srep',
                                                                       'snom',
                                                                       'srem'],
                               'socle.schema_schema3.databases.password': None,
                               'socle.schema_schema3.databases.user_database_snom.name': None,
                               'socle.schema_schema3.databases.user_database_snom.login': None,
                               'socle.schema_schema3.databases.user_database_snom.password2': None,
                               'socle.schema_schema3.databases.user_database_srem.name': None,
                               'socle.schema_schema3.databases.user_database_srem.login': None,
                               'socle.schema_schema3.databases.user_database_srem.password2': None,
                               'socle.schema_schema3.databases.user_database_srep.name': None,
                               'socle.schema_schema3.databases.user_database_srep.login': None,
                               'socle.schema_schema3.databases.user_database_srep.password2': None,
                               }
    #
    assert [opt.path() for opt in cfg.value.mandatory()] == ['socle.schema_schema1.databases.password',
                                                             'socle.schema_schema1.databases.user_database_srep.name',
                                                             'socle.schema_schema1.databases.user_database_srep.login',
                                                             'socle.schema_schema1.databases.user_database_srep.password2',
                                                             'socle.schema_schema1.databases.user_database_snom.name',
                                                             'socle.schema_schema1.databases.user_database_snom.login',
                                                             'socle.schema_schema1.databases.user_database_snom.password2',
                                                             'socle.schema_schema1.databases.user_database_srem.name',
                                                             'socle.schema_schema1.databases.user_database_srem.login',
                                                             'socle.schema_schema1.databases.user_database_srem.password2',
                                                             'socle.schema_schema2.databases.password',
                                                             'socle.schema_schema2.databases.user_database_srep.name',
                                                             'socle.schema_schema2.databases.user_database_srep.login',
                                                             'socle.schema_schema2.databases.user_database_srep.password2',
                                                             'socle.schema_schema2.databases.user_database_snom.name',
                                                             'socle.schema_schema2.databases.user_database_snom.login',
                                                             'socle.schema_schema2.databases.user_database_snom.password2',
                                                             'socle.schema_schema2.databases.user_database_srem.name',
                                                             'socle.schema_schema2.databases.user_database_srem.login',
                                                             'socle.schema_schema2.databases.user_database_srem.password2',
                                                             'socle.schema_schema3.databases.password',
                                                             'socle.schema_schema3.databases.user_database_srep.name',
                                                             'socle.schema_schema3.databases.user_database_srep.login',
                                                             'socle.schema_schema3.databases.user_database_srep.password2',
                                                             'socle.schema_schema3.databases.user_database_snom.name',
                                                             'socle.schema_schema3.databases.user_database_snom.login',
                                                             'socle.schema_schema3.databases.user_database_snom.password2',
                                                             'socle.schema_schema3.databases.user_database_srem.name',
                                                             'socle.schema_schema3.databases.user_database_srem.login',
                                                             'socle.schema_schema3.databases.user_database_srem.password2',
                                                             ]
    #
    cfg.option('socle.schema_schema2.database_names').value.set(['another'])
    assert parse_od_get(cfg.value.get()) == {'socle.database_schemas': ['schema1',
                                                          'schema2',
                                                          'schema3'],
                               'socle.schema_schema1.database_names': ['srep',
                                                                       'snom',
                                                                       'srem'],
                               'socle.schema_schema1.databases.password': None,
                               'socle.schema_schema1.databases.user_database_snom.name': None,
                               'socle.schema_schema1.databases.user_database_snom.login': None,
                               'socle.schema_schema1.databases.user_database_snom.password2': None,
                               'socle.schema_schema1.databases.user_database_srem.name': None,
                               'socle.schema_schema1.databases.user_database_srem.login': None,
                               'socle.schema_schema1.databases.user_database_srem.password2': None,
                               'socle.schema_schema1.databases.user_database_srep.name': None,
                               'socle.schema_schema1.databases.user_database_srep.login': None,
                               'socle.schema_schema1.databases.user_database_srep.password2': None,
                               'socle.schema_schema2.database_names': ['another'],
                               'socle.schema_schema2.databases.password': None,
                               'socle.schema_schema2.databases.user_database_another.name': None,
                               'socle.schema_schema2.databases.user_database_another.login': None,
                               'socle.schema_schema2.databases.user_database_another.password2': None,
                               'socle.schema_schema3.database_names': ['srep',
                                                                       'snom',
                                                                       'srem'],
                               'socle.schema_schema3.databases.password': None,
                               'socle.schema_schema3.databases.user_database_snom.name': None,
                               'socle.schema_schema3.databases.user_database_snom.login': None,
                               'socle.schema_schema3.databases.user_database_snom.password2': None,
                               'socle.schema_schema3.databases.user_database_srem.name': None,
                               'socle.schema_schema3.databases.user_database_srem.login': None,
                               'socle.schema_schema3.databases.user_database_srem.password2': None,
                               'socle.schema_schema3.databases.user_database_srep.name': None,
                               'socle.schema_schema3.databases.user_database_srep.login': None,
                               'socle.schema_schema3.databases.user_database_srep.password2': None,
                               }
    #
    cfg.option('socle.database_schemas').value.set(['schema1'])
    assert parse_od_get(cfg.value.get()) == {'socle.database_schemas': ['schema1'],
                               'socle.schema_schema1.database_names': ['srep',
                                                                       'snom',
                                                                       'srem'],
                               'socle.schema_schema1.databases.password': None,
                               'socle.schema_schema1.databases.user_database_snom.name': None,
                               'socle.schema_schema1.databases.user_database_snom.login': None,
                               'socle.schema_schema1.databases.user_database_snom.password2': None,
                               'socle.schema_schema1.databases.user_database_srem.name': None,
                               'socle.schema_schema1.databases.user_database_srem.login': None,
                               'socle.schema_schema1.databases.user_database_srem.password2': None,
                               'socle.schema_schema1.databases.user_database_srep.name': None,
                               'socle.schema_schema1.databases.user_database_srep.login': None,
                               'socle.schema_schema1.databases.user_database_srep.password2': None,
                               }
    #
    cfg.option('socle.schema_schema1.databases.password').value.set('password')
    cfg.option('socle.schema_schema1.databases.user_database_snom.name').value.set('name1')
    cfg.option('socle.schema_schema1.databases.user_database_srem.name').value.set('name2')
    cfg.option('socle.schema_schema1.databases.user_database_srep.name').value.set('name3')
    assert parse_od_get(cfg.value.get()) == {'socle.database_schemas': ['schema1'],
                               'socle.schema_schema1.database_names': ['srep',
                                                                       'snom',
                                                                       'srem'],
                               'socle.schema_schema1.databases.password': 'password',
                               'socle.schema_schema1.databases.user_database_snom.login': 'name1',
                               'socle.schema_schema1.databases.user_database_snom.name': 'name1',
                               'socle.schema_schema1.databases.user_database_snom.password2': 'password',
                               'socle.schema_schema1.databases.user_database_srem.login': 'name2',
                               'socle.schema_schema1.databases.user_database_srem.name': 'name2',
                               'socle.schema_schema1.databases.user_database_srem.password2': 'password',
                               'socle.schema_schema1.databases.user_database_srep.login': 'name3',
                               'socle.schema_schema1.databases.user_database_srep.name': 'name3',
                               'socle.schema_schema1.databases.user_database_srep.password2': 'password',
                               }
    assert [opt.path() for opt in cfg.value.mandatory()] == []
    #
    cfg.option('socle.schema_schema1.database_names').value.set(['snom'])
    assert parse_od_get(cfg.value.get()) == {'socle.database_schemas': ['schema1'],
                               'socle.schema_schema1.database_names': ['snom'],
                               'socle.schema_schema1.databases.password': 'password',
                               'socle.schema_schema1.databases.user_database_snom.login': 'name1',
                               'socle.schema_schema1.databases.user_database_snom.name': 'name1',
                               'socle.schema_schema1.databases.user_database_snom.password2': 'password',
                               }
    assert [opt.path() for opt in cfg.value.mandatory()] == []


def test_dyn_link_subdyn_tree():
    password = StrOption(name="password", doc="password", properties=('mandatory',))
    name = StrOption(name="name", doc="name", properties=('mandatory',))
    login = StrOption(name="login", doc="login", default=Calculation(calc_value, Params((ParamOption(name)))), properties=('mandatory',))
    password2 = StrOption(name="password2", doc="password2", default=Calculation(calc_value, Params((ParamOption(password)))), properties=('mandatory',))
    user_names = StrOption(name="users", doc="users", multi=True, default=["user1"])
    user_database = DynOptionDescription(name="user_database_", doc="user database", identifiers=Calculation(calc_value, Params((ParamOption(user_names, notraisepropertyerror=True)))), children=[name, login, password2])
    database_names = StrOption(name="database_names", doc="database_names", multi=True, default=["srep"])
    databases = DynOptionDescription(name="db_", doc="database", identifiers=Calculation(calc_value, Params((ParamOption(database_names, notraisepropertyerror=True)))), children=[user_names, password, user_database])
    schema_names = StrOption(name="database_schemas", doc="database_schemas", multi=True, default=["schema1"])
    schema = DynOptionDescription(name="schema_", doc="schema_", identifiers=Calculation(calc_value, Params((ParamOption(schema_names, notraisepropertyerror=True)))), children=[database_names, databases])
    socle = OptionDescription(name="socle", doc="socle", children=[schema, schema_names])
    root = OptionDescription(name="baseoption", doc="baseoption", children=[socle])
    cfg = Config(root)
    assert [opt.path() for opt in cfg.value.mandatory()] == ['socle.schema_schema1.db_srep.password',
                                                             'socle.schema_schema1.db_srep.user_database_user1.name',
                                                             'socle.schema_schema1.db_srep.user_database_user1.login',
                                                             'socle.schema_schema1.db_srep.user_database_user1.password2',
                                                             ]
    #
    cfg.option('socle.schema_schema1.db_srep.user_database_user1.name').value.set('name')
    assert [opt.path() for opt in cfg.value.mandatory()] == ['socle.schema_schema1.db_srep.password',
                                                             'socle.schema_schema1.db_srep.user_database_user1.password2',
                                                             ]
    #
    cfg.option('socle.schema_schema1.db_srep.password').value.set('password')
    assert [opt.path() for opt in cfg.value.mandatory()] == []
    assert parse_od_get(cfg.value.get()) == {'socle.database_schemas': ['schema1'],
                               'socle.schema_schema1.database_names': ['srep'],
                               'socle.schema_schema1.db_srep.password': 'password',
                               'socle.schema_schema1.db_srep.user_database_user1.login': 'name',
                               'socle.schema_schema1.db_srep.user_database_user1.name': 'name',
                               'socle.schema_schema1.db_srep.user_database_user1.password2': 'password',
                               'socle.schema_schema1.db_srep.users': ['user1'],
                               }
    #
    cfg.option('socle.schema_schema1.db_srep.users').value.set(['user1', 'user2'])
    assert parse_od_get(cfg.value.get()) == {'socle.database_schemas': ['schema1'],
                               'socle.schema_schema1.database_names': ['srep'],
                               'socle.schema_schema1.db_srep.password': 'password',
                               'socle.schema_schema1.db_srep.user_database_user1.login': 'name',
                               'socle.schema_schema1.db_srep.user_database_user1.name': 'name',
                               'socle.schema_schema1.db_srep.user_database_user1.password2': 'password',
                               'socle.schema_schema1.db_srep.user_database_user2.login': None,
                               'socle.schema_schema1.db_srep.user_database_user2.name': None,
                               'socle.schema_schema1.db_srep.user_database_user2.password2': 'password',
                               'socle.schema_schema1.db_srep.users': ['user1', 'user2'],
                               }
    #
    cfg.option('socle.schema_schema1.db_srep.users').value.set([])
    assert parse_od_get(cfg.value.get()) == {'socle.database_schemas': ['schema1'],
                               'socle.schema_schema1.database_names': ['srep'],
                               'socle.schema_schema1.db_srep.password': 'password',
                               'socle.schema_schema1.db_srep.users': [],
                               }
    #
    cfg.option('socle.schema_schema1.database_names').value.set([])
    assert parse_od_get(cfg.value.get()) == {'socle.database_schemas': ['schema1'],
                               'socle.schema_schema1.database_names': [],
                               }
    #
    cfg.option('socle.database_schemas').value.set([])
    assert parse_od_get(cfg.value.get()) == {'socle.database_schemas': [],
                               }
    #
    cfg.option('socle.database_schemas').value.reset()
    cfg.option('socle.schema_schema1.database_names').value.reset()
    cfg.option('socle.schema_schema1.db_srep.users').value.reset()
    assert parse_od_get(cfg.value.get()) == {'socle.database_schemas': ['schema1'],
                               'socle.schema_schema1.database_names': ['srep'],
                               'socle.schema_schema1.db_srep.password': 'password',
                               'socle.schema_schema1.db_srep.user_database_user1.login': 'name',
                               'socle.schema_schema1.db_srep.user_database_user1.name': 'name',
                               'socle.schema_schema1.db_srep.user_database_user1.password2': 'password',
                               'socle.schema_schema1.db_srep.users': ['user1'],
                               }


def test_dyn_link_subdyn_same_variable():
    password = StrOption(name="password", doc="password", properties=('mandatory',))
    name = StrOption(name="name", doc="name", properties=('mandatory',))
    login = StrOption(name="login", doc="login", default=Calculation(calc_value, Params((ParamOption(name)))), properties=('mandatory',))
    password2 = StrOption(name="password2", doc="password2", default=Calculation(calc_value, Params((ParamOption(password)))), properties=('mandatory',))
    schema_names = StrOption(name="database_schemas", doc="database_schemas", multi=True, default=["schema1"])
    user_database = DynOptionDescription(name="user_database_", doc="user database", identifiers=Calculation(calc_value, Params((ParamOption(schema_names, notraisepropertyerror=True)))), children=[name, login, password2])
    databases = DynOptionDescription(name="db_", doc="database", identifiers=Calculation(calc_value, Params((ParamOption(schema_names, notraisepropertyerror=True)))), children=[password, user_database])
    schema = DynOptionDescription(name="schema_", doc="schema_", identifiers=Calculation(calc_value, Params((ParamOption(schema_names, notraisepropertyerror=True)))), children=[databases])
    socle = OptionDescription(name="socle", doc="socle", children=[schema, schema_names])
    root = OptionDescription(name="baseoption", doc="baseoption", children=[socle])
    cfg = Config(root)
    assert [opt.path() for opt in cfg.value.mandatory()] == ['socle.schema_schema1.db_schema1.password',
                                                             'socle.schema_schema1.db_schema1.user_database_schema1.name',
                                                             'socle.schema_schema1.db_schema1.user_database_schema1.login',
                                                             'socle.schema_schema1.db_schema1.user_database_schema1.password2',
                                                             ]
    #
    cfg.option('socle.schema_schema1.db_schema1.user_database_schema1.name').value.set('name')
    assert [opt.path() for opt in cfg.value.mandatory()] == ['socle.schema_schema1.db_schema1.password',
                                                             'socle.schema_schema1.db_schema1.user_database_schema1.password2',
                                                             ]
    #
    cfg.option('socle.schema_schema1.db_schema1.password').value.set('password')
    cfg.option('socle.schema_schema1.db_schema1.user_database_schema1.name').value.set('name')
    assert [opt.path() for opt in cfg.value.mandatory()] == []
    assert parse_od_get(cfg.value.get()) == {'socle.database_schemas': ['schema1'],
                               'socle.schema_schema1.db_schema1.password': 'password',
                               'socle.schema_schema1.db_schema1.user_database_schema1.login': 'name',
                               'socle.schema_schema1.db_schema1.user_database_schema1.name': 'name',
                               'socle.schema_schema1.db_schema1.user_database_schema1.password2': 'password',
                               }
    #
    cfg.option('socle.database_schemas').value.set(['schema1', 'schema2'])
    assert [opt.path() for opt in cfg.value.mandatory()] == ['socle.schema_schema1.db_schema1.user_database_schema2.name',
                                                             'socle.schema_schema1.db_schema1.user_database_schema2.login',
                                                             'socle.schema_schema1.db_schema2.password',
                                                             'socle.schema_schema1.db_schema2.user_database_schema1.name',
                                                             'socle.schema_schema1.db_schema2.user_database_schema1.login',
                                                             'socle.schema_schema1.db_schema2.user_database_schema1.password2',
                                                             'socle.schema_schema1.db_schema2.user_database_schema2.name',
                                                             'socle.schema_schema1.db_schema2.user_database_schema2.login',
                                                             'socle.schema_schema1.db_schema2.user_database_schema2.password2',
                                                             'socle.schema_schema2.db_schema1.password',
                                                             'socle.schema_schema2.db_schema1.user_database_schema1.name',
                                                             'socle.schema_schema2.db_schema1.user_database_schema1.login',
                                                             'socle.schema_schema2.db_schema1.user_database_schema1.password2',
                                                             'socle.schema_schema2.db_schema1.user_database_schema2.name',
                                                             'socle.schema_schema2.db_schema1.user_database_schema2.login',
                                                             'socle.schema_schema2.db_schema1.user_database_schema2.password2',
                                                             'socle.schema_schema2.db_schema2.password',
                                                             'socle.schema_schema2.db_schema2.user_database_schema1.name',
                                                             'socle.schema_schema2.db_schema2.user_database_schema1.login',
                                                             'socle.schema_schema2.db_schema2.user_database_schema1.password2',

                                                             'socle.schema_schema2.db_schema2.user_database_schema2.name',
                                                             'socle.schema_schema2.db_schema2.user_database_schema2.login',
                                                             'socle.schema_schema2.db_schema2.user_database_schema2.password2',
                                                             ]
    assert parse_od_get(cfg.value.get()) == {'socle.database_schemas': ['schema1', 'schema2'],
                               'socle.schema_schema1.db_schema1.password': 'password',
                               'socle.schema_schema1.db_schema1.user_database_schema1.login': 'name',
                               'socle.schema_schema1.db_schema1.user_database_schema1.name': 'name',
                               'socle.schema_schema1.db_schema1.user_database_schema1.password2': 'password',
                               'socle.schema_schema1.db_schema1.user_database_schema2.login': None,
                               'socle.schema_schema1.db_schema1.user_database_schema2.name': None,
                               'socle.schema_schema1.db_schema1.user_database_schema2.password2': 'password',
                               'socle.schema_schema1.db_schema2.password': None,
                               'socle.schema_schema1.db_schema2.user_database_schema1.login': None,
                               'socle.schema_schema1.db_schema2.user_database_schema1.name': None,
                               'socle.schema_schema1.db_schema2.user_database_schema1.password2': None,
                               'socle.schema_schema1.db_schema2.user_database_schema2.login': None,
                               'socle.schema_schema1.db_schema2.user_database_schema2.name': None,
                               'socle.schema_schema1.db_schema2.user_database_schema2.password2': None,
                               'socle.schema_schema2.db_schema1.password': None,
                               'socle.schema_schema2.db_schema1.user_database_schema1.login': None,
                               'socle.schema_schema2.db_schema1.user_database_schema1.name': None,
                               'socle.schema_schema2.db_schema1.user_database_schema1.password2': None,
                               'socle.schema_schema2.db_schema1.user_database_schema2.login': None,
                               'socle.schema_schema2.db_schema1.user_database_schema2.name': None,
                               'socle.schema_schema2.db_schema1.user_database_schema2.password2': None,
                               'socle.schema_schema2.db_schema2.password': None,
                               'socle.schema_schema2.db_schema2.user_database_schema1.login': None,
                               'socle.schema_schema2.db_schema2.user_database_schema1.name': None,
                               'socle.schema_schema2.db_schema2.user_database_schema1.password2': None,
                               'socle.schema_schema2.db_schema2.user_database_schema2.login': None,
                               'socle.schema_schema2.db_schema2.user_database_schema2.name': None,
                               'socle.schema_schema2.db_schema2.user_database_schema2.password2': None,
                               }
    assert parse_od_get(cfg.option('socle.schema_schema1.db_schema1.user_database_schema1').value.get()) == {
                               'socle.schema_schema1.db_schema1.user_database_schema1.login': 'name',
                               'socle.schema_schema1.db_schema1.user_database_schema1.name': 'name',
                               'socle.schema_schema1.db_schema1.user_database_schema1.password2': 'password',
                               }


def test_dyn_link_subdyn_disabled():
    password = StrOption(name="password", doc="password")
    name = StrOption(name="name", doc="name")
    login = StrOption(name="login", doc="login", default=Calculation(calc_value, Params((ParamOption(name)))))
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(login),
                                                   'expected': ParamValue('name'),
                                                   'default': ParamValue(None)}))
    password2 = StrOption(name="password2", doc="password2", default=Calculation(calc_value, Params((ParamOption(password)))), properties=(disabled_property,))
    schema_names = StrOption(name="database_schemas", doc="database_schemas", multi=True, default=["schema1"])
    user_database = DynOptionDescription(name="user_database_", doc="user database", identifiers=Calculation(calc_value, Params((ParamOption(schema_names, notraisepropertyerror=True)))), children=[name, login, password2])
    databases = DynOptionDescription(name="db_", doc="database", identifiers=Calculation(calc_value, Params((ParamOption(schema_names, notraisepropertyerror=True)))), children=[password, user_database])
    schema = DynOptionDescription(name="schema_", doc="schema_", identifiers=Calculation(calc_value, Params((ParamOption(schema_names, notraisepropertyerror=True)))), children=[databases])
    socle = OptionDescription(name="socle", doc="socle", children=[schema, schema_names])
    root = OptionDescription(name="baseoption", doc="baseoption", children=[socle])
    cfg = Config(root)
    cfg.property.read_write()
    assert [opt.path() for opt in cfg.value.mandatory()] == []
    assert parse_od_get(cfg.value.get()) == {'socle.database_schemas': ['schema1'],
                               'socle.schema_schema1.db_schema1.password': None,
                               'socle.schema_schema1.db_schema1.user_database_schema1.login': None,
                               'socle.schema_schema1.db_schema1.user_database_schema1.name': None,
                               'socle.schema_schema1.db_schema1.user_database_schema1.password2': None,
                               }
    #
    cfg.option('socle.schema_schema1.db_schema1.user_database_schema1.name').value.set('name')
    assert parse_od_get(cfg.value.get()) == {'socle.database_schemas': ['schema1'],
                               'socle.schema_schema1.db_schema1.password': None,
                               'socle.schema_schema1.db_schema1.user_database_schema1.login': 'name',
                               'socle.schema_schema1.db_schema1.user_database_schema1.name': 'name',
                               }
    #
    cfg.option('socle.database_schemas').value.set(['schema1', 'schema2'])
    cfg.option('socle.schema_schema2.db_schema2.user_database_schema2.name').value.set('name2')
    assert parse_od_get(cfg.value.get()) == {'socle.database_schemas': ['schema1', 'schema2'],
                               'socle.schema_schema1.db_schema1.password': None,
                               'socle.schema_schema1.db_schema1.user_database_schema1.login': 'name',
                               'socle.schema_schema1.db_schema1.user_database_schema1.name': 'name',
                               'socle.schema_schema1.db_schema1.user_database_schema2.login': None,
                               'socle.schema_schema1.db_schema1.user_database_schema2.name': None,
                               'socle.schema_schema1.db_schema1.user_database_schema2.password2': None,
                               'socle.schema_schema1.db_schema2.password': None,
                               'socle.schema_schema1.db_schema2.user_database_schema1.login': None,
                               'socle.schema_schema1.db_schema2.user_database_schema1.name': None,
                               'socle.schema_schema1.db_schema2.user_database_schema1.password2': None,
                               'socle.schema_schema1.db_schema2.user_database_schema2.login': None,
                               'socle.schema_schema1.db_schema2.user_database_schema2.name': None,
                               'socle.schema_schema1.db_schema2.user_database_schema2.password2': None,
                               'socle.schema_schema2.db_schema1.password': None,
                               'socle.schema_schema2.db_schema1.user_database_schema1.login': None,
                               'socle.schema_schema2.db_schema1.user_database_schema1.name': None,
                               'socle.schema_schema2.db_schema1.user_database_schema1.password2': None,
                               'socle.schema_schema2.db_schema1.user_database_schema2.login': None,
                               'socle.schema_schema2.db_schema1.user_database_schema2.name': None,
                               'socle.schema_schema2.db_schema1.user_database_schema2.password2': None,
                               'socle.schema_schema2.db_schema2.password': None,
                               'socle.schema_schema2.db_schema2.user_database_schema1.login': None,
                               'socle.schema_schema2.db_schema2.user_database_schema1.name': None,
                               'socle.schema_schema2.db_schema2.user_database_schema1.password2': None,
                               'socle.schema_schema2.db_schema2.user_database_schema2.login': 'name2',
                               'socle.schema_schema2.db_schema2.user_database_schema2.name': 'name2',
                               'socle.schema_schema2.db_schema2.user_database_schema2.password2': None,
                               }
    assert cfg.option('socle.schema_schema1.db_schema1.user_database_schema1.name').owner.get() == owners.user
    assert cfg.option('socle.schema_schema1.db_schema1.user_database_schema1.name').information.get('doc') == 'name'


def test_option_dynoption_display_name():
    password = StrOption(name="password", doc="password")
    schema_names = StrOption(name="database_schemas", doc="database_schemas", multi=True, default=["schema1"])
    user_database = OptionDescription(name="user_database", doc="user database", children=[password])
    databases = DynOptionDescription(name="db_", doc="database", identifiers=Calculation(calc_value, Params((ParamOption(schema_names, notraisepropertyerror=True)))), children=[user_database])
    schema = DynOptionDescription(name="schema_", doc="schema_", identifiers=Calculation(calc_value, Params((ParamOption(schema_names, notraisepropertyerror=True)))), children=[databases])
    socle = OptionDescription(name="socle", doc="socle", children=[schema, schema_names])
    root = OptionDescription(name="baseoption", doc="baseoption", children=[socle])
    cfg = Config(root, display_name=display_name)
    assert cfg.option('socle.schema_schema1.db_schema1.user_database').description() == 'socle.schema_schema1.db_schema1.user_database (user database)'


def test_option_dynoption_param_information():
    info1 = StrOption("info1", '', Calculation(calc_value, Params(ParamSelfInformation('key'))), informations={'key': 'value'})
    info2 = StrOption("info2", '', Calculation(calc_value, Params(ParamInformation('key', option=info1))))
    schema = DynOptionDescription(name="schema_", doc="schema_", identifiers=Calculation(calc_value, Params(ParamValue(['1', '2']))), children=[info1, info2])
    root = OptionDescription(name="baseoption", doc="baseoption", children=[schema])
    cfg = Config(root, display_name=display_name)
    assert parse_od_get(cfg.value.get()) == {'schema_1.info1': 'value', 'schema_1.info2': 'value', 'schema_2.info1': 'value', 'schema_2.info2': 'value'}
    cfg.option('schema_1.info1').information.set('key', 'value1')
    assert parse_od_get(cfg.value.get()) == {'schema_1.info1': 'value1', 'schema_1.info2': 'value1', 'schema_2.info1': 'value', 'schema_2.info2': 'value'}


def test_callback_list_dyndescription_information():
    st = StrOption('st', '', Calculation(return_list2, Params(ParamIdentifier())), multi=True, properties=('notunique',))
    dod = DynOptionDescription('dod', '', [st], identifiers=Calculation(return_list, Params(ParamInformation('identifier'))))
    od = OptionDescription('od', '', [dod])
    od2 = OptionDescription('od', '', [od], informations={'identifier': ['ival1', 'ival2']})
    cfg = Config(od2)
    owner = cfg.owner.get()
    assert cfg.option('od.dodival1.st').value.get() == ['ival1', 'val2']
    assert cfg.option('od.dodival2.st').value.get() == ['ival2', 'val2']
    assert cfg.option('od.dodival1.st').owner.isdefault()
    assert cfg.option('od.dodival2.st').owner.isdefault()
    cfg.option('od.dodival1.st').value.set(['val3', 'val2'])
    assert cfg.option('od.dodival1.st').value.get() == ['val3', 'val2']
    assert cfg.option('od.dodival2.st').value.get() == ['ival2', 'val2']
    assert cfg.option('od.dodival1.st').owner.get() == owner
    assert cfg.option('od.dodival2.st').owner.isdefault()
    cfg.information.set('identifier', ['ival3'])
    assert cfg.option('od.dodival3.st').value.get() == ['ival3', 'val2']
#    assert not list_sessions()


def test_callback_list_dyndescription_information_not_list():
    st = StrOption('st', '', Calculation(return_list2, Params(ParamIdentifier())), multi=True, properties=('notunique',))
    dod = DynOptionDescription('dod', '', [st], identifiers=["sval1", Calculation(return_dynval, Params(ParamInformation('identifier')))])
    od = OptionDescription('od', '', [dod])
    od2 = OptionDescription('od', '', [od], informations={'identifier': 'ival2'})
    cfg = Config(od2)
    owner = cfg.owner.get()
    assert cfg.option('od.dodsval1.st').value.get() == ['sval1', 'val2']
    assert cfg.option('od.dodival2.st').value.get() == ['ival2', 'val2']
    assert cfg.option('od.dodsval1.st').owner.isdefault()
    assert cfg.option('od.dodival2.st').owner.isdefault()
    cfg.option('od.dodsval1.st').value.set(['val3', 'val2'])
    assert cfg.option('od.dodsval1.st').value.get() == ['val3', 'val2']
    assert cfg.option('od.dodival2.st').value.get() == ['ival2', 'val2']
    assert cfg.option('od.dodsval1.st').owner.get() == owner
    assert cfg.option('od.dodival2.st').owner.isdefault()
    cfg.information.set('identifier', 'ival3')
    assert cfg.option('od.dodival3.st').value.get() == ['ival3', 'val2']
#    assert not list_sessions()
