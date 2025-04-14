"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Chandra Yogas (Moon combinations)
    for Vedic astrology.
"""

from flatlib import const
from flatlib.vedic.yogas.core import (
    get_house_number, are_planets_conjunct,
    get_yoga_strength
)


def get_chandra_yogas(chart):
    """
    Identify Chandra Yogas in a chart
    
    Chandra Yogas are planetary combinations involving the Moon that indicate
    various aspects of personality and life experiences.
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        list: List of Chandra Yogas in the chart
    """
    # Initialize the result
    result = []
    
    # Check for Adhi Yoga
    adhi = has_adhi_yoga(chart)
    if adhi:
        result.append(adhi)
    
    # Check for Sunapha Yoga
    sunapha = has_sunapha_yoga(chart)
    if sunapha:
        result.append(sunapha)
    
    # Check for Anapha Yoga
    anapha = has_anapha_yoga(chart)
    if anapha:
        result.append(anapha)
    
    # Check for Durudhura Yoga
    durudhura = has_durudhura_yoga(chart)
    if durudhura:
        result.append(durudhura)
    
    # Check for Kemadruma Yoga
    kemadruma = has_kemadruma_yoga(chart)
    if kemadruma:
        result.append(kemadruma)
    
    return result


def has_adhi_yoga(chart):
    """
    Check if a chart has Adhi Yoga
    
    Adhi Yoga is formed when Mercury, Venus, and Jupiter are in the 6th, 7th,
    and 8th houses from the Moon.
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Adhi Yoga information, or None if not present
    """
    # Get the Moon
    moon = chart.getObject(const.MOON)
    
    # Get the house number of the Moon
    moon_house = get_house_number(chart, const.MOON)
    
    # Calculate the 6th, 7th, and 8th houses from the Moon
    house_6_from_moon = (moon_house + 5) % 12 or 12
    house_7_from_moon = (moon_house + 6) % 12 or 12
    house_8_from_moon = (moon_house + 7) % 12 or 12
    
    # Check if Mercury, Venus, and Jupiter are in the 6th, 7th, and 8th houses from the Moon
    mercury_house = get_house_number(chart, const.MERCURY)
    venus_house = get_house_number(chart, const.VENUS)
    jupiter_house = get_house_number(chart, const.JUPITER)
    
    is_in_6_7_8 = (
        mercury_house in [house_6_from_moon, house_7_from_moon, house_8_from_moon] and
        venus_house in [house_6_from_moon, house_7_from_moon, house_8_from_moon] and
        jupiter_house in [house_6_from_moon, house_7_from_moon, house_8_from_moon]
    )
    
    # Check if Adhi Yoga is formed
    if is_in_6_7_8:
        # Create the Yoga information
        yoga = {
            'name': 'Adhi Yoga',
            'type': 'Chandra Yoga',
            'planets': [const.MOON, const.MERCURY, const.VENUS, const.JUPITER],
            'houses': [moon_house, mercury_house, venus_house, jupiter_house],
            'description': 'Formed when Mercury, Venus, and Jupiter are in the 6th, 7th, and 8th houses from the Moon',
            'is_beneficial': True
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    return None


def has_sunapha_yoga(chart):
    """
    Check if a chart has Sunapha Yoga
    
    Sunapha Yoga is formed when there is a planet (other than the Sun) in the
    2nd house from the Moon.
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Sunapha Yoga information, or None if not present
    """
    # Get the Moon
    moon = chart.getObject(const.MOON)
    
    # Get the house number of the Moon
    moon_house = get_house_number(chart, const.MOON)
    
    # Calculate the 2nd house from the Moon
    house_2_from_moon = (moon_house + 1) % 12 or 12
    
    # Check if there is a planet (other than the Sun) in the 2nd house from the Moon
    planet_in_2nd = None
    for planet_id in [const.MERCURY, const.VENUS, const.MARS, const.JUPITER, const.SATURN]:
        planet_house = get_house_number(chart, planet_id)
        if planet_house == house_2_from_moon:
            planet_in_2nd = planet_id
            break
    
    # Check if Sunapha Yoga is formed
    if planet_in_2nd:
        # Create the Yoga information
        yoga = {
            'name': 'Sunapha Yoga',
            'type': 'Chandra Yoga',
            'planets': [const.MOON, planet_in_2nd],
            'houses': [moon_house, house_2_from_moon],
            'description': f'Formed when {planet_in_2nd} is in the 2nd house from the Moon',
            'is_beneficial': True
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    return None


def has_anapha_yoga(chart):
    """
    Check if a chart has Anapha Yoga
    
    Anapha Yoga is formed when there is a planet (other than the Sun) in the
    12th house from the Moon.
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Anapha Yoga information, or None if not present
    """
    # Get the Moon
    moon = chart.getObject(const.MOON)
    
    # Get the house number of the Moon
    moon_house = get_house_number(chart, const.MOON)
    
    # Calculate the 12th house from the Moon
    house_12_from_moon = (moon_house - 1) % 12 or 12
    
    # Check if there is a planet (other than the Sun) in the 12th house from the Moon
    planet_in_12th = None
    for planet_id in [const.MERCURY, const.VENUS, const.MARS, const.JUPITER, const.SATURN]:
        planet_house = get_house_number(chart, planet_id)
        if planet_house == house_12_from_moon:
            planet_in_12th = planet_id
            break
    
    # Check if Anapha Yoga is formed
    if planet_in_12th:
        # Create the Yoga information
        yoga = {
            'name': 'Anapha Yoga',
            'type': 'Chandra Yoga',
            'planets': [const.MOON, planet_in_12th],
            'houses': [moon_house, house_12_from_moon],
            'description': f'Formed when {planet_in_12th} is in the 12th house from the Moon',
            'is_beneficial': True
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    return None


def has_durudhura_yoga(chart):
    """
    Check if a chart has Durudhura Yoga
    
    Durudhura Yoga is formed when there are planets (other than the Sun) in
    both the 2nd and 12th houses from the Moon.
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Durudhura Yoga information, or None if not present
    """
    # Get the Moon
    moon = chart.getObject(const.MOON)
    
    # Get the house number of the Moon
    moon_house = get_house_number(chart, const.MOON)
    
    # Calculate the 2nd and 12th houses from the Moon
    house_2_from_moon = (moon_house + 1) % 12 or 12
    house_12_from_moon = (moon_house - 1) % 12 or 12
    
    # Check if there is a planet (other than the Sun) in the 2nd house from the Moon
    planet_in_2nd = None
    for planet_id in [const.MERCURY, const.VENUS, const.MARS, const.JUPITER, const.SATURN]:
        planet_house = get_house_number(chart, planet_id)
        if planet_house == house_2_from_moon:
            planet_in_2nd = planet_id
            break
    
    # Check if there is a planet (other than the Sun) in the 12th house from the Moon
    planet_in_12th = None
    for planet_id in [const.MERCURY, const.VENUS, const.MARS, const.JUPITER, const.SATURN]:
        if planet_id == planet_in_2nd:
            continue  # Skip the planet already found in the 2nd house
        
        planet_house = get_house_number(chart, planet_id)
        if planet_house == house_12_from_moon:
            planet_in_12th = planet_id
            break
    
    # Check if Durudhura Yoga is formed
    if planet_in_2nd and planet_in_12th:
        # Create the Yoga information
        yoga = {
            'name': 'Durudhura Yoga',
            'type': 'Chandra Yoga',
            'planets': [const.MOON, planet_in_2nd, planet_in_12th],
            'houses': [moon_house, house_2_from_moon, house_12_from_moon],
            'description': f'Formed when {planet_in_2nd} is in the 2nd house and {planet_in_12th} is in the 12th house from the Moon',
            'is_beneficial': True
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    return None


def has_kemadruma_yoga(chart):
    """
    Check if a chart has Kemadruma Yoga
    
    Kemadruma Yoga is formed when there are no planets in the 2nd and 12th
    houses from the Moon, and the Moon is not conjunct with any planet.
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Kemadruma Yoga information, or None if not present
    """
    # Get the Moon
    moon = chart.getObject(const.MOON)
    
    # Get the house number of the Moon
    moon_house = get_house_number(chart, const.MOON)
    
    # Calculate the 2nd and 12th houses from the Moon
    house_2_from_moon = (moon_house + 1) % 12 or 12
    house_12_from_moon = (moon_house - 1) % 12 or 12
    
    # Check if there are planets in the 2nd and 12th houses from the Moon
    planets_in_2_12 = False
    for planet_id in [const.SUN, const.MERCURY, const.VENUS, const.MARS, const.JUPITER, const.SATURN]:
        planet_house = get_house_number(chart, planet_id)
        if planet_house == house_2_from_moon or planet_house == house_12_from_moon:
            planets_in_2_12 = True
            break
    
    # Check if the Moon is conjunct with any planet
    moon_conjunct = False
    for planet_id in [const.SUN, const.MERCURY, const.VENUS, const.MARS, const.JUPITER, const.SATURN]:
        if are_planets_conjunct(chart, const.MOON, planet_id):
            moon_conjunct = True
            break
    
    # Check if Kemadruma Yoga is formed
    if not planets_in_2_12 and not moon_conjunct:
        # Create the Yoga information
        yoga = {
            'name': 'Kemadruma Yoga',
            'type': 'Chandra Yoga',
            'planets': [const.MOON],
            'houses': [moon_house],
            'description': 'Formed when there are no planets in the 2nd and 12th houses from the Moon, and the Moon is not conjunct with any planet',
            'is_beneficial': False
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    return None
