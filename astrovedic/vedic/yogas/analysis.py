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


def get_yoga_predictions(chart, yogas):
    """
    Generate predictions based on Yogas in a chart
    
    Args:
        chart (Chart): The birth chart
        yogas (dict): Dictionary with Yoga information
    
    Returns:
        dict: Dictionary with Yoga predictions
    """
    # Initialize the result
    result = {
        'general': [],
        'personality': [],
        'career': [],
        'wealth': [],
        'relationships': [],
        'health': [],
        'challenges': []
    }
    
    # Generate general predictions
    total_yogas = yogas['summary']['total_yogas']
    beneficial_yogas = yogas['summary']['beneficial_yogas']
    harmful_yogas = yogas['summary']['harmful_yogas']
    
    if total_yogas > 0:
        ratio = beneficial_yogas / total_yogas
        
        if ratio >= 0.8:
            result['general'].append("The chart has a very high number of beneficial Yogas, indicating a highly fortunate life with many opportunities for success and happiness.")
        elif ratio >= 0.6:
            result['general'].append("The chart has a good number of beneficial Yogas, indicating a generally fortunate life with opportunities for success.")
        elif ratio >= 0.4:
            result['general'].append("The chart has a balanced mix of beneficial and challenging Yogas, indicating a life with both opportunities and challenges.")
        elif ratio >= 0.2:
            result['general'].append("The chart has more challenging Yogas than beneficial ones, indicating a life with significant obstacles to overcome.")
        else:
            result['general'].append("The chart has a high number of challenging Yogas, indicating a life with many difficulties and obstacles.")
    
    # Generate predictions based on Mahapurusha Yogas
    has_mahapurusha = False
    for yoga in yogas.get('mahapurusha_yogas', []):
        has_mahapurusha = True
        
        if yoga['name'] == 'Ruchaka Yoga':
            result['personality'].append("Ruchaka Yoga gives a strong, courageous, and ambitious personality with leadership qualities.")
            result['career'].append("Ruchaka Yoga indicates success in competitive fields, sports, military, or technical professions.")
        elif yoga['name'] == 'Bhadra Yoga':
            result['personality'].append("Bhadra Yoga gives an intelligent, analytical, and communicative personality with good business sense.")
            result['career'].append("Bhadra Yoga indicates success in business, writing, teaching, or intellectual pursuits.")
        elif yoga['name'] == 'Hamsa Yoga':
            result['personality'].append("Hamsa Yoga gives a wise, spiritual, and benevolent personality with strong moral values.")
            result['career'].append("Hamsa Yoga indicates success in teaching, counseling, law, or religious fields.")
        elif yoga['name'] == 'Malavya Yoga':
            result['personality'].append("Malavya Yoga gives a charming, artistic, and refined personality with a love for beauty and comfort.")
            result['career'].append("Malavya Yoga indicates success in arts, entertainment, luxury goods, or diplomatic fields.")
        elif yoga['name'] == 'Sasa Yoga':
            result['personality'].append("Sasa Yoga gives a disciplined, patient, and hardworking personality with a serious outlook on life.")
            result['career'].append("Sasa Yoga indicates success in government, administration, or fields requiring long-term planning.")
    
    if has_mahapurusha:
        result['general'].append("The presence of Mahapurusha Yoga(s) indicates a person of great stature and accomplishment.")
    
    # Generate predictions based on Raja Yogas
    has_raja = False
    for yoga in yogas.get('raja_yogas', []):
        has_raja = True
        
        if yoga['name'] == 'Dharmakarmaadhipati Yoga':
            result['career'].append("Dharmakarmaadhipati Yoga indicates high position, authority, and success in career.")
        elif yoga['name'] == 'Gajakesari Yoga':
            result['general'].append("Gajakesari Yoga indicates good fortune, wisdom, and success in life.")
        elif yoga['name'] == 'Amala Yoga':
            result['personality'].append("Amala Yoga indicates a pure character, good reputation, and ethical conduct.")
        elif yoga['name'] == 'Sreenatha Yoga':
            result['wealth'].append("Sreenatha Yoga indicates wealth, prosperity, and financial success.")
        elif yoga['name'] == 'Chandra Mangala Yoga':
            result['general'].append("Chandra Mangala Yoga indicates courage, energy, and success in undertakings.")
    
    if has_raja:
        result['general'].append("The presence of Raja Yoga(s) indicates power, authority, and high social status.")
    
    # Generate predictions based on Dhana Yogas
    has_dhana = False
    for yoga in yogas.get('dhana_yogas', []):
        has_dhana = True
        
        if yoga['name'] == 'Lakshmi Yoga':
            result['wealth'].append("Lakshmi Yoga indicates wealth, prosperity, and financial success.")
        elif yoga['name'] == 'Kubera Yoga':
            result['wealth'].append("Kubera Yoga indicates the ability to accumulate wealth and material possessions.")
        elif yoga['name'] == 'Kalanidhi Yoga':
            result['wealth'].append("Kalanidhi Yoga indicates wealth through knowledge, education, or creative pursuits.")
        elif yoga['name'] == 'Vasumati Yoga':
            result['wealth'].append("Vasumati Yoga indicates wealth through land, property, or natural resources.")
        elif yoga['name'] == 'Mridanga Yoga':
            result['wealth'].append("Mridanga Yoga indicates wealth through multiple sources and financial stability.")
    
    if has_dhana:
        result['general'].append("The presence of Dhana Yoga(s) indicates wealth, prosperity, and financial success.")
    
    # Generate predictions based on Dosha Yogas
    has_dosha = False
    for yoga in yogas.get('dosha_yogas', []):
        has_dosha = True
        
        if yoga['name'] == 'Kemadruma Yoga':
            result['challenges'].append("Kemadruma Yoga indicates challenges in achieving success and stability in life.")
        elif yoga['name'] == 'Daridra Yoga':
            result['challenges'].append("Daridra Yoga indicates financial difficulties and struggles with poverty.")
        elif yoga['name'] == 'Shakat Yoga':
            result['challenges'].append("Shakat Yoga indicates conflicts with authority figures and obstacles in career.")
        elif yoga['name'] == 'Kalasarpa Yoga':
            result['challenges'].append("Kalasarpa Yoga indicates karmic challenges and obstacles in various areas of life.")
        elif yoga['name'] == 'Graha Yuddha':
            result['challenges'].append("Graha Yuddha indicates internal conflicts and difficulties in decision-making.")
    
    if has_dosha:
        result['general'].append("The presence of Dosha Yoga(s) indicates challenges and obstacles that need to be overcome.")
    
    return result


