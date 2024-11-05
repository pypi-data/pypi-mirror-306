=============================
Module `greenland.base.enums`
=============================

.. implementation: ../src/greenland/base/enums.py
.. automodule::    greenland.base.enums
.. currentmodule:: greenland.base.enums

The way programming languages handle "enums" --- a small set of
discrete objects belonging together, like primary colors or days of
the week -- is often influenced by the capabilities of the programming
language whithin which such a facility exists. Very often the emphasis
is on providing names (identifiers) for integers as if the central
semantics of e.g. a weekday is it being a number. Enums in C certainly
work like this.

One unfortunate consequence of these types of design decisions is,
that it is difficult to express in type annotations that a certain
parameter should only take members of a specific enum. The conclusion
we must draw is, that it is desirable that enum types correspond to
classes and that the enum members are instances of those classes, so
it is possible to express the following:

.. code-block:: python

   def foo(day: Weekday):
       ...

The built-in enums of *Python* work like this already.  The author of
this package also became (admittedly) aware of the built-in enums too
late, so went down a slightly different (but possibly simpler) path.

This package provides enums as a type where the enumeration type is a
class (almost like any other) which only has a finite, explicitely
specified number of instances (the members) and where the enum member
can be enriched with almost any kind of additional behaviour.


Constructing enum types with :py:class:`Enum`
=============================================

.. autoclass:: Enum(name_or_ord: Union[str, int], ord: Union[int,None] = None)

.. literate-code:: Define enum type and members

   from greenland.base.enums import Enum


   class Direction(Enum):
       pass


   NORTH  = Direction('NORTH')
   EAST = Direction('EAST')
   SOUTH = Direction('SOUTH')
   WEST = Direction('WEST')

   Direction.finalize()

:py:meth:`finalize` will actually do two things:

- Lock the type so that further calls to the constructor result either
  in retrieval of an already defined member or in raising a
  :py:class:`ParseError` if no such member exists.

- Check if all members have been bound to names in the same namespace
  where the enum class has been defined.

.. literate-code:: Behavior after finalization
   :lang: python

   assert Direction('SOUTH') == SOUTH

   with pytest.raises(AssertionError):
       _ = Direction('FOO')


Typically enums are global types. I cannot currently see (except for
testing purposes) much of an application for defining an enum in a
local namespace.

Regardless, if one desires to do so, this is possible, but
:py:meth:`finalize` needs to be called with :py-code:`locals()`:

.. literate-code:: Local enum definition

   class Turn(Enum):
       pass

   LEFT = Turn('LEFT')
   RIGHT = Turn('RIGHT')

   Turn.finalize(locals())


Membership
----------

Membership (if a value is a member of an enum) can be tested using the
operator *in* or using *isinstance*.

.. literate-code:: Testing membership

   assert SOUTH in Direction
   assert isinstance(SOUTH, Direction)

   thing = object()

   assert thing not in Direction


Iteration
---------

The members of an enum type can be iterated over with the operator
*in*. The order in which the members are provided by the iterator is
the order of definition.

.. literate-code:: Iterate over enum members

   members = []

   for member in Direction:
       members.append(member)

   assert members == [NORTH, EAST, SOUTH, WEST]


An iterator can also be explicitely obtained using the property
:py:attr:`member`.

.. literate-code:: Iterate over enum members with the property 'members'

   members = []

   for member in Direction.members:
       members.append(member)

   assert members == [NORTH, EAST, SOUTH, WEST]


Sort order
----------

.. literate-code:: Default ordering

   assert NORTH < SOUTH
   assert not NORTH > SOUTH
   assert EAST  > NORTH
   assert not EAST < NORTH
   assert EAST != NORTH


Conversion to and from numbers
------------------------------

.. literate-code:: Conversion to and from numbers

   assert SOUTH.ord == 2
   assert int(SOUTH) == 2
   assert Direction(2) is SOUTH
   assert Direction[2] is SOUTH


Conversion to and from strings
------------------------------

.. literate-code:: Conversion to and from strings

   assert str(SOUTH) == 'SOUTH'
   assert repr(SOUTH) == 'SOUTH'
   assert Direction('SOUTH') is SOUTH
   assert Direction['SOUTH'] is SOUTH


Explicitely specifying `ord`
----------------------------

:py:meth:`ord` can be overridden in the default constructor with the
keyword argument ``ord``. It is possible to provide an own
constructor, but it then should be considered whether and how to pass
on ``ord`` to the super class :py:class:`Enum`.

.. literate-code:: Explicitely specifying ord

   class Quartett(Enum):
       pass

   ONE = Quartett('ONE')                # automatic ord = 0
   TWO = Quartett('TWO', ord = 100)
   THREE = Quartett('THREE')            # automatic ord = 101
   FOUR = Quartett('FOUR', ord = 50)
   
   Quartett.finalize(locals())

Those members where ``ord`` is specified get the desired
:py:attr:`ord`, but will raise an assertion if the ord value already
exists. Where no ``ord`` is specified, an :py:attr:`ord` value (one)
larger than all :py:attr:`ord` values of the members existing so far
is chosen automatically. This algorithm has the advantage of
preserving the definition order in the sort order as far as possible,
but avoids unwelcome surprises.

.. literate-code:: Overridden ord values

   assert ONE.ord == 0
   assert TWO.ord == 100
   assert THREE.ord == 101
   assert FOUR.ord == 50

The sort order is defined by the :py:attr:`ord` attribute of the enum
members.
   
.. literate-code:: Sort order when overriding ord

   assert FOUR < THREE
   assert FOUR < TWO

Whereas the iteration order is always the order in which the members where defined.
   
.. literate-code:: Unchanged iteration order when overriding ord

   assert list(Quartett.members) == [
       ONE, TWO, THREE, FOUR
   ]
		   

Attributes
----------

(TBD)

.. ?

   Should we really document the single methods, given that above we
   have already given complete examples?

.. !

   No public methods!


Typing
------

(TBD)

.. literate-code:: Typed function example

   def print_direction(d: Direction) -> None:
       print(d)


   print_direction(NORTH)

.. ?

   Failsafes.


Example(s)
==========

The complete code examples can be found in the file *enums-example.py*
in the doc distribution archive or in ``doc/_build/tangle`` after
building the documentation with ``make tangle``.

.. only:: tangle

   .. literate-code:: Copyright header
      :lang: python

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


   .. literate-code:: enums-example.py
      :lang: python
      :file:

      {{Copyright header}}

      import pytest

      {{Define enum type and members}}


      def test():

          # Behavior after finalization

          {{Behavior after finalization}}

	  # Membership tests

	  {{Testing membership}}

	  # Conversion to and from numbers

          {{Conversion to and from numbers}}

	  # Conversion to and from strings

	  {{Conversion to and from strings}}

	  # Iterating over enum members

	  {{Iterate over enum members}}
	  {{Iterate over enum members with the property 'members'}}

	  # Default ordering

	  {{Default ordering}}


      # Defining an enum in a local namespace

      def test_local_enum_definition():

  	  {{Local enum definition}}
	  

      # Explicitely specifying ord

      def test_explicitely_ord_specification():

          {{Explicitely specifying ord}}
   
	  {{Overridden ord values}}
      
	  {{Sort order when overriding ord}}

	  {{Unchanged iteration order when overriding ord}}

	  
   .. literate-code:: enums-typing-example.py
      :lang: python
      :file:

      {{Copyright header}}

      {{Define enum type and members}}


      {{Typed function example}}


Comparison to built-in enum
===========================

- TBD: More complicated
- TBD: Only a single construction parameter


Design decisions and alternatives
=================================

(TBD)
