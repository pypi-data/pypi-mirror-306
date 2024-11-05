# test_enums - Testing greenland.base.enums
# Copyright (C) <year>  <name of author>
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
import pytest

# Note: A lot of simple tests/examples are embedded in the manual via literate
# programming.


class Direction(Enum):
    pass


NORTH  = Direction('NORTH')
EAST = Direction('EAST')
SOUTH = Direction('SOUTH')
WEST = Direction('WEST')

Direction.finalize()


def test_base_enums():

    with pytest.raises(AssertionError):
        _ = Direction('FOO')

    assert list(Direction) == [
        NORTH,
        EAST,
        SOUTH,
        WEST
    ]


def test_local_enums():
    class Turn(Enum):
        pass

    LEFT = Turn('LEFT')
    RIGHT = Turn('RIGHT')

    Turn.finalize(locals())

    with pytest.raises(AssertionError):
        _ = Turn('FOO')


def test_GLBS_I1():  # Issue #1 repproduction

    d = {}

    d[NORTH] = 0
    d[SOUTH] = 180

    assert WEST not in d
    assert EAST not in d

    assert d[NORTH] == 0
    assert d[SOUTH] == 180
