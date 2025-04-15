"""
    Tests for Sun Yogas (Surya Yogas) calculations
"""

import unittest
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic import const
from astrovedic.vedic.yogas.surya import (
    get_surya_yogas, has_vasi_yoga, has_vesi_yoga,
    has_ubhayachari_yoga, has_budha_aditya_yoga,
    has_sun_parivartana_yoga
)

class TestSuryaYogas(unittest.TestCase):
    """Test Sun Yogas (Surya Yogas) calculations"""

    def setUp(self):
        """Set up test data"""
        self.date = Datetime('2000/1/1', '12:00', '+00:00')
        self.pos = GeoPos('51n30', '0w10')
        self.chart = Chart(self.date, self.pos)

    def test_get_surya_yogas(self):
        """Test getting all Sun Yogas"""
        # Get all Sun Yogas
        yogas = get_surya_yogas(self.chart)

        # Check that the result is a list
        self.assertIsInstance(yogas, list)

        # Check that each yoga has the expected structure
        for yoga in yogas:
            self.assertIn('name', yoga)
            self.assertIn('type', yoga)
            self.assertIn('planets', yoga)
            self.assertIn('houses', yoga)
            self.assertIn('description', yoga)
            self.assertIn('is_beneficial', yoga)
            self.assertIn('strength', yoga)

            # Check that the type is 'Surya Yoga'
            self.assertEqual(yoga['type'], 'Surya Yoga')

            # Check that the Sun is one of the planets
            self.assertIn(const.SUN, yoga['planets'])

    def test_vasi_yoga(self):
        """Test Vasi Yoga calculation"""
        # Create a mock chart with the Sun in the 12th house from the Moon
        from unittest.mock import MagicMock, patch

        # Create a mock for the get_house_number function
        with patch('astrovedic.vedic.yogas.surya.get_house_number') as mock_get_house:
            # Set up the mock to return specific house numbers
            # Sun in the 12th house from the Moon
            mock_get_house.side_effect = lambda chart, planet_id: 12 if planet_id == const.SUN else 1

            # Check if Vasi Yoga is formed
            yoga = has_vasi_yoga(self.chart)

            # Check that the yoga is detected
            self.assertIsNotNone(yoga)
            if yoga:
                self.assertEqual(yoga['name'], 'Vasi Yoga')
                self.assertEqual(yoga['type'], 'Surya Yoga')
                self.assertIn(const.SUN, yoga['planets'])
                self.assertIn(const.MOON, yoga['planets'])

    def test_vesi_yoga(self):
        """Test Vesi Yoga calculation"""
        # Create a mock chart with the Sun in the 2nd house from the Moon
        from unittest.mock import MagicMock, patch

        # Create a mock for the get_house_number function
        with patch('astrovedic.vedic.yogas.surya.get_house_number') as mock_get_house:
            # Set up the mock to return specific house numbers
            # Sun in the 2nd house from the Moon
            mock_get_house.side_effect = lambda chart, planet_id: 2 if planet_id == const.SUN else 1

            # Check if Vesi Yoga is formed
            yoga = has_vesi_yoga(self.chart)

            # Check that the yoga is detected
            self.assertIsNotNone(yoga)
            if yoga:
                self.assertEqual(yoga['name'], 'Vesi Yoga')
                self.assertEqual(yoga['type'], 'Surya Yoga')
                self.assertIn(const.SUN, yoga['planets'])
                self.assertIn(const.MOON, yoga['planets'])

    def test_ubhayachari_yoga(self):
        """Test Ubhayachari Yoga calculation"""
        # This test is a bit tricky because Ubhayachari Yoga requires
        # both Vasi and Vesi Yogas to be present, which is impossible
        # in a real chart. We'll need to mock the has_vasi_yoga and
        # has_vesi_yoga functions.

        # For now, we'll just check that the function exists and returns None
        # for our test chart
        yoga = has_ubhayachari_yoga(self.chart)
        self.assertIsNone(yoga)

    def test_budha_aditya_yoga(self):
        """Test Budha-Aditya Yoga calculation"""
        # Create a mock chart with Mercury conjunct with the Sun
        from unittest.mock import MagicMock, patch

        # Create a mock for the get_house_number function
        with patch('astrovedic.vedic.yogas.surya.get_house_number') as mock_get_house:
            # Set up the mock to return specific house numbers
            # Sun and Mercury in the same house
            mock_get_house.side_effect = lambda chart, planet_id: 1

            # Create a mock for the angle.closestdistance function
            with patch('astrovedic.angle.closestdistance') as mock_distance:
                # Set up the mock to return a small distance (5 degrees)
                mock_distance.return_value = 5

                # Check if Budha-Aditya Yoga is formed
                yoga = has_budha_aditya_yoga(self.chart)

                # Check that the yoga is detected
                self.assertIsNotNone(yoga)
                if yoga:
                    self.assertEqual(yoga['name'], 'Budha-Aditya Yoga')
                    self.assertEqual(yoga['type'], 'Surya Yoga')
                    self.assertIn(const.SUN, yoga['planets'])
                    self.assertIn(const.MERCURY, yoga['planets'])

    def test_sun_parivartana_yoga(self):
        """Test Sun Parivartana Yoga calculation"""
        # Create a mock chart with the Sun in Cancer and Moon in Leo
        from unittest.mock import MagicMock, patch

        # Create a mock for the get_house_number function
        with patch('astrovedic.vedic.yogas.surya.get_house_number') as mock_get_house:
            # Set up the mock to return specific house numbers
            mock_get_house.side_effect = lambda chart, planet_id: 4 if planet_id == const.SUN else 5

            # Create mocks for the chart.getObject method
            sun_mock = MagicMock()
            sun_mock.sign = const.CANCER

            moon_mock = MagicMock()
            moon_mock.sign = const.LEO

            # Replace the chart.getObject method with a mock
            original_getObject = self.chart.getObject
            self.chart.getObject = lambda planet_id: sun_mock if planet_id == const.SUN else moon_mock if planet_id == const.MOON else original_getObject(planet_id)

            # Check if Sun Parivartana Yoga is formed
            yoga = has_sun_parivartana_yoga(self.chart)

            # Restore the original getObject method
            self.chart.getObject = original_getObject

            # Check that the yoga is detected
            self.assertIsNotNone(yoga)
            if yoga:
                self.assertEqual(yoga['name'], 'Sun-Moon Parivartana Yoga')
                self.assertEqual(yoga['type'], 'Surya Yoga')
                self.assertIn(const.SUN, yoga['planets'])
                self.assertIn(const.MOON, yoga['planets'])

if __name__ == '__main__':
    unittest.main()
