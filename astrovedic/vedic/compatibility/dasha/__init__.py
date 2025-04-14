"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Dasha compatibility analysis
    for Vedic astrology.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos

from astrovedic.vedic.compatibility.dasha.compatibility import (
    get_dasha_compatibility, get_antardasha_compatibility
)

from astrovedic.vedic.compatibility.dasha.periods import (
    get_dasha_periods_compatibility
)

from astrovedic.vedic.compatibility.dasha.helpers import (
    get_dasha, get_antardasha, get_dasha_lord, get_antardasha_lord
)

from astrovedic.vedic.compatibility.dasha.predictions import (
    get_dasha_predictions
)


def get_dasha_compatibility(chart1, chart2):
    """
    Get the Dasha compatibility between two charts

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with Dasha compatibility information
    """
    from astrovedic.vedic.compatibility.dasha.compatibility import get_dasha_compatibility as get_compatibility
    return get_compatibility(chart1, chart2)


def get_antardasha_compatibility(chart1, chart2):
    """
    Get the Antardasha compatibility between two charts

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with Antardasha compatibility information
    """
    from astrovedic.vedic.compatibility.dasha.compatibility import get_antardasha_compatibility as get_compatibility
    return get_compatibility(chart1, chart2)


def get_dasha_periods_compatibility(chart1, chart2):
    """
    Get the compatibility of Dasha periods between two charts

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with Dasha periods compatibility information
    """
    from astrovedic.vedic.compatibility.dasha.compatibility import get_dasha_periods_compatibility as get_compatibility
    return get_compatibility(chart1, chart2)


def get_dasha_predictions(chart1, chart2):
    """
    Get the Dasha-based predictions for the compatibility between two charts

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with Dasha-based predictions
    """
    from astrovedic.vedic.compatibility.dasha.predictions import get_dasha_predictions as get_predictions
    return get_predictions(chart1, chart2)
