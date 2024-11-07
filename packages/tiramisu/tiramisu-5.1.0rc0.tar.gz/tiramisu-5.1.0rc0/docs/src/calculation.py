from tiramisu import Config, OptionDescription, Leadership, IntOption, Params, ParamOption, ParamValue, ParamContext, ParamIndex

def a_function():
    pass
Calculation(a_function)


def a_function_with_parameters(value1, value2):
    return value1 + ' ' + value2
Calculation(a_function_with_parameters, Params(ParamValue('my value 1'), kwargs={value2: ParamValue('my value 2')}))


def a_function_with_parameters(value1, value2):
    return value1 + ' ' + value2
Calculation(a_function_with_parameters, Params((ParamValue('my value 1'), ParamValue('my value 2'))))


def a_function_with_option(option1):
    return option1
option1 = IntOption('option1', 'first option', 1)
Calculation(a_function_with_option, Params(ParamOption(option1)))


def a_function_with_option(option1):
    return option1
option1 = IntOption('option1', 'first option', 1, properties=('disabled',))
Calculation(a_function_with_option, Params(ParamOption(option1)))

def a_function_with_option(option1):
    return option1
Calculation(a_function_with_option, Params(ParamOption(option1, raisepropertyerror=True)))

def a_function_with_option(option1=None):
    return option1
Calculation(a_function_with_option, Params(ParamOption(option1, notraisepropertyerror=True)))

def a_function_with_dict_option(option1):
    return "the option {} has value {}".format(option1['name'], option1['value'])
Calculation(a_function_with_option, Params(ParamOption(todict=True)))


def a_function_with_context(context):
    pass
Calculation(a_function_with_context, Params(ParamContext()))

def a_function_multi(option1):
    return option1
option1 = IntOption('option1', 'option1', [1], multi=True)
Calculation(a_function, Params(ParamOption(option1)))  

def a_function_leader(option): 
    return option 
leader = IntOption('leader', 'leader', [1], multi=True)
follower1 = IntOption('follower1', 'follower1', default_multi=2, multi=True)
follower2 = IntOption('follower2', 'follower2', default_multi=3, multi=True)
leadership = Leadership('leadership', 'leadership', [leader, follower1, follower2])
Calculation(a_function_leader, Params(ParamOption(leader)))   

def a_function_follower(follower):
    return follower
leader = IntOption('leader', 'leader', [1], multi=True)
follower1 = IntOption('follower1', 'follower1', default_multi=2, multi=True)
follower2 = IntOption('follower2', 'follower2', default_multi=3, multi=True)
leadership = Leadership('leadership', 'leadership', [leader, follower1, follower2])
Calculation(a_function_follower, Params(ParamOption(follower1)))

def a_function_index(index):
    return index
leader = IntOption('leader', 'leader', [1], multi=True)
follower1 = IntOption('follower1', 'follower1', default_multi=2, multi=True)
follower2 = IntOption('follower2', 'follower2', default_multi=3, multi=True)
leadership = Leadership('leadership', 'leadership', [leader, follower1, follower2])
Calculation(a_function_index, Params(ParamIndex()))
