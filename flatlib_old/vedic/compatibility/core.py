"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements core functionality for compatibility analysis
    in Vedic astrology.
"""

from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import angle

# Import Kuta functions
from flatlib.vedic.compatibility.kuta import (
    get_varna_kuta, get_vashya_kuta, get_tara_kuta,
    get_yoni_kuta, get_graha_maitri_kuta, get_gana_kuta,
    get_bhakoot_kuta, get_nadi_kuta
)
from flatlib.vedic.compatibility.kuta.total import get_total_kuta_score

# Import Dosha functions
from flatlib.vedic.compatibility.dosha import (
    get_mangal_dosha, get_kuja_dosha, get_shani_dosha,
    get_grahan_dosha, get_dosha_cancellation, get_dosha_remedies
)

# Import Dasha functions
from flatlib.vedic.compatibility.dasha import (
    get_dasha_compatibility, get_antardasha_compatibility,
    get_dasha_periods_compatibility, get_dasha_predictions
)

# Import Navamsa functions
from flatlib.vedic.compatibility.navamsa import (
    get_navamsa_compatibility, get_navamsa_positions,
    get_navamsa_aspects, get_navamsa_strength
)


def get_compatibility_score(chart1, chart2):
    """
    Calculate the overall compatibility score between two charts

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        float: The compatibility score (0-100)
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
    total_kuta_score = get_total_kuta_score(chart1, chart2)

    # Get the Dosha analysis
    mangal_dosha1 = get_mangal_dosha(chart1)
    mangal_dosha2 = get_mangal_dosha(chart2)
    kuja_dosha1 = get_kuja_dosha(chart1)
    kuja_dosha2 = get_kuja_dosha(chart2)

    # Check for Dosha cancellation
    dosha_cancellation = get_dosha_cancellation(chart1, chart2)

    # Get the Dasha compatibility
    dasha_compatibility = get_dasha_compatibility(chart1, chart2)

    # Get the Navamsa compatibility
    navamsa_compatibility = get_navamsa_compatibility(chart1, chart2)

    # Calculate the overall score

    # Kuta score (0-36) converted to 0-70 scale
    kuta_score_normalized = (total_kuta_score['score'] / 36) * 70

    # Dosha score (0-10)
    dosha_score = 10
    if (mangal_dosha1['has_dosha'] and mangal_dosha2['has_dosha']) or \
       (kuja_dosha1['has_dosha'] and kuja_dosha2['has_dosha']):
        dosha_score -= 5
    elif mangal_dosha1['has_dosha'] or mangal_dosha2['has_dosha'] or \
         kuja_dosha1['has_dosha'] or kuja_dosha2['has_dosha']:
        dosha_score -= 2

    # Add points for Dosha cancellation
    if dosha_cancellation['is_cancelled']:
        dosha_score += 5

    # Dasha compatibility score (0-10)
    dasha_score = dasha_compatibility['score'] / 10

    # Navamsa compatibility score (0-10)
    navamsa_score = navamsa_compatibility['score'] / 10

    # Calculate the overall score
    overall_score = kuta_score_normalized + dosha_score + dasha_score + navamsa_score

    # Ensure the score is between 0 and 100
    overall_score = min(100, max(0, overall_score))

    return overall_score


def get_compatibility_factors(chart1, chart2):
    """
    Get the compatibility factors between two charts

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        list: List of compatibility factors
    """
    factors = []

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

    # Add factors for each Kuta
    for kuta_name, kuta_info in kuta_scores.items():
        if kuta_info['score'] >= kuta_info['max_score'] * 0.8:
            factors.append(f"Strong {kuta_name}: {kuta_info['description']}")
        elif kuta_info['score'] <= kuta_info['max_score'] * 0.2:
            factors.append(f"Weak {kuta_name}: {kuta_info['description']}")

    # Get the Dosha analysis
    mangal_dosha1 = get_mangal_dosha(chart1)
    mangal_dosha2 = get_mangal_dosha(chart2)
    kuja_dosha1 = get_kuja_dosha(chart1)
    kuja_dosha2 = get_kuja_dosha(chart2)

    # Add factors for Doshas
    if mangal_dosha1['has_dosha']:
        factors.append(f"Person 1 has Mangal Dosha: {mangal_dosha1['description']}")
    if mangal_dosha2['has_dosha']:
        factors.append(f"Person 2 has Mangal Dosha: {mangal_dosha2['description']}")
    if kuja_dosha1['has_dosha']:
        factors.append(f"Person 1 has Kuja Dosha: {kuja_dosha1['description']}")
    if kuja_dosha2['has_dosha']:
        factors.append(f"Person 2 has Kuja Dosha: {kuja_dosha2['description']}")

    # Check for Dosha cancellation
    dosha_cancellation = get_dosha_cancellation(chart1, chart2)
    if dosha_cancellation['is_cancelled']:
        factors.append(f"Dosha Cancellation: {dosha_cancellation['description']}")

    # Get the Dasha compatibility
    dasha_compatibility = get_dasha_compatibility(chart1, chart2)
    if dasha_compatibility['score'] >= 8:
        factors.append(f"Strong Dasha Compatibility: {dasha_compatibility['description']}")
    elif dasha_compatibility['score'] <= 3:
        factors.append(f"Weak Dasha Compatibility: {dasha_compatibility['description']}")

    # Get the Navamsa compatibility
    navamsa_compatibility = get_navamsa_compatibility(chart1, chart2)
    if navamsa_compatibility['score'] >= 8:
        factors.append(f"Strong Navamsa Compatibility: {navamsa_compatibility['description']}")
    elif navamsa_compatibility['score'] <= 3:
        factors.append(f"Weak Navamsa Compatibility: {navamsa_compatibility['description']}")

    return factors


