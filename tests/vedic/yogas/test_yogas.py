#!/usr/bin/env python3
"""
Test Yoga Calculations

This script tests the Yoga (planetary combinations) calculations in astrovedic.
"""

import unittest
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic import const
from astrovedic.vedic.yogas import (
    get_all_yogas, get_yoga_data,
    MAHAPURUSHA_YOGA, RAJA_YOGA, DHANA_YOGA,
    NABHASA_YOGA, DOSHA_YOGA, CHANDRA_YOGA
)
from astrovedic.vedic.yogas.mahapurusha import (
    get_mahapurusha_yogas, has_ruchaka_yoga,
    has_bhadra_yoga, has_hamsa_yoga,
    has_malavya_yoga, has_sasa_yoga
)
from astrovedic.vedic.yogas.raja import (
    get_raja_yogas, has_dharmakarmaadhipati_yoga,
    has_gajakesari_yoga, has_amala_yoga,
    has_sreenatha_yoga, has_chandra_mangala_yoga
)
from astrovedic.vedic.yogas.dhana import (
    get_dhana_yogas, has_lakshmi_yoga,
    has_kubera_yoga, has_kalanidhi_yoga,
    has_vasumati_yoga, has_mridanga_yoga
)
from astrovedic.vedic.yogas.nabhasa import (
    get_nabhasa_yogas, has_rajju_yoga,
    has_musala_yoga, has_nala_yoga,
    has_mala_yoga, has_sarpa_yoga
)
from astrovedic.vedic.yogas.dosha import (
    get_dosha_yogas, has_kemadruma_yoga,
    has_daridra_yoga, has_shakat_yoga,
    has_kalasarpa_yoga, has_graha_yuddha
)
from astrovedic.vedic.yogas.chandra import (
    get_chandra_yogas, has_adhi_yoga,
    has_sunapha_yoga, has_anapha_yoga,
    has_durudhura_yoga, has_kemadruma_yoga
)
from astrovedic.vedic.yogas import (
    get_yoga_data
)
from astrovedic.vedic.yogas.analysis import (
    get_yoga_comparison, get_yoga_strength_score
)

