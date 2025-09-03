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
import concurrent.futures
import json
import os
import subprocess
import sys
import threading
import time


def detect_clang_tidy_config(path=None):
    if not path:
        path = os.getcwd()

    if os.path.isfile(path):
        path = os.path.dirname(path)

    while True:
        candidate = os.path.join(path, '.clang-tidy')
        if os.path.exists(candidate):
            return candidate

        dirname = os.path.dirname(path)
        if dirname == path:
            message = (
                "failed to automatically detect a '.clang-tidy' "
                'configuration file.'
            )
            raise RuntimeError(message)

        path = dirname


def invoke_clang_tidy(stop, invocation, source):
    if stop.is_set():
        return

    # Complete the invocation
    config = detect_clang_tidy_config(source)

    invocation += ['--config-file', config, source]

    # Execute clang-tidy
    result = subprocess.run(
        invocation,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )

    # Return the results
    return argparse.Namespace(
        command=' '.join(invocation),
        exit_code=result.returncode,
        output=result.stdout,
        source=source,
    )


def main():
    parser = argparse.ArgumentParser(description='Invoke clang-tidy')

    parser.add_argument(
        '--clang-tidy',
        help='Path to the clang-tidy executable (default: clang-tidy)',
        default='clang-tidy',
        type=str,
    )
    parser.add_argument(
        '--jobs',
        '-j',
        help='Run the specified amount of clang-tidy invocations in parallel.',
        required=False,
        default=os.cpu_count(),
        type=int,
    )
    parser.add_argument(
        '-k',
        help=(
            'Keep going until the specified amount of clang-tidy invocations '
            "have failed. Default is '1'."
        ),
        required=False,
        default=1,
        type=int,
    )

    parser.add_argument(
        '-p',
        help='Specify the path to the compile commands database.',
        metavar='BUILD_PATH',
        required=True,
        type=str,
    )
    parser.add_argument(
        '--sources',
        help=(
            'The source files for which clang-tidy shall perform an analyis. '
            'Files that are not part of this set will be skipped.'
        ),
        required=False,
        default=[],
        type=lambda x: json.load(open(x, 'r')),
    )
    parser.add_argument(
        '--vfsoverlay',
        help=(
            'Overlay the virtual filesystem described by file over the real '
            'file system.'
        ),
        required=False,
        default=None,
        type=str,
    )

    args = parser.parse_args()

    # Prepare a common base for the clang-tidy invocation.
    invocation = [
        args.clang_tidy,
        '-p',
        args.p,
    ]

    if args.vfsoverlay:
        invocation += ['--vfsoverlay', args.vfsoverlay]

    jobs = min(max(len(args.sources), 1), args.jobs)
    stop = threading.Event()
    failed_jobs = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as executor:
        tstart = time.monotonic()
        # Execute a clang-tidy invocation for each source file.
        futures = [
            executor.submit(invoke_clang_tidy, stop, invocation[:], source)
            for source in args.sources
        ]

        # Collect the results from the invocations.
        for i, future in enumerate(
            concurrent.futures.as_completed(futures), start=1
        ):
            result = future.result()

            if stop.is_set():
                continue

            elapsed = time.monotonic() - tstart
            print(
                (
                    f'[{i}/{len(args.sources)} :: {elapsed:.3f}] '
                    f'CLANG-TIDY {result.source}'
                ),
                file=sys.stderr,
            )
            print(result.output, end='', file=sys.stderr)

            if result.exit_code == 0:
                continue

            failed_jobs += 1
            print(
                f'FAILED: [code={result.exit_code}]\n{result.command}',
                file=sys.stderr,
            )

            if args.k > 0 and failed_jobs >= args.k:
                stop.set()

    exit_code = failed_jobs != 0

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
