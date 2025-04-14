"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements transit effects on Dashas
    for Vedic astrology.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic import angle

# Import core functions
from astrovedic.vedic.transits.core import get_house_number

# Import Dasha functions
from astrovedic.vedic.vimshottari import (
    get_dasha, get_antardasha, get_pratyantardasha,
    get_dasha_lord, get_antardasha_lord, get_pratyantardasha_lord
)


def get_transit_dasha_effects(natal_chart, transit_chart):
    """
    Get the effects of transits on the current Dasha
    
    Args:
        natal_chart (Chart): The natal chart
        transit_chart (Chart): The transit chart
    
    Returns:
        dict: Dictionary with transit Dasha effects
    """
    # Get the current Dasha
    dasha = get_dasha(natal_chart, transit_chart.date)
    
    # Get the current Antardasha
    antardasha = get_antardasha(natal_chart, transit_chart.date)
    
    # Get the current Pratyantardasha
    pratyantardasha = get_pratyantardasha(natal_chart, transit_chart.date)
    
    # Get the Dasha lord
    dasha_lord = get_dasha_lord(dasha)
    
    # Get the Antardasha lord
    antardasha_lord = get_antardasha_lord(antardasha)
    
    # Get the Pratyantardasha lord
    pratyantardasha_lord = get_pratyantardasha_lord(pratyantardasha)
    
    # Get the transit effects on the Dasha lord
    dasha_effects = get_transit_effects_on_planet(natal_chart, transit_chart, dasha_lord)
    
    # Get the transit effects on the Antardasha lord
    antardasha_effects = get_transit_effects_on_planet(natal_chart, transit_chart, antardasha_lord)
    
    # Get the transit effects on the Pratyantardasha lord
    pratyantardasha_effects = get_transit_effects_on_planet(natal_chart, transit_chart, pratyantardasha_lord)
    
    return {
        'dasha': dasha,
        'antardasha': antardasha,
        'pratyantardasha': pratyantardasha,
        'dasha_lord': dasha_lord,
        'antardasha_lord': antardasha_lord,
        'pratyantardasha_lord': pratyantardasha_lord,
        'dasha_effects': dasha_effects,
        'antardasha_effects': antardasha_effects,
        'pratyantardasha_effects': pratyantardasha_effects
    }


def get_transit_antardasha_effects(natal_chart, transit_chart):
    """
    Get the effects of transits on the current Antardasha
    
    Args:
        natal_chart (Chart): The natal chart
        transit_chart (Chart): The transit chart
    
    Returns:
        dict: Dictionary with transit Antardasha effects
    """
    # Get the current Antardasha
    antardasha = get_antardasha(natal_chart, transit_chart.date)
    
    # Get the Antardasha lord
    antardasha_lord = get_antardasha_lord(antardasha)
    
    # Get the transit effects on the Antardasha lord
    antardasha_effects = get_transit_effects_on_planet(natal_chart, transit_chart, antardasha_lord)
    
    return {
        'antardasha': antardasha,
        'antardasha_lord': antardasha_lord,
        'antardasha_effects': antardasha_effects
    }


def get_transit_pratyantardasha_effects(natal_chart, transit_chart):
    """
    Get the effects of transits on the current Pratyantardasha
    
    Args:
        natal_chart (Chart): The natal chart
        transit_chart (Chart): The transit chart
    
    Returns:
        dict: Dictionary with transit Pratyantardasha effects
    """
    # Get the current Pratyantardasha
    pratyantardasha = get_pratyantardasha(natal_chart, transit_chart.date)
    
    # Get the Pratyantardasha lord
    pratyantardasha_lord = get_pratyantardasha_lord(pratyantardasha)
    
    # Get the transit effects on the Pratyantardasha lord
    pratyantardasha_effects = get_transit_effects_on_planet(natal_chart, transit_chart, pratyantardasha_lord)
    
    return {
        'pratyantardasha': pratyantardasha,
        'pratyantardasha_lord': pratyantardasha_lord,
        'pratyantardasha_effects': pratyantardasha_effects
    }


