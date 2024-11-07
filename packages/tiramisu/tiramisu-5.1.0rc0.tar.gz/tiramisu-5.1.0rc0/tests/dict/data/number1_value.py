
from tiramisu.option import IntOption, OptionDescription

def get_description():
    """generate description for this test
    """
    option = IntOption('integer', "integer 1", 0)
    descr1 = OptionDescription("options", "Common configuration", [option])
    descr = OptionDescription("number1_value", "Number with value 0", [descr1])
    return descr

