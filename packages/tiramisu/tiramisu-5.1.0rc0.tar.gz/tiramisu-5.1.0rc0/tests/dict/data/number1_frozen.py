
from tiramisu.option import IntOption, OptionDescription

def get_description():
    """generate description for this test
    """
    option = IntOption('integer', "integer 1 frozen", properties=('frozen',))
    descr1 = OptionDescription("options", "Common configuration", [option])
    descr = OptionDescription("number1_frozen", "Simple number", [descr1])
    return descr
