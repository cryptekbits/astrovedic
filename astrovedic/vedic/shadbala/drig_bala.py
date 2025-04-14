"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Drig Bala (aspectual strength) calculations
    for Shadbala in Vedic astrology.
"""

from astrovedic import const
from astrovedic import angle
from astrovedic.vedic import aspects as vedic_aspects


def calculate_drig_bala(chart, planet_id):
    """
    Calculate Drig Bala (aspectual strength) for a planet

    According to standard Vedic astrology texts, Drig Bala is based solely on the
    aspects received by a planet, not the aspects cast by it. Benefic aspects
    increase strength, while malefic aspects decrease it. This implementation
    now includes Rashi Drishti (sign aspects) and calculates aspectual strength
    based on the aspecting planet's strength.

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

    # Initialize the net value
    net_value = 0.0

    # Calculate aspects received
    aspects_received = calculate_aspects_received(chart, planet_id)
    net_value += aspects_received['value']

    # Calculate aspects cast (for information only, not used in net value)
    aspects_cast = calculate_aspects_cast(chart, planet_id)

    # Include Rashi Drishti (sign aspects)
    rashi_drishti = calculate_rashi_drishti(chart, planet_id)
    net_value += rashi_drishti['value']

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
        'aspects_cast': aspects_cast,
        'rashi_drishti': rashi_drishti
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


def calculate_rashi_drishti(chart, planet_id):
    """
    Calculate Rashi Drishti (sign aspects) for a planet

    In Vedic astrology, Rashi Drishti refers to aspects based on the signs
    occupied by planets. Certain signs aspect other signs based on their
    relationship (e.g., movable signs aspect fixed signs except the adjacent one).

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet

    Returns:
        dict: Dictionary with Rashi Drishti information
    """
    # Get the planet from the chart
    planet = chart.getObject(planet_id)

    # Get the sign of the planet
    planet_sign = int(planet.lon / 30) % 12

    # Initialize the aspect value
    aspect_value = 0.0

    # List of Rashi Drishti received
    rashi_aspects = []

    # Define Rashi Drishti rules
    movable_signs = [0, 3, 6, 9]  # Aries, Cancer, Libra, Capricorn
    fixed_signs = [1, 4, 7, 10]   # Taurus, Leo, Scorpio, Aquarius
    dual_signs = [2, 5, 8, 11]    # Gemini, Virgo, Sagittarius, Pisces

    # Determine the type of sign the planet is in
    if planet_sign in movable_signs:
        # Movable signs aspect fixed signs except the adjacent one
        aspected_signs = [s for s in fixed_signs if (s - planet_sign) % 12 != 1]
    elif planet_sign in fixed_signs:
        # Fixed signs aspect movable signs except the adjacent one
        aspected_signs = [s for s in movable_signs if (s - planet_sign) % 12 != 11]
    else:
        # Dual signs aspect other dual signs
        aspected_signs = dual_signs

    # Check for planets in aspected signs
    for other_id in const.LIST_OBJECTS_VEDIC:
        if other_id != planet_id:
            other_planet = chart.getObject(other_id)
            other_sign = int(other_planet.lon / 30) % 12

            if other_sign in aspected_signs:
                # Calculate aspect strength based on the aspecting planet's strength
                from astrovedic.vedic.shadbala.sthana_bala import calculate_sthana_bala
                sthana_bala = calculate_sthana_bala(chart, other_id)
                strength_factor = sthana_bala['total'] / 300.0  # Normalize to 0-1
                virupa_points = 15.0 * strength_factor  # Base strength adjusted by planet's strength

                # Determine if the aspect is benefic or malefic
                is_benefic = is_benefic_planet(other_id)

                # Adjust the value based on benefic/malefic nature
                if is_benefic:
                    aspect_value += virupa_points
                else:
                    aspect_value -= virupa_points

                # Add to the list of aspects
                rashi_aspects.append({
                    'planet': other_id,
                    'virupa_points': virupa_points,
                    'is_benefic': is_benefic,
                    'sign': other_sign
                })

    return {
        'value': aspect_value,
        'aspects': rashi_aspects
    }


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
