"""
    This module implements the HouseSystemManager class for managing house system selection
    and configuration in Vedic astrology calculations.
"""

from astrovedic import const

class HouseSystemManager:
    """Manages house system selection and configuration."""
    
    # Dictionary of supported house systems with metadata
    SUPPORTED_HOUSE_SYSTEMS = {
        const.HOUSES_WHOLE_SIGN: {
            'name': 'Whole Sign',
            'description': 'Traditional Vedic house system',
            'category': 'vedic',
            'recommended_ayanamsas': [const.AY_LAHIRI, const.AY_RAMAN]
        },
        const.HOUSES_EQUAL: {
            'name': 'Equal',
            'description': 'Equal house system',
            'category': 'vedic',
            'recommended_ayanamsas': [const.AY_LAHIRI, const.AY_RAMAN]
        },
        const.HOUSES_PLACIDUS: {
            'name': 'Placidus',
            'description': 'Preferred house system for KP astrology',
            'category': 'kp',
            'recommended_ayanamsas': [const.AY_KRISHNAMURTI]
        },
        const.HOUSES_KOCH: {
            'name': 'Koch',
            'description': 'Koch house system',
            'category': 'alternative',
            'recommended_ayanamsas': []
        },
        const.HOUSES_PORPHYRIUS: {
            'name': 'Porphyrius',
            'description': 'Porphyrius house system',
            'category': 'alternative',
            'recommended_ayanamsas': []
        },
        const.HOUSES_REGIOMONTANUS: {
            'name': 'Regiomontanus',
            'description': 'Regiomontanus house system',
            'category': 'alternative',
            'recommended_ayanamsas': []
        },
        const.HOUSES_CAMPANUS: {
            'name': 'Campanus',
            'description': 'Campanus house system',
            'category': 'alternative',
            'recommended_ayanamsas': []
        },
        const.HOUSES_MERIDIAN: {
            'name': 'Meridian',
            'description': 'Meridian house system',
            'category': 'alternative',
            'recommended_ayanamsas': []
        },
        const.HOUSES_MORINUS: {
            'name': 'Morinus',
            'description': 'Morinus house system',
            'category': 'alternative',
            'recommended_ayanamsas': []
        }
    }
    
    # Default house system
    _default_house_system = const.HOUSES_WHOLE_SIGN
    
    # Default KP house system
    _default_kp_house_system = const.HOUSES_PLACIDUS
    
    @classmethod
    def get_default(cls):
        """Get the default house system."""
        return cls._default_house_system
    
    @classmethod
    def set_default(cls, house_system):
        """Set the default house system."""
        if house_system not in cls.SUPPORTED_HOUSE_SYSTEMS:
            raise ValueError(f"Unsupported house system: {house_system}")
        cls._default_house_system = house_system
    
    @classmethod
    def get_kp_default(cls):
        """Get the default KP house system."""
        return cls._default_kp_house_system
    
    @classmethod
    def set_kp_default(cls, house_system):
        """Set the default KP house system."""
        if house_system not in cls.SUPPORTED_HOUSE_SYSTEMS:
            raise ValueError(f"Unsupported house system: {house_system}")
        cls._default_kp_house_system = house_system
    
    @classmethod
    def get_recommended_ayanamsas(cls, house_system):
        """Get recommended ayanamsas for a house system."""
        if house_system not in cls.SUPPORTED_HOUSE_SYSTEMS:
            raise ValueError(f"Unsupported house system: {house_system}")
        return cls.SUPPORTED_HOUSE_SYSTEMS[house_system]['recommended_ayanamsas']
    
    @classmethod
    def get_all_house_systems(cls):
        """Get all supported house systems."""
        return list(cls.SUPPORTED_HOUSE_SYSTEMS.keys())
    
    @classmethod
    def get_house_systems_by_category(cls, category):
        """Get house systems by category."""
        return [
            house_system for house_system, data in cls.SUPPORTED_HOUSE_SYSTEMS.items()
            if data['category'] == category
        ]
    
    @classmethod
    def get_house_system_info(cls, house_system):
        """Get information about a house system."""
        if house_system not in cls.SUPPORTED_HOUSE_SYSTEMS:
            raise ValueError(f"Unsupported house system: {house_system}")
        return cls.SUPPORTED_HOUSE_SYSTEMS[house_system]
    
    @classmethod
    def is_supported(cls, house_system):
        """Check if a house system is supported."""
        return house_system in cls.SUPPORTED_HOUSE_SYSTEMS
