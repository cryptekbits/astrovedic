"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology

    This module provides utility functions for Vedic astrology calculations.
"""

import functools
from datetime import timedelta

from flatlib import const
from flatlib.datetime import Datetime
from flatlib.chart import Chart
from flatlib.vedic.exceptions import InputError, ValidationError


# Caching decorator
def memoize(func):
    """
    Memoization decorator for caching function results.

    Args:
        func (function): The function to memoize

    Returns:
        function: The memoized function
    """
    cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create a key from the function arguments
        key = str(args) + str(kwargs)

        # Check if the result is already in the cache
        if key not in cache:
            # Calculate the result and store it in the cache
            cache[key] = func(*args, **kwargs)

        return cache[key]

    # Add a method to clear the cache
    wrapper.clear_cache = lambda: cache.clear()

    return wrapper


def validate_chart(chart):
    """
    Validate a chart object.

    Args:
        chart (Chart): The chart to validate

    Returns:
        Chart: The validated chart

    Raises:
        ValidationError: If the chart is invalid
    """
    if not isinstance(chart, Chart):
        raise ValidationError("Invalid chart object")

    # Check if the chart has the required attributes
    required_attrs = ['date', 'pos', 'houses', 'objects']
    for attr in required_attrs:
        if not hasattr(chart, attr):
            raise ValidationError(f"Chart missing required attribute: {attr}")

    return chart


def validate_planet(chart, planet_id):
    """
    Validate a planet ID and get the planet object.

    Args:
        chart (Chart): The chart
        planet_id (str): The ID of the planet

    Returns:
        Object: The planet object

    Raises:
        ValidationError: If the planet ID is invalid
        InputError: If the planet is not found in the chart
    """
    # Validate the chart
    validate_chart(chart)

    # Check if the planet ID is valid
    if planet_id not in const.LIST_OBJECTS_VEDIC:
        raise ValidationError(f"Invalid planet ID: {planet_id}")

    # Get the planet object
    planet = chart.getObject(planet_id)

    # Check if the planet was found
    if not planet:
        raise InputError(f"Planet not found in chart: {planet_id}")

    return planet


def validate_house(chart, house_num):
    """
    Validate a house number and get the house object.

    Args:
        chart (Chart): The chart
        house_num (int): The house number (1-12)

    Returns:
        Object: The house object

    Raises:
        ValidationError: If the house number is invalid
        InputError: If the house is not found in the chart
    """
    # Validate the chart
    validate_chart(chart)

    # Check if the house number is valid
    if not isinstance(house_num, int) or house_num < 1 or house_num > 12:
        raise ValidationError(f"Invalid house number: {house_num}")

    # Get the house object
    house = chart.getHouse(house_num)

    # Check if the house was found
    if not house:
        raise InputError(f"House not found in chart: {house_num}")

    return house


def validate_date(date):
    """
    Validate a date object.

    Args:
        date (Datetime): The date to validate

    Returns:
        Datetime: The validated date

    Raises:
        ValidationError: If the date is invalid
    """
    if not isinstance(date, Datetime):
        raise ValidationError("Invalid date object")

    return date


def normalize_longitude(longitude):
    """
    Normalize a longitude value to the range [0, 360).

    Args:
        longitude (float): The longitude to normalize

    Returns:
        float: The normalized longitude
    """
    return longitude % 360


def get_sign_from_longitude(longitude):
    """
    Get the sign from a longitude value.

    Args:
        longitude (float): The longitude

    Returns:
        str: The sign
    """
    # Normalize the longitude
    longitude = normalize_longitude(longitude)

    # Calculate the sign index (0-11)
    sign_index = int(longitude / 30)

    # Get the sign from the index
    signs = [
        const.ARIES, const.TAURUS, const.GEMINI, const.CANCER,
        const.LEO, const.VIRGO, const.LIBRA, const.SCORPIO,
        const.SAGITTARIUS, const.CAPRICORN, const.AQUARIUS, const.PISCES
    ]

    return signs[sign_index]


def get_sign_lord(sign):
    """
    Get the lord of a sign.

    Args:
        sign (str): The sign

    Returns:
        str: The sign lord
    """
    sign_lords = {
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

    return sign_lords.get(sign)


def get_sign_number(sign):
    """
    Get the number of a sign (1-12).

    Args:
        sign (str): The sign

    Returns:
        int: The sign number

    Raises:
        ValidationError: If the sign is invalid
    """
    sign_numbers = {
        const.ARIES: 1,
        const.TAURUS: 2,
        const.GEMINI: 3,
        const.CANCER: 4,
        const.LEO: 5,
        const.VIRGO: 6,
        const.LIBRA: 7,
        const.SCORPIO: 8,
        const.SAGITTARIUS: 9,
        const.CAPRICORN: 10,
        const.AQUARIUS: 11,
        const.PISCES: 12
    }

    if sign not in sign_numbers:
        raise ValidationError(f"Invalid sign: {sign}")

    return sign_numbers[sign]


def get_sign_from_number(sign_num):
    """
    Get the sign from a sign number (1-12).

    Args:
        sign_num (int): The sign number

    Returns:
        str: The sign

    Raises:
        ValidationError: If the sign number is invalid
    """
    if not isinstance(sign_num, int) or sign_num < 1 or sign_num > 12:
        raise ValidationError(f"Invalid sign number: {sign_num}")

    signs = [
        const.ARIES, const.TAURUS, const.GEMINI, const.CANCER,
        const.LEO, const.VIRGO, const.LIBRA, const.SCORPIO,
        const.SAGITTARIUS, const.CAPRICORN, const.AQUARIUS, const.PISCES
    ]

    return signs[sign_num - 1]


def get_planet_sign(chart, planet_id):
    """
    Get the sign of a planet.

    Args:
        chart (Chart): The chart
        planet_id (str): The ID of the planet

    Returns:
        str: The sign of the planet
    """
    # Validate and get the planet
    planet = validate_planet(chart, planet_id)

    return planet.sign


def get_planet_house(chart, planet_id):
    """
    Get the house of a planet.

    Args:
        chart (Chart): The chart
        planet_id (str): The ID of the planet

    Returns:
        int: The house number of the planet
    """
    # Validate and get the planet
    planet = validate_planet(chart, planet_id)

    # Get the sign of the planet
    planet_sign = planet.sign

    # Get the sign of the 1st house
    first_house = chart.getHouse(1)
    first_house_sign = first_house.sign

    # Calculate the house number
    sign_num = get_sign_number(planet_sign)
    first_house_sign_num = get_sign_number(first_house_sign)

    house_num = ((sign_num - first_house_sign_num) % 12) + 1

    return house_num


def get_house_sign(chart, house_num):
    """
    Get the sign of a house.

    Args:
        chart (Chart): The chart
        house_num (int): The house number

    Returns:
        str: The sign of the house
    """
    # Validate and get the house
    house = validate_house(chart, house_num)

    return house.sign


def get_house_lord(chart, house_num):
    """
    Get the lord of a house.

    Args:
        chart (Chart): The chart
        house_num (int): The house number

    Returns:
        str: The lord of the house
    """
    # Get the sign of the house
    house_sign = get_house_sign(chart, house_num)

    # Get the lord of the sign
    return get_sign_lord(house_sign)


def get_aspect(chart, planet1_id, planet2_id):
    """
    Get the aspect between two planets.

    Args:
        chart (Chart): The chart
        planet1_id (str): The ID of the first planet
        planet2_id (str): The ID of the second planet

    Returns:
        float: The aspect angle in degrees
    """
    # Validate and get the planets
    planet1 = validate_planet(chart, planet1_id)
    planet2 = validate_planet(chart, planet2_id)

    # Calculate the aspect angle
    angle = abs(planet1.lon - planet2.lon)

    # Normalize the angle to the range [0, 180]
    if angle > 180:
        angle = 360 - angle

    return angle


def is_retrograde(chart, planet_id):
    """
    Check if a planet is retrograde.

    Args:
        chart (Chart): The chart
        planet_id (str): The ID of the planet

    Returns:
        bool: True if the planet is retrograde, False otherwise
    """
    # Validate and get the planet
    planet = validate_planet(chart, planet_id)

    return planet.isRetrograde()


def get_planet_degree(chart, planet_id):
    """
    Get the degree of a planet within its sign.

    Args:
        chart (Chart): The chart
        planet_id (str): The ID of the planet

    Returns:
        float: The degree of the planet within its sign
    """
    # Validate and get the planet
    planet = validate_planet(chart, planet_id)

    # Calculate the degree within the sign
    return planet.lon % 30


def get_planet_nakshatra(chart, planet_id):
    """
    Get the nakshatra of a planet.

    Args:
        chart (Chart): The chart
        planet_id (str): The ID of the planet

    Returns:
        dict: Dictionary with nakshatra information
    """
    from flatlib.vedic.nakshatras import get_nakshatra

    # Validate and get the planet
    planet = validate_planet(chart, planet_id)

    return get_nakshatra(planet)


def get_planet_navamsa(chart, planet_id):
    """
    Get the navamsa (D-9) position of a planet.

    Args:
        chart (Chart): The chart
        planet_id (str): The ID of the planet

    Returns:
        str: The navamsa sign of the planet
    """
    from flatlib.vedic.vargas import get_varga_positions

    # Get the navamsa positions
    navamsa_positions = get_varga_positions(chart, 'D9')

    return navamsa_positions.get(planet_id, {}).get('sign')


def get_date_range(start_date, end_date, days=None):
    """
    Get a range of dates.

    Args:
        start_date (Datetime): The start date
        end_date (Datetime, optional): The end date
        days (int, optional): The number of days to include

    Returns:
        tuple: A tuple of (start_date, end_date)

    Raises:
        ValidationError: If the date range is invalid
    """
    # Validate the start date
    start_date = validate_date(start_date)

    # If end_date is not provided, use days
    if end_date is None:
        if days is None:
            days = 7  # Default to 7 days

        # Convert start_date to Python datetime
        start_datetime = start_date.datetime()

        # Calculate end_date
        end_datetime = start_datetime + timedelta(days=days)

        # Convert back to flatlib Datetime
        end_date = Datetime.fromDatetime(end_datetime)
    else:
        # Validate the end date
        end_date = validate_date(end_date)

        # Check if end_date is after start_date
        if end_date.datetime() <= start_date.datetime():
            raise ValidationError("End date must be after start date")

    return (start_date, end_date)


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


def get_gender(sign):
    """
    Get the gender (masculine, feminine) of a sign.

    Args:
        sign (str): The sign

    Returns:
        str: The gender of the sign

    Raises:
        ValidationError: If the sign is invalid
    """
    genders = {
        const.ARIES: 'Masculine',
        const.GEMINI: 'Masculine',
        const.LEO: 'Masculine',
        const.LIBRA: 'Masculine',
        const.SAGITTARIUS: 'Masculine',
        const.AQUARIUS: 'Masculine',
        const.TAURUS: 'Feminine',
        const.CANCER: 'Feminine',
        const.VIRGO: 'Feminine',
        const.SCORPIO: 'Feminine',
        const.CAPRICORN: 'Feminine',
        const.PISCES: 'Feminine'
    }

    if sign not in genders:
        raise ValidationError(f"Invalid sign: {sign}")

    return genders[sign]


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


def get_planet_friendship(planet1_id, planet2_id):
    """
    Get the friendship between two planets.

    Args:
        planet1_id (str): The ID of the first planet
        planet2_id (str): The ID of the second planet

    Returns:
        str: The friendship status ('Friend', 'Neutral', 'Enemy')

    Raises:
        ValidationError: If either planet ID is invalid
    """
    # Define planet friendships
    friendships = {
        const.SUN: {
            'Friends': [const.MOON, const.MARS, const.JUPITER],
            'Neutrals': [const.MERCURY],
            'Enemies': [const.VENUS, const.SATURN]
        },
        const.MOON: {
            'Friends': [const.SUN, const.MERCURY],
            'Neutrals': [const.MARS, const.JUPITER, const.VENUS, const.SATURN],
            'Enemies': []
        },
        const.MERCURY: {
            'Friends': [const.SUN, const.VENUS],
            'Neutrals': [const.MARS, const.JUPITER, const.SATURN],
            'Enemies': [const.MOON]
        },
        const.VENUS: {
            'Friends': [const.MERCURY, const.SATURN],
            'Neutrals': [const.MARS, const.JUPITER],
            'Enemies': [const.SUN, const.MOON]
        },
        const.MARS: {
            'Friends': [const.SUN, const.MOON, const.JUPITER],
            'Neutrals': [const.VENUS, const.SATURN],
            'Enemies': [const.MERCURY]
        },
        const.JUPITER: {
            'Friends': [const.SUN, const.MOON, const.MARS],
            'Neutrals': [const.SATURN],
            'Enemies': [const.MERCURY, const.VENUS]
        },
        const.SATURN: {
            'Friends': [const.MERCURY, const.VENUS],
            'Neutrals': [const.JUPITER],
            'Enemies': [const.SUN, const.MOON, const.MARS]
        }
    }

    # Check if the planet IDs are valid
    if planet1_id not in friendships:
        raise ValidationError(f"Invalid planet ID: {planet1_id}")

    if planet2_id not in friendships:
        raise ValidationError(f"Invalid planet ID: {planet2_id}")

    # Get the friendship status
    if planet2_id in friendships[planet1_id]['Friends']:
        return 'Friend'
    elif planet2_id in friendships[planet1_id]['Enemies']:
        return 'Enemy'
    else:
        return 'Neutral'


def get_planet_abbreviation(planet_id):
    """
    Get the abbreviation of a planet.

    Args:
        planet_id (str): The ID of the planet

    Returns:
        str: The abbreviation of the planet

    Raises:
        ValidationError: If the planet ID is invalid
    """
    abbreviations = {
        const.SUN: 'Su',
        const.MOON: 'Mo',
        const.MERCURY: 'Me',
        const.VENUS: 'Ve',
        const.MARS: 'Ma',
        const.JUPITER: 'Ju',
        const.SATURN: 'Sa',
        const.URANUS: 'Ur',
        const.NEPTUNE: 'Ne',
        const.PLUTO: 'Pl',
        const.NORTH_NODE: 'Ra',
        const.SOUTH_NODE: 'Ke'
    }

    if planet_id not in abbreviations:
        raise ValidationError(f"Invalid planet ID: {planet_id}")

    return abbreviations[planet_id]


def to_vedic_object(obj, chart=None):
    """
    Convert a regular object to a VedicBody object with Vedic attributes.

    Args:
        obj: The object to convert
        chart: The chart containing the object (optional, for context-dependent calculations)

    Returns:
        VedicBody: A VedicBody object with Vedic attributes
    """
    from flatlib.factory import AstronomicalObjectFactory
    from flatlib.vedic.nakshatras import get_nakshatra

    # Create a dictionary with the object's attributes
    data = obj.__dict__.copy()

    # Add Vedic-specific attributes

    # Add nakshatra information
    nakshatra_info = get_nakshatra(obj.lon)
    data['nakshatra'] = nakshatra_info['name']
    data['nakshatra_lord'] = nakshatra_info['lord']
    data['nakshatra_pada'] = nakshatra_info['pada']
    data['nakshatra_degree'] = obj.lon % (360/27)

    # Add Shadbala components if chart is provided
    if chart and obj.id in const.LIST_SEVEN_PLANETS:
        try:
            from flatlib.vedic.shadbala import get_shadbala
            shadbala_info = get_shadbala(chart, obj.id)
            data['sthana_bala'] = shadbala_info['sthana_bala']
            data['dig_bala'] = shadbala_info['dig_bala']
            data['kala_bala'] = shadbala_info['kala_bala']
            data['cheshta_bala'] = shadbala_info['cheshta_bala']
            data['naisargika_bala'] = shadbala_info['naisargika_bala']
            data['drig_bala'] = shadbala_info['drig_bala']
            data['total_shadbala'] = shadbala_info['total_shadbala']['total_rupas']
            data['ishta_phala'] = shadbala_info['ishta_phala']
            data['kashta_phala'] = shadbala_info['kashta_phala']
            data['vimsopaka_bala'] = shadbala_info['vimsopaka_bala']
        except (ImportError, Exception):
            # If shadbala calculation fails, continue without it
            pass

    # Add Varga positions if chart is provided
    if chart and obj.id in const.LIST_OBJECTS_VEDIC:
        try:
            from flatlib.vedic.vargas import get_varga_positions
            data['varga_positions'] = get_varga_positions(chart, obj.id)
        except (ImportError, Exception):
            # If varga calculation fails, continue without it
            pass

    # Create a VedicBody object
    return AstronomicalObjectFactory.create_vedic_object(data)


def to_vedic_chart(chart):
    """
    Convert a regular chart to a chart with VedicBody objects.

    Args:
        chart: The chart to convert

    Returns:
        Chart: A chart with VedicBody objects
    """
    # Create a copy of the chart
    vedic_chart = chart.copy()

    # Replace objects with VedicBody objects
    for obj_id in [const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS,
                  const.JUPITER, const.SATURN, const.RAHU, const.KETU]:
        if obj_id in vedic_chart.objects:
            obj = vedic_chart.getObject(obj_id)
            if obj:
                vedic_obj = to_vedic_object(obj, vedic_chart)
                vedic_chart.objects[obj_id] = vedic_obj

    return vedic_chart
