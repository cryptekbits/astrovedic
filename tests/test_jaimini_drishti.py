"""
    Tests for Jaimini Rashi Drishti (sign aspect) calculations
"""

import unittest
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic import const
from astrovedic.vedic.jaimini.drishti import (
    has_jaimini_rashi_drishti, get_jaimini_rashi_drishti_info,
    get_jaimini_sign_aspects, get_jaimini_sign_aspects_received,
    get_all_jaimini_sign_aspects, get_jaimini_planet_aspects,
    get_jaimini_planet_aspects_received, get_all_jaimini_planet_aspects,
    get_all_jaimini_aspects, JAIMINI_FULL_ASPECT, JAIMINI_MUTUAL_ASPECT
)

class TestJaiminiDrishti(unittest.TestCase):
    """Test Jaimini Rashi Drishti (sign aspect) calculations"""

    def setUp(self):
        """Set up test data"""
        self.date = Datetime('2000/1/1', '12:00', '+00:00')
        self.pos = GeoPos('51n30', '0w10')
        self.chart = Chart(self.date, self.pos)

    def test_jaimini_rashi_drishti(self):
        """Test Jaimini Rashi Drishti (sign aspect) calculation"""
        # Test 7th sign aspect (all signs)
        self.assertTrue(has_jaimini_rashi_drishti(const.ARIES, const.LIBRA))
        self.assertTrue(has_jaimini_rashi_drishti(const.TAURUS, const.SCORPIO))
        self.assertTrue(has_jaimini_rashi_drishti(const.GEMINI, const.SAGITTARIUS))

        # Test 2/12 relationship
        self.assertTrue(has_jaimini_rashi_drishti(const.ARIES, const.TAURUS))  # 2nd
        self.assertTrue(has_jaimini_rashi_drishti(const.ARIES, const.PISCES))  # 12th

        # Test 5/9 relationship
        self.assertTrue(has_jaimini_rashi_drishti(const.ARIES, const.LEO))  # 5th
        self.assertTrue(has_jaimini_rashi_drishti(const.ARIES, const.SAGITTARIUS))  # 9th

        # Test 4/10 relationship
        self.assertTrue(has_jaimini_rashi_drishti(const.ARIES, const.CANCER))  # 4th
        self.assertTrue(has_jaimini_rashi_drishti(const.ARIES, const.CAPRICORN))  # 10th

        # Test 3/11 relationship
        self.assertTrue(has_jaimini_rashi_drishti(const.ARIES, const.GEMINI))  # 3rd
        self.assertTrue(has_jaimini_rashi_drishti(const.ARIES, const.AQUARIUS))  # 11th

        # Test without 3/11 relationship
        self.assertFalse(has_jaimini_rashi_drishti(const.ARIES, const.GEMINI, False))  # 3rd
        self.assertFalse(has_jaimini_rashi_drishti(const.ARIES, const.AQUARIUS, False))  # 11th

        # Test non-aspects (should be none if all relationships are included)
        # But if we exclude 3/11, then we should have non-aspects
        self.assertFalse(has_jaimini_rashi_drishti(const.ARIES, const.VIRGO, False))  # 6th
        self.assertFalse(has_jaimini_rashi_drishti(const.ARIES, const.SCORPIO, False))  # 8th

    def test_jaimini_rashi_drishti_info(self):
        """Test Jaimini Rashi Drishti info"""
        # Test 7th sign aspect
        aspect_info = get_jaimini_rashi_drishti_info(const.ARIES, const.LIBRA)
        self.assertTrue(aspect_info['has_aspect'])
        self.assertEqual(aspect_info['type'], JAIMINI_FULL_ASPECT)
        self.assertTrue(aspect_info['is_mutual'])
        self.assertEqual(aspect_info['sign_distance'], 7)

        # Test 2/12 relationship
        aspect_info = get_jaimini_rashi_drishti_info(const.ARIES, const.TAURUS)
        self.assertTrue(aspect_info['has_aspect'])
        self.assertEqual(aspect_info['type'], JAIMINI_MUTUAL_ASPECT)
        self.assertTrue(aspect_info['is_mutual'])
        self.assertEqual(aspect_info['sign_distance'], 2)

        # Test 5/9 relationship
        aspect_info = get_jaimini_rashi_drishti_info(const.ARIES, const.LEO)
        self.assertTrue(aspect_info['has_aspect'])
        self.assertEqual(aspect_info['type'], JAIMINI_MUTUAL_ASPECT)
        self.assertTrue(aspect_info['is_mutual'])
        self.assertEqual(aspect_info['sign_distance'], 5)

        # Test 4/10 relationship
        aspect_info = get_jaimini_rashi_drishti_info(const.ARIES, const.CANCER)
        self.assertTrue(aspect_info['has_aspect'])
        self.assertEqual(aspect_info['type'], JAIMINI_MUTUAL_ASPECT)
        self.assertTrue(aspect_info['is_mutual'])
        self.assertEqual(aspect_info['sign_distance'], 4)

        # Test 3/11 relationship
        aspect_info = get_jaimini_rashi_drishti_info(const.ARIES, const.GEMINI)
        self.assertTrue(aspect_info['has_aspect'])
        self.assertEqual(aspect_info['type'], JAIMINI_MUTUAL_ASPECT)
        self.assertTrue(aspect_info['is_mutual'])
        self.assertEqual(aspect_info['sign_distance'], 3)

        # Test without 3/11 relationship
        aspect_info = get_jaimini_rashi_drishti_info(const.ARIES, const.GEMINI, False)
        self.assertFalse(aspect_info['has_aspect'])
        self.assertIsNone(aspect_info['type'])
        self.assertFalse(aspect_info['is_mutual'])
        self.assertEqual(aspect_info['sign_distance'], 3)

    def test_jaimini_sign_aspects(self):
        """Test getting all Jaimini aspects cast by a sign"""
        # Get aspects cast by Aries
        aspects = get_jaimini_sign_aspects(const.ARIES)

        # Aries should aspect all signs except Virgo and Scorpio
        # (if 3/11 relationship is included)
        self.assertEqual(len(aspects), 9)

        # Verify that each aspect has the required fields
        for aspect in aspects:
            self.assertEqual(aspect['from_sign'], const.ARIES)
            self.assertIn('to_sign', aspect)
            self.assertIn('type', aspect)
            self.assertIn('sign_distance', aspect)
            self.assertIn('is_mutual', aspect)

        # Get aspects cast by Aries without 3/11 relationship
        aspects = get_jaimini_sign_aspects(const.ARIES, False)

        # Aries should aspect 7 signs (excluding 3rd, 6th, 8th, 11th)
        self.assertEqual(len(aspects), 7)

    def test_jaimini_sign_aspects_received(self):
        """Test getting all Jaimini aspects received by a sign"""
        # Get aspects received by Aries
        aspects = get_jaimini_sign_aspects_received(const.ARIES)

        # Aries should receive aspects from all signs except Virgo and Scorpio
        # (if 3/11 relationship is included)
        self.assertEqual(len(aspects), 9)

        # Verify that each aspect has the required fields
        for aspect in aspects:
            self.assertEqual(aspect['to_sign'], const.ARIES)
            self.assertIn('from_sign', aspect)
            self.assertIn('type', aspect)
            self.assertIn('sign_distance', aspect)
            self.assertIn('is_mutual', aspect)

        # Get aspects received by Aries without 3/11 relationship
        aspects = get_jaimini_sign_aspects_received(const.ARIES, False)

        # Aries should receive aspects from 7 signs (excluding 3rd, 6th, 8th, 11th)
        self.assertEqual(len(aspects), 7)

    def test_all_jaimini_sign_aspects(self):
        """Test getting all Jaimini sign aspects"""
        # Get all sign aspects
        all_aspects = get_all_jaimini_sign_aspects()

        # Verify that the result has the required structure
        for sign in const.LIST_SIGNS:
            self.assertIn(sign, all_aspects)
            self.assertIn('aspects_cast', all_aspects[sign])
            self.assertIn('aspects_received', all_aspects[sign])

    def test_jaimini_planet_aspects(self):
        """Test getting all Jaimini aspects cast by a planet"""
        # Get aspects cast by the Sun
        aspects = get_jaimini_planet_aspects(self.chart, const.SUN)

        # Verify that each aspect has the required fields
        for aspect in aspects:
            self.assertEqual(aspect['from_planet'], const.SUN)
            self.assertIn('to_planet', aspect)
            self.assertIn('from_sign', aspect)
            self.assertIn('to_sign', aspect)
            self.assertIn('type', aspect)
            self.assertIn('sign_distance', aspect)
            self.assertIn('is_mutual', aspect)

    def test_jaimini_planet_aspects_received(self):
        """Test getting all Jaimini aspects received by a planet"""
        # Get aspects received by the Moon
        aspects = get_jaimini_planet_aspects_received(self.chart, const.MOON)

        # Verify that each aspect has the required fields
        for aspect in aspects:
            self.assertEqual(aspect['to_planet'], const.MOON)
            self.assertIn('from_planet', aspect)
            self.assertIn('from_sign', aspect)
            self.assertIn('to_sign', aspect)
            self.assertIn('type', aspect)
            self.assertIn('sign_distance', aspect)
            self.assertIn('is_mutual', aspect)

    def test_all_jaimini_planet_aspects(self):
        """Test getting all Jaimini planet aspects"""
        # Get all planet aspects
        all_aspects = get_all_jaimini_planet_aspects(self.chart)

        # Verify that the result has the required structure
        from astrovedic.vedic.jaimini.drishti import JAIMINI_PLANETS
        for planet_id in JAIMINI_PLANETS:
            self.assertIn(planet_id, all_aspects)
            self.assertIn('aspects_cast', all_aspects[planet_id])
            self.assertIn('aspects_received', all_aspects[planet_id])

    def test_all_jaimini_aspects(self):
        """Test getting all Jaimini aspects"""
        # Get all aspects
        all_aspects = get_all_jaimini_aspects(self.chart)

        # Verify that the result has the required structure
        self.assertIn('sign_aspects', all_aspects)
        self.assertIn('planet_aspects', all_aspects)

if __name__ == '__main__':
    unittest.main()
