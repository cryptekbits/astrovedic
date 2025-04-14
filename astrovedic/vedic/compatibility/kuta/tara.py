"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Tara Kuta (birth star compatibility)
    for Vedic astrology.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.vedic.nakshatras import get_nakshatra


def get_tara_kuta(chart1, chart2):
    """
    Calculate the Tara Kuta (birth star compatibility)

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with Tara Kuta information
    """
    # Get the Moon positions
    moon1 = chart1.getObject(const.MOON)
    moon2 = chart2.getObject(const.MOON)

    # Get the Nakshatras for each Moon
    nakshatra1 = get_nakshatra(moon1.lon)
    nakshatra2 = get_nakshatra(moon2.lon)

    # Get the Nakshatra numbers (1-27)
    nakshatra_num1 = nakshatra1['index'] + 1  # Convert from 0-based to 1-based
    nakshatra_num2 = nakshatra2['index'] + 1  # Convert from 0-based to 1-based

    # Calculate the Tara (birth star compatibility)
    tara = calculate_tara(nakshatra_num1, nakshatra_num2)

    # Calculate the score
    score = calculate_tara_score(tara)

    

    return {
        'nakshatra1': nakshatra1['name'],
        'nakshatra2': nakshatra2['name'],
        'tara': tara,
        'score': score,
        'max_score': 3,
        }


def calculate_tara(nakshatra_num1, nakshatra_num2):
    """
    Calculate the Tara (birth star compatibility)

    Args:
        nakshatra_num1 (int): The Nakshatra number of the first person (1-27)
        nakshatra_num2 (int): The Nakshatra number of the second person (1-27)

    Returns:
        int: The Tara (1-9)
    """
    # Calculate the count from nakshatra1 to nakshatra2
    count = (nakshatra_num2 - nakshatra_num1) % 27

    # If count is 0, it means both have the same nakshatra
    if count == 0:
        count = 27

    # Calculate the Tara (1-9)
    tara = count % 9

    # If tara is 0, it means it's the 9th Tara
    if tara == 0:
        tara = 9

    return tara


def calculate_tara_score(tara):
    """
    Calculate the Tara Kuta score

    Args:
        tara (int): The Tara (1-9)

    Returns:
        int: The Tara Kuta score (0-3)
    """
    # Define the Tara scores
    tara_scores = {
        1: 3,  # Janma (Birth) - Excellent
        2: 0,  # Sampat (Wealth) - Inauspicious
        3: 1,  # Vipat (Danger) - Good
        4: 2,  # Kshema (Well-being) - Excellent
        5: 3,  # Pratyak (Obstacle) - Inauspicious
        6: 0,  # Sadhaka (Achievement) - Good
        7: 1,  # Vadha (Destruction) - Inauspicious
        8: 2,  # Mitra (Friend) - Excellent
        9: 3   # Ati-Mitra (Best Friend) - Excellent
    }

    return tara_scores.get(tara, 0)




    # Get the Tara information
    tara_name = tara_info.get(tara, {}).get('name', 'Unknown')
    tara_desc = tara_info.get(tara, {}).get('description', '')

    # Generate the description
    if score == 3:
        return f"The Tara is {tara_name}, which is excellent. {tara_desc}"
    elif score == 2:
        return f"The Tara is {tara_name}, which is good. {tara_desc}"
    elif score == 1:
        return f"The Tara is {tara_name}, which is moderate. {tara_desc}"
    else:
        return f"The Tara is {tara_name}, which is challenging. {tara_desc}"
