"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Vedic combustion (Asta) calculations.
    In Vedic astrology, planets are considered combust when they are
    too close to the Sun, which diminishes their strength.
"""

from typing import Dict, List, Optional, Tuple, Union
from astrovedic import const
from astrovedic import angle
from astrovedic.chart import Chart
from astrovedic.object import GenericObject

# Standard combustion orbs (degrees) for each planet
# These are the standard Vedic values for when a planet is considered combust
COMBUSTION_ORBS = {
    const.MOON: 12,
    const.MERCURY: 14,
    const.VENUS: 10,
    const.MARS: 17,
    const.JUPITER: 11,
    const.SATURN: 15,
    const.RAHU: 9,
    const.KETU: 9
}

# Deep combustion orbs (degrees) for each planet
# When a planet is within these orbs, it is considered deeply combust
DEEP_COMBUSTION_ORBS = {
    const.MOON: 3,
    const.MERCURY: 3,
    const.VENUS: 3,
    const.MARS: 3,
    const.JUPITER: 3,
    const.SATURN: 3,
    const.RAHU: 3,
    const.KETU: 3
}

def is_combust(chart: Chart, planet_id: str) -> bool:
    """
    Check if a planet is combust (too close to the Sun)

    Args:
        chart (Chart): The chart
        planet_id (str): The ID of the planet to check

    Returns:
        bool: True if the planet is combust, False otherwise
    """
    # Get the planet and the Sun
    planet = chart.getObject(planet_id)
    sun = chart.getObject(const.SUN)

    # Skip if the planet is the Sun
    if planet_id == const.SUN:
        return False

    # Calculate the orb
    orb = abs(angle.closestdistance(planet.lon, sun.lon))

    # Adjust combustion orb for retrograde planets
    combustion_orbs = COMBUSTION_ORBS.copy()
    # Check if the planet has the isRetrograde method (Moon nodes don't have it)
    if hasattr(planet, 'isRetrograde') and planet.isRetrograde():
        # Retrograde planets have a slightly different orb for combustion
        if planet_id == const.MERCURY:
            combustion_orbs[const.MERCURY] = 12  # Reduced from 14 as it's closer when retrograde
        elif planet_id == const.VENUS:
            combustion_orbs[const.VENUS] = 8     # Reduced from 10 as it's closer when retrograde

    # Check if the planet is combust
    return orb <= combustion_orbs.get(planet_id, 10)

def is_deeply_combust(chart: Chart, planet_id: str) -> bool:
    """
    Check if a planet is deeply combust (very close to the Sun)

    Args:
        chart (Chart): The chart
        planet_id (str): The ID of the planet to check

    Returns:
        bool: True if the planet is deeply combust, False otherwise
    """
    # Get the planet and the Sun
    planet = chart.getObject(planet_id)
    sun = chart.getObject(const.SUN)

    # Skip if the planet is the Sun
    if planet_id == const.SUN:
        return False

    # Calculate the orb
    orb = abs(angle.closestdistance(planet.lon, sun.lon))

    # Check if the planet is deeply combust
    return orb <= DEEP_COMBUSTION_ORBS.get(planet_id, 3)

def get_combustion_details(chart: Chart, planet_id: str) -> Dict[str, any]:
    """
    Get detailed information about a planet's combustion status

    Args:
        chart (Chart): The chart
        planet_id (str): The ID of the planet to check

    Returns:
        dict: Dictionary with combustion details
    """
    # Get the planet and the Sun
    planet = chart.getObject(planet_id)
    sun = chart.getObject(const.SUN)

    # Skip if the planet is the Sun
    if planet_id == const.SUN:
        return {
            'is_combust': False,
            'is_deeply_combust': False,
            'orb': 0,
            'combustion_orb': 0,
            'deep_combustion_orb': 0,
            'strength_reduction': 0
        }

    # Calculate the orb
    orb = abs(angle.closestdistance(planet.lon, sun.lon))

    # Adjust combustion orb for retrograde planets
    combustion_orbs = COMBUSTION_ORBS.copy()
    # Check if the planet has the isRetrograde method (Moon nodes don't have it)
    if hasattr(planet, 'isRetrograde') and planet.isRetrograde():
        # Retrograde planets have a slightly different orb for combustion
        if planet_id == const.MERCURY:
            combustion_orbs[const.MERCURY] = 12  # Reduced from 14 as it's closer when retrograde
        elif planet_id == const.VENUS:
            combustion_orbs[const.VENUS] = 8     # Reduced from 10 as it's closer when retrograde

    # Get the combustion orb for this planet
    combustion_orb = combustion_orbs.get(planet_id, 10)
    deep_combustion_orb = DEEP_COMBUSTION_ORBS.get(planet_id, 3)

    # Check if the planet is combust or deeply combust
    is_combust_status = orb <= combustion_orb
    is_deeply_combust_status = orb <= deep_combustion_orb

    # Calculate strength reduction (0-100%)
    # The closer to the Sun, the greater the reduction
    if is_combust_status:
        if is_deeply_combust_status:
            # Deep combustion causes severe strength reduction
            strength_reduction = float(100 - ((orb / deep_combustion_orb) * 50))
        else:
            # Regular combustion causes moderate strength reduction
            strength_reduction = float(50 - ((orb - deep_combustion_orb) / (combustion_orb - deep_combustion_orb) * 50))
    else:
        strength_reduction = 0.0

    return {
        'is_combust': is_combust_status,
        'is_deeply_combust': is_deeply_combust_status,
        'orb': orb,
        'combustion_orb': combustion_orb,
        'deep_combustion_orb': deep_combustion_orb,
        'strength_reduction': strength_reduction
    }

def get_all_combustion_details(chart: Chart) -> Dict[str, Dict[str, any]]:
    """
    Get combustion details for all planets in a chart

    Args:
        chart (Chart): The chart

    Returns:
        dict: Dictionary with combustion details for all planets
    """
    # List of planets to check for combustion
    planets = [
        const.MOON, const.MERCURY, const.VENUS, const.MARS,
        const.JUPITER, const.SATURN, const.RAHU, const.KETU
    ]

    # Initialize the result
    result = {}

    # Get combustion details for each planet
    for planet_id in planets:
        result[planet_id] = get_combustion_details(chart, planet_id)

    return result
