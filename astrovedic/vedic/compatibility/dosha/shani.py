"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Shani Dosha (Saturn affliction) analysis
    for Vedic astrology.
"""

from astrovedic import const
from astrovedic.chart import Chart


def get_shani_dosha(chart):
    """
    Check for Shani Dosha (Saturn affliction)
    
    Args:
        chart (Chart): The chart
    
    Returns:
        dict: Dictionary with Shani Dosha information
    """
    # Get Saturn
    saturn = chart.getObject(const.SATURN)
    
    # Get the house position of Saturn
    saturn_house = get_house_position(chart, saturn.lon)
    
    # Check if Saturn is in a Shani Dosha house
    is_in_dosha_house = saturn_house in [1, 2, 4, 7, 8, 10, 12]
    
    # Check for cancellation
    cancellation = check_shani_dosha_cancellation(chart, saturn, saturn_house)
    
    # Determine if there is Shani Dosha
    has_dosha = is_in_dosha_house and not cancellation['is_cancelled']
    
    # Check for Sade Sati
    sade_sati = check_sade_sati(chart, saturn)
    
    # Generate the description
    description = generate_shani_dosha_description(saturn_house, is_in_dosha_house, cancellation, sade_sati)
    
    return {
        'has_dosha': has_dosha,
        'saturn_house': saturn_house,
        'is_in_dosha_house': is_in_dosha_house,
        'cancellation': cancellation,
        'sade_sati': sade_sati,
        'description': description
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


def check_shani_dosha_cancellation(chart, saturn, saturn_house):
    """
    Check for Shani Dosha cancellation
    
    Args:
        chart (Chart): The chart
        saturn (Object): The Saturn object
        saturn_house (int): The house position of Saturn
    
    Returns:
        dict: Dictionary with cancellation information
    """
    # Initialize the cancellation
    is_cancelled = False
    cancellation_factors = []
    
    # Get Jupiter
    jupiter = chart.getObject(const.JUPITER)
    
    # Get the house position of Jupiter
    jupiter_house = get_house_position(chart, jupiter.lon)
    
    # Check if Saturn is in its own sign (Capricorn or Aquarius)
    if saturn.sign in [const.CAPRICORN, const.AQUARIUS]:
        is_cancelled = True
        cancellation_factors.append("Saturn is in its own sign")
    
    # Check if Saturn is in Libra (exaltation)
    if saturn.sign == const.LIBRA:
        is_cancelled = True
        cancellation_factors.append("Saturn is exalted in Libra")
    
    # Check if Saturn is aspected by Jupiter
    if is_aspected_by(chart, saturn.lon, jupiter.lon):
        is_cancelled = True
        cancellation_factors.append("Saturn is aspected by Jupiter")
    
    # Check if Saturn is in the same house as Jupiter
    if saturn_house == jupiter_house:
        is_cancelled = True
        cancellation_factors.append("Saturn is in the same house as Jupiter")
    
    # Check if Saturn is in the 3rd, 6th, or 11th house
    if saturn_house in [3, 6, 11]:
        is_cancelled = True
        cancellation_factors.append(f"Saturn is in the {saturn_house}th house, which is a favorable house for Saturn")
    
    return {
        'is_cancelled': is_cancelled,
        'cancellation_factors': cancellation_factors
    }


def check_sade_sati(chart, saturn):
    """
    Check for Sade Sati (7.5 years of Saturn transit)
    
    Args:
        chart (Chart): The chart
        saturn (Object): The Saturn object
    
    Returns:
        dict: Dictionary with Sade Sati information
    """
    # Get the Moon
    moon = chart.getObject(const.MOON)
    
    # Get the Moon sign
    moon_sign = moon.sign
    
    # Get the Moon sign number (0-11)
    moon_sign_num = const.LIST_SIGNS.index(moon_sign)
    
    # Get the Saturn sign
    saturn_sign = saturn.sign
    
    # Get the Saturn sign number (0-11)
    saturn_sign_num = const.LIST_SIGNS.index(saturn_sign)
    
    # Calculate the distance between Saturn and Moon signs
    distance = (saturn_sign_num - moon_sign_num) % 12
    
    # Check if Saturn is in the 12th, 1st, or 2nd house from the Moon sign
    is_in_sade_sati = distance in [11, 0, 1]
    
    # Determine the phase of Sade Sati
    if distance == 11:
        phase = "First phase (Dhaiya)"
    elif distance == 0:
        phase = "Second phase (Peak)"
    elif distance == 1:
        phase = "Third phase (Kantaka)"
    else:
        phase = "Not in Sade Sati"
    
    return {
        'is_in_sade_sati': is_in_sade_sati,
        'phase': phase
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


def generate_shani_dosha_description(saturn_house, is_in_dosha_house, cancellation, sade_sati):
    """
    Generate a description for Shani Dosha
    
    Args:
        saturn_house (int): The house position of Saturn
        is_in_dosha_house (bool): Whether Saturn is in a Dosha house
        cancellation (dict): The cancellation information
        sade_sati (dict): The Sade Sati information
    
    Returns:
        str: The Shani Dosha description
    """
    description = ""
    
    # Check if there is no Shani Dosha
    if not is_in_dosha_house:
        description += f"No Shani Dosha is present. Saturn is in the {saturn_house}th house, which is not a Dosha house. "
    else:
        # Check if Shani Dosha is cancelled
        if cancellation['is_cancelled']:
            factors = ", ".join(cancellation['cancellation_factors'])
            description += f"Shani Dosha is present but cancelled. Saturn is in the {saturn_house}th house, but the Dosha is cancelled due to: {factors}. "
        else:
            # Define the effects for each Dosha house
            dosha_effects = {
                1: "may cause physical ailments, obstacles, and a serious personality",
                2: "may cause financial problems, family conflicts, and speech defects",
                4: "may cause property disputes, emotional instability, and mother-related issues",
                7: "may cause marital discord, delayed marriage, or health issues for the spouse",
                8: "may cause health problems, accidents, and sudden changes in life",
                10: "may cause career obstacles, authority issues, and father-related problems",
                12: "may cause financial losses, isolation, and foreign residence"
            }
            
            effect = dosha_effects.get(saturn_house, "may cause various challenges in life")
            
            description += f"Shani Dosha is present. Saturn is in the {saturn_house}th house, which {effect}. "
    
    # Add Sade Sati information
    if sade_sati['is_in_sade_sati']:
        description += f"The person is currently in Sade Sati ({sade_sati['phase']}), which is a challenging 7.5-year period of Saturn transit."
    else:
        description += "The person is not currently in Sade Sati."
    
    return description
