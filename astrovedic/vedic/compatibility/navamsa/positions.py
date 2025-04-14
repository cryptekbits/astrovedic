"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Navamsa positions for compatibility analysis
    in Vedic astrology.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos

from astrovedic.vedic.compatibility.navamsa.helpers import get_navamsa_sign, get_navamsa_longitude


def get_navamsa_positions(chart):
    """
    Get the Navamsa positions for a chart

    Args:
        chart (Chart): The chart

    Returns:
        dict: Dictionary with Navamsa positions
    """
    # Initialize the positions
    positions = {}

    # Get the Navamsa positions for each planet
    for planet_id in const.LIST_OBJECTS_VEDIC:
        # Get the planet
        planet = chart.getObject(planet_id)

        # Get the Navamsa sign and longitude
        navamsa_sign = get_navamsa_sign(planet.lon)
        navamsa_lon = get_navamsa_longitude(planet.lon)

        # Add to positions
        positions[planet_id] = {
            'sign': navamsa_sign,
            'longitude': navamsa_lon,
            'retrograde': hasattr(planet, 'isRetrograde') and planet.isRetrograde()
        }

    # Get the Navamsa positions for the angles
    for angle_id in [const.ASC, const.MC, const.DESC, const.IC]:
        # Get the angle
        angle = chart.getAngle(angle_id)

        # Get the Navamsa sign and longitude
        navamsa_sign = get_navamsa_sign(angle.lon)
        navamsa_lon = get_navamsa_longitude(angle.lon)

        # Add to positions
        positions[angle_id] = {
            'sign': navamsa_sign,
            'longitude': navamsa_lon
        }

    return positions


def get_navamsa_house_positions(chart):
    """
    Get the Navamsa house positions for a chart

    Args:
        chart (Chart): The chart

    Returns:
        dict: Dictionary with Navamsa house positions
    """
    # Get the Navamsa positions
    positions = get_navamsa_positions(chart)

    # Get the Navamsa Ascendant
    navamsa_asc = positions[const.ASC]

    # Get the Navamsa Ascendant sign
    navamsa_asc_sign = navamsa_asc['sign']

    # Get the Navamsa Ascendant sign number (0-11)
    navamsa_asc_sign_num = const.LIST_SIGNS.index(navamsa_asc_sign)

    # Initialize the house positions
    house_positions = {}

    # Calculate the house positions for each planet
    for planet_id, position in positions.items():
        # Skip angles
        if planet_id in [const.ASC, const.MC, const.DESC, const.IC]:
            continue

        # Get the sign
        sign = position['sign']

        # Get the sign number (0-11)
        sign_num = const.LIST_SIGNS.index(sign)

        # Calculate the house position
        house_position = ((sign_num - navamsa_asc_sign_num) % 12) + 1

        # Add to house positions
        house_positions[planet_id] = house_position

    return house_positions


def get_navamsa_sign_lords(chart):
    """
    Get the Navamsa sign lords for a chart

    Args:
        chart (Chart): The chart

    Returns:
        dict: Dictionary with Navamsa sign lords
    """
    # Get the Navamsa positions
    positions = get_navamsa_positions(chart)

    # Initialize the sign lords
    sign_lords = {}

    # Define the sign lords
    sign_lord_map = {
        const.ARIES: const.MARS,
        const.TAURUS: const.VENUS,
        const.GEMINI: const.MERCURY,
        const.CANCER: const.MOON,
        const.LEO: const.SUN,
        const.VIRGO: const.MERCURY,
        const.LIBRA: const.VENUS,
        const.SCORPIO: const.MARS,
        const.SAGITTARIUS: const.JUPITER,
        const.CAPRICORN: const.SATURN,
        const.AQUARIUS: const.SATURN,
        const.PISCES: const.JUPITER
    }

    # Calculate the sign lords for each planet
    for planet_id, position in positions.items():
        # Get the sign
        sign = position['sign']

        # Get the sign lord
        sign_lord = sign_lord_map.get(sign, 'Unknown')

        # Add to sign lords
        sign_lords[planet_id] = sign_lord

    return sign_lords


def get_navamsa_exaltation_debilitation(chart):
    """
    Get the Navamsa exaltation and debilitation status for a chart

    Args:
        chart (Chart): The chart

    Returns:
        dict: Dictionary with Navamsa exaltation and debilitation status
    """
    # Get the Navamsa positions
    positions = get_navamsa_positions(chart)

    # Initialize the status
    status = {}

    # Define the exaltation and debilitation signs
    exaltation_signs = {
        const.SUN: const.ARIES,
        const.MOON: const.TAURUS,
        const.MARS: const.CAPRICORN,
        const.MERCURY: const.VIRGO,
        const.JUPITER: const.CANCER,
        const.VENUS: const.PISCES,
        const.SATURN: const.LIBRA,
        const.RAHU: const.GEMINI,
        const.KETU: const.SAGITTARIUS
    }

    debilitation_signs = {
        const.SUN: const.LIBRA,
        const.MOON: const.SCORPIO,
        const.MARS: const.CANCER,
        const.MERCURY: const.PISCES,
        const.JUPITER: const.CAPRICORN,
        const.VENUS: const.VIRGO,
        const.SATURN: const.ARIES,
        const.RAHU: const.SAGITTARIUS,
        const.KETU: const.GEMINI
    }

    # Calculate the status for each planet
    for planet_id, position in positions.items():
        # Skip angles
        if planet_id in [const.ASC, const.MC, const.DESC, const.IC]:
            continue

        # Get the sign
        sign = position['sign']

        # Check exaltation
        is_exalted = sign == exaltation_signs.get(planet_id, None)

        # Check debilitation
        is_debilitated = sign == debilitation_signs.get(planet_id, None)

        # Add to status
        status[planet_id] = {
            'is_exalted': is_exalted,
            'is_debilitated': is_debilitated
        }

    return status
