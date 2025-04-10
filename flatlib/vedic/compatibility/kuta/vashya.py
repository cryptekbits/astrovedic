"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Vashya Kuta (dominance compatibility)
    for Vedic astrology.
"""

from flatlib import const
from flatlib.chart import Chart


def get_vashya_kuta(chart1, chart2):
    """
    Calculate the Vashya Kuta (dominance compatibility)
    
    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart
    
    Returns:
        dict: Dictionary with Vashya Kuta information
    """
    # Get the Moon signs
    moon1 = chart1.getObject(const.MOON)
    moon2 = chart2.getObject(const.MOON)
    
    # Get the Vashya categories for each Moon sign
    vashya1 = get_vashya_category(moon1.sign)
    vashya2 = get_vashya_category(moon2.sign)
    
    # Calculate the score
    score = calculate_vashya_score(vashya1, vashya2)
    
    # Generate the description
    description = generate_vashya_description(vashya1, vashya2, score)
    
    return {
        'vashya1': vashya1,
        'vashya2': vashya2,
        'score': score,
        'max_score': 2,
        'description': description
    }


def get_vashya_category(sign):
    """
    Get the Vashya category for a sign
    
    Args:
        sign (str): The sign
    
    Returns:
        str: The Vashya category
    """
    # Define the Vashya categories for each sign
    vashya_map = {
        const.ARIES: 'Chatushpad',  # Quadruped
        const.TAURUS: 'Chatushpad',  # Quadruped
        const.GEMINI: 'Manav',  # Human
        const.CANCER: 'Keet',  # Insect
        const.LEO: 'Chatushpad',  # Quadruped
        const.VIRGO: 'Manav',  # Human
        const.LIBRA: 'Manav',  # Human
        const.SCORPIO: 'Keet',  # Insect
        const.SAGITTARIUS: 'Chatushpad',  # Quadruped
        const.CAPRICORN: 'Jalachar',  # Aquatic
        const.AQUARIUS: 'Manav',  # Human
        const.PISCES: 'Jalachar'  # Aquatic
    }
    
    return vashya_map.get(sign, 'Unknown')


def calculate_vashya_score(vashya1, vashya2):
    """
    Calculate the Vashya Kuta score
    
    Args:
        vashya1 (str): The Vashya category of the first person
        vashya2 (str): The Vashya category of the second person
    
    Returns:
        int: The Vashya Kuta score (0-2)
    """
    # Define the Vashya compatibility matrix
    vashya_compatibility = {
        'Manav': {
            'Manav': 2,
            'Chatushpad': 1,
            'Jalachar': 0,
            'Keet': 0
        },
        'Chatushpad': {
            'Manav': 1,
            'Chatushpad': 2,
            'Jalachar': 0,
            'Keet': 0
        },
        'Jalachar': {
            'Manav': 0,
            'Chatushpad': 0,
            'Jalachar': 2,
            'Keet': 1
        },
        'Keet': {
            'Manav': 0,
            'Chatushpad': 0,
            'Jalachar': 1,
            'Keet': 2
        }
    }
    
    # Get the compatibility score
    return vashya_compatibility.get(vashya1, {}).get(vashya2, 0)


def generate_vashya_description(vashya1, vashya2, score):
    """
    Generate a description for the Vashya Kuta
    
    Args:
        vashya1 (str): The Vashya category of the first person
        vashya2 (str): The Vashya category of the second person
        score (int): The Vashya Kuta score
    
    Returns:
        str: The Vashya Kuta description
    """
    if score == 2:
        return f"Both individuals belong to the same Vashya category ({vashya1}), indicating excellent dominance compatibility."
    elif score == 1:
        return f"The individuals belong to compatible Vashya categories ({vashya1} and {vashya2}), indicating moderate dominance compatibility."
    else:
        return f"The individuals belong to incompatible Vashya categories ({vashya1} and {vashya2}), indicating potential dominance issues."
