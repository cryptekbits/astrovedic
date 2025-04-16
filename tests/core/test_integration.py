#!/usr/bin/env python3
"""
Test Integration

This script tests integration between different modules in astrovedic.
"""

import unittest
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic import const
from astrovedic.vedic.api import VedicChart, create_vedic_chart
from astrovedic.vedic.nakshatras import get_nakshatra
from astrovedic.vedic.panchang import get_panchang
from astrovedic.vedic.upagrah import get_upagrah_positions
from astrovedic.vedic.vargas.navamsha import calculate_d9
from astrovedic.vedic.kp_utils import get_kp_sublord_wrapper as get_kp_sublord, create_kp_chart


class TestFullSystemIntegration(unittest.TestCase):
    """Test case for full system integration"""

    def setUp(self):
        """Set up test case"""
        # Create a chart for testing
        self.date = Datetime('2025/04/09', '20:51', '+05:30')
        self.pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart = Chart(self.date, self.pos)

        # Create a VedicChart for testing
        self.vedic_chart = VedicChart(self.chart)

    def test_full_chart_creation(self):
        """Test full chart creation"""
        # Check that the chart is created correctly
        self.assertIsNotNone(self.chart)

        # Check that the chart has the correct date and position
        self.assertEqual(self.chart.date.jd, self.date.jd)
        self.assertEqual(self.chart.pos.lat, self.pos.lat)
        self.assertEqual(self.chart.pos.lon, self.pos.lon)

        # Check that the chart has all the required objects
        for obj_id in [const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS, const.JUPITER, const.SATURN]:
            obj = self.chart.getObject(obj_id)
            self.assertIsNotNone(obj)
            self.assertEqual(obj.id, obj_id)

        # Print the chart information for reference
        print(f"Full Chart:")
        print(f"  Date: {self.chart.date.date.date()}/{self.chart.date.time.time()}")
        print(f"  Position: {self.chart.pos.lat}°, {self.chart.pos.lon}°")

        # Print the positions of the planets
        print(f"Planet Positions:")
        for obj_id in [const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS, const.JUPITER, const.SATURN]:
            obj = self.chart.getObject(obj_id)
            print(f"  {obj_id}: {obj.sign} {obj.signlon:.2f}°")

    def test_vedic_chart_creation(self):
        """Test VedicChart creation"""
        # Check that the VedicChart is created correctly
        self.assertIsNotNone(self.vedic_chart)

        # Check that the VedicChart has the correct chart
        self.assertEqual(self.vedic_chart.chart.date.jd, self.chart.date.jd)
        self.assertEqual(self.vedic_chart.chart.pos.lat, self.chart.pos.lat)
        self.assertEqual(self.vedic_chart.chart.pos.lon, self.chart.pos.lon)

        # Print the VedicChart information for reference
        print(f"VedicChart:")
        print(f"  Date: {self.vedic_chart.chart.date.date.date()}/{self.vedic_chart.chart.date.time.time()}")
        print(f"  Position: {self.vedic_chart.chart.pos.lat}°, {self.vedic_chart.chart.pos.lon}°")
        print(f"  Ayanamsa: {self.vedic_chart.ayanamsa}")


class TestCoreLibraryVedicIntegration(unittest.TestCase):
    """Test case for integration between core library and Vedic extensions"""

    def setUp(self):
        """Set up test case"""
        # Create a chart for testing
        self.date = Datetime('2025/04/09', '20:51', '+05:30')
        self.pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart = Chart(self.date, self.pos)

    def test_nakshatra_integration(self):
        """Test integration with nakshatra module"""
        # Get the Sun
        sun = self.chart.getObject(const.SUN)

        # Get the nakshatra of the Sun
        nakshatra = get_nakshatra(sun.lon)

        # Check that the nakshatra is returned correctly
        self.assertIsNotNone(nakshatra)
        self.assertIn('name', nakshatra)
        self.assertIn('lord', nakshatra)

        # Print the nakshatra information for reference
        print(f"Sun Nakshatra:")
        print(f"  Name: {nakshatra['name']}")
        print(f"  Lord: {nakshatra['lord']}")

    def test_panchang_integration(self):
        """Test integration with panchang module"""
        # Get the panchang
        panchang = get_panchang(self.chart.date.jd, self.chart.pos.lat, self.chart.pos.lon, self.chart.date.utcoffset)

        # Check that the panchang is returned correctly
        self.assertIsNotNone(panchang)
        self.assertIn('tithi', panchang)
        self.assertIn('karana', panchang)
        self.assertIn('yoga', panchang)
        self.assertIn('vara', panchang)

        # Print the panchang information for reference
        print(f"Panchang:")
        print(f"  Tithi: {panchang['tithi']['name']}")
        print(f"  Karana: {panchang['karana']['name']}")
        print(f"  Yoga: {panchang['yoga']['name']}")
        print(f"  Vara: {panchang['vara']['name']}")

    def test_upagrah_integration(self):
        """Test integration with upagrah module"""
        # Get the upagrah positions
        upagrah_positions = get_upagrah_positions(self.chart)

        # Check that the upagrah positions are returned correctly
        self.assertIsNotNone(upagrah_positions)
        self.assertIn('Gulika', upagrah_positions)
        self.assertIn('Mandi', upagrah_positions)

        # Print the upagrah positions for reference
        print(f"Upagrah Positions:")
        print(f"  Gulika: {upagrah_positions['Gulika']['lon']:.2f}°")
        print(f"  Mandi: {upagrah_positions['Mandi']['lon']:.2f}°")

    def test_varga_integration(self):
        """Test integration with varga module"""
        # Get the Sun
        sun = self.chart.getObject(const.SUN)

        # Calculate the D9 (Navamsha) position of the Sun
        d9_position = calculate_d9(sun.lon)

        # Check that the D9 position is returned correctly
        self.assertIsNotNone(d9_position)
        self.assertIsInstance(d9_position, float)

        # Print the D9 position for reference
        print(f"Sun D9 Position: {d9_position:.2f}°")

    def test_kp_integration(self):
        """Test integration with KP module"""
        # Get the Sun
        sun = self.chart.getObject(const.SUN)

        # Get the KP sublord of the Sun
        sublord = get_kp_sublord(sun.lon)

        # Check that the sublord is returned correctly
        self.assertIsNotNone(sublord)

        # Print the sublord for reference
        print(f"Sun KP Sublord: {sublord}")


