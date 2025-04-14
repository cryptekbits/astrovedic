"""
    Tests for Vedic Dasha systems
"""

import unittest
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic import const
from astrovedic.vedic import vimshottari, yogini, chara

class TestVimshottariDasha(unittest.TestCase):
    """Test Vimshottari Dasha calculations"""
    
    def setUp(self):
        """Set up test data"""
        self.date = Datetime('2000/1/1', '12:00', '+00:00')
        self.pos = GeoPos('51n30', '0w10')
        self.chart = Chart(self.date, self.pos)
    
    def test_dasha_balance(self):
        """Test Vimshottari Dasha balance calculation"""
        balance = vimshottari.get_dasha_balance(self.chart)
        self.assertIsInstance(balance, float)
        self.assertTrue(0 <= balance <= 20)  # Max period is Venus at 20 years
    
    def test_current_dasha(self):
        """Test current Vimshottari Dasha calculation"""
        dasha = vimshottari.get_current_dasha(self.chart)
        self.assertIsNotNone(dasha)
        self.assertIn('mahadasha', dasha)
        self.assertIn(dasha['mahadasha'], const.LIST_OBJECTS_TRADITIONAL)
    
    def test_mahadasha(self):
        """Test Mahadasha retrieval"""
        mahadasha = vimshottari.get_mahadasha(self.chart)
        self.assertIsNotNone(mahadasha)
        self.assertIn(mahadasha, const.LIST_OBJECTS_TRADITIONAL)
    
    def test_antardasha(self):
        """Test Antardasha retrieval"""
        antardasha = vimshottari.get_antardasha(self.chart)
        # Antardasha might be None for a new chart at birth time
        if antardasha:
            self.assertIn(antardasha, const.LIST_OBJECTS_TRADITIONAL)

class TestYoginiDasha(unittest.TestCase):
    """Test Yogini Dasha calculations"""
    
    def setUp(self):
        """Set up test data"""
        self.date = Datetime('2000/1/1', '12:00', '+00:00')
        self.pos = GeoPos('51n30', '0w10')
        self.chart = Chart(self.date, self.pos)
    
    def test_dasha_balance(self):
        """Test Yogini Dasha balance calculation"""
        balance = yogini.get_dasha_balance(self.chart)
        self.assertIsInstance(balance, float)
        self.assertTrue(0 <= balance <= 8)  # Max period is Rahu at 8 years
    
    def test_current_dasha(self):
        """Test current Yogini Dasha calculation"""
        dasha = yogini.get_current_dasha(self.chart)
        self.assertIsNotNone(dasha)
        self.assertIn('mahadasha', dasha)
        
        # Yogini Dasha uses a subset of planets
        yogini_planets = [const.MOON, const.SUN, const.JUPITER, const.MERCURY, 
                          const.SATURN, const.VENUS, const.MARS, const.RAHU]
        self.assertIn(dasha['mahadasha']['planet'], yogini_planets)
    
    def test_mahadasha(self):
        """Test Mahadasha retrieval"""
        mahadasha = yogini.get_mahadasha(self.chart)
        self.assertIsNotNone(mahadasha)
        
        # Yogini Dasha uses a subset of planets
        yogini_planets = [const.MOON, const.SUN, const.JUPITER, const.MERCURY, 
                          const.SATURN, const.VENUS, const.MARS, const.RAHU]
        self.assertIn(mahadasha['planet'], yogini_planets)
    
    def test_antardasha(self):
        """Test Antardasha retrieval"""
        antardasha = yogini.get_antardasha(self.chart)
        # Antardasha might be None for a new chart at birth time
        if antardasha:
            # Yogini Dasha uses a subset of planets
            yogini_planets = [const.MOON, const.SUN, const.JUPITER, const.MERCURY, 
                              const.SATURN, const.VENUS, const.MARS, const.RAHU]
            self.assertIn(antardasha['planet'], yogini_planets)

class TestCharaDasha(unittest.TestCase):
    """Test Chara Dasha calculations"""
    
    def setUp(self):
        """Set up test data"""
        self.date = Datetime('2000/1/1', '12:00', '+00:00')
        self.pos = GeoPos('51n30', '0w10')
        self.chart = Chart(self.date, self.pos)
    
    def test_dasha_balance(self):
        """Test Chara Dasha balance calculation"""
        balance = chara.get_dasha_balance(self.chart)
        self.assertIsInstance(balance, float)
        self.assertTrue(0 <= balance <= 12)  # Max period is Pisces at 12 years
    
    def test_current_dasha(self):
        """Test current Chara Dasha calculation"""
        dasha = chara.get_current_dasha(self.chart)
        self.assertIsNotNone(dasha)
        self.assertIn('mahadasha', dasha)
        
        # Chara Dasha uses signs
        signs = [const.ARIES, const.TAURUS, const.GEMINI, const.CANCER,
                 const.LEO, const.VIRGO, const.LIBRA, const.SCORPIO,
                 const.SAGITTARIUS, const.CAPRICORN, const.AQUARIUS, const.PISCES]
        self.assertIn(dasha['mahadasha']['sign'], signs)
    
    def test_mahadasha(self):
        """Test Mahadasha retrieval"""
        mahadasha = chara.get_mahadasha(self.chart)
        self.assertIsNotNone(mahadasha)
        
        # Chara Dasha uses signs
        signs = [const.ARIES, const.TAURUS, const.GEMINI, const.CANCER,
                 const.LEO, const.VIRGO, const.LIBRA, const.SCORPIO,
                 const.SAGITTARIUS, const.CAPRICORN, const.AQUARIUS, const.PISCES]
        self.assertIn(mahadasha['sign'], signs)
    
    def test_antardasha(self):
        """Test Antardasha retrieval"""
        antardasha = chara.get_antardasha(self.chart)
        # Antardasha might be None for a new chart at birth time
        if antardasha:
            # Chara Dasha uses signs
            signs = [const.ARIES, const.TAURUS, const.GEMINI, const.CANCER,
                     const.LEO, const.VIRGO, const.LIBRA, const.SCORPIO,
                     const.SAGITTARIUS, const.CAPRICORN, const.AQUARIUS, const.PISCES]
            self.assertIn(antardasha['sign'], signs)

if __name__ == '__main__':
    unittest.main()
