from tiramisu import StrOption, OptionDescription, Leadership, Calculation, ParamValue, ParamOption, Params, calc_value


def get_description():
    """generate description for this test
    """
    option = StrOption('unicode', "Value 'test' must show Leadership")
    option1 = StrOption('unicode1', "Unicode leader", multi=True)
    option2 = StrOption('unicode2', "Unicode follower 1", multi=True)
    option3 = StrOption('unicode3', "Unicode follower 2", multi=True)
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(option),
                                                 'expected': ParamValue('test'),
                                                 'reverse_condition': ParamValue(True)}))
    descr1 = Leadership("unicode1", "Common configuration",
                          [option1, option2, option3], properties=(hidden_property,))
    descr = OptionDescription("options", "Common configuration", [option, descr1])
    descr = OptionDescription("unicode1_leadership_requires_all", "Leader follower with requirement", [descr])
    return descr
