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

import argparse
import os
import re
import sys

import util

import gn


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--exclude',
        help='Exclude sources matching one of the specified glob(s).',
        nargs='*',
        default=[],
        type=str,
    )
    parser.add_argument(
        '--description',
        help='The builds dispatched description file.',
        required=True,
        type=gn.Description.from_file,
    )
    parser.add_argument(
        '--include',
        help=(
            'Only include sources matching the specified glob(s) in the check.'
        ),
        required=False,
        nargs='*',
        default=['*.py'],
        type=str,
    )

    args = parser.parse_args()

    regex = re.compile(r'[a-z][a-z0-9]*(:?[-_][a-z][a-z0-9]*)*')

    scripts = set(
        args.description.get_if(
            lambda x: (
                x['type'] == 'action'
                and x['metadata'].get('template') == ['python']
            )
        ).extract(
            'inputs',
            flatten=True,
            predicate=lambda x: (
                util.any_fnmatch(x, args.include)
                and not util.any_fnmatch(x, args.exclude)
            ),
        )
    )

    invalid_paths = []
    for script in scripts:
        # Avoid having the build directory somehow in the path as it name
        # can be freely chosen.
        path = os.path.relpath(script, gn.root())
        trunk = os.path.splitext(path)[0]

        while trunk:
            trunk, name = os.path.split(trunk)

            if regex.fullmatch(name):
                continue

            invalid_paths.append((path, name))

    for path, name in invalid_paths:
        print(
            f"{path}: error: invalid name '{name}' in script path",
            file=sys.stderr,
        )

    exit_code = len(invalid_paths) != 0
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
