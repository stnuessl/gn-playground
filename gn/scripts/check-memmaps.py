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
import fnmatch
import os
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--description',
        help='',
        required=True,
        type=str
    )
    parser.add_argument(
        '--stub-config',
        help='',
        required=True,
        type=str
    )
    parser.add_argument(
        '--memmap-glob',
        help='',
        required=False,
        nargs='+',
        default=['**/*MemMap*.h'],
        type=str
    )
    parser.add_argument(
        '--root',
        help='',
        required=True,
        type=str
    )

    args = parser.parse_args()

    with open(args.description, 'r') as f:
        description = json.load(f)

    with open(args.stub_config, 'r') as f:
        stub_config = json.load(f)

    memmaps = set()
    target_types = {
        'executable',
        'source_set',
        'static_library',
        'dynamic_library',
    }

    for item in description.values():
        if item['type'] not in target_types:
            continue

        for source in item.get('sources', []):
            if not any(fnmatch.fnmatch(source, x) for x in args.memmap_glob):
                continue

            path = os.path.join(args.root, source.removeprefix('//'))
            path = os.path.normpath(path)

            memmaps.add(path)

    known = set(x['source'] for x in stub_config)
    missing = [x for x in memmaps if x not in known]

    if len(missing) == 0:
        exit_code = 0
    else:
        exit_code = 1

        for item in missing:
            print(
                f'error: \'{item}\' not listed as a MemMap file',
                file=sys.stderr
            )

    sys.exit(exit_code)

if __name__ == '__main__':
    main()
