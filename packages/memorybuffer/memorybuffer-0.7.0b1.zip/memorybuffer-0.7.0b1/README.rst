memorybuffer
============

Python buffer protocol.

Overview
========

| Provides routines to implement `Python Buffer Protocol`_ in clean Python
| instead of C extension class.
| TODO...

`PyPI record`_.

`Documentation`_.

Installation
============

Prerequisites:

+ Python 3.9 or higher

  * https://www.python.org/

+ pip and setuptools

  * https://pypi.org/project/pip/
  * https://pypi.org/project/setuptools/

To install run:

  .. parsed-literal::

    python -m pip install --upgrade |package|

Development
===========

Prerequisites:

+ Development is strictly based on *tox*. To install it run::

    python -m pip install --upgrade tox

Visit `Development page`_.

Installation from sources:

clone the sources:

  .. parsed-literal::

    git clone |respository| |package|

and run:

  .. parsed-literal::

    python -m pip install ./|package|

or on development mode:

  .. parsed-literal::

    python -m pip install --editable ./|package|

License
=======

  | |copyright|
  | Licensed under the zlib/libpng License
  | https://opensource.org/license/zlib
  | Please refer to the accompanying LICENSE file.

Authors
=======

* Adam Karpierz <adam@karpierz.net>

.. |package| replace:: memorybuffer
.. |package_bold| replace:: **memorybuffer**
.. |copyright| replace:: Copyright (c) 2012-2024 Adam Karpierz
.. |respository| replace:: https://github.com/karpierz/memorybuffer.git
.. _Development page: https://github.com/karpierz/memorybuffer
.. _PyPI record: https://pypi.org/project/memorybuffer/
.. _Documentation: https://memorybuffer.readthedocs.io/
.. _Python Buffer Protocol: https://docs.python.org/3/c-api/buffer.html
