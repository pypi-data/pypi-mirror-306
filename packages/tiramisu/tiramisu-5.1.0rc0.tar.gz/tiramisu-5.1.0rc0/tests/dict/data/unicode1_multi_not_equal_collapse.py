from tiramisu.option import StrOption, OptionDescription

def get_description():
    """generate description for this test
    """
    option1 = StrOption('unicode1', "Unicode 1, not equal to 'a'")
    option2 = StrOption('unicode1_multi', "Multi unicode 1, not equal to 'a' or 'b'", multi=True)
    option3 = StrOption('unicode2', "Unicode 2", default='a')
    option4 = StrOption('unicode2_multi', "Multi unicode 2", multi=True, default=['a', 'b'])
    option5 = StrOption('unicode3', "Unicode 3")
    option6 = StrOption('unicode3_multi', "Multi unicode 3", multi=True)
    #option1.impl_add_consistency('not_equal', option3, option5)
    #option2.impl_add_consistency('not_equal', option4, option6)
    option3.impl_add_consistency('not_equal', option1)
    option4.impl_add_consistency('not_equal', option2)
    option5.impl_add_consistency('not_equal', option1)
    option6.impl_add_consistency('not_equal', option2)
    option5.impl_add_consistency('not_equal', option3)
    option6.impl_add_consistency('not_equal', option4)
    descr1 = OptionDescription("descr1", "Common configuration 1", [option1, option2])
    descr2 = OptionDescription("descr2", "Common configuration 2", [option3, option4])
    descr3 = OptionDescription("descr3", "Common configuration 3", [option5, option6])
    descr = OptionDescription("unicode1_multi_not_equal_collapse",
                              "Multi Unicode 1 and unicode 2 not equal with collapse",
                              [descr1, descr2, descr3])
    return descr


def get_form(allpath=False):
    key1 = 'descr1'
    if allpath:
        key1 = 'unicode1_multi_not_equal_collapse.' + key1
    key2 = 'descr2'
    if allpath:
        key2 = 'unicode1_multi_not_equal_collapse.' + key2
    key3 = 'descr3'
    if allpath:
        key3 = 'unicode1_multi_not_equal_collapse.' + key3
    return [{'key': key1,
             'collapse': True},
            {'key': key2,
             'collapse': True},
            {'key': key3,
             'collapse': True}
            ]
