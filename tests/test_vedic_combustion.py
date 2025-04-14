"""
    Tests for Vedic combustion (Asta) calculations
"""

import unittest
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic import const
from astrovedic.vedic.combustion import (
    is_combust, is_deeply_combust, get_combustion_details,
    get_all_combustion_details, COMBUSTION_ORBS, DEEP_COMBUSTION_ORBS
)

class TestVedicCombustion(unittest.TestCase):
    """Test Vedic combustion (Asta) calculations"""
    
    def setUp(self):
        """Set up test data"""
        self.date = Datetime('2000/1/1', '12:00', '+00:00')
        self.pos = GeoPos('51n30', '0w10')
        self.chart = Chart(self.date, self.pos)
    
    def test_combustion_orbs(self):
        """Test combustion orbs"""
        # Check that all planets have combustion orbs
        for planet_id in [const.MOON, const.MERCURY, const.VENUS, const.MARS,
                         const.JUPITER, const.SATURN, const.RAHU, const.KETU]:
            self.assertIn(planet_id, COMBUSTION_ORBS)
            self.assertIn(planet_id, DEEP_COMBUSTION_ORBS)
    
    def test_is_combust(self):
        """Test is_combust function"""
        # Test for each planet
        for planet_id in [const.MOON, const.MERCURY, const.VENUS, const.MARS,
                         const.JUPITER, const.SATURN, const.RAHU, const.KETU]:
            # Get the result
            result = is_combust(self.chart, planet_id)
            
            # Check that the result is a boolean
            self.assertIsInstance(result, bool)
        
        # Test that the Sun is never combust
        self.assertFalse(is_combust(self.chart, const.SUN))
    
    def test_is_deeply_combust(self):
        """Test is_deeply_combust function"""
        # Test for each planet
        for planet_id in [const.MOON, const.MERCURY, const.VENUS, const.MARS,
                         const.JUPITER, const.SATURN, const.RAHU, const.KETU]:
            # Get the result
            result = is_deeply_combust(self.chart, planet_id)
            
            # Check that the result is a boolean
            self.assertIsInstance(result, bool)
        
        # Test that the Sun is never deeply combust
        self.assertFalse(is_deeply_combust(self.chart, const.SUN))
    
    def test_get_combustion_details(self):
        """Test get_combustion_details function"""
        # Test for each planet
        for planet_id in [const.MOON, const.MERCURY, const.VENUS, const.MARS,
                         const.JUPITER, const.SATURN, const.RAHU, const.KETU]:
            # Get the result
            result = get_combustion_details(self.chart, planet_id)
            
            # Check that the result has the expected structure
            self.assertIn('is_combust', result)
            self.assertIn('is_deeply_combust', result)
            self.assertIn('orb', result)
            self.assertIn('combustion_orb', result)
            self.assertIn('deep_combustion_orb', result)
            self.assertIn('strength_reduction', result)
            
            # Check that the values are of the expected types
            self.assertIsInstance(result['is_combust'], bool)
            self.assertIsInstance(result['is_deeply_combust'], bool)
            self.assertIsInstance(result['orb'], float)
            self.assertIsInstance(result['combustion_orb'], (int, float))
            self.assertIsInstance(result['deep_combustion_orb'], (int, float))
            self.assertIsInstance(result['strength_reduction'], float)
            
            # Check that the strength reduction is in the valid range (0-100)
            self.assertGreaterEqual(result['strength_reduction'], 0)
            self.assertLessEqual(result['strength_reduction'], 100)
        
        # Test that the Sun has no combustion
        sun_result = get_combustion_details(self.chart, const.SUN)
        self.assertFalse(sun_result['is_combust'])
        self.assertFalse(sun_result['is_deeply_combust'])
        self.assertEqual(sun_result['strength_reduction'], 0)
    
    def test_get_all_combustion_details(self):
        """Test get_all_combustion_details function"""
        # Get the result
        result = get_all_combustion_details(self.chart)
        
        # Check that the result has entries for all planets
        for planet_id in [const.MOON, const.MERCURY, const.VENUS, const.MARS,
                         const.JUPITER, const.SATURN, const.RAHU, const.KETU]:
            self.assertIn(planet_id, result)
            
            # Check that each entry has the expected structure
            planet_result = result[planet_id]
            self.assertIn('is_combust', planet_result)
            self.assertIn('is_deeply_combust', planet_result)
            self.assertIn('orb', planet_result)
            self.assertIn('combustion_orb', planet_result)
            self.assertIn('deep_combustion_orb', planet_result)
            self.assertIn('strength_reduction', planet_result)
    
    def test_combustion_logic(self):
        """Test the logic of combustion calculations"""
        # Create a test case where we know a planet is combust
        # For example, place Mercury at the same longitude as the Sun
        sun = self.chart.getObject(const.SUN)
        mercury = self.chart.getObject(const.MERCURY)
        
        # Store the original longitudes
        original_sun_lon = sun.lon
        original_mercury_lon = mercury.lon
        
        # Set Mercury's longitude to be the same as the Sun's
        mercury.lon = sun.lon
        
        # Check that Mercury is combust and deeply combust
        self.assertTrue(is_combust(self.chart, const.MERCURY))
        self.assertTrue(is_deeply_combust(self.chart, const.MERCURY))
        
        # Check the combustion details
        details = get_combustion_details(self.chart, const.MERCURY)
        self.assertTrue(details['is_combust'])
        self.assertTrue(details['is_deeply_combust'])
        self.assertEqual(details['orb'], 0)
        self.assertGreaterEqual(details['strength_reduction'], 50)
        
        # Now set Mercury's longitude to be just outside the deep combustion orb
        mercury.lon = (sun.lon + DEEP_COMBUSTION_ORBS[const.MERCURY] + 0.1) % 360
        
        # Check that Mercury is still combust but not deeply combust
        self.assertTrue(is_combust(self.chart, const.MERCURY))
        self.assertFalse(is_deeply_combust(self.chart, const.MERCURY))
        
        # Now set Mercury's longitude to be just outside the combustion orb
        mercury.lon = (sun.lon + COMBUSTION_ORBS[const.MERCURY] + 0.1) % 360
        
        # Check that Mercury is no longer combust
        self.assertFalse(is_combust(self.chart, const.MERCURY))
        self.assertFalse(is_deeply_combust(self.chart, const.MERCURY))
        
        # Restore the original longitudes
        sun.lon = original_sun_lon
        mercury.lon = original_mercury_lon

if __name__ == '__main__':
    unittest.main()
