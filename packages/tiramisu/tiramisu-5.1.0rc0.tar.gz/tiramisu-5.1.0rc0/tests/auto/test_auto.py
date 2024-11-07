"""test API
"""
#import weakref
import pytest
#import warnings
#from copy import copy
#from py.test import raises
#from collections import OrderedDict
#from .autopath import do_autopath
#do_autopath()
#from tiramisu import Config, MetaConfig, \
#                     StrOption, SymLinkOption, OptionDescription, Leadership, DynOptionDescription, \
#                     submulti, undefined, owners, Params, ParamOption, Calculation
from tiramisu import Config, DynOptionDescription, OptionDescription, Leadership, \
        StrOption, IntOption, ChoiceOption, SymLinkOption, \
        Calculation, Params, ParamValue, ParamOption, ParamSelfOption, ParamInformation, ParamSelfInformation, ParamIndex, ParamIdentifier, \
        submulti, calc_value, owners
from tiramisu.option.baseoption import BaseOption
from tiramisu.error import ConfigError, ConstError, PropertiesOptionError, LeadershipError
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES


def return_var(val=None):
    return val


def return_var_disabled(multi, p=None):
    if p is not None:
        multi = p
    if multi:
        return []
    return None


def return_val(multi):
    if multi:
        return ['val']
    return 'val'


def return_property():
    return 'prop'


def return_disabled(var=None):
    return 'disabled'


def return_validator(self, other):
    return self == other


