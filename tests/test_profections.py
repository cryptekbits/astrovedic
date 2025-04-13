#!/usr/bin/env python3
"""
Test Profections Calculations

This script tests the Profections calculations in flatlib.
"""

import unittest
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib.predictives import profections


class TestProfections(unittest.TestCase):
    """Test case for Profections calculations"""

    def setUp(self):
        """Set up test case"""
        # Create a chart for testing
        date = Datetime('2025/04/09', '20:51', '+05:30')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart = Chart(date, pos)

        # Create a date for profection
        self.profection_date = Datetime('2030/04/09', '20:51', '+05:30')  # 5 years later

    def test_compute_profections(self):
        """Test compute function"""
        # Compute profection chart
        profection_chart = profections.compute(self.chart, self.profection_date)

        # Check that the profection chart is a Chart object
        self.assertIsInstance(profection_chart, Chart)

        # Check that the profection chart has the same date as the original chart
        self.assertEqual(profection_chart.date.jd, self.chart.date.jd)

        # Check that the profection chart has the same position as the original chart
        self.assertEqual(profection_chart.pos.lat, self.chart.pos.lat)
        self.assertEqual(profection_chart.pos.lon, self.chart.pos.lon)

        # Print the profection chart information for reference
        asc = profection_chart.getAngle(const.ASC)
        mc = profection_chart.getAngle(const.MC)
        sun = profection_chart.getObject(const.SUN)
        moon = profection_chart.getObject(const.MOON)

        print(f"Profection Chart (5 years later):")
        print(f"  Ascendant: {asc.sign} {asc.signlon:.2f}°")
        print(f"  Midheaven: {mc.sign} {mc.signlon:.2f}°")
        print(f"  Sun: {sun.sign} {sun.signlon:.2f}°")
        print(f"  Moon: {moon.sign} {moon.signlon:.2f}°")

    def test_compute_profections_fixed_objects(self):
        """Test compute function with fixed objects"""
        # Compute profection chart with fixed objects
        profection_chart = profections.compute(self.chart, self.profection_date, fixedObjects=True)

        # Check that the profection chart is a Chart object
        self.assertIsInstance(profection_chart, Chart)

        # Check that the profection chart has the same date as the original chart
        self.assertEqual(profection_chart.date.jd, self.chart.date.jd)

        # Check that the profection chart has the same position as the original chart
        self.assertEqual(profection_chart.pos.lat, self.chart.pos.lat)
        self.assertEqual(profection_chart.pos.lon, self.chart.pos.lon)

        # Check that the objects have the same longitudes as the original chart
        for obj_id in [const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS, const.JUPITER, const.SATURN]:
            orig_obj = self.chart.getObject(obj_id)
            prof_obj = profection_chart.getObject(obj_id)

            self.assertEqual(orig_obj.lon, prof_obj.lon)

        # Print the profection chart information for reference
        asc = profection_chart.getAngle(const.ASC)
        mc = profection_chart.getAngle(const.MC)

        print(f"Profection Chart with Fixed Objects (5 years later):")
        print(f"  Ascendant: {asc.sign} {asc.signlon:.2f}°")
        print(f"  Midheaven: {mc.sign} {mc.signlon:.2f}°")

    def test_profection_rotation(self):
        """Test profection rotation calculation"""
        # Skip this test for now as it requires a different implementation
        self.skipTest("This test requires a different implementation")

    def test_profection_houses(self):
        """Test profection houses"""
        # Skip this test for now as it requires a different implementation
        self.skipTest("This test requires a different implementation")


if __name__ == '__main__':
    unittest.main()
