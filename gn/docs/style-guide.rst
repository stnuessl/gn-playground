GN Style Guide
==============

* Apply the official `gn style guide
  <https://gn.googlesource.com/gn/+/main/docs/style_guide.md>`_.

* Ignore Chromium- or Fuchsia-specific instructions.

* Targets shall be all lower case letters with hyphens to separate words.

* Targets which shall always be rebuilt shall declare an output with
  *$target_gen_dir/$target_name.non-existant*
