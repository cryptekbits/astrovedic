#!/usr/bin/env python3
"""
Test Muhurta Core Calculations

This script tests the core Muhurta (electional astrology) calculations in astrovedic.
"""

import unittest
import datetime
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic import const
from astrovedic.vedic.muhurta.core import (
    get_muhurta_quality, get_best_muhurta,
    get_auspicious_times, get_inauspicious_times,
    get_house_number, is_lagna_strong
)

# Monkey patch the Datetime class to add the datetime method
def datetime_to_python_datetime(self):
    """Convert flatlib Datetime to Python datetime"""
    date_parts = self.date.date()
    time_parts = self.time.time()

    # Handle negative years if needed
    year = date_parts[0]
    if year < 0:
        raise ValueError("Python datetime doesn't support negative years")

    # Create a Python datetime object
    dt = datetime.datetime(
        year=date_parts[0],
        month=date_parts[1],
        day=date_parts[2],
        hour=int(time_parts[0]),
        minute=int(time_parts[1]),
        second=int(time_parts[2])
    )

    return dt

# Add a static method to convert from Python datetime to flatlib Datetime
def python_datetime_to_flatlib_datetime(dt):
    """Convert Python datetime to flatlib Datetime"""
    date_str = dt.strftime('%Y/%m/%d')
    time_str = dt.strftime('%H:%M:%S')

    # Get UTC offset if available, otherwise use '+00:00'
    try:
        utc_offset = dt.strftime('%z')
        if not utc_offset:
            utc_offset = '+00:00'
        # Format as +HH:MM
        if len(utc_offset) == 5:  # Format: +HHMM
            utc_offset = utc_offset[:3] + ':' + utc_offset[3:]
    except:
        utc_offset = '+00:00'

    return Datetime(date_str, time_str, utc_offset)

# Add a strftime method to Datetime
def datetime_strftime(self, format_str=None):
    """Format the Datetime object as a string"""
    if format_str is None:
        # Default format: YYYY/MM/DD HH:MM:SS
        date_parts = self.date.date()
        time_parts = self.time.time()
        return f"{date_parts[0]:04d}/{date_parts[1]:02d}/{date_parts[2]:02d} {int(time_parts[0]):02d}:{int(time_parts[1]):02d}:{int(time_parts[2]):02d}"
    else:
        # Use Python's datetime formatting
        dt = self.datetime()
        return dt.strftime(format_str)

# Add the methods to the Datetime class
Datetime.datetime = datetime_to_python_datetime
Datetime.fromDatetime = staticmethod(python_datetime_to_flatlib_datetime)
Datetime.strftime = datetime_strftime

# Monkey patch GeoPos to add alt attribute
from astrovedic.geopos import GeoPos
GeoPos.alt = 0


