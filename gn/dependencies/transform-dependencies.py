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
import json
import os
import posixpath
import sys

import util


class PathTransformer:
    def __init__(self, build_dir, prefix_map):
        if prefix_map:
            source, dest = prefix_map.split('=', 1)
        else:
            source, dest = None, None

        self.build_dir = build_dir
        self.source = source
        self.dest = dest

    def __call__(self, path):
        if path.startswith(self.build_dir):
            path = posixpath.relpath(path, self.build_dir)
        else:
            path = posixpath.normpath(path)

        if self.source == self.dest:
            return path

        if not path.startswith(self.source):
            return path

        path = path.removeprefix(self.source)
        return posixpath.join(self.dest, path)


def main():
    parser = argparse.ArgumentParser(
        description='Convert clang-scan-deps full output data.'
    )
    parser.add_argument(
        'input',
        help="The output of clang-scan-deps using the 'full' output format.",
        type=lambda x: json.load(open(x, 'r')),
    )
    parser.add_argument(
        '--build-dir',
        help='The directory used by the build as its working directory',
        required=False,
        default=os.getcwd(),
        type=str,
    )
    parser.add_argument(
        '--exclude-deps',
        help=(
            'Exclude any dependencies matching at least one of the specified '
            'globs. This is useful to strip the data from system header '
            'dependencies.'
        ),
        nargs='*',
        required=False,
        default=[],
        type=str,
    )
    parser.add_argument(
        '-o',
        help='The output file containing the converted data.',
        required=False,
        default=sys.stdout,
        type=lambda x: open(x, 'w'),
    )
    parser.add_argument(
        '--prefix-map',
        help=(
            'Rewrite paths of dependencies by replacing a specifiable prefix. '
            'A prefix-map must be specfied like this: source/path=dest/path'
        ),
        required=False,
        default=None,
        type=str,
    )

    args = parser.parse_args()

    transform = PathTransformer(args.build_dir, args.prefix_map)
    data = []

    for entry in args.input['translation-units']:
        for command in entry['commands']:
            item = {
                'main': transform(command['input-file']),
                'deps': [],
            }

            visited = set()
            for path in command.get('file-deps', []):
                if path in visited:
                    continue

                visited.add(path)

                normpath = posixpath.normpath(path)

                if util.any_fnmatch(normpath, args.exclude_deps):
                    continue

                item['deps'].append(transform(path))

            data.append(item)

    print(json.dumps(data, indent=4), file=args.o)

    sys.exit(0)


if __name__ == '__main__':
    main()