def build_variables(*,
                    mandatory=False,
                    multi=False,
                    leadership=False,
                    dynoptiondescription=False,
                    parent_variables=[],
                    dynamic=False,
                    hidden=False,
                    ):
    base_name = 'str_'
    if mandatory:
        properties = ['mandatory']
        base_name += 'mandatory_'
    else:
        properties = []
    if multi is True:
        base_name += 'multi_'
    elif multi is submulti:
        base_name += 'submulti_'
    if leadership:
        param_multi = multi is submulti
    else:
        param_multi = multi
    if not param_multi:
        str1_5_informations = {'info': 'value'}
        cfg_informations = Calculation(return_var, Params(ParamInformation('cfg_key')))
    else:
        str1_5_informations = {'info': ['value']}
        cfg_informations = [Calculation(return_var, Params(ParamInformation('cfg_key')))]
    if leadership:
        base_name += 'deps_follower_0_'
    if dynamic or dynoptiondescription:
        base_name += 'dynamic_'
    if hidden:
        base_name += 'hidden_'
    #str_mandatory_multi_hidden_information_deps
    str1 = StrOption(base_name + 'information_deps',
                     '',
                     multi=multi,
                     properties=tuple(properties),
                     informations=str1_5_informations,
                     )
    str2 = StrOption(base_name + 'disabled_deps',
                     '',
                     multi=multi,
                     properties=tuple(properties + ['disabled']),
                     )
    str3_name = base_name + 'calc_property_param_disabled'
    if not leadership:
        str3_name += '_deps'
    str3 = StrOption(str3_name,
                     '',
                     multi=multi,
                     properties=tuple(properties + [Calculation(return_disabled, Params(ParamOption(str2, notraisepropertyerror=True)))]),
                     )
    choice = ChoiceOption(base_name + 'choice_deps',
                          '',
                          values=('val1', 'val2'),
                          multi=multi,
                          properties=tuple(properties),
                          )
    variables = [str1,
                 str2,
                 StrOption(base_name + 'calc_default',
                           '',
                           Calculation(return_val, Params(ParamValue(param_multi))),
                           multi=multi,
                           properties=tuple(properties),
                           ),
                 StrOption(base_name + 'calc_default_param',
                           '',
                           Calculation(return_var, Params(ParamOption(str1))),
                           multi=multi,
                           properties=tuple(properties)
                           ),
                 StrOption(base_name + 'calc_default_param_disable',
                           '',
                           Calculation(return_var_disabled, Params((ParamOption(str2, notraisepropertyerror=True), ParamValue(param_multi)))),
                           multi=multi,
                           properties=tuple(properties),
                           ),
                 StrOption(base_name + 'calc_property',
                           '',
                           multi=multi,
                           properties=tuple(properties + [Calculation(return_property)]),
                           ),
                 StrOption(base_name + 'calc_property_disabled',
                           '',
                           multi=multi,
                           properties=tuple(properties + [Calculation(return_disabled, Params(ParamOption(str1)))]),
                           ),
                 StrOption(base_name + 'calc_property_disabled_self',
                           '',
                           multi=multi,
                           properties=tuple(properties + [Calculation(return_disabled, Params(ParamSelfOption()))]),
                           ),
                 StrOption(base_name + 'validator',
                           '',
                           multi=multi,
                           properties=tuple(properties),
                           validators=[Calculation(return_validator, Params((ParamSelfOption(), ParamOption(str1))))],
                           ),
                 StrOption(base_name + 'calc_default_information',
                           '',
                           Calculation(return_var, Params(ParamInformation('info', option=str1))),
                           multi=multi,
                           properties=tuple(properties),
                           ),
                 StrOption(base_name + 'calc_default_information_cfg',
                           '',
                           cfg_informations,
                           multi=multi,
                           properties=tuple(properties),
                           ),
                 str3,
                 StrOption(base_name + 'calc_default_information_self',
                           '',
                           Calculation(return_var, Params(ParamSelfInformation('info'))),
                           multi=multi,
                           properties=tuple(properties),
                           informations=str1_5_informations,
                           ),
                 choice,
                 ]
    if not leadership:
        sym1 = SymLinkOption(base_name + 'symlink_information_deps', str1)
        sym2 = SymLinkOption(base_name + 'symlink_disabled_deps', str2)
        variables.extend([sym1,
                          sym2,
                          SymLinkOption(base_name + 'symlink_calc_property_disabled_deps', str3),
                          SymLinkOption(base_name + 'symlink_choice_deps', choice),
                          StrOption(base_name + 'calc_default_param_sym',
                                    '',
                                    Calculation(return_var, Params(ParamOption(sym1))),
                                    multi=multi,
                                    properties=tuple(properties)
                                    ),
                          StrOption(base_name + 'calc_default_param_disable_sym',
                                    '',
                                    Calculation(return_var_disabled, Params((ParamOption(sym2, notraisepropertyerror=True), ParamValue(param_multi)))),
                                    multi=multi,
                                    properties=tuple(properties),
                                    ),
                          StrOption(base_name + 'calc_property_param_disabled_sym',
                                   '',
                                   multi=multi,
                                   properties=tuple(properties + [Calculation(return_disabled, Params(ParamOption(sym2, notraisepropertyerror=True)))]),
                                   )
                          ])
    else:
        default = Calculation(calc_value, Params(ParamIndex()))
        if param_multi:
            default = [default]
        variables.append(IntOption(base_name + 'calc_default_index',
                                   '',
                                   default,
                                   multi=multi,
                                   properties=tuple(properties),
                                   )
                          )
    if dynoptiondescription:
        default = Calculation(calc_value, Params(ParamIdentifier()))
        if param_multi:
            default = [default]
        variables.append(StrOption(base_name + 'calc_default_identifier',
                                   '',
                                   default,
                                   multi=multi,
                                   properties=tuple(properties),
                                   )
                          )
    if not leadership:
        for idx, parent in enumerate(parent_variables):
            if not parent:
                continue
            base_name_2 = 'parent_'
            if dynamic or dynoptiondescription:
                base_name_2 += 'dynamic_'
            if hidden:
                base_name_2 += 'hidden_'
            base_name_3 = base_name_2
            if mandatory:
                base_name_2 += 'mandatory_'
            variables.extend([
                StrOption(f'{base_name_2}calc_default_param_{idx}',
                          '',
                          Calculation(return_var, Params(ParamOption(parent[0]))),
                          properties=tuple(properties),
                          ),
                StrOption(f'{base_name_2}calc_property_disabled_{idx}',
                          '',
                          properties=tuple(properties + [Calculation(return_disabled, Params(ParamOption(parent[0])))]),
                          ),
                StrOption(f'{base_name_2}validator_{idx}',
                          '',
                          properties=tuple(properties),
                          validators=[Calculation(return_validator, Params((ParamSelfOption(), ParamOption(parent[0]))))],
                          ),
                StrOption(f'{base_name_2}calc_default_information_{idx}',
                          '',
                          Calculation(return_var, Params(ParamInformation('info', option=parent[0]))),
                          properties=tuple(properties),
                          ),
                SymLinkOption(f'{base_name_3}symlink_information_deps_{idx}', parent[0]),
                #
                StrOption(f'{base_name_2}calc_property_param_disabled_{idx}',
                          '',
                          properties=tuple(properties + [Calculation(return_disabled, Params(ParamOption(parent[1], notraisepropertyerror=True)))]),
                          ),
                StrOption(f'{base_name_2}calc_default_param_disable_{idx}',
                          '',
                          Calculation(return_var_disabled, Params((ParamOption(parent[1], notraisepropertyerror=True), ParamValue(False)))),
                          properties=tuple(properties),
                          ),
                SymLinkOption(f'{base_name_3}symlink_disabled_deps_{idx}', parent[1]),
            ])
    return variables


