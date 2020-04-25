========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
.. |docs| image:: https://readthedocs.org/projects/lazymaker/badge/?style=flat
    :target: https://readthedocs.org/projects/lazymaker
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/dougmvieira/lazymaker.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/dougmvieira/lazymaker

.. |codecov| image:: https://codecov.io/gh/dougmvieira/lazymaker/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/dougmvieira/lazymaker

.. |version| image:: https://img.shields.io/pypi/v/lazymaker.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/lazymaker

.. |wheel| image:: https://img.shields.io/pypi/wheel/lazymaker.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/lazymaker

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/lazymaker.svg
    :alt: Supported versions
    :target: https://pypi.org/project/lazymaker

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/lazymaker.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/lazymaker



.. end-badges

Minimalistic build system for Python using memoisation

* Free software: MIT license

Installation
============

::

    pip install lazymaker

You can also install the in-development version with::

    pip install https://github.com/dougmvieira/lazymaker/archive/master.zip


Documentation
=============


https://lazymaker.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
