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
import json
import os
import subprocess
import sys
import tempfile


def main():
    parser = argparse.ArgumentParser(
        description=(
            'Analyze which GN targets are affected by a set of changed files and '
            'build only those targets with ninja. Wraps `gn analyze` to scope '
            'incremental builds and test runs in CI to the minimal set of work.'
        ),
        fromfile_prefix_chars='@',
    )
    parser.add_argument(
        '--gn-tool',
        help='Path to the gn executable.',
        required=False,
        default='gn',
        type=str,
    )
    parser.add_argument(
        '--ninja-tool',
        help='Path to the ninja executable.',
        required=False,
        default='ninja',
        type=str,
    )
    parser.add_argument(
        '--files',
        help='Source files to analyze.',
        default=[],
        nargs='*',
        type=str,
    )
    parser.add_argument(
        '--test-targets',
        help='GN test targets to check for a dependency on the changed files.',
        default=[],
        nargs='*',
        type=str,
    )
    parser.add_argument(
        '--additional-compile-targets',
        help='Build targets to check in addition to test targets.',
        default=[],
        nargs='*',
        type=str,
    )
    parser.add_argument(
        '--remap',
        help=(
            'Rewrite affected target labels before passing them to ninja. '
            'Format: FROM=TO'
        ),
        default=[],
        nargs='+',
        type=str,
    )
    parser.add_argument(
        '--exclude',
        help='Drop affected target labels before passing them to ninja.',
        default=[],
        nargs='+',
        type=str,
    )
    parser.add_argument(
        '--build-dir',
        help='Path to the build output directory.',
        required=True,
        type=str,
    )
    args = parser.parse_args()

    data = {
        'files': [
            f'{x}' if x.startswith('//') or os.path.isabs(x) else f'//{x}'
            for x in args.files
        ],
        'test_targets': args.test_targets,
        'additional_compile_targets': args.additional_compile_targets,
    }

    # Prepare input and output files for gn analyze
    infile = tempfile.NamedTemporaryFile(mode='w', delete=False)
    infile.write(json.dumps(data))
    infile.close()

    outfile = tempfile.NamedTemporaryFile(mode='r')

    invocation = [
        args.gn_tool,
        'analyze',
        args.build_dir,
        infile.name,
        outfile.name,
    ]

    result = subprocess.run(invocation, check=False)
    os.unlink(infile.name)

    if result.returncode != 0:
        print('error: gn analyzed failed', file=sys.stderr)
        sys.exit(1)

    data = json.load(outfile)

    if message := data.get('error'):
        print(f'error: gn analyze: {message}', file=sys.stderr)
        sys.exit(1)

    if data['status'] == 'Found dependency':
        # Remap and exlude targets for the ninja invocation as specified by
        # the user.
        remap = dict(x.split('=', maxsplit=1) for x in args.remap)
        excludes = set(args.exclude)
        targets = [
            remap.get(x, x)
            for x in data['compile_targets']
            if x not in excludes
        ]

        # Convert gn target label to a ninja target.
        targets = [target.lstrip('/') for target in targets]
        invocation = [args.ninja_tool, '-C', args.build_dir, *targets]

        with subprocess.Popen(
            invocation,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        ) as proc:
            for line in proc.stdout:
                print(line, end='', file=sys.stdout)

            proc.wait()

        if proc.returncode != 0:
            sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main()
