"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements core functionality for Yogas (planetary combinations)
    calculations in Vedic astrology.
"""

from flatlib import const
from flatlib import angle


def get_yoga_summary(yogas):
    """
    Generate a summary of Yogas in a chart
    
    Args:
        yogas (dict): Dictionary with Yoga information
    
    Returns:
        dict: Dictionary with summary information
    """
    # Initialize the summary
    summary = {
        'total_yogas': 0,
        'beneficial_yogas': 0,
        'harmful_yogas': 0,
        'yoga_types': {},
        'strongest_yoga': None
    }
    
    # Count the number of Yogas of each type
    for yoga_type, yoga_list in yogas.items():
        if yoga_type != 'summary':
            # Count the Yogas
            num_yogas = len(yoga_list)
            summary['total_yogas'] += num_yogas
            summary['yoga_types'][yoga_type] = num_yogas
            
            # Count beneficial and harmful Yogas
            for yoga in yoga_list:
                if yoga.get('is_beneficial', True):
                    summary['beneficial_yogas'] += 1
                else:
                    summary['harmful_yogas'] += 1
    
    # Find the strongest Yoga
    strongest_yoga = None
    max_strength = -1
    
    for yoga_type, yoga_list in yogas.items():
        if yoga_type != 'summary':
            for yoga in yoga_list:
                strength = yoga.get('strength', 0)
                if strength > max_strength:
                    max_strength = strength
                    strongest_yoga = yoga
    
    summary['strongest_yoga'] = strongest_yoga
    
    return summary


def get_yoga_strength(chart, yoga):
    """
    Calculate the strength of a Yoga
    
    Args:
        chart (Chart): The birth chart
        yoga (dict): Dictionary with Yoga information
    
    Returns:
        float: The strength of the Yoga (0-100)
    """
    # Get the planets involved in the Yoga
    planets = yoga.get('planets', [])
    
    # If no planets are specified, return a default strength
    if not planets:
        return 50.0
    
    # Calculate the strength based on the planets' positions
    strength = 0.0
    
    for planet_id in planets:
        # Get the planet from the chart
        planet = chart.getObject(planet_id)
        
        # Check if the planet is in its own sign
        if is_in_own_sign(planet):
            strength += 20.0
        
        # Check if the planet is exalted
        elif is_exalted(planet):
            strength += 15.0
        
        # Check if the planet is in a friendly sign
        elif is_in_friendly_sign(planet):
            strength += 10.0
        
        # Check if the planet is in an enemy sign
        elif is_in_enemy_sign(planet):
            strength += 5.0
        
        # Check if the planet is debilitated
        elif is_debilitated(planet):
            strength += 0.0
        
        # Default case
        else:
            strength += 7.5
    
    # Calculate the average strength
    avg_strength = strength / len(planets) if planets else 0.0
    
    # Adjust based on the Yoga type
    yoga_type = yoga.get('type', '')
    
    if yoga_type == 'Mahapurusha Yoga':
        avg_strength *= 1.2
    elif yoga_type == 'Raja Yoga':
        avg_strength *= 1.1
    elif yoga_type == 'Dhana Yoga':
        avg_strength *= 1.0
    elif yoga_type == 'Nabhasa Yoga':
        avg_strength *= 0.9
    elif yoga_type == 'Chandra Yoga':
        avg_strength *= 0.8
    elif yoga_type == 'Dosha Yoga':
        avg_strength = 100.0 - avg_strength
    
    # Ensure the strength is within 0-100
    return max(0.0, min(avg_strength, 100.0))


def get_yoga_effects(chart, yoga):
    """
    Generate the effects of a Yoga
    
    Args:
        chart (Chart): The birth chart
        yoga (dict): Dictionary with Yoga information
    
    Returns:
        list: List of effects of the Yoga
    """
    # Get the Yoga name and type
    yoga_name = yoga.get('name', '')
    yoga_type = yoga.get('type', '')
    
    # Get the strength of the Yoga
    strength = get_yoga_strength(chart, yoga)
    
    # Initialize the effects list
    effects = []
    
    # Add effects based on the Yoga type
    if yoga_type == 'Mahapurusha Yoga':
        effects.append("Indicates a great personality with leadership qualities")
        effects.append("Brings fame, power, and recognition in society")
        effects.append("Enhances the positive qualities of the planet forming the Yoga")
    
    elif yoga_type == 'Raja Yoga':
        effects.append("Indicates royal status, authority, and power")
        effects.append("Brings success in career and professional life")
        effects.append("Enhances social status and reputation")
    
    elif yoga_type == 'Dhana Yoga':
        effects.append("Indicates wealth, prosperity, and financial success")
        effects.append("Brings material comforts and luxuries")
        effects.append("Enhances the ability to accumulate wealth")
    
    elif yoga_type == 'Nabhasa Yoga':
        effects.append("Indicates specific patterns of planetary arrangements")
        effects.append("Brings unique personality traits and life experiences")
        effects.append("Enhances specific areas of life based on the Yoga")
    
    elif yoga_type == 'Chandra Yoga':
        effects.append("Indicates emotional well-being and mental stability")
        effects.append("Brings success in areas related to the Moon")
        effects.append("Enhances intuition, creativity, and emotional intelligence")
    
    elif yoga_type == 'Dosha Yoga':
        effects.append("Indicates challenges and obstacles in life")
        effects.append("Brings difficulties in areas related to the Yoga")
        effects.append("May cause delays, setbacks, or hardships")
    
    # Add specific effects based on the Yoga name
    # This is a simplified version; a more comprehensive implementation
    # would include specific effects for each Yoga
    
    # Adjust the effects based on the strength
    if strength >= 75.0:
        effects.append("The effects of this Yoga are very strong and prominent")
    elif strength >= 50.0:
        effects.append("The effects of this Yoga are moderate and noticeable")
    elif strength >= 25.0:
        effects.append("The effects of this Yoga are mild and subtle")
    else:
        effects.append("The effects of this Yoga are very weak and may not be noticeable")
    
    return effects


def get_strongest_yoga(yogas):
    """
    Find the strongest Yoga in a chart
    
    Args:
        yogas (dict): Dictionary with Yoga information
    
    Returns:
        dict: Dictionary with the strongest Yoga information
    """
    # Initialize variables
    strongest_yoga = None
    max_strength = -1
    
    # Check each type of Yoga
    for yoga_type, yoga_list in yogas.items():
        if yoga_type != 'summary':
            for yoga in yoga_list:
                strength = yoga.get('strength', 0)
                if strength > max_strength:
                    max_strength = strength
                    strongest_yoga = yoga
    
    return strongest_yoga


def is_in_own_sign(planet):
    """
    Check if a planet is in its own sign
    
    Args:
        planet (Object): The planet to check
    
    Returns:
        bool: True if the planet is in its own sign, False otherwise
    """
    # Get the planet's sign
    sign = planet.sign
    
    # Check if the planet is in its own sign
    if planet.id == const.SUN and sign == const.LEO:
        return True
    elif planet.id == const.MOON and sign == const.CANCER:
        return True
    elif planet.id == const.MERCURY and (sign == const.GEMINI or sign == const.VIRGO):
        return True
    elif planet.id == const.VENUS and (sign == const.TAURUS or sign == const.LIBRA):
        return True
    elif planet.id == const.MARS and (sign == const.ARIES or sign == const.SCORPIO):
        return True
    elif planet.id == const.JUPITER and (sign == const.SAGITTARIUS or sign == const.PISCES):
        return True
    elif planet.id == const.SATURN and (sign == const.CAPRICORN or sign == const.AQUARIUS):
        return True
    
    return False


def is_exalted(planet):
    """
    Check if a planet is exalted
    
    Args:
        planet (Object): The planet to check
    
    Returns:
        bool: True if the planet is exalted, False otherwise
    """
    # Get the planet's sign
    sign = planet.sign
    
    # Check if the planet is exalted
    if planet.id == const.SUN and sign == const.ARIES:
        return True
    elif planet.id == const.MOON and sign == const.TAURUS:
        return True
    elif planet.id == const.MERCURY and sign == const.VIRGO:
        return True
    elif planet.id == const.VENUS and sign == const.PISCES:
        return True
    elif planet.id == const.MARS and sign == const.CAPRICORN:
        return True
    elif planet.id == const.JUPITER and sign == const.CANCER:
        return True
    elif planet.id == const.SATURN and sign == const.LIBRA:
        return True
    elif planet.id == const.RAHU and sign == const.TAURUS:
        return True
    elif planet.id == const.KETU and sign == const.SCORPIO:
        return True
    
    return False


def is_debilitated(planet):
    """
    Check if a planet is debilitated
    
    Args:
        planet (Object): The planet to check
    
    Returns:
        bool: True if the planet is debilitated, False otherwise
    """
    # Get the planet's sign
    sign = planet.sign
    
    # Check if the planet is debilitated
    if planet.id == const.SUN and sign == const.LIBRA:
        return True
    elif planet.id == const.MOON and sign == const.SCORPIO:
        return True
    elif planet.id == const.MERCURY and sign == const.PISCES:
        return True
    elif planet.id == const.VENUS and sign == const.VIRGO:
        return True
    elif planet.id == const.MARS and sign == const.CANCER:
        return True
    elif planet.id == const.JUPITER and sign == const.CAPRICORN:
        return True
    elif planet.id == const.SATURN and sign == const.ARIES:
        return True
    elif planet.id == const.RAHU and sign == const.SCORPIO:
        return True
    elif planet.id == const.KETU and sign == const.TAURUS:
        return True
    
    return False


def is_in_friendly_sign(planet):
    """
    Check if a planet is in a friendly sign
    
    Args:
        planet (Object): The planet to check
    
    Returns:
        bool: True if the planet is in a friendly sign, False otherwise
    """
    # Get the planet's sign
    sign = planet.sign
    
    # Check if the planet is in a friendly sign
    if planet.id == const.SUN:
        return sign in [const.ARIES, const.SAGITTARIUS]
    elif planet.id == const.MOON:
        return sign in [const.TAURUS, const.PISCES]
    elif planet.id == const.MERCURY:
        return sign in [const.TAURUS, const.LIBRA]
    elif planet.id == const.VENUS:
        return sign in [const.GEMINI, const.CAPRICORN, const.AQUARIUS]
    elif planet.id == const.MARS:
        return sign in [const.LEO, const.SAGITTARIUS, const.CAPRICORN]
    elif planet.id == const.JUPITER:
        return sign in [const.ARIES, const.LEO]
    elif planet.id == const.SATURN:
        return sign in [const.GEMINI, const.VIRGO, const.LIBRA]
    
    return False


def is_in_enemy_sign(planet):
    """
    Check if a planet is in an enemy sign
    
    Args:
        planet (Object): The planet to check
    
    Returns:
        bool: True if the planet is in an enemy sign, False otherwise
    """
    # Get the planet's sign
    sign = planet.sign
    
    # Check if the planet is in an enemy sign
    if planet.id == const.SUN:
        return sign in [const.TAURUS, const.LIBRA, const.CAPRICORN, const.AQUARIUS]
    elif planet.id == const.MOON:
        return sign in [const.CAPRICORN, const.AQUARIUS]
    elif planet.id == const.MERCURY:
        return sign in [const.SAGITTARIUS, const.PISCES]
    elif planet.id == const.VENUS:
        return sign in [const.ARIES, const.SCORPIO]
    elif planet.id == const.MARS:
        return sign in [const.TAURUS, const.LIBRA]
    elif planet.id == const.JUPITER:
        return sign in [const.GEMINI, const.VIRGO, const.CAPRICORN, const.AQUARIUS]
    elif planet.id == const.SATURN:
        return sign in [const.ARIES, const.LEO, const.CANCER]
    
    return False


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


def get_house_number(chart, planet_id):
    """
    Get the house number of a planet
    
    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet
    
    Returns:
        int: The house number (1-12) of the planet
    """
    # Get the planet
    planet = chart.getObject(planet_id)
    
    # Get the Ascendant
    asc = chart.getAngle(const.ASC)
    
    # Calculate the house number
    house_num = 1 + int(angle.distance(planet.lon, asc.lon) / 30) % 12
    
    # Adjust for 0-based indexing
    if house_num == 0:
        house_num = 12
    
    return house_num


def are_planets_conjunct(chart, planet1_id, planet2_id, orb=10):
    """
    Check if two planets are conjunct
    
    Args:
        chart (Chart): The birth chart
        planet1_id (str): The ID of the first planet
        planet2_id (str): The ID of the second planet
        orb (float, optional): The maximum orb in degrees
    
    Returns:
        bool: True if the planets are conjunct, False otherwise
    """
    # Get the planets
    planet1 = chart.getObject(planet1_id)
    planet2 = chart.getObject(planet2_id)
    
    # Calculate the distance between the planets
    dist = abs(angle.closestdistance(planet1.lon, planet2.lon))
    
    # Check if the distance is within the orb
    return dist <= orb


def are_planets_in_aspect(chart, planet1_id, planet2_id, orb=10):
    """
    Check if two planets are in aspect
    
    Args:
        chart (Chart): The birth chart
        planet1_id (str): The ID of the first planet
        planet2_id (str): The ID of the second planet
        orb (float, optional): The maximum orb in degrees
    
    Returns:
        bool: True if the planets are in aspect, False otherwise
    """
    # Get the planets
    planet1 = chart.getObject(planet1_id)
    planet2 = chart.getObject(planet2_id)
    
    # Calculate the distance between the planets
    dist = angle.distance(planet1.lon, planet2.lon)
    
    # Check for aspects (conjunction, opposition, trine, square, sextile)
    aspects = [0, 60, 90, 120, 180]
    
    for aspect in aspects:
        if abs((dist - aspect) % 360) <= orb or abs((dist - aspect) % 360 - 360) <= orb:
            return True
    
    return False
