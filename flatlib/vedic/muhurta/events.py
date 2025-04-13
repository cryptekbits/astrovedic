"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements specific event timing for Muhurta (electional astrology)
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


def get_marriage_muhurta(start_date, end_date, location):
    """
    Find auspicious times for marriage within a date range
    
    Args:
        start_date (Datetime): The start date and time
        end_date (Datetime): The end date and time
        location (GeoPos): The geographical location
    
    Returns:
        list: List of auspicious time periods for marriage
    """
    # Get all auspicious times
    auspicious_times = get_auspicious_times(start_date, end_date, location, min_duration=120)
    
    # Filter for marriage-specific criteria
    marriage_times = []
    
    for time_period in auspicious_times:
        # Create a chart for the start time
        chart = Chart(time_period['start'], location, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
        
        # Get the Panchanga
        panchanga = get_panchanga(chart)
        
        # Check marriage-specific criteria
        
        # Auspicious Tithis for marriage: 2, 3, 5, 7, 10, 11, 13
        tithi_num = panchanga['tithi']['num']
        is_good_tithi = tithi_num in [2, 3, 5, 7, 10, 11, 13]
        
        # Auspicious Nakshatras for marriage: 1, 3, 5, 7, 8, 13, 14, 17, 20, 23, 24, 25, 27
        nakshatra_num = panchanga['nakshatra']['num']
        is_good_nakshatra = nakshatra_num in [1, 3, 5, 7, 8, 13, 14, 17, 20, 23, 24, 25, 27]
        
        # Auspicious Varas for marriage: 2, 4, 5, 6 (Monday, Wednesday, Thursday, Friday)
        vara_num = panchanga['vara']['num']
        is_good_vara = vara_num in [2, 4, 5, 6]
        
        # Check if Venus is strong
        venus = chart.getObject(const.VENUS)
        is_venus_strong = not is_combust(chart, const.VENUS) and not is_retrograde(venus)
        
        # Check if all criteria are met
        if is_good_tithi and is_good_nakshatra and is_good_vara and is_venus_strong:
            # Add additional information
            time_period['suitability'] = 'Excellent for marriage'
            time_period['panchanga'] = panchanga
            
            marriage_times.append(time_period)
    
    return marriage_times


def get_travel_muhurta(start_date, end_date, location, direction=None):
    """
    Find auspicious times for travel within a date range
    
    Args:
        start_date (Datetime): The start date and time
        end_date (Datetime): The end date and time
        location (GeoPos): The geographical location
        direction (str, optional): The direction of travel
    
    Returns:
        list: List of auspicious time periods for travel
    """
    # Get all auspicious times
    auspicious_times = get_auspicious_times(start_date, end_date, location, min_duration=60)
    
    # Filter for travel-specific criteria
    travel_times = []
    
    for time_period in auspicious_times:
        # Create a chart for the start time
        chart = Chart(time_period['start'], location, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
        
        # Get the Panchanga
        panchanga = get_panchanga(chart)
        
        # Check travel-specific criteria
        
        # Auspicious Tithis for travel: 2, 3, 5, 7, 10, 11, 12
        tithi_num = panchanga['tithi']['num']
        is_good_tithi = tithi_num in [2, 3, 5, 7, 10, 11, 12]
        
        # Auspicious Nakshatras for travel: 1, 3, 5, 7, 8, 13, 14, 17, 20, 23, 24, 25, 27
        nakshatra_num = panchanga['nakshatra']['num']
        is_good_nakshatra = nakshatra_num in [1, 3, 5, 7, 8, 13, 14, 17, 20, 23, 24, 25, 27]
        
        # Auspicious Varas for travel: 2, 4, 5 (Monday, Wednesday, Thursday)
        vara_num = panchanga['vara']['num']
        is_good_vara = vara_num in [2, 4, 5]
        
        # Check if Mercury is strong
        mercury = chart.getObject(const.MERCURY)
        is_mercury_strong = not is_combust(chart, const.MERCURY) and not is_retrograde(mercury)
        
        # Check direction-specific criteria
        is_good_direction = True
        if direction:
            # Get the Moon
            moon = chart.getObject(const.MOON)
            
            # Get the Moon's sign
            moon_sign = moon.sign
            
            # Check if the direction is favorable based on the Moon's sign
            if direction == 'North' and moon_sign in [const.ARIES, const.TAURUS, const.GEMINI]:
                is_good_direction = True
            elif direction == 'East' and moon_sign in [const.CANCER, const.LEO, const.VIRGO]:
                is_good_direction = True
            elif direction == 'South' and moon_sign in [const.LIBRA, const.SCORPIO, const.SAGITTARIUS]:
                is_good_direction = True
            elif direction == 'West' and moon_sign in [const.CAPRICORN, const.AQUARIUS, const.PISCES]:
                is_good_direction = True
            else:
                is_good_direction = False
        
        # Check if all criteria are met
        if is_good_tithi and is_good_nakshatra and is_good_vara and is_mercury_strong and is_good_direction:
            # Add additional information
            time_period['suitability'] = 'Excellent for travel'
            time_period['panchanga'] = panchanga
            
            travel_times.append(time_period)
    
    return travel_times


def get_business_muhurta(start_date, end_date, location):
    """
    Find auspicious times for business activities within a date range
    
    Args:
        start_date (Datetime): The start date and time
        end_date (Datetime): The end date and time
        location (GeoPos): The geographical location
    
    Returns:
        list: List of auspicious time periods for business
    """
    # Get all auspicious times
    auspicious_times = get_auspicious_times(start_date, end_date, location, min_duration=60)
    
    # Filter for business-specific criteria
    business_times = []
    
    for time_period in auspicious_times:
        # Create a chart for the start time
        chart = Chart(time_period['start'], location, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
        
        # Get the Panchanga
        panchanga = get_panchanga(chart)
        
        # Check business-specific criteria
        
        # Auspicious Tithis for business: 2, 3, 5, 7, 10, 11
        tithi_num = panchanga['tithi']['num']
        is_good_tithi = tithi_num in [2, 3, 5, 7, 10, 11]
        
        # Auspicious Nakshatras for business: 1, 3, 5, 7, 10, 13, 14, 16, 17, 20, 23, 24, 25
        nakshatra_num = panchanga['nakshatra']['num']
        is_good_nakshatra = nakshatra_num in [1, 3, 5, 7, 10, 13, 14, 16, 17, 20, 23, 24, 25]
        
        # Auspicious Varas for business: 2, 4, 5, 6 (Monday, Wednesday, Thursday, Friday)
        vara_num = panchanga['vara']['num']
        is_good_vara = vara_num in [2, 4, 5, 6]
        
        # Check if Mercury and Jupiter are strong
        mercury = chart.getObject(const.MERCURY)
        jupiter = chart.getObject(const.JUPITER)
        is_mercury_strong = not is_combust(chart, const.MERCURY) and not is_retrograde(mercury)
        is_jupiter_strong = not is_combust(chart, const.JUPITER) and not is_retrograde(jupiter)
        
        # Check if all criteria are met
        if is_good_tithi and is_good_nakshatra and is_good_vara and (is_mercury_strong or is_jupiter_strong):
            # Add additional information
            time_period['suitability'] = 'Excellent for business'
            time_period['panchanga'] = panchanga
            
            business_times.append(time_period)
    
    return business_times


def get_education_muhurta(start_date, end_date, location):
    """
    Find auspicious times for education-related activities within a date range
    
    Args:
        start_date (Datetime): The start date and time
        end_date (Datetime): The end date and time
        location (GeoPos): The geographical location
    
    Returns:
        list: List of auspicious time periods for education
    """
    # Get all auspicious times
    auspicious_times = get_auspicious_times(start_date, end_date, location, min_duration=60)
    
    # Filter for education-specific criteria
    education_times = []
    
    for time_period in auspicious_times:
        # Create a chart for the start time
        chart = Chart(time_period['start'], location, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
        
        # Get the Panchanga
        panchanga = get_panchanga(chart)
        
        # Check education-specific criteria
        
        # Auspicious Tithis for education: 2, 3, 5, 7, 10, 11, 13
        tithi_num = panchanga['tithi']['num']
        is_good_tithi = tithi_num in [2, 3, 5, 7, 10, 11, 13]
        
        # Auspicious Nakshatras for education: 3, 5, 7, 13, 14, 16, 17, 20, 22, 23, 24, 25, 27
        nakshatra_num = panchanga['nakshatra']['num']
        is_good_nakshatra = nakshatra_num in [3, 5, 7, 13, 14, 16, 17, 20, 22, 23, 24, 25, 27]
        
        # Auspicious Varas for education: 2, 4, 5 (Monday, Wednesday, Thursday)
        vara_num = panchanga['vara']['num']
        is_good_vara = vara_num in [2, 4, 5]
        
        # Check if Mercury and Jupiter are strong
        mercury = chart.getObject(const.MERCURY)
        jupiter = chart.getObject(const.JUPITER)
        is_mercury_strong = not is_combust(chart, const.MERCURY) and not is_retrograde(mercury)
        is_jupiter_strong = not is_combust(chart, const.JUPITER) and not is_retrograde(jupiter)
        
        # Check if all criteria are met
        if is_good_tithi and is_good_nakshatra and is_good_vara and (is_mercury_strong or is_jupiter_strong):
            # Add additional information
            time_period['suitability'] = 'Excellent for education'
            time_period['panchanga'] = panchanga
            
            education_times.append(time_period)
    
    return education_times


def get_medical_muhurta(start_date, end_date, location):
    """
    Find auspicious times for medical procedures within a date range
    
    Args:
        start_date (Datetime): The start date and time
        end_date (Datetime): The end date and time
        location (GeoPos): The geographical location
    
    Returns:
        list: List of auspicious time periods for medical procedures
    """
    # Get all auspicious times
    auspicious_times = get_auspicious_times(start_date, end_date, location, min_duration=60)
    
    # Filter for medical-specific criteria
    medical_times = []
    
    for time_period in auspicious_times:
        # Create a chart for the start time
        chart = Chart(time_period['start'], location, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
        
        # Get the Panchanga
        panchanga = get_panchanga(chart)
        
        # Check medical-specific criteria
        
        # Auspicious Tithis for medical procedures: 2, 3, 5, 7, 10, 11, 12
        tithi_num = panchanga['tithi']['num']
        is_good_tithi = tithi_num in [2, 3, 5, 7, 10, 11, 12]
        
        # Auspicious Nakshatras for medical procedures: 1, 3, 5, 7, 10, 12, 13, 16, 17, 20, 23, 24, 25
        nakshatra_num = panchanga['nakshatra']['num']
        is_good_nakshatra = nakshatra_num in [1, 3, 5, 7, 10, 12, 13, 16, 17, 20, 23, 24, 25]
        
        # Auspicious Varas for medical procedures: 2, 4, 5 (Monday, Wednesday, Thursday)
        vara_num = panchanga['vara']['num']
        is_good_vara = vara_num in [2, 4, 5]
        
        # Check if Moon is strong
        moon = chart.getObject(const.MOON)
        is_moon_strong = not is_combust(chart, const.MOON) and not is_in_gandanta(moon)
        
        # Check if all criteria are met
        if is_good_tithi and is_good_nakshatra and is_good_vara and is_moon_strong:
            # Add additional information
            time_period['suitability'] = 'Excellent for medical procedures'
            time_period['panchanga'] = panchanga
            
            medical_times.append(time_period)
    
    return medical_times


def get_house_muhurta(start_date, end_date, location, activity_type='construction'):
    """
    Find auspicious times for house-related activities within a date range
    
    Args:
        start_date (Datetime): The start date and time
        end_date (Datetime): The end date and time
        location (GeoPos): The geographical location
        activity_type (str, optional): The type of house-related activity
    
    Returns:
        list: List of auspicious time periods for house-related activities
    """
    # Get all auspicious times
    auspicious_times = get_auspicious_times(start_date, end_date, location, min_duration=120)
    
    # Filter for house-specific criteria
    house_times = []
    
    for time_period in auspicious_times:
        # Create a chart for the start time
        chart = Chart(time_period['start'], location, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
        
        # Get the Panchanga
        panchanga = get_panchanga(chart)
        
        # Check house-specific criteria
        
        # Auspicious Tithis for house activities: 2, 3, 5, 7, 10, 11, 13
        tithi_num = panchanga['tithi']['num']
        is_good_tithi = tithi_num in [2, 3, 5, 7, 10, 11, 13]
        
        # Auspicious Nakshatras for house activities: 1, 3, 5, 7, 10, 13, 14, 16, 17, 20, 23, 24, 25, 27
        nakshatra_num = panchanga['nakshatra']['num']
        is_good_nakshatra = nakshatra_num in [1, 3, 5, 7, 10, 13, 14, 16, 17, 20, 23, 24, 25, 27]
        
        # Auspicious Varas for house activities: 2, 4, 5 (Monday, Wednesday, Thursday)
        vara_num = panchanga['vara']['num']
        is_good_vara = vara_num in [2, 4, 5]
        
        # Check if Jupiter and Venus are strong
        jupiter = chart.getObject(const.JUPITER)
        venus = chart.getObject(const.VENUS)
        is_jupiter_strong = not is_combust(chart, const.JUPITER) and not is_retrograde(jupiter)
        is_venus_strong = not is_combust(chart, const.VENUS) and not is_retrograde(venus)
        
        # Check activity-specific criteria
        is_activity_good = True
        if activity_type == 'construction':
            # For construction, check if Mars is strong
            mars = chart.getObject(const.MARS)
            is_activity_good = not is_combust(chart, const.MARS) and not is_retrograde(mars)
        elif activity_type == 'moving':
            # For moving, check if Mercury is strong
            mercury = chart.getObject(const.MERCURY)
            is_activity_good = not is_combust(chart, const.MERCURY) and not is_retrograde(mercury)
        
        # Check if all criteria are met
        if is_good_tithi and is_good_nakshatra and is_good_vara and (is_jupiter_strong or is_venus_strong) and is_activity_good:
            # Add additional information
            time_period['suitability'] = f'Excellent for house {activity_type}'
            time_period['panchanga'] = panchanga
            
            house_times.append(time_period)
    
    return house_times


def get_general_muhurta(start_date, end_date, location):
    """
    Find generally auspicious times within a date range
    
    Args:
        start_date (Datetime): The start date and time
        end_date (Datetime): The end date and time
        location (GeoPos): The geographical location
    
    Returns:
        list: List of generally auspicious time periods
    """
    # Get all auspicious times
    auspicious_times = get_auspicious_times(start_date, end_date, location, min_duration=60)
    
    # Filter for generally auspicious criteria
    general_times = []
    
    for time_period in auspicious_times:
        # Create a chart for the start time
        chart = Chart(time_period['start'], location, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
        
        # Get the Panchanga
        panchanga = get_panchanga(chart)
        
        # Check general criteria
        
        # Auspicious Tithis: 2, 3, 5, 7, 10, 11, 13
        tithi_num = panchanga['tithi']['num']
        is_good_tithi = tithi_num in [2, 3, 5, 7, 10, 11, 13]
        
        # Auspicious Nakshatras: 1, 3, 5, 7, 10, 13, 14, 16, 17, 20, 23, 24, 25, 27
        nakshatra_num = panchanga['nakshatra']['num']
        is_good_nakshatra = nakshatra_num in [1, 3, 5, 7, 10, 13, 14, 16, 17, 20, 23, 24, 25, 27]
        
        # Auspicious Varas: 2, 4, 5, 6 (Monday, Wednesday, Thursday, Friday)
        vara_num = panchanga['vara']['num']
        is_good_vara = vara_num in [2, 4, 5, 6]
        
        # Check if Moon is strong
        moon = chart.getObject(const.MOON)
        is_moon_strong = not is_combust(chart, const.MOON) and not is_in_gandanta(moon)
        
        # Check if all criteria are met
        if is_good_tithi and is_good_nakshatra and is_good_vara and is_moon_strong:
            # Add additional information
            time_period['suitability'] = 'Generally auspicious'
            time_period['panchanga'] = panchanga
            
            general_times.append(time_period)
    
    return general_times


def is_combust(chart, planet_id):
    """
    Check if a planet is combust (too close to the Sun)
    
    Args:
        chart (Chart): The chart
        planet_id (str): The ID of the planet to check
    
    Returns:
        bool: True if the planet is combust, False otherwise
    """
    # Get the planet and the Sun
    planet = chart.getObject(planet_id)
    sun = chart.getObject(const.SUN)
    
    # Skip if the planet is the Sun
    if planet_id == const.SUN:
        return False
    
    # Calculate the orb
    from flatlib import angle
    orb = abs(angle.closestdistance(planet.lon, sun.lon))
    
    # Define combustion orbs for each planet based on standard Vedic rules
    combustion_orbs = {
        const.MOON: 12,
        const.MERCURY: 14,
        const.VENUS: 10,
        const.MARS: 17,
        const.JUPITER: 11,
        const.SATURN: 15
    }
    
    # Adjust combustion orb for retrograde planets
    if is_retrograde(planet):
        # Retrograde planets have a slightly wider orb for combustion
        combustion_orbs[const.MERCURY] = 12  # Reduced from 14 as it's closer when retrograde
        combustion_orbs[const.VENUS] = 8     # Reduced from 10 as it's closer when retrograde
    
    # Check if the planet is combust
    return orb <= combustion_orbs.get(planet_id, 10)


def is_retrograde(planet):
    """
    Check if a planet is retrograde
    
    Args:
        planet (Object): The planet to check
    
    Returns:
        bool: True if the planet is retrograde, False otherwise
    """
    return planet.isRetrograde()


def is_in_gandanta(moon):
    """
    Check if the Moon is in Gandanta (junction of water and fire signs)
    
    Args:
        moon (Object): The Moon
    
    Returns:
        bool: True if the Moon is in Gandanta, False otherwise
    """
    # Get the Moon's longitude
    moon_lon = moon.lon
    
    # Define Gandanta ranges (last 3 degrees of water signs and first 3 degrees of fire signs)
    gandanta_ranges = [
        (87, 93),    # Cancer-Leo
        (207, 213),  # Scorpio-Sagittarius
        (327, 333)   # Pisces-Aries
    ]
    
    # Check if the Moon is in any Gandanta range
    for start, end in gandanta_ranges:
        if start <= moon_lon <= end:
            return True
    
    return False
