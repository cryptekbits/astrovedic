"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Kaksha Bala (zodiacal strength) calculations
    for Vedic astrology.
"""

from flatlib import const
from flatlib.vedic.ashtakavarga.bhinna import get_benefic_points
from flatlib.vedic.ashtakavarga.core import get_sign_number


def calculate_kaksha_bala(chart, planet_id):
    """
    Calculate Kaksha Bala (zodiacal strength) for a planet
    
    Kaksha Bala is the strength of a planet based on its position in the
    Ashtakavarga of other planets.
    
    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet to analyze
    
    Returns:
        dict: Dictionary with Kaksha Bala information
    """
    # Get the planet from the chart
    planet = chart.getObject(planet_id)
    
    # Get the sign number (0-11)
    sign_num = get_sign_number(planet.sign)
    
    # List of planets used in Ashtakavarga
    planets = [const.SUN, const.MOON, const.MARS, const.MERCURY,
              const.JUPITER, const.VENUS, const.SATURN]
    
    # Initialize the result
    result = {
        'planet': planet_id,
        'sign': planet.sign,
        'kaksha_bala': 0,
        'contributions': {}
    }
    
    # Calculate the contribution from each planet's Ashtakavarga
    for contributor_id in planets:
        # Skip the planet itself
        if contributor_id == planet_id:
            continue
        
        # Get the benefic points
        benefic_points = get_benefic_points(chart, contributor_id)
        
        # Get the contribution at the planet's sign
        contribution = benefic_points[sign_num]
        
        # Add to the total
        result['kaksha_bala'] += contribution
        
        # Add to the contributions
        result['contributions'][contributor_id] = contribution
    
    # Calculate the percentage of maximum possible Kaksha Bala (42)
    result['percentage'] = (result['kaksha_bala'] / 42.0) * 100.0
    
    # Determine the strength category
    if result['percentage'] >= 75.0:
        result['category'] = 'Very Strong'
    elif result['percentage'] >= 50.0:
        result['category'] = 'Strong'
    elif result['percentage'] >= 25.0:
        result['category'] = 'Moderate'
    else:
        result['category'] = 'Weak'
    
    return result


def get_kaksha_strengths(chart):
    """
    Calculate Kaksha Bala for all planets
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Kaksha Bala information for all planets
    """
    # List of planets used in Ashtakavarga
    planets = [const.SUN, const.MOON, const.MARS, const.MERCURY,
              const.JUPITER, const.VENUS, const.SATURN]
    
    # Initialize the result
    result = {}
    
    # Calculate Kaksha Bala for each planet
    for planet_id in planets:
        result[planet_id] = calculate_kaksha_bala(chart, planet_id)
    
    return result


def get_kaksha_bala_at_sign(chart, sign):
    """
    Calculate Kaksha Bala for a specific sign
    
    Args:
        chart (Chart): The birth chart
        sign (str): The sign to analyze
    
    Returns:
        dict: Dictionary with Kaksha Bala information for the sign
    """
    # Get the sign number (0-11)
    sign_num = get_sign_number(sign)
    
    # List of planets used in Ashtakavarga
    planets = [const.SUN, const.MOON, const.MARS, const.MERCURY,
              const.JUPITER, const.VENUS, const.SATURN]
    
    # Initialize the result
    result = {
        'sign': sign,
        'kaksha_bala': 0,
        'contributions': {}
    }
    
    # Calculate the contribution from each planet's Ashtakavarga
    for planet_id in planets:
        # Get the benefic points
        benefic_points = get_benefic_points(chart, planet_id)
        
        # Get the contribution at the sign
        contribution = benefic_points[sign_num]
        
        # Add to the total
        result['kaksha_bala'] += contribution
        
        # Add to the contributions
        result['contributions'][planet_id] = contribution
    
    # Calculate the percentage of maximum possible Kaksha Bala (56)
    result['percentage'] = (result['kaksha_bala'] / 56.0) * 100.0
    
    # Determine the strength category
    if result['percentage'] >= 75.0:
        result['category'] = 'Very Strong'
    elif result['percentage'] >= 50.0:
        result['category'] = 'Strong'
    elif result['percentage'] >= 25.0:
        result['category'] = 'Moderate'
    else:
        result['category'] = 'Weak'
    
    return result
