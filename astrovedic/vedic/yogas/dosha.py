"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Dosha Yogas (combinations indicating difficulties)
    for Vedic astrology.
"""

from astrovedic import const
from astrovedic import angle
from astrovedic.vedic.yogas.core import (
    get_house_number, are_planets_conjunct,
    get_yoga_strength
)


def get_dosha_yogas(chart):
    """
    Identify Dosha Yogas in a chart
    
    Dosha Yogas are planetary combinations that indicate challenges, obstacles,
    and difficulties in life.
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        list: List of Dosha Yogas in the chart
    """
    # Initialize the result
    result = []
    
    # Check for Kemadruma Yoga
    kemadruma = has_kemadruma_yoga(chart)
    if kemadruma:
        result.append(kemadruma)
    
    # Check for Daridra Yoga
    daridra = has_daridra_yoga(chart)
    if daridra:
        result.append(daridra)
    
    # Check for Shakat Yoga
    shakat = has_shakat_yoga(chart)
    if shakat:
        result.append(shakat)
    
    # Check for Kalasarpa Yoga
    kalasarpa = has_kalasarpa_yoga(chart)
    if kalasarpa:
        result.append(kalasarpa)
    
    # Check for Graha Yuddha
    graha_yuddha = has_graha_yuddha(chart)
    if graha_yuddha:
        result.append(graha_yuddha)
    
    return result


def has_kemadruma_yoga(chart):
    """
    Check if a chart has Kemadruma Yoga
    
    Kemadruma Yoga is formed when there are no planets in the 2nd and 12th
    houses from the Moon, and the Moon is not conjunct with any planet.
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Kemadruma Yoga information, or None if not present
    """
    # Get the Moon
    moon = chart.getObject(const.MOON)
    
    # Get the house number of the Moon
    moon_house = get_house_number(chart, const.MOON)
    
    # Calculate the 2nd and 12th houses from the Moon
    house_2_from_moon = (moon_house + 1) % 12 or 12
    house_12_from_moon = (moon_house - 1) % 12 or 12
    
    # Check if there are planets in the 2nd and 12th houses from the Moon
    planets_in_2_12 = False
    for planet_id in [const.SUN, const.MERCURY, const.VENUS, const.MARS, const.JUPITER, const.SATURN]:
        planet_house = get_house_number(chart, planet_id)
        if planet_house == house_2_from_moon or planet_house == house_12_from_moon:
            planets_in_2_12 = True
            break
    
    # Check if the Moon is conjunct with any planet
    moon_conjunct = False
    for planet_id in [const.SUN, const.MERCURY, const.VENUS, const.MARS, const.JUPITER, const.SATURN]:
        if are_planets_conjunct(chart, const.MOON, planet_id):
            moon_conjunct = True
            break
    
    # Check if Kemadruma Yoga is formed
    if not planets_in_2_12 and not moon_conjunct:
        # Create the Yoga information
        yoga = {
            'name': 'Kemadruma Yoga',
            'type': 'Dosha Yoga',
            'planets': [const.MOON],
            'houses': [moon_house],
            'description': 'Formed when there are no planets in the 2nd and 12th houses from the Moon, and the Moon is not conjunct with any planet',
            'is_beneficial': False
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    return None


def has_daridra_yoga(chart):
    """
    Check if a chart has Daridra Yoga
    
    Daridra Yoga is formed when the lords of the 1st, 5th, and 9th houses
    are all in the 6th, 8th, or 12th houses.
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Daridra Yoga information, or None if not present
    """
    # Get the lords of the 1st, 5th, and 9th houses
    lord_1 = get_house_lord(chart, 1)
    lord_5 = get_house_lord(chart, 5)
    lord_9 = get_house_lord(chart, 9)
    
    # Get the house numbers of the lords
    lord_1_house = get_house_number(chart, lord_1)
    lord_5_house = get_house_number(chart, lord_5)
    lord_9_house = get_house_number(chart, lord_9)
    
    # Check if all lords are in the 6th, 8th, or 12th houses
    all_in_dusthana = (
        lord_1_house in [6, 8, 12] and
        lord_5_house in [6, 8, 12] and
        lord_9_house in [6, 8, 12]
    )
    
    # Check if Daridra Yoga is formed
    if all_in_dusthana:
        # Create the Yoga information
        yoga = {
            'name': 'Daridra Yoga',
            'type': 'Dosha Yoga',
            'planets': [lord_1, lord_5, lord_9],
            'houses': [1, 5, 9],
            'description': 'Formed when the lords of the 1st, 5th, and 9th houses are all in the 6th, 8th, or 12th houses',
            'is_beneficial': False
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    return None


def has_shakat_yoga(chart):
    """
    Check if a chart has Shakat Yoga
    
    Shakat Yoga is formed when the Moon is in the 6th, 8th, or 12th house
    from Jupiter.
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Shakat Yoga information, or None if not present
    """
    # Get the Moon and Jupiter
    moon = chart.getObject(const.MOON)
    jupiter = chart.getObject(const.JUPITER)
    
    # Get the house numbers of the Moon and Jupiter
    moon_house = get_house_number(chart, const.MOON)
    jupiter_house = get_house_number(chart, const.JUPITER)
    
    # Calculate the house position of the Moon from Jupiter
    moon_from_jupiter = (moon_house - jupiter_house) % 12 or 12
    
    # Check if the Moon is in the 6th, 8th, or 12th house from Jupiter
    is_in_dusthana = moon_from_jupiter in [6, 8, 12]
    
    # Check if Shakat Yoga is formed
    if is_in_dusthana:
        # Create the Yoga information
        yoga = {
            'name': 'Shakat Yoga',
            'type': 'Dosha Yoga',
            'planets': [const.MOON, const.JUPITER],
            'houses': [moon_house, jupiter_house],
            'description': 'Formed when the Moon is in the 6th, 8th, or 12th house from Jupiter',
            'is_beneficial': False
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    return None


def has_kalasarpa_yoga(chart):
    """
    Check if a chart has Kalasarpa Yoga
    
    Kalasarpa Yoga is formed when all planets are between Rahu and Ketu.
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Kalasarpa Yoga information, or None if not present
    """
    # Get Rahu and Ketu
    rahu = chart.getObject(const.RAHU)
    ketu = chart.getObject(const.KETU)
    
    # Get the longitudes of Rahu and Ketu
    rahu_lon = rahu.lon
    ketu_lon = ketu.lon
    
    # Check if all planets are between Rahu and Ketu
    all_between = True
    for planet_id in [const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS, const.JUPITER, const.SATURN]:
        planet = chart.getObject(planet_id)
        
        # Calculate the distance from Rahu to the planet
        dist_rahu_planet = angle.distance(rahu_lon, planet.lon)
        
        # Calculate the distance from Rahu to Ketu
        dist_rahu_ketu = angle.distance(rahu_lon, ketu_lon)
        
        # Check if the planet is between Rahu and Ketu
        if dist_rahu_planet > dist_rahu_ketu:
            all_between = False
            break
    
    # Check if Kalasarpa Yoga is formed
    if all_between:
        # Create the Yoga information
        yoga = {
            'name': 'Kalasarpa Yoga',
            'type': 'Dosha Yoga',
            'planets': [const.RAHU, const.KETU],
            'houses': [get_house_number(chart, const.RAHU), get_house_number(chart, const.KETU)],
            'description': 'Formed when all planets are between Rahu and Ketu',
            'is_beneficial': False
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    return None


def has_graha_yuddha(chart):
    """
    Check if a chart has Graha Yuddha (Planetary War)
    
    Graha Yuddha is formed when two planets (except the Sun and Moon) are
    within 1 degree of each other.
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Graha Yuddha information, or None if not present
    """
    # List of planets that can participate in Graha Yuddha
    planets = [const.MERCURY, const.VENUS, const.MARS, const.JUPITER, const.SATURN]
    
    # Check for Graha Yuddha between each pair of planets
    for i in range(len(planets)):
        for j in range(i+1, len(planets)):
            planet1_id = planets[i]
            planet2_id = planets[j]
            
            # Get the planets
            planet1 = chart.getObject(planet1_id)
            planet2 = chart.getObject(planet2_id)
            
            # Calculate the distance between the planets
            dist = abs(angle.closestdistance(planet1.lon, planet2.lon))
            
            # Check if the planets are within 1 degree of each other
            if dist <= 1.0:
                # Create the Yoga information
                yoga = {
                    'name': 'Graha Yuddha',
                    'type': 'Dosha Yoga',
                    'planets': [planet1_id, planet2_id],
                    'houses': [get_house_number(chart, planet1_id), get_house_number(chart, planet2_id)],
                    'description': f'Formed when {planet1_id} and {planet2_id} are within 1 degree of each other',
                    'is_beneficial': False
                }
                
                # Calculate the strength of the Yoga
                yoga['strength'] = get_yoga_strength(chart, yoga)
                
                return yoga
    
    return None


def get_house_lord(chart, house_num):
    """
    Get the lord of a house
    
    Args:
        chart (Chart): The birth chart
        house_num (int): The house number (1-12)
    
    Returns:
        str: The ID of the planet ruling the house
    """
    # Get the house
    house = chart.getHouse(f"House{house_num}")
    
    # Get the sign of the house
    sign = house.sign
    
    # Get the lord of the sign
    if sign == const.ARIES:
        return const.MARS
    elif sign == const.TAURUS:
        return const.VENUS
    elif sign == const.GEMINI:
        return const.MERCURY
    elif sign == const.CANCER:
        return const.MOON
    elif sign == const.LEO:
        return const.SUN
    elif sign == const.VIRGO:
        return const.MERCURY
    elif sign == const.LIBRA:
        return const.VENUS
    elif sign == const.SCORPIO:
        return const.MARS
    elif sign == const.SAGITTARIUS:
        return const.JUPITER
    elif sign == const.CAPRICORN:
        return const.SATURN
    elif sign == const.AQUARIUS:
        return const.SATURN
    elif sign == const.PISCES:
        return const.JUPITER
    
    return None
