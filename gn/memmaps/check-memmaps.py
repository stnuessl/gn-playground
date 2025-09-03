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
import itertools
import json
import sys

import util


def main():
    parser = argparse.ArgumentParser(
        description=(
            'Check whether all memory mapping header files were known at '
            'build generation time.'
        )
    )
    parser.add_argument(
        '--dependencies',
        help='A JSON file containing known file dependencies.',
        required=True,
        type=lambda x: json.load(open(x, 'r')),
    )
    parser.add_argument(
        '--memmaps',
        help=(
            'A file containing all the memory mapping header files known at '
            'build generation time.'
        ),
        required=True,
        type=lambda x: {value for x in open(x, 'r') if (value := x.strip())},
    )
    parser.add_argument(
        '--include',
        help='A list of globs used to identify memory mapping headers.',
        nargs='+',
        default=['*MemMap*.h'],
        type=str,
    )
    parser.add_argument(
        '--exclude',
        help='A list of globs used to exclude files from the check.',
        nargs='*',
        default=[],
        type=str,
    )

    args = parser.parse_args()

    deps = itertools.chain(*(item['deps'] for item in args.dependencies))
    memmaps = {
        item
        for item in deps
        if util.any_fnmatch(item, args.include)
        and not util.any_fnmatch(item, args.exclude)
    }

    missing = memmaps.difference(args.memmaps)
    unused = args.memmaps.difference(memmaps)

    for item in missing:
        print(
            f'{item}: error: unspecified memory mapping file', file=sys.stderr
        )

    for item in unused:
        print(f'{item}: error: unused memory mapping file', file=sys.stderr)

    exit_code = len(missing) != 0 or len(unused) != 0
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
