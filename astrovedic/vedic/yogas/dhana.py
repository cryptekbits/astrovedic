"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Dhana Yogas (combinations for wealth)
    for Vedic astrology.
"""

from astrovedic import const
from astrovedic.vedic.yogas.core import (
    get_house_lord, get_house_number, are_planets_conjunct,
    are_planets_in_aspect, get_yoga_strength
)


def get_dhana_yogas(chart):
    """
    Identify Dhana Yogas in a chart
    
    Dhana Yogas are planetary combinations that indicate wealth, prosperity,
    and financial success.
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        list: List of Dhana Yogas in the chart
    """
    # Initialize the result
    result = []
    
    # Check for Lakshmi Yoga
    lakshmi = has_lakshmi_yoga(chart)
    if lakshmi:
        result.append(lakshmi)
    
    # Check for Kubera Yoga
    kubera = has_kubera_yoga(chart)
    if kubera:
        result.append(kubera)
    
    # Check for Kalanidhi Yoga
    kalanidhi = has_kalanidhi_yoga(chart)
    if kalanidhi:
        result.append(kalanidhi)
    
    # Check for Vasumati Yoga
    vasumati = has_vasumati_yoga(chart)
    if vasumati:
        result.append(vasumati)
    
    # Check for Mridanga Yoga
    mridanga = has_mridanga_yoga(chart)
    if mridanga:
        result.append(mridanga)
    
    return result


def has_lakshmi_yoga(chart):
    """
    Check if a chart has Lakshmi Yoga
    
    Lakshmi Yoga is formed when Venus is in the 9th house and Jupiter is in
    the Ascendant, or vice versa.
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Lakshmi Yoga information, or None if not present
    """
    # Get Venus and Jupiter from the chart
    venus = chart.getObject(const.VENUS)
    jupiter = chart.getObject(const.JUPITER)
    
    # Get the house numbers of Venus and Jupiter
    venus_house = get_house_number(chart, const.VENUS)
    jupiter_house = get_house_number(chart, const.JUPITER)
    
    # Check if Venus is in the 9th house and Jupiter is in the Ascendant
    condition1 = venus_house == 9 and jupiter_house == 1
    
    # Check if Jupiter is in the 9th house and Venus is in the Ascendant
    condition2 = jupiter_house == 9 and venus_house == 1
    
    # Check if Lakshmi Yoga is formed
    if condition1 or condition2:
        # Create the Yoga information
        yoga = {
            'name': 'Lakshmi Yoga',
            'type': 'Dhana Yoga',
            'planets': [const.VENUS, const.JUPITER],
            'houses': [venus_house, jupiter_house],
            'description': 'Formed when Venus is in the 9th house and Jupiter is in the Ascendant, or vice versa',
            'is_beneficial': True
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    return None


def has_kubera_yoga(chart):
    """
    Check if a chart has Kubera Yoga
    
    Kubera Yoga is formed when the lords of the 2nd and 11th houses are
    conjunct or aspect each other.
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Kubera Yoga information, or None if not present
    """
    # Get the lords of the 2nd and 11th houses
    lord_2 = get_house_lord(chart, 2)
    lord_11 = get_house_lord(chart, 11)
    
    # Check if the lords are the same planet
    if lord_2 == lord_11:
        # Create the Yoga information
        yoga = {
            'name': 'Kubera Yoga',
            'type': 'Dhana Yoga',
            'planets': [lord_2],
            'houses': [2, 11],
            'description': 'Formed when the same planet is the lord of both the 2nd and 11th houses',
            'is_beneficial': True
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    # Check if the lords are conjunct
    if are_planets_conjunct(chart, lord_2, lord_11):
        # Create the Yoga information
        yoga = {
            'name': 'Kubera Yoga',
            'type': 'Dhana Yoga',
            'planets': [lord_2, lord_11],
            'houses': [2, 11],
            'description': 'Formed when the lords of the 2nd and 11th houses are conjunct',
            'is_beneficial': True
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    # Check if the lords aspect each other
    if are_planets_in_aspect(chart, lord_2, lord_11):
        # Create the Yoga information
        yoga = {
            'name': 'Kubera Yoga',
            'type': 'Dhana Yoga',
            'planets': [lord_2, lord_11],
            'houses': [2, 11],
            'description': 'Formed when the lords of the 2nd and 11th houses aspect each other',
            'is_beneficial': True
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    return None


def has_kalanidhi_yoga(chart):
    """
    Check if a chart has Kalanidhi Yoga
    
    Kalanidhi Yoga is formed when the lord of the 2nd house is in the 5th house,
    or the lord of the 5th house is in the 2nd house.
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Kalanidhi Yoga information, or None if not present
    """
    # Get the lords of the 2nd and 5th houses
    lord_2 = get_house_lord(chart, 2)
    lord_5 = get_house_lord(chart, 5)
    
    # Get the house numbers of the lords
    lord_2_house = get_house_number(chart, lord_2)
    lord_5_house = get_house_number(chart, lord_5)
    
    # Check if the lord of the 2nd house is in the 5th house
    condition1 = lord_2_house == 5
    
    # Check if the lord of the 5th house is in the 2nd house
    condition2 = lord_5_house == 2
    
    # Check if Kalanidhi Yoga is formed
    if condition1 or condition2:
        # Create the Yoga information
        yoga = {
            'name': 'Kalanidhi Yoga',
            'type': 'Dhana Yoga',
            'planets': [lord_2, lord_5],
            'houses': [2, 5],
            'description': 'Formed when the lord of the 2nd house is in the 5th house, or the lord of the 5th house is in the 2nd house',
            'is_beneficial': True
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    return None


def has_vasumati_yoga(chart):
    """
    Check if a chart has Vasumati Yoga
    
    Vasumati Yoga is formed when the lord of the 2nd house is in the 11th house,
    or the lord of the 11th house is in the 2nd house.
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Vasumati Yoga information, or None if not present
    """
    # Get the lords of the 2nd and 11th houses
    lord_2 = get_house_lord(chart, 2)
    lord_11 = get_house_lord(chart, 11)
    
    # Get the house numbers of the lords
    lord_2_house = get_house_number(chart, lord_2)
    lord_11_house = get_house_number(chart, lord_11)
    
    # Check if the lord of the 2nd house is in the 11th house
    condition1 = lord_2_house == 11
    
    # Check if the lord of the 11th house is in the 2nd house
    condition2 = lord_11_house == 2
    
    # Check if Vasumati Yoga is formed
    if condition1 or condition2:
        # Create the Yoga information
        yoga = {
            'name': 'Vasumati Yoga',
            'type': 'Dhana Yoga',
            'planets': [lord_2, lord_11],
            'houses': [2, 11],
            'description': 'Formed when the lord of the 2nd house is in the 11th house, or the lord of the 11th house is in the 2nd house',
            'is_beneficial': True
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    return None


def has_mridanga_yoga(chart):
    """
    Check if a chart has Mridanga Yoga
    
    Mridanga Yoga is formed when the lords of the 1st, 4th, and 10th houses
    are in mutual angles (Kendra houses) from each other.
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Mridanga Yoga information, or None if not present
    """
    # Get the lords of the 1st, 4th, and 10th houses
    lord_1 = get_house_lord(chart, 1)
    lord_4 = get_house_lord(chart, 4)
    lord_10 = get_house_lord(chart, 10)
    
    # Get the house numbers of the lords
    lord_1_house = get_house_number(chart, lord_1)
    lord_4_house = get_house_number(chart, lord_4)
    lord_10_house = get_house_number(chart, lord_10)
    
    # Check if the lords are in mutual angles
    is_1_4_in_angle = (lord_1_house - lord_4_house) % 3 == 0
    is_1_10_in_angle = (lord_1_house - lord_10_house) % 3 == 0
    is_4_10_in_angle = (lord_4_house - lord_10_house) % 3 == 0
    
    # Check if Mridanga Yoga is formed
    if is_1_4_in_angle and is_1_10_in_angle and is_4_10_in_angle:
        # Create the Yoga information
        yoga = {
            'name': 'Mridanga Yoga',
            'type': 'Dhana Yoga',
            'planets': [lord_1, lord_4, lord_10],
            'houses': [1, 4, 10],
            'description': 'Formed when the lords of the 1st, 4th, and 10th houses are in mutual angles from each other',
            'is_beneficial': True
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    return None
