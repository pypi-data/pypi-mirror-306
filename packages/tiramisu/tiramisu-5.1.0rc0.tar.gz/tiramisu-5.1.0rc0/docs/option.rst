==================================
Instanciate an option
==================================

Option
========

.. list-table:: 
   :widths: 15 45
   :header-rows: 1

   * - Parameter
     - Comments

   * - name
     - The `name` is important to retrieve this option.

   * - doc
     - The `description` allows the user to understand where this option will be used for.

   * - default
     - For each option, we can defined a default value. This value will be the value of this option until user customize it.

       This default value is store directly in the option. So we can, at any moment we can go back to the default value.

       The default value can be a :doc:`calculation`.

   * - default_multi
     - A second default value is available for multi option, `default_multi`. This value is used when we add new value without specified a value.

       This `default_multi` must not be a list in multi purpose. For submulti, it has to be a list.

       The default_multi value can be a :doc:`calculation`.

   * - multi
     - There are cases where it can be interesting to have a list of values rather than just one.

   * - validators
     - A list of :doc:`validator`.

   * - properties
     - A list of :doc:`property` (inside a frozenset().

   * - warnings_only
     - Only emit warnings if not type validation is invalid.

   * - informations
     - We can add default informations to this option.


Examples
==========

Let's try a simple option:

>>> from tiramisu import StrOption
>>> StrOption('welcome',
...           'Welcome message to the user login')


Add a default value:

>>> from tiramisu import StrOption
>>> StrOption('welcome',
...           'Welcome message to the user login',
...           'Hey guys, welcome here!')

Or a calculated default value:

>>> from tiramisu import StrOption, Calculation
>>> def get_value():
...     return 'Hey guys, welcome here'
>>> StrOption('welcome',
...           'Welcome message to the user login',
...           Calculation(get_value))


A multi option. In this case, the default value has to be a list:

>>> from tiramisu import StrOption
>>> StrOption('shopping_list',
...           'The shopping list',
...           ['1 kilogram of carrots', 'leeks', '1 kilogram of potatos'],
...           multi=True)

The option could be a list of list, which is could submulti:

>>> from tiramisu import StrOption, submulti
>>> StrOption('shopping_list',
...           'The shopping list',
...           [['1 kilogram of carrots', 'leeks', '1 kilogram of potatos'],
...            ['milk', 'eggs']],
...           multi=submulti)

The default value can be a :doc:`calculation`. For a multi, the function have to return a list or have to be in a list:

>>> from tiramisu import StrOption, Calculation
>>> def get_values():
...     return ['1 kilogram of carrots', 'leeks', '1 kilogram of potatos']
>>> StrOption('shopping_list',
...           'The shopping list',
...           Calculation(get_values),
...           multi=True)

or

>>> from tiramisu import StrOption, Calculation
>>> def get_a_value():
...     return 'leeks'
>>> StrOption('shopping_list',
...           'The shopping list',
...           ['1 kilogram of carrots', Calculation(get_a_value), '1 kilogram of potatos'],
...           multi=True)

Add a default_multi:

>>> from tiramisu import StrOption, submulti
>>> StrOption('shopping_list',
...           'The shopping list',
...           ['1 kilogram of carrots', 'leeks', '1 kilogram of potatos'],
...           default_multi='some vegetables',
...           multi=True)
>>> StrOption('shopping_list',
...           'The shopping list',
...           [['1 kilogram of carrots', 'leeks', '1 kilogram of potatos'],
...            ['milk', 'eggs']],
...           default_multi=['some', 'vegetables'],
...           multi=submulti)

Or calculated default_multi:

>>> from tiramisu import StrOption
>>> def get_a_value():
...     return 'some vegetables'
>>> StrOption('shopping_list',
...           'The shopping list',
...           ['1 kilogram of carrots', 'leeks', '1 kilogram of potatos'],
...           default_multi=Calculation(get_a_value),
...           multi=True)