def build_options_for_parent(dynoptiondescription,
                             hidden,
                             ):
    base_name = 'parent_'
    if dynoptiondescription:
        base_name += 'dynamic_'
    if hidden:
        base_name += 'hidden_'
    return (StrOption(base_name + 'information_deps', '', informations={'info': 'parent_value'}),
            StrOption(base_name + 'disabled_deps',
                      '',
                      properties=('disabled',),
                      ),
            )


def build_root_variables(*,
                         tree,
                         **kwargs,
                         ):
    parent_variables = []
    dynamic = False
    hidden = False
    hidden_idx = 0
    for t in tree:
        if hidden:
            hidden_idx += 1
        if t.startswith('h'):
            t = t[1:]
            hidden = True
        if t == 'dod':
            dynamic=True
        parent_variables.append(build_options_for_parent(dynamic, hidden))
    variables = build_variables(**kwargs, parent_variables=parent_variables, dynamic=dynamic, hidden=hidden)
    follower_params = kwargs.copy()
    follower_params['leadership'] = True
    if 'multi' in follower_params and follower_params['multi']:
        follower_params['multi'] = submulti
    else:
        follower_params['multi'] = True
    identifier = ''
    if dynamic:
        identifier += '_dynamic'
    lidentifier = identifier
    if hidden:
        lidentifier += '_hidden'
    variables.append(Leadership('leadership' + lidentifier, '', [StrOption('leader_multi_deps' + lidentifier,
                                                                      '',
                                                                      default=['l1', 'l2'],
                                                                      multi=True,
                                                                      ),
                                                            ] + build_variables(**follower_params, parent_variables=parent_variables, dynamic=dynamic, hidden=hidden),
                                ))
    identifiers = StrOption('identifiers_multi_deps' + lidentifier, '', ['d1', 'd2'], multi=True)
    variables.append(identifiers)
    dynamic_name = 'dynamic_'
    if hidden:
        dynamic_name += 'hidden_'
    variables.append(DynOptionDescription(dynamic_name, '', build_variables(**kwargs, dynoptiondescription=True, parent_variables=parent_variables, dynamic=dynamic, hidden=hidden), Calculation(return_var, Params(ParamOption(identifiers)))))
    tree.reverse()
    for idx, t in enumerate(tree):
        lidentifier = identifier
        variables.extend(parent_variables.pop(-1))
        if hidden and idx <= hidden_idx:
            if t.startswith('h'):
                lidentifier = '_self_hidden' + identifier
            else:
                lidentifier = '_hidden' + identifier
        if t.startswith('h'):
            t = t[1:]
            properties = frozenset(['hidden'])
        else:
            properties = frozenset()
        if t == 'dod':
            variables = [DynOptionDescription('tree_dynamic' + lidentifier, '', variables, Calculation(return_var, Params(ParamValue(['var1', 'var2']))), properties=properties)]
        else:
            variables = [OptionDescription('tree' + lidentifier, '', variables, properties=properties)]
    od = OptionDescription('root', 'root', variables, informations={'cfg_key': 'cfg_info'})
    return od


PARAMS = [{},
          {'mandatory': True},
          {'multi': True},
          {'mandatory': True, 'multi': True},
          ]
OD = [
      [],
      ['od'],
      ['od', 'od'],
      ['hod'],
      ['hod', 'od'],
      ['od', 'hod'],
      ['dod'],
      ['hdod'],
      ['dod', 'dod'],
      ['hdod', 'dod'],
      ['dod', 'hdod'],
      ['dod', 'od'],
      ['dod', 'od', 'dod'],
      ['dod', 'od', 'dod', 'od'],
      ['dod', 'od', 'dod', 'hod'],
      ['dod', 'od', 'hdod', 'od'],
      ]


SCENARII = []
for od in OD:
    SCENARII.append({'tree': od})
    for params in PARAMS:
        SCENARII[-1].update(params)


@pytest.fixture(scope="function", params=SCENARII)
def root_variables(request):
    try:
        owners.addowner('test')
    except ConstError:
        pass
    ALLOWED_LEADER_PROPERTIES.add('new')
    return build_root_variables(**request.param)

from pprint import pprint as pprint2
#pprint = pprint2
def pprint(a):
    print()
    def p(b):
        ret = {}
        for i, j in b.items():
            k = i.name()
            if isinstance(j, dict):
                ret[k] = p(j)
            else:
                ret[k] = j
        return ret
    c = p(a)
                
    pprint2(c)


