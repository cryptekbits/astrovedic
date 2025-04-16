"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module provides cached functions for nakshatra calculations.
    These functions are optimized versions of the functions in nakshatras.py with caching.
"""

from astrovedic import const
from astrovedic.cache import reference_cache, calculation_cache

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
    'Dhanishta': 'Air',
    'Shatabhisha': 'Water',
    'Purva Bhadrapada': 'Fire',
    'Uttara Bhadrapada': 'Water',
    'Revati': 'Water'
}

# Nakshatra doshas
NAKSHATRA_DOSHAS = {
    'Ashwini': 'Vata',
    'Bharani': 'Kapha',
    'Krittika': 'Pitta',
    'Rohini': 'Kapha',
    'Mrigashira': 'Vata',
    'Ardra': 'Vata',
    'Punarvasu': 'Vata',
    'Pushya': 'Kapha',
    'Ashlesha': 'Kapha',
    'Magha': 'Pitta',
    'Purva Phalguni': 'Pitta',
    'Uttara Phalguni': 'Pitta',
    'Hasta': 'Vata',
    'Chitra': 'Vata',
    'Swati': 'Vata',
    'Vishakha': 'Pitta',
    'Anuradha': 'Kapha',
    'Jyeshtha': 'Kapha',
    'Mula': 'Vata',
    'Purva Ashadha': 'Pitta',
    'Uttara Ashadha': 'Kapha',
    'Shravana': 'Kapha',
    'Dhanishta': 'Vata',
    'Shatabhisha': 'Vata',
    'Purva Bhadrapada': 'Pitta',
    'Uttara Bhadrapada': 'Kapha',
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


@calculation_cache(maxsize=360)
def get_nakshatra(longitude):
    """
    Get nakshatra information from longitude

    Args:
        longitude (float): The longitude in degrees (0-360)

    Returns:
        dict: Dictionary with nakshatra information
    """
    # Calculate nakshatra index (0-26) - use integer division for better performance
    nakshatra_index = int(longitude / NAKSHATRA_SPAN) % 27

    # Get nakshatra name
    nakshatra = LIST_NAKSHATRAS[nakshatra_index]

    # Calculate position within nakshatra (0-13.33333 degrees)
    pos_in_nakshatra = longitude % NAKSHATRA_SPAN

    # Calculate pada (quarter) (1-4)
    pada = int(pos_in_nakshatra / PADA_SPAN) + 1

    # Get nakshatra lord, element, and dosha directly
    lord = NAKSHATRA_LORDS[nakshatra]
    element = NAKSHATRA_ELEMENTS[nakshatra]
    dosha = NAKSHATRA_DOSHAS[nakshatra]

    # Return a pre-constructed dictionary for better performance
    return {
        'index': nakshatra_index,
        'name': nakshatra,
        'lord': lord,
        'pada': pada,
        'percentage': (pos_in_nakshatra / NAKSHATRA_SPAN) * 100,
        'element': element,
        'dosha': dosha
    }


@calculation_cache()
def get_nakshatra_lord(longitude):
    """
    Get nakshatra lord from longitude

    Args:
        longitude (float): The longitude in degrees (0-360)

    Returns:
        str: Nakshatra lord (planet name)
    """
    # If longitude is a string (nakshatra name), return the lord directly
    if isinstance(longitude, str):
        if longitude not in NAKSHATRA_LORDS:
            raise ValueError(f"Invalid nakshatra: {longitude}")
        return NAKSHATRA_LORDS[longitude]

    # Otherwise, calculate the nakshatra index and return the lord
    nakshatra_index = int(longitude / NAKSHATRA_SPAN) % 27
    nakshatra = LIST_NAKSHATRAS[nakshatra_index]
    return NAKSHATRA_LORDS[nakshatra]


@calculation_cache(maxsize=360)
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
    return int(pos_in_nakshatra / PADA_SPAN) + 1


@calculation_cache(maxsize=360)
def get_nakshatra_degree(longitude):
    """
    Get the degree within the nakshatra (0-13.33...)

    Args:
        longitude (float): The longitude in degrees (0-360)

    Returns:
        float: Degree within the nakshatra
    """
    # More efficient calculation using modulo
    return longitude % NAKSHATRA_SPAN


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
