"""two unicode options
"""
from tiramisu.option import StrOption, OptionDescription
from tiramisu import Params, ParamOption
from tiramisu import tiramisu_copy

def get_description():
    """generate description for this test
    """
    option1 = StrOption('unicode1', "Unicode 1")
    option2 = StrOption('unicode2', "Unicode 2 (copy)", callback=tiramisu_copy, callback_params=Params(ParamOption(option1)))
    descr1 = OptionDescription("options", "Common configuration", [option1, option2])
    descr = OptionDescription("unicode2_copy", "First unicode copy in second unicode", [descr1])
    return descr

