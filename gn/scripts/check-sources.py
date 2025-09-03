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
import json
import os
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--description',
        help='',
        required=True,
        type=lambda x: json.load(open(x, 'r'))
    )
    parser.add_argument(
        '--deps',
        help='',
        required=True,
        type=lambda x: json.load(open(x, 'r'))
    )
    parser.add_argument(
        '--skip',
        help='',
        default=[],
        nargs='*',
        required=False,
        type=str
    )
    parser.add_argument(
        '--root',
        help='The project\'s root directory.',
        required=False,
        default=os.getcwd(),
        type=str
    )
    parser.add_argument(
        '-o',
        help='',
        metavar='file',
        default=sys.stdout,
        type=lambda x: open(x, 'r')
    )

    args = parser.parse_args()

    lookup = { x['source'] for x in args.description }

    # Compactify everything into a set to remove duplicates
    prerequisites = {
        os.path.abspath(x)
        for dep in args.deps
        for x in dep['prerequisites']
    }

    exit_code = 0

    for item in prerequisites:
        if any(fnmatch.fnmatch(item, x) for x in args.skip):
            continue

        if item not in lookup:
            exit_code = 1
            print((
                f'{sys.argv[0]}: error: '
                f'file \'{item}\' not listed in any target sources'
            ), file=sys.stderr)

    sys.exit(exit_code)

if __name__ == '__main__':
    main()
