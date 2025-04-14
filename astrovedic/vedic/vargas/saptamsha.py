"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements the D7 (Saptamsha) chart calculations.
    The D7 chart is used to analyze children, progeny, and fertility.
"""

from astrovedic.vedic.vargas.core import calculate_varga_longitude

def calculate_d7(longitude):
    """
    Calculate the D7 (Saptamsha) longitude
    
    In the Saptamsha chart, each sign is divided into seven parts of 4.2857° each.
    The resulting sign depends on the original sign:
    
    For odd signs (Aries, Gemini, etc.):
        The seven divisions map to the same sign and the next six signs in order
        
    For even signs (Taurus, Cancer, etc.):
        The seven divisions map to the 7th sign from the birth sign and the next six signs in order
    
    Args:
        longitude (float): The longitude in the birth chart (0-360)
    
    Returns:
        float: The longitude in the D7 chart
    """
    # Get the sign number (0-11) and longitude within the sign (0-30)
    sign_num = int(longitude / 30)
    sign_lon = longitude % 30
    
    # Determine which division (0-6)
    division = int(sign_lon / (30/7))
    
    # Determine if the sign is odd (1-based, so even in 0-based)
    is_odd_sign = (sign_num % 2 == 0)
    
    # Calculate the resulting sign
    if is_odd_sign:
        # For odd signs: start from the same sign
        result_sign = (sign_num + division) % 12
    else:
        # For even signs: start from the 7th sign
        result_sign = (sign_num + 6 + division) % 12
    
    # Calculate the longitude within the resulting sign
    result_lon = (sign_lon % (30/7)) * 7
    
    # Return the final longitude
    return result_sign * 30 + result_lon
