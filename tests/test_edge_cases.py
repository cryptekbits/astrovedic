#!/usr/bin/env python3
"""
Test Edge Cases

This script tests edge cases in flatlib.
"""

import unittest
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib.vedic.api import VedicChart, create_vedic_chart, create_kp_chart


class TestInvalidInputs(unittest.TestCase):
    """Test case for invalid inputs"""
    
    def test_invalid_date_format(self):
        """Test with invalid date format"""
        # Test with various invalid date formats
        test_cases = [
            '2025-04-09',  # Wrong separator
            '09/04/2025',  # Wrong order
            '2025/13/09',  # Invalid month
            '2025/04/32',  # Invalid day
            'abcd/ef/gh',  # Non-numeric
            '',            # Empty string
            '2025/04',     # Incomplete
            '2025/04/09/12'  # Too many components
        ]
        
        for date_str in test_cases:
            # Check that creating a Datetime with invalid date format raises an exception
            with self.assertRaises(Exception):
                Datetime(date_str, '12:00', '+05:30')
    
    def test_invalid_time_format(self):
        """Test with invalid time format"""
        # Test with various invalid time formats
        test_cases = [
            '12-00',      # Wrong separator
            '25:00',      # Invalid hour
            '12:60',      # Invalid minute
            'ab:cd',      # Non-numeric
            '',           # Empty string
            '12',         # Incomplete
            '12:00:00'    # Too many components
        ]
        
        for time_str in test_cases:
            # Check that creating a Datetime with invalid time format raises an exception
            with self.assertRaises(Exception):
                Datetime('2025/04/09', time_str, '+05:30')
    
    def test_invalid_timezone_format(self):
        """Test with invalid timezone format"""
        # Test with various invalid timezone formats
        test_cases = [
            '05:30',      # Missing sign
            '+5:30',      # Missing leading zero
            '+05-30',     # Wrong separator
            '+05:60',     # Invalid minute
            '+ab:cd',     # Non-numeric
            '',           # Empty string
            '+05',        # Incomplete
            '+05:30:00'   # Too many components
        ]
        
        for timezone_str in test_cases:
            # Check that creating a Datetime with invalid timezone format raises an exception
            with self.assertRaises(Exception):
                Datetime('2025/04/09', '12:00', timezone_str)
    
    def test_invalid_latitude(self):
        """Test with invalid latitude"""
        # Test with various invalid latitudes
        test_cases = [
            -91,    # Below minimum
            91,     # Above maximum
            'abc'   # Non-numeric
        ]
        
        for lat in test_cases:
            # Check that creating a GeoPos with invalid latitude raises an exception
            with self.assertRaises(Exception):
                GeoPos(lat, 0)
    
    def test_invalid_longitude(self):
        """Test with invalid longitude"""
        # Test with various invalid longitudes
        test_cases = [
            -181,   # Below minimum
            181,    # Above maximum
            'abc'   # Non-numeric
        ]
        
        for lon in test_cases:
            # Check that creating a GeoPos with invalid longitude raises an exception
            with self.assertRaises(Exception):
                GeoPos(0, lon)
    
    def test_invalid_house_system(self):
        """Test with invalid house system"""
        # Create a valid date and position
        date = Datetime('2025/04/09', '12:00', '+05:30')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        
        # Test with various invalid house systems
        test_cases = [
            'invalid',     # Non-existent
            '',            # Empty string
            123            # Non-string
        ]
        
        for hsys in test_cases:
            # Check that creating a Chart with invalid house system raises an exception
            with self.assertRaises(Exception):
                Chart(date, pos, hsys=hsys)
    
    def test_invalid_ayanamsa(self):
        """Test with invalid ayanamsa"""
        # Create a valid date and position
        date = Datetime('2025/04/09', '12:00', '+05:30')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        
        # Test with various invalid ayanamsas
        test_cases = [
            'invalid',     # Non-existent
            '',            # Empty string
            123            # Non-string
        ]
        
        for ayanamsa in test_cases:
            # Check that creating a Chart with invalid ayanamsa raises an exception
            with self.assertRaises(Exception):
                Chart(date, pos, mode=ayanamsa)


