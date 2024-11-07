==========================================================
Leadership OptionDescription: :class:`Leadership`
==========================================================

A leadership is a special `OptionDescription` that wait a leader and one or multiple followers.

Leader and follower are multi option. The difference is that the length is defined by the length of the option leader.

If the length of leader is 3, all followers have also length 3.

An other different is that the follower is isolate. That means that you can only change on value on a specified index in the list of it's values.
If a value is mark as modified in a specified index, that not affect the other values in other index.

The leadership
==============================================

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

       Note:: the option has to be multi or submulti option and not other option description.

   * - properties
     - A list of :doc:`property` (inside a frozenset().

   * - informations
     - We can add default informations to this option description.

Example
====================

Let's try:

>>> from tiramisu import StrOption, Leadership
>>> users = StrOption('users', 'User', multi=True)
>>> passwords = StrOption('passwords', 'Password', multi=True)
>>> Leadership('users',
...            'User allow to connect',
...            [users, passwods])
