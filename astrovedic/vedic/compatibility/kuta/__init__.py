"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Kuta (compatibility) calculations
    for Vedic astrology.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos

from astrovedic.vedic.compatibility.kuta.varna import get_varna_kuta
from astrovedic.vedic.compatibility.kuta.vashya import get_vashya_kuta
from astrovedic.vedic.compatibility.kuta.tara import get_tara_kuta
from astrovedic.vedic.compatibility.kuta.yoni import get_yoni_kuta
from astrovedic.vedic.compatibility.kuta.graha_maitri import get_graha_maitri_kuta
from astrovedic.vedic.compatibility.kuta.gana import get_gana_kuta
from astrovedic.vedic.compatibility.kuta.bhakoot import get_bhakoot_kuta
from astrovedic.vedic.compatibility.kuta.nadi import get_nadi_kuta
from astrovedic.vedic.compatibility.kuta.total import get_total_kuta_score as get_total_kuta_score_direct


def get_total_kuta_score(kuta_scores):
    """
    Calculate the total Kuta score

    Args:
        kuta_scores (dict): Dictionary with Kuta scores

    Returns:
        dict: Dictionary with total Kuta score information
    """
    # Initialize the total score
    total_score = 0
    max_total_score = 0

    # Add up the scores
    for kuta_name, kuta_info in kuta_scores.items():
        total_score += kuta_info['score']
        max_total_score += kuta_info['max_score']

    # Calculate the percentage
    percentage = (total_score / max_total_score) * 100 if max_total_score > 0 else 0

    return {
        'total_score': total_score,
        'max_total_score': max_total_score,
        'percentage': percentage
    }


def get_all_kuta_scores(chart1, chart2):
    """
    Get all Kuta scores

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with all Kuta scores
    """
    # Get the Kuta scores
    kuta_scores = {}
    kuta_scores['Varna Kuta'] = get_varna_kuta(chart1, chart2)
    kuta_scores['Vashya Kuta'] = get_vashya_kuta(chart1, chart2)
    kuta_scores['Tara Kuta'] = get_tara_kuta(chart1, chart2)
    kuta_scores['Yoni Kuta'] = get_yoni_kuta(chart1, chart2)
    kuta_scores['Graha Maitri Kuta'] = get_graha_maitri_kuta(chart1, chart2)
    kuta_scores['Gana Kuta'] = get_gana_kuta(chart1, chart2)
    kuta_scores['Bhakoot Kuta'] = get_bhakoot_kuta(chart1, chart2)
    kuta_scores['Nadi Kuta'] = get_nadi_kuta(chart1, chart2)

    # Get the total Kuta score
    total_kuta_score = get_total_kuta_score(kuta_scores)

    return {
        'kuta_scores': kuta_scores,
        'total_kuta_score': total_kuta_score
    }
