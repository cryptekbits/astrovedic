#!/usr/bin/env python3
"""
Test Higher Divisional Charts (Vargas)

This script tests the higher divisional chart calculations in astrovedic.
"""

import unittest
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic import const
from astrovedic.vedic.vargas import (
    D20, D24, D27, D30, D40, D45, D60,
    get_varga_chart, get_varga_longitude
)
from astrovedic.vedic.vargas.vimshamsha import calculate_d20
from astrovedic.vedic.vargas.chaturvimshamsha import calculate_d24
from astrovedic.vedic.vargas.saptavimshamsha import calculate_d27
from astrovedic.vedic.vargas.trimshamsha import calculate_d30
from astrovedic.vedic.vargas.khavedamsha import calculate_d40
from astrovedic.vedic.vargas.akshavedamsha import calculate_d45
from astrovedic.vedic.vargas.shashtiamsha import calculate_d60
from astrovedic.vedic.vargas.analysis import get_vimshopaka_bala


class TestHigherVargas(unittest.TestCase):
    """Test case for higher divisional chart calculations"""
    
    def setUp(self):
        """Set up test case"""
        # Create a chart for the reference date
        date = Datetime('2025/04/09', '20:51', '+05:30')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart = Chart(date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
        
        # Set up test longitudes for different sign types
        self.movable_sign_lon = 15.0  # Aries 15°
        self.fixed_sign_lon = 45.0    # Taurus 15°
        self.dual_sign_lon = 75.0     # Gemini 15°
    
    def test_d20_chart(self):
        """Test D20 (Vimshamsha) chart calculations"""
        # Get the D20 chart
        d20_chart = get_varga_chart(self.chart, D20)
        
        # Check that the chart was created successfully
        self.assertIsNotNone(d20_chart)
        
        # Check that all planets are present
        for planet_id in const.LIST_OBJECTS_VEDIC:
            planet = d20_chart.getObject(planet_id)
            self.assertIsNotNone(planet)
        
        # Test the calculation function directly
        for test_lon, sign_type in [
            (self.movable_sign_lon, "movable"),
            (self.fixed_sign_lon, "fixed"),
            (self.dual_sign_lon, "dual")
        ]:
            d20_lon = calculate_d20(test_lon)
            
            # Check that the longitude is valid
            self.assertGreaterEqual(d20_lon, 0)
            self.assertLess(d20_lon, 360)
            
            # Print the result for reference
            sign_num = int(d20_lon / 30)
            sign_lon = d20_lon % 30
            print(f"D20 for {sign_type} sign {test_lon}°: {const.LIST_SIGNS[sign_num]} {sign_lon:.2f}°")
    
    def test_d24_chart(self):
        """Test D24 (Chaturvimshamsha) chart calculations"""
        # Get the D24 chart
        d24_chart = get_varga_chart(self.chart, D24)
        
        # Check that the chart was created successfully
        self.assertIsNotNone(d24_chart)
        
        # Check that all planets are present
        for planet_id in const.LIST_OBJECTS_VEDIC:
            planet = d24_chart.getObject(planet_id)
            self.assertIsNotNone(planet)
        
        # Test the calculation function directly
        for test_lon, sign_type in [
            (self.movable_sign_lon, "movable"),
            (self.fixed_sign_lon, "fixed"),
            (self.dual_sign_lon, "dual")
        ]:
            d24_lon = calculate_d24(test_lon)
            
            # Check that the longitude is valid
            self.assertGreaterEqual(d24_lon, 0)
            self.assertLess(d24_lon, 360)
            
            # Print the result for reference
            sign_num = int(d24_lon / 30)
            sign_lon = d24_lon % 30
            print(f"D24 for {sign_type} sign {test_lon}°: {const.LIST_SIGNS[sign_num]} {sign_lon:.2f}°")
    
    def test_d27_chart(self):
        """Test D27 (Saptavimshamsha) chart calculations"""
        # Get the D27 chart
        d27_chart = get_varga_chart(self.chart, D27)
        
        # Check that the chart was created successfully
        self.assertIsNotNone(d27_chart)
        
        # Check that all planets are present
        for planet_id in const.LIST_OBJECTS_VEDIC:
            planet = d27_chart.getObject(planet_id)
            self.assertIsNotNone(planet)
        
        # Test the calculation function directly
        for test_lon, sign_type in [
            (self.movable_sign_lon, "movable"),
            (self.fixed_sign_lon, "fixed"),
            (self.dual_sign_lon, "dual")
        ]:
            d27_lon = calculate_d27(test_lon)
            
            # Check that the longitude is valid
            self.assertGreaterEqual(d27_lon, 0)
            self.assertLess(d27_lon, 360)
            
            # Print the result for reference
            sign_num = int(d27_lon / 30)
            sign_lon = d27_lon % 30
            print(f"D27 for {sign_type} sign {test_lon}°: {const.LIST_SIGNS[sign_num]} {sign_lon:.2f}°")
    
    def test_d30_chart(self):
        """Test D30 (Trimshamsha) chart calculations"""
        # Get the D30 chart
        d30_chart = get_varga_chart(self.chart, D30)
        
        # Check that the chart was created successfully
        self.assertIsNotNone(d30_chart)
        
        # Check that all planets are present
        for planet_id in const.LIST_OBJECTS_VEDIC:
            planet = d30_chart.getObject(planet_id)
            self.assertIsNotNone(planet)
        
        # Test the calculation function directly
        for test_lon, sign_type in [
            (self.movable_sign_lon, "movable"),
            (self.fixed_sign_lon, "fixed"),
            (self.dual_sign_lon, "dual")
        ]:
            d30_lon = calculate_d30(test_lon)
            
            # Check that the longitude is valid
            self.assertGreaterEqual(d30_lon, 0)
            self.assertLess(d30_lon, 360)
            
            # Print the result for reference
            sign_num = int(d30_lon / 30)
            sign_lon = d30_lon % 30
            print(f"D30 for {sign_type} sign {test_lon}°: {const.LIST_SIGNS[sign_num]} {sign_lon:.2f}°")
    
    def test_d40_chart(self):
        """Test D40 (Khavedamsha) chart calculations"""
        # Get the D40 chart
        d40_chart = get_varga_chart(self.chart, D40)
        
        # Check that the chart was created successfully
        self.assertIsNotNone(d40_chart)
        
        # Check that all planets are present
        for planet_id in const.LIST_OBJECTS_VEDIC:
            planet = d40_chart.getObject(planet_id)
            self.assertIsNotNone(planet)
        
        # Test the calculation function directly
        for test_lon, sign_type in [
            (self.movable_sign_lon, "movable"),
            (self.fixed_sign_lon, "fixed"),
            (self.dual_sign_lon, "dual")
        ]:
            d40_lon = calculate_d40(test_lon)
            
            # Check that the longitude is valid
            self.assertGreaterEqual(d40_lon, 0)
            self.assertLess(d40_lon, 360)
            
            # Print the result for reference
            sign_num = int(d40_lon / 30)
            sign_lon = d40_lon % 30
            print(f"D40 for {sign_type} sign {test_lon}°: {const.LIST_SIGNS[sign_num]} {sign_lon:.2f}°")
    
    def test_d45_chart(self):
        """Test D45 (Akshavedamsha) chart calculations"""
        # Get the D45 chart
        d45_chart = get_varga_chart(self.chart, D45)
        
        # Check that the chart was created successfully
        self.assertIsNotNone(d45_chart)
        
        # Check that all planets are present
        for planet_id in const.LIST_OBJECTS_VEDIC:
            planet = d45_chart.getObject(planet_id)
            self.assertIsNotNone(planet)
        
        # Test the calculation function directly
        for test_lon, sign_type in [
            (self.movable_sign_lon, "movable"),
            (self.fixed_sign_lon, "fixed"),
            (self.dual_sign_lon, "dual")
        ]:
            d45_lon = calculate_d45(test_lon)
            
            # Check that the longitude is valid
            self.assertGreaterEqual(d45_lon, 0)
            self.assertLess(d45_lon, 360)
            
            # Print the result for reference
            sign_num = int(d45_lon / 30)
            sign_lon = d45_lon % 30
            print(f"D45 for {sign_type} sign {test_lon}°: {const.LIST_SIGNS[sign_num]} {sign_lon:.2f}°")
    
    def test_d60_chart(self):
        """Test D60 (Shashtiamsha) chart calculations"""
        # Get the D60 chart
        d60_chart = get_varga_chart(self.chart, D60)
        
        # Check that the chart was created successfully
        self.assertIsNotNone(d60_chart)
        
        # Check that all planets are present
        for planet_id in const.LIST_OBJECTS_VEDIC:
            planet = d60_chart.getObject(planet_id)
            self.assertIsNotNone(planet)
        
        # Test the calculation function directly
        for test_lon, sign_type in [
            (self.movable_sign_lon, "movable"),
            (self.fixed_sign_lon, "fixed"),
            (self.dual_sign_lon, "dual")
        ]:
            d60_lon = calculate_d60(test_lon)
            
            # Check that the longitude is valid
            self.assertGreaterEqual(d60_lon, 0)
            self.assertLess(d60_lon, 360)
            
            # Print the result for reference
            sign_num = int(d60_lon / 30)
            sign_lon = d60_lon % 30
            print(f"D60 for {sign_type} sign {test_lon}°: {const.LIST_SIGNS[sign_num]} {sign_lon:.2f}°")
    
    def test_vimshopaka_bala(self):
        """Test Vimshopaka Bala calculation"""
        # Calculate Vimshopaka Bala for each planet
        for planet_id in const.LIST_OBJECTS_VEDIC:
            vimshopaka_bala = get_vimshopaka_bala(self.chart, planet_id)
            
            # Check that the result is a dictionary
            self.assertIsInstance(vimshopaka_bala, dict)
            
            # Check that all required keys are present
            self.assertIn('planet', vimshopaka_bala)
            self.assertIn('vimshopaka_bala', vimshopaka_bala)
            self.assertIn('max_possible', vimshopaka_bala)
            self.assertIn('percentage', vimshopaka_bala)
            
            # Check that the planet ID is correct
            self.assertEqual(vimshopaka_bala['planet'], planet_id)
            
            # Check that the Vimshopaka Bala is within the valid range
            self.assertGreaterEqual(vimshopaka_bala['vimshopaka_bala'], 0.0)
            self.assertLessEqual(vimshopaka_bala['vimshopaka_bala'], vimshopaka_bala['max_possible'])
            
            # Check that the percentage is within the valid range
            self.assertGreaterEqual(vimshopaka_bala['percentage'], 0.0)
            self.assertLessEqual(vimshopaka_bala['percentage'], 100.0)
            
            # Print the result for reference
            print(f"Vimshopaka Bala for {planet_id}: {vimshopaka_bala['vimshopaka_bala']:.2f} ({vimshopaka_bala['percentage']:.2f}%)")
    
    def test_varga_longitude_consistency(self):
        """Test consistency of varga longitude calculations"""
        # Test that get_varga_longitude and the specific calculation functions produce the same results
        for test_lon in [self.movable_sign_lon, self.fixed_sign_lon, self.dual_sign_lon]:
            # D20
            d20_lon1 = calculate_d20(test_lon)
            d20_lon2 = get_varga_longitude(test_lon, D20)
            self.assertAlmostEqual(d20_lon1, d20_lon2, places=6)
            
            # D24
            d24_lon1 = calculate_d24(test_lon)
            d24_lon2 = get_varga_longitude(test_lon, D24)
            self.assertAlmostEqual(d24_lon1, d24_lon2, places=6)
            
            # D27
            d27_lon1 = calculate_d27(test_lon)
            d27_lon2 = get_varga_longitude(test_lon, D27)
            self.assertAlmostEqual(d27_lon1, d27_lon2, places=6)
            
            # D30
            d30_lon1 = calculate_d30(test_lon)
            d30_lon2 = get_varga_longitude(test_lon, D30)
            self.assertAlmostEqual(d30_lon1, d30_lon2, places=6)
            
            # D40
            d40_lon1 = calculate_d40(test_lon)
            d40_lon2 = get_varga_longitude(test_lon, D40)
            self.assertAlmostEqual(d40_lon1, d40_lon2, places=6)
            
            # D45
            d45_lon1 = calculate_d45(test_lon)
            d45_lon2 = get_varga_longitude(test_lon, D45)
            self.assertAlmostEqual(d45_lon1, d45_lon2, places=6)
            
            # D60
            d60_lon1 = calculate_d60(test_lon)
            d60_lon2 = get_varga_longitude(test_lon, D60)
            self.assertAlmostEqual(d60_lon1, d60_lon2, places=6)


if __name__ == '__main__':
    unittest.main()
