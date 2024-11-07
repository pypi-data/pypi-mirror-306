==================
Option's property
==================

Let's start to build a config.

First of, import needed object:

.. literalinclude:: src/api_option_property.py
   :lines: 1-9
   :linenos:

Instanciate a first option to call a file name:

.. literalinclude:: src/api_option_property.py
   :lines: 56-59
   :linenos:

Secondly add an `exists` option to know if this file is already created:

.. literalinclude:: src/api_option_property.py
   :lines: 60-64
   :linenos:

Thirdly add a `create` option used by a potential script to create wanted file:

.. literalinclude:: src/api_option_property.py
   :lines: 65-72
   :linenos:

A new option is create to known the file type. If file already exists, retrieve automaticly the type, otherwise ask to the user:

.. literalinclude:: src/api_option_property.py
   :lines: 35-42
   :linenos:

.. literalinclude:: src/api_option_property.py
   :lines: 73-87
   :linenos:

In same model, create a `user` and `group` name options:

.. literalinclude:: src/api_option_property.py
   :lines: 12-32
   :linenos:

.. literalinclude:: src/api_option_property.py
   :lines: 88-111
   :linenos:

Finally create a `mode` option:

.. literalinclude:: src/api_option_property.py
   :lines: 45-53
   :linenos:

.. literalinclude:: src/api_option_property.py
   :lines: 112-116
   :linenos:

Let's build the config:

.. literalinclude:: src/api_option_property.py
   :lines: 118-124
   :linenos:

:download:`download the config <src/api_option_property.py>`

Get/add/pop/reset property
=================================

option description's property
'''''''''''''''''''''''''''''''''''''''''

An option description is an option. It's possible to set property to it:

>>> config.property.read_write()
>>> config.option('new').property.get()
set()

To add a property:

>>> config.option('new').property.add('disabled')
>>> config.option('new').property.get()
set('disabled')

The property affect the option description:

>>> try:
...     config.option('new').value.get()
... except PropertiesOptionError as err:
...     print(err)
cannot access to optiondescription "Add new file" because has property "disabled"

But, of course the child option too. If access to option description is not possible, it's not possible to child option too:

>>> try:
...     config.option('new.filename').value.get()
... except PropertiesOptionError as err:
...     print(err)
cannot access to optiondescription "Add new file" because has property "disabled"

We can remove an existed property too:

>>> config.option('new').property.add('hidden')
>>> config.option('new').property.get()
{'hidden', 'disabled'}
>>> config.option('new').property.pop('hidden')
>>> config.option('new').property.get()
{'disabled'}


It's possible to reset property:

>>> config.option('new').property.reset()
>>> config.option('new').value.get()
{'filename': [], 'exists': [], 'create': [], 'type': [], 'user': [], 'group': [], 'mode': []}

option's property
'''''''''''''''''''''''''''''''''''''''

In a simple option we can add, pop or reset property:

>>> config.property.read_write()
>>> config.option('new.filename').property.get())
{'mandatory', 'unique', 'empty'}
>>> config.option('new.filename').property.add('frozen')
>>> config.option('new.filename').property.get()
{'mandatory', 'unique', 'frozen', 'empty'}
>>> config.option('new.filename').property.pop('empty')
>>> config.option('new.filename').property.get()
{'frozen', 'mandatory', 'unique'}
>>> config.option('new.filename').property.reset()
>>> config.option('new.filename').property.get()
{'mandatory', 'unique', 'empty'}

leader's property
''''''''''''''''''''''''''''

In leader's option can only have a list of property. For other's property, please set directly in leadership option:

>>> config.property.read_write()
>>> try:
...     config.option('new.filename').property.add('hidden')
... except LeadershipError as err:
...     print(err)
leader cannot have "hidden" property
>>> config.option('new').property.add('hidden')

This `hidden` property has to affect leader option but also all follower option.
That why you have to set this kind of properties directly in leadership option.

.. note::
	Allowed properties for a leader: 'empty', 'unique', 'force_store_value', 'mandatory', 'force_default_on_freeze', 'force_metaconfig_on_freeze', and 'frozen'.


follower's property
'''''''''''''''''''''''''''''''''''''''

