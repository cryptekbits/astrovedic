"""
    Tests for Planetary States (Avasthas) calculations
"""

import unittest
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic import const
from astrovedic.vedic.avasthas import (
    get_baladi_avastha, get_jagradadi_avastha, get_lajjitadi_avastha,
    get_all_avasthas, get_all_planets_avasthas,
    BALADI_INFANT, BALADI_YOUTH, BALADI_ADULT, BALADI_OLD, BALADI_DEAD,
    JAGRADADI_AWAKE, JAGRADADI_DREAMING, JAGRADADI_SLEEPING,
    LAJJITADI_DELIGHTED, LAJJITADI_ASHAMED, LAJJITADI_EXALTED,
    LAJJITADI_BURNING, LAJJITADI_AGITATED, LAJJITADI_SEEKING
)

class TestVedicAvasthas(unittest.TestCase):
    """Test Planetary States (Avasthas) calculations"""
    
    def setUp(self):
        """Set up test data"""
        self.date = Datetime('2000/1/1', '12:00', '+00:00')
        self.pos = GeoPos('51n30', '0w10')
        self.chart = Chart(self.date, self.pos)
    
    def test_baladi_avastha(self):
        """Test Baladi Avastha (five-fold state) calculation"""
        # Test for each planet
        for planet_id in [const.SUN, const.MOON, const.MERCURY, const.VENUS,
                         const.MARS, const.JUPITER, const.SATURN, const.RAHU, const.KETU]:
            # Get the result
            result = get_baladi_avastha(self.chart, planet_id)
            
            # Check that the result has the expected structure
            self.assertIn('avastha', result)
            self.assertIn('strength', result)
            self.assertIn('sign_longitude', result)
            
            # Check that the avastha is one of the expected values
            self.assertIn(result['avastha'], [
                BALADI_INFANT, BALADI_YOUTH, BALADI_ADULT, BALADI_OLD, BALADI_DEAD
            ])
            
            # Check that the strength is in the valid range (0-100)
            self.assertGreaterEqual(result['strength'], 0)
            self.assertLessEqual(result['strength'], 100)
            
            # Check that the sign longitude is in the valid range (0-30)
            self.assertGreaterEqual(result['sign_longitude'], 0)
            self.assertLess(result['sign_longitude'], 30)
    
    def test_jagradadi_avastha(self):
        """Test Jagradadi Avastha (three-fold state) calculation"""
        # Test for each planet
        for planet_id in [const.SUN, const.MOON, const.MERCURY, const.VENUS,
                         const.MARS, const.JUPITER, const.SATURN, const.RAHU, const.KETU]:
            # Get the result
            result = get_jagradadi_avastha(self.chart, planet_id)
            
            # Check that the result has the expected structure
            self.assertIn('avastha', result)
            self.assertIn('strength', result)
            self.assertIn('sign_longitude', result)
            
            # Check that the avastha is one of the expected values
            self.assertIn(result['avastha'], [
                JAGRADADI_AWAKE, JAGRADADI_DREAMING, JAGRADADI_SLEEPING
            ])
            
            # Check that the strength is in the valid range (0-100)
            self.assertGreaterEqual(result['strength'], 0)
            self.assertLessEqual(result['strength'], 100)
            
            # Check that the sign longitude is in the valid range (0-30)
            self.assertGreaterEqual(result['sign_longitude'], 0)
            self.assertLess(result['sign_longitude'], 30)
    
    def test_lajjitadi_avastha(self):
        """Test Lajjitadi Avastha (six-fold state) calculation"""
        # Test for each planet
        for planet_id in [const.SUN, const.MOON, const.MERCURY, const.VENUS,
                         const.MARS, const.JUPITER, const.SATURN, const.RAHU, const.KETU]:
            # Get the result
            result = get_lajjitadi_avastha(self.chart, planet_id)
            
            # Check that the result has the expected structure
            self.assertIn('avastha', result)
            self.assertIn('strength', result)
            self.assertIn('sign', result)
            self.assertIn('is_combust', result)
            
            # Check that the avastha is one of the expected values
            self.assertIn(result['avastha'], [
                LAJJITADI_DELIGHTED, LAJJITADI_ASHAMED, LAJJITADI_EXALTED,
                LAJJITADI_BURNING, LAJJITADI_AGITATED, LAJJITADI_SEEKING
            ])
            
            # Check that the strength is in the valid range (0-100)
            self.assertGreaterEqual(result['strength'], 0)
            self.assertLessEqual(result['strength'], 100)
            
            # Check that the sign is a valid sign
            self.assertIn(result['sign'], const.LIST_SIGNS)
            
            # Check that is_combust is a boolean
            self.assertIsInstance(result['is_combust'], bool)
    
    def test_all_avasthas(self):
        """Test getting all Avasthas for a planet"""
        # Test for each planet
        for planet_id in [const.SUN, const.MOON, const.MERCURY, const.VENUS,
                         const.MARS, const.JUPITER, const.SATURN, const.RAHU, const.KETU]:
            # Get the result
            result = get_all_avasthas(self.chart, planet_id)
            
            # Check that the result has the expected structure
            self.assertIn('baladi', result)
            self.assertIn('jagradadi', result)
            self.assertIn('lajjitadi', result)
            
            # Check that each avastha has the expected structure
            self.assertIn('avastha', result['baladi'])
            self.assertIn('strength', result['baladi'])
            
            self.assertIn('avastha', result['jagradadi'])
            self.assertIn('strength', result['jagradadi'])
            
            self.assertIn('avastha', result['lajjitadi'])
            self.assertIn('strength', result['lajjitadi'])
    
    def test_all_planets_avasthas(self):
        """Test getting all Avasthas for all planets"""
        # Get the result
        result = get_all_planets_avasthas(self.chart)
        
        # Check that the result has entries for all planets
        for planet_id in [const.SUN, const.MOON, const.MERCURY, const.VENUS,
                         const.MARS, const.JUPITER, const.SATURN, const.RAHU, const.KETU]:
            self.assertIn(planet_id, result)
            
            # Check that each planet has all three avasthas
            planet_result = result[planet_id]
            self.assertIn('baladi', planet_result)
            self.assertIn('jagradadi', planet_result)
            self.assertIn('lajjitadi', planet_result)
    
    def test_baladi_avastha_logic(self):
        """Test the logic of Baladi Avastha calculation"""
        # Create a test case where we know the Baladi Avastha
        # For example, place the Sun at 3 degrees in its sign
        sun = self.chart.getObject(const.SUN)
        
        # Store the original longitude
        original_lon = sun.lon
        
        # Set the Sun's longitude to 3 degrees in its sign
        sun.lon = (sun.lon - (sun.lon % 30)) + 3
        
        # Check that the Sun is in the Infant state
        result = get_baladi_avastha(self.chart, const.SUN)
        self.assertEqual(result['avastha'], BALADI_INFANT)
        
        # Set the Sun's longitude to 9 degrees in its sign
        sun.lon = (sun.lon - (sun.lon % 30)) + 9
        
        # Check that the Sun is in the Youth state
        result = get_baladi_avastha(self.chart, const.SUN)
        self.assertEqual(result['avastha'], BALADI_YOUTH)
        
        # Set the Sun's longitude to 15 degrees in its sign
        sun.lon = (sun.lon - (sun.lon % 30)) + 15
        
        # Check that the Sun is in the Adult state
        result = get_baladi_avastha(self.chart, const.SUN)
        self.assertEqual(result['avastha'], BALADI_ADULT)
        
        # Set the Sun's longitude to 21 degrees in its sign
        sun.lon = (sun.lon - (sun.lon % 30)) + 21
        
        # Check that the Sun is in the Old state
        result = get_baladi_avastha(self.chart, const.SUN)
        self.assertEqual(result['avastha'], BALADI_OLD)
        
        # Set the Sun's longitude to 27 degrees in its sign
        sun.lon = (sun.lon - (sun.lon % 30)) + 27
        
        # Check that the Sun is in the Dead state
        result = get_baladi_avastha(self.chart, const.SUN)
        self.assertEqual(result['avastha'], BALADI_DEAD)
        
        # Restore the original longitude
        sun.lon = original_lon
    
    def test_jagradadi_avastha_logic(self):
        """Test the logic of Jagradadi Avastha calculation"""
        # Create a test case where we know the Jagradadi Avastha
        # For example, place the Moon at 5 degrees in its sign
        moon = self.chart.getObject(const.MOON)
        
        # Store the original longitude
        original_lon = moon.lon
        
        # Set the Moon's longitude to 5 degrees in its sign
        moon.lon = (moon.lon - (moon.lon % 30)) + 5
        
        # Check that the Moon is in the Awake state
        result = get_jagradadi_avastha(self.chart, const.MOON)
        self.assertEqual(result['avastha'], JAGRADADI_AWAKE)
        
        # Set the Moon's longitude to 15 degrees in its sign
        moon.lon = (moon.lon - (moon.lon % 30)) + 15
        
        # Check that the Moon is in the Dreaming state
        result = get_jagradadi_avastha(self.chart, const.MOON)
        self.assertEqual(result['avastha'], JAGRADADI_DREAMING)
        
        # Set the Moon's longitude to 25 degrees in its sign
        moon.lon = (moon.lon - (moon.lon % 30)) + 25
        
        # Check that the Moon is in the Sleeping state
        result = get_jagradadi_avastha(self.chart, const.MOON)
        self.assertEqual(result['avastha'], JAGRADADI_SLEEPING)
        
        # Restore the original longitude
        moon.lon = original_lon

if __name__ == '__main__':
    unittest.main()
