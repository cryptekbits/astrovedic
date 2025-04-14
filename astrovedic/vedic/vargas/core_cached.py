"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements cached core functionality for Varga (divisional chart)
    calculations in Vedic astrology.
"""

from astrovedic import const
from astrovedic import angle
from astrovedic.chart import Chart
from astrovedic.object import Object
from astrovedic.cache import calculation_cache, reference_cache


@calculation_cache()
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

    # Calculate the division within the sign
    division = int(sign_lon * divisor / 30)

    # Calculate the resulting sign
    result_sign = (sign_num * divisor + division + offset) % 12

    # Calculate the longitude within the resulting sign
    result_lon = (sign_lon * divisor) % 30

    # Return the final longitude
    return result_sign * 30 + result_lon


@reference_cache()
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


@reference_cache()
def get_varga_description(varga_type):
    """
    Get the description of a divisional chart

    Args:
        varga_type (str): The type of divisional chart (e.g., D9, D10)

    Returns:
        str: The description of the divisional chart
    """
    varga_descriptions = {
        'D1': 'Physical body, overall personality',
        'D2': 'Wealth, family resources',
        'D3': 'Siblings, courage, communication',
        'D4': 'Property, home, mother, education',
        'D7': 'Children, creativity',
        'D9': 'Spouse, marriage, dharma',
        'D10': 'Career, profession, status',
        'D12': 'Parents, ancestors',
        'D16': 'Vehicles, comforts',
        'D20': 'Spiritual pursuits, religious activities',
        'D24': 'Education, learning',
        'D27': 'Strengths and weaknesses',
        'D30': 'Misfortunes, challenges',
        'D40': 'Auspicious and inauspicious effects',
        'D45': 'All aspects of life',
        'D60': 'All karmas, past life influences'
    }

    return varga_descriptions.get(varga_type, '')
