#!/usr/bin/env python3
"""
Test Vimshopaka Bala Calculations

This script tests the Vimshopaka Bala (twenty-fold strength) calculations in flatlib.
"""

import unittest
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib.vedic.vargas import (
    D1, D2, D3, D4, D7, D9, D10, D12,
    D16, D20, D24, D27, D30, D40, D45, D60
)
from flatlib.vedic.vargas.analysis import (
    get_vimshopaka_bala, get_shodashavarga_bala,
    get_varga_visesha, get_bhava_bala
)


class TestVimshopakaBala(unittest.TestCase):
    """Test case for Vimshopaka Bala calculations"""

    def setUp(self):
        """Set up test case"""
        # Create a chart for the reference date
        date = Datetime('2025/04/09', '20:51', '+05:30')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart = Chart(date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)

    def test_shodashavarga_bala(self):
        """Test Shodashavarga Bala calculation"""
        # Calculate Shodashavarga Bala for each planet
        for planet_id in const.LIST_OBJECTS_VEDIC:
            shodashavarga_bala = get_shodashavarga_bala(self.chart, planet_id)

            # Check that the result is a dictionary
            self.assertIsInstance(shodashavarga_bala, dict)

            # Check that all 16 varga types are present
            for varga_type in [D1, D2, D3, D4, D7, D9, D10, D12, D16, D20, D24, D27, D30, D40, D45, D60]:
                self.assertIn(varga_type, shodashavarga_bala)

            # Check that the values are valid
            for varga_type, value in shodashavarga_bala.items():
                # Skip non-numeric values
                if isinstance(value, (int, float)):
                    self.assertGreaterEqual(value, 0.0)

            # Print the result for reference
            print(f"Shodashavarga Bala for {planet_id}:")
            for varga_type, value in shodashavarga_bala.items():
                if isinstance(value, (int, float)):
                    print(f"  {varga_type}: {value:.2f}")
                else:
                    print(f"  {varga_type}: {value}")

    def test_vimshopaka_bala(self):
        """Test Vimshopaka Bala calculation"""
        # Calculate Vimshopaka Bala for each planet
        for planet_id in const.LIST_OBJECTS_VEDIC:
            vimshopaka_bala = get_vimshopaka_bala(self.chart, planet_id)

            # Check that the result is a dictionary
            self.assertIsInstance(vimshopaka_bala, dict)

            # Check that all required keys are present
            self.assertIn('planet', vimshopaka_bala)
            self.assertIn('vimshopaka_bala', vimshopaka_bala)
            self.assertIn('max_possible', vimshopaka_bala)
            self.assertIn('percentage', vimshopaka_bala)

            # Check that the planet ID is correct
            self.assertEqual(vimshopaka_bala['planet'], planet_id)

            # Check that the Vimshopaka Bala is within the valid range
            self.assertGreaterEqual(vimshopaka_bala['vimshopaka_bala'], 0.0)
            self.assertLessEqual(vimshopaka_bala['vimshopaka_bala'], vimshopaka_bala['max_possible'])

            # Check that the percentage is within the valid range
            self.assertGreaterEqual(vimshopaka_bala['percentage'], 0.0)
            self.assertLessEqual(vimshopaka_bala['percentage'], 100.0)

            # Print the result for reference
            print(f"Vimshopaka Bala for {planet_id}: {vimshopaka_bala['vimshopaka_bala']:.2f} ({vimshopaka_bala['percentage']:.2f}%)")

    def test_vimshopaka_bala_weights(self):
        """Test Vimshopaka Bala weights"""
        # The weights for different vargas should sum to 20
        # D1: 3.5, D2: 1.0, D3: 1.0, D4: 0.5, D7: 0.5, D9: 3.0, D10: 2.0, D12: 0.5,
        # D16: 1.0, D20: 0.5, D24: 0.5, D27: 0.5, D30: 1.0, D40: 1.5, D45: 1.5, D60: 1.5

        # Calculate Vimshopaka Bala for the Sun
        vimshopaka_bala = get_vimshopaka_bala(self.chart, const.SUN)

        # Check that the maximum possible value is 20.0
        self.assertEqual(vimshopaka_bala['max_possible'], 20.0)

        # Calculate Shodashavarga Bala for the Sun
        shodashavarga_bala = get_shodashavarga_bala(self.chart, const.SUN)

        # Calculate the expected Vimshopaka Bala manually
        weights = {
            D1: 3.5, D2: 1.0, D3: 1.0, D4: 0.5, D7: 0.5, D9: 3.0, D10: 2.0, D12: 0.5,
            D16: 1.0, D20: 0.5, D24: 0.5, D27: 0.5, D30: 1.0, D40: 1.5, D45: 1.5, D60: 1.5
        }

        expected_bala = 0.0
        for varga_type, weight in weights.items():
            if varga_type in shodashavarga_bala:
                expected_bala += shodashavarga_bala[varga_type] * weight

        # Check that the calculated Vimshopaka Bala matches the expected value
        self.assertAlmostEqual(vimshopaka_bala['vimshopaka_bala'], expected_bala, places=6)

    def test_varga_visesha(self):
        """Test Varga Visesha calculation"""
        # Calculate Varga Visesha for each planet
        for planet_id in const.LIST_OBJECTS_VEDIC:
            varga_visesha = get_varga_visesha(self.chart, planet_id)

            # Check that the result is a dictionary
            self.assertIsInstance(varga_visesha, dict)

            # Check that all required keys are present
            self.assertIn('planet', varga_visesha)
            self.assertIn('highest', varga_visesha)

            # Check that the planet ID is correct
            self.assertEqual(varga_visesha['planet'], planet_id)

            # Check for specific varga visesha keys
            for key in ['parijatamsha', 'uttamamsha', 'gopuramsha', 'simhasanamsha', 'paravatamsha', 'devalokamsha', 'brahmalokamsha']:
                self.assertIn(key, varga_visesha)

            # Print the result for reference
            print(f"Varga Visesha for {planet_id}:")
            print(f"  Highest: {varga_visesha['highest']}")
            # Print the varga visesha details
            details = []
            for key in ['parijatamsha', 'uttamamsha', 'gopuramsha', 'simhasanamsha', 'paravatamsha', 'devalokamsha', 'brahmalokamsha']:
                if varga_visesha[key]:
                    details.append(key)
            print(f"  Details: {', '.join(details) if details else 'None'}")

    def test_bhava_bala(self):
        """Test Bhava Bala calculation"""
        # Skip this test for now as it requires a different house implementation
        self.skipTest("This test requires a different house implementation")


if __name__ == '__main__':
    unittest.main()