class TestVedicModulesIntegration(unittest.TestCase):
    """Test case for integration between different Vedic modules"""

    def setUp(self):
        """Set up test case"""
        # Create a VedicChart for testing
        self.date = Datetime('2025/04/09', '20:51', '+05:30')
        self.pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.vedic_chart = create_vedic_chart('2025/04/09', '20:51', 12.9716, 77.5946, '+05:30')

    def test_nakshatra_panchang_integration(self):
        """Test integration between nakshatra and panchang modules"""
        # Get the nakshatra of the Moon
        moon_nakshatra = self.vedic_chart.get_nakshatra(const.MOON)

        # Get the panchang
        panchang = self.vedic_chart.get_panchang()

        # Check that the nakshatra and panchang are returned correctly
        self.assertIsNotNone(moon_nakshatra)
        self.assertIsNotNone(panchang)

        # Print the nakshatra and panchang information for reference
        print(f"Moon Nakshatra:")
        print(f"  Name: {moon_nakshatra['name']}")
        print(f"  Lord: {moon_nakshatra['lord']}")

        print(f"Panchang:")
        print(f"  Tithi: {panchang['tithi']['name']}")
        print(f"  Karana: {panchang['karana']['name']}")
        print(f"  Yoga: {panchang['yoga']['name']}")
        print(f"  Vara: {panchang['vara']['name']}")

    def test_upagrah_varga_integration(self):
        """Test integration between upagrah and varga modules"""
        # Get the upagrah positions
        upagrah_positions = self.vedic_chart.get_upagrah_positions()

        # Get a varga chart
        d9_chart = self.vedic_chart.get_varga_chart('D9')

        # Check that the upagrah positions and varga chart are returned correctly
        self.assertIsNotNone(upagrah_positions)
        self.assertIsNotNone(d9_chart)

        # Print the upagrah positions and varga chart information for reference
        print(f"Upagrah Positions:")
        print(f"  Gulika: {upagrah_positions['Gulika']['lon']:.2f}°")
        print(f"  Mandi: {upagrah_positions['Mandi']['lon']:.2f}°")

        print(f"D9 Chart:")
        print(f"  Date: {d9_chart.date.date.date()}/{d9_chart.date.time.time()}")
        print(f"  Position: {d9_chart.pos.lat}°, {d9_chart.pos.lon}°")

    def test_real_world_chart(self):
        """Test with a real-world chart"""
        # Create a chart for a real person (using a public figure's birth data)
        # Albert Einstein: March 14, 1879, 11:30 AM, Ulm, Germany
        einstein_chart = create_vedic_chart('1879/03/14', '11:30', 48.4011, 9.9876, '+01:00')

        # Check that the chart is created correctly
        self.assertIsNotNone(einstein_chart)

        # Get the positions of the planets
        sun = einstein_chart.get_planet(const.SUN)
        moon = einstein_chart.get_planet(const.MOON)
        mercury = einstein_chart.get_planet(const.MERCURY)
        venus = einstein_chart.get_planet(const.VENUS)
        mars = einstein_chart.get_planet(const.MARS)
        jupiter = einstein_chart.get_planet(const.JUPITER)
        saturn = einstein_chart.get_planet(const.SATURN)

        # Print the planet positions for reference
        print(f"Albert Einstein's Chart:")
        print(f"  Sun: {sun.sign} {sun.signlon:.2f}°")
        print(f"  Moon: {moon.sign} {moon.signlon:.2f}°")
        print(f"  Mercury: {mercury.sign} {mercury.signlon:.2f}°")
        print(f"  Venus: {venus.sign} {venus.signlon:.2f}°")
        print(f"  Mars: {mars.sign} {mars.signlon:.2f}°")
        print(f"  Jupiter: {jupiter.sign} {jupiter.signlon:.2f}°")
        print(f"  Saturn: {saturn.sign} {saturn.signlon:.2f}°")

        # Get the nakshatra of the Moon
        moon_nakshatra = einstein_chart.get_nakshatra(const.MOON)

        # Print the Moon's nakshatra for reference
        print(f"  Moon Nakshatra: {moon_nakshatra['name']} (Lord: {moon_nakshatra['lord']})")


if __name__ == '__main__':
    unittest.main()
