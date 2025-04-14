"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Dasha compatibility analysis
    for Vedic astrology.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos

from astrovedic.vedic.compatibility.dasha.helpers import (
    get_dasha, get_antardasha, get_dasha_lord, get_antardasha_lord
)


def get_dasha_compatibility(chart1, chart2):
    """
    Get the Dasha compatibility between two charts

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with Dasha compatibility information
    """
    # Get the current date
    from datetime import datetime
    current_date = Datetime.fromDatetime(datetime.now())

    # Get the current Dasha for each chart
    dasha1 = get_dasha(chart1, current_date)
    dasha2 = get_dasha(chart2, current_date)

    # Get the Dasha lords
    dasha_lord1 = get_dasha_lord(dasha1)
    dasha_lord2 = get_dasha_lord(dasha2)

    # Calculate the compatibility between the Dasha lords
    compatibility = calculate_planet_compatibility(dasha_lord1, dasha_lord2)

    # Generate the description
    description = generate_dasha_compatibility_description(dasha_lord1, dasha_lord2, compatibility)

    return {
        'dasha1': dasha1,
        'dasha2': dasha2,
        'dasha_lord1': dasha_lord1,
        'dasha_lord2': dasha_lord2,
        'compatibility': compatibility,
        'score': compatibility['score'],
        'description': description
    }


def get_antardasha_compatibility(chart1, chart2):
    """
    Get the Antardasha compatibility between two charts

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with Antardasha compatibility information
    """
    # Get the current date
    from datetime import datetime
    current_date = Datetime.fromDatetime(datetime.now())

    # Get the current Antardasha for each chart
    antardasha1 = get_antardasha(chart1, current_date)
    antardasha2 = get_antardasha(chart2, current_date)

    # Get the Antardasha lords
    antardasha_lord1 = get_antardasha_lord(antardasha1)
    antardasha_lord2 = get_antardasha_lord(antardasha2)

    # Calculate the compatibility between the Antardasha lords
    compatibility = calculate_planet_compatibility(antardasha_lord1, antardasha_lord2)

    # Generate the description
    description = generate_antardasha_compatibility_description(antardasha_lord1, antardasha_lord2, compatibility)

    return {
        'antardasha1': antardasha1,
        'antardasha2': antardasha2,
        'antardasha_lord1': antardasha_lord1,
        'antardasha_lord2': antardasha_lord2,
        'compatibility': compatibility,
        'score': compatibility['score'],
        'description': description
    }


