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
from flatlib.vedic.shadbala.kala_bala import calculate_kala_bala, calculate_yuddha_bala, calculate_ayana_bala, calculate_paksha_bala
from flatlib.vedic.shadbala.cheshta_bala import calculate_cheshta_bala
from flatlib.vedic.shadbala.naisargika_bala import calculate_naisargika_bala
from flatlib.vedic.shadbala.drig_bala import calculate_drig_bala
from flatlib.vedic.shadbala.advanced import (
    calculate_ishta_phala, calculate_kashta_phala,
    calculate_vimsopaka_bala, calculate_bhava_bala
)
from flatlib.vedic.shadbala.basic_analysis import (
    get_basic_shadbala_analysis
)

# Note: For detailed analysis, use the astroved_extension package

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

    # Calculate Yuddha Bala (planetary war) separately
    # This is now a correction applied after summing the six main components
    yuddha_bala = calculate_yuddha_bala(chart, planet_id)

    # Calculate total Shadbala
    total_shadbala = calculate_total_shadbala(
        sthana_bala, dig_bala, kala_bala,
        cheshta_bala, naisargika_bala, drig_bala
    )

    # Apply the Yuddha Bala correction to the total
    yuddha_correction = yuddha_bala.get('correction', 0.0)

    # Update the total values with the Yuddha Bala correction
    corrected_total_virupas = total_shadbala['total_virupas'] + yuddha_correction
    corrected_total_rupas = corrected_total_virupas / 60.0

    # Update the total Shadbala dictionary
    total_shadbala['yuddha_correction'] = yuddha_correction
    total_shadbala['total_virupas_before_correction'] = total_shadbala['total_virupas']
    total_shadbala['total_rupas_before_correction'] = total_shadbala['total_rupas']
    total_shadbala['total_virupas'] = corrected_total_virupas
    total_shadbala['total_rupas'] = corrected_total_rupas

    # Calculate the relative strength (percentage of minimum required strength)
    # This is a more meaningful metric than the previous fixed maximum approach
    minimum_required = MINIMUM_SHADBALA.get(planet_id, 5.0)
    relative_strength = (corrected_total_rupas / minimum_required) * 100.0 if minimum_required > 0 else 0.0
    total_shadbala['relative_strength'] = relative_strength

    # Calculate Ishta and Kashta Phala
    uchcha_bala_value = sthana_bala['uchcha_bala']['value']

    # Determine the correct 'Cheshta Bala' value for Ishta/Kashta formula
    # Use full Ayana Bala for Sun, full Paksha Bala for Moon
    if planet_id == const.SUN:
        ayana_bala_value = calculate_ayana_bala(chart, planet_id)['value'] # Re-calc needed if not already stored
        cheshta_bala_for_phala = ayana_bala_value
    elif planet_id == const.MOON:
        paksha_bala_value = calculate_paksha_bala(chart, planet_id)['value'] # Re-calc needed if not already stored
        cheshta_bala_for_phala = paksha_bala_value
    else:
        # For other planets, use the calculated Cheshta Bala value
        cheshta_bala_for_phala = cheshta_bala['value']

    # Handle cases where Cheshta Bala might not be calculated (e.g., Rahu/Ketu in current cheshta_bala.py)
    # or if Ayana/Paksha are needed but not calculated yet (should be part of kala_bala)
    # For safety, default to 0 if the value is unexpectedly missing or invalid
    if not isinstance(cheshta_bala_for_phala, (int, float)) or not (0 <= cheshta_bala_for_phala <= 60):
         # Add logging here? print(f"Warning: Invalid Cheshta Bala {cheshta_bala_for_phala} for {planet_id}, using 0 for Ishta/Kashta.")
         cheshta_bala_for_phala = 0.0

    # Ensure Uchcha Bala is valid too
    if not isinstance(uchcha_bala_value, (int, float)) or not (0 <= uchcha_bala_value <= 60):
        # Add logging here? print(f"Warning: Invalid Uchcha Bala {uchcha_bala_value} for {planet_id}, using 0 for Ishta/Kashta.")
        uchcha_bala_value = 0.0

    try:
        ishta_phala = calculate_ishta_phala(uchcha_bala_value, cheshta_bala_for_phala)
        kashta_phala = calculate_kashta_phala(uchcha_bala_value, cheshta_bala_for_phala)
    except ValueError as e:
        # Handle potential validation errors from the functions themselves
        # print(f"Error calculating Ishta/Kashta for {planet_id}: {e}")
        ishta_phala = {'value': 0.0, 'description': 'Calculation Error'}
        kashta_phala = {'value': 0.0, 'description': 'Calculation Error'}

    # Calculate Vimsopaka Bala
    vimsopaka_bala = calculate_vimsopaka_bala(chart, planet_id)

    # Check if the planet has sufficient strength
    minimum_required = MINIMUM_SHADBALA.get(planet_id, 5.0)
    is_sufficient = total_shadbala['total_rupas'] >= minimum_required

    return {
        'planet': planet_id,
        'sthana_bala': sthana_bala.get('total', 0),
        'dig_bala': dig_bala.get('value', 0),
        'kala_bala': kala_bala.get('total', 0),
        'cheshta_bala': cheshta_bala.get('value', 0),
        'naisargika_bala': naisargika_bala.get('value', 0),
        'drig_bala': drig_bala.get('value', 0),
        'yuddha_bala': yuddha_bala,  # Include the full Yuddha Bala information
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


def get_shadbala_analysis(chart):
    """
    Analyze Shadbala data for a chart
    Note: For detailed analysis, use the astroved_extension package

    Args:
        chart (Chart): The birth chart

    Returns:
        dict: Dictionary with basic Shadbala analysis
    """
    # Get all Shadbala data
    shadbala_data = get_all_shadbala(chart)

    # Get basic analysis
    analysis = get_basic_shadbala_analysis(shadbala_data)

    return analysis


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


def get_planet_strength(chart, planet_id):
    """
    Get the strength of a planet in a chart

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet to analyze

    Returns:
        float: The strength of the planet (0-100)
    """
    # Get the Shadbala data for the planet
    shadbala = get_shadbala(chart, planet_id)

    # Calculate the strength as a percentage of the minimum required strength
    minimum_required = shadbala['minimum_required']
    total_rupas = shadbala['total_shadbala']['total_rupas']

    # Calculate the strength as a percentage (0-100)
    strength = min(100, (total_rupas / minimum_required) * 100)

    return strength


def get_house_strength(chart, house_num):
    """
    Get the strength of a house in a chart

    Args:
        chart (Chart): The birth chart
        house_num (int): The house number (1-12)

    Returns:
        float: The strength of the house (0-100)
    """
    # Get the Bhava Bala data for the house
    bhava_bala = get_bhava_bala(chart, house_num)

    # Calculate the strength as a percentage (0-100)
    strength = min(100, bhava_bala['total_bhava_bala'] / 30 * 100)

    return strength
