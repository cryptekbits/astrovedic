"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements core functionality for transit analysis
    in Vedic astrology.
"""

from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import angle


def get_transit_chart(natal_chart, transit_date):
    """
    Create a transit chart for a specific date
    
    Args:
        natal_chart (Chart): The natal chart
        transit_date (Datetime): The transit date
    
    Returns:
        Chart: The transit chart
    """
    # Get the location from the natal chart
    location = natal_chart.pos
    
    # Create a transit chart with the same house system and ayanamsa as the natal chart
    transit_chart = Chart(transit_date, location, hsys=natal_chart.hsys, mode=natal_chart.mode)
    
    return transit_chart


def get_transit_planets(natal_chart, transit_chart):
    """
    Get the transit planets and their positions relative to the natal chart
    
    Args:
        natal_chart (Chart): The natal chart
        transit_chart (Chart): The transit chart
    
    Returns:
        dict: Dictionary with transit planet information
    """
    # Initialize the result
    transit_planets = {}
    
    # Get the transit planets
    for planet_id in const.LIST_OBJECTS_VEDIC:
        # Get the natal and transit planets
        natal_planet = natal_chart.getObject(planet_id)
        transit_planet = transit_chart.getObject(planet_id)
        
        # Calculate the house position of the transit planet in the natal chart
        house_num = get_house_number(natal_chart, transit_planet.lon)
        
        # Calculate the distance from the natal position
        distance = angle.distance(transit_planet.lon, natal_planet.lon)
        
        # Check if the planet is retrograde
        is_retrograde = transit_planet.isRetrograde()
        
        # Add the planet to the result
        transit_planets[planet_id] = {
            'natal_sign': natal_planet.sign,
            'natal_lon': natal_planet.lon,
            'transit_sign': transit_planet.sign,
            'transit_lon': transit_planet.lon,
            'house': house_num,
            'distance': distance,
            'is_retrograde': is_retrograde
        }
    
    return transit_planets


def get_transit_aspects(natal_chart, transit_chart):
    """
    Get the aspects between transit planets and natal planets
    
    Args:
        natal_chart (Chart): The natal chart
        transit_chart (Chart): The transit chart
    
    Returns:
        list: List of aspects between transit and natal planets
    """
    # Initialize the result
    transit_aspects = []
    
    # Define the aspects to check
    aspects = [
        {'name': 'Conjunction', 'angle': 0, 'orb': 10},
        {'name': 'Opposition', 'angle': 180, 'orb': 10},
        {'name': 'Trine', 'angle': 120, 'orb': 10},
        {'name': 'Square', 'angle': 90, 'orb': 10},
        {'name': 'Sextile', 'angle': 60, 'orb': 6}
    ]
    
    # Check aspects between transit planets and natal planets
    for transit_planet_id in const.LIST_OBJECTS_VEDIC:
        transit_planet = transit_chart.getObject(transit_planet_id)
        
        for natal_planet_id in const.LIST_OBJECTS_VEDIC:
            natal_planet = natal_chart.getObject(natal_planet_id)
            
            # Calculate the angular distance
            dist = angle.closestdistance(transit_planet.lon, natal_planet.lon)
            
            # Check each aspect
            for aspect in aspects:
                # Calculate the orb
                orb = abs(abs(dist) - aspect['angle'])
                
                # Check if the aspect is within the allowed orb
                if orb <= aspect['orb']:
                    # Add the aspect to the result
                    transit_aspects.append({
                        'transit_planet': transit_planet_id,
                        'natal_planet': natal_planet_id,
                        'aspect': aspect['name'],
                        'angle': aspect['angle'],
                        'orb': orb,
                        'applying': is_aspect_applying(transit_planet, natal_planet, aspect['angle'])
                    })
    
    return transit_aspects


def get_transit_houses(natal_chart, transit_chart):
    """
    Get the houses occupied by transit planets in the natal chart
    
    Args:
        natal_chart (Chart): The natal chart
        transit_chart (Chart): The transit chart
    
    Returns:
        dict: Dictionary with house information
    """
    # Initialize the result
    transit_houses = {}
    
    # Initialize the houses
    for house_num in range(1, 13):
        transit_houses[house_num] = {
            'planets': [],
            'sign': get_house_sign(natal_chart, house_num)
        }
    
    # Add transit planets to the houses
    for planet_id in const.LIST_OBJECTS_VEDIC:
        # Get the transit planet
        transit_planet = transit_chart.getObject(planet_id)
        
        # Calculate the house position
        house_num = get_house_number(natal_chart, transit_planet.lon)
        
        # Add the planet to the house
        transit_houses[house_num]['planets'].append(planet_id)
    
    return transit_houses


def get_transit_quality(natal_chart, transit_chart):
    """
    Calculate the overall quality of the transits
    
    Args:
        natal_chart (Chart): The natal chart
        transit_chart (Chart): The transit chart
    
    Returns:
        dict: Dictionary with transit quality information
    """
    # Get the transit aspects
    transit_aspects = get_transit_aspects(natal_chart, transit_chart)
    
    # Initialize the score
    score = 0
    factors = []
    
    # Define the aspect scores
    aspect_scores = {
        'Conjunction': 0,  # Neutral, depends on the planets
        'Opposition': -2,  # Challenging
        'Trine': 2,        # Favorable
        'Square': -1,      # Mildly challenging
        'Sextile': 1       # Mildly favorable
    }
    
    # Define the planet combinations
    benefic_planets = [const.MOON, const.MERCURY, const.JUPITER, const.VENUS]
    malefic_planets = [const.SUN, const.MARS, const.SATURN, const.RAHU, const.KETU]
    
    # Analyze each aspect
    for aspect in transit_aspects:
        # Get the base score for the aspect
        base_score = aspect_scores.get(aspect['aspect'], 0)
        
        # Adjust the score based on the planets involved
        transit_planet = aspect['transit_planet']
        natal_planet = aspect['natal_planet']
        
        # Conjunction between benefics is favorable
        if aspect['aspect'] == 'Conjunction':
            if transit_planet in benefic_planets and natal_planet in benefic_planets:
                base_score = 2
                factors.append(f"Conjunction between benefics {transit_planet} and {natal_planet}")
            elif transit_planet in malefic_planets and natal_planet in malefic_planets:
                base_score = -2
                factors.append(f"Conjunction between malefics {transit_planet} and {natal_planet}")
            elif (transit_planet in benefic_planets and natal_planet in malefic_planets) or \
                 (transit_planet in malefic_planets and natal_planet in benefic_planets):
                base_score = 0
                factors.append(f"Conjunction between {transit_planet} and {natal_planet}")
        
        # Add the score
        score += base_score
        
        # Add the aspect to the factors if significant
        if base_score != 0:
            if aspect['applying']:
                factors.append(f"{aspect['aspect']} between transit {transit_planet} and natal {natal_planet} (applying)")
            else:
                factors.append(f"{aspect['aspect']} between transit {transit_planet} and natal {natal_planet} (separating)")
    
    # Check for retrograde planets
    for planet_id in const.LIST_OBJECTS_VEDIC:
        transit_planet = transit_chart.getObject(planet_id)
        
        if transit_planet.isRetrograde():
            # Retrograde Mercury, Venus, and Jupiter can be positive
            if planet_id in [const.MERCURY, const.VENUS, const.JUPITER]:
                score += 1
                factors.append(f"Retrograde {planet_id} (favorable for introspection)")
            # Retrograde Mars and Saturn are more challenging
            elif planet_id in [const.MARS, const.SATURN]:
                score -= 1
                factors.append(f"Retrograde {planet_id} (challenging)")
    
    # Determine the quality based on the score
    if score >= 5:
        quality = 'Excellent'
    elif score >= 2:
        quality = 'Good'
    elif score >= -1:
        quality = 'Neutral'
    elif score >= -4:
        quality = 'Challenging'
    else:
        quality = 'Difficult'
    
    return {
        'score': score,
        'quality': quality,
        'factors': factors
    }


def get_house_number(chart, longitude):
    """
    Get the house number for a specific longitude in a chart
    
    Args:
        chart (Chart): The chart
        longitude (float): The longitude
    
    Returns:
        int: The house number (1-12)
    """
    # Get the Ascendant
    asc = chart.getAngle(const.ASC)
    
    # Calculate the house number
    house_num = 1 + int(angle.distance(longitude, asc.lon) / 30) % 12
    
    # Adjust for 0-based indexing
    if house_num == 0:
        house_num = 12
    
    return house_num


def get_house_sign(chart, house_num):
    """
    Get the sign of a specific house in a chart
    
    Args:
        chart (Chart): The chart
        house_num (int): The house number (1-12)
    
    Returns:
        str: The sign of the house
    """
    # Get the Ascendant
    asc = chart.getAngle(const.ASC)
    
    # Get the sign of the Ascendant
    asc_sign_num = const.LIST_SIGNS.index(asc.sign)
    
    # Calculate the sign of the house
    sign_num = (asc_sign_num + house_num - 1) % 12
    
    # Return the sign
    return const.LIST_SIGNS[sign_num]


def is_aspect_applying(transit_planet, natal_planet, aspect_angle):
    """
    Check if an aspect is applying (getting closer) or separating (moving away)
    
    Args:
        transit_planet (Object): The transit planet
        natal_planet (Object): The natal planet
        aspect_angle (float): The aspect angle
    
    Returns:
        bool: True if the aspect is applying, False if separating
    """
    # Check if the transit planet is retrograde
    is_retrograde = transit_planet.isRetrograde()
    
    # Calculate the current angular distance
    current_dist = angle.closestdistance(transit_planet.lon, natal_planet.lon)
    
    # Calculate the direction of movement
    if is_retrograde:
        # For retrograde planets, the longitude is decreasing
        next_lon = transit_planet.lon - 1
    else:
        # For direct planets, the longitude is increasing
        next_lon = transit_planet.lon + 1
    
    # Calculate the next angular distance
    next_dist = angle.closestdistance(next_lon, natal_planet.lon)
    
    # Check if the aspect is getting closer (applying) or moving away (separating)
    if abs(abs(next_dist) - aspect_angle) < abs(abs(current_dist) - aspect_angle):
        return True  # Applying
    else:
        return False  # Separating
