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
import io
import sys

import util

import gn


class DepFile:
    def __init__(self, f):
        self.f = f
        self.patterns = [
            ('\\', '/'),
            (' ', '\\ '),
        ]

    def write(self, outputs, inputs):
        if isinstance(outputs, str):
            outputs = [outputs]

        # Precompute text of dependency list
        buf = io.StringIO()

        last = len(inputs) - 1

        for i, path in enumerate(inputs):
            prerequisite = self._escape(path)

            buf.write(f'\t{prerequisite}')

            if i != last:
                buf.write(' \\')

            buf.write('\n')

        for item in outputs:
            target = self._escape(item)

            self.f.write(f'{target}: \\\n{buf.getvalue()}\n')

    def close(self):
        self.f.close()

    def _escape(self, s):
        for old, new in self.patterns:
            s = s.replace(old, new)

        return s


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
        '--description',
        help='The builds processed description file.',
        type=gn.Description.from_file,
    )
    parser.add_argument(
        '--depfile',
        help='The generated output dependency file.',
        required=True,
        type=lambda x: open(x, 'w', encoding='utf-8'),
    )
    parser.add_argument(
        '--exclude',
        help='Exclude prerequisites matching one of the specified glob(s).',
        nargs='*',
        default=[],
        type=str,
    )
    parser.add_argument(
        '--include',
        help=('Only include prerequisites matching the specified glob(s).'),
        required=False,
        nargs='+',
        default=['*'],
        type=str,
    )
    parser.add_argument(
        '-o',
        help='The generated output file containing all required input files',
        required=False,
        default=None,
        type=lambda x: open(x, 'w', encoding='utf-8'),
    )
    parser.add_argument(
        'labels',
        help='The target labels for which to build a dependency file',
        default=['default'],
        nargs='+',
        type=str,
    )

    args = parser.parse_args()

    # Collect all prerequisites of the specified labels.
    prerequisites = set()

    # Special case which allows to retrieve all prerequisites for the complete
    # build.
    if args.labels == ['//*']:
        args.labels = args.description.extract_targets()

    for label in args.labels:
        desc = args.description.get_subdesc(label)

        inputs = desc.extract('inputs', flatten=True)
        sources = desc.extract('sources', flatten=True)

        prerequisites = prerequisites.union(inputs).union(sources)

    prerequisites = [
        item
        for item in prerequisites
        if util.any_fnmatch(item, args.include)
        and not util.any_fnmatch(item, args.exclude)
    ]

    targets = args.o.name if args.o else args.depfile.name

    depfile = DepFile(args.depfile)
    depfile.write(targets, prerequisites)
    depfile.close()

    if args.o:
        print('\n'.join(prerequisites), file=args.o)

    sys.exit(0)


if __name__ == '__main__':
    main()
