============
Build Checks
============

.. contents::
    :depth: 1

If you running into trouble with one of the checks on this page, it is probably
best to read the document describing the
`component integration <component-integration.rst>`_ into the software build to
get your issues resolved.

Clang-Format Check
==================

Description
-----------

Rationale
---------

Clang-Tidy Check
================

Description
-----------

This check ensures that for every source file participating in the software
build there is an appropriate clang-tidy target for it which can be used
for source code analyis.

Rationale
---------

Static code analysis and linting improves software quality which positively
correlates with `developer productivity
<https://research.google/pubs/what-improves-developer-productivity-at-google-code-quality/>`_.

Compile Commands Check
======================

Description
-----------

This check ensures that every C and C++ source file participating in the build
has an appropriate entry in the ``compile_commands.json`` file at the top of the
build directory.

Rationale
---------

A valid ``compile_commands.json`` allows the project to be seamlessly integrated
into code editors and integrated development environments. This enables
us to use features like *code-completion*, *jump-to-definition*,
*error-highlighting* and *cross-referencing*, thus boosting developer
productivity.



MemMaps Check
=============

Description
-----------

This check ensures that each memory mapping header file is explicitly defined
within the software build.


Rationale
---------

Due to their nature, memory mapping header files are highly compiler-specific
and therefore a huge burden for any integrated development environment or code
editor. This approach allows to deal with such files and offer a better
integration into the user's development enviornment.

Metadata Check
==============

Description
-----------

Used to check that all files participating in the software build are correctly
attributed with metadata.


Rationale
---------

Our automation needs a mechanism to track supplier and other
important information for each file participating in the software build.


Targets Check
=============

Description
-----------

This check ensures that all build targets adhere to the defined naming
conventions. Roughly, all targets need to be typed in lower-case letters and
words are supposed to be separated by a hyphen. The exact regex which is used
to check the target names can be seen in the script
`check-targety.py <../targets/check-targets.py>`_.


Rationale
---------

The use of naming conventions allow for a uniform look and feel which improves
readability. The specified naming convention is supposed to make the build
targets easier to type on the command-line and within automation scripts.


Unit Test Check
===============

Description
-----------

This check ensures that each C source file participating in the software build
is associated with a unit test and that the unit test is part of the
**unittest** build target.


Rationale
---------

Unit tests form the backbone of our verifcation and validation strategy and
are therefore mandatory.


