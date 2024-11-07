"""just a multi unicode option
"""
from tiramisu.option import StrOption, OptionDescription

def get_description():
    """generate description for this test
    """
    option = StrOption('unicode', "Multi string 1", multi=True)
    descr1 = OptionDescription("options", "Common configuration", [option])
    descr = OptionDescription("unicode1_multi", "Multi unicode", [descr1])
    return descr
