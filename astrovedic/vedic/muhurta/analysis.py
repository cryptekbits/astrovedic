"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements analysis tools for Muhurta (electional astrology)
    in Vedic astrology.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from datetime import timedelta

# Import core functions
from astrovedic.vedic.muhurta.core import get_muhurta_quality
from astrovedic.vedic.muhurta.panchanga import get_panchanga
from astrovedic.vedic.muhurta.activities import get_activity_score


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


def get_muhurta_data(date, location):
    """
    Get Muhurta data for a specific date and time

    Args:
        date (Datetime): The date and time
        location (GeoPos): The geographical location

    Returns:
        dict: Dictionary with Muhurta data
    """
    # Analyze the Muhurta
    analysis = analyze_muhurta(date, location)

    # Initialize the data structure
    data = {
        'quality': analysis['quality'],
        'panchanga': analysis['panchanga'],
        'activity_scores': analysis['activity_scores'],
        'best_activity': analysis['best_activity'],
        'planets': analysis['planets'],
        'ascendant': analysis['ascendant']
    }

    return data


def get_muhurta_comparison(date1, date2, location):
    """
    Compare two Muhurtas

    Args:
        date1 (Datetime): The first date and time
        date2 (Datetime): The second date and time
        location (GeoPos): The geographical location

    Returns:
        dict: Dictionary with comparison information
    """
    # Analyze both Muhurtas
    analysis1 = analyze_muhurta(date1, location)
    analysis2 = analyze_muhurta(date2, location)

    # Initialize the comparison
    comparison = {
        'score': 0,
        'factors': []
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

    # Add to the comparison score
    comparison['score'] += avg_quality * 10

    # Compare the Panchangas
    panchanga1 = analysis1['panchanga']
    panchanga2 = analysis2['panchanga']

    # Check Tithi compatibility
    tithi1 = panchanga1['tithi']['type']
    tithi2 = panchanga2['tithi']['type']

    if tithi1 == tithi2:
        comparison['score'] += 10
        comparison['factors'].append(f"Same Tithi type: {tithi1}")
    elif (tithi1 in ['Nanda', 'Bhadra', 'Jaya'] and tithi2 in ['Nanda', 'Bhadra', 'Jaya']):
        comparison['score'] += 5
        comparison['factors'].append(f"Compatible Tithi types: {tithi1} and {tithi2}")

    # Check Nakshatra compatibility
    nakshatra1 = panchanga1['nakshatra']['type']
    nakshatra2 = panchanga2['nakshatra']['type']

    if nakshatra1 == nakshatra2:
        comparison['score'] += 10
        comparison['factors'].append(f"Same Nakshatra type: {nakshatra1}")
    elif (nakshatra1 == 'Mixed' or nakshatra2 == 'Mixed'):
        comparison['score'] += 5
        comparison['factors'].append(f"One Mixed Nakshatra type")

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
        comparison['score'] += 10
        comparison['factors'].append(f"Same Vara: {panchanga1['vara']['name']}")
    elif vara2 in compatible_varas.get(vara1, []):
        comparison['score'] += 5
        comparison['factors'].append(f"Compatible Varas: {panchanga1['vara']['name']} and {panchanga2['vara']['name']}")

    # Ensure the score is between 0 and 100
    comparison['score'] = min(100, max(0, comparison['score']))

    return comparison


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
    from astrovedic import angle
    house_num = 1 + int(angle.distance(planet.lon, asc.lon) / 30) % 12

    # Adjust for 0-based indexing
    if house_num == 0:
        house_num = 12

    return house_num
