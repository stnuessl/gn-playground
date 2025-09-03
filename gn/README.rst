GN (Generate Ninja)
===================

This directory contains the configuration, templates, utilities and checks
contained within this repositories software build.

Public Available Import Files
-----------------------------

The **.gni** files below can be freely imported into any **gn** related file
within the repository without hesitation.

* `//gn/binary/binary.gni <binary/binary.gni>`_
* `//gn/component/component.gni <component/component.gni>`_
* `//gn/unittest/unittest.gni <unittest/unittest.gni>`_
* `//gn/python/python.gni <python/python.gni>`_
* `//gn/capture-output/capture-output.gni <capture-output/capture-output.gni>`_

Other files require previously granted approval from the build system
maintainers. As a consequence of such an approval, the above list must be
updated **by the approving maintainer**.

File and Directory Naming Convention
------------------------------------

Keep file and directory names in lower-case and separate words with hyphens.
The obvious exceptions to this rule are **BUILD.gn** and **README** files.

