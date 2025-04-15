"""
    Tests for Jaimini Karaka calculations
"""

import unittest
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic import const
from astrovedic.vedic.jaimini.karakas import (
    calculate_chara_karakas, calculate_sthira_karakas,
    ATMAKARAKA_FULL, AMATYAKARAKA_FULL, BHRATRIKARAKA_FULL, MATRIKARAKA_FULL,
    PUTRAKARAKA_FULL, GNATIKARAKA_FULL, DARAKARAKA_FULL, STRIKAKARAKA_FULL
)

class TestJaiminiKarakas(unittest.TestCase):
    """Test Jaimini Karaka calculations"""
    
    def setUp(self):
        """Set up test data"""
        self.date = Datetime('2000/1/1', '12:00', '+00:00')
        self.pos = GeoPos('51n30', '0w10')
        self.chart = Chart(self.date, self.pos)
    
    def test_chara_karakas(self):
        """Test Chara Karaka calculation"""
        karakas = calculate_chara_karakas(self.chart)
        
        # Check that we have the expected karakas
        self.assertIn(ATMAKARAKA_FULL, karakas)
        self.assertIn(AMATYAKARAKA_FULL, karakas)
        self.assertIn(BHRATRIKARAKA_FULL, karakas)
        self.assertIn(MATRIKARAKA_FULL, karakas)
        self.assertIn(PUTRAKARAKA_FULL, karakas)
        self.assertIn(GNATIKARAKA_FULL, karakas)
        self.assertIn(DARAKARAKA_FULL, karakas)
        
        # Check that all karakas have valid planets
        valid_planets = [
            const.SUN, const.MOON, const.MARS, const.MERCURY,
            const.JUPITER, const.VENUS, const.SATURN, const.RAHU
        ]
        
        for karaka, planet in karakas.items():
            self.assertIn(planet, valid_planets)
        
        # Check that no planet is assigned to more than one karaka
        planets = list(karakas.values())
        self.assertEqual(len(planets), len(set(planets)), 
                         "Each planet should be assigned to only one karaka")
    
    def test_sthira_karakas(self):
        """Test Sthira Karaka calculation"""
        karakas = calculate_sthira_karakas()
        
        # Check that we have the expected karakas
        self.assertIn(ATMAKARAKA_FULL, karakas)
        self.assertIn(AMATYAKARAKA_FULL, karakas)
        self.assertIn(BHRATRIKARAKA_FULL, karakas)
        self.assertIn(MATRIKARAKA_FULL, karakas)
        self.assertIn(PUTRAKARAKA_FULL, karakas)
        self.assertIn(GNATIKARAKA_FULL, karakas)
        self.assertIn(DARAKARAKA_FULL, karakas)
        self.assertIn(STRIKAKARAKA_FULL, karakas)
        
        # Check specific assignments
        self.assertEqual(karakas[ATMAKARAKA_FULL], const.SUN)
        self.assertEqual(karakas[AMATYAKARAKA_FULL], const.JUPITER)
        self.assertEqual(karakas[BHRATRIKARAKA_FULL], const.MARS)
        self.assertEqual(karakas[MATRIKARAKA_FULL], const.MOON)
        self.assertEqual(karakas[PUTRAKARAKA_FULL], const.JUPITER)
        self.assertEqual(karakas[GNATIKARAKA_FULL], const.SATURN)
        self.assertEqual(karakas[DARAKARAKA_FULL], const.VENUS)
        self.assertEqual(karakas[STRIKAKARAKA_FULL], const.VENUS)

if __name__ == '__main__':
    unittest.main()
