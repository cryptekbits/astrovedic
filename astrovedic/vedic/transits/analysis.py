"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements advanced analysis tools for transit analysis
    in Vedic astrology.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic import angle
from datetime import timedelta

# Import core functions
from astrovedic.vedic.transits.core import (
    get_transit_chart, get_transit_planets,
    get_transit_aspects, get_transit_houses,
    get_transit_quality
)

# Import Gochara functions
from astrovedic.vedic.transits.gochara import (
    get_gochara_effects, get_planet_gochara
)

# Import Ashtakavarga functions
from astrovedic.vedic.transits.ashtakavarga import (
    get_transit_ashtakavarga, get_transit_bindus
)

# Import Dasha functions
from astrovedic.vedic.transits.dashas import (
    get_transit_dasha_effects, get_dasha_transit_compatibility
)

# Import prediction functions
from astrovedic.vedic.transits.predictions import (
    get_transit_predictions, get_transit_timeline,
    get_transit_events, get_transit_periods
)


def analyze_transits(natal_chart, start_date, end_date):
    """
    Analyze transits for a specific period
    
    Args:
        natal_chart (Chart): The natal chart
        start_date (Datetime): The start date
        end_date (Datetime): The end date
    
    Returns:
        dict: Dictionary with transit analysis
    """
    # Get the transit chart for the start date
    transit_chart = get_transit_chart(natal_chart, start_date)
    
    # Get the transit planets
    transit_planets = get_transit_planets(natal_chart, transit_chart)
    
    # Get the transit aspects
    transit_aspects = get_transit_aspects(natal_chart, transit_chart)
    
    # Get the transit houses
    transit_houses = get_transit_houses(natal_chart, transit_chart)
    
    # Get the transit quality
    transit_quality = get_transit_quality(natal_chart, transit_chart)
    
    # Get the Gochara effects
    gochara_effects = get_gochara_effects(natal_chart, transit_chart)
    
    # Get the transit Ashtakavarga
    transit_ashtakavarga = get_transit_ashtakavarga(natal_chart, transit_chart)
    
    # Get the transit Dasha effects
    transit_dasha_effects = get_transit_dasha_effects(natal_chart, transit_chart)
    
    # Get the transit timeline
    timeline = get_transit_timeline(natal_chart, start_date, end_date)
    
    # Get the significant transit events
    events = get_transit_events(natal_chart, start_date, end_date)
    
    # Get the transit periods
    periods = get_transit_periods(natal_chart, start_date, end_date)
    
    # Get the transit predictions
    transits = {
        'transit_chart': transit_chart,
        'transit_planets': transit_planets,
        'transit_aspects': transit_aspects,
        'transit_houses': transit_houses,
        'transit_quality': transit_quality,
        'gochara_effects': gochara_effects,
        'transit_ashtakavarga': transit_ashtakavarga,
        'transit_dasha_effects': transit_dasha_effects
    }
    
    predictions = get_transit_predictions(natal_chart, transits)
    
    return {
        'start_date': start_date,
        'end_date': end_date,
        'transit_quality': transit_quality,
        'timeline': timeline,
        'events': events,
        'periods': periods,
        'predictions': predictions
    }


