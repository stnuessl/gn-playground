#!/usr/bin/env python
#
# The MIT License (MIT)
#
# Copyright (c) 2025-2026  Steffen Nuessle
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
import json
import sys

import util

import gn


def main():
    parser = argparse.ArgumentParser(
        description='Select source files for the clang-tidy analysis.'
    )
    parser.add_argument(
        '-o',
        help=(
            'The output file containing all sources that are supposed to be '
            'analyzed by clang-tidy.'
        ),
        metavar='PATH',
        required=True,
        type=lambda x: open(x, 'w'),
    )
    parser.add_argument(
        '--exclude-sources',
        help='Exclude files from the clang-tidy analysis based on their path.',
        nargs='*',
        default=[],
        type=str,
    )
    parser.add_argument(
        '--exclude-sources-with-metadata',
        help=(
            'Exclude files from the clang-tidy analysis based on the metadata '
            'associated with them.'
        ),
        nargs='*',
        default=[],
        type=str,
    )
    parser.add_argument(
        '--metadata',
        help="The project's metadata file.",
        required=True,
        type=gn.Metadata.from_file,
    )
    parser.add_argument(
        '--include-sources',
        help='Include files from the clang-tidy analysis based on their path.',
        nargs='+',
        default=[],
        type=str,
    )
    parser.add_argument(
        '--include-sources-with-metadata',
        help=(
            'Include files from the clang-tidy analysis based on the metadata '
            'associated with them.'
        ),
        nargs='+',
        default=[],
        type=str,
    )

    args = parser.parse_args()

    incl = util.invoke_split(
        args.include_sources_with_metadata, '=', maxsplit=1
    )
    excl = util.invoke_split(
        args.exclude_sources_with_metadata, '=', maxsplit=1
    )

    sources = set(
        args.metadata.get_if(
            lambda item: (
                item['type']
                in {
                    'executable',
                    'shared_library',
                    'static_library',
                    'source_set',
                }
                and util.any_fnmatch(item['source'], args.include_sources)
                and not util.any_fnmatch(item['source'], args.exclude_sources)
                and all(item[key] == value for key, value in incl)
                and not any(item[key] == value for key, value in excl)
            )
        ).extract('source')
    )

    print(json.dumps(list(sources), indent=4), file=args.o)

    sys.exit(0)


if __name__ == '__main__':
    main()
