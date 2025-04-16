"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module tests the ayanamsa and house system selection functionality.
"""

import unittest
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic import const
from astrovedic.vedic.ayanamsa import AyanamsaManager
from astrovedic.vedic.houses import HouseSystemManager
from astrovedic.vedic.config import ChartConfiguration
from astrovedic.vedic.api import VedicChart, create_vedic_chart, create_kp_chart


class TestAyanamsaHouseSystem(unittest.TestCase):
    """Test the ayanamsa and house system selection functionality."""

    def setUp(self):
        """Set up test data."""
        self.date = Datetime('2025/04/09', '20:51', '+05:30')
        self.pos = GeoPos(12.9716, 77.5946)  # Bangalore, India

    def test_ayanamsa_manager(self):
        """Test the AyanamsaManager class."""
        # Test default ayanamsa
        default_ayanamsa = AyanamsaManager.get_default()
        self.assertEqual(default_ayanamsa, const.AY_LAHIRI)

        # Test setting default ayanamsa
        AyanamsaManager.set_default(const.AY_RAMAN)
        self.assertEqual(AyanamsaManager.get_default(), const.AY_RAMAN)

        # Reset default ayanamsa
        AyanamsaManager.set_default(const.AY_LAHIRI)
        self.assertEqual(AyanamsaManager.get_default(), const.AY_LAHIRI)

        # Test KP default ayanamsa
        kp_default_ayanamsa = AyanamsaManager.get_kp_default()
        self.assertEqual(kp_default_ayanamsa, const.AY_KRISHNAMURTI)

        # Test getting recommended house systems
        recommended_house_systems = AyanamsaManager.get_recommended_house_systems(const.AY_LAHIRI)
        self.assertIn(const.HOUSES_WHOLE_SIGN, recommended_house_systems)

        # Test getting all ayanamsas
        all_ayanamsas = AyanamsaManager.get_all_ayanamsas()
        self.assertIn(const.AY_LAHIRI, all_ayanamsas)
        self.assertIn(const.AY_KRISHNAMURTI, all_ayanamsas)

        # Test getting ayanamsas by category
        primary_ayanamsas = AyanamsaManager.get_ayanamsas_by_category('primary')
        self.assertIn(const.AY_LAHIRI, primary_ayanamsas)
        self.assertIn(const.AY_RAMAN, primary_ayanamsas)

        # Test getting ayanamsa info
        lahiri_info = AyanamsaManager.get_ayanamsa_info(const.AY_LAHIRI)
        self.assertEqual(lahiri_info['name'], 'Lahiri')
        self.assertEqual(lahiri_info['category'], 'primary')

        # Test is_supported
        self.assertTrue(AyanamsaManager.is_supported(const.AY_LAHIRI))
        self.assertFalse(AyanamsaManager.is_supported('Invalid Ayanamsa'))

    def test_house_system_manager(self):
        """Test the HouseSystemManager class."""
        # Test default house system
        default_house_system = HouseSystemManager.get_default()
        self.assertEqual(default_house_system, const.HOUSES_WHOLE_SIGN)

        # Test setting default house system
        HouseSystemManager.set_default(const.HOUSES_EQUAL)
        self.assertEqual(HouseSystemManager.get_default(), const.HOUSES_EQUAL)

        # Reset default house system
        HouseSystemManager.set_default(const.HOUSES_WHOLE_SIGN)
        self.assertEqual(HouseSystemManager.get_default(), const.HOUSES_WHOLE_SIGN)

        # Test KP default house system
        kp_default_house_system = HouseSystemManager.get_kp_default()
        self.assertEqual(kp_default_house_system, const.HOUSES_PLACIDUS)

        # Test getting recommended ayanamsas
        recommended_ayanamsas = HouseSystemManager.get_recommended_ayanamsas(const.HOUSES_WHOLE_SIGN)
        self.assertIn(const.AY_LAHIRI, recommended_ayanamsas)
        self.assertIn(const.AY_RAMAN, recommended_ayanamsas)

        # Test getting all house systems
        all_house_systems = HouseSystemManager.get_all_house_systems()
        self.assertIn(const.HOUSES_WHOLE_SIGN, all_house_systems)
        self.assertIn(const.HOUSES_PLACIDUS, all_house_systems)

        # Test getting house systems by category
        vedic_house_systems = HouseSystemManager.get_house_systems_by_category('vedic')
        self.assertIn(const.HOUSES_WHOLE_SIGN, vedic_house_systems)
        self.assertIn(const.HOUSES_EQUAL, vedic_house_systems)

        # Test getting house system info
        whole_sign_info = HouseSystemManager.get_house_system_info(const.HOUSES_WHOLE_SIGN)
        self.assertEqual(whole_sign_info['name'], 'Whole Sign')
        self.assertEqual(whole_sign_info['category'], 'vedic')

        # Test is_supported
        self.assertTrue(HouseSystemManager.is_supported(const.HOUSES_WHOLE_SIGN))
        self.assertFalse(HouseSystemManager.is_supported('Invalid House System'))

    def test_chart_configuration(self):
        """Test the ChartConfiguration class."""
        # Test default configuration
        config = ChartConfiguration()
        self.assertEqual(config.ayanamsa, const.AY_LAHIRI)
        self.assertEqual(config.house_system, const.HOUSES_WHOLE_SIGN)

        # Test KP configuration
        kp_config = ChartConfiguration(is_kp=True)
        self.assertEqual(kp_config.ayanamsa, const.AY_KRISHNAMURTI)
        self.assertEqual(kp_config.house_system, const.HOUSES_PLACIDUS)

        # Test custom configuration
        custom_config = ChartConfiguration(const.AY_RAMAN, const.HOUSES_EQUAL)
        self.assertEqual(custom_config.ayanamsa, const.AY_RAMAN)
        self.assertEqual(custom_config.house_system, const.HOUSES_EQUAL)

        # Test validation
        custom_config.validate()  # Should not raise an exception

        # Test recommended combination
        self.assertTrue(config.is_recommended_combination())
        self.assertTrue(kp_config.is_recommended_combination())
        self.assertTrue(custom_config.is_recommended_combination())

        # Test non-recommended combination
        non_recommended_config = ChartConfiguration(const.AY_KRISHNAMURTI, const.HOUSES_WHOLE_SIGN)
        self.assertFalse(non_recommended_config.is_recommended_combination())

        # Test warnings
        warnings = non_recommended_config.get_warnings()
        self.assertTrue(len(warnings) > 0)
        self.assertIn('not recommended', warnings[0])

    def test_chart_creation(self):
        """Test chart creation with different ayanamsas and house systems."""
        # Test default chart
        chart = Chart(self.date, self.pos)
        self.assertEqual(chart.ayanamsa, const.AY_LAHIRI)
        self.assertEqual(chart.hsys, const.HOUSES_WHOLE_SIGN)

        # Test chart with custom ayanamsa and house system
        chart = Chart(self.date, self.pos, ayanamsa=const.AY_RAMAN, hsys=const.HOUSES_EQUAL)
        self.assertEqual(chart.ayanamsa, const.AY_RAMAN)
        self.assertEqual(chart.hsys, const.HOUSES_EQUAL)

        # Test KP chart
        chart = Chart(self.date, self.pos, is_kp=True)
        self.assertEqual(chart.ayanamsa, const.AY_KRISHNAMURTI)
        self.assertEqual(chart.hsys, const.HOUSES_PLACIDUS)

        # Test backward compatibility with mode parameter
        chart = Chart(self.date, self.pos, mode=const.AY_RAMAN)
        self.assertEqual(chart.ayanamsa, const.AY_RAMAN)
        self.assertEqual(chart.mode, const.AY_RAMAN)

    def test_vedic_chart_creation(self):
        """Test VedicChart creation with different ayanamsas and house systems."""
        # Test default VedicChart
        vedic_chart = VedicChart.from_data(self.date, self.pos)
        self.assertEqual(vedic_chart.ayanamsa, const.AY_LAHIRI)
        self.assertEqual(vedic_chart.chart.hsys, const.HOUSES_WHOLE_SIGN)

        # Test VedicChart with custom ayanamsa and house system
        vedic_chart = VedicChart.from_data(self.date, self.pos, const.HOUSES_EQUAL, const.AY_RAMAN)
        self.assertEqual(vedic_chart.ayanamsa, const.AY_RAMAN)
        self.assertEqual(vedic_chart.chart.hsys, const.HOUSES_EQUAL)

        # Test KP chart
        kp_chart = VedicChart.kp_chart(self.date, self.pos)
        self.assertEqual(kp_chart.ayanamsa, const.AY_KRISHNAMURTI)
        self.assertEqual(kp_chart.chart.hsys, const.HOUSES_PLACIDUS)

        # Test from_date_place
        vedic_chart = VedicChart.from_date_place('2025/04/09', '20:51', 12.9716, 77.5946, '+05:30')
        self.assertEqual(vedic_chart.ayanamsa, const.AY_LAHIRI)
        self.assertEqual(vedic_chart.chart.hsys, const.HOUSES_WHOLE_SIGN)

    def test_helper_functions(self):
        """Test helper functions for chart creation."""
        # Test create_vedic_chart
        vedic_chart = create_vedic_chart('2025/04/09', '20:51', 12.9716, 77.5946, '+05:30')
        self.assertEqual(vedic_chart.ayanamsa, const.AY_LAHIRI)
        self.assertEqual(vedic_chart.chart.hsys, const.HOUSES_WHOLE_SIGN)

        # Test create_kp_chart
        kp_chart = create_kp_chart('2025/04/09', '20:51', 12.9716, 77.5946, '+05:30')
        self.assertEqual(kp_chart.ayanamsa, const.AY_KRISHNAMURTI)
        self.assertEqual(kp_chart.chart.hsys, const.HOUSES_PLACIDUS)


if __name__ == '__main__':
    unittest.main()
