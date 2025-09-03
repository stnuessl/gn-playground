#
# Copyright (C) 2023-2025  Steffen Nuessle
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

FROM archlinux:base
RUN pacman -Syu --noconfirm \
    ccache \
    clang \
    gcc \
    git \
    gn \
    gtest \
    llvm \
    ninja \
    python \
    ruff \
    uv \
&& pacman -Scc --noconfirm \
&& useradd \
    --no-create-home \
    --shell /usr/bin/bash \
    arch
USER arch
CMD [ "/usr/bin/bash" ]

