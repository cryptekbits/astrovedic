"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements basic compatibility analysis
    for Vedic astrology. For detailed analysis and reporting,
    use the astroved_extension package.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos

from astrovedic.vedic.compatibility.core import (
    get_compatibility_score, get_compatibility_factors,
    get_compatibility_description, get_compatibility_report,
    get_compatibility_level
)

from astrovedic.vedic.compatibility.kuta import (
    get_all_kuta_scores
)

from astrovedic.vedic.compatibility.dosha import (
    get_mangal_dosha, get_kuja_dosha, get_shani_dosha,
    get_grahan_dosha, get_dosha_cancellation, get_dosha_remedies
)

from astrovedic.vedic.compatibility.dasha import (
    get_dasha_compatibility, get_antardasha_compatibility
)

from astrovedic.vedic.compatibility.navamsa import (
    get_navamsa_compatibility, get_navamsa_positions
)


def analyze_basic_compatibility(chart1, chart2):
    """
    Analyze the basic compatibility between two charts.
    For detailed analysis, use the astroved_extension package.

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with basic compatibility information
    """
    # Get the Kuta scores
    kuta_scores = get_all_kuta_scores(chart1, chart2)

    # Get the Dosha analysis
    dosha_analysis = {}
    dosha_analysis['Mangal Dosha'] = {
        'chart1': get_mangal_dosha(chart1),
        'chart2': get_mangal_dosha(chart2)
    }
    dosha_analysis['Kuja Dosha'] = {
        'chart1': get_kuja_dosha(chart1),
        'chart2': get_kuja_dosha(chart2)
    }

    # Get the Dosha cancellation
    dosha_cancellation = get_dosha_cancellation(chart1, chart2)

    # Get the Dasha compatibility
    dasha_compatibility = get_dasha_compatibility(chart1, chart2)

    # Get the Navamsa compatibility
    navamsa_compatibility = get_navamsa_compatibility(chart1, chart2)

    # Calculate the overall compatibility score
    score = get_compatibility_score(chart1, chart2)

    # Get the compatibility level
    level = get_compatibility_level(score)

    return {
        'score': score,
        'level': level,
        'kuta_scores': kuta_scores,
        'dosha_analysis': dosha_analysis,
        'dosha_cancellation': dosha_cancellation,
        'dasha_compatibility': dasha_compatibility,
        'navamsa_compatibility': navamsa_compatibility
    }
