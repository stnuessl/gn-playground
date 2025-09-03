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
import fnmatch
import sys

import gn


def any_fnmatch(data, globs, *, key=lambda x: x):
    return any(fnmatch.fnmatch(key(data), glob) for glob in globs)


def main():
    parser = argparse.ArgumentParser(
        description=(
            'Checks whether a specific target contains a selected set of '
            'source files.'
        )
    )
    parser.add_argument(
        '--exclude',
        help='Exclude sources matching one of the specified glob(s).',
        nargs='*',
        default=[],
        type=str,
    )
    parser.add_argument(
        '--description',
        help='The builds processed description file.',
        required=True,
        type=gn.desc.Description.from_file,
    )
    parser.add_argument(
        '--include',
        help=(
            'Only include sources matching the specified glob(s) in the check.'
        ),
        required=False,
        nargs='*',
        default=['*.c', '*.cc', '*.cpp', '*.cxx'],
        type=str,
    )
    parser.add_argument(
        '--target',
        help='The build target supposed to contain the selected sources.',
        required=True,
        type=str,
    )

    args = parser.parse_args()

    sources = set(
        args.description.get_if(lambda x: len(x.get('sources')) != 0).extract(
            'sources',
            flatten=True,
            predicate=lambda x: any_fnmatch(x, args.include)
            and not any_fnmatch(x, args.exclude),
        )
    )

    available = set(
        args.description.get_subdesc(args.target)
        .get_if(lambda x: len(x.get('sources')) != 0)
        .extract('sources', flatten=True)
    )

    missing = [path for path in sources if path not in available]

    for source in missing:
        print(
            f"error: {source}: not listed as a source of '{args.target}'",
            file=sys.stderr,
        )

    exit_code = len(missing) != 0
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
