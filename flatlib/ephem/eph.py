"""
    This file is part of flatlib - (C) FlatAngle
    Author: João Ventura (flatangleweb@gmail.com)


    This module implements functions for retrieving
    astronomical and astrological data from an ephemeris.

    It is as middle layer between the Swiss Ephemeris
    and user software. Objects are treated as python
    dicts and jd/lat/lon as float.

"""

from . import swe
from . import tools
from flatlib import angle
from flatlib import const
import logging

# Import Vedic modules for shadow planets
try:
    from flatlib.vedic import upagrah
    VEDIC_MODULES_AVAILABLE = True
except ImportError:
    VEDIC_MODULES_AVAILABLE = False

# Get logger
logger = logging.getLogger("flatlib")


# === Objects === #

def getObject(ID, jd, lat, lon):
    """ Returns an object for a specific date and
    location with error handling.

    """
    try:
        # Handle Ketu (South Node)
        if ID == const.KETU or ID == const.SOUTH_NODE:
            try:
                obj = swe.sweObject(const.RAHU, jd)
                obj.update({
                    'id': ID,
                    'lon': angle.norm(obj['lon'] + 180)
                })
            except Exception as e:
                logger.error(f"Error calculating {ID}: {e}")
                obj = {
                    'id': ID,
                    'lon': 0.0,
                    'lat': 0.0,
                    'lonspeed': 0.0,
                    'latspeed': 0.0
                }
        # Handle shadow planets (Upagrah)
        elif ID in const.LIST_SHADOW_PLANETS and VEDIC_MODULES_AVAILABLE:
            try:
                if ID in [const.GULIKA, const.MANDI]:
                    obj = upagrah.get_upagrah(ID, jd, lat, lon)
                else:
                    obj = upagrah.get_upagrah(ID, jd)
            except Exception as e:
                logger.error(f"Error calculating {ID}: {e}")
                obj = {
                    'id': ID,
                    'lon': 0.0,
                    'lat': 0.0,
                    'lonspeed': 0.0,
                    'latspeed': 0.0
                }
        # Outer planets are handled by the default case
        # Pars Fortuna has been removed for Vedic implementation
        elif ID == const.SYZYGY:
            try:
                szjd = tools.syzygyJD(jd)
                obj = swe.sweObject(const.MOON, szjd)
                obj['id'] = const.SYZYGY
            except Exception as e:
                logger.error(f"Error calculating Syzygy: {e}")
                obj = {
                    'id': const.SYZYGY,
                    'lon': 0.0,
                    'lat': 0.0,
                    'lonspeed': 0.0,
                    'latspeed': 0.0
                }
        else:
            try:
                obj = swe.sweObject(ID, jd)
            except Exception as e:
                logger.error(f"Error calculating object {ID}: {e}")
                obj = {
                    'id': ID,
                    'lon': 0.0,
                    'lat': 0.0,
                    'lonspeed': 0.0,
                    'latspeed': 0.0
                }

        # Ensure all required attributes are present
        _signInfo(obj)

        # Validate the object has all required attributes
        required_attrs = ['id', 'lon', 'lat', 'sign', 'signlon']
        for attr in required_attrs:
            if attr not in obj:
                raise ValueError(f"Missing required attribute: {attr}")

        return obj
    except Exception as e:
        # Log the error and return a minimal valid object
        logger.error(f"Error creating object {ID}: {e}")
        obj = {
            'id': ID,
            'lon': 0.0,
            'lat': 0.0,
            'sign': const.ARIES,
            'signlon': 0.0,
            'lonspeed': 0.0,
            'latspeed': 0.0
        }
        return obj


# === Houses === #

def getHouses(jd, lat, lon, hsys):
    """ Returns lists of houses and angles. """
    houses, angles = swe.sweHouses(jd, lat, lon, hsys)
    for house in houses:
        _signInfo(house)
    for angle in angles:
        _signInfo(angle)
    return (houses, angles)


# === Fixed stars === #

def getFixedStar(ID, jd):
    """ Returns a fixed star. """
    star = swe.sweFixedStar(ID, jd)
    _signInfo(star)
    return star


# === Solar returns === #

