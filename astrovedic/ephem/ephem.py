"""
    This file is part of astrovedic - (C) FlatAngle
    Author: João Ventura (flatangleweb@gmail.com)


    This module implements functions which are useful
    for astrovedic. Basically, it converts internal objects
    and lists from the ephemeris to astrovedic.objects and
    astrovedic.lists.

    Flatlib users will want to use this module for
    accessing the ephemeris.

"""

from . import eph
from . import swe

from astrovedic import const
from astrovedic.datetime import Datetime
from astrovedic.object import (GenericObject, Object,
                            House, FixedStar, Asteroid, MoonNode)
from astrovedic.lists import (GenericList, ObjectList,
                           HouseList, FixedStarList)
from astrovedic.factory import AstronomicalObjectFactory
import logging

# Get logger
logger = logging.getLogger("flatlib")


# === Objects === #


def getObjectClass(ID):
    """Returns the corresponding class for the specified object"""
    if ID in const.LIST_TEN_PLANETS:
        return Object
    elif ID in const.LIST_ASTEROIDS:
        return Asteroid
    elif ID in const.LIST_MOON_NODES:
        return MoonNode
    else:
        return Object

def getObject(ID, date, pos):
    """ Returns an ephemeris object with validation. """
    try:
        obj_data = eph.getObject(ID, date.jd, pos.lat, pos.lon)

        # Determine object type based on ID
        if ID in const.LIST_TEN_PLANETS:
            obj_type = const.OBJ_PLANET
        elif ID in const.LIST_ASTEROIDS:
            obj_type = const.OBJ_ASTEROID
        elif ID in const.LIST_MOON_NODES:
            obj_type = const.OBJ_MOON_NODE
        else:
            obj_type = const.OBJ_GENERIC

        # Create object using factory
        return AstronomicalObjectFactory.create_object(obj_data, obj_type)
    except Exception as e:
        logger.error(f"Error in getObject for {ID}: {e}")
        # Create a minimal valid object
        obj_data = {
            'id': ID,
            'lon': 0.0,
            'lat': 0.0,
            'sign': const.ARIES,
            'signlon': 0.0,
            'lonspeed': 0.0,
            'latspeed': 0.0
        }
        return AstronomicalObjectFactory.create_object(obj_data)


def getObjectList(IDs, date, pos):
    """ Returns a list of objects. """
    objList = [getObject(ID, date, pos) for ID in IDs]
    return ObjectList(objList)


def get_object(obj, date, pos, alt=None, mode=None):
    """
    Returns an object for a specific date and location with validation.
    - If the altitude value is set, returns the topocentric position
    - If mode is set, returns sidereal positions for the given mode

    :param obj: the object
    :param date: the date
    :param pos: the geographical position
    :param alt: the altitude above msl in meters
    :param mode: the ayanamsa
    :return: Object
    """
    try:
        obj_values = eph.get_object(obj, date.jd, pos.lat, pos.lon, alt, mode)

        # Determine object type based on ID
        if obj in const.LIST_TEN_PLANETS:
            obj_type = const.OBJ_PLANET
        elif obj in const.LIST_ASTEROIDS:
            obj_type = const.OBJ_ASTEROID
        elif obj in const.LIST_MOON_NODES:
            obj_type = const.OBJ_MOON_NODE
        else:
            obj_type = const.OBJ_GENERIC

        # Create object using factory
        return AstronomicalObjectFactory.create_object(obj_values, obj_type)
    except Exception as e:
        logger.error(f"Error in get_object for {obj}: {e}")
        # Create a minimal valid object
        obj_values = {
            'id': obj,
            'lon': 0.0,
            'lat': 0.0,
            'sign': const.ARIES,
            'signlon': 0.0,
            'lonspeed': 0.0,
            'latspeed': 0.0
        }
        return AstronomicalObjectFactory.create_object(obj_values)


def get_objects(objs, date, pos, alt=None, mode=None):
    """
    Returns a list of object for a specific date and location.
    - If the altitude value is set, returns the topocentric position
    - If mode is set, returns sidereal positions for the given mode

    :param objs: the ids of the objects
    :param date: the date
    :param pos: the geographical position
    :param alt: the altitude above msl in meters
    :param mode: the ayanamsa
    :return: ObjectList
    """

    objects = [get_object(obj, date, pos, alt, mode) for obj in objs]
    return ObjectList(objects)


# === Houses and angles === #

