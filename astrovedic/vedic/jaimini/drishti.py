"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Jaimini Rashi Drishti (sign aspect) calculations.
    In Jaimini astrology, sign aspects follow specific rules that differ from
    standard Vedic aspects.
"""

from typing import Dict, List, Optional, Tuple, Union
from astrovedic import const
from astrovedic.chart import Chart

# List of planets to use for Jaimini aspects
JAIMINI_PLANETS = [
    const.SUN, const.MOON, const.MERCURY, const.VENUS,
    const.MARS, const.JUPITER, const.SATURN, const.RAHU, const.KETU
]

# Jaimini Rashi Drishti (sign aspect) rules
# In Jaimini astrology, signs aspect other signs based on specific rules:
# 1. All signs aspect the 7th sign from them (standard Vedic rule)
# 2. Signs in a 2/12 relationship have mutual aspect
# 3. Signs in a 5/9 relationship have mutual aspect
# 4. Signs in a 4/10 relationship have mutual aspect
# 5. Signs in a 3/11 relationship have mutual aspect (some traditions)

# Aspect types
JAIMINI_FULL_ASPECT = "Jaimini Full Aspect"
JAIMINI_MUTUAL_ASPECT = "Jaimini Mutual Aspect"

# Aspect relationships
SEVENTH_ASPECT = 7  # Standard 7th aspect
SECOND_TWELFTH_ASPECT = [2, 12]  # 2/12 relationship
FIFTH_NINTH_ASPECT = [5, 9]  # 5/9 relationship
FOURTH_TENTH_ASPECT = [4, 10]  # 4/10 relationship
THIRD_ELEVENTH_ASPECT = [3, 11]  # 3/11 relationship (some traditions)

def get_sign_number(sign: str) -> int:
    """
    Get the number (1-12) of a sign.

    Args:
        sign (str): The sign name (e.g., 'Aries', 'Taurus', etc.)

    Returns:
        int: The sign number (1-12)
    """
    signs = [
        const.ARIES, const.TAURUS, const.GEMINI, const.CANCER,
        const.LEO, const.VIRGO, const.LIBRA, const.SCORPIO,
        const.SAGITTARIUS, const.CAPRICORN, const.AQUARIUS, const.PISCES
    ]
    return signs.index(sign) + 1

def get_sign_from_number(sign_num: int) -> str:
    """
    Get the sign name from a sign number (1-12).

    Args:
        sign_num (int): The sign number (1-12)

    Returns:
        str: The sign name (e.g., 'Aries', 'Taurus', etc.)
    """
    signs = [
        const.ARIES, const.TAURUS, const.GEMINI, const.CANCER,
        const.LEO, const.VIRGO, const.LIBRA, const.SCORPIO,
        const.SAGITTARIUS, const.CAPRICORN, const.AQUARIUS, const.PISCES
    ]
    return signs[(sign_num - 1) % 12]

def get_sign_distance(from_sign: str, to_sign: str) -> int:
    """
    Calculate the distance in signs (1-12) between two signs.

    Args:
        from_sign (str): The starting sign
        to_sign (str): The ending sign

    Returns:
        int: The distance in signs (1-12)
    """
    from_num = get_sign_number(from_sign)
    to_num = get_sign_number(to_sign)

    # Calculate the distance (1-12)
    return ((to_num - from_num) % 12) + 1

def has_jaimini_rashi_drishti(from_sign: str, to_sign: str, include_third_eleventh: bool = True) -> bool:
    """
    Check if a sign aspects another sign according to Jaimini rules.

    Args:
        from_sign (str): The sign casting the aspect
        to_sign (str): The sign receiving the aspect
        include_third_eleventh (bool): Whether to include 3/11 aspects (some traditions)

    Returns:
        bool: True if the sign aspects the other sign, False otherwise
    """
    # Calculate the distance in signs (1-12)
    sign_distance = get_sign_distance(from_sign, to_sign)

    # All signs aspect the 7th sign
    if sign_distance == SEVENTH_ASPECT:
        return True

    # Signs in a 2/12 relationship have mutual aspect
    if sign_distance in SECOND_TWELFTH_ASPECT:
        return True

    # Signs in a 5/9 relationship have mutual aspect
    if sign_distance in FIFTH_NINTH_ASPECT:
        return True

    # Signs in a 4/10 relationship have mutual aspect
    if sign_distance in FOURTH_TENTH_ASPECT:
        return True

    # Signs in a 3/11 relationship have mutual aspect (some traditions)
    if include_third_eleventh and sign_distance in THIRD_ELEVENTH_ASPECT:
        return True

    # No aspect
    return False

def get_jaimini_rashi_drishti_info(from_sign: str, to_sign: str, include_third_eleventh: bool = True) -> Dict[str, any]:
    """
    Get information about a Jaimini Rashi Drishti (sign aspect).

    Args:
        from_sign (str): The sign casting the aspect
        to_sign (str): The sign receiving the aspect
        include_third_eleventh (bool): Whether to include 3/11 aspects (some traditions)

    Returns:
        dict: Dictionary with aspect information
    """
    # Calculate the distance in signs (1-12)
    sign_distance = get_sign_distance(from_sign, to_sign)

    # Initialize aspect information
    aspect_info = {
        'has_aspect': False,
        'type': None,
        'sign_distance': sign_distance,
        'is_mutual': False
    }

    # All signs aspect the 7th sign
    if sign_distance == SEVENTH_ASPECT:
        aspect_info['has_aspect'] = True
        aspect_info['type'] = JAIMINI_FULL_ASPECT
        aspect_info['is_mutual'] = True
        return aspect_info

    # Signs in a 2/12 relationship have mutual aspect
    if sign_distance in SECOND_TWELFTH_ASPECT:
        aspect_info['has_aspect'] = True
        aspect_info['type'] = JAIMINI_MUTUAL_ASPECT
        aspect_info['is_mutual'] = True
        return aspect_info

    # Signs in a 5/9 relationship have mutual aspect
    if sign_distance in FIFTH_NINTH_ASPECT:
        aspect_info['has_aspect'] = True
        aspect_info['type'] = JAIMINI_MUTUAL_ASPECT
        aspect_info['is_mutual'] = True
        return aspect_info

    # Signs in a 4/10 relationship have mutual aspect
    if sign_distance in FOURTH_TENTH_ASPECT:
        aspect_info['has_aspect'] = True
        aspect_info['type'] = JAIMINI_MUTUAL_ASPECT
        aspect_info['is_mutual'] = True
        return aspect_info

    # Signs in a 3/11 relationship have mutual aspect (some traditions)
    if include_third_eleventh and sign_distance in THIRD_ELEVENTH_ASPECT:
        aspect_info['has_aspect'] = True
        aspect_info['type'] = JAIMINI_MUTUAL_ASPECT
        aspect_info['is_mutual'] = True
        return aspect_info

    # No aspect
    return aspect_info

def get_jaimini_sign_aspects(sign: str, include_third_eleventh: bool = True) -> List[Dict[str, any]]:
    """
    Get all Jaimini aspects cast by a sign.

    Args:
        sign (str): The sign
        include_third_eleventh (bool): Whether to include 3/11 aspects (some traditions)

    Returns:
        list: List of aspects cast by the sign
    """
    # Initialize the list of aspects
    aspects = []

    # Check aspects to each sign
    for other_sign in const.LIST_SIGNS:
        if other_sign != sign:
            # Calculate the aspect information
            aspect_info = get_jaimini_rashi_drishti_info(sign, other_sign, include_third_eleventh)

            if aspect_info['has_aspect']:
                # Add to the list of aspects
                aspects.append({
                    'from_sign': sign,
                    'to_sign': other_sign,
                    'type': aspect_info['type'],
                    'sign_distance': aspect_info['sign_distance'],
                    'is_mutual': aspect_info['is_mutual']
                })

    return aspects

def get_jaimini_sign_aspects_received(sign: str, include_third_eleventh: bool = True) -> List[Dict[str, any]]:
    """
    Get all Jaimini aspects received by a sign.

    Args:
        sign (str): The sign
        include_third_eleventh (bool): Whether to include 3/11 aspects (some traditions)

    Returns:
        list: List of aspects received by the sign
    """
    # Initialize the list of aspects
    aspects = []

    # Check aspects from each sign
    for other_sign in const.LIST_SIGNS:
        if other_sign != sign:
            # Calculate the aspect information
            aspect_info = get_jaimini_rashi_drishti_info(other_sign, sign, include_third_eleventh)

            if aspect_info['has_aspect']:
                # Add to the list of aspects
                aspects.append({
                    'from_sign': other_sign,
                    'to_sign': sign,
                    'type': aspect_info['type'],
                    'sign_distance': aspect_info['sign_distance'],
                    'is_mutual': aspect_info['is_mutual']
                })

    return aspects

def get_all_jaimini_sign_aspects(include_third_eleventh: bool = True) -> Dict[str, Dict[str, List[Dict[str, any]]]]:
    """
    Get all Jaimini sign aspects.

    Args:
        include_third_eleventh (bool): Whether to include 3/11 aspects (some traditions)

    Returns:
        dict: Dictionary with all sign aspects
    """
    # Initialize the result
    result = {}

    # Get aspects for each sign
    for sign in const.LIST_SIGNS:
        result[sign] = {
            'aspects_cast': get_jaimini_sign_aspects(sign, include_third_eleventh),
            'aspects_received': get_jaimini_sign_aspects_received(sign, include_third_eleventh)
        }

    return result

def get_jaimini_planet_aspects(chart: Chart, planet_id: str, include_third_eleventh: bool = True) -> List[Dict[str, any]]:
    """
    Get all Jaimini aspects cast by a planet in a chart based on its sign placement.

    Args:
        chart (Chart): The chart
        planet_id (str): The ID of the planet
        include_third_eleventh (bool): Whether to include 3/11 aspects (some traditions)

    Returns:
        list: List of aspects cast by the planet
    """
    # Get the planet
    planet = chart.getObject(planet_id)

    # Get the sign of the planet
    planet_sign = planet.sign

    # Get all aspects cast by the sign
    sign_aspects = get_jaimini_sign_aspects(planet_sign, include_third_eleventh)

    # Initialize the list of planet aspects
    planet_aspects = []

    # Convert sign aspects to planet aspects
    for sign_aspect in sign_aspects:
        # Find planets in the aspected sign
        for other_id in JAIMINI_PLANETS:
            if other_id != planet_id:
                other = chart.getObject(other_id)

                if other.sign == sign_aspect['to_sign']:
                    # Add to the list of planet aspects
                    planet_aspects.append({
                        'from_planet': planet_id,
                        'to_planet': other_id,
                        'from_sign': planet_sign,
                        'to_sign': other.sign,
                        'type': sign_aspect['type'],
                        'sign_distance': sign_aspect['sign_distance'],
                        'is_mutual': sign_aspect['is_mutual']
                    })

    return planet_aspects

def get_jaimini_planet_aspects_received(chart: Chart, planet_id: str, include_third_eleventh: bool = True) -> List[Dict[str, any]]:
    """
    Get all Jaimini aspects received by a planet in a chart based on its sign placement.

    Args:
        chart (Chart): The chart
        planet_id (str): The ID of the planet
        include_third_eleventh (bool): Whether to include 3/11 aspects (some traditions)

    Returns:
        list: List of aspects received by the planet
    """
    # Get the planet
    planet = chart.getObject(planet_id)

    # Get the sign of the planet
    planet_sign = planet.sign

    # Get all aspects received by the sign
    sign_aspects = get_jaimini_sign_aspects_received(planet_sign, include_third_eleventh)

    # Initialize the list of planet aspects
    planet_aspects = []

    # Convert sign aspects to planet aspects
    for sign_aspect in sign_aspects:
        # Find planets in the aspecting sign
        for other_id in JAIMINI_PLANETS:
            if other_id != planet_id:
                other = chart.getObject(other_id)

                if other.sign == sign_aspect['from_sign']:
                    # Add to the list of planet aspects
                    planet_aspects.append({
                        'from_planet': other_id,
                        'to_planet': planet_id,
                        'from_sign': other.sign,
                        'to_sign': planet_sign,
                        'type': sign_aspect['type'],
                        'sign_distance': sign_aspect['sign_distance'],
                        'is_mutual': sign_aspect['is_mutual']
                    })

    return planet_aspects

def get_all_jaimini_planet_aspects(chart: Chart, include_third_eleventh: bool = True) -> Dict[str, Dict[str, List[Dict[str, any]]]]:
    """
    Get all Jaimini planet aspects in a chart based on sign placements.

    Args:
        chart (Chart): The chart
        include_third_eleventh (bool): Whether to include 3/11 aspects (some traditions)

    Returns:
        dict: Dictionary with all planet aspects
    """
    # Initialize the result
    result = {}

    # Get aspects for each planet
    for planet_id in JAIMINI_PLANETS:
        result[planet_id] = {
            'aspects_cast': get_jaimini_planet_aspects(chart, planet_id, include_third_eleventh),
            'aspects_received': get_jaimini_planet_aspects_received(chart, planet_id, include_third_eleventh)
        }

    return result

def get_all_jaimini_aspects(chart: Chart, include_third_eleventh: bool = True) -> Dict[str, Dict]:
    """
    Get all Jaimini aspects in a chart.

    Args:
        chart (Chart): The chart
        include_third_eleventh (bool): Whether to include 3/11 aspects (some traditions)

    Returns:
        dict: Dictionary with all aspects
    """
    # Initialize the result
    result = {
        'sign_aspects': get_all_jaimini_sign_aspects(include_third_eleventh),
        'planet_aspects': get_all_jaimini_planet_aspects(chart, include_third_eleventh)
    }

    return result
