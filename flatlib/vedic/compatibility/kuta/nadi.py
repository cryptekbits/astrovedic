"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Nadi Kuta (pulse compatibility)
    for Vedic astrology.
"""

from flatlib import const
from flatlib.chart import Chart
from flatlib.vedic.nakshatras import get_nakshatra


def get_nadi_kuta(chart1, chart2):
    """
    Calculate the Nadi Kuta (pulse compatibility)

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with Nadi Kuta information
    """
    # Get the Moon positions
    moon1 = chart1.getObject(const.MOON)
    moon2 = chart2.getObject(const.MOON)

    # Get the Nakshatras for each Moon
    nakshatra1 = get_nakshatra(moon1.lon)
    nakshatra2 = get_nakshatra(moon2.lon)

    # Get the Nadi (pulse) for each Nakshatra
    nadi1 = get_nadi(nakshatra1['name'])
    nadi2 = get_nadi(nakshatra2['name'])

    # Calculate the score
    score = calculate_nadi_score(nadi1, nadi2)

    # Generate the description
    description = generate_nadi_description(nadi1, nadi2, score)

    return {
        'nadi1': nadi1,
        'nadi2': nadi2,
        'score': score,
        'max_score': 8,
        'description': description
    }


def get_nadi(nakshatra):
    """
    Get the Nadi (pulse) for a Nakshatra

    Args:
        nakshatra (str): The Nakshatra name

    Returns:
        str: The Nadi (pulse)
    """
    # Define the Nadi for each Nakshatra
    nadi_map = {
        'Ashwini': 'Vata',
        'Bharani': 'Pitta',
        'Krittika': 'Kapha',
        'Rohini': 'Vata',
        'Mrigashira': 'Pitta',
        'Ardra': 'Kapha',
        'Punarvasu': 'Vata',
        'Pushya': 'Pitta',
        'Ashlesha': 'Kapha',
        'Magha': 'Vata',
        'Purva Phalguni': 'Pitta',
        'Uttara Phalguni': 'Kapha',
        'Hasta': 'Vata',
        'Chitra': 'Pitta',
        'Swati': 'Kapha',
        'Vishakha': 'Vata',
        'Anuradha': 'Pitta',
        'Jyeshtha': 'Kapha',
        'Mula': 'Vata',
        'Purva Ashadha': 'Pitta',
        'Uttara Ashadha': 'Kapha',
        'Shravana': 'Vata',
        'Dhanishta': 'Pitta',
        'Shatabhisha': 'Kapha',
        'Purva Bhadrapada': 'Vata',
        'Uttara Bhadrapada': 'Pitta',
        'Revati': 'Kapha'
    }

    return nadi_map.get(nakshatra, 'Unknown')


def calculate_nadi_score(nadi1, nadi2):
    """
    Calculate the Nadi Kuta score

    Args:
        nadi1 (str): The Nadi of the first person
        nadi2 (str): The Nadi of the second person

    Returns:
        int: The Nadi Kuta score (0 or 8)
    """
    # In Nadi Kuta, different Nadis are favorable
    if nadi1 != nadi2:
        return 8
    else:
        return 0


def generate_nadi_description(nadi1, nadi2, score):
    """
    Generate a description for the Nadi Kuta

    Args:
        nadi1 (str): The Nadi of the first person
        nadi2 (str): The Nadi of the second person
        score (int): The Nadi Kuta score

    Returns:
        str: The Nadi Kuta description
    """
    # Define the Nadi descriptions
    nadi_descriptions = {
        'Vata': 'air constitution (active, creative, and quick)',
        'Pitta': 'fire constitution (intense, intelligent, and determined)',
        'Kapha': 'water constitution (calm, stable, and nurturing)'
    }

    # Get the descriptions
    desc1 = nadi_descriptions.get(nadi1, 'unknown constitution')
    desc2 = nadi_descriptions.get(nadi2, 'unknown constitution')

    if score == 8:
        return f"The individuals have different Nadis ({nadi1} and {nadi2}), indicating excellent health compatibility. One has a {desc1}, while the other has a {desc2}, which creates a balanced relationship."
    else:
        return f"Both individuals have the same Nadi ({nadi1}), indicating potential health compatibility issues. They both have a {desc1}, which may lead to similar health problems and genetic incompatibility."
