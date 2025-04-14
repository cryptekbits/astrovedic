import unittest

from astrovedic import const
from astrovedic.factory import AstronomicalObjectFactory
from astrovedic.object import GenericObject, Object, MoonNode, Asteroid, House, FixedStar


class FactoryTests(unittest.TestCase):

    def test_create_object_with_complete_data(self):
        """Test creating an object with complete data"""
        obj_data = {
            'id': const.SUN,
            'lon': 45.0,
            'lat': 0.0,
            'lonspeed': 1.0,
            'latspeed': 0.0
        }
        obj = AstronomicalObjectFactory.create_object(obj_data, const.OBJ_PLANET)

        self.assertEqual(obj.id, const.SUN)
        self.assertEqual(obj.lon, 45.0)
        self.assertEqual(obj.lat, 0.0)
        self.assertEqual(obj.lonspeed, 1.0)
        self.assertEqual(obj.latspeed, 0.0)
        self.assertEqual(obj.sign, const.TAURUS)  # Should be calculated
        self.assertEqual(obj.signlon, 15.0)  # Should be calculated

    def test_create_object_with_missing_data(self):
        """
        Test creating an object with missing data

        Note: This test intentionally creates an object with missing required attributes
        (lat, lonspeed, latspeed). The test will generate ERROR and WARNING log messages
        like:
        - ERROR - Missing required attributes for Sun: lat, lonspeed, latspeed
        - WARNING - Created object with default values for missing attributes: Sun

        These messages are expected and indicate that the factory is correctly identifying
        missing attributes and applying default values as designed.
        """
        obj_data = {
            'id': const.SUN,
            'lon': 45.0
            # Missing 'lat', 'lonspeed', 'latspeed'
        }
        obj = AstronomicalObjectFactory.create_object(obj_data, const.OBJ_PLANET)

        self.assertEqual(obj.id, const.SUN)
        self.assertEqual(obj.lon, 45.0)
        self.assertEqual(obj.lat, 0.0)  # Default value
        self.assertEqual(obj.lonspeed, 0.0)  # Default value
        self.assertEqual(obj.latspeed, 0.0)  # Default value
        self.assertEqual(obj.sign, const.TAURUS)  # Should be calculated
        self.assertEqual(obj.signlon, 15.0)  # Should be calculated

    def test_create_house(self):
        """Test creating a house object"""
        house_data = {
            'id': const.HOUSE1,
            'lon': 30.0,
            'lat': 0.0,
            'size': 30.0
        }
        house = AstronomicalObjectFactory.create_object(house_data, const.OBJ_HOUSE)

        self.assertEqual(house.id, const.HOUSE1)
        self.assertEqual(house.lon, 30.0)
        self.assertEqual(house.lat, 0.0)
        self.assertEqual(house.size, 30.0)
        self.assertEqual(house.sign, const.TAURUS)  # Should be calculated
        self.assertEqual(house.signlon, 0.0)  # Should be calculated

    def test_create_fixed_star(self):
        """Test creating a fixed star object"""
        star_data = {
            'id': const.STAR_ALDEBARAN,
            'lon': 60.0,
            'lat': 5.0,
            'mag': 1.0
        }
        star = AstronomicalObjectFactory.create_object(star_data, const.OBJ_FIXED_STAR)

        self.assertEqual(star.id, const.STAR_ALDEBARAN)
        self.assertEqual(star.lon, 60.0)
        self.assertEqual(star.lat, 5.0)
        self.assertEqual(star.mag, 1.0)
        self.assertEqual(star.sign, const.GEMINI)  # Should be calculated
        self.assertEqual(star.signlon, 0.0)  # Should be calculated

    def test_create_object_with_empty_data(self):
        """
        Test creating an object with empty data

        Note: This test intentionally creates an object with completely empty data.
        The test will generate ERROR and WARNING log messages like:
        - ERROR - Missing required attributes for None: id, lon, lat
        - WARNING - Created object with default values for missing attributes: None

        These messages are expected and indicate that the factory is correctly handling
        the case of empty data by applying default values for all required attributes.
        """
        obj_data = {}
        obj = AstronomicalObjectFactory.create_object(obj_data)

        self.assertEqual(obj.id, const.NO_PLANET)  # Default value
        self.assertEqual(obj.lon, 0.0)  # Default value
        self.assertEqual(obj.lat, 0.0)  # Default value
        self.assertEqual(obj.sign, const.ARIES)  # Default value
        self.assertEqual(obj.signlon, 0.0)  # Default value

    def test_get_object_class(self):
        """Test getting the correct object class"""
        self.assertEqual(AstronomicalObjectFactory.get_object_class(const.OBJ_PLANET, const.SUN), Object)
        self.assertEqual(AstronomicalObjectFactory.get_object_class(const.OBJ_ASTEROID, const.CHIRON), Asteroid)
        self.assertEqual(AstronomicalObjectFactory.get_object_class(const.OBJ_MOON_NODE, const.NORTH_NODE), MoonNode)
        self.assertEqual(AstronomicalObjectFactory.get_object_class(const.OBJ_HOUSE, const.HOUSE1), House)
        self.assertEqual(AstronomicalObjectFactory.get_object_class(const.OBJ_FIXED_STAR, const.STAR_ALDEBARAN), FixedStar)
        self.assertEqual(AstronomicalObjectFactory.get_object_class(const.OBJ_GENERIC, const.NO_PLANET), GenericObject)


if __name__ == '__main__':
    unittest.main()
