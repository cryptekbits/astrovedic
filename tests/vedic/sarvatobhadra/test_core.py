#!/usr/bin/env python3
"""
Test Sarvatobhadra Chakra Calculations

This script tests the Sarvatobhadra Chakra calculations in astrovedic.
"""

import unittest
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic import const
from astrovedic.vedic.sarvatobhadra.core import (
    get_sarvatobhadra_chakra, get_chakra_quality,
    get_auspicious_directions, get_inauspicious_directions,
    is_auspicious_position, is_inauspicious_position
)


class TestSarvatobhadraCore(unittest.TestCase):
    """Test case for Sarvatobhadra Chakra core calculations"""

    def setUp(self):
        """Set up test case"""
        # Create a chart for the reference date
        date = Datetime('2025/04/09', '20:51', '+05:30')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart = Chart(date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
        self.date = date
        self.location = pos

    def test_get_sarvatobhadra_chakra(self):
        """Test get_sarvatobhadra_chakra function"""
        # Get the Sarvatobhadra Chakra
        chakra = get_sarvatobhadra_chakra(self.chart)

        # Check that all required keys are present
        self.assertIn('janma_nakshatra', chakra)
        self.assertIn('grid', chakra)
        self.assertIn('planets', chakra)
        self.assertIn('tara_bala', chakra)

        # Check that the grid is a 9x9 grid
        self.assertEqual(len(chakra['grid']), 9)
        for row in chakra['grid']:
            self.assertEqual(len(row), 9)

        # Check that the planets dictionary contains all planets
        planets = chakra['planets']
        for planet_id in const.LIST_OBJECTS_VEDIC + [const.ASC]:
            self.assertIn(planet_id, planets)

            # Check that each planet has the required keys
            planet = planets[planet_id]
            self.assertIn('position', planet)
            self.assertIn('sign', planet)
            self.assertIn('longitude', planet)
            self.assertIn('nakshatra', planet)

        # Check that the tara_bala dictionary has the required keys
        tara_bala = chakra['tara_bala']
        self.assertIn('janma_tara', tara_bala)
        self.assertIn('current_tara', tara_bala)

        # Print the chakra information for reference
        print(f"Janma Nakshatra: {chakra['janma_nakshatra']}")
        print(f"Current Tara: {tara_bala['current_tara']}")

        # Print the positions of a few planets for reference
        print(f"Sun position in chakra: {planets[const.SUN]['position']}")
        print(f"Moon position in chakra: {planets[const.MOON]['position']}")
        print(f"Ascendant position in chakra: {planets[const.ASC]['position']}")

    def test_get_chakra_quality(self):
        """Test get_chakra_quality function"""
        # Get the Sarvatobhadra Chakra
        chakra = get_sarvatobhadra_chakra(self.chart)

        # Get the chakra quality
        quality = get_chakra_quality(chakra)

        # Check that all required keys are present
        self.assertIn('score', quality)
        self.assertIn('quality', quality)
        self.assertIn('factors', quality)

        # Check that the score is a number
        self.assertIsInstance(quality['score'], int)

        # Check that the quality is one of the expected values
        self.assertIn(quality['quality'], ['Excellent', 'Good', 'Neutral', 'Inauspicious', 'Highly Inauspicious'])

        # Check that the factors is a list
        self.assertIsInstance(quality['factors'], list)

        # Print the quality for reference
        print(f"Chakra Quality: {quality['quality']} (Score: {quality['score']})")
        print(f"Factors: {', '.join(quality['factors'])}")

    def test_get_auspicious_directions(self):
        """Test get_auspicious_directions function"""
        # Get the Sarvatobhadra Chakra
        chakra = get_sarvatobhadra_chakra(self.chart)

        # Get the auspicious directions
        auspicious_directions = get_auspicious_directions(chakra)

        # Check that the result is a list
        self.assertIsInstance(auspicious_directions, list)

        # Check each auspicious direction
        for direction in auspicious_directions:
            self.assertIn('direction', direction)
            self.assertIn('quality', direction)
            self.assertIn('score', direction)
            self.assertIn('factors', direction)

            # Check that the direction is one of the expected values
            self.assertIn(direction['direction'], ['North', 'Northeast', 'East', 'Southeast', 'South', 'Southwest', 'West', 'Northwest', 'Center'])

            # Check that the quality is one of the expected values
            self.assertIn(direction['quality'], ['Excellent', 'Good'])

            # Check that the score is a number
            self.assertIsInstance(direction['score'], (int, float))

            # Check that the factors is a list
            self.assertIsInstance(direction['factors'], list)

        # Print the auspicious directions for reference
        print(f"Found {len(auspicious_directions)} auspicious directions:")
        for i, direction in enumerate(auspicious_directions):
            print(f"{i+1}. {direction['direction']} - {direction['quality']} (Score: {direction['score']})")
            print(f"   Factors: {', '.join(direction['factors'])}")

    def test_get_inauspicious_directions(self):
        """Test get_inauspicious_directions function"""
        # Get the Sarvatobhadra Chakra
        chakra = get_sarvatobhadra_chakra(self.chart)

        # Get the inauspicious directions
        inauspicious_directions = get_inauspicious_directions(chakra)

        # Check that the result is a list
        self.assertIsInstance(inauspicious_directions, list)

        # Check each inauspicious direction
        for direction in inauspicious_directions:
            self.assertIn('direction', direction)
            self.assertIn('quality', direction)
            self.assertIn('score', direction)
            self.assertIn('factors', direction)

            # Check that the direction is one of the expected values
            self.assertIn(direction['direction'], ['North', 'Northeast', 'East', 'Southeast', 'South', 'Southwest', 'West', 'Northwest', 'Center'])

            # Check that the quality is one of the expected values
            self.assertIn(direction['quality'], ['Inauspicious', 'Highly Inauspicious'])

            # Check that the score is a number
            self.assertIsInstance(direction['score'], (int, float))

            # Check that the factors is a list
            self.assertIsInstance(direction['factors'], list)

        # Print the inauspicious directions for reference
        print(f"Found {len(inauspicious_directions)} inauspicious directions:")
        for i, direction in enumerate(inauspicious_directions):
            print(f"{i+1}. {direction['direction']} - {direction['quality']} (Score: {direction['score']})")
            print(f"   Factors: {', '.join(direction['factors'])}")

    def test_is_auspicious_position(self):
        """Test is_auspicious_position function"""
        # Check auspicious positions
        auspicious_positions = [
            (4, 4),  # Center
            (0, 0),  # Northwest corner
            (0, 8),  # Northeast corner
            (8, 0),  # Southwest corner
            (8, 8),  # Southeast corner
            (0, 4),  # North
            (4, 0),  # West
            (4, 8),  # East
            (8, 4)   # South
        ]

        for row, col in auspicious_positions:
            self.assertTrue(is_auspicious_position(row, col))

        # Check a few non-auspicious positions
        non_auspicious_positions = [
            (1, 1),
            (2, 2),
            (3, 3),
            (5, 5),
            (6, 6),
            (7, 7)
        ]

        for row, col in non_auspicious_positions:
            self.assertFalse(is_auspicious_position(row, col))

    def test_is_inauspicious_position(self):
        """Test is_inauspicious_position function"""
        # Check a few inauspicious positions
        # These are positions in the 3rd, 6th, and 8th positions from the center
        inauspicious_positions = [
            (1, 4),  # 3rd position from center (North)
            (4, 1),  # 3rd position from center (West)
            (7, 4),  # 3rd position from center (South)
            (4, 7)   # 3rd position from center (East)
        ]

        for row, col in inauspicious_positions:
            self.assertTrue(is_inauspicious_position(row, col), f"Position ({row}, {col}) should be inauspicious")

        # Check a few non-inauspicious positions
        non_inauspicious_positions = [
            (4, 4),  # Center
            (0, 0),  # Northwest corner
            (0, 8),  # Northeast corner
            (8, 0),  # Southwest corner
            (8, 8)   # Southeast corner
        ]

        for row, col in non_inauspicious_positions:
            self.assertFalse(is_inauspicious_position(row, col), f"Position ({row}, {col}) should not be inauspicious")


if __name__ == '__main__':
    unittest.main()
