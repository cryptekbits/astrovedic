"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements cached versions of Panchang (Vedic almanac) calculations.
"""

from flatlib import const
from flatlib import angle
from flatlib.datetime import Datetime
from flatlib.ephem import swe
from flatlib.cache import calculation_cache, ephemeris_cache
from flatlib.vedic.nakshatras_cached import get_nakshatra as get_nakshatra_from_lon


@calculation_cache()
def get_tithi(jd, ayanamsa=None):
    """
    Calculate tithi (lunar day) for a given Julian day

    Args:
        jd (float): Julian day
        ayanamsa (str, optional): Ayanamsa to use for sidereal calculations

    Returns:
        dict: Dictionary with tithi information
    """
    # Calculate the phase angle between the Moon and the Sun
    phase_angle = angle.norm(swe.sweObjectLon(const.MOON, jd) - swe.sweObjectLon(const.SUN, jd))

    # Calculate tithi index (0-29)
    tithi_index = int(phase_angle / 12)

    # Calculate tithi number (1-30)
    tithi_number = tithi_index + 1

    # Determine paksha (fortnight)
    paksha = 'Shukla' if tithi_number <= 15 else 'Krishna'

    # Adjust tithi number for Krishna Paksha
    if paksha == 'Krishna':
        tithi_number = tithi_number - 15

    # Get tithi name
    tithi_names = [
        'Pratipada', 'Dwitiya', 'Tritiya', 'Chaturthi', 'Panchami',
        'Shashthi', 'Saptami', 'Ashtami', 'Navami', 'Dashami',
        'Ekadashi', 'Dwadashi', 'Trayodashi', 'Chaturdashi', 'Purnima/Amavasya'
    ]
    tithi_name = tithi_names[tithi_number - 1]

    # Adjust name for full moon and new moon
    if tithi_number == 15:
        tithi_name = 'Purnima' if paksha == 'Shukla' else 'Amavasya'

    # Calculate completion percentage
    completion = (phase_angle % 12) / 12 * 100

    return {
        'index': tithi_index,
        'number': tithi_number,
        'name': tithi_name,
        'paksha': paksha,
        'completion': completion
    }


@calculation_cache()
def get_karana(jd, ayanamsa=None):
    """
    Calculate karana (half tithi) for a given Julian day

    Args:
        jd (float): Julian day
        ayanamsa (str, optional): Ayanamsa to use for sidereal calculations

    Returns:
        dict: Dictionary with karana information
    """
    # Get tithi information
    tithi_info = get_tithi(jd, ayanamsa)

    # Calculate karana index (0-59)
    phase_angle = angle.norm(swe.sweObjectLon(const.MOON, jd) - swe.sweObjectLon(const.SUN, jd))
    karana_index = int(phase_angle / 6)

    # Get karana name
    karana_names = [
        'Bava', 'Balava', 'Kaulava', 'Taitila', 'Garija',
        'Vanija', 'Vishti', 'Bava', 'Balava', 'Kaulava',
        'Taitila', 'Garija', 'Vanija', 'Vishti', 'Bava',
        'Balava', 'Kaulava', 'Taitila', 'Garija', 'Vanija',
        'Vishti', 'Bava', 'Balava', 'Kaulava', 'Taitila',
        'Garija', 'Vanija', 'Vishti', 'Bava', 'Balava',
        'Kaulava', 'Taitila', 'Garija', 'Vanija', 'Vishti',
        'Bava', 'Balava', 'Kaulava', 'Taitila', 'Garija',
        'Vanija', 'Vishti', 'Bava', 'Balava', 'Kaulava',
        'Taitila', 'Garija', 'Vanija', 'Vishti', 'Bava',
        'Balava', 'Kaulava', 'Taitila', 'Garija', 'Vanija',
        'Vishti', 'Shakuni', 'Chatushpada', 'Naga', 'Kimstughna'
    ]
    karana_name = karana_names[karana_index]

    # Calculate completion percentage
    completion = (phase_angle % 6) / 6 * 100

    return {
        'index': karana_index,
        'name': karana_name,
        'completion': completion
    }


@calculation_cache()
def get_yoga(jd, ayanamsa=None):
    """
    Calculate yoga (lunar-solar sum) for a given Julian day

    Args:
        jd (float): Julian day
        ayanamsa (str, optional): Ayanamsa to use for sidereal calculations

    Returns:
        dict: Dictionary with yoga information
    """
    # Calculate the sum of the Moon and Sun longitudes
    sum_angle = angle.norm(swe.sweObjectLon(const.MOON, jd) + swe.sweObjectLon(const.SUN, jd))

    # Calculate yoga index (0-26)
    yoga_index = int(sum_angle / 13.333333)

    # Get yoga name
    yoga_names = [
        'Vishkambha', 'Priti', 'Ayushman', 'Saubhagya', 'Shobhana',
        'Atiganda', 'Sukarma', 'Dhriti', 'Shula', 'Ganda',
        'Vriddhi', 'Dhruva', 'Vyaghata', 'Harshana', 'Vajra',
        'Siddhi', 'Vyatipata', 'Variyana', 'Parigha', 'Shiva',
        'Siddha', 'Sadhya', 'Shubha', 'Shukla', 'Brahma',
        'Indra', 'Vaidhriti'
    ]
    yoga_name = yoga_names[yoga_index]

    # Calculate completion percentage
    completion = (sum_angle % 13.333333) / 13.333333 * 100

    return {
        'index': yoga_index,
        'name': yoga_name,
        'completion': completion
    }


@calculation_cache()
def get_vara(jd):
    """
    Calculate vara (weekday) for a given Julian day

    Args:
        jd (float): Julian day

    Returns:
        dict: Dictionary with vara information
    """
    # Calculate day of week (0 = Monday, 6 = Sunday)
    day_of_week = int(jd + 1.5) % 7

    # Adjust to match traditional order (0 = Sunday, 6 = Saturday)
    day_of_week = (day_of_week + 6) % 7

    # Get vara name
    vara_names = [
        'Ravivara', 'Somavara', 'Mangalavara', 'Budhavara',
        'Guruvara', 'Shukravara', 'Shanivara'
    ]
    vara_name = vara_names[day_of_week]

    # Get vara lord
    vara_lords = [
        const.SUN, const.MOON, const.MARS, const.MERCURY,
        const.JUPITER, const.VENUS, const.SATURN
    ]
    vara_lord = vara_lords[day_of_week]

    return {
        'index': day_of_week,
        'name': vara_name,
        'lord': vara_lord
    }


@calculation_cache()
def get_hora(jd):
    """
    Calculate hora (planetary hour) for a given Julian day

    Args:
        jd (float): Julian day

    Returns:
        dict: Dictionary with hora information
    """
    from flatlib.ephem import ephem

    # Get date from Julian day
    date = Datetime.fromJD(jd)

    # Find the previous sunrise and sunset
    prev_sunrise = ephem.lastSunrise(date, (0, 0))  # Using default location
    prev_sunset = ephem.lastSunset(date, (0, 0))    # Using default location

    # Determine if it's day or night
    is_day = prev_sunrise.jd > prev_sunset.jd

    # Get the day of week (0 = Sunday, 6 = Saturday)
    day_of_week = int(jd + 1.5) % 7

    # Calculate the hora index
    if is_day:
        # Day hora sequence starts with the lord of the day
        hora_start = day_of_week
        day_duration = ephem.nextSunset(date, (0, 0)).jd - prev_sunrise.jd
        elapsed = jd - prev_sunrise.jd
    else:
        # Night hora sequence starts with the 5th lord from the day lord
        hora_start = (day_of_week + 5) % 7
        next_sunrise = ephem.nextSunrise(date, (0, 0))
        night_duration = next_sunrise.jd - prev_sunset.jd
        elapsed = jd - prev_sunset.jd

    # Calculate which hora it is (0-11 for day, 0-11 for night)
    hora_index = int(elapsed * 12 / (day_duration if is_day else night_duration))

    # Calculate the lord of the hora
    hora_sequence = [0, 4, 1, 5, 2, 6, 3]  # Sun, Venus, Mercury, Moon, Saturn, Jupiter, Mars
    hora_lord_index = (hora_start + hora_index) % 7
    hora_lord = hora_sequence[hora_lord_index]

    # Get the lord name
    lord_names = [
        const.SUN, const.MOON, const.MARS, const.MERCURY,
        const.JUPITER, const.VENUS, const.SATURN
    ]
    hora_lord_name = lord_names[hora_lord]

    return {
        'index': hora_index,
        'is_day': is_day,
        'lord': hora_lord_name
    }


@calculation_cache()
def get_panchang(jd, lat, lon, ayanamsa=None):
    """
    Calculate complete Panchang (Vedic almanac) for a given Julian day

    Args:
        jd (float): Julian day
        lat (float): Latitude
        lon (float): Longitude
        ayanamsa (str, optional): Ayanamsa to use for sidereal calculations

    Returns:
        dict: Dictionary with complete Panchang information
    """
    # Calculate all Panchang elements
    tithi_info = get_tithi(jd, ayanamsa)
    nakshatra_info = get_nakshatra(jd, ayanamsa)
    yoga_info = get_yoga(jd, ayanamsa)
    karana_info = get_karana(jd, ayanamsa)
    vara_info = get_vara(jd)
    hora_info = get_hora(jd)

    return {
        'tithi': tithi_info,
        'nakshatra': nakshatra_info,
        'yoga': yoga_info,
        'karana': karana_info,
        'vara': vara_info,
        'hora': hora_info
    }


@ephemeris_cache()
def get_nakshatra(jd, ayanamsa=None):
    """
    Calculate nakshatra (lunar mansion) for a given Julian day

    Args:
        jd (float): Julian day
        ayanamsa (str, optional): Ayanamsa to use for sidereal calculations

    Returns:
        dict: Dictionary with nakshatra information
    """
    # Get the Moon's longitude
    moon_lon = swe.sweObjectLon(const.MOON, jd)

    # Apply ayanamsa if specified
    if ayanamsa:
        moon_lon = swe.swe_get_ayanamsa(jd, ayanamsa)

    # Get nakshatra information
    return get_nakshatra_from_lon(moon_lon)
