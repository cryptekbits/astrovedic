#!/usr/bin/env python3
"""
Test Vedic Object Representation

This script tests the VedicBody class and related utility functions.
"""

import unittest
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib.object import VedicBody
from flatlib.factory import AstronomicalObjectFactory
from flatlib.vedic.utils import to_vedic_object, to_vedic_chart


class TestVedicObject(unittest.TestCase):
    """Test case for Vedic object representation"""
    
    def setUp(self):
        """Set up test case"""
        # Create a chart for the reference date
        date = Datetime('2025/04/09', '20:51', '+05:30')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart = Chart(date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
    
    def test_vedic_body_creation(self):
        """Test VedicBody creation"""
        # Create a VedicBody object
        vedic_body = VedicBody()
        
        # Check that it has the expected attributes
        self.assertIsNone(vedic_body.nakshatra)
        self.assertIsNone(vedic_body.nakshatra_lord)
        self.assertIsNone(vedic_body.nakshatra_pada)
        self.assertIsNone(vedic_body.nakshatra_degree)
        
        self.assertEqual(vedic_body.sthana_bala, 0.0)
        self.assertEqual(vedic_body.dig_bala, 0.0)
        self.assertEqual(vedic_body.kala_bala, 0.0)
        self.assertEqual(vedic_body.cheshta_bala, 0.0)
        self.assertEqual(vedic_body.naisargika_bala, 0.0)
        self.assertEqual(vedic_body.drig_bala, 0.0)
        self.assertEqual(vedic_body.total_shadbala, 0.0)
        
        self.assertEqual(vedic_body.varga_positions, {})
        self.assertIsNone(vedic_body.avastha)
        self.assertEqual(vedic_body.graha_drishti, [])
        self.assertEqual(vedic_body.aspects_received, [])
        self.assertEqual(vedic_body.ishta_phala, 0.0)
        self.assertEqual(vedic_body.kashta_phala, 0.0)
        self.assertEqual(vedic_body.vimsopaka_bala, 0.0)
    
    def test_vedic_body_methods(self):
        """Test VedicBody methods"""
        # Create a VedicBody object with some attributes
        vedic_body = VedicBody()
        vedic_body.nakshatra = 'Pushya'
        vedic_body.nakshatra_lord = const.SATURN
        vedic_body.nakshatra_pada = 2
        vedic_body.nakshatra_degree = 10.5
        
        vedic_body.sthana_bala = 5.0
        vedic_body.dig_bala = 4.0
        vedic_body.kala_bala = 3.0
        vedic_body.cheshta_bala = 2.0
        vedic_body.naisargika_bala = 1.0
        vedic_body.drig_bala = 0.5
        vedic_body.total_shadbala = 15.5
        
        vedic_body.varga_positions = {9: 120.5}  # D9 position
        vedic_body.lon = 90.5  # D1 position
        
        # Test get_nakshatra_info method
        nakshatra_info = vedic_body.get_nakshatra_info()
        self.assertEqual(nakshatra_info['name'], 'Pushya')
        self.assertEqual(nakshatra_info['lord'], const.SATURN)
        self.assertEqual(nakshatra_info['pada'], 2)
        self.assertEqual(nakshatra_info['degree'], 10.5)
        
        # Test get_shadbala_info method
        shadbala_info = vedic_body.get_shadbala_info()
        self.assertEqual(shadbala_info['sthana_bala'], 5.0)
        self.assertEqual(shadbala_info['dig_bala'], 4.0)
        self.assertEqual(shadbala_info['kala_bala'], 3.0)
        self.assertEqual(shadbala_info['cheshta_bala'], 2.0)
        self.assertEqual(shadbala_info['naisargika_bala'], 1.0)
        self.assertEqual(shadbala_info['drig_bala'], 0.5)
        self.assertEqual(shadbala_info['total_shadbala'], 15.5)
        
        # Test get_varga_position method
        self.assertEqual(vedic_body.get_varga_position(9), 120.5)
        self.assertIsNone(vedic_body.get_varga_position(10))
        
        # Test set_varga_position method
        vedic_body.set_varga_position(10, 150.5)
        self.assertEqual(vedic_body.get_varga_position(10), 150.5)
        
        # Test is_vargottama method
        self.assertFalse(vedic_body.is_vargottama())
        
        # Set D9 position to be in the same sign as D1
        vedic_body.set_varga_position(9, 95.5)  # Same sign as D1 (Cancer)
        self.assertTrue(vedic_body.is_vargottama())
    
    def test_to_vedic_object(self):
        """Test to_vedic_object function"""
        # Get a regular object from the chart
        sun = self.chart.getObject(const.SUN)
        
        # Convert it to a VedicBody object
        vedic_sun = to_vedic_object(sun, self.chart)
        
        # Check that it's a VedicBody object
        self.assertIsInstance(vedic_sun, VedicBody)
        
        # Check that it has the expected attributes
        self.assertIsNotNone(vedic_sun.nakshatra)
        self.assertIsNotNone(vedic_sun.nakshatra_lord)
        self.assertIsNotNone(vedic_sun.nakshatra_pada)
        self.assertIsNotNone(vedic_sun.nakshatra_degree)
        
        # Check that it has the same basic attributes as the original object
        self.assertEqual(vedic_sun.id, sun.id)
        self.assertEqual(vedic_sun.lon, sun.lon)
        self.assertEqual(vedic_sun.lat, sun.lat)
        self.assertEqual(vedic_sun.sign, sun.sign)
    
    def test_to_vedic_chart(self):
        """Test to_vedic_chart function"""
        # Convert the chart to a Vedic chart
        vedic_chart = to_vedic_chart(self.chart)
        
        # Check that it's a Chart object
        self.assertIsInstance(vedic_chart, Chart)
        
        # Check that it has the same basic attributes as the original chart
        self.assertEqual(vedic_chart.date.jd, self.chart.date.jd)
        self.assertEqual(vedic_chart.pos.lat, self.chart.pos.lat)
        self.assertEqual(vedic_chart.pos.lon, self.chart.pos.lon)
        
        # Check that the objects are VedicBody objects
        for obj_id in const.LIST_OBJECTS_VEDIC:
            if obj_id in vedic_chart.objects:
                obj = vedic_chart.getObject(obj_id)
                self.assertIsInstance(obj, VedicBody)
                self.assertIsNotNone(obj.nakshatra)
                self.assertIsNotNone(obj.nakshatra_lord)
                self.assertIsNotNone(obj.nakshatra_pada)
                self.assertIsNotNone(obj.nakshatra_degree)


if __name__ == '__main__':
    unittest.main()
