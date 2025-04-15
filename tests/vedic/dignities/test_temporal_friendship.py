#!/usr/bin/env python3
"""
    Test for Temporal and Combined Friendship in Vedic astrology
"""

import sys
import os
import json
from datetime import datetime

# Add the parent directory to the path so we can import astrovedic
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from astrovedic import const
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic.vedic import dignities as vedic_dignities

# Test data
DATE = Datetime('2025/04/09', '20:51', '+05:30')
POS = GeoPos('12n58', '77e35')  # Bangalore

def test_temporal_friendship():
    """Test Temporal Friendship calculation"""
    
    # Create a chart
    chart = Chart(DATE, POS, hsys=const.HOUSES_PLACIDUS, mode=const.AY_KRISHNAMURTI)
    
    # Print chart information
    print(f"Testing Temporal Friendship for chart: {DATE}, {POS}")
    
    # Calculate Temporal Friendship for each pair of planets
    print("\nTemporal Friendship:")
    for planet1_id in const.LIST_SEVEN_PLANETS:
        for planet2_id in const.LIST_SEVEN_PLANETS:
            if planet1_id == planet2_id:
                continue  # Skip self
                
            try:
                # Calculate Temporal Friendship
                temporal = vedic_dignities.calculate_temporal_friendship(chart, planet1_id, planet2_id)
                
                # Convert to string representation
                if temporal == vedic_dignities.FRIENDSHIP_LEVELS['GREAT_FRIEND']:
                    temporal_str = "Great Friend"
                elif temporal == vedic_dignities.FRIENDSHIP_LEVELS['FRIEND']:
                    temporal_str = "Friend"
                elif temporal == vedic_dignities.FRIENDSHIP_LEVELS['NEUTRAL']:
                    temporal_str = "Neutral"
                elif temporal == vedic_dignities.FRIENDSHIP_LEVELS['ENEMY']:
                    temporal_str = "Enemy"
                else:
                    temporal_str = "Great Enemy"
                
                print(f"{planet1_id} -> {planet2_id}: {temporal_str} ({temporal})")
            except Exception as e:
                print(f"{planet1_id} -> {planet2_id}: Error - {str(e)}")
    
    # Calculate Combined Friendship for each pair of planets
    print("\nCombined Friendship:")
    for planet1_id in const.LIST_SEVEN_PLANETS:
        for planet2_id in const.LIST_SEVEN_PLANETS:
            if planet1_id == planet2_id:
                continue  # Skip self
                
            try:
                # Calculate Combined Friendship
                combined = vedic_dignities.calculate_combined_friendship(chart, planet1_id, planet2_id)
                
                # Get Natural Friendship for comparison
                natural = vedic_dignities.get_natural_friendship(planet1_id, planet2_id)
                if natural == vedic_dignities.FRIENDSHIP_LEVELS['GREAT_FRIEND']:
                    natural_str = "Great Friend"
                elif natural == vedic_dignities.FRIENDSHIP_LEVELS['FRIEND']:
                    natural_str = "Friend"
                elif natural == vedic_dignities.FRIENDSHIP_LEVELS['NEUTRAL']:
                    natural_str = "Neutral"
                elif natural == vedic_dignities.FRIENDSHIP_LEVELS['ENEMY']:
                    natural_str = "Enemy"
                else:
                    natural_str = "Great Enemy"
                
                print(f"{planet1_id} -> {planet2_id}: {combined} (Natural: {natural_str})")
            except Exception as e:
                print(f"{planet1_id} -> {planet2_id}: Error - {str(e)}")
    
    # Verify that the Combined Friendship calculation works correctly
    print("\nVerifying Combined Friendship calculation:")
    
    # Test case: Sun and Moon
    natural = vedic_dignities.get_natural_friendship(const.SUN, const.MOON)
    temporal = vedic_dignities.calculate_temporal_friendship(chart, const.SUN, const.MOON)
    combined = vedic_dignities.calculate_combined_friendship(chart, const.SUN, const.MOON)
    
    print(f"Sun -> Moon: Natural = {natural}, Temporal = {temporal}, Combined = {combined}")
    
    # Calculate the expected combined level
    expected_combined = (natural + temporal) // 2
    expected_combined_str = ""
    if expected_combined >= vedic_dignities.FRIENDSHIP_LEVELS['GREAT_FRIEND']:
        expected_combined_str = "GREAT_FRIEND"
    elif expected_combined >= vedic_dignities.FRIENDSHIP_LEVELS['FRIEND']:
        expected_combined_str = "FRIEND"
    elif expected_combined >= vedic_dignities.FRIENDSHIP_LEVELS['NEUTRAL']:
        expected_combined_str = "NEUTRAL"
    elif expected_combined >= vedic_dignities.FRIENDSHIP_LEVELS['ENEMY']:
        expected_combined_str = "ENEMY"
    else:
        expected_combined_str = "GREAT_ENEMY"
    
    print(f"Expected combined level: {expected_combined_str}")
    assert combined == expected_combined_str, f"Combined friendship should be {expected_combined_str}, not {combined}"
    
    print("\nAll tests passed!")

if __name__ == "__main__":
    test_temporal_friendship()
