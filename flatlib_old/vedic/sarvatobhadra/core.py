"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements core functionality for Sarvatobhadra Chakra
    calculations in Vedic astrology.
"""

from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

# Import Panchanga functions
from flatlib.vedic.muhurta.panchanga import get_panchanga


def get_sarvatobhadra_chakra(chart):
    """
    Create the Sarvatobhadra Chakra for a chart
    
    Args:
        chart (Chart): The chart
    
    Returns:
        dict: Dictionary with Sarvatobhadra Chakra information
    """
    # Get the Panchanga
    panchanga = get_panchanga(chart)
    
    # Get the Nakshatra
    nakshatra = panchanga['nakshatra']
    
    # Create the chakra
    from flatlib.vedic.sarvatobhadra.chakra import create_chakra
    chakra = create_chakra(nakshatra['num'])
    
    # Add planetary positions to the chakra
    chakra = add_planets_to_chakra(chart, chakra)
    
    # Add Tara Bala to the chakra
    from flatlib.vedic.sarvatobhadra.tara import get_tara_bala
    tara_bala = get_tara_bala(chart)
    chakra['tara_bala'] = tara_bala
    
    return chakra


def add_planets_to_chakra(chart, chakra):
    """
    Add planetary positions to the Sarvatobhadra Chakra
    
    Args:
        chart (Chart): The chart
        chakra (dict): The Sarvatobhadra Chakra
    
    Returns:
        dict: Updated Sarvatobhadra Chakra with planetary positions
    """
    # Initialize the planets dictionary
    planets = {}
    
    # Add each planet to the chakra
    for planet_id in const.LIST_OBJECTS_VEDIC:
        planet = chart.getObject(planet_id)
        
        # Get the planet's position in the chakra
        position = get_planet_position_in_chakra(planet, chakra)
        
        # Add the planet to the planets dictionary
        planets[planet_id] = {
            'position': position,
            'sign': planet.sign,
            'longitude': planet.lon,
            'nakshatra': get_nakshatra_from_longitude(planet.lon)
        }
    
    # Add the Ascendant to the chakra
    asc = chart.getAngle(const.ASC)
    planets[const.ASC] = {
        'position': get_planet_position_in_chakra(asc, chakra),
        'sign': asc.sign,
        'longitude': asc.lon,
        'nakshatra': get_nakshatra_from_longitude(asc.lon)
    }
    
    # Add the planets to the chakra
    chakra['planets'] = planets
    
    return chakra


def get_planet_position_in_chakra(planet, chakra):
    """
    Get the position of a planet in the Sarvatobhadra Chakra
    
    Args:
        planet (Object): The planet
        chakra (dict): The Sarvatobhadra Chakra
    
    Returns:
        tuple: (row, column) position in the chakra
    """
    # Get the planet's nakshatra
    nakshatra = get_nakshatra_from_longitude(planet.lon)
    
    # Find the position of the nakshatra in the chakra
    for row in range(9):
        for col in range(9):
            if chakra['grid'][row][col] == nakshatra:
                return (row, col)
    
    return None


def get_nakshatra_from_longitude(longitude):
    """
    Get the nakshatra number from a longitude
    
    Args:
        longitude (float): The longitude in degrees
    
    Returns:
        int: The nakshatra number (1-27)
    """
    # Calculate the nakshatra number
    nakshatra_num = int(longitude / (360 / 27)) + 1
    
    return nakshatra_num


def get_chakra_quality(chakra):
    """
    Calculate the quality of a Sarvatobhadra Chakra
    
    Args:
        chakra (dict): The Sarvatobhadra Chakra
    
    Returns:
        dict: Dictionary with chakra quality information
    """
    # Initialize the score
    score = 0
    factors = []
    
    # Check planetary positions
    planets = chakra['planets']
    
    # Check if benefics are in auspicious positions
    benefics = [const.MOON, const.MERCURY, const.JUPITER, const.VENUS]
    for planet_id in benefics:
        if planet_id in planets:
            position = planets[planet_id]['position']
            if position:
                row, col = position
                
                # Check if the planet is in an auspicious position
                if is_auspicious_position(row, col):
                    score += 1
                    factors.append(f"{planet_id} is in an auspicious position")
    
    # Check if malefics are in inauspicious positions
    malefics = [const.SUN, const.MARS, const.SATURN, const.RAHU, const.KETU]
    for planet_id in malefics:
        if planet_id in planets:
            position = planets[planet_id]['position']
            if position:
                row, col = position
                
                # Check if the planet is in an inauspicious position
                if is_inauspicious_position(row, col):
                    score += 1
                    factors.append(f"{planet_id} is in an inauspicious position")
    
    # Check Tara Bala
    tara_bala = chakra['tara_bala']
    
    # Check if the Moon is in a favorable Tara
    if tara_bala['current_tara'] in ['Sampath Tara', 'Kshema Tara', 'Sadhaka Tara', 'Mitra Tara', 'Ati Mitra Tara']:
        score += 2
        factors.append(f"Moon is in {tara_bala['current_tara']}")
    elif tara_bala['current_tara'] in ['Vipat Tara', 'Pratyak Tara', 'Vadha Tara']:
        score -= 2
        factors.append(f"Moon is in {tara_bala['current_tara']}")
    
    # Determine the quality based on the score
    if score >= 5:
        quality = 'Excellent'
    elif score >= 2:
        quality = 'Good'
    elif score >= -1:
        quality = 'Neutral'
    elif score >= -4:
        quality = 'Inauspicious'
    else:
        quality = 'Highly Inauspicious'
    
    return {
        'score': score,
        'quality': quality,
        'factors': factors
    }


def is_auspicious_position(row, col):
    """
    Check if a position in the Sarvatobhadra Chakra is auspicious
    
    Args:
        row (int): The row in the chakra (0-8)
        col (int): The column in the chakra (0-8)
    
    Returns:
        bool: True if the position is auspicious, False otherwise
    """
    # Auspicious positions are in the center, corners, and cardinal directions
    if (row == 4 and col == 4) or \
       (row == 0 and col == 0) or \
       (row == 0 and col == 8) or \
       (row == 8 and col == 0) or \
       (row == 8 and col == 8) or \
       (row == 0 and col == 4) or \
       (row == 4 and col == 0) or \
       (row == 4 and col == 8) or \
       (row == 8 and col == 4):
        return True
    
    return False


def is_inauspicious_position(row, col):
    """
    Check if a position in the Sarvatobhadra Chakra is inauspicious
    
    Args:
        row (int): The row in the chakra (0-8)
        col (int): The column in the chakra (0-8)
    
    Returns:
        bool: True if the position is inauspicious, False otherwise
    """
    # Inauspicious positions are in the 3rd, 6th, and 8th positions from the center
    center_row, center_col = 4, 4
    
    # Calculate the distance from the center
    row_dist = abs(row - center_row)
    col_dist = abs(col - center_col)
    
    # Check if the position is in the 3rd, 6th, or 8th position from the center
    if (row_dist == 3 or col_dist == 3) or \
       (row_dist == 6 or col_dist == 6) or \
       (row_dist == 8 or col_dist == 8):
        return True
    
    return False


def get_auspicious_directions(chakra):
    """
    Get the auspicious directions from a Sarvatobhadra Chakra
    
    Args:
        chakra (dict): The Sarvatobhadra Chakra
    
    Returns:
        list: List of auspicious directions
    """
    # Initialize the result
    auspicious_directions = []
    
    # Get the direction qualities
    from flatlib.vedic.sarvatobhadra.directions import get_direction_quality
    
    # Check each direction
    for direction in ['North', 'Northeast', 'East', 'Southeast', 'South', 'Southwest', 'West', 'Northwest', 'Center']:
        # Get the quality of the direction
        quality = get_direction_quality(chakra, direction)
        
        # Add the direction if it's auspicious
        if quality['quality'] in ['Excellent', 'Good']:
            auspicious_directions.append({
                'direction': direction,
                'quality': quality['quality'],
                'score': quality['score'],
                'factors': quality['factors']
            })
    
    return auspicious_directions


def get_inauspicious_directions(chakra):
    """
    Get the inauspicious directions from a Sarvatobhadra Chakra
    
    Args:
        chakra (dict): The Sarvatobhadra Chakra
    
    Returns:
        list: List of inauspicious directions
    """
    # Initialize the result
    inauspicious_directions = []
    
    # Get the direction qualities
    from flatlib.vedic.sarvatobhadra.directions import get_direction_quality
    
    # Check each direction
    for direction in ['North', 'Northeast', 'East', 'Southeast', 'South', 'Southwest', 'West', 'Northwest', 'Center']:
        # Get the quality of the direction
        quality = get_direction_quality(chakra, direction)
        
        # Add the direction if it's inauspicious
        if quality['quality'] in ['Inauspicious', 'Highly Inauspicious']:
            inauspicious_directions.append({
                'direction': direction,
                'quality': quality['quality'],
                'score': quality['score'],
                'factors': quality['factors']
            })
    
    return inauspicious_directions
