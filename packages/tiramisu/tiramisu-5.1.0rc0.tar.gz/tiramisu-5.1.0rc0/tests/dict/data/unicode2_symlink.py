"""two unicode options
"""
from tiramisu.option import StrOption, OptionDescription, SymLinkOption

def get_description():
    """generate description for this test
    """
    option1 = StrOption('unicode1', "Unicode 1", 'test')
    option2 = SymLinkOption('unicode2', option1)
    descr1 = OptionDescription("options", "Common configuration", [option1, option2])
    descr = OptionDescription("unicode2_symlink", "One unicode, one symlink", [descr1])
    return descr