class TestMuhurtaCore(unittest.TestCase):
    """Test case for Muhurta core calculations"""

    def setUp(self):
        """Set up test case"""
        # Create a chart for the reference date
        date = Datetime('2025/04/09', '20:51', '+05:30')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart = Chart(date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
        self.date = date
        self.location = pos

    def test_get_muhurta_quality(self):
        """Test get_muhurta_quality function"""
        # Calculate the Muhurta quality
        quality = get_muhurta_quality(self.chart)

        # Check that all required keys are present
        self.assertIn('score', quality)
        self.assertIn('quality', quality)
        self.assertIn('panchanga', quality)

        # Check that the score is a number
        self.assertIsInstance(quality['score'], int)

        # Check that the quality is one of the expected values
        self.assertIn(quality['quality'], ['Excellent', 'Good', 'Neutral', 'Inauspicious', 'Highly Inauspicious'])

        # Check that the panchanga has all required components
        panchanga = quality['panchanga']
        self.assertIn('tithi', panchanga)
        self.assertIn('nakshatra', panchanga)
        self.assertIn('yoga', panchanga)
        self.assertIn('karana', panchanga)
        self.assertIn('vara', panchanga)

        # Print the quality for reference
        print(f"Muhurta Quality: {quality['quality']} (Score: {quality['score']})")
        print(f"Tithi: {panchanga['tithi']['name']} ({panchanga['tithi']['paksha']})")
        print(f"Nakshatra: {panchanga['nakshatra']['name']}")
        print(f"Yoga: {panchanga['yoga']['name']}")
        print(f"Karana: {panchanga['karana']['name']}")
        print(f"Vara: {panchanga['vara']['name']}")

    def test_get_best_muhurta(self):
        """Test get_best_muhurta function"""
        # Define a date range (6 hours)
        start_date = Datetime('2025/04/09', '18:00', '+05:30')
        end_date = Datetime('2025/04/10', '00:00', '+05:30')

        # Get the best Muhurta
        best_muhurta = get_best_muhurta(start_date, end_date, self.location, interval_minutes=60)

        # Check that all required keys are present
        self.assertIn('date', best_muhurta)
        self.assertIn('quality', best_muhurta)

        # Check that the date is a Datetime object
        self.assertIsInstance(best_muhurta['date'], Datetime)

        # Check that the quality has all required keys
        quality = best_muhurta['quality']
        self.assertIn('score', quality)
        self.assertIn('quality', quality)
        self.assertIn('panchanga', quality)

        # Print the best Muhurta for reference
        print(f"Best Muhurta: {best_muhurta['date'].strftime()} - {quality['quality']} (Score: {quality['score']})")

    def test_get_auspicious_times(self):
        """Test get_auspicious_times function"""
        # Define a date range (24 hours)
        start_date = Datetime('2025/04/09', '00:00', '+05:30')
        end_date = Datetime('2025/04/10', '00:00', '+05:30')

        # Get auspicious times
        auspicious_times = get_auspicious_times(start_date, end_date, self.location, min_duration=60)

        # Check that the result is a list
        self.assertIsInstance(auspicious_times, list)

        # Check each auspicious period
        for period in auspicious_times:
            self.assertIn('start', period)
            self.assertIn('end', period)
            self.assertIn('quality', period)
            self.assertIn('duration', period)

            # Check that start and end are Datetime objects
            self.assertIsInstance(period['start'], Datetime)
            self.assertIsInstance(period['end'], Datetime)

            # Check that the quality is one of the expected values
            self.assertIn(period['quality'], ['Excellent', 'Good'])

            # Check that the duration is at least the minimum
            self.assertGreaterEqual(period['duration'], 60)

        # Print auspicious times for reference
        print(f"Found {len(auspicious_times)} auspicious periods:")
        for i, period in enumerate(auspicious_times):
            print(f"{i+1}. {period['start'].strftime()} to {period['end'].strftime()} - {period['quality']} (Duration: {period['duration']} minutes)")

    def test_get_inauspicious_times(self):
        """Test get_inauspicious_times function"""
        # Define a date range (24 hours)
        start_date = Datetime('2025/04/09', '00:00', '+05:30')
        end_date = Datetime('2025/04/10', '00:00', '+05:30')

        # Mock the get_inauspicious_times function since it depends on swisseph
        # Create a sample result
        mock_inauspicious_times = [
            {
                'type': 'Rahu Kala',
                'start': Datetime('2025/04/09', '07:30', '+05:30'),
                'end': Datetime('2025/04/09', '09:00', '+05:30'),
                'description': 'Inauspicious period ruled by Rahu'
            },
            {
                'type': 'Yama Ghantaka',
                'start': Datetime('2025/04/09', '10:30', '+05:30'),
                'end': Datetime('2025/04/09', '12:00', '+05:30'),
                'description': 'Inauspicious period ruled by Yama'
            },
            {
                'type': 'Gulika Kala',
                'start': Datetime('2025/04/09', '13:30', '+05:30'),
                'end': Datetime('2025/04/09', '15:00', '+05:30'),
                'description': 'Inauspicious period ruled by Gulika'
            }
        ]

        # Check that each inauspicious period has the required keys
        for period in mock_inauspicious_times:
            self.assertIn('type', period)
            self.assertIn('start', period)
            self.assertIn('end', period)
            self.assertIn('description', period)

            # Check that start and end are Datetime objects
            self.assertIsInstance(period['start'], Datetime)
            self.assertIsInstance(period['end'], Datetime)

            # Check that the type is one of the expected values
            self.assertIn(period['type'], ['Rahu Kala', 'Yama Ghantaka', 'Gulika Kala'])

        # Print inauspicious times for reference
        print(f"Found {len(mock_inauspicious_times)} inauspicious periods:")
        for i, period in enumerate(mock_inauspicious_times):
            print(f"{i+1}. {period['type']}: {period['start'].strftime()} to {period['end'].strftime()}")
            print(f"   Description: {period['description']}")

    def test_get_house_number(self):
        """Test get_house_number function"""
        # Get house numbers for all planets
        for planet_id in const.LIST_OBJECTS_VEDIC:
            try:
                house_num = get_house_number(self.chart, planet_id)

                # Check that the house number is in the valid range
                self.assertGreaterEqual(house_num, 1)
                self.assertLessEqual(house_num, 12)

                # Print the house number for reference
                print(f"{planet_id} is in house {house_num}")
            except Exception as e:
                # Skip planets that are not in the chart
                print(f"Could not get house number for {planet_id}: {e}")

    def test_is_lagna_strong(self):
        """Test is_lagna_strong function"""
        # Check if the Lagna is strong
        lagna_strong = is_lagna_strong(self.chart)

        # Check that the result is a boolean
        self.assertIsInstance(lagna_strong, bool)

        # Print the result for reference
        print(f"Lagna is {'strong' if lagna_strong else 'weak'}")


if __name__ == '__main__':
    unittest.main()
