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


def any_fnmatch(path, globs):
    return any(fnmatch.fnmatch(path, glob) for glob in globs)


def main():
    parser = argparse.ArgumentParser(
        description=(
            'Ensure that a unit test exists for each source file used in the '
            'software build'
        )
    )
    parser.add_argument(
        'metadata',
        help="The project's metadata file.",
        type=gn.metadata.Metadata.from_file,
    )
    parser.add_argument(
        '--exclude',
        help='Exclude sources matching one of the specified glob(s).',
        nargs='*',
        default=[],
        type=str,
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

    args = parser.parse_args()

    sources = set(
        args.metadata.get_if(lambda x: x['template'] in {'binary', 'component'})
        .get_if(lambda x: any_fnmatch(x['source'], args.include))
        .get_if(lambda x: not any_fnmatch(x['source'], args.exclude))
        .extract('source')
    )

    available = set(
        args.metadata.get_if(lambda x: x['template'] == 'unittest').extract(
            'validates'
        )
    )

    missing = sources.difference(available)

    for item in missing:
        print(f'{item}: error: no unit test available', file=sys.stderr)

    exit_code = len(missing) != 0

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
