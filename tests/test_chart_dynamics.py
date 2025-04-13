#!/usr/bin/env python3
"""
Test Chart Dynamics

This script tests the chart dynamics calculations in flatlib.
"""

import unittest
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib.tools.chartdynamics import ChartDynamics


class TestChartDynamics(unittest.TestCase):
    """Test case for chart dynamics calculations"""
    
    def setUp(self):
        """Set up test case"""
        # Create a chart for testing
        date = Datetime('2025/04/09', '20:51', '+05:30')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart = Chart(date, pos)
        
        # Create ChartDynamics object
        self.dyn = ChartDynamics(self.chart)
    
    def test_in_dignities(self):
        """Test inDignities method"""
        # Test with various planet pairs
        test_cases = [
            (const.SUN, const.JUPITER),
            (const.MOON, const.VENUS),
            (const.MERCURY, const.MERCURY),
            (const.VENUS, const.MARS),
            (const.MARS, const.SATURN),
            (const.JUPITER, const.SUN),
            (const.SATURN, const.MOON)
        ]
        
        for planet_a, planet_b in test_cases:
            # Get the dignities of planet A which belong to planet B
            dignities = self.dyn.inDignities(planet_a, planet_b)
            
            # Check that the dignities is a list
            self.assertIsInstance(dignities, list)
            
            # Print the dignities for reference
            print(f"Dignities of {planet_a} which belong to {planet_b}: {dignities}")
    
    def test_receives(self):
        """Test receives method"""
        # Test with various planet pairs
        test_cases = [
            (const.SUN, const.JUPITER),
            (const.MOON, const.VENUS),
            (const.MERCURY, const.MERCURY),
            (const.VENUS, const.MARS),
            (const.MARS, const.SATURN),
            (const.JUPITER, const.SUN),
            (const.SATURN, const.MOON)
        ]
        
        for planet_a, planet_b in test_cases:
            # Get the dignities where planet A receives planet B
            dignities = self.dyn.receives(planet_a, planet_b)
            
            # Check that the dignities is a list
            self.assertIsInstance(dignities, list)
            
            # Print the dignities for reference
            print(f"Dignities where {planet_a} receives {planet_b}: {dignities}")
    
    def test_disposits(self):
        """Test disposits method"""
        # Test with various planet pairs
        test_cases = [
            (const.SUN, const.JUPITER),
            (const.MOON, const.VENUS),
            (const.MERCURY, const.MERCURY),
            (const.VENUS, const.MARS),
            (const.MARS, const.SATURN),
            (const.JUPITER, const.SUN),
            (const.SATURN, const.MOON)
        ]
        
        for planet_a, planet_b in test_cases:
            # Get the dignities where planet A is dispositor of planet B
            dignities = self.dyn.disposits(planet_a, planet_b)
            
            # Check that the dignities is a list
            self.assertIsInstance(dignities, list)
            
            # Print the dignities for reference
            print(f"Dignities where {planet_a} is dispositor of {planet_b}: {dignities}")
    
    def test_mutual_receptions(self):
        """Test mutualReceptions method"""
        # Test with various planet pairs
        test_cases = [
            (const.SUN, const.JUPITER),
            (const.MOON, const.VENUS),
            (const.MERCURY, const.MERCURY),
            (const.VENUS, const.MARS),
            (const.MARS, const.SATURN),
            (const.JUPITER, const.SUN),
            (const.SATURN, const.MOON)
        ]
        
        for planet_a, planet_b in test_cases:
            # Get the mutual receptions between planet A and planet B
            receptions = self.dyn.mutualReceptions(planet_a, planet_b)
            
            # Check that the receptions is a list
            self.assertIsInstance(receptions, list)
            
            # Print the receptions for reference
            print(f"Mutual receptions between {planet_a} and {planet_b}: {receptions}")
    
    def test_re_mutual_receptions(self):
        """Test reMutualReceptions method"""
        # Test with various planet pairs
        test_cases = [
            (const.SUN, const.JUPITER),
            (const.MOON, const.VENUS),
            (const.MERCURY, const.MERCURY),
            (const.VENUS, const.MARS),
            (const.MARS, const.SATURN),
            (const.JUPITER, const.SUN),
            (const.SATURN, const.MOON)
        ]
        
        for planet_a, planet_b in test_cases:
            # Get the ruler and exaltation mutual receptions between planet A and planet B
            receptions = self.dyn.reMutualReceptions(planet_a, planet_b)
            
            # Check that the receptions is a list
            self.assertIsInstance(receptions, list)
            
            # Print the receptions for reference
            print(f"Ruler and exaltation mutual receptions between {planet_a} and {planet_b}: {receptions}")
    
    def test_valid_aspects(self):
        """Test validAspects method"""
        # Test with various planets
        test_cases = [
            const.SUN,
            const.MOON,
            const.MERCURY,
            const.VENUS,
            const.MARS,
            const.JUPITER,
            const.SATURN
        ]
        
        for planet in test_cases:
            # Get the valid aspects for the planet
            aspects = self.dyn.validAspects(planet, const.MAJOR_ASPECTS)
            
            # Check that the aspects is a list
            self.assertIsInstance(aspects, list)
            
            # Print the aspects for reference
            print(f"Valid aspects for {planet}:")
            for aspect in aspects:
                print(f"  {aspect['id']} - {aspect['asp']}")
    
    def test_aspects_by_cat(self):
        """Test aspectsByCat method"""
        # Test with various planets
        test_cases = [
            const.SUN,
            const.MOON,
            const.MERCURY,
            const.VENUS,
            const.MARS,
            const.JUPITER,
            const.SATURN
        ]
        
        for planet in test_cases:
            # Get the aspects by category for the planet
            aspects = self.dyn.aspectsByCat(planet, const.MAJOR_ASPECTS)
            
            # Check that the aspects is a dictionary
            self.assertIsInstance(aspects, dict)
            
            # Check that the dictionary has the required keys
            self.assertIn(const.APPLICATIVE, aspects)
            self.assertIn(const.SEPARATIVE, aspects)
            self.assertIn(const.EXACT, aspects)
            self.assertIn(const.NO_MOVEMENT, aspects)
            
            # Print the aspects for reference
            print(f"Aspects by category for {planet}:")
            for category, category_aspects in aspects.items():
                print(f"  {category}:")
                for aspect in category_aspects:
                    print(f"    {aspect['id']} - {aspect['asp']} - {aspect['orb']:.2f}°")
    
    def test_immediate_aspects(self):
        """Test immediateAspects method"""
        # Test with various planets
        test_cases = [
            const.SUN,
            const.MOON,
            const.MERCURY,
            const.VENUS,
            const.MARS,
            const.JUPITER,
            const.SATURN
        ]
        
        for planet in test_cases:
            # Get the immediate aspects for the planet
            separation, application = self.dyn.immediateAspects(planet, const.MAJOR_ASPECTS)
            
            # Print the aspects for reference
            print(f"Immediate aspects for {planet}:")
            print(f"  Last separation: {separation}")
            print(f"  Next application: {application}")
    
    def test_is_voc(self):
        """Test isVOC method"""
        # Test with various planets
        test_cases = [
            const.SUN,
            const.MOON,
            const.MERCURY,
            const.VENUS,
            const.MARS,
            const.JUPITER,
            const.SATURN
        ]
        
        for planet in test_cases:
            # Check if the planet is Void of Course
            is_voc = self.dyn.isVOC(planet)
            
            # Check that the result is a boolean
            self.assertIsInstance(is_voc, bool)
            
            # Print the result for reference
            print(f"{planet} is Void of Course: {is_voc}")


if __name__ == '__main__':
    unittest.main()
