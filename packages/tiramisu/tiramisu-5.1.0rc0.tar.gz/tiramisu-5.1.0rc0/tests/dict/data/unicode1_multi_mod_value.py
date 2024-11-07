"""just a multi unicode option
"""
from tiramisu.option import StrOption, OptionDescription

def get_description():
    """generate description for this test
    """
    option = StrOption('unicode', "String 1", ['a', 'b'], multi=True)
    descr1 = OptionDescription("options", "Common configuration", [option])
    descr = OptionDescription("unicode1_multi_mod_value", "Multi unicode with default value 'a' and 'b' and modified value 'c', 'd' and 'e'", [descr1])
    return descr


def get_values(api, allpath=False):
    if allpath:
        root = 'unicode1_multi_mod_value.'
    else:
        root = ''
    api.option(root + 'options.unicode').value.set(['c', 'd', 'e'])
