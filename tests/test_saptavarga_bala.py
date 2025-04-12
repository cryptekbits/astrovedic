#!/usr/bin/env python3
"""
    Test for Saptavarga Bala calculation in Shadbala
"""

import sys
import os
import json
from datetime import datetime

# Add the parent directory to the path so we can import flatlib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib.vedic.shadbala import sthana_bala
from flatlib.vedic import dignities as vedic_dignities

# Test data
DATE = Datetime('2025/04/09', '20:51', '+05:30')
POS = GeoPos('12n58', '77e35')  # Bangalore

def test_saptavarga_bala():
    """Test Saptavarga Bala calculation"""

    # Create a chart
    chart = Chart(DATE, POS, hsys=const.HOUSES_PLACIDUS, mode=const.AY_KRISHNAMURTI)

    # Print chart information
    print(f"Testing Saptavarga Bala for chart: {DATE}, {POS}")

    # Calculate Saptavarga Bala for each planet
    print("\nSaptavarga Bala:")
    for planet_id in const.LIST_SEVEN_PLANETS:
        try:
            # Calculate Saptavarga Bala
            saptavarga_bala_info = sthana_bala.calculate_saptavarga_bala(chart, planet_id)

            # Print the results
            print(f"\n{planet_id}:")
            print(f"  Total Virupa: {saptavarga_bala_info['total_virupa']}")
            print(f"  Value: {saptavarga_bala_info['value']}")
            print(f"  Description: {saptavarga_bala_info['description']}")

            # Print the details for each varga
            print("  Varga details:")
            for varga_type, varga_info in saptavarga_bala_info['varga_details'].items():
                print(f"    {varga_type}: {varga_info['sign']} {varga_info['degree']:.2f}° - {varga_info['dignity']} ({varga_info['virupa_points']:.2f} Virupas, weighted: {varga_info['weighted_virupa']:.2f})")

            # Verify that the function is using Natural Friendship, not Combined Friendship
            print("  Checking friendship calculation:")
            for varga_type, varga_info in saptavarga_bala_info['varga_details'].items():
                if varga_info['dignity'] in ['Great Friend', 'Friend', 'Neutral', 'Enemy', 'Great Enemy']:
                    sign = varga_info['sign']
                    sign_lord = vedic_dignities.get_ruler(sign)

                    # Get Natural Friendship
                    natural = vedic_dignities.get_natural_friendship(planet_id, sign_lord)
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

                    # Calculate Combined Friendship
                    combined = vedic_dignities.calculate_combined_friendship(chart, planet_id, sign_lord)

                    print(f"    {varga_type}: {planet_id} -> {sign_lord} (lord of {sign}): Natural: {natural_str}, Combined: {combined}, Used: {varga_info['dignity']}")

                    # Verify that the dignity matches the Combined Friendship
                    expected_dignity = combined
                    if expected_dignity == 'GREAT_FRIEND':
                        expected_dignity = 'Great Friend'
                    elif expected_dignity == 'FRIEND':
                        expected_dignity = 'Friend'
                    elif expected_dignity == 'NEUTRAL':
                        expected_dignity = 'Neutral'
                    elif expected_dignity == 'ENEMY':
                        expected_dignity = 'Enemy'
                    else:  # GREAT_ENEMY
                        expected_dignity = 'Great Enemy'

                    assert varga_info['dignity'] == expected_dignity, f"Dignity should be {expected_dignity}, not {varga_info['dignity']}"
        except Exception as e:
            print(f"{planet_id}: Error - {str(e)}")

    print("\nAll tests passed!")

if __name__ == "__main__":
    test_saptavarga_bala()
