from tiramisu.option import DomainnameOption, OptionDescription

def get_description():
    """generate description for this test
    """
    option1 = DomainnameOption('hostname1', "Domainname Description")
    option2 = DomainnameOption('hostname2', "Domainname without dot Description", allow_without_dot=True)
    option3 = DomainnameOption('hostname3', "Hostname or IP Description", type='hostname', allow_ip=True)
    option4 = DomainnameOption('hostname4', "Netbios Description", type='netbios')
    descr1 = OptionDescription("options", "Common configuration", [option1, option2, option3, option4])
    descr = OptionDescription("hostname1", "Simple hostnames", [descr1])
    return descr
