"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Sthana Bala (positional strength) calculations
    for Shadbala in Vedic astrology.
"""

from flatlib import const
from flatlib import angle


def calculate_sthana_bala(chart, planet_id):
    """
    Calculate Sthana Bala (positional strength) for a planet
    
    Sthana Bala includes:
    1. Uchcha Bala (exaltation strength)
    2. Saptavarga Bala (strength in divisional charts)
    3. Ojha-Yugma Bala (odd-even sign strength)
    4. Kendradi Bala (quadrant strength)
    5. Drekkana Bala (decanate strength)
    
    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet to analyze
    
    Returns:
        dict: Dictionary with Sthana Bala information
    """
    # Get the planet from the chart
    planet = chart.getObject(planet_id)
    
    # Calculate each component of Sthana Bala
    uchcha_bala = calculate_uchcha_bala(planet_id, planet.lon)
    saptavarga_bala = calculate_saptavarga_bala(chart, planet_id)
    ojha_yugma_bala = calculate_ojha_yugma_bala(planet_id, planet.sign)
    kendradi_bala = calculate_kendradi_bala(chart, planet_id)
    drekkana_bala = calculate_drekkana_bala(planet_id, planet.lon)
    
    # Calculate total Sthana Bala
    total = (uchcha_bala['value'] + saptavarga_bala['value'] + 
             ojha_yugma_bala['value'] + kendradi_bala['value'] + 
             drekkana_bala['value'])
    
    return {
        'planet': planet_id,
        'uchcha_bala': uchcha_bala,
        'saptavarga_bala': saptavarga_bala,
        'ojha_yugma_bala': ojha_yugma_bala,
        'kendradi_bala': kendradi_bala,
        'drekkana_bala': drekkana_bala,
        'total': total
    }


def calculate_uchcha_bala(planet_id, longitude):
    """
    Calculate Uchcha Bala (exaltation strength) for a planet
    
    Args:
        planet_id (str): The ID of the planet
        longitude (float): The longitude of the planet
    
    Returns:
        dict: Dictionary with Uchcha Bala information
    """
    # Exaltation and debilitation points for each planet
    exaltation_points = {
        const.SUN: 10.0,      # 10° Aries
        const.MOON: 33.0,     # 3° Taurus
        const.MERCURY: 165.0, # 15° Virgo
        const.VENUS: 357.0,   # 27° Pisces
        const.MARS: 298.0,    # 28° Capricorn
        const.JUPITER: 95.0,  # 5° Cancer
        const.SATURN: 200.0,  # 20° Libra
        const.RAHU: 50.0,     # 20° Taurus (some traditions)
        const.KETU: 230.0     # 20° Scorpio (some traditions)
    }
    
    debilitation_points = {
        const.SUN: 190.0,     # 10° Libra
        const.MOON: 213.0,    # 3° Scorpio
        const.MERCURY: 345.0, # 15° Pisces
        const.VENUS: 165.0,   # 15° Virgo
        const.MARS: 95.0,     # 5° Cancer
        const.JUPITER: 275.0, # 5° Capricorn
        const.SATURN: 20.0,   # 20° Aries
        const.RAHU: 230.0,    # 20° Scorpio (some traditions)
        const.KETU: 50.0      # 20° Taurus (some traditions)
    }
    
    # Maximum Uchcha Bala value (in Virupas)
    max_value = 60.0
    
    # If the planet is not in the list, return 0
    if planet_id not in exaltation_points:
        return {'value': 0.0, 'description': 'Not applicable'}
    
    # Get exaltation and debilitation points
    exaltation_point = exaltation_points[planet_id]
    debilitation_point = debilitation_points[planet_id]
    
    # Calculate the distance from the exaltation point
    distance_from_exaltation = angle.distance(longitude, exaltation_point)
    
    # Calculate the distance from the debilitation point
    distance_from_debilitation = angle.distance(longitude, debilitation_point)
    
    # Calculate Uchcha Bala
    if distance_from_exaltation <= 180:
        # Planet is moving from exaltation to debilitation
        value = max_value * (1 - distance_from_exaltation / 180.0)
    else:
        # Planet is moving from debilitation to exaltation
        value = max_value * (distance_from_debilitation / 180.0)
    
    # Determine the description
    if distance_from_exaltation == 0:
        description = 'Exalted'
    elif distance_from_debilitation == 0:
        description = 'Debilitated'
    elif distance_from_exaltation < distance_from_debilitation:
        description = 'Closer to exaltation'
    else:
        description = 'Closer to debilitation'
    
    return {'value': value, 'description': description}


def calculate_saptavarga_bala(chart, planet_id):
    """
    Calculate Saptavarga Bala (strength in divisional charts) for a planet
    
    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet
    
    Returns:
        dict: Dictionary with Saptavarga Bala information
    """
    # For now, we'll use a simplified approach
    # In a full implementation, we would calculate the strength in each of the
    # seven divisional charts (D1, D2, D3, D7, D9, D12, D30)
    
    # Import the necessary functions from the vargas module
    from flatlib.vedic.vargas import (
        D1, D2, D3, D7, D9, D12, D30,
        get_varga_chart
    )
    from flatlib.vedic.vargas.analysis import calculate_sign_strength
    
    # Get the planet's sign in each divisional chart
    d1_sign = chart.getObject(planet_id).sign
    d2_sign = get_varga_chart(chart, D2).getObject(planet_id).sign
    d3_sign = get_varga_chart(chart, D3).getObject(planet_id).sign
    d7_sign = get_varga_chart(chart, D7).getObject(planet_id).sign
    d9_sign = get_varga_chart(chart, D9).getObject(planet_id).sign
    d12_sign = get_varga_chart(chart, D12).getObject(planet_id).sign
    d30_sign = get_varga_chart(chart, D30).getObject(planet_id).sign
    
    # Calculate the strength in each divisional chart
    d1_strength = calculate_sign_strength(planet_id, d1_sign)
    d2_strength = calculate_sign_strength(planet_id, d2_sign)
    d3_strength = calculate_sign_strength(planet_id, d3_sign)
    d7_strength = calculate_sign_strength(planet_id, d7_sign)
    d9_strength = calculate_sign_strength(planet_id, d9_sign)
    d12_strength = calculate_sign_strength(planet_id, d12_sign)
    d30_strength = calculate_sign_strength(planet_id, d30_sign)
    
    # Calculate the total Saptavarga Bala
    # The weights for each divisional chart are:
    # D1: 5, D2: 2, D3: 3, D7: 2.5, D9: 4.5, D12: 2, D30: 1
    total_strength = (
        d1_strength * 5.0 +
        d2_strength * 2.0 +
        d3_strength * 3.0 +
        d7_strength * 2.5 +
        d9_strength * 4.5 +
        d12_strength * 2.0 +
        d30_strength * 1.0
    )
    
    # Maximum possible value is 20 (if all charts have strength 1.0)
    max_value = 20.0
    
    # Scale to Virupas (maximum 30)
    value = (total_strength / max_value) * 30.0
    
    return {
        'value': value,
        'description': 'Strength in seven divisional charts',
        'd1_strength': d1_strength,
        'd2_strength': d2_strength,
        'd3_strength': d3_strength,
        'd7_strength': d7_strength,
        'd9_strength': d9_strength,
        'd12_strength': d12_strength,
        'd30_strength': d30_strength
    }


def calculate_ojha_yugma_bala(planet_id, sign):
    """
    Calculate Ojha-Yugma Bala (odd-even sign strength) for a planet
    
    Args:
        planet_id (str): The ID of the planet
        sign (str): The sign of the planet
    
    Returns:
        dict: Dictionary with Ojha-Yugma Bala information
    """
    # Get the sign number (0-11)
    sign_num = {
        const.ARIES: 0, const.TAURUS: 1, const.GEMINI: 2, const.CANCER: 3,
        const.LEO: 4, const.VIRGO: 5, const.LIBRA: 6, const.SCORPIO: 7,
        const.SAGITTARIUS: 8, const.CAPRICORN: 9, const.AQUARIUS: 10, const.PISCES: 11
    }[sign]
    
    # Determine if the sign is odd or even
    is_odd_sign = (sign_num % 2 == 0)  # 0-based, so even indices are odd signs
    
    # Planets that prefer odd signs
    odd_sign_planets = [const.SUN, const.MARS, const.JUPITER, const.MERCURY]
    
    # Planets that prefer even signs
    even_sign_planets = [const.MOON, const.VENUS, const.SATURN]
    
    # Rahu and Ketu don't have a preference
    
    # Determine if the planet is in its preferred sign type
    if planet_id in odd_sign_planets and is_odd_sign:
        value = 15.0
        description = 'In preferred odd sign'
    elif planet_id in even_sign_planets and not is_odd_sign:
        value = 15.0
        description = 'In preferred even sign'
    elif planet_id in odd_sign_planets and not is_odd_sign:
        value = 0.0
        description = 'Not in preferred odd sign'
    elif planet_id in even_sign_planets and is_odd_sign:
        value = 0.0
        description = 'Not in preferred even sign'
    else:
        value = 7.5  # Half strength for Rahu and Ketu
        description = 'No preference for odd/even signs'
    
    return {'value': value, 'description': description}


def calculate_kendradi_bala(chart, planet_id):
    """
    Calculate Kendradi Bala (quadrant strength) for a planet
    
    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet
    
    Returns:
        dict: Dictionary with Kendradi Bala information
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
        value = 60.0
        description = 'In Kendra (angular) house'
    elif house_position in [2, 5, 8, 11]:
        # Panapara (succedent) houses
        value = 30.0
        description = 'In Panapara (succedent) house'
    else:
        # Apoklima (cadent) houses
        value = 15.0
        description = 'In Apoklima (cadent) house'
    
    return {'value': value, 'description': description}


