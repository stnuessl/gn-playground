#!/usr/bin/env python
#
# The MIT License (MIT)
#
# Copyright (c) 2026 Steffen Nuessle
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
import os
import sys

import ninja
import util
import xxhash

import gn


class PathTransformer:
    def __init__(self, build_dir):
        self.build_dir = build_dir

    def __call__(self, path):
        if os.path.isabs(path):
            return path

        return os.path.relpath(path, self.build_dir)


def main():
    parser = argparse.ArgumentParser(
        description='Generate an unused include directories analysis build.'
    )
    parser.add_argument(
        '--build-directory',
        help=(
            'The directory used by the generated build. '
            'Must not be shared by another ninja build.'
        ),
        required=True,
        type=str,
    )
    parser.add_argument(
        '--exclude',
        help='Exclude sources matching one of the specified glob(s).',
        nargs='*',
        default=[],
        type=str,
    )
    parser.add_argument(
        '--description',
        help='The builds dispatched description file.',
        required=True,
        type=str,
    )
    parser.add_argument(
        '--script',
        help='The script invoked during the generated ninja build.',
        required=True,
        type=str,
    )
    parser.add_argument(
        '--compilation-database',
        help=(
            'The compilation database containing the compile commands for all '
            'relevant source files.'
        ),
        required=True,
        type=str,
    )
    parser.add_argument(
        '--vfs-config',
        help=(
            'A file descriping the mapping of files to each other as used in a '
            'virtual filesystem.'
        ),
        required=True,
        type=str,
    )
    parser.add_argument(
        '-o',
        help='The generated ninja build file.',
        metavar='PATH',
        required=False,
        default=sys.stdout,
        type=lambda x: open(x, 'w'),
    )

    args = parser.parse_args()

    desc = gn.Description.from_file(args.description).get_if(
        lambda data: (
            data['type']
            in {'executable', 'shared_library', 'static_library', 'source_set'}
        )
    )

    transform = PathTransformer(args.build_directory)

    writer = ninja.ninja_syntax.Writer(args.o)

    writer.comment(
        'Automatically generated file to invoke the check include directories '
        'script on a selected set of source files.'
    )
    writer.newline()

    writer.rule(
        name='invoke',
        command=[
            os.environ['UV'],
            # Since we are using 'libclang', change the working directory to
            # the original build directory so the relative paths in the builds
            # description and the compilation database can be simply used.
            '--directory',
            transform(os.getcwd()),
            'run',
            '--with',
            'libclang',
            'python',
            args.script,
            '--description',
            args.description,
            '--compilation-database',
            args.compilation_database,
            '--vfs-config',
            args.vfs_config,
            '--target',
            '$target',
            '&&',
            os.path.realpath(sys.executable),
            '-c',
            "\"open('$out', 'w')\"",
        ],
        description='CHECK-INCLUDE-DIRS $target',
    )
    writer.newline()

    script = transform(args.script)
    compilation_database = transform(args.compilation_database)
    description = transform(args.description)

    for label, details in desc.items():
        # Do not create a build target for excluded labels.
        if util.any_fnmatch(label, args.exclude):
            continue

        # Do not create a build target for components that do not contain a
        # a full translation unit.
        sources = [
            path
            for path in details['sources']
            if util.any_fnmatch(path, ['*.c', '*.cc', '*.cpp', '*.cxx'])
        ]

        if not sources:
            continue

        build_file = gn.label.get_referenced_build_file(label)
        target = gn.label.get_name(label)
        digest = xxhash.xxh3_128_hexdigest(build_file)
        output = os.path.join(digest, f'{target}.ack')

        writer.build(
            outputs=[output],
            rule='invoke',
            variables={'target': label},
            inputs=[
                script,
                compilation_database,
                description,
            ],
        )
        writer.newline()

    writer.close()

    sys.exit(0)


if __name__ == '__main__':
    main()
