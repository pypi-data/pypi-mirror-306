from tiramisu import StrOption, OptionDescription, Leadership, Calculation, ParamValue, ParamOption, Params, calc_value


def get_description():
    """generate description for this test
    """
    option = StrOption('unicode', "Values 'test' must show 'Unicode follower 3'", multi=True)
    option1 = StrOption('unicode1', "Unicode follower 1", multi=True)
    option2 = StrOption('unicode2', "Unicode follower 2", multi=True)
    disabled_property = Calculation(calc_value,
                                    Params(ParamValue('disabled'),
                                           kwargs={'condition': ParamOption(option),
                                                   'expected': ParamValue('test'),
                                                   'reverse_condition': ParamValue(True)}))
    option3 = StrOption('unicode3', "Unicode follower 3", properties=(disabled_property,), multi=True)
    descr1 = Leadership("unicode", "Common configuration 1",
                          [option, option1, option2, option3])
    descr = OptionDescription("options", "Common configuration 2", [descr1])
    descr = OptionDescription("unicode1_leadership_requires_disabled_value", "Leader followers with Unicode follower 3 disabled when Unicode follower 2 is test and modified value", [descr])
    return descr


def get_values(api, allpath=False):
    if allpath:
        root = 'unicode1_leadership_requires_disabled_value.'
    else:
        root = ''
    api.option(root + 'options.unicode.unicode').value.set([u'test', u'val2'])
    api.option(root + 'options.unicode.unicode1', 0).value.set(u'super1')
    api.option(root + 'options.unicode.unicode1', 1).value.set(u'super2')
    api.option(root + 'options.unicode.unicode2', 0).value.set(u'pas test')
    api.option(root + 'options.unicode.unicode2', 1).value.set(u'test')
    api.option(root + 'options.unicode.unicode3', 1).value.set(u'super')
