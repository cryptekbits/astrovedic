"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements helper functions for Dasha compatibility analysis
    in Vedic astrology.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.vedic.dashas import (
    get_current_dasha, calculate_dasha_periods
)


def get_dasha(chart, date):
    """
    Get the current Dasha for a chart

    Args:
        chart (Chart): The chart
        date (Datetime): The date

    Returns:
        str: The current Dasha
    """
    # Get the Moon
    moon = chart.getObject(const.MOON)

    # Calculate dasha periods
    dasha_periods = calculate_dasha_periods(chart.date, moon.lon)

    # Get current dasha
    # Convert Datetime to Python datetime if needed
    if hasattr(date, 'jd'):
        from datetime import datetime
        dt = datetime.fromtimestamp(date.jd * 86400.0 - 2440587.5 * 86400.0)
    else:
        dt = date

    current_dasha = get_current_dasha(dasha_periods, dt)

    # Handle the case when current_dasha is None
    if current_dasha is None:
        return "Unknown"

    return current_dasha.get('mahadasha', "Unknown")


def get_antardasha(chart, date):
    """
    Get the current Antardasha for a chart

    Args:
        chart (Chart): The chart
        date (Datetime): The date

    Returns:
        str: The current Antardasha
    """
    # Get the Moon
    moon = chart.getObject(const.MOON)

    # Calculate dasha periods
    dasha_periods = calculate_dasha_periods(chart.date, moon.lon)

    # Get current dasha
    # Convert Datetime to Python datetime if needed
    if hasattr(date, 'jd'):
        from datetime import datetime
        dt = datetime.fromtimestamp(date.jd * 86400.0 - 2440587.5 * 86400.0)
    else:
        dt = date

    current_dasha = get_current_dasha(dasha_periods, dt)

    # Handle the case when current_dasha is None
    if current_dasha is None:
        return "Unknown"

    return current_dasha.get('antardasha', "Unknown")


def get_dasha_lord(dasha):
    """
    Get the lord of a Dasha

    Args:
        dasha (str): The Dasha

    Returns:
        str: The Dasha lord
    """
    return dasha


def get_antardasha_lord(antardasha):
    """
    Get the lord of an Antardasha

    Args:
        antardasha (str): The Antardasha

    Returns:
        str: The Antardasha lord
    """
    return antardasha
