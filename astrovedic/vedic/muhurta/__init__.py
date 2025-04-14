"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Muhurta (electional astrology) calculations
    for Vedic astrology. It includes functions to find auspicious times
    for various activities based on Panchanga and planetary positions.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos

from astrovedic.vedic.muhurta.core import (
    get_muhurta_quality, get_best_muhurta,
    get_auspicious_times, get_inauspicious_times
)

from astrovedic.vedic.muhurta.panchanga import (
    get_panchanga, get_tithi, get_nakshatra,
    get_yoga, get_karana, get_vara,
    is_auspicious_tithi, is_auspicious_nakshatra,
    is_auspicious_yoga, is_auspicious_karana,
    is_auspicious_vara
)

from astrovedic.vedic.muhurta.timing import (
    get_abhijit_muhurta, get_brahma_muhurta,
    get_rahu_kala, get_yama_ghantaka, get_gulika_kala,
    get_hora, get_kaala, get_amrita_yoga,
    get_siddha_yoga, get_amrita_siddha_yoga
)

from astrovedic.vedic.muhurta.events import (
    get_marriage_muhurta, get_travel_muhurta,
    get_business_muhurta, get_education_muhurta,
    get_medical_muhurta, get_house_muhurta,
    get_general_muhurta
)

from astrovedic.vedic.muhurta.activities import (
    get_activity_rules, get_activity_score,
    get_best_time_for_activity
)

from astrovedic.vedic.muhurta.basic_analysis import (
    get_basic_muhurta_analysis
)

# Note: For detailed analysis, use the astroved_extension package

# Constants for Muhurta
EXCELLENT = 'Excellent'
GOOD = 'Good'
NEUTRAL = 'Neutral'
INAUSPICIOUS = 'Inauspicious'
HIGHLY_INAUSPICIOUS = 'Highly Inauspicious'

# List of Muhurta quality levels
LIST_MUHURTA_QUALITY = [
    EXCELLENT, GOOD, NEUTRAL, INAUSPICIOUS, HIGHLY_INAUSPICIOUS
]

# Constants for Panchanga components
TITHI = 'Tithi'
NAKSHATRA = 'Nakshatra'
YOGA = 'Yoga'
KARANA = 'Karana'
VARA = 'Vara'

# List of Panchanga components
LIST_PANCHANGA_COMPONENTS = [
    TITHI, NAKSHATRA, YOGA, KARANA, VARA
]


def find_auspicious_time(start_date, end_date, location, activity=None, min_duration=60):
    """
    Find auspicious times for a specific activity within a date range

    Args:
        start_date (Datetime): The start date and time
        end_date (Datetime): The end date and time
        location (GeoPos): The geographical location
        activity (str, optional): The type of activity
        min_duration (int, optional): Minimum duration in minutes

    Returns:
        list: List of auspicious time periods
    """
    # Get the auspicious times
    auspicious_times = get_auspicious_times(start_date, end_date, location, min_duration)

    # If no specific activity is provided, return all auspicious times
    if activity is None:
        return auspicious_times

    # Filter the auspicious times based on the activity
    activity_times = []

    for time_period in auspicious_times:
        # Get the activity score for this time period
        score = get_activity_score(time_period['start'], location, activity)

        # Add the time period if it's suitable for the activity
        if score['quality'] in [EXCELLENT, GOOD]:
            time_period['activity_score'] = score
            activity_times.append(time_period)

    return activity_times


def get_muhurta_for_date(date, location):
    """
    Get Muhurta information for a specific date
    Note: For detailed analysis, use the astroved_extension package

    Args:
        date (Datetime): The date and time
        location (GeoPos): The geographical location

    Returns:
        dict: Dictionary with basic Muhurta information
    """
    # Get basic Muhurta analysis
    return get_basic_muhurta_analysis(date, location)


def get_best_muhurta_for_activity(start_date, end_date, location, activity):
    """
    Get the best Muhurta for a specific activity within a date range
    Note: For detailed analysis, use the astroved_extension package

    Args:
        start_date (Datetime): The start date and time
        end_date (Datetime): The end date and time
        location (GeoPos): The geographical location
        activity (str): The type of activity

    Returns:
        dict: Dictionary with the best Muhurta information
    """
    # Get the best Muhurta
    return get_best_time_for_activity(start_date, end_date, location, activity)
