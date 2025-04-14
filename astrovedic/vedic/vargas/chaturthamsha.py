"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements the D4 (Chaturthamsha) chart calculations.
    The D4 chart is used to analyze fortune, property, and fixed assets.
"""

from astrovedic.vedic.vargas.core import calculate_varga_longitude

def calculate_d4(longitude):
    """
    Calculate the D4 (Chaturthamsha) longitude
    
    In the Chaturthamsha chart, each sign is divided into four parts of 7.5° each.
    The resulting sign depends on the original sign and the quarter:
    
    For movable signs (Aries, Cancer, Libra, Capricorn):
        1st quarter: Same sign
        2nd quarter: 4th sign from birth sign
        3rd quarter: 7th sign from birth sign
        4th quarter: 10th sign from birth sign
        
    For fixed signs (Taurus, Leo, Scorpio, Aquarius):
        1st quarter: 11th sign from birth sign
        2nd quarter: 2nd sign from birth sign
        3rd quarter: 5th sign from birth sign
        4th quarter: 8th sign from birth sign
        
    For dual signs (Gemini, Virgo, Sagittarius, Pisces):
        1st quarter: 9th sign from birth sign
        2nd quarter: 12th sign from birth sign
        3rd quarter: 3rd sign from birth sign
        4th quarter: 6th sign from birth sign
    
    Args:
        longitude (float): The longitude in the birth chart (0-360)
    
    Returns:
        float: The longitude in the D4 chart
    """
    # Get the sign number (0-11) and longitude within the sign (0-30)
    sign_num = int(longitude / 30)
    sign_lon = longitude % 30
    
    # Determine which quarter (0, 1, 2, or 3)
    quarter = int(sign_lon / 7.5)
    
    # Determine the sign type (movable, fixed, or dual)
    sign_type = sign_num % 3  # 0 = movable, 1 = fixed, 2 = dual
    
    # Calculate the resulting sign based on the sign type and quarter
    if sign_type == 0:  # Movable signs
        offsets = [0, 3, 6, 9]
    elif sign_type == 1:  # Fixed signs
        offsets = [10, 1, 4, 7]
    else:  # Dual signs
        offsets = [8, 11, 2, 5]
    
    result_sign = (sign_num + offsets[quarter]) % 12
    
    # Calculate the longitude within the resulting sign
    result_lon = (sign_lon % 7.5) * 4
    
    # Return the final longitude
    return result_sign * 30 + result_lon
