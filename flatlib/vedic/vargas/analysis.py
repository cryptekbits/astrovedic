"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements analysis tools for Varga (divisional chart) calculations
    in Vedic astrology, including Varga Visesha (special divisional chart strengths)
    and other strength calculations.
"""

from flatlib import const
from flatlib.chart import Chart
from flatlib.vedic.vargas import (
    D1, D2, D3, D4, D7, D9, D10, D12,
    D16, D20, D24, D27, D30, D40, D45, D60,
    get_varga_chart
)


def get_varga_visesha(chart, planet_id):
    """
    Calculate Varga Visesha (special divisional chart strengths) for a planet

    Varga Visesha is calculated based on the position of a planet in multiple divisional charts:
    - Parijatamsha: Same sign in D1 and D9
    - Uttamamsha: Same sign in D1, D2, and D9
    - Gopuramsha: Same sign in D1, D2, D3, and D9
    - Simhasanamsha: Same sign in D1, D2, D3, D9, and D12
    - Paravatamsha: Same sign in D1, D2, D3, D9, D12, and D30
    - Devalokamsha: Same sign in D1, D2, D3, D4, D9, D12, and D30
    - Brahmalokamsha: Same sign in D1, D2, D3, D4, D9, D12, D16, and D30

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet to analyze

    Returns:
        dict: Dictionary with Varga Visesha information
    """
    # Get the planet from the birth chart
    planet = chart.getObject(planet_id)

    # Get the sign of the planet in the birth chart
    birth_sign = planet.sign

    # Get the signs in various divisional charts
    d1_sign = birth_sign  # Same as birth chart
    d2_sign = get_varga_chart(chart, D2).getObject(planet_id).sign
    d3_sign = get_varga_chart(chart, D3).getObject(planet_id).sign
    d4_sign = get_varga_chart(chart, D4).getObject(planet_id).sign
    d9_sign = get_varga_chart(chart, D9).getObject(planet_id).sign
    d12_sign = get_varga_chart(chart, D12).getObject(planet_id).sign
    d16_sign = get_varga_chart(chart, D16).getObject(planet_id).sign
    d30_sign = get_varga_chart(chart, D30).getObject(planet_id).sign

    # Check for Varga Visesha conditions
    parijatamsha = (d1_sign == d9_sign)
    uttamamsha = parijatamsha and (d1_sign == d2_sign)
    gopuramsha = uttamamsha and (d1_sign == d3_sign)
    simhasanamsha = gopuramsha and (d1_sign == d12_sign)
    paravatamsha = simhasanamsha and (d1_sign == d30_sign)
    devalokamsha = paravatamsha and (d1_sign == d4_sign)
    brahmalokamsha = devalokamsha and (d1_sign == d16_sign)

    # Determine the highest Varga Visesha
    if brahmalokamsha:
        highest = "Brahmalokamsha"
    elif devalokamsha:
        highest = "Devalokamsha"
    elif paravatamsha:
        highest = "Paravatamsha"
    elif simhasanamsha:
        highest = "Simhasanamsha"
    elif gopuramsha:
        highest = "Gopuramsha"
    elif uttamamsha:
        highest = "Uttamamsha"
    elif parijatamsha:
        highest = "Parijatamsha"
    else:
        highest = None

    return {
        'planet': planet_id,
        'parijatamsha': parijatamsha,
        'uttamamsha': uttamamsha,
        'gopuramsha': gopuramsha,
        'simhasanamsha': simhasanamsha,
        'paravatamsha': paravatamsha,
        'devalokamsha': devalokamsha,
        'brahmalokamsha': brahmalokamsha,
        'highest': highest
    }


def get_shadvarga_bala(chart, planet_id):
    """
    Calculate Shadvarga Bala (six divisional chart strength) for a planet

    Shadvarga Bala is calculated based on the position of a planet in six divisional charts:
    D1, D2, D3, D9, D12, and D30

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet to analyze

    Returns:
        dict: Dictionary with Shadvarga Bala information
    """
    # Get the planet from the birth chart
    planet = chart.getObject(planet_id)

    # Get the signs in various divisional charts
    d1_sign = planet.sign
    d2_sign = get_varga_chart(chart, D2).getObject(planet_id).sign
    d3_sign = get_varga_chart(chart, D3).getObject(planet_id).sign
    d9_sign = get_varga_chart(chart, D9).getObject(planet_id).sign
    d12_sign = get_varga_chart(chart, D12).getObject(planet_id).sign
    d30_sign = get_varga_chart(chart, D30).getObject(planet_id).sign

    # Calculate the strength in each divisional chart
    # (This is a simplified version; a more complex calculation would consider
    # exaltation, debilitation, own sign, friendly sign, etc.)

    # Get the signs ruled by the planet
    planet_signs = get_ruled_signs(planet_id)

    # Calculate strength in each divisional chart
    d1_strength = calculate_sign_strength(planet_id, d1_sign)
    d2_strength = calculate_sign_strength(planet_id, d2_sign)
    d3_strength = calculate_sign_strength(planet_id, d3_sign)
    d9_strength = calculate_sign_strength(planet_id, d9_sign)
    d12_strength = calculate_sign_strength(planet_id, d12_sign)
    d30_strength = calculate_sign_strength(planet_id, d30_sign)

    # Calculate total strength
    total_strength = d1_strength + d2_strength + d3_strength + d9_strength + d12_strength + d30_strength

    return {
        'planet': planet_id,
        'd1_strength': d1_strength,
        'd2_strength': d2_strength,
        'd3_strength': d3_strength,
        'd9_strength': d9_strength,
        'd12_strength': d12_strength,
        'd30_strength': d30_strength,
        'total_strength': total_strength
    }


def get_saptavarga_bala(chart, planet_id):
    """
    Calculate Saptavarga Bala (seven divisional chart strength) for a planet

    Saptavarga Bala is calculated based on the position of a planet in seven divisional charts:
    D1, D2, D3, D7, D9, D12, and D30

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet to analyze

    Returns:
        dict: Dictionary with Saptavarga Bala information
    """
    # Get the planet from the birth chart
    planet = chart.getObject(planet_id)

    # Get the signs in various divisional charts
    d1_sign = planet.sign
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
    d12_strength = calculate_sign_strength(planet_id, d12_strength)
    d30_strength = calculate_sign_strength(planet_id, d30_sign)

    # Calculate total strength
    total_strength = d1_strength + d2_strength + d3_strength + d7_strength + d9_strength + d12_strength + d30_strength

    return {
        'planet': planet_id,
        'd1_strength': d1_strength,
        'd2_strength': d2_strength,
        'd3_strength': d3_strength,
        'd7_strength': d7_strength,
        'd9_strength': d9_strength,
        'd12_strength': d12_strength,
        'd30_strength': d30_strength,
        'total_strength': total_strength
    }


def get_dashavarga_bala(chart, planet_id):
    """
    Calculate Dashavarga Bala (ten divisional chart strength) for a planet

    Dashavarga Bala is calculated based on the position of a planet in ten divisional charts:
    D1, D2, D3, D4, D7, D9, D10, D12, D16, and D30

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet to analyze

    Returns:
        dict: Dictionary with Dashavarga Bala information
    """
    # Get the planet from the birth chart
    planet = chart.getObject(planet_id)

    # Get the signs in various divisional charts
    d1_sign = planet.sign
    d2_sign = get_varga_chart(chart, D2).getObject(planet_id).sign
    d3_sign = get_varga_chart(chart, D3).getObject(planet_id).sign
    d4_sign = get_varga_chart(chart, D4).getObject(planet_id).sign
    d7_sign = get_varga_chart(chart, D7).getObject(planet_id).sign
    d9_sign = get_varga_chart(chart, D9).getObject(planet_id).sign
    d10_sign = get_varga_chart(chart, D10).getObject(planet_id).sign
    d12_sign = get_varga_chart(chart, D12).getObject(planet_id).sign
    d16_sign = get_varga_chart(chart, D16).getObject(planet_id).sign
    d30_sign = get_varga_chart(chart, D30).getObject(planet_id).sign

    # Calculate the strength in each divisional chart
    d1_strength = calculate_sign_strength(planet_id, d1_sign)
    d2_strength = calculate_sign_strength(planet_id, d2_sign)
    d3_strength = calculate_sign_strength(planet_id, d3_sign)
    d4_strength = calculate_sign_strength(planet_id, d4_sign)
    d7_strength = calculate_sign_strength(planet_id, d7_sign)
    d9_strength = calculate_sign_strength(planet_id, d9_sign)
    d10_strength = calculate_sign_strength(planet_id, d10_sign)
    d12_strength = calculate_sign_strength(planet_id, d12_sign)
    d16_strength = calculate_sign_strength(planet_id, d16_sign)
    d30_strength = calculate_sign_strength(planet_id, d30_sign)

    # Calculate total strength
    total_strength = (
        d1_strength + d2_strength + d3_strength + d4_strength + d7_strength +
        d9_strength + d10_strength + d12_strength + d16_strength + d30_strength
    )

    return {
        'planet': planet_id,
        'd1_strength': d1_strength,
        'd2_strength': d2_strength,
        'd3_strength': d3_strength,
        'd4_strength': d4_strength,
        'd7_strength': d7_strength,
        'd9_strength': d9_strength,
        'd10_strength': d10_strength,
        'd12_strength': d12_strength,
        'd16_strength': d16_strength,
        'd30_strength': d30_strength,
        'total_strength': total_strength
    }


def get_shodashavarga_bala(chart, planet_id):
    """
    Calculate Shodashavarga Bala (sixteen divisional chart strength) for a planet

    Shodashavarga Bala is calculated based on the position of a planet in all sixteen divisional charts

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet to analyze

    Returns:
        dict: Dictionary with Shodashavarga Bala information
    """
    # Get the planet from the birth chart
    planet = chart.getObject(planet_id)

    # Get the signs in all divisional charts
    strengths = {}
    total_strength = 0

    for varga in [D1, D2, D3, D4, D7, D9, D10, D12, D16, D20, D24, D27, D30, D40, D45, D60]:
        varga_sign = get_varga_chart(chart, varga).getObject(planet_id).sign
        strength = calculate_sign_strength(planet_id, varga_sign)
        strengths[varga] = strength
        total_strength += strength

    # Add total strength to the dictionary
    strengths['total_strength'] = total_strength
    strengths['planet'] = planet_id

    return strengths


def calculate_sign_strength(planet_id, sign):
    """
    Calculate the strength of a planet in a sign

    Args:
        planet_id (str): The ID of the planet
        sign (str): The sign to analyze

    Returns:
        float: The strength of the planet in the sign
    """
    # Get the signs ruled by the planet
    ruled_signs = get_ruled_signs(planet_id)

    # Get exaltation and debilitation signs
    exaltation_signs = get_exaltation_signs(planet_id)
    debilitation_signs = get_debilitation_signs(planet_id)

    # Get friendly and enemy signs
    friendly_signs = get_friendly_signs(planet_id)
    enemy_signs = get_enemy_signs(planet_id)

    # Calculate strength
    if sign in exaltation_signs:
        return 1.0  # Exalted
    elif sign in ruled_signs:
        return 0.75  # Own sign
    elif sign in friendly_signs:
        return 0.5  # Friendly sign
    elif sign in enemy_signs:
        return 0.25  # Enemy sign
    elif sign in debilitation_signs:
        return 0.0  # Debilitated
    else:
        return 0.375  # Neutral sign


def get_ruled_signs(planet_id):
    """
    Get the signs ruled by a planet

    Args:
        planet_id (str): The ID of the planet

    Returns:
        list: List of signs ruled by the planet
    """
    ruled_signs = {
        const.SUN: [const.LEO],
        const.MOON: [const.CANCER],
        const.MERCURY: [const.GEMINI, const.VIRGO],
        const.VENUS: [const.TAURUS, const.LIBRA],
        const.MARS: [const.ARIES, const.SCORPIO],
        const.JUPITER: [const.SAGITTARIUS, const.PISCES],
        const.SATURN: [const.CAPRICORN, const.AQUARIUS],
        const.RAHU: [],  # Rahu doesn't rule any sign in traditional astrology
        const.KETU: []   # Ketu doesn't rule any sign in traditional astrology
    }

    return ruled_signs.get(planet_id, [])


def get_exaltation_signs(planet_id):
    """
    Get the exaltation sign(s) of a planet

    Args:
        planet_id (str): The ID of the planet

    Returns:
        list: List of exaltation signs for the planet
    """
    exaltation_signs = {
        const.SUN: [const.ARIES],
        const.MOON: [const.TAURUS],
        const.MERCURY: [const.VIRGO],  # Some traditions say Virgo
        const.VENUS: [const.PISCES],
        const.MARS: [const.CAPRICORN],
        const.JUPITER: [const.CANCER],
        const.SATURN: [const.LIBRA],
        const.RAHU: [const.TAURUS],  # In some traditions
        const.KETU: [const.SCORPIO]  # In some traditions
    }

    return exaltation_signs.get(planet_id, [])


def get_debilitation_signs(planet_id):
    """
    Get the debilitation sign(s) of a planet

    Args:
        planet_id (str): The ID of the planet

    Returns:
        list: List of debilitation signs for the planet
    """
    debilitation_signs = {
        const.SUN: [const.LIBRA],
        const.MOON: [const.SCORPIO],
        const.MERCURY: [const.PISCES],
        const.VENUS: [const.VIRGO],
        const.MARS: [const.CANCER],
        const.JUPITER: [const.CAPRICORN],
        const.SATURN: [const.ARIES],
        const.RAHU: [const.SCORPIO],  # In some traditions
        const.KETU: [const.TAURUS]    # In some traditions
    }

    return debilitation_signs.get(planet_id, [])


def get_friendly_signs(planet_id):
    """
    Get the friendly signs for a planet

    Args:
        planet_id (str): The ID of the planet

    Returns:
        list: List of friendly signs for the planet
    """
    # This is a simplified version; a more accurate version would consider
    # temporary friendships based on the birth chart

    friendly_planets = {
        const.SUN: [const.MOON, const.MARS, const.JUPITER],
        const.MOON: [const.SUN, const.MERCURY],
        const.MERCURY: [const.SUN, const.VENUS],
        const.VENUS: [const.MERCURY, const.SATURN],
        const.MARS: [const.SUN, const.MOON, const.JUPITER],
        const.JUPITER: [const.SUN, const.MOON, const.MARS],
        const.SATURN: [const.MERCURY, const.VENUS],
        const.RAHU: [const.VENUS, const.SATURN],
        const.KETU: [const.VENUS, const.SATURN]
    }

    friendly_signs = []
    for friend in friendly_planets.get(planet_id, []):
        friendly_signs.extend(get_ruled_signs(friend))

    return friendly_signs


def get_enemy_signs(planet_id):
    """
    Get the enemy signs for a planet

    Args:
        planet_id (str): The ID of the planet

    Returns:
        list: List of enemy signs for the planet
    """
    # This is a simplified version; a more accurate version would consider
    # temporary enmities based on the birth chart

    enemy_planets = {
        const.SUN: [const.SATURN, const.VENUS],
        const.MOON: [const.SATURN],
        const.MERCURY: [const.MOON],
        const.VENUS: [const.SUN, const.MOON],
        const.MARS: [const.MERCURY],
        const.JUPITER: [const.MERCURY, const.VENUS],
        const.SATURN: [const.SUN, const.MOON, const.MARS],
        const.RAHU: [const.SUN, const.MOON, const.MARS],
        const.KETU: [const.SUN, const.MOON, const.MARS]
    }

    enemy_signs = []
    for enemy in enemy_planets.get(planet_id, []):
        enemy_signs.extend(get_ruled_signs(enemy))

    return enemy_signs


def get_varga_strength(chart, planet_id):
    """
    Get the strength of a planet in all divisional charts

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet

    Returns:
        dict: Dictionary with varga strength information
    """
    # Get the Shodashavarga Bala (16 divisional chart strength)
    shodashavarga = get_shodashavarga_bala(chart, planet_id)

    # Calculate the normalized strength (0-100)
    max_possible_strength = 16.0  # Maximum possible strength if exalted in all 16 vargas
    normalized_strength = min(100, (shodashavarga['total_strength'] / max_possible_strength) * 100)

    # Get the Varga Visesha
    varga_visesha = get_varga_visesha(chart, planet_id)

    return {
        'planet': planet_id,
        'shodashavarga_bala': shodashavarga,
        'varga_visesha': varga_visesha,
        'normalized_strength': normalized_strength
    }


def get_shad_bala(chart, planet_id):
    """
    Get the Shad Bala (six-fold strength) of a planet

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet

    Returns:
        dict: Dictionary with Shad Bala information
    """
    # This is an alias for get_shadvarga_bala
    return get_shadvarga_bala(chart, planet_id)


def get_shad_varga_bala(chart, planet_id):
    """
    Get the Shad Varga Bala (six divisional chart strength) of a planet

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet

    Returns:
        dict: Dictionary with Shad Varga Bala information
    """
    # This is an alias for get_shadvarga_bala
    return get_shadvarga_bala(chart, planet_id)


def get_vimshopaka_bala(chart, planet_id):
    """
    Get the Vimshopaka Bala (20-point strength) of a planet

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet

    Returns:
        dict: Dictionary with Vimshopaka Bala information
    """
    # Get the Shodashavarga Bala
    shodashavarga = get_shodashavarga_bala(chart, planet_id)

    # Calculate the Vimshopaka Bala (20-point strength)
    # Different divisional charts have different weights
    weights = {
        D1: 3.5,  # Rashi
        D2: 1.0,  # Hora
        D3: 1.0,  # Drekkana
        D4: 0.5,  # Chaturthamsha
        D7: 0.5,  # Saptamsha
        D9: 3.0,  # Navamsha
        D10: 2.0,  # Dashamsha
        D12: 0.5,  # Dwadashamsha
        D16: 1.0,  # Shodashamsha
        D20: 0.5,  # Vimshamsha
        D24: 0.5,  # Chaturvimshamsha
        D27: 0.5,  # Saptavimshamsha
        D30: 1.0,  # Trimshamsha
        D40: 1.5,  # Khavedamsha
        D45: 1.5,  # Akshavedamsha
        D60: 1.5   # Shashtiamsha
    }

    # Calculate the weighted strength
    vimshopaka_bala = 0.0
    for varga, weight in weights.items():
        if varga in shodashavarga:
            vimshopaka_bala += shodashavarga[varga] * weight

    return {
        'planet': planet_id,
        'vimshopaka_bala': vimshopaka_bala,
        'max_possible': 20.0,
        'percentage': (vimshopaka_bala / 20.0) * 100
    }


def get_bhava_bala(chart, house_num):
    """
    Get the strength of a house in all divisional charts

    Args:
        chart (Chart): The birth chart
        house_num (int): The house number (1-12)

    Returns:
        dict: Dictionary with house strength information
    """
    # Get the house from the birth chart
    house = chart.houses.get(house_num)

    # Get the sign of the house
    house_sign = house.sign

    # Get the lord of the house
    house_lord = const.LIST_SIGN_RULERS[const.LIST_SIGNS.index(house_sign)]

    # Get the strength of the house lord
    lord_strength = get_varga_strength(chart, house_lord)

    # Calculate the house strength based on the lord's strength
    house_strength = lord_strength['normalized_strength']

    return {
        'house': house_num,
        'sign': house_sign,
        'lord': house_lord,
        'lord_strength': lord_strength,
        'house_strength': house_strength
    }
