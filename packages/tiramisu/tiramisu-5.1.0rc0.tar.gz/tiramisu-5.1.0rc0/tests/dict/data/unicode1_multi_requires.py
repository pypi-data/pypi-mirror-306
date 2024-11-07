from tiramisu import StrOption, OptionDescription, Calculation, ParamValue, ParamOption, Params, calc_value


def get_description():
    """generate description for this test
    """
    option1 = StrOption('unicode1', "Value 'test' must show Unicode 2")
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(option1),
                                                 'expected': ParamValue('test'),
                                                 'reverse_condition': ParamValue(True)}))
    option2 = StrOption('unicode2', "Unicode 2", properties=(hidden_property,), multi=True)
    descr1 = OptionDescription("options", "Common configuration", [option1, option2])
    descr = OptionDescription("unicode1_multi_requires", "Unicode multi with requirement", [descr1])
    return descr
