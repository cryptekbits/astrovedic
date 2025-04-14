"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module provides cached utility functions for Vedic astrology calculations.
    These functions are optimized versions of the functions in utils.py with caching.
"""

import math
import functools
from datetime import datetime, timedelta

from astrovedic import const
from astrovedic.datetime import Datetime
from astrovedic.chart import Chart
from astrovedic.vedic.exceptions import InputError, ValidationError
from astrovedic.cache import reference_cache, calculation_cache


@reference_cache()
def get_sign_lord(sign):
    """
    Get the lord (ruling planet) of a sign.
    
    Args:
        sign (str): The sign
    
    Returns:
        str: The lord (ruling planet)
    
    Raises:
        ValidationError: If the sign is invalid
    """
    # Define the lords for each sign
    lord_map = {
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
    
    if sign not in lord_map:
        raise ValidationError(f"Invalid sign: {sign}")
    
    return lord_map[sign]


@reference_cache()
def get_element(sign):
    """
    Get the element of a sign.
    
    Args:
        sign (str): The sign
    
    Returns:
        str: The element of the sign
    
    Raises:
        ValidationError: If the sign is invalid
    """
    elements = {
        const.ARIES: 'Fire',
        const.LEO: 'Fire',
        const.SAGITTARIUS: 'Fire',
        const.TAURUS: 'Earth',
        const.VIRGO: 'Earth',
        const.CAPRICORN: 'Earth',
        const.GEMINI: 'Air',
        const.LIBRA: 'Air',
        const.AQUARIUS: 'Air',
        const.CANCER: 'Water',
        const.SCORPIO: 'Water',
        const.PISCES: 'Water'
    }
    
    if sign not in elements:
        raise ValidationError(f"Invalid sign: {sign}")
    
    return elements[sign]


@reference_cache()
def get_quality(sign):
    """
    Get the quality (cardinal, fixed, mutable) of a sign.
    
    Args:
        sign (str): The sign
    
    Returns:
        str: The quality of the sign
    
    Raises:
        ValidationError: If the sign is invalid
    """
    qualities = {
        const.ARIES: 'Cardinal',
        const.CANCER: 'Cardinal',
        const.LIBRA: 'Cardinal',
        const.CAPRICORN: 'Cardinal',
        const.TAURUS: 'Fixed',
        const.LEO: 'Fixed',
        const.SCORPIO: 'Fixed',
        const.AQUARIUS: 'Fixed',
        const.GEMINI: 'Mutable',
        const.VIRGO: 'Mutable',
        const.SAGITTARIUS: 'Mutable',
        const.PISCES: 'Mutable'
    }
    
    if sign not in qualities:
        raise ValidationError(f"Invalid sign: {sign}")
    
    return qualities[sign]


@reference_cache()
def get_gender(sign):
    """
    Get the gender of a sign.
    
    Args:
        sign (str): The sign
    
    Returns:
        str: The gender of the sign
    
    Raises:
        ValidationError: If the sign is invalid
    """
    genders = {
        const.ARIES: const.MASCULINE,
        const.TAURUS: const.FEMININE,
        const.GEMINI: const.MASCULINE,
        const.CANCER: const.FEMININE,
        const.LEO: const.MASCULINE,
        const.VIRGO: const.FEMININE,
        const.LIBRA: const.MASCULINE,
        const.SCORPIO: const.FEMININE,
        const.SAGITTARIUS: const.MASCULINE,
        const.CAPRICORN: const.FEMININE,
        const.AQUARIUS: const.MASCULINE,
        const.PISCES: const.FEMININE
    }
    
    if sign not in genders:
        raise ValidationError(f"Invalid sign: {sign}")
    
    return genders[sign]


@reference_cache()
def get_planet_nature(planet_id):
    """
    Get the nature (benefic, malefic) of a planet.
    
    Args:
        planet_id (str): The ID of the planet
    
    Returns:
        str: The nature of the planet
    
    Raises:
        ValidationError: If the planet ID is invalid
    """
    natures = {
        const.SUN: 'Malefic',
        const.MOON: 'Benefic',
        const.MERCURY: 'Neutral',
        const.VENUS: 'Benefic',
        const.MARS: 'Malefic',
        const.JUPITER: 'Benefic',
        const.SATURN: 'Malefic',
        const.URANUS: 'Malefic',
        const.NEPTUNE: 'Malefic',
        const.PLUTO: 'Malefic',
        const.NORTH_NODE: 'Malefic',
        const.SOUTH_NODE: 'Malefic'
    }
    
    if planet_id not in natures:
        raise ValidationError(f"Invalid planet ID: {planet_id}")
    
    return natures[planet_id]


@reference_cache()
def get_planet_element(planet_id):
    """
    Get the element of a planet.
    
    Args:
        planet_id (str): The ID of the planet
    
    Returns:
        str: The element of the planet
    
    Raises:
        ValidationError: If the planet ID is invalid
    """
    elements = {
        const.SUN: 'Fire',
        const.MOON: 'Water',
        const.MERCURY: 'Earth',
        const.VENUS: 'Water',
        const.MARS: 'Fire',
        const.JUPITER: 'Ether',
        const.SATURN: 'Air',
        const.URANUS: 'Air',
        const.NEPTUNE: 'Water',
        const.PLUTO: 'Fire',
        const.NORTH_NODE: 'Air',
        const.SOUTH_NODE: 'Fire'
    }
    
    if planet_id not in elements:
        raise ValidationError(f"Invalid planet ID: {planet_id}")
    
    return elements[planet_id]


@reference_cache()
def get_planet_friendship(planet1, planet2):
    """
    Get the friendship between two planets.
    
    Args:
        planet1 (str): The first planet
        planet2 (str): The second planet
    
    Returns:
        str: The friendship status ('Friend', 'Enemy', 'Neutral')
    
    Raises:
        ValidationError: If either planet ID is invalid
    """
    # Define the friendship table
    friendship_table = {
        const.SUN: {
            'Friends': [const.MOON, const.MARS, const.JUPITER],
            'Enemies': [const.VENUS, const.SATURN],
            'Neutral': [const.MERCURY]
        },
        const.MOON: {
            'Friends': [const.SUN, const.MERCURY],
            'Enemies': [const.SATURN],
            'Neutral': [const.MARS, const.JUPITER, const.VENUS]
        },
        const.MERCURY: {
            'Friends': [const.SUN, const.VENUS],
            'Enemies': [const.MOON],
            'Neutral': [const.MARS, const.JUPITER, const.SATURN]
        },
        const.VENUS: {
            'Friends': [const.MERCURY, const.SATURN],
            'Enemies': [const.SUN, const.MOON],
            'Neutral': [const.MARS, const.JUPITER]
        },
        const.MARS: {
            'Friends': [const.SUN, const.MOON, const.JUPITER],
            'Enemies': [const.MERCURY],
            'Neutral': [const.VENUS, const.SATURN]
        },
        const.JUPITER: {
            'Friends': [const.SUN, const.MOON, const.MARS],
            'Enemies': [const.VENUS, const.MERCURY],
            'Neutral': [const.SATURN]
        },
        const.SATURN: {
            'Friends': [const.MERCURY, const.VENUS],
            'Enemies': [const.SUN, const.MOON, const.MARS],
            'Neutral': [const.JUPITER]
        }
    }
    
    # Add outer planets
    friendship_table[const.URANUS] = friendship_table[const.SATURN]
    friendship_table[const.NEPTUNE] = friendship_table[const.JUPITER]
    friendship_table[const.PLUTO] = friendship_table[const.MARS]
    friendship_table[const.NORTH_NODE] = friendship_table[const.JUPITER]
    friendship_table[const.SOUTH_NODE] = friendship_table[const.SATURN]
    
    # Validate planets
    if planet1 not in friendship_table:
        raise ValidationError(f"Invalid planet ID: {planet1}")
    if planet2 not in friendship_table:
        raise ValidationError(f"Invalid planet ID: {planet2}")
    
    # Get friendship status
    if planet2 in friendship_table[planet1]['Friends']:
        return 'Friend'
    elif planet2 in friendship_table[planet1]['Enemies']:
        return 'Enemy'
    else:
        return 'Neutral'


@reference_cache()
def get_planet_abbreviation(planet_id):
    """
    Get the abbreviation for a planet.
    
    Args:
        planet_id (str): The ID of the planet
    
    Returns:
        str: The abbreviation of the planet
    
    Raises:
        ValidationError: If the planet ID is invalid
    """
    abbreviations = {
        const.SUN: 'Sun',
        const.MOON: 'Moo',
        const.MERCURY: 'Mer',
        const.VENUS: 'Ven',
        const.MARS: 'Mar',
        const.JUPITER: 'Jup',
        const.SATURN: 'Sat',
        const.URANUS: 'Ura',
        const.NEPTUNE: 'Nep',
        const.PLUTO: 'Plu',
        const.NORTH_NODE: 'Rah',
        const.SOUTH_NODE: 'Ket'
    }
    
    if planet_id not in abbreviations:
        raise ValidationError(f"Invalid planet ID: {planet_id}")
    
    return abbreviations[planet_id]


@calculation_cache()
def normalize_longitude(longitude):
    """
    Normalize a longitude value to the range [0, 360).
    
    Args:
        longitude (float): The longitude to normalize
    
    Returns:
        float: The normalized longitude
    """
    return longitude % 360


@calculation_cache()
def get_sign_from_longitude(longitude):
    """
    Get the sign from a longitude.
    
    Args:
        longitude (float): The longitude in degrees (0-360)
    
    Returns:
        str: The sign
    """
    # Normalize the longitude
    lon = normalize_longitude(longitude)
    
    # Calculate the sign index (0-11)
    sign_index = int(lon / 30)
    
    # Return the sign
    return const.LIST_SIGNS[sign_index]


@calculation_cache()
def get_sign_number(sign):
    """
    Get the number of a sign (1-12).
    
    Args:
        sign (str): The sign
    
    Returns:
        int: The sign number (1-12)
    
    Raises:
        ValidationError: If the sign is invalid
    """
    try:
        return const.LIST_SIGNS.index(sign) + 1
    except ValueError:
        raise ValidationError(f"Invalid sign: {sign}")


@calculation_cache()
def get_sign_from_number(number):
    """
    Get the sign from a sign number (1-12).
    
    Args:
        number (int): The sign number (1-12)
    
    Returns:
        str: The sign
    
    Raises:
        ValidationError: If the number is invalid
    """
    if not isinstance(number, int) or number < 1 or number > 12:
        raise ValidationError(f"Invalid sign number: {number}")
    
    return const.LIST_SIGNS[number - 1]
