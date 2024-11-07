.. default-role:: literal

.. meta::

   :description: python tiramisu library user documentation
   :keywords: python, tiramisu, tutorial

.. title:: Tiramisu

The tasting of `Tiramisu` --- `user documentation`
===================================================

.. image:: logo.png
   :height: 150px

`Tiramisu`

    - is a cool, refreshing Italian dessert,

    - it is also an `options controller tool`_.

.. _`options controller tool`: http://en.wikipedia.org/wiki/Configuration_management#Overview


It's a pretty small, local (that is, straight on the operating system) options
handler and controller.


.. toctree::
    :maxdepth: 2

    gettingstarted
    config
    browse
    api_value
    api_property
    application
    quiz
    glossary

.. External project:
.. 
.. .. toctree::
..     :maxdepth: 2
.. 
..     cmdline_parser

.. FIXME ca veut rien dire : "AssertionError: type <class 'tiramisu.autolib.Calculation'> invalide pour des propriétés pour protocols, doit être un frozenset"


.. FIXME changer le display_name !
.. FIXME voir si warnings_only dans validator !
.. FIXME submulti dans les leadership
.. FIXME exemple avec default_multi (et undefined)
.. FIXME config, metaconfig, ...
.. FIXME fonction de base
.. FIXME information
.. FIXME demoting_error_warning, warnings, ...
.. FIXME class _TiramisuOptionOptionDescription(CommonTiramisuOption):
.. FIXME class _TiramisuOptionOption(_TiramisuOptionOptionDescription):
.. FIXME class TiramisuOptionInformation(CommonTiramisuOption):
.. FIXME class TiramisuContextInformation(TiramisuConfig):
.. FIXME expire
.. FIXME custom display_name
.. FIXME     assert await cfg.cache.get_expiration_time() == 5
.. FIXME    await cfg.cache.set_expiration_time(1)
.. FIXME convert_suffix_to_path



Indices and full bunch of code
===============================


* `All files for which code is available <_modules/index.html>`_
* :ref:`genindex`
* :ref:`search`
