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


def get_sarvatobhadra_predictions(chart):
    """
    Generate predictions based on Sarvatobhadra Chakra for a chart
    
    Args:
        chart (Chart): The chart
    
    Returns:
        dict: Dictionary with Sarvatobhadra Chakra predictions
    """
    # Analyze the Sarvatobhadra Chakra
    analysis = analyze_sarvatobhadra(chart)
    
    # Initialize the predictions
    predictions = {
        'general': [],
        'directions': {},
        'tara_bala': [],
        'activities': {}
    }
    
    # Generate general predictions
    quality = analysis['quality']['quality']
    score = analysis['quality']['score']
    
    if quality == 'Excellent':
        predictions['general'].append("The Sarvatobhadra Chakra is excellent. This is a highly auspicious time for most activities.")
    elif quality == 'Good':
        predictions['general'].append("The Sarvatobhadra Chakra is good. This is a favorable time for most activities.")
    elif quality == 'Neutral':
        predictions['general'].append("The Sarvatobhadra Chakra is neutral. This time has both favorable and unfavorable aspects.")
    elif quality == 'Inauspicious':
        predictions['general'].append("The Sarvatobhadra Chakra is inauspicious. This is not a favorable time for important activities.")
    elif quality == 'Highly Inauspicious':
        predictions['general'].append("The Sarvatobhadra Chakra is highly inauspicious. This is a very unfavorable time for most activities.")
    
    # Generate direction predictions
    for direction in ['North', 'Northeast', 'East', 'Southeast', 'South', 'Southwest', 'West', 'Northwest', 'Center']:
        direction_quality = get_direction_quality(analysis['chakra'], direction)
        
        if direction_quality['quality'] in ['Excellent', 'Good']:
            predictions['directions'][direction] = f"{direction} is {direction_quality['quality'].lower()}. {', '.join(direction_quality['factors'][:2])}"
        else:
            predictions['directions'][direction] = f"{direction} is not favorable. {', '.join(direction_quality['factors'][:2])}"
    
    # Generate Tara Bala predictions
    current_tara = analysis['current_tara']
    tara_description = analysis['tara_description']
    
    predictions['tara_bala'].append(f"The current Tara is {current_tara}. {tara_description}")
    
    if analysis['is_favorable_tara']:
        predictions['tara_bala'].append(f"{current_tara} is favorable. This is a good time for most activities.")
    elif analysis['is_unfavorable_tara']:
        predictions['tara_bala'].append(f"{current_tara} is unfavorable. This is not a good time for important activities.")
    
    # Generate activity-specific predictions
    for activity, direction in analysis['activity_directions'].items():
        if direction['quality'] in ['Excellent', 'Good']:
            predictions['activities'][activity] = f"For {activity}, the best direction is {direction['direction']} ({direction['quality'].lower()}). {', '.join(direction['factors'][:2])}"
        else:
            predictions['activities'][activity] = f"For {activity}, no direction is particularly favorable. The least unfavorable is {direction['direction']}. {', '.join(direction['factors'][:2])}"
    
    return predictions


def get_sarvatobhadra_compatibility(chart1, chart2):
    """
    Calculate compatibility between two charts based on Sarvatobhadra Chakra
    
    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart
    
    Returns:
        dict: Dictionary with compatibility information
    """
    # Analyze both charts
    analysis1 = analyze_sarvatobhadra(chart1)
    analysis2 = analyze_sarvatobhadra(chart2)
    
    # Initialize the compatibility
    compatibility = {
        'score': 0,
        'factors': [],
        'description': ''
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
    
    # Add to the compatibility score
    compatibility['score'] += avg_quality * 10
    
    # Compare the best directions
    best_direction1 = analysis1['best_direction']['direction']
    best_direction2 = analysis2['best_direction']['direction']
    
    # Check if the best directions are the same or adjacent
    if best_direction1 == best_direction2:
        compatibility['score'] += 20
        compatibility['factors'].append(f"Both charts have the same best direction: {best_direction1}")
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
            compatibility['score'] += 10
            compatibility['factors'].append(f"The best directions ({best_direction1} and {best_direction2}) are adjacent")
    
    # Compare the Tara Bala
    tara1 = analysis1['current_tara']
    tara2 = analysis2['current_tara']
    
    # Check if both Taras are favorable
    if analysis1['is_favorable_tara'] and analysis2['is_favorable_tara']:
        compatibility['score'] += 20
        compatibility['factors'].append(f"Both charts have favorable Taras: {tara1} and {tara2}")
    elif analysis1['is_favorable_tara'] or analysis2['is_favorable_tara']:
        compatibility['score'] += 10
        compatibility['factors'].append(f"One chart has a favorable Tara: {tara1 if analysis1['is_favorable_tara'] else tara2}")
    
    # Check if both Taras are unfavorable
    if analysis1['is_unfavorable_tara'] and analysis2['is_unfavorable_tara']:
        compatibility['score'] -= 20
        compatibility['factors'].append(f"Both charts have unfavorable Taras: {tara1} and {tara2}")
    elif analysis1['is_unfavorable_tara'] or analysis2['is_unfavorable_tara']:
        compatibility['score'] -= 10
        compatibility['factors'].append(f"One chart has an unfavorable Tara: {tara1 if analysis1['is_unfavorable_tara'] else tara2}")
    
    # Ensure the score is between 0 and 100
    compatibility['score'] = min(100, max(0, compatibility['score']))
    
    # Generate a description based on the score
    if compatibility['score'] >= 80:
        compatibility['description'] = "These charts are highly compatible based on Sarvatobhadra Chakra analysis."
    elif compatibility['score'] >= 60:
        compatibility['description'] = "These charts are compatible based on Sarvatobhadra Chakra analysis."
    elif compatibility['score'] >= 40:
        compatibility['description'] = "These charts have moderate compatibility based on Sarvatobhadra Chakra analysis."
    elif compatibility['score'] >= 20:
        compatibility['description'] = "These charts have low compatibility based on Sarvatobhadra Chakra analysis."
    else:
        compatibility['description'] = "These charts are incompatible based on Sarvatobhadra Chakra analysis."
    
    return compatibility


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
