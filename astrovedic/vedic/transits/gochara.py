"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Gochara (planetary transits) analysis
    for Vedic astrology.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic import angle

# Import core functions
from astrovedic.vedic.transits.core import get_house_number


def get_gochara_effects(natal_chart, transit_chart):
    """
    Get the Gochara (transit) effects for all planets
    
    Args:
        natal_chart (Chart): The natal chart
        transit_chart (Chart): The transit chart
    
    Returns:
        dict: Dictionary with Gochara effects for each planet
    """
    # Initialize the result
    gochara_effects = {}
    
    # Get the Gochara effects for each planet
    for planet_id in const.LIST_OBJECTS_VEDIC:
        gochara_effects[planet_id] = get_planet_gochara(natal_chart, transit_chart, planet_id)
    
    return gochara_effects


def get_planet_gochara(natal_chart, transit_chart, planet_id):
    """
    Get the Gochara (transit) effects for a specific planet
    
    Args:
        natal_chart (Chart): The natal chart
        transit_chart (Chart): The transit chart
        planet_id (str): The ID of the planet
    
    Returns:
        dict: Dictionary with Gochara effects for the planet
    """
    # Get the transit planet
    transit_planet = transit_chart.getObject(planet_id)
    
    # Get the house position of the transit planet in the natal chart
    house_num = get_house_number(natal_chart, transit_planet.lon)
    
    # Get the Moon's natal position
    natal_moon = natal_chart.getObject(const.MOON)
    moon_sign = natal_moon.sign
    
    # Calculate the house from the Moon
    moon_house = get_house_from_moon(moon_sign, transit_planet.sign)
    
    # Get the effect based on the house from the Moon
    effect = get_effect_from_moon(planet_id, moon_house)
    
    # Get the Vedha (obstruction) effects
    vedha_effects = get_vedha_effects(natal_chart, transit_chart, planet_id)
    
    # Get the Argala (intervention) effects
    argala_effects = get_argala_effects(natal_chart, transit_chart, planet_id)
    
    # Calculate the overall strength
    strength = get_gochara_strength(effect, vedha_effects, argala_effects)
    
    return {
        'house': house_num,
        'moon_house': moon_house,
        'effect': effect,
        'vedha_effects': vedha_effects,
        'argala_effects': argala_effects,
        'strength': strength
    }


def get_house_from_moon(moon_sign, planet_sign):
    """
    Calculate the house number from the Moon's sign
    
    Args:
        moon_sign (str): The Moon's sign
        planet_sign (str): The planet's sign
    
    Returns:
        int: The house number from the Moon (1-12)
    """
    # Get the sign numbers
    moon_sign_num = const.LIST_SIGNS.index(moon_sign)
    planet_sign_num = const.LIST_SIGNS.index(planet_sign)
    
    # Calculate the house from the Moon
    house_num = ((planet_sign_num - moon_sign_num) % 12) + 1
    
    return house_num


