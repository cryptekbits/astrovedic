"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements the D20 (Vimshamsha) chart calculations.
    The D20 chart is used to analyze spiritual life and religious activities.
"""

from astrovedic.vedic.vargas.core import calculate_varga_longitude

def calculate_d20(longitude):
    """
    Calculate the D20 (Vimshamsha) longitude
    
    In the Vimshamsha chart, each sign is divided into twenty parts of 1.5° each.
    The resulting sign depends on the original sign:
    
    For movable signs (Aries, Cancer, Libra, Capricorn):
        The twenty divisions map to Aries through Virgo, then Libra through Pisces, then Aries through Scorpio
        
    For fixed signs (Taurus, Leo, Scorpio, Aquarius):
        The twenty divisions map to Leo through Pisces, then Aries through Pisces, then Aries
        
    For dual signs (Gemini, Virgo, Sagittarius, Pisces):
        The twenty divisions map to Sagittarius through Pisces, then Aries through Pisces, then Aries through Gemini
    
    Args:
        longitude (float): The longitude in the birth chart (0-360)
    
    Returns:
        float: The longitude in the D20 chart
    """
    # Get the sign number (0-11) and longitude within the sign (0-30)
    sign_num = int(longitude / 30)
    sign_lon = longitude % 30
    
    # Determine which division (0-19)
    division = int(sign_lon / 1.5)
    
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
    result_lon = (sign_lon % 1.5) * 20
    
    # Return the final longitude
    return result_sign * 30 + result_lon
