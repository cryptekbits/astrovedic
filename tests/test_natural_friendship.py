#!/usr/bin/env python3
"""
    Test for Natural Friendship in Vedic astrology
"""

import sys
import os
import json
from datetime import datetime

# Add the parent directory to the path so we can import astrovedic
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from astrovedic import const
from astrovedic.vedic import dignities as vedic_dignities
from astrovedic.vedic.vargas import analysis as vargas_analysis

def test_natural_friendship():
    """Test Natural Friendship data and functions"""
    
    # Print the Natural Friendship data from NATURAL_FRIENDSHIPS
    print("Natural Friendship data from NATURAL_FRIENDSHIPS:")
    for planet1_id in const.LIST_SEVEN_PLANETS:
        friends = []
        neutrals = []
        enemies = []
        
        for planet2_id in const.LIST_SEVEN_PLANETS:
            if planet1_id == planet2_id:
                continue  # Skip self
                
            friendship = vedic_dignities.get_natural_friendship(planet1_id, planet2_id)
            
            if friendship == vedic_dignities.FRIENDSHIP_LEVELS['FRIEND'] or friendship == vedic_dignities.FRIENDSHIP_LEVELS['GREAT_FRIEND']:
                friends.append(planet2_id)
            elif friendship == vedic_dignities.FRIENDSHIP_LEVELS['NEUTRAL']:
                neutrals.append(planet2_id)
            else:  # ENEMY or GREAT_ENEMY
                enemies.append(planet2_id)
        
        print(f"{planet1_id}:")
        print(f"  Friends: {', '.join(friends)}")
        print(f"  Neutrals: {', '.join(neutrals)}")
        print(f"  Enemies: {', '.join(enemies)}")
    
    # Print the Natural Friendship data from get_friendly_signs and get_enemy_signs
    print("\nNatural Friendship data from get_friendly_signs and get_enemy_signs:")
    for planet_id in const.LIST_SEVEN_PLANETS:
        friendly_planets = vargas_analysis.get_friendly_signs(planet_id)
        enemy_planets = vargas_analysis.get_enemy_signs(planet_id)
        
        print(f"{planet_id}:")
        print(f"  Friendly signs: {', '.join(friendly_planets)}")
        print(f"  Enemy signs: {', '.join(enemy_planets)}")
    
    # Verify that the Moon's enemies are correct
    print("\nVerifying Moon's enemies:")
    moon_enemies_from_dignities = [planet_id for planet_id in const.LIST_SEVEN_PLANETS 
                                  if planet_id != const.MOON and 
                                  vedic_dignities.get_natural_friendship(const.MOON, planet_id) <= vedic_dignities.FRIENDSHIP_LEVELS['ENEMY']]
    
    moon_enemies_from_analysis = [planet_id for planet_id in const.LIST_SEVEN_PLANETS
                                 if any(sign in vargas_analysis.get_enemy_signs(const.MOON) 
                                       for sign in vedic_dignities.get_ruled_signs(planet_id))]
    
    print(f"  Moon's enemies from dignities: {', '.join(moon_enemies_from_dignities)}")
    print(f"  Moon's enemies from analysis: {', '.join(moon_enemies_from_analysis)}")
    
    # Verify that the Moon's enemies include Saturn
    assert const.SATURN in moon_enemies_from_dignities, "Saturn should be an enemy of the Moon according to dignities"
    
    # Verify that the Moon's enemies from analysis include Saturn
    assert const.SATURN in moon_enemies_from_analysis, "Saturn should be an enemy of the Moon according to analysis"
    
    print("\nAll tests passed!")

if __name__ == "__main__":
    test_natural_friendship()
