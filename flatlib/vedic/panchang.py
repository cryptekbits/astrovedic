"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Panchang (Vedic almanac) calculations.
    It includes tithi, nakshatra, yoga, karana, and other
    Vedic time elements.
"""

import math
from flatlib import const
from flatlib import angle
from flatlib.datetime import Datetime
from flatlib.ephem import swe

# Tithi (lunar day) names
TITHI_NAMES = [
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima",
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Amavasya"
]

# Paksha (lunar fortnight) names
SHUKLA_PAKSHA = "Shukla Paksha"  # Bright half (waxing moon)
KRISHNA_PAKSHA = "Krishna Paksha"  # Dark half (waning moon)

# Karana (half tithi) names
KARANA_NAMES = [
    "Bava", "Balava", "Kaulava", "Taitila", "Garija",
    "Vanija", "Vishti", "Bava", "Balava", "Kaulava",
    "Taitila", "Garija", "Vanija", "Vishti", "Bava",
    "Balava", "Kaulava", "Taitila", "Garija", "Vanija",
    "Vishti", "Bava", "Balava", "Kaulava", "Taitila",
    "Garija", "Vanija", "Vishti", "Bava", "Balava",
    "Kaulava", "Taitila", "Garija", "Vanija", "Vishti",
    "Bava", "Balava", "Kaulava", "Taitila", "Garija",
    "Vanija", "Vishti", "Bava", "Balava", "Kaulava",
    "Taitila", "Garija", "Vanija", "Vishti", "Bava",
    "Balava", "Kaulava", "Taitila", "Garija", "Vanija",
    "Vishti", "Shakuni", "Chatushpada", "Naga", "Kimstughna"
]

# Yoga (lunar-solar combination) names
YOGA_NAMES = [
    "Vishkumbha", "Preeti", "Ayushman", "Saubhagya", "Shobhana",
    "Atiganda", "Sukarma", "Dhriti", "Shoola", "Ganda",
    "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra",
    "Siddhi", "Vyatipata", "Variyana", "Parigha", "Shiva",
    "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma",
    "Indra", "Vaidhriti"
]

# Vara (weekday) names
VARA_NAMES = [
    "Ravivara",    # Sunday
    "Somavara",    # Monday
    "Mangalavara", # Tuesday
    "Budhavara",   # Wednesday
    "Guruvara",    # Thursday
    "Shukravara",  # Friday
    "Shanivara"    # Saturday
]

# Hora (planetary hour) rulers
HORA_RULERS = [
    const.SUN, const.VENUS, const.MERCURY, const.MOON, const.SATURN,
    const.JUPITER, const.MARS
]


def get_tithi(jd, ayanamsa=None):
    """
    Calculate tithi (lunar day) for a given Julian day
    
    Args:
        jd (float): Julian day
        ayanamsa (str, optional): Ayanamsa to use for sidereal calculations
    
    Returns:
        dict: Dictionary with tithi information
    """
    # Get Sun and Moon longitudes
    sun_lon = swe.sweObjectLon(const.SUN, jd)
    moon_lon = swe.sweObjectLon(const.MOON, jd)
    
    # If ayanamsa is provided, convert to sidereal
    if ayanamsa:
        ayanamsa_val = swe.get_ayanamsa(jd, ayanamsa)
        sun_lon = angle.norm(sun_lon - ayanamsa_val)
        moon_lon = angle.norm(moon_lon - ayanamsa_val)
    
    # Calculate lunar phase angle
    phase_angle = angle.norm(moon_lon - sun_lon)
    
    # Calculate tithi (0-29)
    tithi_index = int(phase_angle / 12)
    
    # Get tithi name
    tithi_name = TITHI_NAMES[tithi_index]
    
    # Determine paksha (lunar fortnight)
    paksha = SHUKLA_PAKSHA if tithi_index < 15 else KRISHNA_PAKSHA
    
    # Calculate completion percentage
    completion = (phase_angle % 12) / 12 * 100
    
    return {
        'index': tithi_index,
        'name': tithi_name,
        'paksha': paksha,
        'completion': completion
    }


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
    karana_name = KARANA_NAMES[karana_index]
    
    # Calculate completion percentage
    completion = (phase_angle % 6) / 6 * 100
    
    return {
        'index': karana_index,
        'name': karana_name,
        'completion': completion
    }


def get_yoga(jd, ayanamsa=None):
    """
    Calculate yoga for a given Julian day
    
    Yoga is the sum of the longitudes of the Sun and Moon
    divided into 27 parts.
    
    Args:
        jd (float): Julian day
        ayanamsa (str, optional): Ayanamsa to use for sidereal calculations
    
    Returns:
        dict: Dictionary with yoga information
    """
    # Get Sun and Moon longitudes
    sun_lon = swe.sweObjectLon(const.SUN, jd)
    moon_lon = swe.sweObjectLon(const.MOON, jd)
    
    # If ayanamsa is provided, convert to sidereal
    if ayanamsa:
        ayanamsa_val = swe.get_ayanamsa(jd, ayanamsa)
        sun_lon = angle.norm(sun_lon - ayanamsa_val)
        moon_lon = angle.norm(moon_lon - ayanamsa_val)
    
    # Calculate yoga angle (sum of Sun and Moon longitudes)
    yoga_angle = angle.norm(sun_lon + moon_lon)
    
    # Calculate yoga index (0-26)
    yoga_index = int(yoga_angle / (360 / 27))
    
    # Get yoga name
    yoga_name = YOGA_NAMES[yoga_index]
    
    # Calculate completion percentage
    completion = (yoga_angle % (360 / 27)) / (360 / 27) * 100
    
    return {
        'index': yoga_index,
        'name': yoga_name,
        'completion': completion
    }


def get_vara(jd):
    """
    Calculate vara (weekday) for a given Julian day
    
    Args:
        jd (float): Julian day
    
    Returns:
        dict: Dictionary with vara information
    """
    # Calculate day of week (0 = Sunday, 1 = Monday, etc.)
    day_of_week = int((jd + 1.5) % 7)
    
    # Get vara name
    vara_name = VARA_NAMES[day_of_week]
    
    return {
        'index': day_of_week,
        'name': vara_name
    }


def get_hora(jd, lat, lon):
    """
    Calculate hora (planetary hour) for a given Julian day
    
    Args:
        jd (float): Julian day
        lat (float): Latitude in degrees
        lon (float): Longitude in degrees
    
    Returns:
        dict: Dictionary with hora information
    """
    from flatlib.ephem import ephem
    
    # Get date from Julian day
    date = Datetime.fromJD(jd)
    
    # Find the previous sunrise
    prev_sunrise = ephem.lastSunrise(date, (lat, lon))
    
    # Find the next sunset
    next_sunset = ephem.nextSunset(date, (lat, lon))
    
    # Find the next sunrise
    next_sunrise = ephem.nextSunrise(date, (lat, lon))
    
    # Determine if it's day or night
    is_day = prev_sunrise.jd <= jd < next_sunset.jd
    
    # Get day of week (0 = Sunday, 1 = Monday, etc.)
    day_of_week = date.date.weekday()
    
    if is_day:
        # Day time calculation
        day_duration = next_sunset.jd - prev_sunrise.jd
        hora_duration = day_duration / 12
        hora_index = int((jd - prev_sunrise.jd) / hora_duration)
    else:
        # Night time calculation
        night_duration = next_sunrise.jd - next_sunset.jd
        hora_duration = night_duration / 12
        hora_index = int((jd - next_sunset.jd) / hora_duration)
    
    # The first hora of the day is ruled by the planet of the day
    # The sequence follows: Sun, Venus, Mercury, Moon, Saturn, Jupiter, Mars
    hora_ruler_index = (day_of_week + hora_index) % 7
    hora_ruler = HORA_RULERS[hora_ruler_index]
    
    return {
        'index': hora_index,
        'ruler': hora_ruler,
        'is_day': is_day
    }


def get_rahukala(jd, lat, lon):
    """
    Calculate Rahukala (inauspicious period) for a given Julian day
    
    Args:
        jd (float): Julian day
        lat (float): Latitude in degrees
        lon (float): Longitude in degrees
    
    Returns:
        dict: Dictionary with Rahukala information
    """
    from flatlib.ephem import ephem
    
    # Get date from Julian day
    date = Datetime.fromJD(jd)
    
    # Find the previous sunrise
    prev_sunrise = ephem.lastSunrise(date, (lat, lon))
    
    # Find the next sunset
    next_sunset = ephem.nextSunset(date, (lat, lon))
    
    # Get day of week (0 = Sunday, 1 = Monday, etc.)
    day_of_week = date.date.weekday()
    
    # Rahukala occurs at different times on different days
    # The sequence is: 8, 2, 7, 5, 6, 4, 3 (in terms of 1/8th parts of the day)
    rahukala_sequence = [7, 1, 6, 4, 5, 3, 2]  # 0-based index
    rahukala_part = rahukala_sequence[day_of_week]
    
    # Calculate day duration
    day_duration = next_sunset.jd - prev_sunrise.jd
    
    # Calculate Rahukala start and end times
    rahukala_start = prev_sunrise.jd + (rahukala_part * day_duration / 8)
    rahukala_end = prev_sunrise.jd + ((rahukala_part + 1) * day_duration / 8)
    
    # Convert to Datetime objects
    rahukala_start_dt = Datetime.fromJD(rahukala_start, date.utcoffset)
    rahukala_end_dt = Datetime.fromJD(rahukala_end, date.utcoffset)
    
    return {
        'start': rahukala_start_dt,
        'end': rahukala_end_dt,
        'duration': rahukala_end - rahukala_start
    }


def get_yamaganda(jd, lat, lon):
    """
    Calculate Yamaganda (inauspicious period) for a given Julian day
    
    Args:
        jd (float): Julian day
        lat (float): Latitude in degrees
        lon (float): Longitude in degrees
    
    Returns:
        dict: Dictionary with Yamaganda information
    """
    from flatlib.ephem import ephem
    
    # Get date from Julian day
    date = Datetime.fromJD(jd)
    
    # Find the previous sunrise
    prev_sunrise = ephem.lastSunrise(date, (lat, lon))
    
    # Find the next sunset
    next_sunset = ephem.nextSunset(date, (lat, lon))
    
    # Get day of week (0 = Sunday, 1 = Monday, etc.)
    day_of_week = date.date.weekday()
    
    # Yamaganda occurs at different times on different days
    # The sequence is: 2, 6, 4, 5, 3, 7, 8 (in terms of 1/8th parts of the day)
    yamaganda_sequence = [1, 5, 3, 4, 2, 6, 7]  # 0-based index
    yamaganda_part = yamaganda_sequence[day_of_week]
    
    # Calculate day duration
    day_duration = next_sunset.jd - prev_sunrise.jd
    
    # Calculate Yamaganda start and end times
    yamaganda_start = prev_sunrise.jd + (yamaganda_part * day_duration / 8)
    yamaganda_end = prev_sunrise.jd + ((yamaganda_part + 1) * day_duration / 8)
    
    # Convert to Datetime objects
    yamaganda_start_dt = Datetime.fromJD(yamaganda_start, date.utcoffset)
    yamaganda_end_dt = Datetime.fromJD(yamaganda_end, date.utcoffset)
    
    return {
        'start': yamaganda_start_dt,
        'end': yamaganda_end_dt,
        'duration': yamaganda_end - yamaganda_start
    }


def get_gulika_kala(jd, lat, lon):
    """
    Calculate Gulika Kala (inauspicious period) for a given Julian day
    
    Args:
        jd (float): Julian day
        lat (float): Latitude in degrees
        lon (float): Longitude in degrees
    
    Returns:
        dict: Dictionary with Gulika Kala information
    """
    from flatlib.ephem import ephem
    
    # Get date from Julian day
    date = Datetime.fromJD(jd)
    
    # Find the previous sunrise
    prev_sunrise = ephem.lastSunrise(date, (lat, lon))
    
    # Find the next sunset
    next_sunset = ephem.nextSunset(date, (lat, lon))
    
    # Get day of week (0 = Sunday, 1 = Monday, etc.)
    day_of_week = date.date.weekday()
    
    # Gulika Kala occurs at different times on different days
    # The sequence is: 7, 6, 5, 4, 3, 2, 1 (in terms of 1/8th parts of the day)
    gulika_sequence = [6, 5, 4, 3, 2, 1, 0]  # 0-based index
    gulika_part = gulika_sequence[day_of_week]
    
    # Calculate day duration
    day_duration = next_sunset.jd - prev_sunrise.jd
    
    # Calculate Gulika Kala start and end times
    gulika_start = prev_sunrise.jd + (gulika_part * day_duration / 8)
    gulika_end = prev_sunrise.jd + ((gulika_part + 1) * day_duration / 8)
    
    # Convert to Datetime objects
    gulika_start_dt = Datetime.fromJD(gulika_start, date.utcoffset)
    gulika_end_dt = Datetime.fromJD(gulika_end, date.utcoffset)
    
    return {
        'start': gulika_start_dt,
        'end': gulika_end_dt,
        'duration': gulika_end - gulika_start
    }


def get_abhijit_muhurta(jd, lat, lon):
    """
    Calculate Abhijit Muhurta (auspicious period) for a given Julian day
    
    Abhijit Muhurta is the 8th muhurta of the day, occurring around midday.
    
    Args:
        jd (float): Julian day
        lat (float): Latitude in degrees
        lon (float): Longitude in degrees
    
    Returns:
        dict: Dictionary with Abhijit Muhurta information
    """
    from flatlib.ephem import ephem
    
    # Get date from Julian day
    date = Datetime.fromJD(jd)
    
    # Find the previous sunrise
    prev_sunrise = ephem.lastSunrise(date, (lat, lon))
    
    # Find the next sunset
    next_sunset = ephem.nextSunset(date, (lat, lon))
    
    # Calculate day duration
    day_duration = next_sunset.jd - prev_sunrise.jd
    
    # Calculate Abhijit Muhurta (8th muhurta of the day)
    # There are 15 muhurtas in a day
    abhijit_start = prev_sunrise.jd + (7 * day_duration / 15)
    abhijit_end = prev_sunrise.jd + (8 * day_duration / 15)
    
    # Convert to Datetime objects
    abhijit_start_dt = Datetime.fromJD(abhijit_start, date.utcoffset)
    abhijit_end_dt = Datetime.fromJD(abhijit_end, date.utcoffset)
    
    return {
        'start': abhijit_start_dt,
        'end': abhijit_end_dt,
        'duration': abhijit_end - abhijit_start
    }


def get_panchang(jd, lat, lon, ayanamsa=None):
    """
    Calculate complete Panchang for a given Julian day
    
    Args:
        jd (float): Julian day
        lat (float): Latitude in degrees
        lon (float): Longitude in degrees
        ayanamsa (str, optional): Ayanamsa to use for sidereal calculations
    
    Returns:
        dict: Dictionary with complete Panchang information
    """
    # Get date from Julian day
    date = Datetime.fromJD(jd)
    
    # Calculate all Panchang elements
    tithi_info = get_tithi(jd, ayanamsa)
    nakshatra_info = get_nakshatra(jd, ayanamsa)
    yoga_info = get_yoga(jd, ayanamsa)
    karana_info = get_karana(jd, ayanamsa)
    vara_info = get_vara(jd)
    
    # Calculate inauspicious periods
    rahukala_info = get_rahukala(jd, lat, lon)
    yamaganda_info = get_yamaganda(jd, lat, lon)
    gulika_kala_info = get_gulika_kala(jd, lat, lon)
    
    # Calculate auspicious periods
    abhijit_muhurta_info = get_abhijit_muhurta(jd, lat, lon)
    
    return {
        'date': date,
        'tithi': tithi_info,
        'nakshatra': nakshatra_info,
        'yoga': yoga_info,
        'karana': karana_info,
        'vara': vara_info,
        'rahukala': rahukala_info,
        'yamaganda': yamaganda_info,
        'gulika_kala': gulika_kala_info,
        'abhijit_muhurta': abhijit_muhurta_info
    }


def get_nakshatra(jd, ayanamsa=None):
    """
    Calculate nakshatra for a given Julian day
    
    Args:
        jd (float): Julian day
        ayanamsa (str, optional): Ayanamsa to use for sidereal calculations
    
    Returns:
        dict: Dictionary with nakshatra information
    """
    from flatlib.vedic.nakshatras import get_nakshatra as get_nak
    
    # Get Moon longitude
    moon_lon = swe.sweObjectLon(const.MOON, jd)
    
    # If ayanamsa is provided, convert to sidereal
    if ayanamsa:
        ayanamsa_val = swe.get_ayanamsa(jd, ayanamsa)
        moon_lon = angle.norm(moon_lon - ayanamsa_val)
    
    # Get nakshatra information
    nakshatra_info = get_nak(moon_lon)
    
    return nakshatra_info
