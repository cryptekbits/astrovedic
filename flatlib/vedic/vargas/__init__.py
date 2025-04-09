"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Varga (divisional chart) calculations for Vedic astrology.
    It includes functions to calculate all 16 major divisional charts used in Jyotish.
"""

from flatlib import const
from flatlib.chart import Chart
from flatlib.vedic.vargas.core import (
    calculate_varga_longitude, create_varga_chart, 
    get_varga_name, get_varga_description
)

# Divisional chart constants
D1 = 'D1'    # Rashi (birth chart)
D2 = 'D2'    # Hora (wealth)
D3 = 'D3'    # Drekkana (siblings)
D4 = 'D4'    # Chaturthamsha (fortune, property)
D7 = 'D7'    # Saptamsha (children)
D9 = 'D9'    # Navamsha (spouse, general life path)
D10 = 'D10'  # Dashamsha (career)
D12 = 'D12'  # Dwadashamsha (parents)
D16 = 'D16'  # Shodashamsha (vehicles, comforts)
D20 = 'D20'  # Vimshamsha (spiritual life)
D24 = 'D24'  # Chaturvimshamsha (education)
D27 = 'D27'  # Saptavimshamsha (strength and weakness)
D30 = 'D30'  # Trimshamsha (misfortunes)
D40 = 'D40'  # Khavedamsha (auspicious and inauspicious effects)
D45 = 'D45'  # Akshavedamsha (general indications)
D60 = 'D60'  # Shashtiamsha (overall analysis)

# List of all divisional charts
LIST_VARGAS = [
    D1, D2, D3, D4, D7, D9, D10, D12, 
    D16, D20, D24, D27, D30, D40, D45, D60
]

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
