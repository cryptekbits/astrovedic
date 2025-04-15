"""
    Tests for Panchanga elements
"""

import unittest
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.vedic.panchang import (
    get_tithi, get_karana, get_yoga, get_vara, get_nakshatra,
    get_bhadra_karana, get_panchaka_dosha, get_chandra_bala,
    get_panchang
)

class TestPanchangaElements(unittest.TestCase):
    """Test Panchanga elements calculations"""
    
    def setUp(self):
        """Set up test data"""
        self.date = Datetime('2000/1/1', '12:00', '+00:00')
        self.jd = self.date.jd
        self.pos = GeoPos('51n30', '0w10')
        self.lat = self.pos.lat
        self.lon = self.pos.lon
        self.utcoffset = self.date.utcoffset
        self.ayanamsa = 'Ayanamsa Lahiri'
    
    def test_tithi(self):
        """Test tithi calculation"""
        tithi_info = get_tithi(self.jd, self.ayanamsa)
        
        # Check that the result has the expected structure
        self.assertIn('index', tithi_info)
        self.assertIn('name', tithi_info)
        self.assertIn('paksha', tithi_info)
        self.assertIn('completion', tithi_info)
        self.assertIn('is_purnima', tithi_info)
        self.assertIn('is_amavasya', tithi_info)
        
        # Check that the index is in the valid range (0-29)
        self.assertGreaterEqual(tithi_info['index'], 0)
        self.assertLess(tithi_info['index'], 30)
        
        # Check that the completion percentage is in the valid range (0-100)
        self.assertGreaterEqual(tithi_info['completion'], 0)
        self.assertLessEqual(tithi_info['completion'], 100)
    
    def test_karana(self):
        """Test karana calculation"""
        karana_info = get_karana(self.jd)
        
        # Check that the result has the expected structure
        self.assertIn('index', karana_info)
        self.assertIn('name', karana_info)
        self.assertIn('completion', karana_info)
        
        # Check that the index is in the valid range (0-59)
        self.assertGreaterEqual(karana_info['index'], 0)
        self.assertLess(karana_info['index'], 60)
        
        # Check that the completion percentage is in the valid range (0-100)
        self.assertGreaterEqual(karana_info['completion'], 0)
        self.assertLessEqual(karana_info['completion'], 100)
    
    def test_yoga(self):
        """Test yoga calculation"""
        yoga_info = get_yoga(self.jd, self.ayanamsa)
        
        # Check that the result has the expected structure
        self.assertIn('index', yoga_info)
        self.assertIn('name', yoga_info)
        self.assertIn('completion', yoga_info)
        
        # Check that the index is in the valid range (0-26)
        self.assertGreaterEqual(yoga_info['index'], 0)
        self.assertLess(yoga_info['index'], 27)
        
        # Check that the completion percentage is in the valid range (0-100)
        self.assertGreaterEqual(yoga_info['completion'], 0)
        self.assertLessEqual(yoga_info['completion'], 100)
    
    def test_vara(self):
        """Test vara calculation"""
        vara_info = get_vara(self.jd)
        
        # Check that the result has the expected structure
        self.assertIn('index', vara_info)
        self.assertIn('name', vara_info)
        
        # Check that the index is in the valid range (0-6)
        self.assertGreaterEqual(vara_info['index'], 0)
        self.assertLess(vara_info['index'], 7)
    
    def test_nakshatra(self):
        """Test nakshatra calculation"""
        nakshatra_info = get_nakshatra(self.jd, self.ayanamsa)
        
        # Check that the result has the expected structure
        self.assertIn('index', nakshatra_info)
        self.assertIn('name', nakshatra_info)
        
        # Check that the index is in the valid range (0-26)
        self.assertGreaterEqual(nakshatra_info['index'], 0)
        self.assertLess(nakshatra_info['index'], 27)
    
    def test_bhadra_karana(self):
        """Test Bhadra Karana (Vishti) calculation"""
        bhadra_info = get_bhadra_karana(self.jd, self.utcoffset, self.ayanamsa)
        
        # Check that the result has the expected structure
        self.assertIn('is_vishti', bhadra_info)
        self.assertIn('karana_index', bhadra_info)
        
        # If it's Vishti, check for start and end times
        if bhadra_info['is_vishti']:
            self.assertIn('start', bhadra_info)
            self.assertIn('end', bhadra_info)
            
            # Check that the start time is before the end time
            self.assertLess(bhadra_info['start'].jd, bhadra_info['end'].jd)
    
    def test_panchaka_dosha(self):
        """Test Panchaka Dosha calculation"""
        panchaka_info = get_panchaka_dosha(self.jd, self.ayanamsa)
        
        # Check that the result has the expected structure
        self.assertIn('is_panchaka_dosha', panchaka_info)
        
        # If it's Panchaka Dosha, check for type and nakshatra
        if panchaka_info['is_panchaka_dosha']:
            self.assertIn('type', panchaka_info)
            self.assertIn('nakshatra', panchaka_info)
            
            # Check that the type is one of the expected values
            self.assertIn(panchaka_info['type'], [
                "Mrityu Panchaka", "Agni Panchaka", "Raja Panchaka",
                "Chora Panchaka", "Roga Panchaka"
            ])
    
    def test_chandra_bala(self):
        """Test Chandra Bala calculation"""
        # Assume natal Moon is in the 1st house
        natal_moon_house = 1
        chandra_bala_info = get_chandra_bala(self.jd, natal_moon_house, self.ayanamsa)
        
        # Check that the result has the expected structure
        self.assertIn('natal_moon_house', chandra_bala_info)
        self.assertIn('current_moon_house', chandra_bala_info)
        self.assertIn('house_distance', chandra_bala_info)
        self.assertIn('is_strong', chandra_bala_info)
        self.assertIn('strength', chandra_bala_info)
        
        # Check that the house distance is in the valid range (1-12)
        self.assertGreaterEqual(chandra_bala_info['house_distance'], 1)
        self.assertLessEqual(chandra_bala_info['house_distance'], 12)
        
        # Check that the strength is in the valid range (0-100)
        self.assertGreaterEqual(chandra_bala_info['strength'], 0)
        self.assertLessEqual(chandra_bala_info['strength'], 100)
    
    def test_panchang(self):
        """Test complete Panchang calculation"""
        panchang_info = get_panchang(self.jd, self.lat, self.lon, self.utcoffset, self.ayanamsa)
        
        # Check that the result has the expected structure
        self.assertIn('date', panchang_info)
        self.assertIn('tithi', panchang_info)
        self.assertIn('nakshatra', panchang_info)
        self.assertIn('yoga', panchang_info)
        self.assertIn('karana', panchang_info)
        self.assertIn('vara', panchang_info)
        self.assertIn('rahukala', panchang_info)
        self.assertIn('yamaganda', panchang_info)
        self.assertIn('gulika_kala', panchang_info)
        self.assertIn('bhadra_karana', panchang_info)
        self.assertIn('panchaka_dosha', panchang_info)
        self.assertIn('abhijit_muhurta', panchang_info)

if __name__ == '__main__':
    unittest.main()
