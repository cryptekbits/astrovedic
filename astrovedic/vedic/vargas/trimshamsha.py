"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements the D30 (Trimshamsha) chart calculations.
    The D30 chart is used to analyze misfortunes and difficulties.
"""

from astrovedic import const

def calculate_d30(longitude):
    """
    Calculate the D30 (Trimshamsha) longitude
    
    In the Trimshamsha chart, each sign is divided into five unequal parts:
    
    For odd signs (Aries, Gemini, etc.):
        - 0-5°: Mars
        - 5-10°: Saturn
        - 10-18°: Jupiter
        - 18-25°: Mercury
        - 25-30°: Venus
        
    For even signs (Taurus, Cancer, etc.):
        - 0-5°: Venus
        - 5-12°: Mercury
        - 12-20°: Jupiter
        - 20-25°: Saturn
        - 25-30°: Mars
    
    Args:
        longitude (float): The longitude in the birth chart (0-360)
    
    Returns:
        float: The longitude in the D30 chart
    """
    # Get the sign number (0-11) and longitude within the sign (0-30)
    sign_num = int(longitude / 30)
    sign_lon = longitude % 30
    
    # Determine if the sign is odd (1-based, so even in 0-based)
    is_odd_sign = (sign_num % 2 == 0)
    
    # Determine the planet and portion based on the longitude within the sign
    if is_odd_sign:
        # For odd signs
        if sign_lon < 5:
            planet = const.MARS
            portion = sign_lon / 5
        elif sign_lon < 10:
            planet = const.SATURN
            portion = (sign_lon - 5) / 5
        elif sign_lon < 18:
            planet = const.JUPITER
            portion = (sign_lon - 10) / 8
        elif sign_lon < 25:
            planet = const.MERCURY
            portion = (sign_lon - 18) / 7
        else:
            planet = const.VENUS
            portion = (sign_lon - 25) / 5
    else:
        # For even signs
        if sign_lon < 5:
            planet = const.VENUS
            portion = sign_lon / 5
        elif sign_lon < 12:
            planet = const.MERCURY
            portion = (sign_lon - 5) / 7
        elif sign_lon < 20:
            planet = const.JUPITER
            portion = (sign_lon - 12) / 8
        elif sign_lon < 25:
            planet = const.SATURN
            portion = (sign_lon - 20) / 5
        else:
            planet = const.MARS
            portion = (sign_lon - 25) / 5
    
    # Map planets to their signs
    planet_signs = {
        const.MARS: [0, 7],      # Aries and Scorpio
        const.VENUS: [1, 6],     # Taurus and Libra
        const.MERCURY: [2, 5],   # Gemini and Virgo
        const.MOON: [3],         # Cancer
        const.SUN: [4],          # Leo
        const.JUPITER: [8, 11],  # Sagittarius and Pisces
        const.SATURN: [9, 10]    # Capricorn and Aquarius
    }
    
    # Get the signs ruled by the planet
    ruled_signs = planet_signs[planet]
    
    # For planets ruling two signs, use the sign of the same element
    # (fire, earth, air, water) as the original sign
    if len(ruled_signs) > 1:
        element = sign_num % 4  # 0 = fire, 1 = earth, 2 = air, 3 = water
        for ruled_sign in ruled_signs:
            if ruled_sign % 4 == element:
                result_sign = ruled_sign
                break
        else:
            # If no match found, use the first sign
            result_sign = ruled_signs[0]
    else:
        result_sign = ruled_signs[0]
    
    # Calculate the longitude within the resulting sign
    result_lon = portion * 30
    
    # Return the final longitude
    return result_sign * 30 + result_lon
