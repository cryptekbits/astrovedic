#!/usr/bin/env python3
"""
Test Ashtakavarga Calculations

This script tests the Ashtakavarga (eight-source strength) calculations in flatlib.
"""

import unittest
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib.vedic.ashtakavarga import (
    get_bhinnashtakavarga, get_sarvashtakavarga, get_all_ashtakavarga,
    get_kaksha_bala, get_transit_ashtakavarga, LIST_ASHTAKAVARGA_PLANETS
)
from flatlib.vedic.ashtakavarga.bhinna import (
    calculate_bhinnashtakavarga, get_benefic_points,
    get_malefic_points, get_rekha_points
)
from flatlib.vedic.ashtakavarga.sarva import (
    calculate_sarvashtakavarga, get_trikona_sodhana,
    get_ekadhi_sodhana, get_sodhita_sarvashtakavarga
)
from flatlib.vedic.ashtakavarga.analysis import (
    get_bindus_in_houses, get_bindus_in_signs,
    get_ashtakavarga_predictions, get_ashtakavarga_strength_in_house
)

class TestAshtakavarga(unittest.TestCase):
    """Test case for Ashtakavarga calculations"""
    
    def setUp(self):
        """Set up test case"""
        # Create a chart for the reference date
        date = Datetime('2025/04/09', '20:51', '+05:30')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart = Chart(date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
    
    def test_bhinnashtakavarga(self):
        """Test Bhinnashtakavarga calculations"""
        # Calculate Bhinnashtakavarga for the Sun
        sun_bhinna = get_bhinnashtakavarga(self.chart, const.SUN)
        
        # Check that all required keys are present
        self.assertIn('planet', sun_bhinna)
        self.assertIn('points', sun_bhinna)
        self.assertIn('contributors', sun_bhinna)
        self.assertIn('total_bindus', sun_bhinna)
        self.assertIn('bindus_in_houses', sun_bhinna)
        self.assertIn('bindus_in_signs', sun_bhinna)
        
        # Check that the planet ID is correct
        self.assertEqual(sun_bhinna['planet'], const.SUN)
        
        # Check that there are 12 points (one for each sign)
        self.assertEqual(len(sun_bhinna['points']), 12)
        
        # Check that the total bindus is the sum of the points
        self.assertEqual(sun_bhinna['total_bindus'], sum(sun_bhinna['points']))
        
        # Check that there are 8 contributors
        self.assertEqual(len(sun_bhinna['contributors']), 8)
        
        # Check that each contributor has 12 points
        for contributor_id, points in sun_bhinna['contributors'].items():
            self.assertEqual(len(points), 12)
    
    def test_sarvashtakavarga(self):
        """Test Sarvashtakavarga calculations"""
        # Calculate Sarvashtakavarga
        sarva = get_sarvashtakavarga(self.chart)
        
        # Check that all required keys are present
        self.assertIn('points', sarva)
        self.assertIn('planet_contributions', sarva)
        self.assertIn('total_bindus', sarva)
        self.assertIn('bindus_in_houses', sarva)
        self.assertIn('bindus_in_signs', sarva)
        self.assertIn('trikona_sodhana', sarva)
        self.assertIn('ekadhi_sodhana', sarva)
        self.assertIn('sodhita_sarvashtakavarga', sarva)
        
        # Check that there are 12 points (one for each sign)
        self.assertEqual(len(sarva['points']), 12)
        
        # Check that the total bindus is the sum of the points
        self.assertEqual(sarva['total_bindus'], sum(sarva['points']))
        
        # Check that there are 7 planet contributions
        self.assertEqual(len(sarva['planet_contributions']), 7)
        
        # Check that each planet contribution has 12 points
        for planet_id, points in sarva['planet_contributions'].items():
            self.assertEqual(len(points), 12)
        
        # Check that there are 12 bindus in houses
        self.assertEqual(len(sarva['bindus_in_houses']), 12)
        
        # Check that there are 12 signs in bindus_in_signs
        self.assertEqual(len(sarva['bindus_in_signs']), 12)
        
        # Check that there are 12 points in trikona_sodhana
        self.assertEqual(len(sarva['trikona_sodhana']), 12)
        
        # Check that there are 12 points in ekadhi_sodhana
        self.assertEqual(len(sarva['ekadhi_sodhana']), 12)
        
        # Check that there are 12 points in sodhita_sarvashtakavarga
        self.assertEqual(len(sarva['sodhita_sarvashtakavarga']), 12)
    
    def test_all_ashtakavarga(self):
        """Test get_all_ashtakavarga function"""
        # Calculate all Ashtakavarga data
        all_ashtakavarga = get_all_ashtakavarga(self.chart)
        
        # Check that all required keys are present
        self.assertIn('bhinnashtakavarga', all_ashtakavarga)
        self.assertIn('sarvashtakavarga', all_ashtakavarga)
        self.assertIn('summary', all_ashtakavarga)
        
        # Check that there are 7 planets in bhinnashtakavarga
        self.assertEqual(len(all_ashtakavarga['bhinnashtakavarga']), 7)
        
        # Check that the summary contains the required keys
        summary = all_ashtakavarga['summary']
        self.assertIn('total_bindus', summary)
        self.assertIn('planet_totals', summary)
        self.assertIn('average_bindus', summary)
        self.assertIn('strongest_planet', summary)
        self.assertIn('weakest_planet', summary)
        
        # Check that the strongest and weakest planets are valid
        self.assertIn(summary['strongest_planet'], LIST_ASHTAKAVARGA_PLANETS)
        self.assertIn(summary['weakest_planet'], LIST_ASHTAKAVARGA_PLANETS)
    
    def test_kaksha_bala(self):
        """Test Kaksha Bala calculations"""
        # Calculate Kaksha Bala for the Sun
        sun_kaksha = get_kaksha_bala(self.chart, const.SUN)
        
        # Check that all required keys are present
        self.assertIn('planet', sun_kaksha)
        self.assertIn('sign', sun_kaksha)
        self.assertIn('kaksha_bala', sun_kaksha)
        self.assertIn('percentage', sun_kaksha)
        self.assertIn('category', sun_kaksha)
        self.assertIn('contributions', sun_kaksha)
        
        # Check that the planet ID is correct
        self.assertEqual(sun_kaksha['planet'], const.SUN)
        
        # Check that the sign is valid
        self.assertIn(sun_kaksha['sign'], [
            const.ARIES, const.TAURUS, const.GEMINI, const.CANCER,
            const.LEO, const.VIRGO, const.LIBRA, const.SCORPIO,
            const.SAGITTARIUS, const.CAPRICORN, const.AQUARIUS, const.PISCES
        ])
        
        # Check that there are 6 contributions (from all planets except the Sun itself)
        self.assertEqual(len(sun_kaksha['contributions']), 6)
        
        # Check that the kaksha_bala is the sum of the contributions
        self.assertEqual(sun_kaksha['kaksha_bala'], sum(sun_kaksha['contributions'].values()))
        
        # Check that the percentage is calculated correctly
        self.assertAlmostEqual(sun_kaksha['percentage'], (sun_kaksha['kaksha_bala'] / 42.0) * 100.0)
        
        # Check that the category is valid
        self.assertIn(sun_kaksha['category'], ['Very Strong', 'Strong', 'Moderate', 'Weak'])
    
    def test_transit_ashtakavarga(self):
        """Test transit Ashtakavarga calculations"""
        # Create a transit chart
        transit_date = Datetime('2025/05/09', '20:51', '+05:30')
        transit_pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        transit_chart = Chart(transit_date, transit_pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
        
        # Calculate transit Ashtakavarga for the Sun
        sun_transit = get_transit_ashtakavarga(self.chart, transit_chart, const.SUN)
        
        # Check that all required keys are present
        self.assertIn('planet', sun_transit)
        self.assertIn('transit_sign', sun_transit)
        self.assertIn('transit_strength', sun_transit)
        self.assertIn('best_positions', sun_transit)
        
        # Check that the planet ID is correct
        self.assertEqual(sun_transit['planet'], const.SUN)
        
        # Check that the transit sign is valid
        self.assertIn(sun_transit['transit_sign'], [
            const.ARIES, const.TAURUS, const.GEMINI, const.CANCER,
            const.LEO, const.VIRGO, const.LIBRA, const.SCORPIO,
            const.SAGITTARIUS, const.CAPRICORN, const.AQUARIUS, const.PISCES
        ])
        
        # Check that the transit strength contains the required keys
        transit_strength = sun_transit['transit_strength']
        self.assertIn('bindus', transit_strength)
        self.assertIn('percentage', transit_strength)
        self.assertIn('category', transit_strength)
        self.assertIn('description', transit_strength)
        
        # Check that the bindus is between 0 and 8
        self.assertGreaterEqual(transit_strength['bindus'], 0)
        self.assertLessEqual(transit_strength['bindus'], 8)
        
        # Check that the percentage is calculated correctly
        self.assertAlmostEqual(transit_strength['percentage'], (transit_strength['bindus'] / 8.0) * 100.0)
        
        # Check that the category is valid
        self.assertIn(transit_strength['category'], ['Excellent', 'Good', 'Moderate', 'Weak'])
        
        # Check that there are 12 best positions
        self.assertEqual(len(sun_transit['best_positions']), 12)
        
        # Check that the best positions are valid sign numbers (0-11)
        for pos in sun_transit['best_positions']:
            self.assertGreaterEqual(pos, 0)
            self.assertLessEqual(pos, 11)
    
    def test_bindus_in_houses(self):
        """Test get_bindus_in_houses function"""
        # Create a list of points (one for each sign)
        points = [3, 4, 5, 6, 7, 8, 2, 3, 4, 5, 6, 7]
        
        # Calculate bindus in houses
        bindus_in_houses = get_bindus_in_houses(self.chart, points)
        
        # Check that there are 12 houses
        self.assertEqual(len(bindus_in_houses), 12)
        
        # Check that the total bindus is the same
        self.assertEqual(sum(bindus_in_houses), sum(points))
    
    def test_bindus_in_signs(self):
        """Test get_bindus_in_signs function"""
        # Create a list of points (one for each sign)
        points = [3, 4, 5, 6, 7, 8, 2, 3, 4, 5, 6, 7]
        
        # Calculate bindus in signs
        bindus_in_signs = get_bindus_in_signs(points)
        
        # Check that there are 12 signs
        self.assertEqual(len(bindus_in_signs), 12)
        
        # Check that the total bindus is the same
        self.assertEqual(sum(bindus_in_signs.values()), sum(points))
        
        # Check that all signs are present
        for sign in [const.ARIES, const.TAURUS, const.GEMINI, const.CANCER,
                    const.LEO, const.VIRGO, const.LIBRA, const.SCORPIO,
                    const.SAGITTARIUS, const.CAPRICORN, const.AQUARIUS, const.PISCES]:
            self.assertIn(sign, bindus_in_signs)
    
    def test_ashtakavarga_predictions(self):
        """Test get_ashtakavarga_predictions function"""
        # Calculate all Ashtakavarga data
        all_ashtakavarga = get_all_ashtakavarga(self.chart)
        
        # Generate predictions
        predictions = get_ashtakavarga_predictions(all_ashtakavarga)
        
        # Check that all required keys are present
        self.assertIn('general', predictions)
        self.assertIn('planets', predictions)
        self.assertIn('houses', predictions)
        
        # Check that there is at least one general prediction
        self.assertGreater(len(predictions['general']), 0)
        
        # Check that there are 7 planet predictions
        self.assertEqual(len(predictions['planets']), 7)
        
        # Check that there are 12 house predictions
        self.assertEqual(len(predictions['houses']), 12)
    
    def test_ashtakavarga_strength_in_house(self):
        """Test get_ashtakavarga_strength_in_house function"""
        # Calculate the strength of the 1st house
        house1_strength = get_ashtakavarga_strength_in_house(self.chart, 1)
        
        # Check that all required keys are present
        self.assertIn('house', house1_strength)
        self.assertIn('sign', house1_strength)
        self.assertIn('total_bindus', house1_strength)
        self.assertIn('percentage', house1_strength)
        self.assertIn('category', house1_strength)
        self.assertIn('planet_contributions', house1_strength)
        
        # Check that the house number is correct
        self.assertEqual(house1_strength['house'], 1)
        
        # Check that the sign is valid
        self.assertIn(house1_strength['sign'], [
            const.ARIES, const.TAURUS, const.GEMINI, const.CANCER,
            const.LEO, const.VIRGO, const.LIBRA, const.SCORPIO,
            const.SAGITTARIUS, const.CAPRICORN, const.AQUARIUS, const.PISCES
        ])
        
        # Check that there are 7 planet contributions
        self.assertEqual(len(house1_strength['planet_contributions']), 7)
        
        # Check that the total bindus is the sum of the contributions
        self.assertEqual(house1_strength['total_bindus'], sum(house1_strength['planet_contributions'].values()))
        
        # Check that the percentage is calculated correctly
        self.assertAlmostEqual(house1_strength['percentage'], (house1_strength['total_bindus'] / 56.0) * 100.0)
        
        # Check that the category is valid
        self.assertIn(house1_strength['category'], ['Very Strong', 'Strong', 'Moderate', 'Weak'])

if __name__ == '__main__':
    unittest.main()
