"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Panchang (Vedic almanac) calculations.
    It includes tithi, nakshatra, yoga, karana, and other
    Vedic time elements.
"""

import math
from astrovedic import const
from astrovedic import angle
from astrovedic.datetime import Datetime
from astrovedic.ephem import swe, ephem
from astrovedic.geopos import GeoPos

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
    from astrovedic.ephem import ephem
    
    # Get date from Julian day
    date = Datetime.fromJD(jd)
    
    # Find the previous sunrise
    prev_sunrise = ephem.lastSunrise(date, GeoPos(lat, lon))
    
    # Find the next sunset
    next_sunset = ephem.nextSunset(date, GeoPos(lat, lon))
    
    # Find the next sunrise
    next_sunrise = ephem.nextSunrise(date, GeoPos(lat, lon))
    
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


def get_rahukala(jd, lat, lon, utcoffset):
    """
    Calculate Rahu Kala for a given Julian day and location
    
    Args:
        jd (float): Julian day
        lat (float): Latitude in degrees
        lon (float): Longitude in degrees
        utcoffset (Time): UTC offset
    
    Returns:
        dict: Dictionary with Rahu Kala start and end times
    """
    # Get date and weekday
    date = Datetime.fromJD(jd, utcoffset)
    # Convert flatlib dayofweek (Sun=0) to Python weekday (Mon=0)
    weekday = (date.date.dayofweek() - 1 + 7) % 7
    
    # Find the previous sunrise and next sunset using ephem
    prev_sunrise = ephem.lastSunrise(date, GeoPos(lat, lon))
    next_sunset = ephem.nextSunset(date, GeoPos(lat, lon))
    
    # Calculate day duration in JD
    day_duration = next_sunset.jd - prev_sunrise.jd
    
    # Rahu Kala sequence (Mon=0 to Sun=6)
    # Original flatlib sequence: [7, 1, 6, 4, 5, 3, 2] for Sun=0 index
    # Adjusted for Mon=0 index: [1, 6, 4, 5, 3, 2, 7]
    rahukala_sequence = [1, 6, 4, 5, 3, 2, 7] 
    rahukala_part = rahukala_sequence[weekday]
    
    # Calculate Rahu Kala start and end Julian Days
    # Note: Sequence parts are 1-based for calculation (1st part to 8th part)
    rahukala_start_jd = prev_sunrise.jd + ((rahukala_part - 1) * day_duration / 8)
    rahukala_end_jd = prev_sunrise.jd + (rahukala_part * day_duration / 8)
    
    # Convert back to Datetime objects with the correct utcoffset
    rahukala_start = Datetime.fromJD(rahukala_start_jd, utcoffset)
    rahukala_end = Datetime.fromJD(rahukala_end_jd, utcoffset)
    
    return {
        'start': rahukala_start,
        'end': rahukala_end
    }


def get_yamaganda(jd, lat, lon, utcoffset):
    """
    Calculate Yamaganda Kalam for a given Julian day and location
    
    Args:
        jd (float): Julian day
        lat (float): Latitude in degrees
        lon (float): Longitude in degrees
        utcoffset (Time): UTC offset
    
    Returns:
        dict: Dictionary with Yamaganda Kalam start and end times
    """
    # Get date and weekday
    date = Datetime.fromJD(jd, utcoffset)
    # Convert flatlib dayofweek (Sun=0) to Python weekday (Mon=0)
    weekday = (date.date.dayofweek() - 1 + 7) % 7
    
    # Find the previous sunrise and next sunset using ephem
    prev_sunrise = ephem.lastSunrise(date, GeoPos(lat, lon))
    next_sunset = ephem.nextSunset(date, GeoPos(lat, lon))
    
    # Calculate day duration in JD
    day_duration = next_sunset.jd - prev_sunrise.jd
    
    # Yamaganda sequence (Mon=0 to Sun=6)
    # Original flatlib sequence: [1, 5, 3, 4, 2, 6, 7] for Sun=0 index
    # Adjusted for Mon=0 index: [5, 3, 4, 2, 6, 7, 1]
    yamaganda_sequence = [5, 3, 4, 2, 6, 7, 1]
    yamaganda_part = yamaganda_sequence[weekday]
    
    # Calculate Yamaganda start and end Julian Days
    yamaganda_start_jd = prev_sunrise.jd + ((yamaganda_part - 1) * day_duration / 8)
    yamaganda_end_jd = prev_sunrise.jd + (yamaganda_part * day_duration / 8)
    
    # Convert back to Datetime objects with the correct utcoffset
    yamaganda_start = Datetime.fromJD(yamaganda_start_jd, utcoffset)
    yamaganda_end = Datetime.fromJD(yamaganda_end_jd, utcoffset)
    
    return {
        'start': yamaganda_start,
        'end': yamaganda_end
    }


def get_gulika_kala(jd, lat, lon, utcoffset):
    """
    Calculate Gulika Kalam for a given Julian day and location
    
    Args:
        jd (float): Julian day
        lat (float): Latitude in degrees
        lon (float): Longitude in degrees
        utcoffset (Time): UTC offset
    
    Returns:
        dict: Dictionary with Gulika Kalam start and end times
    """
    # Get date and weekday
    date = Datetime.fromJD(jd, utcoffset)
    # Convert flatlib dayofweek (Sun=0) to Python weekday (Mon=0)
    weekday = (date.date.dayofweek() - 1 + 7) % 7
    
    # Find the previous sunrise and next sunset using ephem
    prev_sunrise = ephem.lastSunrise(date, GeoPos(lat, lon))
    next_sunset = ephem.nextSunset(date, GeoPos(lat, lon))
    
    # Calculate day duration in JD
    day_duration = next_sunset.jd - prev_sunrise.jd
    
    # Gulika sequence (Mon=0 to Sun=6)
    # Original flatlib sequence: [6, 5, 4, 3, 2, 1, 0] for Sun=0 index --> [6, 5, 4, 3, 2, 1, 7] 1-based
    # Adjusted for Mon=0 index: [5, 4, 3, 2, 1, 7, 6]
    gulika_sequence = [5, 4, 3, 2, 1, 7, 6] 
    gulika_part = gulika_sequence[weekday]
    
    # Calculate Gulika start and end Julian Days
    gulika_start_jd = prev_sunrise.jd + ((gulika_part - 1) * day_duration / 8)
    gulika_end_jd = prev_sunrise.jd + (gulika_part * day_duration / 8)
    
    # Convert back to Datetime objects with the correct utcoffset
    gulika_start = Datetime.fromJD(gulika_start_jd, utcoffset)
    gulika_end = Datetime.fromJD(gulika_end_jd, utcoffset)
    
    return {
        'start': gulika_start,
        'end': gulika_end
    }


def get_abhijit_muhurta(jd, lat, lon, utcoffset):
    """
    Calculate Abhijit Muhurta for a given Julian day and location
    
    Args:
        jd (float): Julian day
        lat (float): Latitude in degrees
        lon (float): Longitude in degrees
        utcoffset (Time): UTC offset

    Returns:
        dict: Dictionary with Abhijit Muhurta start and end times
    """
    # Get date object
    date = Datetime.fromJD(jd, utcoffset)

    # Find the previous sunrise and next sunset using ephem
    prev_sunrise = ephem.lastSunrise(date, GeoPos(lat, lon))
    next_sunset = ephem.nextSunset(date, GeoPos(lat, lon))
    
    # Calculate day duration in JD
    day_duration = next_sunset.jd - prev_sunrise.jd
    
    # Calculate Abhijit Muhurta (8th muhurta of the day)
    # There are 15 muhurtas in a day, so the 8th starts after 7/15 and ends after 8/15
    abhijit_start_jd = prev_sunrise.jd + (7 * day_duration / 15)
    abhijit_end_jd = prev_sunrise.jd + (8 * day_duration / 15)
    
    # Convert back to Datetime objects with the correct utcoffset
    abhijit_start = Datetime.fromJD(abhijit_start_jd, utcoffset)
    abhijit_end = Datetime.fromJD(abhijit_end_jd, utcoffset)

    return {
        'start': abhijit_start,
        'end': abhijit_end
    }


def get_panchang(jd, lat, lon, utcoffset, ayanamsa=None):
    """
    Calculate complete Panchang for a given Julian day
    
    Args:
        jd (float): Julian day
        lat (float): Latitude in degrees
        lon (float): Longitude in degrees
        utcoffset (Time): UTC offset
        ayanamsa (str, optional): Ayanamsa to use for sidereal calculations
    
    Returns:
        dict: Dictionary with complete Panchang information
    """
    # Get date from Julian day
    date = Datetime.fromJD(jd, utcoffset)
    
    # Calculate all Panchang elements
    tithi_info = get_tithi(jd, ayanamsa)
    nakshatra_info = get_nakshatra(jd, ayanamsa)
    yoga_info = get_yoga(jd, ayanamsa)
    karana_info = get_karana(jd, ayanamsa)
    vara_info = get_vara(jd)
    
    # Calculate inauspicious periods
    rahukala_info = get_rahukala(jd, lat, lon, utcoffset)
    yamaganda_info = get_yamaganda(jd, lat, lon, utcoffset)
    gulika_kala_info = get_gulika_kala(jd, lat, lon, utcoffset)
    
    # Calculate auspicious periods
    abhijit_muhurta_info = get_abhijit_muhurta(jd, lat, lon, utcoffset)
    
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
    from astrovedic.vedic.nakshatras import get_nakshatra as get_nak
    
    # Get Moon longitude
    moon_lon = swe.sweObjectLon(const.MOON, jd)
    
    # If ayanamsa is provided, convert to sidereal
    if ayanamsa:
        ayanamsa_val = swe.get_ayanamsa(jd, ayanamsa)
        moon_lon = angle.norm(moon_lon - ayanamsa_val)
    
    # Get nakshatra information
    nakshatra_info = get_nak(moon_lon)
    
    return nakshatra_info
