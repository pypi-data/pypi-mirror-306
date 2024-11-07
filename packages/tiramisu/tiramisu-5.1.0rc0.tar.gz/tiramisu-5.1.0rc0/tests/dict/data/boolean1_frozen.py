"""just an boolean option
"""
from tiramisu.option import BoolOption, OptionDescription

def get_description():
    """generate description for this test
    """
    option = BoolOption('boolean', "Boolean 1 frozen", properties=('frozen',))
    descr1 = OptionDescription("options", "Common configuration", [option])
    descr = OptionDescription("boolean1_frozen", "Simple boolean", [descr1])
    return descr

