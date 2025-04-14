"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements the D9 (Navamsha) chart calculations.
    The D9 chart is one of the most important divisional charts in Vedic astrology,
    used to analyze marriage, spouse, and general life path.
"""

from astrovedic.vedic.vargas.core import calculate_varga_longitude

def calculate_d9(longitude):
    """
    Calculate the D9 (Navamsha) longitude
    
    In the Navamsha chart, each sign is divided into nine parts of 3.33° each.
    The resulting sign depends on the original sign:
    
    For fire signs (Aries, Leo, Sagittarius):
        The nine divisions map to Aries, Taurus, Gemini, Cancer, Leo, Virgo, Libra, Scorpio, Sagittarius
        
    For earth signs (Taurus, Virgo, Capricorn):
        The nine divisions map to Capricorn, Aquarius, Pisces, Aries, Taurus, Gemini, Cancer, Leo, Virgo
        
    For air signs (Gemini, Libra, Aquarius):
        The nine divisions map to Libra, Scorpio, Sagittarius, Capricorn, Aquarius, Pisces, Aries, Taurus, Gemini
        
    For water signs (Cancer, Scorpio, Pisces):
        The nine divisions map to Cancer, Leo, Virgo, Libra, Scorpio, Sagittarius, Capricorn, Aquarius, Pisces
    
    Args:
        longitude (float): The longitude in the birth chart (0-360)
    
    Returns:
        float: The longitude in the D9 chart
    """
    # Get the sign number (0-11) and longitude within the sign (0-30)
    sign_num = int(longitude / 30)
    sign_lon = longitude % 30
    
    # Determine which navamsha (0-8)
    navamsha = int(sign_lon / (30/9))
    
    # Determine the element of the sign
    element = sign_num % 4  # 0 = fire, 1 = earth, 2 = air, 3 = water
    
    # Calculate the starting sign based on the element
    if element == 0:  # Fire signs
        start_sign = 0  # Aries
    elif element == 1:  # Earth signs
        start_sign = 9  # Capricorn
    elif element == 2:  # Air signs
        start_sign = 6  # Libra
    else:  # Water signs
        start_sign = 3  # Cancer
    
    # Calculate the resulting sign
    result_sign = (start_sign + navamsha) % 12
    
    # Calculate the longitude within the resulting sign
    result_lon = (sign_lon % (30/9)) * 9
    
    # Return the final longitude
    return result_sign * 30 + result_lon
