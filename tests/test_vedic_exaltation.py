#!/usr/bin/env python3
"""
    Test for Vedic exaltation and fall degrees
"""

import sys
import os
import json
from datetime import datetime

# Add the parent directory to the path so we can import flatlib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flatlib import const
from flatlib.vedic import dignities as vedic_dignities
from flatlib.dignities import tables as western_tables

def test_vedic_exaltation_degrees():
    """Test Vedic exaltation and fall degrees"""
    
    # Print the Vedic exaltation degrees
    print("Vedic Exaltation Degrees:")
    for planet_id in const.LIST_SEVEN_PLANETS + [const.RAHU, const.KETU]:
        exaltation = vedic_dignities.get_exaltation(planet_id)
        if exaltation:
            print(f"{planet_id}: {exaltation[0]} {exaltation[1]}°")
        else:
            print(f"{planet_id}: No exaltation")
    
    # Print the Vedic debilitation degrees
    print("\nVedic Debilitation Degrees:")
    for planet_id in const.LIST_SEVEN_PLANETS + [const.RAHU, const.KETU]:
        debilitation = vedic_dignities.get_debilitation(planet_id)
        if debilitation:
            print(f"{planet_id}: {debilitation[0]} {debilitation[1]}°")
        else:
            print(f"{planet_id}: No debilitation")
    
    # Print the Western exaltation degrees from ESSENTIAL_DIGNITIES
    print("\nWestern Exaltation Degrees (from ESSENTIAL_DIGNITIES):")
    for sign, data in western_tables.ESSENTIAL_DIGNITIES.items():
        if data['exalt'][0]:  # If there's an exalted planet
            print(f"{data['exalt'][0]}: {sign} {data['exalt'][1]}°")
    
    # Print the Western fall degrees from ESSENTIAL_DIGNITIES
    print("\nWestern Fall Degrees (from ESSENTIAL_DIGNITIES):")
    for sign, data in western_tables.ESSENTIAL_DIGNITIES.items():
        if data['fall'][0]:  # If there's a fallen planet
            print(f"{data['fall'][0]}: {sign} {data['fall'][1]}°")
    
    # Verify that the Vedic exaltation degrees match the standard values
    standard_exaltation = {
        const.SUN: (const.ARIES, 10),
        const.MOON: (const.TAURUS, 3),
        const.MERCURY: (const.VIRGO, 15),
        const.VENUS: (const.PISCES, 27),
        const.MARS: (const.CAPRICORN, 28),
        const.JUPITER: (const.CANCER, 5),
        const.SATURN: (const.LIBRA, 20)
    }
    
    print("\nVerifying Vedic exaltation degrees:")
    for planet_id, (sign, degree) in standard_exaltation.items():
        vedic_exalt = vedic_dignities.get_exaltation(planet_id)
        if vedic_exalt:
            vedic_sign, vedic_degree = vedic_exalt
            print(f"{planet_id}: Standard: {sign} {degree}°, Vedic: {vedic_sign} {vedic_degree}°")
            assert vedic_sign == sign, f"Exaltation sign for {planet_id} should be {sign}, not {vedic_sign}"
            assert vedic_degree == degree, f"Exaltation degree for {planet_id} should be {degree}, not {vedic_degree}"
        else:
            print(f"{planet_id}: No exaltation in Vedic dignities")
            assert False, f"{planet_id} should have an exaltation"
    
    print("\nAll tests passed!")

if __name__ == "__main__":
    test_vedic_exaltation_degrees()
