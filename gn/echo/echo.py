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


def main():
    parser = argparse.ArgumentParser(
        description='A platform-independant echo command.'
    )

    parser.add_argument(
        'input',
        help='The lines to echo to the specified output.',
        nargs='*',
        default=[],
        type=str,
    )
    parser.add_argument(
        '--stderr',
        help='Write to standard error instead of standard output',
        action='store_true',
        default=False,
    )
    parser.add_argument(
        '--with-ack',
        help=(
            'Create an acknowledgement file. This allows the build system '
            'to correctly identify when a target needs to be rebuilt.'
        ),
        required=False,
        default=None,
        type=lambda x: open(x, 'w'),
    )

    args = parser.parse_args()

    output = sys.stderr if args.stderr else sys.stdout

    for line in args.input:
        print(line, file=output)

    sys.exit(0)


if __name__ == '__main__':
    main()
