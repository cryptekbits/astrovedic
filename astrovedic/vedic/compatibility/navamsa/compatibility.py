"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Navamsa compatibility analysis
    for Vedic astrology.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic import angle

from astrovedic.vedic.compatibility.navamsa.positions import (
    get_navamsa_positions, get_navamsa_house_positions,
    get_navamsa_sign_lords, get_navamsa_exaltation_debilitation
)


def get_navamsa_compatibility(chart1, chart2):
    """
    Get the Navamsa compatibility between two charts
    
    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart
    
    Returns:
        dict: Dictionary with Navamsa compatibility information
    """
    # Get the Navamsa positions
    positions1 = get_navamsa_positions(chart1)
    positions2 = get_navamsa_positions(chart2)
    
    # Get the Navamsa house positions
    house_positions1 = get_navamsa_house_positions(chart1)
    house_positions2 = get_navamsa_house_positions(chart2)
    
    # Get the Navamsa aspects
    aspects = get_navamsa_aspects(chart1, chart2)
    
    # Get the Navamsa strength
    strength1 = get_navamsa_strength(chart1)
    strength2 = get_navamsa_strength(chart2)
    
    # Calculate the compatibility score
    score = calculate_navamsa_compatibility_score(
        positions1, positions2, house_positions1, house_positions2,
        aspects, strength1, strength2
    )
    
    # Generate the description
    description = generate_navamsa_compatibility_description(
        positions1, positions2, house_positions1, house_positions2,
        aspects, strength1, strength2, score
    )
    
    return {
        'positions1': positions1,
        'positions2': positions2,
        'house_positions1': house_positions1,
        'house_positions2': house_positions2,
        'aspects': aspects,
        'strength1': strength1,
        'strength2': strength2,
        'score': score,
        'description': description
    }


def get_navamsa_aspects(chart1, chart2):
    """
    Get the Navamsa aspects between two charts
    
    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart
    
    Returns:
        list: List of Navamsa aspects
    """
    # Get the Navamsa positions
    positions1 = get_navamsa_positions(chart1)
    positions2 = get_navamsa_positions(chart2)
    
    # Initialize the aspects
    aspects = []
    
    # Define the aspect types
    aspect_types = [
        {'name': 'Conjunction', 'angle': 0, 'orb': 8},
        {'name': 'Opposition', 'angle': 180, 'orb': 8},
        {'name': 'Trine', 'angle': 120, 'orb': 8},
        {'name': 'Square', 'angle': 90, 'orb': 7},
        {'name': 'Sextile', 'angle': 60, 'orb': 6}
    ]
    
    # Check for aspects between planets
    for planet_id1, position1 in positions1.items():
        # Skip angles
        if planet_id1 in [const.ASC, const.MC, const.DESC, const.IC]:
            continue
        
        for planet_id2, position2 in positions2.items():
            # Skip angles
            if planet_id2 in [const.ASC, const.MC, const.DESC, const.IC]:
                continue
            
            # Get the longitudes
            lon1 = position1['longitude']
            lon2 = position2['longitude']
            
            # Calculate the angular distance
            dist = angle.closestdistance(lon1, lon2)
            
            # Check for aspects
            for aspect_type in aspect_types:
                # Calculate the orb
                orb = abs(abs(dist) - aspect_type['angle'])
                
                # Check if the aspect is within the allowed orb
                if orb <= aspect_type['orb']:
                    # Add the aspect
                    aspects.append({
                        'planet1': planet_id1,
                        'planet2': planet_id2,
                        'aspect': aspect_type['name'],
                        'orb': orb
                    })
    
    # Check for aspects to angles
    for planet_id1, position1 in positions1.items():
        # Skip angles
        if planet_id1 in [const.ASC, const.MC, const.DESC, const.IC]:
            continue
        
        for angle_id in [const.ASC, const.MC]:
            # Get the angle position
            position2 = positions2[angle_id]
            
            # Get the longitudes
            lon1 = position1['longitude']
            lon2 = position2['longitude']
            
            # Calculate the angular distance
            dist = angle.closestdistance(lon1, lon2)
            
            # Check for aspects
            for aspect_type in aspect_types:
                # Calculate the orb
                orb = abs(abs(dist) - aspect_type['angle'])
                
                # Check if the aspect is within the allowed orb
                if orb <= aspect_type['orb']:
                    # Add the aspect
                    aspects.append({
                        'planet1': planet_id1,
                        'planet2': angle_id,
                        'aspect': aspect_type['name'],
                        'orb': orb
                    })
    
    # Check for aspects from angles
    for angle_id in [const.ASC, const.MC]:
        # Get the angle position
        position1 = positions1[angle_id]
        
        for planet_id2, position2 in positions2.items():
            # Skip angles
            if planet_id2 in [const.ASC, const.MC, const.DESC, const.IC]:
                continue
            
            # Get the longitudes
            lon1 = position1['longitude']
            lon2 = position2['longitude']
            
            # Calculate the angular distance
            dist = angle.closestdistance(lon1, lon2)
            
            # Check for aspects
            for aspect_type in aspect_types:
                # Calculate the orb
                orb = abs(abs(dist) - aspect_type['angle'])
                
                # Check if the aspect is within the allowed orb
                if orb <= aspect_type['orb']:
                    # Add the aspect
                    aspects.append({
                        'planet1': angle_id,
                        'planet2': planet_id2,
                        'aspect': aspect_type['name'],
                        'orb': orb
                    })
    
    return aspects


