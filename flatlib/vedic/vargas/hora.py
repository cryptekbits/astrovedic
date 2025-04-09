"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements the D2 (Hora) chart calculations.
    The D2 chart is used to analyze wealth and financial prosperity.
"""

from flatlib import const

def calculate_d2(longitude):
    """
    Calculate the D2 (Hora) longitude
    
    In the Hora chart:
    - For odd signs (Aries, Gemini, etc.), the first half (0-15°) goes to Leo,
      and the second half (15-30°) goes to Cancer
    - For even signs (Taurus, Cancer, etc.), the first half (0-15°) goes to Cancer,
      and the second half (15-30°) goes to Leo
    
    Args:
        longitude (float): The longitude in the birth chart (0-360)
    
    Returns:
        float: The longitude in the D2 chart
    """
    # Get the sign number (0-11) and longitude within the sign (0-30)
    sign_num = int(longitude / 30)
    sign_lon = longitude % 30
    
    # Determine if the sign is odd (1-based, so even in 0-based)
    is_odd_sign = (sign_num % 2 == 0)
    
    # Determine if it's the first or second half of the sign
    is_first_half = (sign_lon < 15)
    
    # Calculate the resulting sign
    if is_odd_sign:
        # For odd signs: first half -> Leo, second half -> Cancer
        result_sign = const.LEO if is_first_half else const.CANCER
    else:
        # For even signs: first half -> Cancer, second half -> Leo
        result_sign = const.CANCER if is_first_half else const.LEO
    
    # Calculate the longitude within the resulting sign
    result_lon = (sign_lon % 15) * 2
    
    # Get the sign number for the resulting sign
    result_sign_num = {
        const.ARIES: 0, const.TAURUS: 1, const.GEMINI: 2, const.CANCER: 3,
        const.LEO: 4, const.VIRGO: 5, const.LIBRA: 6, const.SCORPIO: 7,
        const.SAGITTARIUS: 8, const.CAPRICORN: 9, const.AQUARIUS: 10, const.PISCES: 11
    }[result_sign]
    
    # Return the final longitude
    return result_sign_num * 30 + result_lon