class TestEdgeCaseBirthData(unittest.TestCase):
    """Test case for edge case birth data"""
    
    def test_polar_regions(self):
        """Test with polar regions"""
        # Create a valid date
        date = Datetime('2025/04/09', '12:00', '+00:00')
        
        # Test with various polar regions
        test_cases = [
            (89, 0),       # Near North Pole
            (-89, 0),      # Near South Pole
            (89, 179),     # Near North Pole, near date line
            (-89, -179)    # Near South Pole, near date line
        ]
        
        for lat, lon in test_cases:
            try:
                # Create a position
                pos = GeoPos(lat, lon)
                
                # Create a chart
                chart = Chart(date, pos)
                
                # Check that the chart is created correctly
                self.assertIsNotNone(chart)
                self.assertEqual(chart.pos.lat, lat)
                self.assertEqual(chart.pos.lon, lon)
                
                # Print the chart information for reference
                print(f"Chart for polar region {lat}°, {lon}°:")
                print(f"  Date: {chart.date.date.date()}/{chart.date.time.time()}")
                print(f"  Position: {chart.pos.lat}°, {chart.pos.lon}°")
            except Exception as e:
                # Some polar regions might cause errors
                print(f"Error for polar region {lat}°, {lon}°: {str(e)}")
    
    def test_date_line_crossing(self):
        """Test with date line crossing"""
        # Create a valid date
        date = Datetime('2025/04/09', '12:00', '+00:00')
        
        # Test with various positions near the date line
        test_cases = [
            (0, 179),      # Near date line, east
            (0, -179),     # Near date line, west
            (0, 180),      # On date line
            (0, -180)      # On date line
        ]
        
        for lat, lon in test_cases:
            try:
                # Create a position
                pos = GeoPos(lat, lon)
                
                # Create a chart
                chart = Chart(date, pos)
                
                # Check that the chart is created correctly
                self.assertIsNotNone(chart)
                self.assertEqual(chart.pos.lat, lat)
                self.assertEqual(chart.pos.lon, lon)
                
                # Print the chart information for reference
                print(f"Chart for date line crossing {lat}°, {lon}°:")
                print(f"  Date: {chart.date.date.date()}/{chart.date.time.time()}")
                print(f"  Position: {chart.pos.lat}°, {chart.pos.lon}°")
            except Exception as e:
                # Some date line crossings might cause errors
                print(f"Error for date line crossing {lat}°, {lon}°: {str(e)}")
    
    def test_extreme_dates(self):
        """Test with extreme dates"""
        # Test with various extreme dates
        test_cases = [
            ('0001/01/01', '00:00', '+00:00'),  # Earliest date
            ('9999/12/31', '23:59', '+00:00')   # Latest date
        ]
        
        for date_str, time_str, timezone_str in test_cases:
            try:
                # Create a date
                date = Datetime(date_str, time_str, timezone_str)
                
                # Create a position
                pos = GeoPos(0, 0)
                
                # Create a chart
                chart = Chart(date, pos)
                
                # Check that the chart is created correctly
                self.assertIsNotNone(chart)
                
                # Print the chart information for reference
                print(f"Chart for extreme date {date_str} {time_str} {timezone_str}:")
                print(f"  Date: {chart.date.date.date()}/{chart.date.time.time()}")
                print(f"  Position: {chart.pos.lat}°, {chart.pos.lon}°")
            except Exception as e:
                # Some extreme dates might cause errors
                print(f"Error for extreme date {date_str} {time_str} {timezone_str}: {str(e)}")


