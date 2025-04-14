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


def get_transit_data(natal_chart, start_date, end_date):
    """
    Get transit data for a specific period

    Args:
        natal_chart (Chart): The natal chart
        start_date (Datetime): The start date
        end_date (Datetime): The end date

    Returns:
        dict: Dictionary with transit data
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

    # Compile the transit data
    transit_data = {
        'transit_chart': transit_chart,
        'transit_planets': transit_planets,
        'transit_aspects': transit_aspects,
        'transit_houses': transit_houses,
        'transit_quality': transit_quality,
        'gochara_effects': gochara_effects,
        'transit_ashtakavarga': transit_ashtakavarga,
        'transit_dasha_effects': transit_dasha_effects
    }

    return {
        'start_date': start_date,
        'end_date': end_date,
        'transit_data': transit_data,
        'timeline': timeline,
        'events': events,
        'periods': periods
    }


def get_transit_comparison(natal_chart1, natal_chart2, transit_date):
    """
    Compare transit effects on two charts

    Args:
        natal_chart1 (Chart): The first natal chart
        natal_chart2 (Chart): The second natal chart
        transit_date (Datetime): The transit date

    Returns:
        dict: Dictionary with transit comparison information
    """
    # Get the transit chart
    transit_chart = get_transit_chart(natal_chart1, transit_date)

    # Get the transit aspects for both charts
    transit_aspects1 = get_transit_aspects(natal_chart1, transit_chart)
    transit_aspects2 = get_transit_aspects(natal_chart2, transit_chart)

    # Get the transit quality for both charts
    transit_quality1 = get_transit_quality(natal_chart1, transit_chart)
    transit_quality2 = get_transit_quality(natal_chart2, transit_chart)

    # Initialize the comparison
    comparison = {
        'score': 0,
        'factors': []
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

    # Add to the comparison score
    comparison['score'] += avg_quality * 10

    # Check for shared favorable aspects
    favorable_aspects1 = [aspect for aspect in transit_aspects1 if aspect['aspect'] in ['Conjunction', 'Trine', 'Sextile']]
    favorable_aspects2 = [aspect for aspect in transit_aspects2 if aspect['aspect'] in ['Conjunction', 'Trine', 'Sextile']]

    # Count shared favorable aspects
    shared_favorable = 0
    for aspect1 in favorable_aspects1:
        for aspect2 in favorable_aspects2:
            if aspect1['transit_planet'] == aspect2['transit_planet'] and aspect1['aspect'] == aspect2['aspect']:
                shared_favorable += 1
                comparison['factors'].append(f"Both charts have favorable {aspect1['aspect']} from transit {aspect1['transit_planet']}")

    # Add to the comparison score
    comparison['score'] += shared_favorable * 5

    # Check for shared challenging aspects
    challenging_aspects1 = [aspect for aspect in transit_aspects1 if aspect['aspect'] in ['Opposition', 'Square']]
    challenging_aspects2 = [aspect for aspect in transit_aspects2 if aspect['aspect'] in ['Opposition', 'Square']]

    # Count shared challenging aspects
    shared_challenging = 0
    for aspect1 in challenging_aspects1:
        for aspect2 in challenging_aspects2:
            if aspect1['transit_planet'] == aspect2['transit_planet'] and aspect1['aspect'] == aspect2['aspect']:
                shared_challenging += 1
                comparison['factors'].append(f"Both charts have challenging {aspect1['aspect']} from transit {aspect1['transit_planet']}")

    # Subtract from the comparison score
    comparison['score'] -= shared_challenging * 5

    # Ensure the score is between 0 and 100
    comparison['score'] = min(100, max(0, comparison['score']))

    return comparison


def get_transit_strength_data(natal_chart, transit_date):
    """
    Get data for calculating transit strength

    Args:
        natal_chart (Chart): The natal chart
        transit_date (Datetime): The transit date

    Returns:
        dict: Dictionary with transit strength data
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

    # Compile the transit strength data
    strength_data = {
        'transit_quality': transit_quality,
        'gochara_effects': gochara_effects,
        'transit_ashtakavarga': transit_ashtakavarga,
        'transit_dasha_effects': transit_dasha_effects,
        'dasha_compatibility': dasha_compatibility
    }

    return strength_data


def get_detailed_transit_data(natal_chart, transit_date):
    """
    Get detailed transit data for a specific date

    Args:
        natal_chart (Chart): The natal chart
        transit_date (Datetime): The transit date

    Returns:
        dict: Dictionary with detailed transit data
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

    # Get the transit strength data
    strength_data = get_transit_strength_data(natal_chart, transit_date)

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
        'strength_data': strength_data
    }
