#
# The MIT License (MIT)
#
# Copyright (c) 2026  Steffen Nuessle
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

# Simple script the prepare the CLANG_TIDY_SOURCES environment so
# invoke-clang-tidy.py will only analyze the specified files.

import os
import subprocess
import sys


def main():
    min_args = 3

    if len(sys.argv) < min_args:
        print(f'{sys.argv[0]}: error: invalid usage', file=sys.stderr)
        sys.exit(1)

    script = sys.argv[1]
    target = sys.argv[2]
    sources = sys.argv[3:]

    env = os.environ.copy()
    build_dir = env['NINJA_BUILD_DIRECTORY']

    # The scripts within the ninja build expect all relative paths to be
    # relativie to the build directory.
    env['CLANG_TIDY_SOURCES'] = os.pathsep.join(
        os.path.relpath(item, build_dir) for item in sources
    )

    invocation = [sys.executable, script, target]

    result = subprocess.run(invocation, env=env, check=False)

    sys.exit(result.returncode)


if __name__ == '__main__':
    main()
