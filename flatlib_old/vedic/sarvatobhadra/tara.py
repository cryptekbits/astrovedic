"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Tara Bala (lunar strength) calculations
    for Vedic astrology.
"""

from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

# Import Panchanga functions
from flatlib.vedic.muhurta.panchanga import get_panchanga


def get_tara_bala(chart):
    """
    Calculate the Tara Bala (lunar strength) for a chart
    
    Args:
        chart (Chart): The chart
    
    Returns:
        dict: Dictionary with Tara Bala information
    """
    # Get the Panchanga
    panchanga = get_panchanga(chart)
    
    # Get the Nakshatra
    nakshatra = panchanga['nakshatra']
    
    # Get the birth nakshatra (Janma Tara)
    janma_tara = nakshatra['num']
    
    # Calculate the other Taras
    sampath_tara = get_sampath_tara(janma_tara)
    vipat_tara = get_vipat_tara(janma_tara)
    kshema_tara = get_kshema_tara(janma_tara)
    pratyak_tara = get_pratyak_tara(janma_tara)
    sadhaka_tara = get_sadhaka_tara(janma_tara)
    vadha_tara = get_vadha_tara(janma_tara)
    mitra_tara = get_mitra_tara(janma_tara)
    ati_mitra_tara = get_ati_mitra_tara(janma_tara)
    
    # Determine the current Tara
    current_tara = get_current_tara(janma_tara, nakshatra['num'])
    
    # Calculate the Tara Bala score
    score = get_tara_bala_score(current_tara)
    
    return {
        'janma_tara': janma_tara,
        'sampath_tara': sampath_tara,
        'vipat_tara': vipat_tara,
        'kshema_tara': kshema_tara,
        'pratyak_tara': pratyak_tara,
        'sadhaka_tara': sadhaka_tara,
        'vadha_tara': vadha_tara,
        'mitra_tara': mitra_tara,
        'ati_mitra_tara': ati_mitra_tara,
        'current_tara': current_tara,
        'score': score
    }


def get_janma_tara(janma_nakshatra):
    """
    Get the Janma Tara (birth star)
    
    Args:
        janma_nakshatra (int): The birth nakshatra number (1-27)
    
    Returns:
        int: The Janma Tara nakshatra number (1-27)
    """
    return janma_nakshatra


def get_sampath_tara(janma_nakshatra):
    """
    Get the Sampath Tara (wealth star)
    
    Args:
        janma_nakshatra (int): The birth nakshatra number (1-27)
    
    Returns:
        int: The Sampath Tara nakshatra number (1-27)
    """
    return ((janma_nakshatra + 5 - 1) % 27) + 1


def get_vipat_tara(janma_nakshatra):
    """
    Get the Vipat Tara (danger star)
    
    Args:
        janma_nakshatra (int): The birth nakshatra number (1-27)
    
    Returns:
        int: The Vipat Tara nakshatra number (1-27)
    """
    return ((janma_nakshatra + 10 - 1) % 27) + 1


def get_kshema_tara(janma_nakshatra):
    """
    Get the Kshema Tara (well-being star)
    
    Args:
        janma_nakshatra (int): The birth nakshatra number (1-27)
    
    Returns:
        int: The Kshema Tara nakshatra number (1-27)
    """
    return ((janma_nakshatra + 15 - 1) % 27) + 1


def get_pratyak_tara(janma_nakshatra):
    """
    Get the Pratyak Tara (obstacle star)
    
    Args:
        janma_nakshatra (int): The birth nakshatra number (1-27)
    
    Returns:
        int: The Pratyak Tara nakshatra number (1-27)
    """
    return ((janma_nakshatra + 20 - 1) % 27) + 1


def get_sadhaka_tara(janma_nakshatra):
    """
    Get the Sadhaka Tara (accomplishment star)
    
    Args:
        janma_nakshatra (int): The birth nakshatra number (1-27)
    
    Returns:
        int: The Sadhaka Tara nakshatra number (1-27)
    """
    return ((janma_nakshatra + 25 - 1) % 27) + 1


def get_vadha_tara(janma_nakshatra):
    """
    Get the Vadha Tara (obstruction star)
    
    Args:
        janma_nakshatra (int): The birth nakshatra number (1-27)
    
    Returns:
        int: The Vadha Tara nakshatra number (1-27)
    """
    return ((janma_nakshatra + 3 - 1) % 27) + 1


def get_mitra_tara(janma_nakshatra):
    """
    Get the Mitra Tara (friendly star)
    
    Args:
        janma_nakshatra (int): The birth nakshatra number (1-27)
    
    Returns:
        int: The Mitra Tara nakshatra number (1-27)
    """
    return ((janma_nakshatra + 8 - 1) % 27) + 1


def get_ati_mitra_tara(janma_nakshatra):
    """
    Get the Ati Mitra Tara (very friendly star)
    
    Args:
        janma_nakshatra (int): The birth nakshatra number (1-27)
    
    Returns:
        int: The Ati Mitra Tara nakshatra number (1-27)
    """
    return ((janma_nakshatra + 13 - 1) % 27) + 1


def get_current_tara(janma_nakshatra, current_nakshatra):
    """
    Get the current Tara based on the birth nakshatra and current nakshatra
    
    Args:
        janma_nakshatra (int): The birth nakshatra number (1-27)
        current_nakshatra (int): The current nakshatra number (1-27)
    
    Returns:
        str: The name of the current Tara
    """
    # Calculate the count from birth nakshatra to current nakshatra
    count = (current_nakshatra - janma_nakshatra) % 9
    if count == 0:
        count = 9
    
    # Determine the Tara based on the count
    tara_names = {
        1: 'Janma Tara',
        2: 'Sampath Tara',
        3: 'Vipat Tara',
        4: 'Kshema Tara',
        5: 'Pratyak Tara',
        6: 'Sadhaka Tara',
        7: 'Vadha Tara',
        8: 'Mitra Tara',
        9: 'Ati Mitra Tara'
    }
    
    return tara_names.get(count, '')


def get_tara_bala_score(tara_name):
    """
    Calculate the Tara Bala score based on the Tara name
    
    Args:
        tara_name (str): The name of the Tara
    
    Returns:
        float: The Tara Bala score (0-100)
    """
    # Assign scores to each Tara
    tara_scores = {
        'Janma Tara': 60,
        'Sampath Tara': 100,
        'Vipat Tara': 20,
        'Kshema Tara': 80,
        'Pratyak Tara': 40,
        'Sadhaka Tara': 90,
        'Vadha Tara': 10,
        'Mitra Tara': 70,
        'Ati Mitra Tara': 50
    }
    
    return tara_scores.get(tara_name, 0)


def is_tara_favorable(tara_name):
    """
    Check if a Tara is favorable
    
    Args:
        tara_name (str): The name of the Tara
    
    Returns:
        bool: True if the Tara is favorable, False otherwise
    """
    # Favorable Taras
    favorable_taras = ['Sampath Tara', 'Kshema Tara', 'Sadhaka Tara', 'Mitra Tara', 'Ati Mitra Tara']
    
    return tara_name in favorable_taras


def is_tara_unfavorable(tara_name):
    """
    Check if a Tara is unfavorable
    
    Args:
        tara_name (str): The name of the Tara
    
    Returns:
        bool: True if the Tara is unfavorable, False otherwise
    """
    # Unfavorable Taras
    unfavorable_taras = ['Vipat Tara', 'Pratyak Tara', 'Vadha Tara']
    
    return tara_name in unfavorable_taras


def get_tara_description(tara_name):
    """
    Get the description of a Tara
    
    Args:
        tara_name (str): The name of the Tara
    
    Returns:
        str: The description of the Tara
    """
    # Descriptions of each Tara
    tara_descriptions = {
        'Janma Tara': 'Birth star - Neutral, but can be good for activities related to birth and beginnings.',
        'Sampath Tara': 'Wealth star - Excellent for financial activities, prosperity, and success.',
        'Vipat Tara': 'Danger star - Unfavorable for most activities, may bring obstacles and dangers.',
        'Kshema Tara': 'Well-being star - Very good for health, peace, and general well-being.',
        'Pratyak Tara': 'Obstacle star - Unfavorable, may bring hindrances and delays.',
        'Sadhaka Tara': 'Accomplishment star - Excellent for achievements, success, and spiritual practices.',
        'Vadha Tara': 'Obstruction star - Highly unfavorable, may bring serious obstacles and failures.',
        'Mitra Tara': 'Friendly star - Good for relationships, partnerships, and social activities.',
        'Ati Mitra Tara': 'Very friendly star - Moderately good for relationships and cooperative ventures.'
    }
    
    return tara_descriptions.get(tara_name, '')
