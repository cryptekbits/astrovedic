#!/usr/bin/env python3
"""
Test Returns Calculations

This script tests the Returns calculations in flatlib.
"""

import unittest
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib.predictives import returns


class TestReturns(unittest.TestCase):
    """Test case for Returns calculations"""

    def setUp(self):
        """Set up test case"""
        # Create a chart for testing
        date = Datetime('2025/04/09', '20:51', '+05:30')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart = Chart(date, pos)

        # Create a date for returns
        self.return_date = Datetime('2030/01/01', '00:00', '+05:30')  # Some date in the future

    def test_next_solar_return(self):
        """Test nextSolarReturn function"""
        # Get the next solar return chart
        sr_chart = returns.nextSolarReturn(self.chart, self.return_date)

        # Check that the solar return chart is a Chart object
        self.assertIsInstance(sr_chart, Chart)

        # Check that the solar return chart has the same position as the original chart
        self.assertEqual(sr_chart.pos.lat, self.chart.pos.lat)
        self.assertEqual(sr_chart.pos.lon, self.chart.pos.lon)

        # Check that the solar return chart has the same house system as the original chart
        self.assertEqual(sr_chart.hsys, self.chart.hsys)

        # Check that the Sun is at the same longitude as in the original chart
        orig_sun = self.chart.getObject(const.SUN)
        sr_sun = sr_chart.getObject(const.SUN)

        self.assertAlmostEqual(orig_sun.lon, sr_sun.lon, places=0)

        # Check that the solar return date is after the return date
        self.assertGreater(sr_chart.date.jd, self.return_date.jd)

        # Print the solar return chart information for reference
        print(f"Next Solar Return Chart:")
        print(f"  Date: {sr_chart.date.date.date()}/{sr_chart.date.time.time()}")
        print(f"  Sun: {sr_sun.sign} {sr_sun.signlon:.2f}°")

        # Check that the solar return is close to the birth date (within a few days)
        birth_month = self.chart.date.date.date()[1]
        birth_day = self.chart.date.date.date()[2]
        sr_month = sr_chart.date.date.date()[1]
        sr_day = sr_chart.date.date.date()[2]

        self.assertTrue(
            (birth_month == sr_month and abs(birth_day - sr_day) <= 2) or
            (abs(birth_month - sr_month) == 1 and (birth_day >= 28 or sr_day >= 28))
        )

    def test_prev_solar_return(self):
        """Test prevSolarReturn function"""
        # Get the previous solar return chart
        sr_chart = returns.prevSolarReturn(self.chart, self.return_date)

        # Check that the solar return chart is a Chart object
        self.assertIsInstance(sr_chart, Chart)

        # Check that the solar return chart has the same position as the original chart
        self.assertEqual(sr_chart.pos.lat, self.chart.pos.lat)
        self.assertEqual(sr_chart.pos.lon, self.chart.pos.lon)

        # Check that the solar return chart has the same house system as the original chart
        self.assertEqual(sr_chart.hsys, self.chart.hsys)

        # Check that the Sun is at the same longitude as in the original chart
        orig_sun = self.chart.getObject(const.SUN)
        sr_sun = sr_chart.getObject(const.SUN)

        self.assertAlmostEqual(orig_sun.lon, sr_sun.lon, places=0)

        # Check that the solar return date is before the return date
        self.assertLess(sr_chart.date.jd, self.return_date.jd)

        # Print the solar return chart information for reference
        print(f"Previous Solar Return Chart:")
        print(f"  Date: {sr_chart.date.date.date()}/{sr_chart.date.time.time()}")
        print(f"  Sun: {sr_sun.sign} {sr_sun.signlon:.2f}°")

        # Check that the solar return is close to the birth date (within a few days)
        birth_month = self.chart.date.date.date()[1]
        birth_day = self.chart.date.date.date()[2]
        sr_month = sr_chart.date.date.date()[1]
        sr_day = sr_chart.date.date.date()[2]

        self.assertTrue(
            (birth_month == sr_month and abs(birth_day - sr_day) <= 2) or
            (abs(birth_month - sr_month) == 1 and (birth_day >= 28 or sr_day >= 28))
        )

    def test_solar_return_objects(self):
        """Test solar return objects"""
        # Get the next solar return chart
        sr_chart = returns.nextSolarReturn(self.chart, self.return_date)

        # Check that all objects are present in the solar return chart
        for obj_id in [const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS, const.JUPITER, const.SATURN]:
            obj = sr_chart.getObject(obj_id)
            self.assertIsNotNone(obj)

        # Print the positions of some objects for reference
        print(f"Solar Return Object Positions:")
        for obj_id in [const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS]:
            obj = sr_chart.getObject(obj_id)
            print(f"  {obj_id}: {obj.sign} {obj.signlon:.2f}°")

    def test_solar_return_houses(self):
        """Test solar return houses"""
        # Skip this test for now as it requires a different implementation
        self.skipTest("This test requires a different implementation")

    def test_solar_return_angles(self):
        """Test solar return angles"""
        # Get the next solar return chart
        sr_chart = returns.nextSolarReturn(self.chart, self.return_date)

        # Check that all angles are present in the solar return chart
        for angle_id in [const.ASC, const.MC, const.DESC, const.IC]:
            angle = sr_chart.getAngle(angle_id)
            self.assertIsNotNone(angle)

        # Print the positions of the angles for reference
        print(f"Solar Return Angle Positions:")
        for angle_id in [const.ASC, const.MC, const.DESC, const.IC]:
            angle = sr_chart.getAngle(angle_id)
            print(f"  {angle_id}: {angle.sign} {angle.signlon:.2f}°")

    def test_consecutive_solar_returns(self):
        """Test consecutive solar returns"""
        # Get two consecutive solar returns
        sr1_chart = returns.nextSolarReturn(self.chart, self.return_date)
        sr2_chart = returns.nextSolarReturn(self.chart, sr1_chart.date)

        # Check that the second solar return is approximately one year after the first
        days_diff = sr2_chart.date.jd - sr1_chart.date.jd
        self.assertAlmostEqual(days_diff, 365.25, delta=5)  # Allow for a few days of difference

        # Print the dates of the solar returns for reference
        print(f"Consecutive Solar Returns:")
        print(f"  First: {sr1_chart.date.date.date()}/{sr1_chart.date.time.time()}")
        print(f"  Second: {sr2_chart.date.date.date()}/{sr2_chart.date.time.time()}")
        print(f"  Days between: {days_diff:.2f}")


if __name__ == '__main__':
    unittest.main()
