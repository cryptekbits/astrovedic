"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Drig Bala (aspectual strength) calculations
    for Shadbala in Vedic astrology.
"""

from flatlib import const
from flatlib import angle


def calculate_drig_bala(chart, planet_id):
    """
    Calculate Drig Bala (aspectual strength) for a planet
    
    Drig Bala is based on the aspects received by and cast by a planet.
    Benefic aspects increase strength, while malefic aspects decrease it.
    
    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet to analyze
    
    Returns:
        dict: Dictionary with Drig Bala information
    """
    # Get the planet from the chart
    planet = chart.getObject(planet_id)
    
    # Maximum value (in Virupas)
    max_value = 60.0
    
    # Calculate the aspects received by the planet
    aspects_received = calculate_aspects_received(chart, planet_id)
    
    # Calculate the aspects cast by the planet
    aspects_cast = calculate_aspects_cast(chart, planet_id)
    
    # Calculate the net Drig Bala
    net_value = aspects_received['value'] - aspects_cast['value']
    
    # Ensure the value is within the range [0, max_value]
    value = max(0.0, min(net_value, max_value))
    
    # Determine the description
    if value >= 45.0:
        description = 'Very strong aspectual strength'
    elif value >= 30.0:
        description = 'Strong aspectual strength'
    elif value >= 15.0:
        description = 'Moderate aspectual strength'
    else:
        description = 'Weak aspectual strength'
    
    return {
        'value': value,
        'description': description,
        'aspects_received': aspects_received,
        'aspects_cast': aspects_cast
    }


def calculate_aspects_received(chart, planet_id):
    """
    Calculate the aspects received by a planet
    
    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet
    
    Returns:
        dict: Dictionary with aspect information
    """
    # Get the planet from the chart
    planet = chart.getObject(planet_id)
    
    # Initialize the aspect value
    aspect_value = 0.0
    
    # List of aspects received
    aspects = []
    
    # Check aspects from each planet
    for other_id in const.LIST_OBJECTS_VEDIC:
        if other_id != planet_id:
            other = chart.getObject(other_id)
            
            # Calculate the aspect strength
            aspect_strength = calculate_vedic_aspect_strength(other_id, other.lon, planet.lon)
            
            if aspect_strength > 0:
                # Determine if the aspect is benefic or malefic
                is_benefic = is_benefic_planet(other_id)
                
                # Benefic aspects increase strength, malefic aspects decrease it
                if is_benefic:
                    aspect_value += aspect_strength
                else:
                    aspect_value -= aspect_strength
                
                # Add to the list of aspects
                aspects.append({
                    'planet': other_id,
                    'strength': aspect_strength,
                    'is_benefic': is_benefic
                })
    
    return {
        'value': aspect_value,
        'aspects': aspects
    }


def calculate_aspects_cast(chart, planet_id):
    """
    Calculate the aspects cast by a planet
    
    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet
    
    Returns:
        dict: Dictionary with aspect information
    """
    # Get the planet from the chart
    planet = chart.getObject(planet_id)
    
    # Initialize the aspect value
    aspect_value = 0.0
    
    # List of aspects cast
    aspects = []
    
    # Check aspects to each planet
    for other_id in const.LIST_OBJECTS_VEDIC:
        if other_id != planet_id:
            other = chart.getObject(other_id)
            
            # Calculate the aspect strength
            aspect_strength = calculate_vedic_aspect_strength(planet_id, planet.lon, other.lon)
            
            if aspect_strength > 0:
                # Determine if the aspect is benefic or malefic
                is_benefic = is_benefic_planet(planet_id)
                
                # Benefic aspects increase strength, malefic aspects decrease it
                if is_benefic:
                    aspect_value += aspect_strength
                else:
                    aspect_value -= aspect_strength
                
                # Add to the list of aspects
                aspects.append({
                    'planet': other_id,
                    'strength': aspect_strength,
                    'is_benefic': is_benefic
                })
    
    return {
        'value': aspect_value,
        'aspects': aspects
    }


def calculate_vedic_aspect_strength(planet_id, from_lon, to_lon):
    """
    Calculate the strength of a Vedic aspect
    
    In Vedic astrology, planets aspect:
    - All planets aspect the 7th house from their position
    - Mars also aspects the 4th and 8th houses
    - Jupiter also aspects the 5th and 9th houses
    - Saturn also aspects the 3rd and 10th houses
    
    Args:
        planet_id (str): The ID of the planet casting the aspect
        from_lon (float): The longitude of the planet casting the aspect
        to_lon (float): The longitude of the planet receiving the aspect
    
    Returns:
        float: The strength of the aspect (0-10)
    """
    # Calculate the distance in houses (0-11)
    distance = int(angle.distance(from_lon, to_lon) / 30) % 12
    
    # All planets aspect the 7th house
    if distance == 6:
        return 10.0
    
    # Special aspects for Mars, Jupiter, and Saturn
    if planet_id == const.MARS and distance in [3, 7]:
        return 10.0
    elif planet_id == const.JUPITER and distance in [4, 8]:
        return 10.0
    elif planet_id == const.SATURN and distance in [2, 9]:
        return 10.0
    
    # No aspect
    return 0.0


def is_benefic_planet(planet_id):
    """
    Determine if a planet is benefic or malefic
    
    Args:
        planet_id (str): The ID of the planet
    
    Returns:
        bool: True if the planet is benefic, False if malefic
    """
    # Benefic planets
    benefic_planets = [const.JUPITER, const.VENUS, const.MERCURY, const.MOON]
    
    # Malefic planets
    malefic_planets = [const.SUN, const.MARS, const.SATURN, const.RAHU, const.KETU]
    
    return planet_id in benefic_planets
