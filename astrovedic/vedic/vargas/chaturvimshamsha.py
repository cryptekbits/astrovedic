"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements the D24 (Chaturvimshamsha) chart calculations.
    The D24 chart is used to analyze education, learning, and knowledge.
"""

from astrovedic.vedic.vargas.core import calculate_varga_longitude

def calculate_d24(longitude):
    """
    Calculate the D24 (Chaturvimshamsha) longitude
    
    In the Chaturvimshamsha chart, each sign is divided into twenty-four parts of 1.25° each.
    The resulting sign depends on the original sign:
    
    For movable signs (Aries, Cancer, Libra, Capricorn):
        The twenty-four divisions map to the twelve signs starting from Aries, then the twelve signs starting from Aries again
        
    For fixed signs (Taurus, Leo, Scorpio, Aquarius):
        The twenty-four divisions map to the twelve signs starting from Leo, then the twelve signs starting from Leo again
        
    For dual signs (Gemini, Virgo, Sagittarius, Pisces):
        The twenty-four divisions map to the twelve signs starting from Sagittarius, then the twelve signs starting from Sagittarius again
    
    Args:
        longitude (float): The longitude in the birth chart (0-360)
    
    Returns:
        float: The longitude in the D24 chart
    """
    # Get the sign number (0-11) and longitude within the sign (0-30)
    sign_num = int(longitude / 30)
    sign_lon = longitude % 30
    
    # Determine which division (0-23)
    division = int(sign_lon / 1.25)
    
    # Determine the sign type (movable, fixed, or dual)
    sign_type = sign_num % 3  # 0 = movable, 1 = fixed, 2 = dual
    
    # Calculate the starting sign based on the sign type
    if sign_type == 0:  # Movable signs
        start_sign = 0  # Aries
    elif sign_type == 1:  # Fixed signs
        start_sign = 4  # Leo
    else:  # Dual signs
        start_sign = 8  # Sagittarius
    
    # Calculate the resulting sign
    result_sign = (start_sign + division % 12) % 12
    
    # Calculate the longitude within the resulting sign
    result_lon = (sign_lon % 1.25) * 24
    
    # Return the final longitude
    return result_sign * 30 + result_lon
