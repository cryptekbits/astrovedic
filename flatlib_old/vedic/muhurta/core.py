"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements core functionality for Muhurta (electional astrology)
    calculations in Vedic astrology.
"""

from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from datetime import timedelta

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

# Constants for Muhurta quality
EXCELLENT = 'Excellent'
GOOD = 'Good'
NEUTRAL = 'Neutral'
INAUSPICIOUS = 'Inauspicious'
HIGHLY_INAUSPICIOUS = 'Highly Inauspicious'


def get_muhurta_quality(chart):
    """
    Calculate the quality of a Muhurta based on Panchanga and planetary positions
    
    Args:
        chart (Chart): The chart for the time to evaluate
    
    Returns:
        dict: Dictionary with Muhurta quality information
    """
    # Get the Panchanga
    panchanga = get_panchanga(chart)
    
    # Initialize the score
    score = 0
    
    # Check Tithi
    tithi = panchanga['tithi']
    if is_auspicious_tithi(tithi['num']):
        score += 2
    elif tithi['num'] in [4, 9, 14]:  # Chaturthi, Navami, Chaturdashi
        score -= 1
    elif tithi['num'] in [8, 12, 30]:  # Ashtami, Dwadashi, Amavasya
        score -= 2
    
    # Check Nakshatra
    nakshatra = panchanga['nakshatra']
    if is_auspicious_nakshatra(nakshatra['num']):
        score += 2
    elif nakshatra['num'] in [3, 5, 7]:  # Krittika, Mrigashira, Punarvasu
        score += 1
    elif nakshatra['num'] in [4, 9, 19]:  # Rohini, Ashlesha, Moola
        score -= 1
    elif nakshatra['num'] in [1, 10, 16, 18]:  # Ashwini, Magha, Vishakha, Jyeshtha
        score -= 2
    
    # Check Yoga
    yoga = panchanga['yoga']
    if is_auspicious_yoga(yoga['num']):
        score += 1
    elif yoga['num'] in [6, 9, 28]:  # Atiganda, Shoola, Vyaghata
        score -= 1
    
    # Check Karana
    karana = panchanga['karana']
    if is_auspicious_karana(karana['num']):
        score += 1
    elif karana['num'] in [4, 7, 11]:  # Vishti, Shakuni, Chatushpada
        score -= 1
    
    # Check Vara (Weekday)
    vara = panchanga['vara']
    if is_auspicious_vara(vara['num']):
        score += 1
    elif vara['num'] in [1, 6]:  # Sunday, Friday
        score += 0
    elif vara['num'] in [3, 7]:  # Tuesday, Saturday
        score -= 1
    
    # Check planetary positions
    # Moon's position
    moon = chart.getObject(const.MOON)
    moon_house = get_house_number(chart, const.MOON)
    
    if moon_house in [1, 4, 7, 10]:  # Kendra houses
        score += 1
    elif moon_house in [6, 8, 12]:  # Dusthana houses
        score -= 1
    
    # Check if Moon is conjunct with malefics
    if is_conjunct_with_malefics(chart, const.MOON):
        score -= 1
    
    # Check if Moon is aspected by benefics
    if is_aspected_by_benefics(chart, const.MOON):
        score += 1
    
    # Check if Lagna is strong
    if is_lagna_strong(chart):
        score += 1
    
    # Check if there are planets in the 8th house
    if has_planets_in_8th_house(chart):
        score -= 1
    
    # Determine the quality based on the score
    if score >= 5:
        quality = EXCELLENT
    elif score >= 2:
        quality = GOOD
    elif score >= -1:
        quality = NEUTRAL
    elif score >= -4:
        quality = INAUSPICIOUS
    else:
        quality = HIGHLY_INAUSPICIOUS
    
    return {
        'score': score,
        'quality': quality,
        'panchanga': panchanga
    }


def get_best_muhurta(start_date, end_date, location, interval_minutes=60):
    """
    Find the best Muhurta within a date range
    
    Args:
        start_date (Datetime): The start date and time
        end_date (Datetime): The end date and time
        location (GeoPos): The geographical location
        interval_minutes (int, optional): The interval in minutes to check
    
    Returns:
        dict: Dictionary with the best Muhurta information
    """
    # Convert start_date and end_date to Python datetime objects
    start_dt = start_date.datetime()
    end_dt = end_date.datetime()
    
    # Initialize variables
    best_score = -float('inf')
    best_muhurta = None
    
    # Iterate through the date range
    current_dt = start_dt
    while current_dt < end_dt:
        # Create a Datetime object for the current time
        current_date = Datetime.fromDatetime(current_dt)
        
        # Create a chart for the current time
        chart = Chart(current_date, location, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
        
        # Get the Muhurta quality
        quality = get_muhurta_quality(chart)
        
        # Check if this is the best Muhurta so far
        if quality['score'] > best_score:
            best_score = quality['score']
            best_muhurta = {
                'date': current_date,
                'quality': quality
            }
        
        # Move to the next interval
        current_dt += timedelta(minutes=interval_minutes)
    
    return best_muhurta


def get_auspicious_times(start_date, end_date, location, min_duration=60):
    """
    Find auspicious time periods within a date range
    
    Args:
        start_date (Datetime): The start date and time
        end_date (Datetime): The end date and time
        location (GeoPos): The geographical location
        min_duration (int, optional): Minimum duration in minutes
    
    Returns:
        list: List of auspicious time periods
    """
    # Convert start_date and end_date to Python datetime objects
    start_dt = start_date.datetime()
    end_dt = end_date.datetime()
    
    # Initialize variables
    auspicious_times = []
    current_period = None
    
    # Iterate through the date range in 15-minute intervals
    current_dt = start_dt
    while current_dt < end_dt:
        # Create a Datetime object for the current time
        current_date = Datetime.fromDatetime(current_dt)
        
        # Create a chart for the current time
        chart = Chart(current_date, location, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
        
        # Get the Muhurta quality
        quality = get_muhurta_quality(chart)
        
        # Check if this is an auspicious time
        is_auspicious = quality['quality'] in [EXCELLENT, GOOD]
        
        # Check if we need to start a new period
        if is_auspicious and current_period is None:
            current_period = {
                'start': current_date,
                'end': None,
                'quality': quality['quality']
            }
        
        # Check if we need to end the current period
        elif not is_auspicious and current_period is not None:
            current_period['end'] = current_date
            
            # Calculate the duration in minutes
            duration = (current_date.datetime() - current_period['start'].datetime()).total_seconds() / 60
            
            # Add the period if it meets the minimum duration
            if duration >= min_duration:
                current_period['duration'] = duration
                auspicious_times.append(current_period)
            
            current_period = None
        
        # Move to the next interval
        current_dt += timedelta(minutes=15)
    
    # Handle the case where the last period extends to the end of the range
    if current_period is not None:
        current_period['end'] = end_date
        
        # Calculate the duration in minutes
        duration = (end_date.datetime() - current_period['start'].datetime()).total_seconds() / 60
        
        # Add the period if it meets the minimum duration
        if duration >= min_duration:
            current_period['duration'] = duration
            auspicious_times.append(current_period)
    
    return auspicious_times


def get_inauspicious_times(start_date, end_date, location):
    """
    Find inauspicious time periods within a date range
    
    Args:
        start_date (Datetime): The start date and time
        end_date (Datetime): The end date and time
        location (GeoPos): The geographical location
    
    Returns:
        list: List of inauspicious time periods
    """
    # Convert start_date and end_date to Python datetime objects
    start_dt = start_date.datetime()
    end_dt = end_date.datetime()
    
    # Initialize variables
    inauspicious_times = []
    
    # Iterate through each day in the date range
    current_dt = start_dt
    while current_dt < end_dt:
        # Create a Datetime object for the current day
        current_date = Datetime.fromDatetime(current_dt)
        
        # Get Rahu Kala
        rahu_kala = get_rahu_kala(current_date, location)
        if rahu_kala['start'].datetime() < end_dt and rahu_kala['end'].datetime() > start_dt:
            inauspicious_times.append({
                'type': 'Rahu Kala',
                'start': rahu_kala['start'],
                'end': rahu_kala['end'],
                'description': 'Inauspicious period ruled by Rahu'
            })
        
        # Get Yama Ghantaka
        yama_ghantaka = get_yama_ghantaka(current_date, location)
        if yama_ghantaka['start'].datetime() < end_dt and yama_ghantaka['end'].datetime() > start_dt:
            inauspicious_times.append({
                'type': 'Yama Ghantaka',
                'start': yama_ghantaka['start'],
                'end': yama_ghantaka['end'],
                'description': 'Inauspicious period ruled by Yama'
            })
        
        # Get Gulika Kala
        gulika_kala = get_gulika_kala(current_date, location)
        if gulika_kala['start'].datetime() < end_dt and gulika_kala['end'].datetime() > start_dt:
            inauspicious_times.append({
                'type': 'Gulika Kala',
                'start': gulika_kala['start'],
                'end': gulika_kala['end'],
                'description': 'Inauspicious period ruled by Gulika'
            })
        
        # Move to the next day
        current_dt += timedelta(days=1)
    
    return inauspicious_times


def get_house_number(chart, planet_id):
    """
    Get the house number of a planet
    
    Args:
        chart (Chart): The birth chart
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


