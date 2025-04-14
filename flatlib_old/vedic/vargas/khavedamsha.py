"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements the D40 (Khavedamsha) chart calculations.
    The D40 chart is used to analyze auspicious and inauspicious effects.
"""

from flatlib.vedic.vargas.core import calculate_varga_longitude

def calculate_d40(longitude):
    """
    Calculate the D40 (Khavedamsha) longitude
    
    In the Khavedamsha chart, each sign is divided into forty parts of 0.75° each.
    The resulting sign depends on the original sign:
    
    For movable signs (Aries, Cancer, Libra, Capricorn):
        The forty divisions map to the twelve signs starting from Aries, then the twelve signs starting from Aries again, 
        then the twelve signs starting from Aries again, and finally the four signs starting from Aries
        
    For fixed signs (Taurus, Leo, Scorpio, Aquarius):
        The forty divisions map to the twelve signs starting from Leo, then the twelve signs starting from Leo again, 
        then the twelve signs starting from Leo again, and finally the four signs starting from Leo
        
    For dual signs (Gemini, Virgo, Sagittarius, Pisces):
        The forty divisions map to the twelve signs starting from Sagittarius, then the twelve signs starting from Sagittarius again, 
        then the twelve signs starting from Sagittarius again, and finally the four signs starting from Sagittarius
    
    Args:
        longitude (float): The longitude in the birth chart (0-360)
    
    Returns:
        float: The longitude in the D40 chart
    """
    # Get the sign number (0-11) and longitude within the sign (0-30)
    sign_num = int(longitude / 30)
    sign_lon = longitude % 30
    
    # Determine which division (0-39)
    division = int(sign_lon / 0.75)
    
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
    result_lon = (sign_lon % 0.75) * 40
    
    # Return the final longitude
    return result_sign * 30 + result_lon
