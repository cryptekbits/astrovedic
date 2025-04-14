"""
    Tests for Kala Sarpa Dosha (Serpent of Time affliction) calculations
"""

import unittest
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic import const
from astrovedic.vedic.compatibility.dosha.kalasarpa import (
    get_kalasarpa_dosha, check_kalasarpa_dosha_cancellation,
    get_house_position, is_conjunct, is_aspected_by
)

class TestKalasarpaDosha(unittest.TestCase):
    """Test Kala Sarpa Dosha (Serpent of Time affliction) calculations"""
    
    def setUp(self):
        """Set up test data"""
        self.date = Datetime('2000/1/1', '12:00', '+00:00')
        self.pos = GeoPos('51n30', '0w10')
        self.chart = Chart(self.date, self.pos)
    
    def test_get_kalasarpa_dosha(self):
        """Test getting Kala Sarpa Dosha"""
        # Get the Kala Sarpa Dosha
        dosha = get_kalasarpa_dosha(self.chart)
        
        # Check that the result has the expected structure
        self.assertIn('has_dosha', dosha)
        self.assertIn('dosha_type', dosha)
        self.assertIn('all_between_rahu_ketu', dosha)
        self.assertIn('all_between_ketu_rahu', dosha)
        self.assertIn('partial_dosha', dosha)
        self.assertIn('cancellation', dosha)
        
        # Check that the cancellation has the expected structure
        self.assertIn('is_cancelled', dosha['cancellation'])
        self.assertIn('cancellation_factors', dosha['cancellation'])
    
    def test_check_kalasarpa_dosha_cancellation(self):
        """Test checking Kala Sarpa Dosha cancellation"""
        # Check the cancellation
        cancellation = check_kalasarpa_dosha_cancellation(self.chart)
        
        # Check that the result has the expected structure
        self.assertIn('is_cancelled', cancellation)
        self.assertIn('cancellation_factors', cancellation)
        
        # Check that is_cancelled is a boolean
        self.assertIsInstance(cancellation['is_cancelled'], bool)
        
        # Check that cancellation_factors is a list
        self.assertIsInstance(cancellation['cancellation_factors'], list)
    
    def test_get_house_position(self):
        """Test getting house position"""
        # Get the house position of the Sun
        sun = self.chart.getObject(const.SUN)
        house_position = get_house_position(self.chart, sun.lon)
        
        # Check that the result is a valid house number
        self.assertGreaterEqual(house_position, 1)
        self.assertLessEqual(house_position, 12)
    
    def test_is_conjunct(self):
        """Test checking if two points are conjunct"""
        # Check if two points at the same longitude are conjunct
        self.assertTrue(is_conjunct(0, 0))
        
        # Check if two points within 10 degrees are conjunct
        self.assertTrue(is_conjunct(0, 5))
        self.assertTrue(is_conjunct(0, 355))
        
        # Check if two points more than 10 degrees apart are not conjunct
        self.assertFalse(is_conjunct(0, 15))
        self.assertFalse(is_conjunct(0, 345))
    
    def test_is_aspected_by(self):
        """Test checking if a point is aspected by another point"""
        # Check if a point is aspected by another point at the same longitude
        self.assertTrue(is_aspected_by(self.chart, 0, 0))
        
        # Check if a point is aspected by another point at opposition
        self.assertTrue(is_aspected_by(self.chart, 0, 180))
        
        # Check if a point is aspected by another point at trine
        self.assertTrue(is_aspected_by(self.chart, 0, 120))
        self.assertTrue(is_aspected_by(self.chart, 0, 240))
        
        # Check if a point is aspected by another point at square
        self.assertTrue(is_aspected_by(self.chart, 0, 90))
        self.assertTrue(is_aspected_by(self.chart, 0, 270))
        
        # Check if a point is not aspected by another point at other angles
        self.assertFalse(is_aspected_by(self.chart, 0, 45))
        self.assertFalse(is_aspected_by(self.chart, 0, 135))
    
    def test_kalasarpa_dosha_with_mock_data(self):
        """Test Kala Sarpa Dosha with mock data"""
        # Get Rahu and Ketu
        rahu = self.chart.getObject(const.RAHU)
        ketu = self.chart.getObject(const.KETU)
        
        # Store the original longitudes
        original_rahu_lon = rahu.lon
        original_ketu_lon = ketu.lon
        
        # Set Rahu and Ketu to opposite points
        rahu.lon = 0
        ketu.lon = 180
        
        # Set all planets to be between Rahu and Ketu
        for planet_id in [const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS, const.JUPITER, const.SATURN]:
            planet = self.chart.getObject(planet_id)
            planet.lon = 90  # Halfway between Rahu and Ketu
        
        # Check if Kala Sarpa Dosha is formed
        dosha = get_kalasarpa_dosha(self.chart)
        
        # Restore the original longitudes
        rahu.lon = original_rahu_lon
        ketu.lon = original_ketu_lon
        
        # Check that the dosha is detected
        self.assertTrue(dosha['all_between_rahu_ketu'])
        self.assertFalse(dosha['all_between_ketu_rahu'])
        
        # Check that the dosha type is correct
        self.assertEqual(dosha['dosha_type'], "Full Kala Sarpa Dosha (Rahu to Ketu)")

if __name__ == '__main__':
    unittest.main()