def get_dasha_periods_compatibility(chart1, chart2):
    """
    Get the compatibility of Dasha periods between two charts

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with Dasha periods compatibility information
    """
    # Get the current date
    from datetime import datetime
    current_date = Datetime.fromDatetime(datetime.now())

    # Get the current Dasha and Antardasha for each chart
    dasha1 = get_dasha(chart1, current_date)
    dasha2 = get_dasha(chart2, current_date)
    antardasha1 = get_antardasha(chart1, current_date)
    antardasha2 = get_antardasha(chart2, current_date)

    # Get the Dasha and Antardasha lords
    dasha_lord1 = get_dasha_lord(dasha1)
    dasha_lord2 = get_dasha_lord(dasha2)
    antardasha_lord1 = get_antardasha_lord(antardasha1)
    antardasha_lord2 = get_antardasha_lord(antardasha2)

    # Calculate the compatibility between the Dasha lords
    dasha_compatibility = calculate_planet_compatibility(dasha_lord1, dasha_lord2)

    # Calculate the compatibility between the Antardasha lords
    antardasha_compatibility = calculate_planet_compatibility(antardasha_lord1, antardasha_lord2)

    # Calculate the compatibility between Dasha lord 1 and Antardasha lord 2
    dasha1_antardasha2_compatibility = calculate_planet_compatibility(dasha_lord1, antardasha_lord2)

    # Calculate the compatibility between Dasha lord 2 and Antardasha lord 1
    dasha2_antardasha1_compatibility = calculate_planet_compatibility(dasha_lord2, antardasha_lord1)

    # Calculate the overall compatibility score
    overall_score = (
        dasha_compatibility['score'] * 0.4 +
        antardasha_compatibility['score'] * 0.3 +
        dasha1_antardasha2_compatibility['score'] * 0.15 +
        dasha2_antardasha1_compatibility['score'] * 0.15
    )

    # Generate the description
    description = generate_dasha_periods_compatibility_description(
        dasha_lord1, dasha_lord2, antardasha_lord1, antardasha_lord2,
        dasha_compatibility, antardasha_compatibility,
        dasha1_antardasha2_compatibility, dasha2_antardasha1_compatibility,
        overall_score
    )

    # Define favorable and challenging periods based on compatibility scores
    favorable_periods = []
    challenging_periods = []

    # Add periods based on Dasha compatibility
    if dasha_compatibility['score'] >= 7:
        favorable_periods.append(f"{dasha_lord1}-{dasha_lord2} Dasha period")
    elif dasha_compatibility['score'] <= 3:
        challenging_periods.append(f"{dasha_lord1}-{dasha_lord2} Dasha period")

    # Add periods based on Antardasha compatibility
    if antardasha_compatibility['score'] >= 7:
        favorable_periods.append(f"{antardasha_lord1}-{antardasha_lord2} Antardasha period")
    elif antardasha_compatibility['score'] <= 3:
        challenging_periods.append(f"{antardasha_lord1}-{antardasha_lord2} Antardasha period")

    # Add periods based on cross-compatibility
    if dasha1_antardasha2_compatibility['score'] >= 7:
        favorable_periods.append(f"{dasha_lord1}-{antardasha_lord2} cross-period")
    elif dasha1_antardasha2_compatibility['score'] <= 3:
        challenging_periods.append(f"{dasha_lord1}-{antardasha_lord2} cross-period")

    if dasha2_antardasha1_compatibility['score'] >= 7:
        favorable_periods.append(f"{dasha_lord2}-{antardasha_lord1} cross-period")
    elif dasha2_antardasha1_compatibility['score'] <= 3:
        challenging_periods.append(f"{dasha_lord2}-{antardasha_lord1} cross-period")

    return {
        'dasha_lord1': dasha_lord1,
        'dasha_lord2': dasha_lord2,
        'antardasha_lord1': antardasha_lord1,
        'antardasha_lord2': antardasha_lord2,
        'dasha_compatibility': dasha_compatibility,
        'antardasha_compatibility': antardasha_compatibility,
        'dasha1_antardasha2_compatibility': dasha1_antardasha2_compatibility,
        'dasha2_antardasha1_compatibility': dasha2_antardasha1_compatibility,
        'overall_score': overall_score,
        'description': description,
        'favorable_periods': favorable_periods,
        'challenging_periods': challenging_periods
    }


