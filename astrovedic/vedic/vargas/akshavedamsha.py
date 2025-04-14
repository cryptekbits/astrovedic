"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements the D45 (Akshavedamsha) chart calculations.
    The D45 chart is used to analyze general indications and overall life.
"""

from astrovedic.vedic.vargas.core import calculate_varga_longitude

def calculate_d45(longitude):
    """
    Calculate the D45 (Akshavedamsha) longitude
    
    In the Akshavedamsha chart, each sign is divided into forty-five parts of 0.67° each.
    The resulting sign depends on the original sign:
    
    For movable signs (Aries, Cancer, Libra, Capricorn):
        The forty-five divisions map to the nine signs starting from Aries, then the nine signs starting from Aries again, 
        then the nine signs starting from Aries again, then the nine signs starting from Aries again, 
        and finally the nine signs starting from Aries again
        
    For fixed signs (Taurus, Leo, Scorpio, Aquarius):
        The forty-five divisions map to the nine signs starting from Leo, then the nine signs starting from Leo again, 
        then the nine signs starting from Leo again, then the nine signs starting from Leo again, 
        and finally the nine signs starting from Leo again
        
    For dual signs (Gemini, Virgo, Sagittarius, Pisces):
        The forty-five divisions map to the nine signs starting from Sagittarius, then the nine signs starting from Sagittarius again, 
        then the nine signs starting from Sagittarius again, then the nine signs starting from Sagittarius again, 
        and finally the nine signs starting from Sagittarius again
    
    Args:
        longitude (float): The longitude in the birth chart (0-360)
    
    Returns:
        float: The longitude in the D45 chart
    """
    # Get the sign number (0-11) and longitude within the sign (0-30)
    sign_num = int(longitude / 30)
    sign_lon = longitude % 30
    
    # Determine which division (0-44)
    division = int(sign_lon / (30/45))
    
    # Determine the sign type (movable, fixed, or dual)
    sign_type = sign_num % 3  # 0 = movable, 1 = fixed, 2 = dual
    
    # Calculate the starting sign based on the sign type
    if sign_type == 0:  # Movable signs
        start_sign = 0  # Aries
    elif sign_type == 1:  # Fixed signs
        start_sign = 4  # Leo
    else:  # Dual signs
        start_sign = 8  # Sagittarius
    
    # Calculate the resulting sign (using modulo 9 because only 9 signs are used)
    result_sign = (start_sign + division % 9) % 12
    
    # Calculate the longitude within the resulting sign
    result_lon = (sign_lon % (30/45)) * 45
    
    # Return the final longitude
    return result_sign * 30 + result_lon
