==================================
Manage values
==================================

Values with options
=========================

Simple option
----------------------------

Begin by creating a Config. This Config will contains two options:

- first one is an option where the user will set an unix path
- second one is an option that calculate the disk usage of the previous unix path

Let's import needed object:

.. literalinclude:: src/api_value.py
   :lines: 1-4
   :linenos:

Create a function that verify the path exists in current system:

.. literalinclude:: src/api_value.py
   :lines: 6-9
   :linenos:

Use this function as a :doc:`validator` in a new option call `path`:

.. literalinclude:: src/api_value.py
   :lines: 24-25
   :linenos:

Create a second function that calculate the disk usage:

.. literalinclude:: src/api_value.py
   :lines: 11-21
   :linenos:

Add a new option call `usage` that use this function with first argument the option `path` created before:

.. literalinclude:: src/api_value.py
   :lines: 26-27
   :linenos:

Finally add those options in option description and a Config:

.. literalinclude:: src/api_value.py
   :lines: 28-31
   :linenos:

:download:`download the config <src/api_value.py>`

Get and set a value
'''''''''''''''''''''''''''''

First of all, retrieve the values of both options:

>>> config.option('disk.path').value.get()
None
>>> config.option('disk.usage').value.get()
None

Enter a value of the `path` option:

>>> config.option('disk.path').value.set('/')

The value is really change:

>>> config.option('disk.path').value.get()
/

Now, calculation retrieve a value:

>>> config.option('disk.usage').value.get()
668520882176.0

When you enter a value it is validated:

>>> try:
>>>     config.option('disk.path').value.set('/unknown')
>>> except ValueError as err:
>>>     print(err)
"/unknown" is an invalid file name for "Path", this directory does not exist

We can also set a :doc:`calculation` as value. For example, we want to launch previous function but with in_gb to True as second argument:

>>> calc = Calculation(calc_disk_usage, Params((ParamOption(filename),
...                                             ParamValue('gigabytes'))))
>>> config.option('disk.usage').value.set(calc)
>>> config.option('disk.usage').value.get()
622.6080360412598

Is value is valid?
'''''''''''''''''''''''''''''

To check is a value is valid:

>>> config.option('disk.path').value.valid()
True

Display the default value
'''''''''''''''''''''''''''''

Even if the value is modify, you can display the default value with `default` method:

>>> config.option('disk.path').value.set('/')
>>> config.option('disk.usage').value.set(1.0)
>>> config.option('disk.usage').value.get()
1.0
>>> config.option('disk.usage').value.default()
668510105600.0

Return to the default value
'''''''''''''''''''''''''''''

If the value is modified, just `reset` it to retrieve the default value:

>>> config.option('disk.path').value.set('/')
>>> config.option('disk.path').value.get()
/
>>> config.option('disk.path').value.reset()
>>> config.option('disk.path').value.get()
None

The ownership of a value
'''''''''''''''''''''''''''''

Every option has an owner, that will indicate who changed the option's value last.

The default owner of every option is "default", and means that the value is the default one.

If you use a "reset" instruction to get back to the default value, the owner will get back
to "default" as well.

>>> config.option('disk.path').value.reset()
>>> config.option('disk.path').owner.isdefault()
True
>>> config.option('disk.path').owner.get()
default
>>> config.option('disk.path').value.set('/')
>>> config.option('disk.path').owner.isdefault()
False
>>> config.option('disk.path').owner.get()
user

All modified values have an owner. We can change at anytime this owner:

>>> config.option('disk.path').owner.set('itsme')
>>> config.option('disk.path').owner.get()
itsme

.. note::
    This will work only if the current owner isn't "default".

This new user will be keep until anyone change the value:

>>> config.option('disk.path').value.set('/')
>>> config.option('disk.path').owner.get()
user

This username is in fact the `config` user, which is `user` by default:

>>> config.owner.get()
user

This owner will be the owner that all the options in the config will get when their value is changed.

This explains why earlier, the owner became "user" when changing the option's value.

We can change this owner:

>>> config.owner.set('itsme')
>>> config.option('disk.path').value.set('/')
>>> config.option('disk.path').owner.get()
itsme

Get choices from a Choice option
--------------------------------------

In the previous example, it's difficult to change the second argument of the `calc_disk_usage`.

For ease the change, add a `ChoiceOption` and replace the `size_type` and `disk` option:

.. literalinclude:: src/api_value_choice.py
   :lines: 26-31
   :linenos:

We set the default value to `bytes`, if not, the default value will be None.

:download:`download the config <src/api_value_choice.py>`

At any time, we can get all de choices avalaible for an option:

>>> config.option('disk.size_type').value.list()
('bytes', 'giga bytes')

Value in multi option
--------------------------------------

.. FIXME undefined

For multi option, just modify a little bit the previous example.
The user can, now, set multiple path.

First of all, we have to modification in this option:

- add multi attribute to True
- the function use in validation valid a single value, so each value in the list must be validate separatly, for that we add whole attribute to False in `ParamSelfOption` object

.. literalinclude:: src/api_value_multi.py
   :lines: 23-25
   :linenos:

Secondly, the function calc_disk_usage must return a list:

.. literalinclude:: src/api_value_multi.py
   :lines: 11-26
   :linenos:

Finally `usage` option is also a multi:

.. literalinclude:: src/api_value_multi.py
   :lines: 27-30
   :linenos:

:download:`download the config <src/api_value_multi.py>`

Get or set a multi value
'''''''''''''''''''''''''''''