def calculate_planet_compatibility(planet1, planet2):
    """
    Calculate the compatibility between two planets

    Args:
        planet1 (str): The first planet
        planet2 (str): The second planet

    Returns:
        dict: Dictionary with planet compatibility information
    """
    # Define the planetary friendships
    friendship_map = {
        const.SUN: {
            const.SUN: 'Friend',
            const.MOON: 'Friend',
            const.MARS: 'Friend',
            const.MERCURY: 'Enemy',
            const.JUPITER: 'Friend',
            const.VENUS: 'Enemy',
            const.SATURN: 'Enemy',
            const.RAHU: 'Enemy',
            const.KETU: 'Enemy'
        },
        const.MOON: {
            const.SUN: 'Friend',
            const.MOON: 'Friend',
            const.MARS: 'Neutral',
            const.MERCURY: 'Friend',
            const.JUPITER: 'Friend',
            const.VENUS: 'Neutral',
            const.SATURN: 'Neutral',
            const.RAHU: 'Enemy',
            const.KETU: 'Enemy'
        },
        const.MARS: {
            const.SUN: 'Friend',
            const.MOON: 'Friend',
            const.MARS: 'Friend',
            const.MERCURY: 'Neutral',
            const.JUPITER: 'Friend',
            const.VENUS: 'Enemy',
            const.SATURN: 'Enemy',
            const.RAHU: 'Enemy',
            const.KETU: 'Enemy'
        },
        const.MERCURY: {
            const.SUN: 'Neutral',
            const.MOON: 'Friend',
            const.MARS: 'Neutral',
            const.MERCURY: 'Friend',
            const.JUPITER: 'Neutral',
            const.VENUS: 'Friend',
            const.SATURN: 'Friend',
            const.RAHU: 'Neutral',
            const.KETU: 'Neutral'
        },
        const.JUPITER: {
            const.SUN: 'Friend',
            const.MOON: 'Friend',
            const.MARS: 'Friend',
            const.MERCURY: 'Enemy',
            const.JUPITER: 'Friend',
            const.VENUS: 'Enemy',
            const.SATURN: 'Enemy',
            const.RAHU: 'Enemy',
            const.KETU: 'Enemy'
        },
        const.VENUS: {
            const.SUN: 'Enemy',
            const.MOON: 'Neutral',
            const.MARS: 'Neutral',
            const.MERCURY: 'Friend',
            const.JUPITER: 'Neutral',
            const.VENUS: 'Friend',
            const.SATURN: 'Friend',
            const.RAHU: 'Neutral',
            const.KETU: 'Neutral'
        },
        const.SATURN: {
            const.SUN: 'Enemy',
            const.MOON: 'Enemy',
            const.MARS: 'Enemy',
            const.MERCURY: 'Friend',
            const.JUPITER: 'Enemy',
            const.VENUS: 'Friend',
            const.SATURN: 'Friend',
            const.RAHU: 'Friend',
            const.KETU: 'Friend'
        },
        const.RAHU: {
            const.SUN: 'Enemy',
            const.MOON: 'Enemy',
            const.MARS: 'Enemy',
            const.MERCURY: 'Neutral',
            const.JUPITER: 'Enemy',
            const.VENUS: 'Neutral',
            const.SATURN: 'Friend',
            const.RAHU: 'Friend',
            const.KETU: 'Enemy'
        },
        const.KETU: {
            const.SUN: 'Enemy',
            const.MOON: 'Enemy',
            const.MARS: 'Enemy',
            const.MERCURY: 'Neutral',
            const.JUPITER: 'Enemy',
            const.VENUS: 'Neutral',
            const.SATURN: 'Friend',
            const.RAHU: 'Enemy',
            const.KETU: 'Friend'
        }
    }

    # Get the friendship
    friendship = friendship_map.get(planet1, {}).get(planet2, 'Unknown')

    # Define the scores for each friendship type
    friendship_scores = {
        'Friend': 10,
        'Neutral': 5,
        'Enemy': 0,
        'Unknown': 0
    }

    # Get the score
    score = friendship_scores.get(friendship, 0)

    # Define the planet qualities
    planet_qualities = {
        const.SUN: 'leadership, authority, and vitality',
        const.MOON: 'emotions, nurturing, and adaptability',
        const.MARS: 'energy, courage, and assertiveness',
        const.MERCURY: 'communication, intellect, and adaptability',
        const.JUPITER: 'wisdom, expansion, and optimism',
        const.VENUS: 'love, harmony, and pleasure',
        const.SATURN: 'discipline, responsibility, and endurance',
        const.RAHU: 'ambition, obsession, and worldly desires',
        const.KETU: 'spirituality, detachment, and liberation'
    }

    # Get the qualities
    quality1 = planet_qualities.get(planet1, 'unknown qualities')
    quality2 = planet_qualities.get(planet2, 'unknown qualities')

    return {
        'friendship': friendship,
        'score': score,
        'quality1': quality1,
        'quality2': quality2
    }


def generate_dasha_compatibility_description(dasha_lord1, dasha_lord2, compatibility):
    """
    Generate a description for Dasha compatibility

    Args:
        dasha_lord1 (str): The Dasha lord of the first person
        dasha_lord2 (str): The Dasha lord of the second person
        compatibility (dict): The compatibility information

    Returns:
        str: The Dasha compatibility description
    """
    friendship = compatibility['friendship']
    score = compatibility['score']
    quality1 = compatibility['quality1']
    quality2 = compatibility['quality2']

    if friendship == 'Friend':
        return f"The Dasha lords ({dasha_lord1} and {dasha_lord2}) are friends, indicating excellent compatibility during this period. Person 1 is currently in a phase of {quality1}, while Person 2 is in a phase of {quality2}, which creates a harmonious and supportive relationship."
    elif friendship == 'Neutral':
        return f"The Dasha lords ({dasha_lord1} and {dasha_lord2}) are neutral to each other, indicating moderate compatibility during this period. Person 1 is currently in a phase of {quality1}, while Person 2 is in a phase of {quality2}, which creates a balanced but sometimes indifferent relationship."
    elif friendship == 'Enemy':
        return f"The Dasha lords ({dasha_lord1} and {dasha_lord2}) are enemies, indicating challenging compatibility during this period. Person 1 is currently in a phase of {quality1}, while Person 2 is in a phase of {quality2}, which may create conflicts and misunderstandings."
    else:
        return f"The relationship between the Dasha lords ({dasha_lord1} and {dasha_lord2}) is unknown. Person 1 is currently in a phase of {quality1}, while Person 2 is in a phase of {quality2}."


