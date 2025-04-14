"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements analysis tools for Sarvatobhadra Chakra
    in Vedic astrology.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos

# Import core functions
from astrovedic.vedic.sarvatobhadra.core import (
    get_sarvatobhadra_chakra, get_chakra_quality,
    get_auspicious_directions, get_inauspicious_directions
)

# Import direction functions
from astrovedic.vedic.sarvatobhadra.directions import (
    get_direction_quality, get_best_direction,
    get_direction_for_activity
)

# Import Tara Bala functions
from astrovedic.vedic.sarvatobhadra.tara import (
    get_tara_bala, get_tara_description,
    is_tara_favorable, is_tara_unfavorable
)


def analyze_sarvatobhadra(chart):
    """
    Analyze the Sarvatobhadra Chakra for a chart

    Args:
        chart (Chart): The chart

    Returns:
        dict: Dictionary with Sarvatobhadra Chakra analysis
    """
    # Get the Sarvatobhadra Chakra
    chakra = get_sarvatobhadra_chakra(chart)

    # Get the chakra quality
    quality = get_chakra_quality(chakra)

    # Get auspicious directions
    auspicious_directions = get_auspicious_directions(chakra)

    # Get inauspicious directions
    inauspicious_directions = get_inauspicious_directions(chakra)

    # Get the best direction
    best_direction = get_best_direction(chakra)

    # Get Tara Bala
    tara_bala = chakra['tara_bala']

    # Get the current Tara
    current_tara = tara_bala['current_tara']

    # Get the Tara description
    tara_description = get_tara_description(current_tara)

    # Check if the current Tara is favorable
    is_favorable_tara = is_tara_favorable(current_tara)

    # Check if the current Tara is unfavorable
    is_unfavorable_tara = is_tara_unfavorable(current_tara)

    # Get the Tara Bala score
    tara_score = tara_bala['score']

    # Get the best directions for different activities
    activity_directions = {}
    for activity in ['marriage', 'travel', 'business', 'education', 'medical', 'house_construction', 'general']:
        activity_directions[activity] = get_direction_for_activity(chakra, activity)

    return {
        'chakra': chakra,
        'quality': quality,
        'auspicious_directions': auspicious_directions,
        'inauspicious_directions': inauspicious_directions,
        'best_direction': best_direction,
        'tara_bala': tara_bala,
        'current_tara': current_tara,
        'tara_description': tara_description,
        'is_favorable_tara': is_favorable_tara,
        'is_unfavorable_tara': is_unfavorable_tara,
        'tara_score': tara_score,
        'activity_directions': activity_directions
    }


def get_sarvatobhadra_data(chart):
    """
    Get Sarvatobhadra Chakra data for a chart

    Args:
        chart (Chart): The chart

    Returns:
        dict: Dictionary with Sarvatobhadra Chakra data
    """
    # Analyze the Sarvatobhadra Chakra
    analysis = analyze_sarvatobhadra(chart)

    # Create the data structure
    data = {
        'chakra': analysis['chakra'],
        'quality': analysis['quality'],
        'auspicious_directions': analysis['auspicious_directions'],
        'inauspicious_directions': analysis['inauspicious_directions'],
        'best_direction': analysis['best_direction'],
        'tara_bala': analysis['tara_bala'],
        'current_tara': analysis['current_tara'],
        'is_favorable_tara': analysis['is_favorable_tara'],
        'is_unfavorable_tara': analysis['is_unfavorable_tara'],
        'tara_score': analysis['tara_score'],
        'activity_directions': analysis['activity_directions']
    }

    return data


