"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements basic analysis tools for Yogas (planetary combinations)
    in Vedic astrology. For detailed analysis and reporting,
    use the astroved_extension package.
"""

from astrovedic import const
from astrovedic.vedic.yogas.core import (
    get_yoga_strength, get_strongest_yoga
)


def get_basic_yoga_data(chart, yogas):
    """
    Get basic data of Yogas in a chart.

    Args:
        chart (Chart): The birth chart
        yogas (dict): Dictionary with Yoga information

    Returns:
        dict: Dictionary with basic Yoga data
    """
    # Initialize the result
    result = {
        'total_yogas': yogas['summary']['total_yogas'],
        'beneficial_yogas': yogas['summary']['beneficial_yogas'],
        'harmful_yogas': yogas['summary']['harmful_yogas'],
        'strongest_yoga': None,
        'yoga_types': {}
    }

    # Get the strongest Yoga
    strongest_yoga = yogas['summary']['strongest_yoga']
    if strongest_yoga:
        result['strongest_yoga'] = {
            'name': strongest_yoga['name'],
            'type': strongest_yoga['type'],
            'strength': strongest_yoga['strength'],
            'is_beneficial': strongest_yoga.get('is_beneficial', True)
        }

    # Count Yogas by type
    for yoga_type, count in yogas['summary']['yoga_types'].items():
        result['yoga_types'][yoga_type] = count

    return result


def get_basic_yoga_analysis(chart, yogas):
    """
    Alias for get_basic_yoga_data for backward compatibility.

    Args:
        chart (Chart): The birth chart
        yogas (dict): Dictionary with Yoga information

    Returns:
        dict: Dictionary with basic Yoga data
    """
    return get_basic_yoga_data(chart, yogas)
