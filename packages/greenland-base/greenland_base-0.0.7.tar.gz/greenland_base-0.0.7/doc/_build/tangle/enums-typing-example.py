# greenland.base.enums -- Examples & Embedded Tests
# Copyright (C) 2024, M E Leypold
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from greenland.base.enums import Enum


class Direction(Enum):
    pass


NORTH  = Direction('NORTH')
EAST = Direction('EAST')
SOUTH = Direction('SOUTH')
WEST = Direction('WEST')

Direction.finalize()


def print_direction(d: Direction) -> None:
    print(d)


print_direction(NORTH)
