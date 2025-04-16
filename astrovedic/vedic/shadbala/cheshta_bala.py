"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Cheshta Bala (motional strength) calculations
    for Shadbala in Vedic astrology.
"""

from astrovedic import const


def calculate_cheshta_bala(chart, planet_id):
    """
    Calculate Cheshta Bala (motional strength) for a planet

    In Vedic astrology, Cheshta Bala is based on the planet's motion relative to its
    mean motion and position in its synodic cycle. For the Sun and Moon, which don't
    have traditional Cheshta Bala, their strength is derived from Ayana Bala (Sun)
    and Paksha Bala (Moon).

    For planets (Mars-Saturn):
    - Retrograde motion (especially when slow) increases Cheshta Bala
    - The planet's position relative to the Sun (Cheshta Kendra) affects strength
    - Deviation from mean speed affects strength

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet to analyze

    Returns:
        dict: Dictionary with Cheshta Bala information
    """
    # Get the planet from the chart
    planet = chart.getObject(planet_id)

    # Maximum value (in Virupas)
    max_value = 60.0

    # Special case for Sun: Use half of Ayana Bala
    if planet_id == const.SUN:
        from astrovedic.vedic.shadbala.kala_bala import calculate_ayana_bala
        ayana_bala = calculate_ayana_bala(chart, planet_id)
        value = ayana_bala['value'] / 2.0
        current_speed = planet.lonspeed if hasattr(planet, 'lonspeed') else 0.0
        max_speed = get_max_speed(planet_id)
        return {
            'value': value,
            'description': 'Based on half of Ayana Bala',
            'source': 'ayana_bala',
            'source_value': ayana_bala['value'],
            'daily_motion': current_speed,
            'max_speed': max_speed,
            'is_retrograde': False,
            'relative_speed': current_speed / max_speed if max_speed > 0 else 0.0
        }

    # Special case for Moon: Use half of Paksha Bala
    if planet_id == const.MOON:
        from astrovedic.vedic.shadbala.kala_bala import calculate_paksha_bala
        paksha_bala = calculate_paksha_bala(chart, planet_id)
        value = paksha_bala['value'] / 2.0
        current_speed = planet.lonspeed if hasattr(planet, 'lonspeed') else 0.0
        max_speed = get_max_speed(planet_id)
        return {
            'value': value,
            'description': 'Based on half of Paksha Bala',
            'source': 'paksha_bala',
            'source_value': paksha_bala['value'],
            'daily_motion': current_speed,
            'max_speed': max_speed,
            'is_retrograde': False,
            'relative_speed': current_speed / max_speed if max_speed > 0 else 0.0
        }

    # Rahu and Ketu don't have traditional Cheshta Bala
    if planet_id in [const.RAHU, const.KETU]:
        current_speed = abs(planet.lonspeed) if hasattr(planet, 'lonspeed') else 0.0
        max_speed = get_max_speed(planet_id)
        return {
            'value': 0.0,
            'description': 'Rahu and Ketu do not have Cheshta Bala',
            'current_speed': current_speed,
            'mean_speed': get_mean_speed(planet_id),
            'daily_motion': current_speed,
            'max_speed': max_speed,
            'is_retrograde': True,
            'relative_speed': current_speed / max_speed if max_speed > 0 else 0.0
        }

    # For planets (Mars, Mercury, Jupiter, Venus, Saturn)
    # Get the Sun
    sun = chart.getObject(const.SUN)

    # Check if the planet is retrograde
    is_retrograde = planet.isRetrograde()

    # Get the planet's daily motion (current speed)
    current_speed = abs(planet.lonspeed)

    # Get the mean daily motion for the planet
    mean_speed = get_mean_speed(planet_id)

    # Calculate the speed ratio (current/mean)
    speed_ratio = current_speed / mean_speed if mean_speed > 0 else 0.0

    # Calculate the Cheshta Kendra using mean longitude
    # In standard Vedic astrology, Cheshta Kendra is the angular distance
    # between the planet's mean longitude and true longitude
    # For simplicity, we'll use the angular distance from the Sun as an approximation
    from astrovedic import angle
    cheshta_kendra = angle.distance(sun.lon, planet.lon) % 180

    # Normalize Cheshta Kendra to 0-90 degrees (distance from conjunction or opposition)
    if cheshta_kendra > 90:
        cheshta_kendra = 180 - cheshta_kendra

    # Calculate the base Cheshta Bala based on speed ratio using standard method
    # In Vedic astrology, planets get strength based on their speed relative to mean speed
    # Retrograde planets get higher strength when moving slowly
    if is_retrograde:
        # Retrograde planets get more strength, especially when moving slowly
        speed_factor = min(2.0 * (1.0 - speed_ratio), 2.0)
    else:
        # Direct planets get strength based on how close they are to mean speed
        speed_deviation = abs(speed_ratio - 1.0)
        speed_factor = 1.0 - min(speed_deviation * 0.5, 0.5)

    # Calculate the Cheshta Kendra factor (0-1) using standard method
    # Planets at conjunction or opposition (0° or 180°) get maximum strength
    # Planets at 90° from the Sun get minimum strength
    kendra_factor = 1.0 - (cheshta_kendra / 90.0)

    # Calculate the final Cheshta Bala value using standard combination
    value = max_value * (speed_factor * 0.6 + kendra_factor * 0.4)

    # Ensure the value doesn't exceed the maximum
    value = min(value, max_value)

    # Create a descriptive message
    if is_retrograde:
        description = f'Retrograde motion with speed ratio {speed_ratio:.2f} and Cheshta Kendra {cheshta_kendra:.2f}°'
    else:
        description = f'Direct motion with speed ratio {speed_ratio:.2f} and Cheshta Kendra {cheshta_kendra:.2f}°'

    # Return detailed information
    return {
        'value': value,
        'description': description,
        'is_retrograde': is_retrograde,
        'current_speed': current_speed,
        'mean_speed': mean_speed,
        'speed_ratio': speed_ratio,
        'speed_factor': speed_factor,
        'cheshta_kendra': cheshta_kendra,
        'kendra_factor': kendra_factor,
        'daily_motion': current_speed,
        'max_speed': get_max_speed(planet_id),
        'relative_speed': current_speed / get_max_speed(planet_id) if get_max_speed(planet_id) > 0 else 0.0
    }


def get_mean_speed(planet_id):
    """
    Get the mean daily motion for a planet

    Args:
        planet_id (str): The ID of the planet

    Returns:
        float: The mean daily motion in degrees per day
    """
    # Mean daily motion for each planet (in degrees per day)
    mean_speeds = {
        const.SUN: 0.9856,      # ~1 degree per day
        const.MOON: 13.1764,    # ~13 degrees per day
        const.MERCURY: 1.3833,  # ~1.38 degrees per day
        const.VENUS: 1.2021,    # ~1.2 degrees per day
        const.MARS: 0.5242,     # ~0.52 degrees per day
        const.JUPITER: 0.0831,  # ~0.08 degrees per day
        const.SATURN: 0.0334,   # ~0.03 degrees per day
        const.RAHU: 0.0529,     # ~0.05 degrees per day (retrograde)
        const.KETU: 0.0529      # ~0.05 degrees per day (retrograde)
    }

    return mean_speeds.get(planet_id, 1.0)


def get_max_speed(planet_id):
    """
    Get the maximum possible speed for a planet

    Args:
        planet_id (str): The ID of the planet

    Returns:
        float: The maximum possible speed in degrees per day
    """
    # Maximum speeds for each planet (in degrees per day)
    max_speeds = {
        const.MERCURY: 2.0,
        const.VENUS: 1.25,
        const.MARS: 0.75,
        const.JUPITER: 0.4,
        const.SATURN: 0.2,
        const.RAHU: 0.05,
        const.KETU: 0.05
    }

    return max_speeds.get(planet_id, 1.0)
