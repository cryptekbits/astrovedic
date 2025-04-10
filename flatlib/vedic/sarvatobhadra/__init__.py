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

from flatlib.vedic.sarvatobhadra.analysis import (
    analyze_sarvatobhadra, get_sarvatobhadra_predictions,
    get_sarvatobhadra_compatibility, get_sarvatobhadra_strength_score
)

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
    
    Args:
        date (Datetime): The date and time
        location (GeoPos): The geographical location
    
    Returns:
        dict: Dictionary with Sarvatobhadra Chakra information
    """
    # Create a chart for the date
    chart = Chart(date, location, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
    
    # Get the Sarvatobhadra Chakra
    chakra = get_sarvatobhadra_chakra(chart)
    
    # Get the chakra quality
    quality = get_chakra_quality(chakra)
    
    # Get auspicious directions
    auspicious_directions = get_auspicious_directions(chakra)
    
    # Get inauspicious directions
    inauspicious_directions = get_inauspicious_directions(chakra)
    
    # Get Tara Bala
    tara_bala = get_tara_bala(chart)
    
    return {
        'date': date,
        'chakra': chakra,
        'quality': quality,
        'auspicious_directions': auspicious_directions,
        'inauspicious_directions': inauspicious_directions,
        'tara_bala': tara_bala
    }


def get_best_direction_for_activity(date, location, activity):
    """
    Get the best direction for a specific activity
    
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
    best_direction = get_direction_for_activity(chakra, activity)
    
    return best_direction


def get_tara_bala_for_date(date, location):
    """
    Get Tara Bala (lunar strength) information for a specific date
    
    Args:
        date (Datetime): The date and time
        location (GeoPos): The geographical location
    
    Returns:
        dict: Dictionary with Tara Bala information
    """
    # Create a chart for the date
    chart = Chart(date, location, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
    
    # Get Tara Bala
    tara_bala = get_tara_bala(chart)
    
    return tara_bala
