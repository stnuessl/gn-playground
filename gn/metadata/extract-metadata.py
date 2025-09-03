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
import itertools
import json
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Extract metadata from a project's gn description"
    )
    parser.add_argument(
        'input',
        help="The project's dispatched description file.",
        type=lambda x: json.load(open(x, 'r')),
    )
    parser.add_argument(
        '-o',
        help='The generated output file.',
        metavar='PATH',
        required=False,
        default=sys.stdout,
        type=lambda x: open(x, 'w'),
    )

    args = parser.parse_args()

    # Focus only on interesting targets
    gn_types = [
        'executable',
        'source_set',
        'static_library',
        'dynamic_library',
    ]

    desc = {k: v for k, v in args.input.items() if v['type'] in gn_types}

    # A list containing an item for each source listed within a target.
    output = []

    for target, data in desc.items():
        for source in itertools.chain(data['inputs'], data['sources']):
            item = {
                'target': target,
                'type': data['type'],
                'source': source,
                'testonly': data['testonly'],
            }

            for key in data['metadata']:
                item[key] = data['metadata'].get(key, [''])[0]

            output.append(item)

    print(json.dumps(output, indent=4), file=args.o)

    sys.exit(0)


if __name__ == '__main__':
    main()
