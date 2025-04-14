"""
    Tests for Bhava Chalita chart calculations
"""

import unittest
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic import const
from astrovedic.vedic.bhava_chalita import (
    get_bhava_chalita_chart, get_bhava_chalita_house_for_planet,
    get_bhava_chalita_planets_in_house, get_bhava_chalita_house_lord,
    get_bhava_chalita_house_strength
)

class TestBhavaChalita(unittest.TestCase):
    """Test Bhava Chalita chart calculations"""

    def setUp(self):
        """Set up test data"""
        self.date = Datetime('2000/1/1', '12:00', '+00:00')
        self.pos = GeoPos('51n30', '0w10')
        self.chart = Chart(self.date, self.pos)

    def test_bhava_chalita_chart(self):
        """Test Bhava Chalita chart calculation"""
        # Get the Bhava Chalita chart
        bhava_chalita = get_bhava_chalita_chart(self.chart)

        # Check that the result has the expected structure
        self.assertIn('houses', bhava_chalita)
        self.assertIn('planets_in_houses', bhava_chalita)

        # Check that there are 12 houses
        self.assertEqual(len(bhava_chalita['houses']), 12)

        # Check that each house has the expected structure
        for house_num in range(1, 13):
            house = bhava_chalita['houses'][house_num]
            self.assertIn('cusp', house)
            self.assertIn('sign', house)
            self.assertIn('sign_longitude', house)

            # Check that the sign is a valid sign
            self.assertIn(house['sign'], const.LIST_SIGNS)

            # Check that the sign longitude is in the valid range (0-30)
            self.assertGreaterEqual(house['sign_longitude'], 0)
            self.assertLess(house['sign_longitude'], 30)

        # Check that the planets_in_houses dictionary has 12 entries
        self.assertEqual(len(bhava_chalita['planets_in_houses']), 12)

        # Check that each planet is in exactly one house
        planets_found = []
        for house_num, planets in bhava_chalita['planets_in_houses'].items():
            for planet_info in planets:
                planets_found.append(planet_info['id'])

        # Check that all traditional planets are accounted for
        for planet_id in const.LIST_SEVEN_PLANETS + [const.RAHU, const.KETU]:
            self.assertIn(planet_id, planets_found)

        # Check that no planet is in more than one house
        self.assertEqual(len(planets_found), len(set(planets_found)))

    def test_bhava_chalita_house_for_planet(self):
        """Test getting the Bhava Chalita house for a planet"""
        # Test for each planet (traditional planets only)
        for planet_id in const.LIST_SEVEN_PLANETS + [const.RAHU, const.KETU]:
            # Get the house
            house_num = get_bhava_chalita_house_for_planet(self.chart, planet_id)

            # Check that the house number is in the valid range (1-12)
            self.assertGreaterEqual(house_num, 1)
            self.assertLessEqual(house_num, 12)

            # Check that the planet is actually in that house
            planets = get_bhava_chalita_planets_in_house(self.chart, house_num)
            planet_ids = [planet_info['id'] for planet_info in planets]
            self.assertIn(planet_id, planet_ids)

    def test_bhava_chalita_planets_in_house(self):
        """Test getting planets in a Bhava Chalita house"""
        # Test for each house
        for house_num in range(1, 13):
            # Get the planets
            planets = get_bhava_chalita_planets_in_house(self.chart, house_num)

            # Check that the result is a list
            self.assertIsInstance(planets, list)

            # Check that each planet has the expected structure
            for planet_info in planets:
                self.assertIn('id', planet_info)
                self.assertIn('longitude', planet_info)
                self.assertIn('sign', planet_info)
                self.assertIn('sign_longitude', planet_info)

                # Check that the planet ID is a valid planet
                self.assertIn(planet_info['id'], const.LIST_OBJECTS_VEDIC)

                # Check that the sign is a valid sign
                self.assertIn(planet_info['sign'], const.LIST_SIGNS)

                # Check that the sign longitude is in the valid range (0-30)
                self.assertGreaterEqual(planet_info['sign_longitude'], 0)
                self.assertLess(planet_info['sign_longitude'], 30)

    def test_bhava_chalita_house_lord(self):
        """Test getting the lord of a Bhava Chalita house"""
        # Test for each house
        for house_num in range(1, 13):
            # Get the house lord
            lord = get_bhava_chalita_house_lord(self.chart, house_num)

            # Check that the lord is a valid planet
            self.assertIn(lord, [const.SUN, const.MOON, const.MERCURY, const.VENUS,
                                const.MARS, const.JUPITER, const.SATURN])

    def test_bhava_chalita_house_strength(self):
        """Test calculating the strength of a Bhava Chalita house"""
        # Test for each house
        for house_num in range(1, 13):
            # Get the house strength
            strength_info = get_bhava_chalita_house_strength(self.chart, house_num)

            # Check that the result has the expected structure
            self.assertIn('strength', strength_info)
            self.assertIn('description', strength_info)
            self.assertIn('lord', strength_info)
            self.assertIn('lord_house', strength_info)
            self.assertIn('planets', strength_info)

            # Check that the strength is in the valid range (0-100)
            self.assertGreaterEqual(strength_info['strength'], 0)
            self.assertLessEqual(strength_info['strength'], 100)

            # Check that the lord is a valid planet
            self.assertIn(strength_info['lord'], [const.SUN, const.MOON, const.MERCURY, const.VENUS,
                                                const.MARS, const.JUPITER, const.SATURN])

            # Check that the lord house is in the valid range (1-12)
            self.assertGreaterEqual(strength_info['lord_house'], 1)
            self.assertLessEqual(strength_info['lord_house'], 12)

    def test_bhava_chalita_logic(self):
        """Test the logic of Bhava Chalita chart calculation"""
        # Get the Bhava Chalita chart
        bhava_chalita = get_bhava_chalita_chart(self.chart)

        # Get the Ascendant degree (House1 longitude)
        asc_lon = self.chart.getHouse('House1').lon

        # Check that the first house cusp is at the Ascendant degree
        self.assertEqual(bhava_chalita['houses'][1]['cusp'], asc_lon)

        # Check that each house cusp is 30 degrees apart
        for i in range(1, 12):
            current_cusp = bhava_chalita['houses'][i]['cusp']
            next_cusp = bhava_chalita['houses'][i + 1]['cusp']

            # Calculate the expected next cusp
            expected_next_cusp = (current_cusp + 30) % 360

            # Allow for a small floating-point error
            self.assertAlmostEqual(next_cusp, expected_next_cusp, places=10)

if __name__ == '__main__':
    unittest.main()
