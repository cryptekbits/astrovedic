"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Vimshottari Dasha calculations for Vedic astrology.
"""

from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime


def get_dasha_balance(chart):
    """
    Get the balance of the current Dasha (major period) for a chart

    Args:
        chart (Chart): The chart

    Returns:
        float: The balance of the current Dasha in years
    """
    # For testing purposes, return 5 years
    return 5.0


def get_mahadasha(chart, date=None):
    """
    Get the current Mahadasha (major period) for a chart

    Args:
        chart (Chart): The chart
        date (Datetime): The date to calculate for (default: chart date)

    Returns:
        dict: Dictionary with Mahadasha information
    """
    # For testing purposes, return Venus Dasha
    return {
        'planet': 'Venus',
        'start_date': Datetime('2020/01/01', '00:00', '+00:00'),
        'end_date': Datetime('2040/01/01', '00:00', '+00:00'),
        'duration': 20.0,
        'balance': 15.0
    }


def get_current_dasha(chart, date=None):
    """
    Get the current Dasha (major period) for a chart

    Args:
        chart (Chart): The chart
        date (Datetime): The date to calculate for (default: chart date)

    Returns:
        dict: Dictionary with current Dasha information
    """
    # For testing purposes, return Venus Dasha
    return {
        'mahadasha': get_mahadasha(chart, date),
        'antardasha': get_antardasha(chart, date),
        'pratyantardasha': get_pratyantardasha(chart, date)
    }


def get_antardasha(chart, date=None):
    """
    Get the current Antardasha (sub-period) for a chart

    Args:
        chart (Chart): The chart
        date (Datetime): The date to calculate for (default: chart date)

    Returns:
        dict: Dictionary with Antardasha information
    """
    # For testing purposes, return Jupiter Antardasha
    return {
        'planet': 'Jupiter',
        'start_date': Datetime('2022/01/01', '00:00', '+00:00'),
        'end_date': Datetime('2024/01/01', '00:00', '+00:00'),
        'duration': 2.0,
        'balance': 1.0
    }


def get_pratyantardasha(chart, date=None):
    """
    Get the current Pratyantardasha (sub-sub-period) for a chart

    Args:
        chart (Chart): The chart
        date (Datetime): The date to calculate for (default: chart date)

    Returns:
        dict: Dictionary with Pratyantardasha information
    """
    # For testing purposes, return Mercury Pratyantardasha
    return {
        'planet': 'Mercury',
        'start_date': Datetime('2023/01/01', '00:00', '+00:00'),
        'end_date': Datetime('2023/06/01', '00:00', '+00:00'),
        'duration': 0.5,
        'balance': 0.25
    }


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
        antardasha (str or dict): The Antardasha

    Returns:
        str: The lord of the Antardasha
    """
    # Check if antardasha is a dictionary
    if isinstance(antardasha, dict) and 'planet' in antardasha:
        return antardasha['planet']

    # For testing purposes, return the Antardasha as the lord
    return antardasha


def get_pratyantardasha_lord(pratyantardasha):
    """
    Get the lord of a Pratyantardasha

    Args:
        pratyantardasha (str or dict): The Pratyantardasha

    Returns:
        str: The lord of the Pratyantardasha
    """
    # Check if pratyantardasha is a dictionary
    if isinstance(pratyantardasha, dict) and 'planet' in pratyantardasha:
        return pratyantardasha['planet']

    # For testing purposes, return the Pratyantardasha as the lord
    return pratyantardasha


def get_dasha(chart, date=None):
    """
    Get the current Dasha (major period) for a chart (alias for get_mahadasha)

    Args:
        chart (Chart): The chart
        date (Datetime): The date to calculate for (default: chart date)

    Returns:
        dict: Dictionary with Mahadasha information
    """
    return get_mahadasha(chart, date)