def get_yoga_compatibility(chart1, chart2):
    """
    Calculate compatibility between two charts based on Yogas
    
    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart
    
    Returns:
        dict: Dictionary with compatibility information
    """
    # Get the Yogas in each chart
    from astrovedic.vedic.yogas import get_all_yogas
    yogas1 = get_all_yogas(chart1)
    yogas2 = get_all_yogas(chart2)
    
    # Initialize the result
    result = {
        'compatibility_score': 0,
        'compatibility_factors': [],
        'compatibility_challenges': []
    }
    
    # Calculate compatibility based on beneficial Yogas
    beneficial_yogas1 = yogas1['summary']['beneficial_yogas']
    beneficial_yogas2 = yogas2['summary']['beneficial_yogas']
    
    # Calculate the average number of beneficial Yogas
    avg_beneficial = (beneficial_yogas1 + beneficial_yogas2) / 2
    
    # Adjust the compatibility score based on beneficial Yogas
    if avg_beneficial >= 5:
        result['compatibility_score'] += 30
        result['compatibility_factors'].append("Both charts have a high number of beneficial Yogas, indicating a harmonious relationship.")
    elif avg_beneficial >= 3:
        result['compatibility_score'] += 20
        result['compatibility_factors'].append("Both charts have a good number of beneficial Yogas, indicating a generally positive relationship.")
    elif avg_beneficial >= 1:
        result['compatibility_score'] += 10
        result['compatibility_factors'].append("Both charts have some beneficial Yogas, indicating potential for a positive relationship.")
    
    # Calculate compatibility based on harmful Yogas
    harmful_yogas1 = yogas1['summary']['harmful_yogas']
    harmful_yogas2 = yogas2['summary']['harmful_yogas']
    
    # Calculate the average number of harmful Yogas
    avg_harmful = (harmful_yogas1 + harmful_yogas2) / 2
    
    # Adjust the compatibility score based on harmful Yogas
    if avg_harmful >= 3:
        result['compatibility_score'] -= 30
        result['compatibility_challenges'].append("Both charts have a high number of challenging Yogas, indicating potential difficulties in the relationship.")
    elif avg_harmful >= 2:
        result['compatibility_score'] -= 20
        result['compatibility_challenges'].append("Both charts have some challenging Yogas, indicating potential obstacles in the relationship.")
    elif avg_harmful >= 1:
        result['compatibility_score'] -= 10
        result['compatibility_challenges'].append("Both charts have a few challenging Yogas, indicating minor challenges in the relationship.")
    
    # Check for specific Yogas that enhance compatibility
    has_compatibility_enhancing_yogas = False
    
    # Check for Gajakesari Yoga in both charts
    has_gajakesari1 = any(yoga['name'] == 'Gajakesari Yoga' for yoga in yogas1.get('raja_yogas', []))
    has_gajakesari2 = any(yoga['name'] == 'Gajakesari Yoga' for yoga in yogas2.get('raja_yogas', []))
    
    if has_gajakesari1 and has_gajakesari2:
        result['compatibility_score'] += 15
        result['compatibility_factors'].append("Both charts have Gajakesari Yoga, indicating mutual respect, understanding, and harmony.")
        has_compatibility_enhancing_yogas = True
    
    # Check for Malavya Yoga in both charts
    has_malavya1 = any(yoga['name'] == 'Malavya Yoga' for yoga in yogas1.get('mahapurusha_yogas', []))
    has_malavya2 = any(yoga['name'] == 'Malavya Yoga' for yoga in yogas2.get('mahapurusha_yogas', []))
    
    if has_malavya1 and has_malavya2:
        result['compatibility_score'] += 15
        result['compatibility_factors'].append("Both charts have Malavya Yoga, indicating mutual attraction, affection, and enjoyment of life together.")
        has_compatibility_enhancing_yogas = True
    
    # Check for specific Yogas that challenge compatibility
    has_compatibility_challenging_yogas = False
    
    # Check for Kemadruma Yoga in both charts
    has_kemadruma1 = any(yoga['name'] == 'Kemadruma Yoga' for yoga in yogas1.get('dosha_yogas', []))
    has_kemadruma2 = any(yoga['name'] == 'Kemadruma Yoga' for yoga in yogas2.get('dosha_yogas', []))
    
    if has_kemadruma1 and has_kemadruma2:
        result['compatibility_score'] -= 15
        result['compatibility_challenges'].append("Both charts have Kemadruma Yoga, indicating potential instability and lack of support in the relationship.")
        has_compatibility_challenging_yogas = True
    
    # Check for Graha Yuddha in both charts
    has_graha_yuddha1 = any(yoga['name'] == 'Graha Yuddha' for yoga in yogas1.get('dosha_yogas', []))
    has_graha_yuddha2 = any(yoga['name'] == 'Graha Yuddha' for yoga in yogas2.get('dosha_yogas', []))
    
    if has_graha_yuddha1 and has_graha_yuddha2:
        result['compatibility_score'] -= 15
        result['compatibility_challenges'].append("Both charts have Graha Yuddha, indicating potential conflicts and power struggles in the relationship.")
        has_compatibility_challenging_yogas = True
    
    # Ensure the compatibility score is within 0-100
    result['compatibility_score'] = max(0, min(result['compatibility_score'] + 50, 100))
    
    # Add a general compatibility description
    if result['compatibility_score'] >= 80:
        result['description'] = "Excellent compatibility with strong potential for a harmonious and fulfilling relationship."
    elif result['compatibility_score'] >= 60:
        result['description'] = "Good compatibility with potential for a positive and supportive relationship."
    elif result['compatibility_score'] >= 40:
        result['description'] = "Moderate compatibility with both strengths and challenges in the relationship."
    elif result['compatibility_score'] >= 20:
        result['description'] = "Challenging compatibility with significant obstacles to overcome in the relationship."
    else:
        result['description'] = "Poor compatibility with major challenges and potential for conflict in the relationship."
    
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
