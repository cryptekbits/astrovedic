"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements analysis tools for Yogas (planetary combinations)
    in Vedic astrology.
"""

from astrovedic import const
from astrovedic.vedic.yogas.core import (
    get_yoga_strength, get_yoga_effects,
    get_strongest_yoga
)


def analyze_yogas(chart, yogas):
    """
    Analyze the Yogas in a chart

    Args:
        chart (Chart): The birth chart
        yogas (dict): Dictionary with Yoga information

    Returns:
        dict: Dictionary with Yoga analysis
    """
    # Initialize the result
    result = {
        'total_yogas': yogas['summary']['total_yogas'],
        'beneficial_yogas': yogas['summary']['beneficial_yogas'],
        'harmful_yogas': yogas['summary']['harmful_yogas'],
        'strongest_yoga': None,
        'yoga_types': {},
        'effects': []
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

    # Analyze each type of Yoga
    for yoga_type, count in yogas['summary']['yoga_types'].items():
        result['yoga_types'][yoga_type] = {
            'count': count,
            'yogas': []
        }

        # Add the Yogas of this type
        if yoga_type == 'mahapurusha_yogas':
            for yoga in yogas['mahapurusha_yogas']:
                result['yoga_types'][yoga_type]['yogas'].append({
                    'name': yoga['name'],
                    'strength': yoga['strength'],
                    'is_beneficial': yoga.get('is_beneficial', True)
                })
        elif yoga_type == 'raja_yogas':
            for yoga in yogas['raja_yogas']:
                result['yoga_types'][yoga_type]['yogas'].append({
                    'name': yoga['name'],
                    'strength': yoga['strength'],
                    'is_beneficial': yoga.get('is_beneficial', True)
                })
        elif yoga_type == 'dhana_yogas':
            for yoga in yogas['dhana_yogas']:
                result['yoga_types'][yoga_type]['yogas'].append({
                    'name': yoga['name'],
                    'strength': yoga['strength'],
                    'is_beneficial': yoga.get('is_beneficial', True)
                })
        elif yoga_type == 'nabhasa_yogas':
            for yoga in yogas['nabhasa_yogas']:
                result['yoga_types'][yoga_type]['yogas'].append({
                    'name': yoga['name'],
                    'strength': yoga['strength'],
                    'is_beneficial': yoga.get('is_beneficial', True)
                })
        elif yoga_type == 'dosha_yogas':
            for yoga in yogas['dosha_yogas']:
                result['yoga_types'][yoga_type]['yogas'].append({
                    'name': yoga['name'],
                    'strength': yoga['strength'],
                    'is_beneficial': yoga.get('is_beneficial', True)
                })
        elif yoga_type == 'chandra_yogas':
            for yoga in yogas['chandra_yogas']:
                result['yoga_types'][yoga_type]['yogas'].append({
                    'name': yoga['name'],
                    'strength': yoga['strength'],
                    'is_beneficial': yoga.get('is_beneficial', True)
                })

    # Generate effects for each Yoga
    for yoga_type, yoga_list in yogas.items():
        if yoga_type != 'summary':
            for yoga in yoga_list:
                effects = get_yoga_effects(chart, yoga)
                result['effects'].append({
                    'name': yoga['name'],
                    'type': yoga['type'],
                    'effects': effects
                })

    return result





def get_yoga_comparison(chart1, chart2):
    """
    Compare yoga data between two charts

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with yoga comparison data
    """
    # Get the Yogas in each chart
    from astrovedic.vedic.yogas import get_all_yogas
    yogas1 = get_all_yogas(chart1)
    yogas2 = get_all_yogas(chart2)

    # Initialize the result
    result = {
        'chart1_yogas': {
            'total': yogas1['summary']['total_yogas'],
            'beneficial': yogas1['summary']['beneficial_yogas'],
            'harmful': yogas1['summary']['harmful_yogas'],
            'types': yogas1['summary']['yoga_types']
        },
        'chart2_yogas': {
            'total': yogas2['summary']['total_yogas'],
            'beneficial': yogas2['summary']['beneficial_yogas'],
            'harmful': yogas2['summary']['harmful_yogas'],
            'types': yogas2['summary']['yoga_types']
        },
        'common_yogas': []
    }

    # Find common yogas between the two charts
    for yoga_type in yogas1:
        if yoga_type != 'summary':
            for yoga1 in yogas1[yoga_type]:
                for yoga2 in yogas2.get(yoga_type, []):
                    if yoga1['name'] == yoga2['name']:
                        result['common_yogas'].append({
                            'name': yoga1['name'],
                            'type': yoga_type,
                            'is_beneficial': yoga1.get('is_beneficial', True)
                        })

    return result


def get_yoga_strength_score(chart, yogas):
    """
    Calculate an overall Yoga strength score for a chart

    Args:
        chart (Chart): The birth chart
        yogas (dict): Dictionary with Yoga information

    Returns:
        float: The overall Yoga strength score (0-100)
    """
    # Initialize variables
    total_strength = 0.0
    total_yogas = 0

    # Calculate the total strength of all Yogas
    for yoga_type, yoga_list in yogas.items():
        if yoga_type != 'summary':
            for yoga in yoga_list:
                # Get the strength of the Yoga
                strength = yoga.get('strength', 0)

                # Adjust the strength based on whether the Yoga is beneficial or harmful
                if yoga.get('is_beneficial', True):
                    total_strength += strength
                else:
                    total_strength -= strength

                total_yogas += 1

    # Calculate the average strength
    avg_strength = total_strength / total_yogas if total_yogas > 0 else 0

    # Scale the average strength to 0-100
    score = (avg_strength + 100) / 2 if avg_strength < 0 else avg_strength

    # Ensure the score is within 0-100
    return max(0.0, min(score, 100.0))
