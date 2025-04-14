"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Latta Dosha calculations for Vedic astrology.
    Latta Dosha is an inauspicious time period based on the position of the Moon.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.vedic.nakshatras import get_nakshatra
from typing import Dict, Optional, Any, List, Tuple

# Latta Dosha Nakshatras for each weekday
# These are the nakshatras that cause Latta Dosha on specific weekdays
LATTA_DOSHA_NAKSHATRAS = {
    const.SUNDAY: [
        'Bharani', 'Krittika', 'Punarvasu', 'Pushya', 'Uttara Phalguni',
        'Hasta', 'Vishakha', 'Anuradha', 'Uttara Ashadha', 'Dhanishta',
        'Purva Bhadrapada', 'Revati'
    ],
    const.MONDAY: [
        'Ashwini', 'Rohini', 'Mrigashira', 'Ashlesha', 'Magha',
        'Chitra', 'Swati', 'Jyeshtha', 'Mula', 'Shravana',
        'Shatabhisha', 'Uttara Bhadrapada'
    ],
    const.TUESDAY: [
        'Bharani', 'Krittika', 'Ardra', 'Punarvasu', 'Purva Phalguni',
        'Uttara Phalguni', 'Hasta', 'Vishakha', 'Purva Ashadha',
        'Uttara Ashadha', 'Purva Bhadrapada', 'Revati'
    ],
    const.WEDNESDAY: [
        'Ashwini', 'Rohini', 'Mrigashira', 'Pushya', 'Ashlesha',
        'Magha', 'Chitra', 'Swati', 'Anuradha', 'Jyeshtha',
        'Shravana', 'Dhanishta'
    ],
    const.THURSDAY: [
        'Bharani', 'Krittika', 'Ardra', 'Punarvasu', 'Pushya',
        'Purva Phalguni', 'Hasta', 'Vishakha', 'Mula',
        'Purva Ashadha', 'Shatabhisha', 'Purva Bhadrapada'
    ],
    const.FRIDAY: [
        'Ashwini', 'Rohini', 'Mrigashira', 'Ardra', 'Ashlesha',
        'Magha', 'Uttara Phalguni', 'Chitra', 'Swati',
        'Anuradha', 'Uttara Ashadha', 'Uttara Bhadrapada'
    ],
    const.SATURDAY: [
        'Bharani', 'Krittika', 'Punarvasu', 'Pushya', 'Purva Phalguni',
        'Hasta', 'Vishakha', 'Jyeshtha', 'Mula', 'Dhanishta',
        'Shatabhisha', 'Revati'
    ]
}

def has_latta_dosha(chart: Chart) -> bool:
    """
    Check if a chart has Latta Dosha based on the Moon's nakshatra and the weekday.

    Args:
        chart (Chart): The chart object containing birth details.

    Returns:
        bool: True if Latta Dosha is present, False otherwise.

    Raises:
        ValueError: If the Moon object is not found in the chart.
    """
    # Get the Moon's position
    moon = chart.getObject(const.MOON)
    if moon is None:
        raise ValueError("Moon object not found in the chart.")
    
    # Get the nakshatra of the Moon
    nakshatra_info = get_nakshatra(moon.lon)
    nakshatra_name = nakshatra_info['name']
    
    # Get the weekday
    weekday = chart.date.weekday()
    
    # Check if the Moon's nakshatra is in the list of Latta Dosha nakshatras for this weekday
    return nakshatra_name in LATTA_DOSHA_NAKSHATRAS.get(weekday, [])

def get_latta_dosha_details(chart: Chart) -> Dict[str, Any]:
    """
    Get detailed information about Latta Dosha in a chart.

    Args:
        chart (Chart): The chart object containing birth details.

    Returns:
        dict: Dictionary with Latta Dosha information.

    Raises:
        ValueError: If the Moon object is not found in the chart.
    """
    # Get the Moon's position
    moon = chart.getObject(const.MOON)
    if moon is None:
        raise ValueError("Moon object not found in the chart.")
    
    # Get the nakshatra of the Moon
    nakshatra_info = get_nakshatra(moon.lon)
    nakshatra_name = nakshatra_info['name']
    
    # Get the weekday
    weekday = chart.date.weekday()
    
    # Check if the Moon's nakshatra is in the list of Latta Dosha nakshatras for this weekday
    is_latta_dosha = nakshatra_name in LATTA_DOSHA_NAKSHATRAS.get(weekday, [])
    
    return {
        'has_latta_dosha': is_latta_dosha,
        'weekday': weekday,
        'moon_nakshatra': nakshatra_name,
        'latta_dosha_nakshatras': LATTA_DOSHA_NAKSHATRAS.get(weekday, [])
    }

def get_latta_dosha_nakshatras_for_weekday(weekday: str) -> List[str]:
    """
    Get the list of nakshatras that cause Latta Dosha for a specific weekday.

    Args:
        weekday (str): The weekday (SUNDAY, MONDAY, etc.)

    Returns:
        list: List of nakshatra names that cause Latta Dosha on the specified weekday.
    """
    return LATTA_DOSHA_NAKSHATRAS.get(weekday, [])

def is_latta_dosha_time(date: Datetime, moon_longitude: float) -> bool:
    """
    Check if a specific time has Latta Dosha based on the Moon's nakshatra and the weekday.

    Args:
        date (Datetime): The date and time to check.
        moon_longitude (float): The Moon's longitude at the specified time.

    Returns:
        bool: True if Latta Dosha is present, False otherwise.
    """
    # Get the nakshatra of the Moon
    nakshatra_info = get_nakshatra(moon_longitude)
    nakshatra_name = nakshatra_info['name']
    
    # Get the weekday
    weekday = date.weekday()
    
    # Check if the Moon's nakshatra is in the list of Latta Dosha nakshatras for this weekday
    return nakshatra_name in LATTA_DOSHA_NAKSHATRAS.get(weekday, [])
