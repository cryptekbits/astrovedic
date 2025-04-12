"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology

    This module defines Vedic-specific planetary dignities including:
    - Rulership (Swakshetra)
    - Exaltation (Uchcha)
    - Debilitation (Neecha)
    - Moolatrikona (special portion of own sign)

    These dignities are used in various Vedic calculations, especially
    Shadbala (six-fold planetary strength).
"""

from flatlib import const

# === Rulership (Swakshetra) === #

# Vedic rulerships (traditional planets only)
VEDIC_RULERSHIPS = {
    const.SUN: [const.LEO],
    const.MOON: [const.CANCER],
    const.MERCURY: [const.GEMINI, const.VIRGO],
    const.VENUS: [const.TAURUS, const.LIBRA],
    const.MARS: [const.ARIES, const.SCORPIO],
    const.JUPITER: [const.SAGITTARIUS, const.PISCES],
    const.SATURN: [const.CAPRICORN, const.AQUARIUS],
    const.RAHU: [],  # Shadow planets don't have rulership
    const.KETU: []   # Shadow planets don't have rulership
}

# Reverse mapping: sign to ruler
VEDIC_SIGN_RULERS = {
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

# === Exaltation (Uchcha) and Debilitation (Neecha) === #

# Exaltation signs and degrees
VEDIC_EXALTATION = {
    const.SUN: (const.ARIES, 10),        # 10° Aries
    const.MOON: (const.TAURUS, 3),       # 3° Taurus
    const.MERCURY: (const.VIRGO, 15),    # 15° Virgo
    const.VENUS: (const.PISCES, 27),     # 27° Pisces
    const.MARS: (const.CAPRICORN, 28),   # 28° Capricorn
    const.JUPITER: (const.CANCER, 5),    # 5° Cancer
    const.SATURN: (const.LIBRA, 20),     # 20° Libra
    const.RAHU: (const.TAURUS, 20),      # 20° Taurus (some traditions)
    const.KETU: (const.SCORPIO, 20)      # 20° Scorpio (some traditions)
}

# Debilitation signs and degrees (opposite of exaltation)
VEDIC_DEBILITATION = {
    const.SUN: (const.LIBRA, 10),        # 10° Libra
    const.MOON: (const.SCORPIO, 3),      # 3° Scorpio
    const.MERCURY: (const.PISCES, 15),   # 15° Pisces
    const.VENUS: (const.VIRGO, 27),      # 27° Virgo
    const.MARS: (const.CANCER, 28),      # 28° Cancer
    const.JUPITER: (const.CAPRICORN, 5), # 5° Capricorn
    const.SATURN: (const.ARIES, 20),     # 20° Aries
    const.RAHU: (const.SCORPIO, 20),     # 20° Scorpio (some traditions)
    const.KETU: (const.TAURUS, 20)       # 20° Taurus (some traditions)
}

# === Moolatrikona === #

# Moolatrikona signs and degree ranges
# Format: (sign, start_degree, end_degree)
VEDIC_MOOLATRIKONA = {
    const.SUN: (const.LEO, 0, 20),           # 0-20° Leo
    const.MOON: (const.TAURUS, 4, 30),       # 4-30° Taurus
    const.MERCURY: (const.VIRGO, 16, 20),    # 16-20° Virgo
    const.VENUS: (const.LIBRA, 0, 15),       # 0-15° Libra
    const.MARS: (const.ARIES, 0, 12),        # 0-12° Aries
    const.JUPITER: (const.SAGITTARIUS, 0, 10), # 0-10° Sagittarius
    const.SATURN: (const.AQUARIUS, 0, 20),   # 0-20° Aquarius
    const.RAHU: None,                        # No Moolatrikona for shadow planets
    const.KETU: None                         # No Moolatrikona for shadow planets
}

# === Temporary Dignity (Tatkalika Bala) === #

# Planetary friendship levels
FRIENDSHIP_LEVELS = {
    'GREAT_FRIEND': 5,    # Adhi Mitra
    'FRIEND': 4,          # Mitra
    'NEUTRAL': 3,         # Sama
    'ENEMY': 2,           # Shatru
    'GREAT_ENEMY': 1      # Adhi Shatru
}

# Natural friendships (Naisargika Maitri)
# 1 = Great Enemy, 2 = Enemy, 3 = Neutral, 4 = Friend, 5 = Great Friend
NATURAL_FRIENDSHIPS = {
    const.SUN: {
        const.SUN: 3,     # Self is neutral
        const.MOON: 4,    # Friend
        const.MERCURY: 3, # Neutral
        const.VENUS: 2,   # Enemy
        const.MARS: 4,    # Friend
        const.JUPITER: 4, # Friend
        const.SATURN: 2,  # Enemy
        const.RAHU: 2,    # Enemy
        const.KETU: 2     # Enemy
    },
    const.MOON: {
        const.SUN: 4,     # Friend
        const.MOON: 3,    # Self is neutral
        const.MERCURY: 4, # Friend
        const.VENUS: 4,   # Friend
        const.MARS: 2,    # Enemy
        const.JUPITER: 4, # Friend
        const.SATURN: 2,  # Enemy
        const.RAHU: 2,    # Enemy
        const.KETU: 2     # Enemy
    },
    const.MERCURY: {
        const.SUN: 4,     # Friend
        const.MOON: 4,    # Friend
        const.MERCURY: 3, # Self is neutral
        const.VENUS: 4,   # Friend
        const.MARS: 3,    # Neutral
        const.JUPITER: 3, # Neutral
        const.SATURN: 3,  # Neutral
        const.RAHU: 3,    # Neutral
        const.KETU: 3     # Neutral
    },
    const.VENUS: {
        const.SUN: 2,     # Enemy
        const.MOON: 4,    # Friend
        const.MERCURY: 4, # Friend
        const.VENUS: 3,   # Self is neutral
        const.MARS: 3,    # Neutral
        const.JUPITER: 3, # Neutral
        const.SATURN: 4,  # Friend
        const.RAHU: 3,    # Neutral
        const.KETU: 3     # Neutral
    },
    const.MARS: {
        const.SUN: 4,     # Friend
        const.MOON: 2,    # Enemy
        const.MERCURY: 3, # Neutral
        const.VENUS: 3,   # Neutral
        const.MARS: 3,    # Self is neutral
        const.JUPITER: 4, # Friend
        const.SATURN: 2,  # Enemy
        const.RAHU: 2,    # Enemy
        const.KETU: 2     # Enemy
    },
    const.JUPITER: {
        const.SUN: 4,     # Friend
        const.MOON: 4,    # Friend
        const.MERCURY: 2, # Enemy
        const.VENUS: 2,   # Enemy
        const.MARS: 4,    # Friend
        const.JUPITER: 3, # Self is neutral
        const.SATURN: 2,  # Enemy
        const.RAHU: 2,    # Enemy
        const.KETU: 2     # Enemy
    },
    const.SATURN: {
        const.SUN: 2,     # Enemy
        const.MOON: 2,    # Enemy
        const.MERCURY: 3, # Neutral
        const.VENUS: 4,   # Friend
        const.MARS: 2,    # Enemy
        const.JUPITER: 2, # Enemy
        const.SATURN: 3,  # Self is neutral
        const.RAHU: 4,    # Friend
        const.KETU: 4     # Friend
    },
    const.RAHU: {
        const.SUN: 2,     # Enemy
        const.MOON: 2,    # Enemy
        const.MERCURY: 3, # Neutral
        const.VENUS: 3,   # Neutral
        const.MARS: 2,    # Enemy
        const.JUPITER: 2, # Enemy
        const.SATURN: 4,  # Friend
        const.RAHU: 3,    # Self is neutral
        const.KETU: 3     # Neutral
    },
    const.KETU: {
        const.SUN: 2,     # Enemy
        const.MOON: 2,    # Enemy
        const.MERCURY: 3, # Neutral
        const.VENUS: 3,   # Neutral
        const.MARS: 2,    # Enemy
        const.JUPITER: 2, # Enemy
        const.SATURN: 4,  # Friend
        const.RAHU: 3,    # Neutral
        const.KETU: 3     # Self is neutral
    }
}

# === Functions === #

def get_ruler(sign):
    """
    Get the ruler of a sign according to Vedic astrology

    Args:
        sign (str): The sign

    Returns:
        str: The ruler of the sign
    """
    return VEDIC_SIGN_RULERS.get(sign)


def get_ruled_signs(planet_id):
    """
    Get the signs ruled by a planet according to Vedic astrology

    Args:
        planet_id (str): The ID of the planet

    Returns:
        list: The signs ruled by the planet
    """
    return VEDIC_RULERSHIPS.get(planet_id, [])


def is_own_sign(planet_id, sign):
    """
    Check if a planet is in its own sign

    Args:
        planet_id (str): The ID of the planet
        sign (str): The sign

    Returns:
        bool: True if the planet is in its own sign, False otherwise
    """
    return sign in VEDIC_RULERSHIPS.get(planet_id, [])


def get_exaltation(planet_id):
    """
    Get the exaltation sign and degree of a planet

    Args:
        planet_id (str): The ID of the planet

    Returns:
        tuple: (sign, degree) or None if the planet has no exaltation
    """
    return VEDIC_EXALTATION.get(planet_id)


def is_exalted(planet_id, sign):
    """
    Check if a planet is in its exaltation sign

    Args:
        planet_id (str): The ID of the planet
        sign (str): The sign

    Returns:
        bool: True if the planet is in its exaltation sign, False otherwise
    """
    exaltation = VEDIC_EXALTATION.get(planet_id)
    return exaltation and exaltation[0] == sign


def is_exact_exaltation(planet_id, sign, degree):
    """
    Check if a planet is at its exact exaltation degree

    Args:
        planet_id (str): The ID of the planet
        sign (str): The sign
        degree (float): The degree within the sign

    Returns:
        bool: True if the planet is at its exact exaltation degree, False otherwise
    """
    exaltation = VEDIC_EXALTATION.get(planet_id)
    return exaltation and exaltation[0] == sign and abs(exaltation[1] - degree) < 1


def get_debilitation(planet_id):
    """
    Get the debilitation sign and degree of a planet

    Args:
        planet_id (str): The ID of the planet

    Returns:
        tuple: (sign, degree) or None if the planet has no debilitation
    """
    return VEDIC_DEBILITATION.get(planet_id)


def is_debilitated(planet_id, sign):
    """
    Check if a planet is in its debilitation sign

    Args:
        planet_id (str): The ID of the planet
        sign (str): The sign

    Returns:
        bool: True if the planet is in its debilitation sign, False otherwise
    """
    debilitation = VEDIC_DEBILITATION.get(planet_id)
    return debilitation and debilitation[0] == sign


def is_exact_debilitation(planet_id, sign, degree):
    """
    Check if a planet is at its exact debilitation degree

    Args:
        planet_id (str): The ID of the planet
        sign (str): The sign
        degree (float): The degree within the sign

    Returns:
        bool: True if the planet is at its exact debilitation degree, False otherwise
    """
    debilitation = VEDIC_DEBILITATION.get(planet_id)
    return debilitation and debilitation[0] == sign and abs(debilitation[1] - degree) < 1


def get_moolatrikona(planet_id):
    """
    Get the Moolatrikona sign and degree range of a planet

    Args:
        planet_id (str): The ID of the planet

    Returns:
        tuple: (sign, start_degree, end_degree) or None if the planet has no Moolatrikona
    """
    return VEDIC_MOOLATRIKONA.get(planet_id)


def is_in_moolatrikona(planet_id, sign, degree):
    """
    Check if a planet is in its Moolatrikona range

    Args:
        planet_id (str): The ID of the planet
        sign (str): The sign
        degree (float): The degree within the sign

    Returns:
        bool: True if the planet is in its Moolatrikona range, False otherwise
    """
    moolatrikona = VEDIC_MOOLATRIKONA.get(planet_id)
    if not moolatrikona:
        return False

    mt_sign, start_deg, end_deg = moolatrikona
    return mt_sign == sign and start_deg <= degree < end_deg


def get_natural_friendship(planet1_id, planet2_id):
    """
    Get the natural friendship level between two planets

    Args:
        planet1_id (str): The ID of the first planet
        planet2_id (str): The ID of the second planet

    Returns:
        int: The friendship level (1-5)
    """
    if planet1_id not in NATURAL_FRIENDSHIPS:
        return FRIENDSHIP_LEVELS['NEUTRAL']

    return NATURAL_FRIENDSHIPS[planet1_id].get(planet2_id, FRIENDSHIP_LEVELS['NEUTRAL'])


def calculate_temporal_friendship(chart, planet1_id, planet2_id):
    """
    Calculate the temporal friendship between two planets based on house positions

    Args:
        chart (Chart): The chart
        planet1_id (str): The ID of the first planet
        planet2_id (str): The ID of the second planet

    Returns:
        int: The friendship level (1-5)
    """
    # Get the planets
    planet1 = chart.getObject(planet1_id)
    planet2 = chart.getObject(planet2_id)

    # Get the houses occupied by the planets
    house1 = chart.houses.getObjectHouse(planet1)
    house2 = chart.houses.getObjectHouse(planet2)

    # Convert house numbers to integers
    house1_num = int(house1.id[5:])
    house2_num = int(house2.id[5:])

    # Calculate the distance between houses
    distance = (house2_num - house1_num) % 12

    # Determine friendship level based on house distance
    if distance in [2, 12]:
        # 2nd and 12th houses are enemies
        return FRIENDSHIP_LEVELS['ENEMY']
    elif distance in [3, 6, 11]:
        # 3rd, 6th, and 11th houses are friends
        return FRIENDSHIP_LEVELS['FRIEND']
    elif distance in [1, 5, 9]:
        # 1st, 5th, and 9th houses are great friends
        return FRIENDSHIP_LEVELS['GREAT_FRIEND']
    elif distance in [4, 8, 10]:
        # 4th, 8th, and 10th houses are great enemies
        return FRIENDSHIP_LEVELS['GREAT_ENEMY']
    else:
        # 7th house is neutral
        return FRIENDSHIP_LEVELS['NEUTRAL']


def calculate_combined_friendship(chart, planet1_id, planet2_id):
    """
    Calculate the combined friendship level between two planets

    Args:
        chart (Chart): The chart
        planet1_id (str): The ID of the first planet
        planet2_id (str): The ID of the second planet

    Returns:
        str: The combined friendship level ('GREAT_FRIEND', 'FRIEND', 'NEUTRAL', 'ENEMY', 'GREAT_ENEMY')
    """
    # Get the natural friendship level
    natural = get_natural_friendship(planet1_id, planet2_id)

    # Get the temporal friendship level
    temporal = calculate_temporal_friendship(chart, planet1_id, planet2_id)

    # Calculate the combined level
    combined = (natural + temporal) // 2

    # Convert to string representation
    if combined >= FRIENDSHIP_LEVELS['GREAT_FRIEND']:
        return 'GREAT_FRIEND'
    elif combined >= FRIENDSHIP_LEVELS['FRIEND']:
        return 'FRIEND'
    elif combined >= FRIENDSHIP_LEVELS['NEUTRAL']:
        return 'NEUTRAL'
    elif combined >= FRIENDSHIP_LEVELS['ENEMY']:
        return 'ENEMY'
    else:
        return 'GREAT_ENEMY'


def get_dignity_score(planet_id, sign, degree):
    """
    Calculate the dignity score for a planet at a specific position

    Args:
        planet_id (str): The ID of the planet
        sign (str): The sign
        degree (float): The degree within the sign

    Returns:
        dict: Dictionary with dignity information and score
    """
    # Initialize the result
    result = {
        'is_own_sign': False,
        'is_moolatrikona': False,
        'is_exalted': False,
        'is_debilitated': False,
        'is_exact_exaltation': False,
        'is_exact_debilitation': False,
        'score': 0
    }

    # Check if the planet is in its own sign
    result['is_own_sign'] = is_own_sign(planet_id, sign)

    # Check if the planet is in its Moolatrikona
    result['is_moolatrikona'] = is_in_moolatrikona(planet_id, sign, degree)

    # Check if the planet is exalted
    result['is_exalted'] = is_exalted(planet_id, sign)
    result['is_exact_exaltation'] = is_exact_exaltation(planet_id, sign, degree)

    # Check if the planet is debilitated
    result['is_debilitated'] = is_debilitated(planet_id, sign)
    result['is_exact_debilitation'] = is_exact_debilitation(planet_id, sign, degree)

    # Calculate the score
    if result['is_exact_exaltation']:
        result['score'] = 10  # Highest score for exact exaltation
    elif result['is_exact_debilitation']:
        result['score'] = -10  # Lowest score for exact debilitation
    elif result['is_exalted']:
        result['score'] = 8  # High score for exaltation
    elif result['is_debilitated']:
        result['score'] = -8  # Low score for debilitation
    elif result['is_moolatrikona']:
        result['score'] = 7  # Very good score for Moolatrikona
    elif result['is_own_sign']:
        result['score'] = 5  # Good score for own sign

    return result


def get_dignity_name(planet_id, sign, degree):
    """
    Get the name of the dignity for a planet at a specific position

    Args:
        planet_id (str): The ID of the planet
        sign (str): The sign
        degree (float): The degree within the sign

    Returns:
        str: The name of the dignity
    """
    # Check dignities in order of strength
    if is_exact_exaltation(planet_id, sign, degree):
        return "Exact Exaltation"
    elif is_exact_debilitation(planet_id, sign, degree):
        return "Exact Debilitation"
    elif is_exalted(planet_id, sign):
        return "Exaltation"
    elif is_debilitated(planet_id, sign):
        return "Debilitation"
    elif is_in_moolatrikona(planet_id, sign, degree):
        return "Moolatrikona"
    elif is_own_sign(planet_id, sign):
        return "Own Sign"
    else:
        return "None"
