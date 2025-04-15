#!/usr/bin/env python3
"""
Test Kuta Analysis

This script tests the Kuta (compatibility factors) analysis in astrovedic.vedic.compatibility.
"""

import unittest
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic import const
from astrovedic.vedic.compatibility.kuta import (
    get_varna_kuta, get_vashya_kuta, get_tara_kuta,
    get_yoni_kuta, get_graha_maitri_kuta, get_gana_kuta,
    get_bhakoot_kuta, get_nadi_kuta
)
from astrovedic.vedic.compatibility.kuta.total import get_total_kuta_score


class TestKuta(unittest.TestCase):
    """Test case for Kuta (compatibility factors) analysis"""

    def setUp(self):
        """Set up test case"""
        # Create charts for two individuals
        # Person 1: Reference date
        date1 = Datetime('2025/04/09', '20:51', '+05:30')
        pos1 = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart1 = Chart(date1, pos1, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)

        # Person 2: Different date
        date2 = Datetime('1990/06/15', '10:30', '+05:30')
        pos2 = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart2 = Chart(date2, pos2, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)

    def test_get_varna_kuta(self):
        """Test get_varna_kuta function"""
        # Calculate the Varna Kuta
        varna_kuta = get_varna_kuta(self.chart1, self.chart2)

        # Check that all required keys are present
        self.assertIn('varna1', varna_kuta)
        self.assertIn('varna2', varna_kuta)
        self.assertIn('score', varna_kuta)
        self.assertIn('max_score', varna_kuta)
        self.assertIn('description', varna_kuta)

        # Check that the score is within the valid range
        self.assertGreaterEqual(varna_kuta['score'], 0)
        self.assertLessEqual(varna_kuta['score'], varna_kuta['max_score'])

        # Check that the varnas are valid
        self.assertIn(varna_kuta['varna1'], ['Brahmin', 'Kshatriya', 'Vaishya', 'Shudra'])
        self.assertIn(varna_kuta['varna2'], ['Brahmin', 'Kshatriya', 'Vaishya', 'Shudra'])

        # Print the Varna Kuta for reference
        print(f"Varna Kuta: {varna_kuta['varna1']} and {varna_kuta['varna2']}")
        print(f"Score: {varna_kuta['score']}/{varna_kuta['max_score']}")
        print(f"Description: {varna_kuta['description']}")

    def test_get_vashya_kuta(self):
        """Test get_vashya_kuta function"""
        # Calculate the Vashya Kuta
        vashya_kuta = get_vashya_kuta(self.chart1, self.chart2)

        # Check that all required keys are present
        self.assertIn('vashya1', vashya_kuta)
        self.assertIn('vashya2', vashya_kuta)
        self.assertIn('score', vashya_kuta)
        self.assertIn('max_score', vashya_kuta)
        self.assertIn('description', vashya_kuta)

        # Check that the score is within the valid range
        self.assertGreaterEqual(vashya_kuta['score'], 0)
        self.assertLessEqual(vashya_kuta['score'], vashya_kuta['max_score'])

        # Check that the vashya categories are valid
        self.assertIn(vashya_kuta['vashya1'], ['Manav', 'Chatushpad', 'Vanchar', 'Jalachar', 'Keet'])
        self.assertIn(vashya_kuta['vashya2'], ['Manav', 'Chatushpad', 'Vanchar', 'Jalachar', 'Keet'])

        # Print the Vashya Kuta for reference
        print(f"Vashya Kuta: {vashya_kuta['vashya1']} and {vashya_kuta['vashya2']}")
        print(f"Score: {vashya_kuta['score']}/{vashya_kuta['max_score']}")
        print(f"Description: {vashya_kuta['description']}")

    def test_get_tara_kuta(self):
        """Test get_tara_kuta function"""
        # Calculate the Tara Kuta
        tara_kuta = get_tara_kuta(self.chart1, self.chart2)

        # Check that all required keys are present
        self.assertIn('nakshatra1', tara_kuta)
        self.assertIn('nakshatra2', tara_kuta)
        self.assertIn('tara', tara_kuta)
        self.assertIn('score', tara_kuta)
        self.assertIn('max_score', tara_kuta)
        self.assertIn('description', tara_kuta)

        # Check that the score is within the valid range
        self.assertGreaterEqual(tara_kuta['score'], 0)
        self.assertLessEqual(tara_kuta['score'], tara_kuta['max_score'])

        # Check that the tara is within the valid range
        self.assertGreaterEqual(tara_kuta['tara'], 1)
        self.assertLessEqual(tara_kuta['tara'], 9)

        # Print the Tara Kuta for reference
        print(f"Tara Kuta: {tara_kuta['nakshatra1']} and {tara_kuta['nakshatra2']}")
        print(f"Tara: {tara_kuta['tara']}")
        print(f"Score: {tara_kuta['score']}/{tara_kuta['max_score']}")
        print(f"Description: {tara_kuta['description']}")

    def test_get_yoni_kuta(self):
        """Test get_yoni_kuta function"""
        # Calculate the Yoni Kuta
        yoni_kuta = get_yoni_kuta(self.chart1, self.chart2)

        # Check that all required keys are present
        self.assertIn('yoni1', yoni_kuta)
        self.assertIn('yoni2', yoni_kuta)
        self.assertIn('score', yoni_kuta)
        self.assertIn('max_score', yoni_kuta)
        self.assertIn('description', yoni_kuta)

        # Check that the score is within the valid range
        self.assertGreaterEqual(yoni_kuta['score'], 0)
        self.assertLessEqual(yoni_kuta['score'], yoni_kuta['max_score'])

        # Check that the yonis are valid
        valid_yonis = ['Horse', 'Elephant', 'Sheep', 'Serpent', 'Dog', 'Cat', 'Rat', 'Cow',
                      'Buffalo', 'Tiger', 'Deer', 'Monkey', 'Mongoose', 'Lion']
        self.assertIn(yoni_kuta['yoni1'], valid_yonis)
        self.assertIn(yoni_kuta['yoni2'], valid_yonis)

        # Print the Yoni Kuta for reference
        print(f"Yoni Kuta: {yoni_kuta['yoni1']} and {yoni_kuta['yoni2']}")
        print(f"Score: {yoni_kuta['score']}/{yoni_kuta['max_score']}")
        print(f"Description: {yoni_kuta['description']}")

    def test_get_graha_maitri_kuta(self):
        """Test get_graha_maitri_kuta function"""
        # Calculate the Graha Maitri Kuta
        graha_maitri_kuta = get_graha_maitri_kuta(self.chart1, self.chart2)

        # Check that all required keys are present
        self.assertIn('lord1', graha_maitri_kuta)
        self.assertIn('lord2', graha_maitri_kuta)
        self.assertIn('friendship', graha_maitri_kuta)
        self.assertIn('score', graha_maitri_kuta)
        self.assertIn('max_score', graha_maitri_kuta)
        self.assertIn('description', graha_maitri_kuta)

        # Check that the score is within the valid range
        self.assertGreaterEqual(graha_maitri_kuta['score'], 0)
        self.assertLessEqual(graha_maitri_kuta['score'], graha_maitri_kuta['max_score'])

        # Check that the lords are valid planets
        self.assertIn(graha_maitri_kuta['lord1'], const.LIST_SEVEN_PLANETS)
        self.assertIn(graha_maitri_kuta['lord2'], const.LIST_SEVEN_PLANETS)

        # Check that the friendship is valid
        self.assertIn(graha_maitri_kuta['friendship'], ['Friend', 'Neutral', 'Enemy', 'Unknown'])

        # Print the Graha Maitri Kuta for reference
        print(f"Graha Maitri Kuta: {graha_maitri_kuta['lord1']} and {graha_maitri_kuta['lord2']}")
        print(f"Friendship: {graha_maitri_kuta['friendship']}")
        print(f"Score: {graha_maitri_kuta['score']}/{graha_maitri_kuta['max_score']}")
        print(f"Description: {graha_maitri_kuta['description']}")

    def test_get_gana_kuta(self):
        """Test get_gana_kuta function"""
        # Calculate the Gana Kuta
        gana_kuta = get_gana_kuta(self.chart1, self.chart2)

        # Check that all required keys are present
        self.assertIn('gana1', gana_kuta)
        self.assertIn('gana2', gana_kuta)
        self.assertIn('score', gana_kuta)
        self.assertIn('max_score', gana_kuta)
        self.assertIn('description', gana_kuta)

        # Check that the score is within the valid range
        self.assertGreaterEqual(gana_kuta['score'], 0)
        self.assertLessEqual(gana_kuta['score'], gana_kuta['max_score'])

        # Check that the ganas are valid
        self.assertIn(gana_kuta['gana1'], ['Deva', 'Manushya', 'Rakshasa'])
        self.assertIn(gana_kuta['gana2'], ['Deva', 'Manushya', 'Rakshasa'])

        # Print the Gana Kuta for reference
        print(f"Gana Kuta: {gana_kuta['gana1']} and {gana_kuta['gana2']}")
        print(f"Score: {gana_kuta['score']}/{gana_kuta['max_score']}")
        print(f"Description: {gana_kuta['description']}")

    def test_get_bhakoot_kuta(self):
        """Test get_bhakoot_kuta function"""
        # Calculate the Bhakoot Kuta
        bhakoot_kuta = get_bhakoot_kuta(self.chart1, self.chart2)

        # Check that all required keys are present
        self.assertIn('sign1', bhakoot_kuta)
        self.assertIn('sign2', bhakoot_kuta)
        self.assertIn('house_position', bhakoot_kuta)
        self.assertIn('score', bhakoot_kuta)
        self.assertIn('max_score', bhakoot_kuta)
        self.assertIn('description', bhakoot_kuta)

        # Check that the score is within the valid range
        self.assertGreaterEqual(bhakoot_kuta['score'], 0)
        self.assertLessEqual(bhakoot_kuta['score'], bhakoot_kuta['max_score'])

        # Check that the signs are valid
        self.assertIn(bhakoot_kuta['sign1'], const.LIST_SIGNS)
        self.assertIn(bhakoot_kuta['sign2'], const.LIST_SIGNS)

        # Check that the house position is within the valid range
        self.assertGreaterEqual(bhakoot_kuta['house_position'], 1)
        self.assertLessEqual(bhakoot_kuta['house_position'], 12)

        # Print the Bhakoot Kuta for reference
        print(f"Bhakoot Kuta: {bhakoot_kuta['sign1']} and {bhakoot_kuta['sign2']}")
        print(f"House Position: {bhakoot_kuta['house_position']}")
        print(f"Score: {bhakoot_kuta['score']}/{bhakoot_kuta['max_score']}")
        print(f"Description: {bhakoot_kuta['description']}")

    def test_get_nadi_kuta(self):
        """Test get_nadi_kuta function"""
        # Calculate the Nadi Kuta
        nadi_kuta = get_nadi_kuta(self.chart1, self.chart2)

        # Check that all required keys are present
        self.assertIn('nadi1', nadi_kuta)
        self.assertIn('nadi2', nadi_kuta)
        self.assertIn('score', nadi_kuta)
        self.assertIn('max_score', nadi_kuta)
        self.assertIn('description', nadi_kuta)

        # Check that the score is within the valid range
        self.assertGreaterEqual(nadi_kuta['score'], 0)
        self.assertLessEqual(nadi_kuta['score'], nadi_kuta['max_score'])

        # Check that the nadis are valid
        self.assertIn(nadi_kuta['nadi1'], ['Vata', 'Pitta', 'Kapha'])
        self.assertIn(nadi_kuta['nadi2'], ['Vata', 'Pitta', 'Kapha'])

        # Print the Nadi Kuta for reference
        print(f"Nadi Kuta: {nadi_kuta['nadi1']} and {nadi_kuta['nadi2']}")
        print(f"Score: {nadi_kuta['score']}/{nadi_kuta['max_score']}")
        print(f"Description: {nadi_kuta['description']}")

    def test_get_total_kuta_score(self):
        """Test get_total_kuta_score function"""
        # Calculate the total Kuta score
        total_kuta_score = get_total_kuta_score(self.chart1, self.chart2)

        # Check that all required keys are present
        self.assertIn('score', total_kuta_score)
        self.assertIn('max_score', total_kuta_score)
        self.assertIn('percentage', total_kuta_score)
        self.assertIn('description', total_kuta_score)

        # Check that the score is within the valid range
        self.assertGreaterEqual(total_kuta_score['score'], 0)
        self.assertLessEqual(total_kuta_score['score'], total_kuta_score['max_score'])

        # Check that the percentage is within the valid range
        self.assertGreaterEqual(total_kuta_score['percentage'], 0)
        self.assertLessEqual(total_kuta_score['percentage'], 100)

        # Print the total Kuta score for reference
        print(f"Total Kuta Score: {total_kuta_score['score']}/{total_kuta_score['max_score']} ({total_kuta_score['percentage']}%)")
        print(f"Description: {total_kuta_score['description']}")


if __name__ == '__main__':
    unittest.main()
