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
import glob
import json
import sys
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config'
    )
    parser.add_argument(
        '-o',
        help='',
        required=False,
        default=sys.stdout,
        type=lambda x: open(x, 'w')
    )

    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = json.load(f)

    vfs = {
        'version': 0,
        'roots': [],
    }

    roots = {}

    for item in config:
        dirname, filename = os.path.split(item['source'])

        entry = {
            'name': filename,
            'type': 'file',
            'external-contents': item['stub'],
        }

        if dirname in roots:
            roots[dirname]['content'].append(entry)
        else:
            roots[dirname] = {
                'name' : dirname,
                'type' : 'directory',
                'contents' : [entry],
            }

    for value in roots.values():
        vfs['roots'].append(value)

    print(json.dumps(vfs, indent=4), file=args.o)


if __name__ == '__main__':
    main()
