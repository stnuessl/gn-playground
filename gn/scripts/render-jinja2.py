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
import jinja2
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--template',
        help='',
        required=True,
        type=str
    )
    parser.add_argument(
        '-o',
        help='',
        default=sys.stdout,
        required=False,
        type=lambda x: open(x, 'w')
    )
    parser.add_argument(
        'data',
        metavar='KEY=VALUE',
        default=[],
        nargs='*',
        type=str
    )

    args = parser.parse_args()

    data = dict(x.split('=', maxsplit=1) for x in args.data)

    with open(args.template, 'r') as f:
        template = jinja2.Template(f.read())

    output = template.render(**data)

    print(output, file=args.o)

    sys.exit(0)

if __name__ == '__main__':
    main()