def walk(cfg, idx=0):
    yield cfg
    for opt in cfg.list():
        # print(' ' * idx, opt.path())
        if opt.isoptiondescription():
            yield from walk(opt, idx + 2)
        else:
            yield(opt)


def _test_option(option, without_index=False):
    # optiondescription and option
    name = option.name()
    opt = option.get()
    if opt is None:
        # it's a 'root' object
        assert name is None
        assert option.isoptiondescription()
        assert not option.isleadership()
        assert not option.isdynamic()
        assert option.description() == 'root'
        assert option.path() is None
        assert not option.has_dependency()
    else:
        assert isinstance(name, str)
        assert isinstance(opt, BaseOption)
        assert (isinstance(opt, OptionDescription) and option.isoptiondescription()) or (not isinstance(opt, OptionDescription) and not option.isoptiondescription())
        if option.isoptiondescription():
            assert ('leadership' not in name and not option.isleadership()) or ('leadership' in name and option.isleadership())
            if option.isleadership():
                assert 'leader_' in option.leader().name()
            else:
                with pytest.raises(ConfigError):
                    option.leader()
        else:
            with pytest.raises(ConfigError):
                option.leadership()
        assert option.isdynamic() == ('dynamic' in name)
        if option.isdynamic():
            identifiers = []
            for path in option.path().split('.'):
                if 'dynamicvar1' in path:
                    identifiers.append('var1')
                if 'dynamicvar2' in path:
                    identifiers.append('var2')
                if 'd1' in path:
                    identifiers.append('d1')
                if 'd2' in path:
                    identifiers.append('d2')
            assert option.identifiers() == identifiers
        assert isinstance(option.description(), str) and option.description() == name and option.description(uncalculated=True) == ''
        assert isinstance(option.path(), str) and (option.path() == name or option.path().endswith(f'.{name}'))
        if '_deps' in name:
            assert option.has_dependency(False)
            assert option.dependencies()
        else:
            assert not option.has_dependency(False)
            assert not option.dependencies()
    if option.isoptiondescription():
        assert option.type() == 'optiondescription'
    elif 'index' in name:
        assert option.type() == 'integer'
    elif 'choice' in name:
        assert option.type() == 'choice'
    else:
        assert option.type() == 'string'
    # only option
    if option.isoptiondescription():
        with pytest.raises(ConfigError):
            option.ismulti()
        with pytest.raises(ConfigError):
            option.issubmulti()
        with pytest.raises(ConfigError):
            option.isleader()
        with pytest.raises(ConfigError):
            option.isfollower()
        with pytest.raises(ConfigError):
            option.issymlinkoption()
        with pytest.raises(ConfigError):
            option.value.default()
        with pytest.raises(ConfigError):
            option.value.defaultmulti()
        with pytest.raises(ConfigError):
            option.pattern()
        with pytest.raises(ConfigError):
            option.index()
    else:
        assert 'symlink' in name and option.issymlinkoption() or 'symlink' not in name and not option.issymlinkoption()
        try:
            assert 'multi' in name and option.ismulti() or 'multi' not in name and not option.ismulti()
        except Exception as err:
            print(err)
            print(option.value.get())
            raise Exception('err')
        assert 'submulti' in name and option.issubmulti() or 'submulti' not in name and not option.issubmulti()
        if option.issymlinkoption():
            assert not option.isleader()
            assert not option.isfollower()
            with pytest.raises(ConfigError):
                option.pattern()
            assert option.index() is None
        else:
            assert 'leader' in name and option.isleader() or 'leader' not in name and not option.isleader()
            assert 'follower' in name and option.isfollower() or 'follower' not in name and not option.isfollower()
            if option.isfollower() and not without_index:
                assert option.index() in [0, 1]
            else:
                assert option.index() is None
            if option.type() == 'integer':
                assert option.pattern() == '^[0-9]+$'
            else:
                assert not option.pattern()
        default = option.value.default(uncalculated=True)
        if 'calc_default' in name:
            assert isinstance(default, Calculation) or (isinstance(default, list) and len(default) == 1 and isinstance(default[0], Calculation))
        elif 'identifiers_multi' in name:
            assert default == ['d1', 'd2']
        elif 'leader_multi' in name:
            assert default == ['l1', 'l2']
        elif 'multi' in name:
            assert default == []
        else:
            assert default is None
        if option.issubmulti():
            assert option.value.defaultmulti() == []
        elif option.ismulti():
            assert option.value.defaultmulti() is None


