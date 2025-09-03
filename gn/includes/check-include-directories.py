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

import clang.cindex
import util
import vfs

import gn


class CCAdapter:
    def __init__(self, compile_command):
        self._args = [
            arg
            for arg in compile_command.arguments
            if arg != compile_command.filename
        ]

        self._args_set = set(self._args)

        self._directory = compile_command.directory
        self._filename = compile_command.filename

    @property
    def args(self):
        it = iter(self._args)

        blacklist_no_arg = {
            '--',
            '--driver-mode=g++',
            '-MD',
            '-MMD',
            '-Wall',
            '-Werror',
            '-Wextra',
            '-c',
            '-pedantic',
            '-fdata-sections',
            '-ffunction-sections',
        }
        blacklist_with_arg = {'-o', '-MT', '-MF'}

        args = []
        while arg := next(it, None):
            if arg in blacklist_no_arg:
                continue

            if arg in blacklist_with_arg:
                next(it, None)
                continue

            args.append(arg)

        return args[1:]

    def contains(self, arg):
        return arg in self._args_set

    @property
    def directory(self):
        return self._directory

    @property
    def filename(self):
        return self._filename

    @property
    def include_directories(self):
        it = iter(self._args)

        data = []
        while arg := next(it, None):
            if arg == '-I' and (path := next(it, None)):
                data.append(path)
            elif arg.startswith('-I') and arg != '-I-':
                data.append(arg.removeprefix('-I'))

        return data


class UnusedIncludeDirectoriesAnalysis:
    def __init__(self, build_path, vfs_map, desc):
        dirname = os.path.dirname(build_path)

        self.compilation_database = (
            clang.cindex.CompilationDatabase.fromDirectory(dirname)
        )
        self.vfs_map = vfs_map
        self.desc = desc
        self.index = clang.cindex.Index.create()
        self.used_include_dirs = set()
        self.provided_include_dirs = set()

    def _get_desc_flags(self, source):
        flags = []
        flags += [f'-D{x}' for x in self.desc.get('defines', [])]

        # The compile commands from the compilation database to not seem to
        # contain trailing slashes, even if the user specified them.
        flags += [
            f'-I{os.path.normpath(x)}'
            for x in self.desc.get('include_dirs', [])
        ]
        flags += self.desc.get('cflags', [])

        if source.endswith('.c'):
            flags += self.desc.get('cflags_c', [])
        else:
            flags += self.desc.get('cflags_cc', [])

        return flags

    def _get_compile_command(self, source):
        # We select the appropriate compile commands based on this strategy:
        #   * Collect the definitions, include directories and compile flags
        #     from the build's description for the given target.
        #   * Check all compile command candidates from the compilation database
        #     whether they fully contain the flags collected from the
        #     description.
        #   * The first command that fully contains all the required flags
        #     is selected as the compile command on which this analysis is
        #     based.
        #
        # This approach might not always return the correct compile command
        # for all general usage scenarios, but usually if all definitions and
        # include directories are the same between two compile commands, then
        # the performed analysis should generate correct results either way.
        source = os.path.abspath(source)
        commands = (
            CCAdapter(command)
            for command in self.compilation_database.getCompileCommands(source)
        )

        flags = self._get_desc_flags(source)

        for command in commands:
            if not all(command.contains(x) for x in flags):
                continue

            return command

        message = f'unable to retrieve compile command for "{source}"'
        raise RuntimeError(message)

    def _analyze_translation_unit(self, tu):
        # Search for each inclusion directive, retrieve the used include
        # directory and store it.
        for cursor in tu.cursor.walk_preorder():
            if cursor.kind != clang.cindex.CursorKind.INCLUSION_DIRECTIVE:
                continue

            # Command-line inclusions like '-include' do not have a valid
            # source location.
            if not cursor.location.file:
                continue

            # Absolute paths are files outside of the repository. Usually
            # standard library headers. Short-circuit them.
            if os.path.isabs(cursor.location.file.name):
                continue

            # Path as written in the source code.
            relative_path = cursor.spelling

            # Complete path to included file.
            full_path = cursor.get_included_file().name

            # Make sure to get the original source file if a virtual file
            # system is used.
            full_path = self.vfs_map.get_source(full_path, full_path)

            # Deduce the used include directory.
            include_dir = full_path.removesuffix(relative_path)
            include_dir = os.path.normpath(include_dir)

            # Mark the directory as used.
            self.used_include_dirs.add(include_dir)

    def _dispatch_source(self, source):
        source = os.path.abspath(source)

        cc = self._get_compile_command(source)

        for path in cc.include_directories:
            self.provided_include_dirs.add(os.path.normpath(path))

        tu = self.index.parse(
            cc.filename,
            args=cc.args,
            options=(
                clang.cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD
                | clang.cindex.TranslationUnit.PARSE_SKIP_FUNCTION_BODIES
            ),
        )

        self._analyze_translation_unit(tu)

    def run(self):
        sources = (
            x
            for x in self.desc['sources']
            if os.path.splitext(x)[1] in {'.c', '.cc', '.cpp', '.cxx'}
        )

        for source in sources:
            self._dispatch_source(source)

        return self.provided_include_dirs - self.used_include_dirs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--compilation-database',
        help="The project's compilation database.",
        required=True,
        type=str,
    )
    parser.add_argument(
        '--vfs-config',
        help=(
            'A file descriping the mapping of files to each other as used in a '
            'virtual filesystem.'
        ),
        default=vfs.VirtualFileSystemMap(),
        type=vfs.VirtualFileSystemMap.from_vfs_config,
    )
    parser.add_argument(
        '--description',
        help="The project's build description.",
        required=True,
        type=gn.Description.from_file,
    )
    parser.add_argument(
        '--target',
        help=(
            'The target of the entity getting analysed. Used for the diagnostic '
            'message.'
        ),
        required=True,
        type=str,
    )
    parser.add_argument(
        '--exclude',
        help=(
            'Do not report unused include directores matching any of the '
            'specified globs.'
        ),
        default=[],
        required=False,
        type=str,
    )

    args = parser.parse_args()

    desc = args.description[args.target]

    analysis = UnusedIncludeDirectoriesAnalysis(
        args.compilation_database, args.vfs_config, desc
    )

    unused_includes = [
        include
        for include in analysis.run()
        if not util.any_fnmatch(include, args.exclude)
    ]

    entity = desc['metadata']['template'][0]
    for include in sorted(unused_includes):
        print(
            f'{args.target}: error: {entity} contains unused include '
            f'directory "{include}"',
            file=sys.stderr,
        )

    exit_code = len(unused_includes) != 0

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
