==============================================
Generic container: :class:`OptionDescription`
==============================================

Option description
===================================

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
       .. note:: the option can be an :doc:`option` or an other option description

   * - properties
     - A list of :doc:`property` (inside a frozenset().

   * - informations
     - We can add default informations to this option description.

    * - group_type
      - Type for this group.

Examples
==============

>>> from tiramisu import StrOption, OptionDescription
>>> child1 = StrOption('first', 'First basic option')
>>> child2 = StrOption('second', 'Second basic option')
>>> child3 = StrOption('third', 'Third basic option')
>>> od1 = OptionDescription('od1', 'First option description', [child3])
>>> OptionDescription('basic',
...                   'Basic options',
...                   [child1, child2, od1])
