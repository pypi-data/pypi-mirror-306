================
Global property
================

Before start, have a look to :doc:property.

Let's start by import needed objects:

.. literalinclude:: src/api_global_property.py
   :lines: 1-4
   :linenos:

Instanciate a first option with `mandatory` property:

.. literalinclude:: src/api_global_property.py
   :lines: 7-10
   :linenos:

Instanciate a second option with calculated value, which verify if the file exists.

This options has `frozen`, `force_default_on_freeze` and `advanced` properties:

.. literalinclude:: src/api_global_property.py
   :lines: 11-15
   :linenos:

This two options are in a leadership:

.. literalinclude:: src/api_global_property.py
   :lines: 16-18
   :linenos:

Finally create the root option description and the config:

.. literalinclude:: src/api_global_property.py
   :lines: 19-20
   :linenos:

:download:`download the config <src/api_global_property.py>`

Read only and read write
==========================

By default, there is no restriction.

For example, it's possible to change value of a `frozen` option (here the `exists`' option):

>>> config.option('new.filename').value.set(['/etc'])
>>> config.option('new.exists', 0).value.set(False)

To have the good properties in "read / write" mode:

>>> config.property.read_write()
>>> config.option('new.filename').value.set(['/etc'])
>>> try:
...    config.option('new.exists', 0).value.set(False)
...except PropertiesOptionError as err:
...    print(err)
cannot modify the option "This file exists" because has property "frozen"

The read write mode is used be a human who wants to modify the configuration.
Some variables are not displayed, because this person cannot modified it.

To have the good properties in "read only" mode:

>>> config.property.read_only()
>>> try:
...    config.option('new.filename').value.set(['/etc'])
...except PropertiesOptionError as err:
...    print(err)
cannot modify the option "Filename" because has property "frozen"

In this mode it is impossible to modify the values of the options.
It should be use by a script, for build a template, ...
All variables not desactived are accessible.

Get/add/pop/reset global property
=======================================

The default read only and read write properties are:

>>> config.property.read_only()
>>> config.property.get()
frozenset({'force_store_value', 'validator', 'everything_frozen', 'warnings', 'cache', 'mandatory', 'frozen', 'empty', 'disabled'})
>>> config.property.read_write()
>>> config.property.get()
frozenset({'frozen', 'cache', 'warnings', 'disabled', 'validator', 'force_store_value', 'hidden'})

In the current config, the option has property `advanced`.

Has you can see below, the `advanced` is not used in any mode. This property doesn't affect Tiramisu.

Imagine that you don't want to see any advanced option by default. Just add this property in global property:

>>> config.option('new.filename').value.set(['/etc'])
>>> config.property.read_write()
>>> config.value.get()
{'new.filename': ['/etc'], 'new.exists': [True]}
>>> config.property.add('advanced')
>>> config.property.get()
frozenset({'frozen', 'advanced', 'hidden', 'validator', 'force_store_value', 'disabled', 'cache', 'warnings'})
>>> config.value.get()
{'new.filename': ['/etc']}

Of course you want to access to this option in read only mode.
So you have to remove this property:

>>> config.property.read_only()
>>> config.property.pop('advanced')
>>> config.property.get()
frozenset({'force_store_value', 'everything_frozen', 'frozen', 'warnings', 'empty', 'disabled', 'mandatory', 'cache', 'validator'})
>>> config.value.get()
{'new.filename': ['/etc'], 'new.exists': [True]}

At any time we can return to the default property (default means initialized properties, before change to read only or read write mode):

>>> config.property.read_only()
>>> config.property.get()
frozenset({'empty', 'cache', 'force_store_value', 'everything_frozen', 'warnings', 'frozen', 'disabled', 'mandatory', 'validator'})
>>> config.property.reset()
>>> config.property.get()
frozenset({'cache', 'warnings', 'validator'})

Get default properties in mode
=======================================

Add or pop properties each time we pass from one mode to an other is not a good idea. It better to change `read_write` and `read_only` mode directly.

Change mode means, in fact, add some properties and remove some other properties.

For example, when we pass to read_write mode, this properties are added:

>>> config.property.getdefault('read_write', 'append')
frozenset({'disabled', 'validator', 'force_store_value', 'hidden', 'frozen'})

and this properties are remove:

>>> config.property.getdefault('read_write', 'remove')
frozenset({'empty', 'everything_frozen', 'mandatory', 'permissive'})

Here is properties added when pass to read_only mode:

>>> config.property.getdefault('read_only', 'append')
frozenset({'empty', 'mandatory', 'validator', 'disabled', 'force_store_value', 'everything_frozen', 'frozen'})

and this properties are remove:

>>> config.property.getdefault('read_only', 'remove')
frozenset({'hidden', 'permissive'})

Just add the property to the default value to automatically automate the addition and deletion.
We want to add the property when we switch to "read write" mode and automatically delete this property when we switch to "read only" mode:

>>> default = config.property.getdefault('read_write', 'append')
>>> config.property.setdefault(frozenset(default | {'advanced'}), 'read_write', 'append')
>>> default = config.property.getdefault('read_only', 'remove')
>>> config.property.setdefault(frozenset(default | {'advanced'}), 'read_only', 'remove')

Let's try:

>>> 'advanced' in config.property.get()
False
>>> config.property.read_write()
>>> 'advanced' in config.property.get()
True
>>> config.property.read_only()
>>> 'advanced' in config.property.get()
False

Importation and exportation
=======================================

In config, all properties (global's and option's properties) can be exportated:

>>> config.property.exportation()
{None: frozenset({'empty', 'cache', 'warnings', 'validator', 'disabled', 'force_store_value', 'everything_frozen', 'frozen', 'mandatory'})}

And reimported later:

>>> export = config.property.exportation()
>>> config.property.importation(export)

.. note:: The exportation format is not stable and can be change later, please do not use importation otherwise than jointly with exportation.


