==================================
Properties
==================================

What are properties?
==================================

The properties are a central element of Tiramisu.

Properties change the behavior of an option or make it unavailable.

Read only and read write
=================================

Config can be in two defaut mode:

read_only
-----------------------

You can get all variables in a `Config` that not disabled.

Off course, as the Config is read only, you cannot set any value to any option.
Only value with :doc`calculation` can change value.
You cannot access to mandatory variable without values. Verify that all values is set before change mode.

read_write
-----------------------

You can get all options not disabled and not hidden. You can also set all variables not frozen.

Common properties
=================================

hidden
-----------------------

Option with this property can only get value in read only mode (or for a :doc:`calculation`).
This property is used for option that user cannot modifify it's value (for example if it's value is calculated).

disabled
-----------------------

We never can access to option with this property.

frozen
-----------------------

Options with this property cannot be modified.

Special option properties
=================================

mandatory
-----------------------

You should set value for option with this properties. In read only mode we cannot access to this option if no value is set.

empty or notempty
-----------------------

Only used for multi option that are not a follower.

Mandatory for a multi means that you cannot add None as a value. But value [] is allowed. This is not permit with `empty` property.

A multi option has automaticly `empty` property. If you don't want allow empty option, just add `notempty` property when you create the option.

unique or notunique
-----------------------

Only used for multi option that are not a follower.

Raise ValueError if a value is set twice or more in a multi Option.

A multi option has automaticly `unique` property. If you want allow duplication in option, just add `notunique` property when you create the option.

permissive
-----------------------

Option with 'permissive' cannot raise PropertiesOptionError for properties set in permissive.

Config with 'permissive', whole option in this config cannot raise PropertiesOptionError for properties set in permissive.

Special Config properties
=================================

cache
-----------------------

Enable cache settings and values.

expire
-----------------------

Enable settings and values in cache expire after `expiration_time` (by default 5 seconds).

everything_frozen
-----------------------

Whole option in config are frozen (even if option have not frozen property).

validator
-----------------------

Launch validator set by user in option (this property has no effect for option validation and second level validation).

warnings
-----------------------

Display warnings during validation.

demoting_error_warning
-----------------------

All value's errors are convert to warning (ValueErrorWarning).

Own properties
=================================

There are no specific instructions for creating a property. Just add a string as property create a new property.



.. #FIXME 
.. FORBIDDEN_SET_PERMISSIVES = frozenset(['force_default_on_freeze',
..                                        'force_metaconfig_on_freeze',
..                                        'force_store_value'])
