"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Varga (divisional chart) calculations for Vedic astrology.
    It includes functions to calculate all 16 major divisional charts used in Jyotish.
"""

from flatlib import const
from flatlib.chart import Chart
from flatlib.vedic.vargas.constants import (
    D1, D2, D3, D4, D7, D9, D10, D12,
    D16, D20, D24, D27, D30, D40, D45, D60,
    LIST_VARGAS
)
from flatlib.vedic.vargas.core import (
    calculate_varga_longitude, create_varga_chart,
    get_varga_name, get_varga_description
)

# Note: For detailed analysis, use the astroved_extension package

# Import all varga calculation functions
from flatlib.vedic.vargas.rashi import calculate_d1
from flatlib.vedic.vargas.hora import calculate_d2
from flatlib.vedic.vargas.drekkana import calculate_d3
from flatlib.vedic.vargas.chaturthamsha import calculate_d4
from flatlib.vedic.vargas.saptamsha import calculate_d7
from flatlib.vedic.vargas.navamsha import calculate_d9
from flatlib.vedic.vargas.dashamsha import calculate_d10
from flatlib.vedic.vargas.dwadashamsha import calculate_d12
from flatlib.vedic.vargas.shodashamsha import calculate_d16
from flatlib.vedic.vargas.vimshamsha import calculate_d20
from flatlib.vedic.vargas.chaturvimshamsha import calculate_d24
from flatlib.vedic.vargas.saptavimshamsha import calculate_d27
from flatlib.vedic.vargas.trimshamsha import calculate_d30
from flatlib.vedic.vargas.khavedamsha import calculate_d40
from flatlib.vedic.vargas.akshavedamsha import calculate_d45
from flatlib.vedic.vargas.shashtiamsha import calculate_d60

# Mapping of varga types to calculation functions
VARGA_CALCULATORS = {
    D1: calculate_d1,
    D2: calculate_d2,
    D3: calculate_d3,
    D4: calculate_d4,
    D7: calculate_d7,
    D9: calculate_d9,
    D10: calculate_d10,
    D12: calculate_d12,
    D16: calculate_d16,
    D20: calculate_d20,
    D24: calculate_d24,
    D27: calculate_d27,
    D30: calculate_d30,
    D40: calculate_d40,
    D45: calculate_d45,
    D60: calculate_d60
}


def get_varga_chart(chart, varga_type):
    """
    Get a divisional chart (varga) from a birth chart

    Args:
        chart (Chart): The birth chart
        varga_type (str): The type of divisional chart (e.g., D9, D10)

    Returns:
        Chart: The divisional chart
    """
    if varga_type not in VARGA_CALCULATORS:
        raise ValueError(f"Unsupported varga type: {varga_type}")

    # Get the calculation function for this varga type
    calculator = VARGA_CALCULATORS[varga_type]

    # Create the varga chart
    return create_varga_chart(chart, calculator, varga_type)


def get_all_varga_charts(chart):
    """
    Get all 16 divisional charts from a birth chart

    Args:
        chart (Chart): The birth chart

    Returns:
        dict: Dictionary of all varga charts with varga type as key
    """
    varga_charts = {}

    for varga_type in LIST_VARGAS:
        varga_charts[varga_type] = get_varga_chart(chart, varga_type)

    return varga_charts


def get_varga_longitude(longitude, varga_type):
    """
    Calculate the longitude in a specific divisional chart

    Args:
        longitude (float): The longitude in the birth chart (0-360)
        varga_type (str): The type of divisional chart (e.g., D9, D10)

    Returns:
        float: The longitude in the divisional chart
    """
    if varga_type not in VARGA_CALCULATORS:
        raise ValueError(f"Unsupported varga type: {varga_type}")

    # Get the calculation function for this varga type
    calculator = VARGA_CALCULATORS[varga_type]

    # Calculate the varga longitude
    return calculator(longitude)


def analyze_varga_charts(chart):
    """
    Analyze the Varga charts for a birth chart
    Note: For detailed analysis, use the astroved_extension package

    Args:
        chart (Chart): The birth chart

    Returns:
        dict: Dictionary with basic Varga analysis
    """
    # Import here to avoid circular imports
    from flatlib.vedic.vargas.basic_analysis import get_basic_varga_analysis

    # Get basic Varga analysis
    return get_basic_varga_analysis(chart)


def get_varga_positions(chart, varga_type):
    """
    Get planet positions in a Varga (divisional) chart

    Args:
        chart (Chart): The birth chart
        varga_type (str): The Varga (e.g., D9, D10, etc.)

    Returns:
        dict: Dictionary with planet positions in the Varga chart
    """
    # Create the Varga chart
    varga_chart = get_varga_chart(chart, varga_type)

    # Get planet positions
    positions = {}
    for planet_id in const.LIST_OBJECTS_VEDIC:
        planet = varga_chart.getObject(planet_id)
        if planet:
            positions[planet_id] = {
                'longitude': planet.lon,
                'sign': planet.sign
                # Removed 'house': planet.house as it's not available here
            }

    return positions


def get_basic_varga_analysis(chart):
    """
    Get basic Varga analysis for a chart
    Note: For detailed analysis, use the astroved_extension package

    Args:
        chart (Chart): The birth chart

    Returns:
        dict: Dictionary with basic Varga analysis
    """
    # Import here to avoid circular imports
    from flatlib.vedic.vargas.basic_analysis import get_basic_varga_analysis as _get_basic_varga_analysis

    # Get basic Varga analysis
    return _get_basic_varga_analysis(chart)
