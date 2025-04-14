"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Yoni Kuta (animal nature compatibility)
    for Vedic astrology.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.vedic.nakshatras import get_nakshatra


def get_yoni_kuta(chart1, chart2):
    """
    Calculate the Yoni Kuta (animal nature compatibility)

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with Yoni Kuta information
    """
    # Get the Moon positions
    moon1 = chart1.getObject(const.MOON)
    moon2 = chart2.getObject(const.MOON)

    # Get the Nakshatras for each Moon
    nakshatra1 = get_nakshatra(moon1.lon)
    nakshatra2 = get_nakshatra(moon2.lon)

    # Get the Yoni (animal symbol) for each Nakshatra
    yoni1 = get_yoni(nakshatra1['name'])
    yoni2 = get_yoni(nakshatra2['name'])

    # Calculate the score
    score = calculate_yoni_score(yoni1, yoni2)

    return {
        'yoni1': yoni1,
        'yoni2': yoni2,
        'score': score,
        'max_score': 4
    }


def get_yoni(nakshatra):
    """
    Get the Yoni (animal symbol) for a Nakshatra

    Args:
        nakshatra (str): The Nakshatra name

    Returns:
        str: The Yoni (animal symbol)
    """
    # Define the Yoni for each Nakshatra
    yoni_map = {
        'Ashwini': 'Horse',
        'Bharani': 'Elephant',
        'Krittika': 'Sheep',
        'Rohini': 'Serpent',
        'Mrigashira': 'Serpent',
        'Ardra': 'Dog',
        'Punarvasu': 'Cat',
        'Pushya': 'Sheep',
        'Ashlesha': 'Cat',
        'Magha': 'Rat',
        'Purva Phalguni': 'Rat',
        'Uttara Phalguni': 'Cow',
        'Hasta': 'Buffalo',
        'Chitra': 'Tiger',
        'Swati': 'Buffalo',
        'Vishakha': 'Tiger',
        'Anuradha': 'Deer',
        'Jyeshtha': 'Deer',
        'Mula': 'Dog',
        'Purva Ashadha': 'Monkey',
        'Uttara Ashadha': 'Mongoose',
        'Shravana': 'Monkey',
        'Dhanishta': 'Lion',
        'Shatabhisha': 'Horse',
        'Purva Bhadrapada': 'Lion',
        'Uttara Bhadrapada': 'Cow',
        'Revati': 'Elephant'
    }

    return yoni_map.get(nakshatra, 'Unknown')


