#!/usr/bin/env python3
"""
Test Primary Directions Calculations

This script tests the Primary Directions calculations in flatlib.
"""

import unittest
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib.predictives import primarydirections
from flatlib.predictives.primarydirections import PrimaryDirections, PDTable


class TestPrimaryDirections(unittest.TestCase):
    """Test case for Primary Directions calculations"""
    
    def setUp(self):
        """Set up test case"""
        # Create a chart for testing
        date = Datetime('2025/04/09', '20:51', '+05:30')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart = Chart(date, pos)
    
    def test_get_arc(self):
        """Test getArc function"""
        # Get the MC
        mc = self.chart.getAngle(const.MC)
        
        # Get a promissor and significator
        prom = self.chart.getObject(const.MARS)
        sig = self.chart.getObject(const.MERCURY)
        
        # Compute arc in zodiaco (zerolat = True)
        arc_z = primarydirections.getArc(prom, sig, mc, self.chart.pos, zerolat=True)
        
        # Compute arc in mundo
        arc_m = primarydirections.getArc(prom, sig, mc, self.chart.pos, zerolat=False)
        
        # Check that the arcs are valid
        self.assertIsInstance(arc_z, float)
        self.assertIsInstance(arc_m, float)
        
        # Print the arcs for reference
        print(f"Arc in zodiaco: {arc_z:.5f}")
        print(f"Arc in mundo: {arc_m:.5f}")
    
    def test_primary_directions_class(self):
        """Test PrimaryDirections class"""
        # Create Primary Directions class
        pd = PrimaryDirections(self.chart)
        
        # Test the object creation methods
        mars_n = pd.N(const.MARS)
        mercury_n = pd.N(const.MERCURY)
        
        # Check that the objects are dictionaries
        self.assertIsInstance(mars_n, dict)
        self.assertIsInstance(mercury_n, dict)
        
        # Check that the objects have the required keys
        for obj in [mars_n, mercury_n]:
            self.assertIn('id', obj)
            self.assertIn('lat', obj)
            self.assertIn('lon', obj)
            self.assertIn('ra', obj)
            self.assertIn('decl', obj)
            self.assertIn('raZ', obj)
            self.assertIn('declZ', obj)
        
        # Test the getArc method
        arc = pd.getArc(mars_n, mercury_n)
        
        # Check that the arc is a dictionary
        self.assertIsInstance(arc, dict)
        
        # Check that the arc has the required keys
        self.assertIn('arcm', arc)
        self.assertIn('arcz', arc)
        
        # Print the arc for reference
        print(f"Arc in mundo: {arc['arcm']:.5f}")
        print(f"Arc in zodiaco: {arc['arcz']:.5f}")
    
    def test_primary_directions_table(self):
        """Test PDTable class"""
        # Create Primary Directions table
        pd_table = PDTable(self.chart, const.MAJOR_ASPECTS)
        
        # Test the view method
        directions = pd_table.view(0, 100)
        
        # Check that the directions is a list
        self.assertIsInstance(directions, list)
        
        # Print the directions for reference
        print(f"Directions between 0 and 100 of arc:")
        for direction in directions[:5]:  # Print only the first 5 directions
            print(f"  {direction}")
        
        # Test the byPromissor method
        mars_directions = pd_table.byPromissor(const.MARS)
        
        # Check that the mars_directions is a list
        self.assertIsInstance(mars_directions, list)
        
        # Print the Mars directions for reference
        print(f"Mars directions:")
        for direction in mars_directions[:5]:  # Print only the first 5 directions
            print(f"  {direction}")
        
        # Test the bySignificator method
        mercury_directions = pd_table.bySignificator(const.MERCURY)
        
        # Check that the mercury_directions is a list
        self.assertIsInstance(mercury_directions, list)
        
        # Print the Mercury directions for reference
        print(f"Mercury directions:")
        for direction in mercury_directions[:5]:  # Print only the first 5 directions
            print(f"  {direction}")
    
    def test_object_creation_methods(self):
        """Test object creation methods"""
        # Create Primary Directions class
        pd = PrimaryDirections(self.chart)
        
        # Test the T method (term)
        term = pd.T(const.MARS, const.ARIES)
        
        # Check that the term is a dictionary
        self.assertIsInstance(term, dict)
        
        # Check that the term has the required keys
        self.assertIn('id', term)
        self.assertIn('lat', term)
        self.assertIn('lon', term)
        
        # Print the term for reference
        print(f"Mars term in Aries: {term['lon']:.5f}")
        
        # Test the A method (antiscia)
        antiscia = pd.A(const.MARS)
        
        # Check that the antiscia is a dictionary
        self.assertIsInstance(antiscia, dict)
        
        # Check that the antiscia has the required keys
        self.assertIn('id', antiscia)
        self.assertIn('lat', antiscia)
        self.assertIn('lon', antiscia)
        
        # Print the antiscia for reference
        print(f"Mars antiscia: {antiscia['lon']:.5f}")
        
        # Test the C method (contra antiscia)
        cantiscia = pd.C(const.MARS)
        
        # Check that the cantiscia is a dictionary
        self.assertIsInstance(cantiscia, dict)
        
        # Check that the cantiscia has the required keys
        self.assertIn('id', cantiscia)
        self.assertIn('lat', cantiscia)
        self.assertIn('lon', cantiscia)
        
        # Print the cantiscia for reference
        print(f"Mars contra antiscia: {cantiscia['lon']:.5f}")
        
        # Test the D method (dexter aspect)
        dexter = pd.D(const.MARS, 90)
        
        # Check that the dexter is a dictionary
        self.assertIsInstance(dexter, dict)
        
        # Check that the dexter has the required keys
        self.assertIn('id', dexter)
        self.assertIn('lat', dexter)
        self.assertIn('lon', dexter)
        
        # Print the dexter for reference
        print(f"Mars dexter square: {dexter['lon']:.5f}")
        
        # Test the S method (sinister aspect)
        sinister = pd.S(const.MARS, 90)
        
        # Check that the sinister is a dictionary
        self.assertIsInstance(sinister, dict)
        
        # Check that the sinister has the required keys
        self.assertIn('id', sinister)
        self.assertIn('lat', sinister)
        self.assertIn('lon', sinister)
        
        # Print the sinister for reference
        print(f"Mars sinister square: {sinister['lon']:.5f}")
    
    def test_get_list(self):
        """Test getList method"""
        # Create Primary Directions class
        pd = PrimaryDirections(self.chart)
        
        # Get the list of directions
        directions = pd.getList(const.MAJOR_ASPECTS)
        
        # Check that the directions is a list
        self.assertIsInstance(directions, list)
        
        # Check that the directions are not empty
        self.assertGreater(len(directions), 0)
        
        # Print the directions for reference
        print(f"Primary Directions:")
        for direction in directions[:5]:  # Print only the first 5 directions
            print(f"  {direction}")


if __name__ == '__main__':
    unittest.main()