def get_transit_compatibility(natal_chart1, natal_chart2, transit_date):
    """
    Calculate the compatibility between two charts based on transits
    
    Args:
        natal_chart1 (Chart): The first natal chart
        natal_chart2 (Chart): The second natal chart
        transit_date (Datetime): The transit date
    
    Returns:
        dict: Dictionary with transit compatibility information
    """
    # Get the transit chart
    transit_chart = get_transit_chart(natal_chart1, transit_date)
    
    # Get the transit aspects for both charts
    transit_aspects1 = get_transit_aspects(natal_chart1, transit_chart)
    transit_aspects2 = get_transit_aspects(natal_chart2, transit_chart)
    
    # Get the transit quality for both charts
    transit_quality1 = get_transit_quality(natal_chart1, transit_chart)
    transit_quality2 = get_transit_quality(natal_chart2, transit_chart)
    
    # Initialize the compatibility
    compatibility = {
        'score': 0,
        'factors': [],
        'description': ''
    }
    
    # Compare the transit qualities
    quality1 = transit_quality1['quality']
    quality2 = transit_quality2['quality']
    
    # Assign scores based on quality
    quality_scores = {
        'Excellent': 5,
        'Good': 4,
        'Neutral': 3,
        'Challenging': 2,
        'Difficult': 1
    }
    
    # Calculate the average quality score
    avg_quality = (quality_scores.get(quality1, 3) + quality_scores.get(quality2, 3)) / 2
    
    # Add to the compatibility score
    compatibility['score'] += avg_quality * 10
    
    # Check for shared favorable aspects
    favorable_aspects1 = [aspect for aspect in transit_aspects1 if aspect['aspect'] in ['Conjunction', 'Trine', 'Sextile']]
    favorable_aspects2 = [aspect for aspect in transit_aspects2 if aspect['aspect'] in ['Conjunction', 'Trine', 'Sextile']]
    
    # Count shared favorable aspects
    shared_favorable = 0
    for aspect1 in favorable_aspects1:
        for aspect2 in favorable_aspects2:
            if aspect1['transit_planet'] == aspect2['transit_planet'] and aspect1['aspect'] == aspect2['aspect']:
                shared_favorable += 1
                compatibility['factors'].append(f"Both charts have favorable {aspect1['aspect']} from transit {aspect1['transit_planet']}")
    
    # Add to the compatibility score
    compatibility['score'] += shared_favorable * 5
    
    # Check for shared challenging aspects
    challenging_aspects1 = [aspect for aspect in transit_aspects1 if aspect['aspect'] in ['Opposition', 'Square']]
    challenging_aspects2 = [aspect for aspect in transit_aspects2 if aspect['aspect'] in ['Opposition', 'Square']]
    
    # Count shared challenging aspects
    shared_challenging = 0
    for aspect1 in challenging_aspects1:
        for aspect2 in challenging_aspects2:
            if aspect1['transit_planet'] == aspect2['transit_planet'] and aspect1['aspect'] == aspect2['aspect']:
                shared_challenging += 1
                compatibility['factors'].append(f"Both charts have challenging {aspect1['aspect']} from transit {aspect1['transit_planet']}")
    
    # Subtract from the compatibility score
    compatibility['score'] -= shared_challenging * 5
    
    # Ensure the score is between 0 and 100
    compatibility['score'] = min(100, max(0, compatibility['score']))
    
    # Generate a description based on the score
    if compatibility['score'] >= 80:
        compatibility['description'] = "The current transits are highly favorable for both charts, indicating a harmonious and productive period for the relationship."
    elif compatibility['score'] >= 60:
        compatibility['description'] = "The current transits are generally favorable for both charts, suggesting a positive period for the relationship."
    elif compatibility['score'] >= 40:
        compatibility['description'] = "The current transits have mixed influences on both charts, indicating a period with both opportunities and challenges for the relationship."
    elif compatibility['score'] >= 20:
        compatibility['description'] = "The current transits are challenging for both charts, suggesting a difficult period for the relationship that requires patience and understanding."
    else:
        compatibility['description'] = "The current transits are very challenging for both charts, indicating a highly stressful period for the relationship that may require significant effort to navigate."
    
    return compatibility


