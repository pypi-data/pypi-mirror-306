from tiramisu import IPOption, PortOption, BoolOption, ChoiceOption, DomainnameOption, \
                     URLOption, NetworkOption, NetmaskOption, \
                     SymLinkOption, OptionDescription, Leadership, Config


proxy_mode = ChoiceOption('proxy_mode', 'Proxy\'s config mode', ('No proxy',
                                                                 'Manual proxy configuration',
                                                                 'Automatic proxy configuration URL'),
                          properties=('positional', 'mandatory'))
http_ip_address = IPOption('http_ip_address', 'Proxy\'s HTTP IP', properties=('mandatory',))
http_ip_short = SymLinkOption('i', http_ip_address)
http_port = PortOption('http_port', 'Proxy\'s HTTP Port', default='8080', properties=('mandatory',))
http_port_short = SymLinkOption('p', http_port)
manual_proxy = OptionDescription('manual_proxy', 'Manual proxy settings', [http_ip_address, http_ip_short, http_port, http_port_short],
                                 requires=[{'option': proxy_mode, 'expected': 'Manual proxy configuration', 'action':'disabled', 'inverse':True}])

auto_config_url = URLOption('auto_config_url','Proxy\'s auto config URL', properties=('mandatory',))
auto_config_url_short = SymLinkOption('i', auto_config_url)
automatic_proxy = OptionDescription('automatic_proxy', 'Automatic proxy setting',
                                    [auto_config_url, auto_config_url_short],
                                    requires=[{'option': proxy_mode, 'expected': 'Automatic proxy configuration URL', 'action':'disabled', 'inverse': True}])

configuration = OptionDescription('configuration', None,
                                  [manual_proxy, automatic_proxy])

no_proxy_domain = DomainnameOption('no_proxy_domain', 'Domain names for which proxy will be desactivated', multi=True)
no_proxy_network = NetworkOption('no_proxy_network', 'Network addresses', multi=True)
no_proxy_network_short = SymLinkOption('n', no_proxy_network)
no_proxy_netmask = NetmaskOption('no_proxy_netmask', 'Netmask addresses', multi=True, properties=('mandatory',))
no_proxy_network_leadership = Leadership('no_proxy_network', 'Network for which proxy will be desactivated', [no_proxy_network, no_proxy_netmask])
no_proxy = OptionDescription('no_proxy', 'Disabled proxy',
                             [no_proxy_domain, no_proxy_network_leadership],
			     requires=[{'option': proxy_mode, 'expected': 'No proxy', 'action':'disabled'}, {'option': proxy_mode, 'expected': None, 'action':'disabled'}])

dns_over_https = BoolOption('dns_over_https', 'Enable DNS over HTTPS', default=False)

root = OptionDescription('proxy', 'Proxy parameters',
                         [proxy_mode, configuration, no_proxy, dns_over_https])

def display_name(option, dyn_name):
    return "--" + option.impl_getpath()

proxy_config = Config(root, display_name=display_name)
proxy_config.property.read_write()

from tiramisu_cmdline_parser import TiramisuCmdlineParser
parser = TiramisuCmdlineParser(proxy_config)
parser.parse_args()

from pprint import pprint
pprint(proxy_config.value.dict())
