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

import os

import conan
import jinja2

GNI_TEMPLATE = r"""#
# Automatically generated file.
#

{% for package in packages -%}
# {{ package['name'] }}/{{ package['version'] }}
{{ package['name'].replace('-', '_') }} = {
  include_dirs = [
{%- for item in package['include_dirs'] %}
    "{{ item }}",
{%- endfor %}
  ]
  lib_dirs = [
{%- for item in package['lib_dirs'] %}
    "{{ item }}",
{%- endfor %}
  ]
  libs = [
{%- for item in package['libs'] %}
    "{{ item }}",
{%- endfor %}
  ]
  sources = [
{%- for item in package['sources'] %}
    "{{ item }}",
{%- endfor %}
  ]
}

{% endfor %}
"""


class GenerateNinjaDeps(conan.ConanFile):
    requires = 'zlib/1.3.1'

    def generate(self):
        # Collect required data for each dependency
        packages = []

        for dep in self.dependencies.values():
            include_dirs = [
                os.path.join(dep.package_folder, x)
                for x in dep.cpp_info.includedirs
            ]
            lib_dirs = [
                os.path.join(dep.package_folder, x)
                for x in dep.cpp_info.libdirs
            ]

            # Collect all sources within the specified include directories.
            sources = set()
            visited = set()

            for item in include_dirs:
                for parent, _, entries in os.walk(item):
                    if parent in visited:
                        continue

                    visited.add(parent)

                    sources.update(os.path.join(parent, x) for x in entries)

            packages.append(
                {
                    'name': dep.ref.name,
                    'version': dep.ref.version,
                    'include_dirs': sorted(include_dirs),
                    'lib_dirs': sorted(lib_dirs),
                    'libs': sorted(dep.cpp_info.libs),
                    'sources': sorted(sources),
                }
            )

        # Generate the output file with the collected data.
        template = jinja2.Template(GNI_TEMPLATE)
        output = template.render(packages=packages)

        conan.tools.files.save(
            self,
            os.path.join(self.generators_folder, 'vars.gni'),
            output,
        )
