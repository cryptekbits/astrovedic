"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Kuja Dosha (Mars affliction) analysis
    for Vedic astrology.
"""

from astrovedic import const
from astrovedic.chart import Chart


def get_kuja_dosha(chart):
    """
    Check for Kuja Dosha (Mars affliction)

    Args:
        chart (Chart): The chart

    Returns:
        dict: Dictionary with Kuja Dosha information
    """
    # Get Mars
    mars = chart.getObject(const.MARS)

    # Get the house position of Mars from the Ascendant
    mars_house_from_asc = get_house_position(chart, mars.lon, const.ASC)

    # Get the house position of Mars from the Moon
    moon = chart.getObject(const.MOON)
    mars_house_from_moon = get_house_position(chart, mars.lon, moon.lon)

    # Get the house position of Mars from Venus
    venus = chart.getObject(const.VENUS)
    mars_house_from_venus = get_house_position(chart, mars.lon, venus.lon)

    # Check if Mars is in a Kuja Dosha house from any reference point
    is_in_dosha_house_from_asc = mars_house_from_asc in [1, 2, 4, 7, 8, 12]
    is_in_dosha_house_from_moon = mars_house_from_moon in [1, 2, 4, 7, 8, 12]
    is_in_dosha_house_from_venus = mars_house_from_venus in [1, 2, 4, 7, 8, 12]

    # Determine if there is Kuja Dosha
    is_in_dosha_house = is_in_dosha_house_from_asc or is_in_dosha_house_from_moon or is_in_dosha_house_from_venus

    # Check for cancellation
    cancellation = check_kuja_dosha_cancellation(chart, mars, mars_house_from_asc)

    # Determine if there is Kuja Dosha
    has_dosha = is_in_dosha_house and not cancellation['is_cancelled']

    

    return {
        'has_dosha': has_dosha,
        'mars_house_from_asc': mars_house_from_asc,
        'mars_house_from_moon': mars_house_from_moon,
        'mars_house_from_venus': mars_house_from_venus,
        'is_in_dosha_house_from_asc': is_in_dosha_house_from_asc,
        'is_in_dosha_house_from_moon': is_in_dosha_house_from_moon,
        'is_in_dosha_house_from_venus': is_in_dosha_house_from_venus,
        'is_in_dosha_house': is_in_dosha_house,
        'cancellation': cancellation,
        }


def get_house_position(chart, longitude, reference_point_id):
    """
    Get the house position for a specific longitude from a reference point

    Args:
        chart (Chart): The chart
        longitude (float): The longitude
        reference_point_id (str): The ID of the reference point

    Returns:
        int: The house position (1-12)
    """
    # Get the reference point
    if isinstance(reference_point_id, (int, float)):
        # If reference_point_id is a number, use it directly as longitude
        reference_point_lon = reference_point_id
    elif reference_point_id in [const.ASC, const.MC, const.DESC, const.IC]:
        reference_point = chart.getAngle(reference_point_id)
        reference_point_lon = reference_point.lon
    else:
        reference_point = chart.getObject(reference_point_id)
        reference_point_lon = reference_point.lon

    # Calculate the house position
    house_position = 1 + int((longitude - reference_point_lon) / 30) % 12

    # If house_position is 0, it means it's the 12th house
    if house_position == 0:
        house_position = 12

    return house_position


def check_kuja_dosha_cancellation(chart, mars, mars_house):
    """
    Check for Kuja Dosha cancellation

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

    # Get Jupiter
    jupiter = chart.getObject(const.JUPITER)

    # Get the house position of Jupiter
    jupiter_house = get_house_position(chart, jupiter.lon, const.ASC)

    # Check if Mars is in its own sign (Aries or Scorpio)
    if mars.sign in [const.ARIES, const.SCORPIO]:
        is_cancelled = True
        cancellation_factors.append("Mars is in its own sign")

    # Check if Mars is in Cancer
    if mars.sign == const.CANCER:
        is_cancelled = True
        cancellation_factors.append("Mars is in Cancer")

    # Check if Mars is aspected by Jupiter
    if is_aspected_by(chart, mars.lon, jupiter.lon):
        is_cancelled = True
        cancellation_factors.append("Mars is aspected by Jupiter")

    # Check if Mars is in the same house as Jupiter
    if mars_house == jupiter_house:
        is_cancelled = True
        cancellation_factors.append("Mars is in the same house as Jupiter")

    # Check if Mars is in the 11th house
    if mars_house == 11:
        is_cancelled = True
        cancellation_factors.append("Mars is in the 11th house")

    # Check if Mars is in the 3rd house
    if mars_house == 3:
        is_cancelled = True
        cancellation_factors.append("Mars is in the 3rd house")

    # Check if Mars is in the 6th house
    if mars_house == 6:
        is_cancelled = True
        cancellation_factors.append("Mars is in the 6th house")

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




    # Check if Kuja Dosha is cancelled
    if cancellation['is_cancelled']:
        factors = ", ".join(cancellation['cancellation_factors'])
        return f"Kuja Dosha is present but cancelled. The Dosha is cancelled due to: {factors}."

    # Generate the description
    description = "Kuja Dosha is present. "

    if is_in_dosha_house_from_asc:
        description += f"Mars is in the {mars_house_from_asc}th house from the Ascendant. "

    if is_in_dosha_house_from_moon:
        description += f"Mars is in the {mars_house_from_moon}th house from the Moon. "

    if is_in_dosha_house_from_venus:
        description += f"Mars is in the {mars_house_from_venus}th house from Venus. "

    description += "This may cause marital discord, health issues for the spouse, or financial problems in marriage."

    return description
