from tiramisu import StrOption, OptionDescription, Calculation, ParamValue, ParamOption, Params, calc_value


def get_description():
    """generate description for this test
    """
    option1 = StrOption('unicode1', "Value 'test' must show OptionDescription")
    descr1 = OptionDescription("options", "Common configuration", [option1])
    option2 = StrOption('unicode2', "Unicode 2")
    option3 = StrOption('unicode3', "Unicode 3")
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(option1),
                                                 'expected': ParamValue('test'),
                                                 'reverse_condition': ParamValue(True)}))
    descr2 = OptionDescription("unicode1", "OptionDescription with 2 options", [option2, option3], properties=(hidden_property,))
    descr = OptionDescription("unicode1_optiondescription_requires", "OptionDesciption with requirement", [descr1, descr2])
    return descr
