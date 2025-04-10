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

from flatlib.vedic.compatibility.analysis import (
    analyze_compatibility, get_detailed_compatibility_report,
    get_compatibility_timeline, get_compatibility_strength_score
)

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

    # Get the compatibility description
    description = get_compatibility_description(score, factors)

    # Get the Kuta scores
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

    # Get the total Kuta score
    total_kuta_score = get_total_kuta_score(kuta_scores)

    # Get the Dosha analysis
    dosha_analysis = {}
    dosha_analysis[MANGAL_DOSHA] = {
        'chart1': get_mangal_dosha(chart1),
        'chart2': get_mangal_dosha(chart2)
    }
    dosha_analysis[KUJA_DOSHA] = {
        'chart1': get_kuja_dosha(chart1),
        'chart2': get_kuja_dosha(chart2)
    }
    dosha_analysis[SHANI_DOSHA] = {
        'chart1': get_shani_dosha(chart1),
        'chart2': get_shani_dosha(chart2)
    }
    dosha_analysis[GRAHAN_DOSHA] = {
        'chart1': get_grahan_dosha(chart1),
        'chart2': get_grahan_dosha(chart2)
    }

    # Get the Dosha cancellation
    dosha_cancellation = get_dosha_cancellation(chart1, chart2)

    # Get the Dasha compatibility
    dasha_compatibility = get_dasha_compatibility(chart1, chart2)

    # Get the Navamsa compatibility
    navamsa_compatibility = get_navamsa_compatibility(chart1, chart2)

    return {
        'score': score,
        'level': get_compatibility_level(score),
        'description': description,
        'factors': factors,
        'kuta_scores': kuta_scores,
        'total_kuta_score': total_kuta_score,
        'dosha_analysis': dosha_analysis,
        'dosha_cancellation': dosha_cancellation,
        'dasha_compatibility': dasha_compatibility,
        'navamsa_compatibility': navamsa_compatibility
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

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with detailed compatibility report
    """
    from flatlib.vedic.compatibility.analysis import get_detailed_compatibility_report as get_detailed_report
    return get_detailed_report(chart1, chart2)


def get_compatibility_timeline(chart1, chart2, start_date, end_date):
    """
    Get a compatibility timeline for a specific period

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart
        start_date (Datetime): The start date
        end_date (Datetime): The end date

    Returns:
        list: List of compatibility events
    """
    from flatlib.vedic.compatibility.analysis import get_compatibility_timeline as get_timeline
    return get_timeline(chart1, chart2, start_date, end_date)


def analyze_charts_compatibility(chart1, chart2):
    """
    Analyze the compatibility between two charts

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with compatibility analysis
    """
    return analyze_compatibility(chart1, chart2)
