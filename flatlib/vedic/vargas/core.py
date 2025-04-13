"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements core functionality for Varga (divisional chart) 
    calculations in Vedic astrology.
"""

from flatlib import const
from flatlib import angle
from flatlib.chart import Chart
from flatlib.object import Object


def calculate_varga_longitude(longitude, divisor, offset=0):
    """
    Calculate the longitude in a divisional chart using the standard formula
    
    Args:
        longitude (float): The longitude in the birth chart (0-360)
        divisor (int): The divisor for the varga (e.g., 9 for D9)
        offset (int, optional): Offset to add to the calculation
    
    Returns:
        float: The longitude in the divisional chart
    """
    # Get the sign number (0-11) and longitude within the sign (0-30)
    sign_num = int(longitude / 30)
    sign_lon = longitude % 30
    
    # Calculate the division within the sign using standard Vedic multiplication
    division = int(sign_lon * divisor / 30)
    
    # Calculate the resulting sign using standard method
    # For D9 (Navamsa), each 3.33 degrees in a sign corresponds to one Navamsa sign
    result_sign = (sign_num * divisor + division + offset) % 12
    
    # Calculate the longitude within the resulting sign
    # This ensures continuity within the divisional chart
    result_lon = (sign_lon * divisor) % 30
    
    # Return the final longitude
    return result_sign * 30 + result_lon


def create_varga_chart(chart, calculator, varga_type):
    """
    Create a divisional chart from a birth chart
    
    Args:
        chart (Chart): The birth chart
        calculator (function): The function to calculate varga longitudes
        varga_type (str): The type of divisional chart (e.g., D9, D10)
    
    Returns:
        Chart: The divisional chart
    """
    # Create a copy of the chart
    varga_chart = chart.copy()
    
    # Update the longitudes of all objects
    for obj in varga_chart.objects:
        varga_lon = calculator(obj.lon)
        obj.relocate(varga_lon)
    
    # Update the longitudes of all houses
    for house in varga_chart.houses:
        varga_lon = calculator(house.lon)
        house.relocate(varga_lon)
    
    # Update the longitudes of all angles
    for angle_obj in varga_chart.angles:
        varga_lon = calculator(angle_obj.lon)
        angle_obj.relocate(varga_lon)
    
    return varga_chart


def get_varga_name(varga_type):
    """
    Get the Sanskrit name of a divisional chart
    
    Args:
        varga_type (str): The type of divisional chart (e.g., D9, D10)
    
    Returns:
        str: The Sanskrit name of the divisional chart
    """
    varga_names = {
        'D1': 'Rashi',
        'D2': 'Hora',
        'D3': 'Drekkana',
        'D4': 'Chaturthamsha',
        'D7': 'Saptamsha',
        'D9': 'Navamsha',
        'D10': 'Dashamsha',
        'D12': 'Dwadashamsha',
        'D16': 'Shodashamsha',
        'D20': 'Vimshamsha',
        'D24': 'Chaturvimshamsha',
        'D27': 'Saptavimshamsha',
        'D30': 'Trimshamsha',
        'D40': 'Khavedamsha',
        'D45': 'Akshavedamsha',
        'D60': 'Shashtiamsha'
    }
    
    return varga_names.get(varga_type, varga_type)


def get_varga_description(varga_type):
    """
    Get the description of a divisional chart
    
    Args:
        varga_type (str): The type of divisional chart (e.g., D9, D10)
    
    Returns:
        str: The description of the divisional chart
    """
    varga_descriptions = {
        'D1': 'Main birth chart (Rashi)',
        'D2': 'Wealth and financial prosperity (Hora)',
        'D3': 'Siblings and courage (Drekkana)',
        'D4': 'Fortune, property, and fixed assets (Chaturthamsha)',
        'D7': 'Children, progeny, and fertility (Saptamsha)',
        'D9': 'Spouse, marriage, and general life path (Navamsha)',
        'D10': 'Career, profession, and status (Dashamsha)',
        'D12': 'Parents and ancestry (Dwadashamsha)',
        'D16': 'Vehicles, comforts, and luxuries (Shodashamsha)',
        'D20': 'Spiritual life and religious activities (Vimshamsha)',
        'D24': 'Education, learning, and knowledge (Chaturvimshamsha)',
        'D27': 'Strength and weakness (Saptavimshamsha)',
        'D30': 'Misfortunes and difficulties (Trimshamsha)',
        'D40': 'Auspicious and inauspicious effects (Khavedamsha)',
        'D45': 'General indications and overall life (Akshavedamsha)',
        'D60': 'Overall analysis and specific karmic influences (Shashtiamsha)'
    }
    
    return varga_descriptions.get(varga_type, f"Divisional chart {varga_type}")
