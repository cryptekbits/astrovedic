"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements calculations for additional Vedic bodies
    like Arun, Varun, and Yama.
"""

from flatlib import const
from flatlib import angle
from flatlib.ephem import swe

def calculate_arun(jd):
    """
    Calculate the position of Arun (Charioteer of the Sun)
    
    Arun is calculated as Sun's longitude + 40°
    
    Args:
        jd (float): Julian day
        
    Returns:
        float: Longitude of Arun in degrees
    """
    # Get Sun's longitude
    sun_lon = swe.sweObjectLon(const.SUN, jd)
    
    # Calculate Arun
    arun_lon = angle.norm(sun_lon + 40)
    
    return arun_lon


def calculate_varun(jd):
    """
    Calculate the position of Varun (God of Water)
    
    Varun is calculated as Jupiter's longitude + 20°
    
    Args:
        jd (float): Julian day
        
    Returns:
        float: Longitude of Varun in degrees
    """
    # Get Jupiter's longitude
    jupiter_lon = swe.sweObjectLon(const.JUPITER, jd)
    
    # Calculate Varun
    varun_lon = angle.norm(jupiter_lon + 20)
    
    return varun_lon


def calculate_yama(jd):
    """
    Calculate the position of Yama (God of Death)
    
    Yama is calculated as Saturn's longitude + 30°
    
    Args:
        jd (float): Julian day
        
    Returns:
        float: Longitude of Yama in degrees
    """
    # Get Saturn's longitude
    saturn_lon = swe.sweObjectLon(const.SATURN, jd)
    
    # Calculate Yama
    yama_lon = angle.norm(saturn_lon + 30)
    
    return yama_lon


def get_vedic_body(body_id, jd):
    """
    Get the position of a Vedic body
    
    Args:
        body_id (str): The ID of the body (e.g., const.ARUN)
        jd (float): Julian day
        
    Returns:
        dict: Dictionary with body information
    """
    # Calculate the longitude based on the body ID
    if body_id == const.ARUN:
        longitude = calculate_arun(jd)
    elif body_id == const.VARUN:
        longitude = calculate_varun(jd)
    elif body_id == const.YAMA:
        longitude = calculate_yama(jd)
    else:
        raise ValueError(f"Unknown Vedic body: {body_id}")
    
    # Calculate sign and sign longitude
    sign_num = int(longitude / 30)
    sign = const.LIST_SIGNS[sign_num]
    sign_lon = longitude % 30
    
    return {
        'id': body_id,
        'lon': longitude,
        'lat': 0.0,  # Vedic bodies are calculated without latitude
        'sign': sign,
        'signlon': sign_lon,
        'type': const.OBJ_GENERIC
    }
