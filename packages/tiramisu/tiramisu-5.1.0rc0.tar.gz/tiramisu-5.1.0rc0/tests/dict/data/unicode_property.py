"""just an unicode option
"""
from tiramisu.option import StrOption, OptionDescription

def get_description():
    """generate description for this test
    """
    option = StrOption('unicode', "Expert unicode", properties=('expert',))
    descr1 = OptionDescription("options", "Common configuration", [option])
    descr = OptionDescription("unicode_property", "Hidden because expert", [descr1])
    return descr


def get_permissives():
    return frozenset(['expert'])


def get_properties():
    return frozenset(['expert'])
