"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Nabhasa Yogas (special planetary patterns)
    for Vedic astrology.
"""

from astrovedic import const
from astrovedic.vedic.yogas.core import (
    get_house_number, get_yoga_strength
)


def get_nabhasa_yogas(chart):
    """
    Identify Nabhasa Yogas in a chart
    
    Nabhasa Yogas are special planetary patterns formed by the arrangement
    of planets in different signs.
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        list: List of Nabhasa Yogas in the chart
    """
    # Initialize the result
    result = []
    
    # Check for Rajju Yoga
    rajju = has_rajju_yoga(chart)
    if rajju:
        result.append(rajju)
    
    # Check for Musala Yoga
    musala = has_musala_yoga(chart)
    if musala:
        result.append(musala)
    
    # Check for Nala Yoga
    nala = has_nala_yoga(chart)
    if nala:
        result.append(nala)
    
    # Check for Mala Yoga
    mala = has_mala_yoga(chart)
    if mala:
        result.append(mala)
    
    # Check for Sarpa Yoga
    sarpa = has_sarpa_yoga(chart)
    if sarpa:
        result.append(sarpa)
    
    return result


def has_rajju_yoga(chart):
    """
    Check if a chart has Rajju Yoga
    
    Rajju Yoga is formed when all planets are in movable signs (Aries, Cancer,
    Libra, Capricorn).
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Rajju Yoga information, or None if not present
    """
    # Get all planets
    planets = [
        chart.getObject(const.SUN),
        chart.getObject(const.MOON),
        chart.getObject(const.MERCURY),
        chart.getObject(const.VENUS),
        chart.getObject(const.MARS),
        chart.getObject(const.JUPITER),
        chart.getObject(const.SATURN)
    ]
    
    # Check if all planets are in movable signs
    movable_signs = [const.ARIES, const.CANCER, const.LIBRA, const.CAPRICORN]
    all_in_movable = all(planet.sign in movable_signs for planet in planets)
    
    # Check if Rajju Yoga is formed
    if all_in_movable:
        # Create the Yoga information
        yoga = {
            'name': 'Rajju Yoga',
            'type': 'Nabhasa Yoga',
            'planets': [planet.id for planet in planets],
            'houses': [],
            'description': 'Formed when all planets are in movable signs (Aries, Cancer, Libra, Capricorn)',
            'is_beneficial': True
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    return None


def has_musala_yoga(chart):
    """
    Check if a chart has Musala Yoga
    
    Musala Yoga is formed when all planets are in fixed signs (Taurus, Leo,
    Scorpio, Aquarius).
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Musala Yoga information, or None if not present
    """
    # Get all planets
    planets = [
        chart.getObject(const.SUN),
        chart.getObject(const.MOON),
        chart.getObject(const.MERCURY),
        chart.getObject(const.VENUS),
        chart.getObject(const.MARS),
        chart.getObject(const.JUPITER),
        chart.getObject(const.SATURN)
    ]
    
    # Check if all planets are in fixed signs
    fixed_signs = [const.TAURUS, const.LEO, const.SCORPIO, const.AQUARIUS]
    all_in_fixed = all(planet.sign in fixed_signs for planet in planets)
    
    # Check if Musala Yoga is formed
    if all_in_fixed:
        # Create the Yoga information
        yoga = {
            'name': 'Musala Yoga',
            'type': 'Nabhasa Yoga',
            'planets': [planet.id for planet in planets],
            'houses': [],
            'description': 'Formed when all planets are in fixed signs (Taurus, Leo, Scorpio, Aquarius)',
            'is_beneficial': True
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    return None


def has_nala_yoga(chart):
    """
    Check if a chart has Nala Yoga
    
    Nala Yoga is formed when all planets are in dual signs (Gemini, Virgo,
    Sagittarius, Pisces).
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Nala Yoga information, or None if not present
    """
    # Get all planets
    planets = [
        chart.getObject(const.SUN),
        chart.getObject(const.MOON),
        chart.getObject(const.MERCURY),
        chart.getObject(const.VENUS),
        chart.getObject(const.MARS),
        chart.getObject(const.JUPITER),
        chart.getObject(const.SATURN)
    ]
    
    # Check if all planets are in dual signs
    dual_signs = [const.GEMINI, const.VIRGO, const.SAGITTARIUS, const.PISCES]
    all_in_dual = all(planet.sign in dual_signs for planet in planets)
    
    # Check if Nala Yoga is formed
    if all_in_dual:
        # Create the Yoga information
        yoga = {
            'name': 'Nala Yoga',
            'type': 'Nabhasa Yoga',
            'planets': [planet.id for planet in planets],
            'houses': [],
            'description': 'Formed when all planets are in dual signs (Gemini, Virgo, Sagittarius, Pisces)',
            'is_beneficial': True
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    return None


def has_mala_yoga(chart):
    """
    Check if a chart has Mala Yoga
    
    Mala Yoga is formed when all planets are in consecutive signs.
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Mala Yoga information, or None if not present
    """
    # Get all planets
    planets = [
        chart.getObject(const.SUN),
        chart.getObject(const.MOON),
        chart.getObject(const.MERCURY),
        chart.getObject(const.VENUS),
        chart.getObject(const.MARS),
        chart.getObject(const.JUPITER),
        chart.getObject(const.SATURN)
    ]
    
    # Get the signs of all planets
    signs = [planet.sign for planet in planets]
    
    # Convert signs to numbers (0-11)
    sign_numbers = []
    for sign in signs:
        if sign == const.ARIES:
            sign_numbers.append(0)
        elif sign == const.TAURUS:
            sign_numbers.append(1)
        elif sign == const.GEMINI:
            sign_numbers.append(2)
        elif sign == const.CANCER:
            sign_numbers.append(3)
        elif sign == const.LEO:
            sign_numbers.append(4)
        elif sign == const.VIRGO:
            sign_numbers.append(5)
        elif sign == const.LIBRA:
            sign_numbers.append(6)
        elif sign == const.SCORPIO:
            sign_numbers.append(7)
        elif sign == const.SAGITTARIUS:
            sign_numbers.append(8)
        elif sign == const.CAPRICORN:
            sign_numbers.append(9)
        elif sign == const.AQUARIUS:
            sign_numbers.append(10)
        elif sign == const.PISCES:
            sign_numbers.append(11)
    
    # Sort the sign numbers
    sign_numbers.sort()
    
    # Check if all planets are in consecutive signs
    is_consecutive = True
    for i in range(1, len(sign_numbers)):
        if (sign_numbers[i] - sign_numbers[i-1]) % 12 != 1:
            is_consecutive = False
            break
    
    # Check if Mala Yoga is formed
    if is_consecutive:
        # Create the Yoga information
        yoga = {
            'name': 'Mala Yoga',
            'type': 'Nabhasa Yoga',
            'planets': [planet.id for planet in planets],
            'houses': [],
            'description': 'Formed when all planets are in consecutive signs',
            'is_beneficial': True
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    return None


def has_sarpa_yoga(chart):
    """
    Check if a chart has Sarpa Yoga
    
    Sarpa Yoga is formed when all planets are in the 6th, 7th, and 8th houses
    from the Ascendant.
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Sarpa Yoga information, or None if not present
    """
    # Get all planets
    planets = [
        chart.getObject(const.SUN),
        chart.getObject(const.MOON),
        chart.getObject(const.MERCURY),
        chart.getObject(const.VENUS),
        chart.getObject(const.MARS),
        chart.getObject(const.JUPITER),
        chart.getObject(const.SATURN)
    ]
    
    # Get the house numbers of all planets
    houses = [get_house_number(chart, planet.id) for planet in planets]
    
    # Check if all planets are in the 6th, 7th, and 8th houses
    all_in_6_7_8 = all(house in [6, 7, 8] for house in houses)
    
    # Check if Sarpa Yoga is formed
    if all_in_6_7_8:
        # Create the Yoga information
        yoga = {
            'name': 'Sarpa Yoga',
            'type': 'Nabhasa Yoga',
            'planets': [planet.id for planet in planets],
            'houses': [6, 7, 8],
            'description': 'Formed when all planets are in the 6th, 7th, and 8th houses from the Ascendant',
            'is_beneficial': False
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    return None
