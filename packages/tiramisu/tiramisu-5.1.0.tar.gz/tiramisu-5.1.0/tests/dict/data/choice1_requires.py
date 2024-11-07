from tiramisu import ChoiceOption, StrOption, OptionDescription, Calculation, ParamValue, ParamOption, Params, calc_value

def get_description():
    """generate description for this test
    """
    option1 = ChoiceOption('choice', "Choice description", ("hide", "show"), default='hide', properties=('mandatory',))
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(option1),
                                                 'expected': ParamValue('hide')}))
    option2 = StrOption('unicode2', "Unicode 2", properties=(hidden_property,))
    descr1 = OptionDescription("options", "Common configuration", [option1, option2])
    descr = OptionDescription("choice1_requires", "Choice with requirement", [descr1])
    return descr