def get_transit_strength_score(natal_chart, transit_date):
    """
    Calculate the overall strength score of transits
    
    Args:
        natal_chart (Chart): The natal chart
        transit_date (Datetime): The transit date
    
    Returns:
        float: The overall strength score (0-100)
    """
    # Get the transit chart
    transit_chart = get_transit_chart(natal_chart, transit_date)
    
    # Get the transit quality
    transit_quality = get_transit_quality(natal_chart, transit_chart)
    
    # Get the Gochara effects
    gochara_effects = get_gochara_effects(natal_chart, transit_chart)
    
    # Get the transit Ashtakavarga
    transit_ashtakavarga = get_transit_ashtakavarga(natal_chart, transit_chart)
    
    # Get the transit Dasha effects
    transit_dasha_effects = get_transit_dasha_effects(natal_chart, transit_chart)
    
    # Get the Dasha compatibility
    dasha_compatibility = get_dasha_transit_compatibility(natal_chart, transit_chart)
    
    # Initialize the score
    score = 0
    
    # Add the transit quality score
    quality_scores = {
        'Excellent': 50,
        'Good': 40,
        'Neutral': 30,
        'Challenging': 20,
        'Difficult': 10
    }
    
    score += quality_scores.get(transit_quality['quality'], 30)
    
    # Add the Gochara effects score
    gochara_score = 0
    for planet_id, effect in gochara_effects.items():
        if effect['strength']['strength'] == 'Strong Favorable':
            gochara_score += 2
        elif effect['strength']['strength'] == 'Moderate Favorable':
            gochara_score += 1
        elif effect['strength']['strength'] == 'Moderate Unfavorable':
            gochara_score -= 1
        elif effect['strength']['strength'] == 'Strong Unfavorable':
            gochara_score -= 2
    
    # Normalize the Gochara score
    gochara_score = min(10, max(-10, gochara_score))
    
    # Add to the total score
    score += (gochara_score + 10) * 2
    
    # Add the Ashtakavarga score
    ashtakavarga_score = 0
    for planet_id, transit in transit_ashtakavarga.items():
        if planet_id != 'sarvashtakavarga':
            if transit['strength']['strength'] == 'Excellent':
                ashtakavarga_score += 2
            elif transit['strength']['strength'] == 'Good':
                ashtakavarga_score += 1
            elif transit['strength']['strength'] == 'Challenging':
                ashtakavarga_score -= 1
            elif transit['strength']['strength'] == 'Difficult':
                ashtakavarga_score -= 2
    
    # Normalize the Ashtakavarga score
    ashtakavarga_score = min(10, max(-10, ashtakavarga_score))
    
    # Add to the total score
    score += (ashtakavarga_score + 10) * 2
    
    # Add the Dasha compatibility score
    score += dasha_compatibility['score'] * 0.2
    
    # Ensure the score is between 0 and 100
    score = min(100, max(0, score))
    
    return score


def get_transit_analysis(natal_chart, transit_date):
    """
    Get a comprehensive analysis of transits for a specific date
    
    Args:
        natal_chart (Chart): The natal chart
        transit_date (Datetime): The transit date
    
    Returns:
        dict: Dictionary with transit analysis
    """
    # Get the transit chart
    transit_chart = get_transit_chart(natal_chart, transit_date)
    
    # Get the transit planets
    transit_planets = get_transit_planets(natal_chart, transit_chart)
    
    # Get the transit aspects
    transit_aspects = get_transit_aspects(natal_chart, transit_chart)
    
    # Get the transit houses
    transit_houses = get_transit_houses(natal_chart, transit_chart)
    
    # Get the transit quality
    transit_quality = get_transit_quality(natal_chart, transit_chart)
    
    # Get the Gochara effects
    gochara_effects = get_gochara_effects(natal_chart, transit_chart)
    
    # Get the transit Ashtakavarga
    transit_ashtakavarga = get_transit_ashtakavarga(natal_chart, transit_chart)
    
    # Get the transit Dasha effects
    transit_dasha_effects = get_transit_dasha_effects(natal_chart, transit_chart)
    
    # Get the Dasha compatibility
    dasha_compatibility = get_dasha_transit_compatibility(natal_chart, transit_chart)
    
    # Get the transit strength score
    strength_score = get_transit_strength_score(natal_chart, transit_date)
    
    # Get the transit predictions
    transits = {
        'transit_chart': transit_chart,
        'transit_planets': transit_planets,
        'transit_aspects': transit_aspects,
        'transit_houses': transit_houses,
        'transit_quality': transit_quality,
        'gochara_effects': gochara_effects,
        'transit_ashtakavarga': transit_ashtakavarga,
        'transit_dasha_effects': transit_dasha_effects
    }
    
    predictions = get_transit_predictions(natal_chart, transits)
    
    return {
        'date': transit_date,
        'transit_chart': transit_chart,
        'transit_planets': transit_planets,
        'transit_aspects': transit_aspects,
        'transit_houses': transit_houses,
        'transit_quality': transit_quality,
        'gochara_effects': gochara_effects,
        'transit_ashtakavarga': transit_ashtakavarga,
        'transit_dasha_effects': transit_dasha_effects,
        'dasha_compatibility': dasha_compatibility,
        'strength_score': strength_score,
        'predictions': predictions
    }