def nextSolarReturn(jd, lon):
    """ Return the JD of the next solar return. """
    return tools.solarReturnJD(jd, lon, True)


def prevSolarReturn(jd, lon):
    """ Returns the JD of the previous solar return. """
    return tools.solarReturnJD(jd, lon, False)


# === Sunrise and sunsets === #

def nextSunrise(jd, lat, lon, mode=None):
    """
    Returns the JD of the next sunrise.

    Args:
        jd (float): Julian day
        lat (float): Latitude in degrees
        lon (float): Longitude in degrees
        mode (str, optional): Ayanamsa mode for sidereal calculations

    Returns:
        float: Julian day of the next sunrise
    """
    return swe.sweNextTransit(const.SUN, jd, lat, lon, 'RISE', mode)


def nextSunset(jd, lat, lon, mode=None):
    """
    Returns the JD of the next sunset.

    Args:
        jd (float): Julian day
        lat (float): Latitude in degrees
        lon (float): Longitude in degrees
        mode (str, optional): Ayanamsa mode for sidereal calculations

    Returns:
        float: Julian day of the next sunset
    """
    return swe.sweNextTransit(const.SUN, jd, lat, lon, 'SET', mode)


def lastSunrise(jd, lat, lon, mode=None):
    """
    Returns the JD of the last sunrise.

    Args:
        jd (float): Julian day
        lat (float): Latitude in degrees
        lon (float): Longitude in degrees
        mode (str, optional): Ayanamsa mode for sidereal calculations

    Returns:
        float: Julian day of the last sunrise
    """
    return nextSunrise(jd - 1.0, lat, lon, mode)


def lastSunset(jd, lat, lon, mode=None):
    """
    Returns the JD of the last sunset.

    Args:
        jd (float): Julian day
        lat (float): Latitude in degrees
        lon (float): Longitude in degrees
        mode (str, optional): Ayanamsa mode for sidereal calculations

    Returns:
        float: Julian day of the last sunset
    """
    return nextSunset(jd - 1.0, lat, lon, mode)


# === Transits === #

def nextLonTransit(obj, jd, target_lon, mode=None):
    """
    Returns the JD when a planet crosses a specific longitude.

    Args:
        obj (str): Object ID
        jd (float): Julian day to start search from
        target_lon (float): Target longitude in degrees
        mode (str, optional): Ayanamsa mode for sidereal calculations

    Returns:
        float: Julian day of the longitude transit
    """
    return swe.sweNextLonTransit(obj, jd, target_lon, False, mode)


def lastLonTransit(obj, jd, target_lon, mode=None):
    """
    Returns the JD when a planet last crossed a specific longitude.

    Args:
        obj (str): Object ID
        jd (float): Julian day to start search from
        target_lon (float): Target longitude in degrees
        mode (str, optional): Ayanamsa mode for sidereal calculations

    Returns:
        float: Julian day of the longitude transit
    """
    return swe.sweNextLonTransit(obj, jd, target_lon, True, mode)


def nextSignTransit(obj, jd, sign, mode=None):
    """
    Returns the JD when a planet enters a specific sign.

    Args:
        obj (str): Object ID
        jd (float): Julian day to start search from
        sign (int): Sign number (1-12)
        mode (str, optional): Ayanamsa mode for sidereal calculations

    Returns:
        float: Julian day of the sign transit
    """
    # Convert sign number to longitude (start of sign)
    target_lon = (sign - 1) * 30.0
    return nextLonTransit(obj, jd, target_lon, mode)


def lastSignTransit(obj, jd, sign, mode=None):
    """
    Returns the JD when a planet last entered a specific sign.

    Args:
        obj (str): Object ID
        jd (float): Julian day to start search from
        sign (int): Sign number (1-12)
        mode (str, optional): Ayanamsa mode for sidereal calculations

    Returns:
        float: Julian day of the sign transit
    """
    # Convert sign number to longitude (start of sign)
    target_lon = (sign - 1) * 30.0
    return lastLonTransit(obj, jd, target_lon, mode)


# === Stations === #

def nextStation(ID, jd):
    """ Returns the aproximate jd of the next station. """
    return tools.nextStationJD(ID, jd)


