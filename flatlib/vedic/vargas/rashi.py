"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements the D1 (Rashi) chart calculations.
    The D1 chart is the main birth chart in Vedic astrology.
"""

def calculate_d1(longitude):
    """
    Calculate the D1 (Rashi) longitude
    
    The D1 chart is the same as the birth chart, so this function
    simply returns the input longitude.
    
    Args:
        longitude (float): The longitude in the birth chart (0-360)
    
    Returns:
        float: The longitude in the D1 chart (same as input)
    """
    return longitude
