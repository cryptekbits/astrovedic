"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements analysis tools for Muhurta (electional astrology)
    in Vedic astrology.
"""

from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from datetime import timedelta

# Import core functions
from flatlib.vedic.muhurta.core import get_muhurta_quality
from flatlib.vedic.muhurta.panchanga import get_panchanga
from flatlib.vedic.muhurta.activities import get_activity_score


def analyze_muhurta(date, location):
    """
    Analyze the Muhurta for a specific date and time
    
    Args:
        date (Datetime): The date and time
        location (GeoPos): The geographical location
    
    Returns:
        dict: Dictionary with Muhurta analysis
    """
    # Create a chart for the date
    chart = Chart(date, location, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
    
    # Get the Muhurta quality
    quality = get_muhurta_quality(chart)
    
    # Get the Panchanga
    panchanga = get_panchanga(chart)
    
    # Get the activity scores for different activities
    activities = ['general', 'marriage', 'travel', 'business', 'education', 'medical', 'house_construction']
    activity_scores = {}
    
    for activity in activities:
        activity_scores[activity] = get_activity_score(date, location, activity)
    
    # Get the best activity for this time
    best_activity = max(activity_scores.items(), key=lambda x: x[1]['percentage'])
    
    # Get the planetary positions
    planets = {}
    for planet_id in const.LIST_OBJECTS_VEDIC:
        planet = chart.getObject(planet_id)
        planets[planet_id] = {
            'sign': planet.sign,
            'longitude': planet.lon,
            'house': get_house_number(chart, planet_id)
        }
    
    # Get the Ascendant
    asc = chart.getAngle(const.ASC)
    
    return {
        'date': date,
        'location': {
            'latitude': location.lat,
            'longitude': location.lon
        },
        'quality': quality,
        'panchanga': panchanga,
        'activity_scores': activity_scores,
        'best_activity': {
            'name': best_activity[0],
            'score': best_activity[1]
        },
        'planets': planets,
        'ascendant': {
            'sign': asc.sign,
            'longitude': asc.lon
        }
    }


def get_muhurta_predictions(date, location):
    """
    Generate predictions based on Muhurta for a specific date and time
    
    Args:
        date (Datetime): The date and time
        location (GeoPos): The geographical location
    
    Returns:
        dict: Dictionary with Muhurta predictions
    """
    # Analyze the Muhurta
    analysis = analyze_muhurta(date, location)
    
    # Initialize the predictions
    predictions = {
        'general': [],
        'activities': {},
        'timing': []
    }
    
    # Generate general predictions
    quality = analysis['quality']['quality']
    score = analysis['quality']['score']
    
    if quality == 'Excellent':
        predictions['general'].append("This is an excellent time for most activities. The planetary and Panchanga factors are highly favorable.")
    elif quality == 'Good':
        predictions['general'].append("This is a good time for most activities. The planetary and Panchanga factors are generally favorable.")
    elif quality == 'Neutral':
        predictions['general'].append("This is a neutral time for most activities. Some planetary and Panchanga factors are favorable, while others are not.")
    elif quality == 'Inauspicious':
        predictions['general'].append("This is an inauspicious time for most activities. Many planetary and Panchanga factors are unfavorable.")
    elif quality == 'Highly Inauspicious':
        predictions['general'].append("This is a highly inauspicious time for most activities. The planetary and Panchanga factors are very unfavorable.")
    
    # Generate activity-specific predictions
    for activity, score in analysis['activity_scores'].items():
        if score['quality'] in ['Excellent', 'Good']:
            predictions['activities'][activity] = f"This is a {score['quality'].lower()} time for {activity}. {', '.join(score['factors'][:3])}"
        else:
            predictions['activities'][activity] = f"This is not a favorable time for {activity}. {', '.join(score['factors'][:3])}"
    
    # Generate timing predictions
    panchanga = analysis['panchanga']
    
    # Tithi prediction
    tithi = panchanga['tithi']
    if tithi['type'] == 'Nanda':
        predictions['timing'].append(f"The current Tithi ({tithi['name']}) is a Nanda Tithi, which is good for starting new ventures and celebrations.")
    elif tithi['type'] == 'Bhadra':
        predictions['timing'].append(f"The current Tithi ({tithi['name']}) is a Bhadra Tithi, which is good for steady work and building foundations.")
    elif tithi['type'] == 'Jaya':
        predictions['timing'].append(f"The current Tithi ({tithi['name']}) is a Jaya Tithi, which is good for competitive activities and victory.")
    elif tithi['type'] == 'Rikta':
        predictions['timing'].append(f"The current Tithi ({tithi['name']}) is a Rikta Tithi, which is not good for starting new ventures but can be used for completing old tasks.")
    elif tithi['type'] == 'Purna':
        predictions['timing'].append(f"The current Tithi ({tithi['name']}) is a Purna Tithi, which is good for completion and fulfillment of desires.")
    
    # Nakshatra prediction
    nakshatra = panchanga['nakshatra']
    if nakshatra['type'] == 'Movable':
        predictions['timing'].append(f"The current Nakshatra ({nakshatra['name']}) is a Movable Nakshatra, which is good for travel and activities requiring movement.")
    elif nakshatra['type'] == 'Fixed':
        predictions['timing'].append(f"The current Nakshatra ({nakshatra['name']}) is a Fixed Nakshatra, which is good for stable activities and long-term projects.")
    elif nakshatra['type'] == 'Mixed':
        predictions['timing'].append(f"The current Nakshatra ({nakshatra['name']}) is a Mixed Nakshatra, which is good for a variety of activities.")
    
    # Vara prediction
    vara = panchanga['vara']
    if vara['name'] == 'Monday':
        predictions['timing'].append("Monday is ruled by the Moon and is good for emotional and nurturing activities.")
    elif vara['name'] == 'Tuesday':
        predictions['timing'].append("Tuesday is ruled by Mars and is good for energetic and competitive activities.")
    elif vara['name'] == 'Wednesday':
        predictions['timing'].append("Wednesday is ruled by Mercury and is good for intellectual and communication activities.")
    elif vara['name'] == 'Thursday':
        predictions['timing'].append("Thursday is ruled by Jupiter and is good for educational and spiritual activities.")
    elif vara['name'] == 'Friday':
        predictions['timing'].append("Friday is ruled by Venus and is good for artistic and relationship activities.")
    elif vara['name'] == 'Saturday':
        predictions['timing'].append("Saturday is ruled by Saturn and is good for disciplined and structured activities.")
    elif vara['name'] == 'Sunday':
        predictions['timing'].append("Sunday is ruled by the Sun and is good for authoritative and leadership activities.")
    
    return predictions


def get_muhurta_compatibility(date1, date2, location):
    """
    Calculate the compatibility between two Muhurtas
    
    Args:
        date1 (Datetime): The first date and time
        date2 (Datetime): The second date and time
        location (GeoPos): The geographical location
    
    Returns:
        dict: Dictionary with compatibility information
    """
    # Analyze both Muhurtas
    analysis1 = analyze_muhurta(date1, location)
    analysis2 = analyze_muhurta(date2, location)
    
    # Initialize the compatibility
    compatibility = {
        'score': 0,
        'factors': [],
        'description': ''
    }
    
    # Compare the Muhurta qualities
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
    
    # Compare the Panchangas
    panchanga1 = analysis1['panchanga']
    panchanga2 = analysis2['panchanga']
    
    # Check Tithi compatibility
    tithi1 = panchanga1['tithi']['type']
    tithi2 = panchanga2['tithi']['type']
    
    if tithi1 == tithi2:
        compatibility['score'] += 10
        compatibility['factors'].append(f"Both times have the same Tithi type ({tithi1})")
    elif (tithi1 in ['Nanda', 'Bhadra', 'Jaya'] and tithi2 in ['Nanda', 'Bhadra', 'Jaya']):
        compatibility['score'] += 5
        compatibility['factors'].append(f"Both times have compatible Tithi types ({tithi1} and {tithi2})")
    
    # Check Nakshatra compatibility
    nakshatra1 = panchanga1['nakshatra']['type']
    nakshatra2 = panchanga2['nakshatra']['type']
    
    if nakshatra1 == nakshatra2:
        compatibility['score'] += 10
        compatibility['factors'].append(f"Both times have the same Nakshatra type ({nakshatra1})")
    elif (nakshatra1 == 'Mixed' or nakshatra2 == 'Mixed'):
        compatibility['score'] += 5
        compatibility['factors'].append(f"One time has a Mixed Nakshatra type, which is compatible with other types")
    
    # Check Vara compatibility
    vara1 = panchanga1['vara']['num']
    vara2 = panchanga2['vara']['num']
    
    # Define compatible Varas
    compatible_varas = {
        1: [2, 5],  # Sunday: Monday, Thursday
        2: [1, 4, 5],  # Monday: Sunday, Wednesday, Thursday
        3: [6, 7],  # Tuesday: Friday, Saturday
        4: [2, 5],  # Wednesday: Monday, Thursday
        5: [1, 2, 4],  # Thursday: Sunday, Monday, Wednesday
        6: [3, 7],  # Friday: Tuesday, Saturday
        7: [3, 6]  # Saturday: Tuesday, Friday
    }
    
    if vara1 == vara2:
        compatibility['score'] += 10
        compatibility['factors'].append(f"Both times have the same Vara ({panchanga1['vara']['name']})")
    elif vara2 in compatible_varas.get(vara1, []):
        compatibility['score'] += 5
        compatibility['factors'].append(f"The Varas ({panchanga1['vara']['name']} and {panchanga2['vara']['name']}) are compatible")
    
    # Ensure the score is between 0 and 100
    compatibility['score'] = min(100, max(0, compatibility['score']))
    
    # Generate a description based on the score
    if compatibility['score'] >= 80:
        compatibility['description'] = "These two times are highly compatible and would work well together for related activities."
    elif compatibility['score'] >= 60:
        compatibility['description'] = "These two times are compatible and would generally work well together for related activities."
    elif compatibility['score'] >= 40:
        compatibility['description'] = "These two times have moderate compatibility and may work together for some activities."
    elif compatibility['score'] >= 20:
        compatibility['description'] = "These two times have low compatibility and may not work well together for most activities."
    else:
        compatibility['description'] = "These two times are incompatible and should not be used together for related activities."
    
    return compatibility


def get_muhurta_strength_score(date, location):
    """
    Calculate the overall strength score of a Muhurta
    
    Args:
        date (Datetime): The date and time
        location (GeoPos): The geographical location
    
    Returns:
        float: The overall strength score (0-100)
    """
    # Create a chart for the date
    chart = Chart(date, location, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
    
    # Get the Muhurta quality
    quality = get_muhurta_quality(chart)
    
    # Get the Panchanga
    panchanga = get_panchanga(chart)
    
    # Initialize the score
    score = 0
    
    # Add the quality score
    quality_scores = {
        'Excellent': 50,
        'Good': 40,
        'Neutral': 30,
        'Inauspicious': 20,
        'Highly Inauspicious': 10
    }
    
    score += quality_scores.get(quality['quality'], 30)
    
    # Add Panchanga scores
    
    # Tithi score
    tithi_scores = {
        'Nanda': 10,
        'Bhadra': 8,
        'Jaya': 6,
        'Rikta': 4,
        'Purna': 10
    }
    
    score += tithi_scores.get(panchanga['tithi']['type'], 5)
    
    # Nakshatra score
    nakshatra_scores = {
        'Movable': 8,
        'Fixed': 10,
        'Mixed': 6
    }
    
    score += nakshatra_scores.get(panchanga['nakshatra']['type'], 5)
    
    # Yoga score
    yoga_scores = {
        'Auspicious': 10,
        'Inauspicious': 5
    }
    
    score += yoga_scores.get(panchanga['yoga']['type'], 5)
    
    # Karana score
    karana_scores = {
        'Movable': 8,
        'Fixed': 10
    }
    
    score += karana_scores.get(panchanga['karana']['type'], 5)
    
    # Vara score
    vara_scores = {
        1: 8,  # Sunday
        2: 10,  # Monday
        3: 6,  # Tuesday
        4: 10,  # Wednesday
        5: 10,  # Thursday
        6: 8,  # Friday
        7: 6  # Saturday
    }
    
    score += vara_scores.get(panchanga['vara']['num'], 5)
    
    # Ensure the score is between 0 and 100
    score = min(100, max(0, score))
    
    return score


def get_house_number(chart, planet_id):
    """
    Get the house number of a planet
    
    Args:
        chart (Chart): The chart
        planet_id (str): The ID of the planet
    
    Returns:
        int: The house number (1-12) of the planet
    """
    # Get the planet
    planet = chart.getObject(planet_id)
    
    # Get the Ascendant
    asc = chart.getAngle(const.ASC)
    
    # Calculate the house number
    from flatlib import angle
    house_num = 1 + int(angle.distance(planet.lon, asc.lon) / 30) % 12
    
    # Adjust for 0-based indexing
    if house_num == 0:
        house_num = 12
    
    return house_num
