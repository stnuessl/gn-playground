Use Cases
=========

Note that the shown examples in this section are kept generic and therefore
do not reflect any actual directory layout or any actual file naming
conventions. All effective internal guidelines still need to be applied by the user.

How do I integrate a software component?
----------------------------------------

Assume that the file hierarchy of the project looks like this:

* core/
    * src/
        * core.c
        * core.h
    * BUILD.gn
* BUILD.gn

To integrate the component **core** into the build system, add
the code below into the component's **BUILD.gn** file. Additionaly, remove
the comments which are only shown here for explanatory reasons.
Make sure to `format the file appropriately <#how-do-i-format-gn-files>`_.

.. code-block::

    import("//gn/component/component.gni")

    component("core") {
      sources = [
        "src/core.c",
        "src/core.h",
      ]
      include_dirs = [ "src" ]
      configs = [
        # ... project-specific ...
      ]
      deps = [
        # ... target-specifc ...
      ]
    }

Finally, navigate to the **BUILD.gn** file containing the binary, into which you
want to integrate your component. Here we assume it is the top-level
**BUILD.gn** file shown in the file hierarchy above.

.. code-block::

    import("//gn/binary/binary.gni")

    binary("app") {
      # ... some variables ...
      deps = [
        # ... some other deps ...
        "//core:core",
      ]
    }

How do I integrate a unit test?
-------------------------------

Assume that the file hierarchy of your component looks like this:

* src/
    * core.c
    * core.h
* test/
    * unittest-core.cpp
* BUILD.gn

To integrate the unit test **unittest-core.cpp** into the build system, add
the code below into the component's **BUILD.gn** file. Additionaly, remove
the comments which are only shown here for explanatory reasons.
Make sure to `format the file appropriately <#how-do-i-format-gn-files>`_.

.. code-block::

    import("//gn/unittest/unittest.gni")

    unittest("core") {
      source = "src/core.c"
      include_dirs = [ "src" ]
      tests = [ test/unittest-core.cpp" ]
    }

    # ... more unit tests ...

    unittest_group("unittest") {
      deps = [
        ":core",
        # ... more unit tests ...
      ]
    }

Navigate in the directory hierarchy towards the root and find the next
**BUILD.gn** file. Add **your unittest** target as a dependency to the
found **BUILD.gn** file.

How do I format GN Files?
-------------------------

Command-Line
^^^^^^^^^^^^

.. code-block:: sh

    gn format <file>

