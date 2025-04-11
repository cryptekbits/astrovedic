"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements cached versions of Varga (divisional chart)
    calculations in Vedic astrology.
"""

from flatlib.cache import calculation_cache
from flatlib.vedic.vargas.core_cached import calculate_varga_longitude


@calculation_cache()
def calculate_d1(longitude):
    """
    Calculate the D1 (Rashi) longitude

    This is just the original longitude, as D1 is the birth chart itself.

    Args:
        longitude (float): The longitude in the birth chart (0-360)

    Returns:
        float: The longitude in the D1 chart (same as input)
    """
    return longitude


@calculation_cache()
def calculate_d2(longitude):
    """
    Calculate the D2 (Hora) longitude

    In the Hora chart, each sign is divided into two parts of 15° each.
    The first half of odd signs and second half of even signs are ruled by the Sun.
    The second half of odd signs and first half of even signs are ruled by the Moon.

    Args:
        longitude (float): The longitude in the birth chart (0-360)

    Returns:
        float: The longitude in the D2 chart
    """
    # Get the sign number (0-11) and longitude within the sign (0-30)
    sign_num = int(longitude / 30)
    sign_lon = longitude % 30

    # Determine if the sign is odd or even
    is_odd_sign = sign_num % 2 == 0  # 0-based, so 0 = Aries (odd)

    # Determine which half of the sign the longitude falls in
    is_first_half = sign_lon < 15

    # Determine the resulting sign
    if (is_odd_sign and is_first_half) or (not is_odd_sign and not is_first_half):
        # Sun's hora
        result_sign = 4  # Leo
    else:
        # Moon's hora
        result_sign = 3  # Cancer

    # Calculate the longitude within the resulting sign
    result_lon = (sign_lon % 15) * 2

    # Return the final longitude
    return result_sign * 30 + result_lon


@calculation_cache()
def calculate_d3(longitude):
    """
    Calculate the D3 (Drekkana) longitude

    In the Drekkana chart, each sign is divided into three parts of 10° each.

    Args:
        longitude (float): The longitude in the birth chart (0-360)

    Returns:
        float: The longitude in the D3 chart
    """
    return calculate_varga_longitude(longitude, 3)


@calculation_cache()
def calculate_d4(longitude):
    """
    Calculate the D4 (Chaturthamsha) longitude

    In the Chaturthamsha chart, each sign is divided into four parts of 7.5° each.

    Args:
        longitude (float): The longitude in the birth chart (0-360)

    Returns:
        float: The longitude in the D4 chart
    """
    return calculate_varga_longitude(longitude, 4)


@calculation_cache()
def calculate_d7(longitude):
    """
    Calculate the D7 (Saptamsha) longitude

    In the Saptamsha chart, each sign is divided into seven parts of 4.2857° each.

    Args:
        longitude (float): The longitude in the birth chart (0-360)

    Returns:
        float: The longitude in the D7 chart
    """
    return calculate_varga_longitude(longitude, 7)


@calculation_cache()
def calculate_d9(longitude):
    """
    Calculate the D9 (Navamsha) longitude

    In the Navamsha chart, each sign is divided into nine parts of 3.33° each.

    Args:
        longitude (float): The longitude in the birth chart (0-360)

    Returns:
        float: The longitude in the D9 chart
    """
    # Use the standard formula but round to avoid floating point issues
    result = calculate_varga_longitude(longitude, 9)
    # Round to 8 decimal places to avoid floating point comparison issues
    return round(result, 8)


@calculation_cache()
def calculate_d10(longitude):
    """
    Calculate the D10 (Dashamsha) longitude

    In the Dashamsha chart, each sign is divided into ten parts of 3° each.

    Args:
        longitude (float): The longitude in the birth chart (0-360)

    Returns:
        float: The longitude in the D10 chart
    """
    return calculate_varga_longitude(longitude, 10)


@calculation_cache()
def calculate_d12(longitude):
    """
    Calculate the D12 (Dwadashamsha) longitude

    In the Dwadashamsha chart, each sign is divided into twelve parts of 2.5° each.

    Args:
        longitude (float): The longitude in the birth chart (0-360)

    Returns:
        float: The longitude in the D12 chart
    """
    return calculate_varga_longitude(longitude, 12)


@calculation_cache()
def calculate_d16(longitude):
    """
    Calculate the D16 (Shodashamsha) longitude

    In the Shodashamsha chart, each sign is divided into sixteen parts of 1.875° each.

    Args:
        longitude (float): The longitude in the birth chart (0-360)

    Returns:
        float: The longitude in the D16 chart
    """
    return calculate_varga_longitude(longitude, 16)


@calculation_cache()
def calculate_d20(longitude):
    """
    Calculate the D20 (Vimshamsha) longitude

    In the Vimshamsha chart, each sign is divided into twenty parts of 1.5° each.

    Args:
        longitude (float): The longitude in the birth chart (0-360)

    Returns:
        float: The longitude in the D20 chart
    """
    return calculate_varga_longitude(longitude, 20)


@calculation_cache()
def calculate_d24(longitude):
    """
    Calculate the D24 (Chaturvimshamsha) longitude

    In the Chaturvimshamsha chart, each sign is divided into 24 parts of 1.25° each.

    Args:
        longitude (float): The longitude in the birth chart (0-360)

    Returns:
        float: The longitude in the D24 chart
    """
    return calculate_varga_longitude(longitude, 24)


@calculation_cache()
def calculate_d27(longitude):
    """
    Calculate the D27 (Saptavimshamsha) longitude

    In the Saptavimshamsha chart, each sign is divided into 27 parts of 1.11° each.

    Args:
        longitude (float): The longitude in the birth chart (0-360)

    Returns:
        float: The longitude in the D27 chart
    """
    return calculate_varga_longitude(longitude, 27)


@calculation_cache()
def calculate_d30(longitude):
    """
    Calculate the D30 (Trimshamsha) longitude

    In the Trimshamsha chart, each sign is divided into 30 parts of 1° each.

    Args:
        longitude (float): The longitude in the birth chart (0-360)

    Returns:
        float: The longitude in the D30 chart
    """
    # Get the sign number (0-11) and longitude within the sign (0-30)
    sign_num = int(longitude / 30)
    sign_lon = longitude % 30

    # Determine if the sign is odd or even
    is_odd_sign = sign_num % 2 == 0  # 0-based, so 0 = Aries (odd)

    # Calculate the resulting sign and longitude
    if is_odd_sign:
        # Odd signs (Aries, Gemini, etc.)
        if sign_lon < 5:
            result_sign = 2  # Mars - Gemini
        elif sign_lon < 10:
            result_sign = 8  # Saturn - Sagittarius
        elif sign_lon < 18:
            result_sign = 10  # Jupiter - Aquarius
        elif sign_lon < 25:
            result_sign = 6  # Mercury - Libra
        else:
            result_sign = 0  # Venus - Aries
    else:
        # Even signs (Taurus, Cancer, etc.)
        if sign_lon < 5:
            result_sign = 11  # Venus - Pisces
        elif sign_lon < 12:
            result_sign = 5  # Mercury - Virgo
        elif sign_lon < 20:
            result_sign = 9  # Jupiter - Capricorn
        elif sign_lon < 25:
            result_sign = 7  # Saturn - Scorpio
        else:
            result_sign = 3  # Mars - Cancer

    # Calculate the longitude within the resulting sign
    result_lon = (sign_lon % 5) * 6

    # Return the final longitude
    return result_sign * 30 + result_lon


@calculation_cache()
def calculate_d40(longitude):
    """
    Calculate the D40 (Khavedamsha) longitude

    In the Khavedamsha chart, each sign is divided into 40 parts of 0.75° each.

    Args:
        longitude (float): The longitude in the birth chart (0-360)

    Returns:
        float: The longitude in the D40 chart
    """
    return calculate_varga_longitude(longitude, 40)


@calculation_cache()
def calculate_d45(longitude):
    """
    Calculate the D45 (Akshavedamsha) longitude

    In the Akshavedamsha chart, each sign is divided into 45 parts of 0.67° each.

    Args:
        longitude (float): The longitude in the birth chart (0-360)

    Returns:
        float: The longitude in the D45 chart
    """
    return calculate_varga_longitude(longitude, 45)


@calculation_cache()
def calculate_d60(longitude):
    """
    Calculate the D60 (Shashtiamsha) longitude

    In the Shashtiamsha chart, each sign is divided into 60 parts of 0.5° each.

    Args:
        longitude (float): The longitude in the birth chart (0-360)

    Returns:
        float: The longitude in the D60 chart
    """
    return calculate_varga_longitude(longitude, 60)
