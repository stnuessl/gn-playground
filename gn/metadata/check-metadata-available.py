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
import json
import sys

import gn


def main():
    parser = argparse.ArgumentParser(
        description=(
            'Check the correct availability of metadata for each source and '
            'header file.'
        )
    )
    parser.add_argument(
        '--metadata',
        help="The project's JSON metadata file.",
        required=True,
        type=gn.Metadata.from_file,
    )
    parser.add_argument(
        '--dependencies',
        help="A JSON file containing all of the project's dependencies.",
        required=True,
        type=lambda x: json.load(open(x, 'r')),
    )

    args = parser.parse_args()

    # Extract all source and header files from the project's dependencies.
    # Use a set to avoid duplicates and reduce input size.
    sources = {x for item in args.dependencies for x in item['deps']}

    # Extract all files which are known to have metadata associated with them
    available = set(args.metadata.extract('source'))
    missing = [x for x in sources if x not in available]

    for item in missing:
        print(
            f'{item}: error: no metadata associated with source',
            file=sys.stderr,
        )

    exit_code = len(missing) != 0
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
