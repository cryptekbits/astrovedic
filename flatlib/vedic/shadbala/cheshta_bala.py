"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Cheshta Bala (motional strength) calculations
    for Shadbala in Vedic astrology.
"""

from flatlib import const


def calculate_cheshta_bala(chart, planet_id):
    """
    Calculate Cheshta Bala (motional strength) for a planet
    
    Cheshta Bala is based on the planet's motion:
    - Direct motion gives strength
    - Retrograde motion gives less strength
    - Acceleration and deceleration affect strength
    
    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet to analyze
    
    Returns:
        dict: Dictionary with Cheshta Bala information
    """
    # Get the planet from the chart
    planet = chart.getObject(planet_id)
    
    # Maximum value (in Virupas)
    max_value = 60.0
    
    # Sun and Moon don't have Cheshta Bala
    if planet_id in [const.SUN, const.MOON]:
        return {'value': 0.0, 'description': 'Sun and Moon do not have Cheshta Bala'}
    
    # Rahu and Ketu also don't have traditional Cheshta Bala
    if planet_id in [const.RAHU, const.KETU]:
        return {'value': 0.0, 'description': 'Rahu and Ketu do not have Cheshta Bala'}

    # Check if the planet is retrograde
    is_retrograde = planet.isRetrograde()
    
    # Get the planet's daily motion
    daily_motion = abs(planet.lonspeed)
    
    # Calculate the maximum possible speed for the planet
    max_speed = get_max_speed(planet_id)
    
    # Calculate the relative speed (0-1)
    relative_speed = min(daily_motion / max_speed, 1.0)
    
    # Calculate Cheshta Bala
    if is_retrograde:
        # Retrograde planets get less strength
        value = max_value * relative_speed * 0.5
        description = 'Retrograde motion'
    else:
        # Direct planets get full strength
        value = max_value * relative_speed
        description = 'Direct motion'
    
    return {
        'value': value,
        'description': description,
        'is_retrograde': is_retrograde,
        'daily_motion': daily_motion,
        'max_speed': max_speed,
        'relative_speed': relative_speed
    }


def get_max_speed(planet_id):
    """
    Get the maximum possible speed for a planet
    
    Args:
        planet_id (str): The ID of the planet
    
    Returns:
        float: The maximum possible speed in degrees per day
    """
    # Maximum speeds for each planet (in degrees per day)
    max_speeds = {
        const.MERCURY: 2.0,
        const.VENUS: 1.25,
        const.MARS: 0.75,
        const.JUPITER: 0.4,
        const.SATURN: 0.2,
        const.RAHU: 0.05,
        const.KETU: 0.05
    }
    
    return max_speeds.get(planet_id, 1.0)
