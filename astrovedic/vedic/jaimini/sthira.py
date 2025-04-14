"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Jaimini Sthira Dasha calculations for Vedic astrology.
    Sthira Dasha is a fixed dasha system based on the position of the Lagna (Ascendant).
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from datetime import datetime, timedelta
from typing import Dict, Optional, Any, List, Tuple

# Sthira Dasha periods (in years)
STHIRA_PERIODS = {
    const.ARIES: 7,
    const.TAURUS: 8,
    const.GEMINI: 9,
    const.CANCER: 10,
    const.LEO: 11,
    const.VIRGO: 12,
    const.LIBRA: 13,
    const.SCORPIO: 14,
    const.SAGITTARIUS: 15,
    const.CAPRICORN: 16,
    const.AQUARIUS: 17,
    const.PISCES: 18
}

# Total years in Sthira Dasha cycle
TOTAL_STHIRA_YEARS = sum(STHIRA_PERIODS.values())  # 150 years

# Sthira Dasha sequence (standard order starting from Aries)
STHIRA_SEQUENCE = [
    const.ARIES, const.TAURUS, const.GEMINI, const.CANCER,
    const.LEO, const.VIRGO, const.LIBRA, const.SCORPIO,
    const.SAGITTARIUS, const.CAPRICORN, const.AQUARIUS, const.PISCES
]

def calculate_sthira_dasha_balance(lagna_sign: str, lagna_degree: float) -> float:
    """
    Calculate the balance of the current Sthira Dasha at birth

    Args:
        lagna_sign (str): The Lagna (Ascendant) sign
        lagna_degree (float): The degree within the sign (0-30)

    Returns:
        float: The balance of the current Sthira Dasha in years
    """
    # Calculate the percentage of sign traversed
    percentage_traversed = lagna_degree / 30.0
    
    # Calculate the balance of the current Sthira Dasha
    years_of_dasha = STHIRA_PERIODS[lagna_sign]
    balance = years_of_dasha * (1 - percentage_traversed)
    
    return balance

def get_sthira_sequence(lagna_sign: str) -> List[Dict[str, Any]]:
    """
    Get the sequence of Sthira Dashas starting from birth

    Args:
        lagna_sign (str): The Lagna (Ascendant) sign

    Returns:
        list: List of dictionaries with Sthira Dasha information
    """
    # Find the starting index in the Sthira sequence
    start_idx = STHIRA_SEQUENCE.index(lagna_sign)
    
    # Create the sequence of Sthira Dashas
    sthira_sequence = []
    
    # Add all Sthira Dashas in sequence
    for i in range(12):
        idx = (start_idx + i) % 12
        sign = STHIRA_SEQUENCE[idx]
        
        sthira_sequence.append({
            'sign': sign,
            'years': STHIRA_PERIODS[sign]
        })
    
    return sthira_sequence

def get_sthira_antardasha_sequence(mahadasha_sign: str, mahadasha_years: float) -> List[Dict[str, Any]]:
    """
    Get the sequence of Sthira Antardashas (sub-periods) for a given Mahadasha

    Args:
        mahadasha_sign (str): The sign ruling the Mahadasha
        mahadasha_years (float): The duration of the Mahadasha in years

    Returns:
        list: List of dictionaries with Antardasha information
    """
    # Find the starting index in the Sthira sequence
    start_idx = STHIRA_SEQUENCE.index(mahadasha_sign)
    
    # Create the sequence of Antardashas
    antardasha_sequence = []
    
    # Add all Antardashas in sequence
    for i in range(12):
        idx = (start_idx + i) % 12
        sign = STHIRA_SEQUENCE[idx]
        
        # Calculate the duration of the Antardasha
        years = (STHIRA_PERIODS[sign] / TOTAL_STHIRA_YEARS) * mahadasha_years
        
        antardasha_sequence.append({
            'sign': sign,
            'years': years
        })
    
    return antardasha_sequence

def years_to_days(years: float) -> float:
    """
    Convert years to days

    Args:
        years (float): Number of years

    Returns:
        float: Number of days
    """
    return years * 365.25

def add_years_to_date(date: datetime, years: float) -> datetime:
    """
    Add a number of years to a date

    Args:
        date (datetime): The starting date
        years (float): Number of years to add

    Returns:
        datetime: The resulting date
    """
    days = years_to_days(years)
    return date + timedelta(days=days)

