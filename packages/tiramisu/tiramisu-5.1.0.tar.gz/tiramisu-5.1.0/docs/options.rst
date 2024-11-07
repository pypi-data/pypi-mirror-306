==================================
Default Options type
==================================

Basic options
==================================

Options
-----------

.. list-table:: 
   :widths: 20 40 40
   :header-rows: 1

   * - Type
     - Comments
     - Extra parameters

   * - StrOption
     - Option that accept any textual data in Tiramisu.
     -

   * - IntOption
     - Option that accept any integers number in Tiramisu.
     -
       - min_number
       - max_number

   * - FloatOption
     - Option that accept any floating point number in Tiramisu.
     -

   * - BoolOption
     - Boolean values are the two constant objects False and True.
     -

Examples
------------

Textual option:

>>> from tiramisu import StrOption
>>> StrOption('str', 'str', 'value')
>>> try:
...     StrOption('str', 'str', 1)
... except ValueError as err:
...     print(err)
... 
"1" is an invalid string for "str"

Integer option:

>>> from tiramisu import IntOption
>>> IntOption('int', 'int', 1)
>>> IntOption('int', 'int', 10, min_number=10, max_number=15)
>>> try:
...     IntOption('int', 'int', 16, max_number=15)
... except ValueError as err:
...     print(err)
... 
"16" is an invalid integer for "int", value must be less than "15"

.. note:: If `warnings_only` parameter it set to True, it will only emit a warning.

Floating point number option:

>>> from tiramisu import FloatOption
>>> FloatOption('float', 'float', 10.1)

Boolean option:

>>> from tiramisu import BoolOption 
>>> BoolOption('bool', 'bool', True)
>>> BoolOption('bool', 'bool', False)

Network options
==================================

.. list-table:: 
   :widths: 20 40 40
   :header-rows: 1

   * - Type
     - Comments
     - Extra parameters

   * - IPOption
     - An Internet Protocol address (IP address) is a numerical label assigned to each device connected to a computer network that uses the Internet Protocol for communication.

       This option only support version 4 of the Internet Protocol.
     -
       - private_only: restrict to only private IPv4 address
       - allow_reserved: allow the IETF reserved address
       - cidr: Classless Inter-Domain Routing (CIDR) is a method for allocating IP addresses and IP routing, such as 192.168.0.1/24

   * - NetworkOption
     - IP networks may be divided into subnetworks
     -
       - cidr: Classless Inter-Domain Routing (CIDR) is a method for allocating IP addresses and IP routing, such as 192.168.0.0/24

   * - NetmaskOption
     - For IPv4, a network may also be characterized by its subnet mask or netmask. This option allow you to enter a netmask.
     -

   * - BroadcastOption
     - The last address within a network broadcast transmission to all hosts on the link. This option allow you to enter a broadcast.
     -

   * - PortOption
     - A port is a network communication endpoint. It's a string object
     -
       - allow_range: allow is a list of port where we specified first port and last port number with the separator is `:`
       - allow_zero: allow the port 0
       - allow_wellknown: by default, the well-known ports (also known as system ports) those from 1 through 1023 are allowed, you can disabled it
       - allow_registred: by default, the registered ports are those from 1024 through 49151 are allowed, you can disabled it
       - allow_private: allow dynamic or private ports, which are those from 49152 through 65535, one common use for this range is for ephemeral ports
       - allow_protocol: allow to define protocol in value, it should be something like tcp:80 or udp:53

   * - MACOption
     - MAC address for a network card.


Examples
-------------------------------------------

>>> from tiramisu import IPOption
>>> IPOption('ip', 'ip', '192.168.0.24')
>>> IPOption('ip', 'ip', '1.1.1.1')
>>> try:
...     IPOption('ip', 'ip', '1.1.1.1', private_only=True)
... except ValueError as err:
...     print(err)
... 
"1.1.1.1" is an invalid IP for "ip", must be private IP

.. note:: If `warnings_only` parameter it set to True, it will only emit a warning.

