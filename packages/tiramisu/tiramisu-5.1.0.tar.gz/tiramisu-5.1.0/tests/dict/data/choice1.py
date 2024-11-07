
from tiramisu.option import ChoiceOption, OptionDescription

def get_description():
    """generate description for this test
    """
    option = ChoiceOption('choice', "Choice description", ("choice 1", "choice 2"))
    descr1 = OptionDescription("options", "Common configuration", [option])
    descr = OptionDescription("choice1", "Simple choice", [descr1])
    return descr
