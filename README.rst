=============
gn-playground
=============

.. image:: https://github.com/stnuessl/gn-playground/actions/workflows/build.yaml/badge.svg
   :alt: Build
   :target: https://github.com/stnuessl/gn-playground/actions

.. image:: https://img.shields.io/badge/License-MIT-blue.svg
   :alt: License: MIT
   :target: https://mit-license.org/

A repository to learn `gn <https://gn.googlesource.com/gn>`_.

.. contents::


How to Get Started
==================

This chapter describes how to install the tools required for this repository
and how to build its software. Almost everything can be adjusted
to a specific use-case. However, for the sake of brevity, the reader
is encouraged to familiarize themselves with build tools like
`gn <https://gn.googlesource.com/gn>`_ and `ninja <https://ninja-build.org/>`_,
and so the sections below will only focus on the most trivial and common use
cases to get you started.

Download the Repository
-----------------------

Use `git <https://git-scm.com>`_ to download the repository.

.. code-block:: sh

    git clone https://github.com/stnuessl/gn-playground

After the command finishes, please switch your working directory to the root
directory of the downloaded repository to ensure the commands in the upcoming
sections will execute successfully.


Tool Installation
-----------------

Tools are automatically installed during the build configuration step.
However, since this might take a long time for the very first build invocation,
it is highly recommended to run the following command manually.

.. code-block:: sh

    ninja -C gn/toolchains -f install.ninja

Software Build
--------------


#. Configure the build.

    .. code-block:: sh

        gn gen build


    This command will prepare the **build** directory so it can be used for
    building software.

#. Execute the software build.

    .. code-block:: sh

        ninja -C build

    This command will build all binary outputs. They will be located in
    **build/bin**.


Unit Tests
----------

The command below will execute all unit tests and generate a coverage report
for them.

.. code-block:: sh

    ninja -C build unittest


Further Documentation
=====================

Style Guides
------------

* `C Coding Style Guide <docs/c-coding-style-guide.rst>`_
* `GN Style Guide <gn/docs/style-guide.rst>`_

Internal Checks
---------------

Internal checks are used to ensure the correct and intended use of the software
build. The list below summarizes these checks.

* `//gn/clang-format:check  <gn/docs/checks.rst#clang-format-check>`_
* `//gn/clang-tidy:check  <gn/docs/checks.rst#clang-tidy-check>`_
* `//gn/compile-commands:check <gn/docs/checks.rst#compile-commands-check>`_
* `//gn/memmaps:check <gn/docs/checks.rst#memmaps-check>`_
* `//gn/metadata:check <gn/docs/checks.rst#metadata-check>`_
* `//gn/targets:check <gn/docs/checks.rst#targets-check>`_
* `//gn/unittest:check <gn/docs/checks.rst#unit-test-check>`_

Integration
-----------

* `Component Integration <gn/docs/component-integration.rst>`_


