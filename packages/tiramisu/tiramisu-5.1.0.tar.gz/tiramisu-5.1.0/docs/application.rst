==================================
A full application
==================================

The firefox network configuration
-------------------------------------

Now we are going to resume everything we have seen with a concrete example.
We're going to take an example based on the `Mozilla Firefox
<https://www.mozilla.org/en-US/firefox/>`_ proxy's
configuration, like what is required when you open the `network settings` in
the General configuration's firefox page:

.. image:: images/firefox_preferences.png

The tiramisu's configuration
----------------------------

Build the `Config`
''''''''''''''''''''

First, let's create our options :

.. literalinclude:: src/application.py
   :lines: 1-3, 12-20
   :linenos:

This first option is the most important one : its value will determine which other options
are disabled and which are not. The same thing will happen with other options later.
Here are the others options we'll be using :

.. literalinclude:: src/application.py
   :lines: 23-221
   :linenos:

As you can see, we're using :doc:`value <api_value>`, :doc:`property <api_option_property>`
and :doc:`calculation` in the setting of our options, because we have many options which
value or accessibility is depending on the value of other options.

Now we need to create OptionDescriptions and configs :

.. literalinclude:: src/application.py
    :lines: 223-232
    :linenos:

Download the :download:`full code <src/application.py>` of this example.

As you can see, we regrouped a lot of options in 'protocols', so we can set a calculated `disabled` property
that is apply to all those options. This way, we don't have to put the instruction on every option
one by one.

Let's try
'''''''''''''''

Now that we have our Config, it's time to run some tests !
Here are a few code blocks you can test and the results you should get :

1. Automatic proxy configuration URL:

>>> proxy_config.property.read_write()
>>> proxy_config.option('proxy_mode').value.set('Automatic proxy configuration URL')
>>> proxy_config.option('auto_config_url').value.set('http://192.168.1.1/wpad.dat')
>>> proxy_config.property.read_only()
>>> for path, value in proxy_config.value.get().items():
...     print(proxy_config.option(path).option.doc() + ': "' + str(value) + '"')
Proxy's config mode: "Automatic proxy configuration URL"
Address for which proxy will be desactivated: "[]"
Proxy's auto config URL: "http://192.168.1.1/wpad.dat"
Prompt for authentication if password is saved: "False"
Enable DNS over HTTPS: "False"

2. Auto-detect proxy settings for this network:

>>> proxy_config.property.read_write()
>>> proxy_config.option('proxy_mode').value.set('Auto-detect proxy settings for this network')
>>> proxy_config.option('no_proxy').value.set(['localhost',
...                                            '127.0.0.1',
...                                            '192.16.10.150',
...                                            '192.168.5.101',
...                                            '192.168.56.101/32',
...                                            '192.168.20.0/24',
...                                            '.tiramisu.org',
...                                            'mozilla.org'])
>>> proxy_config.option('dns_over_https.enable_dns_over_https').value.set(True)
>>> proxy_config.option('dns_over_https.used_dns').value.set('default')
>>> proxy_config.property.read_only()
>>> for path, value in proxy_config.value.get().items():
...    print(proxy_config.option(path).option.doc() + ': "' + str(value) + '"')
Proxy's config mode: "Auto-detect proxy settings for this network"
Address for which proxy will be desactivated: "['localhost', '127.0.0.1', '192.16.10.150', '192.168.5.101', '192.168.56.101/32', '192.168.20.0/24', '.tiramisu.org', 'mozilla.org']"
Prompt for authentication if password is saved: "False"
Enable DNS over HTTPS: "True"
Used DNS: "default"

Set use_for_all_protocols to True:

>>> proxy_config.property.read_write()
>>> proxy_config.option('protocols.use_for_all_protocols').value.set(True)
>>> proxy_config.property.read_only()
>>> for path, value in proxy_config.value.get().items():
...     print(proxy_config.option(path).option.doc() + ': "' + str(value) + '"')
Proxy's config mode: "Manual proxy configuration"
Address: "192.168.20.1"
Port: "8080"
Use HTTP IP and Port for all protocols: "True"
Address: "192.168.20.1"
Port: "8080"
Address: "192.168.20.1"
Port: "8080"
Address: "192.168.20.1"
Port: "8080"
SOCKS host version used by proxy: "v5"
Address for which proxy will be desactivated: "[]"
Prompt for authentication if password is saved: "False"
Use Proxy DNS when using SOCKS v5: "False"
Enable DNS over HTTPS: "True"
Used DNS: "custom"
Custom DNS URL: "https://dns-url.com"

