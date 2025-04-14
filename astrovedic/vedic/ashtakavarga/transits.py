"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements transit analysis using Ashtakavarga
    for Vedic astrology.
"""

from astrovedic import const
from astrovedic.vedic.ashtakavarga.bhinna import get_benefic_points
from astrovedic.vedic.ashtakavarga.core import get_sign_number


def get_transit_strength(benefic_points, transit_sign_num):
    """
    Calculate the strength of a transit based on Ashtakavarga
    
    Args:
        benefic_points (list): List of 12 values representing benefic points
        transit_sign_num (int): The sign number (0-11) of the transit
    
    Returns:
        dict: Dictionary with transit strength information
    """
    # Get the benefic points at the transit sign
    bindus = benefic_points[transit_sign_num]
    
    # Calculate the percentage of maximum possible bindus (8)
    percentage = (bindus / 8.0) * 100.0
    
    # Determine the strength category
    if bindus >= 6:
        category = 'Excellent'
        description = 'Very favorable transit'
    elif bindus >= 4:
        category = 'Good'
        description = 'Favorable transit'
    elif bindus >= 2:
        category = 'Moderate'
        description = 'Neutral transit'
    else:
        category = 'Weak'
        description = 'Unfavorable transit'
    
    return {
        'bindus': bindus,
        'percentage': percentage,
        'category': category,
        'description': description
    }


def get_best_transit_positions(benefic_points):
    """
    Get the best positions for a planet to transit based on Ashtakavarga
    
    Args:
        benefic_points (list): List of 12 values representing benefic points
    
    Returns:
        list: List of sign numbers (0-11) sorted by transit strength
    """
    # Create a list of (sign_num, bindus) tuples
    sign_bindus = [(i, benefic_points[i]) for i in range(12)]
    
    # Sort by bindus in descending order
    sign_bindus.sort(key=lambda x: x[1], reverse=True)
    
    # Extract the sign numbers
    best_positions = [sign_num for sign_num, _ in sign_bindus]
    
    return best_positions


def get_transit_predictions(birth_chart, transit_chart):
    """
    Generate transit predictions based on Ashtakavarga
    
    Args:
        birth_chart (Chart): The birth chart
        transit_chart (Chart): The transit chart
    
    Returns:
        dict: Dictionary with transit predictions
    """
    # List of planets used in Ashtakavarga
    planets = [const.SUN, const.MOON, const.MARS, const.MERCURY,
              const.JUPITER, const.VENUS, const.SATURN]
    
    # Initialize the result
    result = {}
    
    # Generate predictions for each planet
    for planet_id in planets:
        # Get the Bhinnashtakavarga for the planet
        benefic_points = get_benefic_points(birth_chart, planet_id)
        
        # Get the transit position
        transit_planet = transit_chart.getObject(planet_id)
        transit_sign_num = get_sign_number(transit_planet.sign)
        
        # Calculate the transit strength
        transit_strength = get_transit_strength(benefic_points, transit_sign_num)
        
        # Get the best transit positions
        best_positions = get_best_transit_positions(benefic_points)
        
        # Add to the result
        result[planet_id] = {
            'transit_sign': transit_planet.sign,
            'transit_strength': transit_strength,
            'best_positions': best_positions
        }
    
    return result


def get_ashtakavarga_dasha_phala(birth_chart, dasha_lord_id):
    """
    Calculate the effects of a Dasha period based on Ashtakavarga
    
    Args:
        birth_chart (Chart): The birth chart
        dasha_lord_id (str): The ID of the Dasha lord
    
    Returns:
        dict: Dictionary with Dasha effects
    """
    # Get the Dasha lord from the chart
    dasha_lord = birth_chart.getObject(dasha_lord_id)
    
    # Get the sign number (0-11)
    sign_num = get_sign_number(dasha_lord.sign)
    
    # Get the Bhinnashtakavarga for the Dasha lord
    benefic_points = get_benefic_points(birth_chart, dasha_lord_id)
    
    # Get the benefic points at the Dasha lord's sign
    bindus = benefic_points[sign_num]
    
    # Calculate the percentage of maximum possible bindus (8)
    percentage = (bindus / 8.0) * 100.0
    
    # Determine the strength category
    if bindus >= 6:
        category = 'Excellent'
        description = 'Very favorable Dasha period'
    elif bindus >= 4:
        category = 'Good'
        description = 'Favorable Dasha period'
    elif bindus >= 2:
        category = 'Moderate'
        description = 'Neutral Dasha period'
    else:
        category = 'Weak'
        description = 'Challenging Dasha period'
    
    return {
        'dasha_lord': dasha_lord_id,
        'sign': dasha_lord.sign,
        'bindus': bindus,
        'percentage': percentage,
        'category': category,
        'description': description
    }


def get_gochara_vedha(birth_chart, transit_chart):
    """
    Calculate Gochara Vedha (transit obstruction) based on Ashtakavarga
    
    Args:
        birth_chart (Chart): The birth chart
        transit_chart (Chart): The transit chart
    
    Returns:
        dict: Dictionary with Gochara Vedha information
    """
    # List of planets used in Ashtakavarga
    planets = [const.SUN, const.MOON, const.MARS, const.MERCURY,
              const.JUPITER, const.VENUS, const.SATURN]
    
    # Vedha (obstruction) positions for each sign
    vedha_positions = {
        0: 6,  # Aries is obstructed by Libra
        1: 7,  # Taurus is obstructed by Scorpio
        2: 8,  # Gemini is obstructed by Sagittarius
        3: 9,  # Cancer is obstructed by Capricorn
        4: 10, # Leo is obstructed by Aquarius
        5: 11, # Virgo is obstructed by Pisces
        6: 0,  # Libra is obstructed by Aries
        7: 1,  # Scorpio is obstructed by Taurus
        8: 2,  # Sagittarius is obstructed by Gemini
        9: 3,  # Capricorn is obstructed by Cancer
        10: 4, # Aquarius is obstructed by Leo
        11: 5  # Pisces is obstructed by Virgo
    }
    
    # Initialize the result
    result = {}
    
    # Check for Vedha for each planet
    for planet_id in planets:
        # Get the transit position
        transit_planet = transit_chart.getObject(planet_id)
        transit_sign_num = get_sign_number(transit_planet.sign)
        
        # Get the Vedha position
        vedha_sign_num = vedha_positions[transit_sign_num]
        
        # Check if any planet is at the Vedha position
        vedha_planets = []
        for other_id in planets:
            other_planet = transit_chart.getObject(other_id)
            other_sign_num = get_sign_number(other_planet.sign)
            
            if other_sign_num == vedha_sign_num:
                vedha_planets.append(other_id)
        
        # Add to the result
        result[planet_id] = {
            'transit_sign': transit_planet.sign,
            'vedha_sign': get_sign_from_number(vedha_sign_num),
            'vedha_planets': vedha_planets,
            'has_vedha': len(vedha_planets) > 0
        }
    
    return result


def get_sign_from_number(sign_num):
    """
    Get the sign from a sign number (0-11)
    
    Args:
        sign_num (int): The sign number (0-11)
    
    Returns:
        str: The sign
    """
    signs = [
        const.ARIES, const.TAURUS, const.GEMINI, const.CANCER,
        const.LEO, const.VIRGO, const.LIBRA, const.SCORPIO,
        const.SAGITTARIUS, const.CAPRICORN, const.AQUARIUS, const.PISCES
    ]
    
    return signs[sign_num % 12]
