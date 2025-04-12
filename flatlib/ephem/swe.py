"""
    This file is part of flatlib - (C) FlatAngle
    Author: João Ventura (flatangleweb@gmail.com)


    This module implements a simple interface with the C
    Swiss Ephemeris using the pyswisseph library.

    The pyswisseph library must be already installed and
    accessible.

"""

import swisseph
from flatlib import angle
from flatlib import const

# Map objects
SWE_OBJECTS = {
    const.SUN: 0,
    const.MOON: 1,
    const.MERCURY: 2,
    const.VENUS: 3,
    const.MARS: 4,
    const.JUPITER: 5,
    const.SATURN: 6,
    const.URANUS: 7,
    const.NEPTUNE: 8,
    const.PLUTO: 9,
    const.LILITH: 12,
    const.CHIRON: 15,
    const.RAHU: 10,      # North Node
    const.KETU: 11,      # South Node (calculated as Rahu + 180°)
    const.PHOLUS: 16,
    const.CERES: 17,
    const.PALLAS: 18,
    const.JUNO: 19,
    const.VESTA: 20,
    # Shadow planets and Vedic bodies are calculated separately
    # in flatlib/vedic/upagrah.py and flatlib/vedic/bodies.py
}

# Map house systems
SWE_HOUSESYS = {
    const.HOUSES_PLACIDUS: b'P',
    const.HOUSES_KOCH: b'K',
    const.HOUSES_PORPHYRIUS: b'O',
    const.HOUSES_REGIOMONTANUS: b'R',
    const.HOUSES_CAMPANUS: b'C',
    const.HOUSES_EQUAL: b'A',
    const.HOUSES_EQUAL_2: b'E',
    const.HOUSES_VEHLOW_EQUAL: b'V',
    const.HOUSES_WHOLE_SIGN: b'W',
    const.HOUSES_MERIDIAN: b'X',
    const.HOUSES_AZIMUTHAL: b'H',
    const.HOUSES_POLICH_PAGE: b'T',
    const.HOUSES_ALCABITUS: b'B',
    const.HOUSES_MORINUS: b'M'
}

# Map ayanamsas
SWE_AYANAMSAS = {
    const.AY_FAGAN_BRADLEY: 0,
    const.AY_LAHIRI: 1,
    const.AY_DELUCE: 2,
    const.AY_RAMAN: 3,
    const.AY_KRISHNAMURTI: 5,
    const.AY_SASSANIAN: 16,
    const.AY_ALDEBARAN_15TAU: 14,
    const.AY_GALCENTER_5SAG: 17,
    # Additional Vedic Ayanamsas
    const.AY_YUKTESHWAR: 7,
    const.AY_JN_BHASIN: 8,
    const.AY_SURYASIDDHANTA: 21,
    const.AY_SURYASIDDHANTA_MSUN: 22,
    const.AY_ARYABHATA: 23,
    const.AY_ARYABHATA_MSUN: 24,
    const.AY_SS_REVATI: 25,
    const.AY_SS_CITRA: 26,
    const.AY_TRUE_CITRA: 27,
    const.AY_TRUE_REVATI: 28,
    const.AY_TRUE_PUSHYA: 29,
    const.AY_TRUE_MULA: 30,
    const.AY_ARYABHATA_522: 34,
    const.AY_TRUE_SHEORAN: 39,
}

# SWE flags for computations
SEFLG_SWIEPH = 2
SEFLG_SPEED = 256
SEFLG_TOPOCTR = 32 * 1024
SEFLG_SIDEREAL = 64 * 1024


# ==== Internal functions ==== #

def setPath(path):
    """ Sets the path for the swe files. """
    swisseph.set_ephe_path(path)


# === Object functions === #

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


def sweObjectLon(obj, jd):
    """ Returns the longitude of an object. """
    sweObj = SWE_OBJECTS[obj]
    sweList, flg = swisseph.calc_ut(jd, sweObj)
    return sweList[0]


def sweNextTransit(obj, jd, lat, lon, flag):
    """ Returns the julian date of the next transit of
    an object. The flag should be 'RISE' or 'SET'.

    """
    sweObj = SWE_OBJECTS[obj]
    flag = swisseph.CALC_RISE if flag == 'RISE' else swisseph.CALC_SET
    ephe_flag = swisseph.FLG_SWIEPH  # Use standard Swiss Ephemeris flag
    altitude = 0 # Use integer altitude
    geopos_tuple = (lon, lat, altitude)
    # Signature from pyswisseph test suite:
    # (tjdut, pl, rsmi, geopos, atpress, attemp, flags)
    trans = swisseph.rise_trans(jd, sweObj, flag, geopos_tuple, 0, 0, ephe_flag)
    return trans[1][0]


