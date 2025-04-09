"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Shadbala (six-fold planetary strength) calculations
    for Vedic astrology. It includes functions to calculate all six sources of
    planetary strength and their combined effects.
"""

from flatlib import const
from flatlib.chart import Chart
from flatlib.vedic.shadbala.core import (
    calculate_total_shadbala, get_shadbala_summary,
    get_strongest_planet, get_weakest_planet
)

# Import all strength calculation functions
from flatlib.vedic.shadbala.sthana_bala import calculate_sthana_bala
from flatlib.vedic.shadbala.dig_bala import calculate_dig_bala
from flatlib.vedic.shadbala.kala_bala import calculate_kala_bala
from flatlib.vedic.shadbala.cheshta_bala import calculate_cheshta_bala
from flatlib.vedic.shadbala.naisargika_bala import calculate_naisargika_bala
from flatlib.vedic.shadbala.drig_bala import calculate_drig_bala
from flatlib.vedic.shadbala.advanced import (
    calculate_ishta_phala, calculate_kashta_phala,
    calculate_vimsopaka_bala, calculate_bhava_bala
)

# Constants for Shadbala components
STHANA_BALA = 'Sthana Bala'  # Positional strength
DIG_BALA = 'Dig Bala'        # Directional strength
KALA_BALA = 'Kala Bala'      # Temporal strength
CHESHTA_BALA = 'Cheshta Bala'  # Motional strength
NAISARGIKA_BALA = 'Naisargika Bala'  # Natural strength
DRIG_BALA = 'Drig Bala'      # Aspectual strength

# List of all Shadbala components
LIST_SHADBALA_COMPONENTS = [
    STHANA_BALA, DIG_BALA, KALA_BALA, 
    CHESHTA_BALA, NAISARGIKA_BALA, DRIG_BALA
]

# Minimum required Shadbala for each planet (in Rupas)
MINIMUM_SHADBALA = {
    const.SUN: 5.0,
    const.MOON: 6.0,
    const.MERCURY: 7.0,
    const.VENUS: 5.5,
    const.MARS: 5.0,
    const.JUPITER: 6.5,
    const.SATURN: 5.0,
    const.RAHU: 5.0,
    const.KETU: 5.0
}


def get_shadbala(chart, planet_id):
    """
    Calculate Shadbala (six-fold strength) for a planet
    
    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet to analyze
    
    Returns:
        dict: Dictionary with Shadbala information
    """
    # Get the planet from the chart
    planet = chart.getObject(planet_id)
    
    # Calculate each component of Shadbala
    sthana_bala = calculate_sthana_bala(chart, planet_id)
    dig_bala = calculate_dig_bala(chart, planet_id)
    kala_bala = calculate_kala_bala(chart, planet_id)
    cheshta_bala = calculate_cheshta_bala(chart, planet_id)
    naisargika_bala = calculate_naisargika_bala(planet_id)
    drig_bala = calculate_drig_bala(chart, planet_id)
    
    # Calculate total Shadbala
    total_shadbala = calculate_total_shadbala(
        sthana_bala, dig_bala, kala_bala,
        cheshta_bala, naisargika_bala, drig_bala
    )
    
    # Calculate Ishta and Kashta Phala
    ishta_phala = calculate_ishta_phala(chart, planet_id, total_shadbala)
    kashta_phala = calculate_kashta_phala(chart, planet_id, total_shadbala)
    
    # Calculate Vimsopaka Bala
    vimsopaka_bala = calculate_vimsopaka_bala(chart, planet_id)
    
    # Check if the planet has sufficient strength
    minimum_required = MINIMUM_SHADBALA.get(planet_id, 5.0)
    is_sufficient = total_shadbala['total_rupas'] >= minimum_required
    
    return {
        'planet': planet_id,
        'sthana_bala': sthana_bala,
        'dig_bala': dig_bala,
        'kala_bala': kala_bala,
        'cheshta_bala': cheshta_bala,
        'naisargika_bala': naisargika_bala,
        'drig_bala': drig_bala,
        'total_shadbala': total_shadbala,
        'ishta_phala': ishta_phala,
        'kashta_phala': kashta_phala,
        'vimsopaka_bala': vimsopaka_bala,
        'minimum_required': minimum_required,
        'is_sufficient': is_sufficient
    }


def get_all_shadbala(chart):
    """
    Calculate Shadbala for all planets in the chart
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Shadbala information for all planets
    """
    shadbala_results = {}
    
    for planet_id in const.LIST_OBJECTS_VEDIC:
        shadbala_results[planet_id] = get_shadbala(chart, planet_id)
    
    # Add summary information
    shadbala_results['summary'] = get_shadbala_summary(shadbala_results)
    shadbala_results['strongest'] = get_strongest_planet(shadbala_results)
    shadbala_results['weakest'] = get_weakest_planet(shadbala_results)
    
    return shadbala_results


def get_bhava_bala(chart, house_id):
    """
    Calculate Bhava Bala (house strength) for a house
    
    Args:
        chart (Chart): The birth chart
        house_id (str): The ID of the house to analyze
    
    Returns:
        dict: Dictionary with Bhava Bala information
    """
    return calculate_bhava_bala(chart, house_id)
