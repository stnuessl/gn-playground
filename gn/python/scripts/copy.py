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
import shutil
import sys


def main():
    parser = argparse.ArgumentParser(
        description='Platform-independant copy operation for a single file.'
    )
    parser.add_argument(
        '--force',
        '-f',
        help='Overwrite the destination file if it exists.',
        required=False,
        action='store_true',
    )
    parser.add_argument(
        '--follow-symlinks',
        '-L',
        help='Follow symbolic links in SOURCE.',
        required=False,
        action='store_true',
    )
    parser.add_argument(
        'source', help='The source for the copy operation.', type=str
    )
    parser.add_argument(
        '-o',
        help='The destination to which the source file will be copied.',
        metavar='PATH',
        required=True,
        type=str,
    )

    args = parser.parse_args()

    if not args.force and os.path.exists(args.o):
        print(f"error: destination '{args.o}' already exists!", file=sys.stderr)
        sys.exit(1)

    shutil.copy2(args.source, args.o, follow_symlinks=args.follow_symlinks)

    sys.exit(0)


if __name__ == '__main__':
    main()
