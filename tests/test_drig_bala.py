#!/usr/bin/env python3
"""
    Test for Drig Bala calculations in Shadbala
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
from flatlib.vedic.shadbala import drig_bala

# Test data
DATE = Datetime('2025/04/09', '20:51', '+05:30')
POS = GeoPos('12n58', '77e35')  # Bangalore

def test_drig_bala():
    """Test Drig Bala calculations"""

    # Create a chart
    chart = Chart(DATE, POS, hsys=const.HOUSES_PLACIDUS, mode=const.AY_KRISHNAMURTI)

    # Calculate Drig Bala for each planet
    results = {}
    for planet_id in const.LIST_SEVEN_PLANETS + [const.RAHU, const.KETU]:
        drig_bala_info = drig_bala.calculate_drig_bala(chart, planet_id)

        # Store the results
        results[planet_id] = {
            'value': drig_bala_info['value'],
            'description': drig_bala_info['description'],
            'aspects_received': [
                {
                    'planet': aspect['planet'],
                    'virupa_points': aspect['virupa_points'],
                    'aspect_type': aspect['aspect_type'],
                    'is_benefic': aspect['is_benefic']
                }
                for aspect in drig_bala_info['aspects_received']['aspects']
            ],
            'aspects_cast': [
                {
                    'planet': aspect['planet'],
                    'virupa_points': aspect['virupa_points'],
                    'aspect_type': aspect['aspect_type'],
                    'is_benefic': aspect['is_benefic']
                }
                for aspect in drig_bala_info['aspects_cast']['aspects']
            ]
        }

    # Print the results
    print(json.dumps(results, indent=2))

    # Verify some expected results
    # Check that the Drig Bala values are within the expected range (0-60)
    for planet_id, planet_data in results.items():
        assert 0 <= planet_data['value'] <= 60, f"{planet_id} should have Drig Bala between 0 and 60"

    # Saturn should have positive Drig Bala in this chart
    assert results[const.SATURN]['value'] > 0, "Saturn should have positive Drig Bala in this chart"

    # Check that the Virupa points are in the correct range
    for planet_id, planet_data in results.items():
        for aspect in planet_data['aspects_received']:
            if aspect['is_benefic']:
                assert aspect['virupa_points'] > 0, f"Benefic aspect from {aspect['planet']} should have positive points"
            else:
                assert aspect['virupa_points'] < 0, f"Malefic aspect from {aspect['planet']} should have negative points"

    print("All tests passed!")

if __name__ == "__main__":
    test_drig_bala()
