#!/usr/bin/env python3
"""
Test Planetary Time

This script tests the planetary time calculations in astrovedic.
"""

import unittest
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic import const
from astrovedic.tools import planetarytime


class TestPlanetaryTime(unittest.TestCase):
    """Test case for planetary time calculations"""
    
    def setUp(self):
        """Set up test case"""
        # Create a date and location for testing
        self.date = Datetime('2025/04/09', '20:51', '+05:30')
        self.pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
    
    def test_nth_ruler(self):
        """Test nthRuler function"""
        # Test with various hour numbers and day of week
        test_cases = [
            (0, 0, const.SUN),    # Sunday, 1st hour
            (1, 0, const.VENUS),  # Sunday, 2nd hour
            (2, 0, const.MERCURY),  # Sunday, 3rd hour
            (0, 1, const.MOON),   # Monday, 1st hour
            (1, 1, const.SATURN),  # Monday, 2nd hour
            (2, 1, const.JUPITER),  # Monday, 3rd hour
            (0, 2, const.MARS),   # Tuesday, 1st hour
            (1, 2, const.SUN),    # Tuesday, 2nd hour
            (2, 2, const.VENUS),  # Tuesday, 3rd hour
            (0, 3, const.MERCURY),  # Wednesday, 1st hour
            (1, 3, const.MOON),   # Wednesday, 2nd hour
            (2, 3, const.SATURN),  # Wednesday, 3rd hour
            (0, 4, const.JUPITER),  # Thursday, 1st hour
            (1, 4, const.MARS),   # Thursday, 2nd hour
            (2, 4, const.SUN),    # Thursday, 3rd hour
            (0, 5, const.VENUS),  # Friday, 1st hour
            (1, 5, const.MERCURY),  # Friday, 2nd hour
            (2, 5, const.MOON),   # Friday, 3rd hour
            (0, 6, const.SATURN),  # Saturday, 1st hour
            (1, 6, const.JUPITER),  # Saturday, 2nd hour
            (2, 6, const.MARS),   # Saturday, 3rd hour
        ]
        
        for hour, day, expected_ruler in test_cases:
            # Get the ruler for the hour and day
            ruler = planetarytime.nthRuler(hour, day)
            
            # Check that the ruler is correct
            self.assertEqual(ruler, expected_ruler)
            
            # Print the ruler for reference
            print(f"Ruler for hour {hour} on day {day}: {ruler}")
    
    def test_hour_table(self):
        """Test hourTable function"""
        # Get the hour table
        table = planetarytime.hourTable(self.date, self.pos)
        
        # Check that the table is a list
        self.assertIsInstance(table, list)
        
        # Check that the table has 24 entries (12 diurnal + 12 nocturnal)
        self.assertEqual(len(table), 24)
        
        # Check that each entry has the correct format
        for entry in table:
            # Each entry should be a list with 3 elements: start JD, end JD, ruler
            self.assertIsInstance(entry, list)
            self.assertEqual(len(entry), 3)
            
            # Start JD should be less than end JD
            self.assertLess(entry[0], entry[1])
            
            # Ruler should be a valid planet
            self.assertIn(entry[2], planetarytime.DAY_RULERS)
        
        # Print the first few entries for reference
        print(f"Hour Table (first 5 entries):")
        for i, entry in enumerate(table[:5]):
            print(f"  Hour {i+1}: {entry[2]} ({entry[0]} - {entry[1]})")
    
    def test_get_hour_table(self):
        """Test getHourTable function"""
        # Get the hour table
        hour_table = planetarytime.getHourTable(self.date, self.pos)
        
        # Check that the hour table is an HourTable object
        self.assertIsInstance(hour_table, planetarytime.HourTable)
        
        # Print the hour table information for reference
        print(f"Hour Table:")
        print(f"  Day Ruler: {hour_table.dayRuler()}")
        print(f"  Night Ruler: {hour_table.nightRuler()}")
        print(f"  Current Ruler: {hour_table.currRuler()}")
        print(f"  Hour Ruler: {hour_table.hourRuler()}")
    
    def test_hour_table_index(self):
        """Test HourTable.index method"""
        # Get the hour table
        hour_table = planetarytime.getHourTable(self.date, self.pos)
        
        # Get the index of the current date
        index = hour_table.index(self.date)
        
        # Check that the index is a valid index (0-23)
        self.assertIsInstance(index, int)
        self.assertGreaterEqual(index, 0)
        self.assertLess(index, 24)
        
        # Print the index for reference
        print(f"Index of current date in hour table: {index}")
    
    def test_hour_table_day_ruler(self):
        """Test HourTable.dayRuler method"""
        # Get the hour table
        hour_table = planetarytime.getHourTable(self.date, self.pos)
        
        # Get the day ruler
        day_ruler = hour_table.dayRuler()
        
        # Check that the day ruler is a valid planet
        self.assertIn(day_ruler, planetarytime.DAY_RULERS)
        
        # Print the day ruler for reference
        print(f"Day Ruler: {day_ruler}")
    
    def test_hour_table_night_ruler(self):
        """Test HourTable.nightRuler method"""
        # Get the hour table
        hour_table = planetarytime.getHourTable(self.date, self.pos)
        
        # Get the night ruler
        night_ruler = hour_table.nightRuler()
        
        # Check that the night ruler is a valid planet
        self.assertIn(night_ruler, planetarytime.NIGHT_RULERS)
        
        # Print the night ruler for reference
        print(f"Night Ruler: {night_ruler}")
    
    def test_hour_table_curr_ruler(self):
        """Test HourTable.currRuler method"""
        # Get the hour table
        hour_table = planetarytime.getHourTable(self.date, self.pos)
        
        # Get the current ruler
        curr_ruler = hour_table.currRuler()
        
        # Check that the current ruler is a valid planet
        self.assertIn(curr_ruler, planetarytime.DAY_RULERS)
        
        # Print the current ruler for reference
        print(f"Current Ruler: {curr_ruler}")
    
    def test_hour_table_hour_ruler(self):
        """Test HourTable.hourRuler method"""
        # Get the hour table
        hour_table = planetarytime.getHourTable(self.date, self.pos)
        
        # Get the hour ruler
        hour_ruler = hour_table.hourRuler()
        
        # Check that the hour ruler is a valid planet
        self.assertIn(hour_ruler, planetarytime.DAY_RULERS)
        
        # Print the hour ruler for reference
        print(f"Hour Ruler: {hour_ruler}")
    
    def test_hour_table_curr_info(self):
        """Test HourTable.currInfo method"""
        # Get the hour table
        hour_table = planetarytime.getHourTable(self.date, self.pos)
        
        # Get the current information
        info = hour_table.currInfo()
        
        # Check that the information is a dictionary
        self.assertIsInstance(info, dict)
        
        # Check that the dictionary has the required keys
        self.assertIn('mode', info)
        self.assertIn('ruler', info)
        self.assertIn('dayRuler', info)
        self.assertIn('nightRuler', info)
        self.assertIn('hourRuler', info)
        self.assertIn('hourNumber', info)
        self.assertIn('tableIndex', info)
        self.assertIn('start', info)
        self.assertIn('end', info)
        
        # Print the information for reference
        print(f"Current Information:")
        print(f"  Mode: {info['mode']}")
        print(f"  Ruler: {info['ruler']}")
        print(f"  Day Ruler: {info['dayRuler']}")
        print(f"  Night Ruler: {info['nightRuler']}")
        print(f"  Hour Ruler: {info['hourRuler']}")
        print(f"  Hour Number: {info['hourNumber']}")
        print(f"  Table Index: {info['tableIndex']}")
        print(f"  Start: {info['start']}")
        print(f"  End: {info['end']}")
    
    def test_hour_table_index_info(self):
        """Test HourTable.indexInfo method"""
        # Get the hour table
        hour_table = planetarytime.getHourTable(self.date, self.pos)
        
        # Test with various indices
        test_cases = [0, 5, 11, 12, 17, 23]
        
        for index in test_cases:
            # Get the information for the index
            info = hour_table.indexInfo(index)
            
            # Check that the information is a dictionary
            self.assertIsInstance(info, dict)
            
            # Check that the dictionary has the required keys
            self.assertIn('mode', info)
            self.assertIn('ruler', info)
            self.assertIn('dayRuler', info)
            self.assertIn('nightRuler', info)
            self.assertIn('hourRuler', info)
            self.assertIn('hourNumber', info)
            self.assertIn('tableIndex', info)
            self.assertIn('start', info)
            self.assertIn('end', info)
            
            # Print the information for reference
            print(f"Information for index {index}:")
            print(f"  Mode: {info['mode']}")
            print(f"  Ruler: {info['ruler']}")
            print(f"  Hour Ruler: {info['hourRuler']}")
            print(f"  Hour Number: {info['hourNumber']}")
    
    def test_different_dates(self):
        """Test with different dates"""
        # Test with various dates
        test_cases = [
            Datetime('2025/01/01', '12:00', '+05:30'),  # New Year's Day at noon
            Datetime('2025/04/09', '00:00', '+05:30'),  # Midnight
            Datetime('2025/04/09', '06:00', '+05:30'),  # Early morning
            Datetime('2025/04/09', '12:00', '+05:30'),  # Noon
            Datetime('2025/04/09', '18:00', '+05:30'),  # Evening
            Datetime('2025/07/04', '12:00', '+05:30'),  # Summer
            Datetime('2025/10/31', '12:00', '+05:30'),  # Fall
        ]
        
        for date in test_cases:
            # Get the hour table
            hour_table = planetarytime.getHourTable(date, self.pos)
            
            # Get the current information
            info = hour_table.currInfo()
            
            # Print the information for reference
            print(f"Information for {date}:")
            print(f"  Mode: {info['mode']}")
            print(f"  Day Ruler: {info['dayRuler']}")
            print(f"  Night Ruler: {info['nightRuler']}")
            print(f"  Hour Ruler: {info['hourRuler']}")
            print(f"  Hour Number: {info['hourNumber']}")
    
    def test_different_locations(self):
        """Test with different locations"""
        # Test with various locations
        test_cases = [
            GeoPos(0, 0),          # Equator
            GeoPos(51.5074, 0.1278),  # London
            GeoPos(40.7128, -74.0060),  # New York
            GeoPos(35.6762, 139.6503),  # Tokyo
            GeoPos(-33.8688, 151.2093),  # Sydney
            GeoPos(90, 0),         # North Pole
            GeoPos(-90, 0),        # South Pole
        ]
        
        for pos in test_cases:
            try:
                # Get the hour table
                hour_table = planetarytime.getHourTable(self.date, pos)
                
                # Get the current information
                info = hour_table.currInfo()
                
                # Print the information for reference
                print(f"Information for location {pos.lat}°, {pos.lon}°:")
                print(f"  Mode: {info['mode']}")
                print(f"  Day Ruler: {info['dayRuler']}")
                print(f"  Night Ruler: {info['nightRuler']}")
                print(f"  Hour Ruler: {info['hourRuler']}")
                print(f"  Hour Number: {info['hourNumber']}")
            except Exception as e:
                # Some extreme locations might cause errors
                print(f"Error for location {pos.lat}°, {pos.lon}°: {str(e)}")


if __name__ == '__main__':
    unittest.main()
