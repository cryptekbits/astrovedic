"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Mangal Dosha (Mars affliction) analysis
    for Vedic astrology.
"""

from astrovedic import const
from astrovedic.chart import Chart


def get_mangal_dosha(chart):
    """
    Check for Mangal Dosha (Mars affliction)

    Args:
        chart (Chart): The chart

    Returns:
        dict: Dictionary with Mangal Dosha information
    """
    # Get Mars
    mars = chart.getObject(const.MARS)

    # Get the house position of Mars
    mars_house = get_house_position(chart, mars.lon)

    # Check if Mars is in a Mangal Dosha house
    is_in_dosha_house = mars_house in [1, 2, 4, 7, 8, 12]

    # Check for cancellation
    cancellation = check_mangal_dosha_cancellation(chart, mars, mars_house)

    # Determine if there is Mangal Dosha
    has_dosha = is_in_dosha_house and not cancellation['is_cancelled']



    return {
        'has_dosha': has_dosha,
        'mars_house': mars_house,
        'is_in_dosha_house': is_in_dosha_house,
        'cancellation': cancellation
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


def check_mangal_dosha_cancellation(chart, mars, mars_house):
    """
    Check for Mangal Dosha cancellation

    Args:
        chart (Chart): The chart
        mars (Object): The Mars object
        mars_house (int): The house position of Mars

    Returns:
        dict: Dictionary with cancellation information
    """
    # Initialize the cancellation
    is_cancelled = False
    cancellation_factors = []

    # Get the Moon
    moon = chart.getObject(const.MOON)

    # Get the house position of the Moon
    moon_house = get_house_position(chart, moon.lon)

    # Get Jupiter
    jupiter = chart.getObject(const.JUPITER)

    # Get the house position of Jupiter
    jupiter_house = get_house_position(chart, jupiter.lon)

    # Check if Mars is in its own sign (Aries or Scorpio)
    if mars.sign in [const.ARIES, const.SCORPIO]:
        is_cancelled = True
        cancellation_factors.append("Mars is in its own sign")

    # Check if Mars is aspected by Jupiter
    if is_aspected_by(chart, mars.lon, jupiter.lon):
        is_cancelled = True
        cancellation_factors.append("Mars is aspected by Jupiter")

    # Check if Mars is in the same house as Jupiter
    if mars_house == jupiter_house:
        is_cancelled = True
        cancellation_factors.append("Mars is in the same house as Jupiter")

    # Check if Mars is in the same house as the Moon
    if mars_house == moon_house:
        is_cancelled = True
        cancellation_factors.append("Mars is in the same house as the Moon")

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



