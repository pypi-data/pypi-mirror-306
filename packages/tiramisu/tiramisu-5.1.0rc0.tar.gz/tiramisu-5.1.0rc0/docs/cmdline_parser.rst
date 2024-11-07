.. .. default-role:: code
.. 
.. ==========================
.. Tiramisu-cmdline-parser
.. ==========================
.. 
.. 
.. This tutorial is intended to be a gentle introduction to **Tiramisu
.. command-line parser**, a command-line parsing module that comes included with
.. the **Tiramisu**'s library.
.. 
.. .. note:: There are a lot of other modules that fulfill the same task,
..           namely getopt (an equivalent for getopt() from the C language) and
..           argparse, from the python standard library.
.. 
..           `tiramisu-cmdline-parser` enables us to *validate* the command line,
..           wich is a quite different scope -- much more powerfull. It is a
..           superset of the argparse_ module
.. 
.. .. _argparse: https://docs.python.org/3/howto/argparse.html
.. 
.. What is Tiramisu-cmdline-parser ?
.. ==================================
.. 
.. Tiramisu-cmdline-parser is a free project that turns Tiramisu's Config into a command line interface.
.. 
.. It automatically generates arguments, help and usage messages. Tiramisu (or
.. Tiramisu-API) validates all arguments provided by the command line's user.
.. 
.. Tiramisu-cmdline-parser uses the well known argparse_ module and adds
.. functionnalities upon it.
.. 
.. 
.. Installation
.. ==============
.. 
.. The best way is to use the python pip_ installer
.. 
.. .. _pip: https://pip.pypa.io/en/stable/installing/
.. 
.. And then type:
.. 
.. .. code-block:: bash
.. 
..     pip install tiramisu-cmdline-parser
.. 
.. Build a Tiramisu-cmdline-parser
.. =================================
.. 
.. Let’s show the sort of functionality that we are going to explore in this
.. introductory tutorial.
.. 
.. We are going to start with a simple example, like making a proxy's
.. configuration script.
.. 
.. First we are going to build the corresponding `Tiramisu` config object:
.. 
.. .. literalinclude:: src/proxy.py
..    :lines: 1-44
..    :linenos:
..    :name: Proxy1
.. 
.. Then we invopque the command line parsing library by creating a commandline
.. parser, and we give the configuration's object to it:
.. 
.. .. literalinclude:: src/proxy.py
..    :lines: 46-48
..    :linenos:
..    :name: Proxy2
.. 
.. Finally pretty printing the configuration:
.. 
.. .. literalinclude:: src/proxy.py
..    :lines: 50-51
..    :linenos:
..    :name: Proxy3
.. 
.. Let's display the help:
.. 
.. .. code-block:: bash
.. 
..     $ python3 src/proxy.py -h
..     usage: proxy.py [-h] [--dns_over_https] [--no-dns_over_https]
..                     {No proxy,Manual proxy configuration,Automatic proxy
..                     configuration URL}
.. 
..     positional arguments:
..       {No proxy,Manual proxy configuration,Automatic proxy configuration URL}
..                             Proxy's config mode
.. 
..     optional arguments:
..       -h, --help            show this help message and exit
..       --dns_over_https      Enable DNS over HTTPS
..       --no-dns_over_https
.. 
.. Positional argument
.. ======================
.. 
.. First of all, we have to set the positional argument :option:`proxy_mode`.
.. 
.. .. option:: proxy_mode
.. 
..     As it's a `ChoiceOption`, you only have three choices:
.. 
..     - No proxy
..     - Manual proxy configuration
..     - Automatic proxy configuration URL
.. 
.. Set proxy_mode to `No proxy`:
.. 
.. .. code-block:: bash
.. 
..     $ python3 src/proxy.py "No proxy"
..     {'dns_over_https': False,
..      'proxy_mode': 'No proxy'}
.. 
.. Requirements
.. ================
.. 
.. Disabled options are not visible as arguments in the command line.
.. Those parameters appears or disappears following the context:
.. 
.. .. code-block:: bash
.. 
..     $ python3 src/proxy.py "No proxy" -h
..     usage: proxy.py "No proxy" [-h] [--dns_over_https] [--no-dns_over_https]
..                                {No proxy,Manual proxy configuration,Automatic
..                                proxy configuration URL}
.. 
..     positional arguments:
..       {No proxy,Manual proxy configuration,Automatic proxy configuration URL}
..                             Proxy's config mode
.. 
..     optional arguments:
..       -h, --help            show this help message and exit
..       --dns_over_https      Enable DNS over HTTPS
..       --no-dns_over_https
.. 
.. If proxy_mode is set to "Automatic proxy configuration URL", some new options are visible:
.. 
.. .. code-block:: bash
.. 
..     $ python3 src/proxy.py "Automatic proxy configuration URL" -h
..     usage: proxy.py "Automatic proxy configuration URL" [-h] -i AUTO_CONFIG_URL
..                                                         [--no_proxy.no_proxy_network.no_proxy_network [NO_PROXY_NETWORK [NO_PROXY_NETWORK ...]]]
..                                                         [--no_proxy.no_proxy_network.pop-no_proxy_network INDEX]
..                                                         --no_proxy.no_proxy_network.no_proxy_netmask
..                                                         INDEX NO_PROXY_NETMASK
..                                                         [--no_proxy.no_proxy_domain [NO_PROXY_DOMAIN [NO_PROXY_DOMAIN ...]]]
..                                                         [--dns_over_https]
..                                                         [--no-dns_over_https]
..                                                         {No proxy,Manual proxy
..                                                         configuration,Automatic
..                                                         proxy configuration URL}
.. 
..     positional arguments:
..       {No proxy,Manual proxy configuration,Automatic proxy configuration URL}
..                             Proxy's config mode
.. 
..     optional arguments:
..       -h, --help            show this help message and exit
..       --dns_over_https      Enable DNS over HTTPS
..       --no-dns_over_https
.. 
..     configuration.automatic_proxy:
..       Automatic proxy setting
.. 
..       -i AUTO_CONFIG_URL, --configuration.automatic_proxy.auto_config_url AUTO_CONFIG_URL
..                             Proxy's auto config URL
.. 
..     no_proxy:
..       Disabled proxy
.. 
..       --no_proxy.no_proxy_domain [NO_PROXY_DOMAIN [NO_PROXY_DOMAIN ...]]
..                             Domain names for which proxy will be desactivated
.. 
..     no_proxy.no_proxy_network:
..       Network for which proxy will be desactivated
.. 
..       --no_proxy.no_proxy_network.no_proxy_network [NO_PROXY_NETWORK [NO_PROXY_NETWORK ...]]
..                             Network addresses
..       --no_proxy.no_proxy_network.pop-no_proxy_network INDEX
..       --no_proxy.no_proxy_network.no_proxy_netmask INDEX NO_PROXY_NETMASK
..                             Netmask addresses
.. 
.. Arguments
.. ===========
.. 
.. Each option creates an argument. To change the value of this option, just launch the application with the appropriate argument:
.. 
.. .. code-block:: bash
.. 
..     $ python3 src/proxy.py "Manual proxy configuration" \
..                            --configuration.manual_proxy.http_ip_address 192.168.1.1
..     {'configuration.manual_proxy.http_ip_address': '192.168.1.1',
..      'configuration.manual_proxy.http_port': '8080',
..      'configuration.manual_proxy.i': '192.168.1.1',
..      'configuration.manual_proxy.p': '8080',
..      'dns_over_https': False,
..      'no_proxy.no_proxy_domain': [],
..      'no_proxy.no_proxy_network.no_proxy_netmask': [],
..      'no_proxy.no_proxy_network.no_proxy_network': [],
..      'proxy_mode': 'Manual proxy configuration'}
.. 
.. Fullpath argument or named argument
.. =====================================
.. 
.. By default, arguments are build with fullpath of option.
.. The `option http_ip_address` is in `manual_proxy` optiondescription, which is also in configuration optiondescription.
.. So the argument is :option:`--configuration.manual_proxy.http_ip_address`:
.. 
.. .. code-block:: bash
.. 
..     $ python3 src/proxy.py "Manual proxy configuration" \
..                            --configuration.manual_proxy.http_ip_address 192.168.1.1
..     {'configuration.manual_proxy.http_ip_address': '192.168.1.1',
..      'configuration.manual_proxy.http_port': '8080',
..      'configuration.manual_proxy.i': '192.168.1.1',
..      'configuration.manual_proxy.p': '8080',
..      'dns_over_https': False,
..      'no_proxy.no_proxy_domain': [],
..      'no_proxy.no_proxy_network.no_proxy_netmask': [],
..      'no_proxy.no_proxy_network.no_proxy_network': [],
..      'proxy_mode': 'Manual proxy configuration'}
.. 
.. If we set fullpath to `False`:
.. 
.. .. code-block:: python
.. 
..     parser = TiramisuCmdlineParser(proxy_config, fullpath=False)
.. 
.. Arguments are build with the name of the option.
.. The option :option:`http_ip_address` is now :option`--http_ip_address`:
.. 
.. .. code-block:: bash
.. 
..     $ python3 src/proxy.py "Manual proxy configuration" \
..                            --http_ip_address 192.168.1.1
..     {'configuration.manual_proxy.http_ip_address': '192.168.1.1',
..      'configuration.manual_proxy.http_port': '8080',
..      'configuration.manual_proxy.i': '192.168.1.1',
..      'configuration.manual_proxy.p': '8080',
..      'dns_over_https': False,
..      'no_proxy.no_proxy_domain': [],
..      'no_proxy.no_proxy_network.no_proxy_netmask': [],
..      'no_proxy.no_proxy_network.no_proxy_network': [],
..      'proxy_mode': 'Manual proxy configuration'}
.. 
.. Short argument
.. ===============
.. 
.. To have short argument, you just have to make `SymLinkOption` to this option:
.. 
.. .. literalinclude:: src/proxy.py
..    :lines: 10-11
..    :linenos:
..    :name: Proxy4
.. 
.. Now argument `-i` or `--configuration.manual_proxy.http_ip_address` can be used alternatively:
.. 
.. .. code-block:: bash
.. 
..     $ python3 src/proxy.py "Manual proxy configuration" \
..                            --configuration.manual_proxy.http_ip_address 192.168.1.1
..     {'configuration.manual_proxy.http_ip_address': '192.168.1.1',
..      'configuration.manual_proxy.http_port': '8080',
..      'configuration.manual_proxy.i': '192.168.1.1',
..      'configuration.manual_proxy.p': '8080',
..      'dns_over_https': False,
..      'no_proxy.no_proxy_domain': [],
..      'no_proxy.no_proxy_network.no_proxy_netmask': [],
..      'no_proxy.no_proxy_network.no_proxy_network': [],
..      'proxy_mode': 'Manual proxy configuration'}
.. 
.. 
..     $ python3 src/proxy.py "Manual proxy configuration" \
..                            -i 192.168.1.1
..     {'configuration.manual_proxy.http_ip_address': '192.168.1.1',
..      'configuration.manual_proxy.http_port': '8080',
..      'configuration.manual_proxy.i': '192.168.1.1',
..      'configuration.manual_proxy.p': '8080',
..      'dns_over_https': False,
..      'no_proxy.no_proxy_domain': [],
..      'no_proxy.no_proxy_network.no_proxy_netmask': [],
..      'no_proxy.no_proxy_network.no_proxy_network': [],
..      'proxy_mode': 'Manual proxy configuration'}
.. 
.. Be carefull, short argument have to be uniqe in the whole configuration.
.. 
.. Here `-i` argument is define a second time in same Config:
.. 
.. .. literalinclude:: src/proxy.py
..    :lines: 17-18
..    :linenos:
..    :name: Proxy5
.. 
.. But `http_ip_address` and `auto_config_url` are not accessible together:
.. 
.. - `http_ip_address` is visible only if `proxy_mode` is "Manual proxy configuration"
.. - `auto_config_url` is only visible when `proxy_mode` is "Automatic proxy configuration URL"
.. 
.. Boolean argument
.. ===================
.. 
.. Boolean option creates two arguments:
.. 
.. - --<boolean_name>: it activates (set to True) the option
.. - --no-<boolean_name>: it deactivates (set to False) the option
.. 
.. .. code-block:: bash
.. 
..     $ python3 src/proxy.py "No proxy" \
..                            --dns_over_https
..     {'dns_over_https': True,
..      'proxy_mode': 'No proxy'}
.. 
..     $ python3 src/proxy.py "No proxy" \
..                            --no-dns_over_https
..     {'dns_over_https': False,
..      'proxy_mode': 'No proxy'}
.. 
.. Multi
.. =========
.. 
.. Some values are multi. So we can set several value for this option.
.. 
.. For example, we can set serveral domain (cadoles.com and gnu.org) to "Domain names for which proxy will be desactivated" option:
.. 
.. .. code-block:: bash
.. 
..     $ python3 src/proxy.py "Automatic proxy configuration URL" \
..                            --configuration.automatic_proxy.auto_config_url http://proxy.cadoles.com/proxy.pac \
..                            --no_proxy.no_proxy_domain cadoles.com gnu.org
..     {'configuration.automatic_proxy.auto_config_url': 'http://proxy.cadoles.com/proxy.pac',
..      'configuration.automatic_proxy.i': 'http://proxy.cadoles.com/proxy.pac',
..      'dns_over_https': False,
..      'no_proxy.no_proxy_domain': ['cadoles.com', 'gnu.org'],
..      'no_proxy.no_proxy_network.no_proxy_netmask': [],
..      'no_proxy.no_proxy_network.no_proxy_network': [],
..      'proxy_mode': 'Automatic proxy configuration URL'}
.. 
.. Leadership
.. ============
.. 
.. Leadership option are also supported. The leader option is a standard multi option.
.. But follower option are not view as a multi option. Follower value are separate and we need to set index to set a follower option.
.. 
.. If we want to had two "Network for which proxy will be desactivated":
.. 
.. - 192.168.1.1/255.255.255.255
.. - 192.168.0.0/255.255.255.0
.. 
.. We have to do:
.. 
.. .. code-block:: bash
.. 
..     $ python3 src/proxy.py "Automatic proxy configuration URL" \
..                            --configuration.automatic_proxy.auto_config_url http://proxy.cadoles.com/proxy.pac \
..                            --no_proxy.no_proxy_network.no_proxy_network 192.168.1.1 192.168.0.0 \
..                            --no_proxy.no_proxy_network.no_proxy_netmask 0 255.255.255.255 \
..                            --no_proxy.no_proxy_network.no_proxy_netmask 1 255.255.255.0
..     {'configuration.automatic_proxy.auto_config_url': 'http://proxy.cadoles.com/proxy.pac',
..      'configuration.automatic_proxy.i': 'http://proxy.cadoles.com/proxy.pac',
..      'dns_over_https': False,
..      'no_proxy.no_proxy_domain': [],
..      'no_proxy.no_proxy_network.no_proxy_netmask': ['255.255.255.255',
..                                                     '255.255.255.0'],
..      'no_proxy.no_proxy_network.no_proxy_network': ['192.168.1.1', '192.168.0.0'],
..      'proxy_mode': 'Automatic proxy configuration URL'}
.. 
.. We cannot reduce leader lenght:
.. 
.. .. code-block:: bash
.. 
..     $ python3 src/proxy.py "Automatic proxy configuration URL" \
..                            --configuration.automatic_proxy.auto_config_url http://proxy.cadoles.com/proxy.pac \
..                            --no_proxy.no_proxy_network.no_proxy_network 192.168.1.1 192.168.0.0 \
..                            --no_proxy.no_proxy_network.no_proxy_netmask 0 255.255.255.255 \
..                            --no_proxy.no_proxy_network.no_proxy_netmask 1 255.255.255.0 \
..                            --no_proxy.no_proxy_network.no_proxy_network 192.168.1.1
..     usage: proxy.py -i "http://proxy.cadoles.com/proxy.pac" --no_proxy.no_proxy_network.no_proxy_network "192.168.1.1" "192.168.0.0" "Automatic proxy configuration URL"
..            [-h] -i AUTO_CONFIG_URL
..            [--no_proxy.no_proxy_network.no_proxy_network [NO_PROXY_NETWORK [NO_PROXY_NETWORK ...]]]
..            [--no_proxy.no_proxy_network.pop-no_proxy_network INDEX]
..            --no_proxy.no_proxy_network.no_proxy_netmask INDEX NO_PROXY_NETMASK
..            [--no_proxy.no_proxy_domain [NO_PROXY_DOMAIN [NO_PROXY_DOMAIN ...]]]
..            [--dns_over_https] [--no-dns_over_https]
..            {No proxy,Manual proxy configuration,Automatic proxy configuration URL}
..     proxy.py: error: cannot reduce length of the leader "--no_proxy.no_proxy_network.no_proxy_network"
.. 
.. So an argument --pop-<leader> is automatically created. You need to specified index as parameter:
.. 
.. .. code-block:: bash
.. 
..     $ python3 src/proxy.py "Automatic proxy configuration URL" \
..                            --configuration.automatic_proxy.auto_config_url http://proxy.cadoles.com/proxy.pac \
..                            --no_proxy.no_proxy_network.no_proxy_network 192.168.1.1 192.168.0.0 \
..                            --no_proxy.no_proxy_network.no_proxy_netmask 0 255.255.255.255 \
..                            --no_proxy.no_proxy_network.pop-no_proxy_network 1
..     {'configuration.automatic_proxy.auto_config_url': 'http://proxy.cadoles.com/proxy.pac',
..      'configuration.automatic_proxy.i': 'http://proxy.cadoles.com/proxy.pac',
..      'dns_over_https': False,
..      'no_proxy.no_proxy_domain': [],
..      'no_proxy.no_proxy_network.no_proxy_netmask': ['255.255.255.255'],
..      'no_proxy.no_proxy_network.no_proxy_network': ['192.168.1.1'],
..      'proxy_mode': 'Automatic proxy configuration URL'}
.. 
.. Validation
.. ===============
.. 
.. All arguments are validated successively by argparser and Tiramisu:
.. 
.. .. code-block:: bash
.. 
..     $ python3 src/proxy.py "Automatic proxy configuration URL" \
..                            --configuration.automatic_proxy.auto_config_url cadoles.com
..     usage: proxy.py "Automatic proxy configuration URL" [-h] -i AUTO_CONFIG_URL
..                                                         [--no_proxy.no_proxy_network.no_proxy_network [NO_PROXY_NETWORK [NO_PROXY_NETWORK ...]]]
..                                                         [--no_proxy.no_proxy_network.pop-no_proxy_network INDEX]
..                                                         --no_proxy.no_proxy_network.no_proxy_netmask
..                                                         INDEX NO_PROXY_NETMASK
..                                                         [--no_proxy.no_proxy_domain [NO_PROXY_DOMAIN [NO_PROXY_DOMAIN ...]]]
..                                                         [--dns_over_https]
..                                                         [--no-dns_over_https]
..                                                         {No proxy,Manual proxy
..                                                         configuration,Automatic
..                                                         proxy configuration URL}
..     proxy.py: error: "cadoles.com" is an invalid URL for "Proxy’s auto config URL", must start with http:// or https://
.. 
.. In error message, we have the option description ("Proxy's auto config URL") by default.
.. 
.. That why we redefined display_name function:
.. 
.. .. literalinclude:: src/proxy.py
..    :lines: 40-43
..    :linenos:
..    :name: Proxy6
.. 
.. Now we have --<path> as description:
.. 
.. .. code-block:: bash
.. 
..     $ python3 src/proxy.py "Automatic proxy configuration URL" \
..                            --configuration.automatic_proxy.auto_config_url cadoles.com
..     usage: proxy.py "Automatic proxy configuration URL" [-h] -i AUTO_CONFIG_URL
..                                                         [--no_proxy.no_proxy_network.no_proxy_network [NO_PROXY_NETWORK [NO_PROXY_NETWORK ...]]]
..                                                         [--no_proxy.no_proxy_network.pop-no_proxy_network INDEX]
..                                                         --no_proxy.no_proxy_network.no_proxy_netmask
..                                                         INDEX NO_PROXY_NETMASK
..                                                         [--no_proxy.no_proxy_domain [NO_PROXY_DOMAIN [NO_PROXY_DOMAIN ...]]]
..                                                         [--dns_over_https]
..                                                         [--no-dns_over_https]
..                                                         {No proxy,Manual proxy
..                                                         configuration,Automatic
..                                                         proxy configuration URL}
..     proxy.py: error: "cadoles.com" is an invalid URL for "--configuration.automatic_proxy.auto_config_url", must start with http:// or https://
.. 
.. Mandatory
.. =============
.. 
.. Obviously the mandatory options are checked.
.. 
.. The positional argument is mandatory, so if we don't set it, an error occured:
.. 
.. .. code-block:: bash
.. 
..     $ python3 src/proxy.py
..     usage: proxy.py [-h] [--dns_over_https] [--no-dns_over_https]
..                     {No proxy,Manual proxy configuration,Automatic proxy
..                     configuration URL}
..     proxy.py: error: the following arguments are required: proxy_mode
.. 
.. Others arguments are also check:
.. 
.. .. code-block:: bash
.. 
..     $ python3 src/proxy.py "Automatic proxy configuration URL"
..     usage: proxy.py "Automatic proxy configuration URL" [-h] -i AUTO_CONFIG_URL
..                                                         [--no_proxy.no_proxy_network.no_proxy_network [NO_PROXY_NETWORK [NO_PROXY_NETWORK ...]]]
..                                                         [--no_proxy.no_proxy_network.pop-no_proxy_network INDEX]
..                                                         --no_proxy.no_proxy_network.no_proxy_netmask
..                                                         INDEX NO_PROXY_NETMASK
..                                                         [--no_proxy.no_proxy_domain [NO_PROXY_DOMAIN [NO_PROXY_DOMAIN ...]]]
..                                                         [--dns_over_https]
..                                                         [--no-dns_over_https]
..                                                         {No proxy,Manual proxy
..                                                         configuration,Automatic
..                                                         proxy configuration URL}
..     proxy.py: error: the following arguments are required: --configuration.automatic_proxy.auto_config_url
.. 
.. Persistence configuration and mandatories validation
.. ======================================================
.. 
.. First of all, activate persistence configuration and remove mandatory validation:
.. 
.. .. literalinclude:: src/proxy_persistent.py
..    :lines: 43-46
..    :linenos:
..    :name: Proxy7
.. 
.. We can disabled mandatory validation in parse_args function.
.. 
.. .. literalinclude:: src/proxy_persistent.py
..    :lines: 51
..    :linenos:
..    :name: Proxy8
.. 
.. In this case, we can store incomplete value:
.. 
.. .. code-block:: bash
.. 
..     $ python3 src/proxy_persistent.py 'Manual proxy configuration'
..     {'configuration.manual_proxy.http_ip_address': None,
..      'configuration.manual_proxy.http_port': '8080',
..      'configuration.manual_proxy.i': None,
..      'configuration.manual_proxy.p': '8080',
..      'dns_over_https': False,
..      'no_proxy.no_proxy_domain': [],
..      'no_proxy.no_proxy_network.no_proxy_netmask': [],
..      'no_proxy.no_proxy_network.no_proxy_network': [],
..      'proxy_mode': 'Manual proxy configuration'}
.. 
.. We can complete configuration after:
.. 
.. .. code-block:: bash
.. 
..     $ python3 src/proxy_persistent.py -i 192.168.1.1
..     {'configuration.manual_proxy.http_ip_address': '192.168.1.1',
..      'configuration.manual_proxy.http_port': '8080',
..      'configuration.manual_proxy.i': '192.168.1.1',
..      'configuration.manual_proxy.p': '8080',
..      'dns_over_https': False,
..      'no_proxy.no_proxy_domain': [],
..      'no_proxy.no_proxy_network.no_proxy_netmask': [],
..      'no_proxy.no_proxy_network.no_proxy_network': [],
..      'proxy_mode': 'Manual proxy configuration'}
.. 
.. When configuration is already set, help command, display already set options is usage ligne.
.. 
.. .. code-block:: bash
.. 
..     $ python3 src/proxy_persistent.py -h
..     usage: proxy_persistent.py -i "192.168.1.1" "Manual proxy configuration"
..            [..]
.. 
.. Description and epilog
.. ============================
.. 
.. As argparser, description and epilog message can be added to the generated help:
.. 
.. .. code-block:: python
.. 
..     parser = TiramisuCmdlineParser(proxy_config, description='New description!', epilog='New epilog!')
.. 
.. .. code-block:: bash
.. 
..     $ python3 src/proxy.py -h
..     usage: proxy.py [-h] [--dns_over_https] [--no-dns_over_https]
..                     {No proxy,Manual proxy configuration,Automatic proxy
..                     configuration URL}
.. 
..     New description!
.. 
..     positional arguments:
..       {No proxy,Manual proxy configuration,Automatic proxy configuration URL}
..                             Proxy's config mode
.. 
..     optional arguments:
..       -h, --help            show this help message and exit
..       --dns_over_https      Enable DNS over HTTPS
..       --no-dns_over_https
.. 
..     New epilog!
.. 
.. 
.. By default, TiramisuCmdlineParser objects line-wrap the description and epilog texts in command-line help messages.
.. 
.. If there are line breaks in description or epilog, it automatically replace by a space. You need to change formatter class:
.. 
.. .. code-block:: python
.. 
..     from argparse import RawDescriptionHelpFormatter
..     parser = TiramisuCmdlineParser(proxy_config, description='New description!\nLine breaks', epilog='New epilog!\nLine breaks', formatter_class=RawDescriptionHelpFormatter)
.. 
.. .. code-block:: bash
.. 
..     $ python3 src/proxy.py -h
..     usage: proxy.py [-h] [--dns_over_https] [--no-dns_over_https]
..                     {No proxy,Manual proxy configuration,Automatic proxy
..                     configuration URL}
.. 
..     New description!
..     Line breaks
.. 
..     positional arguments:
..       {No proxy,Manual proxy configuration,Automatic proxy configuration URL}
..                             Proxy's config mode
.. 
..     optional arguments:
..       -h, --help            show this help message and exit
..       --dns_over_https      Enable DNS over HTTPS
..       --no-dns_over_https
.. 
..     New epilog!
..     Line breaks
.. 
.. Hide empty optiondescription
.. ===============================
.. 
.. An empty optiondescription, is an optiondescription without any option (could have others optiondescriptions).
.. 
.. For example, configuration is an empty optiondescription:
.. 
.. .. literalinclude:: src/proxy.py
..    :lines: 23-24
..    :linenos:
..    :name: Proxy9
.. 
.. This optiondescription doesn't appears in help:
.. 
.. .. code-block:: bash
.. 
..     $ python3 src/proxy.py "No proxy" -h
..     usage: proxy.py "No proxy" [-h] [--dns_over_https] [--no-dns_over_https]
..                                {No proxy,Manual proxy configuration,Automatic
..                                proxy configuration URL}
.. 
..     positional arguments:
..       {No proxy,Manual proxy configuration,Automatic proxy configuration URL}
..                             Proxy's config mode
.. 
..     optional arguments:
..       -h, --help            show this help message and exit
..       --dns_over_https      Enable DNS over HTTPS
..       --no-dns_over_https
.. 
.. 
.. 
.. This behavior is, in fact, due to two conditions:
.. 
.. - there is no option
.. - there is no description (None)
.. 
.. If we add description:
.. 
.. .. code-block:: python
.. 
..     configuration = OptionDescription('configuration', 'Configuration',
..                                       [manual_proxy, automatic_proxy])
.. 
.. This optiondescription is specified in help:
.. 
.. .. code-block:: bash
.. 
..     $ python3 src/proxy.py "No proxy" -h
..     usage: proxy.py "No proxy" [-h] [--dns_over_https] [--no-dns_over_https]
..                                {No proxy,Manual proxy configuration,Automatic
..                                proxy configuration URL}
.. 
..     positional arguments:
..       {No proxy,Manual proxy configuration,Automatic proxy configuration URL}
..                             Proxy's config mode
.. 
..     optional arguments:
..       -h, --help            show this help message and exit
..       --dns_over_https      Enable DNS over HTTPS
..       --no-dns_over_https
.. 
..     configuration:
..       Configuration
.. 
.. If you don't want empty optiondescription even if there is a description, you could add remove_empty_od to True in parse_args function:
.. 
.. .. code-block:: python
.. 
..     parser = TiramisuCmdlineParser(proxy_config, remove_empty_od=True)
.. 
.. SubConfig
.. ================
.. 
.. Entire Config is transformed into an argument by default.
.. 
.. It could be interesting to display only 'configuration' OptionDescription.
.. 
.. To do this, we have to define default all mandatories options outside this scope:
.. 
.. .. code-block:: python
.. 
..     proxy_mode = ChoiceOption('proxy_mode', 'Proxy\'s config mode', ('No proxy',
..                                                                      'Manual proxy configuration',
..                                                                      'Automatic proxy configuration URL'),
..                               default='Manual proxy configuration',
..                               properties=('positional', 'mandatory'))
.. 
.. Finally specified the root argument to `TiramisuCmdlineParser`:
.. 
.. .. code-block:: python
.. 
..     parser = TiramisuCmdlineParser(proxy_config, root='configuration')
.. 
.. Now, only sub option of configuration is proposed:
.. 
.. .. code-block:: bash
.. 
..     $ python3 src/proxy.py -h
..     usage: proxy.py [-h] -i HTTP_IP_ADDRESS -p [HTTP_PORT]
.. 
..     optional arguments:
..       -h, --help            show this help message and exit
.. 
..     configuration.manual_proxy:
..       Manual proxy settings
.. 
..       -i HTTP_IP_ADDRESS, --configuration.manual_proxy.http_ip_address HTTP_IP_ADDRESS
..                             Proxy's HTTP IP
..       -p [HTTP_PORT], --configuration.manual_proxy.http_port [HTTP_PORT]
..                             Proxy's HTTP Port
.. 
