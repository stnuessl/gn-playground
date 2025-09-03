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

import json
import os


class VirtualFileSystemMap:
    def __init__(self, table={}):
        self.table = table

    @staticmethod
    def from_vfs_config(path):
        with open(path, 'r') as f:
            items = json.load(f)

        table = {item['target']: item['source'] for item in items}

        return VirtualFileSystemMap(table)

    @staticmethod
    def from_vfs(path):
        with open(path, 'r') as f:
            vfs = json.load(f)

        vfs_roots = vfs['roots']

        table = {}
        for item in vfs_roots:
            if item['type'] != 'directory':
                continue

            for content in item['contents']:
                source = os.path.join(item['name'], content['name'])
                target = content['external-contents']

                table[target] = source

        return VirtualFileSystemMap(table)

    def get_source(self, target, default=None):
        return self.table.get(target, default)
