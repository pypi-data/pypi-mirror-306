
from tiramisu.option import ChoiceOption, OptionDescription

def get_description():
    """generate description for this test
    """
    option = ChoiceOption('choice', "Choice description", ("choice 1", "choice 2"))
    descr1 = OptionDescription("options", "Common configuration", [option])
    descr = OptionDescription("choice1_rename", "Rename displayed value", [descr1])
    return descr


def get_form(allpath=False):
    key = 'options.choice'
    if allpath:
        key = 'choice1_rename.' + key
    return [{'key': key,
             'displayed': {'choice 1': 'renamed 1',
                           'choice 2': 'renamed 2'}
            }]
