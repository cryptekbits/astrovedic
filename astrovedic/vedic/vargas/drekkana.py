"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements the D3 (Drekkana) chart calculations.
    The D3 chart is used to analyze siblings, courage, and initiative.
"""

from astrovedic.vedic.vargas.core import calculate_varga_longitude

def calculate_d3(longitude):
    """
    Calculate the D3 (Drekkana) longitude
    
    In the Drekkana chart, each sign is divided into three parts of 10° each:
    - First Drekkana (0-10°): Same sign
    - Second Drekkana (10-20°): 5th sign from the birth sign
    - Third Drekkana (20-30°): 9th sign from the birth sign
    
    Args:
        longitude (float): The longitude in the birth chart (0-360)
    
    Returns:
        float: The longitude in the D3 chart
    """
    # Get the sign number (0-11) and longitude within the sign (0-30)
    sign_num = int(longitude / 30)
    sign_lon = longitude % 30
    
    # Determine which drekkana (0, 1, or 2)
    drekkana = int(sign_lon / 10)
    
    # Calculate the resulting sign based on the drekkana
    if drekkana == 0:
        # First drekkana: same sign
        result_sign = sign_num
    elif drekkana == 1:
        # Second drekkana: 5th sign from birth sign
        result_sign = (sign_num + 4) % 12
    else:  # drekkana == 2
        # Third drekkana: 9th sign from birth sign
        result_sign = (sign_num + 8) % 12
    
    # Calculate the longitude within the resulting sign
    result_lon = (sign_lon % 10) * 3
    
    # Return the final longitude
    return result_sign * 30 + result_lon
