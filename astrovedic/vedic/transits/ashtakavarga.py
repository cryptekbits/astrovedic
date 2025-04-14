"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Ashtakavarga transit analysis
    for Vedic astrology.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic import angle

# Import core functions
from astrovedic.vedic.transits.core import get_house_number

# Import Ashtakavarga functions
from astrovedic.vedic.ashtakavarga import (
    get_ashtakavarga, get_sarvashtakavarga,
    get_bindu_score, get_kaksha
)


def get_transit_ashtakavarga(natal_chart, transit_chart):
    """
    Get the Ashtakavarga transit analysis
    
    Args:
        natal_chart (Chart): The natal chart
        transit_chart (Chart): The transit chart
    
    Returns:
        dict: Dictionary with Ashtakavarga transit information
    """
    # Initialize the result
    transit_ashtakavarga = {}
    
    # Get the Ashtakavarga for the natal chart
    ashtakavarga = get_ashtakavarga(natal_chart)
    
    # Get the Sarvashtakavarga for the natal chart
    sarvashtakavarga = get_sarvashtakavarga(natal_chart)
    
    # Get the transit bindus for each planet
    for planet_id in const.LIST_OBJECTS_VEDIC:
        transit_ashtakavarga[planet_id] = get_transit_bindus(natal_chart, transit_chart, planet_id, ashtakavarga)
    
    # Add the Sarvashtakavarga transit
    transit_ashtakavarga['sarvashtakavarga'] = get_transit_sarvashtakavarga(natal_chart, transit_chart, sarvashtakavarga)
    
    return transit_ashtakavarga


def get_transit_bindus(natal_chart, transit_chart, planet_id, ashtakavarga):
    """
    Get the Ashtakavarga bindus for a transit planet
    
    Args:
        natal_chart (Chart): The natal chart
        transit_chart (Chart): The transit chart
        planet_id (str): The ID of the planet
        ashtakavarga (dict): The Ashtakavarga for the natal chart
    
    Returns:
        dict: Dictionary with transit bindu information
    """
    # Get the transit planet
    transit_planet = transit_chart.getObject(planet_id)
    
    # Get the sign of the transit planet
    transit_sign = transit_planet.sign
    
    # Get the Ashtakavarga for the planet
    planet_ashtakavarga = ashtakavarga.get(planet_id, {})
    
    # Get the bindus for the transit sign
    bindus = planet_ashtakavarga.get(transit_sign, 0)
    
    # Get the house position of the transit planet in the natal chart
    house_num = get_house_number(natal_chart, transit_planet.lon)
    
    # Get the Kaksha (sub-division) of the transit planet
    kaksha = get_transit_kaksha(transit_planet)
    
    # Calculate the strength based on the bindus
    strength = get_transit_ashtakavarga_strength(bindus)
    
    return {
        'sign': transit_sign,
        'house': house_num,
        'bindus': bindus,
        'kaksha': kaksha,
        'strength': strength
    }


def get_transit_sarvashtakavarga(natal_chart, transit_chart, sarvashtakavarga):
    """
    Get the Sarvashtakavarga transit analysis
    
    Args:
        natal_chart (Chart): The natal chart
        transit_chart (Chart): The transit chart
        sarvashtakavarga (dict): The Sarvashtakavarga for the natal chart
    
    Returns:
        dict: Dictionary with Sarvashtakavarga transit information
    """
    # Initialize the result
    transit_sarvashtakavarga = {}
    
    # Get the transit bindus for each planet
    for planet_id in const.LIST_OBJECTS_VEDIC:
        # Get the transit planet
        transit_planet = transit_chart.getObject(planet_id)
        
        # Get the sign of the transit planet
        transit_sign = transit_planet.sign
        
        # Get the bindus for the transit sign
        bindus = sarvashtakavarga.get(transit_sign, 0)
        
        # Get the house position of the transit planet in the natal chart
        house_num = get_house_number(natal_chart, transit_planet.lon)
        
        # Calculate the strength based on the bindus
        strength = get_transit_sarvashtakavarga_strength(bindus)
        
        # Add the planet to the result
        transit_sarvashtakavarga[planet_id] = {
            'sign': transit_sign,
            'house': house_num,
            'bindus': bindus,
            'strength': strength
        }
    
    return transit_sarvashtakavarga


def get_transit_kaksha(transit_planet):
    """
    Get the Kaksha (sub-division) of a transit planet
    
    Args:
        transit_planet (Object): The transit planet
    
    Returns:
        dict: Dictionary with Kaksha information
    """
    # Get the sign and longitude of the transit planet
    sign = transit_planet.sign
    lon = transit_planet.lon
    
    # Calculate the sign longitude (0-30)
    sign_lon = transit_planet.signlon
    
    # Calculate the Kaksha (sub-division)
    kaksha_num = int(sign_lon / 3.33333) + 1
    
    # Get the lord of the Kaksha
    kaksha_lords = {
        1: const.SUN,
        2: const.MOON,
        3: const.MARS,
        4: const.MERCURY,
        5: const.JUPITER,
        6: const.VENUS,
        7: const.SATURN,
        8: const.RAHU,
        9: const.KETU
    }
    
    kaksha_lord = kaksha_lords.get(kaksha_num, const.SUN)
    
    return {
        'num': kaksha_num,
        'lord': kaksha_lord,
        'start_lon': (kaksha_num - 1) * 3.33333,
        'end_lon': kaksha_num * 3.33333
    }


def get_transit_ashtakavarga_strength(bindus):
    """
    Calculate the strength of a transit based on Ashtakavarga bindus
    
    Args:
        bindus (int): The number of bindus
    
    Returns:
        dict: Dictionary with strength information
    """
    # Calculate the strength based on the bindus
    if bindus >= 6:
        strength = 'Excellent'
        description = 'Highly favorable transit, brings success and positive outcomes'
    elif bindus >= 4:
        strength = 'Good'
        description = 'Favorable transit, generally positive results'
    elif bindus >= 2:
        strength = 'Neutral'
        description = 'Mixed transit, neither strongly positive nor negative'
    elif bindus >= 1:
        strength = 'Challenging'
        description = 'Difficult transit, may bring obstacles and challenges'
    else:
        strength = 'Difficult'
        description = 'Very challenging transit, significant obstacles and problems'
    
    return {
        'strength': strength,
        'description': description
    }


def get_transit_sarvashtakavarga_strength(bindus):
    """
    Calculate the strength of a transit based on Sarvashtakavarga bindus
    
    Args:
        bindus (int): The number of bindus
    
    Returns:
        dict: Dictionary with strength information
    """
    # Calculate the strength based on the bindus
    if bindus >= 30:
        strength = 'Excellent'
        description = 'Highly favorable transit, brings success and positive outcomes'
    elif bindus >= 25:
        strength = 'Good'
        description = 'Favorable transit, generally positive results'
    elif bindus >= 20:
        strength = 'Neutral'
        description = 'Mixed transit, neither strongly positive nor negative'
    elif bindus >= 15:
        strength = 'Challenging'
        description = 'Difficult transit, may bring obstacles and challenges'
    else:
        strength = 'Difficult'
        description = 'Very challenging transit, significant obstacles and problems'
    
    return {
        'strength': strength,
        'description': description
    }
