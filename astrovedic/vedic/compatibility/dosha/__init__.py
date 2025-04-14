"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Dosha (affliction) analysis
    for Vedic astrology.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos

from astrovedic.vedic.compatibility.dosha.mangal import get_mangal_dosha
from astrovedic.vedic.compatibility.dosha.kuja import get_kuja_dosha
from astrovedic.vedic.compatibility.dosha.shani import get_shani_dosha
from astrovedic.vedic.compatibility.dosha.grahan import get_grahan_dosha
from astrovedic.vedic.compatibility.dosha.kalasarpa import get_kalasarpa_dosha


def get_dosha_cancellation(chart1, chart2):
    """
    Check if Doshas are cancelled between two charts

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with Dosha cancellation information
    """
    # Get the Doshas for each chart
    mangal_dosha1 = get_mangal_dosha(chart1)
    mangal_dosha2 = get_mangal_dosha(chart2)
    kuja_dosha1 = get_kuja_dosha(chart1)
    kuja_dosha2 = get_kuja_dosha(chart2)
    shani_dosha1 = get_shani_dosha(chart1)
    shani_dosha2 = get_shani_dosha(chart2)
    grahan_dosha1 = get_grahan_dosha(chart1)
    grahan_dosha2 = get_grahan_dosha(chart2)
    kalasarpa_dosha1 = get_kalasarpa_dosha(chart1)
    kalasarpa_dosha2 = get_kalasarpa_dosha(chart2)

    # Check if both have the same Dosha
    both_have_mangal = mangal_dosha1['has_dosha'] and mangal_dosha2['has_dosha']
    both_have_kuja = kuja_dosha1['has_dosha'] and kuja_dosha2['has_dosha']
    both_have_shani = shani_dosha1['has_dosha'] and shani_dosha2['has_dosha']
    both_have_grahan = grahan_dosha1['has_dosha'] and grahan_dosha2['has_dosha']
    both_have_kalasarpa = kalasarpa_dosha1['has_dosha'] and kalasarpa_dosha2['has_dosha']

    # Check for cancellation
    is_cancelled = both_have_mangal or both_have_kuja or both_have_shani or both_have_grahan or both_have_kalasarpa

    return {
        'is_cancelled': is_cancelled,
        'both_have_mangal': both_have_mangal,
        'both_have_kuja': both_have_kuja,
        'both_have_shani': both_have_shani,
        'both_have_grahan': both_have_grahan,
        'both_have_kalasarpa': both_have_kalasarpa,
        'mangal_dosha_cancelled': both_have_mangal,
        'kuja_dosha_cancelled': both_have_kuja,
        'shani_dosha_cancelled': both_have_shani,
        'grahan_dosha_cancelled': both_have_grahan,
        'kalasarpa_dosha_cancelled': both_have_kalasarpa
    }