def is_conjunct_with_malefics(chart, planet_id):
    """
    Check if a planet is conjunct with malefics
    
    Args:
        chart (Chart): The chart
        planet_id (str): The ID of the planet to check
    
    Returns:
        bool: True if the planet is conjunct with malefics, False otherwise
    """
    # Get the planet
    planet = chart.getObject(planet_id)
    
    # List of malefic planets
    malefics = [const.SUN, const.MARS, const.SATURN, const.RAHU, const.KETU]
    
    # Check if the planet is conjunct with any malefic
    for malefic_id in malefics:
        if malefic_id == planet_id:
            continue  # Skip the planet itself
        
        malefic = chart.getObject(malefic_id)
        
        # Calculate the orb
        from flatlib import angle
        orb = abs(angle.closestdistance(planet.lon, malefic.lon))
        
        # Check if the planets are conjunct
        if orb <= 10:  # 10 degrees orb
            return True
    
    return False


def is_aspected_by_benefics(chart, planet_id):
    """
    Check if a planet is aspected by benefics
    
    Args:
        chart (Chart): The chart
        planet_id (str): The ID of the planet to check
    
    Returns:
        bool: True if the planet is aspected by benefics, False otherwise
    """
    # Get the target object (planet or Ascendant)
    if planet_id == const.ASC:
        target_object = chart.getAngle(const.ASC) # Use getAngle method
    else:
        target_object = chart.getObject(planet_id)

    # If target object doesn't exist (e.g., in some chart types), return False
    if target_object is None:
        return False

    # List of benefic planets
    benefics = [const.MOON, const.MERCURY, const.JUPITER, const.VENUS]
    
    # Check if the planet is aspected by any benefic
    for benefic_id in benefics:
        if benefic_id == planet_id:
            continue  # Skip the planet itself
        
        benefic = chart.getObject(benefic_id)
        
        # Calculate the orb for different aspects
        from flatlib import angle
        
        # Check for conjunction (0 degrees)
        conj_orb = abs(angle.closestdistance(target_object.lon, benefic.lon))
        if conj_orb <= 10:  # 10 degrees orb
            return True
        
        # Check for opposition (180 degrees)
        opp_orb = abs(angle.closestdistance(target_object.lon, benefic.lon + 180))
        if opp_orb <= 10:  # 10 degrees orb
            return True
        
        # Check for trine (120 degrees)
        trine1_orb = abs(angle.closestdistance(target_object.lon, benefic.lon + 120))
        trine2_orb = abs(angle.closestdistance(target_object.lon, benefic.lon - 120))
        if trine1_orb <= 10 or trine2_orb <= 10:  # 10 degrees orb
            return True
    
    return False


