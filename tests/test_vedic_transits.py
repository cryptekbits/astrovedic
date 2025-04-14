#!/usr/bin/env python3
"""
Test Vedic Transit Calculations

This script tests the Vedic transit calculations in astrovedic.
"""

import unittest
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic import const
from astrovedic.vedic.transits import (
    get_transits, get_transit_predictions_for_date,
    get_transit_timeline_for_period, analyze_transit_period,
    get_transit_chart, get_transit_planets, get_transit_aspects,
    get_transit_houses, get_transit_quality, get_gochara_effects,
    get_transit_ashtakavarga, get_transit_dasha_effects,
    get_transit_analysis
)
from astrovedic.vedic.transits.core import (
    get_house_number, get_house_sign,
    is_aspect_applying
)
from astrovedic.vedic.transits.gochara import (
    get_planet_gochara, get_house_from_moon,
    get_effect_from_moon, get_vedha_effects,
    get_argala_effects, get_gochara_strength
)
from astrovedic.vedic.transits.ashtakavarga import (
    get_transit_bindus, get_transit_sarvashtakavarga,
    get_transit_kaksha, get_transit_ashtakavarga_strength,
    get_transit_sarvashtakavarga_strength
)
from astrovedic.vedic.transits.dashas import (
    get_transit_dasha_effects, get_transit_antardasha_effects,
    get_transit_pratyantardasha_effects, get_dasha_transit_compatibility,
    get_transit_effects_on_planet, get_aspect_effect,
    get_house_transit_effect, get_aspect_score,
    get_house_transit_score
)
from astrovedic.vedic.transits.predictions import (
    get_transit_predictions, get_transit_timeline,
    get_transit_events, get_transit_periods,
    generate_planet_prediction, generate_house_prediction,
    generate_dasha_prediction
)
from astrovedic.vedic.transits.analysis import (
    analyze_transits, get_transit_compatibility,
    get_transit_strength_score, get_transit_analysis
)
from datetime import timedelta

