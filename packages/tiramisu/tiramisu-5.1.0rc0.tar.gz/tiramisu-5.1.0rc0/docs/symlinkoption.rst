====================================================
The symbolic link option: :class:`SymLinkOption`
====================================================

A `SymLinkOption` is an option that actually points to another option.

Each time we will access to a properties of this options, we will have in return the value of other option.

Creation a `SymLinkOption` is easy:

>>> from tiramisu import StrOption, SymLinkOption
>>> st = StrOption('str', 'str')
>>> sym = SymLinkOption('sym', st)
