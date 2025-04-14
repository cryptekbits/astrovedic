"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Navamsa compatibility analysis
    for Vedic astrology.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos

from astrovedic.vedic.compatibility.navamsa.compatibility import (
    get_navamsa_compatibility, get_navamsa_aspects,
    get_navamsa_strength
)

from astrovedic.vedic.compatibility.navamsa.positions import (
    get_navamsa_positions
)


def get_navamsa_compatibility(chart1, chart2):
    """
    Get the Navamsa compatibility between two charts
    
    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart
    
    Returns:
        dict: Dictionary with Navamsa compatibility information
    """
    from astrovedic.vedic.compatibility.navamsa.compatibility import get_navamsa_compatibility as get_compatibility
    return get_compatibility(chart1, chart2)


def get_navamsa_positions(chart):
    """
    Get the Navamsa positions for a chart
    
    Args:
        chart (Chart): The chart
    
    Returns:
        dict: Dictionary with Navamsa positions
    """
    from astrovedic.vedic.compatibility.navamsa.positions import get_navamsa_positions as get_positions
    return get_positions(chart)


def get_navamsa_aspects(chart1, chart2):
    """
    Get the Navamsa aspects between two charts
    
    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart
    
    Returns:
        list: List of Navamsa aspects
    """
    from astrovedic.vedic.compatibility.navamsa.compatibility import get_navamsa_aspects as get_aspects
    return get_aspects(chart1, chart2)


def get_navamsa_strength(chart):
    """
    Get the Navamsa strength for a chart
    
    Args:
        chart (Chart): The chart
    
    Returns:
        dict: Dictionary with Navamsa strength information
    """
    from astrovedic.vedic.compatibility.navamsa.compatibility import get_navamsa_strength as get_strength
    return get_strength(chart)
