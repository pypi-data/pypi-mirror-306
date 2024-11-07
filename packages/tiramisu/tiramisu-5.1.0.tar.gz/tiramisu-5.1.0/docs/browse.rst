Browse the :class:`Config`
===========================

Getting the options
----------------------

.. note:: The :class:`Config` object we are using is located here in this script:

          :download:`download the source <src/property.py>`

Let's retrieve the config object, named `cfg`

.. code-block:: python

    from property import cfg

We retrieve by path an option named `var1`
and then we retrieve its name and its docstring

.. code-block:: bash
    :emphasize-lines: 2, 5, 8

    print(cfg.option('od1.var1'))
    <tiramisu.api.TiramisuOption object at 0x7f3876cc5940>

    print(cfg.option('od1.var1').option.name())
    'var1'

    print(cfg.option('od1.var1').option.doc())
    'first option'


Accessing the values of the options
-------------------------------------

Let's browse the configuration structure and option values.

You have getters as a `get` method on option objects:


.. code-block:: bash
    :emphasize-lines: 10, 14

    # getting all the options
    print(cfg.option.value.get())
    {'var1': None, 'var2': 'value'}

    # getting the `od1` option description
    print(cfg.option('od1').value.get())
    {'od1.var1': None, 'od1.var2': 'value'}

    # getting the var1 option's value
    print(cfg.option('od1.var1').value.get())
    None

    # getting the var2 option's default value
    print(cfg.option('od1.var2').value.get())
    'value'

    # trying to get a non existent option's value
    cfg.option('od1.idontexist').value.get()
    AttributeError: unknown option "idontexist" in optiondescription "od1"


Setting the value of an option
------------------------------

An important part of the setting's configuration consists of setting the
value's option.


You have setters as a `set` method on option objects.

And if you wanna come back to a default value, use the `reset()` method.

.. code-block:: bash
    :emphasize-lines: 2

    # changing the `od1.var1` value
    cfg.option('od1.var1').value.set('éééé')
    print(cfg.option('od1.var1').value.get())
    'éééé'

    # carefull to the type of the value to be set
    cfg.option('od1.var1').value.set(23454)
    ValueError: "23454" is an invalid string for "first variable"

    # let's come back to the default value
    cfg.option('od1.var2').value.reset()
    print(cfg.option('od1.var2').value.get())
    'value'

.. important:: If the config is `read only`, setting an option's value isn't allowed, see :doc:`property`


Let's make the protocol of accessing a `Config`'s option explicit
(because explicit is better than implicit):

1. If the option has not been declared, an `Error` is raised,
2. If an option is declared, but neither a value nor a default value has
   been set, the returned value is `None`,
3. If an option is declared and a default value has been set, but no value
   has been set, the returned value is the default value of the option,

4. If an option is declared, and a value has been set, the returned value is
   the value of the option.

But there are special exceptions. We will see later on that an option can be a
:term:`mandatory option`. A mandatory option is an option that must have a value
defined.

Searching for an option
~~~~~~~~~~~~~~~~~~~~~~~~~~

In an application, knowing the path of an option is not always feasible.
That's why a tree of options can easily be searched with the :func:`find()` method.

Let's find an option by it's name

And let's find first an option by it's name

The search can be performed in a subtree

.. code-block:: bash
    :emphasize-lines: 1, 6, 19

    print(cfg.option.find(name='var1'))
    # [<tiramisu.api.TiramisuOption object at 0x7f490a530f98>, <tiramisu.api.TiramisuOption object at 0x7f490a530748>]

    # If the option name is unique, the search can be stopped once one matched option
    # has been found:
    print(cfg.option.find(name='var1', first=True))
    # <tiramisu.api.TiramisuOption object at 0x7f6c2beae128>

    # a search object behaves like a cfg object, for example
    print(cfg.option.find(name='var1', first=True).option.name())
    # 'var1'
    print(cfg.option.find(name='var1', first=True).option.doc())

    # a search can be made with various criteria
    print(cfg.option.find(name='var3', value=undefined))
    print(cfg.option.find(name='var3', type=StrOption))

    # the find method can be used in subconfigs
    print(cfg.option('od2').find('var1'))

:download:`download the config used for the find <src/find.py>`

The `get` flattening utility
-------------------------------------

In a config or a subconfig, you can print a dict-like representation

.. code-block:: bash
    :emphasize-lines: 2

    # get the `od1` option description
    print(cfg.option('od1').value.get())
    {'od1.var1': 'éééé', 'od1.var2': 'value'}
