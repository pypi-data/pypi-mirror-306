
from tiramisu.option import IntOption, OptionDescription

def get_description():
    """generate description for this test
    """
    option = IntOption('integer', "integer 1", 0)
    descr1 = OptionDescription("options", "Common configuration", [option])
    descr = OptionDescription("number1_mod_value", "Number with modified value 3 and default value 0", [descr1])
    return descr


def get_values(api, allpath=False):
    if allpath:
        root = 'number1_mod_value.'
    else:
        root = ''
    api.option(root + 'options.integer').value.set(3)
