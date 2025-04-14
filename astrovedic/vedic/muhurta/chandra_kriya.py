"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Chandra Kriya calculations for Vedic astrology.
    Chandra Kriya refers to the activities suitable based on the Moon's position.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.vedic.nakshatras import get_nakshatra
from typing import Dict, Optional, Any, List, Tuple

# Chandra Kriya (activities suitable for each nakshatra)
CHANDRA_KRIYA = {
    'Ashwini': {
        'suitable': ['Travel', 'Medical treatment', 'Starting new ventures', 'Physical activities'],
        'unsuitable': ['Rest', 'Meditation', 'Passive activities']
    },
    'Bharani': {
        'suitable': ['Funeral rites', 'Ending relationships', 'Destructive activities', 'Separation'],
        'unsuitable': ['Marriage', 'Starting new ventures', 'Constructive activities']
    },
    'Krittika': {
        'suitable': ['Cooking', 'Fire ceremonies', 'Competitive activities', 'Leadership tasks'],
        'unsuitable': ['Peaceful negotiations', 'Water-related activities', 'Sensitive discussions']
    },
    'Rohini': {
        'suitable': ['Agriculture', 'Gardening', 'Financial activities', 'Luxury purchases', 'Romance'],
        'unsuitable': ['Fasting', 'Ascetic practices', 'Conflict resolution']
    },
    'Mrigashira': {
        'suitable': ['Research', 'Study', 'Travel', 'Artistic pursuits', 'Communication'],
        'unsuitable': ['Physical labor', 'Confrontation', 'Fixed commitments']
    },
    'Ardra': {
        'suitable': ['Competitive activities', 'Debates', 'Martial arts', 'Challenging tasks'],
        'unsuitable': ['Peace negotiations', 'Delicate work', 'Marriage', 'Partnership']
    },
    'Punarvasu': {
        'suitable': ['Education', 'Religious activities', 'Home improvement', 'Family gatherings'],
        'unsuitable': ['Separation', 'Conflict', 'Risky ventures']
    },
    'Pushya': {
        'suitable': ['Religious ceremonies', 'Starting new ventures', 'Financial activities', 'Healing'],
        'unsuitable': ['Destructive activities', 'Arguments', 'Separation']
    },
    'Ashlesha': {
        'suitable': ['Research', 'Secret activities', 'Occult practices', 'Strategic planning'],
        'unsuitable': ['Open communication', 'Public appearances', 'Straightforward activities']
    },
    'Magha': {
        'suitable': ['Government work', 'Authority-related tasks', 'Leadership', 'Ancestral ceremonies'],
        'unsuitable': ['Subordinate roles', 'Humble activities', 'Isolation']
    },
    'Purva Phalguni': {
        'suitable': ['Entertainment', 'Romance', 'Creative activities', 'Celebrations'],
        'unsuitable': ['Serious business', 'Ascetic practices', 'Solitary activities']
    },
    'Uttara Phalguni': {
        'suitable': ['Marriage', 'Partnerships', 'Contracts', 'Agreements', 'Social activities'],
        'unsuitable': ['Solitary work', 'Breaking relationships', 'Isolation']
    },
    'Hasta': {
        'suitable': ['Skilled work', 'Crafts', 'Medical treatment', 'Detailed tasks', 'Learning skills'],
        'unsuitable': ['Rough work', 'Activities requiring little precision', 'Delegation']
    },
    'Chitra': {
        'suitable': ['Art', 'Beauty-related activities', 'Decoration', 'Fashion', 'Trade'],
        'unsuitable': ['Plain or mundane activities', 'Rough work', 'Asceticism']
    },
    'Swati': {
        'suitable': ['Trade', 'Travel', 'Wind-related activities', 'Independence', 'Freedom'],
        'unsuitable': ['Fixed commitments', 'Rooting down', 'Stability-seeking']
    },
    'Vishakha': {
        'suitable': ['Goal achievement', 'Focused work', 'Determination', 'Purposeful activities'],
        'unsuitable': ['Aimless activities', 'Relaxation', 'Unfocused work']
    },
    'Anuradha': {
        'suitable': ['Friendship', 'Cooperation', 'Teamwork', 'Alliances', 'Partnerships'],
        'unsuitable': ['Competition', 'Solitary work', 'Confrontation']
    },
    'Jyeshtha': {
        'suitable': ['Leadership', 'Courage', 'Protection', 'Security measures', 'Defense'],
        'unsuitable': ['Submission', 'Vulnerability', 'Openness']
    },
    'Mula': {
        'suitable': ['Spiritual practices', 'Research', 'Digging', 'Foundation work', 'Root causes'],
        'unsuitable': ['Superficial activities', 'Surface-level work', 'Temporary solutions']
    },
    'Purva Ashadha': {
        'suitable': ['Water-related activities', 'Purification', 'Cleansing', 'First attempts'],
        'unsuitable': ['Final decisions', 'Permanent commitments', 'Dry activities']
    },
    'Uttara Ashadha': {
        'suitable': ['Victory celebrations', 'Achievement', 'Final steps', 'Completion'],
        'unsuitable': ['Starting new projects', 'Preliminary work', 'Beginnings']
    },
    'Shravana': {
        'suitable': ['Learning', 'Teaching', 'Communication', 'Listening', 'Study'],
        'unsuitable': ['Action without thought', 'Physical labor', 'Silent activities']
    },
    'Dhanishta': {
        'suitable': ['Music', 'Wealth generation', 'Prosperity activities', 'Abundance'],
        'unsuitable': ['Asceticism', 'Poverty vows', 'Restriction']
    },
    'Shatabhisha': {
        'suitable': ['Healing', 'Medicine', 'Secret work', 'Occult practices', 'Isolation'],
        'unsuitable': ['Public activities', 'Social gatherings', 'Open communication']
    },
    'Purva Bhadrapada': {
        'suitable': ['Funeral rites', 'Endings', 'Transformation', 'Letting go'],
        'unsuitable': ['Beginnings', 'New ventures', 'Attachments']
    },
    'Uttara Bhadrapada': {
        'suitable': ['Spiritual activities', 'Service', 'Charitable work', 'Selfless actions'],
        'unsuitable': ['Selfish pursuits', 'Material focus', 'Ego-driven activities']
    },
    'Revati': {
        'suitable': ['Water activities', 'Nourishment', 'Nurturing', 'Compassion', 'Care'],
        'unsuitable': ['Harsh actions', 'Cruelty', 'Severity', 'Dryness']
    }
}

