from tiramisu import StrOption, OptionDescription, Leadership, Calculation, ParamValue, ParamOption, Params, calc_value

def get_description():
    """generate description for this test
    """
    option = StrOption('unicode', "Unicode leader", multi=True)
    option1 = StrOption('unicode1', "Unicode follower 1", multi=True)
    option2 = StrOption('unicode2', "Values 'test' must show 'Unicode follower 3'", multi=True)
    hidden_property = Calculation(calc_value,
                                  Params(ParamValue('hidden'),
                                         kwargs={'condition': ParamOption(option2),
                                                 'expected': ParamValue('test'),
                                                 'reverse_condition': ParamValue(True)}))
    option3 = StrOption('unicode3', "Unicode follower 3", properties=(hidden_property,), multi=True)
    descr1 = Leadership("unicode", "Common configuration 1",
                          [option, option1, option2, option3])
    descr = OptionDescription("options", "Common configuration 2", [descr1])
    descr = OptionDescription("unicode1_leadership_requires", "Leader followers with Unicode follower 3 hidden when Unicode follower 2 is test", [descr])
    return descr
