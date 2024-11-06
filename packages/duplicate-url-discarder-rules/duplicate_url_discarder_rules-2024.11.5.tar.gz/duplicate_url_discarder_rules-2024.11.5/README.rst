=============================
duplicate-url-discarder-rules
=============================

.. image:: https://img.shields.io/pypi/v/duplicate-url-discarder-rules.svg
   :target: https://pypi.python.org/pypi/duplicate-url-discarder-rules
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/duplicate-url-discarder-rules.svg
   :target: https://pypi.python.org/pypi/duplicate-url-discarder-rules
   :alt: Supported Python Versions

.. image:: https://github.com/zytedata/duplicate-url-discarder-rules/workflows/tox/badge.svg
   :target: https://github.com/zytedata/duplicate-url-discarder-rules/actions
   :alt: Build Status:

This contains rules for https://github.com/zytedata/duplicate-url-discarder.

Quick Start
***********

Installation
============

.. code-block::

    pip install duplicate-url-discarder-rules

Using
=====

The rules can be imported via:

.. code-block:: python

    from duplicate_url_discarder_rules import RULE_PATHS

It can then be used to configure the ``DUD_LOAD_RULE_PATHS`` setting of
``duplicate-url-discarder``.

``RULE_PATHS`` contains all files shipped in this package. If you want to
reduce the number of loaded rules to improve performance you can instead
use one or more of the following variables:

* ``RULE_PATHS_COMMON``: rules not specific to any data type.
* ``RULE_PATHS_ARTICLE``: rules for article websites.
* ``RULE_PATHS_PRODUCT``: rules for e-commerce websites.

As all of them are lists, you can combine them (e.g.
``RULE_PATHS_COMMON + RULE_PATHS_PRODUCT``).
