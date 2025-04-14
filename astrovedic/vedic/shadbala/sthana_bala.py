"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Sthana Bala (positional strength) calculations
    for Shadbala in Vedic astrology.
"""

from astrovedic import const
from astrovedic import angle
from astrovedic.vedic import dignities as vedic_dignities


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

    # Import the necessary functions from the vargas module
    from astrovedic.vedic.vargas import get_varga_chart

    # Calculate each component of Sthana Bala
    # Pass retrograde status to uchcha_bala calculation
    uchcha_bala = calculate_uchcha_bala(planet_id, planet.lon, planet.isRetrograde())
    saptavarga_bala = calculate_saptavarga_bala(chart, planet_id)

    # Get the Navamsha (D9) chart and planet position for Ojha-Yugma Bala
    navamsha_chart = get_varga_chart(chart, 'D9')
    navamsha_planet = navamsha_chart.getObject(planet_id)
    navamsha_sign = navamsha_planet.sign

    # Calculate Ojha-Yugma Bala with both D1 and D9 signs
    ojha_yugma_bala = calculate_ojha_yugma_bala(planet_id, planet.sign, navamsha_sign)

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


def calculate_uchcha_bala(planet_id, longitude, is_retrograde):
    """
    Calculate Uchcha Bala (exaltation strength) for a planet

    Args:
        planet_id (str): The ID of the planet
        longitude (float): The longitude of the planet
        is_retrograde (bool): Whether the planet is retrograde

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
        # Include strength key for consistency
        return {'value': 0.0, 'description': 'Not applicable', 'strength': 'N/A'}

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

    # Calculate standard Uchcha Bala based on distance
    if distance_from_exaltation <= 180:
        # Planet is moving from exaltation to debilitation
        value = max_value * (1 - distance_from_exaltation / 180.0)
    else:
        # Planet is moving from debilitation to exaltation
        value = max_value * (distance_from_debilitation / 180.0)

    # Initialize description and strength
    description = 'Calculated by distance'
    strength = 'Weak'  # Default

    # Check for Neecha Bhanga due to retrograde in debilitation sign
    if is_retrograde and sign == debil_sign:
        value = max_value  # Grant full strength
        description = f'Retrograde in debilitation sign ({debil_sign}) - Neecha Bhanga'
        strength = 'Very strong'
    else:
        # Determine the description based on position if Neecha Bhanga doesn't apply
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

        # Add strength assessment based on standard value
        if value >= 45.0:
            strength = 'Very strong'
        elif value >= 30.0:
            strength = 'Strong'
        elif value >= 15.0:
            strength = 'Moderate'
        # else: strength remains 'Weak' (default)

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
    according to standard Vedic astrology rules.

    Saptavarga Bala is calculated based on the dignity of a planet in seven
    divisional charts (D1, D2, D3, D7, D9, D12, D30) using the standard
    Virupa point system.

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet

    Returns:
        dict: Dictionary with Saptavarga Bala information
    """
    # Import the necessary functions from the vargas module
    from astrovedic.vedic.vargas import (
        get_varga_chart, get_varga_longitude
    )

    # Define the varga types to use (standard Saptavarga)
    varga_types = ['D1', 'D2', 'D3', 'D7', 'D9', 'D12', 'D30']

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

        # Standard Virupa points for each dignity level
        virupa_points = 0.0
        dignity_name = 'None'

        # Check if the planet is in its own sign or Moolatrikona
        if vedic_dignities.is_in_moolatrikona(planet_id, varga_sign, varga_degree):
            virupa_points = 45.0  # Standard Virupa points for Moolatrikona
            dignity_name = 'Moolatrikona'
        elif vedic_dignities.is_own_sign(planet_id, varga_sign):
            virupa_points = 30.0  # Standard Virupa points for Own Sign
            dignity_name = 'Own Sign'
        else:
            # Check Combined Friendship level with sign lord
            sign_lord = vedic_dignities.get_ruler(varga_sign)
            combined_friendship = vedic_dignities.calculate_combined_friendship(chart, planet_id, sign_lord)

            if combined_friendship == 'GREAT_FRIEND':
                virupa_points = 22.5  # Standard Virupa points for Great Friend
                dignity_name = 'Great Friend'
            elif combined_friendship == 'FRIEND':
                virupa_points = 15.0  # Standard Virupa points for Friend
                dignity_name = 'Friend'
            elif combined_friendship == 'NEUTRAL':
                virupa_points = 7.5   # Standard Virupa points for Neutral
                dignity_name = 'Neutral'
            elif combined_friendship == 'ENEMY':
                virupa_points = 3.75  # Standard Virupa points for Enemy
                dignity_name = 'Enemy'
            else:  # GREAT_ENEMY
                virupa_points = 1.875  # Standard Virupa points for Great Enemy
                dignity_name = 'Great Enemy'

        # Add to the total (no weighting - all vargas contribute equally)
        result['total_virupa'] += virupa_points

        # Store the details for this varga
        result['varga_details'][varga_type] = {
            'sign': varga_sign,
            'degree': varga_degree,
            'dignity': dignity_name,
            'virupa_points': virupa_points,
            'weighted_virupa': virupa_points  # No weighting applied
        }

    # The final value is the simple sum of Virupas obtained
    # No scaling or arbitrary maximums
    value = result['total_virupa']

    # Add the final value to the result
    result['value'] = value
    result['description'] = 'Strength in seven divisional charts (standard Virupa points)'

    return result


def calculate_ojha_yugma_bala(planet_id, d1_sign, d9_sign=None):
    """
    Calculate Ojha-Yugma Bala (odd-even sign strength) for a planet

    According to standard Vedic rules, Ojha-Yugma Bala is awarded only if the planet
    occupies a favorable sign type in BOTH the Rashi (D1) and Navamsha (D9) charts.

    Args:
        planet_id (str): The ID of the planet
        d1_sign (str): The sign of the planet in the Rashi (D1) chart
        d9_sign (str, optional): The sign of the planet in the Navamsha (D9) chart
                                If not provided, only D1 is considered (non-standard)

    Returns:
        dict: Dictionary with Ojha-Yugma Bala information
    """
    # Get the sign numbers (0-11) for both D1 and D9 signs
    sign_map = {
        const.ARIES: 0, const.TAURUS: 1, const.GEMINI: 2, const.CANCER: 3,
        const.LEO: 4, const.VIRGO: 5, const.LIBRA: 6, const.SCORPIO: 7,
        const.SAGITTARIUS: 8, const.CAPRICORN: 9, const.AQUARIUS: 10, const.PISCES: 11
    }

    d1_sign_num = sign_map[d1_sign]

    # Determine if the D1 sign is odd or even
    is_d1_odd_sign = (d1_sign_num % 2 == 0)  # 0-based, so even indices are odd signs

    # Check D9 sign if provided
    if d9_sign:
        d9_sign_num = sign_map[d9_sign]
        is_d9_odd_sign = (d9_sign_num % 2 == 0)  # 0-based, so even indices are odd signs
    else:
        # If D9 sign is not provided, assume it matches D1 (non-standard)
        is_d9_odd_sign = is_d1_odd_sign

    # Define planets that prefer odd signs (Aries, Gemini, Leo, Libra, Sagittarius, Aquarius)
    odd_sign_planets = [const.SUN, const.MARS, const.JUPITER]

    # Define planets that prefer even signs (Taurus, Cancer, Virgo, Scorpio, Capricorn, Pisces)
    even_sign_planets = [const.MOON, const.VENUS, const.SATURN]

    # Mercury gains strength in both odd and even signs
    mercury_special_case = (planet_id == const.MERCURY)

    # Determine if the planet is in its preferred sign type in BOTH D1 and D9
    if mercury_special_case:
        # Mercury always gets full strength
        value = 15.0
        description = 'Mercury gains strength in both odd and even signs'
    elif planet_id in odd_sign_planets and is_d1_odd_sign and is_d9_odd_sign:
        value = 15.0
        description = 'In preferred odd signs in both D1 and D9'
    elif planet_id in even_sign_planets and not is_d1_odd_sign and not is_d9_odd_sign:
        value = 15.0
        description = 'In preferred even signs in both D1 and D9'
    elif planet_id in [const.RAHU, const.KETU]:
        # For Rahu/Ketu, we'll use a more standard approach based on their dispositors
        # For simplicity, we'll assign 0 points as they don't have standard Ojha-Yugma Bala
        value = 0.0
        description = 'Nodes (Rahu/Ketu) do not receive Ojha-Yugma Bala'
    else:
        # If the planet is not in its preferred sign type in BOTH charts, it gets 0
        value = 0.0
        if d9_sign:
            description = 'Not in preferred sign type in both D1 and D9 charts'
        else:
            description = 'Not in preferred sign type'

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
