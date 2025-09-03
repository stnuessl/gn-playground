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


def main():
    parser = argparse.ArgumentParser()
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
        '--clang-format',
        help='The clang-format executable used within the generated build.',
        required=False,
        default='clang-format',
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
        '--include',
        help=(
            'Only include sources matching the specified glob(s) in the check.'
        ),
        required=False,
        nargs='*',
        default=['*.[ch]', '*.cc', '*.[ch]pp', '*.[ch]xx', '*.hh'],
        type=str,
    )
    parser.add_argument(
        '--metadata',
        help='The builds generated metadata file.',
        required=True,
        type=gn.Metadata.from_file,
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

    sources = set(
        args.metadata.get_if(
            lambda x: (
                'source' in x
                and x['type']
                in {
                    'executable',
                    'shared_library',
                    'source_set',
                    'static_library',
                }
                and util.any_fnmatch(x['source'], args.include)
                and not util.any_fnmatch(x['source'], args.exclude)
            ),
        ).extract('source')
    )

    writer = ninja.ninja_syntax.Writer(args.o)

    writer.comment(
        'Automatically generated file to invoke clang-format on a '
        'selected set  of source files.'
    )
    writer.newline()

    writer.rule(
        name='clang-format',
        command=[
            args.clang_format,
            '--dry-run',
            '--Werror',
            '$in',
            '&&',
            os.path.realpath(sys.executable),
            '-c',
            "\"open('$out', 'w')\"",
        ],
        description='CLANG-FORMAT $in',
    )
    writer.newline()

    for path in sources:
        source = os.path.relpath(path, args.build_directory)

        dirname, filename = os.path.split(source)
        digest = xxhash.xxh3_128_hexdigest(dirname)
        output = os.path.join(args.build_directory, digest, f'{filename}.ack')

        writer.build(outputs=[output], rule='clang-format', inputs=[source])
        writer.newline()

    writer.close()

    sys.exit(0)


if __name__ == '__main__':
    main()