class TestVedicTransits(unittest.TestCase):
    """Test case for Vedic transit calculations"""
    
    def setUp(self):
        """Set up test case"""
        # Create a natal chart
        birth_date = Datetime('1990/01/01', '12:00', '+05:30')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.natal_chart = Chart(birth_date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
        
        # Create a transit chart
        transit_date = Datetime('2025/04/09', '20:51', '+05:30')
        self.transit_chart = Chart(transit_date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
        self.transit_date = transit_date
    
    def test_get_transit_chart(self):
        """Test get_transit_chart function"""
        # Get a transit chart
        transit_chart = get_transit_chart(self.natal_chart, self.transit_date)
        
        # Check that the chart is created correctly
        self.assertEqual(transit_chart.date, self.transit_date)
        self.assertEqual(transit_chart.pos, self.natal_chart.pos)
        self.assertEqual(transit_chart.hsys, self.natal_chart.hsys)
        self.assertEqual(transit_chart.mode, self.natal_chart.mode)
    
    def test_get_transit_planets(self):
        """Test get_transit_planets function"""
        # Get transit planets
        transit_planets = get_transit_planets(self.natal_chart, self.transit_chart)
        
        # Check that all planets are included
        for planet_id in const.LIST_OBJECTS_VEDIC:
            self.assertIn(planet_id, transit_planets)
            
            # Check that all required keys are present
            self.assertIn('natal_sign', transit_planets[planet_id])
            self.assertIn('natal_lon', transit_planets[planet_id])
            self.assertIn('transit_sign', transit_planets[planet_id])
            self.assertIn('transit_lon', transit_planets[planet_id])
            self.assertIn('house', transit_planets[planet_id])
            self.assertIn('distance', transit_planets[planet_id])
            self.assertIn('is_retrograde', transit_planets[planet_id])
    
    def test_get_transit_aspects(self):
        """Test get_transit_aspects function"""
        # Get transit aspects
        transit_aspects = get_transit_aspects(self.natal_chart, self.transit_chart)
        
        # Check that the result is a list
        self.assertIsInstance(transit_aspects, list)
        
        # Check that each aspect has the required keys
        for aspect in transit_aspects:
            self.assertIn('transit_planet', aspect)
            self.assertIn('natal_planet', aspect)
            self.assertIn('aspect', aspect)
            self.assertIn('angle', aspect)
            self.assertIn('orb', aspect)
            self.assertIn('applying', aspect)
    
    def test_get_transit_houses(self):
        """Test get_transit_houses function"""
        # Get transit houses
        transit_houses = get_transit_houses(self.natal_chart, self.transit_chart)
        
        # Check that all houses are included
        for house_num in range(1, 13):
            self.assertIn(house_num, transit_houses)
            
            # Check that all required keys are present
            self.assertIn('planets', transit_houses[house_num])
            self.assertIn('sign', transit_houses[house_num])
    
    def test_get_transit_quality(self):
        """Test get_transit_quality function"""
        # Get transit quality
        transit_quality = get_transit_quality(self.natal_chart, self.transit_chart)
        
        # Check that all required keys are present
        self.assertIn('score', transit_quality)
        self.assertIn('quality', transit_quality)
        self.assertIn('factors', transit_quality)
        
        # Check that the quality is one of the expected values
        self.assertIn(transit_quality['quality'], ['Excellent', 'Good', 'Neutral', 'Challenging', 'Difficult'])
    
    def test_get_gochara_effects(self):
        """Test get_gochara_effects function"""
        # Get Gochara effects
        gochara_effects = get_gochara_effects(self.natal_chart, self.transit_chart)
        
        # Check that all planets are included
        for planet_id in const.LIST_OBJECTS_VEDIC:
            self.assertIn(planet_id, gochara_effects)
            
            # Check that all required keys are present
            self.assertIn('house', gochara_effects[planet_id])
            self.assertIn('moon_house', gochara_effects[planet_id])
            self.assertIn('effect', gochara_effects[planet_id])
            self.assertIn('vedha_effects', gochara_effects[planet_id])
            self.assertIn('argala_effects', gochara_effects[planet_id])
            self.assertIn('strength', gochara_effects[planet_id])
    
    def test_get_planet_gochara(self):
        """Test get_planet_gochara function"""
        # Get planet Gochara
        planet_gochara = get_planet_gochara(self.natal_chart, self.transit_chart, const.SUN)
        
        # Check that all required keys are present
        self.assertIn('house', planet_gochara)
        self.assertIn('moon_house', planet_gochara)
        self.assertIn('effect', planet_gochara)
        self.assertIn('vedha_effects', planet_gochara)
        self.assertIn('argala_effects', planet_gochara)
        self.assertIn('strength', planet_gochara)
    
    def test_get_house_from_moon(self):
        """Test get_house_from_moon function"""
        # Test with specific signs
        house_num = get_house_from_moon('Aries', 'Taurus')
        self.assertEqual(house_num, 2)
        
        house_num = get_house_from_moon('Aries', 'Aries')
        self.assertEqual(house_num, 1)
        
        house_num = get_house_from_moon('Aries', 'Pisces')
        self.assertEqual(house_num, 12)
    
    def test_get_effect_from_moon(self):
        """Test get_effect_from_moon function"""
        # Test with specific planet and house
        effect = get_effect_from_moon(const.SUN, 1)
        
        # Check that all required keys are present
        self.assertIn('effect', effect)
        self.assertIn('description', effect)
        
        # Check that the effect is one of the expected values
        self.assertIn(effect['effect'], ['Favorable', 'Unfavorable', 'Mixed', 'Neutral'])
    
    def test_get_vedha_effects(self):
        """Test get_vedha_effects function"""
        # Get Vedha effects
        vedha_effects = get_vedha_effects(self.natal_chart, self.transit_chart, const.SUN)
        
        # Check that the result is a list
        self.assertIsInstance(vedha_effects, list)
        
        # Check that each Vedha effect has the required keys
        for vedha in vedha_effects:
            self.assertIn('planet', vedha)
            self.assertIn('house', vedha)
            self.assertIn('description', vedha)
    
    def test_get_argala_effects(self):
        """Test get_argala_effects function"""
        # Get Argala effects
        argala_effects = get_argala_effects(self.natal_chart, self.transit_chart, const.SUN)
        
        # Check that the result is a list
        self.assertIsInstance(argala_effects, list)
        
        # Check that each Argala effect has the required keys
        for argala in argala_effects:
            self.assertIn('planet', argala)
            self.assertIn('house', argala)
            self.assertIn('description', argala)
    
    def test_get_gochara_strength(self):
        """Test get_gochara_strength function"""
        # Test with specific effect, Vedha effects, and Argala effects
        effect = {'effect': 'Favorable', 'description': 'Test effect'}
        vedha_effects = []
        argala_effects = []
        
        strength = get_gochara_strength(effect, vedha_effects, argala_effects)
        
        # Check that all required keys are present
        self.assertIn('score', strength)
        self.assertIn('strength', strength)
        
        # Check that the strength is one of the expected values
        self.assertIn(strength['strength'], ['Strong Favorable', 'Moderate Favorable', 'Neutral', 'Moderate Unfavorable', 'Strong Unfavorable'])
    
    def test_get_transit_ashtakavarga(self):
        """Test get_transit_ashtakavarga function"""
        # Get transit Ashtakavarga
        transit_ashtakavarga = get_transit_ashtakavarga(self.natal_chart, self.transit_chart)
        
        # Check that all planets are included
        for planet_id in const.LIST_OBJECTS_VEDIC:
            self.assertIn(planet_id, transit_ashtakavarga)
        
        # Check that Sarvashtakavarga is included
        self.assertIn('sarvashtakavarga', transit_ashtakavarga)
    
    def test_get_transit_bindus(self):
        """Test get_transit_bindus function"""
        # Get the Ashtakavarga for the natal chart
        from astrovedic.vedic.ashtakavarga import get_ashtakavarga
        ashtakavarga = get_ashtakavarga(self.natal_chart)
        
        # Get transit bindus
        transit_bindus = get_transit_bindus(self.natal_chart, self.transit_chart, const.SUN, ashtakavarga)
        
        # Check that all required keys are present
        self.assertIn('sign', transit_bindus)
        self.assertIn('house', transit_bindus)
        self.assertIn('bindus', transit_bindus)
        self.assertIn('kaksha', transit_bindus)
        self.assertIn('strength', transit_bindus)
    
    def test_get_transit_sarvashtakavarga(self):
        """Test get_transit_sarvashtakavarga function"""
        # Get the Sarvashtakavarga for the natal chart
        from astrovedic.vedic.ashtakavarga import get_sarvashtakavarga
        sarvashtakavarga = get_sarvashtakavarga(self.natal_chart)
        
        # Get transit Sarvashtakavarga
        transit_sarvashtakavarga = get_transit_sarvashtakavarga(self.natal_chart, self.transit_chart, sarvashtakavarga)
        
        # Check that all planets are included
        for planet_id in const.LIST_OBJECTS_VEDIC:
            self.assertIn(planet_id, transit_sarvashtakavarga)
            
            # Check that all required keys are present
            self.assertIn('sign', transit_sarvashtakavarga[planet_id])
            self.assertIn('house', transit_sarvashtakavarga[planet_id])
            self.assertIn('bindus', transit_sarvashtakavarga[planet_id])
            self.assertIn('strength', transit_sarvashtakavarga[planet_id])
    
    def test_get_transit_kaksha(self):
        """Test get_transit_kaksha function"""
        # Get the transit planet
        transit_planet = self.transit_chart.getObject(const.SUN)
        
        # Get transit Kaksha
        kaksha = get_transit_kaksha(transit_planet)
        
        # Check that all required keys are present
        self.assertIn('num', kaksha)
        self.assertIn('lord', kaksha)
        self.assertIn('start_lon', kaksha)
        self.assertIn('end_lon', kaksha)
    
    def test_get_transit_ashtakavarga_strength(self):
        """Test get_transit_ashtakavarga_strength function"""
        # Test with different bindu counts
        strength = get_transit_ashtakavarga_strength(6)
        self.assertEqual(strength['strength'], 'Excellent')
        
        strength = get_transit_ashtakavarga_strength(4)
        self.assertEqual(strength['strength'], 'Good')
        
        strength = get_transit_ashtakavarga_strength(2)
        self.assertEqual(strength['strength'], 'Neutral')
        
        strength = get_transit_ashtakavarga_strength(1)
        self.assertEqual(strength['strength'], 'Challenging')
        
        strength = get_transit_ashtakavarga_strength(0)
        self.assertEqual(strength['strength'], 'Difficult')
    
    def test_get_transit_sarvashtakavarga_strength(self):
        """Test get_transit_sarvashtakavarga_strength function"""
        # Test with different bindu counts
        strength = get_transit_sarvashtakavarga_strength(30)
        self.assertEqual(strength['strength'], 'Excellent')
        
        strength = get_transit_sarvashtakavarga_strength(25)
        self.assertEqual(strength['strength'], 'Good')
        
        strength = get_transit_sarvashtakavarga_strength(20)
        self.assertEqual(strength['strength'], 'Neutral')
        
        strength = get_transit_sarvashtakavarga_strength(15)
        self.assertEqual(strength['strength'], 'Challenging')
        
        strength = get_transit_sarvashtakavarga_strength(10)
        self.assertEqual(strength['strength'], 'Difficult')
    
    def test_get_transit_dasha_effects(self):
        """Test get_transit_dasha_effects function"""
        # Get transit Dasha effects
        transit_dasha_effects = get_transit_dasha_effects(self.natal_chart, self.transit_chart)
        
        # Check that all required keys are present
        self.assertIn('dasha', transit_dasha_effects)
        self.assertIn('antardasha', transit_dasha_effects)
        self.assertIn('pratyantardasha', transit_dasha_effects)
        self.assertIn('dasha_lord', transit_dasha_effects)
        self.assertIn('antardasha_lord', transit_dasha_effects)
        self.assertIn('pratyantardasha_lord', transit_dasha_effects)
        self.assertIn('dasha_effects', transit_dasha_effects)
        self.assertIn('antardasha_effects', transit_dasha_effects)
        self.assertIn('pratyantardasha_effects', transit_dasha_effects)
    
    def test_get_transit_antardasha_effects(self):
        """Test get_transit_antardasha_effects function"""
        # Get transit Antardasha effects
        transit_antardasha_effects = get_transit_antardasha_effects(self.natal_chart, self.transit_chart)
        
        # Check that all required keys are present
        self.assertIn('antardasha', transit_antardasha_effects)
        self.assertIn('antardasha_lord', transit_antardasha_effects)
        self.assertIn('antardasha_effects', transit_antardasha_effects)
    
    def test_get_transit_pratyantardasha_effects(self):
        """Test get_transit_pratyantardasha_effects function"""
        # Get transit Pratyantardasha effects
        transit_pratyantardasha_effects = get_transit_pratyantardasha_effects(self.natal_chart, self.transit_chart)
        
        # Check that all required keys are present
        self.assertIn('pratyantardasha', transit_pratyantardasha_effects)
        self.assertIn('pratyantardasha_lord', transit_pratyantardasha_effects)
        self.assertIn('pratyantardasha_effects', transit_pratyantardasha_effects)
    
    def test_get_transit_effects_on_planet(self):
        """Test get_transit_effects_on_planet function"""
        # Get transit effects on a planet
        transit_effects = get_transit_effects_on_planet(self.natal_chart, self.transit_chart, const.SUN)
        
        # Check that the result is a list
        self.assertIsInstance(transit_effects, list)
    
    def test_get_dasha_transit_compatibility(self):
        """Test get_dasha_transit_compatibility function"""
        # Get Dasha-transit compatibility
        dasha_compatibility = get_dasha_transit_compatibility(self.natal_chart, self.transit_chart)
        
        # Check that all required keys are present
        self.assertIn('dasha', dasha_compatibility)
        self.assertIn('antardasha', dasha_compatibility)
        self.assertIn('dasha_lord', dasha_compatibility)
        self.assertIn('antardasha_lord', dasha_compatibility)
        self.assertIn('score', dasha_compatibility)
        self.assertIn('compatibility', dasha_compatibility)
        self.assertIn('description', dasha_compatibility)
        self.assertIn('factors', dasha_compatibility)
        
        # Check that the compatibility is one of the expected values
        self.assertIn(dasha_compatibility['compatibility'], ['Excellent', 'Good', 'Neutral', 'Challenging', 'Difficult'])
    
    def test_get_aspect_effect(self):
        """Test get_aspect_effect function"""
        # Test with specific planets and aspect
        effect = get_aspect_effect(const.JUPITER, const.SUN, 'Trine')
        
        # Check that all required keys are present
        self.assertIn('effect', effect)
        self.assertIn('description', effect)
        
        # Check that the effect is one of the expected values
        self.assertIn(effect['effect'], ['Favorable', 'Unfavorable', 'Mixed', 'Neutral', 'Challenging'])
    
    def test_get_house_transit_effect(self):
        """Test get_house_transit_effect function"""
        # Test with specific planets and house
        effect = get_house_transit_effect(const.JUPITER, const.SUN, 1)
        
        # Check that all required keys are present
        self.assertIn('effect', effect)
        self.assertIn('description', effect)
        
        # Check that the effect is one of the expected values
        self.assertIn(effect['effect'], ['Favorable', 'Unfavorable', 'Mixed', 'Neutral', 'Challenging'])
    
    def test_get_aspect_score(self):
        """Test get_aspect_score function"""
        # Test with specific planets and aspect
        score = get_aspect_score('Trine', const.JUPITER, const.SUN)
        
        # Check that the score is a number
        self.assertIsInstance(score, (int, float))
    
    def test_get_house_transit_score(self):
        """Test get_house_transit_score function"""
        # Test with specific planets and house
        score = get_house_transit_score(const.JUPITER, const.SUN, 1)
        
        # Check that the score is a number
        self.assertIsInstance(score, (int, float))
    
    def test_get_transit_predictions(self):
        """Test get_transit_predictions function"""
        # Get transits
        transits = get_transits(self.natal_chart, self.transit_date)
        
        # Get transit predictions
        predictions = get_transit_predictions(self.natal_chart, transits)
        
        # Check that all required keys are present
        self.assertIn('general', predictions)
        self.assertIn('planets', predictions)
        self.assertIn('houses', predictions)
        self.assertIn('dashas', predictions)
    
    def test_get_transit_timeline(self):
        """Test get_transit_timeline function"""
        # Calculate the end date
        end_dt = self.transit_date.datetime() + timedelta(days=30)
        end_date = Datetime.fromDatetime(end_dt)
        
        # Get transit timeline
        timeline = get_transit_timeline(self.natal_chart, self.transit_date, end_date)
        
        # Check that the result is a list
        self.assertIsInstance(timeline, list)
    
    def test_get_transit_events(self):
        """Test get_transit_events function"""
        # Calculate the end date
        end_dt = self.transit_date.datetime() + timedelta(days=30)
        end_date = Datetime.fromDatetime(end_dt)
        
        # Get transit events
        events = get_transit_events(self.natal_chart, self.transit_date, end_date)
        
        # Check that the result is a list
        self.assertIsInstance(events, list)
    
    def test_get_transit_periods(self):
        """Test get_transit_periods function"""
        # Calculate the end date
        end_dt = self.transit_date.datetime() + timedelta(days=30)
        end_date = Datetime.fromDatetime(end_dt)
        
        # Get transit periods
        periods = get_transit_periods(self.natal_chart, self.transit_date, end_date)
        
        # Check that the result is a list
        self.assertIsInstance(periods, list)
        
        # Check that each period has the required keys
        for period in periods:
            self.assertIn('start_date', period)
            self.assertIn('end_date', period)
            self.assertIn('quality', period)
            self.assertIn('description', period)
    
    def test_generate_planet_prediction(self):
        """Test generate_planet_prediction function"""
        # Get transits
        transits = get_transits(self.natal_chart, self.transit_date)
        
        # Generate a planet prediction
        prediction = generate_planet_prediction(
            const.SUN,
            transits['transit_planets'][const.SUN],
            transits['gochara_effects'][const.SUN],
            transits['transit_ashtakavarga'][const.SUN]
        )
        
        # Check that all required keys are present
        self.assertIn('planet', prediction)
        self.assertIn('sign', prediction)
        self.assertIn('house', prediction)
        self.assertIn('is_retrograde', prediction)
        self.assertIn('gochara_effect', prediction)
        self.assertIn('ashtakavarga_strength', prediction)
        self.assertIn('description', prediction)
    
    def test_generate_house_prediction(self):
        """Test generate_house_prediction function"""
        # Get transits
        transits = get_transits(self.natal_chart, self.transit_date)
        
        # Generate a house prediction
        prediction = generate_house_prediction(1, transits['transit_houses'][1])
        
        # Check that all required keys are present
        self.assertIn('house', prediction)
        self.assertIn('sign', prediction)
        self.assertIn('planets', prediction)
        self.assertIn('description', prediction)
    
    def test_generate_dasha_prediction(self):
        """Test generate_dasha_prediction function"""
        # Get transits
        transits = get_transits(self.natal_chart, self.transit_date)
        
        # Get the Dasha compatibility
        dasha_compatibility = get_dasha_transit_compatibility(self.natal_chart, transits['transit_chart'])
        
        # Generate a Dasha prediction
        prediction = generate_dasha_prediction(transits['transit_dasha_effects'], dasha_compatibility)
        
        # Check that the result is a list
        self.assertIsInstance(prediction, list)
    
    def test_analyze_transits(self):
        """Test analyze_transits function"""
        # Calculate the end date
        end_dt = self.transit_date.datetime() + timedelta(days=30)
        end_date = Datetime.fromDatetime(end_dt)
        
        # Analyze transits
        analysis = analyze_transits(self.natal_chart, self.transit_date, end_date)
        
        # Check that all required keys are present
        self.assertIn('start_date', analysis)
        self.assertIn('end_date', analysis)
        self.assertIn('transit_quality', analysis)
        self.assertIn('timeline', analysis)
        self.assertIn('events', analysis)
        self.assertIn('periods', analysis)
        self.assertIn('predictions', analysis)
    
    def test_get_transit_compatibility(self):
        """Test get_transit_compatibility function"""
        # Create a second natal chart
        birth_date2 = Datetime('1995/01/01', '12:00', '+05:30')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        natal_chart2 = Chart(birth_date2, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
        
        # Get transit compatibility
        compatibility = get_transit_compatibility(self.natal_chart, natal_chart2, self.transit_date)
        
        # Check that all required keys are present
        self.assertIn('score', compatibility)
        self.assertIn('factors', compatibility)
        self.assertIn('description', compatibility)
        
        # Check that the score is within 0-100
        self.assertGreaterEqual(compatibility['score'], 0)
        self.assertLessEqual(compatibility['score'], 100)
    
    def test_get_transit_strength_score(self):
        """Test get_transit_strength_score function"""
        # Get transit strength score
        score = get_transit_strength_score(self.natal_chart, self.transit_date)
        
        # Check that the score is within 0-100
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
    
    def test_get_transit_analysis(self):
        """Test get_transit_analysis function"""
        # Get transit analysis
        analysis = get_transit_analysis(self.natal_chart, self.transit_date)
        
        # Check that all required keys are present
        self.assertIn('date', analysis)
        self.assertIn('transit_chart', analysis)
        self.assertIn('transit_planets', analysis)
        self.assertIn('transit_aspects', analysis)
        self.assertIn('transit_houses', analysis)
        self.assertIn('transit_quality', analysis)
        self.assertIn('gochara_effects', analysis)
        self.assertIn('transit_ashtakavarga', analysis)
        self.assertIn('transit_dasha_effects', analysis)
        self.assertIn('dasha_compatibility', analysis)
        self.assertIn('strength_score', analysis)
        self.assertIn('predictions', analysis)
    
    def test_get_transits(self):
        """Test get_transits function"""
        # Get transits
        transits = get_transits(self.natal_chart, self.transit_date)
        
        # Check that all required keys are present
        self.assertIn('transit_chart', transits)
        self.assertIn('transit_planets', transits)
        self.assertIn('transit_aspects', transits)
        self.assertIn('transit_houses', transits)
        self.assertIn('transit_quality', transits)
        self.assertIn('gochara_effects', transits)
        self.assertIn('transit_ashtakavarga', transits)
        self.assertIn('transit_dasha_effects', transits)
    
    def test_get_transit_predictions_for_date(self):
        """Test get_transit_predictions_for_date function"""
        # Get transit predictions
        predictions = get_transit_predictions_for_date(self.natal_chart, self.transit_date)
        
        # Check that all required keys are present
        self.assertIn('general', predictions)
        self.assertIn('planets', predictions)
        self.assertIn('houses', predictions)
        self.assertIn('dashas', predictions)
    
    def test_get_transit_timeline_for_period(self):
        """Test get_transit_timeline_for_period function"""
        # Calculate the end date
        end_dt = self.transit_date.datetime() + timedelta(days=30)
        end_date = Datetime.fromDatetime(end_dt)
        
        # Get transit timeline
        timeline = get_transit_timeline_for_period(self.natal_chart, self.transit_date, end_date)
        
        # Check that the result is a list
        self.assertIsInstance(timeline, list)

if __name__ == '__main__':
    unittest.main()
