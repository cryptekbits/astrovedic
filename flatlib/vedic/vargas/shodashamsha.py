"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements the D16 (Shodashamsha) chart calculations.
    The D16 chart is used to analyze vehicles, comforts, and luxuries.
"""

from flatlib.vedic.vargas.core import calculate_varga_longitude

def calculate_d16(longitude):
    """
    Calculate the D16 (Shodashamsha) longitude
    
    In the Shodashamsha chart, each sign is divided into sixteen parts of 1.875° each.
    The resulting sign depends on the original sign:
    
    For movable signs (Aries, Cancer, Libra, Capricorn):
        The sixteen divisions map to Aries through Pisces, then Aries through Cancer
        
    For fixed signs (Taurus, Leo, Scorpio, Aquarius):
        The sixteen divisions map to Leo through Pisces, then Aries through Cancer
        
    For dual signs (Gemini, Virgo, Sagittarius, Pisces):
        The sixteen divisions map to Sagittarius through Pisces, then Aries through Scorpio
    
    Args:
        longitude (float): The longitude in the birth chart (0-360)
    
    Returns:
        float: The longitude in the D16 chart
    """
    # Get the sign number (0-11) and longitude within the sign (0-30)
    sign_num = int(longitude / 30)
    sign_lon = longitude % 30
    
    # Determine which division (0-15)
    division = int(sign_lon / (30/16))
    
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
    result_sign = (start_sign + division) % 12
    
    # Calculate the longitude within the resulting sign
    result_lon = (sign_lon % (30/16)) * 16
    
    # Return the final longitude
    return result_sign * 30 + result_lon
