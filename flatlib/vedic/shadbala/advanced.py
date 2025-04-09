"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements advanced strength calculations for Shadbala
    in Vedic astrology, including Ishta Phala, Kashta Phala, Vimsopaka Bala,
    and Bhava Bala.
"""

from flatlib import const
from flatlib import angle


def calculate_ishta_phala(chart, planet_id, total_shadbala):
    """
    Calculate Ishta Phala (beneficial effects) for a planet
    
    Ishta Phala represents the beneficial effects a planet can produce
    based on its strength and nature.
    
    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet to analyze
        total_shadbala (dict): The total Shadbala information
    
    Returns:
        dict: Dictionary with Ishta Phala information
    """
    # Get the planet from the chart
    planet = chart.getObject(planet_id)
    
    # Get the total Shadbala in Rupas
    shadbala_rupas = total_shadbala['total_rupas']
    
    # Benefic planets (Jupiter, Venus, Mercury, Moon)
    benefic_planets = [const.JUPITER, const.VENUS, const.MERCURY, const.MOON]
    
    # Malefic planets (Sun, Mars, Saturn, Rahu, Ketu)
    malefic_planets = [const.SUN, const.MARS, const.SATURN, const.RAHU, const.KETU]
    
    # Calculate the base Ishta Phala
    if planet_id in benefic_planets:
        # For benefic planets, Ishta Phala is proportional to strength
        base_value = shadbala_rupas
    elif planet_id in malefic_planets:
        # For malefic planets, Ishta Phala is inversely proportional to strength
        base_value = 5.0 - (shadbala_rupas - 5.0) if shadbala_rupas > 5.0 else shadbala_rupas
    else:
        base_value = shadbala_rupas / 2.0
    
    # Adjust based on the planet's position
    position_factor = calculate_position_factor(chart, planet_id)
    
    # Calculate the final Ishta Phala
    value = base_value * position_factor
    
    # Determine the description
    if value >= 40.0:
        description = 'Very high beneficial effects'
    elif value >= 30.0:
        description = 'High beneficial effects'
    elif value >= 20.0:
        description = 'Moderate beneficial effects'
    elif value >= 10.0:
        description = 'Low beneficial effects'
    else:
        description = 'Very low beneficial effects'
    
    return {
        'value': value,
        'description': description,
        'base_value': base_value,
        'position_factor': position_factor
    }


def calculate_kashta_phala(chart, planet_id, total_shadbala):
    """
    Calculate Kashta Phala (harmful effects) for a planet
    
    Kashta Phala represents the harmful effects a planet can produce
    based on its strength and nature.
    
    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet to analyze
        total_shadbala (dict): The total Shadbala information
    
    Returns:
        dict: Dictionary with Kashta Phala information
    """
    # Get the planet from the chart
    planet = chart.getObject(planet_id)
    
    # Get the total Shadbala in Rupas
    shadbala_rupas = total_shadbala['total_rupas']
    
    # Benefic planets (Jupiter, Venus, Mercury, Moon)
    benefic_planets = [const.JUPITER, const.VENUS, const.MERCURY, const.MOON]
    
    # Malefic planets (Sun, Mars, Saturn, Rahu, Ketu)
    malefic_planets = [const.SUN, const.MARS, const.SATURN, const.RAHU, const.KETU]
    
    # Calculate the base Kashta Phala
    if planet_id in benefic_planets:
        # For benefic planets, Kashta Phala is inversely proportional to strength
        base_value = 5.0 - (shadbala_rupas - 5.0) if shadbala_rupas > 5.0 else shadbala_rupas
    elif planet_id in malefic_planets:
        # For malefic planets, Kashta Phala is proportional to strength
        base_value = shadbala_rupas
    else:
        base_value = shadbala_rupas / 2.0
    
    # Adjust based on the planet's position
    position_factor = calculate_position_factor(chart, planet_id)
    
    # Calculate the final Kashta Phala
    value = base_value * position_factor
    
    # Determine the description
    if value >= 40.0:
        description = 'Very high harmful effects'
    elif value >= 30.0:
        description = 'High harmful effects'
    elif value >= 20.0:
        description = 'Moderate harmful effects'
    elif value >= 10.0:
        description = 'Low harmful effects'
    else:
        description = 'Very low harmful effects'
    
    return {
        'value': value,
        'description': description,
        'base_value': base_value,
        'position_factor': position_factor
    }


def calculate_position_factor(chart, planet_id):
    """
    Calculate a factor based on the planet's position in the chart
    
    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet
    
    Returns:
        float: A factor between 0.5 and 1.5
    """
    # Get the planet from the chart
    planet = chart.getObject(planet_id)
    
    # Get the Ascendant
    asc = chart.getAngle(const.ASC)
    
    # Calculate the house position of the planet (1-12)
    house_position = 1 + int(angle.distance(planet.lon, asc.lon) / 30)
    
    # Determine the house type
    if house_position in [1, 4, 7, 10]:
        # Kendra (angular) houses
        return 1.5
    elif house_position in [2, 5, 8, 11]:
        # Panapara (succedent) houses
        return 1.0
    else:
        # Apoklima (cadent) houses
        return 0.5


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
    from flatlib.vedic.vargas import (
        D1, D2, D3, D9, D12, D30,
        get_varga_chart
    )
    from flatlib.vedic.vargas.analysis import calculate_sign_strength
    
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
    
    Bhava Bala includes:
    1. Bhavadhipati Bala (house lord strength)
    2. Bhava Digbala (house directional strength)
    3. Bhava Drishti Bala (house aspect strength)
    4. Bhava Sthana Bala (house positional strength)
    
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
    bhava_digbala = calculate_bhava_digbala(house_num)
    bhava_drishti_bala = calculate_bhava_drishti_bala(chart, house_id)
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
    from flatlib.vedic.shadbala import get_shadbala
    lord_shadbala = get_shadbala(chart, sign_lord)
    
    # Bhavadhipati Bala is the Shadbala of the house lord
    value = lord_shadbala['total_shadbala']['total_virupas']
    
    return {
        'value': value,
        'description': f'Strength of house lord ({sign_lord})',
        'lord': sign_lord
    }


def calculate_bhava_digbala(house_num):
    """
    Calculate Bhava Digbala (house directional strength) for a house
    
    Args:
        house_num (int): The house number (1-12)
    
    Returns:
        dict: Dictionary with Bhava Digbala information
    """
    # Maximum value
    max_value = 60.0
    
    # Houses and their preferred directions
    # 1, 5, 9: East
    # 4, 8, 12: North
    # 7, 11, 3: West
    # 10, 2, 6: South
    
    if house_num in [1, 5, 9]:
        direction = 'East'
        value = max_value
    elif house_num in [4, 8, 12]:
        direction = 'North'
        value = max_value
    elif house_num in [7, 11, 3]:
        direction = 'West'
        value = max_value
    elif house_num in [10, 2, 6]:
        direction = 'South'
        value = max_value
    else:
        direction = 'Unknown'
        value = 0.0
    
    return {
        'value': value,
        'description': f'House in preferred direction ({direction})',
        'direction': direction
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
