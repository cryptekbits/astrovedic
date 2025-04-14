"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Bhava Chalita chart calculations
    for Vedic astrology.
"""

from typing import Dict, List, Optional, Tuple, Union
from astrovedic import const
from astrovedic import angle
from astrovedic.chart import Chart
from astrovedic.object import GenericObject

def is_in_range(lon: float, start_lon: float, end_lon: float) -> bool:
    """
    Check if a longitude is in a range (inclusive of start, exclusive of end).

    Args:
        lon (float): The longitude to check
        start_lon (float): The start longitude of the range
        end_lon (float): The end longitude of the range

    Returns:
        bool: True if the longitude is in the range, False otherwise
    """
    # Normalize all longitudes to 0-360
    lon = angle.norm(lon)
    start_lon = angle.norm(start_lon)
    end_lon = angle.norm(end_lon)

    # If the range doesn't cross 0 degrees
    if start_lon < end_lon:
        return start_lon <= lon < end_lon

    # If the range crosses 0 degrees
    return start_lon <= lon or lon < end_lon

def get_bhava_chalita_chart(chart: Chart) -> Dict[str, any]:
    """
    Calculate the Bhava Chalita chart.

    The Bhava Chalita chart is based on equal house division from the Ascendant degree.
    Each house is exactly 30 degrees, starting from the Ascendant degree.

    Args:
        chart (Chart): The chart

    Returns:
        dict: Dictionary with Bhava Chalita chart information
    """
    # Get the Ascendant degree (House1 longitude)
    asc_lon = chart.getHouse('House1').lon

    # Calculate the house cusps
    house_cusps = []
    for i in range(12):
        cusp_lon = angle.norm(asc_lon + (i * 30))
        house_cusps.append(cusp_lon)

    # Create the Bhava Chalita houses
    houses = {}
    for i in range(12):
        house_num = i + 1

        # Get the house cusp longitude
        cusp_lon = house_cusps[i]

        # Determine the sign of the house cusp
        sign_num = int(cusp_lon / 30)
        sign = const.LIST_SIGNS[sign_num]

        # Create the house
        houses[house_num] = {
            'cusp': cusp_lon,
            'sign': sign,
            'sign_longitude': cusp_lon % 30
        }

    # Determine which planets are in which houses
    planets_in_houses = {}
    for house_num, house_info in houses.items():
        planets_in_houses[house_num] = []

        # Get the house cusp longitude
        cusp_lon = house_info['cusp']

        # Get the next house cusp longitude
        next_house_num = (house_num % 12) + 1
        next_cusp_lon = houses[next_house_num]['cusp']

        # Check each planet (traditional planets only)
        for planet_id in const.LIST_SEVEN_PLANETS + [const.RAHU, const.KETU]:
            planet = chart.getObject(planet_id)
            planet_lon = planet.lon

            # Check if the planet is in this house
            if is_in_range(planet_lon, cusp_lon, next_cusp_lon):
                planets_in_houses[house_num].append({
                    'id': planet_id,
                    'longitude': planet_lon,
                    'sign': planet.sign,
                    'sign_longitude': planet_lon % 30
                })

    return {
        'houses': houses,
        'planets_in_houses': planets_in_houses
    }

def get_bhava_chalita_house_for_planet(chart: Chart, planet_id: str) -> int:
    """
    Determine which Bhava Chalita house a planet is in.

    Args:
        chart (Chart): The chart
        planet_id (str): The ID of the planet

    Returns:
        int: The house number (1-12)
    """
    # Get the Bhava Chalita chart
    bhava_chalita = get_bhava_chalita_chart(chart)

    # Get the planet's longitude
    planet = chart.getObject(planet_id)
    planet_lon = planet.lon

    # Check each house
    for house_num, planets in bhava_chalita['planets_in_houses'].items():
        for planet_info in planets:
            if planet_info['id'] == planet_id:
                return house_num

    # If the planet is not found in any house (which should not happen),
    # determine the house based on the planet's longitude
    asc_lon = chart.getHouse('House1').lon

    # Calculate the house number based on the planet's longitude
    # The house number is determined by the number of 30-degree segments
    # from the Ascendant degree
    house_num = int(angle.distance(asc_lon, planet_lon) / 30) + 1

    return house_num

def get_bhava_chalita_planets_in_house(chart: Chart, house_num: int) -> List[Dict[str, any]]:
    """
    Get all planets in a specific Bhava Chalita house.

    Args:
        chart (Chart): The chart
        house_num (int): The house number (1-12)

    Returns:
        list: List of planets in the house
    """
    # Get the Bhava Chalita chart
    bhava_chalita = get_bhava_chalita_chart(chart)

    # Get the planets in the specified house
    return bhava_chalita['planets_in_houses'].get(house_num, [])

def get_bhava_chalita_house_lord(chart: Chart, house_num: int) -> str:
    """
    Get the lord of a specific Bhava Chalita house.

    Args:
        chart (Chart): The chart
        house_num (int): The house number (1-12)

    Returns:
        str: The planet ID of the house lord
    """
    # Get the Bhava Chalita chart
    bhava_chalita = get_bhava_chalita_chart(chart)

    # Get the sign of the house
    house_sign = bhava_chalita['houses'][house_num]['sign']

    # Determine the lord of the sign
    sign_lords = {
        const.ARIES: const.MARS,
        const.TAURUS: const.VENUS,
        const.GEMINI: const.MERCURY,
        const.CANCER: const.MOON,
        const.LEO: const.SUN,
        const.VIRGO: const.MERCURY,
        const.LIBRA: const.VENUS,
        const.SCORPIO: const.MARS,
        const.SAGITTARIUS: const.JUPITER,
        const.CAPRICORN: const.SATURN,
        const.AQUARIUS: const.SATURN,
        const.PISCES: const.JUPITER
    }

    return sign_lords[house_sign]

def get_bhava_chalita_house_strength(chart: Chart, house_num: int) -> Dict[str, any]:
    """
    Calculate the strength of a specific Bhava Chalita house.

    Args:
        chart (Chart): The chart
        house_num (int): The house number (1-12)

    Returns:
        dict: Dictionary with house strength information
    """
    # Get the Bhava Chalita chart (not used directly, but needed for consistency)
    _ = get_bhava_chalita_chart(chart)

    # Get the house lord
    house_lord = get_bhava_chalita_house_lord(chart, house_num)

    # Get the house where the lord is placed
    lord_house = get_bhava_chalita_house_for_planet(chart, house_lord)

    # Calculate the strength based on the relationship between the house and its lord's house
    # This is a simplified version; in reality, house strength is more complex

    # Calculate the distance between the house and its lord's house
    distance = ((lord_house - house_num) % 12) + 1

    # Determine the strength based on the distance
    if distance == 1:  # Lord in the same house
        strength = 100  # Very strong
        description = "Very strong - Lord in the same house"
    elif distance in [5, 9]:  # Lord in a trine house
        strength = 90  # Strong
        description = "Strong - Lord in a trine house"
    elif distance in [3, 11]:  # Lord in a friendly house
        strength = 75  # Good
        description = "Good - Lord in a friendly house"
    elif distance in [2, 12]:  # Lord in an adjacent house
        strength = 60  # Moderate
        description = "Moderate - Lord in an adjacent house"
    elif distance in [4, 10]:  # Lord in a square house
        strength = 40  # Weak
        description = "Weak - Lord in a square house"
    elif distance in [6, 8]:  # Lord in a malefic house
        strength = 20  # Very weak
        description = "Very weak - Lord in a malefic house"
    else:  # Lord in the 7th house
        strength = 50  # Neutral
        description = "Neutral - Lord in the 7th house"

    # Get the planets in the house
    planets = get_bhava_chalita_planets_in_house(chart, house_num)

    # Adjust strength based on planets in the house
    # This is a simplified version; in reality, the adjustment is more complex
    for planet_info in planets:
        planet_id = planet_info['id']

        # Benefics increase strength, malefics decrease it
        if planet_id in [const.JUPITER, const.VENUS, const.MERCURY, const.MOON]:
            strength += 5  # Benefic
        elif planet_id in [const.SATURN, const.MARS, const.RAHU, const.KETU]:
            strength -= 5  # Malefic
        # Sun is neutral

    # Ensure strength is within the valid range (0-100)
    strength = max(0, min(100, strength))

    return {
        'strength': strength,
        'description': description,
        'lord': house_lord,
        'lord_house': lord_house,
        'planets': planets
    }