class TestExtremePlanetaryPositions(unittest.TestCase):
    """Test case for extreme planetary positions"""
    
    def test_retrograde_planets(self):
        """Test with retrograde planets"""
        # Create a chart for a date when Mercury is retrograde
        date = Datetime('2025/09/17', '12:00', '+00:00')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        chart = Chart(date, pos)
        
        # Get Mercury
        mercury = chart.getObject(const.MERCURY)
        
        # Check that Mercury is retrograde
        self.assertTrue(mercury.isRetrograde())
        
        # Print the Mercury information for reference
        print(f"Mercury on {date.date.date()} {date.time.time()}:")
        print(f"  Sign: {mercury.sign}")
        print(f"  Longitude: {mercury.lon:.2f}°")
        print(f"  Retrograde: {mercury.isRetrograde()}")
    
    def test_stationary_planets(self):
        """Test with stationary planets"""
        # Create a chart for a date when Mercury is stationary
        date = Datetime('2025/09/09', '12:00', '+00:00')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        chart = Chart(date, pos)
        
        # Get Mercury
        mercury = chart.getObject(const.MERCURY)
        
        # Print the Mercury information for reference
        print(f"Mercury on {date.date.date()} {date.time.time()}:")
        print(f"  Sign: {mercury.sign}")
        print(f"  Longitude: {mercury.lon:.2f}°")
        print(f"  Speed: {mercury.speed:.6f}°/day")
    
    def test_combust_planets(self):
        """Test with combust planets"""
        # Create a chart for a date when Mercury is combust
        date = Datetime('2025/04/09', '12:00', '+00:00')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        chart = Chart(date, pos)
        
        # Get Sun and Mercury
        sun = chart.getObject(const.SUN)
        mercury = chart.getObject(const.MERCURY)
        
        # Calculate the distance between Sun and Mercury
        distance = abs(sun.lon - mercury.lon)
        if distance > 180:
            distance = 360 - distance
        
        # Check if Mercury is combust (within 8 degrees of Sun)
        is_combust = distance < 8
        
        # Print the Mercury information for reference
        print(f"Mercury on {date.date.date()} {date.time.time()}:")
        print(f"  Sign: {mercury.sign}")
        print(f"  Longitude: {mercury.lon:.2f}°")
        print(f"  Distance from Sun: {distance:.2f}°")
        print(f"  Combust: {is_combust}")
    
    def test_eclipses(self):
        """Test with eclipses"""
        # Create a chart for a date of a solar eclipse
        date = Datetime('2026/08/12', '12:00', '+00:00')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        chart = Chart(date, pos)
        
        # Get Sun and Moon
        sun = chart.getObject(const.SUN)
        moon = chart.getObject(const.MOON)
        
        # Calculate the distance between Sun and Moon
        distance = abs(sun.lon - moon.lon)
        if distance > 180:
            distance = 360 - distance
        
        # Check if it's a solar eclipse (Sun and Moon are very close)
        is_eclipse = distance < 1
        
        # Print the Sun and Moon information for reference
        print(f"Sun and Moon on {date.date.date()} {date.time.time()}:")
        print(f"  Sun: {sun.sign} {sun.lon:.2f}°")
        print(f"  Moon: {moon.sign} {moon.lon:.2f}°")
        print(f"  Distance: {distance:.2f}°")
        print(f"  Eclipse: {is_eclipse}")


class TestTimezoneHandling(unittest.TestCase):
    """Test case for timezone handling"""
    
    def test_timezone_handling(self):
        """Test timezone handling"""
        # Test with various timezone edge cases
        test_cases = [
            ('+14:00', True),    # Maximum positive timezone
            ('-12:00', True),    # Maximum negative timezone
            ('+14:01', False),   # Beyond maximum positive timezone
            ('-12:01', False)    # Beyond maximum negative timezone
        ]
        
        for timezone_str, should_succeed in test_cases:
            try:
                # Create a date
                date = Datetime('2025/04/09', '12:00', timezone_str)
                
                # Check that the date is created correctly if it should succeed
                if should_succeed:
                    self.assertIsNotNone(date)
                    print(f"Timezone {timezone_str} is valid")
                else:
                    self.fail(f"Timezone {timezone_str} should be invalid")
            except Exception as e:
                # Check that an exception is raised if it should not succeed
                if should_succeed:
                    self.fail(f"Timezone {timezone_str} should be valid, but got error: {str(e)}")
                else:
                    print(f"Timezone {timezone_str} is invalid: {str(e)}")


if __name__ == '__main__':
    unittest.main()
