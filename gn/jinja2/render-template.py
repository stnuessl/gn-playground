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

import jinja2


def main():
    parser = argparse.ArgumentParser(
        description='A generic script to render simple jinja2 templates.'
    )
    parser.add_argument(
        '--template',
        help='The jinja2 template used for rendering.',
        required=True,
        type=lambda x: jinja2.Template(open(x, 'r').read()),
    )
    parser.add_argument(
        '-o',
        help='The generated output file containing the rendered template.',
        metavar='PATH',
        default=sys.stdout,
        required=False,
        type=lambda x: open(x, 'w'),
    )
    parser.add_argument(
        'data',
        help='The data used for rendering the template',
        metavar='KEY=VALUE',
        default=[],
        nargs='+',
        type=str,
    )

    args = parser.parse_args()

    data = dict(x.split('=', maxsplit=1) for x in args.data)

    output = args.template.render(**data)

    print(output, file=args.o)

    sys.exit(0)


if __name__ == '__main__':
    main()