def get_chandra_kriya(moon_longitude: float) -> Dict[str, Any]:
    """
    Get Chandra Kriya (suitable and unsuitable activities) based on the Moon's position.

    Args:
        moon_longitude (float): The Moon's longitude in degrees (0-360)

    Returns:
        dict: Dictionary with Chandra Kriya information.
    """
    # Get nakshatra information
    nakshatra_info = get_nakshatra(moon_longitude)
    nakshatra_name = nakshatra_info['name']
    
    # Get the Chandra Kriya for this nakshatra
    kriya = CHANDRA_KRIYA.get(nakshatra_name, {'suitable': [], 'unsuitable': []})
    
    return {
        'nakshatra': nakshatra_name,
        'suitable_activities': kriya['suitable'],
        'unsuitable_activities': kriya['unsuitable']
    }

def get_suitable_activities(moon_longitude: float) -> List[str]:
    """
    Get suitable activities based on the Moon's position.

    Args:
        moon_longitude (float): The Moon's longitude in degrees (0-360)

    Returns:
        list: List of suitable activities.
    """
    kriya = get_chandra_kriya(moon_longitude)
    return kriya['suitable_activities']

def get_unsuitable_activities(moon_longitude: float) -> List[str]:
    """
    Get unsuitable activities based on the Moon's position.

    Args:
        moon_longitude (float): The Moon's longitude in degrees (0-360)

    Returns:
        list: List of unsuitable activities.
    """
    kriya = get_chandra_kriya(moon_longitude)
    return kriya['unsuitable_activities']

def get_chandra_kriya_for_chart(chart: Chart) -> Dict[str, Any]:
    """
    Get Chandra Kriya (suitable and unsuitable activities) for a chart.

    Args:
        chart (Chart): The chart object containing birth details.

    Returns:
        dict: Dictionary with Chandra Kriya information.

    Raises:
        ValueError: If the Moon object is not found in the chart.
    """
    # Get the Moon's position
    moon = chart.getObject(const.MOON)
    if moon is None:
        raise ValueError("Moon object not found in the chart.")
    
    # Get the Chandra Kriya based on the Moon's position
    return get_chandra_kriya(moon.lon)

def get_chandra_kriya_for_nakshatra(nakshatra_name: str) -> Dict[str, List[str]]:
    """
    Get Chandra Kriya (suitable and unsuitable activities) for a specific nakshatra.

    Args:
        nakshatra_name (str): The name of the nakshatra.

    Returns:
        dict: Dictionary with suitable and unsuitable activities.
    """
    return CHANDRA_KRIYA.get(nakshatra_name, {'suitable': [], 'unsuitable': []})
