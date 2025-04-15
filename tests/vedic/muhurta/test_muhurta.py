#!/usr/bin/env python3
"""
Test Muhurta Calculations

This script tests the Muhurta (electional astrology) calculations in astrovedic.
"""

import unittest
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic import const
from astrovedic.vedic.muhurta import (
    get_panchanga, get_muhurta_quality, get_abhijit_muhurta,
    get_brahma_muhurta, get_rahu_kala, get_yama_ghantaka,
    get_gulika_kala, get_activity_score, get_best_time_for_activity,
    get_muhurta_predictions, analyze_muhurta
)
from astrovedic.vedic.muhurta.panchanga import (
    get_tithi, get_nakshatra_for_muhurta, get_yoga,
    get_karana, get_vara
)
from astrovedic.vedic.muhurta.timing import (
    get_hora, get_kaala, get_amrita_yoga,
    get_siddha_yoga, get_amrita_siddha_yoga
)
from astrovedic.vedic.muhurta.activities import (
    get_activity_rules, get_activity_score,
    get_best_time_for_activity
)
from astrovedic.vedic.muhurta.analysis import (
    analyze_muhurta, get_muhurta_predictions,
    get_muhurta_compatibility, get_muhurta_strength_score
)

class TestMuhurta(unittest.TestCase):
    """Test case for Muhurta calculations"""
    
    def setUp(self):
        """Set up test case"""
        # Create a chart for the reference date
        date = Datetime('2025/04/09', '20:51', '+05:30')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart = Chart(date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
        self.date = date
        self.location = pos
    
    def test_get_panchanga(self):
        """Test get_panchanga function"""
        # Calculate the Panchanga
        panchanga = get_panchanga(self.chart)
        
        # Check that all required keys are present
        self.assertIn('tithi', panchanga)
        self.assertIn('nakshatra', panchanga)
        self.assertIn('yoga', panchanga)
        self.assertIn('karana', panchanga)
        self.assertIn('vara', panchanga)
        
        # Check that each component has the required keys
        tithi = panchanga['tithi']
        self.assertIn('num', tithi)
        self.assertIn('name', tithi)
        self.assertIn('type', tithi)
        self.assertIn('paksha', tithi)
        self.assertIn('elapsed', tithi)
        
        nakshatra = panchanga['nakshatra']
        self.assertIn('num', nakshatra)
        self.assertIn('name', nakshatra)
        self.assertIn('pada', nakshatra)
        self.assertIn('lord', nakshatra)
        self.assertIn('type', nakshatra)
        self.assertIn('elapsed', nakshatra)
        
        yoga = panchanga['yoga']
        self.assertIn('num', yoga)
        self.assertIn('name', yoga)
        self.assertIn('type', yoga)
        self.assertIn('elapsed', yoga)
        
        karana = panchanga['karana']
        self.assertIn('num', karana)
        self.assertIn('name', karana)
        self.assertIn('type', karana)
        self.assertIn('elapsed', karana)
        
        vara = panchanga['vara']
        self.assertIn('num', vara)
        self.assertIn('name', vara)
        self.assertIn('lord', vara)
    
    def test_get_muhurta_quality(self):
        """Test get_muhurta_quality function"""
        # Calculate the Muhurta quality
        quality = get_muhurta_quality(self.chart)
        
        # Check that all required keys are present
        self.assertIn('score', quality)
        self.assertIn('quality', quality)
        self.assertIn('panchanga', quality)
        
        # Check that the quality is one of the expected values
        self.assertIn(quality['quality'], ['Excellent', 'Good', 'Neutral', 'Inauspicious', 'Highly Inauspicious'])
    
    def test_get_special_muhurtas(self):
        """Test special Muhurta functions"""
        # Calculate Abhijit Muhurta
        abhijit = get_abhijit_muhurta(self.date, self.location)
        
        # Check that all required keys are present
        self.assertIn('start', abhijit)
        self.assertIn('end', abhijit)
        self.assertIn('duration', abhijit)
        self.assertIn('description', abhijit)
        
        # Calculate Brahma Muhurta
        brahma = get_brahma_muhurta(self.date, self.location)
        
        # Check that all required keys are present
        self.assertIn('start', brahma)
        self.assertIn('end', brahma)
        self.assertIn('duration', brahma)
        self.assertIn('description', brahma)
    
    def test_get_inauspicious_periods(self):
        """Test inauspicious period functions"""
        # Calculate Rahu Kala
        rahu_kala = get_rahu_kala(self.date, self.location)
        
        # Check that all required keys are present
        self.assertIn('start', rahu_kala)
        self.assertIn('end', rahu_kala)
        self.assertIn('duration', rahu_kala)
        self.assertIn('description', rahu_kala)
        
        # Calculate Yama Ghantaka
        yama_ghantaka = get_yama_ghantaka(self.date, self.location)
        
        # Check that all required keys are present
        self.assertIn('start', yama_ghantaka)
        self.assertIn('end', yama_ghantaka)
        self.assertIn('duration', yama_ghantaka)
        self.assertIn('description', yama_ghantaka)
        
        # Calculate Gulika Kala
        gulika_kala = get_gulika_kala(self.date, self.location)
        
        # Check that all required keys are present
        self.assertIn('start', gulika_kala)
        self.assertIn('end', gulika_kala)
        self.assertIn('duration', gulika_kala)
        self.assertIn('description', gulika_kala)
    
    def test_get_timing_functions(self):
        """Test timing functions"""
        # Calculate Hora
        hora = get_hora(self.date, self.location)
        
        # Check that all required keys are present
        self.assertIn('lord', hora)
        self.assertIn('start', hora)
        self.assertIn('end', hora)
        self.assertIn('duration', hora)
        self.assertIn('elapsed', hora)
        self.assertIn('is_day', hora)
        
        # Calculate Kaala
        kaala = get_kaala(self.date, self.location)
        
        # Check that all required keys are present if not None
        if kaala is not None:
            self.assertIn('name', kaala)
            self.assertIn('start', kaala)
            self.assertIn('end', kaala)
            self.assertIn('duration', kaala)
            self.assertIn('elapsed', kaala)
    
    def test_get_yoga_functions(self):
        """Test yoga functions"""
        # Check Amrita Yoga
        amrita_yoga = get_amrita_yoga(self.chart)
        self.assertIsInstance(amrita_yoga, bool)
        
        # Check Siddha Yoga
        siddha_yoga = get_siddha_yoga(self.chart)
        self.assertIsInstance(siddha_yoga, bool)
        
        # Check Amrita-Siddha Yoga
        amrita_siddha_yoga = get_amrita_siddha_yoga(self.chart)
        self.assertIsInstance(amrita_siddha_yoga, bool)
    
    def test_get_activity_functions(self):
        """Test activity functions"""
        # Get activity rules
        rules = get_activity_rules('marriage')
        
        # Check that all required keys are present
        self.assertIn('auspicious_tithis', rules)
        self.assertIn('inauspicious_tithis', rules)
        self.assertIn('auspicious_nakshatras', rules)
        self.assertIn('inauspicious_nakshatras', rules)
        self.assertIn('auspicious_varas', rules)
        self.assertIn('inauspicious_varas', rules)
        self.assertIn('auspicious_yogas', rules)
        self.assertIn('inauspicious_yogas', rules)
        self.assertIn('auspicious_karanas', rules)
        self.assertIn('inauspicious_karanas', rules)
        self.assertIn('important_planets', rules)
        self.assertIn('avoid_houses', rules)
        self.assertIn('min_duration', rules)
        self.assertIn('description', rules)
        
        # Calculate activity score
        score = get_activity_score(self.date, self.location, 'marriage')
        
        # Check that all required keys are present
        self.assertIn('activity', score)
        self.assertIn('score', score)
        self.assertIn('max_score', score)
        self.assertIn('percentage', score)
        self.assertIn('quality', score)
        self.assertIn('factors', score)
        self.assertIn('panchanga', score)
        
        # Check that the quality is one of the expected values
        self.assertIn(score['quality'], ['Excellent', 'Good', 'Neutral', 'Inauspicious', 'Highly Inauspicious'])
    
    def test_get_best_time_for_activity(self):
        """Test get_best_time_for_activity function"""
        # Create a date range
        end_dt = self.date.datetime() + timedelta(days=1)
        end_date = Datetime.fromDatetime(end_dt)
        
        # Find the best time for an activity
        best_time = get_best_time_for_activity(self.date, end_date, self.location, 'general')
        
        # Check that all required keys are present if not None
        if best_time is not None:
            self.assertIn('start', best_time)
            self.assertIn('end', best_time)
            self.assertIn('duration', best_time)
            self.assertIn('activity', best_time)
            self.assertIn('score', best_time)
    
    def test_analyze_muhurta(self):
        """Test analyze_muhurta function"""
        # Analyze the Muhurta
        analysis = analyze_muhurta(self.date, self.location)
        
        # Check that all required keys are present
        self.assertIn('date', analysis)
        self.assertIn('location', analysis)
        self.assertIn('quality', analysis)
        self.assertIn('panchanga', analysis)
        self.assertIn('activity_scores', analysis)
        self.assertIn('best_activity', analysis)
        self.assertIn('planets', analysis)
        self.assertIn('ascendant', analysis)
    
    def test_get_muhurta_predictions(self):
        """Test get_muhurta_predictions function"""
        # Generate predictions
        predictions = get_muhurta_predictions(self.date, self.location)
        
        # Check that all required keys are present
        self.assertIn('general', predictions)
        self.assertIn('activities', predictions)
        self.assertIn('timing', predictions)
    
    def test_get_muhurta_compatibility(self):
        """Test get_muhurta_compatibility function"""
        # Create a second date
        date2 = Datetime('2025/04/10', '20:51', '+05:30')
        
        # Calculate compatibility
        compatibility = get_muhurta_compatibility(self.date, date2, self.location)
        
        # Check that all required keys are present
        self.assertIn('score', compatibility)
        self.assertIn('factors', compatibility)
        self.assertIn('description', compatibility)
        
        # Check that the score is within 0-100
        self.assertGreaterEqual(compatibility['score'], 0)
        self.assertLessEqual(compatibility['score'], 100)
    
    def test_get_muhurta_strength_score(self):
        """Test get_muhurta_strength_score function"""
        # Calculate the strength score
        score = get_muhurta_strength_score(self.date, self.location)
        
        # Check that the score is within 0-100
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

if __name__ == '__main__':
    unittest.main()
