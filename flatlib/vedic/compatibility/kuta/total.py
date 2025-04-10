"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements the total Kuta score calculation
    for compatibility analysis in Vedic astrology.
"""

from flatlib.chart import Chart
from flatlib.vedic.compatibility.kuta.varna import get_varna_kuta
from flatlib.vedic.compatibility.kuta.vashya import get_vashya_kuta
from flatlib.vedic.compatibility.kuta.tara import get_tara_kuta
from flatlib.vedic.compatibility.kuta.yoni import get_yoni_kuta
from flatlib.vedic.compatibility.kuta.graha_maitri import get_graha_maitri_kuta
from flatlib.vedic.compatibility.kuta.gana import get_gana_kuta
from flatlib.vedic.compatibility.kuta.bhakoot import get_bhakoot_kuta
from flatlib.vedic.compatibility.kuta.nadi import get_nadi_kuta


def get_total_kuta_score(chart1, chart2):
    """
    Calculate the total Kuta score for compatibility analysis
    
    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart
    
    Returns:
        dict: The total Kuta score
    """
    # Get all Kuta scores
    varna_kuta = get_varna_kuta(chart1, chart2)
    vashya_kuta = get_vashya_kuta(chart1, chart2)
    tara_kuta = get_tara_kuta(chart1, chart2)
    yoni_kuta = get_yoni_kuta(chart1, chart2)
    graha_maitri_kuta = get_graha_maitri_kuta(chart1, chart2)
    gana_kuta = get_gana_kuta(chart1, chart2)
    bhakoot_kuta = get_bhakoot_kuta(chart1, chart2)
    nadi_kuta = get_nadi_kuta(chart1, chart2)
    
    # Calculate total score
    total_score = (
        varna_kuta['score'] +
        vashya_kuta['score'] +
        tara_kuta['score'] +
        yoni_kuta['score'] +
        graha_maitri_kuta['score'] +
        gana_kuta['score'] +
        bhakoot_kuta['score'] +
        nadi_kuta['score']
    )
    
    # Calculate maximum score
    max_score = (
        varna_kuta['max_score'] +
        vashya_kuta['max_score'] +
        tara_kuta['max_score'] +
        yoni_kuta['max_score'] +
        graha_maitri_kuta['max_score'] +
        gana_kuta['max_score'] +
        bhakoot_kuta['max_score'] +
        nadi_kuta['max_score']
    )
    
    # Calculate percentage
    percentage = (total_score / max_score) * 100 if max_score > 0 else 0
    
    # Get description based on percentage
    if percentage >= 80:
        description = "Excellent compatibility. This match is highly favorable."
    elif percentage >= 60:
        description = "Good compatibility. This match is favorable."
    elif percentage >= 40:
        description = "Average compatibility. This match may have some challenges."
    elif percentage >= 20:
        description = "Below average compatibility. This match has significant challenges."
    else:
        description = "Poor compatibility. This match is not recommended."
    
    # Return result
    return {
        'score': total_score,
        'max_score': max_score,
        'percentage': percentage,
        'description': description,
        'varna_kuta': varna_kuta,
        'vashya_kuta': vashya_kuta,
        'tara_kuta': tara_kuta,
        'yoni_kuta': yoni_kuta,
        'graha_maitri_kuta': graha_maitri_kuta,
        'gana_kuta': gana_kuta,
        'bhakoot_kuta': bhakoot_kuta,
        'nadi_kuta': nadi_kuta
    }
