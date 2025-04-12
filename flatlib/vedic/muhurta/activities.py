"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Muhurta rules for different activities
    in Vedic astrology.
"""

from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from datetime import timedelta

# Import core functions
from flatlib.vedic.muhurta.core import (
    get_muhurta_quality, get_best_muhurta,
    get_auspicious_times, get_inauspicious_times
)

# Import Panchanga functions
from flatlib.vedic.muhurta.panchanga import (
    get_panchanga, is_auspicious_tithi, is_auspicious_nakshatra,
    is_auspicious_yoga, is_auspicious_karana, is_auspicious_vara
)

# Import timing functions
from flatlib.vedic.muhurta.timing import (
    get_rahu_kala, get_yama_ghantaka, get_gulika_kala,
    get_abhijit_muhurta, get_brahma_muhurta
)

# Import event functions
from flatlib.vedic.muhurta.events import (
    is_combust, is_retrograde, is_in_gandanta
)


def get_activity_rules(activity):
    """
    Get the Muhurta rules for a specific activity
    
    Args:
        activity (str): The type of activity
    
    Returns:
        dict: Dictionary with Muhurta rules for the activity
    """
    # Define rules for different activities
    activity_rules = {
        'marriage': {
            'auspicious_tithis': [2, 3, 5, 7, 10, 11, 13],
            'inauspicious_tithis': [4, 8, 9, 14, 30],
            'auspicious_nakshatras': [1, 3, 5, 7, 8, 13, 14, 17, 20, 23, 24, 25, 27],
            'inauspicious_nakshatras': [4, 9, 19],
            'auspicious_varas': [2, 4, 5, 6],  # Monday, Wednesday, Thursday, Friday
            'inauspicious_varas': [3, 7],  # Tuesday, Saturday
            'auspicious_yogas': [2, 3, 4, 5, 7, 8, 11, 12, 14, 16, 20, 21, 22, 23, 24, 25, 26],
            'inauspicious_yogas': [6, 9, 17, 19, 27],
            'auspicious_karanas': [1, 2, 3, 4, 5, 6, 8, 9, 10, 11],
            'inauspicious_karanas': [7],
            'important_planets': [const.VENUS, const.JUPITER, const.MOON],
            'avoid_houses': [6, 8, 12],
            'min_duration': 120,
            'description': 'Marriage is one of the most important samskaras (life rituals) in Vedic tradition. The Muhurta for marriage should be carefully selected to ensure a harmonious and prosperous married life.'
        },
        'travel': {
            'auspicious_tithis': [2, 3, 5, 7, 10, 11, 12],
            'inauspicious_tithis': [4, 8, 9, 14, 30],
            'auspicious_nakshatras': [1, 3, 5, 7, 8, 13, 14, 17, 20, 23, 24, 25, 27],
            'inauspicious_nakshatras': [4, 9, 19],
            'auspicious_varas': [2, 4, 5],  # Monday, Wednesday, Thursday
            'inauspicious_varas': [3, 7],  # Tuesday, Saturday
            'auspicious_yogas': [2, 3, 4, 5, 7, 8, 11, 12, 14, 16, 20, 21, 22, 23, 24, 25, 26],
            'inauspicious_yogas': [6, 9, 17, 19, 27],
            'auspicious_karanas': [1, 2, 3, 4, 5, 6, 8, 9, 10, 11],
            'inauspicious_karanas': [7],
            'important_planets': [const.MERCURY, const.JUPITER, const.MOON],
            'avoid_houses': [6, 8, 12],
            'min_duration': 60,
            'description': 'Travel Muhurta is important for ensuring a safe, successful, and pleasant journey. The direction of travel should also be considered in relation to the day and the Moon\'s position.'
        },
        'business': {
            'auspicious_tithis': [2, 3, 5, 7, 10, 11],
            'inauspicious_tithis': [4, 8, 9, 14, 30],
            'auspicious_nakshatras': [1, 3, 5, 7, 10, 13, 14, 16, 17, 20, 23, 24, 25],
            'inauspicious_nakshatras': [4, 9, 19],
            'auspicious_varas': [2, 4, 5, 6],  # Monday, Wednesday, Thursday, Friday
            'inauspicious_varas': [3, 7],  # Tuesday, Saturday
            'auspicious_yogas': [2, 3, 4, 5, 7, 8, 11, 12, 14, 16, 20, 21, 22, 23, 24, 25, 26],
            'inauspicious_yogas': [6, 9, 17, 19, 27],
            'auspicious_karanas': [1, 2, 3, 4, 5, 6, 8, 9, 10, 11],
            'inauspicious_karanas': [7],
            'important_planets': [const.MERCURY, const.JUPITER, const.SUN],
            'avoid_houses': [6, 8, 12],
            'min_duration': 60,
            'description': 'Business Muhurta is crucial for starting a new business, signing contracts, or making important business decisions. The strength of Mercury and Jupiter is particularly important for business success.'
        },
        'education': {
            'auspicious_tithis': [2, 3, 5, 7, 10, 11, 13],
            'inauspicious_tithis': [4, 8, 9, 14, 30],
            'auspicious_nakshatras': [3, 5, 7, 13, 14, 16, 17, 20, 22, 23, 24, 25, 27],
            'inauspicious_nakshatras': [4, 9, 19],
            'auspicious_varas': [2, 4, 5],  # Monday, Wednesday, Thursday
            'inauspicious_varas': [3, 7],  # Tuesday, Saturday
            'auspicious_yogas': [2, 3, 4, 5, 7, 8, 11, 12, 14, 16, 20, 21, 22, 23, 24, 25, 26],
            'inauspicious_yogas': [6, 9, 17, 19, 27],
            'auspicious_karanas': [1, 2, 3, 4, 5, 6, 8, 9, 10, 11],
            'inauspicious_karanas': [7],
            'important_planets': [const.MERCURY, const.JUPITER, const.SUN],
            'avoid_houses': [6, 8, 12],
            'min_duration': 60,
            'description': 'Education Muhurta is important for beginning education, taking exams, or starting a new course of study. The strength of Mercury and Jupiter is particularly important for educational success.'
        },
        'medical': {
            'auspicious_tithis': [2, 3, 5, 7, 10, 11, 12],
            'inauspicious_tithis': [4, 8, 9, 14, 30],
            'auspicious_nakshatras': [1, 3, 5, 7, 10, 12, 13, 16, 17, 20, 23, 24, 25],
            'inauspicious_nakshatras': [4, 9, 19],
            'auspicious_varas': [2, 4, 5],  # Monday, Wednesday, Thursday
            'inauspicious_varas': [3, 7],  # Tuesday, Saturday
            'auspicious_yogas': [2, 3, 4, 5, 7, 8, 11, 12, 14, 16, 20, 21, 22, 23, 24, 25, 26],
            'inauspicious_yogas': [6, 9, 17, 19, 27],
            'auspicious_karanas': [1, 2, 3, 4, 5, 6, 8, 9, 10, 11],
            'inauspicious_karanas': [7],
            'important_planets': [const.MOON, const.JUPITER, const.SUN],
            'avoid_houses': [6, 8, 12],
            'min_duration': 60,
            'description': 'Medical Muhurta is crucial for scheduling surgeries, starting medical treatments, or taking important medications. The strength of the Moon is particularly important for medical procedures.'
        },
        'house_construction': {
            'auspicious_tithis': [2, 3, 5, 7, 10, 11, 13],
            'inauspicious_tithis': [4, 8, 9, 14, 30],
            'auspicious_nakshatras': [1, 3, 5, 7, 10, 13, 14, 16, 17, 20, 23, 24, 25, 27],
            'inauspicious_nakshatras': [4, 9, 19],
            'auspicious_varas': [2, 4, 5],  # Monday, Wednesday, Thursday
            'inauspicious_varas': [3, 7],  # Tuesday, Saturday
            'auspicious_yogas': [2, 3, 4, 5, 7, 8, 11, 12, 14, 16, 20, 21, 22, 23, 24, 25, 26],
            'inauspicious_yogas': [6, 9, 17, 19, 27],
            'auspicious_karanas': [1, 2, 3, 4, 5, 6, 8, 9, 10, 11],
            'inauspicious_karanas': [7],
            'important_planets': [const.JUPITER, const.VENUS, const.MARS],
            'avoid_houses': [6, 8, 12],
            'min_duration': 120,
            'description': 'House construction Muhurta is important for laying the foundation, starting construction, or moving into a new home. The strength of Jupiter, Venus, and Mars is particularly important for house-related activities.'
        },
        'general': {
            'auspicious_tithis': [2, 3, 5, 7, 10, 11, 13],
            'inauspicious_tithis': [4, 8, 9, 14, 30],
            'auspicious_nakshatras': [1, 3, 5, 7, 10, 13, 14, 16, 17, 20, 23, 24, 25, 27],
            'inauspicious_nakshatras': [4, 9, 19],
            'auspicious_varas': [2, 4, 5, 6],  # Monday, Wednesday, Thursday, Friday
            'inauspicious_varas': [3, 7],  # Tuesday, Saturday
            'auspicious_yogas': [2, 3, 4, 5, 7, 8, 11, 12, 14, 16, 20, 21, 22, 23, 24, 25, 26],
            'inauspicious_yogas': [6, 9, 17, 19, 27],
            'auspicious_karanas': [1, 2, 3, 4, 5, 6, 8, 9, 10, 11],
            'inauspicious_karanas': [7],
            'important_planets': [const.MOON, const.JUPITER, const.VENUS],
            'avoid_houses': [6, 8, 12],
            'min_duration': 60,
            'description': 'General Muhurta is suitable for most activities that do not have specific Muhurta requirements. It ensures that the time chosen is generally auspicious and free from major negative influences.'
        }
    }
    
    # Return the rules for the specified activity
    return activity_rules.get(activity, activity_rules['general'])


def get_activity_score(date, location, activity):
    """
    Calculate the suitability score of a time for a specific activity
    
    Args:
        date (Datetime): The date and time
        location (GeoPos): The geographical location
        activity (str): The type of activity
    
    Returns:
        dict: Dictionary with activity score information
    """
    # Create a chart for the date
    chart = Chart(date, location, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
    
    # Get the Panchanga
    panchanga = get_panchanga(chart)
    
    # Get the activity rules
    rules = get_activity_rules(activity)
    
    # Initialize the score
    score = 0
    max_score = 0
    factors = []
    
    # Check Tithi
    tithi_num = panchanga['tithi']['num']
    max_score += 2
    if tithi_num in rules['auspicious_tithis']:
        score += 2
        factors.append(f"Auspicious Tithi: {panchanga['tithi']['name']}")
    elif tithi_num in rules['inauspicious_tithis']:
        factors.append(f"Inauspicious Tithi: {panchanga['tithi']['name']}")
    else:
        score += 1
        factors.append(f"Neutral Tithi: {panchanga['tithi']['name']}")
    
    # Check Nakshatra
    nakshatra_num = panchanga['nakshatra']['num']
    max_score += 2
    if nakshatra_num in rules['auspicious_nakshatras']:
        score += 2
        factors.append(f"Auspicious Nakshatra: {panchanga['nakshatra']['name']}")
    elif nakshatra_num in rules['inauspicious_nakshatras']:
        factors.append(f"Inauspicious Nakshatra: {panchanga['nakshatra']['name']}")
    else:
        score += 1
        factors.append(f"Neutral Nakshatra: {panchanga['nakshatra']['name']}")
    
    # Check Vara (Weekday)
    vara_num = panchanga['vara']['num']
    max_score += 2
    if vara_num in rules['auspicious_varas']:
        score += 2
        factors.append(f"Auspicious Vara: {panchanga['vara']['name']}")
    elif vara_num in rules['inauspicious_varas']:
        factors.append(f"Inauspicious Vara: {panchanga['vara']['name']}")
    else:
        score += 1
        factors.append(f"Neutral Vara: {panchanga['vara']['name']}")
    
    # Check Yoga
    yoga_num = panchanga['yoga']['num']
    max_score += 1
    if yoga_num in rules['auspicious_yogas']:
        score += 1
        factors.append(f"Auspicious Yoga: {panchanga['yoga']['name']}")
    elif yoga_num in rules['inauspicious_yogas']:
        factors.append(f"Inauspicious Yoga: {panchanga['yoga']['name']}")
    else:
        score += 0.5
        factors.append(f"Neutral Yoga: {panchanga['yoga']['name']}")
    
    # Check Karana
    karana_num = panchanga['karana']['num']
    max_score += 1
    if karana_num in rules['auspicious_karanas']:
        score += 1
        factors.append(f"Auspicious Karana: {panchanga['karana']['name']}")
    elif karana_num in rules['inauspicious_karanas']:
        factors.append(f"Inauspicious Karana: {panchanga['karana']['name']}")
    else:
        score += 0.5
        factors.append(f"Neutral Karana: {panchanga['karana']['name']}")
    
    # Check important planets
    for planet_id in rules['important_planets']:
        max_score += 1
        planet = chart.getObject(planet_id)
        
        # Check if the planet is strong
        is_planet_strong = not is_combust(chart, planet_id) and not is_retrograde(planet)
        
        # Check if the planet is in a good house
        planet_house = get_house_number(chart, planet_id)
        is_in_good_house = planet_house not in rules['avoid_houses']
        
        if is_planet_strong and is_in_good_house:
            score += 1
            factors.append(f"Strong {planet_id} in favorable house")
        elif is_planet_strong:
            score += 0.5
            factors.append(f"Strong {planet_id} in unfavorable house")
        elif is_in_good_house:
            score += 0.5
            factors.append(f"Weak {planet_id} in favorable house")
        else:
            factors.append(f"Weak {planet_id} in unfavorable house")
    
    # Check for inauspicious periods
    max_score += 2
    
    # Get Rahu Kala
    rahu_kala = get_rahu_kala(date, location)
    is_in_rahu_kala = rahu_kala['start'].jd <= date.jd <= rahu_kala['end'].jd
    
    # Get Yama Ghantaka
    yama_ghantaka = get_yama_ghantaka(date, location)
    is_in_yama_ghantaka = yama_ghantaka['start'].jd <= date.jd <= yama_ghantaka['end'].jd
    
    # Get Gulika Kala
    gulika_kala = get_gulika_kala(date, location)
    is_in_gulika_kala = gulika_kala['start'].jd <= date.jd <= gulika_kala['end'].jd
    
    if not (is_in_rahu_kala or is_in_yama_ghantaka or is_in_gulika_kala):
        score += 2
        factors.append("Not in any inauspicious period")
    elif is_in_rahu_kala:
        factors.append("In Rahu Kala (inauspicious)")
    elif is_in_yama_ghantaka:
        factors.append("In Yama Ghantaka (inauspicious)")
    elif is_in_gulika_kala:
        factors.append("In Gulika Kala (inauspicious)")
    
    # Check for special Muhurtas
    max_score += 1
    
    # Get Abhijit Muhurta
    abhijit_muhurta = get_abhijit_muhurta(date, location)
    is_in_abhijit_muhurta = abhijit_muhurta['start'].jd <= date.jd <= abhijit_muhurta['end'].jd
    
    # Get Brahma Muhurta
    brahma_muhurta = get_brahma_muhurta(date, location)
    is_in_brahma_muhurta = brahma_muhurta['start'].jd <= date.jd <= brahma_muhurta['end'].jd
    
    if is_in_abhijit_muhurta:
        score += 1
        factors.append("In Abhijit Muhurta (highly auspicious)")
    elif is_in_brahma_muhurta:
        score += 1
        factors.append("In Brahma Muhurta (highly auspicious)")
    
    # Calculate the percentage score
    percentage = (score / max_score) * 100
    
    # Determine the quality
    if percentage >= 80:
        quality = 'Excellent'
    elif percentage >= 60:
        quality = 'Good'
    elif percentage >= 40:
        quality = 'Neutral'
    elif percentage >= 20:
        quality = 'Inauspicious'
    else:
        quality = 'Highly Inauspicious'
    
    return {
        'activity': activity,
        'score': score,
        'max_score': max_score,
        'percentage': percentage,
        'quality': quality,
        'factors': factors,
        'panchanga': panchanga
    }


def get_best_time_for_activity(start_date, end_date, location, activity):
    """
    Find the best time for a specific activity within a date range
    
    Args:
        start_date (Datetime): The start date and time
        end_date (Datetime): The end date and time
        location (GeoPos): The geographical location
        activity (str): The type of activity
    
    Returns:
        dict: Dictionary with the best time information
    """
    # Get the activity rules
    rules = get_activity_rules(activity)
    
    # Get the minimum duration
    min_duration = rules.get('min_duration', 60)
    
    # Get all auspicious times
    auspicious_times = get_auspicious_times(start_date, end_date, location, min_duration)
    
    # Initialize variables
    best_score = -1
    best_time = None
    
    # Check each auspicious time
    for time_period in auspicious_times:
        # Calculate the activity score
        score = get_activity_score(time_period['start'], location, activity)
        
        # Check if this is the best time so far
        if score['percentage'] > best_score:
            best_score = score['percentage']
            best_time = {
                'start': time_period['start'],
                'end': time_period['end'],
                'duration': time_period['duration'],
                'activity': activity,
                'score': score
            }
    
    return best_time


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
