"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Panchanga analysis for Muhurta (electional astrology)
    in Vedic astrology.
"""

from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import angle
from datetime import timedelta

# Import Nakshatra functions
from flatlib.vedic.nakshatras import get_nakshatra


def get_panchanga(chart):
    """
    Calculate the Panchanga (five limbs of the day) for a chart
    
    Args:
        chart (Chart): The chart
    
    Returns:
        dict: Dictionary with Panchanga information
    """
    # Get the Tithi
    tithi = get_tithi(chart)
    
    # Get the Nakshatra
    nakshatra = get_nakshatra_for_muhurta(chart)
    
    # Get the Yoga
    yoga = get_yoga(chart)
    
    # Get the Karana
    karana = get_karana(chart)
    
    # Get the Vara (Weekday)
    vara = get_vara(chart)
    
    return {
        'tithi': tithi,
        'nakshatra': nakshatra,
        'yoga': yoga,
        'karana': karana,
        'vara': vara
    }


def get_tithi(chart):
    """
    Calculate the Tithi (lunar day) for a chart
    
    Args:
        chart (Chart): The chart
    
    Returns:
        dict: Dictionary with Tithi information
    """
    # Get the Sun and Moon
    sun = chart.getObject(const.SUN)
    moon = chart.getObject(const.MOON)
    
    # Calculate the longitudinal distance between the Moon and the Sun
    dist = angle.distance(moon.lon, sun.lon)
    
    # Calculate the Tithi number (1-30)
    tithi_num = int(dist / 12) + 1
    
    # Calculate the elapsed portion of the Tithi
    elapsed = (dist % 12) / 12
    
    # Get the Tithi name
    tithi_name = get_tithi_name(tithi_num)
    
    # Get the Tithi type
    tithi_type = get_tithi_type(tithi_num)
    
    # Get the Paksha (fortnight)
    paksha = 'Shukla' if tithi_num <= 15 else 'Krishna'
    
    # Adjust the Tithi number for Krishna Paksha
    if paksha == 'Krishna':
        tithi_num = tithi_num - 15
        if tithi_num == 15:
            tithi_num = 30  # Amavasya
    
    return {
        'num': tithi_num,
        'name': tithi_name,
        'type': tithi_type,
        'paksha': paksha,
        'elapsed': elapsed
    }


def get_nakshatra_for_muhurta(chart):
    """
    Calculate the Nakshatra (lunar mansion) for a chart
    
    Args:
        chart (Chart): The chart
    
    Returns:
        dict: Dictionary with Nakshatra information
    """
    # Get the Moon
    moon = chart.getObject(const.MOON)
    
    # Get the Nakshatra
    nakshatra_info = get_nakshatra(moon.lon)
    
    # Get the Nakshatra lord
    nakshatra_lord = get_nakshatra_lord(nakshatra_info['num'])
    
    # Get the Nakshatra type
    nakshatra_type = get_nakshatra_type(nakshatra_info['num'])
    
    return {
        'num': nakshatra_info['num'],
        'name': nakshatra_info['name'],
        'pada': nakshatra_info['pada'],
        'lord': nakshatra_lord,
        'type': nakshatra_type,
        'start_lon': nakshatra_info['start_lon'],
        'end_lon': nakshatra_info['end_lon'],
        'elapsed': nakshatra_info['elapsed']
    }


def get_yoga(chart):
    """
    Calculate the Yoga (combination of Sun and Moon) for a chart
    
    Args:
        chart (Chart): The chart
    
    Returns:
        dict: Dictionary with Yoga information
    """
    # Get the Sun and Moon
    sun = chart.getObject(const.SUN)
    moon = chart.getObject(const.MOON)
    
    # Calculate the sum of the longitudes of the Sun and Moon
    total_lon = (sun.lon + moon.lon) % 360
    
    # Calculate the Yoga number (1-27)
    yoga_num = int(total_lon / (360 / 27)) + 1
    
    # Calculate the elapsed portion of the Yoga
    elapsed = (total_lon % (360 / 27)) / (360 / 27)
    
    # Get the Yoga name
    yoga_name = get_yoga_name(yoga_num)
    
    # Get the Yoga type
    yoga_type = get_yoga_type(yoga_num)
    
    return {
        'num': yoga_num,
        'name': yoga_name,
        'type': yoga_type,
        'elapsed': elapsed
    }


def get_karana(chart):
    """
    Calculate the Karana (half of a Tithi) for a chart
    
    Args:
        chart (Chart): The chart
    
    Returns:
        dict: Dictionary with Karana information
    """
    # Get the Tithi
    tithi = get_tithi(chart)
    
    # Calculate the Karana number (1-11)
    karana_num = ((tithi['num'] - 1) * 2 + (1 if tithi['elapsed'] >= 0.5 else 0)) % 11
    if karana_num == 0:
        karana_num = 11
    
    # Calculate the elapsed portion of the Karana
    elapsed = (tithi['elapsed'] * 2) % 1
    
    # Get the Karana name
    karana_name = get_karana_name(karana_num)
    
    # Get the Karana type
    karana_type = get_karana_type(karana_num)
    
    return {
        'num': karana_num,
        'name': karana_name,
        'type': karana_type,
        'elapsed': elapsed
    }


def get_vara(chart):
    """
    Calculate the Vara (weekday) for a chart
    
    Args:
        chart (Chart): The chart
    
    Returns:
        dict: Dictionary with Vara information
    """
    # Get the date
    date = chart.date
    
    # Get the weekday (0-6, where 0 is Monday)
    weekday = date.datetime().weekday()
    
    # Convert to Vedic weekday (1-7, where 1 is Sunday)
    vara_num = weekday + 2
    if vara_num > 7:
        vara_num = vara_num - 7
    
    # Get the Vara name
    vara_name = get_vara_name(vara_num)
    
    # Get the Vara lord
    vara_lord = get_vara_lord(vara_num)
    
    return {
        'num': vara_num,
        'name': vara_name,
        'lord': vara_lord
    }


def get_tithi_name(tithi_num):
    """
    Get the name of a Tithi
    
    Args:
        tithi_num (int): The Tithi number (1-30)
    
    Returns:
        str: The name of the Tithi
    """
    tithi_names = {
        1: 'Pratipada',
        2: 'Dwitiya',
        3: 'Tritiya',
        4: 'Chaturthi',
        5: 'Panchami',
        6: 'Shashthi',
        7: 'Saptami',
        8: 'Ashtami',
        9: 'Navami',
        10: 'Dashami',
        11: 'Ekadashi',
        12: 'Dwadashi',
        13: 'Trayodashi',
        14: 'Chaturdashi',
        15: 'Purnima',
        30: 'Amavasya'
    }
    
    return tithi_names.get(tithi_num, '')


def get_tithi_type(tithi_num):
    """
    Get the type of a Tithi
    
    Args:
        tithi_num (int): The Tithi number (1-30)
    
    Returns:
        str: The type of the Tithi
    """
    # Nanda Tithis: 1, 6, 11
    if tithi_num in [1, 6, 11]:
        return 'Nanda'
    
    # Bhadra Tithis: 2, 7, 12
    elif tithi_num in [2, 7, 12]:
        return 'Bhadra'
    
    # Jaya Tithis: 3, 8, 13
    elif tithi_num in [3, 8, 13]:
        return 'Jaya'
    
    # Rikta Tithis: 4, 9, 14
    elif tithi_num in [4, 9, 14]:
        return 'Rikta'
    
    # Purna Tithis: 5, 10, 15, 30
    elif tithi_num in [5, 10, 15, 30]:
        return 'Purna'
    
    return ''


def get_nakshatra_lord(nakshatra_num):
    """
    Get the lord of a Nakshatra
    
    Args:
        nakshatra_num (int): The Nakshatra number (1-27)
    
    Returns:
        str: The lord of the Nakshatra
    """
    nakshatra_lords = {
        1: 'Ketu',
        2: 'Venus',
        3: 'Sun',
        4: 'Moon',
        5: 'Mars',
        6: 'Rahu',
        7: 'Jupiter',
        8: 'Saturn',
        9: 'Mercury',
        10: 'Ketu',
        11: 'Venus',
        12: 'Sun',
        13: 'Moon',
        14: 'Mars',
        15: 'Rahu',
        16: 'Jupiter',
        17: 'Saturn',
        18: 'Mercury',
        19: 'Ketu',
        20: 'Venus',
        21: 'Sun',
        22: 'Moon',
        23: 'Mars',
        24: 'Rahu',
        25: 'Jupiter',
        26: 'Saturn',
        27: 'Mercury'
    }
    
    return nakshatra_lords.get(nakshatra_num, '')


def get_nakshatra_type(nakshatra_num):
    """
    Get the type of a Nakshatra
    
    Args:
        nakshatra_num (int): The Nakshatra number (1-27)
    
    Returns:
        str: The type of the Nakshatra
    """
    # Movable Nakshatras
    if nakshatra_num in [1, 5, 7, 8, 13, 15, 22, 26, 27]:
        return 'Movable'
    
    # Fixed Nakshatras
    elif nakshatra_num in [2, 6, 9, 10, 14, 18, 19, 23, 25]:
        return 'Fixed'
    
    # Mixed Nakshatras
    elif nakshatra_num in [3, 4, 11, 12, 16, 17, 20, 21, 24]:
        return 'Mixed'
    
    return ''


def get_yoga_name(yoga_num):
    """
    Get the name of a Yoga
    
    Args:
        yoga_num (int): The Yoga number (1-27)
    
    Returns:
        str: The name of the Yoga
    """
    yoga_names = {
        1: 'Vishkambha',
        2: 'Preeti',
        3: 'Ayushman',
        4: 'Saubhagya',
        5: 'Shobhana',
        6: 'Atiganda',
        7: 'Sukarma',
        8: 'Dhriti',
        9: 'Shoola',
        10: 'Ganda',
        11: 'Vriddhi',
        12: 'Dhruva',
        13: 'Vyaghata',
        14: 'Harshana',
        15: 'Vajra',
        16: 'Siddhi',
        17: 'Vyatipata',
        18: 'Variyan',
        19: 'Parigha',
        20: 'Shiva',
        21: 'Siddha',
        22: 'Sadhya',
        23: 'Shubha',
        24: 'Shukla',
        25: 'Brahma',
        26: 'Indra',
        27: 'Vaidhriti'
    }
    
    return yoga_names.get(yoga_num, '')


def get_yoga_type(yoga_num):
    """
    Get the type of a Yoga
    
    Args:
        yoga_num (int): The Yoga number (1-27)
    
    Returns:
        str: The type of the Yoga
    """
    # Auspicious Yogas
    if yoga_num in [2, 3, 4, 5, 7, 8, 11, 12, 14, 16, 20, 21, 22, 23, 24, 25, 26]:
        return 'Auspicious'
    
    # Inauspicious Yogas
    elif yoga_num in [1, 6, 9, 10, 13, 15, 17, 18, 19, 27]:
        return 'Inauspicious'
    
    return ''


def get_karana_name(karana_num):
    """
    Get the name of a Karana
    
    Args:
        karana_num (int): The Karana number (1-11)
    
    Returns:
        str: The name of the Karana
    """
    karana_names = {
        1: 'Bava',
        2: 'Balava',
        3: 'Kaulava',
        4: 'Taitila',
        5: 'Garaja',
        6: 'Vanija',
        7: 'Vishti',
        8: 'Shakuni',
        9: 'Chatushpada',
        10: 'Naga',
        11: 'Kimstughna'
    }
    
    return karana_names.get(karana_num, '')


def get_karana_type(karana_num):
    """
    Get the type of a Karana
    
    Args:
        karana_num (int): The Karana number (1-11)
    
    Returns:
        str: The type of the Karana
    """
    # Fixed Karanas
    if karana_num in [8, 9, 10, 11]:
        return 'Fixed'
    
    # Movable Karanas
    elif karana_num in [1, 2, 3, 4, 5, 6, 7]:
        return 'Movable'
    
    return ''


def get_vara_name(vara_num):
    """
    Get the name of a Vara (weekday)
    
    Args:
        vara_num (int): The Vara number (1-7)
    
    Returns:
        str: The name of the Vara
    """
    vara_names = {
        1: 'Sunday',
        2: 'Monday',
        3: 'Tuesday',
        4: 'Wednesday',
        5: 'Thursday',
        6: 'Friday',
        7: 'Saturday'
    }
    
    return vara_names.get(vara_num, '')


def get_vara_lord(vara_num):
    """
    Get the lord of a Vara (weekday)
    
    Args:
        vara_num (int): The Vara number (1-7)
    
    Returns:
        str: The lord of the Vara
    """
    vara_lords = {
        1: 'Sun',
        2: 'Moon',
        3: 'Mars',
        4: 'Mercury',
        5: 'Jupiter',
        6: 'Venus',
        7: 'Saturn'
    }
    
    return vara_lords.get(vara_num, '')


def is_auspicious_tithi(tithi_num):
    """
    Check if a Tithi is auspicious
    
    Args:
        tithi_num (int): The Tithi number (1-30)
    
    Returns:
        bool: True if the Tithi is auspicious, False otherwise
    """
    # Auspicious Tithis
    auspicious_tithis = [1, 2, 3, 5, 6, 7, 10, 11, 13, 15]
    
    return tithi_num in auspicious_tithis


def is_auspicious_nakshatra(nakshatra_num):
    """
    Check if a Nakshatra is auspicious
    
    Args:
        nakshatra_num (int): The Nakshatra number (1-27)
    
    Returns:
        bool: True if the Nakshatra is auspicious, False otherwise
    """
    # Auspicious Nakshatras
    auspicious_nakshatras = [1, 3, 5, 7, 8, 10, 12, 13, 15, 16, 17, 20, 22, 23, 24, 25, 26, 27]
    
    return nakshatra_num in auspicious_nakshatras


def is_auspicious_yoga(yoga_num):
    """
    Check if a Yoga is auspicious
    
    Args:
        yoga_num (int): The Yoga number (1-27)
    
    Returns:
        bool: True if the Yoga is auspicious, False otherwise
    """
    # Auspicious Yogas
    auspicious_yogas = [2, 3, 4, 5, 7, 8, 11, 12, 14, 16, 20, 21, 22, 23, 24, 25, 26]
    
    return yoga_num in auspicious_yogas


def is_auspicious_karana(karana_num):
    """
    Check if a Karana is auspicious
    
    Args:
        karana_num (int): The Karana number (1-11)
    
    Returns:
        bool: True if the Karana is auspicious, False otherwise
    """
    # Auspicious Karanas
    auspicious_karanas = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11]
    
    return karana_num in auspicious_karanas


def is_auspicious_vara(vara_num):
    """
    Check if a Vara (weekday) is auspicious
    
    Args:
        vara_num (int): The Vara number (1-7)
    
    Returns:
        bool: True if the Vara is auspicious, False otherwise
    """
    # Auspicious Varas
    auspicious_varas = [2, 4, 5]  # Monday, Wednesday, Thursday
    
    return vara_num in auspicious_varas
