from tiramisu import StrOption, OptionDescription, Leadership, Calculation, ParamValue, ParamOption, Params, calc_value


def get_description():
    """generate description for this test
    """
    option1 = StrOption('unicode1', "Values 'test' must show 'Unicode follower 2'", multi=True)
    option2 = StrOption('unicode2', "Unicode follower 1", multi=True)
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(option1),
                                                 'expected': ParamValue('test'),
                                                 'reverse_condition': ParamValue(True)}))
    option3 = StrOption('unicode3', "Unicode follower 2", multi=True, properties=(hidden_property,))
    descr1 = Leadership("unicode1", "Common configuration",
                          [option1, option2, option3])
    descr = OptionDescription("options", "Common configuration", [descr1])
    descr = OptionDescription("unicode1_leadership_requires_follower", "Leader follower requires follower with leader", [descr])
    return descr