def get_navamsa_strength(chart):
    """
    Get the Navamsa strength for a chart
    
    Args:
        chart (Chart): The chart
    
    Returns:
        dict: Dictionary with Navamsa strength information
    """
    # Get the Navamsa positions
    positions = get_navamsa_positions(chart)
    
    # Get the Navamsa exaltation and debilitation status
    exalt_debil = get_navamsa_exaltation_debilitation(chart)
    
    # Initialize the strength
    strength = {}
    
    # Calculate the strength for each planet
    for planet_id, position in positions.items():
        # Skip angles
        if planet_id in [const.ASC, const.MC, const.DESC, const.IC]:
            continue
        
        # Get the exaltation and debilitation status
        status = exalt_debil.get(planet_id, {'is_exalted': False, 'is_debilitated': False})
        
        # Calculate the strength
        if status['is_exalted']:
            strength_value = 10
            strength_description = 'Exalted'
        elif status['is_debilitated']:
            strength_value = 0
            strength_description = 'Debilitated'
        else:
            # Default strength
            strength_value = 5
            strength_description = 'Neutral'
        
        # Add to strength
        strength[planet_id] = {
            'value': strength_value,
            'description': strength_description
        }
    
    # Calculate the overall strength
    total_strength = sum(s['value'] for s in strength.values())
    max_strength = 10 * len(strength)
    percentage = (total_strength / max_strength) * 100 if max_strength > 0 else 0
    
    # Determine the overall strength description
    if percentage >= 80:
        overall_description = 'Excellent'
    elif percentage >= 60:
        overall_description = 'Good'
    elif percentage >= 40:
        overall_description = 'Average'
    elif percentage >= 20:
        overall_description = 'Weak'
    else:
        overall_description = 'Very Weak'
    
    # Add the overall strength
    strength['overall'] = {
        'value': percentage,
        'description': overall_description
    }
    
    return strength


def calculate_navamsa_compatibility_score(
    positions1, positions2, house_positions1, house_positions2,
    aspects, strength1, strength2
):
    """
    Calculate the Navamsa compatibility score
    
    Args:
        positions1 (dict): The Navamsa positions for the first chart
        positions2 (dict): The Navamsa positions for the second chart
        house_positions1 (dict): The Navamsa house positions for the first chart
        house_positions2 (dict): The Navamsa house positions for the second chart
        aspects (list): The Navamsa aspects
        strength1 (dict): The Navamsa strength for the first chart
        strength2 (dict): The Navamsa strength for the second chart
    
    Returns:
        float: The Navamsa compatibility score (0-10)
    """
    # Initialize the score
    score = 0
    
    # Add points for favorable aspects
    for aspect in aspects:
        if aspect['aspect'] in ['Conjunction', 'Trine', 'Sextile']:
            # Check if the aspect involves important planets
            if aspect['planet1'] in [const.SUN, const.MOON, const.ASC] or aspect['planet2'] in [const.SUN, const.MOON, const.ASC]:
                score += 1.0
            else:
                score += 0.5
        elif aspect['aspect'] in ['Opposition', 'Square']:
            # Check if the aspect involves important planets
            if aspect['planet1'] in [const.SUN, const.MOON, const.ASC] or aspect['planet2'] in [const.SUN, const.MOON, const.ASC]:
                score -= 0.5
            else:
                score -= 0.25
    
    # Add points for favorable house positions
    for planet_id, house in house_positions1.items():
        if planet_id == const.VENUS and house in [1, 5, 7, 9]:
            score += 0.5
        elif planet_id == const.JUPITER and house in [1, 2, 5, 9]:
            score += 0.5
        elif planet_id == const.MOON and house in [1, 4, 7, 10]:
            score += 0.5
    
    for planet_id, house in house_positions2.items():
        if planet_id == const.VENUS and house in [1, 5, 7, 9]:
            score += 0.5
        elif planet_id == const.JUPITER and house in [1, 2, 5, 9]:
            score += 0.5
        elif planet_id == const.MOON and house in [1, 4, 7, 10]:
            score += 0.5
    
    # Add points for strong charts
    score += strength1['overall']['value'] / 20  # Add up to 5 points
    score += strength2['overall']['value'] / 20  # Add up to 5 points
    
    # Ensure the score is between 0 and 10
    score = min(10, max(0, score))
    
    return score


