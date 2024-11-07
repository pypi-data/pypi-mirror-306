# coding: utf-8
from .autopath import do_autopath
do_autopath()
from .config import config_type, get_config, value_list, global_owner, parse_od_get

from pytest import raises
from tiramisu import ChoiceOption, StrOption, OptionDescription, Config, owners, Calculation, \
                     undefined, Params, ParamValue, ParamOption
from tiramisu.error import ConfigError


def return_val(val):
    return val


def return_list():
    return ['val1', 'val2']


def return_calc_list(val):
    return [val]


def return_error(*args, **kwargs):
    raise Exception('test')


def test_choiceoption(config_type):
    choice = ChoiceOption('choice', '', values=('val1', 'val2'))
    od1 = OptionDescription('od', '', [choice])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    owner = global_owner(cfg, config_type)
    assert cfg.option('choice').owner.get() == owners.default
    assert cfg.option('choice').owner.isdefault()
    #
    cfg.option('choice').value.set('val1')
    assert cfg.option('choice').owner.get() == owner
    assert not cfg.option('choice').owner.isdefault()
    #
    cfg.option('choice').value.reset()
    assert cfg.option('choice').owner.get() == owners.default
    assert cfg.option('choice').owner.isdefault()
    #
    with raises(ValueError):
        cfg.option('choice').value.set('no')
    assert cfg.option('choice').owner.get() == owners.default
    assert cfg.option('choice').owner.isdefault()
    #
    assert value_list(cfg.option('choice').value.list()) == ('val1', 'val2')
#    assert not list_sessions()


def test_choiceoption_function(config_type):
    choice = ChoiceOption('choice', '', values=Calculation(return_list))
    od1 = OptionDescription('od', '', [choice])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    owner = global_owner(cfg, config_type)
    assert cfg.option('choice').owner.isdefault()
    #
    cfg.option('choice').value.set('val1')
    assert cfg.option('choice').owner.get() == owner
    #
    cfg.option('choice').value.reset()
    assert cfg.option('choice').owner.isdefault()
    #
    with raises(ValueError):
        cfg.option('choice').value.set('no')
    assert cfg.option('choice').owner.isdefault()
    #
    assert value_list(cfg.option('choice').value.list()) == ('val1', 'val2')
    assert isinstance(cfg.option('choice').value.list(uncalculated=True), Calculation)
#    assert not list_sessions()


def test_choiceoption_subfunction(config_type):
    choice = ChoiceOption('choice', '', values=(Calculation(return_val, Params(ParamValue('val1'))), Calculation(return_val, Params(ParamValue('val2')))))
    od1 = OptionDescription('od', '', [choice])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    owner = global_owner(cfg, config_type)
    assert cfg.option('choice').owner.isdefault()
    #
    cfg.option('choice').value.set('val1')
    assert cfg.option('choice').owner.get() == owner
    #
    cfg.option('choice').value.reset()
    assert cfg.option('choice').owner.isdefault()
    #
    with raises(ValueError):
        cfg.option('choice').value.set('no')
    assert cfg.option('choice').owner.isdefault()
    #
    assert value_list(cfg.option('choice').value.list()) == ('val1', 'val2')
#    assert not list_sessions()


def test_choiceoption_function_error():
    choice = ChoiceOption('choice', '', values=Calculation(return_error))
    od1 = OptionDescription('od', '', [choice])
    cfg = Config(od1)
    cfg.property.read_write()
    with raises(ConfigError):
        cfg.option('choice').value.set('val1')
#    assert not list_sessions()


def test_choiceoption_function_error_args():
    choice = ChoiceOption('choice', '', values=Calculation(return_error, Params(ParamValue('val1'))))
    od1 = OptionDescription('od', '', [choice])
    cfg = Config(od1)
    cfg.property.read_write()
    with raises(ConfigError):
        cfg.option('choice').value.set('val1')
#    assert not list_sessions()


def test_choiceoption_function_error_kwargs():
    choice = ChoiceOption('choice', '', values=Calculation(return_error, Params(kwargs={'kwargs': ParamValue('val1')})))
    od1 = OptionDescription('od', '', [choice])
    cfg = Config(od1)
    cfg.property.read_write()
    with raises(ConfigError):
        cfg.option('choice').value.set('val1')
#    assert not list_sessions()


def test_choiceoption_calc_function(config_type):
    choice = ChoiceOption('choice', "", values=Calculation(return_calc_list, Params(ParamValue('val1'))))
    od1 = OptionDescription('od', '', [choice])
    cfg = Config(od1)
    cfg.property.read_write()
    cfg = get_config(cfg, config_type)
    owner = global_owner(cfg, config_type)
    assert cfg.option('choice').owner.isdefault()
    #
    cfg.option('choice').value.set('val1')
    assert cfg.option('choice').owner.get() == owner
    #
    cfg.option('choice').value.reset()
    assert cfg.option('choice').owner.isdefault()
    #
    with raises(ValueError):
        cfg.option('choice').value.set('no')
    assert cfg.option('choice').owner.isdefault()
#    assert not list_sessions()