def generate_antardasha_compatibility_description(antardasha_lord1, antardasha_lord2, compatibility):
    """
    Generate a description for Antardasha compatibility

    Args:
        antardasha_lord1 (str): The Antardasha lord of the first person
        antardasha_lord2 (str): The Antardasha lord of the second person
        compatibility (dict): The compatibility information

    Returns:
        str: The Antardasha compatibility description
    """
    friendship = compatibility['friendship']
    score = compatibility['score']
    quality1 = compatibility['quality1']
    quality2 = compatibility['quality2']

    if friendship == 'Friend':
        return f"The Antardasha lords ({antardasha_lord1} and {antardasha_lord2}) are friends, indicating excellent compatibility during this sub-period. Person 1 is currently experiencing {quality1}, while Person 2 is experiencing {quality2}, which creates a harmonious and supportive interaction."
    elif friendship == 'Neutral':
        return f"The Antardasha lords ({antardasha_lord1} and {antardasha_lord2}) are neutral to each other, indicating moderate compatibility during this sub-period. Person 1 is currently experiencing {quality1}, while Person 2 is experiencing {quality2}, which creates a balanced but sometimes indifferent interaction."
    elif friendship == 'Enemy':
        return f"The Antardasha lords ({antardasha_lord1} and {antardasha_lord2}) are enemies, indicating challenging compatibility during this sub-period. Person 1 is currently experiencing {quality1}, while Person 2 is experiencing {quality2}, which may create conflicts and misunderstandings."
    else:
        return f"The relationship between the Antardasha lords ({antardasha_lord1} and {antardasha_lord2}) is unknown. Person 1 is currently experiencing {quality1}, while Person 2 is experiencing {quality2}."


def generate_dasha_periods_compatibility_description(
    dasha_lord1, dasha_lord2, antardasha_lord1, antardasha_lord2,
    dasha_compatibility, antardasha_compatibility,
    dasha1_antardasha2_compatibility, dasha2_antardasha1_compatibility,
    overall_score
):
    """
    Generate a description for Dasha periods compatibility

    Args:
        dasha_lord1 (str): The Dasha lord of the first person
        dasha_lord2 (str): The Dasha lord of the second person
        antardasha_lord1 (str): The Antardasha lord of the first person
        antardasha_lord2 (str): The Antardasha lord of the second person
        dasha_compatibility (dict): The Dasha compatibility information
        antardasha_compatibility (dict): The Antardasha compatibility information
        dasha1_antardasha2_compatibility (dict): The compatibility between Dasha lord 1 and Antardasha lord 2
        dasha2_antardasha1_compatibility (dict): The compatibility between Dasha lord 2 and Antardasha lord 1
        overall_score (float): The overall compatibility score

    Returns:
        str: The Dasha periods compatibility description
    """
    description = f"Person 1 is currently in {dasha_lord1} Dasha and {antardasha_lord1} Antardasha, while Person 2 is in {dasha_lord2} Dasha and {antardasha_lord2} Antardasha. "

    # Add Dasha compatibility
    description += f"The Dasha lords ({dasha_lord1} and {dasha_lord2}) are {dasha_compatibility['friendship'].lower()} to each other. "

    # Add Antardasha compatibility
    description += f"The Antardasha lords ({antardasha_lord1} and {antardasha_lord2}) are {antardasha_compatibility['friendship'].lower()} to each other. "

    # Add cross-compatibility
    description += f"The Dasha lord of Person 1 ({dasha_lord1}) is {dasha1_antardasha2_compatibility['friendship'].lower()} to the Antardasha lord of Person 2 ({antardasha_lord2}). "
    description += f"The Dasha lord of Person 2 ({dasha_lord2}) is {dasha2_antardasha1_compatibility['friendship'].lower()} to the Antardasha lord of Person 1 ({antardasha_lord1}). "

    # Add overall assessment
    if overall_score >= 8:
        description += "Overall, this is an excellent period for the relationship, with strong compatibility and mutual understanding."
    elif overall_score >= 6:
        description += "Overall, this is a good period for the relationship, with positive compatibility and mutual support."
    elif overall_score >= 4:
        description += "Overall, this is a moderate period for the relationship, with mixed compatibility and occasional challenges."
    elif overall_score >= 2:
        description += "Overall, this is a challenging period for the relationship, with difficult compatibility and potential conflicts."
    else:
        description += "Overall, this is a very challenging period for the relationship, with poor compatibility and significant obstacles."

    return description