def is_lagna_strong(chart):
    """
    Check if the Lagna (Ascendant) is strong
    
    Args:
        chart (Chart): The chart
    
    Returns:
        bool: True if the Lagna is strong, False otherwise
    """
    # Get the Ascendant
    asc = chart.getAngle(const.ASC)
    
    # Get the lord of the Ascendant
    asc_lord_id = get_sign_lord(asc.sign)
    
    # Check if the Ascendant lord is in a Kendra or Trikona house
    asc_lord_house = get_house_number(chart, asc_lord_id)
    if asc_lord_house in [1, 4, 7, 10, 5, 9]:  # Kendra or Trikona houses
        return True
    
    # Check if benefics are in the Ascendant
    for benefic_id in [const.MOON, const.MERCURY, const.JUPITER, const.VENUS]:
        benefic_house = get_house_number(chart, benefic_id)
        if benefic_house == 1:
            return True
    
    # Check if the Ascendant is aspected by benefics
    if is_aspected_by_benefics(chart, const.ASC):
        return True
    
    return False


def has_planets_in_8th_house(chart):
    """
    Check if there are planets in the 8th house
    
    Args:
        chart (Chart): The chart
    
    Returns:
        bool: True if there are planets in the 8th house, False otherwise
    """
    # Check if any planet is in the 8th house
    for planet_id in const.LIST_OBJECTS_VEDIC:
        planet_house = get_house_number(chart, planet_id)
        if planet_house == 8:
            return True
    
    return False


def get_sign_lord(sign):
    """
    Get the lord of a sign
    
    Args:
        sign (str): The sign
    
    Returns:
        str: The ID of the planet ruling the sign
    """
    # Get the lord of the sign
    if sign == const.ARIES:
        return const.MARS
    elif sign == const.TAURUS:
        return const.VENUS
    elif sign == const.GEMINI:
        return const.MERCURY
    elif sign == const.CANCER:
        return const.MOON
    elif sign == const.LEO:
        return const.SUN
    elif sign == const.VIRGO:
        return const.MERCURY
    elif sign == const.LIBRA:
        return const.VENUS
    elif sign == const.SCORPIO:
        return const.MARS
    elif sign == const.SAGITTARIUS:
        return const.JUPITER
    elif sign == const.CAPRICORN:
        return const.SATURN
    elif sign == const.AQUARIUS:
        return const.SATURN
    elif sign == const.PISCES:
        return const.JUPITER
    
    return None