# === Houses and angles === #

def sweHouses(jd, lat, lon, hsys):
    """ Returns lists of houses and angles. """
    hsys = SWE_HOUSESYS[hsys]
    hlist, ascmc = swisseph.houses(jd, lat, lon, hsys)
    # Add first house to the end of 'hlist' so that we
    # can compute house sizes with an iterator
    hlist += (hlist[0],)
    houses = [
        {
            'id': const.LIST_HOUSES[i],
            'lon': hlist[i],
            'lat': 0.0,  # Add lat attribute to avoid warnings
            'size': angle.distance(hlist[i], hlist[i + 1])
        } for i in range(12)
    ]
    angles = [
        {'id': const.ASC, 'lon': ascmc[0], 'lat': 0.0},
        {'id': const.MC, 'lon': ascmc[1], 'lat': 0.0},
        {'id': const.DESC, 'lon': angle.norm(ascmc[0] + 180), 'lat': 0.0},
        {'id': const.IC, 'lon': angle.norm(ascmc[1] + 180), 'lat': 0.0},
        {'id': const.VERTEX, 'lon': ascmc[3], 'lat': 0.0}
    ]
    return (houses, angles)


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

# Beware: the swisseph.fixstar_mag function is really
# slow because it parses the fixstars.cat file every
# time..

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


def lunarEclipseGlobal(jd, backward):
    """ Returns the jd details of previous or next global lunar eclipse. """

    sweList = swisseph.lun_eclipse_when(jd, backward=backward)
    return {
        'maximum': sweList[1][0],
        'partial_begin': sweList[1][2],
        'partial_end': sweList[1][3],
        'totality_begin': sweList[1][4],
        'totality_end': sweList[1][5],
        'penumbral_begin': sweList[1][6],
        'penumbral_end': sweList[1][7],
    }


# === Sidereal zodiac === #

def get_ayanamsa(jd, mode):
    """ Returns the distance of the tropical vernal point
    from the sidereal zero point of the zodiac.
    """
    eph_mode = SWE_AYANAMSAS[mode]
    swisseph.set_sid_mode(eph_mode, 0, 0)
    return swisseph.get_ayanamsa_ut(jd)


# === Sidereal and topocentric functions == #

def swe_object(obj, jd, lat=None, lon=None, alt=None, mode=None):
    """ Returns an object from the swiss ephemeris.
    - If lat/lon/alt values are set, it returns the topocentric position
    - If mode is set, returns sidereal positions for the given mode

    :param obj: the object
    :param jd: the julian date
    :param lat: the latitude in degrees
    :param lon: the longitude in degrees
    :param alt: the altitude above msl in meters
    :param mode: the ayanamsa
    :return: swiss ephem object dict
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


def swe_houses_lon(jd, lat, lon, hsys, mode=None):
    """ Returns the longitudes of houses and angles cusps.
    - If mode is set, returns sidereal positions for the given mode

    :param jd: the julian date
    :param lat: the latitude in degrees
    :param lon: the longitude in degrees
    :param hsys: the house system
    :param mode: the ayanamsa
    :return: list of houses and angles longitudes
    """
    swe_hsys = SWE_HOUSESYS[hsys]
    flags = SEFLG_SWIEPH + SEFLG_SPEED

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


def swe_houses(jd, lat, lon, hsys, mode=None):
    """ Returns the houses and angles.
    - If mode is set, returns sidereal positions for the given mode

    :param jd: the julian date
    :param lat: the latitude in degrees
    :param lon: the longitude in degrees
    :param hsys: the house system
    :param mode: the ayanamsa
    :return: list of houses and angles
    """
    # Compute house cusps and angles
    cusps, ascmc = swe_houses_lon(jd, lat, lon, hsys, mode)

    # Compute house sizes
    cusps += (cusps[0],)
    houses = [
        {
            'id': const.LIST_HOUSES[i],
            'lon': cusps[i],
            'lat': 0.0,  # Add lat attribute to avoid warnings
            'size': angle.distance(cusps[i], cusps[i + 1]),
        } for i in range(12)
    ]

    # Create angles
    angles = [
        {'id': const.ASC, 'lon': ascmc[0], 'lat': 0.0},
        {'id': const.MC, 'lon': ascmc[1], 'lat': 0.0},
        {'id': const.DESC, 'lon': angle.norm(ascmc[0] + 180), 'lat': 0.0},
        {'id': const.IC, 'lon': angle.norm(ascmc[1] + 180), 'lat': 0.0},
        {'id': const.VERTEX, 'lon': ascmc[4], 'lat': 0.0}
    ]

    return (houses, angles)
