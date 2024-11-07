
from tiramisu.option import ChoiceOption, OptionDescription

def get_description():
    """generate description for this test
    """
    option = ChoiceOption('choice', "Choice description frozen", ("choice 1", "choice 2"), properties=('frozen',))
    descr1 = OptionDescription("options", "Common configuration", [option])
    descr = OptionDescription("choice1_frozen", "Simple choice", [descr1])
    return descr
