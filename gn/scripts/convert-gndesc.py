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


def main():
    import argparse
    import os
    import sys
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input',
        help='A JSON description emitted by \'gn desc ...\'',
        nargs='+',
        type=str
    )
    parser.add_argument(
        '-o',
        help='The generated output file.',
        required=False,
        default=sys.stdout,
        type=lambda x: open(x, 'w')
    )
    parser.add_argument(
        '--root',
        help='The project\'s root directory.',
        required=False,
        default=os.getcwd(),
        type=str
    )

    args = parser.parse_args()

    gn_desc = {}

    for path in args.input:
        with open(path, 'r') as f:
            gn_desc.update(json.load(f))

    # Filter out items containing information about source files
    gn_desc = { k: v for k, v in gn_desc.items() if 'sources' in v }
    output = []

    for target, data in gn_desc.items():
        for source in data['sources']:
            path = os.path.join(args.root, source.removeprefix('//'))

            item = {
                'source': os.path.normpath(path),
                'target': target,
                'type' : data['type'],
                'tags': data['metadata'].get('tags', [''])[0],
            }

            output.append(item)

    print(json.dumps(output, indent=4), file=args.o)

    sys.exit(0)


if __name__ == '__main__':
    main()

