"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology

    This module provides cached functions for nakshatra calculations.
    These functions are optimized versions of the functions in nakshatras.py with caching.
"""

from flatlib import const
from flatlib.cache import reference_cache, calculation_cache

# List of 27 nakshatras
LIST_NAKSHATRAS = [
    'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
    'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
    'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
    'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
    'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
]

# Nakshatra lords (for Vimshottari Dasha)
NAKSHATRA_LORDS = {
    'Ashwini': const.KETU,
    'Bharani': const.VENUS,
    'Krittika': const.SUN,
    'Rohini': const.MOON,
    'Mrigashira': const.MARS,
    'Ardra': const.RAHU,
    'Punarvasu': const.JUPITER,
    'Pushya': const.SATURN,
    'Ashlesha': const.MERCURY,
    'Magha': const.KETU,
    'Purva Phalguni': const.VENUS,
    'Uttara Phalguni': const.SUN,
    'Hasta': const.MOON,
    'Chitra': const.MARS,
    'Swati': const.RAHU,
    'Vishakha': const.JUPITER,
    'Anuradha': const.SATURN,
    'Jyeshtha': const.MERCURY,
    'Mula': const.KETU,
    'Purva Ashadha': const.VENUS,
    'Uttara Ashadha': const.SUN,
    'Shravana': const.MOON,
    'Dhanishta': const.MARS,
    'Shatabhisha': const.RAHU,
    'Purva Bhadrapada': const.JUPITER,
    'Uttara Bhadrapada': const.SATURN,
    'Revati': const.MERCURY
}

# Nakshatra elements
NAKSHATRA_ELEMENTS = {
    'Ashwini': 'Fire',
    'Bharani': 'Earth',
    'Krittika': 'Fire',
    'Rohini': 'Earth',
    'Mrigashira': 'Air',
    'Ardra': 'Water',
    'Punarvasu': 'Air',
    'Pushya': 'Water',
    'Ashlesha': 'Water',
    'Magha': 'Fire',
    'Purva Phalguni': 'Fire',
    'Uttara Phalguni': 'Fire',
    'Hasta': 'Air',
    'Chitra': 'Air',
    'Swati': 'Air',
    'Vishakha': 'Fire',
    'Anuradha': 'Earth',
    'Jyeshtha': 'Earth',
    'Mula': 'Water',
    'Purva Ashadha': 'Water',
    'Uttara Ashadha': 'Earth',
    'Shravana': 'Earth',
    'Dhanishta': 'Fire',
    'Shatabhisha': 'Air',
    'Purva Bhadrapada': 'Fire',
    'Uttara Bhadrapada': 'Water',
    'Revati': 'Water'
}

# Nakshatra doshas
NAKSHATRA_DOSHAS = {
    'Ashwini': 'Vata',
    'Bharani': 'Pitta',
    'Krittika': 'Kapha',
    'Rohini': 'Vata',
    'Mrigashira': 'Pitta',
    'Ardra': 'Kapha',
    'Punarvasu': 'Vata',
    'Pushya': 'Pitta',
    'Ashlesha': 'Kapha',
    'Magha': 'Vata',
    'Purva Phalguni': 'Pitta',
    'Uttara Phalguni': 'Kapha',
    'Hasta': 'Vata',
    'Chitra': 'Pitta',
    'Swati': 'Kapha',
    'Vishakha': 'Vata',
    'Anuradha': 'Pitta',
    'Jyeshtha': 'Kapha',
    'Mula': 'Vata',
    'Purva Ashadha': 'Pitta',
    'Uttara Ashadha': 'Kapha',
    'Shravana': 'Vata',
    'Dhanishta': 'Pitta',
    'Shatabhisha': 'Kapha',
    'Purva Bhadrapada': 'Vata',
    'Uttara Bhadrapada': 'Pitta',
    'Revati': 'Kapha'
}

# Vimshottari Dasha periods (in years)
VIMSHOTTARI_PERIODS = {
    const.KETU: 7,
    const.VENUS: 20,
    const.SUN: 6,
    const.MOON: 10,
    const.MARS: 7,
    const.RAHU: 18,
    const.JUPITER: 16,
    const.SATURN: 19,
    const.MERCURY: 17
}

# Total years in Vimshottari Dasha cycle
TOTAL_VIMSHOTTARI_YEARS = sum(VIMSHOTTARI_PERIODS.values())  # 120 years

# Nakshatra span in degrees
NAKSHATRA_SPAN = 13.33333333333333  # 360 / 27

# Pada (quarter) span in degrees
PADA_SPAN = NAKSHATRA_SPAN / 4  # 3.33333333333333


@calculation_cache()
def get_nakshatra(longitude):
    """
    Get nakshatra information from longitude

    Args:
        longitude (float): The longitude in degrees (0-360)

    Returns:
        dict: Dictionary with nakshatra information
    """
    # Calculate nakshatra index (0-26)
    nakshatra_index = int(longitude / NAKSHATRA_SPAN) % 27

    # Get nakshatra name
    nakshatra = LIST_NAKSHATRAS[nakshatra_index]

    # Calculate position within nakshatra (0-13.33333 degrees)
    pos_in_nakshatra = longitude % NAKSHATRA_SPAN

    # Calculate pada (quarter) (1-4)
    pada = int(pos_in_nakshatra / PADA_SPAN) + 1

    # Calculate percentage through nakshatra
    percentage = (pos_in_nakshatra / NAKSHATRA_SPAN) * 100

    # Get nakshatra lord
    lord = NAKSHATRA_LORDS[nakshatra]

    # Get nakshatra element and dosha
    element = NAKSHATRA_ELEMENTS[nakshatra]
    dosha = NAKSHATRA_DOSHAS[nakshatra]

    return {
        'index': nakshatra_index,
        'name': nakshatra,
        'lord': lord,
        'pada': pada,
        'percentage': percentage,
        'element': element,
        'dosha': dosha
    }


@reference_cache()
def get_nakshatra_lord(nakshatra):
    """
    Get the lord of a nakshatra

    Args:
        nakshatra (str): The nakshatra name

    Returns:
        str: The lord (planet name)
    """
    if nakshatra not in NAKSHATRA_LORDS:
        raise ValueError(f"Invalid nakshatra: {nakshatra}")
    
    return NAKSHATRA_LORDS[nakshatra]


@calculation_cache()
def get_nakshatra_pada(longitude):
    """
    Get the pada (quarter) of a nakshatra

    Args:
        longitude (float): The longitude in degrees (0-360)

    Returns:
        int: The pada (1-4)
    """
    # Calculate position within nakshatra (0-13.33333 degrees)
    pos_in_nakshatra = longitude % NAKSHATRA_SPAN
    
    # Calculate pada (quarter) (1-4)
    pada = int(pos_in_nakshatra / PADA_SPAN) + 1
    
    return pada


@calculation_cache()
def get_nakshatra_degree(longitude):
    """
    Get the degree within the nakshatra (0-13.33...)

    Args:
        longitude (float): The longitude in degrees (0-360)

    Returns:
        float: Degree within the nakshatra
    """
    nakshatra_index = int(longitude / NAKSHATRA_SPAN)
    nakshatra_start = nakshatra_index * NAKSHATRA_SPAN
    return longitude - nakshatra_start


@reference_cache()
def get_nakshatra_qualities(nakshatra):
    """
    Get the qualities of a nakshatra

    Args:
        nakshatra (str): The nakshatra name

    Returns:
        dict: Dictionary with nakshatra qualities
    """
    if nakshatra not in LIST_NAKSHATRAS:
        raise ValueError(f"Invalid nakshatra: {nakshatra}")
    
    return {
        'element': NAKSHATRA_ELEMENTS[nakshatra],
        'dosha': NAKSHATRA_DOSHAS[nakshatra]
    }