# === Other functions === #

def _signInfo(obj):
    """ Appends the sign id and longitude to an object. """
    lon = obj['lon']
    obj.update({
        'sign': const.LIST_SIGNS[int(lon / 30)],
        'signlon': lon % 30
    })


# === Objects and houses (sidereal and topocentric functions) === #


def get_object(obj, jd, lat=None, lon=None, alt=None, mode=None):
    """
    Returns an object for a specific date and location with error handling.
    - If lat/lon/alt values are set, it returns the topocentric position
    - If mode is set, returns sidereal positions for the given mode

    :param obj: the object
    :param jd: the julian date
    :param lat: the latitude in degrees
    :param lon: the longitude in degrees
    :param alt: the altitude above msl in meters
    :param mode: the ayanamsa
    :return: dictionary
    """
    try:
        if obj == const.SOUTH_NODE:
            try:
                eph_obj = swe.swe_object(const.NORTH_NODE, jd, lat, lon, alt, mode)
                eph_obj.update(
                    {"id": const.SOUTH_NODE, "lon": angle.norm(eph_obj["lon"] + 180)}
                )
            except Exception as e:
                logger.error(f"Error calculating South Node: {e}")
                eph_obj = {
                    'id': const.SOUTH_NODE,
                    'lon': 0.0,
                    'lat': 0.0,
                    'lonspeed': 0.0,
                    'latspeed': 0.0
                }

        # Commented out PARS_FORTUNA as it is not defined in const for Vedic implementation
        # elif obj == const.PARS_FORTUNA:
        #     try:
        #         # TODO: tools.pfLon must compute sidereal/topocentric positions
        #         pflon = tools.pfLon(jd, lat, lon)
        #     except Exception as e:
        #         logger.error(f"Error calculating Pars Fortuna: {e}")
        #         pflon = 0.0
        #
        #     eph_obj = {"id": obj, "lon": pflon, "lat": 0, "lonspeed": 0, "latspeed": 0}

        elif obj == const.SYZYGY:
            try:
                szjd = tools.syzygyJD(jd)
                eph_obj = swe.swe_object(const.MOON, szjd, lat, lon, alt, mode)
                eph_obj["id"] = const.SYZYGY
            except Exception as e:
                logger.error(f"Error calculating Syzygy: {e}")
                eph_obj = {
                    'id': const.SYZYGY,
                    'lon': 0.0,
                    'lat': 0.0,
                    'lonspeed': 0.0,
                    'latspeed': 0.0
                }

        else:
            try:
                eph_obj = swe.swe_object(obj, jd, lat, lon, alt, mode)
            except Exception as e:
                logger.error(f"Error calculating object {obj}: {e}")
                eph_obj = {
                    'id': obj,
                    'lon': 0.0,
                    'lat': 0.0,
                    'lonspeed': 0.0,
                    'latspeed': 0.0
                }

        # Ensure all required attributes are present
        _signInfo(eph_obj)

        # Validate the object has all required attributes
        required_attrs = ['id', 'lon', 'lat', 'sign', 'signlon']
        for attr in required_attrs:
            if attr not in eph_obj:
                raise ValueError(f"Missing required attribute: {attr}")

        return eph_obj
    except Exception as e:
        # Log the error and return a minimal valid object
        logger.error(f"Error creating object {obj}: {e}")
        eph_obj = {
            'id': obj,
            'lon': 0.0,
            'lat': 0.0,
            'sign': const.ARIES,
            'signlon': 0.0,
            'lonspeed': 0.0,
            'latspeed': 0.0
        }
        return eph_obj


def get_houses(jd, lat, lon, hsys, mode=None):
    """
    Returns a list of house and angle cusps.
    - If mode is set, returns sidereal positions for the given mode

    :param jd: the julian date
    :param lat: the latitude in degrees
    :param lon: the longitude in degrees
    :param hsys: the house system
    :param mode: the ayanamsa
    :return: list of houses and angles
    """
    houses, angles = swe.swe_houses(jd, lat, lon, hsys, mode)

    for house in houses:
        _signInfo(house)
    for angle in angles:
        _signInfo(angle)

    return houses, angles
