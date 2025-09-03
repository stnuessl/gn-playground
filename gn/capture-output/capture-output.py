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
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(
        description='Capture the output of a process into a file.'
    )
    parser.add_argument(
        '--stdout',
        help=(
            'Write the standard output of the invoked process to the '
            'specified file.'
        ),
        required=False,
        default=sys.stdout,
        type=lambda x: open(x, 'w'),
    )
    parser.add_argument(
        '--stderr',
        help=(
            'Write the standard error of the invoked process to the '
            'specified file.'
        ),
        required=False,
        default=sys.stderr,
        type=lambda x: open(x, 'w'),
    )
    parser.add_argument(
        'command',
        help=(
            'The command to invoke the process whose output is going to be '
            'captured.',
        ),
        nargs='+',
        type=str,
    )
    args = parser.parse_args()

    result = subprocess.run(
        args.command, stdout=args.stdout, stderr=args.stderr, check=True
    )

    args.stdout.close()
    args.stderr.close()

    sys.exit(result.returncode)


if __name__ == '__main__':
    main()
