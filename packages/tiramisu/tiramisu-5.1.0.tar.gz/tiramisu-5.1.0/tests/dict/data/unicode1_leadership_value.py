from tiramisu.option import StrOption, OptionDescription
from tiramisu import Leadership


def get_description():
    """generate description for this test
    """
    option = StrOption('unicode', "Unicode leader", ['val1', 'val2'], multi=True)
    option1 = StrOption('unicode1', "Unicode follower 1", multi=True)
    option2 = StrOption('unicode2', "Unicode follower 2 with default multi", default_multi="follower2", multi=True)
    option3 = StrOption('unicode3', "Unicode follower 3", multi=True)
    descr1 = Leadership("unicode", "Common configuration 1",
                        [option, option1, option2, option3])
    descr = OptionDescription("options", "Common configuration 2", [descr1])
    descr = OptionDescription("unicode1_leadership_value", "Leader followers with unicode with default value", [descr])
    return descr


def get_values(api, allpath=False):
    if allpath:
        root = 'unicode1_leadership_value.'
    else:
        root = ''
    api.option(root + 'options.unicode.unicode').value.set([u'val3', u'val4'])
    api.option(root + 'options.unicode.unicode1', 0).value.set(u'super1')
    api.option(root + 'options.unicode.unicode1', 1).value.set(u'super2')
    api.option(root + 'options.unicode.unicode2', 0).value.set(u'pas test')
    api.option(root + 'options.unicode.unicode2', 1).value.set(u'test')
    api.option(root + 'options.unicode.unicode3', 1).value.set(u'super')
