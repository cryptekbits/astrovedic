#!/usr/bin/env python3
"""
    Test for Moolatrikona dignity in Vedic astrology
"""

import sys
import os
import json
from datetime import datetime

# Add the parent directory to the path so we can import astrovedic
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic import const
from astrovedic.vedic import dignities as vedic_dignities

# Test data
DATE = Datetime('2025/04/09', '20:51', '+05:30')
POS = GeoPos('12n58', '77e35')  # Bangalore

def test_moolatrikona():
    """Test Moolatrikona dignity"""

    # Create a chart
    chart = Chart(DATE, POS, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)

    # Print chart information
    print(f"Testing Moolatrikona dignity for chart: {DATE}, {POS}")

    # Verify that all planets have Moolatrikona data
    print("\nMoolatrikona data for each planet:")
    for planet_id in const.LIST_SEVEN_PLANETS:
        moolatrikona = vedic_dignities.get_moolatrikona(planet_id)
        if moolatrikona:
            print(f"{planet_id}: {moolatrikona[0]} {moolatrikona[1]}°-{moolatrikona[2]}°")
            # Verify that the Moolatrikona sign is one of the signs ruled by the planet
            # Note: The Moon is a special case - its Moolatrikona is in Taurus (4-30°) according to some sources,
            # while others say it's in Cancer. We'll allow both for now.
            if planet_id == const.MOON:
                print(f"  Note: The Moon's Moolatrikona is in Taurus, not in its ruled sign Cancer.")
                print(f"  This is a known variation in Vedic astrology texts.")
            else:
                assert moolatrikona[0] in vedic_dignities.get_ruled_signs(planet_id), f"{planet_id}'s Moolatrikona sign should be one of its ruled signs"
        else:
            print(f"{planet_id}: No Moolatrikona")

    # Test is_in_moolatrikona function
    print("\nTesting is_in_moolatrikona function:")

    # Test cases for each planet
    test_cases = [
        # Planet, Sign, Degree, Expected Result
        (const.SUN, const.LEO, 10, True),       # Sun in Leo 10° (within 0-20°)
        (const.SUN, const.LEO, 25, False),      # Sun in Leo 25° (outside 0-20°)
        (const.MOON, const.TAURUS, 15, True),   # Moon in Taurus 15° (within 4-30°)
        (const.MOON, const.TAURUS, 3, False),   # Moon in Taurus 3° (outside 4-30°)
        (const.MERCURY, const.VIRGO, 18, True), # Mercury in Virgo 18° (within 16-20°)
        (const.MERCURY, const.VIRGO, 15, False),# Mercury in Virgo 15° (outside 16-20°)
        (const.VENUS, const.LIBRA, 10, True),   # Venus in Libra 10° (within 0-15°)
        (const.VENUS, const.LIBRA, 20, False),  # Venus in Libra 20° (outside 0-15°)
        (const.MARS, const.ARIES, 5, True),     # Mars in Aries 5° (within 0-12°)
        (const.MARS, const.ARIES, 15, False),   # Mars in Aries 15° (outside 0-12°)
        (const.JUPITER, const.SAGITTARIUS, 5, True),  # Jupiter in Sagittarius 5° (within 0-10°)
        (const.JUPITER, const.SAGITTARIUS, 15, False),# Jupiter in Sagittarius 15° (outside 0-10°)
        (const.SATURN, const.AQUARIUS, 10, True),     # Saturn in Aquarius 10° (within 0-20°)
        (const.SATURN, const.AQUARIUS, 25, False),    # Saturn in Aquarius 25° (outside 0-20°)
        (const.RAHU, const.TAURUS, 10, False),  # Rahu has no Moolatrikona
        (const.KETU, const.SCORPIO, 10, False)  # Ketu has no Moolatrikona
    ]

    for planet_id, sign, degree, expected in test_cases:
        result = vedic_dignities.is_in_moolatrikona(planet_id, sign, degree)
        print(f"{planet_id} in {sign} {degree}°: {result} (Expected: {expected})")
        assert result == expected, f"is_in_moolatrikona failed for {planet_id} in {sign} {degree}°"

    # Test get_dignity_score function
    print("\nTesting get_dignity_score function:")

    # Test cases for different dignities
    dignity_test_cases = [
        # Planet, Sign, Degree, Expected Dignity
        (const.SUN, const.ARIES, 10, "Exact Exaltation"),
        (const.SUN, const.LEO, 10, "Moolatrikona"),
        (const.SUN, const.LEO, 25, "Own Sign"),
        (const.MOON, const.TAURUS, 3, "Exact Exaltation"),
        (const.MOON, const.TAURUS, 15, "Exaltation"),  # Moon is exalted in Taurus, which takes precedence over Moolatrikona
        (const.MERCURY, const.VIRGO, 15, "Exact Exaltation"),
        (const.MERCURY, const.VIRGO, 18, "Exaltation"),  # Mercury is exalted in Virgo, which takes precedence over Moolatrikona
        (const.VENUS, const.LIBRA, 10, "Moolatrikona"),
        (const.VENUS, const.LIBRA, 20, "Own Sign"),
        (const.MARS, const.ARIES, 5, "Moolatrikona"),
        (const.MARS, const.ARIES, 15, "Own Sign"),
        (const.JUPITER, const.SAGITTARIUS, 5, "Moolatrikona"),
        (const.JUPITER, const.SAGITTARIUS, 15, "Own Sign"),
        (const.SATURN, const.AQUARIUS, 10, "Moolatrikona"),
        (const.SATURN, const.AQUARIUS, 25, "Own Sign")
    ]

    for planet_id, sign, degree, expected_dignity in dignity_test_cases:
        dignity_name = vedic_dignities.get_dignity_name(planet_id, sign, degree)
        print(f"{planet_id} in {sign} {degree}°: {dignity_name} (Expected: {expected_dignity})")
        assert dignity_name == expected_dignity, f"get_dignity_name failed for {planet_id} in {sign} {degree}°"

    print("\nAll tests passed!")

if __name__ == "__main__":
    test_moolatrikona()
