"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology

    This subpackage implements Vedic astrology features including:
    - Nakshatra calculations
    - KP (Krishnamurti Paddhati) astrology
    - Panchang elements (tithi, yoga, karana, etc.)
    - Shadow planets (upagrah) calculations
    - Vimshottari Dasha calculations
    - Divisional charts (Vargas)
    - Planetary strength calculations (Shadbala)
    - Ashtakavarga system
    - Yogas (planetary combinations)
    - Muhurta (electional astrology)
    - Sarvatobhadra Chakra
    - Transit analysis (Gochara)
    - Compatibility analysis (Kuta matching)
"""

from flatlib import const

# Default ayanamsa for Vedic calculations
DEFAULT_AYANAMSA = const.AY_DEFAULT_VEDIC

# Default ayanamsa for KP calculations
DEFAULT_KP_AYANAMSA = const.AY_DEFAULT_KP

# Default house system for Vedic calculations
DEFAULT_HOUSE_SYSTEM = const.HOUSES_WHOLE_SIGN

# Default house system for KP calculations
DEFAULT_KP_HOUSE_SYSTEM = const.HOUSES_PLACIDUS

# Define the public API
__all__ = [
    # Constants
    'DEFAULT_AYANAMSA', 'DEFAULT_KP_AYANAMSA',
    'DEFAULT_HOUSE_SYSTEM', 'DEFAULT_KP_HOUSE_SYSTEM',

    # Unified API
    'VedicChart', 'create_vedic_chart', 'create_kp_chart',

    # Exceptions
    'VedicError', 'InputError', 'CalculationError', 'ValidationError',
    'ConfigurationError', 'DataError', 'NotSupportedError',

    # Utility functions
    'normalize_longitude', 'get_sign_from_longitude', 'get_sign_lord',
    'get_sign_number', 'get_sign_from_number', 'get_planet_sign',
    'get_planet_house', 'get_house_sign', 'get_house_lord',
    'get_aspect', 'is_retrograde', 'get_planet_degree',
    'get_planet_nakshatra', 'get_planet_navamsa', 'get_date_range',
    'get_element', 'get_quality', 'get_gender', 'get_planet_nature',
    'get_planet_element', 'get_planet_friendship', 'get_planet_abbreviation'
]

# Import the unified API
from flatlib.vedic.api import (
    VedicChart, create_vedic_chart, create_kp_chart
)

# Import exceptions
from flatlib.vedic.exceptions import (
    VedicError, InputError, CalculationError, ValidationError,
    ConfigurationError, DataError, NotSupportedError
)

# Import utility functions
from flatlib.vedic.utils import (
    normalize_longitude, get_sign_from_longitude, get_sign_lord,
    get_sign_number, get_sign_from_number, get_planet_sign,
    get_planet_house, get_house_sign, get_house_lord,
    get_aspect, is_retrograde, get_planet_degree,
    get_planet_nakshatra, get_planet_navamsa, get_date_range,
    get_element, get_quality, get_gender, get_planet_nature,
    get_planet_element, get_planet_friendship, get_planet_abbreviation
)
