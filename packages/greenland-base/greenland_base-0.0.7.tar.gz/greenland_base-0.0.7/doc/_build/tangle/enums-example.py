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

import pytest

from greenland.base.enums import Enum


class Direction(Enum):
    pass


NORTH  = Direction('NORTH')
EAST = Direction('EAST')
SOUTH = Direction('SOUTH')
WEST = Direction('WEST')

Direction.finalize()


def test():

    # Behavior after finalization

    assert Direction('SOUTH') == SOUTH

    with pytest.raises(AssertionError):
        _ = Direction('FOO')

    # Membership tests

    assert SOUTH in Direction
    assert isinstance(SOUTH, Direction)

    thing = object()

    assert thing not in Direction

    # Conversion to and from numbers

    assert SOUTH.ord == 2
    assert int(SOUTH) == 2
    assert Direction(2) is SOUTH
    assert Direction[2] is SOUTH

    # Conversion to and from strings

    assert str(SOUTH) == 'SOUTH'
    assert repr(SOUTH) == 'SOUTH'
    assert Direction('SOUTH') is SOUTH
    assert Direction['SOUTH'] is SOUTH

    # Iterating over enum members

    members = []

    for member in Direction:
        members.append(member)

    assert members == [NORTH, EAST, SOUTH, WEST]
    members = []

    for member in Direction.members:
        members.append(member)

    assert members == [NORTH, EAST, SOUTH, WEST]

    # Default ordering

    assert NORTH < SOUTH
    assert not NORTH > SOUTH
    assert EAST  > NORTH
    assert not EAST < NORTH
    assert EAST != NORTH


# Defining an enum in a local namespace

def test_local_enum_definition():

    class Turn(Enum):
        pass

    LEFT = Turn('LEFT')
    RIGHT = Turn('RIGHT')

    Turn.finalize(locals())


# Explicitely specifying ord

def test_explicitely_ord_specification():

    class Quartett(Enum):
        pass

    ONE = Quartett('ONE')                # automatic ord = 0
    TWO = Quartett('TWO', ord = 100)
    THREE = Quartett('THREE')            # automatic ord = 101
    FOUR = Quartett('FOUR', ord = 50)

    Quartett.finalize(locals())

    assert ONE.ord == 0
    assert TWO.ord == 100
    assert THREE.ord == 101
    assert FOUR.ord == 50

    assert FOUR < THREE
    assert FOUR < TWO

    assert list(Quartett.members) == [
        ONE, TWO, THREE, FOUR
    ]
