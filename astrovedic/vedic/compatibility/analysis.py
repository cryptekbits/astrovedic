"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements advanced compatibility analysis
    for Vedic astrology.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from datetime import timedelta

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
    get_grahan_dosha, get_dosha_cancellation
)

from astrovedic.vedic.compatibility.dasha import (
    get_dasha_compatibility
)

from astrovedic.vedic.compatibility.navamsa import (
    get_navamsa_compatibility, get_navamsa_positions,
    get_navamsa_aspects, get_navamsa_strength
)


def get_compatibility_data_summary(kuta_scores, dosha_analysis, dosha_cancellation, dasha_compatibility, navamsa_compatibility):
    """Get a summary of compatibility data.

    Args:
        kuta_scores (dict): The Kuta scores
        dosha_analysis (dict): The Dosha analysis
        dosha_cancellation (dict): The Dosha cancellation
        dasha_compatibility (dict): The Dasha compatibility
        navamsa_compatibility (dict): The Navamsa compatibility

    Returns:
        dict: A summary of compatibility data
    """
    summary = {
        'kuta_percentage': 0,
        'dosha_status': {
            'mangal_dosha': {'chart1': False, 'chart2': False},
            'kuja_dosha': {'chart1': False, 'chart2': False},
            'shani_dosha': {'chart1': False, 'chart2': False},
            'grahan_dosha': {'chart1': False, 'chart2': False}
        },
        'dosha_cancellation': False,
        'dasha_score': 0,
        'navamsa_score': 0
    }

    # Get Kuta percentage
    if 'total_kuta_score' in kuta_scores:
        summary['kuta_percentage'] = kuta_scores['total_kuta_score']['percentage']

    # Get Dosha status
    if 'Mangal Dosha' in dosha_analysis:
        summary['dosha_status']['mangal_dosha']['chart1'] = dosha_analysis['Mangal Dosha']['chart1']['has_dosha']
        summary['dosha_status']['mangal_dosha']['chart2'] = dosha_analysis['Mangal Dosha']['chart2']['has_dosha']

    if 'Kuja Dosha' in dosha_analysis:
        summary['dosha_status']['kuja_dosha']['chart1'] = dosha_analysis['Kuja Dosha']['chart1']['has_dosha']
        summary['dosha_status']['kuja_dosha']['chart2'] = dosha_analysis['Kuja Dosha']['chart2']['has_dosha']

    if 'Shani Dosha' in dosha_analysis:
        summary['dosha_status']['shani_dosha']['chart1'] = dosha_analysis['Shani Dosha']['chart1']['has_dosha']
        summary['dosha_status']['shani_dosha']['chart2'] = dosha_analysis['Shani Dosha']['chart2']['has_dosha']

    if 'Grahan Dosha' in dosha_analysis:
        summary['dosha_status']['grahan_dosha']['chart1'] = dosha_analysis['Grahan Dosha']['chart1']['has_dosha']
        summary['dosha_status']['grahan_dosha']['chart2'] = dosha_analysis['Grahan Dosha']['chart2']['has_dosha']

    # Get Dosha cancellation
    summary['dosha_cancellation'] = dosha_cancellation['is_cancelled']

    # Get Dasha score
    if 'score' in dasha_compatibility:
        summary['dasha_score'] = dasha_compatibility['score']

    # Get Navamsa score
    if 'score' in navamsa_compatibility:
        summary['navamsa_score'] = navamsa_compatibility['score']

    return summary


