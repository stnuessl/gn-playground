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
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input",
        help='',
        metavar='file',
        nargs='+',
        type=str
    )
    parser.add_argument(
        "-o",
        help='',
        default=sys.stdout,
        type=lambda x: open(x, 'w')
    )

    args = parser.parse_args()

    data = []

    for path in args.input:
        item = { 'target': '', 'prerequisites': [] }

        for line in open(path, 'r'):
            if not item['target']:
                item['target'] = line.split(':', maxsplit=1)[0]
            elif dep := line.strip():
                item['prerequisites'].append(dep)
            else:
                data.append(item)
                item = { 'target': '', 'prerequisites': [] }

    print(json.dumps(data, indent=4), file=args.o)
    sys.exit(0)


if __name__ == '__main__':
    main()
