"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Vimshottari Dasha calculations for Vedic astrology.
"""

from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.vedic.dashas import (
    calculate_dasha_balance as calculate_actual_dasha_balance,
    calculate_dasha_periods as calculate_actual_dasha_periods,
    get_current_dasha as get_actual_current_dasha
)
from typing import Dict, Optional, Any


def get_dasha_balance(chart: Chart) -> float:
    """
    Get the balance of the first Mahadasha (major period) at birth for a chart.

    This function retrieves the Moon's longitude from the chart and uses the
    standard Vimshottari Dasha calculation based on the Moon's Nakshatra position
    to determine the remaining duration of the first Dasha period.

    Args:
        chart (Chart): The chart object containing birth details.

    Returns:
        float: The balance of the first Mahadasha in years.

    Raises:
        ValueError: If the Moon object is not found in the chart.
    """
    moon = chart.getObject(const.MOON)
    if moon is None:
        raise ValueError("Moon object not found in the chart.")
    
    return calculate_actual_dasha_balance(moon.lon)


def get_current_dasha(chart: Chart, date: Optional[Datetime] = None) -> Optional[Dict[str, Any]]:
    """
    Get the current operating Vimshottari Dasha (Mahadasha, Antardasha, 
    Pratyantardasha) for a chart at a specific date.

    Args:
        chart (Chart): The chart object containing birth details.
        date (Datetime, optional): The date to calculate for. 
                                   Defaults to the chart's date if None.

    Returns:
        dict or None: A dictionary containing the current 'mahadasha', 
                      'antardasha', and 'pratyantardasha' lords and their 
                      periods, or None if calculation fails.

    Raises:
        ValueError: If the Moon object or birth date is not found in the chart.
    """
    moon = chart.getObject(const.MOON)
    if moon is None:
        raise ValueError("Moon object not found in the chart.")
    
    if chart.date is None:
         raise ValueError("Birth date not found in the chart.")

    target_date = date if date else chart.date

    # Calculate all dasha periods starting from birth
    # Note: calculate_actual_dasha_periods requires a datetime.datetime object
    all_periods = calculate_actual_dasha_periods(chart.date.to_datetime(), moon.lon)
    
    # Find the specific dasha for the target date
    # Note: get_actual_current_dasha also requires datetime.datetime
    current_dasha_info = get_actual_current_dasha(all_periods, target_date.to_datetime())

    return current_dasha_info


def get_mahadasha(chart: Chart, date: Optional[Datetime] = None) -> Optional[Dict[str, Any]]:
    """
    Get the current Mahadasha (major period) for a chart at a specific date.

    Args:
        chart (Chart): The chart object containing birth details.
        date (Datetime, optional): The date to calculate for. 
                                   Defaults to the chart's date if None.

    Returns:
        dict or None: Dictionary with current Mahadasha information 
                      (planet, start_date, end_date), or None if not found.
    """
    current_dasha = get_current_dasha(chart, date)
    return current_dasha.get('mahadasha') if current_dasha else None


def get_antardasha(chart: Chart, date: Optional[Datetime] = None) -> Optional[Dict[str, Any]]:
    """
    Get the current Antardasha (sub-period) for a chart at a specific date.

    Args:
        chart (Chart): The chart object containing birth details.
        date (Datetime, optional): The date to calculate for. 
                                   Defaults to the chart's date if None.

    Returns:
        dict or None: Dictionary with current Antardasha information 
                      (planet, start_date, end_date), or None if not found.
    """
    current_dasha = get_current_dasha(chart, date)
    return current_dasha.get('antardasha') if current_dasha else None


def get_pratyantardasha(chart: Chart, date: Optional[Datetime] = None) -> Optional[Dict[str, Any]]:
    """
    Get the current Pratyantardasha (sub-sub-period) for a chart at a specific date.

    Args:
        chart (Chart): The chart object containing birth details.
        date (Datetime, optional): The date to calculate for. 
                                   Defaults to the chart's date if None.

    Returns:
        dict or None: Dictionary with current Pratyantardasha information 
                      (planet, start_date, end_date), or None if not found.
    """
    current_dasha = get_current_dasha(chart, date)
    return current_dasha.get('pratyantardasha') if current_dasha else None


def get_dasha_lord(dasha_info: Optional[Dict[str, Any]]) -> Optional[str]:
    """
    Get the ruling planet (lord) from a Dasha information dictionary.

    Args:
        dasha_info (dict or None): The Dasha dictionary (e.g., from get_mahadasha) 
                                   containing a 'planet' key.

    Returns:
        str or None: The lord of the Dasha, or None if input is invalid.
    """
    return dasha_info.get('planet') if isinstance(dasha_info, dict) else None


def get_antardasha_lord(antardasha_info: Optional[Dict[str, Any]]) -> Optional[str]:
    """
    Get the ruling planet (lord) from an Antardasha information dictionary.

    Args:
        antardasha_info (dict or None): The Antardasha dictionary containing a 'planet' key.

    Returns:
        str or None: The lord of the Antardasha, or None if input is invalid.
    """
    return get_dasha_lord(antardasha_info)


def get_pratyantardasha_lord(pratyantardasha_info: Optional[Dict[str, Any]]) -> Optional[str]:
    """
    Get the ruling planet (lord) from a Pratyantardasha information dictionary.

    Args:
        pratyantardasha_info (dict or None): The Pratyantardasha dictionary containing a 'planet' key.

    Returns:
        str or None: The lord of the Pratyantardasha, or None if input is invalid.
    """
    return get_dasha_lord(pratyantardasha_info)


def get_dasha(chart: Chart, date: Optional[Datetime] = None) -> Optional[Dict[str, Any]]:
    """
    Alias for get_mahadasha.
    Get the current Mahadasha (major period) for a chart at a specific date.

    Args:
        chart (Chart): The chart object containing birth details.
        date (Datetime, optional): The date to calculate for. 
                                   Defaults to the chart's date if None.

    Returns:
        dict or None: Dictionary with current Mahadasha information, or None if not found.
    """
    return get_mahadasha(chart, date)
