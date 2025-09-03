#!/usr/bin/env bash
#
# The MIT License (MIT)
#
# Copyright (c) 2026 Steffen Nuessle
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
import sys

import git


def main():
    if len(sys.argv) <= 1:
        # Check all files.
        repo = git.Repo(search_parent_directories=True)
        data = (
            item.path
            for item in repo.head.commit.tree.traverse()
            if item.type == 'blob'
        )
    else:
        data = sys.argv[1:]

    excludes = {
        # Compilers rely on uppercase file extensions to decide whether to
        # preprocess the passed in source file or not.
        '.S'
    }

    # Fail if there is an uppercase letter in any filenames extension.
    exit_code = 0
    for name in data:
        _, ext = os.path.splitext(name)

        if ext in excludes:
            continue

        if not any(x.isupper() for x in ext):
            continue

        print(
            f'{name}: error: file contains at least one uppercase letter in '
            f'its extension "{ext}"',
            file=sys.stderr,
        )
        exit_code = 1

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
