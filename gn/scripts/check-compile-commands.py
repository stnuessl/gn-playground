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
import fnmatch
import os
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--compile-commands',
        help='Path to the build\'s generated \'compile_commands.json\' file',
        required=True,
        type=str,
    )
    parser.add_argument(
        '--gn-description',
        required=True,
        type=str,
    )
    parser.add_argument(
        '--root',
        help='The project\'s root directory.',
        required=True,
        type=str
    )
    parser.add_argument(
        '--exclude',
        help='Exclude files matching one of the specified glob patterns.',
        nargs='*',
        default=['*.h', '*.hpp', '*.hxx', '*.s', '*.S'],
        type=str,
    )

    args = parser.parse_args()

    # Load input data.
    with open(args.compile_commands, 'r') as f:
        compile_commands = json.load(f)

    with open(args.gn_description, 'r') as f:
        gn_description = json.load(f)

    # Build a fast lookup containing every entry in the compile commands.
    lookup = set()

    for item in compile_commands:
        if os.path.isabs(item['file']):
            path = item['file']
        else:
            path = os.path.join(item['directory'], item['file'])

        lookup.add(os.path.normpath(path))


    # Check if each source listed in the gn description is also part of the
    # compile commands file. Use a set to remove duplicates.
    sources = set()
    target_types = {
        'executable',
        'source_set',
        'static_library',
        'shared_library'
    }

    for entry in gn_description.values():
        if entry['type'] not in target_types:
            continue

        for source in entry.get('sources', []):
            path = os.path.join(args.root, source.removeprefix('//'))
            path = os.path.normpath(path)

            if any(fnmatch.fnmatch(path, glob) for glob in args.exclude):
                continue

            sources.add(path)

    # Calculate all missing items from the compile commands file.
    missing = [ source for source in sources if source not in lookup ]

    if len(missing) == 0:
        exit_code = 0
    else:
        exit_code = 1

        # Emit an error for each missing item.
        path = os.path.relpath(args.compile_commands, args.root)

        for item in missing:
            print(
                f'error: \'{item}\' not found in \'{path}\'',
                file=sys.stderr
            )

    sys.exit(exit_code)


if __name__ == '__main__':
    main()

