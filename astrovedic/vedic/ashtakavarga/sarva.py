"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Sarvashtakavarga (combined ashtakavarga) calculations
    for Vedic astrology.
"""

from astrovedic import const
from astrovedic.vedic.ashtakavarga.bhinna import calculate_bhinnashtakavarga


def calculate_sarvashtakavarga(chart):
    """
    Calculate Sarvashtakavarga (combined ashtakavarga) for all planets

    Args:
        chart (Chart): The birth chart

    Returns:
        dict: Dictionary with Sarvashtakavarga information
    """
    # List of planets used in Ashtakavarga
    planets = [const.SUN, const.MOON, const.MARS, const.MERCURY,
              const.JUPITER, const.VENUS, const.SATURN]

    # Initialize the result
    result = {
        'points': [0] * 12,
        'planet_contributions': {}
    }

    # Calculate Bhinnashtakavarga for each planet and add to the total
    for planet_id in planets:
        bhinna = calculate_bhinnashtakavarga(chart, planet_id)

        # Add to the total
        for i in range(12):
            result['points'][i] += bhinna['points'][i]

        # Add to the planet contributions
        result['planet_contributions'][planet_id] = bhinna['points']

    # No manual adjustments needed

    return result


def get_trikona_sodhana(sarva_points):
    """
    Calculate Trikona Sodhana (triangular reduction) for Sarvashtakavarga

    Trikona Sodhana reduces the Sarvashtakavarga points by considering
    the triangular relationship between signs (1-5-9, 2-6-10, 3-7-11, 4-8-12).

    Args:
        sarva_points (list): List of 12 values representing Sarvashtakavarga points

    Returns:
        list: List of 12 values after Trikona Sodhana
    """
    # Initialize the result with a copy of the original points
    result = sarva_points.copy()

    # Apply Trikona Sodhana for each triangular relationship
    for i in range(4):
        # Get the three signs in this triangular relationship
        sign1 = i
        sign2 = (i + 4) % 12
        sign3 = (i + 8) % 12

        # Find the minimum value among the three signs
        min_value = min(result[sign1], result[sign2], result[sign3])

        # Subtract the minimum value from all three signs
        result[sign1] -= min_value
        result[sign2] -= min_value
        result[sign3] -= min_value

    return result


def get_ekadhi_sodhana(sarva_points):
    """
    Calculate Ekadhi Sodhana (one-to-one reduction) for Sarvashtakavarga

    Ekadhi Sodhana reduces the Sarvashtakavarga points by considering
    the one-to-one relationship between opposite signs (1-7, 2-8, 3-9, etc.).

    Args:
        sarva_points (list): List of 12 values representing Sarvashtakavarga points

    Returns:
        list: List of 12 values after Ekadhi Sodhana
    """
    # Initialize the result with a copy of the original points
    result = sarva_points.copy()

    # Apply Ekadhi Sodhana for each pair of opposite signs
    for i in range(6):
        # Get the two signs in this opposite relationship
        sign1 = i
        sign2 = (i + 6) % 12

        # Find the minimum value between the two signs
        min_value = min(result[sign1], result[sign2])

        # Subtract the minimum value from both signs
        result[sign1] -= min_value
        result[sign2] -= min_value

    return result


def get_sodhita_sarvashtakavarga(sarva_points):
    """
    Calculate Sodhita Sarvashtakavarga (reduced combined ashtakavarga)

    Sodhita Sarvashtakavarga is calculated by applying both Trikona Sodhana
    and Ekadhi Sodhana to the Sarvashtakavarga points.

    Args:
        sarva_points (list): List of 12 values representing Sarvashtakavarga points

    Returns:
        list: List of 12 values after both reductions
    """
    # Apply Trikona Sodhana
    trikona_sodhana = get_trikona_sodhana(sarva_points)

    # Apply Ekadhi Sodhana to the result of Trikona Sodhana
    sodhita_sarva = get_ekadhi_sodhana(trikona_sodhana)

    return sodhita_sarva


def get_prastara_ashtakavarga(chart):
    """
    Calculate Prastara Ashtakavarga (detailed ashtakavarga table)

    Prastara Ashtakavarga shows the contribution of each planet to each sign
    in a detailed table format.

    Args:
        chart (Chart): The birth chart

    Returns:
        dict: Dictionary with Prastara Ashtakavarga information
    """
    # List of planets used in Ashtakavarga
    planets = [const.SUN, const.MOON, const.MARS, const.MERCURY,
              const.JUPITER, const.VENUS, const.SATURN]

    # List of contributors
    contributors = [const.SUN, const.MOON, const.MARS, const.MERCURY,
                   const.JUPITER, const.VENUS, const.SATURN, const.ASC]

    # Initialize the result
    result = {
        'signs': [const.ARIES, const.TAURUS, const.GEMINI, const.CANCER,
                 const.LEO, const.VIRGO, const.LIBRA, const.SCORPIO,
                 const.SAGITTARIUS, const.CAPRICORN, const.AQUARIUS, const.PISCES],
        'planets': planets,
        'contributors': contributors,
        'data': {}
    }

    # Calculate Bhinnashtakavarga for each planet
    for planet_id in planets:
        bhinna = calculate_bhinnashtakavarga(chart, planet_id)

        # Add to the data
        result['data'][planet_id] = {
            'points': bhinna['points'],
            'contributors': bhinna['contributors']
        }

    return result


def get_sarvashtakavarga_bindus_for_sign(sarva_points, sign):
    """
    Get the Sarvashtakavarga bindus for a specific sign

    Args:
        sarva_points (list): List of 12 values representing Sarvashtakavarga points
        sign (str): The sign to check

    Returns:
        int: The number of bindus for the sign
    """
    # Get the sign number (0-11)
    sign_numbers = {
        const.ARIES: 0,
        const.TAURUS: 1,
        const.GEMINI: 2,
        const.CANCER: 3,
        const.LEO: 4,
        const.VIRGO: 5,
        const.LIBRA: 6,
        const.SCORPIO: 7,
        const.SAGITTARIUS: 8,
        const.CAPRICORN: 9,
        const.AQUARIUS: 10,
        const.PISCES: 11
    }

    sign_num = sign_numbers.get(sign, 0)

    # Return the bindus for the sign
    return sarva_points[sign_num]
