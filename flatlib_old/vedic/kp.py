"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements KP (Krishnamurti Paddhati) astrology calculations.
    It includes sublord and sub-sublord calculations based on the
    Vimshottari Dasha system.
"""

from flatlib import const
from flatlib import angle
from flatlib.vedic.nakshatras import (
    get_nakshatra, VIMSHOTTARI_PERIODS, TOTAL_VIMSHOTTARI_YEARS,
    NAKSHATRA_SPAN
)

# Planet abbreviations for KP pointers
PLANET_ABBR = {
    const.SUN: 'Sun',
    const.MOON: 'Moo',
    const.MERCURY: 'Mer',
    const.VENUS: 'Ven',
    const.MARS: 'Mar',
    const.JUPITER: 'Jup',
    const.SATURN: 'Sat',
    const.RAHU: 'Rah',
    const.KETU: 'Ket'
}

# Vimshottari Dasha planet sequence
VIMSHOTTARI_SEQUENCE = [
    const.KETU, const.VENUS, const.SUN, const.MOON, const.MARS,
    const.RAHU, const.JUPITER, const.SATURN, const.MERCURY
]


def get_kp_sublord(longitude):
    """
    Get the sublord for KP astrology based on Vimshottari Dasha periods

    Args:
        longitude (float): The longitude in degrees (0-360)

    Returns:
        dict: Dictionary with sublord information
    """
    # Get nakshatra information
    nakshatra_info = get_nakshatra(longitude)
    nakshatra_index = nakshatra_info['index']
    star_lord = nakshatra_info['lord']

    # Calculate position within nakshatra (0-13.33333 degrees)
    pos_in_nakshatra = longitude % NAKSHATRA_SPAN

    # Get sign information
    sign_num = int(longitude / 30)
    sign = const.LIST_SIGNS[sign_num]
    sign_lord = const.LIST_RULERS[sign]

    # Find the starting index in the Vimshottari sequence
    start_idx = VIMSHOTTARI_SEQUENCE.index(star_lord)

    # Calculate sub divisions based on Vimshottari dasha periods
    current_pos = 0
    sub_lord = None

    for i in range(9):  # 9 planets in Vimshottari
        lord_idx = (start_idx + i) % 9
        current_lord = VIMSHOTTARI_SEQUENCE[lord_idx]

        # Calculate sub length based on Vimshottari period
        sub_length = (VIMSHOTTARI_PERIODS[current_lord] / TOTAL_VIMSHOTTARI_YEARS) * NAKSHATRA_SPAN

        if current_pos <= pos_in_nakshatra < (current_pos + sub_length):
            sub_lord = current_lord
            sub_pos = pos_in_nakshatra - current_pos
            sub_length_found = sub_length
            break

        current_pos += sub_length

    # If no sub lord found (shouldn't happen), use star lord
    if not sub_lord:
        sub_lord = star_lord
        sub_pos = 0
        sub_length_found = NAKSHATRA_SPAN

    return {
        'rasi_lord': sign_lord,
        'nakshatra_lord': star_lord,
        'sub_lord': sub_lord,
        'sub_position': sub_pos,
        'sub_length': sub_length_found
    }


def get_kp_sub_sublord(longitude):
    """
    Get the sub-sublord for KP astrology

    Args:
        longitude (float): The longitude in degrees (0-360)

    Returns:
        str: The sub-sublord (planet name)
    """
    # Get sublord information
    sublord_info = get_kp_sublord(longitude)
    sub_lord = sublord_info['sub_lord']
    sub_pos = sublord_info['sub_position']
    sub_length = sublord_info['sub_length']

    # Find the starting index in the Vimshottari sequence
    start_idx = VIMSHOTTARI_SEQUENCE.index(sub_lord)

    # Calculate sub-sub divisions based on Vimshottari dasha periods
    current_pos = 0
    sub_sub_lord = None

    for i in range(9):  # 9 planets in Vimshottari
        lord_idx = (start_idx + i) % 9
        current_lord = VIMSHOTTARI_SEQUENCE[lord_idx]

        # Calculate sub-sub length based on Vimshottari period
        sub_sub_length = (VIMSHOTTARI_PERIODS[current_lord] / TOTAL_VIMSHOTTARI_YEARS) * sub_length

        if current_pos <= sub_pos < (current_pos + sub_sub_length):
            sub_sub_lord = current_lord
            break

        current_pos += sub_sub_length

    # If no sub-sub lord found (shouldn't happen), use sub lord
    if not sub_sub_lord:
        sub_sub_lord = sub_lord

    return sub_sub_lord


def get_kp_pointer(longitude):
    """
    Get the KP pointer (Sign Lord-Star Lord-Sub Lord-Sub Sub Lord)

    Args:
        longitude (float): The longitude in degrees (0-360)

    Returns:
        str: The KP pointer string
    """
    # Get the KP lords information
    sublord_info = get_kp_sublord(longitude)
    sub_sublord = get_kp_sub_sublord(longitude)

    # Format the KP pointer
    sign_lord = sublord_info['rasi_lord']
    star_lord = sublord_info['nakshatra_lord']
    sub_lord = sublord_info['sub_lord']

    sign_abbr = PLANET_ABBR.get(sign_lord, sign_lord[:3])
    star_abbr = PLANET_ABBR.get(star_lord, star_lord[:3])
    sub_abbr = PLANET_ABBR.get(sub_lord, sub_lord[:3])
    sub_sub_abbr = PLANET_ABBR.get(sub_sublord, sub_sublord[:3])

    kp_pointer = f"{sign_abbr}-{star_abbr}-{sub_abbr}-{sub_sub_abbr}"

    return kp_pointer


def get_kp_lords(longitude):
    """
    Get sign lord, star lord, sub lord, and sub-sub lord for KP astrology

    Args:
        longitude (float): The longitude in degrees (0-360)

    Returns:
        dict: Dictionary with KP lords information
    """
    # Get the sublord information
    sublord_info = get_kp_sublord(longitude)

    # Get the sub-sublord
    sub_sublord = get_kp_sub_sublord(longitude)

    # Get the KP pointer
    kp_pointer = get_kp_pointer(longitude)

    return {
        'sign_lord': sublord_info['rasi_lord'],
        'star_lord': sublord_info['nakshatra_lord'],
        'sub_lord': sublord_info['sub_lord'],
        'sub_sub_lord': sub_sublord,
        'kp_pointer': kp_pointer
    }


def get_kp_planets(chart):
    """
    Get KP information for all planets in a chart

    Args:
        chart (Chart): The chart

    Returns:
        dict: Dictionary with KP information for all planets
    """
    kp_planets = {}

    for planet_id in const.LIST_PLANETS:
        planet = chart.getObject(planet_id)
        if planet:
            kp_planets[planet_id] = {
                'longitude': planet['lon'],
                'sign': planet['sign'],
                'house': planet['house'],
                'kp_lords': get_kp_lords(planet['lon']),
                'kp_pointer': get_kp_pointer(planet['lon'])
            }

    return kp_planets


def get_kp_houses(chart):
    """
    Get KP information for all houses in a chart

    Args:
        chart (Chart): The chart

    Returns:
        dict: Dictionary with KP information for all houses
    """
    kp_houses = {}

    for house_num in range(1, 13):
        house = chart.houses.get(house_num)
        kp_houses[house_num] = {
            'longitude': house.lon,
            'sign': house.sign,
            'kp_lords': get_kp_lords(house.lon),
            'kp_pointer': get_kp_pointer(house.lon)
        }

    return kp_houses


def get_kp_cusps(chart):
    """
    Get KP information for all house cusps in a chart

    Args:
        chart (Chart): The chart

    Returns:
        dict: Dictionary with KP information for all house cusps
    """
    return get_kp_houses(chart)


def get_kp_significators(chart, house_num):
    """
    Get KP significators for a house

    Args:
        chart (Chart): The chart
        house_num (int): The house number (1-12)

    Returns:
        dict: Dictionary with KP significators for the house
    """
    # Get the house
    house = chart.houses.get(house_num)

    # Get the house sublord
    house_sublord = get_kp_sublord(house.lon)['sub_lord']

    # Get the planets in the star of the house sublord
    star_significators = []
    for planet_id in const.LIST_PLANETS:
        planet = chart.getObject(planet_id)
        if planet and get_nakshatra(planet['lon'])['lord'] == house_sublord:
            star_significators.append(planet_id)

    # Get the planets in the house
    occupants = []
    for planet_id in const.LIST_PLANETS:
        planet = chart.getObject(planet_id)
        if planet and planet['house'] == house_num:
            occupants.append(planet_id)

    return {
        'house_num': house_num,
        'house_sublord': house_sublord,
        'star_significators': star_significators,
        'occupants': occupants
    }


def get_kp_sublords(chart):
    """
    Get KP sublords for all planets and houses in a chart

    Args:
        chart (Chart): The chart

    Returns:
        dict: Dictionary with KP sublords for all planets and houses
    """
    sublords = {
        'planets': {},
        'houses': {}
    }

    # Get sublords for planets
    for planet_id in const.LIST_PLANETS:
        planet = chart.getObject(planet_id)
        if planet:
            sublords['planets'][planet_id] = get_kp_sublord(planet['lon'])['sub_lord']

    # Get sublords for houses
    for house_num in range(1, 13):
        house = chart.houses.get(house_num)
        sublords['houses'][house_num] = get_kp_sublord(house.lon)['sub_lord']

    return sublords


def get_kp_ruling_planets(chart):
    """
    Get KP ruling planets for a chart

    Args:
        chart (Chart): The chart

    Returns:
        dict: Dictionary with KP ruling planets
    """
    # Get the current time
    current_time = chart.date

    # Get the day lord (ruler of the day)
    day_of_week = current_time.dayofweek()
    day_lord = const.LIST_WEEK_RULERS[day_of_week]

    # Get the Moon nakshatra lord
    moon = chart.getObject(const.MOON)
    moon_nakshatra_lord = get_nakshatra(moon['lon'])['lord']

    # Get the lagna (ascendant) sublord
    lagna = chart.houses.get(1)
    lagna_sublord = get_kp_sublord(lagna.lon)['sub_lord']

    return {
        'day_lord': day_lord,
        'moon_nakshatra_lord': moon_nakshatra_lord,
        'lagna_sublord': lagna_sublord
    }
