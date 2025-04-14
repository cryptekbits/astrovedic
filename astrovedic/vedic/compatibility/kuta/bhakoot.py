"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Bhakoot Kuta (sign compatibility)
    for Vedic astrology.
"""

from astrovedic import const
from astrovedic.chart import Chart


def get_bhakoot_kuta(chart1, chart2):
    """
    Calculate the Bhakoot Kuta (sign compatibility)
    
    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart
    
    Returns:
        dict: Dictionary with Bhakoot Kuta information
    """
    # Get the Moon signs
    moon1 = chart1.getObject(const.MOON)
    moon2 = chart2.getObject(const.MOON)
    
    # Get the sign numbers (1-12)
    sign_num1 = get_sign_number(moon1.sign)
    sign_num2 = get_sign_number(moon2.sign)
    
    # Calculate the house position
    house_position = calculate_house_position(sign_num1, sign_num2)
    
    # Calculate the score
    score = calculate_bhakoot_score(house_position)
    
    
    
    return {
        'sign1': moon1.sign,
        'sign2': moon2.sign,
        'house_position': house_position,
        'score': score,
        'max_score': 7,
        }


def get_sign_number(sign):
    """
    Get the sign number (1-12)
    
    Args:
        sign (str): The sign
    
    Returns:
        int: The sign number (1-12)
    """
    # Define the sign numbers
    sign_numbers = {
        const.ARIES: 1,
        const.TAURUS: 2,
        const.GEMINI: 3,
        const.CANCER: 4,
        const.LEO: 5,
        const.VIRGO: 6,
        const.LIBRA: 7,
        const.SCORPIO: 8,
        const.SAGITTARIUS: 9,
        const.CAPRICORN: 10,
        const.AQUARIUS: 11,
        const.PISCES: 12
    }
    
    return sign_numbers.get(sign, 0)


def calculate_house_position(sign_num1, sign_num2):
    """
    Calculate the house position
    
    Args:
        sign_num1 (int): The sign number of the first person (1-12)
        sign_num2 (int): The sign number of the second person (1-12)
    
    Returns:
        int: The house position (1-12)
    """
    # Calculate the house position
    house_position = (sign_num2 - sign_num1) % 12
    
    # If house_position is 0, it means it's the 12th house
    if house_position == 0:
        house_position = 12
    
    return house_position


def calculate_bhakoot_score(house_position):
    """
    Calculate the Bhakoot Kuta score
    
    Args:
        house_position (int): The house position (1-12)
    
    Returns:
        int: The Bhakoot Kuta score (0-7)
    """
    # Define the Bhakoot scores for each house position
    bhakoot_scores = {
        1: 7,  # 1st house - Excellent
        2: 0,  # 2nd house - Inauspicious
        3: 0,  # 3rd house - Inauspicious
        4: 0,  # 4th house - Inauspicious
        5: 0,  # 5th house - Inauspicious
        6: 0,  # 6th house - Inauspicious
        7: 7,  # 7th house - Excellent
        8: 0,  # 8th house - Inauspicious
        9: 0,  # 9th house - Inauspicious
        10: 0,  # 10th house - Inauspicious
        11: 0,  # 11th house - Inauspicious
        12: 0   # 12th house - Inauspicious
    }
    
    return bhakoot_scores.get(house_position, 0)



