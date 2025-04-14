"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Dig Bala (directional strength) calculations
    for Shadbala in Vedic astrology.
"""

from astrovedic import const
from astrovedic import angle


def calculate_dig_bala(chart, planet_id):
    """
    Calculate Dig Bala (directional strength) for a planet

    Dig Bala is based on the planet's position relative to the four directions:
    - Jupiter and Mercury are strong in the East (1st house)
    - Sun and Mars are strong in the South (10th house)
    - Saturn is strong in the West (7th house)
    - Moon and Venus are strong in the North (4th house)

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet to analyze

    Returns:
        dict: Dictionary with Dig Bala information
    """
    # Get the planet from the chart
    planet = chart.getObject(planet_id)

    # Get the Ascendant
    asc = chart.getAngle(const.ASC)

    # Calculate the house position of the planet (1-12)
    house_position = 1 + int(angle.distance(planet.lon, asc.lon) / 30)

    # Maximum Dig Bala value (in Virupas)
    max_value = 60.0

    # Determine the preferred direction for each planet according to standard Vedic rules
    if planet_id in [const.JUPITER, const.MERCURY]:
        # East (1st house)
        preferred_house = 1
        direction = 'East'
    elif planet_id in [const.SUN, const.MARS]:
        # South (10th house)
        preferred_house = 10
        direction = 'South'
    elif planet_id == const.SATURN:
        # West (7th house)
        preferred_house = 7
        direction = 'West'
    elif planet_id in [const.MOON, const.VENUS]:
        # North (4th house)
        preferred_house = 4
        direction = 'North'
    else:
        # Rahu and Ketu don't have a preferred direction
        return {'value': 0.0, 'description': 'No preferred direction'}

    # Calculate the distance from the preferred house
    distance = min((house_position - preferred_house) % 12, (preferred_house - house_position) % 12)

    # Calculate Dig Bala
    value = max_value * (1 - distance / 6.0)
    if value < 0:
        value = 0.0

    # Determine the description
    if house_position == preferred_house:
        description = f'In preferred direction ({direction})'
    else:
        description = f'Not in preferred direction ({direction})'

    return {
        'value': value,
        'description': description,
        'preferred_direction': direction,
        'preferred_house': preferred_house,
        'actual_house': house_position
    }
