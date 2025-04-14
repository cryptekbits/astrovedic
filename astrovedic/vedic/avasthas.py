"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Planetary States (Avasthas) calculations
    for Vedic astrology.
"""

from typing import Dict, List, Optional, Tuple, Union
from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.object import GenericObject

# Baladi Avastha (Five-fold state)
BALADI_INFANT = "Infant"  # Bala (Infant)
BALADI_YOUTH = "Youth"    # Kumara (Youth)
BALADI_ADULT = "Adult"    # Yuva (Adult)
BALADI_OLD = "Old"        # Vriddha (Old)
BALADI_DEAD = "Dead"      # Mrita (Dead)

# Jagradadi Avastha (Three-fold state)
JAGRADADI_AWAKE = "Awake"       # Jagrad (Awake)
JAGRADADI_DREAMING = "Dreaming" # Swapna (Dreaming)
JAGRADADI_SLEEPING = "Sleeping" # Sushupti (Sleeping)

# Lajjitadi Avastha (Six-fold state)
LAJJITADI_DELIGHTED = "Delighted"     # Mudita (Delighted)
LAJJITADI_ASHAMED = "Ashamed"         # Lajjita (Ashamed)
LAJJITADI_EXALTED = "Exalted"         # Garvita (Exalted)
LAJJITADI_BURNING = "Burning"         # Kshudita (Burning)
LAJJITADI_AGITATED = "Agitated"       # Trashita (Agitated)
LAJJITADI_SEEKING = "Seeking"         # Mushita (Seeking)

def get_baladi_avastha(chart: Chart, planet_id: str) -> Dict[str, any]:
    """
    Calculate the Baladi Avastha (five-fold state) of a planet.
    
    Baladi Avastha is determined by the planet's position in a sign:
    - 0-6 degrees: Infant (Bala)
    - 6-12 degrees: Youth (Kumara)
    - 12-18 degrees: Adult (Yuva)
    - 18-24 degrees: Old (Vriddha)
    - 24-30 degrees: Dead (Mrita)
    
    Args:
        chart (Chart): The chart
        planet_id (str): The ID of the planet
    
    Returns:
        dict: Dictionary with Baladi Avastha information
    """
    # Get the planet
    planet = chart.getObject(planet_id)
    
    # Get the planet's longitude in the sign (0-30 degrees)
    sign_lon = planet.lon % 30
    
    # Determine the Baladi Avastha
    if sign_lon < 6:
        avastha = BALADI_INFANT
        strength = 60  # Moderate strength
    elif sign_lon < 12:
        avastha = BALADI_YOUTH
        strength = 80  # Good strength
    elif sign_lon < 18:
        avastha = BALADI_ADULT
        strength = 100  # Full strength
    elif sign_lon < 24:
        avastha = BALADI_OLD
        strength = 50  # Reduced strength
    else:
        avastha = BALADI_DEAD
        strength = 20  # Very weak
    
    return {
        'avastha': avastha,
        'strength': strength,
        'sign_longitude': sign_lon
    }

def get_jagradadi_avastha(chart: Chart, planet_id: str) -> Dict[str, any]:
    """
    Calculate the Jagradadi Avastha (three-fold state) of a planet.
    
    Jagradadi Avastha is determined by the planet's position in a sign:
    - 0-10 degrees: Awake (Jagrad)
    - 10-20 degrees: Dreaming (Swapna)
    - 20-30 degrees: Sleeping (Sushupti)
    
    Args:
        chart (Chart): The chart
        planet_id (str): The ID of the planet
    
    Returns:
        dict: Dictionary with Jagradadi Avastha information
    """
    # Get the planet
    planet = chart.getObject(planet_id)
    
    # Get the planet's longitude in the sign (0-30 degrees)
    sign_lon = planet.lon % 30
    
    # Determine the Jagradadi Avastha
    if sign_lon < 10:
        avastha = JAGRADADI_AWAKE
        strength = 100  # Full strength
    elif sign_lon < 20:
        avastha = JAGRADADI_DREAMING
        strength = 60   # Moderate strength
    else:
        avastha = JAGRADADI_SLEEPING
        strength = 30   # Weak
    
    return {
        'avastha': avastha,
        'strength': strength,
        'sign_longitude': sign_lon
    }

def get_lajjitadi_avastha(chart: Chart, planet_id: str) -> Dict[str, any]:
    """
    Calculate the Lajjitadi Avastha (six-fold state) of a planet.
    
    Lajjitadi Avastha is determined by the planet's relationship with the sign lord:
    - In own sign: Delighted (Mudita)
    - In debilitation sign: Ashamed (Lajjita)
    - In exaltation sign: Exalted (Garvita)
    - In enemy's sign: Burning (Kshudita)
    - Combust: Agitated (Trashita)
    - In friend's sign: Seeking (Mushita)
    
    Args:
        chart (Chart): The chart
        planet_id (str): The ID of the planet
    
    Returns:
        dict: Dictionary with Lajjitadi Avastha information
    """
    # Get the planet
    planet = chart.getObject(planet_id)
    
    # Get the planet's sign
    sign = planet.sign
    
    # Define sign lordships
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
    
    # Define exaltation signs
    exaltation_signs = {
        const.SUN: const.ARIES,
        const.MOON: const.TAURUS,
        const.MERCURY: const.VIRGO,
        const.VENUS: const.PISCES,
        const.MARS: const.CAPRICORN,
        const.JUPITER: const.CANCER,
        const.SATURN: const.LIBRA,
        const.RAHU: const.TAURUS,
        const.KETU: const.SCORPIO
    }
    
    # Define debilitation signs (opposite to exaltation)
    debilitation_signs = {
        const.SUN: const.LIBRA,
        const.MOON: const.SCORPIO,
        const.MERCURY: const.PISCES,
        const.VENUS: const.VIRGO,
        const.MARS: const.CANCER,
        const.JUPITER: const.CAPRICORN,
        const.SATURN: const.ARIES,
        const.RAHU: const.SCORPIO,
        const.KETU: const.TAURUS
    }
    
    # Define planetary friendships
    # This is a simplified version; in reality, friendships are more complex
    friends = {
        const.SUN: [const.MOON, const.MARS, const.JUPITER],
        const.MOON: [const.SUN, const.MERCURY],
        const.MERCURY: [const.SUN, const.VENUS],
        const.VENUS: [const.MERCURY, const.SATURN],
        const.MARS: [const.SUN, const.MOON, const.JUPITER],
        const.JUPITER: [const.SUN, const.MOON, const.MARS],
        const.SATURN: [const.MERCURY, const.VENUS],
        const.RAHU: [const.VENUS, const.SATURN],
        const.KETU: [const.MARS, const.VENUS]
    }
    
    # Define planetary enemies (simplified)
    enemies = {
        const.SUN: [const.SATURN, const.VENUS],
        const.MOON: [const.SATURN],
        const.MERCURY: [const.MOON],
        const.VENUS: [const.SUN, const.MOON],
        const.MARS: [const.MERCURY],
        const.JUPITER: [const.MERCURY, const.VENUS],
        const.SATURN: [const.SUN, const.MOON, const.MARS],
        const.RAHU: [const.SUN, const.MOON],
        const.KETU: [const.SUN, const.MOON]
    }
    
    # Get the sign lord
    sign_lord = sign_lords.get(sign)
    
    # Check if the planet is combust
    # For this, we need to check the distance from the Sun
    sun = chart.getObject(const.SUN)
    from astrovedic import angle
    orb = abs(angle.closestdistance(planet.lon, sun.lon))
    
    # Define combustion orbs for each planet
    combustion_orbs = {
        const.MOON: 12,
        const.MERCURY: 14,
        const.VENUS: 10,
        const.MARS: 17,
        const.JUPITER: 11,
        const.SATURN: 15,
        const.RAHU: 9,
        const.KETU: 9
    }
    
    is_combust = planet_id != const.SUN and orb <= combustion_orbs.get(planet_id, 10)
    
    # Determine the Lajjitadi Avastha
    if is_combust:
        avastha = LAJJITADI_AGITATED
        strength = 20  # Very weak
    elif sign == exaltation_signs.get(planet_id):
        avastha = LAJJITADI_EXALTED
        strength = 100  # Full strength
    elif sign == debilitation_signs.get(planet_id):
        avastha = LAJJITADI_ASHAMED
        strength = 10  # Extremely weak
    elif planet_id == sign_lord:
        avastha = LAJJITADI_DELIGHTED
        strength = 90  # Very strong
    elif sign_lord in enemies.get(planet_id, []):
        avastha = LAJJITADI_BURNING
        strength = 30  # Weak
    elif sign_lord in friends.get(planet_id, []):
        avastha = LAJJITADI_SEEKING
        strength = 70  # Strong
    else:
        # Default to Seeking if no other condition is met
        avastha = LAJJITADI_SEEKING
        strength = 50  # Moderate
    
    return {
        'avastha': avastha,
        'strength': strength,
        'sign': sign,
        'is_combust': is_combust
    }

def get_all_avasthas(chart: Chart, planet_id: str) -> Dict[str, Dict[str, any]]:
    """
    Calculate all Avasthas (states) for a planet.
    
    Args:
        chart (Chart): The chart
        planet_id (str): The ID of the planet
    
    Returns:
        dict: Dictionary with all Avastha information
    """
    return {
        'baladi': get_baladi_avastha(chart, planet_id),
        'jagradadi': get_jagradadi_avastha(chart, planet_id),
        'lajjitadi': get_lajjitadi_avastha(chart, planet_id)
    }

def get_all_planets_avasthas(chart: Chart) -> Dict[str, Dict[str, Dict[str, any]]]:
    """
    Calculate all Avasthas (states) for all planets in a chart.
    
    Args:
        chart (Chart): The chart
    
    Returns:
        dict: Dictionary with all Avastha information for all planets
    """
    # List of planets to calculate Avasthas for
    planets = [
        const.SUN, const.MOON, const.MERCURY, const.VENUS,
        const.MARS, const.JUPITER, const.SATURN, const.RAHU, const.KETU
    ]
    
    # Initialize the result
    result = {}
    
    # Calculate Avasthas for each planet
    for planet_id in planets:
        result[planet_id] = get_all_avasthas(chart, planet_id)
    
    return result
