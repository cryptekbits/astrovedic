"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements advanced strength calculations for Shadbala
    in Vedic astrology, including Ishta Phala, Kashta Phala, Vimsopaka Bala,
    and Bhava Bala.
"""

from astrovedic import const
from astrovedic import angle
import math
from astrovedic import const
from astrovedic.angle import closestdistance

def calculate_ishta_phala(uchcha_bala_value: float, cheshta_bala_value: float) -> dict:
    """
    Calculate Ishta Phala (beneficial potential) for a planet.

    Ishta Phala represents the beneficial potential based on the planet's
    exaltation strength (Uchcha Bala) and motional strength (Cheshta Bala).
    The standard formula is sqrt(Uchcha Bala * Cheshta Bala).

    Args:
        uchcha_bala_value (float): The Uchcha Bala value (0-60 Virupas).
        cheshta_bala_value (float): The Cheshta Bala value (0-60 Virupas).
                                    (For Sun/Moon, use full Ayana/Paksha Bala).

    Returns:
        dict: Dictionary with Ishta Phala value and description.

    Raises:
        ValueError: If input values are outside the 0-60 range.
    """
    # Validate inputs
    if not (0 <= uchcha_bala_value <= 60) or not (0 <= cheshta_bala_value <= 60):
        raise ValueError("Uchcha Bala and Cheshta Bala values must be between 0 and 60.")

    # Calculate Ishta Phala using the standard formula
    # Handle potential domain error if product is negative (though validation should prevent this)
    try:
        value = math.sqrt(uchcha_bala_value * cheshta_bala_value)
    except ValueError:
        # This should not happen with validated inputs, but as a safeguard
        value = 0.0

    # Provide a simple description
    if value >= 45.0:
        description = 'Very High (Auspicious Potential)'
    elif value >= 30.0:
        description = 'High (Auspicious Potential)'
    elif value >= 15.0:
        description = 'Moderate (Auspicious Potential)'
    else:
        description = 'Low (Auspicious Potential)'

    return {
        'value': value,  # Value range 0-60
        'description': description
    }


def calculate_kashta_phala(uchcha_bala_value: float, cheshta_bala_value: float) -> dict:
    """
    Calculate Kashta Phala (malefic potential) for a planet.

    Kashta Phala represents the malefic potential based on the planet's
    proximity to debilitation and lack of motional strength.
    The standard formula is sqrt((60 - Uchcha Bala) * (60 - Cheshta Bala)).

    Args:
        uchcha_bala_value (float): The Uchcha Bala value (0-60 Virupas).
        cheshta_bala_value (float): The Cheshta Bala value (0-60 Virupas).
                                    (For Sun/Moon, use full Ayana/Paksha Bala).

    Returns:
        dict: Dictionary with Kashta Phala value and description.

    Raises:
        ValueError: If input values are outside the 0-60 range.
    """
    # Validate inputs
    if not (0 <= uchcha_bala_value <= 60) or not (0 <= cheshta_bala_value <= 60):
        raise ValueError("Uchcha Bala and Cheshta Bala values must be between 0 and 60.")

    # Calculate Kashta Phala using the standard formula
    # Handle potential domain error if product is negative (though validation should prevent this)
    try:
        value = math.sqrt((60.0 - uchcha_bala_value) * (60.0 - cheshta_bala_value))
    except ValueError:
        # This should not happen with validated inputs, but as a safeguard
        value = 0.0

    # Provide a simple description
    if value >= 45.0:
        description = 'Very High (Inauspicious Potential)'
    elif value >= 30.0:
        description = 'High (Inauspicious Potential)'
    elif value >= 15.0:
        description = 'Moderate (Inauspicious Potential)'
    else:
        description = 'Low (Inauspicious Potential)'

    return {
        'value': value,  # Value range 0-60
        'description': description
    }


def calculate_vimsopaka_bala(chart, planet_id):
    """
    Calculate Vimsopaka Bala (twenty-fold strength) for a planet

    Vimsopaka Bala is calculated based on the planet's position in
    various divisional charts.

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet to analyze

    Returns:
        dict: Dictionary with Vimsopaka Bala information
    """
    # Import the necessary functions from the vargas module
    from astrovedic.vedic.vargas import (
        D1, D2, D3, D9, D12, D30,
        get_varga_chart
    )
    from astrovedic.vedic.vargas.analysis import calculate_sign_strength

    # Get the planet's sign in each divisional chart
    d1_sign = chart.getObject(planet_id).sign
    d2_sign = get_varga_chart(chart, D2).getObject(planet_id).sign
    d3_sign = get_varga_chart(chart, D3).getObject(planet_id).sign
    d9_sign = get_varga_chart(chart, D9).getObject(planet_id).sign
    d12_sign = get_varga_chart(chart, D12).getObject(planet_id).sign
    d30_sign = get_varga_chart(chart, D30).getObject(planet_id).sign

    # Calculate the strength in each divisional chart
    d1_strength = calculate_sign_strength(planet_id, d1_sign)
    d2_strength = calculate_sign_strength(planet_id, d2_sign)
    d3_strength = calculate_sign_strength(planet_id, d3_sign)
    d9_strength = calculate_sign_strength(planet_id, d9_sign)
    d12_strength = calculate_sign_strength(planet_id, d12_sign)
    d30_strength = calculate_sign_strength(planet_id, d30_sign)

    # Calculate the Vimsopaka Bala
    # The weights for each divisional chart are:
    # D1: 6, D2: 2, D3: 4, D9: 5, D12: 2, D30: 1
    value = (
        d1_strength * 6.0 +
        d2_strength * 2.0 +
        d3_strength * 4.0 +
        d9_strength * 5.0 +
        d12_strength * 2.0 +
        d30_strength * 1.0
    )

    # Maximum possible value is 20 (if all charts have strength 1.0)
    max_value = 20.0

    # Scale to a percentage
    percentage = (value / max_value) * 100.0

    # Determine the description
    if percentage >= 75.0:
        description = 'Very strong'
    elif percentage >= 50.0:
        description = 'Strong'
    elif percentage >= 25.0:
        description = 'Moderate'
    else:
        description = 'Weak'

    return {
        'value': value,
        'percentage': percentage,
        'description': description,
        'd1_strength': d1_strength,
        'd2_strength': d2_strength,
        'd3_strength': d3_strength,
        'd9_strength': d9_strength,
        'd12_strength': d12_strength,
        'd30_strength': d30_strength
    }


def calculate_bhava_bala(chart, house_id):
    """
    Calculate Bhava Bala (house strength) for a house

    Bhava Bala includes the standard components:
    1. Bhavadhipati Bala (house lord strength)
    2. Bhava Digbala (house directional strength)
    3. Bhava Drishti Bala (house aspect strength)

    Args:
        chart (Chart): The birth chart
        house_id (str): The ID of the house to analyze

    Returns:
        dict: Dictionary with Bhava Bala information
    """
    # Get the house from the chart
    house = chart.getHouse(house_id)

    # Get the house number (1-12)
    house_num = int(house_id.replace('House', ''))

    # Calculate each component of Bhava Bala
    bhavadhipati_bala = calculate_bhavadhipati_bala(chart, house_id)
    bhava_digbala = calculate_bhava_digbala(chart, house_id)
    bhava_drishti_bala = calculate_bhava_drishti_bala(chart, house_id)

    # Calculate Bhava Sthana Bala
    bhava_sthana_bala = calculate_bhava_sthana_bala(house_num)

    # Calculate total Bhava Bala
    total = (bhavadhipati_bala['value'] + bhava_digbala['value'] +
             bhava_drishti_bala['value'] + bhava_sthana_bala['value'])

    # Determine the description
    if total >= 500.0:
        description = 'Very strong house'
    elif total >= 400.0:
        description = 'Strong house'
    elif total >= 300.0:
        description = 'Moderate house'
    elif total >= 200.0:
        description = 'Weak house'
    else:
        description = 'Very weak house'

    return {
        'house': house_id,
        'bhavadhipati_bala': bhavadhipati_bala,
        'bhava_digbala': bhava_digbala,
        'bhava_drishti_bala': bhava_drishti_bala,
        'bhava_sthana_bala': bhava_sthana_bala,
        'total': total,
        'description': description
    }


def calculate_bhavadhipati_bala(chart, house_id):
    """
    Calculate Bhavadhipati Bala (house lord strength) for a house

    Args:
        chart (Chart): The birth chart
        house_id (str): The ID of the house

    Returns:
        dict: Dictionary with Bhavadhipati Bala information
    """
    # Get the house from the chart
    house = chart.getHouse(house_id)

    # Get the sign of the house
    house_sign = house.sign

    # Get the lord of the sign
    sign_lord = get_sign_lord(house_sign)

    # Get the Shadbala of the lord
    from astrovedic.vedic.shadbala import get_shadbala
    lord_shadbala = get_shadbala(chart, sign_lord)

    # Bhavadhipati Bala is the Shadbala of the house lord
    value = lord_shadbala['total_shadbala']['total_virupas']

    return {
        'value': value,
        'description': f'Strength of house lord ({sign_lord})',
        'lord': sign_lord
    }


def calculate_bhava_digbala(chart, house_id):
    """
    Calculate Bhava Digbala (house directional strength) for a house
    based on its cusp's proximity to the directional strength point.

    Args:
        chart (Chart): The birth chart
        house_id (str): The ID of the house (e.g., 'House1')

    Returns:
        dict: Dictionary with Bhava Digbala information
    """
    # Maximum value
    max_value = 60.0

    # Get house number and cusp longitude
    try:
        house_num = int(house_id.replace(const.HOUSE, ''))
        house_cusp_lon = chart.getHouse(house_id).lon
    except (ValueError, AttributeError):
        # Handle cases where house_id is invalid or house doesn't exist
        return {'value': 0.0, 'description': 'Invalid house ID', 'direction': 'Unknown'}

    # Determine the directional point and its longitude
    if house_num in [1, 5, 9]: # East Houses
        direction = 'East'
        target_lon = chart.getHouse(const.HOUSE1).lon
    elif house_num in [4, 8, 12]: # North Houses
        direction = 'North'
        target_lon = chart.getHouse(const.HOUSE4).lon
    elif house_num in [7, 11, 3]: # West Houses
        direction = 'West'
        target_lon = chart.getHouse(const.HOUSE7).lon
    elif house_num in [10, 2, 6]: # South Houses
        direction = 'South'
        target_lon = chart.getHouse(const.HOUSE10).lon
    else: # Should not happen for valid house_num 1-12
        return {'value': 0.0, 'description': 'Unknown house number', 'direction': 'Unknown'}

    # Calculate the shortest distance
    distance = closestdistance(house_cusp_lon, target_lon)

    # Calculate Dig Bala value
    # Strength decreases linearly from max_value at 0 distance to 0 at 180 distance
    value = max_value * (1 - distance / 180.0)
    value = max(0.0, value) # Ensure value is not negative

    description = f'Strength based on distance from {direction} point ({target_lon:.2f}°)'

    return {
        'value': value,
        'description': description,
        'direction': direction,
        'target_point_lon': target_lon,
        'cusp_lon': house_cusp_lon,
        'distance': distance
    }


def calculate_bhava_drishti_bala(chart, house_id):
    """
    Calculate Bhava Drishti Bala (house aspect strength) for a house

    Args:
        chart (Chart): The birth chart
        house_id (str): The ID of the house

    Returns:
        dict: Dictionary with Bhava Drishti Bala information
    """
    # Get the house from the chart
    house = chart.getHouse(house_id)

    # Get the house number (1-12)
    house_num = int(house_id.replace('House', ''))

    # Initialize the aspect value
    aspect_value = 0.0

    # List of aspects received
    aspects = []

    # Check aspects from each planet
    for planet_id in const.LIST_OBJECTS_VEDIC:
        planet = chart.getObject(planet_id)

        # Calculate the aspect strength
        aspect_strength = calculate_vedic_aspect_to_house(planet_id, planet.lon, house.lon)

        if aspect_strength > 0:
            # Determine if the aspect is benefic or malefic
            is_benefic = is_benefic_planet(planet_id)

            # Benefic aspects increase strength, malefic aspects decrease it
            if is_benefic:
                aspect_value += aspect_strength
            else:
                aspect_value -= aspect_strength

            # Add to the list of aspects
            aspects.append({
                'planet': planet_id,
                'strength': aspect_strength,
                'is_benefic': is_benefic
            })

    # Ensure the value is not negative
    aspect_value = max(0.0, aspect_value)

    return {
        'value': aspect_value,
        'description': 'Strength from planetary aspects',
        'aspects': aspects
    }


def calculate_bhava_sthana_bala(house_num):
    """
    Calculate Bhava Sthana Bala (house positional strength) for a house

    Args:
        house_num (int): The house number (1-12)

    Returns:
        dict: Dictionary with Bhava Sthana Bala information
    """
    # Maximum value
    max_value = 60.0

    # Kendra (angular) houses: 1, 4, 7, 10
    # Trikona (trine) houses: 1, 5, 9
    # Dusthana (malefic) houses: 6, 8, 12

    if house_num in [1, 5, 9]:
        # Trikona houses
        value = max_value
        description = 'Trikona (trine) house'
    elif house_num in [4, 7, 10]:
        # Kendra houses (excluding 1st house, which is already counted as Trikona)
        value = max_value * 0.75
        description = 'Kendra (angular) house'
    elif house_num in [2, 11]:
        # Upachaya houses (excluding 10th house, which is already counted as Kendra)
        value = max_value * 0.5
        description = 'Upachaya (increasing) house'
    elif house_num == 3:
        # 3rd house is mixed
        value = max_value * 0.25
        description = 'Mixed house'
    else:
        # Dusthana houses
        value = 0.0
        description = 'Dusthana (malefic) house'

    return {
        'value': value,
        'description': description
    }


def calculate_vedic_aspect_to_house(planet_id, planet_lon, house_lon):
    """
    Calculate the strength of a Vedic aspect to a house

    Args:
        planet_id (str): The ID of the planet casting the aspect
        planet_lon (float): The longitude of the planet
        house_lon (float): The longitude of the house

    Returns:
        float: The strength of the aspect (0-10)
    """
    # Calculate the distance in houses (0-11)
    distance = int(angle.distance(planet_lon, house_lon) / 30) % 12

    # All planets aspect the 7th house
    if distance == 6:
        return 10.0

    # Special aspects for Mars, Jupiter, and Saturn
    if planet_id == const.MARS and distance in [3, 7]:
        return 10.0
    elif planet_id == const.JUPITER and distance in [4, 8]:
        return 10.0
    elif planet_id == const.SATURN and distance in [2, 9]:
        return 10.0

    # No aspect
    return 0.0


def is_benefic_planet(planet_id):
    """
    Determine if a planet is benefic or malefic

    Args:
        planet_id (str): The ID of the planet

    Returns:
        bool: True if the planet is benefic, False if malefic
    """
    # Benefic planets
    benefic_planets = [const.JUPITER, const.VENUS, const.MERCURY, const.MOON]

    # Malefic planets
    malefic_planets = [const.SUN, const.MARS, const.SATURN, const.RAHU, const.KETU]

    return planet_id in benefic_planets


def get_sign_lord(sign):
    """
    Get the lord (ruler) of a sign

    Args:
        sign (str): The sign

    Returns:
        str: The ID of the planet ruling the sign
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

    return sign_lords.get(sign, const.SUN)
