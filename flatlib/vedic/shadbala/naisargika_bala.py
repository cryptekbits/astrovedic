"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Naisargika Bala (natural strength) calculations
    for Shadbala in Vedic astrology.
"""

from flatlib import const


def calculate_naisargika_bala(planet_id):
    """
    Calculate Naisargika Bala (natural strength) for a planet

    Naisargika Bala is the inherent strength of a planet based on its nature.
    The order of strength is:
    Saturn < Mars < Mercury < Venus < Jupiter < Moon < Sun

    Args:
        planet_id (str): The ID of the planet to analyze

    Returns:
        dict: Dictionary with Naisargika Bala information
    """
    # Maximum value (in Virupas)
    max_value = 60.0

    # Natural strength values for each planet
    # The standard hierarchy is: Sun > Moon > Venus > Jupiter > Mercury > Mars > Saturn
    natural_strengths = {
        const.SUN: 60.0,      # 100%
        const.MOON: 51.4,     # 85.7%
        const.VENUS: 42.9,    # 71.4% (corrected from 34.3)
        const.JUPITER: 34.3,  # 57.1% (corrected from 42.9)
        const.MERCURY: 25.7,  # 42.9%
        const.MARS: 17.1,     # 28.6%
        const.SATURN: 8.6,    # 14.3%
        # Rahu and Ketu are assigned Saturn's value as per traditional methods
        const.RAHU: 8.6,      # 14.3% (same as Saturn)
        const.KETU: 8.6       # 14.3% (same as Saturn)
    }

    # Get the natural strength for the planet
    value = natural_strengths.get(planet_id, 0.0)

    # Determine the description
    if value >= 50.0:
        description = 'Very strong natural strength'
    elif value >= 30.0:
        description = 'Strong natural strength'
    elif value >= 15.0:
        description = 'Moderate natural strength'
    else:
        description = 'Weak natural strength'

    return {'value': value, 'description': description}
