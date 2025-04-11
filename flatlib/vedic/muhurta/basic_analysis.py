"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements basic analysis tools for Muhurta
    (electional astrology) in Vedic astrology. For detailed analysis and reporting,
    use the astroved_extension package.
"""

from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

# Import core functions
from flatlib.vedic.muhurta.core import get_muhurta_quality
from flatlib.vedic.muhurta.panchanga import get_panchanga
from flatlib.vedic.muhurta.activities import get_activity_score
from flatlib.vedic.muhurta.timing import (
    get_abhijit_muhurta, get_brahma_muhurta,
    get_rahu_kala, get_yama_ghantaka, get_gulika_kala
)


def get_basic_muhurta_analysis(date, location):
    """
    Get basic analysis of Muhurta for a specific date and time.
    For detailed analysis, use the astroved_extension package.
    
    Args:
        date (Datetime): The date and time
        location (GeoPos): The geographical location
    
    Returns:
        dict: Dictionary with basic Muhurta analysis
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
    
    # Get special Muhurtas
    abhijit = get_abhijit_muhurta(date, location)
    brahma = get_brahma_muhurta(date, location)
    
    # Get inauspicious periods
    rahu_kala = get_rahu_kala(date, location)
    yama_ghantaka = get_yama_ghantaka(date, location)
    gulika_kala = get_gulika_kala(date, location)
    
    # Check if the time is in any special Muhurta
    in_abhijit = False
    in_brahma = False
    
    if abhijit:
        abhijit_start = abhijit['start']
        abhijit_end = abhijit['end']
        if date >= abhijit_start and date <= abhijit_end:
            in_abhijit = True
    
    if brahma:
        brahma_start = brahma['start']
        brahma_end = brahma['end']
        if date >= brahma_start and date <= brahma_end:
            in_brahma = True
    
    # Check if the time is in any inauspicious period
    in_rahu_kala = False
    in_yama_ghantaka = False
    in_gulika_kala = False
    
    if rahu_kala:
        rahu_start = rahu_kala['start']
        rahu_end = rahu_kala['end']
        if date >= rahu_start and date <= rahu_end:
            in_rahu_kala = True
    
    if yama_ghantaka:
        yama_start = yama_ghantaka['start']
        yama_end = yama_ghantaka['end']
        if date >= yama_start and date <= yama_end:
            in_yama_ghantaka = True
    
    if gulika_kala:
        gulika_start = gulika_kala['start']
        gulika_end = gulika_kala['end']
        if date >= gulika_start and date <= gulika_end:
            in_gulika_kala = True
    
    # Generate a basic analysis
    analysis = {
        'date': date,
        'quality': quality,
        'panchanga': panchanga,
        'best_activity': {
            'name': best_activity[0],
            'score': best_activity[1]['percentage']
        },
        'special_muhurtas': {
            'abhijit_muhurta': in_abhijit,
            'brahma_muhurta': in_brahma
        },
        'inauspicious_periods': {
            'rahu_kala': in_rahu_kala,
            'yama_ghantaka': in_yama_ghantaka,
            'gulika_kala': in_gulika_kala
        }
    }
    
    return analysis
