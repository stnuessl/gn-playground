=====================
Component Integration
=====================

This document schematically describes how to integrate a component
into the software build. Text placeholders like `{{ variable }}` must be
substituted wherever appropriate.
The integration roughly consists of three parts and each part is described in
one of the sections below.

.. contents:: \
    :depth: 1


If any of the below steps do not just *simply work* reach out for support to
the build system maintainers.


Software Component BUILD.gn file
================================

Assume your component's BUILD.gn is located at
``//{{ project_directory }}/{{ binary_name }}/{{ component }}:BUILD.gn``,
to have your component integrated into the software build, the file must
roughly look like shown below.

.. code-block:: text

    import("//gn/component/component.gni")
    import("//gn/unittest/unittest.gni")

    component("{{ name }}") {
      sources = [
        "{{ file1 }}.c",
        "{{ file1 }}.h",
        "{{ file2 }}.c",
        "{{ file2 }}.h",
      ]
      include_dirs = [
        "{{ path1 }}",
        "{{ path2 }}",
      ]
      configs = [ "{{ project-binary-config }}" ]
    }

    unittest("{{ file1 }}") {
      source = "{{ file1 }}.c"
      tests = [ "{{ file1 }}.cpp" ]
      include_dirs = [
        "{{ path1 }}",
        "{{ path2 }}",
      ]
    }

    unittest("{{ file2 }}") {
      source = "{{ file2 }}.c"
      tests = [ "{{ file2 }}.cpp" ]
      include_dirs = [
        "{{ path1 }}",
        "{{ path2 }}",
      ]
    }

    unittest_group("unittest") {
      deps = [
        ":{{ file1 }}",
        ":{{ file2 }}",
      ]
    }

Binary-specific memmaps.gni file
================================

There is a ``memmaps.gni`` file specifically for the binary into which you
want to integrate your component. The file is located at
``//{{ project_directory }}/{{ binary_directory }}/gn/memmaps/memmaps.gni``.
Extend the file as shown below.

.. code-block:: text

    # ...

    {{ project_name }}_{{ binary_name }}_memmaps = [
      # ...
      "{{ file1 }}.h"
      "{{ file2 }}.h"
    ]

Binary-specific BUILD.gn file
=============================

Finally, the binary-specific ``BUILD.gn`` file at
``//{{ project_directory}}/{{ binary_directory }}/BUILD.gn``
must be extended as shown below.

.. code-block:: text

    # ...

    binary("{{ name }}") {
      # ...
      deps = [
        "//{{ project_directory }}/{{ binary_name }}/{{ component }}:{{ name }}"
      ]
    }

    group("unittest") {
      testonly = true
      deps = [
        # ...
        "//{{ project_directory }}/{{ binary_name }}/{{ component }}:unittest"
      ]

    }


