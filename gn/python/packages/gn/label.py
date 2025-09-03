#!/usr/bin/env python
#
# The MIT License (MIT)
#
# Copyright (c) 2025 Steffen Nuessle
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import os

from . import lib


def get_name(label):
    """Returns the name of a label.

    Example:
        '//a/b:c' will return 'c'
        '//a/b    will return 'b'
    """
    if ':' in label:
        name = label.rsplit(':', maxsplit=1)[-1]
    else:
        name = label.rsplit('/', maxsplit=1)[-1]

    return name


def get_dir(label):
    """Returns the directory of a label.

    Example:
        '//a/b:c' will return '//a/b'
        '//a/b    will return '//a/b'
    """
    return label.rsplit(':', maxsplit=1)[0]


def as_abspath(label, root=None):
    if not root:
        root = lib.root()

    label = get_dir(label)
    label = label.removeprefix('//')

    return os.path.join(root, label)


def as_relpath(label, root=None, start=None):
    if not start:
        start = os.getcwd()

    abspath = as_abspath(label, root)

    return os.path.relpath(abspath, start)


def get_referenced_build_file(label):
    """Returns the directory of a label.

    Example:
        '//a/b:c' will return '//a/b/BUILD.gn'
    """

    dir_path = get_dir(label)
    return f'{dir_path}/BUILD.gn'


def has_toolchain(label):
    """Returns true if the label contains a specific toolchain."""
    return '(' in label


def remove_toolchain(label):
    """Returns the label with a potentially specified toolchain removed.

    Example:
        '//a/b:c(//x/y:z)' will return '//a/b:c'
    """
    return label.rsplit('(', maxsplit=1)[0]
