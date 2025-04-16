"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Nakshatra (lunar mansion) calculations
    for Vedic astrology.
"""

from astrovedic import const
from astrovedic import angle

# Nakshatra names
ASHWINI = 'Ashwini'
BHARANI = 'Bharani'
KRITTIKA = 'Krittika'
ROHINI = 'Rohini'
MRIGASHIRA = 'Mrigashira'
ARDRA = 'Ardra'
PUNARVASU = 'Punarvasu'
PUSHYA = 'Pushya'
ASHLESHA = 'Ashlesha'
MAGHA = 'Magha'
PURVA_PHALGUNI = 'Purva Phalguni'
UTTARA_PHALGUNI = 'Uttara Phalguni'
HASTA = 'Hasta'
CHITRA = 'Chitra'
SWATI = 'Swati'
VISHAKHA = 'Vishakha'
ANURADHA = 'Anuradha'
JYESHTHA = 'Jyeshtha'
MULA = 'Mula'
PURVA_ASHADHA = 'Purva Ashadha'
UTTARA_ASHADHA = 'Uttara Ashadha'
SHRAVANA = 'Shravana'
DHANISHTA = 'Dhanishta'
SHATABHISHA = 'Shatabhisha'
PURVA_BHADRAPADA = 'Purva Bhadrapada'
UTTARA_BHADRAPADA = 'Uttara Bhadrapada'
REVATI = 'Revati'

# List of all 27 nakshatras
LIST_NAKSHATRAS = [
    ASHWINI, BHARANI, KRITTIKA, ROHINI, MRIGASHIRA, ARDRA, PUNARVASU,
    PUSHYA, ASHLESHA, MAGHA, PURVA_PHALGUNI, UTTARA_PHALGUNI, HASTA,
    CHITRA, SWATI, VISHAKHA, ANURADHA, JYESHTHA, MULA,
    PURVA_ASHADHA, UTTARA_ASHADHA, SHRAVANA, DHANISHTA, SHATABHISHA,
    PURVA_BHADRAPADA, UTTARA_BHADRAPADA, REVATI
]

# Nakshatra lords (rulers) in Vimshottari Dasha system
NAKSHATRA_LORDS = {
    ASHWINI: const.KETU,
    BHARANI: const.VENUS,
    KRITTIKA: const.SUN,
    ROHINI: const.MOON,
    MRIGASHIRA: const.MARS,
    ARDRA: const.RAHU,
    PUNARVASU: const.JUPITER,
    PUSHYA: const.SATURN,
    ASHLESHA: const.MERCURY,
    MAGHA: const.KETU,
    PURVA_PHALGUNI: const.VENUS,
    UTTARA_PHALGUNI: const.SUN,
    HASTA: const.MOON,
    CHITRA: const.MARS,
    SWATI: const.RAHU,
    VISHAKHA: const.JUPITER,
    ANURADHA: const.SATURN,
    JYESHTHA: const.MERCURY,
    MULA: const.KETU,
    PURVA_ASHADHA: const.VENUS,
    UTTARA_ASHADHA: const.SUN,
    SHRAVANA: const.MOON,
    DHANISHTA: const.MARS,
    SHATABHISHA: const.RAHU,
    PURVA_BHADRAPADA: const.JUPITER,
    UTTARA_BHADRAPADA: const.SATURN,
    REVATI: const.MERCURY
}

# Nakshatra elements (tattvas)
NAKSHATRA_ELEMENTS = {
    ASHWINI: const.FIRE,
    BHARANI: const.EARTH,
    KRITTIKA: const.FIRE,
    ROHINI: const.EARTH,
    MRIGASHIRA: const.AIR,
    ARDRA: const.WATER,
    PUNARVASU: const.AIR,
    PUSHYA: const.WATER,
    ASHLESHA: const.WATER,
    MAGHA: const.FIRE,
    PURVA_PHALGUNI: const.FIRE,
    UTTARA_PHALGUNI: const.FIRE,
    HASTA: const.AIR,
    CHITRA: const.AIR,
    SWATI: const.AIR,
    VISHAKHA: const.FIRE,
    ANURADHA: const.EARTH,
    JYESHTHA: const.EARTH,
    MULA: const.WATER,
    PURVA_ASHADHA: const.WATER,
    UTTARA_ASHADHA: const.EARTH,
    SHRAVANA: const.EARTH,
    DHANISHTA: const.AIR,
    SHATABHISHA: const.WATER,
    PURVA_BHADRAPADA: const.FIRE,
    UTTARA_BHADRAPADA: const.WATER,
    REVATI: const.WATER
}

# Nakshatra doshas (temperaments)
NAKSHATRA_DOSHAS = {
    ASHWINI: const.VATA,
    BHARANI: const.KAPHA,
    KRITTIKA: const.PITTA,
    ROHINI: const.KAPHA,
    MRIGASHIRA: const.VATA,
    ARDRA: const.VATA,
    PUNARVASU: const.VATA,
    PUSHYA: const.KAPHA,
    ASHLESHA: const.KAPHA,
    MAGHA: const.PITTA,
    PURVA_PHALGUNI: const.PITTA,
    UTTARA_PHALGUNI: const.PITTA,
    HASTA: const.VATA,
    CHITRA: const.VATA,
    SWATI: const.VATA,
    VISHAKHA: const.PITTA,
    ANURADHA: const.KAPHA,
    JYESHTHA: const.KAPHA,
    MULA: const.VATA,
    PURVA_ASHADHA: const.PITTA,
    UTTARA_ASHADHA: const.KAPHA,
    SHRAVANA: const.KAPHA,
    DHANISHTA: const.VATA,
    SHATABHISHA: const.VATA,
    PURVA_BHADRAPADA: const.PITTA,
    UTTARA_BHADRAPADA: const.KAPHA,
    REVATI: const.KAPHA
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


def get_nakshatra_lord(longitude):
    """
    Get nakshatra lord from longitude

    Args:
        longitude (float): The longitude in degrees (0-360)

    Returns:
        str: Nakshatra lord (planet name)
    """
    nakshatra_info = get_nakshatra(longitude)
    return nakshatra_info['lord']


def get_nakshatra_span(nakshatra_index):
    """
    Get the span (start and end longitudes) of a nakshatra

    Args:
        nakshatra_index (int): The nakshatra index (0-26)

    Returns:
        tuple: (start_longitude, end_longitude)
    """
    start_longitude = (nakshatra_index * NAKSHATRA_SPAN) % 360
    end_longitude = (start_longitude + NAKSHATRA_SPAN) % 360
    return (start_longitude, end_longitude)


def get_pada_span(nakshatra_index, pada):
    """
    Get the span (start and end longitudes) of a pada

    Args:
        nakshatra_index (int): The nakshatra index (0-26)
        pada (int): The pada (1-4)

    Returns:
        tuple: (start_longitude, end_longitude)
    """
    nakshatra_start, _ = get_nakshatra_span(nakshatra_index)
    pada_start = nakshatra_start + ((pada - 1) * PADA_SPAN)
    pada_end = pada_start + PADA_SPAN
    return (pada_start % 360, pada_end % 360)


def get_nakshatra_pada(longitude):
    """
    Get nakshatra pada from longitude

    Args:
        longitude (float): The longitude in degrees (0-360)

    Returns:
        int: Pada (1-4)
    """
    nakshatra_info = get_nakshatra(longitude)
    return nakshatra_info['pada']


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


def get_nakshatra_qualities(nakshatra):
    """
    Get the qualities of a nakshatra

    Args:
        nakshatra (str): The nakshatra name

    Returns:
        dict: Dictionary with nakshatra qualities
    """
    # Validate the nakshatra name
    if nakshatra not in LIST_NAKSHATRAS:
        raise ValueError(f"Invalid nakshatra: {nakshatra}")

    # Get the element and dosha directly from the dictionaries
    element = NAKSHATRA_ELEMENTS[nakshatra]
    dosha = NAKSHATRA_DOSHAS[nakshatra]

    return {
        'element': element,
        'dosha': dosha
    }
