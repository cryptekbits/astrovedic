"""
    This file is part of flatlib - (C) FlatAngle
    
    This module implements a cached version of the Swiss Ephemeris interface.
    It provides the same functionality as swe.py but with caching for improved performance.
"""

import swisseph
from flatlib import angle
from flatlib import const
from flatlib.cache import ephemeris_cache

# Import constants from swe.py
from flatlib.ephem.swe import (
    SWE_OBJECTS, SWE_HOUSESYS, SWE_AYANAMSAS,
    SEFLG_SWIEPH, SEFLG_SPEED, SEFLG_TOPOCTR, SEFLG_SIDEREAL
)


# ==== Internal functions ==== #

def setPath(path):
    """ Sets the path for the swe files. """
    swisseph.set_ephe_path(path)


# === Object functions === #

@ephemeris_cache()
def sweObject(obj, jd):
    """ Returns an object from the Ephemeris. """
    sweObj = SWE_OBJECTS[obj]
    sweList, flg = swisseph.calc_ut(jd, sweObj)
    return {
        'id': obj,
        'lon': sweList[0],
        'lat': sweList[1],
        'lonspeed': sweList[3],
        'latspeed': sweList[4]
    }


@ephemeris_cache()
def sweObjectLon(obj, jd):
    """ Returns the longitude of an object. """
    sweObj = SWE_OBJECTS[obj]
    sweList, flg = swisseph.calc_ut(jd, sweObj)
    return sweList[0]


@ephemeris_cache()
def sweNextTransit(obj, jd, lat, lon, flag):
    """ Returns the julian date of the next transit of
    an object. The flag should be 'RISE' or 'SET'.
    """
    sweObj = SWE_OBJECTS[obj]
    flag = swisseph.CALC_RISE if flag == 'RISE' else swisseph.CALC_SET
    trans = swisseph.rise_trans(jd, sweObj, lon, lat, 0, 0, 0, flag)
    return trans[1][0]


# === Houses and angles === #

@ephemeris_cache()
def sweHouses(jd, lat, lon, hsys):
    """ Returns lists with house and angle objects. """
    hsys = SWE_HOUSESYS[hsys]
    hlist, ascmc = swisseph.houses(jd, lat, lon, hsys)
    
    # Create house objects
    houses = []
    for i in range(12):
        houses.append({
            'id': 'House' + str(i + 1),
            'lon': hlist[i],
            'lat': 0.0
        })
    
    # Create angle objects
    angles = []
    angles.append({
        'id': const.ASC,
        'lon': ascmc[0],
        'lat': 0.0
    })
    angles.append({
        'id': const.MC,
        'lon': ascmc[1],
        'lat': 0.0
    })
    angles.append({
        'id': const.DESC,
        'lon': angle.norm(ascmc[0] + 180),
        'lat': 0.0
    })
    angles.append({
        'id': const.IC,
        'lon': angle.norm(ascmc[1] + 180),
        'lat': 0.0
    })
    angles.append({
        'id': const.VERTEX,
        'lon': ascmc[3],
        'lat': 0.0
    })
    
    return (houses, angles)


@ephemeris_cache()
def sweHousesLon(jd, lat, lon, hsys):
    """ Returns lists with house and angle longitudes. """
    hsys = SWE_HOUSESYS[hsys]
    hlist, ascmc = swisseph.houses(jd, lat, lon, hsys)
    angles = [
        ascmc[0],
        ascmc[1],
        angle.norm(ascmc[0] + 180),
        angle.norm(ascmc[1] + 180),
        ascmc[3]
    ]
    return (hlist, angles)


# === Fixed stars === #

@ephemeris_cache()
def sweFixedStar(star, jd):
    """ Returns a fixed star from the Ephemeris. """
    sweList, stnam, flg = swisseph.fixstar2_ut(star, jd)
    mag = swisseph.fixstar2_mag(star)
    return {
        'id': star,
        'mag': mag,
        'lon': sweList[0],
        'lat': sweList[1]
    }


# === Eclipses === #

@ephemeris_cache()
def solarEclipseGlobal(jd, backward):
    """ Returns the jd details of previous or next global solar eclipse. """
    sweList = swisseph.sol_eclipse_when_glob(jd, backward=backward)
    return {
        'maximum': sweList[1][0],
        'begin': sweList[1][2],
        'end': sweList[1][3],
        'totality_begin': sweList[1][4],
        'totality_end': sweList[1][5],
        'center_line_begin': sweList[1][6],
        'center_line_end': sweList[1][7],
    }


# === Ayanamsa === #

@ephemeris_cache()
def swe_get_ayanamsa(jd, mode):
    """ Returns the ayanamsa value for a given Julian day and mode. """
    eph_mode = SWE_AYANAMSAS[mode]
    swisseph.set_sid_mode(eph_mode, 0, 0)
    return swisseph.get_ayanamsa_ut(jd)


# === Enhanced functions === #

@ephemeris_cache()
def swe_object(obj, jd, lat=None, lon=None, alt=None, mode=None):
    """ Returns an object from the swiss ephemeris.
    - If lat/lon/alt values are set, it returns the topocentric position
    - If mode is set, returns sidereal positions for the given mode

    Args:
        obj: the object
        jd: the julian date
        lat: the latitude in degrees
        lon: the longitude in degrees
        alt: the altitude above msl in meters
        mode: the ayanamsa
    
    Returns:
        dict: swiss ephem object dict
    """
    swe_obj = SWE_OBJECTS[obj]
    flags = SEFLG_SWIEPH + SEFLG_SPEED

    # Use topocentric positions
    if lat and lon and alt:
        swisseph.set_topo(lat, lon, alt)
        flags += SEFLG_TOPOCTR

    # Use sidereal zodiac
    if mode:
        eph_mode = SWE_AYANAMSAS[mode]
        swisseph.set_sid_mode(eph_mode, 0, 0)
        flags += SEFLG_SIDEREAL

    # Compute and return positions
    swelist, flg = swisseph.calc_ut(jd, swe_obj, flags)
    return {
        'id': obj,
        'lon': swelist[0],
        'lat': swelist[1],
        'lonspeed': swelist[3],
        'latspeed': swelist[4],
    }


@ephemeris_cache()
def swe_houses(jd, lat, lon, hsys, mode=None):
    """ Returns lists with house and angle objects with sidereal option.
    
    Args:
        jd: the julian date
        lat: the latitude in degrees
        lon: the longitude in degrees
        hsys: the house system
        mode: the ayanamsa
    
    Returns:
        tuple: (houses, angles)
    """
    swe_hsys = SWE_HOUSESYS[hsys]
    flags = 0

    # Use sidereal zodiac
    if mode:
        eph_mode = SWE_AYANAMSAS[mode]
        swisseph.set_sid_mode(eph_mode, 0, 0)
        flags = SEFLG_SIDEREAL

    # Compute house cusps and angles
    cusps, ascmc = swisseph.houses_ex(jd, lat, lon, swe_hsys, flags)
    angles = [
        ascmc[0],
        ascmc[1],
        angle.norm(ascmc[0] + 180),
        angle.norm(ascmc[1] + 180),
        ascmc[3]  # Vertex
    ]

    return (cusps, angles)
