"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Arudha Pada calculations for Jaimini astrology.
    Arudha Padas are the externally visible manifestations of houses and planets.
"""

from typing import Dict, List, Optional, Tuple, Union
from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.object import GenericObject

# House numbers (1-12)
HOUSE_NUMBERS = list(range(1, 13))

# Arudha Pada names
LAGNA_PADA = "Lagna Pada"  # Arudha of 1st house (AL)
DHANA_PADA = "Dhana Pada"  # Arudha of 2nd house (A2)
BHRATRI_PADA = "Bhratri Pada"  # Arudha of 3rd house (A3)
MATRI_PADA = "Matri Pada"  # Arudha of 4th house (A4)
PUTRA_PADA = "Putra Pada"  # Arudha of 5th house (A5)
ROGA_PADA = "Roga Pada"  # Arudha of 6th house (A6)
DARA_PADA = "Dara Pada"  # Arudha of 7th house (A7)
MRITYU_PADA = "Mrityu Pada"  # Arudha of 8th house (A8)
BHAGYA_PADA = "Bhagya Pada"  # Arudha of 9th house (A9)
KARMA_PADA = "Karma Pada"  # Arudha of 10th house (A10)
LABHA_PADA = "Labha Pada"  # Arudha of 11th house (A11)
VYAYA_PADA = "Vyaya Pada"  # Arudha of 12th house (A12)

# Special Arudha Padas
UPAPADA_LAGNA = "Upapada Lagna"  # Special Arudha of 12th house (UL)

# Mapping of house numbers to Arudha Pada names
HOUSE_TO_ARUDHA = {
    1: LAGNA_PADA,
    2: DHANA_PADA,
    3: BHRATRI_PADA,
    4: MATRI_PADA,
    5: PUTRA_PADA,
    6: ROGA_PADA,
    7: DARA_PADA,
    8: MRITYU_PADA,
    9: BHAGYA_PADA,
    10: KARMA_PADA,
    11: LABHA_PADA,
    12: VYAYA_PADA
}

def get_sign_number(sign: str) -> int:
    """
    Get the number (1-12) of a sign.

    Args:
        sign (str): The sign name (e.g., 'Aries', 'Taurus', etc.)

    Returns:
        int: The sign number (1-12)
    """
    signs = [
        const.ARIES, const.TAURUS, const.GEMINI, const.CANCER,
        const.LEO, const.VIRGO, const.LIBRA, const.SCORPIO,
        const.SAGITTARIUS, const.CAPRICORN, const.AQUARIUS, const.PISCES
    ]
    return signs.index(sign) + 1

def get_sign_from_number(sign_num: int) -> str:
    """
    Get the sign name from a sign number (1-12).

    Args:
        sign_num (int): The sign number (1-12)

    Returns:
        str: The sign name (e.g., 'Aries', 'Taurus', etc.)
    """
    signs = [
        const.ARIES, const.TAURUS, const.GEMINI, const.CANCER,
        const.LEO, const.VIRGO, const.LIBRA, const.SCORPIO,
        const.SAGITTARIUS, const.CAPRICORN, const.AQUARIUS, const.PISCES
    ]
    return signs[(sign_num - 1) % 12]

def get_house_lord(chart: Chart, house_num: int) -> str:
    """
    Get the lord (ruling planet) of a house.

    Args:
        chart (Chart): The chart object
        house_num (int): The house number (1-12)

    Returns:
        str: The planet ID of the house lord
    """
    house = chart.getHouse(f'House{house_num}')
    sign = house.sign

    # Get the lord of the sign
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

    return sign_lords[sign]

def get_planet_sign(chart: Chart, planet_id: str) -> str:
    """
    Get the sign occupied by a planet.

    Args:
        chart (Chart): The chart object
        planet_id (str): The planet ID

    Returns:
        str: The sign occupied by the planet
    """
    planet = chart.getObject(planet_id)
    return planet.sign

def calculate_arudha_pada(chart: Chart, house_num: int) -> str:
    """
    Calculate the Arudha Pada (externally visible manifestation) of a house.

    The Arudha Pada is calculated as follows:
    1. Find the lord of the house
    2. Find the sign occupied by the lord
    3. Count the same number of signs from the lord's sign
    4. Apply special rules for the resulting sign

    Args:
        chart (Chart): The chart object
        house_num (int): The house number (1-12)

    Returns:
        str: The sign of the Arudha Pada
    """
    # Get the house sign
    house = chart.getHouse(f'House{house_num}')
    house_sign = house.sign
    house_sign_num = get_sign_number(house_sign)

    # Get the lord of the house
    lord = get_house_lord(chart, house_num)

    # Get the sign occupied by the lord
    lord_sign = get_planet_sign(chart, lord)
    lord_sign_num = get_sign_number(lord_sign)

    # Calculate the distance from house sign to lord sign
    distance = (lord_sign_num - house_sign_num) % 12
    if distance == 0:
        distance = 12

    # Count the same number of signs from the lord's sign
    arudha_sign_num = (lord_sign_num + distance) % 12
    if arudha_sign_num == 0:
        arudha_sign_num = 12

    # Apply special rules
    # Rule 1: If Arudha falls in the same sign as the house, take the 10th from it
    if arudha_sign_num == house_sign_num:
        arudha_sign_num = (arudha_sign_num + 9) % 12
        if arudha_sign_num == 0:
            arudha_sign_num = 12

    # Rule 2: If Arudha falls in the 7th from the house, take the 4th from the house
    elif arudha_sign_num == (house_sign_num + 6) % 12:
        arudha_sign_num = (house_sign_num + 3) % 12
        if arudha_sign_num == 0:
            arudha_sign_num = 12

    return get_sign_from_number(arudha_sign_num)

def calculate_all_arudha_padas(chart: Chart) -> Dict[str, str]:
    """
    Calculate all Arudha Padas for a chart.

    Args:
        chart (Chart): The chart object

    Returns:
        Dict[str, str]: A dictionary mapping Arudha Pada names to their signs
    """
    arudha_padas = {}

    for house_num in HOUSE_NUMBERS:
        arudha_name = HOUSE_TO_ARUDHA[house_num]
        arudha_sign = calculate_arudha_pada(chart, house_num)
        arudha_padas[arudha_name] = arudha_sign

    # Calculate special Arudha Padas
    # Upapada Lagna (UL) - Special calculation for the 12th house
    # In some traditions, UL is calculated differently from A12
    # Here we're using the standard A12 calculation for simplicity
    arudha_padas[UPAPADA_LAGNA] = arudha_padas[VYAYA_PADA]

    return arudha_padas

def calculate_graha_padas(chart: Chart) -> Dict[str, str]:
    """
    Calculate Graha Padas (Arudha of planets) for a chart.

    Args:
        chart (Chart): The chart object

    Returns:
        Dict[str, str]: A dictionary mapping planet names to their Graha Pada signs
    """
    graha_padas = {}

    # List of planets to calculate Graha Padas for
    planets = [
        const.SUN, const.MOON, const.MARS, const.MERCURY,
        const.JUPITER, const.VENUS, const.SATURN, const.RAHU, const.KETU
    ]

    for planet_id in planets:
        try:
            # Get the sign occupied by the planet
            planet = chart.getObject(planet_id)
            planet_sign = planet.sign
            planet_sign_num = get_sign_number(planet_sign)

            # Find all houses ruled by this planet
            ruled_houses = []
            for house_num in HOUSE_NUMBERS:
                house_lord = get_house_lord(chart, house_num)
                if house_lord == planet_id:
                    ruled_houses.append(house_num)

            # If the planet rules any houses, calculate its Graha Pada
            if ruled_houses:
                # Use the first house ruled by the planet
                house_num = ruled_houses[0]
                house = chart.getHouse(f'House{house_num}')
                house_sign = house.sign
                house_sign_num = get_sign_number(house_sign)

                # Calculate the distance from house sign to planet sign
                distance = (planet_sign_num - house_sign_num) % 12
                if distance == 0:
                    distance = 12

                # Count the same number of signs from the planet's sign
                pada_sign_num = (planet_sign_num + distance) % 12
                if pada_sign_num == 0:
                    pada_sign_num = 12

                # Apply special rules
                # Rule 1: If Pada falls in the same sign as the planet, take the 10th from it
                if pada_sign_num == planet_sign_num:
                    pada_sign_num = (pada_sign_num + 9) % 12
                    if pada_sign_num == 0:
                        pada_sign_num = 12

                # Rule 2: If Pada falls in the 7th from the planet, take the 4th from the planet
                elif pada_sign_num == (planet_sign_num + 6) % 12:
                    pada_sign_num = (planet_sign_num + 3) % 12
                    if pada_sign_num == 0:
                        pada_sign_num = 12

                graha_padas[planet_id] = get_sign_from_number(pada_sign_num)
            else:
                # For planets that don't rule any houses (like Rahu and Ketu)
                # Use their dispositor's Graha Pada
                dispositor = get_house_lord(chart, planet_sign_num)
                if dispositor in graha_padas:
                    graha_padas[planet_id] = graha_padas[dispositor]
                else:
                    # If dispositor's Pada is not calculated yet, use the planet's sign
                    graha_padas[planet_id] = planet_sign

        except (ValueError, AttributeError):
            # Skip planets that are not in the chart
            continue

    return graha_padas

def get_lagna_pada(chart: Chart) -> str:
    """
    Get the Lagna Pada (Arudha Lagna) for a chart.

    Args:
        chart (Chart): The chart object

    Returns:
        str: The sign of the Lagna Pada
    """
    return calculate_arudha_pada(chart, 1)

def get_upapada_lagna(chart: Chart) -> str:
    """
    Get the Upapada Lagna for a chart.

    Args:
        chart (Chart): The chart object

    Returns:
        str: The sign of the Upapada Lagna
    """
    # In some traditions, UL is calculated differently from A12
    # Here we're using the standard A12 calculation for simplicity
    return calculate_arudha_pada(chart, 12)