First of add, add values in leader option:

>>> config.property.read_write()
>>> config.option('new.filename').value.set(['/etc/passwd', 'unknown1', 'unknown2'])

We have to get property with an index:

>>> config.option('new.create', 1).property.get()
set()

We can set property with index:

>>> config.option('new.create', 1).property.add('frozen')
>>> config.option('new.create', 1).property.get()
{'frozen'}
>>> config.option('new.create', 2).property.get()
set()

But we can alse set without index (available for all follower's value):

>>> config.option('new.create').property.add('frozen')
>>> print(config.option('new.create', 1).property.get())
{'frozen'}
>>> print(config.option('new.create', 2).property.get())
{'frozen'}

Calculated property
=======================

A property can be a :doc:`calculation`. That means that the property will be set or not following the context.

The Calculation can return two type of value:

- a `str` this string is a new property
- `None` so this property is cancel

First of all, have a look to the `create` properties:

.. literalinclude:: src/api_option_property.py
   :lines: 68-72
   :linenos:

This option has only one property which is `disabled` when `exists` has value True.

If the file exists, we don't have to now if user wants create it. It is already exists. So we don't have to access to this option.

Secondly, have a look to the `type` properties:

.. literalinclude:: src/api_option_property.py
   :lines: 79-87
   :linenos:

There is:

- two static properties: `force_default_on_freeze` and `mandatory`.
- two calculated properties: `hidden` and `frozen`

If the file is already exists, the two calculated properties are present to this option.

So we can access to this option only in read only mode and user cannot modified it's value.

Finally have a look to the `username` and `grpname` options' properties:

.. literalinclude:: src/api_option_property.py
   :lines: 94-99
   :linenos:

In this case we have two properties:

- one static property: `force_store_value`
- one calculated property: `mandatory`

This calculated property is apply only if `create` is True.

Be carefull to the `create` option. It could be disabled, so not accessible in calculation if the file exists as see previously.

That why we add notraisepropertyerror attribute to True, even if the calculation will failed.
In this case the value of `create` is not add in `calc_value` argument.

In this case the function `calc_value` consider that the property `mandatory` has to be set.

But we just want to set `mandatory` property only if create is False. That why we add the no_condition_is_invalid to True.

Force the registration of a value
====================================

The property `force_store_value` is a special property. This property permit to store a value automaticly even if user do not set value or reset the value.
This is useful especially, for example, for recording a random draw password through a calculation. Or to store any first result for a calculation.

To the, create a new config:

>>> config = Config(root)

If we add value in `filename`, the option `exists` stay a default value, but not the `mode` option, which has `force_store_value`:

>>> config.property.read_write()
>>> config.option('new.filename').value.set(['/etc'])
>>> print(config.option('new.filename').owner.get())
user
>>> print(config.option('new.exists', 0).owner.get())
default
>>> print(config.option('new.mode', 0).owner.get())
forced

If we try to reset `mode` value, this option is modified:

>>> config.option('new.mode', 0).value.reset()
>>> config.option('new.mode', 0).owner.get()
forced

Non-empty value, mandatory and unique
========================================================

Leader and multi have automaticly two properties `unique` and `empty`:

>>> config = Config(OptionDescription('root', 'root', [FilenameOption('filename',
...                                                                   'Filename',
...                                                                   multi=True)]))
>>> config.option('filename').property.get()
{'empty', 'unique'}

To remove `empty` property

>>> config = Config(OptionDescription('root', 'root', [FilenameOption('filename',
...                                                                   'Filename',
...                                                                   properties=('notempty',),
...                                                                   multi=True)]))
>>> config.option('filename').property.get()
{'unique'}
>>> config = Config(OptionDescription('root', 'root', [FilenameOption('filename',
...                                                                   'Filename',
...                                                                   properties=('notunique',),
...                                                                   multi=True)]))
>>> config.option('filename').property.get()
{'empty'}

Let's try with previous config.

First of all we remove `force_store_value` mode:

>>> config = Config(root)
>>> properties = config.property.getdefault('read_write', 'append') - {'force_store_value'}
>>> config.property.setdefault(frozenset(properties), 'read_write', 'append')
>>> properties = config.property.getdefault('read_only', 'append') - {'force_store_value'}
>>> config.property.setdefault(frozenset(properties), 'read_only', 'append')

In addition to the specified `mandatory` property, leader have automaticly two properties: `unique` and `empty`:

>>> config.option('new.filename').property.get()
{'unique', 'mandatory', 'empty'}

What is the difference between the property `unique` and `mandatory`?

Let's try with no value at all:

>>> config.property.read_only()
>>> try:
...     config.option('new.filename').value.get()
>>> except PropertiesOptionError as err:
...     print(err)
cannot access to option "Filename" because has property "mandatory"

A `mandatory` multi must have at least one value. This value is check only in read only mode.

If we remove the `mandatory` property, the value is valid:

>>> config.property.read_write()
>>> config.option('new.filename').property.pop('mandatory')
>>> config.option('new.filename').property.get()
{'unique', 'empty'}
>>> config.property.read_only()
>>> config.option('new.filename').value.get()
[]

A `empty` multi can has no value, but if you set a value, it must not be None:

>>> config.property.read_write()
>>> config.option('new.filename').value.set(['/etc', None])
>>> config.property.read_only()
>>> try:
...     config.option('new.filename').value.get()
... except PropertiesOptionError as err:
...     print(err)
cannot access to option "Filename" because has property "empty"

Trying now without this property:

>>> config.property.read_write()
>>> config.option('new.filename').property.pop('empty')
>>> config.option('new.filename').value.set(['/etc', None])
>>> config.property.read_only()
>>> config.option('new.filename').value.get()
['/etc', None]

A `unique` property in multi means you cannot have same value twice:

>>> config.property.read_write()
>>> try:
... 	config.option('new.filename').value.set(['/etc', '/etc'])
... except ValueError as err:
... 	print(err)
"['/etc', '/etc']" is an invalid file name for "Filename", the value "/etc" is not unique

When removing this property:

>>> config.property.read_write()
>>> config.option('new.filename').property.pop('unique')
>>> config.option('new.filename').value.set(['/etc', '/etc'])
>>> config.property.read_only()
>>> config.option('new.filename').value.get()
['/etc', '/etc']

Non-modifiable option
=====================

Freeze an option means that you cannot change the value of this option:

>>> config = Config(root)
>>> config.property.read_write()
>>> config.option('new.filename').value.set(['unknown'])
>>> config.option('new.create', 0).value.set(False)
>>> config.option('new.create', 0).property.add('frozen')
>>> try:
...     config.option('new.create', 0).value.set(False)
... except PropertiesOptionError as err:
...     print(err)
cannot modify the option "Create automaticly the file" because has property "frozen"

Sometime (for example when an option is calculated) we want retrieve the default value (so the calculated value) when we add `frozen` option.

In the current example, `new.exists` is a calculated value and we don't want that the used modify this option. So we add `frozen` and `force_default_on_freeze` properties.

For example, without mode, we can modify the `new.exists` option, but in `read_only` mode, we want to have default value:

>>> config = Config(root)
>>> config.option('new.filename').value.set(['unknown'])
>>> config.option('new.exists', 0).value.set(True)
>>> config.option('new.exists', 0).value.get()
True
>>> config.property.read_write()
>>> config.option('new.exists', 0).value.get()
False

The property `force_default_on_freeze` is also avalaible in the option `new.type`. If the file exists, the type is calculated but if it not already exists, the user needs to set the correct wanted type.
