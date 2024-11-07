from tiramisu.option import StrOption, OptionDescription
from tiramisu import Leadership


def get_description():
    """generate description for this test
    """
    option = StrOption('unicode', "Unicode leader", multi=True)
    option1 = StrOption('unicode1', "Unicode follower 1", multi=True)
    option2 = StrOption('unicode2', "Unicode follower 2 hidden", multi=True, properties=('hidden',))
    option3 = StrOption('unicode3', "Unicode follower 3", multi=True)
    descr1 = Leadership("unicode", "Common configuration",
                          [option, option1, option2, option3])
    descr = OptionDescription("options", "Common configuration", [descr1])
    descr = OptionDescription("unicode1_leadership_hidden", "Leader followers with second follower hidden", [descr])
    return descr


def get_values(api, allpath=False):
    if allpath:
        root = 'unicode1_leadership_hidden.'
    else:
        root = ''
    api.option(root + 'options.unicode.unicode').value.set([u'val1', u'val2'])
    api.option(root + 'options.unicode.unicode2', 0).value.set(u'super')