def _test_information(cfg, option, without_index=False):
    name = option.name()
    # list
    lst = option.information.list()
    if name is None:
        assert lst == {'cfg_key', 'doc'}
    elif 'information' in name and ('information_self' in name or 'calc_default' not in name):
        assert lst == {'doc', 'info'}
    else:
        assert lst == {'doc'}
    # get
    assert option.information.get('unknown', 'no_value') == 'no_value'
    if name is None:
        assert option.information.get('doc') == 'root'
    else:
        assert option.information.get('doc') == ''
    if 'cfg_key' in lst:
        assert option.information.get('cfg_key') == 'cfg_info'
    if 'info' in lst:
        if 'parent' in name:
            value = 'parent_value'
        else:
            value = 'value'
        if 'multi' in name:
            value = [value]
        assert option.information.get('info') == value
    # set
    if not option.isoptiondescription() and option.issymlinkoption():
        with pytest.raises(ConfigError):
            option.information.set('new', 'value')
        with pytest.raises(ConfigError):
            option.information.reset('new')
        return
    if not option.isoptiondescription() and option.isfollower() and not without_index:
        # index is not allowed
        with pytest.raises(ConfigError):
            option.information.set('new', 'value')
        with pytest.raises(ConfigError):
            option.information.reset('new')
        option.information.get('doc')
        with pytest.raises(ConfigError):
            option.information.set('new', 'value')
        option.information.list()
        with pytest.raises(ConfigError):
            option.information.remove('new')
    else:
        option.information.set('new', 'value')
        assert option.information.get('new') == 'value'
        assert option.information.list() == lst | {'new'}
        option.information.set('new', 'value2')
        assert option.information.get('new') == 'value2'
        assert option.information.list() == lst | {'new'}
        # remove
        option.information.remove('new')
        assert option.information.list() == lst
        with pytest.raises(ValueError):
            option.information.remove('doc')

# Value
def _test_value(cfg, option, unrestraint=False, without_index=False):
    #owner
    name = option.name()
    if option.isoptiondescription():
        _test_owner_optiondescription(name, option)
        _test_value_optiondescription(name, option, unrestraint)
    elif not unrestraint and 'disabled' in name:
        if not without_index or 'calc_property' not in name or 'hidden' in name:
            _test_owner_disabled(name, option, without_index)
            _test_value_disabled(name, option, without_index)
        else:
            _test_owner_without_index(option)
            _test_value_without_index(option)
    elif not unrestraint and 'hidden' in name:
        _test_owner_disabled(name, option, without_index)
        _test_value_disabled(name, option, without_index)
    elif without_index:
        _test_owner_without_index(option)
        _test_value_without_index(option)
    else:
        _test_owner(option, without_index)
        _test_value_normal(name, cfg, option, unrestraint, without_index)


def _test_owner_optiondescription(name, option):
    with pytest.raises((AttributeError, ConfigError)):
        option.owner.isdefault()
    if name is None:
        assert option.owner.get() == owners.user
        option.owner.set(owners.test)
        assert option.owner.get() == owners.test
        option.owner.set(owners.user)
        assert option.owner.get() == owners.user
    else:
        with pytest.raises(ConfigError):
            option.owner.get()
        with pytest.raises(ConfigError):
            option.owner.set(owners.test)


def _test_value_optiondescription(name, option, unrestraint):
    if not unrestraint and name and 'hidden' in name:
        with pytest.raises(PropertiesOptionError):
            option.value.get()
    else:
        assert isinstance(option.value.get(), dict)
    if name != None:
        with pytest.raises(ConfigError):
            option.value.set('value')
        with pytest.raises(ConfigError):
            option.value.reset()
        with pytest.raises(ConfigError):
            option.value.default()
        with pytest.raises(ConfigError):
            option.value.valid()
        with pytest.raises(ConfigError):
            option.value.list()
        with pytest.raises(ConfigError):
            option.value.pop(1)
        with pytest.raises(ConfigError):
            option.value.len()


def _test_owner_disabled(name, option, without_index):
    if without_index:
        errtype = ConfigError
    else:
        errtype = PropertiesOptionError
    with pytest.raises(errtype):
        option.owner.isdefault()
    with pytest.raises(errtype):
        option.owner.get()
    if 'symlink' in name:
        with pytest.raises(ConfigError):
            option.owner.set(owners.test)
    else:
        with pytest.raises(errtype):
            option.owner.set(owners.test)


def _test_owner_without_index(option):
    with pytest.raises(ConfigError):
        option.owner.isdefault()
    with pytest.raises(ConfigError):
        option.owner.get()
    with pytest.raises(ConfigError):
        option.owner.set(owners.test)


