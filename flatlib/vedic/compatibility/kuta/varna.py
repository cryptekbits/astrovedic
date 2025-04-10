"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Varna Kuta (caste/class compatibility)
    for Vedic astrology.
"""

from flatlib import const
from flatlib.chart import Chart


def get_varna_kuta(chart1, chart2):
    """
    Calculate the Varna Kuta (caste/class compatibility)
    
    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart
    
    Returns:
        dict: Dictionary with Varna Kuta information
    """
    # Get the Moon signs
    moon1 = chart1.getObject(const.MOON)
    moon2 = chart2.getObject(const.MOON)
    
    # Get the Varnas for each Moon sign
    varna1 = get_varna(moon1.sign)
    varna2 = get_varna(moon2.sign)
    
    # Calculate the score
    score = calculate_varna_score(varna1, varna2)
    
    # Generate the description
    description = generate_varna_description(varna1, varna2, score)
    
    return {
        'varna1': varna1,
        'varna2': varna2,
        'score': score,
        'max_score': 1,
        'description': description
    }


def get_varna(sign):
    """
    Get the Varna (caste/class) for a sign
    
    Args:
        sign (str): The sign
    
    Returns:
        str: The Varna
    """
    # Define the Varnas for each sign
    varna_map = {
        const.ARIES: 'Kshatriya',
        const.TAURUS: 'Vaishya',
        const.GEMINI: 'Shudra',
        const.CANCER: 'Brahmin',
        const.LEO: 'Kshatriya',
        const.VIRGO: 'Vaishya',
        const.LIBRA: 'Shudra',
        const.SCORPIO: 'Brahmin',
        const.SAGITTARIUS: 'Kshatriya',
        const.CAPRICORN: 'Vaishya',
        const.AQUARIUS: 'Shudra',
        const.PISCES: 'Brahmin'
    }
    
    return varna_map.get(sign, 'Unknown')


def calculate_varna_score(varna1, varna2):
    """
    Calculate the Varna Kuta score
    
    Args:
        varna1 (str): The Varna of the first person
        varna2 (str): The Varna of the second person
    
    Returns:
        int: The Varna Kuta score (0 or 1)
    """
    # Define the Varna hierarchy
    varna_hierarchy = {
        'Brahmin': 4,
        'Kshatriya': 3,
        'Vaishya': 2,
        'Shudra': 1
    }
    
    # Get the hierarchy values
    hierarchy1 = varna_hierarchy.get(varna1, 0)
    hierarchy2 = varna_hierarchy.get(varna2, 0)
    
    # In traditional Vedic astrology, the male's Varna should be higher or equal to the female's Varna
    # For a gender-neutral approach, we'll consider it favorable if the Varnas are equal or close
    if hierarchy1 == hierarchy2:
        return 1  # Equal Varnas
    elif abs(hierarchy1 - hierarchy2) == 1:
        return 0.5  # Adjacent Varnas
    else:
        return 0  # Distant Varnas


def generate_varna_description(varna1, varna2, score):
    """
    Generate a description for the Varna Kuta
    
    Args:
        varna1 (str): The Varna of the first person
        varna2 (str): The Varna of the second person
        score (float): The Varna Kuta score
    
    Returns:
        str: The Varna Kuta description
    """
    if score == 1:
        return f"Both individuals belong to the same Varna ({varna1}), indicating excellent social compatibility."
    elif score == 0.5:
        return f"The individuals belong to adjacent Varnas ({varna1} and {varna2}), indicating moderate social compatibility."
    else:
        return f"The individuals belong to distant Varnas ({varna1} and {varna2}), indicating potential social differences."
