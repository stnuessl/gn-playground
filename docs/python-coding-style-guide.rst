Python Coding Style Guide
=========================

The python ecosystem offers a wide variety of world-class tools. We therefore
don't have to rely on manually written coding guidelines and manual reviews
for those guidelines, but instead we'll enforce them by automated checks.

This document briefly summarizes the most important use-cases which any
software developer should be familiar with.

Linting Python Code
-------------------

To check python code for obvious coding issues, run the command below
in a terminal.

.. code-block:: sh

    uv run ruff check


Formatting Python Code
----------------------

To automatically format python code, run the command below in a terminal:

.. code-block:: sh

    uv run ruff format

Using Ninja for Checking Python Code
------------------------------------

Simply invoke the command below to check the linting and formatting of python
code:

.. code-block:: sh

    ninja check-python


Further Documentation
---------------------

If you are interested in some of the details related to python linting and
code formatting, feel free to have a look at the links below:

* `PEP 8: Style Guide for Python Code <https://peps.python.org/pep-0008/>`_
* `Ruff: An extremely fast Python linter and code formatter
  <https://docs.astral.sh/ruff/>`_
* `Flake8: Your Tool For Style Guide Enforcement
  <https://flake8.pycqa.org/en/latest/>`_
