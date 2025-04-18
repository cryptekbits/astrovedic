"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Grahan Dosha (eclipse affliction) analysis
    for Vedic astrology.
"""

from astrovedic import const
from astrovedic.chart import Chart


def get_grahan_dosha(chart):
    """
    Check for Grahan Dosha (eclipse affliction)
    
    Args:
        chart (Chart): The chart
    
    Returns:
        dict: Dictionary with Grahan Dosha information
    """
    # Get the Sun and Moon
    sun = chart.getObject(const.SUN)
    moon = chart.getObject(const.MOON)
    
    # Get Rahu and Ketu
    rahu = chart.getObject(const.RAHU)
    ketu = chart.getObject(const.KETU)
    
    # Check for Sun-Rahu conjunction or opposition
    sun_rahu_conjunction = is_conjunct(sun.lon, rahu.lon)
    sun_rahu_opposition = is_opposite(sun.lon, rahu.lon)
    
    # Check for Moon-Ketu conjunction or opposition
    moon_ketu_conjunction = is_conjunct(moon.lon, ketu.lon)
    moon_ketu_opposition = is_opposite(moon.lon, ketu.lon)
    
    # Check for Sun-Ketu conjunction or opposition
    sun_ketu_conjunction = is_conjunct(sun.lon, ketu.lon)
    sun_ketu_opposition = is_opposite(sun.lon, ketu.lon)
    
    # Check for Moon-Rahu conjunction or opposition
    moon_rahu_conjunction = is_conjunct(moon.lon, rahu.lon)
    moon_rahu_opposition = is_opposite(moon.lon, rahu.lon)
    
    # Determine if there is Grahan Dosha
    has_solar_eclipse = sun_rahu_conjunction or sun_rahu_opposition or sun_ketu_conjunction or sun_ketu_opposition
    has_lunar_eclipse = moon_ketu_conjunction or moon_ketu_opposition or moon_rahu_conjunction or moon_rahu_opposition
    has_dosha = has_solar_eclipse or has_lunar_eclipse
    
    # Check for cancellation
    cancellation = check_grahan_dosha_cancellation(chart, has_solar_eclipse, has_lunar_eclipse)
    
    # Determine if there is Grahan Dosha after cancellation
    has_dosha = has_dosha and not cancellation['is_cancelled']
    
    
    
    return {
        'has_dosha': has_dosha,
        'has_solar_eclipse': has_solar_eclipse,
        'has_lunar_eclipse': has_lunar_eclipse,
        'sun_rahu_conjunction': sun_rahu_conjunction,
        'sun_rahu_opposition': sun_rahu_opposition,
        'moon_ketu_conjunction': moon_ketu_conjunction,
        'moon_ketu_opposition': moon_ketu_opposition,
        'sun_ketu_conjunction': sun_ketu_conjunction,
        'sun_ketu_opposition': sun_ketu_opposition,
        'moon_rahu_conjunction': moon_rahu_conjunction,
        'moon_rahu_opposition': moon_rahu_opposition,
        'cancellation': cancellation,
        }


def is_conjunct(longitude1, longitude2, orb=10):
    """
    Check if two points are conjunct
    
    Args:
        longitude1 (float): The longitude of the first point
        longitude2 (float): The longitude of the second point
        orb (float): The orb in degrees
    
    Returns:
        bool: True if the points are conjunct
    """
    # Calculate the angular distance
    distance = abs((longitude2 - longitude1) % 360)
    
    # Check if the distance is within the orb
    return distance <= orb or distance >= 360 - orb


def is_opposite(longitude1, longitude2, orb=10):
    """
    Check if two points are opposite
    
    Args:
        longitude1 (float): The longitude of the first point
        longitude2 (float): The longitude of the second point
        orb (float): The orb in degrees
    
    Returns:
        bool: True if the points are opposite
    """
    # Calculate the angular distance
    distance = abs((longitude2 - longitude1) % 360)
    
    # Check if the distance is within the orb of 180 degrees
    return abs(distance - 180) <= orb


def check_grahan_dosha_cancellation(chart, has_solar_eclipse, has_lunar_eclipse):
    """
    Check for Grahan Dosha cancellation
    
    Args:
        chart (Chart): The chart
        has_solar_eclipse (bool): Whether there is a solar eclipse
        has_lunar_eclipse (bool): Whether there is a lunar eclipse
    
    Returns:
        dict: Dictionary with cancellation information
    """
    # Initialize the cancellation
    is_cancelled = False
    cancellation_factors = []
    
    # Get Jupiter
    jupiter = chart.getObject(const.JUPITER)
    
    # Get the Sun and Moon
    sun = chart.getObject(const.SUN)
    moon = chart.getObject(const.MOON)
    
    # Get Rahu and Ketu
    rahu = chart.getObject(const.RAHU)
    ketu = chart.getObject(const.KETU)
    
    # Check if Jupiter aspects the Sun (for solar eclipse)
    if has_solar_eclipse and is_aspected_by(chart, sun.lon, jupiter.lon):
        is_cancelled = True
        cancellation_factors.append("Jupiter aspects the Sun")
    
    # Check if Jupiter aspects the Moon (for lunar eclipse)
    if has_lunar_eclipse and is_aspected_by(chart, moon.lon, jupiter.lon):
        is_cancelled = True
        cancellation_factors.append("Jupiter aspects the Moon")
    
    # Check if Jupiter aspects Rahu
    if is_aspected_by(chart, rahu.lon, jupiter.lon):
        is_cancelled = True
        cancellation_factors.append("Jupiter aspects Rahu")
    
    # Check if Jupiter aspects Ketu
    if is_aspected_by(chart, ketu.lon, jupiter.lon):
        is_cancelled = True
        cancellation_factors.append("Jupiter aspects Ketu")
    
    return {
        'is_cancelled': is_cancelled,
        'cancellation_factors': cancellation_factors
    }


def is_aspected_by(chart, longitude1, longitude2):
    """
    Check if a point is aspected by another point
    
    Args:
        chart (Chart): The chart
        longitude1 (float): The longitude of the first point
        longitude2 (float): The longitude of the second point
    
    Returns:
        bool: True if the first point is aspected by the second point
    """
    # Calculate the angular distance
    distance = abs((longitude2 - longitude1) % 360)
    
    # Check for aspects (conjunction, opposition, trine, square)
    aspects = [0, 180, 120, 90]
    
    for aspect in aspects:
        if abs(distance - aspect) <= 10:  # 10-degree orb
            return True
    
    return False



