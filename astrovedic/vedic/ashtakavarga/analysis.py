"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements advanced analysis tools for Ashtakavarga
    in Vedic astrology.
"""

from astrovedic import const
from astrovedic import angle
from astrovedic.vedic.ashtakavarga.core import get_sign_number


def get_bindus_in_houses(chart, points):
    """
    Get the number of bindus in each house

    Args:
        chart (Chart): The birth chart
        points (list): List of 12 values representing points in each sign

    Returns:
        list: List of 12 values representing points in each house
    """
    # Get the Ascendant
    asc = chart.getAngle(const.ASC)

    # Get the Ascendant sign number (0-11)
    asc_sign_num = get_sign_number(asc.sign)

    # Initialize the result
    result = [0] * 12

    # Map the signs to houses
    for i in range(12):
        # Calculate the house number (0-11)
        house_num = (i - asc_sign_num) % 12

        # Add the points to the house
        result[house_num] = points[i]

    return result


def get_bindus_in_signs(points):
    """
    Get the number of bindus in each sign

    Args:
        points (list): List of 12 values representing points in each sign

    Returns:
        dict: Dictionary with sign names as keys and points as values
    """
    # List of signs
    signs = [
        const.ARIES, const.TAURUS, const.GEMINI, const.CANCER,
        const.LEO, const.VIRGO, const.LIBRA, const.SCORPIO,
        const.SAGITTARIUS, const.CAPRICORN, const.AQUARIUS, const.PISCES
    ]

    # Initialize the result
    result = {}

    # Map the points to signs
    for i in range(12):
        result[signs[i]] = points[i]

    return result


def get_ashtakavarga_strength_categories(ashtakavarga_data):
    """
    Get strength categories based on Ashtakavarga bindu counts

    Args:
        ashtakavarga_data (dict): Dictionary with Ashtakavarga data

    Returns:
        dict: Dictionary with strength categories
    """
    # Initialize the result
    result = {
        'total_strength': '',
        'planet_strength': {},
        'house_strength': {}
    }

    # Get the total bindus
    sarva = ashtakavarga_data['sarvashtakavarga']
    total_bindus = sarva['total_bindus']

    # Categorize total strength
    if total_bindus >= 300:
        result['total_strength'] = "Very Strong"
    elif total_bindus >= 250:
        result['total_strength'] = "Strong"
    elif total_bindus >= 200:
        result['total_strength'] = "Moderate"
    else:
        result['total_strength'] = "Weak"

    # Categorize planet strength
    for planet_id, bhinna in ashtakavarga_data['bhinnashtakavarga'].items():
        total_bindus = bhinna['total_bindus']

        if total_bindus >= 40:
            result['planet_strength'][planet_id] = "Very Strong"
        elif total_bindus >= 30:
            result['planet_strength'][planet_id] = "Strong"
        elif total_bindus >= 20:
            result['planet_strength'][planet_id] = "Moderate"
        else:
            result['planet_strength'][planet_id] = "Weak"

    # Categorize house strength
    bindus_in_houses = sarva['bindus_in_houses']

    for house_num in range(12):
        bindus = bindus_in_houses[house_num]

        if bindus >= 30:
            result['house_strength'][house_num + 1] = "Very Strong"
        elif bindus >= 25:
            result['house_strength'][house_num + 1] = "Strong"
        elif bindus >= 20:
            result['house_strength'][house_num + 1] = "Moderate"
        else:
            result['house_strength'][house_num + 1] = "Weak"

    return result


def get_ashtakavarga_planet_distances(chart1, chart2):
    """
    Calculate distances between planets in two charts based on Ashtakavarga

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with planet distance information
    """
    # List of planets used in Ashtakavarga
    planets = [const.SUN, const.MOON, const.MARS, const.MERCURY,
              const.JUPITER, const.VENUS, const.SATURN]

    # Initialize the result
    result = {
        'planet_distances': {},
        'total_score': 0,
        'max_score': 0,
        'percentage': 0
    }

    # Calculate distances for each planet
    for planet_id in planets:
        # Get the planet from each chart
        planet1 = chart1.getObject(planet_id)
        planet2 = chart2.getObject(planet_id)

        # Get the sign numbers (0-11)
        sign_num1 = get_sign_number(planet1.sign)
        sign_num2 = get_sign_number(planet2.sign)

        # Calculate the distance between the signs
        distance = min((sign_num2 - sign_num1) % 12, (sign_num1 - sign_num2) % 12)

        # Calculate the compatibility score (0-10)
        if distance == 0:
            score = 10  # Same sign
        elif distance == 1 or distance == 11:
            score = 2   # Adjacent signs
        elif distance == 2 or distance == 10:
            score = 4   # 2 signs apart
        elif distance == 3 or distance == 9:
            score = 6   # 3 signs apart
        elif distance == 4 or distance == 8:
            score = 8   # 4 signs apart
        elif distance == 5 or distance == 7:
            score = 5   # 5 signs apart
        else:  # distance == 6
            score = 0   # Opposite signs

        # Add to the result
        result['planet_distances'][planet_id] = {
            'sign1': planet1.sign,
            'sign2': planet2.sign,
            'distance': distance,
            'score': score
        }

        # Add to the total score
        result['total_score'] += score
        result['max_score'] += 10

    # Calculate the percentage
    result['percentage'] = (result['total_score'] / result['max_score']) * 100.0

    return result


def get_ashtakavarga_bindus_in_house(chart, house_num):
    """
    Calculate the Ashtakavarga bindus in a house

    Args:
        chart (Chart): The birth chart
        house_num (int): The house number (1-12)

    Returns:
        dict: Dictionary with house bindu information
    """
    # Adjust house number to 0-based index
    house_idx = house_num - 1

    # Get the Ascendant
    asc = chart.getAngle(const.ASC)

    # Get the Ascendant sign number (0-11)
    asc_sign_num = get_sign_number(asc.sign)

    # Calculate the sign number for this house
    sign_num = (asc_sign_num + house_idx) % 12

    # Get the sign for this house
    sign = get_sign_from_number(sign_num)

    # List of planets used in Ashtakavarga
    planets = [const.SUN, const.MOON, const.MARS, const.MERCURY,
              const.JUPITER, const.VENUS, const.SATURN]

    # Initialize the result
    result = {
        'house': house_num,
        'sign': sign,
        'total_bindus': 0,
        'planet_contributions': {}
    }

    # Calculate the contribution from each planet's Ashtakavarga
    from astrovedic.vedic.ashtakavarga.bhinna import get_benefic_points

    for planet_id in planets:
        # Get the benefic points
        benefic_points = get_benefic_points(chart, planet_id)

        # Get the contribution at this house's sign
        contribution = benefic_points[sign_num]

        # Add to the total
        result['total_bindus'] += contribution

        # Add to the contributions
        result['planet_contributions'][planet_id] = contribution

    # Calculate the percentage of maximum possible bindus (56)
    result['percentage'] = (result['total_bindus'] / 56.0) * 100.0

    return result


def get_sign_from_number(sign_num):
    """
    Get the sign from a sign number (0-11)

    Args:
        sign_num (int): The sign number (0-11)

    Returns:
        str: The sign
    """
    signs = [
        const.ARIES, const.TAURUS, const.GEMINI, const.CANCER,
        const.LEO, const.VIRGO, const.LIBRA, const.SCORPIO,
        const.SAGITTARIUS, const.CAPRICORN, const.AQUARIUS, const.PISCES
    ]

    return signs[sign_num % 12]
