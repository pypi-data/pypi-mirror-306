from tiramisu import BoolOption, ChoiceOption, DomainnameOption, PortOption, URLOption, \
                     OptionDescription, Calculation, Params, ParamOption, ParamValue, \
                     Config, calc_value, calc_value_property_help


def protocols_settings(use: bool, value):
    if use is True:
        return value


# this option's value will determine which of the others options are frozen and which are not thanks
proxy_mode = ChoiceOption('proxy_mode',
                          'Proxy\'s config mode',
                          ('No proxy',
                           'Auto-detect proxy settings for this network',
                           'Use system proxy settings',
                           'Manual proxy configuration',
                           'Automatic proxy configuration URL'),
                          default = 'No proxy',
                          properties=('mandatory',))


http_address = DomainnameOption('http_address',
                                'Address',
                                allow_ip=True,
                                properties=('mandatory',))
http_port = PortOption('http_port',
                       'Port',
                       default='8080',
                       properties=('mandatory',))
http_proxy = OptionDescription('http_proxy',
                               'HTTP Proxy',
                               [http_address, http_port])

use_for_all_protocols = BoolOption('use_for_all_protocols',
                                   'Use HTTP IP and Port for all protocols',
                                   default=True)


# if this option is valued with 'True', set all the others IP and port values to the same as HTTP IP and port.
ssl_address = DomainnameOption('ssl_address',
                               'Address',
                               Calculation(protocols_settings,
                                           Params((ParamOption(use_for_all_protocols), ParamOption(http_address)))),
                               allow_ip=True,
                               properties=('mandatory', 'force_default_on_freeze',
                                           Calculation(calc_value,
                                                       Params(ParamValue('frozen'),
                                                              kwargs={'condition': ParamOption(use_for_all_protocols, todict=True),
                                                                      'expected': ParamValue(True)}),
                                                       calc_value_property_help)))
ssl_port = PortOption('ssl_port',
                      'Port',
                      Calculation(protocols_settings,
                                  Params((ParamOption(use_for_all_protocols), ParamOption(http_port)))),
                      properties=('mandatory', 'force_default_on_freeze',
                                  Calculation(calc_value,
                                              Params(ParamValue('frozen'),
                                                     kwargs={'condition': ParamOption(use_for_all_protocols, todict=True),
                                                             'expected': ParamValue(True)}),
                                              calc_value_property_help)))
ssl_proxy = OptionDescription('ssl_proxy',
                              'SSL Proxy',
                              [ssl_address, ssl_port],
                              properties=(Calculation(calc_value,
                                                      Params(ParamValue('hidden'),
                                                             kwargs={'condition': ParamOption(use_for_all_protocols, todict=True),
                                                                     'expected': ParamValue(True)}),
                                                      calc_value_property_help),))

ftp_address = DomainnameOption('ftp_address',
                               'Address',
                               Calculation(protocols_settings,
                                           Params((ParamOption(use_for_all_protocols), ParamOption(http_address)))),
                               allow_ip=True,
                               properties=('mandatory', 'force_default_on_freeze',
                                           Calculation(calc_value,
                                                       Params(ParamValue('frozen'),
                                                              kwargs={'condition': ParamOption(use_for_all_protocols, todict=True),
                                                                      'expected': ParamValue(True)}),
                                                       calc_value_property_help)))
ftp_port = PortOption('ftp_port',
                      'Port',
                      Calculation(protocols_settings,
                                  Params((ParamOption(use_for_all_protocols), ParamOption(http_port)))),
                      properties=('force_default_on_freeze',
                                  Calculation(calc_value,
                                              Params(ParamValue('frozen'),
                                                     kwargs={'condition': ParamOption(use_for_all_protocols, todict=True),
                                                             'expected': ParamValue(True)}),
                                              calc_value_property_help)))
ftp_proxy = OptionDescription('ftp_proxy',
                              'FTP Proxy',
                              [ftp_address, ftp_port],
                              properties=(Calculation(calc_value,
                                                      Params(ParamValue('hidden'),
                                                             kwargs={'condition': ParamOption(use_for_all_protocols, todict=True),
                                                                     'expected': ParamValue(True)}),
                                                      calc_value_property_help),))

socks_address = DomainnameOption('socks_address',
                                 'Address',
                                 Calculation(protocols_settings,
                                             Params((ParamOption(use_for_all_protocols), ParamOption(http_address)))),
                                 allow_ip=True,
                                 properties=('mandatory', 'force_default_on_freeze',
                                             Calculation(calc_value,
                                                         Params(ParamValue('frozen'),
                                                                kwargs={'condition': ParamOption(use_for_all_protocols, todict=True),
                                                                        'expected': ParamValue(True)}),
                                                         calc_value_property_help)))
socks_port = PortOption('socks_port',
                        'Port',
                        Calculation(protocols_settings,
                                    Params((ParamOption(use_for_all_protocols), ParamOption(http_port)))),
                        properties=('mandatory', 'force_default_on_freeze',
                                    Calculation(calc_value,
                                                Params(ParamValue('frozen'),
                                                       kwargs={'condition': ParamOption(use_for_all_protocols, todict=True),
                                                               'expected': ParamValue(True)}),
                                                calc_value_property_help)))
