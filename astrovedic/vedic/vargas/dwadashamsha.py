"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements the D12 (Dwadashamsha) chart calculations.
    The D12 chart is used to analyze parents and ancestry.
"""

from astrovedic.vedic.vargas.core import calculate_varga_longitude

def calculate_d12(longitude):
    """
    Calculate the D12 (Dwadashamsha) longitude
    
    In the Dwadashamsha chart, each sign is divided into twelve parts of 2.5° each.
    The twelve divisions of a sign map to the twelve signs starting from the birth sign.
    
    Args:
        longitude (float): The longitude in the birth chart (0-360)
    
    Returns:
        float: The longitude in the D12 chart
    """
    # Get the sign number (0-11) and longitude within the sign (0-30)
    sign_num = int(longitude / 30)
    sign_lon = longitude % 30
    
    # Determine which division (0-11)
    division = int(sign_lon / 2.5)
    
    # Calculate the resulting sign
    result_sign = (sign_num + division) % 12
    
    # Calculate the longitude within the resulting sign
    result_lon = (sign_lon % 2.5) * 12
    
    # Return the final longitude
    return result_sign * 30 + result_lon
