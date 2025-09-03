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
import os
import sys

import ninja

import gn


class PathTransformer:
    def __init__(self, build_dir):
        self.build_dir = build_dir

    def __call__(self, path):
        if os.path.isabs(path):
            return path

        return os.path.relpath(path, self.build_dir)


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
        '-o',
        help='The generated ninja build file.',
        metavar='PATH',
        required=False,
        default=sys.stdout,
        type=lambda x: open(x, 'w'),
    )
    parser.add_argument(
        '--build-output',
        help='The output file resulting from the generated build.',
        required=True,
        type=str,
    )
    parser.add_argument(
        '--build-directory',
        help='The directory used by the generated build.',
        required=True,
        type=str,
    )
    parser.add_argument(
        '--clang-scan-deps',
        help='The clang-scan-deps executable used within the generated build.',
        required=False,
        default='clang-scan-deps',
        type=str,
    )
    parser.add_argument(
        '--compile-commands',
        help="The project's compile_commands.json file.",
        required=True,
        type=str,
    )
    parser.add_argument(
        '--description',
        help="The project's dispatched description file.",
        required=True,
        type=gn.Description.from_file,
    )

    args = parser.parse_args()

    transform = PathTransformer(args.build_directory)

    inputs = set(args.description.extract('sources', flatten=True))

    writer = ninja.ninja_syntax.Writer(args.o)

    writer.comment('Automatically generated file to invoke clang-scan-deps.')
    writer.newline()

    writer.rule(
        name='clang-scan-deps',
        command=[
            args.clang_scan_deps,
            '-compilation-database',
            args.compile_commands,
            '-mode',
            'preprocess-dependency-directives',
            '-format',
            'experimental-full',
            '-o',
            '$out',
        ],
        description='SCAN $out',
    )
    writer.newline()

    writer.build(
        outputs=args.build_output,
        rule='clang-scan-deps',
        inputs=[transform(path) for path in inputs],
    )
    writer.newline()

    writer.close()

    sys.exit(0)


if __name__ == '__main__':
    main()
