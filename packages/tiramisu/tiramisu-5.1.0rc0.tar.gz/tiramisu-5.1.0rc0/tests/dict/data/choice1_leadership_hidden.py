from tiramisu.option import ChoiceOption, OptionDescription
from tiramisu import Leadership
from tiramisu.setting import groups

def get_description():
    """generate description for this test
    """
    option = ChoiceOption('choice1', "Choice description leader", ("choice 1", "choice 2"), multi=True)
    option1 = ChoiceOption('choice2', "Choice description follower 1", ("choice 3", "choice 4"), multi=True)
    option2 = ChoiceOption('choice3', "Choice description follower 2 hidden", ("choice 5", "choice 6"), multi=True, properties=('hidden',))
    option3 = ChoiceOption('choice4', "Choice description follower 3", ("choice 7", "choice 8"), multi=True)
    descr1 = Leadership("choice1", "Slave 2 is hidden",
                          [option, option1, option2, option3])
    descr = OptionDescription("options", "Common configuration 2", [descr1])
    descr = OptionDescription("choice1_leadership_hidden", "Leader follower with choice, one is hidden", [descr])
    return descr