def calculate_drekkana_bala(planet_id, longitude):
    """
    Calculate Drekkana Bala (decanate strength) for a planet
    
    Args:
        planet_id (str): The ID of the planet
        longitude (float): The longitude of the planet
    
    Returns:
        dict: Dictionary with Drekkana Bala information
    """
    # Get the sign longitude (0-30)
    sign_lon = longitude % 30
    
    # Determine the decanate (0, 1, or 2)
    decanate = int(sign_lon / 10)
    
    # Male planets (Sun, Mars, Jupiter) get strength in the first decanate
    male_planets = [const.SUN, const.MARS, const.JUPITER]
    
    # Female planets (Moon, Venus) get strength in the second decanate
    female_planets = [const.MOON, const.VENUS]
    
    # Neutral planets (Mercury, Saturn, Rahu, Ketu) get strength in the third decanate
    neutral_planets = [const.MERCURY, const.SATURN, const.RAHU, const.KETU]
    
    # Determine the strength based on the planet and decanate
    if (planet_id in male_planets and decanate == 0) or \
       (planet_id in female_planets and decanate == 1) or \
       (planet_id in neutral_planets and decanate == 2):
        value = 15.0
        description = 'In preferred decanate'
    else:
        value = 0.0
        description = 'Not in preferred decanate'
    
    return {'value': value, 'description': description}