def calculate_sthira_dasha_periods(birth_date: datetime, lagna_sign: str, lagna_degree: float) -> Dict[str, Any]:
    """
    Calculate all Sthira Dasha periods from birth

    Args:
        birth_date (datetime): The birth date
        lagna_sign (str): The Lagna (Ascendant) sign
        lagna_degree (float): The degree within the sign (0-30)

    Returns:
        dict: Dictionary with Mahadasha and Antardasha information
    """
    # Convert flatlib Datetime to Python datetime if needed
    if isinstance(birth_date, Datetime):
        birth_dt = birth_date.to_datetime()
    else:
        birth_dt = birth_date
    
    # Calculate the balance of the current Sthira Dasha
    balance = calculate_sthira_dasha_balance(lagna_sign, lagna_degree)
    
    # Get the Sthira Dasha sequence
    sthira_sequence = get_sthira_sequence(lagna_sign)
    
    # Calculate start and end dates for each Mahadasha
    current_date = birth_dt
    mahadashas = []
    
    # Add the first Mahadasha with its balance
    first_mahadasha = sthira_sequence[0]
    first_sign = first_mahadasha['sign']
    
    start_date = current_date
    end_date = add_years_to_date(start_date, balance)
    
    # Get Antardashas for this Mahadasha
    antardasha_sequence = get_sthira_antardasha_sequence(first_sign, balance)
    antardashas = []
    
    # Calculate start and end dates for each Antardasha
    antardasha_date = start_date
    
    for antardasha in antardasha_sequence:
        ad_sign = antardasha['sign']
        ad_years = antardasha['years']
        
        ad_start_date = antardasha_date
        ad_end_date = add_years_to_date(ad_start_date, ad_years)
        
        antardashas.append({
            'sign': ad_sign,
            'start_date': ad_start_date,
            'end_date': ad_end_date,
            'years': ad_years
        })
        
        antardasha_date = ad_end_date
    
    mahadashas.append({
        'sign': first_sign,
        'start_date': start_date,
        'end_date': end_date,
        'years': balance,
        'antardashas': antardashas
    })
    
    current_date = end_date
    
    # Add the remaining Mahadashas
    for i in range(1, 12):
        mahadasha = sthira_sequence[i]
        sign = mahadasha['sign']
        years = mahadasha['years']
        
        start_date = current_date
        end_date = add_years_to_date(start_date, years)
        
        # Get Antardashas for this Mahadasha
        antardasha_sequence = get_sthira_antardasha_sequence(sign, years)
        antardashas = []
        
        # Calculate start and end dates for each Antardasha
        antardasha_date = start_date
        
        for antardasha in antardasha_sequence:
            ad_sign = antardasha['sign']
            ad_years = antardasha['years']
            
            ad_start_date = antardasha_date
            ad_end_date = add_years_to_date(ad_start_date, ad_years)
            
            antardashas.append({
                'sign': ad_sign,
                'start_date': ad_start_date,
                'end_date': ad_end_date,
                'years': ad_years
            })
            
            antardasha_date = ad_end_date
        
        mahadashas.append({
            'sign': sign,
            'start_date': start_date,
            'end_date': end_date,
            'years': years,
            'antardashas': antardashas
        })
        
        current_date = end_date
    
    return {
        'mahadashas': mahadashas,
        'birth_date': birth_dt,
        'lagna_sign': lagna_sign,
        'lagna_degree': lagna_degree
    }

def get_current_sthira_dasha(dasha_periods: Dict[str, Any], date: Optional[datetime] = None) -> Optional[Dict[str, Any]]:
    """
    Get the current operating Sthira Dasha period

    Args:
        dasha_periods (dict): Dictionary with Dasha periods
        date (datetime, optional): The date to check. Defaults to current date.

    Returns:
        dict: Dictionary with current Mahadasha and Antardasha
    """
    if date is None:
        date = datetime.now()
    
    # Find the current Mahadasha
    current_mahadasha = None
    for mahadasha in dasha_periods['mahadashas']:
        if mahadasha['start_date'] <= date < mahadasha['end_date']:
            current_mahadasha = mahadasha
            break
    
    if not current_mahadasha:
        return None
    
    # Find the current Antardasha
    current_antardasha = None
    for antardasha in current_mahadasha['antardashas']:
        if antardasha['start_date'] <= date < antardasha['end_date']:
            current_antardasha = antardasha
            break
    
    if not current_antardasha:
        return {
            'mahadasha': current_mahadasha,
            'antardasha': None
        }
    
    return {
        'mahadasha': current_mahadasha,
        'antardasha': current_antardasha,
        'mahadasha_start': current_mahadasha['start_date'],
        'mahadasha_end': current_mahadasha['end_date'],
        'antardasha_start': current_antardasha['start_date'],
        'antardasha_end': current_antardasha['end_date']
    }

