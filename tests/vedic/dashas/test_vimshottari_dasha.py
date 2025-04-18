#!/usr/bin/env python3
"""
Test Vimshottari Dasha Calculations

This script tests the Vimshottari Dasha calculations in astrovedic.
"""

import unittest
from datetime import datetime
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic import const
from astrovedic.vedic.dashas import (
    calculate_dasha_balance, get_mahadasha_sequence,
    get_antardasha_sequence, get_pratyantardasha_sequence,
    calculate_dasha_periods, get_current_dasha
)
from astrovedic.vedic.nakshatras import VIMSHOTTARI_PERIODS

class TestVimshottariDasha(unittest.TestCase):
    """Test Vimshottari Dasha calculations"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a chart for the reference date
        self.date = Datetime('2025/04/09', '20:51', '+05:30')
        self.pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart = Chart(self.date, self.pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)

        # Get the Moon's longitude
        self.moon = self.chart.getObject(const.MOON)
        self.moon_longitude = self.moon.lon

    def test_dasha_balance(self):
        """Test dasha balance calculation"""
        # Calculate dasha balance
        balance = calculate_dasha_balance(self.moon_longitude)

        # Balance should be a positive number less than the maximum dasha period
        self.assertGreater(balance, 0)
        self.assertLess(balance, 20)  # Maximum dasha period is Venus at 20 years

        # Test with known values
        # Moon at 0° Ashwini (Ketu's nakshatra) should have full balance of 7 years
        balance_ashwini_start = calculate_dasha_balance(0)
        self.assertAlmostEqual(balance_ashwini_start, 7.0, places=1)

        # Moon at end of Ashwini should have almost 0 balance
        balance_ashwini_end = calculate_dasha_balance(13.33)
        self.assertLess(balance_ashwini_end, 0.1)

    def test_mahadasha_sequence(self):
        """Test mahadasha sequence calculation"""
        # Get mahadasha sequence
        sequence = get_mahadasha_sequence(self.moon_longitude)

        # Should have 9 dashas
        self.assertEqual(len(sequence), 9)

        # First dasha should have a partial duration
        self.assertLess(sequence[0]['years'], 20)

        # Verify the sequence follows the Vimshottari order
        # The exact order depends on the Moon's nakshatra
        # Just check that all planets are present with their correct durations
        planet_years = {item['planet']: item['years'] for item in sequence[1:]}

        # Check that full periods are correct for subsequent dashas
        for planet, years in planet_years.items():
            if planet != sequence[0]['planet']:  # Skip the first partial dasha
                self.assertEqual(years, VIMSHOTTARI_PERIODS[planet])

        # Test with known values
        # Moon at 0° Ashwini (Ketu's nakshatra) should start with Ketu
        sequence_ashwini = get_mahadasha_sequence(0)
        self.assertEqual(sequence_ashwini[0]['planet'], const.KETU)
        self.assertEqual(sequence_ashwini[1]['planet'], const.VENUS)

    def test_antardasha_sequence(self):
        """Test antardasha sequence calculation"""
        # Get antardasha sequence for Venus mahadasha
        sequence = get_antardasha_sequence(const.VENUS, 20)

        # Should have 9 antardashas
        self.assertEqual(len(sequence), 9)

        # First antardasha should be Venus itself
        self.assertEqual(sequence[0]['planet'], const.VENUS)

        # Sum of all antardashas should equal the mahadasha duration
        total_years = sum(ad['years'] for ad in sequence)
        self.assertAlmostEqual(total_years, 20, places=5)

    def test_pratyantardasha_sequence(self):
        """Test pratyantardasha sequence calculation"""
        # Get pratyantardasha sequence for Sun antardasha
        sequence = get_pratyantardasha_sequence(const.SUN, 1)

        # Should have 9 pratyantardashas
        self.assertEqual(len(sequence), 9)

        # First pratyantardasha should be Sun itself
        self.assertEqual(sequence[0]['planet'], const.SUN)

        # Sum of all pratyantardashas should equal the antardasha duration
        total_years = sum(pad['years'] for pad in sequence)
        self.assertAlmostEqual(total_years, 1, places=5)

    def test_dasha_periods(self):
        """Test dasha periods calculation"""
        # Calculate dasha periods
        periods = calculate_dasha_periods(self.date, self.moon_longitude)

        # Should have mahadashas
        self.assertIn('mahadashas', periods)
        self.assertGreater(len(periods['mahadashas']), 0)

        # Each mahadasha should have antardashas
        for mahadasha in periods['mahadashas']:
            self.assertIn('antardashas', mahadasha)
            self.assertEqual(len(mahadasha['antardashas']), 9)

            # Each antardasha should have pratyantardashas
            for antardasha in mahadasha['antardashas']:
                self.assertIn('pratyantardashas', antardasha)
                self.assertEqual(len(antardasha['pratyantardashas']), 9)

    def test_current_dasha(self):
        """Test current dasha calculation"""
        # Calculate dasha periods
        periods = calculate_dasha_periods(self.date, self.moon_longitude)

        # Get current dasha for the birth date
        # Create a Python datetime from the components
        date_parts = str(self.date.date).strip('<>').split('/')
        time_parts = str(self.date.time).strip('<>').split(':')

        year = int(date_parts[0])
        month = int(date_parts[1])
        day = int(date_parts[2])
        hour = int(time_parts[0])
        minute = int(time_parts[1])

        birth_dt = datetime(year, month, day, hour, minute)
        current = get_current_dasha(periods, birth_dt)

        # Should have mahadasha, antardasha, and pratyantardasha
        self.assertIn('mahadasha', current)
        self.assertIn('antardasha', current)
        self.assertIn('pratyantardasha', current)

        # Should have start and end dates
        self.assertIn('mahadasha_start', current)
        self.assertIn('mahadasha_end', current)
        self.assertIn('antardasha_start', current)
        self.assertIn('antardasha_end', current)
        self.assertIn('pratyantardasha_start', current)
        self.assertIn('pratyantardasha_end', current)

if __name__ == '__main__':
    unittest.main()
