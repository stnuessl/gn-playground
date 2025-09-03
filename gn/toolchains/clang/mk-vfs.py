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
import os
import sys


def main():
    parser = argparse.ArgumentParser(
        description=(
            'A tool to create a virtual filesystem suiteable for usage with '
            'clang.'
        )
    )
    parser.add_argument(
        'data',
        help='The input data required to build a virtual filesystem.',
        nargs='+',
        type=str,
    )
    parser.add_argument(
        '-o',
        help=(
            'The generated output file containing the specified virtual '
            'filesystem.'
        ),
        metavar='PATH',
        required=False,
        default=sys.stdout,
        type=lambda x: open(x, 'w'),
    )

    args = parser.parse_args()

    # Load the input data.
    config = []

    for item in args.data:
        with open(item, 'r') as f:
            config.extend(json.load(f))

    # Create an entry for each item in the configuration and
    # sort them according to their parent directory.
    roots = {}

    for item in config:
        dirname, filename = os.path.split(item['source'])

        entry = {
            'name': filename,
            'type': 'file',
            'external-contents': item['target'],
        }

        if dirname in roots:
            roots[dirname]['contents'].append(entry)
        else:
            roots[dirname] = {
                'name': os.path.abspath(dirname),
                'type': 'directory',
                'contents': [entry],
            }

    # Finalize the virtual filesystem data structure.
    vfs = {
        'version': 0,
        'root-relative': 'cwd',
        'roots': list(roots.values()),
    }

    # Write the virtual filesystem to the specified output.
    print(json.dumps(vfs, indent=4), file=args.o)

    sys.exit(0)


if __name__ == '__main__':
    main()
