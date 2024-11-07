from tiramisu.option import IPOption, OptionDescription

def get_description():
    """generate description for this test
    """
    option1 = IPOption('ip', "IP Description frozen", properties=('frozen',))
    descr1 = OptionDescription("options", "Common configuration", [option1])
    descr = OptionDescription("ip1_frozen", "Simple IP", [descr1])
    return descr
