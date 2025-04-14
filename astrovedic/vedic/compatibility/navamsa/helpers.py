"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements helper functions for Navamsa compatibility analysis
    in Vedic astrology.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.vedic.vargas import D9, get_varga_chart
from astrovedic.vedic.vargas.navamsha import calculate_d9


def get_navamsa_sign(longitude):
    """
    Get the Navamsa sign for a longitude
    
    Args:
        longitude (float): The longitude in degrees (0-360)
    
    Returns:
        str: The Navamsa sign
    """
    # Calculate the Navamsa longitude
    navamsa_lon = calculate_d9(longitude)
    
    # Get the sign
    sign_num = int(navamsa_lon / 30)
    
    # Get the sign name
    signs = [
        const.ARIES, const.TAURUS, const.GEMINI, const.CANCER,
        const.LEO, const.VIRGO, const.LIBRA, const.SCORPIO,
        const.SAGITTARIUS, const.CAPRICORN, const.AQUARIUS, const.PISCES
    ]
    
    return signs[sign_num]


def get_navamsa_longitude(longitude):
    """
    Get the Navamsa longitude for a longitude
    
    Args:
        longitude (float): The longitude in degrees (0-360)
    
    Returns:
        float: The Navamsa longitude
    """
    # Calculate the Navamsa longitude
    return calculate_d9(longitude)
