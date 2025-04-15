"""
    Tests for Upagrah (shadow planets) calculations
"""

import unittest
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic import const
from astrovedic.vedic.upagrah import (
    calculate_gulika, calculate_mandi, calculate_dhuma, calculate_vyatipata,
    calculate_parivesha, calculate_indrachapa, calculate_upaketu,
    calculate_kala, calculate_mrityu, calculate_artha_prahara,
    get_upagrah, get_upagrah_positions
)

class TestVedicUpagrah(unittest.TestCase):
    """Test Upagrah (shadow planets) calculations"""
    
    def setUp(self):
        """Set up test data"""
        self.date = Datetime('2000/1/1', '12:00', '+00:00')
        self.jd = self.date.jd
        self.pos = GeoPos('51n30', '0w10')
        self.lat = self.pos.lat
        self.lon = self.pos.lon
        self.chart = Chart(self.date, self.pos)
    
    def test_calculate_gulika(self):
        """Test Gulika calculation"""
        # Calculate Gulika
        gulika_lon = calculate_gulika(self.jd, self.lat, self.lon)
        
        # Check that the result is a valid longitude
        self.assertGreaterEqual(gulika_lon, 0)
        self.assertLess(gulika_lon, 360)
    
    def test_calculate_mandi(self):
        """Test Mandi calculation"""
        # Calculate Mandi
        mandi_lon = calculate_mandi(self.jd, self.lat, self.lon)
        
        # Check that the result is a valid longitude
        self.assertGreaterEqual(mandi_lon, 0)
        self.assertLess(mandi_lon, 360)
    
    def test_calculate_dhuma(self):
        """Test Dhuma calculation"""
        # Calculate Dhuma
        dhuma_lon = calculate_dhuma(self.jd)
        
        # Check that the result is a valid longitude
        self.assertGreaterEqual(dhuma_lon, 0)
        self.assertLess(dhuma_lon, 360)
    
    def test_calculate_vyatipata(self):
        """Test Vyatipata calculation"""
        # Calculate Vyatipata
        vyatipata_lon = calculate_vyatipata(self.jd)
        
        # Check that the result is a valid longitude
        self.assertGreaterEqual(vyatipata_lon, 0)
        self.assertLess(vyatipata_lon, 360)
        
        # Check that Vyatipata is 360 - Dhuma
        dhuma_lon = calculate_dhuma(self.jd)
        expected_vyatipata_lon = (360 - dhuma_lon) % 360
        self.assertAlmostEqual(vyatipata_lon, expected_vyatipata_lon, places=10)
    
    def test_calculate_parivesha(self):
        """Test Parivesha calculation"""
        # Calculate Parivesha
        parivesha_lon = calculate_parivesha(self.jd)
        
        # Check that the result is a valid longitude
        self.assertGreaterEqual(parivesha_lon, 0)
        self.assertLess(parivesha_lon, 360)
        
        # Check that Parivesha is Vyatipata + 180
        vyatipata_lon = calculate_vyatipata(self.jd)
        expected_parivesha_lon = (vyatipata_lon + 180) % 360
        self.assertAlmostEqual(parivesha_lon, expected_parivesha_lon, places=10)
    
    def test_calculate_indrachapa(self):
        """Test Indrachapa calculation"""
        # Calculate Indrachapa
        indrachapa_lon = calculate_indrachapa(self.jd)
        
        # Check that the result is a valid longitude
        self.assertGreaterEqual(indrachapa_lon, 0)
        self.assertLess(indrachapa_lon, 360)
        
        # Check that Indrachapa is Parivesha + 180
        parivesha_lon = calculate_parivesha(self.jd)
        expected_indrachapa_lon = (parivesha_lon + 180) % 360
        self.assertAlmostEqual(indrachapa_lon, expected_indrachapa_lon, places=10)
    
    def test_calculate_upaketu(self):
        """Test Upaketu calculation"""
        # Calculate Upaketu
        upaketu_lon = calculate_upaketu(self.jd)
        
        # Check that the result is a valid longitude
        self.assertGreaterEqual(upaketu_lon, 0)
        self.assertLess(upaketu_lon, 360)
    
    def test_calculate_kala(self):
        """Test Kala calculation"""
        # Calculate Kala
        kala_lon = calculate_kala(self.jd)
        
        # Check that the result is a valid longitude
        self.assertGreaterEqual(kala_lon, 0)
        self.assertLess(kala_lon, 360)
    
    def test_calculate_mrityu(self):
        """Test Mrityu calculation"""
        # Calculate Mrityu
        mrityu_lon = calculate_mrityu(self.jd)
        
        # Check that the result is a valid longitude
        self.assertGreaterEqual(mrityu_lon, 0)
        self.assertLess(mrityu_lon, 360)
    
    def test_calculate_artha_prahara(self):
        """Test Artha Prahara calculation"""
        # Calculate Artha Prahara
        artha_prahara_lon = calculate_artha_prahara(self.jd)
        
        # Check that the result is a valid longitude
        self.assertGreaterEqual(artha_prahara_lon, 0)
        self.assertLess(artha_prahara_lon, 360)
    
    def test_get_upagrah(self):
        """Test getting an Upagrah"""
        # Test for each Upagrah
        for upagrah_id in const.LIST_SHADOW_PLANETS:
            # Get the Upagrah
            upagrah = get_upagrah(upagrah_id, self.jd, self.lat, self.lon)
            
            # Check that the result has the expected structure
            self.assertIn('id', upagrah)
            self.assertIn('lon', upagrah)
            self.assertIn('lat', upagrah)
            self.assertIn('sign', upagrah)
            self.assertIn('signlon', upagrah)
            self.assertIn('type', upagrah)
            
            # Check that the ID is correct
            self.assertEqual(upagrah['id'], upagrah_id)
            
            # Check that the longitude is in the valid range
            self.assertGreaterEqual(upagrah['lon'], 0)
            self.assertLess(upagrah['lon'], 360)
            
            # Check that the sign is a valid sign
            self.assertIn(upagrah['sign'], const.LIST_SIGNS)
            
            # Check that the sign longitude is in the valid range
            self.assertGreaterEqual(upagrah['signlon'], 0)
            self.assertLess(upagrah['signlon'], 30)
            
            # Check that the type is correct
            self.assertEqual(upagrah['type'], const.OBJ_SHADOW_PLANET)
    
    def test_get_upagrah_positions(self):
        """Test getting all Upagrah positions"""
        # Get all Upagrah positions
        positions = get_upagrah_positions(self.chart)
        
        # Check that there are entries for all Upagrah
        for upagrah_id in const.LIST_SHADOW_PLANETS:
            self.assertIn(upagrah_id, positions)
            
            # Check that each entry has the expected structure
            upagrah = positions[upagrah_id]
            self.assertIn('id', upagrah)
            self.assertIn('lon', upagrah)
            self.assertIn('lat', upagrah)
            self.assertIn('sign', upagrah)
            self.assertIn('signlon', upagrah)
            self.assertIn('type', upagrah)
            
            # Check that the ID is correct
            self.assertEqual(upagrah['id'], upagrah_id)
    
    def test_upagrah_formulas(self):
        """Test the formulas for Upagrah calculations"""
        from astrovedic.ephem import swe
        
        # Get Sun's longitude
        sun_lon = swe.sweObjectLon(const.SUN, self.jd)
        
        # Check Upaketu formula
        upaketu_lon = calculate_upaketu(self.jd)
        expected_upaketu_lon = (sun_lon + 30) % 360
        self.assertAlmostEqual(upaketu_lon, expected_upaketu_lon, places=10)
        
        # Check Kala formula
        kala_lon = calculate_kala(self.jd)
        expected_kala_lon = (sun_lon + 45) % 360
        self.assertAlmostEqual(kala_lon, expected_kala_lon, places=10)
        
        # Check Mrityu formula
        mrityu_lon = calculate_mrityu(self.jd)
        expected_mrityu_lon = (sun_lon + 255) % 360
        self.assertAlmostEqual(mrityu_lon, expected_mrityu_lon, places=10)
        
        # Check Artha Prahara formula
        artha_prahara_lon = calculate_artha_prahara(self.jd)
        expected_artha_prahara_lon = (sun_lon + 165) % 360
        self.assertAlmostEqual(artha_prahara_lon, expected_artha_prahara_lon, places=10)

if __name__ == '__main__':
    unittest.main()