def get_transit_effects_on_planet(natal_chart, transit_chart, planet_id):
    """
    Get the effects of transits on a specific planet
    
    Args:
        natal_chart (Chart): The natal chart
        transit_chart (Chart): The transit chart
        planet_id (str): The ID of the planet
    
    Returns:
        dict: Dictionary with transit effects on the planet
    """
    # Initialize the result
    effects = []
    
    # Get the natal planet
    natal_planet = natal_chart.getObject(planet_id)
    
    # Get the house position of the natal planet
    natal_house = get_house_number(natal_chart, natal_planet.lon)
    
    # Check transits to the natal planet
    for transit_planet_id in const.LIST_OBJECTS_VEDIC:
        # Get the transit planet
        transit_planet = transit_chart.getObject(transit_planet_id)
        
        # Calculate the angular distance
        dist = angle.closestdistance(transit_planet.lon, natal_planet.lon)
        
        # Check for aspects
        aspects = [
            {'name': 'Conjunction', 'angle': 0, 'orb': 10},
            {'name': 'Opposition', 'angle': 180, 'orb': 10},
            {'name': 'Trine', 'angle': 120, 'orb': 10},
            {'name': 'Square', 'angle': 90, 'orb': 10},
            {'name': 'Sextile', 'angle': 60, 'orb': 6}
        ]
        
        for aspect in aspects:
            # Calculate the orb
            orb = abs(abs(dist) - aspect['angle'])
            
            # Check if the aspect is within the allowed orb
            if orb <= aspect['orb']:
                # Add the aspect to the effects
                effects.append({
                    'transit_planet': transit_planet_id,
                    'aspect': aspect['name'],
                    'orb': orb,
                    'applying': is_aspect_applying(transit_planet, natal_planet, aspect['angle']),
                    'effect': get_aspect_effect(transit_planet_id, planet_id, aspect['name'])
                })
    
    # Check transits to the house of the natal planet
    for transit_planet_id in const.LIST_OBJECTS_VEDIC:
        # Get the transit planet
        transit_planet = transit_chart.getObject(transit_planet_id)
        
        # Get the house position of the transit planet
        transit_house = get_house_number(natal_chart, transit_planet.lon)
        
        # Check if the transit planet is in the same house as the natal planet
        if transit_house == natal_house:
            # Add the house transit to the effects
            effects.append({
                'transit_planet': transit_planet_id,
                'house': natal_house,
                'effect': get_house_transit_effect(transit_planet_id, planet_id, natal_house)
            })
    
    return effects


