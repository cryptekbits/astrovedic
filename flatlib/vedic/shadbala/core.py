"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements core functionality for Shadbala (six-fold planetary strength)
    calculations in Vedic astrology.
"""

from flatlib import const


def calculate_total_shadbala(sthana_bala, dig_bala, kala_bala, 
                            cheshta_bala, naisargika_bala, drig_bala):
    """
    Calculate the total Shadbala (six-fold strength) for a planet
    
    Args:
        sthana_bala (dict): Sthana Bala (positional strength) information
        dig_bala (dict): Dig Bala (directional strength) information
        kala_bala (dict): Kala Bala (temporal strength) information
        cheshta_bala (dict): Cheshta Bala (motional strength) information
        naisargika_bala (dict): Naisargika Bala (natural strength) information
        drig_bala (dict): Drig Bala (aspectual strength) information
    
    Returns:
        dict: Dictionary with total Shadbala information
    """
    # Get the total values from each component
    sthana_total = sthana_bala['total']
    dig_total = dig_bala['total']
    kala_total = kala_bala['total']
    cheshta_total = cheshta_bala['total']
    naisargika_total = naisargika_bala['total']
    drig_total = drig_bala['total']
    
    # Calculate the total Shadbala
    total = sthana_total + dig_total + kala_total + cheshta_total + naisargika_total + drig_total
    
    # Convert to Rupas (1 Rupa = 60 Virupas)
    total_rupas = total / 60.0
    
    # Calculate the relative strength (percentage of total possible strength)
    # The maximum possible Shadbala varies by planet, but we'll use a simplified approach
    max_possible = 600.0  # This is an approximation
    relative_strength = (total / max_possible) * 100.0
    
    return {
        'sthana_total': sthana_total,
        'dig_total': dig_total,
        'kala_total': kala_total,
        'cheshta_total': cheshta_total,
        'naisargika_total': naisargika_total,
        'drig_total': drig_total,
        'total_virupas': total,
        'total_rupas': total_rupas,
        'relative_strength': relative_strength
    }


def get_shadbala_summary(shadbala_results):
    """
    Get a summary of Shadbala results for all planets
    
    Args:
        shadbala_results (dict): Dictionary with Shadbala results for all planets
    
    Returns:
        dict: Dictionary with summary information
    """
    # Calculate average Shadbala
    total_rupas = 0.0
    count = 0
    
    for planet_id, result in shadbala_results.items():
        if planet_id in const.LIST_OBJECTS_VEDIC:
            total_rupas += result['total_shadbala']['total_rupas']
            count += 1
    
    average_rupas = total_rupas / count if count > 0 else 0.0
    
    # Count planets with sufficient strength
    sufficient_count = 0
    for planet_id, result in shadbala_results.items():
        if planet_id in const.LIST_OBJECTS_VEDIC and result['is_sufficient']:
            sufficient_count += 1
    
    return {
        'average_rupas': average_rupas,
        'sufficient_count': sufficient_count,
        'total_planets': count
    }


def get_strongest_planet(shadbala_results):
    """
    Get the strongest planet based on Shadbala
    
    Args:
        shadbala_results (dict): Dictionary with Shadbala results for all planets
    
    Returns:
        str: The ID of the strongest planet
    """
    strongest_planet = None
    max_strength = -1.0
    
    for planet_id, result in shadbala_results.items():
        if planet_id in const.LIST_OBJECTS_VEDIC:
            strength = result['total_shadbala']['total_rupas']
            if strength > max_strength:
                max_strength = strength
                strongest_planet = planet_id
    
    return strongest_planet


def get_weakest_planet(shadbala_results):
    """
    Get the weakest planet based on Shadbala
    
    Args:
        shadbala_results (dict): Dictionary with Shadbala results for all planets
    
    Returns:
        str: The ID of the weakest planet
    """
    weakest_planet = None
    min_strength = float('inf')
    
    for planet_id, result in shadbala_results.items():
        if planet_id in const.LIST_OBJECTS_VEDIC:
            strength = result['total_shadbala']['total_rupas']
            if strength < min_strength:
                min_strength = strength
                weakest_planet = planet_id
    
    return weakest_planet
