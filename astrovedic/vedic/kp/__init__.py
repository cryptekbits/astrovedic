"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This package implements KP (Krishnamurti Paddhati) astrology calculations.
"""

# Import the chart wrapper
from astrovedic.vedic.kp.chart import create_kp_chart, KPChart

# Re-export functions from the main KP module
from astrovedic.vedic.nakshatras import get_nakshatra

# Import functions from the main KP module
import sys
import importlib.util

# Load the kp.py module directly
spec = importlib.util.spec_from_file_location("kp_module", "astrovedic/vedic/kp.py")
kp = importlib.util.module_from_spec(spec)
sys.modules["kp_module"] = kp
spec.loader.exec_module(kp)

# Re-export functions from the kp module
get_kp_sublord = kp.get_kp_sublord
get_kp_sub_sublord = kp.get_kp_sub_sublord
get_kp_pointer = kp.get_kp_pointer
get_kp_lords = kp.get_kp_lords
get_kp_planets = kp.get_kp_planets
get_kp_houses = kp.get_kp_houses
get_kp_significators = kp.get_kp_significators
get_kp_ruling_planets = kp.get_kp_ruling_planets
