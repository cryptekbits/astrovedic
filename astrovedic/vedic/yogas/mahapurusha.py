"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Pancha Mahapurusha Yogas (five great person yogas)
    for Vedic astrology.
"""

from astrovedic import const
from astrovedic.vedic.yogas.core import (
    is_in_own_sign, is_exalted, get_house_number,
    get_yoga_strength
)


def get_mahapurusha_yogas(chart):
    """
    Identify Pancha Mahapurusha Yogas in a chart
    
    Pancha Mahapurusha Yogas are formed when Mars, Mercury, Jupiter, Venus,
    or Saturn is in its own sign or exaltation and placed in a Kendra house
    (1, 4, 7, or 10).
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        list: List of Mahapurusha Yogas in the chart
    """
    # Initialize the result
    result = []
    
    # Check for Ruchaka Yoga (Mars)
    ruchaka = has_ruchaka_yoga(chart)
    if ruchaka:
        result.append(ruchaka)
    
    # Check for Bhadra Yoga (Mercury)
    bhadra = has_bhadra_yoga(chart)
    if bhadra:
        result.append(bhadra)
    
    # Check for Hamsa Yoga (Jupiter)
    hamsa = has_hamsa_yoga(chart)
    if hamsa:
        result.append(hamsa)
    
    # Check for Malavya Yoga (Venus)
    malavya = has_malavya_yoga(chart)
    if malavya:
        result.append(malavya)
    
    # Check for Sasa Yoga (Saturn)
    sasa = has_sasa_yoga(chart)
    if sasa:
        result.append(sasa)
    
    return result


def has_ruchaka_yoga(chart):
    """
    Check if a chart has Ruchaka Yoga
    
    Ruchaka Yoga is formed when Mars is in its own sign (Aries or Scorpio)
    or exaltation (Capricorn) and placed in a Kendra house (1, 4, 7, or 10).
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Ruchaka Yoga information, or None if not present
    """
    # Get Mars from the chart
    mars = chart.getObject(const.MARS)
    
    # Check if Mars is in its own sign or exaltation
    is_strong = is_in_own_sign(mars) or is_exalted(mars)
    
    # Check if Mars is in a Kendra house
    house_num = get_house_number(chart, const.MARS)
    is_in_kendra = house_num in [1, 4, 7, 10]
    
    # Check if Ruchaka Yoga is formed
    if is_strong and is_in_kendra:
        # Create the Yoga information
        yoga = {
            'name': 'Ruchaka Yoga',
            'type': 'Mahapurusha Yoga',
            'planets': [const.MARS],
            'houses': [house_num],
            'description': 'Formed when Mars is in its own sign or exaltation and placed in a Kendra house',
            'is_beneficial': True
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    return None


def has_bhadra_yoga(chart):
    """
    Check if a chart has Bhadra Yoga
    
    Bhadra Yoga is formed when Mercury is in its own sign (Gemini or Virgo)
    or exaltation (Virgo) and placed in a Kendra house (1, 4, 7, or 10).
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Bhadra Yoga information, or None if not present
    """
    # Get Mercury from the chart
    mercury = chart.getObject(const.MERCURY)
    
    # Check if Mercury is in its own sign or exaltation
    is_strong = is_in_own_sign(mercury) or is_exalted(mercury)
    
    # Check if Mercury is in a Kendra house
    house_num = get_house_number(chart, const.MERCURY)
    is_in_kendra = house_num in [1, 4, 7, 10]
    
    # Check if Bhadra Yoga is formed
    if is_strong and is_in_kendra:
        # Create the Yoga information
        yoga = {
            'name': 'Bhadra Yoga',
            'type': 'Mahapurusha Yoga',
            'planets': [const.MERCURY],
            'houses': [house_num],
            'description': 'Formed when Mercury is in its own sign or exaltation and placed in a Kendra house',
            'is_beneficial': True
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    return None


def has_hamsa_yoga(chart):
    """
    Check if a chart has Hamsa Yoga
    
    Hamsa Yoga is formed when Jupiter is in its own sign (Sagittarius or Pisces)
    or exaltation (Cancer) and placed in a Kendra house (1, 4, 7, or 10).
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Hamsa Yoga information, or None if not present
    """
    # Get Jupiter from the chart
    jupiter = chart.getObject(const.JUPITER)
    
    # Check if Jupiter is in its own sign or exaltation
    is_strong = is_in_own_sign(jupiter) or is_exalted(jupiter)
    
    # Check if Jupiter is in a Kendra house
    house_num = get_house_number(chart, const.JUPITER)
    is_in_kendra = house_num in [1, 4, 7, 10]
    
    # Check if Hamsa Yoga is formed
    if is_strong and is_in_kendra:
        # Create the Yoga information
        yoga = {
            'name': 'Hamsa Yoga',
            'type': 'Mahapurusha Yoga',
            'planets': [const.JUPITER],
            'houses': [house_num],
            'description': 'Formed when Jupiter is in its own sign or exaltation and placed in a Kendra house',
            'is_beneficial': True
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    return None


def has_malavya_yoga(chart):
    """
    Check if a chart has Malavya Yoga
    
    Malavya Yoga is formed when Venus is in its own sign (Taurus or Libra)
    or exaltation (Pisces) and placed in a Kendra house (1, 4, 7, or 10).
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Malavya Yoga information, or None if not present
    """
    # Get Venus from the chart
    venus = chart.getObject(const.VENUS)
    
    # Check if Venus is in its own sign or exaltation
    is_strong = is_in_own_sign(venus) or is_exalted(venus)
    
    # Check if Venus is in a Kendra house
    house_num = get_house_number(chart, const.VENUS)
    is_in_kendra = house_num in [1, 4, 7, 10]
    
    # Check if Malavya Yoga is formed
    if is_strong and is_in_kendra:
        # Create the Yoga information
        yoga = {
            'name': 'Malavya Yoga',
            'type': 'Mahapurusha Yoga',
            'planets': [const.VENUS],
            'houses': [house_num],
            'description': 'Formed when Venus is in its own sign or exaltation and placed in a Kendra house',
            'is_beneficial': True
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    return None


def has_sasa_yoga(chart):
    """
    Check if a chart has Sasa Yoga
    
    Sasa Yoga is formed when Saturn is in its own sign (Capricorn or Aquarius)
    or exaltation (Libra) and placed in a Kendra house (1, 4, 7, or 10).
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Sasa Yoga information, or None if not present
    """
    # Get Saturn from the chart
    saturn = chart.getObject(const.SATURN)
    
    # Check if Saturn is in its own sign or exaltation
    is_strong = is_in_own_sign(saturn) or is_exalted(saturn)
    
    # Check if Saturn is in a Kendra house
    house_num = get_house_number(chart, const.SATURN)
    is_in_kendra = house_num in [1, 4, 7, 10]
    
    # Check if Sasa Yoga is formed
    if is_strong and is_in_kendra:
        # Create the Yoga information
        yoga = {
            'name': 'Sasa Yoga',
            'type': 'Mahapurusha Yoga',
            'planets': [const.SATURN],
            'houses': [house_num],
            'description': 'Formed when Saturn is in its own sign or exaltation and placed in a Kendra house',
            'is_beneficial': True
        }
        
        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)
        
        return yoga
    
    return None
