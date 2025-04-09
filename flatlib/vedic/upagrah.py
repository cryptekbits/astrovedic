"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements calculations for Upagrah (shadow planets)
    in Vedic astrology.
"""

import math
from flatlib import const
from flatlib import angle
from flatlib.datetime import Datetime

def calculate_gulika(jd, lat, lon):
    """
    Calculate the position of Gulika (Mandi)
    
    Gulika is the son of Saturn and is considered a shadow planet.
    Its position is calculated based on the day of the week and
    the duration of day or night.
    
    Args:
        jd (float): Julian day
        lat (float): Latitude in degrees
        lon (float): Longitude in degrees
        
    Returns:
        float: Longitude of Gulika in degrees
    """
    from flatlib.ephem import ephem
    
    # Get sunrise and sunset times
    date = Datetime.fromJD(jd)
    
    # Find the previous sunrise
    prev_sunrise = ephem.lastSunrise(date, (lat, lon))
    
    # Find the next sunset
    next_sunset = ephem.nextSunset(date, (lat, lon))
    
    # Find the next sunrise
    next_sunrise = ephem.nextSunrise(date, (lat, lon))
    
    # Determine if it's day or night
    is_day = prev_sunrise.jd <= jd < next_sunset.jd
    
    # Get day of week (0 = Sunday, 1 = Monday, etc.)
    day_of_week = date.date.weekday()
    
    # Saturn's hora (planetary hour) order for each day of the week
    # The index represents the day of the week (0 = Sunday, etc.)
    saturn_hora_order = [
        6,  # Sunday: 7th hora
        5,  # Monday: 6th hora
        4,  # Tuesday: 5th hora
        3,  # Wednesday: 4th hora
        2,  # Thursday: 3rd hora
        1,  # Friday: 2nd hora
        0   # Saturday: 1st hora
    ]
    
    # Get Saturn's hora for the current day
    saturn_hora = saturn_hora_order[day_of_week]
    
    if is_day:
        # Day time calculation
        day_duration = next_sunset.jd - prev_sunrise.jd
        hora_duration = day_duration / 12
        gulika_start = prev_sunrise.jd + (saturn_hora * hora_duration)
        gulika_end = gulika_start + hora_duration
    else:
        # Night time calculation
        night_duration = next_sunrise.jd - next_sunset.jd
        hora_duration = night_duration / 12
        gulika_start = next_sunset.jd + (saturn_hora * hora_duration)
        gulika_end = gulika_start + hora_duration
    
    # Calculate the middle point of Gulika's hora
    gulika_jd = (gulika_start + gulika_end) / 2
    
    # Get the longitude of the ascendant at this time
    from flatlib.ephem import swe
    houses, angles = swe.sweHouses(gulika_jd, lat, lon, const.HOUSES_PLACIDUS)
    
    # Return the longitude of the ascendant as Gulika's position
    return angles[0]['lon']


def calculate_mandi(jd, lat, lon):
    """
    Calculate the position of Mandi
    
    Mandi is another name for Gulika in some traditions.
    In some systems, they are calculated slightly differently.
    
    Args:
        jd (float): Julian day
        lat (float): Latitude in degrees
        lon (float): Longitude in degrees
        
    Returns:
        float: Longitude of Mandi in degrees
    """
    # In this implementation, Mandi is the same as Gulika
    return calculate_gulika(jd, lat, lon)


def calculate_dhuma(jd):
    """
    Calculate the position of Dhuma
    
    Dhuma (the smoky one) is calculated as:
    Dhuma = 360 - (Sun's longitude + 133°20')
    
    Args:
        jd (float): Julian day
        
    Returns:
        float: Longitude of Dhuma in degrees
    """
    from flatlib.ephem import swe
    
    # Get Sun's longitude
    sun_lon = swe.sweObjectLon(const.SUN, jd)
    
    # Calculate Dhuma
    dhuma_lon = angle.norm(360 - (sun_lon + 133 + (20/60)))
    
    return dhuma_lon


def calculate_vyatipata(jd):
    """
    Calculate the position of Vyatipata
    
    Vyatipata (calamity) is calculated as:
    Vyatipata = 360 - Dhuma
    
    Args:
        jd (float): Julian day
        
    Returns:
        float: Longitude of Vyatipata in degrees
    """
    dhuma_lon = calculate_dhuma(jd)
    vyatipata_lon = angle.norm(360 - dhuma_lon)
    
    return vyatipata_lon


def calculate_parivesha(jd):
    """
    Calculate the position of Parivesha
    
    Parivesha (halo) is calculated as:
    Parivesha = Vyatipata + 180°
    
    Args:
        jd (float): Julian day
        
    Returns:
        float: Longitude of Parivesha in degrees
    """
    vyatipata_lon = calculate_vyatipata(jd)
    parivesha_lon = angle.norm(vyatipata_lon + 180)
    
    return parivesha_lon


def calculate_indrachapa(jd):
    """
    Calculate the position of Indrachapa
    
    Indrachapa (rainbow) is calculated as:
    Indrachapa = Parivesha + 180°
    
    Args:
        jd (float): Julian day
        
    Returns:
        float: Longitude of Indrachapa in degrees
    """
    parivesha_lon = calculate_parivesha(jd)
    indrachapa_lon = angle.norm(parivesha_lon + 180)
    
    return indrachapa_lon


def calculate_upaketu(jd):
    """
    Calculate the position of Upaketu
    
    Upaketu (comet) is calculated as:
    Upaketu = Sun's longitude + 30°
    
    Args:
        jd (float): Julian day
        
    Returns:
        float: Longitude of Upaketu in degrees
    """
    from flatlib.ephem import swe
    
    # Get Sun's longitude
    sun_lon = swe.sweObjectLon(const.SUN, jd)
    
    # Calculate Upaketu
    upaketu_lon = angle.norm(sun_lon + 30)
    
    return upaketu_lon


def get_upagrah(upagrah_id, jd, lat=None, lon=None):
    """
    Get the position of an Upagrah (shadow planet)
    
    Args:
        upagrah_id (str): The ID of the upagrah (e.g., const.GULIKA)
        jd (float): Julian day
        lat (float, optional): Latitude in degrees (required for some upagrah)
        lon (float, optional): Longitude in degrees (required for some upagrah)
        
    Returns:
        dict: Dictionary with upagrah information
    """
    # Check if latitude and longitude are provided for upagrah that need them
    if upagrah_id in [const.GULIKA, const.MANDI] and (lat is None or lon is None):
        raise ValueError(f"{upagrah_id} calculation requires latitude and longitude")
    
    # Calculate the longitude based on the upagrah ID
    if upagrah_id == const.GULIKA:
        longitude = calculate_gulika(jd, lat, lon)
    elif upagrah_id == const.MANDI:
        longitude = calculate_mandi(jd, lat, lon)
    elif upagrah_id == const.DHUMA:
        longitude = calculate_dhuma(jd)
    elif upagrah_id == const.VYATIPATA:
        longitude = calculate_vyatipata(jd)
    elif upagrah_id == const.PARIVESHA:
        longitude = calculate_parivesha(jd)
    elif upagrah_id == const.INDRACHAPA:
        longitude = calculate_indrachapa(jd)
    elif upagrah_id == const.UPAKETU:
        longitude = calculate_upaketu(jd)
    else:
        raise ValueError(f"Unknown upagrah: {upagrah_id}")
    
    # Calculate sign and sign longitude
    sign_num = int(longitude / 30)
    sign = const.LIST_SIGNS[sign_num]
    sign_lon = longitude % 30
    
    return {
        'id': upagrah_id,
        'lon': longitude,
        'lat': 0.0,  # Upagrah are calculated without latitude
        'sign': sign,
        'signlon': sign_lon,
        'type': const.OBJ_SHADOW_PLANET
    }
