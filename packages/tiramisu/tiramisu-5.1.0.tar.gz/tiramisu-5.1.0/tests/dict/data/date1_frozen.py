from tiramisu.option import DateOption, OptionDescription

def get_description():
    """generate description for this test
    """
    option = DateOption('date', "Date description frozen", properties=('frozen',))
    descr1 = OptionDescription("options", "Common configuration", [option])
    descr = OptionDescription("date1_frozen", "Simple date", [descr1])
    return descr
