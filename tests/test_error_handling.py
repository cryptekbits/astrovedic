import unittest
from unittest.mock import patch, MagicMock

from astrovedic import const
from astrovedic.ephem import eph
from astrovedic.ephem import swe
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart


class ErrorHandlingTests(unittest.TestCase):

    def setUp(self):
        self.date = Datetime('2015/03/13', '17:00', '+00:00')
        self.pos = GeoPos('38n32', '8w54')

    @patch('astrovedic.ephem.swe.sweObject')
    def test_getObject_handles_exception(self, mock_sweObject):
        """
        Test that getObject handles exceptions from sweObject

        Note: This test intentionally mocks sweObject to raise an exception.
        The test will generate an ERROR log message like:
        - ERROR - Error calculating object Sun: Test exception

        This message is expected and indicates that the error handling mechanism
        is correctly catching exceptions and returning a valid object with default
        values when the calculation fails.
        """
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

    # Note: PARS_FORTUNA test removed as it's not used in Vedic astrology implementation

    @patch('astrovedic.ephem.tools.syzygyJD')
    def test_getObject_handles_syzygy_exception(self, mock_syzygyJD):
        """
        Test that getObject handles exceptions when calculating Syzygy

        Note: This test intentionally mocks syzygyJD to raise an exception.
        The test will generate an ERROR log message like:
        - ERROR - Error calculating Syzygy: Test exception

        This message is expected and indicates that the error handling mechanism
        is correctly catching exceptions during Syzygy calculations and returning
        a valid object with default values when the calculation fails.
        """
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

    @patch('astrovedic.ephem.swe.swe_object')
    def test_get_object_handles_exception(self, mock_swe_object):
        """
        Test that get_object handles exceptions from swe_object

        Note: This test intentionally mocks swe_object to raise an exception.
        The test will generate an ERROR log message like:
        - ERROR - Error calculating object Sun: Test exception

        This message is expected and indicates that the error handling mechanism
        is correctly catching exceptions and returning a valid object with default
        values when the calculation fails.
        """
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
        """
        Test that Chart creation handles invalid objects gracefully

        Note: This test intentionally creates a chart with a non-existent object.
        The test will generate an ERROR log message like:
        - ERROR - Error calculating object NonExistentObject: 'NonExistentObject'

        This message is expected and indicates that the chart creation process
        is correctly handling invalid objects by creating placeholder objects
        with default values when the actual object cannot be calculated.
        """
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
