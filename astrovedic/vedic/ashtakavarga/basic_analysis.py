"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements basic analysis tools for Ashtakavarga
    in Vedic astrology. For detailed analysis and reporting,
    use the astroved_extension package.
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


def get_ashtakavarga_bindu_summary(ashtakavarga_data):
    """
    Get a summary of Ashtakavarga bindu counts.

    Args:
        ashtakavarga_data (dict): Dictionary with Ashtakavarga data

    Returns:
        dict: Dictionary with Ashtakavarga bindu summary
    """
    # Initialize the result
    result = {
        'total_bindus': 0,
        'planet_bindus': {},
        'house_bindus': []
    }

    # Get the total bindus from Sarvashtakavarga
    sarva = ashtakavarga_data['sarvashtakavarga']
    result['total_bindus'] = sarva['total_bindus']

    # Get the bindus for each planet from Bhinnashtakavarga
    for planet_id, bhinna in ashtakavarga_data['bhinnashtakavarga'].items():
        result['planet_bindus'][planet_id] = bhinna['total_bindus']

    # Get the bindus in each house
    result['house_bindus'] = sarva['bindus_in_houses']

    return result


def get_basic_ashtakavarga_analysis(ashtakavarga_data):
    """
    Alias for get_ashtakavarga_bindu_summary for backward compatibility.

    Args:
        ashtakavarga_data (dict): Dictionary with Ashtakavarga data

    Returns:
        dict: Dictionary with Ashtakavarga bindu summary
    """
    return get_ashtakavarga_bindu_summary(ashtakavarga_data)
