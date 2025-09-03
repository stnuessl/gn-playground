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

import gn


def main():
    parser = argparse.ArgumentParser(
        description=(
            'Check whether all unit test targets will be built by a specified '
            'target.'
        )
    )
    parser.add_argument(
        'description',
        help="The project's dispatched description file.",
        type=gn.Description.from_file,
    )
    parser.add_argument(
        '--target',
        help='The build target supposed to run all unit tests.',
        required=True,
        type=str,
    )

    args = parser.parse_args()

    unittests = set(
        args.description.get_if(
            lambda x: x['metadata'].get('template', [''])[0] == 'unittest'
        ).extract_targets()
    )

    active = set(
        args.description.get_subdesc(args.target).extract('deps', flatten=True)
    )

    inactive = unittests.difference(active)

    for item in inactive:
        print(
            f"{item}: error: not listed as a dependency of '{args.target}'",
            file=sys.stderr,
        )

    exit_code = len(inactive) != 0

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