def analyze_compatibility(chart1, chart2):
    """
    Analyze the compatibility between two charts

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with compatibility analysis
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

    # Dosha remedies are no longer used

    # Get the Dasha compatibility
    dasha_compatibility = get_dasha_compatibility(chart1, chart2)

    # Get the Dasha periods data
    dasha_periods_data = get_dasha_period_data(chart1, chart2, chart1.date)

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

    # Calculate the overall compatibility score
    overall_score = calculate_overall_compatibility_score(
        kuta_scores, dosha_analysis, dosha_cancellation,
        dasha_compatibility, navamsa_compatibility
    )

    # Get compatibility data summary
    factors = get_compatibility_data_summary(
        kuta_scores, dosha_analysis, dosha_cancellation,
        dasha_compatibility, navamsa_compatibility
    )

    # Get the compatibility summary
    compatibility_summary = get_compatibility_summary(
        overall_score, factors
    )

    return {
        'score': overall_score,  # For backward compatibility
        'factors': factors,  # For backward compatibility
        'overall_score': overall_score,
        'compatibility_summary': compatibility_summary,
        'kuta_scores': kuta_scores,
        'dosha_analysis': dosha_analysis,
        'dosha_cancellation': dosha_cancellation,
        'dasha_compatibility': dasha_compatibility,
        'dasha_periods_data': dasha_periods_data,
        'navamsa_compatibility': navamsa_compatibility,
        'navamsa_positions': navamsa_positions,
        'navamsa_aspects': navamsa_aspects,
        'navamsa_strength': navamsa_strength
    }


def get_detailed_compatibility_data(chart1, chart2):
    """
    Get detailed compatibility data between two charts

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with detailed compatibility data
    """
    # Get the compatibility analysis
    analysis = analyze_compatibility(chart1, chart2)

    # Create the data structure
    data = {
        'overall': {
            'score': analysis['overall_score'],
            'level': get_compatibility_level(analysis['overall_score'])
        },
        'kuta': {
            'scores': analysis['kuta_scores']['kuta_scores'],
            'total_score': analysis['kuta_scores']['total_kuta_score']
        },
        'dosha': {
            'analysis': analysis['dosha_analysis'],
            'cancellation': analysis['dosha_cancellation']
        },
        'dasha': {
            'compatibility': analysis['dasha_compatibility'],
            'timeline': analysis['dasha_periods_compatibility']
        },
        'navamsa': {
            'compatibility': analysis['navamsa_compatibility'],
            'positions': analysis['navamsa_positions']
        }
    }

    return data


def get_dasha_period_data(chart1, chart2, date):
    """
    Get Dasha period data for a specific date

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart
        date (Datetime): The date

    Returns:
        dict: Dictionary with Dasha period data
    """
    # Get the Dasha and Antardasha for each chart
    from astrovedic.vedic.vimshottari import get_dasha, get_antardasha, get_dasha_lord, get_antardasha_lord

    dasha1 = get_dasha(chart1, date)
    dasha2 = get_dasha(chart2, date)
    antardasha1 = get_antardasha(chart1, date)
    antardasha2 = get_antardasha(chart2, date)

    dasha_lord1 = get_dasha_lord(dasha1)
    dasha_lord2 = get_dasha_lord(dasha2)
    antardasha_lord1 = get_antardasha_lord(antardasha1)
    antardasha_lord2 = get_antardasha_lord(antardasha2)

    # Calculate the compatibility between the Dasha lords
    from astrovedic.vedic.compatibility.dasha.compatibility import calculate_planet_compatibility

    dasha_compatibility = calculate_planet_compatibility(dasha_lord1, dasha_lord2)
    antardasha_compatibility = calculate_planet_compatibility(antardasha_lord1, antardasha_lord2)

    # Calculate the overall compatibility score
    overall_score = (dasha_compatibility['score'] * 0.6 + antardasha_compatibility['score'] * 0.4)

    # Create the data structure
    data = {
        'date': date,
        'dasha_lord1': dasha_lord1,
        'dasha_lord2': dasha_lord2,
        'antardasha_lord1': antardasha_lord1,
        'antardasha_lord2': antardasha_lord2,
        'dasha_compatibility': dasha_compatibility,
        'antardasha_compatibility': antardasha_compatibility,
        'overall_score': overall_score
    }

    return data


def get_compatibility_strength_score(chart1, chart2):
    """
    Get the overall compatibility strength score

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        float: The compatibility strength score (0-100)
    """
    # Get the compatibility analysis
    analysis = analyze_compatibility(chart1, chart2)

    # Return the overall score
    return analysis['overall_score']


def calculate_overall_compatibility_score(
    kuta_scores, dosha_analysis, dosha_cancellation,
    dasha_compatibility, navamsa_compatibility
):
    """
    Calculate the overall compatibility score

    Args:
        kuta_scores (dict): The Kuta scores
        dosha_analysis (dict): The Dosha analysis
        dosha_cancellation (dict): The Dosha cancellation
        dasha_compatibility (dict): The Dasha compatibility
        navamsa_compatibility (dict): The Navamsa compatibility

    Returns:
        float: The overall compatibility score (0-100)
    """
    # Get the Kuta score (0-36) and convert to 0-50 scale
    kuta_score = kuta_scores['total_kuta_score']['total_score']
    kuta_score_normalized = (kuta_score / 36) * 50

    # Get the Dosha score (0-10)
    dosha_score = 10

    # Check for Mangal Dosha
    mangal_dosha1 = dosha_analysis['Mangal Dosha']['chart1']
    mangal_dosha2 = dosha_analysis['Mangal Dosha']['chart2']

    # Check for Kuja Dosha
    kuja_dosha1 = dosha_analysis['Kuja Dosha']['chart1']
    kuja_dosha2 = dosha_analysis['Kuja Dosha']['chart2']

    # Reduce score for Doshas
    if (mangal_dosha1['has_dosha'] and mangal_dosha2['has_dosha']) or \
       (kuja_dosha1['has_dosha'] and kuja_dosha2['has_dosha']):
        dosha_score -= 5
    elif mangal_dosha1['has_dosha'] or mangal_dosha2['has_dosha'] or \
         kuja_dosha1['has_dosha'] or kuja_dosha2['has_dosha']:
        dosha_score -= 2

    # Add points for Dosha cancellation
    if dosha_cancellation['is_cancelled']:
        dosha_score += 5

    # Get the Dasha compatibility score (0-10) and convert to 0-20 scale
    dasha_score = dasha_compatibility['score']
    dasha_score_normalized = (dasha_score / 10) * 20

    # Get the Navamsa compatibility score (0-10) and convert to 0-20 scale
    navamsa_score = navamsa_compatibility['score']
    navamsa_score_normalized = (navamsa_score / 10) * 20

    # Calculate the overall score
    overall_score = kuta_score_normalized + dosha_score + dasha_score_normalized + navamsa_score_normalized

    # Ensure the score is between 0 and 100
    overall_score = min(100, max(0, overall_score))

    return overall_score


def get_compatibility_summary(overall_score, compatibility_data):
    """
    Get a summary of compatibility data with the overall score

    Args:
        overall_score (float): The overall compatibility score
        compatibility_data (dict): The compatibility data summary

    Returns:
        dict: Dictionary with compatibility summary
    """
    # Get the compatibility level
    level = get_compatibility_level(overall_score)

    # Create the summary
    summary = {
        'overall_score': overall_score,
        'level': level,
        'kuta_percentage': compatibility_data['kuta_percentage'],
        'dosha_status': compatibility_data['dosha_status'],
        'dosha_cancellation': compatibility_data['dosha_cancellation'],
        'dasha_score': compatibility_data['dasha_score'],
        'navamsa_score': compatibility_data['navamsa_score']
    }

    return summary






