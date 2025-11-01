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
import re
import sys

import gn


def main():
    parser = argparse.ArgumentParser(
        description=(
            'Check if build target names adhere to a specified naming '
            'convention.'
        )
    )
    parser.add_argument(
        'description',
        help="The build's dispatched description file.",
        type=gn.desc.Description.from_file,
    )

    args = parser.parse_args()

    regex = re.compile(r'[a-z][a-z0-9]*(:?-[a-z][a-z0-9]*)*')

    invalid_targets = list(
        args.description.extract_targets(
            predicate=lambda x: not regex.fullmatch(x.split(':')[-1])
        )
    )

    for item in invalid_targets:
        print(f'{item}: error: invalid target name', file=sys.stderr)

    exit_code = len(invalid_targets) != 0

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