def getHouses(date, pos, hsys, houses_offset):
    """ Returns the lists of houses and angles.

    Since houses and angles are computed at the
    same time, this function should be fast.

    """
    houses, angles = eph.getHouses(date.jd, pos.lat, pos.lon, hsys)
    hList = [House.fromDict(house, houses_offset) for house in houses]
    aList = [GenericObject.fromDict(angle) for angle in angles]
    return (HouseList(hList), GenericList(aList))


def getHouseList(date, pos, hsys, houses_offset):
    """ Returns a list of houses. """
    return getHouses(date, pos, hsys, houses_offset)[0]


def getAngleList(date, pos, hsys):
    """ Returns a list of angles (Asc, MC..) """
    return getHouses(date, pos, hsys, const.MODERN_HOUSE_OFFSET)[1]


def get_houses(date, pos, hsys, houses_offset=const.MODERN_HOUSE_OFFSET, mode=None):
    """ Returns a list of house and angle cusps.
    - If mode is set, returns sidereal positions for the given mode

    :param date: the date
    :param pos: the geographical position
    :param hsys: the house system
    :param houses_offset: offset for house calculations
    :param mode: the ayanamsa
    :return: list of houses and angles
    """

    houses, angles = eph.get_houses(date.jd, pos.lat, pos.lon, hsys, mode)
    house_list = [House.fromDict(house, houses_offset) for house in houses]
    angle_list = [GenericObject.fromDict(angle) for angle in angles]
    return HouseList(house_list), GenericList(angle_list)


# === Fixed stars === #

def getFixedStar(ID, date):
    """ Returns a fixed star from the ephemeris. """
    star = eph.getFixedStar(ID, date.jd)
    return FixedStar.fromDict(star)


def getFixedStarList(IDs, date):
    """ Returns a list of fixed stars. """
    starList = [getFixedStar(ID, date) for ID in IDs]
    return FixedStarList(starList)


# === Solar returns === #

def nextSolarReturn(date, lon):
    """ Returns the next date when sun is at longitude 'lon'. """
    jd = eph.nextSolarReturn(date.jd, lon)
    return Datetime.fromJD(jd, date.utcoffset)


def prevSolarReturn(date, lon):
    """ Returns the previous date when sun is at longitude 'lon'. """
    jd = eph.prevSolarReturn(date.jd, lon)
    return Datetime.fromJD(jd, date.utcoffset)


# === Sunrise and sunsets === #

def nextSunrise(date, pos):
    """ Returns the date of the next sunrise. """
    jd = eph.nextSunrise(date.jd, pos.lat, pos.lon)
    return Datetime.fromJD(jd, date.utcoffset)


def nextSunset(date, pos):
    """ Returns the date of the next sunset. """
    jd = eph.nextSunset(date.jd, pos.lat, pos.lon)
    return Datetime.fromJD(jd, date.utcoffset)


def lastSunrise(date, pos):
    """ Returns the date of the last sunrise. """
    jd = eph.lastSunrise(date.jd, pos.lat, pos.lon)
    return Datetime.fromJD(jd, date.utcoffset)


def lastSunset(date, pos):
    """ Returns the date of the last sunset. """
    jd = eph.lastSunset(date.jd, pos.lat, pos.lon)
    return Datetime.fromJD(jd, date.utcoffset)


# === Station === #

def nextStation(ID, date):
    """ Returns the aproximate date of the next station. """
    jd = eph.nextStation(ID, date.jd)
    return Datetime.fromJD(jd, date.utcoffset)


# === Eclipses === #

def prevSolarEclipse(date):
    """ Returns the Datetime of the maximum phase of the
    previous global solar eclipse.

    """

    eclipse = swe.solarEclipseGlobal(date.jd, backward=True)
    return Datetime.fromJD(eclipse['maximum'], date.utcoffset)


def nextSolarEclipse(date):
    """ Returns the Datetime of the maximum phase of the
    next global solar eclipse.

    """

    eclipse = swe.solarEclipseGlobal(date.jd, backward=False)
    return Datetime.fromJD(eclipse['maximum'], date.utcoffset)


def prevLunarEclipse(date):
    """ Returns the Datetime of the maximum phase of the
    previous global lunar eclipse.

    """

    eclipse = swe.lunarEclipseGlobal(date.jd, backward=True)
    return Datetime.fromJD(eclipse['maximum'], date.utcoffset)


def nextLunarEclipse(date):
    """ Returns the Datetime of the maximum phase of the
    next global lunar eclipse.

    """

    eclipse = swe.lunarEclipseGlobal(date.jd, backward=False)
    return Datetime.fromJD(eclipse['maximum'], date.utcoffset)