def generate_navamsa_compatibility_description(
    positions1, positions2, house_positions1, house_positions2,
    aspects, strength1, strength2, score
):
    """
    Generate a description for Navamsa compatibility
    
    Args:
        positions1 (dict): The Navamsa positions for the first chart
        positions2 (dict): The Navamsa positions for the second chart
        house_positions1 (dict): The Navamsa house positions for the first chart
        house_positions2 (dict): The Navamsa house positions for the second chart
        aspects (list): The Navamsa aspects
        strength1 (dict): The Navamsa strength for the first chart
        strength2 (dict): The Navamsa strength for the second chart
        score (float): The Navamsa compatibility score
    
    Returns:
        str: The Navamsa compatibility description
    """
    # Generate the description
    description = f"Navamsa Compatibility Score: {score:.1f}/10. "
    
    # Add overall assessment
    if score >= 8:
        description += "This indicates excellent compatibility at the soul level, suggesting a deep spiritual connection and mutual growth. "
    elif score >= 6:
        description += "This indicates good compatibility at the soul level, suggesting a positive spiritual connection and potential for growth together. "
    elif score >= 4:
        description += "This indicates average compatibility at the soul level, suggesting a moderate spiritual connection with both opportunities and challenges. "
    elif score >= 2:
        description += "This indicates challenging compatibility at the soul level, suggesting a difficult spiritual connection with significant obstacles to overcome. "
    else:
        description += "This indicates poor compatibility at the soul level, suggesting a very challenging spiritual connection with major obstacles. "
    
    # Add information about important aspects
    important_aspects = []
    
    for aspect in aspects:
        if aspect['planet1'] in [const.SUN, const.MOON, const.ASC, const.VENUS] and aspect['planet2'] in [const.SUN, const.MOON, const.ASC, const.VENUS]:
            if aspect['aspect'] in ['Conjunction', 'Trine', 'Sextile']:
                important_aspects.append(f"Favorable {aspect['aspect']} between {aspect['planet1']} and {aspect['planet2']}")
            elif aspect['aspect'] in ['Opposition', 'Square']:
                important_aspects.append(f"Challenging {aspect['aspect']} between {aspect['planet1']} and {aspect['planet2']}")
    
    if important_aspects:
        description += "Key aspects in Navamsa: " + ", ".join(important_aspects[:3]) + ". "
    
    # Add information about chart strength
    description += f"Person 1's Navamsa chart is {strength1['overall']['description'].lower()} ({strength1['overall']['value']:.0f}%), while Person 2's Navamsa chart is {strength2['overall']['description'].lower()} ({strength2['overall']['value']:.0f}%). "
    
    # Add information about Venus and Moon
    venus1_house = house_positions1.get(const.VENUS, 0)
    venus2_house = house_positions2.get(const.VENUS, 0)
    moon1_house = house_positions1.get(const.MOON, 0)
    moon2_house = house_positions2.get(const.MOON, 0)
    
    if venus1_house in [1, 5, 7, 9] and venus2_house in [1, 5, 7, 9]:
        description += "Both individuals have Venus well-placed in Navamsa, indicating strong romantic compatibility. "
    elif venus1_house in [1, 5, 7, 9] or venus2_house in [1, 5, 7, 9]:
        description += "One individual has Venus well-placed in Navamsa, indicating moderate romantic compatibility. "
    
    if moon1_house in [1, 4, 7, 10] and moon2_house in [1, 4, 7, 10]:
        description += "Both individuals have Moon well-placed in Navamsa, indicating strong emotional compatibility. "
    elif moon1_house in [1, 4, 7, 10] or moon2_house in [1, 4, 7, 10]:
        description += "One individual has Moon well-placed in Navamsa, indicating moderate emotional compatibility. "
    
    return description