>>> from tiramisu import IPOption
>>> try:
...     IPOption('ip', 'ip', '255.255.255.255')
... except ValueError as err:
...     print(err)
... 
"255.255.255.255" is an invalid IP for "ip", mustn't be reserved IP
>>> IPOption('ip', 'ip', '255.255.255.255', allow_reserved=True)

.. note:: If `warnings_only` parameter it set to True, it will only emit a warning.

>>> from tiramisu import IPOption
>>> IPOption('ip', 'ip', '192.168.0.1/24', cidr=True)
>>> try:
...     IPOption('ip', 'ip', '192.168.0.0/24', cidr=True)
... except ValueError as err:
...     print(err)
... 
"192.168.0.0/24" is an invalid IP for "ip", it's in fact a network address

>>> from tiramisu import NetworkOption
>>> NetworkOption('net', 'net', '192.168.0.0')
>>> NetworkOption('net', 'net', '192.168.0.0/24', cidr=True)
>>> NetmaskOption('mask', 'mask', '255.255.255.0')

>>> from tiramisu import BroadcastOption
>>> BroadcastOption('bcast', 'bcast', '192.168.0.254')

>>> from tiramisu import PortOption
>>> PortOption('port', 'port', '80')
>>> PortOption('port', 'port', '2000', allow_range=True)
>>> PortOption('port', 'port', '2000:3000', allow_range=True)
>>> from tiramisu import PortOption
>>> try:
...     PortOption('port', 'port', '0')
... except ValueError as err:
...     print(err)
... 
"0" is an invalid port for "port", must be between 1 and 49151
>>> PortOption('port', 'port', '0', allow_zero=True)

.. note:: This option affect the minimal and maximal port number, if `warnings_only` parameter it set to True, it will only emit a warning.

>>> from tiramisu import PortOption
>>> PortOption('port', 'port', '80')
>>> try:
...     PortOption('port', 'port', '80', allow_wellknown=False)
... except ValueError as err:
...     print(err)
... 
"80" is an invalid port for "port", must be between 1024 and 49151

.. note:: This option affect the minimal and maximal port number, if `warnings_only` parameter it set to True, it will only emit a warning.

>>> from tiramisu import PortOption
>>> PortOption('port', 'port', '1300')
>>> try:
...     PortOption('port', 'port', '1300', allow_registred=False)
... except ValueError as err:
...     print(err)
... 
"1300" is an invalid port for "port", must be between 1 and 1023

.. note:: This option affect the minimal and maximal port number, if `warnings_only` parameter it set to True, it will only emit a warning.

>>> from tiramisu import PortOption
>>> try:
...     PortOption('port', 'port', '64000')
... except ValueError as err:
...     print(err)
... 
"64000" is an invalid port for "port", must be between 1 and 49151
>>> PortOption('port', 'port', '64000', allow_private=True)

.. note:: This option affect the minimal and maximal port number, if `warnings_only` parameter it set to True, it will only emit a warning.

Internet options
==================================

.. list-table:: 
   :widths: 20 40 40
   :header-rows: 1

   * - Type
     - Comments
     - Extra parameters

   * - DomainnameOption
     - Domain names are used in various networking contexts and for application-specific naming and addressing purposes.
     - 
       - type: There is three type for a domain name:

         - "domainname" (default): lowercase, number, "-" and "." characters are allowed, this must have at least one "."
         - "hostname": lowercase, number and "-" characters are allowed, the maximum length is 63 characters
         - "netbios": lowercase, number and "-" characters are allowed, the maximum length is 15 characters

       - allow_ip: the option can contain a domain name or an IP, in this case, IP is validate has IPOption would do.
       - allow_cidr_network: the option can contain a CIDR network
       - allow_without_dot: a domain name with domainname's type must have a dot, if active, we can set a domainname or an hostname
       - allow_startswith_dot: a domain name with domainname's type mustn't start by a dot, .example.net is not a valid domain, in some case it could be interesting to allow domain name starts by a dot (for ACL in Squid, no proxy option in Firefox, ...)

   * - URLOption
     - An Uniform Resource Locator is, in fact, a string starting with http:// or https://, a DomainnameOption, optionaly ':' and a PortOption, and finally filename
     - See PortOption and DomainnameOption parameters

   * - EmailOption
     - Electronic mail (email or e-mail) is a method of exchanging messages ("mail") between people using electronic devices.
     -