def _test_owner(option, without_index):
    if without_index:
        with pytest.raises(ConfigError):
            assert option.owner.isdefault()
        with pytest.raises(ConfigError):
            assert option.owner.get()
    else:
        assert option.owner.isdefault()
        assert option.owner.get() == owners.default
    with pytest.raises(ConfigError):
        # not availlable for symlink or without index or option has default value
        option.owner.set(owners.test)


def _test_value_disabled(name, option, without_index):
    if without_index:
        errtype = ConfigError
    else:
        errtype = PropertiesOptionError
    with pytest.raises(errtype):
        option.value.get()
    if 'symlink' in name:
        with pytest.raises(ConfigError):
            option.value.set('val')
        with pytest.raises(ConfigError):
            option.value.reset()
        with pytest.raises(ConfigError):
            option.value.valid()
    else:
        with pytest.raises(errtype):
            option.value.set('val')
        with pytest.raises(errtype):
            option.value.reset()
        with pytest.raises(errtype):
            option.value.valid()
    #if without_index:
    #    assert option.value.len() == 2
    #    if 'choice' in name:
    #        assert option.value.list() == ('val1', 'val2')
    #    else:
    #        with pytest.raises(ConfigError):
    #            option.value.list()
    #else:
    if 'leader' in name or 'follower' in name:
        with pytest.raises(PropertiesOptionError):
            option.value.len()
    else:
        with pytest.raises(ConfigError):
            option.value.len()
    if 'choice' in name and 'symlink' not in name:
        with pytest.raises(errtype):
            option.value.list()
    else:
        with pytest.raises(ConfigError):
            option.value.list()


def _test_value_without_index(option):
    with pytest.raises(ConfigError):
        option.value.get()
    with pytest.raises(ConfigError):
        option.value.set('val')
    with pytest.raises(ConfigError):
        option.value.reset()
    with pytest.raises(ConfigError):
        option.value.valid()
    with pytest.raises(ConfigError):
        option.value.list()
    assert option.value.len() == 2


def _get_value(name, option, unrestraint):
    if 'calc_default_information' in name:
        if 'calc_default_information_cfg' in name:
            value = 'cfg_info'
        elif 'parent' in name:
            value = 'parent_value'
        else:
            value = 'value'
        if 'multi' in name:
            value = [value]
    elif 'calc_default_identifier' in name:
        value = option.identifiers()[-1]
        if 'multi' in name:
            value = [value]
    elif 'calc_default_index' in name:
        value = option.index()
        if 'multi' in name:
            value = [value]
    elif 'calc_default' in name and 'calc_default_param' not in name:
        value = 'val'
        if 'multi' in name:
            value = [value]
    elif 'identifiers_multi' in name:
        value = ['d1', 'd2']
    elif 'leader_multi_deps' in name:
        value = ['l1', 'l2']
    elif 'multi' in name:
        value = []
    else:
        value = None
    return value


def _test_value_normal(name, cfg, option, unrestraint, without_index):
    #value
    value = _get_value(name, option, unrestraint)
    if without_index:
        with pytest.raises(ConfigError):
            option.value.get()
    else:
        assert option.value.get() == value
    #set
    if option.issymlinkoption() or without_index:
        with pytest.raises(ConfigError):
            option.value.set(owners.test)
        with pytest.raises(ConfigError):
            option.value.reset()
        with pytest.raises(ConfigError):
            option.value.valid()
        if without_index:
            assert option.value.len() == 2
            if 'choice' in name:
                assert option.value.list() == ('val1', 'val2')
            else:
                with pytest.raises(ConfigError):
                    option.value.list()
        else:
            with pytest.raises(ConfigError):
                option.value.len()
            with pytest.raises(ConfigError):
                option.value.list()
    else:
        if option.type() == 'string':
            new_value = 'new_value'
            new_value2 = 'new_value1'
            new_value3 = 'new_value2'
        elif option.type() == 'integer':
            new_value = 10
            new_value2 = 11
            new_value3 = 12
        elif 'choice' in name:
            new_value = 'val2'
            new_value2 = 'val1'
        if 'multi' in name:
            new_value = [new_value, new_value2]
        option.value.set(new_value)
        assert option.value.get() == new_value
        assert not option.owner.isdefault()
        assert option.owner.get() == owners.user
        #
        option.owner.set(owners.test)
        assert option.owner.get() == owners.test
        option.value.set(new_value)
        assert option.owner.get() == owners.user
        cfg.owner.set(owners.test)
        option.value.set(new_value)
        assert option.owner.get() == owners.test
        cfg.owner.set(owners.user)
        #
        if 'leader' in name:
            option.value.set(new_value + [new_value3])
            assert option.value.len() == 3
            with pytest.raises(LeadershipError):
                option.value.set(new_value)
            assert option.value.len() == 3
            option.value.pop(2)
            assert option.value.get() == new_value
        #
        assert option.value.default() == value
        #
        option.value.reset()
        assert option.value.get() == value
        assert option.owner.isdefault()
        assert option.owner.get() == owners.default
        # valid
        assert option.value.valid() is True
        # list
        if 'choice' in name:
            assert option.value.list() == ['val1', 'val2']
        else:
            with pytest.raises(ConfigError):
                option.value.list()
        if 'leader' in name or 'follower' in name:
            assert option.value.len() == 2
        else:
            with pytest.raises(ConfigError):
                option.value.len()


