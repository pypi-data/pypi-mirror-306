from tiramisu.option import UsernameOption, OptionDescription

def get_description():
    """generate description for this test
    """
    option = UsernameOption('username', "Username description")
    descr1 = OptionDescription("options", "Common configuration", [option])
    descr = OptionDescription("username1", "Simple username", [descr1])
    return descr