socks_version = ChoiceOption('socks_version',
                             'SOCKS host version used by proxy',
                             ('v4', 'v5'),
                             default='v5',
                             properties=('force_default_on_freeze',
                                         Calculation(calc_value,
                                                     Params(ParamValue('frozen'),
                                                            kwargs={'condition': ParamOption(use_for_all_protocols, todict=True),
                                                                    'expected': ParamValue(True)}),
                                                     calc_value_property_help)))
socks_proxy = OptionDescription('socks_proxy',
                                'Socks host proxy',
                                [socks_address, socks_port, socks_version],
                                properties=(Calculation(calc_value,
                                                        Params(ParamValue('hidden'),
                                                               kwargs={'condition': ParamOption(use_for_all_protocols, todict=True),
                                                                       'expected': ParamValue(True)}),
                                                        calc_value_property_help),))
protocols = OptionDescription('protocols',
                              'Protocols parameters',
                              [http_proxy,
                               use_for_all_protocols,
                               ssl_proxy,
                               ftp_proxy,
                               socks_proxy],
                              properties=(Calculation(calc_value,
                                                      Params(ParamValue('disabled'),
                                                             kwargs={'condition': ParamOption(proxy_mode, todict=True),
                                                                     'expected': ParamValue('Manual proxy configuration'),
                                                                     'reverse_condition': ParamValue(True)}),
                                                      calc_value_property_help),))

auto_config_url = URLOption('auto_config_url',
                            'Proxy\'s auto config URL',
                            allow_ip=True,
                            properties=('mandatory',
                                        Calculation(calc_value,
                                                    Params(ParamValue('disabled'),
                                                           kwargs={'condition': ParamOption(proxy_mode, todict=True),
                                                                   'expected': ParamValue('Automatic proxy configuration URL'),
                                                                   'reverse_condition': ParamValue(True)}),
                                                    calc_value_property_help),))

no_proxy = DomainnameOption('no_proxy',
                            'Address for which proxy will be desactivated',
                            multi=True,
                            allow_ip=True,
                            allow_cidr_network=True,
                            allow_without_dot=True,
                            allow_startswith_dot=True,
                            properties=(Calculation(calc_value,
                                                    Params(ParamValue('disabled'),
                                                           kwargs={'condition': ParamOption(proxy_mode, todict=True),
                                                                   'expected': ParamValue('No proxy')}),
                                                    calc_value_property_help),))

prompt_authentication = BoolOption('prompt_authentication',
                                   'Prompt for authentication if password is saved',
                                   default=False,
                                   properties=(Calculation(calc_value,
                                                           Params(ParamValue('disabled'),
                                                                  kwargs={'condition': ParamOption(proxy_mode, todict=True),
                                                                          'expected': ParamValue('No proxy')}),
                                                           calc_value_property_help),))
proxy_dns_socks5 = BoolOption('proxy_dns_socks5',
                              'Use Proxy DNS when using SOCKS v5',
                              default=False,
                              properties=(Calculation(calc_value,
                                                      Params(ParamValue('disabled'),
                                                             kwargs={'condition_1': ParamOption(socks_version,
                                                                                                raisepropertyerror=True),
                                                                     'expected_1': ParamValue('v4'),
                                                                     'condition_2': ParamOption(proxy_mode, todict=True),
                                                                     'expected_2': ParamValue('No proxy'),
                                                                     'condition_operator': ParamValue('OR')}),
                                                      calc_value_property_help),))
enable_dns_over_https = BoolOption('enable_dns_over_https',
                                   'Enable DNS over HTTPS',
                                   default=False)

used_dns = ChoiceOption('used_dns',
                        'Used DNS',
                        ('default', 'custom'),
                        properties=(Calculation(calc_value,
                                                Params(ParamValue('disabled'),
                                                       kwargs={'condition': ParamOption(enable_dns_over_https, todict=True),
                                                               'expected': ParamValue(False)}),
                                                calc_value_property_help),))

custom_dns_url = URLOption('custom_dns_url',
                           'Custom DNS URL',
                           properties=(Calculation(calc_value,
                                                   Params(ParamValue('disabled'),
                                                          kwargs={'condition': ParamOption(used_dns, todict=True,
                                                                                           raisepropertyerror=True),
                                                                  'expected': ParamValue('default')}),
                                                   calc_value_property_help),))
dns_over_https = OptionDescription('dns_over_https',
                                   'DNS over HTTPS',
                                   [enable_dns_over_https, used_dns, custom_dns_url])

rootod = OptionDescription('proxy',
                           'Proxy parameters',
                           [proxy_mode,
                            protocols,
                            no_proxy,
                            auto_config_url,
                            prompt_authentication,
                            proxy_dns_socks5, dns_over_https])
proxy_config = Config(rootod)
proxy_config.property.read_write()
