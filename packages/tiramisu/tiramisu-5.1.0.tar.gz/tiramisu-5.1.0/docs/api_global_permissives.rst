==================
Global permissive
==================

Permissives allow access, during a calculation, to a normally unavailable variable.

In the :doc:api_property example we add a new `create` option that has a calculation with the option `exists` as parameter.

This option has a calculated default_multi value. If the file exists (so `exists` option is True) we don't want create automaticly the file:

.. literalinclude:: src/api_global_permissive.py
   :lines: 7-8
   :linenos:

Here is the new option:

.. literalinclude:: src/api_global_permissive.py
   :lines: 20-23
   :linenos:

:download:`download the config <src/api_global_permissive.py>`

Get/add/pop/reset global permissive
=====================================

Let's try this config:

>>> config.property.read_write()
>>> config.option('new.filename').value.set(['/etc', '/unknown'])
>>> config.value.get()
{'new.filename': ['/etc', '/unknown'], 'new.exists': [True, False], 'new.create': [False, True]}

Now we want to see `advanced` option. But how calculate create value?

>>> config.property.add('advanced')
>>> try:
...     config.value.get()
... except ConfigError as err:
...     print(err)
unable to carry out a calculation for "Create automaticly the file", cannot access to option "This file exists" because has property "advanced"

We just have to add `advanced` permissive to allow calculation:

>>> config.permissive.add('advanced')
>>> config.value.get()
{'new.filename': ['/etc', '/unknown'], 'new.create': [False, True]}

At any time we can retrieve all global permissive:

>>> config.permissive.get()
frozenset({'hidden', 'advanced'})

We can remove on permissive:

>>> config.permissive.pop('hidden') 
>>> config.permissive.get()
frozenset({'advanced'})

And finally we can reset all permissives:

>>> config.permissive.reset()
>>> config.permissive.get()
frozenset()

Default permissives
============================

Tiramisu estimate default permissive.

All properties added in `read write` mode and removed in `read only` mode are, by default, included in permissive list when we change mode:

>>> default = config.property.getdefault('read_write', 'append')
>>> config.property.setdefault(frozenset(default | {'advanced'}), 'read_write', 'append')
>>> default = config.property.getdefault('read_only', 'remove')
>>> config.property.setdefault(frozenset(default | {'advanced'}), 'read_only', 'remove')
>>> config.property.read_write()
>>> config.permissive.get()
frozenset({'advanced', 'hidden'})

Importation and exportation
================================

In config, all permissive (global's and option's permissives) can be exportated:

>>> config.permissive.exportation()
{None: frozenset({'hidden', 'advanced'})}

And reimported later:

>>> export = config.permissive.exportation()
>>> config.permissive.importation(export)

.. note:: The exportation format is not stable and can be change later, please do not use importation otherwise than jointly with exportation.
