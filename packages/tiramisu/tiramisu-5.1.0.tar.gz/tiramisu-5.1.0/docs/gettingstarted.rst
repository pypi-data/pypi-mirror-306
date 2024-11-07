==================================
Getting started
==================================

What is options handling?
=================================

Due to more and more available options required to set up an operating system,
compiler options or whatever, it became quite annoying to hand the necessary
options to where they are actually used and even more annoying to add new
options.

To circumvent these problems the configuration control was introduced.

What is Tiramisu?
===================

Tiramisu is an options handler and an options controller, which aims at
producing flexible and fast options access. The main advantages are its access
rules and the fact that the whole consistency is preserved at any time.

There is of course type and structure validations, but also
validations towards the whole options. Furthermore, options can be reached and
changed according to the access rules from nearly everywhere.

Installation
-------------

The best way is to use the python pip_ installer

.. _pip: https://pip.pypa.io/en/stable/installing/

And then type:

.. code-block:: bash

    pip install tiramisu

Advanced users
==============

.. _gettingtiramisu:

- the library's development homepage is there_

.. _there: https://forge.cloud.silique.fr/stove/tiramisu/

To obtain a copy of the sources, check it out from the repository using `git`.
We suggest using `git` if one wants to access to the current developments.

.. code-block:: bash

    git clone https://forge.cloud.silique.fr/stove/tiramisu.git

This will get you a fresh checkout of the code repository in a local directory
named ``tiramisu``.