def get_dasha_transit_compatibility(natal_chart, transit_chart):
    """
    Calculate the compatibility between the current Dasha and transits
    
    Args:
        natal_chart (Chart): The natal chart
        transit_chart (Chart): The transit chart
    
    Returns:
        dict: Dictionary with Dasha-transit compatibility information
    """
    # Get the current Dasha
    dasha = get_dasha(natal_chart, transit_chart.date)
    
    # Get the current Antardasha
    antardasha = get_antardasha(natal_chart, transit_chart.date)
    
    # Get the Dasha lord
    dasha_lord = get_dasha_lord(dasha)
    
    # Get the Antardasha lord
    antardasha_lord = get_antardasha_lord(antardasha)
    
    # Get the transit effects on the Dasha lord
    dasha_effects = get_transit_effects_on_planet(natal_chart, transit_chart, dasha_lord)
    
    # Get the transit effects on the Antardasha lord
    antardasha_effects = get_transit_effects_on_planet(natal_chart, transit_chart, antardasha_lord)
    
    # Calculate the compatibility score
    score = 0
    factors = []
    
    # Analyze the Dasha effects
    for effect in dasha_effects:
        if 'aspect' in effect:
            # Get the score for the aspect
            aspect_score = get_aspect_score(effect['aspect'], effect['transit_planet'], dasha_lord)
            
            # Add to the score
            score += aspect_score
            
            # Add to the factors
            if aspect_score > 0:
                factors.append(f"Favorable {effect['aspect']} from transit {effect['transit_planet']} to Dasha lord {dasha_lord}")
            elif aspect_score < 0:
                factors.append(f"Challenging {effect['aspect']} from transit {effect['transit_planet']} to Dasha lord {dasha_lord}")
        
        if 'house' in effect:
            # Get the score for the house transit
            house_score = get_house_transit_score(effect['transit_planet'], dasha_lord, effect['house'])
            
            # Add to the score
            score += house_score
            
            # Add to the factors
            if house_score > 0:
                factors.append(f"Favorable transit of {effect['transit_planet']} through the house of Dasha lord {dasha_lord}")
            elif house_score < 0:
                factors.append(f"Challenging transit of {effect['transit_planet']} through the house of Dasha lord {dasha_lord}")
    
    # Analyze the Antardasha effects
    for effect in antardasha_effects:
        if 'aspect' in effect:
            # Get the score for the aspect
            aspect_score = get_aspect_score(effect['aspect'], effect['transit_planet'], antardasha_lord)
            
            # Add to the score (with less weight)
            score += aspect_score * 0.5
            
            # Add to the factors
            if aspect_score > 0:
                factors.append(f"Favorable {effect['aspect']} from transit {effect['transit_planet']} to Antardasha lord {antardasha_lord}")
            elif aspect_score < 0:
                factors.append(f"Challenging {effect['aspect']} from transit {effect['transit_planet']} to Antardasha lord {antardasha_lord}")
        
        if 'house' in effect:
            # Get the score for the house transit
            house_score = get_house_transit_score(effect['transit_planet'], antardasha_lord, effect['house'])
            
            # Add to the score (with less weight)
            score += house_score * 0.5
            
            # Add to the factors
            if house_score > 0:
                factors.append(f"Favorable transit of {effect['transit_planet']} through the house of Antardasha lord {antardasha_lord}")
            elif house_score < 0:
                factors.append(f"Challenging transit of {effect['transit_planet']} through the house of Antardasha lord {antardasha_lord}")
    
    # Determine the compatibility based on the score
    if score >= 3:
        compatibility = 'Excellent'
        description = 'Highly favorable transits during this Dasha period'
    elif score >= 1:
        compatibility = 'Good'
        description = 'Favorable transits during this Dasha period'
    elif score >= -1:
        compatibility = 'Neutral'
        description = 'Mixed transits during this Dasha period'
    elif score >= -3:
        compatibility = 'Challenging'
        description = 'Difficult transits during this Dasha period'
    else:
        compatibility = 'Difficult'
        description = 'Very challenging transits during this Dasha period'
    
    return {
        'dasha': dasha,
        'antardasha': antardasha,
        'dasha_lord': dasha_lord,
        'antardasha_lord': antardasha_lord,
        'score': score,
        'compatibility': compatibility,
        'description': description,
        'factors': factors
    }


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


def get_aspect_effect(transit_planet_id, natal_planet_id, aspect_name):
    """
    Get the effect of an aspect between a transit planet and a natal planet
    
    Args:
        transit_planet_id (str): The ID of the transit planet
        natal_planet_id (str): The ID of the natal planet
        aspect_name (str): The name of the aspect
    
    Returns:
        dict: Dictionary with aspect effect information
    """
    # Define the effects for different aspects
    aspect_effects = {
        'Conjunction': {
            'effect': 'Mixed',
            'description': f"Transit {transit_planet_id} conjunct natal {natal_planet_id}"
        },
        'Opposition': {
            'effect': 'Challenging',
            'description': f"Transit {transit_planet_id} opposite natal {natal_planet_id}"
        },
        'Trine': {
            'effect': 'Favorable',
            'description': f"Transit {transit_planet_id} trine natal {natal_planet_id}"
        },
        'Square': {
            'effect': 'Challenging',
            'description': f"Transit {transit_planet_id} square natal {natal_planet_id}"
        },
        'Sextile': {
            'effect': 'Favorable',
            'description': f"Transit {transit_planet_id} sextile natal {natal_planet_id}"
        }
    }
    
    # Get the base effect for the aspect
    base_effect = aspect_effects.get(aspect_name, {'effect': 'Neutral', 'description': 'No specific effect'})
    
    # Adjust the effect based on the planets involved
    benefic_planets = [const.MOON, const.MERCURY, const.JUPITER, const.VENUS]
    malefic_planets = [const.SUN, const.MARS, const.SATURN, const.RAHU, const.KETU]
    
    # Conjunction between benefics is favorable
    if aspect_name == 'Conjunction':
        if transit_planet_id in benefic_planets and natal_planet_id in benefic_planets:
            base_effect['effect'] = 'Favorable'
            base_effect['description'] = f"Favorable conjunction between transit {transit_planet_id} and natal {natal_planet_id}"
        elif transit_planet_id in malefic_planets and natal_planet_id in malefic_planets:
            base_effect['effect'] = 'Challenging'
            base_effect['description'] = f"Challenging conjunction between transit {transit_planet_id} and natal {natal_planet_id}"
    
    return base_effect


