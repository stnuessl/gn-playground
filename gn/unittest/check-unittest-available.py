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
import sys

import util

import gn


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
        type=gn.Metadata.from_file,
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

    # Get all source files used in the software build.
    sources = set(
        args.metadata.get_if(
            lambda x: (
                x['testonly'] is False
                and x['template'] in {'binary', 'component'}
                and util.any_fnmatch(x['source'], args.include)
                and not util.any_fnmatch(x['source'], args.exclude)
            )
        ).extract('source')
    )

    # Map labels to source files. The required labels of test-only components
    # will be unique within the build. Other labels will be also listed in the
    # map but they will not be used.
    source_map = {
        item['target']: item['source']
        for item in args.metadata.get_if(
            lambda x: (
                x['testonly'] is True
                and x['template'] in {'binary', 'component'}
            )
        )
    }

    # Get metadata for all unit test files
    unittests = args.metadata.get_if(
        lambda x: x['testonly'] is True and x['template'] == 'unittest'
    )

    # Get all source files associated with a unit test.
    available = {source_map[item['validates']] for item in unittests}

    missing = sources.difference(available)

    for item in missing:
        print(f'{item}: error: no unit test available', file=sys.stderr)

    exit_code = len(missing) != 0

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
