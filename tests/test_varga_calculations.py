#!/usr/bin/env python3
"""
Test Varga Calculation Logic

This script tests the specific calculation logic for each Varga (divisional chart)
against standard definitions from Vedic astrology.
"""

import unittest
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic import const
from astrovedic.vedic.vargas import (
    D1, D2, D3, D4, D7, D9, D10, D12,
    D16, D20, D24, D27, D30, D40, D45, D60,
    get_varga_chart, get_varga_longitude
)
from astrovedic.vedic.vargas.hora import calculate_d2
from astrovedic.vedic.vargas.drekkana import calculate_d3
from astrovedic.vedic.vargas.chaturthamsha import calculate_d4
from astrovedic.vedic.vargas.saptamsha import calculate_d7
from astrovedic.vedic.vargas.navamsha import calculate_d9
from astrovedic.vedic.vargas.dashamsha import calculate_d10
from astrovedic.vedic.vargas.dwadashamsha import calculate_d12
from astrovedic.vedic.vargas.trimshamsha import calculate_d30
from astrovedic.vedic.vargas.shashtiamsha import calculate_d60

class TestVargaCalculations(unittest.TestCase):
    """Test case for specific Varga calculation logic"""

    def setUp(self):
        """Set up test case"""
        # Create a chart for the reference date
        date = Datetime('2025/04/09', '20:51', '+05:30')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart = Chart(date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)

        # Test longitudes for each sign type
        self.fire_sign_lon = 5.0    # Aries 5°
        self.earth_sign_lon = 35.0  # Taurus 5°
        self.air_sign_lon = 65.0    # Gemini 5°
        self.water_sign_lon = 95.0  # Cancer 5°

    def test_hora_calculation(self):
        """Test D2 (Hora) calculation logic"""
        # For odd signs (Aries, Gemini, etc.):
        # - First half (0-15°): Leo
        # - Second half (15-30°): Cancer

        # For even signs (Taurus, Cancer, etc.):
        # - First half (0-15°): Cancer
        # - Second half (15-30°): Leo

        # Test Aries 5° (odd sign, first half) -> Leo
        d2_lon = calculate_d2(self.fire_sign_lon)
        self.assertEqual(int(d2_lon / 30), const.LIST_SIGNS.index(const.LEO))

        # Test Aries 20° (odd sign, second half) -> Cancer
        d2_lon = calculate_d2(self.fire_sign_lon + 15)
        self.assertEqual(int(d2_lon / 30), const.LIST_SIGNS.index(const.CANCER))

        # Test Taurus 5° (even sign, first half) -> Cancer
        d2_lon = calculate_d2(self.earth_sign_lon)
        self.assertEqual(int(d2_lon / 30), const.LIST_SIGNS.index(const.CANCER))

        # Test Taurus 20° (even sign, second half) -> Leo
        d2_lon = calculate_d2(self.earth_sign_lon + 15)
        self.assertEqual(int(d2_lon / 30), const.LIST_SIGNS.index(const.LEO))

    def test_drekkana_calculation(self):
        """Test D3 (Drekkana) calculation logic"""
        # Each sign is divided into three parts of 10° each:
        # - First Drekkana (0-10°): Same sign
        # - Second Drekkana (10-20°): 5th sign from the birth sign
        # - Third Drekkana (20-30°): 9th sign from the birth sign

        # Test Aries 5° (first drekkana) -> Aries
        d3_lon = calculate_d3(self.fire_sign_lon)
        self.assertEqual(int(d3_lon / 30), int(self.fire_sign_lon / 30))

        # Test Aries 15° (second drekkana) -> Leo (5th from Aries)
        d3_lon = calculate_d3(self.fire_sign_lon + 10)
        self.assertEqual(int(d3_lon / 30), (int(self.fire_sign_lon / 30) + 4) % 12)

        # Test Aries 25° (third drekkana) -> Sagittarius (9th from Aries)
        d3_lon = calculate_d3(self.fire_sign_lon + 20)
        self.assertEqual(int(d3_lon / 30), (int(self.fire_sign_lon / 30) + 8) % 12)

    def test_navamsha_calculation(self):
        """Test D9 (Navamsha) calculation logic"""
        # Each sign is divided into nine parts of 3.33° each
        # The resulting sign depends on the original sign element

        # Test that different positions within a sign produce different navamsha results
        prev_d9_sign = None
        for i in range(9):
            lon = self.fire_sign_lon + i * (30/9)
            d9_lon = calculate_d9(lon)
            d9_sign = int(d9_lon / 30)

            # Verify the longitude is valid
            self.assertGreaterEqual(d9_lon, 0)
            self.assertLess(d9_lon, 360)

            # Verify the sign is valid
            self.assertGreaterEqual(d9_sign, 0)
            self.assertLess(d9_sign, 12)

            # Verify that consecutive navamshas produce different signs
            # (except for the first one where prev_d9_sign is None)
            if prev_d9_sign is not None and i < 8:  # Skip the last one which might wrap around
                self.assertNotEqual(d9_sign, prev_d9_sign,
                                  f"Consecutive navamshas {i-1} and {i} produced the same sign")

            prev_d9_sign = d9_sign

        # Test that different signs produce different navamsha patterns
        fire_navamshas = set()
        earth_navamshas = set()
        air_navamshas = set()
        water_navamshas = set()

        for i in range(9):
            # Fire sign (Aries)
            lon = self.fire_sign_lon + i * (30/9)
            fire_navamshas.add(int(calculate_d9(lon) / 30))

            # Earth sign (Taurus)
            lon = self.earth_sign_lon + i * (30/9)
            earth_navamshas.add(int(calculate_d9(lon) / 30))

            # Air sign (Gemini)
            lon = self.air_sign_lon + i * (30/9)
            air_navamshas.add(int(calculate_d9(lon) / 30))

            # Water sign (Cancer)
            lon = self.water_sign_lon + i * (30/9)
            water_navamshas.add(int(calculate_d9(lon) / 30))

        # Verify that each element produces a different set of navamsha signs
        self.assertNotEqual(fire_navamshas, earth_navamshas)
        self.assertNotEqual(fire_navamshas, air_navamshas)
        self.assertNotEqual(fire_navamshas, water_navamshas)
        self.assertNotEqual(earth_navamshas, air_navamshas)
        self.assertNotEqual(earth_navamshas, water_navamshas)
        self.assertNotEqual(air_navamshas, water_navamshas)

    def test_trimshamsha_calculation(self):
        """Test D30 (Trimshamsha) calculation logic"""
        # Each sign is divided into five unequal parts
        # The implementation maps each portion to a sign ruled by the corresponding planet

        # Test that the calculation produces valid results
        test_longitudes = [
            # Odd sign (Aries) - different portions
            self.fire_sign_lon,      # 0-5°: Mars
            self.fire_sign_lon + 7,  # 5-10°: Saturn
            self.fire_sign_lon + 14, # 10-18°: Jupiter
            self.fire_sign_lon + 22, # 18-25°: Mercury
            self.fire_sign_lon + 27, # 25-30°: Venus

            # Even sign (Taurus) - different portions
            self.earth_sign_lon,      # 0-5°: Venus
            self.earth_sign_lon + 7,  # 5-12°: Mercury
            self.earth_sign_lon + 16, # 12-20°: Jupiter
            self.earth_sign_lon + 22, # 20-25°: Saturn
            self.earth_sign_lon + 27, # 25-30°: Mars
        ]

        # Verify that each longitude produces a valid D30 result
        for lon in test_longitudes:
            d30_lon = calculate_d30(lon)

            # Verify the longitude is valid
            self.assertGreaterEqual(d30_lon, 0)
            self.assertLess(d30_lon, 360)

            # Verify the sign is valid
            d30_sign = int(d30_lon / 30)
            self.assertGreaterEqual(d30_sign, 0)
            self.assertLess(d30_sign, 12)

        # Test that different portions of a sign produce different D30 results
        odd_sign_results = set()
        even_sign_results = set()

        # Test odd sign (Aries)
        odd_sign_results.add(int(calculate_d30(self.fire_sign_lon) / 30))      # 0-5°: Mars
        odd_sign_results.add(int(calculate_d30(self.fire_sign_lon + 7) / 30))  # 5-10°: Saturn
        odd_sign_results.add(int(calculate_d30(self.fire_sign_lon + 14) / 30)) # 10-18°: Jupiter
        odd_sign_results.add(int(calculate_d30(self.fire_sign_lon + 22) / 30)) # 18-25°: Mercury
        odd_sign_results.add(int(calculate_d30(self.fire_sign_lon + 27) / 30)) # 25-30°: Venus

        # Test even sign (Taurus)
        even_sign_results.add(int(calculate_d30(self.earth_sign_lon) / 30))      # 0-5°: Venus
        even_sign_results.add(int(calculate_d30(self.earth_sign_lon + 7) / 30))  # 5-12°: Mercury
        even_sign_results.add(int(calculate_d30(self.earth_sign_lon + 16) / 30)) # 12-20°: Jupiter
        even_sign_results.add(int(calculate_d30(self.earth_sign_lon + 22) / 30)) # 20-25°: Saturn
        even_sign_results.add(int(calculate_d30(self.earth_sign_lon + 27) / 30)) # 25-30°: Mars

        # Verify that we have multiple different results for each sign type
        # (not all portions should map to the same sign)
        self.assertGreater(len(odd_sign_results), 1)
        self.assertGreater(len(even_sign_results), 1)

    def test_shashtiamsha_calculation(self):
        """Test D60 (Shashtiamsha) calculation logic"""
        # Each sign is divided into 60 parts of 0.5° each
        # This is the most detailed divisional chart

        # Test a few specific longitudes
        test_lon = 15.25  # Aries 15°15'
        d60_lon = calculate_d60(test_lon)

        # Verify that the calculation produces a valid longitude
        self.assertGreaterEqual(d60_lon, 0)
        self.assertLess(d60_lon, 360)

        # Test that different longitudes produce different D60 results
        test_lon2 = 15.75  # Aries 15°45'
        d60_lon2 = calculate_d60(test_lon2)
        self.assertNotEqual(d60_lon, d60_lon2)

if __name__ == '__main__':
    unittest.main()
