#!/usr/bin/env python
#
# The MIT License (MIT)
#
# Copyright (c) 2025-2026  Steffen Nuessle
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
import sys

import util
import vfs


class PathTransformer:
    def __init__(self, build_dir, vfs_map, prefix_map):
        if not vfs_map:
            vfs_map = vfs.VirtualFileSystemMap()

        self.build_dir = build_dir
        self.vfs_map = vfs_map
        self.mappings = [item.split('=', 1) for item in prefix_map]

    def __call__(self, path):
        if value := self.vfs_map.get_source(path):
            return value

        if path.startswith(self.build_dir):
            path = os.path.relpath(path, self.build_dir)
        else:
            path = os.path.normpath(path)

        for source, dest in self.mappings:
            if path.startswith(source):
                path = path.removeprefix(source)

                return os.path.join(dest, path)

        return path


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
        metavar='PATH',
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
        action='append',
        default=[],
        type=str,
    )
    parser.add_argument(
        '--vfs-config',
        help=(
            'A file descriping the mapping of files to each other as used in a '
            'virtual filesystem.'
        ),
        required=False,
        default=None,
        type=vfs.VirtualFileSystemMap.from_vfs_config,
    )

    args = parser.parse_args()

    transform = PathTransformer(
        args.build_dir, args.vfs_config, args.prefix_map
    )
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

                normpath = os.path.normpath(path)

                if util.any_fnmatch(normpath, args.exclude_deps):
                    continue

                item['deps'].append(transform(path))

            data.append(item)

    print(json.dumps(data, indent=4), file=args.o)

    sys.exit(0)


if __name__ == '__main__':
    main()
