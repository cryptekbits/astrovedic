"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements compatibility analysis for Vedic astrology.
    It includes functions to analyze Kuta (compatibility) factors,
    Dosha (affliction) analysis, and advanced compatibility tools.
"""

from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

from flatlib.vedic.compatibility.core import (
    get_compatibility_score, get_compatibility_factors,
    get_compatibility_description, get_compatibility_report
)

from flatlib.vedic.compatibility.kuta import (
    get_varna_kuta, get_vashya_kuta, get_tara_kuta,
    get_yoni_kuta, get_graha_maitri_kuta, get_gana_kuta,
    get_bhakoot_kuta, get_nadi_kuta, get_total_kuta_score
)

from flatlib.vedic.compatibility.dosha import (
    get_mangal_dosha, get_kuja_dosha, get_shani_dosha,
    get_grahan_dosha, get_dosha_cancellation, get_dosha_remedies
)

from flatlib.vedic.compatibility.dasha import (
    get_dasha_compatibility, get_antardasha_compatibility,
    get_dasha_periods_compatibility, get_dasha_predictions
)

from flatlib.vedic.compatibility.navamsa import (
    get_navamsa_compatibility, get_navamsa_positions,
    get_navamsa_aspects, get_navamsa_strength
)

from flatlib.vedic.compatibility.basic_analysis import (
    analyze_basic_compatibility
)

# Note: For detailed analysis, use the astroved_extension package

# Constants for compatibility levels
EXCELLENT = 'Excellent'
GOOD = 'Good'
AVERAGE = 'Average'
CHALLENGING = 'Challenging'
DIFFICULT = 'Difficult'

# List of compatibility levels
LIST_COMPATIBILITY_LEVELS = [
    EXCELLENT, GOOD, AVERAGE, CHALLENGING, DIFFICULT
]

# Constants for Kuta factors
VARNA_KUTA = 'Varna Kuta'
VASHYA_KUTA = 'Vashya Kuta'
TARA_KUTA = 'Tara Kuta'
YONI_KUTA = 'Yoni Kuta'
GRAHA_MAITRI_KUTA = 'Graha Maitri Kuta'
GANA_KUTA = 'Gana Kuta'
BHAKOOT_KUTA = 'Bhakoot Kuta'
NADI_KUTA = 'Nadi Kuta'

# List of Kuta factors
LIST_KUTA_FACTORS = [
    VARNA_KUTA, VASHYA_KUTA, TARA_KUTA, YONI_KUTA,
    GRAHA_MAITRI_KUTA, GANA_KUTA, BHAKOOT_KUTA, NADI_KUTA
]

# Constants for Dosha types
MANGAL_DOSHA = 'Mangal Dosha'
KUJA_DOSHA = 'Kuja Dosha'
SHANI_DOSHA = 'Shani Dosha'
GRAHAN_DOSHA = 'Grahan Dosha'

# List of Dosha types
LIST_DOSHA_TYPES = [
    MANGAL_DOSHA, KUJA_DOSHA, SHANI_DOSHA, GRAHAN_DOSHA
]


def get_moon_compatibility(chart1, chart2):
    """
    Get the compatibility between the Moon signs in two charts

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with Moon compatibility information
    """
    # Get the Moon signs
    moon1 = chart1.getObject(const.MOON)
    moon2 = chart2.getObject(const.MOON)

    # Calculate the distance between the Moon signs
    sign_distance = abs(const.LIST_SIGNS.index(moon1.sign) - const.LIST_SIGNS.index(moon2.sign))

    # Determine the compatibility level
    if sign_distance == 0:
        compatibility = "Excellent"
        score = 100
    elif sign_distance in [3, 6, 9]:
        compatibility = "Good"
        score = 75
    elif sign_distance in [5, 7]:
        compatibility = "Average"
        score = 50
    elif sign_distance in [2, 4, 8, 10]:
        compatibility = "Poor"
        score = 25
    else:  # 1, 11
        compatibility = "Very Poor"
        score = 0

    return {
        'sign1': moon1.sign,
        'sign2': moon2.sign,
        'distance': sign_distance,
        'compatibility': compatibility,
        'score': score
    }


def get_sun_compatibility(chart1, chart2):
    """
    Get the compatibility between the Sun signs in two charts

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with Sun compatibility information
    """
    # Get the Sun signs
    sun1 = chart1.getObject(const.SUN)
    sun2 = chart2.getObject(const.SUN)

    # Calculate the distance between the Sun signs
    sign_distance = abs(const.LIST_SIGNS.index(sun1.sign) - const.LIST_SIGNS.index(sun2.sign))

    # Determine the compatibility level
    if sign_distance == 0:
        compatibility = "Excellent"
        score = 100
    elif sign_distance in [4, 8]:
        compatibility = "Good"
        score = 75
    elif sign_distance in [3, 5, 9]:
        compatibility = "Average"
        score = 50
    elif sign_distance in [2, 6, 10]:
        compatibility = "Poor"
        score = 25
    else:  # 1, 7, 11
        compatibility = "Very Poor"
        score = 0

    return {
        'sign1': sun1.sign,
        'sign2': sun2.sign,
        'distance': sign_distance,
        'compatibility': compatibility,
        'score': score
    }


def get_ascendant_compatibility(chart1, chart2):
    """
    Get the compatibility between the Ascendant signs in two charts

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with Ascendant compatibility information
    """
    # Get the Ascendant signs
    asc1 = chart1.getAngle(const.ASC).sign
    asc2 = chart2.getAngle(const.ASC).sign

    # Calculate the distance between the Ascendant signs
    sign_distance = abs(const.LIST_SIGNS.index(asc1) - const.LIST_SIGNS.index(asc2))

    # Determine the compatibility level
    if sign_distance == 0:
        compatibility = "Excellent"
        score = 100
    elif sign_distance in [3, 6, 9, 11]:
        compatibility = "Good"
        score = 75
    elif sign_distance in [2, 5, 8]:
        compatibility = "Average"
        score = 50
    elif sign_distance in [4, 10]:
        compatibility = "Poor"
        score = 25
    else:  # 1, 7
        compatibility = "Very Poor"
        score = 0

    return {
        'sign1': asc1,
        'sign2': asc2,
        'distance': sign_distance,
        'compatibility': compatibility,
        'score': score
    }


def get_compatibility(chart1, chart2):
    """
    Get compatibility information between two charts

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with compatibility information
    """
    # Get the compatibility score
    score = get_compatibility_score(chart1, chart2)

    # Get the compatibility factors
    factors = get_compatibility_factors(chart1, chart2)

    # Get the Moon compatibility
    moon_compatibility = get_moon_compatibility(chart1, chart2)

    # Get the Sun compatibility
    sun_compatibility = get_sun_compatibility(chart1, chart2)

    # Get the Ascendant compatibility
    ascendant_compatibility = get_ascendant_compatibility(chart1, chart2)

    return {
        'overall_score': score,
        'factors': factors,
        'moon_compatibility': moon_compatibility,
        'sun_compatibility': sun_compatibility,
        'ascendant_compatibility': ascendant_compatibility
    }


def get_compatibility_level(score):
    """
    Get the compatibility level based on the score

    Args:
        score (float): The compatibility score (0-100)

    Returns:
        str: The compatibility level
    """
    if score >= 80:
        return EXCELLENT
    elif score >= 60:
        return GOOD
    elif score >= 40:
        return AVERAGE
    elif score >= 20:
        return CHALLENGING
    else:
        return DIFFICULT


def get_detailed_compatibility_report(chart1, chart2):
    """
    Get a detailed compatibility report between two charts
    Note: This function is deprecated. Use astroved_extension for detailed reports.

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with compatibility information
    """
    # Return basic compatibility information
    return analyze_basic_compatibility(chart1, chart2)


def get_compatibility_timeline(chart1, chart2, start_date, end_date):
    """
    Get a compatibility timeline for a specific period
    Note: This function is deprecated. Use astroved_extension for timeline analysis.

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart
        start_date (Datetime): The start date
        end_date (Datetime): The end date

    Returns:
        dict: Dictionary with basic compatibility information
    """
    # Return basic compatibility information
    return analyze_basic_compatibility(chart1, chart2)


def analyze_charts_compatibility(chart1, chart2):
    """
    Analyze the compatibility between two charts

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with basic compatibility information
    """
    return analyze_basic_compatibility(chart1, chart2)


def get_basic_compatibility_analysis(chart1, chart2):
    """
    Get basic compatibility analysis between two charts (alias for analyze_basic_compatibility)

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with basic compatibility analysis
    """
    return analyze_basic_compatibility(chart1, chart2)


def get_compatibility_timeline(chart1, chart2, start_date, end_date):
    """
    Get compatibility timeline between two charts

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart
        start_date (Datetime): The start date
        end_date (Datetime): The end date

    Returns:
        dict: Dictionary with compatibility timeline information
    """
    # Get the compatibility score
    score = get_compatibility_score(chart1, chart2)

    # Get the compatibility level
    level = get_compatibility_level(score)

    # Get the compatibility factors
    factors = get_compatibility_factors(chart1, chart2)

    # Get the kuta scores
    kuta_scores = {}
    for kuta_factor in LIST_KUTA_FACTORS:
        if kuta_factor == VARNA_KUTA:
            kuta_scores[kuta_factor] = get_varna_kuta(chart1, chart2)
        elif kuta_factor == VASHYA_KUTA:
            kuta_scores[kuta_factor] = get_vashya_kuta(chart1, chart2)
        elif kuta_factor == TARA_KUTA:
            kuta_scores[kuta_factor] = get_tara_kuta(chart1, chart2)
        elif kuta_factor == YONI_KUTA:
            kuta_scores[kuta_factor] = get_yoni_kuta(chart1, chart2)
        elif kuta_factor == GRAHA_MAITRI_KUTA:
            kuta_scores[kuta_factor] = get_graha_maitri_kuta(chart1, chart2)
        elif kuta_factor == GANA_KUTA:
            kuta_scores[kuta_factor] = get_gana_kuta(chart1, chart2)
        elif kuta_factor == BHAKOOT_KUTA:
            kuta_scores[kuta_factor] = get_bhakoot_kuta(chart1, chart2)
        elif kuta_factor == NADI_KUTA:
            kuta_scores[kuta_factor] = get_nadi_kuta(chart1, chart2)

    # Get the total kuta score
    total_kuta_score = get_total_kuta_score(kuta_scores)

    return {
        'score': score,
        'level': level,
        'kuta_scores': {'kuta_scores': kuta_scores, 'total_kuta_score': total_kuta_score},
        'events': [],
        'periods': []
    }
