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

import functools
import json


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
