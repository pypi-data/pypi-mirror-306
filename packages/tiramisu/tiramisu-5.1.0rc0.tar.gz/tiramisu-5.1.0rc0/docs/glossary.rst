.. default-role:: literal

Glossary
==========

.. glossary::

    configuration

        Global configuration object, wich contains the whole configuration
        options *and* their descriptions (option types and group)

    schema
    option description

        see :class:`tiramisu.option.OptionDescription`

        The schema of a configuration :

        - the option types

        - how they are organised in groups or even subgroups, that's why we
          call them **groups** too.

    configuration option

        An option object wich has a name and a value and can be accessed
        from the configuration object

    access rules

        Global access rules are : :meth:`~config.CommonConfig.read_write()` or
        :meth:`~config.Config.read_only()`

    default value

        Default value of a configuration option. The default value can be
        set at instanciation time, or even at any moment. Remember that if
        you reset the default value, the owner reset to `default`

    freeze

        A whole configuration can be frozen (used in read only access).

        A single option can be frozen too.

    value owner

        When an option is modified, including at the instanciation, we
        always know who has modified it. It's the owner of the option.

    properties

        an option with properties is a option wich has property like 'hidden' or 'disabled' is an option
        wich has restricted acces rules.

    hidden option

        a hidden option has a different behaviour on regards to the access
        of the value in the configuration.

    disabled option

        a disabled option has a different behaviour on regards to the access
        of the value in the configuration.

    mandatory option

        A mandatory option is a configuration option wich value has to be
        set, that is the default value cannot be `None`.

    consistency

        Preserving the consistency in a whole configuration is a tricky thing,
        tiramisu takes care of it for you.

    context

        The context is a :class:`tiramisu.setting.Setting()` object in the
        configuration that enables us to access to the global properties

        for example the `read_write` or `read_only` :term:`access rules`


