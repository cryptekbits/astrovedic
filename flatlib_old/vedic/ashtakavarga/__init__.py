"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Ashtakavarga (eight-source strength) calculations
    for Vedic astrology. It includes functions to calculate Bhinnashtakavarga
    (individual ashtakavarga) and Sarvashtakavarga (combined ashtakavarga).
"""

from flatlib import const
from flatlib.chart import Chart
from flatlib.vedic.ashtakavarga.core import (
    get_ashtakavarga_points, get_ashtakavarga_table,
    get_ashtakavarga_summary, get_ashtakavarga_strengths
)

# Import specific ashtakavarga calculation functions
from flatlib.vedic.ashtakavarga.bhinna import (
    calculate_bhinnashtakavarga, get_benefic_points,
    get_malefic_points, get_rekha_points
)
from flatlib.vedic.ashtakavarga.sarva import (
    calculate_sarvashtakavarga, get_trikona_sodhana,
    get_ekadhi_sodhana, get_sodhita_sarvashtakavarga
)
from flatlib.vedic.ashtakavarga.kaksha import (
    calculate_kaksha_bala, get_kaksha_strengths
)
from flatlib.vedic.ashtakavarga.transits import (
    get_transit_strength, get_best_transit_positions,
    get_ashtakavarga_dasha_phala
)
from flatlib.vedic.ashtakavarga.basic_analysis import (
    get_bindus_in_houses, get_bindus_in_signs,
    get_basic_ashtakavarga_analysis
)

# Note: For detailed analysis, use the astroved_extension package

# Constants for Ashtakavarga
BINDU = 1    # Favorable point
REKHA = 0    # Unfavorable point

# List of planets used in Ashtakavarga calculations
# Note: Rahu and Ketu are not included in traditional Ashtakavarga
LIST_ASHTAKAVARGA_PLANETS = [
    const.SUN, const.MOON, const.MERCURY, const.VENUS,
    const.MARS, const.JUPITER, const.SATURN
]

# Lagna (Ascendant) is also considered in Ashtakavarga
LAGNA = const.ASC


def get_bhinnashtakavarga(chart, planet_id):
    """
    Calculate Bhinnashtakavarga (individual ashtakavarga) for a planet

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet to analyze

    Returns:
        dict: Dictionary with Bhinnashtakavarga information
    """
    # Check if the planet is valid for Ashtakavarga
    if planet_id not in LIST_ASHTAKAVARGA_PLANETS:
        raise ValueError(f"Invalid planet for Ashtakavarga: {planet_id}")

    # Calculate Bhinnashtakavarga
    bhinna = calculate_bhinnashtakavarga(chart, planet_id)

    # Get the total number of benefic points
    total_bindus = sum(bhinna['points'])

    # Get the number of bindus in each house
    bindus_in_houses = get_bindus_in_houses(chart, bhinna['points'])

    # Get the number of bindus in each sign
    bindus_in_signs = get_bindus_in_signs(bhinna['points'])

    return {
        'planet': planet_id,
        'points': bhinna['points'],
        'contributors': bhinna['contributors'],
        'total_bindus': total_bindus,
        'bindus_in_houses': bindus_in_houses,
        'bindus_in_signs': bindus_in_signs
    }


def get_sarvashtakavarga(chart):
    """
    Calculate Sarvashtakavarga (combined ashtakavarga) for all planets

    Args:
        chart (Chart): The birth chart

    Returns:
        dict: Dictionary with Sarvashtakavarga information
    """
    # Calculate Sarvashtakavarga
    sarva = calculate_sarvashtakavarga(chart)

    # Get the total number of benefic points
    total_bindus = sum(sarva['points'])

    # Get the number of bindus in each house
    bindus_in_houses = get_bindus_in_houses(chart, sarva['points'])

    # Get the number of bindus in each sign
    bindus_in_signs = get_bindus_in_signs(sarva['points'])

    # Calculate Trikona Sodhana
    trikona_sodhana = get_trikona_sodhana(sarva['points'])

    # Calculate Ekadhi Sodhana
    ekadhi_sodhana = get_ekadhi_sodhana(sarva['points'])

    # Calculate Sodhita Sarvashtakavarga
    sodhita_sarva = get_sodhita_sarvashtakavarga(sarva['points'])

    return {
        'points': sarva['points'],
        'planet_contributions': sarva['planet_contributions'],
        'total_bindus': total_bindus,
        'bindus_in_houses': bindus_in_houses,
        'bindus_in_signs': bindus_in_signs,
        'trikona_sodhana': trikona_sodhana,
        'ekadhi_sodhana': ekadhi_sodhana,
        'sodhita_sarvashtakavarga': sodhita_sarva
    }


def get_all_ashtakavarga(chart):
    """
    Calculate all Ashtakavarga data for a chart

    Args:
        chart (Chart): The birth chart

    Returns:
        dict: Dictionary with all Ashtakavarga information
    """
    # Initialize the result dictionary
    result = {
        'bhinnashtakavarga': {},
        'sarvashtakavarga': None,
        'summary': None
    }

    # Calculate Bhinnashtakavarga for each planet
    for planet_id in LIST_ASHTAKAVARGA_PLANETS:
        result['bhinnashtakavarga'][planet_id] = get_bhinnashtakavarga(chart, planet_id)

    # Calculate Sarvashtakavarga
    result['sarvashtakavarga'] = get_sarvashtakavarga(chart)

    # Calculate summary information
    result['summary'] = get_ashtakavarga_summary(result)

    return result


def get_ashtakavarga_analysis(chart):
    """
    Analyze Ashtakavarga data for a chart
    Note: For detailed analysis, use the astroved_extension package

    Args:
        chart (Chart): The birth chart

    Returns:
        dict: Dictionary with basic Ashtakavarga analysis
    """
    # Get all Ashtakavarga data
    ashtakavarga_data = get_all_ashtakavarga(chart)

    # Get basic analysis
    analysis = get_basic_ashtakavarga_analysis(ashtakavarga_data)

    return analysis


def get_kaksha_bala(chart, planet_id):
    """
    Calculate Kaksha Bala (zodiacal strength) for a planet

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet to analyze

    Returns:
        dict: Dictionary with Kaksha Bala information
    """
    return calculate_kaksha_bala(chart, planet_id)


def get_transit_ashtakavarga(birth_chart, transit_chart, planet_id):
    """
    Calculate transit strength using Ashtakavarga

    Args:
        birth_chart (Chart): The birth chart
        transit_chart (Chart): The transit chart
        planet_id (str): The ID of the transiting planet

    Returns:
        dict: Dictionary with transit Ashtakavarga information
    """
    # Get the Bhinnashtakavarga for the planet
    bhinna = get_bhinnashtakavarga(birth_chart, planet_id)

    # Get the transit position
    transit_planet = transit_chart.getObject(planet_id)
    transit_sign_num = {
        const.ARIES: 0, const.TAURUS: 1, const.GEMINI: 2, const.CANCER: 3,
        const.LEO: 4, const.VIRGO: 5, const.LIBRA: 6, const.SCORPIO: 7,
        const.SAGITTARIUS: 8, const.CAPRICORN: 9, const.AQUARIUS: 10, const.PISCES: 11
    }[transit_planet.sign]

    # Get the transit strength
    transit_strength = get_transit_strength(bhinna['points'], transit_sign_num)

    # Get the best transit positions
    best_positions = get_best_transit_positions(bhinna['points'])

    return {
        'planet': planet_id,
        'transit_sign': transit_planet.sign,
        'transit_strength': transit_strength,
        'best_positions': best_positions
    }


def get_ashtakavarga(chart):
    """
    Get all Ashtakavarga data for a chart (alias for get_all_ashtakavarga)

    Args:
        chart (Chart): The birth chart

    Returns:
        dict: Dictionary with all Ashtakavarga information
    """
    return get_all_ashtakavarga(chart)


def get_bindu_score(chart, planet_id, sign_num):
    """
    Get the bindu score for a planet in a sign

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet
        sign_num (int): The sign number (0-11)

    Returns:
        int: The bindu score (0-8)
    """
    # Get the Bhinnashtakavarga for the planet
    bhinna = get_bhinnashtakavarga(chart, planet_id)

    # Return the bindu score for the sign
    return bhinna['points'][sign_num]


def get_kaksha(chart, planet_id):
    """
    Get the kaksha (zodiacal division) of a planet

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet

    Returns:
        dict: Dictionary with kaksha information
    """
    return get_kaksha_bala(chart, planet_id)
