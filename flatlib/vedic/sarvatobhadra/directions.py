"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements auspicious directions calculation
    for Vedic astrology.
"""

from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

# Import chakra functions
from flatlib.vedic.sarvatobhadra.chakra import (
    get_direction_cells, get_nakshatras_in_direction,
    get_planets_in_direction, get_nakshatra_lord
)


def get_direction_quality(chakra, direction):
    """
    Calculate the quality of a direction in the Sarvatobhadra Chakra
    
    Args:
        chakra (dict): The Sarvatobhadra Chakra
        direction (str): The direction ('North', 'Northeast', etc.)
    
    Returns:
        dict: Dictionary with direction quality information
    """
    # Initialize the score
    score = 0
    factors = []
    
    # Get the nakshatras in the direction
    nakshatras = get_nakshatras_in_direction(chakra, direction)
    
    # Get the planets in the direction
    planets = get_planets_in_direction(chakra, direction)
    
    # Check if benefics are in the direction
    benefics = [const.MOON, const.MERCURY, const.JUPITER, const.VENUS]
    for planet_id in benefics:
        if planet_id in planets:
            score += 1
            factors.append(f"{planet_id} is in this direction")
    
    # Check if malefics are in the direction
    malefics = [const.SUN, const.MARS, const.SATURN, const.RAHU, const.KETU]
    for planet_id in malefics:
        if planet_id in planets:
            score -= 1
            factors.append(f"{planet_id} is in this direction")
    
    # Check if the Ascendant is in the direction
    if const.ASC in planets:
        score += 2
        factors.append("Ascendant is in this direction")
    
    # Check the nakshatras in the direction
    for nakshatra in nakshatras:
        # Get the lord of the nakshatra
        lord = get_nakshatra_lord(nakshatra)
        
        # Check if the lord is a benefic
        if lord in ['Moon', 'Mercury', 'Jupiter', 'Venus']:
            score += 0.5
            factors.append(f"Nakshatra {nakshatra} with benefic lord {lord} is in this direction")
        
        # Check if the lord is a malefic
        elif lord in ['Sun', 'Mars', 'Saturn', 'Rahu', 'Ketu']:
            score -= 0.5
            factors.append(f"Nakshatra {nakshatra} with malefic lord {lord} is in this direction")
    
    # Check if the direction is the same as the birth nakshatra
    janma_nakshatra = chakra['janma_nakshatra']
    if janma_nakshatra in nakshatras:
        score += 1
        factors.append(f"Birth nakshatra {janma_nakshatra} is in this direction")
    
    # Check Tara Bala
    tara_bala = chakra['tara_bala']
    
    # Check if favorable Taras are in the direction
    favorable_taras = {
        'Sampath Tara': 'sampath_tara',
        'Kshema Tara': 'kshema_tara',
        'Sadhaka Tara': 'sadhaka_tara',
        'Mitra Tara': 'mitra_tara',
        'Ati Mitra Tara': 'ati_mitra_tara'
    }
    for tara_name, tara_key in favorable_taras.items():
        if tara_key in tara_bala and tara_bala[tara_key] in nakshatras:
            score += 1
            factors.append(f"{tara_name} is in this direction")
    
    # Check if unfavorable Taras are in the direction
    unfavorable_taras = {
        'Vipat Tara': 'vipat_tara',
        'Pratyak Tara': 'pratyak_tara',
        'Vadha Tara': 'vadha_tara'
    }
    for tara_name, tara_key in unfavorable_taras.items():
        if tara_key in tara_bala and tara_bala[tara_key] in nakshatras:
            score -= 1
            factors.append(f"{tara_name} is in this direction")
    
    # Determine the quality based on the score
    if score >= 3:
        quality = 'Excellent'
    elif score >= 1:
        quality = 'Good'
    elif score >= -1:
        quality = 'Neutral'
    elif score >= -3:
        quality = 'Inauspicious'
    else:
        quality = 'Highly Inauspicious'
    
    return {
        'direction': direction,
        'score': score,
        'quality': quality,
        'factors': factors
    }


def get_best_direction(chakra):
    """
    Get the best direction from a Sarvatobhadra Chakra
    
    Args:
        chakra (dict): The Sarvatobhadra Chakra
    
    Returns:
        dict: Dictionary with the best direction information
    """
    # Initialize variables
    best_score = float('-inf')
    best_direction = None
    
    # Check each direction
    for direction in ['North', 'Northeast', 'East', 'Southeast', 'South', 'Southwest', 'West', 'Northwest', 'Center']:
        # Get the quality of the direction
        quality = get_direction_quality(chakra, direction)
        
        # Check if this is the best direction so far
        if quality['score'] > best_score:
            best_score = quality['score']
            best_direction = quality
    
    return best_direction


def get_direction_for_activity(chakra, activity):
    """
    Get the best direction for a specific activity
    
    Args:
        chakra (dict): The Sarvatobhadra Chakra
        activity (str): The type of activity
    
    Returns:
        dict: Dictionary with the best direction information
    """
    # Define the preferred directions for different activities
    activity_directions = {
        'marriage': ['Northeast', 'East', 'North'],
        'travel': ['Northwest', 'West', 'Southwest'],
        'business': ['North', 'East', 'Southeast'],
        'education': ['Northeast', 'East', 'North'],
        'medical': ['East', 'Northeast', 'Southeast'],
        'house_construction': ['Northeast', 'East', 'North'],
        'general': ['North', 'East', 'Northeast', 'Southeast']
    }
    
    # Get the preferred directions for the activity
    preferred_directions = activity_directions.get(activity, activity_directions['general'])
    
    # Initialize variables
    best_score = float('-inf')
    best_direction = None
    
    # Check each preferred direction
    for direction in preferred_directions:
        # Get the quality of the direction
        quality = get_direction_quality(chakra, direction)
        
        # Check if this is the best direction so far
        if quality['score'] > best_score:
            best_score = quality['score']
            best_direction = quality
    
    # If no preferred direction is good, check all directions
    if best_direction is None or best_direction['quality'] in ['Inauspicious', 'Highly Inauspicious']:
        return get_best_direction(chakra)
    
    return best_direction


def get_direction_compatibility(chakra, direction1, direction2):
    """
    Calculate the compatibility between two directions
    
    Args:
        chakra (dict): The Sarvatobhadra Chakra
        direction1 (str): The first direction
        direction2 (str): The second direction
    
    Returns:
        dict: Dictionary with compatibility information
    """
    # Get the quality of each direction
    quality1 = get_direction_quality(chakra, direction1)
    quality2 = get_direction_quality(chakra, direction2)
    
    # Initialize the compatibility
    compatibility = {
        'score': 0,
        'factors': [],
        'description': ''
    }
    
    # Assign scores based on quality
    quality_scores = {
        'Excellent': 5,
        'Good': 4,
        'Neutral': 3,
        'Inauspicious': 2,
        'Highly Inauspicious': 1
    }
    
    # Calculate the average quality score
    avg_quality = (quality_scores.get(quality1['quality'], 3) + quality_scores.get(quality2['quality'], 3)) / 2
    
    # Add to the compatibility score
    compatibility['score'] += avg_quality * 10
    
    # Check if the directions are adjacent
    adjacent_directions = {
        'North': ['Northeast', 'Northwest'],
        'Northeast': ['North', 'East'],
        'East': ['Northeast', 'Southeast'],
        'Southeast': ['East', 'South'],
        'South': ['Southeast', 'Southwest'],
        'Southwest': ['South', 'West'],
        'West': ['Southwest', 'Northwest'],
        'Northwest': ['West', 'North'],
        'Center': ['North', 'Northeast', 'East', 'Southeast', 'South', 'Southwest', 'West', 'Northwest']
    }
    
    if direction2 in adjacent_directions.get(direction1, []):
        compatibility['score'] += 10
        compatibility['factors'].append(f"Directions {direction1} and {direction2} are adjacent")
    
    # Check if the directions are opposite
    opposite_directions = {
        'North': 'South',
        'Northeast': 'Southwest',
        'East': 'West',
        'Southeast': 'Northwest',
        'South': 'North',
        'Southwest': 'Northeast',
        'West': 'East',
        'Northwest': 'Southeast',
        'Center': None
    }
    
    if direction2 == opposite_directions.get(direction1):
        compatibility['score'] -= 20
        compatibility['factors'].append(f"Directions {direction1} and {direction2} are opposite")
    
    # Check if both directions have benefics
    benefics = [const.MOON, const.MERCURY, const.JUPITER, const.VENUS]
    
    planets1 = get_planets_in_direction(chakra, direction1)
    planets2 = get_planets_in_direction(chakra, direction2)
    
    benefics1 = [planet for planet in planets1 if planet in benefics]
    benefics2 = [planet for planet in planets2 if planet in benefics]
    
    if benefics1 and benefics2:
        compatibility['score'] += 10
        compatibility['factors'].append(f"Both directions have benefic planets")
    
    # Ensure the score is between 0 and 100
    compatibility['score'] = min(100, max(0, compatibility['score']))
    
    # Generate a description based on the score
    if compatibility['score'] >= 80:
        compatibility['description'] = f"Directions {direction1} and {direction2} are highly compatible"
    elif compatibility['score'] >= 60:
        compatibility['description'] = f"Directions {direction1} and {direction2} are compatible"
    elif compatibility['score'] >= 40:
        compatibility['description'] = f"Directions {direction1} and {direction2} have moderate compatibility"
    elif compatibility['score'] >= 20:
        compatibility['description'] = f"Directions {direction1} and {direction2} have low compatibility"
    else:
        compatibility['description'] = f"Directions {direction1} and {direction2} are incompatible"
    
    return compatibility
