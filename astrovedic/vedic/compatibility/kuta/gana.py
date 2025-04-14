"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Gana Kuta (temperament compatibility)
    for Vedic astrology.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.vedic.nakshatras import get_nakshatra


def get_gana_kuta(chart1, chart2):
    """
    Calculate the Gana Kuta (temperament compatibility)

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with Gana Kuta information
    """
    # Get the Moon positions
    moon1 = chart1.getObject(const.MOON)
    moon2 = chart2.getObject(const.MOON)

    # Get the Nakshatras for each Moon
    nakshatra1 = get_nakshatra(moon1.lon)
    nakshatra2 = get_nakshatra(moon2.lon)

    # Get the Gana (temperament) for each Nakshatra
    gana1 = get_gana(nakshatra1['name'])
    gana2 = get_gana(nakshatra2['name'])

    # Calculate the score
    score = calculate_gana_score(gana1, gana2)

    

    return {
        'gana1': gana1,
        'gana2': gana2,
        'score': score,
        'max_score': 6,
        }


def get_gana(nakshatra):
    """
    Get the Gana (temperament) for a Nakshatra

    Args:
        nakshatra (str): The Nakshatra name

    Returns:
        str: The Gana (temperament)
    """
    # Define the Gana for each Nakshatra
    gana_map = {
        'Ashwini': 'Deva',
        'Bharani': 'Manushya',
        'Krittika': 'Rakshasa',
        'Rohini': 'Manushya',
        'Mrigashira': 'Deva',
        'Ardra': 'Manushya',
        'Punarvasu': 'Deva',
        'Pushya': 'Deva',
        'Ashlesha': 'Rakshasa',
        'Magha': 'Rakshasa',
        'Purva Phalguni': 'Manushya',
        'Uttara Phalguni': 'Manushya',
        'Hasta': 'Deva',
        'Chitra': 'Rakshasa',
        'Swati': 'Deva',
        'Vishakha': 'Rakshasa',
        'Anuradha': 'Deva',
        'Jyeshtha': 'Rakshasa',
        'Mula': 'Rakshasa',
        'Purva Ashadha': 'Manushya',
        'Uttara Ashadha': 'Manushya',
        'Shravana': 'Deva',
        'Dhanishta': 'Rakshasa',
        'Shatabhisha': 'Rakshasa',
        'Purva Bhadrapada': 'Manushya',
        'Uttara Bhadrapada': 'Manushya',
        'Revati': 'Deva'
    }

    return gana_map.get(nakshatra, 'Unknown')


def calculate_gana_score(gana1, gana2):
    """
    Calculate the Gana Kuta score

    Args:
        gana1 (str): The Gana of the first person
        gana2 (str): The Gana of the second person

    Returns:
        int: The Gana Kuta score (0-6)
    """
    # Define the Gana compatibility matrix
    gana_compatibility = {
        'Deva': {
            'Deva': 6,
            'Manushya': 5,
            'Rakshasa': 0
        },
        'Manushya': {
            'Deva': 5,
            'Manushya': 6,
            'Rakshasa': 1
        },
        'Rakshasa': {
            'Deva': 0,
            'Manushya': 1,
            'Rakshasa': 6
        }
    }

    # Get the compatibility score
    return gana_compatibility.get(gana1, {}).get(gana2, 0)




    # Get the descriptions
    desc1 = gana_descriptions.get(gana1, 'unknown nature')
    desc2 = gana_descriptions.get(gana2, 'unknown nature')

    if score == 6:
        return f"Both individuals belong to the same Gana ({gana1}), indicating excellent temperamental compatibility. They share a {desc1}."
    elif score == 5:
        return f"The Ganas ({gana1} and {gana2}) are highly compatible, indicating good temperamental harmony. One has a {desc1}, while the other has a {desc2}."
    elif score == 1:
        return f"The Ganas ({gana1} and {gana2}) have low compatibility, indicating potential temperamental differences. One has a {desc1}, while the other has a {desc2}."
    else:
        return f"The Ganas ({gana1} and {gana2}) are incompatible, indicating significant temperamental differences. One has a {desc1}, while the other has a {desc2}."
