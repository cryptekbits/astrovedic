"""
    This module implements the AyanamsaManager class for managing ayanamsa selection
    and configuration in Vedic astrology calculations.
"""

from astrovedic import const

class AyanamsaManager:
    """Manages ayanamsa selection and configuration."""
    
    # Dictionary of supported ayanamsas with metadata
    SUPPORTED_AYANAMSAS = {
        const.AY_LAHIRI: {
            'name': 'Lahiri',
            'description': 'Official ayanamsa of the Indian government',
            'category': 'primary',
            'recommended_house_systems': [const.HOUSES_WHOLE_SIGN]
        },
        const.AY_RAMAN: {
            'name': 'Raman',
            'description': 'B.V. Raman\'s ayanamsa, a variant of Lahiri',
            'category': 'primary',
            'recommended_house_systems': [const.HOUSES_WHOLE_SIGN]
        },
        const.AY_KRISHNAMURTI: {
            'name': 'Krishnamurti',
            'description': 'K.S. Krishnamurti\'s ayanamsa for KP system',
            'category': 'kp',
            'recommended_house_systems': [const.HOUSES_PLACIDUS]
        },
        const.AY_YUKTESHWAR: {
            'name': 'Yukteshwar',
            'description': 'Based on Sri Yukteshwar\'s book "The Holy Science"',
            'category': 'secondary',
            'recommended_house_systems': [const.HOUSES_WHOLE_SIGN]
        },
        const.AY_JN_BHASIN: {
            'name': 'JN Bhasin',
            'description': 'J.N. Bhasin\'s ayanamsa',
            'category': 'secondary',
            'recommended_house_systems': [const.HOUSES_WHOLE_SIGN]
        },
        const.AY_SURYASIDDHANTA: {
            'name': 'Surya Siddhanta',
            'description': 'Based on the ancient Surya Siddhanta text',
            'category': 'traditional',
            'recommended_house_systems': [const.HOUSES_WHOLE_SIGN]
        },
        const.AY_ARYABHATA: {
            'name': 'Aryabhata',
            'description': 'Based on Aryabhata\'s work',
            'category': 'traditional',
            'recommended_house_systems': [const.HOUSES_WHOLE_SIGN]
        },
        const.AY_TRUE_CITRA: {
            'name': 'True Citra',
            'description': 'True Citra ayanamsa with Spica at 0° Libra',
            'category': 'traditional',
            'recommended_house_systems': [const.HOUSES_WHOLE_SIGN]
        },
        const.AY_TRUE_REVATI: {
            'name': 'True Revati',
            'description': 'True Revati ayanamsa with Revati at 0° Aries',
            'category': 'traditional',
            'recommended_house_systems': [const.HOUSES_WHOLE_SIGN]
        }
    }
    
    # Default ayanamsa
    _default_ayanamsa = const.AY_LAHIRI
    
    # Default KP ayanamsa
    _default_kp_ayanamsa = const.AY_KRISHNAMURTI
    
    @classmethod
    def get_default(cls):
        """Get the default ayanamsa."""
        return cls._default_ayanamsa
    
    @classmethod
    def set_default(cls, ayanamsa):
        """Set the default ayanamsa."""
        if ayanamsa not in cls.SUPPORTED_AYANAMSAS:
            raise ValueError(f"Unsupported ayanamsa: {ayanamsa}")
        cls._default_ayanamsa = ayanamsa
    
    @classmethod
    def get_kp_default(cls):
        """Get the default KP ayanamsa."""
        return cls._default_kp_ayanamsa
    
    @classmethod
    def set_kp_default(cls, ayanamsa):
        """Set the default KP ayanamsa."""
        if ayanamsa not in cls.SUPPORTED_AYANAMSAS:
            raise ValueError(f"Unsupported ayanamsa: {ayanamsa}")
        cls._default_kp_ayanamsa = ayanamsa
    
    @classmethod
    def get_recommended_house_systems(cls, ayanamsa):
        """Get recommended house systems for an ayanamsa."""
        if ayanamsa not in cls.SUPPORTED_AYANAMSAS:
            raise ValueError(f"Unsupported ayanamsa: {ayanamsa}")
        return cls.SUPPORTED_AYANAMSAS[ayanamsa]['recommended_house_systems']
    
    @classmethod
    def get_all_ayanamsas(cls):
        """Get all supported ayanamsas."""
        return list(cls.SUPPORTED_AYANAMSAS.keys())
    
    @classmethod
    def get_ayanamsas_by_category(cls, category):
        """Get ayanamsas by category."""
        return [
            ayanamsa for ayanamsa, data in cls.SUPPORTED_AYANAMSAS.items()
            if data['category'] == category
        ]
    
    @classmethod
    def get_ayanamsa_info(cls, ayanamsa):
        """Get information about an ayanamsa."""
        if ayanamsa not in cls.SUPPORTED_AYANAMSAS:
            raise ValueError(f"Unsupported ayanamsa: {ayanamsa}")
        return cls.SUPPORTED_AYANAMSAS[ayanamsa]
    
    @classmethod
    def is_supported(cls, ayanamsa):
        """Check if an ayanamsa is supported."""
        return ayanamsa in cls.SUPPORTED_AYANAMSAS
