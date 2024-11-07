
from tiramisu.option import IntOption, OptionDescription

def get_description():
    """generate description for this test
    """
    option = IntOption('integer', "integer 1")
    descr1 = OptionDescription("options", "Common configuration", [option])
    descr = OptionDescription("number1", "Simple number", [descr1])
    return descr