def get_dasha_balance(chart: Chart) -> float:
    """
    Get the balance of the first Sthira Dasha (major period) at birth for a chart.

    Args:
        chart (Chart): The chart object containing birth details.

    Returns:
        float: The balance of the first Sthira Dasha in years.

    Raises:
        ValueError: If the Lagna (Ascendant) is not found in the chart.
    """
    # Get the Lagna (Ascendant) sign and degree
    lagna = chart.getAngle(const.ASC)
    if lagna is None:
        raise ValueError("Lagna (Ascendant) not found in the chart.")
    
    lagna_sign = lagna.sign
    lagna_degree = lagna.signlon
    
    return calculate_sthira_dasha_balance(lagna_sign, lagna_degree)

def get_current_dasha(chart: Chart, date: Optional[Datetime] = None) -> Optional[Dict[str, Any]]:
    """
    Get the current operating Sthira Dasha for a chart at a specific date.

    Args:
        chart (Chart): The chart object containing birth details.
        date (Datetime, optional): The date to calculate for. 
                                   Defaults to the chart's date if None.

    Returns:
        dict or None: A dictionary containing the current 'mahadasha' and
                      'antardasha' lords and their periods, or None if calculation fails.

    Raises:
        ValueError: If the Lagna (Ascendant) or birth date is not found in the chart.
    """
    # Get the Lagna (Ascendant) sign and degree
    lagna = chart.getAngle(const.ASC)
    if lagna is None:
        raise ValueError("Lagna (Ascendant) not found in the chart.")
    
    if chart.date is None:
         raise ValueError("Birth date not found in the chart.")

    lagna_sign = lagna.sign
    lagna_degree = lagna.signlon
    
    target_date = date if date else chart.date

    # Calculate all dasha periods starting from birth
    all_periods = calculate_sthira_dasha_periods(chart.date.to_datetime(), lagna_sign, lagna_degree)
    
    # Find the specific dasha for the target date
    current_dasha_info = get_current_sthira_dasha(all_periods, target_date.to_datetime())

    return current_dasha_info

def get_mahadasha(chart: Chart, date: Optional[Datetime] = None) -> Optional[Dict[str, Any]]:
    """
    Get the current Sthira Mahadasha (major period) for a chart at a specific date.

    Args:
        chart (Chart): The chart object containing birth details.
        date (Datetime, optional): The date to calculate for. 
                                   Defaults to the chart's date if None.

    Returns:
        dict or None: Dictionary with current Mahadasha information 
                      (sign, start_date, end_date), or None if not found.
    """
    current_dasha = get_current_dasha(chart, date)
    return current_dasha.get('mahadasha') if current_dasha else None

def get_antardasha(chart: Chart, date: Optional[Datetime] = None) -> Optional[Dict[str, Any]]:
    """
    Get the current Sthira Antardasha (sub-period) for a chart at a specific date.

    Args:
        chart (Chart): The chart object containing birth details.
        date (Datetime, optional): The date to calculate for. 
                                   Defaults to the chart's date if None.

    Returns:
        dict or None: Dictionary with current Antardasha information 
                      (sign, start_date, end_date), or None if not found.
    """
    current_dasha = get_current_dasha(chart, date)
    return current_dasha.get('antardasha') if current_dasha else None

def get_dasha_lord(dasha_info: Optional[Dict[str, Any]]) -> Optional[str]:
    """
    Get the ruling sign from a Dasha information dictionary.

    Args:
        dasha_info (dict or None): The Dasha dictionary containing a 'sign' key.

    Returns:
        str or None: The sign of the Dasha, or None if input is invalid.
    """
    return dasha_info.get('sign') if isinstance(dasha_info, dict) else None

def get_antardasha_lord(antardasha_info: Optional[Dict[str, Any]]) -> Optional[str]:
    """
    Get the ruling sign from an Antardasha information dictionary.

    Args:
        antardasha_info (dict or None): The Antardasha dictionary containing a 'sign' key.

    Returns:
        str or None: The sign of the Antardasha, or None if input is invalid.
    """
    return get_dasha_lord(antardasha_info)

def get_dasha(chart: Chart, date: Optional[Datetime] = None) -> Optional[Dict[str, Any]]:
    """
    Alias for get_mahadasha.
    Get the current Sthira Mahadasha (major period) for a chart at a specific date.

    Args:
        chart (Chart): The chart object containing birth details.
        date (Datetime, optional): The date to calculate for. 
                                   Defaults to the chart's date if None.

    Returns:
        dict or None: Dictionary with current Mahadasha information, or None if not found.
    """
    return get_mahadasha(chart, date)
