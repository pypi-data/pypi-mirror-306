from tiramisu.option import StrOption, OptionDescription
from tiramisu import Leadership

def get_description():
    """generate description for this test
    """
    option = StrOption('unicode', "Unicode leader", multi=True)
    option1 = StrOption('unicode1', "Unicode follower 1", multi=True)
    option2 = StrOption('unicode2', "Unicode follower 2", multi=True)
    option3 = StrOption('unicode3', "Unicode follower 3", multi=True)
    descr1 = Leadership("unicode", "Common configuration",
                          [option, option1, option2, option3], properties=('hidden',))
    descr = OptionDescription("options", "Common configuration", [descr1])
    descr = OptionDescription("unicode1_leader_hidden_followers", "Leader follower with unicode and hidden leader", [descr])
    return descr
