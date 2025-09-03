
How do I integrate a unit test?
-------------------------------

Note that the example below is kept generic and therefore doesn't reflect
any actual directory layout or any actual file naming conventions.
Internal guidelines still need to be applied by the user.

Assume that the file hierarchy of your component looks like this:

* src
    * core.c
    * core.h
* test
    * unittest-core.cpp
* BUILD.gn

To integrate the unit test **unittest-core.cpp** into the build system, add
the lines below into the **BUILD.gn** file.

.. code-block::

    unittest("core") {
      # The file containing the code getting unit tested
      source = "src/core.c"
      include_dirs = [ "src" ]
      # The files containing the test cases.
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
**unittest** target in the found **BUILD.gn** file if it isn't listed there yet.
