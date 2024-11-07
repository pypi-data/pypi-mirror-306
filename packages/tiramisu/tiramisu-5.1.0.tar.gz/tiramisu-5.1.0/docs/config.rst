The :class:`Config`
====================

Tiramisu is made of almost three main classes/concepts :

- the :class:`Option` stands for the option types
- the :class:`OptionDescription` is the schema, the option's structure
- the :class:`Config` which is the whole configuration entry point

.. image:: config.png

The handling of options
~~~~~~~~~~~~~~~~~~~~~~~~~~

The handling of options is split into two parts: the description of
which options are available, what their possible values and defaults are
and how they are organized into a tree. A specific choice of options is
bundled into a configuration object which has a reference to its option
description (and therefore makes sure that the configuration values
adhere to the option description).

.. toctree::
    :maxdepth: 2

    option
    options
    symlinkoption
    own_option

Option description are nested Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :class:`Option` (in this case the :class:`BoolOption`),
are organized into a tree into nested
:class:`~tiramisu.option.OptionDescription` objects.

Every option has a name, as does every option group.

.. toctree::
    :maxdepth: 2

    optiondescription
    dynoptiondescription
    leadership


Config
~~~~~~

Let's perform a *Getting started* code review :

.. literalinclude:: src/getting_started.py
   :lines: 1-12
   :linenos:
   :name: GettingStarted

Let's review the code. First, line 7, we create an :class:`OptionDescription` named `optgroup`.

.. literalinclude:: src/getting_started.py
   :lines: 4, 6-7
   :emphasize-lines: 3

Option objects can be created in different ways, here we create a
:class:`BoolOption`

.. literalinclude:: src/getting_started.py
   :lines: 4, 8-9
   :emphasize-lines: 3

Then, line 12, we make a :class:`Config` with the :class:`OptionDescription` we
built :

.. literalinclude:: src/getting_started.py
   :lines: 3, 12
   :emphasize-lines: 2

Here is how to print our :class:`Config` details:

.. literalinclude:: src/getting_started.py
   :lines: 15

.. code-block:: bash

    Root config object that enables us to handle the configuration options
    
    Commands:
        description              Get option description
        dict                     Convert config and option to tiramisu format
        get                      Get Tiramisu option
        has_dependency           Test if option has dependency
        isdynamic                Test if option is a dynamic optiondescription
        isleadership             Test if option is a leader or a follower
        isoptiondescription      Test if option is an optiondescription
        list                     List options (by default list only option)
        name                     Get option name
        option                   Select an option by path
        path                     Get option path
        type                     Get de option type
        updates                  Updates value with tiramisu format

Then let's print our :class:`Option` details.

.. literalinclude:: src/getting_started.py
   :lines: 17

.. code-block:: bash

    Manage selected option
    
    Commands:
        dependencies             Get dependencies from this option
        description              Get option description
        dict                     Convert config and option to tiramisu format
        extra                    Get de option extra
        followers                Get the followers option for a leadership
        get                      Get Tiramisu option
        group_type               Get type for an optiondescription (only for optiondescription)
        has_dependency           Test if option has dependency
        identifiers              Get identifiers for dynamic option
        index                    Get index of option
        isdynamic                Test if option is a dynamic optiondescription
        isfollower               Test if option is a follower
        isleader                 Test if option is a leader
        isleadership             Test if option is a leader or a follower
        ismulti                  Test if option could have multi value
        isoptiondescription      Test if option is an optiondescription
        issubmulti               Test if option could have submulti value
        issymlinkoption          Test if option is a symlink option
        leader                   Get the leader option for a leadership or a follower option
        list                     List options inside an option description (by default list only option)
        name                     Get option name
        option                   For OptionDescription get sub option, for symlinkoption get the linked option
        path                     Get option path
        pattern                  Get the option pattern
        type                     Get de option type
        updates                  Updates value with tiramisu format

Finaly, let's print the :class:`Config`.

.. literalinclude:: src/getting_started.py
   :lines: 19

.. code-block:: bash

    <Config path=None>

:download:`download the getting started code <src/getting_started.py>`

Go futher with `Option` and `Config`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
    :maxdepth: 2

    property
    validator
    calculation
