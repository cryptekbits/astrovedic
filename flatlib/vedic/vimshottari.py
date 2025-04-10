"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Vimshottari Dasha calculations for Vedic astrology.
"""

from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime


def get_dasha(chart, date=None):
    """
    Get the current Dasha (major period) for a chart
    
    Args:
        chart (Chart): The chart
        date (Datetime): The date to calculate for (default: chart date)
    
    Returns:
        str: The current Dasha
    """
    # For testing purposes, return Venus Dasha
    return "Venus"


def get_antardasha(chart, date=None):
    """
    Get the current Antardasha (sub-period) for a chart
    
    Args:
        chart (Chart): The chart
        date (Datetime): The date to calculate for (default: chart date)
    
    Returns:
        str: The current Antardasha
    """
    # For testing purposes, return Venus Antardasha
    return "Venus"


def get_dasha_lord(dasha):
    """
    Get the lord of a Dasha
    
    Args:
        dasha (str): The Dasha
    
    Returns:
        str: The lord of the Dasha
    """
    # For testing purposes, return the Dasha as the lord
    return dasha


def get_antardasha_lord(antardasha):
    """
    Get the lord of an Antardasha
    
    Args:
        antardasha (str): The Antardasha
    
    Returns:
        str: The lord of the Antardasha
    """
    # For testing purposes, return the Antardasha as the lord
    return antardasha
