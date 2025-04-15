"""
    Tests for Jaimini Arudha Pada calculations
"""

import unittest
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic import const
from astrovedic.vedic.jaimini.arudha import (
    calculate_arudha_pada, calculate_all_arudha_padas,
    calculate_graha_padas, get_lagna_pada, get_upapada_lagna,
    LAGNA_PADA, DHANA_PADA, BHRATRI_PADA, MATRI_PADA,
    PUTRA_PADA, ROGA_PADA, DARA_PADA, MRITYU_PADA,
    BHAGYA_PADA, KARMA_PADA, LABHA_PADA, VYAYA_PADA,
    UPAPADA_LAGNA
)

class TestJaiminiArudha(unittest.TestCase):
    """Test Jaimini Arudha Pada calculations"""
    
    def setUp(self):
        """Set up test data"""
        self.date = Datetime('2000/1/1', '12:00', '+00:00')
        self.pos = GeoPos('51n30', '0w10')
        self.chart = Chart(self.date, self.pos)
    
    def test_arudha_pada_calculation(self):
        """Test individual Arudha Pada calculation"""
        # Calculate Arudha Pada for the 1st house (Lagna Pada)
        lagna_pada = calculate_arudha_pada(self.chart, 1)
        
        # Check that the result is a valid sign
        valid_signs = [
            const.ARIES, const.TAURUS, const.GEMINI, const.CANCER,
            const.LEO, const.VIRGO, const.LIBRA, const.SCORPIO,
            const.SAGITTARIUS, const.CAPRICORN, const.AQUARIUS, const.PISCES
        ]
        self.assertIn(lagna_pada, valid_signs)
    
    def test_all_arudha_padas(self):
        """Test calculation of all Arudha Padas"""
        arudha_padas = calculate_all_arudha_padas(self.chart)
        
        # Check that we have all the expected Arudha Padas
        expected_padas = [
            LAGNA_PADA, DHANA_PADA, BHRATRI_PADA, MATRI_PADA,
            PUTRA_PADA, ROGA_PADA, DARA_PADA, MRITYU_PADA,
            BHAGYA_PADA, KARMA_PADA, LABHA_PADA, VYAYA_PADA,
            UPAPADA_LAGNA
        ]
        
        for pada in expected_padas:
            self.assertIn(pada, arudha_padas)
        
        # Check that all Arudha Padas have valid signs
        valid_signs = [
            const.ARIES, const.TAURUS, const.GEMINI, const.CANCER,
            const.LEO, const.VIRGO, const.LIBRA, const.SCORPIO,
            const.SAGITTARIUS, const.CAPRICORN, const.AQUARIUS, const.PISCES
        ]
        
        for pada, sign in arudha_padas.items():
            self.assertIn(sign, valid_signs)
    
    def test_graha_padas(self):
        """Test calculation of Graha Padas"""
        graha_padas = calculate_graha_padas(self.chart)
        
        # Check that we have Graha Padas for the main planets
        expected_planets = [
            const.SUN, const.MOON, const.MARS, const.MERCURY,
            const.JUPITER, const.VENUS, const.SATURN
        ]
        
        for planet in expected_planets:
            self.assertIn(planet, graha_padas)
        
        # Check that all Graha Padas have valid signs
        valid_signs = [
            const.ARIES, const.TAURUS, const.GEMINI, const.CANCER,
            const.LEO, const.VIRGO, const.LIBRA, const.SCORPIO,
            const.SAGITTARIUS, const.CAPRICORN, const.AQUARIUS, const.PISCES
        ]
        
        for planet, sign in graha_padas.items():
            self.assertIn(sign, valid_signs)
    
    def test_lagna_pada(self):
        """Test Lagna Pada calculation"""
        lagna_pada = get_lagna_pada(self.chart)
        
        # Check that the result is a valid sign
        valid_signs = [
            const.ARIES, const.TAURUS, const.GEMINI, const.CANCER,
            const.LEO, const.VIRGO, const.LIBRA, const.SCORPIO,
            const.SAGITTARIUS, const.CAPRICORN, const.AQUARIUS, const.PISCES
        ]
        self.assertIn(lagna_pada, valid_signs)
    
    def test_upapada_lagna(self):
        """Test Upapada Lagna calculation"""
        upapada_lagna = get_upapada_lagna(self.chart)
        
        # Check that the result is a valid sign
        valid_signs = [
            const.ARIES, const.TAURUS, const.GEMINI, const.CANCER,
            const.LEO, const.VIRGO, const.LIBRA, const.SCORPIO,
            const.SAGITTARIUS, const.CAPRICORN, const.AQUARIUS, const.PISCES
        ]
        self.assertIn(upapada_lagna, valid_signs)

if __name__ == '__main__':
    unittest.main()
