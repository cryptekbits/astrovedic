"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements basic analysis tools for transit calculations
    in Vedic astrology. For detailed analysis and reporting,
    use the astroved_extension package.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos

# Import core functions
from astrovedic.vedic.transits.core import (
    get_transit_chart, get_transit_planets,
    get_transit_aspects, get_transit_houses,
    get_transit_quality
)

# Import Gochara functions
from astrovedic.vedic.transits.gochara import (
    get_gochara_effects, get_planet_gochara
)

# Import Ashtakavarga functions
from astrovedic.vedic.transits.ashtakavarga import (
    get_transit_ashtakavarga, get_transit_bindus
)


def get_basic_transit_data(natal_chart, transit_date):
    """
    Get basic transit data for a specific date.

    Args:
        natal_chart (Chart): The natal chart
        transit_date (Datetime): The transit date

    Returns:
        dict: Dictionary with basic transit data
    """
    # Get the transit chart
    transit_chart = get_transit_chart(natal_chart, transit_date)

    # Get the transit planets
    transit_planets = get_transit_planets(natal_chart, transit_chart)

    # Get the transit aspects
    transit_aspects = get_transit_aspects(natal_chart, transit_chart)

    # Get the transit houses
    transit_houses = get_transit_houses(natal_chart, transit_chart)

    # Get the transit quality
    transit_quality = get_transit_quality(natal_chart, transit_chart)

    # Get the Gochara effects
    gochara_effects = get_gochara_effects(natal_chart, transit_chart)

    # Get the Ashtakavarga transit data
    ashtakavarga_data = get_transit_ashtakavarga(natal_chart, transit_chart)

    # Compile the basic transit data
    data = {
        'transit_date': transit_date,
        'transit_planets': transit_planets,
        'transit_aspects': transit_aspects,
        'transit_houses': transit_houses,
        'transit_quality': transit_quality,
        'gochara_effects': gochara_effects,
        'ashtakavarga_data': ashtakavarga_data
    }

    return data


def get_basic_transit_analysis(natal_chart, transit_date):
    """
    Alias for get_basic_transit_data for backward compatibility.

    Args:
        natal_chart (Chart): The natal chart
        transit_date (Datetime): The transit date

    Returns:
        dict: Dictionary with basic transit data
    """
    return get_basic_transit_data(natal_chart, transit_date)
