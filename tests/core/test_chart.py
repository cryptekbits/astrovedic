import unittest

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos


class ChartTests(unittest.TestCase):

    def setUp(self):
        self.date = Datetime('2015/03/13', '17:00', '+00:00')
        self.pos = GeoPos('38n32', '8w54')

    def test_chart_creation(self):
        """Test that a chart can be created successfully."""
        chart = Chart(self.date, self.pos, hsys=const.HOUSES_MORINUS)
        self.assertIsNotNone(chart)
        self.assertEqual(chart.hsys, const.HOUSES_MORINUS)
