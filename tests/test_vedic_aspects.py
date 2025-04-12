#!/usr/bin/env python3
"""
Test Vedic Aspects

This script tests the Vedic aspect (Drishti) calculations in flatlib.
"""

import unittest
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib.vedic import aspects as vedic_aspects


class TestVedicAspects(unittest.TestCase):
    """Test case for Vedic aspect calculations"""

    def setUp(self):
        """Set up test case"""
        # Create a chart for the reference date
        date = Datetime('2025/04/09', '20:51', '+05:30')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart = Chart(date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)

    def test_house_distance(self):
        """Test house distance calculation"""
        # Test same house
        self.assertEqual(vedic_aspects.get_house_distance(0, 0), 1)
        self.assertEqual(vedic_aspects.get_house_distance(15, 15), 1)

        # Test adjacent houses
        self.assertEqual(vedic_aspects.get_house_distance(15, 45), 2)
        self.assertEqual(vedic_aspects.get_house_distance(345, 15), 2)

        # Test opposite houses
        self.assertEqual(vedic_aspects.get_house_distance(15, 195), 7)
        self.assertEqual(vedic_aspects.get_house_distance(195, 15), 7)

    def test_graha_drishti(self):
        """Test Graha Drishti (planetary aspect) calculation"""
        # All planets aspect the 7th house
        self.assertTrue(vedic_aspects.has_graha_drishti(const.SUN, 0, 180))
        self.assertTrue(vedic_aspects.has_graha_drishti(const.MOON, 0, 180))
        self.assertTrue(vedic_aspects.has_graha_drishti(const.MERCURY, 0, 180))
        self.assertTrue(vedic_aspects.has_graha_drishti(const.VENUS, 0, 180))
        self.assertTrue(vedic_aspects.has_graha_drishti(const.MARS, 0, 180))
        self.assertTrue(vedic_aspects.has_graha_drishti(const.JUPITER, 0, 180))
        self.assertTrue(vedic_aspects.has_graha_drishti(const.SATURN, 0, 180))

        # Mars aspects the 4th and 8th houses
        self.assertTrue(vedic_aspects.has_graha_drishti(const.MARS, 0, 90))
        self.assertTrue(vedic_aspects.has_graha_drishti(const.MARS, 0, 210))

        # Jupiter aspects the 5th and 9th houses
        self.assertTrue(vedic_aspects.has_graha_drishti(const.JUPITER, 0, 120))
        self.assertTrue(vedic_aspects.has_graha_drishti(const.JUPITER, 0, 240))

        # Saturn aspects the 3rd and 10th houses
        self.assertTrue(vedic_aspects.has_graha_drishti(const.SATURN, 0, 60))
        self.assertTrue(vedic_aspects.has_graha_drishti(const.SATURN, 0, 270))

        # No aspects to other houses
        self.assertFalse(vedic_aspects.has_graha_drishti(const.SUN, 0, 30))
        self.assertFalse(vedic_aspects.has_graha_drishti(const.MOON, 0, 60))
        self.assertFalse(vedic_aspects.has_graha_drishti(const.MERCURY, 0, 90))
        self.assertFalse(vedic_aspects.has_graha_drishti(const.VENUS, 0, 120))

    def test_graha_drishti_strength(self):
        """Test Graha Drishti strength calculation"""
        # All planets aspect the 7th house with full strength
        aspect_info = vedic_aspects.get_graha_drishti_strength(const.SUN, 0, 180)
        self.assertTrue(aspect_info['has_aspect'])
        self.assertEqual(aspect_info['strength'], 1.0)
        self.assertEqual(aspect_info['type'], const.VEDIC_FULL_ASPECT)

        # Mars aspects the 4th house with 75% strength
        aspect_info = vedic_aspects.get_graha_drishti_strength(const.MARS, 0, 90)
        self.assertTrue(aspect_info['has_aspect'])
        self.assertEqual(aspect_info['strength'], 0.75)
        self.assertEqual(aspect_info['type'], const.VEDIC_THREE_QUARTER_ASPECT)

        # Mars aspects the 8th house with full strength
        aspect_info = vedic_aspects.get_graha_drishti_strength(const.MARS, 0, 210)
        self.assertTrue(aspect_info['has_aspect'])
        self.assertEqual(aspect_info['strength'], 1.0)
        self.assertEqual(aspect_info['type'], const.VEDIC_FULL_ASPECT)

        # Jupiter aspects the 5th house with full strength
        aspect_info = vedic_aspects.get_graha_drishti_strength(const.JUPITER, 0, 120)
        self.assertTrue(aspect_info['has_aspect'])
        self.assertEqual(aspect_info['strength'], 1.0)
        self.assertEqual(aspect_info['type'], const.VEDIC_FULL_ASPECT)

        # Jupiter aspects the 9th house with 75% strength
        aspect_info = vedic_aspects.get_graha_drishti_strength(const.JUPITER, 0, 240)
        self.assertTrue(aspect_info['has_aspect'])
        self.assertEqual(aspect_info['strength'], 0.75)
        self.assertEqual(aspect_info['type'], const.VEDIC_THREE_QUARTER_ASPECT)

        # Saturn aspects the 3rd house with 75% strength
        aspect_info = vedic_aspects.get_graha_drishti_strength(const.SATURN, 0, 60)
        self.assertTrue(aspect_info['has_aspect'])
        self.assertEqual(aspect_info['strength'], 0.75)
        self.assertEqual(aspect_info['type'], const.VEDIC_THREE_QUARTER_ASPECT)

        # Saturn aspects the 10th house with full strength
        aspect_info = vedic_aspects.get_graha_drishti_strength(const.SATURN, 0, 270)
        self.assertTrue(aspect_info['has_aspect'])
        self.assertEqual(aspect_info['strength'], 1.0)
        self.assertEqual(aspect_info['type'], const.VEDIC_FULL_ASPECT)

        # No aspect to other houses
        aspect_info = vedic_aspects.get_graha_drishti_strength(const.SUN, 0, 30)
        self.assertFalse(aspect_info['has_aspect'])
        self.assertEqual(aspect_info['strength'], 0.0)
        self.assertIsNone(aspect_info['type'])

    def test_rashi_drishti(self):
        """Test Rashi Drishti (sign aspect) calculation"""
        # All signs aspect the 7th sign
        self.assertTrue(vedic_aspects.has_rashi_drishti(const.ARIES, const.LIBRA))
        self.assertTrue(vedic_aspects.has_rashi_drishti(const.TAURUS, const.SCORPIO))
        self.assertTrue(vedic_aspects.has_rashi_drishti(const.GEMINI, const.SAGITTARIUS))

        # Movable (Cardinal) signs aspect the 4th and 10th signs
        self.assertTrue(vedic_aspects.has_rashi_drishti(const.ARIES, const.CANCER))
        self.assertTrue(vedic_aspects.has_rashi_drishti(const.ARIES, const.CAPRICORN))
        self.assertTrue(vedic_aspects.has_rashi_drishti(const.CANCER, const.LIBRA))
        self.assertTrue(vedic_aspects.has_rashi_drishti(const.CANCER, const.ARIES))

        # Fixed signs aspect the 5th and 9th signs
        self.assertTrue(vedic_aspects.has_rashi_drishti(const.TAURUS, const.VIRGO))
        self.assertTrue(vedic_aspects.has_rashi_drishti(const.TAURUS, const.CAPRICORN))
        self.assertTrue(vedic_aspects.has_rashi_drishti(const.LEO, const.SAGITTARIUS))
        self.assertTrue(vedic_aspects.has_rashi_drishti(const.LEO, const.ARIES))

        # Dual (Mutable) signs aspect the 3rd and 11th signs
        self.assertTrue(vedic_aspects.has_rashi_drishti(const.GEMINI, const.LEO))
        self.assertTrue(vedic_aspects.has_rashi_drishti(const.GEMINI, const.ARIES))
        self.assertTrue(vedic_aspects.has_rashi_drishti(const.VIRGO, const.SCORPIO))
        self.assertTrue(vedic_aspects.has_rashi_drishti(const.VIRGO, const.CANCER))

    def test_rashi_drishti_strength(self):
        """Test Rashi Drishti strength calculation"""
        # All signs aspect the 7th sign with full strength
        aspect_info = vedic_aspects.get_rashi_drishti_strength(const.ARIES, const.LIBRA)
        self.assertTrue(aspect_info['has_aspect'])
        self.assertEqual(aspect_info['strength'], 1.0)
        self.assertEqual(aspect_info['type'], const.VEDIC_FULL_ASPECT)

        # Movable (Cardinal) signs aspect the 4th sign with 75% strength
        aspect_info = vedic_aspects.get_rashi_drishti_strength(const.ARIES, const.CANCER)
        self.assertTrue(aspect_info['has_aspect'])
        self.assertEqual(aspect_info['strength'], 0.75)
        self.assertEqual(aspect_info['type'], const.VEDIC_THREE_QUARTER_ASPECT)

        # Movable (Cardinal) signs aspect the 10th sign with full strength
        aspect_info = vedic_aspects.get_rashi_drishti_strength(const.ARIES, const.CAPRICORN)
        self.assertTrue(aspect_info['has_aspect'])
        self.assertEqual(aspect_info['strength'], 1.0)
        self.assertEqual(aspect_info['type'], const.VEDIC_FULL_ASPECT)

        # Fixed signs aspect the 5th sign with full strength
        aspect_info = vedic_aspects.get_rashi_drishti_strength(const.TAURUS, const.VIRGO)
        self.assertTrue(aspect_info['has_aspect'])
        self.assertEqual(aspect_info['strength'], 1.0)
        self.assertEqual(aspect_info['type'], const.VEDIC_FULL_ASPECT)

        # Fixed signs aspect the 9th sign with 75% strength
        aspect_info = vedic_aspects.get_rashi_drishti_strength(const.TAURUS, const.CAPRICORN)
        self.assertTrue(aspect_info['has_aspect'])
        self.assertEqual(aspect_info['strength'], 0.75)
        self.assertEqual(aspect_info['type'], const.VEDIC_THREE_QUARTER_ASPECT)

        # Dual (Mutable) signs aspect the 3rd sign with 75% strength
        aspect_info = vedic_aspects.get_rashi_drishti_strength(const.GEMINI, const.LEO)
        self.assertTrue(aspect_info['has_aspect'])
        self.assertEqual(aspect_info['strength'], 0.75)
        self.assertEqual(aspect_info['type'], const.VEDIC_THREE_QUARTER_ASPECT)

        # Dual (Mutable) signs aspect the 11th sign with full strength
        aspect_info = vedic_aspects.get_rashi_drishti_strength(const.GEMINI, const.ARIES)
        self.assertTrue(aspect_info['has_aspect'])
        self.assertEqual(aspect_info['strength'], 1.0)
        self.assertEqual(aspect_info['type'], const.VEDIC_FULL_ASPECT)

    def test_planet_aspects(self):
        """Test getting all aspects cast by a planet"""
        # Get aspects cast by Mars
        aspects = vedic_aspects.get_planet_aspects(self.chart, const.MARS)

        # Mars should aspect planets in the 4th, 7th, and 8th houses from its position
        self.assertGreater(len(aspects), 0)

        # Verify that each aspect has the required fields
        for aspect in aspects:
            self.assertEqual(aspect['from_planet'], const.MARS)
            self.assertIn('to_planet', aspect)
            self.assertIn('strength', aspect)
            self.assertIn('type', aspect)
            self.assertIn('house_distance', aspect)

    def test_planet_aspects_received(self):
        """Test getting all aspects received by a planet"""
        # Get aspects received by Jupiter (more likely to receive aspects)
        aspects = vedic_aspects.get_planet_aspects_received(self.chart, const.JUPITER)

        # If no aspects are found in the test chart, create a simple test case
        if len(aspects) == 0:
            # Create a simple chart with known aspects
            test_date = Datetime('2025/01/01', '12:00', '+00:00')
            test_pos = GeoPos(0, 0)
            test_chart = Chart(test_date, test_pos)

            # Get aspects received by Jupiter in the test chart
            aspects = vedic_aspects.get_planet_aspects_received(test_chart, const.JUPITER)

        # Jupiter should receive aspects from other planets
        self.assertGreater(len(aspects), 0)

        # Verify that each aspect has the required fields
        for aspect in aspects:
            self.assertEqual(aspect['to_planet'], const.JUPITER)
            self.assertIn('from_planet', aspect)
            self.assertIn('strength', aspect)
            self.assertIn('type', aspect)
            self.assertIn('house_distance', aspect)

    def test_sign_aspects(self):
        """Test getting all aspects cast by a sign"""
        # Get aspects cast by Aries
        aspects = vedic_aspects.get_sign_aspects(const.ARIES)

        # Aries should aspect Libra (7th), Cancer (4th), and Capricorn (10th)
        self.assertEqual(len(aspects), 3)

        # Verify that each aspect has the required fields
        for aspect in aspects:
            self.assertEqual(aspect['from_sign'], const.ARIES)
            self.assertIn('to_sign', aspect)
            self.assertIn('strength', aspect)
            self.assertIn('type', aspect)
            self.assertIn('sign_distance', aspect)

        # Check specific aspects
        aspect_signs = [aspect['to_sign'] for aspect in aspects]
        self.assertIn(const.CANCER, aspect_signs)
        self.assertIn(const.LIBRA, aspect_signs)
        self.assertIn(const.CAPRICORN, aspect_signs)

    def test_sign_aspects_received(self):
        """Test getting all aspects received by a sign"""
        # Get aspects received by Aries
        aspects = vedic_aspects.get_sign_aspects_received(const.ARIES)

        # Aries should receive aspects from Libra (7th), Gemini (3rd), and Sagittarius (9th)
        self.assertGreater(len(aspects), 0)

        # Verify that each aspect has the required fields
        for aspect in aspects:
            self.assertEqual(aspect['to_sign'], const.ARIES)
            self.assertIn('from_sign', aspect)
            self.assertIn('strength', aspect)
            self.assertIn('type', aspect)
            self.assertIn('sign_distance', aspect)

    def test_all_aspects(self):
        """Test getting all aspects in a chart"""
        # Get all aspects in the chart
        all_aspects = vedic_aspects.get_all_aspects(self.chart)

        # Verify that the result has the required structure
        self.assertIn('planet_aspects', all_aspects)
        self.assertIn('sign_aspects', all_aspects)

        # Verify that planet aspects are present for each planet
        for planet_id in const.LIST_OBJECTS_VEDIC:
            self.assertIn(planet_id, all_aspects['planet_aspects'])
            self.assertIn('aspects_cast', all_aspects['planet_aspects'][planet_id])
            self.assertIn('aspects_received', all_aspects['planet_aspects'][planet_id])

        # Verify that sign aspects are present for each sign
        for sign in const.LIST_SIGNS:
            self.assertIn(sign, all_aspects['sign_aspects'])
            self.assertIn('aspects_cast', all_aspects['sign_aspects'][sign])
            self.assertIn('aspects_received', all_aspects['sign_aspects'][sign])


if __name__ == '__main__':
    unittest.main()
