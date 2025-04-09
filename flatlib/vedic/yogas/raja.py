"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Raja Yogas (combinations for power and authority)
    for Vedic astrology.
"""

from flatlib import const
from flatlib.vedic.yogas.core import (
    get_house_lord, get_house_number, are_planets_conjunct,
    are_planets_in_aspect, get_yoga_strength
)


def get_raja_yogas(chart):
    """
    Identify Raja Yogas in a chart
    
    Raja Yogas are planetary combinations that indicate power, authority,
    and success in life.
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        list: List of Raja Yogas in the chart
    """
    # Initialize the result
    result = []
    
    # Check for Dharmakarmaadhipati Yoga
    dharmakarmaadhipati = has_dharmakarmaadhipati_yoga(chart)
    if dharmakarmaadhipati:
        result.append(dharmakarmaadhipati)
    
    # Check for Gajakesari Yoga
    gajakesari = has_gajakesari_yoga(chart)
    if gajakesari:
        result.append(gajakesari)
    
    # Check for Amala Yoga
    amala = has_amala_yoga(chart)
    if amala:
        result.append(amala)
    
    # Check for Sreenatha Yoga
    sreenatha = has_sreenatha_yoga(chart)
    if sreenatha:
        result.append(sreenatha)
    
    # Check for Chandra Mangala Yoga
    chandra_mangala = has_chandra_mangala_yoga(chart)
    if chandra_mangala:
        result.append(chandra_mangala)
    
    return result


def has_dharmakarmaadhipati_yoga(chart):
    """
    Check if a chart has Dharmakarmaadhipati Yoga
    
    Dharmakarmaadhipati Yoga is formed when the lords of the 9th and 10th
    houses are conjunct or aspect each other.
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Dharmakarmaadhipati Yoga information, or None if not present
    """
    # Get the lords of the 9th and 10th houses
    lord_9 = get_house_lord(chart, 9)
    lord_10 = get_house_lord(chart, 10)
    
    # Check if the lords are the same planet
    if lord_9 == lord_10:
        # Create the Yoga information
        yoga = {
            'name': 'Dharmakarmaadhipati Yoga',
            'type': 'Raja Yoga',
            'planets': [lord_9],
            'houses': [9, 10],
            'description': 'Formed when the same planet is the lord of both the 9th and 10th houses',
            'is_beneficial': True
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    # Check if the lords are conjunct
    if are_planets_conjunct(chart, lord_9, lord_10):
        # Create the Yoga information
        yoga = {
            'name': 'Dharmakarmaadhipati Yoga',
            'type': 'Raja Yoga',
            'planets': [lord_9, lord_10],
            'houses': [9, 10],
            'description': 'Formed when the lords of the 9th and 10th houses are conjunct',
            'is_beneficial': True
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    # Check if the lords aspect each other
    if are_planets_in_aspect(chart, lord_9, lord_10):
        # Create the Yoga information
        yoga = {
            'name': 'Dharmakarmaadhipati Yoga',
            'type': 'Raja Yoga',
            'planets': [lord_9, lord_10],
            'houses': [9, 10],
            'description': 'Formed when the lords of the 9th and 10th houses aspect each other',
            'is_beneficial': True
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    return None


def has_gajakesari_yoga(chart):
    """
    Check if a chart has Gajakesari Yoga
    
    Gajakesari Yoga is formed when Jupiter is in a Kendra house (1, 4, 7, or 10)
    from the Moon.
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Gajakesari Yoga information, or None if not present
    """
    # Get the Moon and Jupiter from the chart
    moon = chart.getObject(const.MOON)
    jupiter = chart.getObject(const.JUPITER)
    
    # Get the house number of the Moon
    moon_house = get_house_number(chart, const.MOON)
    
    # Get the house number of Jupiter
    jupiter_house = get_house_number(chart, const.JUPITER)
    
    # Check if Jupiter is in a Kendra house from the Moon
    is_in_kendra = (jupiter_house - moon_house) % 12 in [0, 3, 6, 9]
    
    # Check if Gajakesari Yoga is formed
    if is_in_kendra:
        # Create the Yoga information
        yoga = {
            'name': 'Gajakesari Yoga',
            'type': 'Raja Yoga',
            'planets': [const.MOON, const.JUPITER],
            'houses': [moon_house, jupiter_house],
            'description': 'Formed when Jupiter is in a Kendra house from the Moon',
            'is_beneficial': True
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    return None


def has_amala_yoga(chart):
    """
    Check if a chart has Amala Yoga
    
    Amala Yoga is formed when there are no malefic planets in the 10th house
    from the Moon or the Ascendant.
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Amala Yoga information, or None if not present
    """
    # Get the Ascendant
    asc = chart.getAngle(const.ASC)
    
    # Get the Moon
    moon = chart.getObject(const.MOON)
    
    # Get the 10th house from the Ascendant
    asc_10th_house = (get_house_number(chart, const.ASC) + 9) % 12 or 12
    
    # Get the 10th house from the Moon
    moon_10th_house = (get_house_number(chart, const.MOON) + 9) % 12 or 12
    
    # Check if there are malefic planets in the 10th house from the Ascendant
    malefics_in_asc_10th = False
    for planet_id in [const.SUN, const.MARS, const.SATURN, const.RAHU, const.KETU]:
        planet_house = get_house_number(chart, planet_id)
        if planet_house == asc_10th_house:
            malefics_in_asc_10th = True
            break
    
    # Check if there are malefic planets in the 10th house from the Moon
    malefics_in_moon_10th = False
    for planet_id in [const.SUN, const.MARS, const.SATURN, const.RAHU, const.KETU]:
        planet_house = get_house_number(chart, planet_id)
        if planet_house == moon_10th_house:
            malefics_in_moon_10th = True
            break
    
    # Check if Amala Yoga is formed
    if not malefics_in_asc_10th or not malefics_in_moon_10th:
        # Create the Yoga information
        yoga = {
            'name': 'Amala Yoga',
            'type': 'Raja Yoga',
            'planets': [],
            'houses': [asc_10th_house, moon_10th_house],
            'description': 'Formed when there are no malefic planets in the 10th house from the Moon or the Ascendant',
            'is_beneficial': True
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = 75.0  # Fixed strength since there are no planets involved
        
        return yoga
    
    return None


def has_sreenatha_yoga(chart):
    """
    Check if a chart has Sreenatha Yoga
    
    Sreenatha Yoga is formed when Venus is in the 9th house and the lord of
    the 9th house is in a Kendra house (1, 4, 7, or 10).
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Sreenatha Yoga information, or None if not present
    """
    # Get Venus from the chart
    venus = chart.getObject(const.VENUS)
    
    # Get the house number of Venus
    venus_house = get_house_number(chart, const.VENUS)
    
    # Check if Venus is in the 9th house
    is_venus_in_9th = venus_house == 9
    
    # Get the lord of the 9th house
    lord_9 = get_house_lord(chart, 9)
    
    # Get the house number of the 9th lord
    lord_9_house = get_house_number(chart, lord_9)
    
    # Check if the 9th lord is in a Kendra house
    is_lord_in_kendra = lord_9_house in [1, 4, 7, 10]
    
    # Check if Sreenatha Yoga is formed
    if is_venus_in_9th and is_lord_in_kendra:
        # Create the Yoga information
        yoga = {
            'name': 'Sreenatha Yoga',
            'type': 'Raja Yoga',
            'planets': [const.VENUS, lord_9],
            'houses': [9, lord_9_house],
            'description': 'Formed when Venus is in the 9th house and the lord of the 9th house is in a Kendra house',
            'is_beneficial': True
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    return None


def has_chandra_mangala_yoga(chart):
    """
    Check if a chart has Chandra Mangala Yoga
    
    Chandra Mangala Yoga is formed when the Moon and Mars are conjunct or
    aspect each other.
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Chandra Mangala Yoga information, or None if not present
    """
    # Check if the Moon and Mars are conjunct
    if are_planets_conjunct(chart, const.MOON, const.MARS):
        # Create the Yoga information
        yoga = {
            'name': 'Chandra Mangala Yoga',
            'type': 'Raja Yoga',
            'planets': [const.MOON, const.MARS],
            'houses': [get_house_number(chart, const.MOON), get_house_number(chart, const.MARS)],
            'description': 'Formed when the Moon and Mars are conjunct',
            'is_beneficial': True
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    # Check if the Moon and Mars aspect each other
    if are_planets_in_aspect(chart, const.MOON, const.MARS):
        # Create the Yoga information
        yoga = {
            'name': 'Chandra Mangala Yoga',
            'type': 'Raja Yoga',
            'planets': [const.MOON, const.MARS],
            'houses': [get_house_number(chart, const.MOON), get_house_number(chart, const.MARS)],
            'description': 'Formed when the Moon and Mars aspect each other',
            'is_beneficial': True
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    return None
