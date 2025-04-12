#!/usr/bin/env python3
"""
Test Vedic Dignities

This script tests the Vedic dignity (Swakshetra, Uchcha, Neecha, Moolatrikona)
calculations in flatlib.
"""

import unittest
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib.vedic import dignities as vedic_dignities


class TestVedicDignities(unittest.TestCase):
    """Test case for Vedic dignity calculations"""
    
    def setUp(self):
        """Set up test case"""
        # Create a chart for the reference date
        date = Datetime('2025/04/09', '20:51', '+05:30')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart = Chart(date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
    
    def test_rulership(self):
        """Test rulership functions"""
        # Test get_ruler
        self.assertEqual(vedic_dignities.get_ruler(const.ARIES), const.MARS)
        self.assertEqual(vedic_dignities.get_ruler(const.TAURUS), const.VENUS)
        self.assertEqual(vedic_dignities.get_ruler(const.GEMINI), const.MERCURY)
        self.assertEqual(vedic_dignities.get_ruler(const.CANCER), const.MOON)
        self.assertEqual(vedic_dignities.get_ruler(const.LEO), const.SUN)
        self.assertEqual(vedic_dignities.get_ruler(const.VIRGO), const.MERCURY)
        self.assertEqual(vedic_dignities.get_ruler(const.LIBRA), const.VENUS)
        self.assertEqual(vedic_dignities.get_ruler(const.SCORPIO), const.MARS)
        self.assertEqual(vedic_dignities.get_ruler(const.SAGITTARIUS), const.JUPITER)
        self.assertEqual(vedic_dignities.get_ruler(const.CAPRICORN), const.SATURN)
        self.assertEqual(vedic_dignities.get_ruler(const.AQUARIUS), const.SATURN)
        self.assertEqual(vedic_dignities.get_ruler(const.PISCES), const.JUPITER)
        
        # Test get_ruled_signs
        self.assertEqual(vedic_dignities.get_ruled_signs(const.SUN), [const.LEO])
        self.assertEqual(vedic_dignities.get_ruled_signs(const.MOON), [const.CANCER])
        self.assertEqual(vedic_dignities.get_ruled_signs(const.MERCURY), [const.GEMINI, const.VIRGO])
        self.assertEqual(vedic_dignities.get_ruled_signs(const.VENUS), [const.TAURUS, const.LIBRA])
        self.assertEqual(vedic_dignities.get_ruled_signs(const.MARS), [const.ARIES, const.SCORPIO])
        self.assertEqual(vedic_dignities.get_ruled_signs(const.JUPITER), [const.SAGITTARIUS, const.PISCES])
        self.assertEqual(vedic_dignities.get_ruled_signs(const.SATURN), [const.CAPRICORN, const.AQUARIUS])
        self.assertEqual(vedic_dignities.get_ruled_signs(const.RAHU), [])
        self.assertEqual(vedic_dignities.get_ruled_signs(const.KETU), [])
        
        # Test is_own_sign
        self.assertTrue(vedic_dignities.is_own_sign(const.SUN, const.LEO))
        self.assertTrue(vedic_dignities.is_own_sign(const.MOON, const.CANCER))
        self.assertTrue(vedic_dignities.is_own_sign(const.MERCURY, const.GEMINI))
        self.assertTrue(vedic_dignities.is_own_sign(const.MERCURY, const.VIRGO))
        self.assertTrue(vedic_dignities.is_own_sign(const.VENUS, const.TAURUS))
        self.assertTrue(vedic_dignities.is_own_sign(const.VENUS, const.LIBRA))
        self.assertTrue(vedic_dignities.is_own_sign(const.MARS, const.ARIES))
        self.assertTrue(vedic_dignities.is_own_sign(const.MARS, const.SCORPIO))
        self.assertTrue(vedic_dignities.is_own_sign(const.JUPITER, const.SAGITTARIUS))
        self.assertTrue(vedic_dignities.is_own_sign(const.JUPITER, const.PISCES))
        self.assertTrue(vedic_dignities.is_own_sign(const.SATURN, const.CAPRICORN))
        self.assertTrue(vedic_dignities.is_own_sign(const.SATURN, const.AQUARIUS))
        
        # Test is_own_sign (negative cases)
        self.assertFalse(vedic_dignities.is_own_sign(const.SUN, const.CANCER))
        self.assertFalse(vedic_dignities.is_own_sign(const.MOON, const.LEO))
        self.assertFalse(vedic_dignities.is_own_sign(const.RAHU, const.TAURUS))
        self.assertFalse(vedic_dignities.is_own_sign(const.KETU, const.SCORPIO))
    
    def test_exaltation(self):
        """Test exaltation functions"""
        # Test get_exaltation
        self.assertEqual(vedic_dignities.get_exaltation(const.SUN), (const.ARIES, 10))
        self.assertEqual(vedic_dignities.get_exaltation(const.MOON), (const.TAURUS, 3))
        self.assertEqual(vedic_dignities.get_exaltation(const.MERCURY), (const.VIRGO, 15))
        self.assertEqual(vedic_dignities.get_exaltation(const.VENUS), (const.PISCES, 27))
        self.assertEqual(vedic_dignities.get_exaltation(const.MARS), (const.CAPRICORN, 28))
        self.assertEqual(vedic_dignities.get_exaltation(const.JUPITER), (const.CANCER, 5))
        self.assertEqual(vedic_dignities.get_exaltation(const.SATURN), (const.LIBRA, 20))
        self.assertEqual(vedic_dignities.get_exaltation(const.RAHU), (const.TAURUS, 20))
        self.assertEqual(vedic_dignities.get_exaltation(const.KETU), (const.SCORPIO, 20))
        
        # Test is_exalted
        self.assertTrue(vedic_dignities.is_exalted(const.SUN, const.ARIES))
        self.assertTrue(vedic_dignities.is_exalted(const.MOON, const.TAURUS))
        self.assertTrue(vedic_dignities.is_exalted(const.MERCURY, const.VIRGO))
        self.assertTrue(vedic_dignities.is_exalted(const.VENUS, const.PISCES))
        self.assertTrue(vedic_dignities.is_exalted(const.MARS, const.CAPRICORN))
        self.assertTrue(vedic_dignities.is_exalted(const.JUPITER, const.CANCER))
        self.assertTrue(vedic_dignities.is_exalted(const.SATURN, const.LIBRA))
        self.assertTrue(vedic_dignities.is_exalted(const.RAHU, const.TAURUS))
        self.assertTrue(vedic_dignities.is_exalted(const.KETU, const.SCORPIO))
        
        # Test is_exalted (negative cases)
        self.assertFalse(vedic_dignities.is_exalted(const.SUN, const.TAURUS))
        self.assertFalse(vedic_dignities.is_exalted(const.MOON, const.ARIES))
        
        # Test is_exact_exaltation
        self.assertTrue(vedic_dignities.is_exact_exaltation(const.SUN, const.ARIES, 10))
        self.assertTrue(vedic_dignities.is_exact_exaltation(const.MOON, const.TAURUS, 3))
        self.assertTrue(vedic_dignities.is_exact_exaltation(const.MERCURY, const.VIRGO, 15))
        self.assertTrue(vedic_dignities.is_exact_exaltation(const.VENUS, const.PISCES, 27))
        self.assertTrue(vedic_dignities.is_exact_exaltation(const.MARS, const.CAPRICORN, 28))
        self.assertTrue(vedic_dignities.is_exact_exaltation(const.JUPITER, const.CANCER, 5))
        self.assertTrue(vedic_dignities.is_exact_exaltation(const.SATURN, const.LIBRA, 20))
        self.assertTrue(vedic_dignities.is_exact_exaltation(const.RAHU, const.TAURUS, 20))
        self.assertTrue(vedic_dignities.is_exact_exaltation(const.KETU, const.SCORPIO, 20))
        
        # Test is_exact_exaltation (negative cases)
        self.assertFalse(vedic_dignities.is_exact_exaltation(const.SUN, const.ARIES, 11))
        self.assertFalse(vedic_dignities.is_exact_exaltation(const.MOON, const.TAURUS, 4))
    
    def test_debilitation(self):
        """Test debilitation functions"""
        # Test get_debilitation
        self.assertEqual(vedic_dignities.get_debilitation(const.SUN), (const.LIBRA, 10))
        self.assertEqual(vedic_dignities.get_debilitation(const.MOON), (const.SCORPIO, 3))
        self.assertEqual(vedic_dignities.get_debilitation(const.MERCURY), (const.PISCES, 15))
        self.assertEqual(vedic_dignities.get_debilitation(const.VENUS), (const.VIRGO, 27))
        self.assertEqual(vedic_dignities.get_debilitation(const.MARS), (const.CANCER, 28))
        self.assertEqual(vedic_dignities.get_debilitation(const.JUPITER), (const.CAPRICORN, 5))
        self.assertEqual(vedic_dignities.get_debilitation(const.SATURN), (const.ARIES, 20))
        self.assertEqual(vedic_dignities.get_debilitation(const.RAHU), (const.SCORPIO, 20))
        self.assertEqual(vedic_dignities.get_debilitation(const.KETU), (const.TAURUS, 20))
        
        # Test is_debilitated
        self.assertTrue(vedic_dignities.is_debilitated(const.SUN, const.LIBRA))
        self.assertTrue(vedic_dignities.is_debilitated(const.MOON, const.SCORPIO))
        self.assertTrue(vedic_dignities.is_debilitated(const.MERCURY, const.PISCES))
        self.assertTrue(vedic_dignities.is_debilitated(const.VENUS, const.VIRGO))
        self.assertTrue(vedic_dignities.is_debilitated(const.MARS, const.CANCER))
        self.assertTrue(vedic_dignities.is_debilitated(const.JUPITER, const.CAPRICORN))
        self.assertTrue(vedic_dignities.is_debilitated(const.SATURN, const.ARIES))
        self.assertTrue(vedic_dignities.is_debilitated(const.RAHU, const.SCORPIO))
        self.assertTrue(vedic_dignities.is_debilitated(const.KETU, const.TAURUS))
        
        # Test is_debilitated (negative cases)
        self.assertFalse(vedic_dignities.is_debilitated(const.SUN, const.ARIES))
        self.assertFalse(vedic_dignities.is_debilitated(const.MOON, const.TAURUS))
        
        # Test is_exact_debilitation
        self.assertTrue(vedic_dignities.is_exact_debilitation(const.SUN, const.LIBRA, 10))
        self.assertTrue(vedic_dignities.is_exact_debilitation(const.MOON, const.SCORPIO, 3))
        self.assertTrue(vedic_dignities.is_exact_debilitation(const.MERCURY, const.PISCES, 15))
        self.assertTrue(vedic_dignities.is_exact_debilitation(const.VENUS, const.VIRGO, 27))
        self.assertTrue(vedic_dignities.is_exact_debilitation(const.MARS, const.CANCER, 28))
        self.assertTrue(vedic_dignities.is_exact_debilitation(const.JUPITER, const.CAPRICORN, 5))
        self.assertTrue(vedic_dignities.is_exact_debilitation(const.SATURN, const.ARIES, 20))
        self.assertTrue(vedic_dignities.is_exact_debilitation(const.RAHU, const.SCORPIO, 20))
        self.assertTrue(vedic_dignities.is_exact_debilitation(const.KETU, const.TAURUS, 20))
        
        # Test is_exact_debilitation (negative cases)
        self.assertFalse(vedic_dignities.is_exact_debilitation(const.SUN, const.LIBRA, 11))
        self.assertFalse(vedic_dignities.is_exact_debilitation(const.MOON, const.SCORPIO, 4))
    
    def test_moolatrikona(self):
        """Test Moolatrikona functions"""
        # Test get_moolatrikona
        self.assertEqual(vedic_dignities.get_moolatrikona(const.SUN), (const.LEO, 0, 20))
        self.assertEqual(vedic_dignities.get_moolatrikona(const.MOON), (const.TAURUS, 4, 30))
        self.assertEqual(vedic_dignities.get_moolatrikona(const.MERCURY), (const.VIRGO, 16, 20))
        self.assertEqual(vedic_dignities.get_moolatrikona(const.VENUS), (const.LIBRA, 0, 15))
        self.assertEqual(vedic_dignities.get_moolatrikona(const.MARS), (const.ARIES, 0, 12))
        self.assertEqual(vedic_dignities.get_moolatrikona(const.JUPITER), (const.SAGITTARIUS, 0, 10))
        self.assertEqual(vedic_dignities.get_moolatrikona(const.SATURN), (const.AQUARIUS, 0, 20))
        self.assertIsNone(vedic_dignities.get_moolatrikona(const.RAHU))
        self.assertIsNone(vedic_dignities.get_moolatrikona(const.KETU))
        
        # Test is_in_moolatrikona
        self.assertTrue(vedic_dignities.is_in_moolatrikona(const.SUN, const.LEO, 10))
        self.assertTrue(vedic_dignities.is_in_moolatrikona(const.MOON, const.TAURUS, 15))
        self.assertTrue(vedic_dignities.is_in_moolatrikona(const.MERCURY, const.VIRGO, 18))
        self.assertTrue(vedic_dignities.is_in_moolatrikona(const.VENUS, const.LIBRA, 10))
        self.assertTrue(vedic_dignities.is_in_moolatrikona(const.MARS, const.ARIES, 5))
        self.assertTrue(vedic_dignities.is_in_moolatrikona(const.JUPITER, const.SAGITTARIUS, 5))
        self.assertTrue(vedic_dignities.is_in_moolatrikona(const.SATURN, const.AQUARIUS, 10))
        
        # Test is_in_moolatrikona (negative cases)
        self.assertFalse(vedic_dignities.is_in_moolatrikona(const.SUN, const.LEO, 25))
        self.assertFalse(vedic_dignities.is_in_moolatrikona(const.MERCURY, const.VIRGO, 15))
        self.assertFalse(vedic_dignities.is_in_moolatrikona(const.VENUS, const.LIBRA, 20))
        self.assertFalse(vedic_dignities.is_in_moolatrikona(const.MARS, const.ARIES, 15))
        self.assertFalse(vedic_dignities.is_in_moolatrikona(const.JUPITER, const.SAGITTARIUS, 15))
        self.assertFalse(vedic_dignities.is_in_moolatrikona(const.SATURN, const.AQUARIUS, 25))
        self.assertFalse(vedic_dignities.is_in_moolatrikona(const.RAHU, const.TAURUS, 10))
        self.assertFalse(vedic_dignities.is_in_moolatrikona(const.KETU, const.SCORPIO, 10))
    
    def test_natural_friendship(self):
        """Test natural friendship functions"""
        # Test get_natural_friendship
        self.assertEqual(vedic_dignities.get_natural_friendship(const.SUN, const.SUN), 3)  # Neutral
        self.assertEqual(vedic_dignities.get_natural_friendship(const.SUN, const.MOON), 4)  # Friend
        self.assertEqual(vedic_dignities.get_natural_friendship(const.SUN, const.MARS), 4)  # Friend
        self.assertEqual(vedic_dignities.get_natural_friendship(const.SUN, const.JUPITER), 4)  # Friend
        self.assertEqual(vedic_dignities.get_natural_friendship(const.SUN, const.VENUS), 2)  # Enemy
        self.assertEqual(vedic_dignities.get_natural_friendship(const.SUN, const.SATURN), 2)  # Enemy
        
        self.assertEqual(vedic_dignities.get_natural_friendship(const.MOON, const.SUN), 4)  # Friend
        self.assertEqual(vedic_dignities.get_natural_friendship(const.MOON, const.JUPITER), 4)  # Friend
        self.assertEqual(vedic_dignities.get_natural_friendship(const.MOON, const.MARS), 2)  # Enemy
        
        self.assertEqual(vedic_dignities.get_natural_friendship(const.JUPITER, const.MERCURY), 2)  # Enemy
        self.assertEqual(vedic_dignities.get_natural_friendship(const.JUPITER, const.VENUS), 2)  # Enemy
        
        self.assertEqual(vedic_dignities.get_natural_friendship(const.SATURN, const.VENUS), 4)  # Friend
        self.assertEqual(vedic_dignities.get_natural_friendship(const.SATURN, const.JUPITER), 2)  # Enemy
    
    def test_temporal_friendship(self):
        """Test temporal friendship functions"""
        # Test calculate_temporal_friendship
        # This is a more complex test that depends on the chart
        sun_moon = vedic_dignities.calculate_temporal_friendship(self.chart, const.SUN, const.MOON)
        self.assertIn(sun_moon, [1, 2, 3, 4, 5])  # Should be a valid friendship level
        
        jupiter_saturn = vedic_dignities.calculate_temporal_friendship(self.chart, const.JUPITER, const.SATURN)
        self.assertIn(jupiter_saturn, [1, 2, 3, 4, 5])  # Should be a valid friendship level
    
    def test_combined_friendship(self):
        """Test combined friendship functions"""
        # Test calculate_combined_friendship
        # This is a more complex test that depends on the chart
        sun_moon = vedic_dignities.calculate_combined_friendship(self.chart, const.SUN, const.MOON)
        self.assertIn(sun_moon, ['GREAT_FRIEND', 'FRIEND', 'NEUTRAL', 'ENEMY', 'GREAT_ENEMY'])
        
        jupiter_saturn = vedic_dignities.calculate_combined_friendship(self.chart, const.JUPITER, const.SATURN)
        self.assertIn(jupiter_saturn, ['GREAT_FRIEND', 'FRIEND', 'NEUTRAL', 'ENEMY', 'GREAT_ENEMY'])
    
    def test_dignity_score(self):
        """Test dignity score functions"""
        # Test get_dignity_score for a planet in its own sign
        sun_in_leo = vedic_dignities.get_dignity_score(const.SUN, const.LEO, 15)
        self.assertTrue(sun_in_leo['is_own_sign'])
        self.assertTrue(sun_in_leo['is_moolatrikona'])
        self.assertFalse(sun_in_leo['is_exalted'])
        self.assertFalse(sun_in_leo['is_debilitated'])
        self.assertEqual(sun_in_leo['score'], 7)  # Moolatrikona score
        
        # Test get_dignity_score for a planet in its exaltation
        sun_in_aries = vedic_dignities.get_dignity_score(const.SUN, const.ARIES, 10)
        self.assertFalse(sun_in_aries['is_own_sign'])
        self.assertFalse(sun_in_aries['is_moolatrikona'])
        self.assertTrue(sun_in_aries['is_exalted'])
        self.assertTrue(sun_in_aries['is_exact_exaltation'])
        self.assertFalse(sun_in_aries['is_debilitated'])
        self.assertEqual(sun_in_aries['score'], 10)  # Exact exaltation score
        
        # Test get_dignity_score for a planet in its debilitation
        sun_in_libra = vedic_dignities.get_dignity_score(const.SUN, const.LIBRA, 10)
        self.assertFalse(sun_in_libra['is_own_sign'])
        self.assertFalse(sun_in_libra['is_moolatrikona'])
        self.assertFalse(sun_in_libra['is_exalted'])
        self.assertTrue(sun_in_libra['is_debilitated'])
        self.assertTrue(sun_in_libra['is_exact_debilitation'])
        self.assertEqual(sun_in_libra['score'], -10)  # Exact debilitation score
    
    def test_dignity_name(self):
        """Test dignity name functions"""
        # Test get_dignity_name
        self.assertEqual(vedic_dignities.get_dignity_name(const.SUN, const.LEO, 15), "Moolatrikona")
        self.assertEqual(vedic_dignities.get_dignity_name(const.SUN, const.ARIES, 10), "Exact Exaltation")
        self.assertEqual(vedic_dignities.get_dignity_name(const.SUN, const.ARIES, 15), "Exaltation")
        self.assertEqual(vedic_dignities.get_dignity_name(const.SUN, const.LIBRA, 10), "Exact Debilitation")
        self.assertEqual(vedic_dignities.get_dignity_name(const.SUN, const.LIBRA, 15), "Debilitation")
        self.assertEqual(vedic_dignities.get_dignity_name(const.MOON, const.CANCER, 15), "Own Sign")
        self.assertEqual(vedic_dignities.get_dignity_name(const.SUN, const.GEMINI, 15), "None")


if __name__ == '__main__':
    unittest.main()
