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
import sys

def main():
    parser = argparse.ArgumentParser(
        description=(
            'Check that all relevant files have a unit test associated with '
            'them.'
        )
    )
    parser.add_argument(
        '--description',
        help='The project\'s description file.',
        required=True,
        type=lambda x: json.load(open(x, 'r'))
    )
    parser.add_argument(
        '--include',
        help=(
            'Check if at least one unit test exists for files matching the '
            'specified glob(s).'
        ),
        required=False,
        nargs='*',
        default=["*.c", "*.cc", "*.cpp", "*.cxx"],
        type=str
    )
    parser.add_argument(
        '--exclude',
        help='Exclude sources from the unit test check',
        required=False,
        nargs='*',
        default=[],
        type=str
    )
    parser.add_argument(
        'targets',
        help=(
            'A list of gn targets which will be searched for unit test '
            'implementations'
        ),
        nargs='+',
        type=str
    )

    args = parser.parse_args()

    # Collect all unit tested files.
    unittest_available = set()
    visited = set()

    queue = []
    for target in args.targets:
        queue.extend(args.description[target]['deps'])

    while len(queue) != 0:
        target = queue.pop()

        # Remove a potentially specified toolchain from the target as
        # the keys used in the description never contain them.
        key = target.split('(')[0]

        if key in visited:
            continue

        visited.add(key)

        if value := args.description[key]['metadata'].get('unittest'):
            unittest_available.add(value[0])

        queue.extend(args.description[key]['deps'])


    # Collect all sources that require at least one unit test
    sources = []
    for item in args.description.values():
        if value := item['metadata'].get('template'):
            if value[0] not in ['binary', 'component']:
                continue

            sources.extend(item['sources'])

    # Extract all files which are missing a unit test
    unittest_missing = [
        path
        for path in sources
        if path not in unittest_available
        and any(fnmatch.fnmatch(path, glob) for glob in args.include)
        and not any(fnmatch.fnmatch(path, glob) for glob in args.exclude)
    ]

    if len(unittest_missing) > 0:
        exit_code = 1

        for path in unittest_missing:
            print(f'error: missing unit test: \'{path}\'', file=sys.stderr)
    else:
        exit_code = 0

    sys.exit(exit_code)

if __name__ == '__main__':
    main()
