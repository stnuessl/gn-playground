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

def main():
    import argparse
    import os
    import shutil
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--source',
        help='',
        nargs='+',
        required=True,
        type=str
    )

    parser.add_argument(
        '--destination',
        help='',
        required=True,
        type=str
    )

    parser.add_argument(
        '--with-ack',
        help='',
        default=None,
        required=False,
        type=str
    )

    args = parser.parse_args()

    if len(args.source) > 1 and os.path.isfile(args.destination):
        print(
            f'{sys.argv[0]}: error: \'{args.destination}\' is not a directory',
            file=sys.stderr
        )
        sys.exit(1)

    if len(args.source) > 1:
        dirname = args.destination
    else:
        dirname = os.path.dirname(args.destination)

    if not os.path.exists(dirname):
        os.makedirs(dirname, mode=0o755, exist_ok=False)

    for item in args.source:
        shutil.copy2(item, args.destination, follow_symlinks=False)

    if args.with_ack:
        with open(args.with_ack, "w") as f:
            pass

    sys.exit(0)


if __name__ == '__main__':
    main()
