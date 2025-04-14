"""
    Tests for Argala (intervention) and Virodhargala (counter-intervention) calculations
"""

import unittest
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic import const
from astrovedic.vedic.argala import (
    get_house_planets, get_argala_houses, get_argala_for_house,
    get_argala_for_planet, get_all_house_argalas, get_all_planet_argalas,
    get_virodhargala_for_house, get_all_house_virodhargalas,
    ARGALA_PRIMARY, ARGALA_SECONDARY, ARGALA_NEUTRALIZED, ARGALA_NONE
)

class TestVedicArgala(unittest.TestCase):
    """Test Argala (intervention) and Virodhargala (counter-intervention) calculations"""
    
    def setUp(self):
        """Set up test data"""
        self.date = Datetime('2000/1/1', '12:00', '+00:00')
        self.pos = GeoPos('51n30', '0w10')
        self.chart = Chart(self.date, self.pos)
    
    def test_get_house_planets(self):
        """Test getting planets in a house"""
        # Test for each house
        for house_num in range(1, 13):
            # Get the planets
            planets = get_house_planets(self.chart, house_num)
            
            # Check that the result is a list
            self.assertIsInstance(planets, list)
            
            # Check that each planet is a valid planet
            for planet_id in planets:
                self.assertIn(planet_id, const.LIST_SEVEN_PLANETS + [const.RAHU, const.KETU])
    
    def test_get_argala_houses(self):
        """Test getting Argala and Virodhargala houses"""
        # Test for each house
        for house_num in range(1, 13):
            # Get the Argala and Virodhargala houses
            houses = get_argala_houses(house_num)
            
            # Check that the result has the expected structure
            self.assertIn('argala', houses)
            self.assertIn('virodhargala', houses)
            
            # Check that the Argala houses have the expected structure
            self.assertIn('primary', houses['argala'])
            self.assertIn('secondary', houses['argala'])
            
            # Check that there are 4 primary Argala houses
            self.assertEqual(len(houses['argala']['primary']), 4)
            
            # Check that there are 3 secondary Argala houses
            self.assertEqual(len(houses['argala']['secondary']), 3)
            
            # Check that there are 4 Virodhargala houses
            self.assertEqual(len(houses['virodhargala']), 4)
            
            # Check that all house numbers are in the valid range (1-12)
            for argala_house in houses['argala']['primary']:
                self.assertGreaterEqual(argala_house, 1)
                self.assertLessEqual(argala_house, 12)
            
            for argala_house in houses['argala']['secondary']:
                self.assertGreaterEqual(argala_house, 1)
                self.assertLessEqual(argala_house, 12)
            
            for virodhargala_house in houses['virodhargala'].values():
                self.assertGreaterEqual(virodhargala_house, 1)
                self.assertLessEqual(virodhargala_house, 12)
    
    def test_get_argala_for_house(self):
        """Test getting Argala for a house"""
        # Test for each house
        for house_num in range(1, 13):
            # Get the Argala
            argala = get_argala_for_house(self.chart, house_num)
            
            # Check that the result has the expected structure
            self.assertIn('reference_house', argala)
            self.assertIn('argala', argala)
            self.assertIn('virodhargala', argala)
            self.assertIn('net_argala', argala)
            
            # Check that the reference house is correct
            self.assertEqual(argala['reference_house'], house_num)
            
            # Check that there are 7 Argala houses (4 primary + 3 secondary)
            self.assertEqual(len(argala['argala']), 7)
            
            # Check that there are 4 Virodhargala houses
            self.assertEqual(len(argala['virodhargala']), 4)
            
            # Check that there are 7 net Argala entries
            self.assertEqual(len(argala['net_argala']), 7)
            
            # Check that each Argala entry has the expected structure
            for argala_house, argala_info in argala['argala'].items():
                self.assertIn('planets', argala_info)
                self.assertIn('strength', argala_info)
                self.assertIn('type', argala_info)
                
                # Check that the strength is non-negative
                self.assertGreaterEqual(argala_info['strength'], 0)
                
                # Check that the type is one of the expected values
                self.assertIn(argala_info['type'], [
                    ARGALA_PRIMARY, ARGALA_SECONDARY, ARGALA_NEUTRALIZED, ARGALA_NONE
                ])
            
            # Check that each Virodhargala entry has the expected structure
            for virodhargala_house, virodhargala_info in argala['virodhargala'].items():
                self.assertIn('planets', virodhargala_info)
                self.assertIn('strength', virodhargala_info)
                self.assertIn('neutralizes', virodhargala_info)
                
                # Check that the strength is non-negative
                self.assertGreaterEqual(virodhargala_info['strength'], 0)
                
                # Check that neutralizes is a boolean
                self.assertIsInstance(virodhargala_info['neutralizes'], bool)
            
            # Check that each net Argala entry has the expected structure
            for argala_house, net_argala_info in argala['net_argala'].items():
                self.assertIn('strength', net_argala_info)
                self.assertIn('is_neutralized', net_argala_info)
                self.assertIn('type', net_argala_info)
                
                # Check that the strength is non-negative
                self.assertGreaterEqual(net_argala_info['strength'], 0)
                
                # Check that is_neutralized is a boolean
                self.assertIsInstance(net_argala_info['is_neutralized'], bool)
                
                # Check that the type is one of the expected values
                self.assertIn(net_argala_info['type'], [
                    ARGALA_PRIMARY, ARGALA_SECONDARY, ARGALA_NEUTRALIZED, ARGALA_NONE
                ])
    
    def test_get_argala_for_planet(self):
        """Test getting Argala for a planet"""
        # Test for each planet
        for planet_id in const.LIST_SEVEN_PLANETS + [const.RAHU, const.KETU]:
            # Get the Argala
            argala = get_argala_for_planet(self.chart, planet_id)
            
            # Check that the result has the expected structure
            self.assertIn('planet', argala)
            
            # Check that the planet is correct
            self.assertEqual(argala['planet'], planet_id)
            
            # If there's no error, check the Argala structure
            if 'error' not in argala:
                self.assertIn('reference_house', argala)
                self.assertIn('argala', argala)
                self.assertIn('virodhargala', argala)
                self.assertIn('net_argala', argala)
                
                # Check that there are 7 Argala houses (4 primary + 3 secondary)
                self.assertEqual(len(argala['argala']), 7)
                
                # Check that there are 4 Virodhargala houses
                self.assertEqual(len(argala['virodhargala']), 4)
                
                # Check that there are 7 net Argala entries
                self.assertEqual(len(argala['net_argala']), 7)
    
    def test_get_all_house_argalas(self):
        """Test getting Argala for all houses"""
        # Get all house Argalas
        all_argalas = get_all_house_argalas(self.chart)
        
        # Check that there are 12 entries
        self.assertEqual(len(all_argalas), 12)
        
        # Check that each entry has the expected structure
        for house_num, argala in all_argalas.items():
            self.assertIn('reference_house', argala)
            self.assertIn('argala', argala)
            self.assertIn('virodhargala', argala)
            self.assertIn('net_argala', argala)
            
            # Check that the reference house is correct
            self.assertEqual(argala['reference_house'], house_num)
    
    def test_get_all_planet_argalas(self):
        """Test getting Argala for all planets"""
        # Get all planet Argalas
        all_argalas = get_all_planet_argalas(self.chart)
        
        # Check that there are 9 entries (7 planets + Rahu + Ketu)
        self.assertEqual(len(all_argalas), 9)
        
        # Check that each entry has the expected structure
        for planet_id, argala in all_argalas.items():
            self.assertIn('planet', argala)
            
            # Check that the planet is correct
            self.assertEqual(argala['planet'], planet_id)
    
    def test_get_virodhargala_for_house(self):
        """Test getting Virodhargala for a house"""
        # Test for each house
        for house_num in range(1, 13):
            # Get the Virodhargala
            virodhargala = get_virodhargala_for_house(self.chart, house_num)
            
            # Check that the result has the expected structure
            self.assertIn('reference_house', virodhargala)
            self.assertIn('virodhargala', virodhargala)
            
            # Check that the reference house is correct
            self.assertEqual(virodhargala['reference_house'], house_num)
            
            # Check that there are 4 Virodhargala houses
            self.assertEqual(len(virodhargala['virodhargala']), 4)
            
            # Check that each Virodhargala entry has the expected structure
            for virodhargala_house, virodhargala_info in virodhargala['virodhargala'].items():
                self.assertIn('planets', virodhargala_info)
                self.assertIn('strength', virodhargala_info)
                self.assertIn('type', virodhargala_info)
                
                # Check that the strength is non-negative
                self.assertGreaterEqual(virodhargala_info['strength'], 0)
                
                # Check that the type is one of the expected values
                self.assertIn(virodhargala_info['type'], [
                    'second', 'fourth', 'fifth', 'eleventh'
                ])
    
    def test_get_all_house_virodhargalas(self):
        """Test getting Virodhargala for all houses"""
        # Get all house Virodhargalas
        all_virodhargalas = get_all_house_virodhargalas(self.chart)
        
        # Check that there are 12 entries
        self.assertEqual(len(all_virodhargalas), 12)
        
        # Check that each entry has the expected structure
        for house_num, virodhargala in all_virodhargalas.items():
            self.assertIn('reference_house', virodhargala)
            self.assertIn('virodhargala', virodhargala)
            
            # Check that the reference house is correct
            self.assertEqual(virodhargala['reference_house'], house_num)
    
    def test_argala_logic(self):
        """Test the logic of Argala calculation"""
        # Test the 2nd house Argala
        second_house = ((1 + 2 - 1) % 12) + 1  # 2nd house from 1st
        second_virodhargala = ((1 + 12 - 1) % 12) + 1  # 12th house from 1st
        
        # Get the planets in these houses
        second_planets = get_house_planets(self.chart, second_house)
        second_virodhargala_planets = get_house_planets(self.chart, second_virodhargala)
        
        # Calculate the expected Argala strength
        expected_strength = max(0, len(second_planets) - len(second_virodhargala_planets))
        
        # Get the actual Argala
        argala = get_argala_for_house(self.chart, 1)
        
        # Check that the strength matches
        self.assertEqual(argala['net_argala'][second_house]['strength'], expected_strength)
        
        # Check that the neutralization status is correct
        is_neutralized = len(second_virodhargala_planets) >= len(second_planets) and len(second_planets) > 0
        self.assertEqual(argala['net_argala'][second_house]['is_neutralized'], is_neutralized)

if __name__ == '__main__':
    unittest.main()
