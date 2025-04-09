"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements the D10 (Dashamsha) chart calculations.
    The D10 chart is used to analyze career, profession, and status.
"""

from flatlib.vedic.vargas.core import calculate_varga_longitude

def calculate_d10(longitude):
    """
    Calculate the D10 (Dashamsha) longitude
    
    In the Dashamsha chart, each sign is divided into ten parts of 3° each.
    The resulting sign depends on the original sign:
    
    For odd signs (Aries, Gemini, etc.):
        The ten divisions map to the 9th sign from the birth sign and the next nine signs in order
        
    For even signs (Taurus, Cancer, etc.):
        The ten divisions map to the 3rd sign from the birth sign and the next nine signs in order
    
    Args:
        longitude (float): The longitude in the birth chart (0-360)
    
    Returns:
        float: The longitude in the D10 chart
    """
    # Get the sign number (0-11) and longitude within the sign (0-30)
    sign_num = int(longitude / 30)
    sign_lon = longitude % 30
    
    # Determine which division (0-9)
    division = int(sign_lon / 3)
    
    # Determine if the sign is odd (1-based, so even in 0-based)
    is_odd_sign = (sign_num % 2 == 0)
    
    # Calculate the resulting sign
    if is_odd_sign:
        # For odd signs: start from the 9th sign
        result_sign = (sign_num + 8 + division) % 12
    else:
        # For even signs: start from the 3rd sign
        result_sign = (sign_num + 2 + division) % 12
    
    # Calculate the longitude within the resulting sign
    result_lon = (sign_lon % 3) * 10
    
    # Return the final longitude
    return result_sign * 30 + result_lon
