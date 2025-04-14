"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements the D27 (Saptavimshamsha) chart calculations.
    The D27 chart is used to analyze strength and weakness.
"""

from flatlib.vedic.vargas.core import calculate_varga_longitude

def calculate_d27(longitude):
    """
    Calculate the D27 (Saptavimshamsha) longitude
    
    In the Saptavimshamsha chart, each sign is divided into twenty-seven parts of 1.11° each.
    The resulting sign depends on the original sign:
    
    For movable signs (Aries, Cancer, Libra, Capricorn):
        The twenty-seven divisions map to the nakshatras starting from Ashwini
        
    For fixed signs (Taurus, Leo, Scorpio, Aquarius):
        The twenty-seven divisions map to the nakshatras starting from Magha
        
    For dual signs (Gemini, Virgo, Sagittarius, Pisces):
        The twenty-seven divisions map to the nakshatras starting from Mula
    
    Args:
        longitude (float): The longitude in the birth chart (0-360)
    
    Returns:
        float: The longitude in the D27 chart
    """
    # Get the sign number (0-11) and longitude within the sign (0-30)
    sign_num = int(longitude / 30)
    sign_lon = longitude % 30
    
    # Determine which division (0-26)
    division = int(sign_lon / (30/27))
    
    # Determine the sign type (movable, fixed, or dual)
    sign_type = sign_num % 3  # 0 = movable, 1 = fixed, 2 = dual
    
    # Calculate the starting nakshatra based on the sign type
    if sign_type == 0:  # Movable signs
        start_nakshatra = 0  # Ashwini
    elif sign_type == 1:  # Fixed signs
        start_nakshatra = 9  # Magha
    else:  # Dual signs
        start_nakshatra = 18  # Mula
    
    # Calculate the resulting nakshatra
    result_nakshatra = (start_nakshatra + division) % 27
    
    # Calculate the resulting sign (each nakshatra spans 13.33° across signs)
    result_sign = int(result_nakshatra * 13.33333 / 30) % 12
    
    # Calculate the longitude within the resulting sign
    result_lon = (result_nakshatra * 13.33333) % 30
    
    # Add the position within the division
    result_lon += (sign_lon % (30/27)) * 27
    
    # Ensure the result is within 0-30
    result_lon %= 30
    
    # Return the final longitude
    return result_sign * 30 + result_lon
