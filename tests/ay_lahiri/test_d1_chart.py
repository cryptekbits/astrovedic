"""
    Tests for D1 chart calculations with Lahiri ayanamsa
"""

import unittest
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic import const
from astrovedic.vedic.api import VedicChart

from tests.ay_lahiri.reference_data import (
    REFERENCE_DATE, REFERENCE_TIME, REFERENCE_TIMEZONE,
    REFERENCE_LAT, REFERENCE_LON, D1_CHART_REFERENCE
)


class TestLahiriD1Chart(unittest.TestCase):
    """Test D1 chart calculations with Lahiri ayanamsa"""

    def get_sign_from_longitude(self, longitude):
        """Get the sign from a longitude"""
        # Normalize the longitude
        lon = longitude % 360

        # Calculate the sign index (0-11)
        sign_index = int(lon / 30)

        # Return the sign
        return const.LIST_SIGNS[sign_index]

    def setUp(self):
        """Set up test case"""
        # Create date and location for testing
        self.date = Datetime(REFERENCE_DATE, REFERENCE_TIME, REFERENCE_TIMEZONE)
        self.pos = GeoPos(REFERENCE_LAT, REFERENCE_LON)

        # Create chart with Lahiri ayanamsa and Whole Sign houses
        self.chart = Chart(self.date, self.pos, hsys=const.HOUSES_WHOLE_SIGN, ayanamsa=const.AY_LAHIRI)

        # Create Vedic chart
        self.vedic_chart = VedicChart(self.chart)

    def test_planet_positions(self):
        """Test planet positions in D1 chart with Lahiri ayanamsa"""
        # Get planets from reference data
        reference_planets = D1_CHART_REFERENCE["planets"]

        # Test Ascendant position
        asc = self.chart.getAngle(const.ASC)
        ref_asc = next(p for p in reference_planets if p["planet"] == "Ascendant")

        # Test Ascendant longitude
        self.assertAlmostEqual(asc.lon, ref_asc["longitude"], delta=0.2,
                              msg=f"Ascendant longitude does not match reference data. Expected: {ref_asc['longitude']}, Got: {asc.lon}")

        # Test Ascendant sign
        asc_sign = asc.sign
        expected_sign = self.get_sign_from_longitude(ref_asc["longitude"])
        self.assertEqual(asc_sign, expected_sign,
                        msg=f"Ascendant sign does not match reference data. Expected: {expected_sign}, Got: {asc_sign}")

        # Test planets
        planets = [const.SUN, const.MOON, const.MARS, const.MERCURY,
                  const.JUPITER, const.VENUS, const.SATURN, const.RAHU, const.KETU]

        for planet_id in planets:
            planet = self.chart.getObject(planet_id)
            planet_name = planet.id.capitalize()
            ref_planet = next(p for p in reference_planets if p["planet"] == planet_name)

            # Test planet longitude
            self.assertAlmostEqual(planet.lon, ref_planet["longitude"], delta=0.2,
                                  msg=f"{planet_name} longitude does not match reference data. Expected: {ref_planet['longitude']}, Got: {planet.lon}")

            # Test planet sign
            planet_sign = planet.sign
            expected_sign = self.get_sign_from_longitude(ref_planet["longitude"])
            self.assertEqual(planet_sign, expected_sign,
                            msg=f"{planet_name} sign does not match reference data. Expected: {expected_sign}, Got: {planet_sign}")

            # Test retrograde status for Venus, Rahu, and Ketu
            if planet_id in [const.VENUS, const.RAHU, const.KETU]:
                # These planets should be retrograde according to Lahiri.md
                if hasattr(planet, 'isRetrograde'):
                    is_retrograde = planet.isRetrograde()
                    self.assertTrue(is_retrograde,
                                  msg=f"{planet_name} should be retrograde according to reference data, but it's not.")
                else:
                    # For nodes that don't have isRetrograde method, check if speed is negative
                    if hasattr(planet, 'lonspeed'):
                        is_retrograde = planet.lonspeed < 0
                        self.assertTrue(is_retrograde,
                                      msg=f"{planet_name} should have negative speed (retrograde) according to reference data, but it doesn't.")
            elif planet_id not in [const.RAHU, const.KETU]:
                # Other planets (except Rahu and Ketu) should not be retrograde
                if hasattr(planet, 'isRetrograde'):
                    is_retrograde = planet.isRetrograde()
                    self.assertFalse(is_retrograde,
                                   msg=f"{planet_name} should not be retrograde according to reference data, but it is.")
                else:
                    # For nodes that don't have isRetrograde method, check if speed is positive
                    if hasattr(planet, 'lonspeed'):
                        is_retrograde = planet.lonspeed < 0
                        self.assertFalse(is_retrograde,
                                       msg=f"{planet_name} should have positive speed (direct) according to reference data, but it doesn't.")

    def test_house_details(self):
        """Test house details in D1 chart with Lahiri ayanamsa"""
        # Get houses from reference data
        reference_houses = D1_CHART_REFERENCE["houses"]

        # Test house details
        for i in range(12):
            house_num = i + 1
            house_id = f"House{house_num}"
            ref_house = next(h for h in reference_houses if h["house"] == house_num)

            # Get house sign
            house = self.chart.getHouse(house_id)
            house_sign = house.sign
            self.assertEqual(house_sign, ref_house["sign"],
                            msg=f"House {house_num} sign does not match reference data. Expected: {ref_house['sign']}, Got: {house_sign}")

            # Get house lord
            from astrovedic.vedic import dignities as vedic_dignities
            house_lord = vedic_dignities.get_ruler(house_sign)
            self.assertEqual(house_lord.lower(), ref_house["owner"].lower(),
                            msg=f"House {house_num} lord does not match reference data. Expected: {ref_house['owner']}, Got: {house_lord}")


if __name__ == '__main__':
    unittest.main()
