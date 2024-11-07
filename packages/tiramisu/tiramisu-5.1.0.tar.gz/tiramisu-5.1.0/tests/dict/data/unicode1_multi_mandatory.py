"""just a multi unicode option
"""
from tiramisu.option import StrOption, OptionDescription

def get_description():
    """generate description for this test
    """
    option = StrOption('unicode', "Unicode 1", multi=True, properties=('mandatory',))
    descr1 = OptionDescription("options", "Common configuration", [option])
    descr = OptionDescription("unicode1_multi_mandatory", "Mandatory multi Unicode", [descr1])
    return descr
