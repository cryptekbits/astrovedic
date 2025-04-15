"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements basic analysis tools for Sarvatobhadra Chakra
    in Vedic astrology. For detailed analysis and reporting,
    use the astroved_extension package.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos

# Import core functions
from astrovedic.vedic.sarvatobhadra.core import (
    get_sarvatobhadra_chakra, get_chakra_quality,
    get_auspicious_directions, get_inauspicious_directions
)

# Import direction functions
from astrovedic.vedic.sarvatobhadra.directions import (
    get_direction_quality, get_best_direction,
    get_direction_for_activity
)

# Import Tara Bala functions
from astrovedic.vedic.sarvatobhadra.tara import (
    get_tara_bala
)


def get_basic_sarvatobhadra_data(chart):
    """
    Get basic Sarvatobhadra Chakra data for a chart.

    Args:
        chart (Chart): The chart

    Returns:
        dict: Dictionary with basic Sarvatobhadra Chakra data
    """
    # Get the Sarvatobhadra Chakra
    chakra = get_sarvatobhadra_chakra(chart)

    # Get the chakra quality
    quality = get_chakra_quality(chakra)

    # Get auspicious directions
    auspicious_directions = get_auspicious_directions(chakra)

    # Get inauspicious directions
    inauspicious_directions = get_inauspicious_directions(chakra)

    # Get Tara Bala
    tara_bala = get_tara_bala(chart)

    # Get the best direction
    best_direction = get_best_direction(chakra)

    # Generate a basic analysis
    analysis = {
        'quality': quality,
        'auspicious_directions': auspicious_directions,
        'inauspicious_directions': inauspicious_directions,
        'best_direction': best_direction,
        'tara_bala': tara_bala
    }

    return analysis


def get_basic_sarvatobhadra_analysis(chart):
    """
    Alias for get_basic_sarvatobhadra_data for backward compatibility.

    Args:
        chart (Chart): The chart

    Returns:
        dict: Dictionary with basic Sarvatobhadra Chakra data
    """
    return get_basic_sarvatobhadra_data(chart)
