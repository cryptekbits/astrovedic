import unittest
from unittest.mock import patch, MagicMock

from flatlib import const
from flatlib.ephem import eph
from flatlib.ephem import swe
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart


class ErrorHandlingTests(unittest.TestCase):

    def setUp(self):
        self.date = Datetime('2015/03/13', '17:00', '+00:00')
        self.pos = GeoPos('38n32', '8w54')

    @patch('flatlib.ephem.swe.sweObject')
    def test_getObject_handles_exception(self, mock_sweObject):
        """Test that getObject handles exceptions from sweObject"""
        # Setup mock to raise an exception
        mock_sweObject.side_effect = Exception("Test exception")
        
        # Call the function that should handle the exception
        obj = eph.getObject(const.SUN, self.date.jd, self.pos.lat, self.pos.lon)
        
        # Verify that we got a valid object with default values
        self.assertEqual(obj['id'], const.SUN)
        self.assertEqual(obj['lon'], 0.0)
        self.assertEqual(obj['lat'], 0.0)
        self.assertEqual(obj['sign'], const.ARIES)
        self.assertEqual(obj['signlon'], 0.0)
        self.assertEqual(obj['lonspeed'], 0.0)
        self.assertEqual(obj['latspeed'], 0.0)

    @patch('flatlib.ephem.tools.pfLon')
    def test_getObject_handles_pars_fortuna_exception(self, mock_pfLon):
        """Test that getObject handles exceptions when calculating Pars Fortuna"""
        # Setup mock to raise an exception
        mock_pfLon.side_effect = Exception("Test exception")
        
        # Call the function that should handle the exception
        obj = eph.getObject(const.PARS_FORTUNA, self.date.jd, self.pos.lat, self.pos.lon)
        
        # Verify that we got a valid object with default values
        self.assertEqual(obj['id'], const.PARS_FORTUNA)
        self.assertEqual(obj['lon'], 0.0)
        self.assertEqual(obj['lat'], 0.0)
        self.assertEqual(obj['sign'], const.ARIES)
        self.assertEqual(obj['signlon'], 0.0)
        self.assertEqual(obj['lonspeed'], 0.0)
        self.assertEqual(obj['latspeed'], 0.0)

    @patch('flatlib.ephem.tools.syzygyJD')
    def test_getObject_handles_syzygy_exception(self, mock_syzygyJD):
        """Test that getObject handles exceptions when calculating Syzygy"""
        # Setup mock to raise an exception
        mock_syzygyJD.side_effect = Exception("Test exception")
        
        # Call the function that should handle the exception
        obj = eph.getObject(const.SYZYGY, self.date.jd, self.pos.lat, self.pos.lon)
        
        # Verify that we got a valid object with default values
        self.assertEqual(obj['id'], const.SYZYGY)
        self.assertEqual(obj['lon'], 0.0)
        self.assertEqual(obj['lat'], 0.0)
        self.assertEqual(obj['sign'], const.ARIES)
        self.assertEqual(obj['signlon'], 0.0)
        self.assertEqual(obj['lonspeed'], 0.0)
        self.assertEqual(obj['latspeed'], 0.0)

    @patch('flatlib.ephem.swe.swe_object')
    def test_get_object_handles_exception(self, mock_swe_object):
        """Test that get_object handles exceptions from swe_object"""
        # Setup mock to raise an exception
        mock_swe_object.side_effect = Exception("Test exception")
        
        # Call the function that should handle the exception
        obj = eph.get_object(const.SUN, self.date.jd, self.pos.lat, self.pos.lon)
        
        # Verify that we got a valid object with default values
        self.assertEqual(obj['id'], const.SUN)
        self.assertEqual(obj['lon'], 0.0)
        self.assertEqual(obj['lat'], 0.0)
        self.assertEqual(obj['sign'], const.ARIES)
        self.assertEqual(obj['signlon'], 0.0)
        self.assertEqual(obj['lonspeed'], 0.0)
        self.assertEqual(obj['latspeed'], 0.0)

    def test_chart_creation_with_invalid_object(self):
        """Test that Chart creation handles invalid objects gracefully"""
        # Create a chart with a non-existent object
        chart = Chart(self.date, self.pos, IDs=[const.SUN, 'NonExistentObject'])
        
        # Verify that the chart was created successfully
        self.assertIsNotNone(chart)
        
        # Verify that we can access the valid object
        sun = chart.getObject(const.SUN)
        self.assertEqual(sun.id, const.SUN)
        
        # Verify that we can access the invalid object (it should have default values)
        invalid_obj = chart.getObject('NonExistentObject')
        self.assertEqual(invalid_obj.id, 'NonExistentObject')
        self.assertEqual(invalid_obj.lon, 0.0)
        self.assertEqual(invalid_obj.lat, 0.0)


if __name__ == '__main__':
    unittest.main()
