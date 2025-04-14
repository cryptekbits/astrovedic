"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Tyajyam (inauspicious time periods) calculations for Vedic astrology.
    Tyajyam is an inauspicious time period based on the Moon's position in the last portion of a nakshatra.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.vedic.nakshatras import get_nakshatra, NAKSHATRA_SPAN
from typing import Dict, Optional, Any, List, Tuple

# Tyajyam durations for each nakshatra (in ghatis, 1 ghati = 24 minutes)
# These are the durations of the inauspicious period at the end of each nakshatra
TYAJYAM_DURATIONS = {
    'Ashwini': 4,
    'Bharani': 5,
    'Krittika': 6,
    'Rohini': 7,
    'Mrigashira': 8,
    'Ardra': 9,
    'Punarvasu': 10,
    'Pushya': 11,
    'Ashlesha': 12,
    'Magha': 13,
    'Purva Phalguni': 14,
    'Uttara Phalguni': 15,
    'Hasta': 16,
    'Chitra': 17,
    'Swati': 18,
    'Vishakha': 19,
    'Anuradha': 20,
    'Jyeshtha': 21,
    'Mula': 22,
    'Purva Ashadha': 23,
    'Uttara Ashadha': 24,
    'Shravana': 1,
    'Dhanishta': 2,
    'Shatabhisha': 3,
    'Purva Bhadrapada': 4,
    'Uttara Bhadrapada': 5,
    'Revati': 6
}

# Convert ghatis to degrees (1 ghati = 1/60 of a nakshatra = 13.33333/60 degrees)
GHATI_TO_DEGREES = NAKSHATRA_SPAN / 60.0

def is_in_tyajyam(moon_longitude: float) -> bool:
    """
    Check if the Moon is in a Tyajyam period based on its longitude.

    Args:
        moon_longitude (float): The Moon's longitude in degrees (0-360)

    Returns:
        bool: True if the Moon is in a Tyajyam period, False otherwise.
    """
    # Get nakshatra information
    nakshatra_info = get_nakshatra(moon_longitude)
    nakshatra_name = nakshatra_info['name']
    
    # Calculate position within nakshatra (0-13.33333 degrees)
    pos_in_nakshatra = moon_longitude % NAKSHATRA_SPAN
    
    # Get the Tyajyam duration for this nakshatra in ghatis
    tyajyam_ghatis = TYAJYAM_DURATIONS.get(nakshatra_name, 0)
    
    # Convert ghatis to degrees
    tyajyam_degrees = tyajyam_ghatis * GHATI_TO_DEGREES
    
    # Check if the Moon is in the Tyajyam portion of the nakshatra
    return (NAKSHATRA_SPAN - pos_in_nakshatra) <= tyajyam_degrees

def get_tyajyam_details(moon_longitude: float) -> Dict[str, Any]:
    """
    Get detailed information about Tyajyam based on the Moon's longitude.

    Args:
        moon_longitude (float): The Moon's longitude in degrees (0-360)

    Returns:
        dict: Dictionary with Tyajyam information.
    """
    # Get nakshatra information
    nakshatra_info = get_nakshatra(moon_longitude)
    nakshatra_name = nakshatra_info['name']
    nakshatra_index = nakshatra_info['index']
    
    # Calculate position within nakshatra (0-13.33333 degrees)
    pos_in_nakshatra = moon_longitude % NAKSHATRA_SPAN
    
    # Get the Tyajyam duration for this nakshatra in ghatis
    tyajyam_ghatis = TYAJYAM_DURATIONS.get(nakshatra_name, 0)
    
    # Convert ghatis to degrees
    tyajyam_degrees = tyajyam_ghatis * GHATI_TO_DEGREES
    
    # Calculate the start and end longitudes of the Tyajyam period
    nakshatra_start = nakshatra_index * NAKSHATRA_SPAN
    tyajyam_start = nakshatra_start + (NAKSHATRA_SPAN - tyajyam_degrees)
    tyajyam_end = nakshatra_start + NAKSHATRA_SPAN
    
    # Check if the Moon is in the Tyajyam portion of the nakshatra
    is_in_tyajyam_period = (NAKSHATRA_SPAN - pos_in_nakshatra) <= tyajyam_degrees
    
    return {
        'is_in_tyajyam': is_in_tyajyam_period,
        'nakshatra': nakshatra_name,
        'tyajyam_ghatis': tyajyam_ghatis,
        'tyajyam_degrees': tyajyam_degrees,
        'tyajyam_start_longitude': tyajyam_start,
        'tyajyam_end_longitude': tyajyam_end
    }

def get_tyajyam_duration(nakshatra_name: str) -> int:
    """
    Get the Tyajyam duration for a specific nakshatra in ghatis.

    Args:
        nakshatra_name (str): The name of the nakshatra.

    Returns:
        int: The Tyajyam duration in ghatis.
    """
    return TYAJYAM_DURATIONS.get(nakshatra_name, 0)

def has_tyajyam_dosha(chart: Chart) -> bool:
    """
    Check if a chart has Tyajyam Dosha based on the Moon's position.

    Args:
        chart (Chart): The chart object containing birth details.

    Returns:
        bool: True if Tyajyam Dosha is present, False otherwise.

    Raises:
        ValueError: If the Moon object is not found in the chart.
    """
    # Get the Moon's position
    moon = chart.getObject(const.MOON)
    if moon is None:
        raise ValueError("Moon object not found in the chart.")
    
    # Check if the Moon is in a Tyajyam period
    return is_in_tyajyam(moon.lon)

def get_all_tyajyam_periods() -> Dict[str, Dict[str, Any]]:
    """
    Get information about all Tyajyam periods for all nakshatras.

    Returns:
        dict: Dictionary with Tyajyam information for all nakshatras.
    """
    tyajyam_periods = {}
    
    for nakshatra_index in range(27):
        nakshatra_name = list(TYAJYAM_DURATIONS.keys())[nakshatra_index]
        tyajyam_ghatis = TYAJYAM_DURATIONS.get(nakshatra_name, 0)
        tyajyam_degrees = tyajyam_ghatis * GHATI_TO_DEGREES
        
        nakshatra_start = nakshatra_index * NAKSHATRA_SPAN
        tyajyam_start = nakshatra_start + (NAKSHATRA_SPAN - tyajyam_degrees)
        tyajyam_end = nakshatra_start + NAKSHATRA_SPAN
        
        tyajyam_periods[nakshatra_name] = {
            'tyajyam_ghatis': tyajyam_ghatis,
            'tyajyam_degrees': tyajyam_degrees,
            'tyajyam_start_longitude': tyajyam_start,
            'tyajyam_end_longitude': tyajyam_end
        }
    
    return tyajyam_periods
