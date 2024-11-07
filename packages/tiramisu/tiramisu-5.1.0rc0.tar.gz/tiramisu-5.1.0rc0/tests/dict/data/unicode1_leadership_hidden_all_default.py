from tiramisu.option import StrOption, OptionDescription
from tiramisu import Leadership


def get_description():
    """generate description for this test
    """
    option = StrOption('unicode', "Unicode leader")
    option1 = StrOption('unicode1', "Unicode follower 1", multi=True)
    option2 = StrOption('unicode2', "Unicode follower 2", multi=True)
    option3 = StrOption('unicode3', "Unicode follower 3", multi=True)
    descr1 = Leadership("unicode1", "Common configuration",
                          [option1, option2, option3])
    descr = OptionDescription("options", "Common configuration", [option, descr1])
    descr = OptionDescription("unicode1_leadership_hidden_all_default", "FIXME...", [descr])
    return descr