Since the options are multi, the default value is a list:

>>> config.option('disk.path').value.get()
[]
>>> config.option('disk.usage').value.get()
[]

A multi option waiting for a list:

>>> config.option('disk.path').value.set(['/', '/tmp'])
>>> config.option('disk.path').value.get()
['/', '/tmp']
>>> config.option('disk.usage').value.get()
[668499898368.0, 8279277568.0]

The ownership of multi option
'''''''''''''''''''''''''''''

There is no difference in behavior between a simple option and a multi option:

>>> config.option('disk.path').value.reset()
>>> config.option('disk.path').owner.isdefault()
True
>>> config.option('disk.path').owner.get()
default
>>> config.option('disk.path').value.set(['/', '/tmp'])
>>> config.option('disk.path').owner.get()
user

Leadership
--------------------------------------

In previous example, we cannot define different `size_type` for each path. If you want do this, you need a leadership.

In this case, each time we add a path, we can change an associate `size_type`.

As each value of followers are isolate, the function `calc_disk_usage` will receive only one path and one size.

So let's change this function:

.. literalinclude:: src/api_value_leader.py
   :lines: 12-18
   :linenos:

Secondly the option `size_type` became a multi:

.. literalinclude:: src/api_value_leader.py
   :lines: 24-25
   :linenos:

Finally disk has to be a leadership:

.. literalinclude:: src/api_value_leader.py
   :lines: 30
   :linenos:

Get and set a leader
'''''''''''''''''''''''''''''

A leader is, in fact, a multi option:

>>> config.option('disk.path').value.set(['/', '/tmp'])
>>> config.option('disk.path').value.get()
['/', '/tmp']

There is two differences:

- we can get the leader length:

>>> config.option('disk.path').value.set(['/', '/tmp'])
>>> config.option('disk.path').value.len()
2

- we cannot reduce by assignation a leader:

>>> config.option('disk.path').value.set(['/', '/tmp'])
>>> from tiramisu.error import LeadershipError
>>> try:
...     config.option('disk.path').value.set(['/'])
... except LeadershipError as err:
...     print(err)
cannot reduce length of the leader "Path"

We cannot reduce a leader because Tiramisu cannot determine which isolate follower we have to remove, this first one or the second one?

To reduce use the `pop` method:

>>> config.option('disk.path').value.set(['/', '/tmp'])
>>> config.option('disk.path').value.pop(1)
>>> config.option('disk.path').value.get()
['/']

Get and set a follower
'''''''''''''''''''''''''''''

As followers are isolate, we cannot get all the follower values:

>>> config.option('disk.path').value.set(['/', '/tmp'])
>>> from tiramisu.error import APIError
>>> try:
...     config.option('disk.size_type').value.get()
... except APIError as err:
...     print(err)
index must be set with the follower option "Size type"

Index is mandatory:

>>> config.option('disk.path').value.set(['/', '/tmp'])
>>> config.option('disk.size_type', 0).value.get()
bytes
>>> config.option('disk.size_type', 1).value.get()
bytes

It's the same thing during the assignment:

>>> config.option('disk.path').value.set(['/', '/tmp'])
>>> config.option('disk.size_type', 0).value.set('giga bytes')

As the leader, follower has a length (in fact, this is the leader's length):

>>> config.option('disk.size_type').value.len()
2

The ownership of a leader and follower
'''''''''''''''''''''''''''''''''''''''''''

There is no differences between a multi option and a leader option:

>>> config.option('disk.path').value.set(['/', '/tmp'])
>>> config.option('disk.path').owner.get()
user

For follower, it's different, always because followers are isolate:

>>> config.option('disk.size_type', 0).value.set('giga bytes')
>>> config.option('disk.size_type', 0).owner.isdefault()
False
>>> config.option('disk.size_type', 0).owner.get()
user
>>> config.option('disk.size_type', 1).owner.isdefault()
True
>>> config.option('disk.size_type', 1).owner.get()
default

Values in option description
==============================

With an option description we can have directly a dict with all option's name and value:

>>> config.option('disk.path').value.set(['/', '/tmp'])
>>> config.option('disk.size_type', 0).value.set('giga bytes')
>>> config.option('disk').value.get()
{'disk.path': ['/', '/tmp'], 'disk.size_type': ['giga bytes', 'bytes'], 'disk.usage': [622.578239440918, 8279273472.0]}

Values in config
==========================

get
--------

With the `config` we can have directly a dict with all option's name and value:

>>> config.option('disk.path').value.set(['/', '/tmp'])
>>> config.option('disk.size_type', 0).value.set('giga bytes')
>>> config.value.get()
{'disk.path': ['/', '/tmp'], 'disk.size_type': ['giga bytes', 'bytes'], 'disk.usage': [622.578239440918, 8279273472.0]}

If you don't wan't path but only the name:

>>> config.value.get(flatten=True)
{'path': ['/', '/tmp'], 'size_type': ['giga bytes', 'bytes'], 'usage': [622.578239440918, 8279273472.0]}

importation/exportation
------------------------

In config, we can export full values:

>>> config.value.exportation()
[['disk.path', 'disk.size_type'], [None, [0]], [['/', '/tmp'], ['giga bytes']], ['user', ['user']]]

and reimport it later:

>>> export = config.value.exportation()
>>> config.value.importation(export)

.. note:: The exportation format is not stable and can be change later, please do not use importation otherwise than jointly with exportation.
