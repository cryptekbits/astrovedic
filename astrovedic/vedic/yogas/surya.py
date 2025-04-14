"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Sun Yogas (Surya Yogas) calculations
    for Vedic astrology.
"""

from astrovedic import const
from astrovedic import angle
from astrovedic.chart import Chart
from astrovedic.vedic.yogas.core import get_yoga_strength


def get_house_number(chart, planet_id):
    """
    Get the house number of a planet

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet

    Returns:
        int: The house number (1-12) of the planet
    """
    # Get the planet
    planet = chart.getObject(planet_id)

    # Get the Ascendant
    asc_lon = chart.getHouse('House1').lon

    # Calculate the house number
    house_num = 1 + int(angle.distance(planet.lon, asc_lon) / 30) % 12

    # Adjust for 0-based indexing
    if house_num == 0:
        house_num = 12

    return house_num


def get_surya_yogas(chart):
    """
    Identify Sun Yogas in a chart

    Sun Yogas are planetary combinations involving the Sun that indicate
    various aspects of personality, leadership, and authority.

    Args:
        chart (Chart): The birth chart

    Returns:
        list: List of Sun Yogas in the chart
    """
    # Initialize the result
    result = []

    # Check for Vasi Yoga
    vasi = has_vasi_yoga(chart)
    if vasi:
        result.append(vasi)

    # Check for Vesi Yoga
    vesi = has_vesi_yoga(chart)
    if vesi:
        result.append(vesi)

    # Check for Ubhayachari Yoga
    ubhayachari = has_ubhayachari_yoga(chart)
    if ubhayachari:
        result.append(ubhayachari)

    # Check for Budha-Aditya Yoga
    budha_aditya = has_budha_aditya_yoga(chart)
    if budha_aditya:
        result.append(budha_aditya)

    # Check for Parivartana Yoga involving Sun
    parivartana = has_sun_parivartana_yoga(chart)
    if parivartana:
        result.append(parivartana)

    return result


def has_vasi_yoga(chart):
    """
    Check if a chart has Vasi Yoga

    Vasi Yoga is formed when the Sun is in the 12th house from the Moon.
    This yoga gives the native control over their emotions and mind.

    Args:
        chart (Chart): The birth chart

    Returns:
        dict or None: Dictionary with Yoga information if present, None otherwise
    """
    # Get the Sun and Moon
    sun = chart.getObject(const.SUN)
    moon = chart.getObject(const.MOON)

    # Get the house numbers
    sun_house = get_house_number(chart, const.SUN)
    moon_house = get_house_number(chart, const.MOON)

    # Calculate the 12th house from the Moon
    house_12_from_moon = ((moon_house - 1 - 1) % 12) + 1  # -1 for 0-based, -1 for 12th, +1 for 1-based

    # Check if the Sun is in the 12th house from the Moon
    if sun_house == house_12_from_moon:
        # Create the Yoga information
        yoga = {
            'name': 'Vasi Yoga',
            'type': 'Surya Yoga',
            'planets': [const.SUN, const.MOON],
            'houses': [sun_house, moon_house],
            'description': 'Formed when the Sun is in the 12th house from the Moon, giving control over emotions and mind',
            'is_beneficial': True
        }

        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)

        return yoga

    return None


def has_vesi_yoga(chart):
    """
    Check if a chart has Vesi Yoga

    Vesi Yoga is formed when the Sun is in the 2nd house from the Moon.
    This yoga gives the native wealth, good speech, and material comforts.

    Args:
        chart (Chart): The birth chart

    Returns:
        dict or None: Dictionary with Yoga information if present, None otherwise
    """
    # Get the Sun and Moon
    sun = chart.getObject(const.SUN)
    moon = chart.getObject(const.MOON)

    # Get the house numbers
    sun_house = get_house_number(chart, const.SUN)
    moon_house = get_house_number(chart, const.MOON)

    # Calculate the 2nd house from the Moon
    house_2_from_moon = ((moon_house - 1 + 1) % 12) + 1  # -1 for 0-based, +1 for 2nd, +1 for 1-based

    # Check if the Sun is in the 2nd house from the Moon
    if sun_house == house_2_from_moon:
        # Create the Yoga information
        yoga = {
            'name': 'Vesi Yoga',
            'type': 'Surya Yoga',
            'planets': [const.SUN, const.MOON],
            'houses': [sun_house, moon_house],
            'description': 'Formed when the Sun is in the 2nd house from the Moon, giving wealth, good speech, and material comforts',
            'is_beneficial': True
        }

        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)

        return yoga

    return None


def has_ubhayachari_yoga(chart):
    """
    Check if a chart has Ubhayachari Yoga

    Ubhayachari Yoga is formed when the Sun and Moon are in the 2nd and 12th
    houses from each other. This is a combination of Vasi and Vesi Yogas.

    Args:
        chart (Chart): The birth chart

    Returns:
        dict or None: Dictionary with Yoga information if present, None otherwise
    """
    # Check if both Vasi and Vesi Yogas are present
    vasi = has_vasi_yoga(chart)
    vesi = has_vesi_yoga(chart)

    if vasi and vesi:
        # Create the Yoga information
        yoga = {
            'name': 'Ubhayachari Yoga',
            'type': 'Surya Yoga',
            'planets': [const.SUN, const.MOON],
            'houses': [vasi['houses'][0], vesi['houses'][1]],
            'description': 'Formed when the Sun and Moon are in the 2nd and 12th houses from each other, combining the benefits of Vasi and Vesi Yogas',
            'is_beneficial': True
        }

        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)

        return yoga

    return None


def has_budha_aditya_yoga(chart):
    """
    Check if a chart has Budha-Aditya Yoga

    Budha-Aditya Yoga is formed when Mercury is conjunct with the Sun.
    This yoga gives intelligence, education, and communication skills.

    Args:
        chart (Chart): The birth chart

    Returns:
        dict or None: Dictionary with Yoga information if present, None otherwise
    """
    # Get the Sun and Mercury
    sun = chart.getObject(const.SUN)
    mercury = chart.getObject(const.MERCURY)

    # Get the house numbers
    sun_house = get_house_number(chart, const.SUN)
    mercury_house = get_house_number(chart, const.MERCURY)

    # Check if Mercury is conjunct with the Sun
    if sun_house == mercury_house:
        # Calculate the orb (distance between the planets)
        orb = abs(angle.closestdistance(sun.lon, mercury.lon))

        # Check if the orb is within the allowed range (usually 10 degrees)
        if orb <= 10:
            # Create the Yoga information
            yoga = {
                'name': 'Budha-Aditya Yoga',
                'type': 'Surya Yoga',
                'planets': [const.SUN, const.MERCURY],
                'houses': [sun_house],
                'description': 'Formed when Mercury is conjunct with the Sun, giving intelligence, education, and communication skills',
                'is_beneficial': True
            }

            # Calculate the strength of the Yoga
            yoga['strength'] = get_yoga_strength(chart, yoga)

            return yoga

    return None


def has_sun_parivartana_yoga(chart):
    """
    Check if a chart has Parivartana Yoga involving the Sun

    Parivartana Yoga is formed when two planets are in each other's signs.
    This yoga involving the Sun gives authority, leadership, and recognition.

    Args:
        chart (Chart): The birth chart

    Returns:
        dict or None: Dictionary with Yoga information if present, None otherwise
    """
    # Get the Sun
    sun = chart.getObject(const.SUN)

    # Get the Sun's sign
    sun_sign = sun.sign

    # Get the house number of the Sun
    sun_house = get_house_number(chart, const.SUN)

    # Get the lord of the Sun's sign
    sun_sign_lord = None
    if sun_sign == const.LEO:
        sun_sign_lord = const.SUN
    elif sun_sign == const.CANCER:
        sun_sign_lord = const.MOON
    elif sun_sign == const.GEMINI or sun_sign == const.VIRGO:
        sun_sign_lord = const.MERCURY
    elif sun_sign == const.TAURUS or sun_sign == const.LIBRA:
        sun_sign_lord = const.VENUS
    elif sun_sign == const.ARIES or sun_sign == const.SCORPIO:
        sun_sign_lord = const.MARS
    elif sun_sign == const.SAGITTARIUS or sun_sign == const.PISCES:
        sun_sign_lord = const.JUPITER
    elif sun_sign == const.CAPRICORN or sun_sign == const.AQUARIUS:
        sun_sign_lord = const.SATURN

    # If the Sun is in its own sign (Leo), there can't be a Parivartana Yoga
    if sun_sign_lord == const.SUN:
        return None

    # Get the lord's sign
    lord = chart.getObject(sun_sign_lord)
    lord_sign = lord.sign

    # Check if the lord is in Leo (Sun's sign)
    if lord_sign == const.LEO:
        # Get the house number of the lord
        lord_house = get_house_number(chart, sun_sign_lord)

        # Create the Yoga information
        yoga = {
            'name': f'Sun-{sun_sign_lord} Parivartana Yoga',
            'type': 'Surya Yoga',
            'planets': [const.SUN, sun_sign_lord],
            'houses': [sun_house, lord_house],
            'description': f'Formed when the Sun is in {sun_sign} and {sun_sign_lord} is in Leo, giving authority, leadership, and recognition',
            'is_beneficial': True
        }

        # Calculate the strength of the Yoga
        yoga['strength'] = get_yoga_strength(chart, yoga)

        return yoga

    return None
