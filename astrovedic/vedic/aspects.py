"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Vedic aspect (Drishti) calculations.
    In Vedic astrology, aspects are based on houses/signs rather than angles.
    
    There are two types of aspects in Vedic astrology:
    1. Graha Drishti (Planetary Aspects): Each planet aspects specific houses from its position
    2. Rashi Drishti (Sign Aspects): Each sign aspects specific signs based on its modality
"""

from astrovedic import const
from astrovedic import angle


def get_house_distance(from_lon, to_lon):
    """
    Calculate the distance in houses (1-12) between two longitudes
    
    Args:
        from_lon (float): The longitude of the starting point
        to_lon (float): The longitude of the ending point
    
    Returns:
        int: The distance in houses (1-12)
    """
    # Calculate the distance in houses (1-12)
    # Add 1 because houses are 1-based
    return (int(angle.distance(from_lon, to_lon) / 30) % 12) + 1


def has_graha_drishti(planet_id, from_lon, to_lon):
    """
    Check if a planet aspects a point according to Vedic rules
    
    Args:
        planet_id (str): The ID of the planet casting the aspect
        from_lon (float): The longitude of the planet casting the aspect
        to_lon (float): The longitude of the point receiving the aspect
    
    Returns:
        bool: True if the planet aspects the point, False otherwise
    """
    # Calculate the distance in houses (1-12)
    house_distance = get_house_distance(from_lon, to_lon)
    
    # All planets aspect the 7th house
    if house_distance == 7:
        return True
    
    # Special aspects for Mars, Jupiter, and Saturn
    if planet_id == const.MARS and house_distance in [4, 8]:
        return True
    elif planet_id == const.JUPITER and house_distance in [5, 9]:
        return True
    elif planet_id == const.SATURN and house_distance in [3, 10]:
        return True
    
    # No aspect
    return False


def get_graha_drishti_strength(planet_id, from_lon, to_lon):
    """
    Calculate the strength of a Vedic aspect
    
    Args:
        planet_id (str): The ID of the planet casting the aspect
        from_lon (float): The longitude of the planet casting the aspect
        to_lon (float): The longitude of the point receiving the aspect
    
    Returns:
        dict: Dictionary with aspect information
    """
    # Calculate the distance in houses (1-12)
    house_distance = get_house_distance(from_lon, to_lon)
    
    # Initialize aspect information
    aspect_info = {
        'has_aspect': False,
        'strength': 0.0,
        'type': None,
        'house_distance': house_distance
    }
    
    # All planets aspect the 7th house with full strength
    if house_distance == 7:
        aspect_info['has_aspect'] = True
        aspect_info['strength'] = 1.0
        aspect_info['type'] = const.VEDIC_FULL_ASPECT
        return aspect_info
    
    # Special aspects for Mars
    if planet_id == const.MARS:
        if house_distance == 4:
            aspect_info['has_aspect'] = True
            aspect_info['strength'] = 0.75
            aspect_info['type'] = const.VEDIC_THREE_QUARTER_ASPECT
            return aspect_info
        elif house_distance == 8:
            aspect_info['has_aspect'] = True
            aspect_info['strength'] = 1.0
            aspect_info['type'] = const.VEDIC_FULL_ASPECT
            return aspect_info
    
    # Special aspects for Jupiter
    elif planet_id == const.JUPITER:
        if house_distance == 5:
            aspect_info['has_aspect'] = True
            aspect_info['strength'] = 1.0
            aspect_info['type'] = const.VEDIC_FULL_ASPECT
            return aspect_info
        elif house_distance == 9:
            aspect_info['has_aspect'] = True
            aspect_info['strength'] = 0.75
            aspect_info['type'] = const.VEDIC_THREE_QUARTER_ASPECT
            return aspect_info
    
    # Special aspects for Saturn
    elif planet_id == const.SATURN:
        if house_distance == 3:
            aspect_info['has_aspect'] = True
            aspect_info['strength'] = 0.75
            aspect_info['type'] = const.VEDIC_THREE_QUARTER_ASPECT
            return aspect_info
        elif house_distance == 10:
            aspect_info['has_aspect'] = True
            aspect_info['strength'] = 1.0
            aspect_info['type'] = const.VEDIC_FULL_ASPECT
            return aspect_info
    
    # No aspect
    return aspect_info


def get_sign_modality(sign):
    """
    Get the modality of a sign
    
    Args:
        sign (str): The sign name
    
    Returns:
        str: The modality (Cardinal, Fixed, or Mutable)
    """
    # Movable (Cardinal) signs
    if sign in [const.ARIES, const.CANCER, const.LIBRA, const.CAPRICORN]:
        return const.CARDINAL
    
    # Fixed signs
    elif sign in [const.TAURUS, const.LEO, const.SCORPIO, const.AQUARIUS]:
        return const.FIXED
    
    # Dual (Mutable) signs
    else:
        return const.MUTABLE


def has_rashi_drishti(from_sign, to_sign):
    """
    Check if a sign aspects another sign according to Vedic rules
    
    Args:
        from_sign (str): The sign casting the aspect
        to_sign (str): The sign receiving the aspect
    
    Returns:
        bool: True if the sign aspects the other sign, False otherwise
    """
    # Get the indices of the signs
    from_index = const.LIST_SIGNS.index(from_sign)
    to_index = const.LIST_SIGNS.index(to_sign)
    
    # Calculate the distance in signs (1-12)
    sign_distance = ((to_index - from_index) % 12) + 1
    
    # All signs aspect the 7th sign
    if sign_distance == 7:
        return True
    
    # Get the modality of the sign
    modality = get_sign_modality(from_sign)
    
    # Special aspects based on modality
    if modality == const.CARDINAL and sign_distance in [4, 10]:
        return True
    elif modality == const.FIXED and sign_distance in [5, 9]:
        return True
    elif modality == const.MUTABLE and sign_distance in [3, 11]:
        return True
    
    # No aspect
    return False


def get_rashi_drishti_strength(from_sign, to_sign):
    """
    Calculate the strength of a Rashi Drishti (sign aspect)
    
    Args:
        from_sign (str): The sign casting the aspect
        to_sign (str): The sign receiving the aspect
    
    Returns:
        dict: Dictionary with aspect information
    """
    # Get the indices of the signs
    from_index = const.LIST_SIGNS.index(from_sign)
    to_index = const.LIST_SIGNS.index(to_sign)
    
    # Calculate the distance in signs (1-12)
    sign_distance = ((to_index - from_index) % 12) + 1
    
    # Initialize aspect information
    aspect_info = {
        'has_aspect': False,
        'strength': 0.0,
        'type': None,
        'sign_distance': sign_distance
    }
    
    # All signs aspect the 7th sign with full strength
    if sign_distance == 7:
        aspect_info['has_aspect'] = True
        aspect_info['strength'] = 1.0
        aspect_info['type'] = const.VEDIC_FULL_ASPECT
        return aspect_info
    
    # Get the modality of the sign
    modality = get_sign_modality(from_sign)
    
    # Special aspects for Cardinal signs
    if modality == const.CARDINAL:
        if sign_distance == 4:
            aspect_info['has_aspect'] = True
            aspect_info['strength'] = 0.75
            aspect_info['type'] = const.VEDIC_THREE_QUARTER_ASPECT
            return aspect_info
        elif sign_distance == 10:
            aspect_info['has_aspect'] = True
            aspect_info['strength'] = 1.0
            aspect_info['type'] = const.VEDIC_FULL_ASPECT
            return aspect_info
    
    # Special aspects for Fixed signs
    elif modality == const.FIXED:
        if sign_distance == 5:
            aspect_info['has_aspect'] = True
            aspect_info['strength'] = 1.0
            aspect_info['type'] = const.VEDIC_FULL_ASPECT
            return aspect_info
        elif sign_distance == 9:
            aspect_info['has_aspect'] = True
            aspect_info['strength'] = 0.75
            aspect_info['type'] = const.VEDIC_THREE_QUARTER_ASPECT
            return aspect_info
    
    # Special aspects for Mutable signs
    elif modality == const.MUTABLE:
        if sign_distance == 3:
            aspect_info['has_aspect'] = True
            aspect_info['strength'] = 0.75
            aspect_info['type'] = const.VEDIC_THREE_QUARTER_ASPECT
            return aspect_info
        elif sign_distance == 11:
            aspect_info['has_aspect'] = True
            aspect_info['strength'] = 1.0
            aspect_info['type'] = const.VEDIC_FULL_ASPECT
            return aspect_info
    
    # No aspect
    return aspect_info


def get_planet_aspects(chart, planet_id):
    """
    Get all aspects cast by a planet in a chart
    
    Args:
        chart (Chart): The chart
        planet_id (str): The ID of the planet
    
    Returns:
        list: List of aspects cast by the planet
    """
    # Get the planet
    planet = chart.getObject(planet_id)
    
    # Initialize the list of aspects
    aspects = []
    
    # Check aspects to each planet
    for other_id in const.LIST_OBJECTS_VEDIC:
        if other_id != planet_id:
            other = chart.getObject(other_id)
            
            # Calculate the aspect strength
            aspect_info = get_graha_drishti_strength(planet_id, planet.lon, other.lon)
            
            if aspect_info['has_aspect']:
                # Add to the list of aspects
                aspects.append({
                    'from_planet': planet_id,
                    'to_planet': other_id,
                    'strength': aspect_info['strength'],
                    'type': aspect_info['type'],
                    'house_distance': aspect_info['house_distance']
                })
    
    return aspects


def get_planet_aspects_received(chart, planet_id):
    """
    Get all aspects received by a planet in a chart
    
    Args:
        chart (Chart): The chart
        planet_id (str): The ID of the planet
    
    Returns:
        list: List of aspects received by the planet
    """
    # Get the planet
    planet = chart.getObject(planet_id)
    
    # Initialize the list of aspects
    aspects = []
    
    # Check aspects from each planet
    for other_id in const.LIST_OBJECTS_VEDIC:
        if other_id != planet_id:
            other = chart.getObject(other_id)
            
            # Calculate the aspect strength
            aspect_info = get_graha_drishti_strength(other_id, other.lon, planet.lon)
            
            if aspect_info['has_aspect']:
                # Add to the list of aspects
                aspects.append({
                    'from_planet': other_id,
                    'to_planet': planet_id,
                    'strength': aspect_info['strength'],
                    'type': aspect_info['type'],
                    'house_distance': aspect_info['house_distance']
                })
    
    return aspects


def get_sign_aspects(sign):
    """
    Get all aspects cast by a sign
    
    Args:
        sign (str): The sign
    
    Returns:
        list: List of aspects cast by the sign
    """
    # Initialize the list of aspects
    aspects = []
    
    # Check aspects to each sign
    for other_sign in const.LIST_SIGNS:
        # Calculate the aspect strength
        aspect_info = get_rashi_drishti_strength(sign, other_sign)
        
        if aspect_info['has_aspect']:
            # Add to the list of aspects
            aspects.append({
                'from_sign': sign,
                'to_sign': other_sign,
                'strength': aspect_info['strength'],
                'type': aspect_info['type'],
                'sign_distance': aspect_info['sign_distance']
            })
    
    return aspects


def get_sign_aspects_received(sign):
    """
    Get all aspects received by a sign
    
    Args:
        sign (str): The sign
    
    Returns:
        list: List of aspects received by the sign
    """
    # Initialize the list of aspects
    aspects = []
    
    # Check aspects from each sign
    for other_sign in const.LIST_SIGNS:
        # Calculate the aspect strength
        aspect_info = get_rashi_drishti_strength(other_sign, sign)
        
        if aspect_info['has_aspect']:
            # Add to the list of aspects
            aspects.append({
                'from_sign': other_sign,
                'to_sign': sign,
                'strength': aspect_info['strength'],
                'type': aspect_info['type'],
                'sign_distance': aspect_info['sign_distance']
            })
    
    return aspects


def get_all_aspects(chart):
    """
    Get all Vedic aspects in a chart
    
    Args:
        chart (Chart): The chart
    
    Returns:
        dict: Dictionary with all aspects
    """
    # Initialize the result
    result = {
        'planet_aspects': {},
        'sign_aspects': {}
    }
    
    # Get aspects for each planet
    for planet_id in const.LIST_OBJECTS_VEDIC:
        result['planet_aspects'][planet_id] = {
            'aspects_cast': get_planet_aspects(chart, planet_id),
            'aspects_received': get_planet_aspects_received(chart, planet_id)
        }
    
    # Get aspects for each sign
    for sign in const.LIST_SIGNS:
        result['sign_aspects'][sign] = {
            'aspects_cast': get_sign_aspects(sign),
            'aspects_received': get_sign_aspects_received(sign)
        }
    
    return result
