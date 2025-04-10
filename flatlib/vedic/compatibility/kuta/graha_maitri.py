"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Graha Maitri Kuta (planetary friendship compatibility)
    for Vedic astrology.
"""

from flatlib import const
from flatlib.chart import Chart


def get_graha_maitri_kuta(chart1, chart2):
    """
    Calculate the Graha Maitri Kuta (planetary friendship compatibility)
    
    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart
    
    Returns:
        dict: Dictionary with Graha Maitri Kuta information
    """
    # Get the Moon signs
    moon1 = chart1.getObject(const.MOON)
    moon2 = chart2.getObject(const.MOON)
    
    # Get the lords of the Moon signs
    lord1 = get_sign_lord(moon1.sign)
    lord2 = get_sign_lord(moon2.sign)
    
    # Calculate the friendship between the lords
    friendship = get_planetary_friendship(lord1, lord2)
    
    # Calculate the score
    score = calculate_graha_maitri_score(friendship)
    
    # Generate the description
    description = generate_graha_maitri_description(lord1, lord2, friendship, score)
    
    return {
        'lord1': lord1,
        'lord2': lord2,
        'friendship': friendship,
        'score': score,
        'max_score': 5,
        'description': description
    }


def get_sign_lord(sign):
    """
    Get the lord (ruling planet) of a sign
    
    Args:
        sign (str): The sign
    
    Returns:
        str: The lord (ruling planet)
    """
    # Define the lords for each sign
    lord_map = {
        const.ARIES: const.MARS,
        const.TAURUS: const.VENUS,
        const.GEMINI: const.MERCURY,
        const.CANCER: const.MOON,
        const.LEO: const.SUN,
        const.VIRGO: const.MERCURY,
        const.LIBRA: const.VENUS,
        const.SCORPIO: const.MARS,
        const.SAGITTARIUS: const.JUPITER,
        const.CAPRICORN: const.SATURN,
        const.AQUARIUS: const.SATURN,
        const.PISCES: const.JUPITER
    }
    
    return lord_map.get(sign, 'Unknown')


def get_planetary_friendship(planet1, planet2):
    """
    Get the friendship between two planets
    
    Args:
        planet1 (str): The first planet
        planet2 (str): The second planet
    
    Returns:
        str: The friendship type
    """
    # Define the planetary friendships
    friendship_map = {
        const.SUN: {
            const.SUN: 'Friend',
            const.MOON: 'Friend',
            const.MARS: 'Friend',
            const.MERCURY: 'Enemy',
            const.JUPITER: 'Friend',
            const.VENUS: 'Enemy',
            const.SATURN: 'Enemy'
        },
        const.MOON: {
            const.SUN: 'Friend',
            const.MOON: 'Friend',
            const.MARS: 'Neutral',
            const.MERCURY: 'Friend',
            const.JUPITER: 'Friend',
            const.VENUS: 'Neutral',
            const.SATURN: 'Neutral'
        },
        const.MARS: {
            const.SUN: 'Friend',
            const.MOON: 'Friend',
            const.MARS: 'Friend',
            const.MERCURY: 'Neutral',
            const.JUPITER: 'Friend',
            const.VENUS: 'Enemy',
            const.SATURN: 'Enemy'
        },
        const.MERCURY: {
            const.SUN: 'Neutral',
            const.MOON: 'Friend',
            const.MARS: 'Neutral',
            const.MERCURY: 'Friend',
            const.JUPITER: 'Neutral',
            const.VENUS: 'Friend',
            const.SATURN: 'Friend'
        },
        const.JUPITER: {
            const.SUN: 'Friend',
            const.MOON: 'Friend',
            const.MARS: 'Friend',
            const.MERCURY: 'Enemy',
            const.JUPITER: 'Friend',
            const.VENUS: 'Enemy',
            const.SATURN: 'Enemy'
        },
        const.VENUS: {
            const.SUN: 'Enemy',
            const.MOON: 'Neutral',
            const.MARS: 'Neutral',
            const.MERCURY: 'Friend',
            const.JUPITER: 'Neutral',
            const.VENUS: 'Friend',
            const.SATURN: 'Friend'
        },
        const.SATURN: {
            const.SUN: 'Enemy',
            const.MOON: 'Enemy',
            const.MARS: 'Enemy',
            const.MERCURY: 'Friend',
            const.JUPITER: 'Enemy',
            const.VENUS: 'Friend',
            const.SATURN: 'Friend'
        }
    }
    
    # Get the friendship
    return friendship_map.get(planet1, {}).get(planet2, 'Unknown')


def calculate_graha_maitri_score(friendship):
    """
    Calculate the Graha Maitri Kuta score
    
    Args:
        friendship (str): The friendship type
    
    Returns:
        int: The Graha Maitri Kuta score (0-5)
    """
    # Define the scores for each friendship type
    friendship_scores = {
        'Friend': 5,
        'Neutral': 3,
        'Enemy': 0,
        'Unknown': 0
    }
    
    return friendship_scores.get(friendship, 0)


def generate_graha_maitri_description(lord1, lord2, friendship, score):
    """
    Generate a description for the Graha Maitri Kuta
    
    Args:
        lord1 (str): The lord of the first person's Moon sign
        lord2 (str): The lord of the second person's Moon sign
        friendship (str): The friendship type
        score (int): The Graha Maitri Kuta score
    
    Returns:
        str: The Graha Maitri Kuta description
    """
    if friendship == 'Friend':
        return f"The lords of the Moon signs ({lord1} and {lord2}) are friends, indicating excellent planetary compatibility and mutual understanding."
    elif friendship == 'Neutral':
        return f"The lords of the Moon signs ({lord1} and {lord2}) are neutral to each other, indicating moderate planetary compatibility."
    elif friendship == 'Enemy':
        return f"The lords of the Moon signs ({lord1} and {lord2}) are enemies, indicating potential conflicts and misunderstandings."
    else:
        return f"The relationship between the lords of the Moon signs ({lord1} and {lord2}) is unknown."
