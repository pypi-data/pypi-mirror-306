"""two unicode options
"""
from tiramisu.option import StrOption, OptionDescription
from tiramisu import Params, ParamOption


def return_word():
    return "word"


def get_description():
    """generate description for this test
    """
    option = StrOption('unicode1', "Unicode 1", callback=return_word)
    descr1 = OptionDescription("options", "Common configuration", [option])
    descr = OptionDescription("unicode1_simple_callback", "Calculate 'word' even if not remotable", [descr1])
    return descr