Examples
-----------------------------------------------

>>> from tiramisu import DomainnameOption
>>> DomainnameOption('domain', 'domain', 'foo.example.net')
>>> DomainnameOption('domain', 'domain', 'foo', type='hostname')

.. note:: If `warnings_only` parameter it set to True, it will raise if length is incorrect by only emit a warning character is not correct.

>>> from tiramisu import DomainnameOption
>>> DomainnameOption('domain', 'domain', 'foo.example.net', allow_ip=True)
>>> DomainnameOption('domain', 'domain', '192.168.0.1', allow_ip=True)
>>> DomainnameOption('domain', 'domain', 'foo.example.net', allow_cidr_network=True)
>>> DomainnameOption('domain', 'domain', '192.168.0.0/24', allow_cidr_network=True)
>>> DomainnameOption('domain', 'domain', 'foo.example.net', allow_without_dot=True)
>>> DomainnameOption('domain', 'domain', 'foo', allow_without_dot=True)
>>> DomainnameOption('domain', 'domain', 'example.net', allow_startswith_dot=True)
>>> DomainnameOption('domain', 'domain', '.example.net', allow_startswith_dot=True)

>>> from tiramisu import URLOption
>>> URLOption('url', 'url', 'http://foo.example.fr/index.php')
>>> URLOption('url', 'url', 'https://foo.example.fr:4200/index.php?login=foo&pass=bar')

>>> from tiramisu import EmailOption
>>> EmailOption('mail', 'mail', 'foo@example.net')

Unix options
===============

.. list-table:: 
   :widths: 20 40
   :header-rows: 1

   * - Type
     - Comments
     - Extra parameters

   * - UsernameOption
     - An unix username option is a 32 characters maximum length with lowercase ASCII characters, number, '_' or '-'. The username have to start with lowercase ASCII characters or "_".
     -

   * - GroupnameOption
     - Same conditions has username
     -

   * - PasswordOption
     - Simple string with no other restriction:
     -
       - min_len: minimum length autorise for a password
       - max_len: maximum length autorise for a passwword
       - forbidden_char: list of forbidden characters for a password

   * - FilenameOption
     - For this option, only lowercase and uppercas ASCII character, "-", ".", "_", "~", and "/" are allowed.
     -
       - allow_relative: filename should starts with "/" (something like /etc/passwd), we can, with this option to allow relative name
       - test_existence: file or directory should exists
       - types
         - file: it should be a file
         - directory: it should be a directory

   * - PermissionsOption
     - Permissions for Unix file. It could be something like 644 or 1644.
     -

>>> from tiramisu import UsernameOption
>>> UsernameOption('user', 'user', 'my_user')

>>> from tiramisu import GroupnameOption
>>> GroupnameOption('group', 'group', 'my_group')

>>> from tiramisu import PasswordOption
>>> PasswordOption('pass', 'pass', 'oP$¨1jiJie')

>>> from tiramisu import FilenameOption
>>> FilenameOption('file', 'file', '/etc/tiramisu/tiramisu.conf')

Date option
=============

Date option waits for a date with format YYYY-MM-DD:

>>> from tiramisu import DateOption
>>> DateOption('date', 'date', '2019-10-30')

Choice option: :class:`ChoiceOption`
======================================

Option that only accepts a list of possible choices.

For example, we just want allowed 1 or 'see later':

>>> from tiramisu import ChoiceOption
>>> ChoiceOption('choice', 'choice', (1, 'see later'), 1)
>>> ChoiceOption('choice', 'choice', (1, 'see later'), 'see later')

Any other value isn't allowed:

>>> try:
...     ChoiceOption('choice', 'choice', (1, 'see later'), "i don't know")
... except ValueError as err:
...     print(err)
... 
"i don't know" is an invalid choice for "choice", only "1" and "see later" are allowed
