"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This subpackage implements Vedic astrology features including:
    - Nakshatra calculations
    - KP (Krishnamurti Paddhati) astrology
    - Panchang elements (tithi, yoga, karana, etc.)
    - Shadow planets (upagrah) calculations
    - Additional Vedic bodies
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
