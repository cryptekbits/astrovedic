"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements calculations for Upagrah (shadow planets)
    in Vedic astrology.
"""

from astrovedic import const
from astrovedic import angle

def calculate_gulika(jd, lat=None, lon=None):
    """
    Calculate the position of Gulika (Mandi)

    Gulika is the son of Saturn and is considered a shadow planet.
    This is a simplified calculation based on Saturn's position.

    Args:
        jd (float): Julian day
        lat (float): Latitude in degrees
        lon (float): Longitude in degrees

    Returns:
        float: Longitude of Gulika in degrees
    """
    from astrovedic.ephem import swe

    # Get Saturn's longitude
    saturn_lon = swe.sweObjectLon(const.SATURN, jd)

    # Calculate Gulika as Saturn + 40°
    gulika_lon = angle.norm(saturn_lon + 40)

    return gulika_lon


def calculate_mandi(jd, lat=None, lon=None):
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
    from astrovedic.ephem import swe

    # Get Saturn's longitude
    saturn_lon = swe.sweObjectLon(const.SATURN, jd)

    # Calculate Mandi as Saturn + 30°
    mandi_lon = angle.norm(saturn_lon + 30)

    return mandi_lon


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
    from astrovedic.ephem import swe

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
    from astrovedic.ephem import swe

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


def get_gulika(chart):
    """
    Get Gulika from a chart

    Args:
        chart (Chart): The chart

    Returns:
        dict: Dictionary with Gulika information
    """
    return get_upagrah(const.GULIKA, chart.date.jd, chart.pos.lat, chart.pos.lon)


def get_mandi(chart):
    """
    Get Mandi from a chart

    Args:
        chart (Chart): The chart

    Returns:
        dict: Dictionary with Mandi information
    """
    return get_upagrah(const.MANDI, chart.date.jd, chart.pos.lat, chart.pos.lon)


def get_upagrah_positions(chart):
    """
    Get all Upagrah positions from a chart

    Args:
        chart (Chart): The chart

    Returns:
        dict: Dictionary with all Upagrah positions
    """
    positions = {}

    for upagrah_id in [const.GULIKA, const.MANDI, const.DHUMA, const.VYATIPATA,
                      const.PARIVESHA, const.INDRACHAPA, const.UPAKETU]:
        positions[upagrah_id] = get_upagrah(upagrah_id, chart.date.jd, chart.pos.lat, chart.pos.lon)

    return positions
