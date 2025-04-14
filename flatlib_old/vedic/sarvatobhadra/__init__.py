"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Sarvatobhadra Chakra (all-auspicious wheel)
    calculations for Vedic astrology. It includes functions to analyze
    auspicious directions and Tara Bala (lunar strength).
"""

from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

from flatlib.vedic.sarvatobhadra.core import (
    get_sarvatobhadra_chakra, get_chakra_quality,
    get_auspicious_directions, get_inauspicious_directions
)

from flatlib.vedic.sarvatobhadra.chakra import (
    create_chakra, get_chakra_cell, get_chakra_row,
    get_chakra_column, get_chakra_diagonal
)

from flatlib.vedic.sarvatobhadra.directions import (
    get_direction_quality, get_best_direction,
    get_direction_for_activity, get_direction_compatibility
)

from flatlib.vedic.sarvatobhadra.tara import (
    get_tara_bala, get_janma_tara, get_sampath_tara,
    get_vipat_tara, get_kshema_tara, get_pratyak_tara,
    get_sadhaka_tara, get_vadha_tara, get_mitra_tara,
    get_ati_mitra_tara
)

from flatlib.vedic.sarvatobhadra.basic_analysis import (
    get_basic_sarvatobhadra_analysis
)

# Note: For detailed analysis, use the astroved_extension package

# Constants for directions
NORTH = 'North'
NORTHEAST = 'Northeast'
EAST = 'East'
SOUTHEAST = 'Southeast'
SOUTH = 'South'
SOUTHWEST = 'Southwest'
WEST = 'West'
NORTHWEST = 'Northwest'
CENTER = 'Center'

# List of directions
LIST_DIRECTIONS = [
    NORTH, NORTHEAST, EAST, SOUTHEAST,
    SOUTH, SOUTHWEST, WEST, NORTHWEST, CENTER
]

# Constants for Tara (lunar strength)
JANMA_TARA = 'Janma Tara'
SAMPATH_TARA = 'Sampath Tara'
VIPAT_TARA = 'Vipat Tara'
KSHEMA_TARA = 'Kshema Tara'
PRATYAK_TARA = 'Pratyak Tara'
SADHAKA_TARA = 'Sadhaka Tara'
VADHA_TARA = 'Vadha Tara'
MITRA_TARA = 'Mitra Tara'
ATI_MITRA_TARA = 'Ati Mitra Tara'

# List of Taras
LIST_TARAS = [
    JANMA_TARA, SAMPATH_TARA, VIPAT_TARA, KSHEMA_TARA,
    PRATYAK_TARA, SADHAKA_TARA, VADHA_TARA, MITRA_TARA, ATI_MITRA_TARA
]

# Constants for Tara quality
EXCELLENT = 'Excellent'
GOOD = 'Good'
NEUTRAL = 'Neutral'
INAUSPICIOUS = 'Inauspicious'
HIGHLY_INAUSPICIOUS = 'Highly Inauspicious'

# List of Tara quality levels
LIST_TARA_QUALITY = [
    EXCELLENT, GOOD, NEUTRAL, INAUSPICIOUS, HIGHLY_INAUSPICIOUS
]


def get_sarvatobhadra_for_date(date, location):
    """
    Get Sarvatobhadra Chakra information for a specific date
    Note: For detailed analysis, use the astroved_extension package

    Args:
        date (Datetime): The date and time
        location (GeoPos): The geographical location

    Returns:
        dict: Dictionary with basic Sarvatobhadra Chakra information
    """
    # Create a chart for the date
    chart = Chart(date, location, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)

    # Get basic Sarvatobhadra analysis
    analysis = get_basic_sarvatobhadra_analysis(chart)

    # Add the date to the result
    result = {'date': date}
    result.update(analysis)

    return result


def get_best_direction_for_activity(date, location, activity):
    """
    Get the best direction for a specific activity
    Note: For detailed analysis, use the astroved_extension package

    Args:
        date (Datetime): The date and time
        location (GeoPos): The geographical location
        activity (str): The type of activity

    Returns:
        dict: Dictionary with the best direction information
    """
    # Create a chart for the date
    chart = Chart(date, location, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)

    # Get the Sarvatobhadra Chakra
    chakra = get_sarvatobhadra_chakra(chart)

    # Get the best direction for the activity
    return get_direction_for_activity(chakra, activity)


def get_tara_bala_for_date(date, location):
    """
    Get Tara Bala (lunar strength) information for a specific date
    Note: For detailed analysis, use the astroved_extension package

    Args:
        date (Datetime): The date and time
        location (GeoPos): The geographical location

    Returns:
        dict: Dictionary with Tara Bala information
    """
    # Create a chart for the date
    chart = Chart(date, location, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)

    # Get Tara Bala
    return get_tara_bala(chart)