class TestYogas(unittest.TestCase):
    """Test case for Yoga calculations"""

    def setUp(self):
        """Set up test case"""
        # Create a chart for the reference date
        date = Datetime('2025/04/09', '20:51', '+05:30')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart = Chart(date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)

    def test_get_all_yogas(self):
        """Test get_all_yogas function"""
        # Calculate all Yogas
        yogas = get_all_yogas(self.chart)

        # Check that all required keys are present
        self.assertIn('mahapurusha_yogas', yogas)
        self.assertIn('raja_yogas', yogas)
        self.assertIn('dhana_yogas', yogas)
        self.assertIn('nabhasa_yogas', yogas)
        self.assertIn('dosha_yogas', yogas)
        self.assertIn('chandra_yogas', yogas)
        self.assertIn('summary', yogas)

        # Check that the summary contains the required keys
        summary = yogas['summary']
        self.assertIn('total_yogas', summary)
        self.assertIn('beneficial_yogas', summary)
        self.assertIn('harmful_yogas', summary)
        self.assertIn('yoga_types', summary)
        self.assertIn('strongest_yoga', summary)

    def test_mahapurusha_yogas(self):
        """Test Mahapurusha Yoga calculations"""
        # Calculate Mahapurusha Yogas
        mahapurusha_yogas = get_mahapurusha_yogas(self.chart)

        # Check that the result is a list
        self.assertIsInstance(mahapurusha_yogas, list)

        # Check individual Mahapurusha Yoga functions
        ruchaka = has_ruchaka_yoga(self.chart)
        bhadra = has_bhadra_yoga(self.chart)
        hamsa = has_hamsa_yoga(self.chart)
        malavya = has_malavya_yoga(self.chart)
        sasa = has_sasa_yoga(self.chart)

        # Check that the individual Yogas are either None or dictionaries
        for yoga in [ruchaka, bhadra, hamsa, malavya, sasa]:
            if yoga is not None:
                self.assertIsInstance(yoga, dict)
                self.assertIn('name', yoga)
                self.assertIn('type', yoga)
                self.assertIn('planets', yoga)
                self.assertIn('houses', yoga)
                self.assertIn('description', yoga)
                self.assertIn('is_beneficial', yoga)
                self.assertIn('strength', yoga)

    def test_raja_yogas(self):
        """Test Raja Yoga calculations"""
        # Calculate Raja Yogas
        raja_yogas = get_raja_yogas(self.chart)

        # Check that the result is a list
        self.assertIsInstance(raja_yogas, list)

        # Check individual Raja Yoga functions
        dharmakarmaadhipati = has_dharmakarmaadhipati_yoga(self.chart)
        gajakesari = has_gajakesari_yoga(self.chart)
        amala = has_amala_yoga(self.chart)
        sreenatha = has_sreenatha_yoga(self.chart)
        chandra_mangala = has_chandra_mangala_yoga(self.chart)

        # Check that the individual Yogas are either None or dictionaries
        for yoga in [dharmakarmaadhipati, gajakesari, amala, sreenatha, chandra_mangala]:
            if yoga is not None:
                self.assertIsInstance(yoga, dict)
                self.assertIn('name', yoga)
                self.assertIn('type', yoga)
                self.assertIn('planets', yoga)
                self.assertIn('houses', yoga)
                self.assertIn('description', yoga)
                self.assertIn('is_beneficial', yoga)
                self.assertIn('strength', yoga)

    def test_dhana_yogas(self):
        """Test Dhana Yoga calculations"""
        # Calculate Dhana Yogas
        dhana_yogas = get_dhana_yogas(self.chart)

        # Check that the result is a list
        self.assertIsInstance(dhana_yogas, list)

        # Check individual Dhana Yoga functions
        lakshmi = has_lakshmi_yoga(self.chart)
        kubera = has_kubera_yoga(self.chart)
        kalanidhi = has_kalanidhi_yoga(self.chart)
        vasumati = has_vasumati_yoga(self.chart)
        mridanga = has_mridanga_yoga(self.chart)

        # Check that the individual Yogas are either None or dictionaries
        for yoga in [lakshmi, kubera, kalanidhi, vasumati, mridanga]:
            if yoga is not None:
                self.assertIsInstance(yoga, dict)
                self.assertIn('name', yoga)
                self.assertIn('type', yoga)
                self.assertIn('planets', yoga)
                self.assertIn('houses', yoga)
                self.assertIn('description', yoga)
                self.assertIn('is_beneficial', yoga)
                self.assertIn('strength', yoga)

    def test_nabhasa_yogas(self):
        """Test Nabhasa Yoga calculations"""
        # Calculate Nabhasa Yogas
        nabhasa_yogas = get_nabhasa_yogas(self.chart)

        # Check that the result is a list
        self.assertIsInstance(nabhasa_yogas, list)

        # Check individual Nabhasa Yoga functions
        rajju = has_rajju_yoga(self.chart)
        musala = has_musala_yoga(self.chart)
        nala = has_nala_yoga(self.chart)
        mala = has_mala_yoga(self.chart)
        sarpa = has_sarpa_yoga(self.chart)

        # Check that the individual Yogas are either None or dictionaries
        for yoga in [rajju, musala, nala, mala, sarpa]:
            if yoga is not None:
                self.assertIsInstance(yoga, dict)
                self.assertIn('name', yoga)
                self.assertIn('type', yoga)
                self.assertIn('planets', yoga)
                self.assertIn('description', yoga)
                self.assertIn('is_beneficial', yoga)
                self.assertIn('strength', yoga)

    def test_dosha_yogas(self):
        """Test Dosha Yoga calculations"""
        # Calculate Dosha Yogas
        dosha_yogas = get_dosha_yogas(self.chart)

        # Check that the result is a list
        self.assertIsInstance(dosha_yogas, list)

        # Check individual Dosha Yoga functions
        kemadruma = has_kemadruma_yoga(self.chart)
        daridra = has_daridra_yoga(self.chart)
        shakat = has_shakat_yoga(self.chart)
        kalasarpa = has_kalasarpa_yoga(self.chart)
        graha_yuddha = has_graha_yuddha(self.chart)

        # Check that the individual Yogas are either None or dictionaries
        for yoga in [kemadruma, daridra, shakat, kalasarpa, graha_yuddha]:
            if yoga is not None:
                self.assertIsInstance(yoga, dict)
                self.assertIn('name', yoga)
                self.assertIn('type', yoga)
                self.assertIn('planets', yoga)
                self.assertIn('houses', yoga)
                self.assertIn('description', yoga)
                self.assertIn('is_beneficial', yoga)
                self.assertIn('strength', yoga)

    def test_chandra_yogas(self):
        """Test Chandra Yoga calculations"""
        # Calculate Chandra Yogas
        chandra_yogas = get_chandra_yogas(self.chart)

        # Check that the result is a list
        self.assertIsInstance(chandra_yogas, list)

        # Check individual Chandra Yoga functions
        adhi = has_adhi_yoga(self.chart)
        sunapha = has_sunapha_yoga(self.chart)
        anapha = has_anapha_yoga(self.chart)
        durudhura = has_durudhura_yoga(self.chart)
        kemadruma = has_kemadruma_yoga(self.chart)

        # Check that the individual Yogas are either None or dictionaries
        for yoga in [adhi, sunapha, anapha, durudhura, kemadruma]:
            if yoga is not None:
                self.assertIsInstance(yoga, dict)
                self.assertIn('name', yoga)
                self.assertIn('type', yoga)
                self.assertIn('planets', yoga)
                self.assertIn('houses', yoga)
                self.assertIn('description', yoga)
                self.assertIn('is_beneficial', yoga)
                self.assertIn('strength', yoga)

    def test_yoga_data(self):
        """Test Yoga data functions"""
        # Calculate all Yogas
        yogas = get_all_yogas(self.chart)

        # Get the Yoga data
        data = get_yoga_data(self.chart)

        # Check that all required keys are present
        self.assertIn('total_yogas', data)
        self.assertIn('beneficial_yogas', data)
        self.assertIn('harmful_yogas', data)
        self.assertIn('strongest_yoga', data)
        self.assertIn('yoga_types', data)



    def test_yoga_comparison(self):
        """Test Yoga comparison functions"""
        # Create a second chart
        date2 = Datetime('2025/05/09', '20:51', '+05:30')
        pos2 = GeoPos(12.9716, 77.5946)  # Bangalore, India
        chart2 = Chart(date2, pos2, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)

        # Calculate comparison
        comparison = get_yoga_comparison(self.chart, chart2)

        # Check that all required keys are present
        self.assertIn('chart1_yogas', comparison)
        self.assertIn('chart2_yogas', comparison)
        self.assertIn('common_yogas', comparison)

        # Check that chart1_yogas contains the required keys
        self.assertIn('total', comparison['chart1_yogas'])
        self.assertIn('beneficial', comparison['chart1_yogas'])
        self.assertIn('harmful', comparison['chart1_yogas'])
        self.assertIn('types', comparison['chart1_yogas'])

    def test_yoga_strength_score(self):
        """Test Yoga strength score function"""
        # Calculate all Yogas
        yogas = get_all_yogas(self.chart)

        # Calculate the strength score
        score = get_yoga_strength_score(self.chart, yogas)

        # Check that the score is within 0-100
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

if __name__ == '__main__':
    unittest.main()
