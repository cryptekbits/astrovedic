#!/usr/bin/env python3
"""
Test Upagrah (Shadow Planets) Calculations

This script tests the Upagrah (shadow planets) calculations in astrovedic.
"""

import unittest
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic import const
from astrovedic.vedic.upagrah import (
    calculate_gulika, calculate_mandi, calculate_dhuma,
    calculate_vyatipata, calculate_parivesha, calculate_indrachapa,
    calculate_upaketu, get_upagrah, get_upagrah_positions
)


class TestUpagrah(unittest.TestCase):
    """Test case for Upagrah (shadow planets) calculations"""
    
    def setUp(self):
        """Set up test case"""
        # Create a chart for the reference date
        date = Datetime('2025/04/09', '20:51', '+05:30')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart = Chart(date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
        self.jd = date.jd
        self.lat = pos.lat
        self.lon = pos.lon
    
    def test_calculate_gulika(self):
        """Test calculate_gulika function"""
        # Calculate Gulika position
        gulika_lon = calculate_gulika(self.jd, self.lat, self.lon)
        
        # Check that the longitude is within valid range
        self.assertGreaterEqual(gulika_lon, 0)
        self.assertLess(gulika_lon, 360)
        
        # Get the sign and sign longitude
        sign_num = int(gulika_lon / 30)
        sign = const.LIST_SIGNS[sign_num]
        sign_lon = gulika_lon % 30
        
        # Print the position for reference
        print(f"Gulika position: {sign} {sign_lon:.2f}°")
    
    def test_calculate_mandi(self):
        """Test calculate_mandi function"""
        # Calculate Mandi position
        mandi_lon = calculate_mandi(self.jd, self.lat, self.lon)
        
        # Check that the longitude is within valid range
        self.assertGreaterEqual(mandi_lon, 0)
        self.assertLess(mandi_lon, 360)
        
        # Get the sign and sign longitude
        sign_num = int(mandi_lon / 30)
        sign = const.LIST_SIGNS[sign_num]
        sign_lon = mandi_lon % 30
        
        # Print the position for reference
        print(f"Mandi position: {sign} {sign_lon:.2f}°")
    
    def test_calculate_dhuma(self):
        """Test calculate_dhuma function"""
        # Calculate Dhuma position
        dhuma_lon = calculate_dhuma(self.jd)
        
        # Check that the longitude is within valid range
        self.assertGreaterEqual(dhuma_lon, 0)
        self.assertLess(dhuma_lon, 360)
        
        # Get the sign and sign longitude
        sign_num = int(dhuma_lon / 30)
        sign = const.LIST_SIGNS[sign_num]
        sign_lon = dhuma_lon % 30
        
        # Print the position for reference
        print(f"Dhuma position: {sign} {sign_lon:.2f}°")
    
    def test_calculate_vyatipata(self):
        """Test calculate_vyatipata function"""
        # Calculate Vyatipata position
        vyatipata_lon = calculate_vyatipata(self.jd)
        
        # Check that the longitude is within valid range
        self.assertGreaterEqual(vyatipata_lon, 0)
        self.assertLess(vyatipata_lon, 360)
        
        # Get the sign and sign longitude
        sign_num = int(vyatipata_lon / 30)
        sign = const.LIST_SIGNS[sign_num]
        sign_lon = vyatipata_lon % 30
        
        # Print the position for reference
        print(f"Vyatipata position: {sign} {sign_lon:.2f}°")
    
    def test_calculate_parivesha(self):
        """Test calculate_parivesha function"""
        # Calculate Parivesha position
        parivesha_lon = calculate_parivesha(self.jd)
        
        # Check that the longitude is within valid range
        self.assertGreaterEqual(parivesha_lon, 0)
        self.assertLess(parivesha_lon, 360)
        
        # Get the sign and sign longitude
        sign_num = int(parivesha_lon / 30)
        sign = const.LIST_SIGNS[sign_num]
        sign_lon = parivesha_lon % 30
        
        # Print the position for reference
        print(f"Parivesha position: {sign} {sign_lon:.2f}°")
    
    def test_calculate_indrachapa(self):
        """Test calculate_indrachapa function"""
        # Calculate Indrachapa position
        indrachapa_lon = calculate_indrachapa(self.jd)
        
        # Check that the longitude is within valid range
        self.assertGreaterEqual(indrachapa_lon, 0)
        self.assertLess(indrachapa_lon, 360)
        
        # Get the sign and sign longitude
        sign_num = int(indrachapa_lon / 30)
        sign = const.LIST_SIGNS[sign_num]
        sign_lon = indrachapa_lon % 30
        
        # Print the position for reference
        print(f"Indrachapa position: {sign} {sign_lon:.2f}°")
    
    def test_calculate_upaketu(self):
        """Test calculate_upaketu function"""
        # Calculate Upaketu position
        upaketu_lon = calculate_upaketu(self.jd)
        
        # Check that the longitude is within valid range
        self.assertGreaterEqual(upaketu_lon, 0)
        self.assertLess(upaketu_lon, 360)
        
        # Get the sign and sign longitude
        sign_num = int(upaketu_lon / 30)
        sign = const.LIST_SIGNS[sign_num]
        sign_lon = upaketu_lon % 30
        
        # Print the position for reference
        print(f"Upaketu position: {sign} {sign_lon:.2f}°")
    
    def test_get_upagrah(self):
        """Test get_upagrah function"""
        # Get Gulika
        gulika = get_upagrah(const.GULIKA, self.jd, self.lat, self.lon)
        
        # Check that all required keys are present
        self.assertIn('id', gulika)
        self.assertIn('lon', gulika)
        self.assertIn('lat', gulika)
        self.assertIn('sign', gulika)
        self.assertIn('signlon', gulika)
        self.assertIn('type', gulika)
        
        # Check that the ID is correct
        self.assertEqual(gulika['id'], const.GULIKA)
        
        # Check that the type is correct
        self.assertEqual(gulika['type'], const.OBJ_SHADOW_PLANET)
        
        # Print the position for reference
        print(f"Gulika: {gulika['sign']} {gulika['signlon']:.2f}°")
    
    def test_get_upagrah_positions(self):
        """Test get_upagrah_positions function"""
        # Get all Upagrah positions
        positions = get_upagrah_positions(self.chart)
        
        # Check that all Upagrah are present
        for upagrah_id in [const.GULIKA, const.MANDI, const.DHUMA, const.VYATIPATA,
                          const.PARIVESHA, const.INDRACHAPA, const.UPAKETU]:
            self.assertIn(upagrah_id, positions)
        
        # Check that each Upagrah has the required keys
        for upagrah_id, upagrah in positions.items():
            self.assertIn('id', upagrah)
            self.assertIn('lon', upagrah)
            self.assertIn('lat', upagrah)
            self.assertIn('sign', upagrah)
            self.assertIn('signlon', upagrah)
            self.assertIn('type', upagrah)
            
            # Check that the ID is correct
            self.assertEqual(upagrah['id'], upagrah_id)
            
            # Check that the type is correct
            self.assertEqual(upagrah['type'], const.OBJ_SHADOW_PLANET)
        
        # Print the positions for reference
        for upagrah_id, upagrah in positions.items():
            print(f"{upagrah_id}: {upagrah['sign']} {upagrah['signlon']:.2f}°")
    
    def test_relationship_between_upagrah(self):
        """Test the relationship between different Upagrah"""
        # Calculate positions
        dhuma_lon = calculate_dhuma(self.jd)
        vyatipata_lon = calculate_vyatipata(self.jd)
        parivesha_lon = calculate_parivesha(self.jd)
        indrachapa_lon = calculate_indrachapa(self.jd)
        
        # Check the relationships
        # Vyatipata = 360 - Dhuma
        self.assertAlmostEqual(vyatipata_lon, (360 - dhuma_lon) % 360, places=2)
        
        # Parivesha = Vyatipata + 180
        self.assertAlmostEqual(parivesha_lon, (vyatipata_lon + 180) % 360, places=2)
        
        # Indrachapa = Parivesha + 180
        self.assertAlmostEqual(indrachapa_lon, (parivesha_lon + 180) % 360, places=2)


if __name__ == '__main__':
    unittest.main()
