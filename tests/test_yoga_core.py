#!/usr/bin/env python3
"""
Test Yoga Core Functions

This script tests the core Yoga (planetary combinations) functions in astrovedic.
"""

import unittest
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic import const
from astrovedic.vedic.yogas.core import (
    get_yoga_strength, get_yoga_effects, get_strongest_yoga,
    is_in_own_sign, is_exalted, is_debilitated,
    is_in_friendly_sign, is_in_enemy_sign,
    get_house_lord, get_house_number,
    are_planets_conjunct, are_planets_in_aspect
)


class TestYogaCore(unittest.TestCase):
    """Test case for Yoga core functions"""
    
    def setUp(self):
        """Set up test case"""
        # Create a chart for testing
        date = Datetime('2025/04/09', '20:51', '+05:30')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart = Chart(date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
        
        # Create a sample Yoga for testing
        self.sample_yoga = {
            'name': 'Test Yoga',
            'type': 'Raja Yoga',
            'planets': [const.SUN, const.JUPITER],
            'houses': [1, 5],
            'description': 'A test Yoga for unit testing',
            'is_beneficial': True
        }
        
        # Create a collection of Yogas for testing
        self.sample_yogas = {
            'Mahapurusha Yoga': [
                {
                    'name': 'Ruchaka Yoga',
                    'type': 'Mahapurusha Yoga',
                    'planets': [const.MARS],
                    'houses': [1],
                    'description': 'Formed when Mars is in its own sign or exaltation and placed in a Kendra house',
                    'is_beneficial': True,
                    'strength': 85.0
                }
            ],
            'Raja Yoga': [
                {
                    'name': 'Dharmakarmaadhipati Yoga',
                    'type': 'Raja Yoga',
                    'planets': [const.JUPITER],
                    'houses': [9, 10],
                    'description': 'Formed when the lords of the 9th and 10th houses are conjunct',
                    'is_beneficial': True,
                    'strength': 75.0
                },
                {
                    'name': 'Gajakesari Yoga',
                    'type': 'Raja Yoga',
                    'planets': [const.MOON, const.JUPITER],
                    'houses': [4, 10],
                    'description': 'Formed when the Moon and Jupiter are in Kendra houses from each other',
                    'is_beneficial': True,
                    'strength': 65.0
                }
            ],
            'Dhana Yoga': [
                {
                    'name': 'Lakshmi Yoga',
                    'type': 'Dhana Yoga',
                    'planets': [const.VENUS, const.JUPITER],
                    'houses': [1, 9],
                    'description': 'Formed when Venus and Jupiter are in Kendra or Trikona houses',
                    'is_beneficial': True,
                    'strength': 70.0
                }
            ],
            'Dosha Yoga': [
                {
                    'name': 'Kemadruma Yoga',
                    'type': 'Dosha Yoga',
                    'planets': [const.MOON],
                    'houses': [7],
                    'description': 'Formed when the Moon has no planets in adjacent houses',
                    'is_beneficial': False,
                    'strength': 60.0
                }
            ],
            'summary': {}
        }
    
    def test_get_yoga_strength(self):
        """Test get_yoga_strength function"""
        # Calculate the strength of the sample Yoga
        strength = get_yoga_strength(self.chart, self.sample_yoga)
        
        # Check that the strength is a float
        self.assertIsInstance(strength, float)
        
        # Check that the strength is within the valid range
        self.assertGreaterEqual(strength, 0.0)
        self.assertLessEqual(strength, 100.0)
        
        # Print the strength for reference
        print(f"Yoga Strength: {strength:.2f}")
        
        # Test with different Yoga types
        for yoga_type in ['Mahapurusha Yoga', 'Raja Yoga', 'Dhana Yoga', 'Nabhasa Yoga', 'Chandra Yoga', 'Dosha Yoga']:
            # Create a Yoga with the specified type
            yoga = {
                'name': f'Test {yoga_type}',
                'type': yoga_type,
                'planets': [const.SUN, const.JUPITER],
                'houses': [1, 5],
                'description': f'A test {yoga_type} for unit testing',
                'is_beneficial': yoga_type != 'Dosha Yoga'
            }
            
            # Calculate the strength
            strength = get_yoga_strength(self.chart, yoga)
            
            # Check that the strength is within the valid range
            self.assertGreaterEqual(strength, 0.0)
            self.assertLessEqual(strength, 100.0)
            
            # Print the strength for reference
            print(f"{yoga_type} Strength: {strength:.2f}")
    
    def test_get_yoga_effects(self):
        """Test get_yoga_effects function"""
        # Get the effects of the sample Yoga
        effects = get_yoga_effects(self.chart, self.sample_yoga)
        
        # Check that the effects is a list
        self.assertIsInstance(effects, list)
        
        # Check that the effects list is not empty
        self.assertGreater(len(effects), 0)
        
        # Print the effects for reference
        print(f"Yoga Effects:")
        for effect in effects:
            print(f"  {effect}")
        
        # Test with different Yoga types
        for yoga_type in ['Mahapurusha Yoga', 'Raja Yoga', 'Dhana Yoga', 'Nabhasa Yoga', 'Chandra Yoga', 'Dosha Yoga']:
            # Create a Yoga with the specified type
            yoga = {
                'name': f'Test {yoga_type}',
                'type': yoga_type,
                'planets': [const.SUN, const.JUPITER],
                'houses': [1, 5],
                'description': f'A test {yoga_type} for unit testing',
                'is_beneficial': yoga_type != 'Dosha Yoga'
            }
            
            # Get the effects
            effects = get_yoga_effects(self.chart, yoga)
            
            # Check that the effects is a list
            self.assertIsInstance(effects, list)
            
            # Check that the effects list is not empty
            self.assertGreater(len(effects), 0)
            
            # Print the effects for reference
            print(f"{yoga_type} Effects:")
            for effect in effects:
                print(f"  {effect}")
    
    def test_get_strongest_yoga(self):
        """Test get_strongest_yoga function"""
        # Get the strongest Yoga
        strongest_yoga = get_strongest_yoga(self.sample_yogas)
        
        # Check that the strongest Yoga is a dictionary
        self.assertIsInstance(strongest_yoga, dict)
        
        # Check that the strongest Yoga has the required keys
        self.assertIn('name', strongest_yoga)
        self.assertIn('type', strongest_yoga)
        self.assertIn('planets', strongest_yoga)
        self.assertIn('houses', strongest_yoga)
        self.assertIn('description', strongest_yoga)
        self.assertIn('is_beneficial', strongest_yoga)
        self.assertIn('strength', strongest_yoga)
        
        # Check that the strongest Yoga is the one with the highest strength
        self.assertEqual(strongest_yoga['name'], 'Ruchaka Yoga')
        self.assertEqual(strongest_yoga['strength'], 85.0)
        
        # Print the strongest Yoga for reference
        print(f"Strongest Yoga: {strongest_yoga['name']} ({strongest_yoga['strength']:.2f})")
    
    def test_is_in_own_sign(self):
        """Test is_in_own_sign function"""
        # Test with planets in their own signs
        for planet_id, sign in [
            (const.SUN, const.LEO),
            (const.MOON, const.CANCER),
            (const.MERCURY, const.GEMINI),
            (const.MERCURY, const.VIRGO),
            (const.VENUS, const.TAURUS),
            (const.VENUS, const.LIBRA),
            (const.MARS, const.ARIES),
            (const.MARS, const.SCORPIO),
            (const.JUPITER, const.SAGITTARIUS),
            (const.JUPITER, const.PISCES),
            (const.SATURN, const.CAPRICORN),
            (const.SATURN, const.AQUARIUS)
        ]:
            # Create a planet object
            planet = type('Object', (), {'id': planet_id, 'sign': sign})
            
            # Check that the planet is in its own sign
            self.assertTrue(is_in_own_sign(planet))
        
        # Test with planets not in their own signs
        for planet_id, sign in [
            (const.SUN, const.CANCER),
            (const.MOON, const.LEO),
            (const.MERCURY, const.ARIES),
            (const.VENUS, const.GEMINI),
            (const.MARS, const.TAURUS),
            (const.JUPITER, const.CAPRICORN),
            (const.SATURN, const.ARIES)
        ]:
            # Create a planet object
            planet = type('Object', (), {'id': planet_id, 'sign': sign})
            
            # Check that the planet is not in its own sign
            self.assertFalse(is_in_own_sign(planet))
    
    def test_is_exalted(self):
        """Test is_exalted function"""
        # Test with planets in their exaltation signs
        for planet_id, sign in [
            (const.SUN, const.ARIES),
            (const.MOON, const.TAURUS),
            (const.MERCURY, const.VIRGO),
            (const.VENUS, const.PISCES),
            (const.MARS, const.CAPRICORN),
            (const.JUPITER, const.CANCER),
            (const.SATURN, const.LIBRA),
            (const.RAHU, const.TAURUS),
            (const.KETU, const.SCORPIO)
        ]:
            # Create a planet object
            planet = type('Object', (), {'id': planet_id, 'sign': sign})
            
            # Check that the planet is exalted
            self.assertTrue(is_exalted(planet))
        
        # Test with planets not in their exaltation signs
        for planet_id, sign in [
            (const.SUN, const.TAURUS),
            (const.MOON, const.ARIES),
            (const.MERCURY, const.PISCES),
            (const.VENUS, const.VIRGO),
            (const.MARS, const.CANCER),
            (const.JUPITER, const.CAPRICORN),
            (const.SATURN, const.ARIES)
        ]:
            # Create a planet object
            planet = type('Object', (), {'id': planet_id, 'sign': sign})
            
            # Check that the planet is not exalted
            self.assertFalse(is_exalted(planet))
    
    def test_is_debilitated(self):
        """Test is_debilitated function"""
        # Test with planets in their debilitation signs
        for planet_id, sign in [
            (const.SUN, const.LIBRA),
            (const.MOON, const.SCORPIO),
            (const.MERCURY, const.PISCES),
            (const.VENUS, const.VIRGO),
            (const.MARS, const.CANCER),
            (const.JUPITER, const.CAPRICORN),
            (const.SATURN, const.ARIES),
            (const.RAHU, const.SCORPIO),
            (const.KETU, const.TAURUS)
        ]:
            # Create a planet object
            planet = type('Object', (), {'id': planet_id, 'sign': sign})
            
            # Check that the planet is debilitated
            self.assertTrue(is_debilitated(planet))
        
        # Test with planets not in their debilitation signs
        for planet_id, sign in [
            (const.SUN, const.ARIES),
            (const.MOON, const.TAURUS),
            (const.MERCURY, const.VIRGO),
            (const.VENUS, const.PISCES),
            (const.MARS, const.CAPRICORN),
            (const.JUPITER, const.CANCER),
            (const.SATURN, const.LIBRA)
        ]:
            # Create a planet object
            planet = type('Object', (), {'id': planet_id, 'sign': sign})
            
            # Check that the planet is not debilitated
            self.assertFalse(is_debilitated(planet))
    
    def test_get_house_lord(self):
        """Test get_house_lord function"""
        # Test the lord of each house
        for house_num in range(1, 13):
            # Get the lord of the house
            lord = get_house_lord(self.chart, house_num)
            
            # Check that the lord is a valid planet
            self.assertIn(lord, const.LIST_OBJECTS_VEDIC)
            
            # Print the lord for reference
            print(f"Lord of House {house_num}: {lord}")
    
    def test_get_house_number(self):
        """Test get_house_number function"""
        # Test the house number of each planet
        for planet_id in const.LIST_OBJECTS_VEDIC:
            # Get the house number of the planet
            house_num = get_house_number(self.chart, planet_id)
            
            # Check that the house number is within the valid range
            self.assertGreaterEqual(house_num, 1)
            self.assertLessEqual(house_num, 12)
            
            # Print the house number for reference
            print(f"House of {planet_id}: {house_num}")
    
    def test_are_planets_conjunct(self):
        """Test are_planets_conjunct function"""
        # Test with planets that are conjunct
        for planet1_id, planet2_id in [
            (const.SUN, const.MERCURY),
            (const.VENUS, const.MARS),
            (const.JUPITER, const.SATURN)
        ]:
            # Check if the planets are conjunct with a large orb
            result = are_planets_conjunct(self.chart, planet1_id, planet2_id, orb=30)
            
            # Print the result for reference
            print(f"{planet1_id} conjunct {planet2_id}: {result}")
        
        # Test with planets that are not conjunct
        for planet1_id, planet2_id in [
            (const.SUN, const.MOON),
            (const.VENUS, const.JUPITER),
            (const.MARS, const.SATURN)
        ]:
            # Check if the planets are conjunct with a small orb
            result = are_planets_conjunct(self.chart, planet1_id, planet2_id, orb=5)
            
            # Print the result for reference
            print(f"{planet1_id} conjunct {planet2_id}: {result}")
    
    def test_are_planets_in_aspect(self):
        """Test are_planets_in_aspect function"""
        # Test with planets that are in aspect
        for planet1_id, planet2_id in [
            (const.SUN, const.MOON),
            (const.VENUS, const.MARS),
            (const.JUPITER, const.SATURN)
        ]:
            # Check if the planets are in aspect with a large orb
            result = are_planets_in_aspect(self.chart, planet1_id, planet2_id, orb=30)
            
            # Print the result for reference
            print(f"{planet1_id} in aspect with {planet2_id}: {result}")
        
        # Test with planets that are not in aspect
        for planet1_id, planet2_id in [
            (const.SUN, const.VENUS),
            (const.MOON, const.JUPITER),
            (const.MARS, const.SATURN)
        ]:
            # Check if the planets are in aspect with a small orb
            result = are_planets_in_aspect(self.chart, planet1_id, planet2_id, orb=5)
            
            # Print the result for reference
            print(f"{planet1_id} in aspect with {planet2_id}: {result}")


if __name__ == '__main__':
    unittest.main()
