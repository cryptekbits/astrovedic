#!/usr/bin/env python3
"""
Test Compatibility Analysis Core Functions

This script tests the core compatibility analysis functions in astrovedic.vedic.compatibility.
"""

import unittest
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic import const
from astrovedic.vedic.compatibility.core import (
    get_compatibility_score, get_compatibility_factors,
    get_compatibility_description, get_compatibility_report,
    get_compatibility_level
)


class TestCompatibilityCore(unittest.TestCase):
    """Test case for compatibility analysis core functions"""

    def setUp(self):
        """Set up test case"""
        # Create charts for two individuals
        # Person 1: Reference date
        date1 = Datetime('2025/04/09', '20:51', '+05:30')
        pos1 = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart1 = Chart(date1, pos1, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)

        # Person 2: Different date
        date2 = Datetime('1990/06/15', '10:30', '+05:30')
        pos2 = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart2 = Chart(date2, pos2, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)

    def test_get_compatibility_score(self):
        """Test get_compatibility_score function"""
        # Calculate the compatibility score
        score = get_compatibility_score(self.chart1, self.chart2)

        # Check that the score is within the valid range
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

        # Print the score for reference
        print(f"Compatibility Score: {score:.2f}/100")

    def test_get_compatibility_factors(self):
        """Test get_compatibility_factors function"""
        # Get the compatibility factors
        factors = get_compatibility_factors(self.chart1, self.chart2)

        # Check that the result is a list
        self.assertIsInstance(factors, list)

        # Print the factors for reference
        print(f"Found {len(factors)} compatibility factors:")
        for i, factor in enumerate(factors):
            print(f"{i+1}. {factor}")

    def test_get_compatibility_description(self):
        """Test get_compatibility_description function"""
        # Get the compatibility description
        description = get_compatibility_description(self.chart1, self.chart2)

        # Check that the result is a string
        self.assertIsInstance(description, str)

        # Check that the description is not empty
        self.assertGreater(len(description), 0)

        # Print the description for reference
        print(f"Compatibility Description:\n{description}")

    def test_get_compatibility_report(self):
        """Test get_compatibility_report function"""
        # Get the compatibility report
        report = get_compatibility_report(self.chart1, self.chart2)

        # Check that the result is a dictionary
        self.assertIsInstance(report, dict)

        # Check that all required keys are present
        self.assertIn('score', report)
        self.assertIn('level', report)
        self.assertIn('description', report)
        self.assertIn('factors', report)
        self.assertIn('kuta_scores', report)
        self.assertIn('total_kuta_score', report)
        self.assertIn('dosha_analysis', report)
        self.assertIn('dosha_cancellation', report)
        self.assertIn('dosha_remedies', report)
        self.assertIn('dasha_compatibility', report)
        self.assertIn('navamsa_compatibility', report)

        # Check that the score is within the valid range
        self.assertGreaterEqual(report['score'], 0)
        self.assertLessEqual(report['score'], 100)

        # Check that the level is one of the expected values
        self.assertIn(report['level'], ['Excellent', 'Good', 'Average', 'Challenging', 'Difficult'])

        # Print the report summary for reference
        print(f"Compatibility Report Summary:")
        print(f"Score: {report['score']:.2f}/100")
        print(f"Level: {report['level']}")
        print(f"Description: {report['description'][:100]}...")
        print(f"Factors: {len(report['factors'])} factors found")
        print(f"Kuta Scores: {len(report['kuta_scores'])} Kutas analyzed")
        print(f"Total Kuta Score: {report['total_kuta_score']['score']}/{report['total_kuta_score']['max_score']}")

    def test_get_compatibility_level(self):
        """Test get_compatibility_level function"""
        # Test with different scores
        test_cases = [
            (90, 'Excellent'),
            (75, 'Good'),
            (50, 'Average'),
            (30, 'Challenging'),
            (10, 'Difficult')
        ]

        for score, expected_level in test_cases:
            level = get_compatibility_level(score)
            self.assertEqual(level, expected_level)

        # Print the levels for reference
        print("Compatibility Levels:")
        for score, level in test_cases:
            print(f"Score {score}: {level}")


if __name__ == '__main__':
    unittest.main()
