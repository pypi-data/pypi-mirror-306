"""just an unicode option
"""
from tiramisu.option import StrOption, OptionDescription

def get_description():
    """generate description for this test
    """
    option = StrOption('unicode', "Unicode 1")
    descr1 = OptionDescription("options", "Common configuration", [option])
    descr = OptionDescription("unicode1_mod_value", "Simple unicode with modified value", [descr1])
    return descr


def get_values(api, allpath=False):
    if allpath:
        root = 'unicode1_mod_value.'
    else:
        root = ''
    api.option(root + 'options.unicode').value.set('a')
