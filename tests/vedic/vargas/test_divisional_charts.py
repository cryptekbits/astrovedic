#!/usr/bin/env python3
"""
Test Divisional Chart Calculations

This script tests the divisional chart calculations in astrovedic.
"""

import unittest
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic import const
from astrovedic.vedic.vargas import (
    D1, D2, D3, D4, D7, D9, D10, D12, 
    D16, D20, D24, D27, D30, D40, D45, D60,
    get_varga_chart, get_varga_longitude
)

class TestDivisionalCharts(unittest.TestCase):
    """Test case for divisional chart calculations"""
    
    def setUp(self):
        """Set up test case"""
        # Create a chart for the reference date
        date = Datetime('2025/04/09', '20:51', '+05:30')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart = Chart(date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
    
    def test_d1_chart(self):
        """Test D1 (Rashi) chart calculations"""
        # D1 chart should be the same as the birth chart
        d1_chart = get_varga_chart(self.chart, D1)
        
        # Check that the longitudes are the same
        for planet_id in const.LIST_OBJECTS_VEDIC:
            birth_planet = self.chart.getObject(planet_id)
            d1_planet = d1_chart.getObject(planet_id)
            self.assertEqual(birth_planet.lon, d1_planet.lon)
    
    def test_d9_chart(self):
        """Test D9 (Navamsha) chart calculations"""
        # Get the D9 chart
        d9_chart = get_varga_chart(self.chart, D9)
        
        # Test a few specific planets
        sun = self.chart.getObject(const.SUN)
        d9_sun = d9_chart.getObject(const.SUN)
        
        # Calculate the expected D9 longitude manually
        sun_sign_num = int(sun.lon / 30)
        sun_sign_lon = sun.lon % 30
        sun_navamsha = int(sun_sign_lon / (30/9))
        
        # Determine the element of the sign
        element = sun_sign_num % 4  # 0 = fire, 1 = earth, 2 = air, 3 = water
        
        # Calculate the starting sign based on the element
        if element == 0:  # Fire signs
            start_sign = 0  # Aries
        elif element == 1:  # Earth signs
            start_sign = 9  # Capricorn
        elif element == 2:  # Air signs
            start_sign = 6  # Libra
        else:  # Water signs
            start_sign = 3  # Cancer
        
        # Calculate the expected sign
        expected_sign_num = (start_sign + sun_navamsha) % 12
        
        # Calculate the expected longitude within the sign
        expected_sign_lon = (sun_sign_lon % (30/9)) * 9
        
        # Calculate the expected total longitude
        expected_lon = expected_sign_num * 30 + expected_sign_lon
        
        # Check that the longitude is correct (within a small margin of error)
        self.assertAlmostEqual(d9_sun.lon, expected_lon, places=6)
    
    def test_all_varga_types(self):
        """Test all varga types"""
        for varga_type in [D1, D2, D3, D4, D7, D9, D10, D12, D16, D20, D24, D27, D30, D40, D45, D60]:
            # Get the varga chart
            varga_chart = get_varga_chart(self.chart, varga_type)
            
            # Check that the chart was created successfully
            self.assertIsNotNone(varga_chart)
            
            # Check that all planets are present
            for planet_id in const.LIST_OBJECTS_VEDIC:
                planet = varga_chart.getObject(planet_id)
                self.assertIsNotNone(planet)
    
    def test_varga_longitude_function(self):
        """Test the get_varga_longitude function"""
        # Test a few specific longitudes
        test_lon = 45.5  # Taurus 15°30'
        
        # Test D1 (should be the same)
        d1_lon = get_varga_longitude(test_lon, D1)
        self.assertEqual(d1_lon, test_lon)
        
        # Test D9 (Navamsha)
        d9_lon = get_varga_longitude(test_lon, D9)
        
        # Calculate the expected D9 longitude manually
        sign_num = int(test_lon / 30)
        sign_lon = test_lon % 30
        navamsha = int(sign_lon / (30/9))
        
        # Determine the element of the sign
        element = sign_num % 4  # 0 = fire, 1 = earth, 2 = air, 3 = water
        
        # Calculate the starting sign based on the element
        if element == 0:  # Fire signs
            start_sign = 0  # Aries
        elif element == 1:  # Earth signs
            start_sign = 9  # Capricorn
        elif element == 2:  # Air signs
            start_sign = 6  # Libra
        else:  # Water signs
            start_sign = 3  # Cancer
        
        # Calculate the expected sign
        expected_sign_num = (start_sign + navamsha) % 12
        
        # Calculate the expected longitude within the sign
        expected_sign_lon = (sign_lon % (30/9)) * 9
        
        # Calculate the expected total longitude
        expected_lon = expected_sign_num * 30 + expected_sign_lon
        
        # Check that the longitude is correct (within a small margin of error)
        self.assertAlmostEqual(d9_lon, expected_lon, places=6)

if __name__ == '__main__':
    unittest.main()
