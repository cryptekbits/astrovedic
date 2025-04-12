"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Drig Bala (aspectual strength) calculations
    for Shadbala in Vedic astrology.
"""

from flatlib import const
from flatlib import angle
from flatlib.vedic import aspects as vedic_aspects


def calculate_drig_bala(chart, planet_id):
    """
    Calculate Drig Bala (aspectual strength) for a planet

    According to standard Vedic astrology texts, Drig Bala is based solely on the
    aspects received by a planet, not the aspects cast by it. Benefic aspects
    increase strength, while malefic aspects decrease it.

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet to analyze

    Returns:
        dict: Dictionary with Drig Bala information
    """
    # Get the planet from the chart
    planet = chart.getObject(planet_id)

    # Maximum value (in Virupas)
    max_value = 60.0

    # Calculate the aspects received by the planet
    aspects_received = calculate_aspects_received(chart, planet_id)

    # For standard Vedic Drig Bala, we only consider aspects received
    # We still calculate aspects cast for informational purposes
    aspects_cast = calculate_aspects_cast(chart, planet_id)

    # The Drig Bala value is simply the sum of Virupa points from aspects received
    # (already accounting for benefic/malefic nature in the Virupa points calculation)
    net_value = aspects_received['value']

    # Ensure the value is within the range [0, max_value]
    value = max(0.0, min(net_value, max_value))

    # Determine the description
    if value >= 45.0:
        description = 'Very strong aspectual strength'
    elif value >= 30.0:
        description = 'Strong aspectual strength'
    elif value >= 15.0:
        description = 'Moderate aspectual strength'
    else:
        description = 'Weak aspectual strength'

    return {
        'value': value,
        'description': description,
        'aspects_received': aspects_received,
        'aspects_cast': aspects_cast
    }


def calculate_aspects_received(chart, planet_id):
    """
    Calculate the aspects received by a planet using standard Virupa points
    for Drig Bala calculations.

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet

    Returns:
        dict: Dictionary with aspect information
    """
    # Get the planet from the chart
    planet = chart.getObject(planet_id)

    # Initialize the aspect value
    aspect_value = 0.0

    # List of aspects received
    aspects = []

    # Check aspects from each planet
    for other_id in const.LIST_OBJECTS_VEDIC:
        if other_id != planet_id:
            other = chart.getObject(other_id)

            # Get aspect information from the Vedic aspects module
            aspect_info = vedic_aspects.get_graha_drishti_strength(other_id, other.lon, planet.lon)

            if aspect_info['has_aspect']:
                # Calculate Virupa points using the standard system
                virupa_points = get_drig_bala_virupa_points(
                    aspecting_planet_id=other_id,
                    aspect_type=aspect_info['type']
                )

                # Add to the total aspect value
                aspect_value += virupa_points

                # Determine if the aspect is benefic or malefic
                is_benefic = is_benefic_planet(other_id)

                # Add to the list of aspects
                aspects.append({
                    'planet': other_id,
                    'virupa_points': virupa_points,
                    'aspect_type': aspect_info['type'],
                    'is_benefic': is_benefic
                })

    return {
        'value': aspect_value,
        'aspects': aspects
    }


def calculate_aspects_cast(chart, planet_id):
    """
    Calculate the aspects cast by a planet using standard Virupa points
    for Drig Bala calculations.

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet

    Returns:
        dict: Dictionary with aspect information
    """
    # Get the planet from the chart
    planet = chart.getObject(planet_id)

    # Initialize the aspect value
    aspect_value = 0.0

    # List of aspects cast
    aspects = []

    # Check aspects to each planet
    for other_id in const.LIST_OBJECTS_VEDIC:
        if other_id != planet_id:
            other = chart.getObject(other_id)

            # Get aspect information from the Vedic aspects module
            aspect_info = vedic_aspects.get_graha_drishti_strength(planet_id, planet.lon, other.lon)

            if aspect_info['has_aspect']:
                # Calculate Virupa points using the standard system
                virupa_points = get_drig_bala_virupa_points(
                    aspecting_planet_id=planet_id,
                    aspect_type=aspect_info['type']
                )

                # Add to the total aspect value
                aspect_value += virupa_points

                # Determine if the aspect is benefic or malefic
                is_benefic = is_benefic_planet(planet_id)

                # Add to the list of aspects
                aspects.append({
                    'planet': other_id,
                    'virupa_points': virupa_points,
                    'aspect_type': aspect_info['type'],
                    'is_benefic': is_benefic
                })

    return {
        'value': aspect_value,
        'aspects': aspects
    }


def calculate_vedic_aspect_strength(planet_id, from_lon, to_lon):
    """
    Calculate the strength of a Vedic aspect

    In Vedic astrology, planets aspect:
    - All planets aspect the 7th house from their position
    - Mars also aspects the 4th and 8th houses
    - Jupiter also aspects the 5th and 9th houses
    - Saturn also aspects the 3rd and 10th houses

    Args:
        planet_id (str): The ID of the planet casting the aspect
        from_lon (float): The longitude of the planet casting the aspect
        to_lon (float): The longitude of the planet receiving the aspect

    Returns:
        float: The strength of the aspect (0-10)
    """
    # Use the new Vedic aspects module to calculate aspect strength
    aspect_info = vedic_aspects.get_graha_drishti_strength(planet_id, from_lon, to_lon)

    # Convert the aspect strength (0-1) to the scale used in Drig Bala (0-10)
    if aspect_info['has_aspect']:
        return aspect_info['strength'] * 10.0
    else:
        return 0.0


def get_drig_bala_virupa_points(aspecting_planet_id, aspect_type):
    """
    Get the standard Virupa points for Drig Bala calculation based on aspect type
    and the benefic/malefic nature of the aspecting planet.

    According to standard Vedic astrology texts, the Virupa points are:
    - Full aspect: 60 points
    - Three-quarter aspect: 45 points
    - Half aspect: 30 points
    - Quarter aspect: 15 points

    The points are positive for benefic planets and negative for malefic planets.

    Args:
        aspecting_planet_id (str): The ID of the planet casting the aspect
        aspect_type (str): The type of aspect (Full, Three-Quarter, Half, Quarter)

    Returns:
        float: The Virupa points for the aspect
    """
    # Base Virupa points based on aspect type
    if aspect_type == const.VEDIC_FULL_ASPECT:
        base_points = 60.0
    elif aspect_type == const.VEDIC_THREE_QUARTER_ASPECT:
        base_points = 45.0
    elif aspect_type == const.VEDIC_HALF_ASPECT:
        base_points = 30.0
    elif aspect_type == const.VEDIC_QUARTER_ASPECT:
        base_points = 15.0
    else:
        return 0.0  # No aspect

    # Determine if the aspecting planet is benefic or malefic
    is_aspecting_benefic = is_benefic_planet(aspecting_planet_id)

    # Adjust points based on benefic/malefic nature of the aspecting planet
    # Benefic planets give positive points, malefic planets give negative points
    if is_aspecting_benefic:
        return base_points  # Benefic aspects are positive
    else:
        return -base_points  # Malefic aspects are negative


def is_benefic_planet(planet_id):
    """
    Determine if a planet is benefic or malefic according to Vedic astrology.

    Args:
        planet_id (str): The ID of the planet

    Returns:
        bool: True if the planet is benefic, False if malefic
    """
    # Benefic planets in Vedic astrology
    benefic_planets = [const.JUPITER, const.VENUS, const.MERCURY, const.MOON]

    # All other planets are considered malefic
    return planet_id in benefic_planets
