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

import functools
import itertools
import json
import os

from . import label


class Description:
    def __init__(self, desc):
        self.desc = dict(desc)

    def __len__(self):
        return len(self.desc)

    @staticmethod
    def from_file(path):
        with open(path, 'r') as f:
            desc = json.load(f)

        return Description(desc)

    @property
    def data(self):
        return self.desc

    def __getitem__(self, label):
        return self.desc[label]

    def items(self):
        return ((target, data) for target, data in self.desc.items())

    def get_if(self, predicate):
        """Return a description consisting only of targets for which the
        specified predicate is true.
        """
        return Description(
            {
                target: data
                for target, data in self.desc.items()
                if predicate(data)
            }
        )

    def extract_targets(self, *, predicate=bool):
        """Return all target labels from the description."""
        return (target for target in self.desc if predicate(target))

    def extract(self, attribute, *, flatten=False, predicate=bool):
        """Return a specific attribute from all targets in the description."""
        values = (data[attribute] for data in self.desc.values())

        if flatten:
            values = itertools.chain(*values)

        return (item for item in values if predicate(item))

    def get_subdesc(self, target, *, predicate=bool):
        """Return a description containing the specified target and all of its
        recursively related dependencies.
        """
        deps = [label.remove_toolchain(target)]
        values = {}
        visited = set()

        while len(deps) != 0:
            # Remove any potentially attached toolchain label, as keys used to
            # retrieve targets from the description are always without the
            # toolchain label.
            target = label.remove_toolchain(deps.pop())

            if target in visited:
                continue

            visited.add(target)

            data = self.desc[target]
            deps.extend(data['deps'])

            if predicate(data):
                values[target] = data

        return Description(values)


class Metadata:
    def __init__(self, metadata):
        self.metadata = list(metadata)

    @staticmethod
    def from_file(path):
        with open(path, 'r') as f:
            metadata = json.load(f)

        return Metadata(metadata)

    @property
    def data(self):
        return self.metadata

    def get_if(self, predicate):
        return Metadata(item for item in self.metadata if predicate(item))

    def extract(self, attribute):
        return (item[attribute] for item in self.metadata)

    @functools.cached_property
    def _path_lookup(self):
        return {item['source']: item for item in self.metadata}

    def get_file_metadata(self, path):
        return self._path_lookup[path]

    def get_file_attribute(self, path, attribute):
        return self.get_file_metadata(path)[attribute]


@functools.cache
def root(path=None, default=None):
    if not path:
        path = os.getcwd()

    path = os.path.abspath(path)

    while True:
        if os.path.isfile(os.path.join(path, '.gn')):
            return path

        parent = os.path.dirname(path)
        if path == parent:
            if default is not None:
                return default

            message = "failed to detect GN's root directory"
            raise RuntimeError(message)

        path = parent