def _test_property(cfg, option, unrestraint=False, without_index=False):
    name = option.name()
    properties = []
    properties_only_raises = []
    properties_apply_requires = []
    properties_uncalculated = []
    if not option.isoptiondescription() and option.issymlinkoption():
        name = option.option().name()
    if name is None:
        if unrestraint:
            properties.append('cache')
            properties_apply_requires.append('cache')
            properties_uncalculated.append('cache')
        else:
            properties.extend(['disabled', 'frozen', 'validator', 'cache', 'force_store_value', 'hidden'])
            properties_apply_requires.extend(['disabled', 'frozen', 'validator', 'cache', 'force_store_value', 'hidden'])
            properties_uncalculated.extend(['disabled', 'frozen', 'validator', 'cache', 'force_store_value', 'hidden'])
    if name and 'disabled' in name:
        properties.append('disabled')
        if not unrestraint:
            properties_only_raises.append('disabled')
        if not 'calc_property' in name:
            properties_apply_requires.append('disabled')
            properties_uncalculated.append('disabled')
        else:
            properties_uncalculated.append('calculation')
    if name and ('hidden' in name or 'hidden' in option.name()):
        properties.append('hidden')
        if not unrestraint:
            properties_only_raises.append('hidden')
        properties_apply_requires.append('hidden')
        if 'self_hidden' in option.name():
            properties_uncalculated.append('hidden')
    if name and 'mandatory' in name:
        properties.append('mandatory')
        properties_apply_requires.append('mandatory')
        properties_uncalculated.append('mandatory')
    if name and 'submulti' in name:
        # it's a follower
        pass
    elif name and 'multi' in name and not option.isfollower():
        properties.append('unique')
        properties.append('empty')
        properties_apply_requires.append('unique')
        properties_apply_requires.append('empty')
        properties_uncalculated.append('unique')
        properties_uncalculated.append('empty')
    if name and 'calc_property' in name and not 'calc_property_disabled' in name and not 'property_param_disabled' in name:
        properties.append('prop')
        properties_uncalculated.append('calculation')
    
    if not without_index:
        assert option.property.get() == set(properties)
        assert option.property.get(only_raises=True) == set(properties_only_raises)
        assert option.property.get(apply_requires=False) == set(properties_apply_requires)
        option_property = option.property.get(uncalculated=True)
        if "calculation" in properties_uncalculated:
            new_option_property = set()
            for p in option_property:
                if isinstance(p, Calculation):
                    properties_uncalculated.remove('calculation')
                else:
                    new_option_property.add(p)
            assert new_option_property == set(properties_uncalculated)
        else:
            assert option_property == set(properties_uncalculated)
        #
        if (name is not None or not unrestraint) and (option.isoptiondescription() or not option.issymlinkoption()):
            assert 'new' not in option.property.get()
            option.property.add('new')
            assert 'new' in option.property.get()
            option.property.remove('new')
            assert 'new' not in option.property.get()
            if properties:
                if option.path() is not None:
                    for prop in properties:
                        with pytest.raises(ConfigError):
                            option.property.remove(prop)
                    assert option.property.get() == set(properties)
                    #
                    option.property.add('new')
                    option.property.reset()
                else:
                    for prop in properties:
                        option.property.remove(prop)
                    assert option.property.get() == set()
                    for prop in properties:
                        option.property.add(prop)
                    assert option.property.get() == set(properties)
                    #
                    option.property.reset()
                    assert option.property.get() == set()
                    for prop in properties:
                        option.property.add(prop)
                with pytest.raises(ConfigError):
                    option.property.remove('unknown')
        else:
            for prop in properties:
                with pytest.raises(ConfigError):
                    option.property.remove(prop)
            with pytest.raises(ConfigError):
                option.property.add('unknown')
            with pytest.raises(ConfigError):
                option.property.reset()
        assert option.property.get() == set(properties)
    else:
        with pytest.raises(ConfigError):
            option.property.get()
        with pytest.raises(ConfigError):
            option.property.get(only_raises=True)
        with pytest.raises(ConfigError):
            option.property.get(apply_requires=False)
        with pytest.raises(ConfigError):
            option.property.get(uncalculated=True)
        #with pytest.raises(ConfigError):
        option.property.add('new')
        #with pytest.raises(ConfigError):
        option.property.remove('new')
        #with pytest.raises(ConfigError):
        option.property.reset()
    #


