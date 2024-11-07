from tiramisu.option import StrOption, OptionDescription
from tiramisu import Leadership
from tiramisu.setting import groups

def get_description():
    """generate description for this test
    """
    option = StrOption('unicode', "Unicode leader", ['val1', 'val2'], multi=True)
    option1 = StrOption('unicode1', "Unicode follower 1", multi=True)
    option2 = StrOption('unicode2', "Unicode follower 2 with default multi", default_multi="follower2", multi=True)
    option3 = StrOption('unicode3', "Unicode follower 3", multi=True)
    descr1 = Leadership("unicode", "Common configuration 1",
                          [option, option1, option2, option3])
    descr = OptionDescription("options", "Common configuration 2", [descr1])
    descr = OptionDescription("unicode1_leadership_default_value", "Leader followers with unicode with default value", [descr])
    return descr
