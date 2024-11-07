"""just a multi unicode option
"""
from tiramisu.option import StrOption, OptionDescription

def get_description():
    """generate description for this test
    """
    option = StrOption('unicode', "Unicode 1", properties=('mandatory',))
    descr1 = OptionDescription("options", "Common configuration", [option])
    descr = OptionDescription("unicode1_mandatory", "Mandatory unicode", [descr1])
    return descr
