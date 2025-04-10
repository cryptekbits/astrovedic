"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements transit analysis for Vedic astrology.
    It includes functions to analyze Gochara (planetary transits),
    transit effects on natal chart, and Ashtakavarga transit analysis.
"""

from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

from flatlib.vedic.transits.core import (
    get_transit_chart, get_transit_planets,
    get_transit_aspects, get_transit_houses,
    get_transit_quality
)

from flatlib.vedic.transits.gochara import (
    get_gochara_effects, get_vedha_effects,
    get_argala_effects, get_planet_gochara,
    get_gochara_strength
)

from flatlib.vedic.transits.ashtakavarga import (
    get_transit_ashtakavarga, get_transit_bindus,
    get_transit_sarvashtakavarga, get_transit_kaksha,
    get_transit_ashtakavarga_strength
)

from flatlib.vedic.transits.dashas import (
    get_transit_dasha_effects, get_transit_antardasha_effects,
    get_transit_pratyantardasha_effects, get_dasha_transit_compatibility
)

from flatlib.vedic.transits.predictions import (
    get_transit_predictions, get_transit_timeline,
    get_transit_events, get_transit_periods
)

from flatlib.vedic.transits.analysis import (
    analyze_transits, get_transit_compatibility,
    get_transit_strength_score, get_transit_analysis
)

# Constants for transit quality
EXCELLENT = 'Excellent'
GOOD = 'Good'
NEUTRAL = 'Neutral'
CHALLENGING = 'Challenging'
DIFFICULT = 'Difficult'

# List of transit quality levels
LIST_TRANSIT_QUALITY = [
    EXCELLENT, GOOD, NEUTRAL, CHALLENGING, DIFFICULT
]

# Constants for transit aspects
CONJUNCTION = 'Conjunction'
OPPOSITION = 'Opposition'
TRINE = 'Trine'
SQUARE = 'Square'
SEXTILE = 'Sextile'

# List of transit aspects
LIST_TRANSIT_ASPECTS = [
    CONJUNCTION, OPPOSITION, TRINE, SQUARE, SEXTILE
]

# Constants for Gochara effects
FAVORABLE = 'Favorable'
UNFAVORABLE = 'Unfavorable'
MIXED = 'Mixed'
NEUTRAL = 'Neutral'

# List of Gochara effect types
LIST_GOCHARA_EFFECTS = [
    FAVORABLE, UNFAVORABLE, MIXED, NEUTRAL
]


def get_transits(natal_chart, transit_date):
    """
    Get transit information for a specific date
    
    Args:
        natal_chart (Chart): The natal chart
        transit_date (Datetime): The transit date
    
    Returns:
        dict: Dictionary with transit information
    """
    # Create a transit chart
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
    
    return {
        'transit_chart': transit_chart,
        'transit_planets': transit_planets,
        'transit_aspects': transit_aspects,
        'transit_houses': transit_houses,
        'transit_quality': transit_quality,
        'gochara_effects': gochara_effects,
        'transit_ashtakavarga': transit_ashtakavarga,
        'transit_dasha_effects': transit_dasha_effects
    }


def get_transit_predictions_for_date(natal_chart, transit_date):
    """
    Get transit predictions for a specific date
    
    Args:
        natal_chart (Chart): The natal chart
        transit_date (Datetime): The transit date
    
    Returns:
        dict: Dictionary with transit predictions
    """
    # Get the transits
    transits = get_transits(natal_chart, transit_date)
    
    # Get the transit predictions
    predictions = get_transit_predictions(natal_chart, transits)
    
    return predictions


def get_transit_timeline_for_period(natal_chart, start_date, end_date):
    """
    Get transit timeline for a specific period
    
    Args:
        natal_chart (Chart): The natal chart
        start_date (Datetime): The start date
        end_date (Datetime): The end date
    
    Returns:
        list: List of transit events
    """
    # Get the transit timeline
    timeline = get_transit_timeline(natal_chart, start_date, end_date)
    
    return timeline


def analyze_transit_period(natal_chart, start_date, end_date):
    """
    Analyze transits for a specific period
    
    Args:
        natal_chart (Chart): The natal chart
        start_date (Datetime): The start date
        end_date (Datetime): The end date
    
    Returns:
        dict: Dictionary with transit analysis
    """
    # Analyze the transits
    analysis = analyze_transits(natal_chart, start_date, end_date)
    
    return analysis