def get_effect_from_moon(planet_id, moon_house):
    """
    Get the effect of a planet's transit based on the house from the Moon
    
    Args:
        planet_id (str): The ID of the planet
        moon_house (int): The house number from the Moon (1-12)
    
    Returns:
        dict: Dictionary with effect information
    """
    # Define the effects for each planet based on the house from the Moon
    effects = {
        const.SUN: {
            1: {'effect': 'Unfavorable', 'description': 'Health issues, ego conflicts'},
            2: {'effect': 'Unfavorable', 'description': 'Financial stress, family conflicts'},
            3: {'effect': 'Favorable', 'description': 'Courage, initiative, success in endeavors'},
            4: {'effect': 'Unfavorable', 'description': 'Mental stress, domestic problems'},
            5: {'effect': 'Favorable', 'description': 'Success, recognition, creativity'},
            6: {'effect': 'Favorable', 'description': 'Victory over enemies, health improvement'},
            7: {'effect': 'Unfavorable', 'description': 'Relationship issues, conflicts'},
            8: {'effect': 'Unfavorable', 'description': 'Health concerns, obstacles'},
            9: {'effect': 'Favorable', 'description': 'Spiritual growth, success in higher education'},
            10: {'effect': 'Favorable', 'description': 'Career success, recognition'},
            11: {'effect': 'Favorable', 'description': 'Gains, fulfillment of desires'},
            12: {'effect': 'Unfavorable', 'description': 'Expenses, isolation, hidden enemies'}
        },
        const.MOON: {
            1: {'effect': 'Mixed', 'description': 'Emotional fluctuations, self-awareness'},
            2: {'effect': 'Favorable', 'description': 'Financial gains, family harmony'},
            3: {'effect': 'Favorable', 'description': 'Communication skills, short journeys'},
            4: {'effect': 'Favorable', 'description': 'Domestic happiness, emotional stability'},
            5: {'effect': 'Favorable', 'description': 'Creativity, romance, enjoyment'},
            6: {'effect': 'Unfavorable', 'description': 'Health issues, conflicts with subordinates'},
            7: {'effect': 'Mixed', 'description': 'Relationship fluctuations, public interactions'},
            8: {'effect': 'Unfavorable', 'description': 'Emotional distress, transformation'},
            9: {'effect': 'Favorable', 'description': 'Spiritual growth, higher learning'},
            10: {'effect': 'Favorable', 'description': 'Professional success, public recognition'},
            11: {'effect': 'Favorable', 'description': 'Social connections, fulfillment of desires'},
            12: {'effect': 'Unfavorable', 'description': 'Isolation, subconscious issues, expenses'}
        },
        const.MERCURY: {
            1: {'effect': 'Mixed', 'description': 'Intellectual activity, communication focus'},
            2: {'effect': 'Favorable', 'description': 'Financial gains through communication, learning'},
            3: {'effect': 'Favorable', 'description': 'Enhanced communication, writing, short trips'},
            4: {'effect': 'Mixed', 'description': 'Intellectual activities at home, family discussions'},
            5: {'effect': 'Favorable', 'description': 'Creative thinking, intellectual games, teaching'},
            6: {'effect': 'Favorable', 'description': 'Problem-solving, analytical work, health improvement'},
            7: {'effect': 'Mixed', 'description': 'Negotiations, contracts, intellectual partnerships'},
            8: {'effect': 'Unfavorable', 'description': 'Mental stress, research, investigation'},
            9: {'effect': 'Favorable', 'description': 'Higher education, publishing, foreign communications'},
            10: {'effect': 'Favorable', 'description': 'Professional communications, intellectual recognition'},
            11: {'effect': 'Favorable', 'description': 'Networking, group projects, technological gains'},
            12: {'effect': 'Unfavorable', 'description': 'Mental confusion, secret communications, isolation'}
        },
        const.VENUS: {
            1: {'effect': 'Favorable', 'description': 'Enhanced charm, focus on appearance and pleasure'},
            2: {'effect': 'Favorable', 'description': 'Financial gains, luxury purchases, family harmony'},
            3: {'effect': 'Favorable', 'description': 'Pleasant communications, artistic expression'},
            4: {'effect': 'Favorable', 'description': 'Domestic harmony, home beautification'},
            5: {'effect': 'Favorable', 'description': 'Romance, creativity, entertainment, children'},
            6: {'effect': 'Mixed', 'description': 'Service to others, health improvement through balance'},
            7: {'effect': 'Favorable', 'description': 'Relationships, partnerships, marriage, harmony'},
            8: {'effect': 'Mixed', 'description': 'Shared resources, intimacy, transformation'},
            9: {'effect': 'Favorable', 'description': 'Travel for pleasure, cultural experiences'},
            10: {'effect': 'Mixed', 'description': 'Career in arts or luxury, public image'},
            11: {'effect': 'Favorable', 'description': 'Social enjoyment, friendship, group harmony'},
            12: {'effect': 'Mixed', 'description': 'Secret relationships, spiritual love, sacrifice'}
        },
        const.MARS: {
            1: {'effect': 'Unfavorable', 'description': 'Aggression, accidents, conflicts, energy'},
            2: {'effect': 'Unfavorable', 'description': 'Financial losses, family conflicts'},
            3: {'effect': 'Favorable', 'description': 'Courage, initiative, siblings, communication'},
            4: {'effect': 'Unfavorable', 'description': 'Domestic conflicts, property issues'},
            5: {'effect': 'Mixed', 'description': 'Creative energy, competitive sports, romance'},
            6: {'effect': 'Favorable', 'description': 'Victory over enemies, health improvement'},
            7: {'effect': 'Unfavorable', 'description': 'Relationship conflicts, legal disputes'},
            8: {'effect': 'Unfavorable', 'description': 'Surgery, accidents, conflicts over shared resources'},
            9: {'effect': 'Favorable', 'description': 'Religious activities, higher education'},
            10: {'effect': 'Favorable', 'description': 'Career advancement, leadership, authority'},
            11: {'effect': 'Favorable', 'description': 'Gains through effort, achievement of goals'},
            12: {'effect': 'Unfavorable', 'description': 'Hidden enemies, isolation, self-undoing'}
        },
        const.JUPITER: {
            1: {'effect': 'Favorable', 'description': 'Growth, optimism, wisdom, expansion'},
            2: {'effect': 'Favorable', 'description': 'Financial gains, family prosperity'},
            3: {'effect': 'Favorable', 'description': 'Positive communication, learning, short journeys'},
            4: {'effect': 'Favorable', 'description': 'Domestic happiness, property gains'},
            5: {'effect': 'Favorable', 'description': 'Children, creativity, education, romance'},
            6: {'effect': 'Mixed', 'description': 'Health improvement, service, debt'},
            7: {'effect': 'Mixed', 'description': 'Partnerships, legal matters, marriage'},
            8: {'effect': 'Mixed', 'description': 'Transformation, inheritance, research'},
            9: {'effect': 'Favorable', 'description': 'Spirituality, higher education, fortune'},
            10: {'effect': 'Favorable', 'description': 'Career success, recognition, authority'},
            11: {'effect': 'Favorable', 'description': 'Gains, fulfillment of desires, social connections'},
            12: {'effect': 'Mixed', 'description': 'Spiritual growth, expenses, isolation'}
        },
        const.SATURN: {
            1: {'effect': 'Unfavorable', 'description': 'Health issues, restrictions, delays'},
            2: {'effect': 'Unfavorable', 'description': 'Financial restrictions, family responsibilities'},
            3: {'effect': 'Favorable', 'description': 'Disciplined communication, focused learning'},
            4: {'effect': 'Unfavorable', 'description': 'Domestic challenges, property issues'},
            5: {'effect': 'Unfavorable', 'description': 'Challenges with children, creative blocks'},
            6: {'effect': 'Favorable', 'description': 'Health improvement through discipline, service'},
            7: {'effect': 'Unfavorable', 'description': 'Relationship challenges, delays in partnerships'},
            8: {'effect': 'Favorable', 'description': 'Transformation through hardship, research'},
            9: {'effect': 'Unfavorable', 'description': 'Obstacles in higher education, travel delays'},
            10: {'effect': 'Favorable', 'description': 'Career advancement through hard work'},
            11: {'effect': 'Favorable', 'description': 'Gains through perseverance, lasting friendships'},
            12: {'effect': 'Unfavorable', 'description': 'Isolation, hidden enemies, spiritual tests'}
        },
        const.RAHU: {
            1: {'effect': 'Unfavorable', 'description': 'Confusion about identity, obsessions'},
            2: {'effect': 'Mixed', 'description': 'Unusual financial gains or losses, foreign resources'},
            3: {'effect': 'Favorable', 'description': 'Unconventional communication, foreign connections'},
            4: {'effect': 'Unfavorable', 'description': 'Domestic disturbances, property issues'},
            5: {'effect': 'Mixed', 'description': 'Unusual creative pursuits, unconventional romance'},
            6: {'effect': 'Favorable', 'description': 'Overcoming enemies, unusual health treatments'},
            7: {'effect': 'Unfavorable', 'description': 'Deceptive partnerships, unusual relationships'},
            8: {'effect': 'Mixed', 'description': 'Occult interests, sudden transformations'},
            9: {'effect': 'Mixed', 'description': 'Unorthodox beliefs, foreign travel'},
            10: {'effect': 'Mixed', 'description': 'Unconventional career, sudden recognition'},
            11: {'effect': 'Favorable', 'description': 'Unusual gains, eccentric friends, technology'},
            12: {'effect': 'Unfavorable', 'description': 'Hidden activities, subconscious disturbances'}
        },
        const.KETU: {
            1: {'effect': 'Unfavorable', 'description': 'Identity crisis, spiritual detachment'},
            2: {'effect': 'Unfavorable', 'description': 'Financial losses, detachment from possessions'},
            3: {'effect': 'Mixed', 'description': 'Spiritual communication, psychic abilities'},
            4: {'effect': 'Unfavorable', 'description': 'Domestic disturbances, emotional detachment'},
            5: {'effect': 'Unfavorable', 'description': 'Challenges with children, detachment from pleasure'},
            6: {'effect': 'Favorable', 'description': 'Healing abilities, overcoming enemies'},
            7: {'effect': 'Unfavorable', 'description': 'Relationship dissolution, spiritual partnerships'},
            8: {'effect': 'Favorable', 'description': 'Spiritual transformation, psychic abilities'},
            9: {'effect': 'Favorable', 'description': 'Spiritual wisdom, moksha, liberation'},
            10: {'effect': 'Unfavorable', 'description': 'Career setbacks, detachment from status'},
            11: {'effect': 'Mixed', 'description': 'Spiritual gains, detachment from desires'},
            12: {'effect': 'Favorable', 'description': 'Spiritual liberation, psychic abilities, isolation'}
        }
    }
    
    # Get the effect for the planet and house
    if planet_id in effects and moon_house in effects[planet_id]:
        return effects[planet_id][moon_house]
    else:
        return {'effect': 'Neutral', 'description': 'No specific effect'}