def get_compatibility_description(chart1, chart2):
    """
    Generate a description of the compatibility between two charts

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        str: The compatibility description
    """
    # Calculate the compatibility score
    score = get_compatibility_score(chart1, chart2)

    # Get the compatibility factors
    factors = get_compatibility_factors(chart1, chart2)

    # Call the internal function to generate the description
    return _get_compatibility_description(score, factors)


def _get_compatibility_description(score, factors):
    """
    Generate a description of the compatibility based on the score and factors

    Args:
        score (float): The compatibility score (0-100)
        factors (list): List of compatibility factors

    Returns:
        str: The compatibility description
    """
    # Generate a description based on the score
    if score >= 80:
        description = "This is an excellent match with strong compatibility. The relationship is likely to be harmonious and fulfilling."
    elif score >= 60:
        description = "This is a good match with positive compatibility. The relationship has strong potential for success with some effort."
    elif score >= 40:
        description = "This is an average match with moderate compatibility. The relationship may face challenges but can succeed with understanding and compromise."
    elif score >= 20:
        description = "This is a challenging match with difficult compatibility. The relationship may face significant obstacles and require substantial effort."
    else:
        description = "This is a difficult match with poor compatibility. The relationship may face severe challenges and may not be advisable."

    # Add information about the main factors
    if factors:
        description += "\n\nKey factors:"
        for i, factor in enumerate(factors[:5]):  # Include up to 5 factors
            description += f"\n- {factor}"

    return description


def get_compatibility_report(chart1, chart2):
    """
    Generate a detailed compatibility report between two charts

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with detailed compatibility report
    """
    # Get the compatibility score
    score = get_compatibility_score(chart1, chart2)

    # Get the compatibility factors
    factors = get_compatibility_factors(chart1, chart2)

    # Get the compatibility description
    description = _get_compatibility_description(score, factors)

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
    total_kuta_score = get_total_kuta_score(chart1, chart2)

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
    dosha_analysis['Shani Dosha'] = {
        'chart1': get_shani_dosha(chart1),
        'chart2': get_shani_dosha(chart2)
    }
    dosha_analysis['Grahan Dosha'] = {
        'chart1': get_grahan_dosha(chart1),
        'chart2': get_grahan_dosha(chart2)
    }

    # Get the Dosha cancellation
    dosha_cancellation = get_dosha_cancellation(chart1, chart2)

    # Get the Dosha remedies
    dosha_remedies = get_dosha_remedies(chart1, chart2)

    # Get the Dasha compatibility
    dasha_compatibility = get_dasha_compatibility(chart1, chart2)

    # Get the Antardasha compatibility
    antardasha_compatibility = get_antardasha_compatibility(chart1, chart2)

    # Get the Dasha periods compatibility
    dasha_periods_compatibility = get_dasha_periods_compatibility(chart1, chart2)

    # Get the Dasha predictions
    dasha_predictions = get_dasha_predictions(chart1, chart2)

    # Get the Navamsa compatibility
    navamsa_compatibility = get_navamsa_compatibility(chart1, chart2)

    # Get the Navamsa positions
    navamsa_positions = {
        'chart1': get_navamsa_positions(chart1),
        'chart2': get_navamsa_positions(chart2)
    }

    # Get the Navamsa aspects
    navamsa_aspects = get_navamsa_aspects(chart1, chart2)

    # Get the Navamsa strength
    navamsa_strength = {
        'chart1': get_navamsa_strength(chart1),
        'chart2': get_navamsa_strength(chart2)
    }

    # Create a kuta object for backward compatibility
    kuta = {
        'scores': kuta_scores,
        'total': total_kuta_score
    }

    # Create a dosha object for backward compatibility
    dosha = {
        'analysis': dosha_analysis,
        'cancellation': dosha_cancellation,
        'remedies': dosha_remedies
    }

    # Create a dasha object for backward compatibility
    dasha = {
        'compatibility': dasha_compatibility,
        'antardasha_compatibility': antardasha_compatibility,
        'periods_compatibility': dasha_periods_compatibility,
        'predictions': dasha_predictions
    }

    # Create a navamsa object for backward compatibility
    navamsa = {
        'compatibility': navamsa_compatibility,
        'positions': navamsa_positions,
        'aspects': navamsa_aspects,
        'strength': navamsa_strength
    }

    return {
        'score': score,
        'level': get_compatibility_level(score),
        'description': description,
        'factors': factors,
        'kuta': kuta,  # Add the kuta key for backward compatibility
        'dosha': dosha,  # Add the dosha key for backward compatibility
        'dasha': dasha,  # Add the dasha key for backward compatibility
        'navamsa': navamsa,  # Add the navamsa key for backward compatibility
        'kuta_scores': kuta_scores,
        'total_kuta_score': total_kuta_score,
        'dosha_analysis': dosha_analysis,
        'dosha_cancellation': dosha_cancellation,
        'dosha_remedies': dosha_remedies,
        'dasha_compatibility': dasha_compatibility,
        'antardasha_compatibility': antardasha_compatibility,
        'dasha_periods_compatibility': dasha_periods_compatibility,
        'dasha_predictions': dasha_predictions,
        'navamsa_compatibility': navamsa_compatibility,
        'navamsa_positions': navamsa_positions,
        'navamsa_aspects': navamsa_aspects,
        'navamsa_strength': navamsa_strength
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
        return 'Excellent'
    elif score >= 60:
        return 'Good'
    elif score >= 40:
        return 'Average'
    elif score >= 20:
        return 'Challenging'
    else:
        return 'Difficult'
