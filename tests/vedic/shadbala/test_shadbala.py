#!/usr/bin/env python3
"""
Test Shadbala Calculations

This script tests the Shadbala (six-fold planetary strength) calculations in astrovedic.
"""

import unittest
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic import const
from astrovedic.vedic.shadbala import (
    get_shadbala, get_all_shadbala, get_bhava_bala,
    STHANA_BALA, DIG_BALA, KALA_BALA,
    CHESHTA_BALA, NAISARGIKA_BALA, DRIG_BALA,
    MINIMUM_SHADBALA
)

class TestShadbala(unittest.TestCase):
    """Test case for Shadbala calculations"""

    def setUp(self):
        """Set up test case"""
        # Create a chart for the reference date
        date = Datetime('2025/04/09', '20:51', '+05:30')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart = Chart(date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)

    def test_get_shadbala(self):
        """Test get_shadbala function"""
        # Calculate Shadbala for the Sun
        sun_shadbala = get_shadbala(self.chart, const.SUN)

        # Check that all components are present
        self.assertIn('sthana_bala', sun_shadbala)
        self.assertIn('dig_bala', sun_shadbala)
        self.assertIn('kala_bala', sun_shadbala)
        self.assertIn('cheshta_bala', sun_shadbala)
        self.assertIn('naisargika_bala', sun_shadbala)
        self.assertIn('drig_bala', sun_shadbala)
        self.assertIn('total_shadbala', sun_shadbala)
        self.assertIn('ishta_phala', sun_shadbala)
        self.assertIn('kashta_phala', sun_shadbala)
        self.assertIn('vimsopaka_bala', sun_shadbala)
        self.assertIn('minimum_required', sun_shadbala)
        self.assertIn('is_sufficient', sun_shadbala)

        # Check that the total Shadbala is calculated correctly
        total_virupas = (
            sun_shadbala['sthana_bala']['total'] +
            sun_shadbala['dig_bala']['value'] +
            sun_shadbala['kala_bala']['total'] +
            sun_shadbala['cheshta_bala']['value'] +
            sun_shadbala['naisargika_bala']['value'] +
            sun_shadbala['drig_bala']['value']
        )
        self.assertAlmostEqual(sun_shadbala['total_shadbala']['total_virupas'], total_virupas)

        # Check that the total Rupas is calculated correctly
        self.assertAlmostEqual(sun_shadbala['total_shadbala']['total_rupas'], total_virupas / 60.0)

    def test_get_all_shadbala(self):
        """Test get_all_shadbala function"""
        # Calculate Shadbala for all planets
        all_shadbala = get_all_shadbala(self.chart)

        # Check that all planets are present
        for planet_id in const.LIST_OBJECTS_VEDIC:
            self.assertIn(planet_id, all_shadbala)

        # Check that summary information is present
        self.assertIn('summary', all_shadbala)
        self.assertIn('strongest', all_shadbala)
        self.assertIn('weakest', all_shadbala)

        # Check that the strongest and weakest planets are valid
        self.assertIn(all_shadbala['strongest'], const.LIST_OBJECTS_VEDIC)
        self.assertIn(all_shadbala['weakest'], const.LIST_OBJECTS_VEDIC)

    def test_get_bhava_bala(self):
        """Test get_bhava_bala function"""
        # Calculate Bhava Bala for the 1st house
        house1_bala = get_bhava_bala(self.chart, const.HOUSE1)

        # Check that all components are present
        self.assertIn('bhavadhipati_bala', house1_bala)
        self.assertIn('bhava_digbala', house1_bala)
        self.assertIn('bhava_drishti_bala', house1_bala)
        self.assertIn('bhava_sthana_bala', house1_bala)
        self.assertIn('total', house1_bala)
        self.assertIn('description', house1_bala)

        # Check that the total Bhava Bala is calculated correctly
        total = (
            house1_bala['bhavadhipati_bala']['value'] +
            house1_bala['bhava_digbala']['value'] +
            house1_bala['bhava_drishti_bala']['value'] +
            house1_bala['bhava_sthana_bala']['value']
        )
        self.assertAlmostEqual(house1_bala['total'], total)

    def test_sthana_bala(self):
        """Test Sthana Bala calculations"""
        # Calculate Shadbala for the Sun
        sun_shadbala = get_shadbala(self.chart, const.SUN)

        # Check that all components of Sthana Bala are present
        self.assertIn('uchcha_bala', sun_shadbala['sthana_bala'])
        self.assertIn('saptavarga_bala', sun_shadbala['sthana_bala'])
        self.assertIn('ojha_yugma_bala', sun_shadbala['sthana_bala'])
        self.assertIn('kendradi_bala', sun_shadbala['sthana_bala'])
        self.assertIn('drekkana_bala', sun_shadbala['sthana_bala'])

        # Check that the total Sthana Bala is calculated correctly
        total = (
            sun_shadbala['sthana_bala']['uchcha_bala']['value'] +
            sun_shadbala['sthana_bala']['saptavarga_bala']['value'] +
            sun_shadbala['sthana_bala']['ojha_yugma_bala']['value'] +
            sun_shadbala['sthana_bala']['kendradi_bala']['value'] +
            sun_shadbala['sthana_bala']['drekkana_bala']['value']
        )
        self.assertAlmostEqual(sun_shadbala['sthana_bala']['total'], total)

    def test_dig_bala(self):
        """Test Dig Bala calculations"""
        # Calculate Shadbala for the Sun
        sun_shadbala = get_shadbala(self.chart, const.SUN)

        # Check that Dig Bala is calculated
        self.assertIn('value', sun_shadbala['dig_bala'])
        self.assertIn('description', sun_shadbala['dig_bala'])
        self.assertIn('preferred_direction', sun_shadbala['dig_bala'])
        self.assertIn('preferred_house', sun_shadbala['dig_bala'])
        self.assertIn('actual_house', sun_shadbala['dig_bala'])

        # Check that the preferred direction for the Sun is South
        self.assertEqual(sun_shadbala['dig_bala']['preferred_direction'], 'South')

        # Check that the preferred house for the Sun is 10
        self.assertEqual(sun_shadbala['dig_bala']['preferred_house'], 10)

    def test_kala_bala(self):
        """Test Kala Bala calculations"""
        # Calculate Shadbala for the Sun
        sun_shadbala = get_shadbala(self.chart, const.SUN)

        # Check that all components of Kala Bala are present
        self.assertIn('nathonnatha_bala', sun_shadbala['kala_bala'])
        self.assertIn('paksha_bala', sun_shadbala['kala_bala'])
        self.assertIn('tribhaga_bala', sun_shadbala['kala_bala'])
        self.assertIn('abda_bala', sun_shadbala['kala_bala'])
        self.assertIn('masa_bala', sun_shadbala['kala_bala'])
        self.assertIn('vara_bala', sun_shadbala['kala_bala'])
        self.assertIn('hora_bala', sun_shadbala['kala_bala'])
        self.assertIn('ayana_bala', sun_shadbala['kala_bala'])
        self.assertIn('yuddha_bala', sun_shadbala['kala_bala'])

        # Check that the total Kala Bala is calculated correctly
        total = (
            sun_shadbala['kala_bala']['nathonnatha_bala']['value'] +
            sun_shadbala['kala_bala']['paksha_bala']['value'] +
            sun_shadbala['kala_bala']['tribhaga_bala']['value'] +
            sun_shadbala['kala_bala']['abda_bala']['value'] +
            sun_shadbala['kala_bala']['masa_bala']['value'] +
            sun_shadbala['kala_bala']['vara_bala']['value'] +
            sun_shadbala['kala_bala']['hora_bala']['value'] +
            sun_shadbala['kala_bala']['ayana_bala']['value'] +
            sun_shadbala['kala_bala']['yuddha_bala']['value']
        )
        self.assertAlmostEqual(sun_shadbala['kala_bala']['total'], total)

    def test_cheshta_bala(self):
        """Test Cheshta Bala calculations"""
        # Calculate Shadbala for Mars
        mars_shadbala = get_shadbala(self.chart, const.MARS)

        # Check that Cheshta Bala is calculated
        self.assertIn('value', mars_shadbala['cheshta_bala'])
        self.assertIn('description', mars_shadbala['cheshta_bala'])
        self.assertIn('is_retrograde', mars_shadbala['cheshta_bala'])
        self.assertIn('daily_motion', mars_shadbala['cheshta_bala'])
        self.assertIn('max_speed', mars_shadbala['cheshta_bala'])
        self.assertIn('relative_speed', mars_shadbala['cheshta_bala'])

        # Check that the Sun and Moon have special Cheshta Bala calculations
        sun_shadbala = get_shadbala(self.chart, const.SUN)
        moon_shadbala = get_shadbala(self.chart, const.MOON)

        # Sun's Cheshta Bala is based on half of Ayana Bala
        self.assertIn('source', sun_shadbala['cheshta_bala'])
        self.assertEqual(sun_shadbala['cheshta_bala']['source'], 'ayana_bala')

        # Moon's Cheshta Bala is based on half of Paksha Bala
        self.assertIn('source', moon_shadbala['cheshta_bala'])
        self.assertEqual(moon_shadbala['cheshta_bala']['source'], 'paksha_bala')

    def test_naisargika_bala(self):
        """Test Naisargika Bala calculations"""
        # Calculate Shadbala for all planets
        all_shadbala = get_all_shadbala(self.chart)

        # Check that the Sun has the highest Naisargika Bala
        sun_naisargika = all_shadbala[const.SUN]['naisargika_bala']['value']

        for planet_id in const.LIST_OBJECTS_VEDIC:
            if planet_id != const.SUN:
                planet_naisargika = all_shadbala[planet_id]['naisargika_bala']['value']
                self.assertGreaterEqual(sun_naisargika, planet_naisargika)

    def test_drig_bala(self):
        """Test Drig Bala calculations"""
        # Calculate Shadbala for the Sun
        sun_shadbala = get_shadbala(self.chart, const.SUN)

        # Check that Drig Bala is calculated
        self.assertIn('value', sun_shadbala['drig_bala'])
        self.assertIn('description', sun_shadbala['drig_bala'])
        self.assertIn('aspects_received', sun_shadbala['drig_bala'])
        self.assertIn('aspects_cast', sun_shadbala['drig_bala'])

if __name__ == '__main__':
    unittest.main()