def get_sarvatobhadra_comparison(chart1, chart2):
    """
    Compare two charts based on Sarvatobhadra Chakra

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with comparison information
    """
    # Analyze both charts
    analysis1 = analyze_sarvatobhadra(chart1)
    analysis2 = analyze_sarvatobhadra(chart2)

    # Initialize the comparison
    comparison = {
        'score': 0,
        'factors': []
    }

    # Compare the chakra qualities
    quality1 = analysis1['quality']['quality']
    quality2 = analysis2['quality']['quality']

    # Assign scores based on quality
    quality_scores = {
        'Excellent': 5,
        'Good': 4,
        'Neutral': 3,
        'Inauspicious': 2,
        'Highly Inauspicious': 1
    }

    # Calculate the average quality score
    avg_quality = (quality_scores.get(quality1, 3) + quality_scores.get(quality2, 3)) / 2

    # Add to the comparison score
    comparison['score'] += avg_quality * 10

    # Compare the best directions
    best_direction1 = analysis1['best_direction']['direction']
    best_direction2 = analysis2['best_direction']['direction']

    # Check if the best directions are the same or adjacent
    if best_direction1 == best_direction2:
        comparison['score'] += 20
        comparison['factors'].append(f"Same best direction: {best_direction1}")
    else:
        # Check if the directions are adjacent
        adjacent_directions = {
            'North': ['Northeast', 'Northwest'],
            'Northeast': ['North', 'East'],
            'East': ['Northeast', 'Southeast'],
            'Southeast': ['East', 'South'],
            'South': ['Southeast', 'Southwest'],
            'Southwest': ['South', 'West'],
            'West': ['Southwest', 'Northwest'],
            'Northwest': ['West', 'North'],
            'Center': ['North', 'Northeast', 'East', 'Southeast', 'South', 'Southwest', 'West', 'Northwest']
        }

        if best_direction2 in adjacent_directions.get(best_direction1, []):
            comparison['score'] += 10
            comparison['factors'].append(f"Adjacent best directions: {best_direction1} and {best_direction2}")

    # Compare the Tara Bala
    tara1 = analysis1['current_tara']
    tara2 = analysis2['current_tara']

    # Check if both Taras are favorable
    if analysis1['is_favorable_tara'] and analysis2['is_favorable_tara']:
        comparison['score'] += 20
        comparison['factors'].append(f"Both favorable Taras: {tara1} and {tara2}")
    elif analysis1['is_favorable_tara'] or analysis2['is_favorable_tara']:
        comparison['score'] += 10
        comparison['factors'].append(f"One favorable Tara: {tara1 if analysis1['is_favorable_tara'] else tara2}")

    # Check if both Taras are unfavorable
    if analysis1['is_unfavorable_tara'] and analysis2['is_unfavorable_tara']:
        comparison['score'] -= 20
        comparison['factors'].append(f"Both unfavorable Taras: {tara1} and {tara2}")
    elif analysis1['is_unfavorable_tara'] or analysis2['is_unfavorable_tara']:
        comparison['score'] -= 10
        comparison['factors'].append(f"One unfavorable Tara: {tara1 if analysis1['is_unfavorable_tara'] else tara2}")

    # Ensure the score is between 0 and 100
    comparison['score'] = min(100, max(0, comparison['score']))

    return comparison


def get_sarvatobhadra_strength_score(chart):
    """
    Calculate the overall strength score of a Sarvatobhadra Chakra

    Args:
        chart (Chart): The chart

    Returns:
        float: The overall strength score (0-100)
    """
    # Analyze the Sarvatobhadra Chakra
    analysis = analyze_sarvatobhadra(chart)

    # Initialize the score
    score = 0

    # Add the chakra quality score
    quality_scores = {
        'Excellent': 50,
        'Good': 40,
        'Neutral': 30,
        'Inauspicious': 20,
        'Highly Inauspicious': 10
    }

    score += quality_scores.get(analysis['quality']['quality'], 30)

    # Add the Tara Bala score
    tara_score = analysis['tara_score']
    score += tara_score * 0.3

    # Add the best direction score
    best_direction_score = analysis['best_direction']['score']
    score += (best_direction_score + 5) * 4

    # Ensure the score is between 0 and 100
    score = min(100, max(0, score))

    return score