def test_choiceoption_calc_opt_function(config_type):
    str_ = StrOption('str', '', 'val1')
    choice = ChoiceOption('choice',
                          "",
                          values=Calculation(return_calc_list, Params(ParamOption(str_))))
    od1 = OptionDescription('od', '', [str_, choice])
    cfg = Config(od1)
    cfg.property.read_write()
    owner = cfg.owner.get()
    cfg = get_config(cfg, config_type)
    assert cfg.option('choice').owner.isdefault()
    #
    cfg.option('choice').value.set('val1')
    assert cfg.option('choice').owner.get() == owner
    #
    cfg.option('choice').value.reset()
    assert cfg.option('choice').owner.isdefault()
    #
    with raises(ValueError):
        cfg.option('choice').value.set('no')
    assert cfg.option('choice').owner.isdefault()
#    assert not list_sessions()


def test_choiceoption_calc_opt_function_propertyerror():
    str_ = StrOption('str', '', 'val1', properties=('disabled',))
    choice = ChoiceOption('choice',
                          "",
                          values=Calculation(return_calc_list, Params(ParamOption(str_))))
    od1 = OptionDescription('od', '', [str_, choice])
    cfg = Config(od1)
    cfg.property.read_write()
    with raises(ConfigError):
        cfg.option('choice').value.set('no')
#    assert not list_sessions()


#def test_choiceoption_calc_opt_multi_function(config_type):
def test_choiceoption_calc_opt_multi_function():
    # FIXME
    config_type = 'tiramisu'
    str_ = StrOption('str', '', ['val1'], multi=True)
    choice = ChoiceOption('choice',
                          "",
                          default_multi='val2',
                          values=Calculation(return_val, Params(ParamOption(str_))),
                          multi=True)
    ch2 = ChoiceOption('ch2',
                       "",
                       default=['val2'],
                       values=Calculation(return_val, Params(ParamOption(str_))),
                       multi=True)
    od1 = OptionDescription('od', '', [str_, choice, ch2])
    cfg = Config(od1)
    cfg.property.read_write()
    owner = cfg.owner.get()
    cfg = get_config(cfg, config_type, True)
    assert cfg.option('choice').owner.isdefault()
    assert cfg.option('choice').value.get() == []
    #
    cfg.option('choice').value.set(['val1'])
    assert cfg.option('choice').owner.get() == owner
    #
    with raises(ValueError):
        cfg.option('choice').value.set([undefined])
    #
    cfg.option('choice').value.set(['val1'])
    assert cfg.option('choice').owner.get() == owner
    #
    cfg.option('choice').value.reset()
    assert cfg.option('choice').owner.isdefault()
    #
    with raises(ValueError):
        cfg.option('choice').value.set('no')
    assert cfg.option('choice').owner.isdefault()
    #
    with raises(ValueError):
        cfg.option('ch2').value.get()
#    assert not list_sessions()


def test_choiceoption_calc_opt_multi_function_kwargs(config_type):
    str_ = StrOption('str', '', ['val1'], multi=True)
    choice = ChoiceOption('choice',
                          "",
                          default_multi='val2',
                          values=Calculation(return_val, Params(kwargs={'val': ParamOption(str_)})),
                          multi=True)
    ch2 = ChoiceOption('ch2',
                       "",
                       default=['val2'],
                       values=Calculation(return_val, Params(kwargs={'val': ParamOption(str_)})),
                       multi=True)
    od1 = OptionDescription('od', '', [str_, choice, ch2])
    cfg = Config(od1)
    cfg.property.read_write()
    owner = cfg.owner.get()
    # FIXME cfg = get_config(cfg, config_type)
    assert cfg.option('choice').owner.isdefault()
    assert cfg.option('choice').value.get() == []
    #
    cfg.option('choice').value.set(['val1'])
    assert cfg.option('choice').owner.get() == owner
    #
    with raises(ValueError):
        cfg.option('choice').value.set([undefined])
    #
    cfg.option('choice').value.set(['val1'])
    assert cfg.option('choice').owner.get() == owner
    #
    cfg.option('choice').value.reset()
    assert cfg.option('choice').owner.isdefault()
    #
    with raises(ValueError):
        cfg.option('choice').value.set('no')
    assert cfg.option('choice').owner.isdefault()
    #
    with raises(ValueError):
        cfg.option('ch2').value.get()
#    assert not list_sessions()


def test_choiceoption_calc_not_list():
    str_ = StrOption('str', '', 'val1')
    choice = ChoiceOption('choice',
                          "",
                          default_multi='val2',
                          values=Calculation(return_val, Params(ParamOption(str_))),
                          multi=True)
    od1 = OptionDescription('od', '', [str_, choice])
    cfg = Config(od1)
    cfg.property.read_write()
    with raises(ConfigError):
        cfg.option('choice').value.set(['val1'])
#    assert not list_sessions()


def test_choiceoption_calc_default_value():
    var1 = StrOption("var1", '', default="val1")
    var2 = StrOption("var2", '', default="val2")
    choice = ChoiceOption("choice", '', values=(Calculation(return_val, Params((ParamOption(var1)))), Calculation(return_val, Params((ParamOption(var2))))), default="val1")
    od2 = OptionDescription("rougail", '', children=[var1, var2, choice])
    od1 = OptionDescription("baseoption", "", children=[od2])
    cfg = Config(od1)
    assert parse_od_get(cfg.value.get()) == {'rougail.var1': 'val1', 'rougail.var2': 'val2', 'rougail.choice': 'val1'}
