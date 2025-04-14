"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Argala (intervention) and Virodhargala
    (counter-intervention) calculations for Vedic astrology.
"""

from typing import Dict, List, Optional, Tuple, Union
from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.object import GenericObject

# Argala (intervention) house positions from the reference house
# Primary Argala houses
ARGALA_SECOND = 2    # 2nd house from reference
ARGALA_FOURTH = 4    # 4th house from reference
ARGALA_FIFTH = 5     # 5th house from reference
ARGALA_ELEVENTH = 11 # 11th house from reference

# Secondary Argala houses
ARGALA_THIRD = 3     # 3rd house from reference (secondary)
ARGALA_TENTH = 10    # 10th house from reference (secondary)
ARGALA_NINTH = 9     # 9th house from reference (secondary)

# Virodhargala (counter-intervention) house positions
# These are houses that can neutralize the Argala effect
VIRODHARGALA_SECOND = 12   # 12th house from reference (counters 2nd)
VIRODHARGALA_FOURTH = 10   # 10th house from reference (counters 4th)
VIRODHARGALA_FIFTH = 9     # 9th house from reference (counters 5th)
VIRODHARGALA_ELEVENTH = 3  # 3rd house from reference (counters 11th)

# Argala types
ARGALA_PRIMARY = "Primary Argala"
ARGALA_SECONDARY = "Secondary Argala"
ARGALA_NEUTRALIZED = "Neutralized Argala"
ARGALA_NONE = "No Argala"

def get_house_planets(chart: Chart, house_num: int) -> List[str]:
    """
    Get all planets in a specific house.
    
    Args:
        chart (Chart): The chart
        house_num (int): The house number (1-12)
    
    Returns:
        list: List of planet IDs in the house
    """
    # Get the house
    house = chart.getHouse(f'House{house_num}')
    house_sign = house.sign
    
    # Find all planets in this sign
    planets = []
    for planet_id in const.LIST_SEVEN_PLANETS + [const.RAHU, const.KETU]:
        planet = chart.getObject(planet_id)
        if planet.sign == house_sign:
            planets.append(planet_id)
    
    return planets

def get_argala_houses(house_num: int) -> Dict[str, List[int]]:
    """
    Get the Argala and Virodhargala houses for a reference house.
    
    Args:
        house_num (int): The reference house number (1-12)
    
    Returns:
        dict: Dictionary with Argala and Virodhargala houses
    """
    # Calculate the Argala houses
    argala_houses = {
        'primary': [
            ((house_num + ARGALA_SECOND - 1) % 12) + 1,
            ((house_num + ARGALA_FOURTH - 1) % 12) + 1,
            ((house_num + ARGALA_FIFTH - 1) % 12) + 1,
            ((house_num + ARGALA_ELEVENTH - 1) % 12) + 1
        ],
        'secondary': [
            ((house_num + ARGALA_THIRD - 1) % 12) + 1,
            ((house_num + ARGALA_NINTH - 1) % 12) + 1,
            ((house_num + ARGALA_TENTH - 1) % 12) + 1
        ]
    }
    
    # Calculate the Virodhargala houses
    virodhargala_houses = {
        'second': ((house_num + VIRODHARGALA_SECOND - 1) % 12) + 1,
        'fourth': ((house_num + VIRODHARGALA_FOURTH - 1) % 12) + 1,
        'fifth': ((house_num + VIRODHARGALA_FIFTH - 1) % 12) + 1,
        'eleventh': ((house_num + VIRODHARGALA_ELEVENTH - 1) % 12) + 1
    }
    
    return {
        'argala': argala_houses,
        'virodhargala': virodhargala_houses
    }

def get_argala_for_house(chart: Chart, house_num: int) -> Dict[str, any]:
    """
    Calculate the Argala (intervention) for a specific house.
    
    Args:
        chart (Chart): The chart
        house_num (int): The house number (1-12)
    
    Returns:
        dict: Dictionary with Argala information
    """
    # Get the Argala and Virodhargala houses
    houses = get_argala_houses(house_num)
    argala_houses = houses['argala']
    virodhargala_houses = houses['virodhargala']
    
    # Initialize the result
    result = {
        'reference_house': house_num,
        'argala': {},
        'virodhargala': {},
        'net_argala': {}
    }
    
    # Check primary Argala houses
    for i, argala_house in enumerate(argala_houses['primary']):
        # Get the planets in the Argala house
        argala_planets = get_house_planets(chart, argala_house)
        
        # Get the corresponding Virodhargala house
        if i == 0:  # 2nd house
            virodhargala_house = virodhargala_houses['second']
        elif i == 1:  # 4th house
            virodhargala_house = virodhargala_houses['fourth']
        elif i == 2:  # 5th house
            virodhargala_house = virodhargala_houses['fifth']
        else:  # 11th house
            virodhargala_house = virodhargala_houses['eleventh']
        
        # Get the planets in the Virodhargala house
        virodhargala_planets = get_house_planets(chart, virodhargala_house)
        
        # Calculate the strength of Argala and Virodhargala
        argala_strength = len(argala_planets)
        virodhargala_strength = len(virodhargala_planets)
        
        # Determine if the Argala is neutralized
        is_neutralized = virodhargala_strength >= argala_strength and argala_strength > 0
        
        # Determine the net Argala strength
        net_strength = max(0, argala_strength - virodhargala_strength)
        
        # Determine the Argala type
        if argala_strength == 0:
            argala_type = ARGALA_NONE
        elif is_neutralized:
            argala_type = ARGALA_NEUTRALIZED
        else:
            argala_type = ARGALA_PRIMARY
        
        # Add to the result
        result['argala'][argala_house] = {
            'planets': argala_planets,
            'strength': argala_strength,
            'type': argala_type
        }
        
        result['virodhargala'][virodhargala_house] = {
            'planets': virodhargala_planets,
            'strength': virodhargala_strength,
            'neutralizes': is_neutralized
        }
        
        result['net_argala'][argala_house] = {
            'strength': net_strength,
            'is_neutralized': is_neutralized,
            'type': argala_type
        }
    
    # Check secondary Argala houses
    for argala_house in argala_houses['secondary']:
        # Get the planets in the Argala house
        argala_planets = get_house_planets(chart, argala_house)
        
        # Calculate the strength of Argala
        argala_strength = len(argala_planets)
        
        # Determine the Argala type
        if argala_strength == 0:
            argala_type = ARGALA_NONE
        else:
            argala_type = ARGALA_SECONDARY
        
        # Add to the result
        result['argala'][argala_house] = {
            'planets': argala_planets,
            'strength': argala_strength,
            'type': argala_type
        }
        
        result['net_argala'][argala_house] = {
            'strength': argala_strength,
            'is_neutralized': False,
            'type': argala_type
        }
    
    return result

def get_argala_for_planet(chart: Chart, planet_id: str) -> Dict[str, any]:
    """
    Calculate the Argala (intervention) for a specific planet.
    
    Args:
        chart (Chart): The chart
        planet_id (str): The planet ID
    
    Returns:
        dict: Dictionary with Argala information
    """
    # Get the planet
    planet = chart.getObject(planet_id)
    
    # Get the sign of the planet
    planet_sign = planet.sign
    
    # Find the house number for this sign
    house_num = None
    for i in range(1, 13):
        house = chart.getHouse(f'House{i}')
        if house.sign == planet_sign:
            house_num = i
            break
    
    # If the house is found, calculate the Argala
    if house_num:
        result = get_argala_for_house(chart, house_num)
        result['planet'] = planet_id
        return result
    
    # If the house is not found (which should not happen), return an empty result
    return {
        'planet': planet_id,
        'error': 'House not found for planet'
    }

def get_all_house_argalas(chart: Chart) -> Dict[int, Dict[str, any]]:
    """
    Calculate the Argala (intervention) for all houses.
    
    Args:
        chart (Chart): The chart
    
    Returns:
        dict: Dictionary with Argala information for all houses
    """
    # Initialize the result
    result = {}
    
    # Calculate Argala for each house
    for house_num in range(1, 13):
        result[house_num] = get_argala_for_house(chart, house_num)
    
    return result

def get_all_planet_argalas(chart: Chart) -> Dict[str, Dict[str, any]]:
    """
    Calculate the Argala (intervention) for all planets.
    
    Args:
        chart (Chart): The chart
    
    Returns:
        dict: Dictionary with Argala information for all planets
    """
    # Initialize the result
    result = {}
    
    # Calculate Argala for each planet
    for planet_id in const.LIST_SEVEN_PLANETS + [const.RAHU, const.KETU]:
        result[planet_id] = get_argala_for_planet(chart, planet_id)
    
    return result

def get_virodhargala_for_house(chart: Chart, house_num: int) -> Dict[str, any]:
    """
    Calculate the Virodhargala (counter-intervention) for a specific house.
    
    Args:
        chart (Chart): The chart
        house_num (int): The house number (1-12)
    
    Returns:
        dict: Dictionary with Virodhargala information
    """
    # Get the Argala and Virodhargala houses
    houses = get_argala_houses(house_num)
    argala_houses = houses['argala']
    virodhargala_houses = houses['virodhargala']
    
    # Initialize the result
    result = {
        'reference_house': house_num,
        'virodhargala': {}
    }
    
    # Check Virodhargala houses
    for virodhargala_type, virodhargala_house in virodhargala_houses.items():
        # Get the planets in the Virodhargala house
        virodhargala_planets = get_house_planets(chart, virodhargala_house)
        
        # Calculate the strength of Virodhargala
        virodhargala_strength = len(virodhargala_planets)
        
        # Add to the result
        result['virodhargala'][virodhargala_house] = {
            'planets': virodhargala_planets,
            'strength': virodhargala_strength,
            'type': virodhargala_type
        }
    
    return result

def get_all_house_virodhargalas(chart: Chart) -> Dict[int, Dict[str, any]]:
    """
    Calculate the Virodhargala (counter-intervention) for all houses.
    
    Args:
        chart (Chart): The chart
    
    Returns:
        dict: Dictionary with Virodhargala information for all houses
    """
    # Initialize the result
    result = {}
    
    # Calculate Virodhargala for each house
    for house_num in range(1, 13):
        result[house_num] = get_virodhargala_for_house(chart, house_num)
    
    return result
