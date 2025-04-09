"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements the D60 (Shashtiamsha) chart calculations.
    The D60 chart is used for overall analysis and specific karmic influences.
"""

from flatlib import const

def calculate_d60(longitude):
    """
    Calculate the D60 (Shashtiamsha) longitude
    
    In the Shashtiamsha chart, each sign is divided into sixty parts of 0.5° each.
    The resulting sign depends on the original sign and a complex mapping system.
    
    Args:
        longitude (float): The longitude in the birth chart (0-360)
    
    Returns:
        float: The longitude in the D60 chart
    """
    # Get the sign number (0-11) and longitude within the sign (0-30)
    sign_num = int(longitude / 30)
    sign_lon = longitude % 30
    
    # Determine which division (0-59)
    division = int(sign_lon / 0.5)
    
    # Determine if the sign is odd (1-based, so even in 0-based)
    is_odd_sign = (sign_num % 2 == 0)
    
    # Determine the element of the sign
    element = sign_num % 4  # 0 = fire, 1 = earth, 2 = air, 3 = water
    
    # The Shashtiamsha mapping is complex and follows a specific pattern
    # We'll implement a simplified version based on traditional rules
    
    # For odd signs, the first five divisions go to the same sign,
    # then the next five to the next sign, and so on
    # For even signs, the pattern is reversed
    
    if is_odd_sign:
        # For odd signs
        result_sign = (sign_num + int(division / 5)) % 12
    else:
        # For even signs
        result_sign = (sign_num + 11 - int(division / 5)) % 12
    
    # Calculate the longitude within the resulting sign
    result_lon = (division % 5) * 6
    
    # Return the final longitude
    return result_sign * 30 + result_lon
