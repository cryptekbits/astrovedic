"""
    This file is part of astrovedic - (C) FlatAngle
    
    This module implements cached functions for retrieving
    astronomical and astrological data from an ephemeris.
    
    It is a middle layer between the Swiss Ephemeris
    and user software. Objects are treated as python
    dicts and jd/lat/lon as float.
"""

from astrovedic import angle
from astrovedic import const
from astrovedic.ephem import tools
from astrovedic.cache import ephemeris_cache
import logging

# Import cached Swiss Ephemeris functions
from astrovedic.ephem.swe_cached import (
    sweObject, sweObjectLon, sweNextTransit,
    sweHouses, sweHousesLon, sweFixedStar,
    solarEclipseGlobal, swe_object, swe_houses
)

# Import Vedic modules for shadow planets
try:
    from astrovedic.vedic import upagrah
    VEDIC_MODULES_AVAILABLE = True
except ImportError:
    VEDIC_MODULES_AVAILABLE = False

# Get logger
logger = logging.getLogger("flatlib")


# === Helper functions === #

def _signInfo(obj):
    """ Adds sign information to an object. """
    lon = obj['lon']
    obj['sign'] = const.LIST_SIGNS[int(lon / 30)]
    obj['signlon'] = lon % 30
    return obj


# === Objects === #

@ephemeris_cache()
def getObject(ID, jd, lat=None, lon=None):
    """ Returns an object from the ephemeris. """
    try:
        # Handle Ketu (South Node)
        if ID == const.KETU or ID == const.SOUTH_NODE:
            try:
                obj = sweObject(const.RAHU, jd)
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
                obj = sweObject(const.MOON, szjd)
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
                obj = sweObject(ID, jd)
            except Exception as e:
                logger.error(f"Error calculating object {ID}: {e}")
                obj = {
                    'id': ID,
                    'lon': 0.0,
                    'lat': 0.0,
                    'lonspeed': 0.0,
                    'latspeed': 0.0
                }
        
        # Add sign information
        _signInfo(obj)
        
        return obj
    except Exception as e:
        # Log the error and return a minimal valid object
        logger.error(f"Error in getObject for {ID}: {e}")
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


@ephemeris_cache()
def get_object(obj, jd, lat=None, lon=None, alt=None, mode=None):
    """
    Returns an object from the ephemeris with topocentric and sidereal options.
    
    Args:
        obj: the object ID
        jd: the julian date
        lat: the latitude in degrees
        lon: the longitude in degrees
        alt: the altitude above msl in meters
        mode: the ayanamsa
    
    Returns:
        dict: object dict
    """
    try:
        # Handle Ketu (South Node)
        if obj == const.KETU or obj == const.SOUTH_NODE:
            try:
                eph_obj = swe_object(const.RAHU, jd, lat, lon, alt, mode)
                eph_obj.update({
                    'id': obj,
                    'lon': angle.norm(eph_obj['lon'] + 180)
                })
            except Exception as e:
                logger.error(f"Error calculating {obj}: {e}")
                eph_obj = {
                    'id': obj,
                    'lon': 0.0,
                    'lat': 0.0,
                    'lonspeed': 0.0,
                    'latspeed': 0.0
                }
        # Handle shadow planets (Upagrah)
        elif obj in const.LIST_SHADOW_PLANETS and VEDIC_MODULES_AVAILABLE:
            try:
                if obj in [const.GULIKA, const.MANDI]:
                    eph_obj = upagrah.get_upagrah(obj, jd, lat, lon)
                else:
                    eph_obj = upagrah.get_upagrah(obj, jd)
            except Exception as e:
                logger.error(f"Error calculating {obj}: {e}")
                eph_obj = {
                    'id': obj,
                    'lon': 0.0,
                    'lat': 0.0,
                    'lonspeed': 0.0,
                    'latspeed': 0.0
                }
        elif obj == const.SYZYGY:
            try:
                szjd = tools.syzygyJD(jd)
                eph_obj = swe_object(const.MOON, szjd, lat, lon, alt, mode)
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
                eph_obj = swe_object(obj, jd, lat, lon, alt, mode)
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


# === Houses === #

@ephemeris_cache()
def getHouses(jd, lat, lon, hsys):
    """ Returns lists of houses and angles. """
    houses, angles = sweHouses(jd, lat, lon, hsys)
    for house in houses:
        _signInfo(house)
    for angle in angles:
        _signInfo(angle)
    return (houses, angles)


@ephemeris_cache()
def get_houses(jd, lat, lon, hsys, mode=None):
    """
    Returns lists of houses and angles with sidereal option.
    
    Args:
        jd: the julian date
        lat: the latitude in degrees
        lon: the longitude in degrees
        hsys: the house system
        mode: the ayanamsa
    
    Returns:
        tuple: (houses, angles)
    """
    cusps, angles = swe_houses(jd, lat, lon, hsys, mode)
    
    # Create house objects
    houses = []
    for i in range(12):
        house = {
            'id': 'House' + str(i + 1),
            'lon': cusps[i],
            'lat': 0.0
        }
        _signInfo(house)
        houses.append(house)
    
    # Create angle objects
    angle_objects = []
    angle_ids = [const.ASC, const.MC, const.DESC, const.IC, const.VERTEX]
    for i, angle_id in enumerate(angle_ids):
        angle_obj = {
            'id': angle_id,
            'lon': angles[i],
            'lat': 0.0
        }
        _signInfo(angle_obj)
        angle_objects.append(angle_obj)
    
    return (houses, angle_objects)


# === Fixed stars === #

@ephemeris_cache()
def getFixedStar(ID, jd):
    """ Returns a fixed star. """
    star = sweFixedStar(ID, jd)
    _signInfo(star)
    return star


# === Solar returns === #

@ephemeris_cache()
def nextSolarReturn(jd, lon):
    """ Return the JD of the next solar return. """
    return tools.solarReturnJD(jd, lon, True)


@ephemeris_cache()
def prevSolarReturn(jd, lon):
    """ Returns the JD of the previous solar return. """
    return tools.solarReturnJD(jd, lon, False)


# === Sunrise and sunsets === #

@ephemeris_cache()
def nextSunrise(jd, lat, lon):
    """ Returns the JD of the next sunrise. """
    return sweNextTransit(const.SUN, jd, lat, lon, 'RISE')


@ephemeris_cache()
def nextSunset(jd, lat, lon):
    """ Returns the JD of the next sunset. """
    return sweNextTransit(const.SUN, jd, lat, lon, 'SET')


@ephemeris_cache()
def lastSunrise(jd, lat, lon):
    """ Returns the JD of the last sunrise. """
    return nextSunrise(jd - 1.0, lat, lon)


@ephemeris_cache()
def lastSunset(jd, lat, lon):
    """ Returns the JD of the last sunset. """
    return nextSunset(jd - 1.0, lat, lon)


# === Stations === #

@ephemeris_cache()
def nextStation(ID, jd):
    """ Returns the aproximate jd of the next station. """
    return tools.nextStationJD(ID, jd)


# === Eclipses === #

@ephemeris_cache()
def solarEclipse(jd, backward):
    """ Returns the details of the previous or next solar eclipse. """
    return solarEclipseGlobal(jd, backward)
