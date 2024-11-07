from tiramisu.option import StrOption, OptionDescription

def get_description():
    """generate description for this test
    """
    option1 = StrOption('unicode1', "Unicode 1")
    option2 = StrOption('unicode2', "Unicode 2")
    option2.impl_add_consistency('not_equal', option1)
    descr1 = OptionDescription("options", "Common configuration", [option1, option2])
    descr = OptionDescription("unicode1_not_equal", "Unicode 1 and unicode 2 not equal", [descr1])
    return descr
