"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Kala Sarpa Dosha (Serpent of Time affliction) analysis
    for Vedic astrology.
"""

from astrovedic import const
from astrovedic import angle
from astrovedic.chart import Chart


def get_kalasarpa_dosha(chart):
    """
    Check for Kala Sarpa Dosha (Serpent of Time affliction)
    
    Args:
        chart (Chart): The chart
    
    Returns:
        dict: Dictionary with Kala Sarpa Dosha information
    """
    # Get Rahu and Ketu
    rahu = chart.getObject(const.RAHU)
    ketu = chart.getObject(const.KETU)
    
    # Get the longitudes of Rahu and Ketu
    rahu_lon = rahu.lon
    ketu_lon = ketu.lon
    
    # Check if all planets are between Rahu and Ketu
    all_between_rahu_ketu = True
    for planet_id in [const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS, const.JUPITER, const.SATURN]:
        planet = chart.getObject(planet_id)
        
        # Calculate the distance from Rahu to the planet
        dist_rahu_planet = angle.distance(rahu_lon, planet.lon)
        
        # Calculate the distance from Rahu to Ketu
        dist_rahu_ketu = angle.distance(rahu_lon, ketu_lon)
        
        # Check if the planet is between Rahu and Ketu
        if dist_rahu_planet > dist_rahu_ketu:
            all_between_rahu_ketu = False
            break
    
    # Check if all planets are between Ketu and Rahu
    all_between_ketu_rahu = True
    for planet_id in [const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS, const.JUPITER, const.SATURN]:
        planet = chart.getObject(planet_id)
        
        # Calculate the distance from Ketu to the planet
        dist_ketu_planet = angle.distance(ketu_lon, planet.lon)
        
        # Calculate the distance from Ketu to Rahu
        dist_ketu_rahu = angle.distance(ketu_lon, rahu_lon)
        
        # Check if the planet is between Ketu and Rahu
        if dist_ketu_planet > dist_ketu_rahu:
            all_between_ketu_rahu = False
            break
    
    # Check for partial Kala Sarpa Dosha
    partial_dosha = False
    if not all_between_rahu_ketu and not all_between_ketu_rahu:
        # Count planets on each side of the Rahu-Ketu axis
        planets_between_rahu_ketu = 0
        planets_between_ketu_rahu = 0
        
        for planet_id in [const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS, const.JUPITER, const.SATURN]:
            planet = chart.getObject(planet_id)
            
            # Calculate the distance from Rahu to the planet
            dist_rahu_planet = angle.distance(rahu_lon, planet.lon)
            
            # Calculate the distance from Rahu to Ketu
            dist_rahu_ketu = angle.distance(rahu_lon, ketu_lon)
            
            # Check if the planet is between Rahu and Ketu
            if dist_rahu_planet <= dist_rahu_ketu:
                planets_between_rahu_ketu += 1
            else:
                planets_between_ketu_rahu += 1
        
        # If most planets (5 or more) are on one side, it's a partial Kala Sarpa Dosha
        partial_dosha = planets_between_rahu_ketu >= 5 or planets_between_ketu_rahu >= 5
    
    # Check for cancellation
    cancellation = check_kalasarpa_dosha_cancellation(chart)
    
    # Determine the type of Kala Sarpa Dosha
    dosha_type = None
    if all_between_rahu_ketu:
        dosha_type = "Full Kala Sarpa Dosha (Rahu to Ketu)"
    elif all_between_ketu_rahu:
        dosha_type = "Full Kala Sarpa Dosha (Ketu to Rahu)"
    elif partial_dosha:
        dosha_type = "Partial Kala Sarpa Dosha"
    
    # Determine if there is Kala Sarpa Dosha
    has_dosha = (all_between_rahu_ketu or all_between_ketu_rahu or partial_dosha) and not cancellation['is_cancelled']
    
    return {
        'has_dosha': has_dosha,
        'dosha_type': dosha_type,
        'all_between_rahu_ketu': all_between_rahu_ketu,
        'all_between_ketu_rahu': all_between_ketu_rahu,
        'partial_dosha': partial_dosha,
        'cancellation': cancellation
    }


def check_kalasarpa_dosha_cancellation(chart):
    """
    Check for Kala Sarpa Dosha cancellation
    
    Args:
        chart (Chart): The chart
    
    Returns:
        dict: Dictionary with cancellation information
    """
    # Initialize the cancellation
    is_cancelled = False
    cancellation_factors = []
    
    # Get Rahu and Ketu
    rahu = chart.getObject(const.RAHU)
    ketu = chart.getObject(const.KETU)
    
    # Get the house positions of Rahu and Ketu
    rahu_house = get_house_position(chart, rahu.lon)
    ketu_house = get_house_position(chart, ketu.lon)
    
    # Get Jupiter
    jupiter = chart.getObject(const.JUPITER)
    
    # Get the house position of Jupiter
    jupiter_house = get_house_position(chart, jupiter.lon)
    
    # Check if Jupiter is conjunct with Rahu or Ketu
    jupiter_conjunct_rahu = is_conjunct(jupiter.lon, rahu.lon)
    jupiter_conjunct_ketu = is_conjunct(jupiter.lon, ketu.lon)
    
    # Check if Jupiter aspects Rahu or Ketu
    jupiter_aspects_rahu = is_aspected_by(chart, rahu.lon, jupiter.lon)
    jupiter_aspects_ketu = is_aspected_by(chart, ketu.lon, jupiter.lon)
    
    # Check for cancellation factors
    if jupiter_conjunct_rahu:
        is_cancelled = True
        cancellation_factors.append("Jupiter is conjunct with Rahu")
    
    if jupiter_conjunct_ketu:
        is_cancelled = True
        cancellation_factors.append("Jupiter is conjunct with Ketu")
    
    if jupiter_aspects_rahu:
        is_cancelled = True
        cancellation_factors.append("Jupiter aspects Rahu")
    
    if jupiter_aspects_ketu:
        is_cancelled = True
        cancellation_factors.append("Jupiter aspects Ketu")
    
    # Check if Rahu and Ketu are in the 3rd and 9th houses
    if (rahu_house == 3 and ketu_house == 9) or (rahu_house == 9 and ketu_house == 3):
        is_cancelled = True
        cancellation_factors.append("Rahu and Ketu are in the 3rd and 9th houses")
    
    # Check if Rahu and Ketu are in the 6th and 12th houses
    if (rahu_house == 6 and ketu_house == 12) or (rahu_house == 12 and ketu_house == 6):
        is_cancelled = True
        cancellation_factors.append("Rahu and Ketu are in the 6th and 12th houses")
    
    return {
        'is_cancelled': is_cancelled,
        'cancellation_factors': cancellation_factors
    }


def get_house_position(chart, longitude):
    """
    Get the house position for a specific longitude
    
    Args:
        chart (Chart): The chart
        longitude (float): The longitude
    
    Returns:
        int: The house position (1-12)
    """
    # Get the Ascendant
    asc = chart.getAngle(const.ASC)
    
    # Calculate the house position
    house_position = 1 + int((longitude - asc.lon) / 30) % 12
    
    # If house_position is 0, it means it's the 12th house
    if house_position == 0:
        house_position = 12
    
    return house_position


def is_conjunct(longitude1, longitude2):
    """
    Check if two points are conjunct
    
    Args:
        longitude1 (float): The longitude of the first point
        longitude2 (float): The longitude of the second point
    
    Returns:
        bool: True if the points are conjunct
    """
    # Calculate the angular distance
    distance = abs((longitude2 - longitude1) % 360)
    if distance > 180:
        distance = 360 - distance
    
    # Check for conjunction (within 10 degrees)
    return distance <= 10


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
    if distance > 180:
        distance = 360 - distance
    
    # Check for aspects (conjunction, opposition, trine, square)
    aspects = [0, 180, 120, 90]
    
    for aspect in aspects:
        if abs(distance - aspect) <= 10:  # 10-degree orb
            return True
    
    return False