def get_house_transit_effect(transit_planet_id, natal_planet_id, house_num):
    """
    Get the effect of a transit planet in the house of a natal planet
    
    Args:
        transit_planet_id (str): The ID of the transit planet
        natal_planet_id (str): The ID of the natal planet
        house_num (int): The house number
    
    Returns:
        dict: Dictionary with house transit effect information
    """
    # Define the effects for different house transits
    house_effects = {
        'effect': 'Mixed',
        'description': f"Transit {transit_planet_id} in the house of natal {natal_planet_id} (house {house_num})"
    }
    
    # Adjust the effect based on the planets involved
    benefic_planets = [const.MOON, const.MERCURY, const.JUPITER, const.VENUS]
    malefic_planets = [const.SUN, const.MARS, const.SATURN, const.RAHU, const.KETU]
    
    # Benefic transit in the house of a natal planet is generally favorable
    if transit_planet_id in benefic_planets:
        house_effects['effect'] = 'Favorable'
        house_effects['description'] = f"Favorable transit of {transit_planet_id} through the house of natal {natal_planet_id} (house {house_num})"
    
    # Malefic transit in the house of a natal planet is generally challenging
    elif transit_planet_id in malefic_planets:
        house_effects['effect'] = 'Challenging'
        house_effects['description'] = f"Challenging transit of {transit_planet_id} through the house of natal {natal_planet_id} (house {house_num})"
    
    return house_effects


def get_aspect_score(aspect_name, transit_planet_id, natal_planet_id):
    """
    Calculate the score for an aspect between a transit planet and a natal planet
    
    Args:
        aspect_name (str): The name of the aspect
        transit_planet_id (str): The ID of the transit planet
        natal_planet_id (str): The ID of the natal planet
    
    Returns:
        float: The aspect score
    """
    # Define the base scores for different aspects
    aspect_scores = {
        'Conjunction': 0,  # Neutral, depends on the planets
        'Opposition': -2,  # Challenging
        'Trine': 2,        # Favorable
        'Square': -1,      # Mildly challenging
        'Sextile': 1       # Mildly favorable
    }
    
    # Get the base score for the aspect
    base_score = aspect_scores.get(aspect_name, 0)
    
    # Adjust the score based on the planets involved
    benefic_planets = [const.MOON, const.MERCURY, const.JUPITER, const.VENUS]
    malefic_planets = [const.SUN, const.MARS, const.SATURN, const.RAHU, const.KETU]
    
    # Conjunction between benefics is favorable
    if aspect_name == 'Conjunction':
        if transit_planet_id in benefic_planets and natal_planet_id in benefic_planets:
            base_score = 2
        elif transit_planet_id in malefic_planets and natal_planet_id in malefic_planets:
            base_score = -2
    
    return base_score


def get_house_transit_score(transit_planet_id, natal_planet_id, house_num):
    """
    Calculate the score for a transit planet in the house of a natal planet
    
    Args:
        transit_planet_id (str): The ID of the transit planet
        natal_planet_id (str): The ID of the natal planet
        house_num (int): The house number
    
    Returns:
        float: The house transit score
    """
    # Define the base score for house transits
    base_score = 0
    
    # Adjust the score based on the planets involved
    benefic_planets = [const.MOON, const.MERCURY, const.JUPITER, const.VENUS]
    malefic_planets = [const.SUN, const.MARS, const.SATURN, const.RAHU, const.KETU]
    
    # Benefic transit in the house of a natal planet is generally favorable
    if transit_planet_id in benefic_planets:
        base_score = 1
    
    # Malefic transit in the house of a natal planet is generally challenging
    elif transit_planet_id in malefic_planets:
        base_score = -1
    
    return base_score
