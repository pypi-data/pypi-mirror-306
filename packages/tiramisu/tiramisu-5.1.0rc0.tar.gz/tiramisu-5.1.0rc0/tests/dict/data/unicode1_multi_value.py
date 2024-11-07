"""just a multi unicode option
"""
from tiramisu.option import StrOption, OptionDescription

def get_description():
    """generate description for this test
    """
    option = StrOption('unicode', "String 1", ['a', 'b'], multi=True)
    descr1 = OptionDescription("options", "Common configuration", [option])
    descr = OptionDescription("unicode1_multi_value", "Multi unicode with default value 'a' and 'b'", [descr1])
    return descr

