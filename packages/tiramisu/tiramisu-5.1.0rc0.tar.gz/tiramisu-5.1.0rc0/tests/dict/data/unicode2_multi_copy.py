"""two unicode options
"""
from tiramisu.option import StrOption, OptionDescription
from tiramisu import Params, ParamOption
from tiramisu import tiramisu_copy

def get_description():
    """generate description for this test
    """
    option1 = StrOption('unicode1', "Unicode 1", multi=True)
    option2 = StrOption('unicode2', "Unicode 2", callback=tiramisu_copy, callback_params=Params(ParamOption(option1)), multi=True)
    descr1 = OptionDescription("options", "Common configuration", [option1, option2])
    descr = OptionDescription("unicode2_multi_copy", "First multi unicode copy in second multi unicode", [descr1])
    return descr

