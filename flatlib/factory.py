"""
    This file is part of flatlib - (C) FlatAngle
    Author: João Ventura (flatangleweb@gmail.com)


    This module implements a factory pattern for creating
    astronomical objects with proper validation.

"""

import logging
from . import const
from .object import GenericObject, Object, MoonNode, Asteroid, House, FixedStar, ShadowPlanet, VedicBody

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("flatlib.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("flatlib")


class AstronomicalObjectFactory:
    """Factory for creating astronomical objects with validation"""

    @staticmethod
    def get_object_class(obj_type, obj_id):
        """Returns the appropriate class for the object type and ID"""
        if obj_type == const.OBJ_PLANET:
            return Object
        elif obj_type == const.OBJ_ASTEROID:
            return Asteroid
        elif obj_type == const.OBJ_MOON_NODE:
            return MoonNode
        elif obj_type == const.OBJ_SHADOW_PLANET:
            return ShadowPlanet
        elif obj_type == const.OBJ_HOUSE:
            return House
        elif obj_type == const.OBJ_FIXED_STAR:
            return FixedStar
        else:
            # Fallback based on object ID
            if obj_id in const.LIST_TEN_PLANETS:
                return Object
            elif obj_id in const.LIST_ASTEROIDS:
                return Asteroid
            elif obj_id in const.LIST_MOON_NODES:
                return MoonNode
            elif obj_id in const.LIST_SHADOW_PLANETS:
                return ShadowPlanet
            elif obj_id in const.LIST_VEDIC_BODIES:
                return VedicBody
            else:
                return GenericObject

    @staticmethod
    def create_object(data, obj_type=None):
        """Create and validate an astronomical object

        Args:
            data (dict): Dictionary with object properties
            obj_type (str, optional): Object type. If None, determined from data

        Returns:
            Object: An instance of the appropriate object class

        Raises:
            ValueError: If required attributes are missing
        """
        # Determine object type if not provided
        if obj_type is None:
            if 'type' in data:
                obj_type = data['type']
            else:
                obj_type = const.OBJ_GENERIC

        # Get object ID
        obj_id = data.get('id', const.NO_PLANET)

        # Get appropriate class
        cls = AstronomicalObjectFactory.get_object_class(obj_type, obj_id)

        # Validate required attributes based on object type
        required_attrs = ['id', 'lon', 'lat']

        # Add type-specific required attributes
        if obj_type in [const.OBJ_PLANET, const.OBJ_ASTEROID]:
            required_attrs.extend(['lonspeed', 'latspeed'])
        elif obj_type == const.OBJ_HOUSE:
            required_attrs.append('size')
        elif obj_type == const.OBJ_FIXED_STAR:
            required_attrs.append('mag')

        # Check for missing attributes
        missing_attrs = [attr for attr in required_attrs if attr not in data]

        if missing_attrs:
            error_msg = f"Missing required attributes for {obj_id}: {', '.join(missing_attrs)}"
            logger.error(error_msg)

            # Add default values for missing attributes
            for attr in missing_attrs:
                if attr == 'id':
                    data['id'] = obj_id
                elif attr in ['lon', 'lat', 'lonspeed', 'latspeed', 'size', 'mag']:
                    data[attr] = 0.0
                elif attr == 'sign':
                    data['sign'] = const.ARIES
                elif attr == 'signlon':
                    data['signlon'] = 0.0

            logger.warning(f"Created object with default values for missing attributes: {obj_id}")

        # Create the object
        obj = cls.fromDict(data)

        # Ensure sign and signlon are set
        if 'sign' not in data or 'signlon' not in data:
            obj.relocate(obj.lon)

        return obj
