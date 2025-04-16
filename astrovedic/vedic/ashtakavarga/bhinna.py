"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Bhinnashtakavarga (individual ashtakavarga) calculations
    for Vedic astrology.
"""

from astrovedic import const
from astrovedic.vedic.ashtakavarga.core import (
    get_ashtakavarga_points, get_ashtakavarga_table,
    get_sign_number
)


def calculate_bhinnashtakavarga(chart, planet_id):
    """
    Calculate Bhinnashtakavarga (individual ashtakavarga) for a planet

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet to analyze

    Returns:
        dict: Dictionary with Bhinnashtakavarga information
    """
    # Get the Ashtakavarga table
    table = get_ashtakavarga_table(chart, planet_id)

    # Get the contributors
    contributors = [const.SUN, const.MOON, const.MARS, const.MERCURY,
                   const.JUPITER, const.VENUS, const.SATURN, const.ASC]

    # Initialize the result
    result = {
        'planet': planet_id,
        'points': table['totals'],
        'contributors': {}
    }

    # Add the contribution from each planet
    for contributor_id in contributors:
        result['contributors'][contributor_id] = table['contributors'][contributor_id]

    return result


def get_benefic_points(chart, planet_id):
    """
    Get the benefic points (bindus) for a planet in each sign

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet to analyze

    Returns:
        list: List of benefic points (0-8) for each sign
    """
    # Calculate Bhinnashtakavarga
    bhinna = calculate_bhinnashtakavarga(chart, planet_id)

    # Return the points
    return bhinna['points']


def get_malefic_points(chart, planet_id):
    """
    Get the malefic points (rekhas) for a planet in each sign

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet to analyze

    Returns:
        list: List of malefic points (0-8) for each sign
    """
    # Calculate Bhinnashtakavarga
    bhinna = calculate_bhinnashtakavarga(chart, planet_id)

    # Calculate the malefic points (8 - benefic points)
    malefic_points = [8 - point for point in bhinna['points']]

    return malefic_points


def get_rekha_points(chart, planet_id):
    """
    Get the rekha points (malefic points) for a planet in each sign

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet to analyze

    Returns:
        list: List of rekha points (0-8) for each sign
    """
    # This is the same as get_malefic_points
    return get_malefic_points(chart, planet_id)


def get_planet_contribution(chart, planet_id, contributor_id):
    """
    Get the contribution of one planet to another in Ashtakavarga

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet receiving the points
        contributor_id (str): The ID of the planet contributing the points

    Returns:
        list: List of 12 values (0 or 1) representing points in each sign
    """
    return get_ashtakavarga_points(chart, planet_id, contributor_id)


def get_planet_in_own_ashtakavarga(chart, planet_id):
    """
    Get the strength of a planet in its own Ashtakavarga

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet to analyze

    Returns:
        int: The strength (0-1) of the planet in its own Ashtakavarga
    """
    # Get the planet from the chart
    planet = chart.getObject(planet_id)

    # Get the sign number (0-11)
    sign_num = get_sign_number(planet.sign)

    # Get the planet's contribution to its own Ashtakavarga
    contribution = get_planet_contribution(chart, planet_id, planet_id)

    # Return the value at the planet's sign
    return contribution[sign_num]


def get_bindus_at_planet(chart, planet_id, target_planet_id):
    """
    Get the number of bindus at a planet's position in another planet's Ashtakavarga

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet whose Ashtakavarga to analyze
        target_planet_id (str): The ID of the planet whose position to check

    Returns:
        int: The number of bindus (0-8) at the target planet's position
    """
    # Get the target planet from the chart
    target_planet = chart.getObject(target_planet_id)

    # Get the sign number (0-11)
    sign_num = get_sign_number(target_planet.sign)

    # Get the benefic points
    benefic_points = get_benefic_points(chart, planet_id)

    # Return the value at the target planet's sign
    return benefic_points[sign_num]
