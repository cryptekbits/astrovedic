"""
    This file is part of astrovedic - (C) FlatAngle
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
        logging.FileHandler("astrovedic.log"),
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

    @staticmethod
    def create_vedic_object(data, obj_type=None):
        """Create and validate a Vedic astronomical object with Vedic-specific attributes

        Args:
            data (dict): Dictionary with object properties
            obj_type (str, optional): Object type. If None, determined from data

        Returns:
            VedicBody: An instance of the VedicBody class with Vedic attributes

        Raises:
            ValueError: If required attributes are missing
        """
        # First create a regular object
        obj = AstronomicalObjectFactory.create_object(data, obj_type)

        # Create a VedicBody object
        vedic_obj = VedicBody()

        # Copy all attributes from the regular object
        for attr, value in obj.__dict__.items():
            setattr(vedic_obj, attr, value)

        # Add Vedic-specific attributes if provided
        if 'nakshatra' in data:
            vedic_obj.nakshatra = data['nakshatra']
        if 'nakshatra_lord' in data:
            vedic_obj.nakshatra_lord = data['nakshatra_lord']
        if 'nakshatra_pada' in data:
            vedic_obj.nakshatra_pada = data['nakshatra_pada']
        if 'nakshatra_degree' in data:
            vedic_obj.nakshatra_degree = data['nakshatra_degree']

        # Add Shadbala components if provided
        if 'sthana_bala' in data:
            vedic_obj.sthana_bala = data['sthana_bala']
        if 'dig_bala' in data:
            vedic_obj.dig_bala = data['dig_bala']
        if 'kala_bala' in data:
            vedic_obj.kala_bala = data['kala_bala']
        if 'cheshta_bala' in data:
            vedic_obj.cheshta_bala = data['cheshta_bala']
        if 'naisargika_bala' in data:
            vedic_obj.naisargika_bala = data['naisargika_bala']
        if 'drig_bala' in data:
            vedic_obj.drig_bala = data['drig_bala']
        if 'total_shadbala' in data:
            vedic_obj.total_shadbala = data['total_shadbala']

        # Add Varga positions if provided
        if 'varga_positions' in data:
            vedic_obj.varga_positions = data['varga_positions']

        # Add other Vedic attributes if provided
        if 'avastha' in data:
            vedic_obj.avastha = data['avastha']
        if 'graha_drishti' in data:
            vedic_obj.graha_drishti = data['graha_drishti']
        if 'aspects_received' in data:
            vedic_obj.aspects_received = data['aspects_received']
        if 'ishta_phala' in data:
            vedic_obj.ishta_phala = data['ishta_phala']
        if 'kashta_phala' in data:
            vedic_obj.kashta_phala = data['kashta_phala']
        if 'vimsopaka_bala' in data:
            vedic_obj.vimsopaka_bala = data['vimsopaka_bala']

        return vedic_obj
