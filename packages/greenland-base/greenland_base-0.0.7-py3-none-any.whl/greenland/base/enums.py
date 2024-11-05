# test_enums - Testing greenland.base.enums
# Copyright (C) 2024 M E Leypold
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

"""Provides an enumeration (Enum) type as python objects.
"""

# Documentation, see ../../../doc/enums.rst

import sys
from typing import Union, Any

from functools import total_ordering


class ParseError(AssertionError):
    pass


class EnumMeta(type):

    _members: Union[None, list['Enum']] = None
    _members_by_name: Union[None, dict[str, 'Enum']] = None
    _members_by_ord: Union[None, dict[int, 'Enum']] = None
    _finalized: bool = False

    @property
    def members(cls):
        assert cls.is_enum_type
        for member in cls._members:
            yield member

    def __iter__(cls):
        return cls.members

    @property
    def is_enum_type(cls):
        return cls._members is not None

    def __call__(
            cls,
            name_or_ord: Union[str, int],
            *pargs,
            ord: Union[int, None] = None,
            **kwargs
    ):

        if not cls._finalized:
            assert isinstance(name_or_ord, str)
            return super().__call__(name_or_ord, *pargs, ord=ord, **kwargs)
        else:
            assert ord is None
            assert not pargs and not kwargs, \
                "Only as single argument of type str or int" \
                " can be used to retrieve enums from enum type" \
                " using the constructor"

            return cls[name_or_ord]

    # TODO: Improve on this typing. Return type should be an instance of cls,
    #       instead of just enum. See also:
    #       https://mypy.readthedocs.io/en/stable/more_types.html#precise-typing-of-alternative-constructors

    def __getitem__(cls: 'EnumMeta', name_or_ord: Union[str, int]) -> 'Enum':

        assert cls._members_by_ord is not None
        assert cls._members_by_name is not None

        if isinstance(name_or_ord, str):
            if name_or_ord not in cls._members_by_name:
                raise ParseError(
                    "No member with name {repr(name_or_ord)} in {cls}"
                )
            return cls._members_by_name[name_or_ord]
        else:
            assert isinstance(name_or_ord, int), \
                "Expected ord or name of enum member from {cls}"
            if name_or_ord not in cls._members_by_ord:
                raise ParseError(
                    "No member with ord {repr(name_or_ord)} in {cls}"
                )
            return cls._members_by_ord[name_or_ord]

    def __contains__(cls, thing: Any) -> bool:
        return isinstance(thing, cls)


@total_ordering
class Enum(object, metaclass=EnumMeta):

    """The super class of all enum types (= classes).

    Enum types are created by deriving from :py:class:`Enum`. Members
    are added by calling the constructor and assigning to an
    identifier in the same namespace as the class definition before
    calling :py:meth:`finalize()`.

    After :py:meth:`finalize()`, the constructor will just either
    return a previously existing member of the enum type or raise a
    :py:class:`ParseError`.

    Args:

      name_or_ord: Before finalizing the enum type only the name of
        the enum member --- a ``str`` -- is allowed here. After
        finalization both a ``str`` and a ``int`` here are allowed and
        do not construct a new member, but rather retrieve a member of
        the give *name* or *ord* respectively. A
        :py:class:`ParseError` will be raised if such a member does
        not exist.

      ord: Before finalizing the the enum type an optional ``ord``
        integer for the member. After finalization this argument must
        not be given.

    """

    # For more documentation, see ../../../doc/enums.rst

    _ord: int
    _name: str

    def __init__(self, name: str, ord = None):
        if ord is None:
            if self.__class__._members_by_ord:
                ord = max(self.__class__._members_by_ord.keys()) + 1
            else:
                ord = 0
        self._ord = ord
        self._name = name

        # Note: mypy is too limited to understand that we'll only ever
        # instantiate subclasses of Enum and that in these classes the
        # members will already have been initialized. Also mypy
        # doesn't take into consideration post condiations of methods
        # (like changes or state guarantees) execpt as encoded by the
        # return type.
        #
        # See also: https://stackoverflow.com/questions/65903525/
        #              postcondition-of-a-method-with-mypy
        #
        # We therefore have to insert the explicit asserts to convince
        # mypy (and cannot put them into a assert_enum_type, AFAICS).

        assert self.__class__._members_by_ord is not None
        assert self.__class__._members_by_name is not None
        assert self.__class__._members is not None

        assert ord not in self.__class__._members_by_ord.keys(), \
            f"Member with ord = {ord} already exists"
        self.__class__._members.append(self)
        self.__class__._members_by_name[name] = self
        self.__class__._members_by_ord[ord] = self

    def __init_subclass__(cls):
        cls._members = []
        cls._members_by_name = {}
        cls._members_by_ord = {}

    def __str__(self):
        return self._name

    def __repr__(self):
        return self._name

    def __int__(self):
        return self._ord

    @property
    def ord(self):
        return self._ord

    def __lt__(self, other) -> bool:
        assert isinstance(other, self.__class__)
        return self.ord < other.ord

    def __eq__(self, other) -> bool:
        return self is other

    def __hash__(self) -> int:

        # See
        # https://docs.python.org/3/reference/datamodel.html#object.__hash__
        #
        #   A class that overrides __eq__() and does not define
        #   __hash__() will have its __hash__() implicitly set to None.

        return super().__hash__()

    @classmethod
    def _module(cls):
        return sys.modules[cls.__module__]

    @classmethod
    def finalize(cls, namespace=None):

        if namespace is None:
            module = cls._module()
            namespace = module.__dict__
        else:
            module = None

        bound  = None
        try:
            bound = namespace[cls.__name__]
            assert bound is cls, \
                "TBD"

        except KeyError:
            assert False, \
                "TBD"
        bound  = None
        for member in cls.members:
            try:
                bound = namespace[str(member)]
                assert bound is member, \
                    "TBD"
            except KeyError:
                assert False, \
                    f"{cls.__name__} member {str(member)} not bound under" \
                    f" its name {repr(str(member))} in" \
                    f" {module or 'local namespace'}"

        cls._finalized = True
