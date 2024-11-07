==========================================================
Dynamic option description: :class:`DynOptionDescription`
==========================================================

Dynamic option description
==============================================

Dynamic option description is an :class:`OptionDescription` which multiplies according to the return of a function.

.. list-table:: 
   :widths: 15 45
   :header-rows: 1

   * - Parameter
     - Comments

   * - name
     - The `name` is important to retrieve this option.

   * - doc
     - The `description` allows the user to understand where this option will be used for.

   * - children
     - The list of children (Option) include inside.

       Note:: the option can be an :doc:`option` or an other option description

   * - identifiers
     - Identifiers is a :doc:`calculation` that return the list of identifiers used to create dynamic option description.

   * - properties
     - A list of :doc:`property` (inside a frozenset().

   * - informations
     - We can add default informations to this option description.

   * - group_type
     - Type for this group.

Example
==============

Let's try:

>>> from tiramisu import StrOption, DynOptionDescription, Calculation
>>> def return_identifiers():
...    return ['1', '2']
>>> child1 = StrOption('first', 'First basic option ')
>>> child2 = StrOption('second', 'Second basic option ')
>>> DynOptionDescription('basic ',
...                      'Basic options ',
...                      [child1, child2],
...                      Calculation(return_identifiers))

This example will construct:

- Basic options 1:

  - First basic option 1
  - Second basic option 1

- Basic options 2:

  - First basic option 2
  - Second basic option 2
