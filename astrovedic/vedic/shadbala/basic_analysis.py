"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements basic analysis tools for Shadbala
    in Vedic astrology. For detailed analysis and reporting,
    use the astroved_extension package.
"""

from astrovedic import const


def get_basic_shadbala_analysis(shadbala_data):
    """
    Get basic analysis of Shadbala data.
    For detailed analysis, use the astroved_extension package.
    
    Args:
        shadbala_data (dict): Dictionary with Shadbala data
    
    Returns:
        dict: Dictionary with basic Shadbala analysis
    """
    # Initialize the result
    result = {
        'planet_strengths': {},
        'strongest_planet': shadbala_data['strongest']['planet'],
        'weakest_planet': shadbala_data['weakest']['planet']
    }
    
    # Calculate the strength of each planet
    for planet_id, planet_data in shadbala_data.items():
        if planet_id not in ['summary', 'strongest', 'weakest']:
            # Get the total strength
            total_rupas = planet_data['total_shadbala']['total_rupas']
            minimum_required = planet_data['minimum_required']
            
            # Calculate the strength ratio
            strength_ratio = total_rupas / minimum_required
            
            # Determine the strength category
            if strength_ratio >= 1.5:
                strength_category = 'Very Strong'
            elif strength_ratio >= 1.0:
                strength_category = 'Strong'
            elif strength_ratio >= 0.75:
                strength_category = 'Moderate'
            else:
                strength_category = 'Weak'
            
            # Add to the result
            result['planet_strengths'][planet_id] = {
                'total_rupas': total_rupas,
                'minimum_required': minimum_required,
                'strength_ratio': strength_ratio,
                'strength_category': strength_category,
                'is_sufficient': planet_data['is_sufficient']
            }
    
    return result