def get_vedha_effects(natal_chart, transit_chart, planet_id):
    """
    Get the Vedha (obstruction) effects for a planet's transit
    
    Args:
        natal_chart (Chart): The natal chart
        transit_chart (Chart): The transit chart
        planet_id (str): The ID of the planet
    
    Returns:
        list: List of Vedha effects
    """
    # Initialize the result
    vedha_effects = []
    
    # Get the transit planet
    transit_planet = transit_chart.getObject(planet_id)
    
    # Get the house position of the transit planet in the natal chart
    house_num = get_house_number(natal_chart, transit_planet.lon)
    
    # Define the Vedha houses for each house
    vedha_houses = {
        1: [7],
        2: [12],
        3: [11],
        4: [10],
        5: [9],
        6: [8],
        7: [1],
        8: [6],
        9: [5],
        10: [4],
        11: [3],
        12: [2]
    }
    
    # Check if there are planets in the Vedha houses
    if house_num in vedha_houses:
        for vedha_house in vedha_houses[house_num]:
            # Check if there are planets in the Vedha house
            for vedha_planet_id in const.LIST_OBJECTS_VEDIC:
                vedha_planet = transit_chart.getObject(vedha_planet_id)
                vedha_house_num = get_house_number(natal_chart, vedha_planet.lon)
                
                if vedha_house_num == vedha_house:
                    # Add the Vedha effect
                    vedha_effects.append({
                        'planet': vedha_planet_id,
                        'house': vedha_house,
                        'description': f"Transit {vedha_planet_id} in house {vedha_house} obstructs the effects of transit {planet_id} in house {house_num}"
                    })
    
    return vedha_effects