def calculate_yoni_score(yoni1, yoni2):
    """
    Calculate the Yoni Kuta score

    Args:
        yoni1 (str): The Yoni of the first person
        yoni2 (str): The Yoni of the second person

    Returns:
        int: The Yoni Kuta score (0-4)
    """
    # Define the Yoni compatibility matrix
    yoni_compatibility = {
        'Horse': {
            'Horse': 4, 'Elephant': 2, 'Sheep': 3, 'Serpent': 0,
            'Dog': 3, 'Cat': 2, 'Rat': 1, 'Cow': 2,
            'Buffalo': 1, 'Tiger': 0, 'Deer': 3, 'Monkey': 2,
            'Mongoose': 1, 'Lion': 0
        },
        'Elephant': {
            'Horse': 2, 'Elephant': 4, 'Sheep': 2, 'Serpent': 1,
            'Dog': 2, 'Cat': 1, 'Rat': 0, 'Cow': 3,
            'Buffalo': 2, 'Tiger': 1, 'Deer': 2, 'Monkey': 1,
            'Mongoose': 0, 'Lion': 1
        },
        'Sheep': {
            'Horse': 3, 'Elephant': 2, 'Sheep': 4, 'Serpent': 1,
            'Dog': 2, 'Cat': 3, 'Rat': 2, 'Cow': 3,
            'Buffalo': 2, 'Tiger': 1, 'Deer': 3, 'Monkey': 2,
            'Mongoose': 1, 'Lion': 0
        },
        'Serpent': {
            'Horse': 0, 'Elephant': 1, 'Sheep': 1, 'Serpent': 4,
            'Dog': 1, 'Cat': 2, 'Rat': 3, 'Cow': 1,
            'Buffalo': 0, 'Tiger': 2, 'Deer': 1, 'Monkey': 2,
            'Mongoose': 0, 'Lion': 3
        },
        'Dog': {
            'Horse': 3, 'Elephant': 2, 'Sheep': 2, 'Serpent': 1,
            'Dog': 4, 'Cat': 0, 'Rat': 1, 'Cow': 2,
            'Buffalo': 3, 'Tiger': 0, 'Deer': 2, 'Monkey': 1,
            'Mongoose': 2, 'Lion': 1
        },
        'Cat': {
            'Horse': 2, 'Elephant': 1, 'Sheep': 3, 'Serpent': 2,
            'Dog': 0, 'Cat': 4, 'Rat': 0, 'Cow': 3,
            'Buffalo': 2, 'Tiger': 1, 'Deer': 3, 'Monkey': 2,
            'Mongoose': 1, 'Lion': 0
        },
        'Rat': {
            'Horse': 1, 'Elephant': 0, 'Sheep': 2, 'Serpent': 3,
            'Dog': 1, 'Cat': 0, 'Rat': 4, 'Cow': 1,
            'Buffalo': 0, 'Tiger': 2, 'Deer': 1, 'Monkey': 2,
            'Mongoose': 3, 'Lion': 0
        },
        'Cow': {
            'Horse': 2, 'Elephant': 3, 'Sheep': 3, 'Serpent': 1,
            'Dog': 2, 'Cat': 3, 'Rat': 1, 'Cow': 4,
            'Buffalo': 3, 'Tiger': 0, 'Deer': 3, 'Monkey': 2,
            'Mongoose': 1, 'Lion': 0
        },
        'Buffalo': {
            'Horse': 1, 'Elephant': 2, 'Sheep': 2, 'Serpent': 0,
            'Dog': 3, 'Cat': 2, 'Rat': 0, 'Cow': 3,
            'Buffalo': 4, 'Tiger': 0, 'Deer': 2, 'Monkey': 1,
            'Mongoose': 2, 'Lion': 1
        },
        'Tiger': {
            'Horse': 0, 'Elephant': 1, 'Sheep': 1, 'Serpent': 2,
            'Dog': 0, 'Cat': 1, 'Rat': 2, 'Cow': 0,
            'Buffalo': 0, 'Tiger': 4, 'Deer': 0, 'Monkey': 1,
            'Mongoose': 2, 'Lion': 3
        },
        'Deer': {
            'Horse': 3, 'Elephant': 2, 'Sheep': 3, 'Serpent': 1,
            'Dog': 2, 'Cat': 3, 'Rat': 1, 'Cow': 3,
            'Buffalo': 2, 'Tiger': 0, 'Deer': 4, 'Monkey': 2,
            'Mongoose': 1, 'Lion': 0
        },
        'Monkey': {
            'Horse': 2, 'Elephant': 1, 'Sheep': 2, 'Serpent': 2,
            'Dog': 1, 'Cat': 2, 'Rat': 2, 'Cow': 2,
            'Buffalo': 1, 'Tiger': 1, 'Deer': 2, 'Monkey': 4,
            'Mongoose': 3, 'Lion': 1
        },
        'Mongoose': {
            'Horse': 1, 'Elephant': 0, 'Sheep': 1, 'Serpent': 0,
            'Dog': 2, 'Cat': 1, 'Rat': 3, 'Cow': 1,
            'Buffalo': 2, 'Tiger': 2, 'Deer': 1, 'Monkey': 3,
            'Mongoose': 4, 'Lion': 2
        },
        'Lion': {
            'Horse': 0, 'Elephant': 1, 'Sheep': 0, 'Serpent': 3,
            'Dog': 1, 'Cat': 0, 'Rat': 0, 'Cow': 0,
            'Buffalo': 1, 'Tiger': 3, 'Deer': 0, 'Monkey': 1,
            'Mongoose': 2, 'Lion': 4
        }
    }

    # Get the compatibility score
    return yoni_compatibility.get(yoni1, {}).get(yoni2, 0)



