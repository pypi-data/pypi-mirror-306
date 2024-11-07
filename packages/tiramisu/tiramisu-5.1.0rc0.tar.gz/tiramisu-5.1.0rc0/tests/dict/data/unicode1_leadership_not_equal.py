from tiramisu.option import StrOption, OptionDescription
from tiramisu import Leadership


def get_description():
    """generate description for this test
    """
    option = StrOption('unicode', "Unicode leader", multi=True)
    option1 = StrOption('unicode1', "Unicode follower 1", multi=True)
    option2 = StrOption('unicode2', "Unicode follower 2 not equal", multi=True)
    option3 = StrOption('unicode3', "Unicode follower 3 not equal", multi=True)
    option2.impl_add_consistency('not_equal', option3)
    descr1 = Leadership("unicode", "Common configuration 1",
                          [option, option1, option2, option3])
    descr = OptionDescription("options", "Common configuration 2", [descr1])
    descr = OptionDescription("unicode1_leadership_not_equal", "Leader followers with follower not equal", [descr])
    return descr
