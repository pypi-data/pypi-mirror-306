"""just an unicode option
"""
from tiramisu.option import StrOption, OptionDescription

def get_description():
    """generate description for this test
    """
    option = StrOption('unicode', "Unicode 1", properties=('hidden',))
    descr1 = OptionDescription("options", "Common configuration", [option])
    descr = OptionDescription("unicode_hidden", "Hidden unicode", [descr1])
    return descr
