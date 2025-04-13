#!/usr/bin/env python3
"""
Test Transit Analysis Core Functions

This script tests the core transit analysis functions in flatlib.
"""

import unittest
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib.vedic.transits.core import (
    get_transit_chart, get_transit_planets,
    get_transit_aspects, get_transit_houses,
    get_transit_quality, get_house_number
)
from datetime import timedelta


class TestTransitCore(unittest.TestCase):
    """Test case for transit analysis core functions"""

    def setUp(self):
        """Set up test case"""
        # Create a natal chart
        natal_date = Datetime('2025/04/09', '20:51', '+05:30')
        self.location = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.natal_chart = Chart(natal_date, self.location, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)

        # Create a transit chart (1 year later)
        transit_date = Datetime('2026/04/09', '20:51', '+05:30')
        self.transit_chart = Chart(transit_date, self.location, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)

        # Store dates for timeline testing
        self.natal_date = natal_date
        self.transit_date = transit_date

    def test_get_transit_chart(self):
        """Test get_transit_chart function"""
        # Create a transit chart using the function
        transit_chart = get_transit_chart(self.natal_chart, self.transit_date)

        # Check that the transit chart has the same house system and ayanamsa as the natal chart
        self.assertEqual(transit_chart.hsys, self.natal_chart.hsys)
        self.assertEqual(transit_chart.mode, self.natal_chart.mode)

        # Check that the transit chart has the correct date
        self.assertEqual(transit_chart.date.jd, self.transit_date.jd)

        # Check that the transit chart has the correct location
        self.assertEqual(transit_chart.pos.lat, self.location.lat)
        self.assertEqual(transit_chart.pos.lon, self.location.lon)

        # Print the transit chart information for reference
        print(f"Transit Chart: {self.transit_date.date.date()}/{self.transit_date.time.time()}")
        print(f"House System: {transit_chart.hsys}")
        print(f"Ayanamsa: {transit_chart.mode}")

    def test_get_transit_planets(self):
        """Test get_transit_planets function"""
        # Get the transit planets
        transit_planets = get_transit_planets(self.natal_chart, self.transit_chart)

        # Check that the result is a dictionary
        self.assertIsInstance(transit_planets, dict)

        # Check that all planets are present
        for planet_id in const.LIST_OBJECTS_VEDIC:
            self.assertIn(planet_id, transit_planets)

        # Check that each planet has the required keys
        for planet_id, planet_info in transit_planets.items():
            self.assertIn('transit_sign', planet_info)
            self.assertIn('house', planet_info)
            self.assertIn('distance', planet_info)
            self.assertIn('is_retrograde', planet_info)

        # Print the transit planets for reference
        print(f"Transit Planets:")
        for planet_id, planet_info in transit_planets.items():
            print(f"{planet_id}: {planet_info['transit_sign']} (House {planet_info['house']})")
            print(f"  Distance from natal position: {planet_info['distance']:.2f}°")
            print(f"  Retrograde: {planet_info['is_retrograde']}")

    def test_get_transit_aspects(self):
        """Test get_transit_aspects function"""
        # Get the transit aspects
        transit_aspects = get_transit_aspects(self.natal_chart, self.transit_chart)

        # Check that the result is a list
        self.assertIsInstance(transit_aspects, list)

        # Check that each aspect has the required keys
        for aspect in transit_aspects:
            self.assertIn('transit_planet', aspect)
            self.assertIn('natal_planet', aspect)
            self.assertIn('aspect', aspect)
            self.assertIn('angle', aspect)
            self.assertIn('orb', aspect)
            self.assertIn('applying', aspect)

            # Check that the transit and natal planets are valid
            self.assertIn(aspect['transit_planet'], const.LIST_OBJECTS_VEDIC)
            self.assertIn(aspect['natal_planet'], const.LIST_OBJECTS_VEDIC)

            # Check that the aspect is valid
            self.assertIn(aspect['aspect'], ['Conjunction', 'Opposition', 'Trine', 'Square', 'Sextile'])

            # Check that the orb is within a reasonable range
            self.assertLessEqual(aspect['orb'], 10)  # Allow up to 10 degrees for testing

            # Check that the applying flag is a boolean
            self.assertIsInstance(aspect['applying'], bool)

        # Print the transit aspects for reference
        print(f"Transit Aspects:")
        for aspect in transit_aspects:
            print(f"{aspect['transit_planet']} {aspect['aspect']} natal {aspect['natal_planet']}")
            print(f"  Orb: {aspect['orb']:.2f}°")
            print(f"  {'Applying' if aspect['applying'] else 'Separating'}")

    def test_get_transit_houses(self):
        """Test get_transit_houses function"""
        # Get the transit houses
        transit_houses = get_transit_houses(self.natal_chart, self.transit_chart)

        # Check that the result is a dictionary
        self.assertIsInstance(transit_houses, dict)

        # Check that all houses are present
        for house_num in range(1, 13):
            self.assertIn(house_num, transit_houses)

        # Check that each house has the required keys
        for house_num, house_info in transit_houses.items():
            self.assertIn('sign', house_info)  # The sign key is used instead of transit_sign
            self.assertIn('planets', house_info)  # The planets key is used instead of transit_planets

            # Check that the sign is valid
            self.assertIn(house_info['sign'], const.LIST_SIGNS)

            # Check that the planets is a list
            self.assertIsInstance(house_info['planets'], list)

            # Check that each planet is valid
            for planet_id in house_info['planets']:
                self.assertIn(planet_id, const.LIST_OBJECTS_VEDIC)

        # Print the transit houses for reference
        print(f"Transit Houses:")
        for house_num, house_info in transit_houses.items():
            print(f"House {house_num}: {house_info['sign']}")
            if house_info['planets']:
                print(f"  Transit Planets: {', '.join(house_info['planets'])}")

    def test_get_transit_quality(self):
        """Test get_transit_quality function"""
        # Get the transit quality
        transit_quality = get_transit_quality(self.natal_chart, self.transit_chart)

        # Check that the result is a dictionary
        self.assertIsInstance(transit_quality, dict)

        # Check that all required keys are present
        self.assertIn('score', transit_quality)
        self.assertIn('quality', transit_quality)
        self.assertIn('factors', transit_quality)

        # Check that the score is a number
        self.assertIsInstance(transit_quality['score'], int)

        # Check that the quality is one of the expected values
        self.assertIn(transit_quality['quality'], ['Excellent', 'Good', 'Neutral', 'Challenging', 'Difficult'])

        # Check that the factors is a list
        self.assertIsInstance(transit_quality['factors'], list)

        # Print the transit quality for reference
        print(f"Transit Quality: {transit_quality['quality']} (Score: {transit_quality['score']})")
        print(f"Factors:")
        for factor in transit_quality['factors']:
            print(f"  {factor}")

    def test_get_house_number(self):
        """Test get_house_number function"""
        # Test with different longitudes
        test_longitudes = [0, 45, 90, 135, 180, 225, 270, 315]

        for longitude in test_longitudes:
            # Get the house number
            house_num = get_house_number(self.natal_chart, longitude)

            # Check that the house number is within the valid range
            self.assertGreaterEqual(house_num, 1)
            self.assertLessEqual(house_num, 12)

            # Print the house number for reference
            print(f"Longitude {longitude}° is in house {house_num}")


if __name__ == '__main__':
    unittest.main()