def get_argala_effects(natal_chart, transit_chart, planet_id):
    """
    Get the Argala (intervention) effects for a planet's transit
    
    Args:
        natal_chart (Chart): The natal chart
        transit_chart (Chart): The transit chart
        planet_id (str): The ID of the planet
    
    Returns:
        list: List of Argala effects
    """
    # Initialize the result
    argala_effects = []
    
    # Get the transit planet
    transit_planet = transit_chart.getObject(planet_id)
    
    # Get the house position of the transit planet in the natal chart
    house_num = get_house_number(natal_chart, transit_planet.lon)
    
    # Define the Argala houses for each house
    argala_houses = {
        1: [2, 4, 11],
        2: [3, 5, 12],
        3: [4, 6, 1],
        4: [5, 7, 2],
        5: [6, 8, 3],
        6: [7, 9, 4],
        7: [8, 10, 5],
        8: [9, 11, 6],
        9: [10, 12, 7],
        10: [11, 1, 8],
        11: [12, 2, 9],
        12: [1, 3, 10]
    }
    
    # Check if there are planets in the Argala houses
    if house_num in argala_houses:
        for argala_house in argala_houses[house_num]:
            # Check if there are planets in the Argala house
            for argala_planet_id in const.LIST_OBJECTS_VEDIC:
                argala_planet = transit_chart.getObject(argala_planet_id)
                argala_house_num = get_house_number(natal_chart, argala_planet.lon)
                
                if argala_house_num == argala_house:
                    # Add the Argala effect
                    argala_effects.append({
                        'planet': argala_planet_id,
                        'house': argala_house,
                        'description': f"Transit {argala_planet_id} in house {argala_house} intervenes with the effects of transit {planet_id} in house {house_num}"
                    })
    
    return argala_effects


def get_gochara_strength(effect, vedha_effects, argala_effects):
    """
    Calculate the overall strength of a Gochara effect
    
    Args:
        effect (dict): The base effect
        vedha_effects (list): The Vedha effects
        argala_effects (list): The Argala effects
    
    Returns:
        dict: Dictionary with strength information
    """
    # Initialize the score
    score = 0
    
    # Assign a base score based on the effect
    if effect['effect'] == 'Favorable':
        score = 2
    elif effect['effect'] == 'Mixed':
        score = 0
    elif effect['effect'] == 'Unfavorable':
        score = -2
    else:  # Neutral
        score = 0
    
    # Adjust the score based on Vedha effects
    for vedha in vedha_effects:
        # Vedha reduces the effect
        score -= 1
    
    # Adjust the score based on Argala effects
    for argala in argala_effects:
        # Argala enhances the effect
        if score > 0:
            score += 0.5
        elif score < 0:
            score -= 0.5
    
    # Determine the strength based on the score
    if score >= 2:
        strength = 'Strong Favorable'
    elif score > 0:
        strength = 'Moderate Favorable'
    elif score == 0:
        strength = 'Neutral'
    elif score > -2:
        strength = 'Moderate Unfavorable'
    else:
        strength = 'Strong Unfavorable'
    
    return {
        'score': score,
        'strength': strength
    }
