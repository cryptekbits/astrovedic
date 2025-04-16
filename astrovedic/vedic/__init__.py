"""
    This file is part of astrovedic - (C) FlatAngle
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

from astrovedic import const
from astrovedic.vedic.ayanamsa import AyanamsaManager
from astrovedic.vedic.houses import HouseSystemManager
from astrovedic.vedic.config import ChartConfiguration

# Define the public API
__all__ = [
    # Managers
    'AyanamsaManager', 'HouseSystemManager', 'ChartConfiguration',

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
from astrovedic.vedic.api import (
    VedicChart, create_vedic_chart, create_kp_chart
)

# Import exceptions
from astrovedic.vedic.exceptions import (
    VedicError, InputError, CalculationError, ValidationError,
    ConfigurationError, DataError, NotSupportedError
)

# Import utility functions
from astrovedic.vedic.utils import (
    normalize_longitude, get_sign_from_longitude, get_sign_lord,
    get_sign_number, get_sign_from_number, get_planet_sign,
    get_planet_house, get_house_sign, get_house_lord,
    get_aspect, is_retrograde, get_planet_degree,
    get_planet_nakshatra, get_planet_navamsa, get_date_range,
    get_element, get_quality, get_gender, get_planet_nature,
    get_planet_element, get_planet_friendship, get_planet_abbreviation
)
