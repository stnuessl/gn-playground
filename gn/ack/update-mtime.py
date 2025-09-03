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
import sys


def main():
    parser = argparse.ArgumentParser(
        description=(
            'Update the modification time of a file based on the '
            'modification time of a reference file.'
        )
    )
    parser.add_argument(
        'input',
        help='The input / reference file.',
        metavar='file',
        type=str,
    )
    parser.add_argument(
        '-o',
        help='The file, whose modification time may potentially be updated.',
        metavar='PATH',
        required=True,
        type=str,
    )

    args = parser.parse_args()

    if (
        not os.path.isfile(args.o)
        or os.stat(args.input).st_mtime_ns > os.stat(args.o).st_mtime_ns
    ):
        open(args.o, 'w').close()

    sys.exit(0)


if __name__ == '__main__':
    main()