def _test_permissive(cfg, option, unrestraint=False, without_index=False):
    name = option.name()
    if name is None:
        default_permissives = {'hidden'}
    else:
        default_permissives = set()
    assert option.permissive.get() == default_permissives
    if (name is not None or not unrestraint) and (option.isoptiondescription() or not option.issymlinkoption()):
        option.permissive.add('new')
        assert option.permissive.get() == default_permissives | {'new'}
        option.permissive.remove('new')
        assert option.permissive.get() == default_permissives
        #
        with pytest.raises(ConfigError):
            option.permissive.remove('unknown')
        #
        option.permissive.add('new')
        option.permissive.reset()
        assert option.permissive.get() == default_permissives
        #
        if name and not unrestraint:
            props = set()
            if 'disabled' in name:
                props.add('disabled')
            if 'hidden' in name:
                props.add('hidden')
            if props:
                for p in props:
                    if not without_index:
                        assert option.property.get(only_raises=True) == props
                        option.permissive.add(p)
                        assert option.property.get(only_raises=True) == props - set([p])
                        option.permissive.remove(p)
                        assert option.property.get(only_raises=True) == props
                    else:
                        with pytest.raises(ConfigError):
                            option.property.get(only_raises=True)
        #
    else:
        with pytest.raises(ConfigError):
            option.permissive.add('new')
        with pytest.raises(ConfigError):
            option.permissive.remove('new')
        with pytest.raises(ConfigError):
            option.permissive.reset()


def test_auto_root(root_variables):
    cfg = Config(root_variables)
    cfg.property.read_write()
    for option in walk(cfg.unrestraint):
        # we are in unrestraint mode, set option with property
        _test_option(option)
        _test_information(cfg, option)
        _test_value(cfg, option, True)
        _test_property(cfg, option, True)
        _test_permissive(cfg, option, True)
        if not option.isoptiondescription() and option.isfollower():
            follower_without_index_option = cfg.unrestraint.option(option.path())
            _test_option(follower_without_index_option, without_index=True)
            _test_information(cfg, follower_without_index_option, without_index=True)
            _test_value(cfg, follower_without_index_option, True, without_index=True)
            _test_property(cfg, follower_without_index_option, True, without_index=True)
            _test_permissive(cfg, follower_without_index_option, True, without_index=True)
        if option.path() is None:
            continue
        elif option.isoptiondescription():
            new_option = cfg.option(option.path())
        else:
            new_option = cfg.option(option.path(), option.index())
        _test_option(new_option)
        _test_information(cfg, new_option)
        _test_value(cfg, new_option)
        _test_property(cfg, new_option)
        _test_permissive(cfg, new_option)
        if not option.isoptiondescription() and option.isfollower():
            follower_without_index_option = cfg.option(option.path())
            _test_option(follower_without_index_option, without_index=True)
            _test_information(cfg, follower_without_index_option, without_index=True)
            _test_value(cfg, follower_without_index_option, without_index=True)
            _test_property(cfg, follower_without_index_option, without_index=True)
            _test_permissive(cfg, follower_without_index_option, without_index=True)
##
##
##def test_auto_root_ro(root_variables):
##    cfg = Config(root_variables)
##    cfg.information.set('cfg_key', 'cfg_info')
##    cfg.property.read_only()
##    mandatories = cfg.value.mandatory()
##    if not mandatories:
##        pprint(cfg.value.get())
#
#
#def test_auto_root_without_cache(root_variables):
#    cfg = Config(root_variables)
#    cfg.information.set('cfg_key', 'cfg_info')
#    cfg.property.read_write()
#    cfg.property.remove('cache')
#    pprint(cfg.value.get())
##
##
##def test_auto_root_without_cache_ro(root_variables):
##    cfg = Config(root_variables)
##    cfg.information.set('cfg_key', 'cfg_info')
##    cfg.property.read_only()
##    cfg.property.remove('cache')
##    mandatories = cfg.value.mandatory()
##    if not mandatories:
##        pprint(cfg.value.get())
#FIXME
#class ParamDynOption()
#leadership property, ...
#tester leader !
#FIXME dependencies doit contenir _dependencies_information

#Choice
#Choice calculé
