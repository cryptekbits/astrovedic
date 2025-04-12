"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Sthana Bala (positional strength) calculations
    for Shadbala in Vedic astrology.
"""

from flatlib import const
from flatlib import angle
from flatlib.vedic import dignities as vedic_dignities


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
    # Maximum Uchcha Bala value (in Virupas)
    max_value = 60.0

    # Get the sign and degree from the longitude
    sign_num = int(longitude / 30)
    sign = const.LIST_SIGNS[sign_num]
    degree = longitude % 30

    # Get exaltation and debilitation information from Vedic dignities
    exaltation = vedic_dignities.get_exaltation(planet_id)
    debilitation = vedic_dignities.get_debilitation(planet_id)

    # If the planet has no exaltation/debilitation, return 0
    if not exaltation or not debilitation:
        return {'value': 0.0, 'description': 'Not applicable'}

    # Convert exaltation and debilitation points to absolute longitudes
    exalt_sign, exalt_deg = exaltation
    debil_sign, debil_deg = debilitation

    exalt_sign_num = const.LIST_SIGNS.index(exalt_sign)
    debil_sign_num = const.LIST_SIGNS.index(debil_sign)

    exaltation_point = exalt_sign_num * 30 + exalt_deg
    debilitation_point = debil_sign_num * 30 + debil_deg

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
    if distance_from_exaltation < 1:
        description = 'Exact exaltation'
    elif distance_from_debilitation < 1:
        description = 'Exact debilitation'
    elif distance_from_exaltation <= 30:
        description = 'Near exaltation'
    elif distance_from_debilitation <= 30:
        description = 'Near debilitation'
    elif distance_from_exaltation <= 90:
        description = 'Moving away from exaltation'
    elif distance_from_debilitation <= 90:
        description = 'Moving away from debilitation'
    elif distance_from_exaltation < distance_from_debilitation:
        description = 'Closer to exaltation'
    else:
        description = 'Closer to debilitation'

    # Add strength assessment
    if value >= 45.0:
        strength = 'Very strong'
    elif value >= 30.0:
        strength = 'Strong'
    elif value >= 15.0:
        strength = 'Moderate'
    else:
        strength = 'Weak'

    return {
        'value': value,
        'description': description,
        'strength': strength,
        'exaltation_point': exaltation_point,
        'debilitation_point': debilitation_point,
        'distance_from_exaltation': distance_from_exaltation,
        'distance_from_debilitation': distance_from_debilitation
    }


def calculate_saptavarga_bala(chart, planet_id):
    """
    Calculate Saptavarga Bala (strength in divisional charts) for a planet

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet

    Returns:
        dict: Dictionary with Saptavarga Bala information
    """
    # Import the necessary functions from the vargas module
    from flatlib.vedic.vargas import (
        get_varga_chart, get_varga_longitude
    )

    # Define the varga types to use
    varga_types = ['D1', 'D2', 'D3', 'D7', 'D9', 'D12', 'D30']

    # Define the weights for each varga
    varga_weights = {
        'D1': 5.0,   # Rashi (birth chart)
        'D2': 2.0,   # Hora
        'D3': 3.0,   # Drekkana
        'D7': 2.5,   # Saptamsha
        'D9': 4.5,   # Navamsha
        'D12': 2.0,  # Dwadashamsha
        'D30': 1.0   # Trimshamsha
    }

    # Get the planet from the chart
    planet = chart.getObject(planet_id)

    # Initialize the result
    result = {
        'varga_details': {},
        'total_virupa': 0.0
    }

    # Calculate the strength in each divisional chart
    for varga_type in varga_types:
        # Get the varga chart
        varga_chart = get_varga_chart(chart, varga_type)

        # Get the planet in the varga chart
        varga_planet = varga_chart.getObject(planet_id)

        # Get the sign and degree
        varga_sign = varga_planet.sign
        varga_degree = varga_planet.signlon

        # Calculate the dignity score using Vedic dignities
        dignity_info = vedic_dignities.get_dignity_score(planet_id, varga_sign, varga_degree)

        # Assign Virupa points based on dignity
        virupa_points = 0.0
        dignity_name = 'None'

        if dignity_info['is_exact_exaltation']:
            virupa_points = 5.0
            dignity_name = 'Exact Exaltation'
        elif dignity_info['is_moolatrikona']:
            virupa_points = 4.0
            dignity_name = 'Moolatrikona'
        elif dignity_info['is_own_sign']:
            virupa_points = 3.0
            dignity_name = 'Own Sign'
        elif dignity_info['is_exalted']:
            virupa_points = 2.0
            dignity_name = 'Exaltation'
        elif dignity_info['is_exact_debilitation']:
            virupa_points = 0.0
            dignity_name = 'Exact Debilitation'
        elif dignity_info['is_debilitated']:
            virupa_points = 0.5
            dignity_name = 'Debilitation'
        else:
            # Check friendship level with sign lord
            sign_lord = vedic_dignities.get_ruler(varga_sign)
            friendship = vedic_dignities.get_natural_friendship(planet_id, sign_lord)

            if friendship == vedic_dignities.FRIENDSHIP_LEVELS['GREAT_FRIEND']:
                virupa_points = 1.5
                dignity_name = 'Great Friend'
            elif friendship == vedic_dignities.FRIENDSHIP_LEVELS['FRIEND']:
                virupa_points = 1.0
                dignity_name = 'Friend'
            elif friendship == vedic_dignities.FRIENDSHIP_LEVELS['NEUTRAL']:
                virupa_points = 0.5
                dignity_name = 'Neutral'
            elif friendship == vedic_dignities.FRIENDSHIP_LEVELS['ENEMY']:
                virupa_points = 0.25
                dignity_name = 'Enemy'
            else:  # GREAT_ENEMY
                virupa_points = 0.0
                dignity_name = 'Great Enemy'

        # Apply the weight for this varga
        weighted_virupa = virupa_points * varga_weights[varga_type]

        # Add to the total
        result['total_virupa'] += weighted_virupa

        # Store the details for this varga
        result['varga_details'][varga_type] = {
            'sign': varga_sign,
            'degree': varga_degree,
            'dignity': dignity_name,
            'virupa_points': virupa_points,
            'weighted_virupa': weighted_virupa
        }

    # Maximum possible value is 100 (if all charts have maximum dignity)
    max_value = 100.0

    # Scale to Virupas (maximum 30)
    value = min(30.0, (result['total_virupa'] / max_value) * 30.0)

    # Add the final value to the result
    result['value'] = value
    result['description'] = 'Strength in seven divisional charts'

    return result


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
