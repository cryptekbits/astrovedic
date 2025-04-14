#!/usr/bin/env python3
"""
Test Sarvatobhadra Chakra Calculations

This script tests the Sarvatobhadra Chakra calculations in astrovedic.
"""

import unittest
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic import const
from astrovedic.vedic.sarvatobhadra import (
    get_sarvatobhadra_chakra, get_chakra_quality,
    get_auspicious_directions, get_inauspicious_directions,
    get_best_direction, get_direction_for_activity,
    get_tara_bala, get_sarvatobhadra_predictions,
    analyze_sarvatobhadra
)
from astrovedic.vedic.sarvatobhadra.chakra import (
    create_chakra, get_chakra_cell, get_chakra_row,
    get_chakra_column, get_chakra_diagonal,
    get_direction_cells, get_nakshatras_in_direction,
    get_planets_in_direction
)
from astrovedic.vedic.sarvatobhadra.directions import (
    get_direction_quality, get_best_direction,
    get_direction_for_activity, get_direction_compatibility
)
from astrovedic.vedic.sarvatobhadra.tara import (
    get_tara_bala, get_janma_tara, get_sampath_tara,
    get_vipat_tara, get_kshema_tara, get_pratyak_tara,
    get_sadhaka_tara, get_vadha_tara, get_mitra_tara,
    get_ati_mitra_tara, get_current_tara, get_tara_bala_score
)
from astrovedic.vedic.sarvatobhadra.analysis import (
    analyze_sarvatobhadra, get_sarvatobhadra_predictions,
    get_sarvatobhadra_compatibility, get_sarvatobhadra_strength_score
)

