"""two unicode options
"""
from tiramisu.option import StrOption, OptionDescription

def get_description():
    """generate description for this test
    """
    option1 = StrOption('unicode1', "Unicode 1")
    option2 = StrOption('unicode2', "Unicode 2")
    descr1 = OptionDescription("options", "Common configuration", [option1, option2])
    descr = OptionDescription("unicode2", "Two unicodes", [descr1])
    return descr

