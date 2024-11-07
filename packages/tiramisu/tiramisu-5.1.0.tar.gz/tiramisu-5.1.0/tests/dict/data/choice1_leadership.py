from tiramisu.option import ChoiceOption, OptionDescription
from tiramisu import Leadership


def get_description():
    """generate description for this test
    """
    option = ChoiceOption('choice1', "Choice description leader", ("choice 1", "choice 2"), multi=True)
    option1 = ChoiceOption('choice2', "Choice description follower 1", ("choice 3", "choice 4"), multi=True)
    option2 = ChoiceOption('choice3', "Choice description follower 2", ("choice 5", "choice 6"), multi=True)
    option3 = ChoiceOption('choice4', "Choice description follower 3", ("choice 7", "choice 8"), multi=True)
    descr1 = Leadership("choice1", "Common configuration 1",
                          [option, option1, option2, option3])
    descr = OptionDescription("options", "Common configuration 2", [descr1])
    descr = OptionDescription("choice1_leadership", "Leader followers with choice", [descr])
    return descr