class TestSarvatobhadra(unittest.TestCase):
    """Test case for Sarvatobhadra Chakra calculations"""
    
    def setUp(self):
        """Set up test case"""
        # Create a chart for the reference date
        date = Datetime('2025/04/09', '20:51', '+05:30')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart = Chart(date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
    
    def test_create_chakra(self):
        """Test create_chakra function"""
        # Create a chakra with a specific birth nakshatra
        chakra = create_chakra(1)  # Ashwini
        
        # Check that all required keys are present
        self.assertIn('janma_nakshatra', chakra)
        self.assertIn('grid', chakra)
        
        # Check that the grid is a 9x9 grid
        self.assertEqual(len(chakra['grid']), 9)
        for row in chakra['grid']:
            self.assertEqual(len(row), 9)
        
        # Check that the center cell contains the birth nakshatra
        self.assertEqual(chakra['grid'][4][4], 1)
    
    def test_get_sarvatobhadra_chakra(self):
        """Test get_sarvatobhadra_chakra function"""
        # Get the Sarvatobhadra Chakra
        chakra = get_sarvatobhadra_chakra(self.chart)
        
        # Check that all required keys are present
        self.assertIn('janma_nakshatra', chakra)
        self.assertIn('grid', chakra)
        self.assertIn('planets', chakra)
        self.assertIn('tara_bala', chakra)
        
        # Check that the planets dictionary contains all planets
        for planet_id in const.LIST_OBJECTS_VEDIC + [const.ASC]:
            self.assertIn(planet_id, chakra['planets'])
    
    def test_get_chakra_cell(self):
        """Test get_chakra_cell function"""
        # Create a chakra
        chakra = create_chakra(1)
        
        # Get a cell
        cell = get_chakra_cell(chakra, 4, 4)
        
        # Check that the cell contains the birth nakshatra
        self.assertEqual(cell, 1)
    
    def test_get_chakra_row(self):
        """Test get_chakra_row function"""
        # Create a chakra
        chakra = create_chakra(1)
        
        # Get a row
        row = get_chakra_row(chakra, 4)
        
        # Check that the row is a list of length 9
        self.assertEqual(len(row), 9)
        
        # Check that the center cell contains the birth nakshatra
        self.assertEqual(row[4], 1)
    
    def test_get_chakra_column(self):
        """Test get_chakra_column function"""
        # Create a chakra
        chakra = create_chakra(1)
        
        # Get a column
        column = get_chakra_column(chakra, 4)
        
        # Check that the column is a list of length 9
        self.assertEqual(len(column), 9)
        
        # Check that the center cell contains the birth nakshatra
        self.assertEqual(column[4], 1)
    
    def test_get_chakra_diagonal(self):
        """Test get_chakra_diagonal function"""
        # Create a chakra
        chakra = create_chakra(1)
        
        # Get the main diagonal
        diagonal = get_chakra_diagonal(chakra, 'main')
        
        # Check that the diagonal is a list of length 9
        self.assertEqual(len(diagonal), 9)
    
    def test_get_direction_cells(self):
        """Test get_direction_cells function"""
        # Create a chakra
        chakra = create_chakra(1)
        
        # Get the cells in a direction
        cells = get_direction_cells(chakra, 'North')
        
        # Check that the cells are a list
        self.assertIsInstance(cells, list)
    
    def test_get_nakshatras_in_direction(self):
        """Test get_nakshatras_in_direction function"""
        # Create a chakra
        chakra = create_chakra(1)
        
        # Get the nakshatras in a direction
        nakshatras = get_nakshatras_in_direction(chakra, 'North')
        
        # Check that the nakshatras are a list
        self.assertIsInstance(nakshatras, list)
    
    def test_get_planets_in_direction(self):
        """Test get_planets_in_direction function"""
        # Get the Sarvatobhadra Chakra
        chakra = get_sarvatobhadra_chakra(self.chart)
        
        # Get the planets in a direction
        planets = get_planets_in_direction(chakra, 'North')
        
        # Check that the planets are a list
        self.assertIsInstance(planets, list)
    
    def test_get_direction_quality(self):
        """Test get_direction_quality function"""
        # Get the Sarvatobhadra Chakra
        chakra = get_sarvatobhadra_chakra(self.chart)
        
        # Get the quality of a direction
        quality = get_direction_quality(chakra, 'North')
        
        # Check that all required keys are present
        self.assertIn('direction', quality)
        self.assertIn('score', quality)
        self.assertIn('quality', quality)
        self.assertIn('factors', quality)
        
        # Check that the quality is one of the expected values
        self.assertIn(quality['quality'], ['Excellent', 'Good', 'Neutral', 'Inauspicious', 'Highly Inauspicious'])
    
    def test_get_best_direction(self):
        """Test get_best_direction function"""
        # Get the Sarvatobhadra Chakra
        chakra = get_sarvatobhadra_chakra(self.chart)
        
        # Get the best direction
        best_direction = get_best_direction(chakra)
        
        # Check that all required keys are present
        self.assertIn('direction', best_direction)
        self.assertIn('score', best_direction)
        self.assertIn('quality', best_direction)
        self.assertIn('factors', best_direction)
    
    def test_get_direction_for_activity(self):
        """Test get_direction_for_activity function"""
        # Get the Sarvatobhadra Chakra
        chakra = get_sarvatobhadra_chakra(self.chart)
        
        # Get the best direction for an activity
        direction = get_direction_for_activity(chakra, 'marriage')
        
        # Check that all required keys are present
        self.assertIn('direction', direction)
        self.assertIn('score', direction)
        self.assertIn('quality', direction)
        self.assertIn('factors', direction)
    
    def test_get_direction_compatibility(self):
        """Test get_direction_compatibility function"""
        # Get the Sarvatobhadra Chakra
        chakra = get_sarvatobhadra_chakra(self.chart)
        
        # Get the compatibility between two directions
        compatibility = get_direction_compatibility(chakra, 'North', 'East')
        
        # Check that all required keys are present
        self.assertIn('score', compatibility)
        self.assertIn('factors', compatibility)
        self.assertIn('description', compatibility)
        
        # Check that the score is within 0-100
        self.assertGreaterEqual(compatibility['score'], 0)
        self.assertLessEqual(compatibility['score'], 100)
    
    def test_get_tara_bala(self):
        """Test get_tara_bala function"""
        # Get the Tara Bala
        tara_bala = get_tara_bala(self.chart)
        
        # Check that all required keys are present
        self.assertIn('janma_tara', tara_bala)
        self.assertIn('sampath_tara', tara_bala)
        self.assertIn('vipat_tara', tara_bala)
        self.assertIn('kshema_tara', tara_bala)
        self.assertIn('pratyak_tara', tara_bala)
        self.assertIn('sadhaka_tara', tara_bala)
        self.assertIn('vadha_tara', tara_bala)
        self.assertIn('mitra_tara', tara_bala)
        self.assertIn('ati_mitra_tara', tara_bala)
        self.assertIn('current_tara', tara_bala)
        self.assertIn('score', tara_bala)
    
    def test_get_tara_functions(self):
        """Test Tara calculation functions"""
        # Test with a specific birth nakshatra
        janma_tara = 1  # Ashwini
        
        # Test each Tara calculation function
        self.assertEqual(get_janma_tara(janma_tara), 1)
        self.assertEqual(get_sampath_tara(janma_tara), 5)
        self.assertEqual(get_vipat_tara(janma_tara), 10)
        self.assertEqual(get_kshema_tara(janma_tara), 15)
        self.assertEqual(get_pratyak_tara(janma_tara), 20)
        self.assertEqual(get_sadhaka_tara(janma_tara), 25)
        self.assertEqual(get_vadha_tara(janma_tara), 3)
        self.assertEqual(get_mitra_tara(janma_tara), 8)
        self.assertEqual(get_ati_mitra_tara(janma_tara), 13)
    
    def test_get_current_tara(self):
        """Test get_current_tara function"""
        # Test with specific birth and current nakshatras
        janma_tara = 1  # Ashwini
        current_nakshatra = 5  # Mrigashira
        
        # Get the current Tara
        current_tara = get_current_tara(janma_tara, current_nakshatra)
        
        # Check that the current Tara is a string
        self.assertIsInstance(current_tara, str)
        
        # Check that the current Tara is one of the expected values
        self.assertIn(current_tara, [
            'Janma Tara', 'Sampath Tara', 'Vipat Tara', 'Kshema Tara',
            'Pratyak Tara', 'Sadhaka Tara', 'Vadha Tara', 'Mitra Tara', 'Ati Mitra Tara'
        ])
    
    def test_get_tara_bala_score(self):
        """Test get_tara_bala_score function"""
        # Test with each Tara
        for tara in [
            'Janma Tara', 'Sampath Tara', 'Vipat Tara', 'Kshema Tara',
            'Pratyak Tara', 'Sadhaka Tara', 'Vadha Tara', 'Mitra Tara', 'Ati Mitra Tara'
        ]:
            # Get the Tara Bala score
            score = get_tara_bala_score(tara)
            
            # Check that the score is within 0-100
            self.assertGreaterEqual(score, 0)
            self.assertLessEqual(score, 100)
    
    def test_get_chakra_quality(self):
        """Test get_chakra_quality function"""
        # Get the Sarvatobhadra Chakra
        chakra = get_sarvatobhadra_chakra(self.chart)
        
        # Get the chakra quality
        quality = get_chakra_quality(chakra)
        
        # Check that all required keys are present
        self.assertIn('score', quality)
        self.assertIn('quality', quality)
        self.assertIn('factors', quality)
        
        # Check that the quality is one of the expected values
        self.assertIn(quality['quality'], ['Excellent', 'Good', 'Neutral', 'Inauspicious', 'Highly Inauspicious'])
    
    def test_get_auspicious_directions(self):
        """Test get_auspicious_directions function"""
        # Get the Sarvatobhadra Chakra
        chakra = get_sarvatobhadra_chakra(self.chart)
        
        # Get the auspicious directions
        auspicious_directions = get_auspicious_directions(chakra)
        
        # Check that the result is a list
        self.assertIsInstance(auspicious_directions, list)
        
        # Check that each direction has the required keys
        for direction in auspicious_directions:
            self.assertIn('direction', direction)
            self.assertIn('quality', direction)
            self.assertIn('score', direction)
            self.assertIn('factors', direction)
    
    def test_get_inauspicious_directions(self):
        """Test get_inauspicious_directions function"""
        # Get the Sarvatobhadra Chakra
        chakra = get_sarvatobhadra_chakra(self.chart)
        
        # Get the inauspicious directions
        inauspicious_directions = get_inauspicious_directions(chakra)
        
        # Check that the result is a list
        self.assertIsInstance(inauspicious_directions, list)
        
        # Check that each direction has the required keys
        for direction in inauspicious_directions:
            self.assertIn('direction', direction)
            self.assertIn('quality', direction)
            self.assertIn('score', direction)
            self.assertIn('factors', direction)
    
    def test_analyze_sarvatobhadra(self):
        """Test analyze_sarvatobhadra function"""
        # Analyze the Sarvatobhadra Chakra
        analysis = analyze_sarvatobhadra(self.chart)
        
        # Check that all required keys are present
        self.assertIn('chakra', analysis)
        self.assertIn('quality', analysis)
        self.assertIn('auspicious_directions', analysis)
        self.assertIn('inauspicious_directions', analysis)
        self.assertIn('best_direction', analysis)
        self.assertIn('tara_bala', analysis)
        self.assertIn('current_tara', analysis)
        self.assertIn('tara_description', analysis)
        self.assertIn('is_favorable_tara', analysis)
        self.assertIn('is_unfavorable_tara', analysis)
        self.assertIn('tara_score', analysis)
        self.assertIn('activity_directions', analysis)
    
    def test_get_sarvatobhadra_predictions(self):
        """Test get_sarvatobhadra_predictions function"""
        # Generate predictions
        predictions = get_sarvatobhadra_predictions(self.chart)
        
        # Check that all required keys are present
        self.assertIn('general', predictions)
        self.assertIn('directions', predictions)
        self.assertIn('tara_bala', predictions)
        self.assertIn('activities', predictions)
    
    def test_get_sarvatobhadra_compatibility(self):
        """Test get_sarvatobhadra_compatibility function"""
        # Create a second chart
        date = Datetime('2025/05/09', '20:51', '+05:30')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        chart2 = Chart(date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
        
        # Calculate compatibility
        compatibility = get_sarvatobhadra_compatibility(self.chart, chart2)
        
        # Check that all required keys are present
        self.assertIn('score', compatibility)
        self.assertIn('factors', compatibility)
        self.assertIn('description', compatibility)
        
        # Check that the score is within 0-100
        self.assertGreaterEqual(compatibility['score'], 0)
        self.assertLessEqual(compatibility['score'], 100)
    
    def test_get_sarvatobhadra_strength_score(self):
        """Test get_sarvatobhadra_strength_score function"""
        # Calculate the strength score
        score = get_sarvatobhadra_strength_score(self.chart)
        
        # Check that the score is within 0-100
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

if __name__ == '__main__':
    unittest.main()
