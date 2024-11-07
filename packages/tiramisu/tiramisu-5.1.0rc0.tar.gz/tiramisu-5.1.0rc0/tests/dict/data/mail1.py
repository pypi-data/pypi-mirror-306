
from tiramisu.option import EmailOption, OptionDescription

def get_description():
    """generate description for this test
    """
    option = EmailOption('mail', "Mail Description")
    descr1 = OptionDescription("options", "Common configuration", [option])
    descr = OptionDescription("mail1", "Simple mail", [descr1])
    return descr
