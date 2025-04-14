"""
    This file is part of flatlib - (C) FlatAngle
    Author: João Ventura (flatangleweb@gmail.com)


    This module defines interfaces for flatlib objects to ensure
    consistent attribute availability and validation.

"""

from abc import ABC


class IAstronomicalObject(ABC):
    """Interface defining the minimum required attributes for all astronomical objects"""
    # We're using a protocol-like approach rather than strict abstract methods
    # to maintain compatibility with existing code
    pass


class IOrbitalObject(IAstronomicalObject):
    """Interface for objects with orbital properties"""
    pass


class IHouse(IAstronomicalObject):
    """Interface for house objects"""
    pass


class IFixedStar(IAstronomicalObject):
    """Interface for fixed star objects"""
    pass
