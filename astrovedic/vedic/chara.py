"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Chara Dasha calculations for Vedic astrology.
    Chara Dasha is a conditional dasha system based on the rising sign (lagna).
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from datetime import datetime, timedelta
from typing import Dict, Optional, Any, List, Tuple

# Chara Dasha periods (in years) for each sign
# The order is based on the sign's position from the Lagna
CHARA_PERIODS = {
    const.ARIES: 10,
    const.TAURUS: 9,
    const.GEMINI: 8,
    const.CANCER: 7,
    const.LEO: 6,
    const.VIRGO: 5,
    const.LIBRA: 4,
    const.SCORPIO: 3,
    const.SAGITTARIUS: 2,
    const.CAPRICORN: 1,
    const.AQUARIUS: 11,
    const.PISCES: 12
}

# Total years in Chara Dasha cycle
TOTAL_CHARA_YEARS = sum(CHARA_PERIODS.values())  # 78 years

def get_sign_sequence_from_lagna(lagna_sign: str) -> List[str]:
    """
    Get the sequence of signs starting from the lagna sign

    Args:
        lagna_sign (str): The lagna (ascendant) sign

    Returns:
        list: List of signs in sequence from lagna
    """
    # List of all signs in zodiacal order
    all_signs = [
        const.ARIES, const.TAURUS, const.GEMINI, const.CANCER,
        const.LEO, const.VIRGO, const.LIBRA, const.SCORPIO,
        const.SAGITTARIUS, const.CAPRICORN, const.AQUARIUS, const.PISCES
    ]
    
    # Find the index of the lagna sign
    lagna_index = all_signs.index(lagna_sign)
    
    # Create the sequence starting from lagna
    sign_sequence = []
    for i in range(12):
        idx = (lagna_index + i) % 12
        sign_sequence.append(all_signs[idx])
    
    return sign_sequence

def calculate_chara_dasha_balance(lagna_longitude: float) -> Tuple[str, float]:
    """
    Calculate the balance of the current Chara Dasha at birth

    Args:
        lagna_longitude (float): The Lagna's longitude in degrees (0-360)

    Returns:
        tuple: (sign, balance_years) - The current sign and balance in years
    """
    # Determine the lagna sign
    sign_index = int(lagna_longitude / 30)
    all_signs = [
        const.ARIES, const.TAURUS, const.GEMINI, const.CANCER,
        const.LEO, const.VIRGO, const.LIBRA, const.SCORPIO,
        const.SAGITTARIUS, const.CAPRICORN, const.AQUARIUS, const.PISCES
    ]
    lagna_sign = all_signs[sign_index]
    
    # Calculate position within sign (0-30 degrees)
    pos_in_sign = lagna_longitude % 30
    
    # Calculate the percentage of sign traversed
    percentage_traversed = pos_in_sign / 30
    
    # Calculate the balance of the current Chara Dasha
    years_of_dasha = CHARA_PERIODS[lagna_sign]
    balance = years_of_dasha * (1 - percentage_traversed)
    
    return (lagna_sign, balance)

def get_chara_dasha_sequence(lagna_longitude: float) -> List[Dict[str, Any]]:
    """
    Get the sequence of Chara Dashas starting from birth

    Args:
        lagna_longitude (float): The Lagna's longitude in degrees (0-360)

    Returns:
        list: List of dictionaries with Chara Dasha information
    """
    # Determine the lagna sign
    sign_index = int(lagna_longitude / 30)
    all_signs = [
        const.ARIES, const.TAURUS, const.GEMINI, const.CANCER,
        const.LEO, const.VIRGO, const.LIBRA, const.SCORPIO,
        const.SAGITTARIUS, const.CAPRICORN, const.AQUARIUS, const.PISCES
    ]
    lagna_sign = all_signs[sign_index]
    
    # Calculate the balance of the current Chara Dasha
    current_sign, balance = calculate_chara_dasha_balance(lagna_longitude)
    
    # Get the sequence of signs from lagna
    sign_sequence = get_sign_sequence_from_lagna(lagna_sign)
    
    # Create the sequence of Chara Dashas
    chara_sequence = []
    
    # Add the current Chara Dasha with its balance
    chara_sequence.append({
        'sign': current_sign,
        'years': balance
    })
    
    # Add the remaining Chara Dashas in sequence
    current_sign_index = sign_sequence.index(current_sign)
    for i in range(1, 12):
        idx = (current_sign_index + i) % 12
        sign = sign_sequence[idx]
        chara_sequence.append({
            'sign': sign,
            'years': CHARA_PERIODS[sign]
        })
    
    return chara_sequence

def get_chara_antardasha_sequence(mahadasha_sign: str, mahadasha_years: float) -> List[Dict[str, Any]]:
    """
    Get the sequence of Chara Antardashas (sub-periods) for a given Mahadasha

    Args:
        mahadasha_sign (str): The sign ruling the Mahadasha
        mahadasha_years (float): The duration of the Mahadasha in years

    Returns:
        list: List of dictionaries with Antardasha information
    """
    # Get the sequence of signs from the mahadasha sign
    sign_sequence = get_sign_sequence_from_lagna(mahadasha_sign)
    
    # Create the sequence of Antardashas
    antardasha_sequence = []
    
    # Add all Antardashas in sequence
    for sign in sign_sequence:
        # Calculate the duration of the Antardasha
        years = (CHARA_PERIODS[sign] / TOTAL_CHARA_YEARS) * mahadasha_years
        
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

def calculate_chara_dasha_periods(birth_date: datetime, lagna_longitude: float) -> Dict[str, Any]:
    """
    Calculate all Chara Dasha periods from birth

    Args:
        birth_date (datetime): The birth date
        lagna_longitude (float): The Lagna's longitude in degrees (0-360)

    Returns:
        dict: Dictionary with Mahadasha and Antardasha information
    """
    # Convert flatlib Datetime to Python datetime if needed
    if isinstance(birth_date, Datetime):
        # Create a Python datetime from the components
        date_parts = str(birth_date.date).strip('<>').split('/')
        time_parts = str(birth_date.time).strip('<>').split(':')
        
        year = int(date_parts[0])
        month = int(date_parts[1])
        day = int(date_parts[2])
        hour = int(time_parts[0])
        minute = int(time_parts[1])
        
        birth_dt = datetime(year, month, day, hour, minute)
    else:
        birth_dt = birth_date
    
    # Get the Chara Dasha sequence
    chara_sequence = get_chara_dasha_sequence(lagna_longitude)
    
    # Calculate start and end dates for each Mahadasha
    current_date = birth_dt
    mahadashas = []
    
    for mahadasha in chara_sequence:
        sign = mahadasha['sign']
        years = mahadasha['years']
        
        start_date = current_date
        end_date = add_years_to_date(start_date, years)
        
        # Get Antardashas for this Mahadasha
        antardasha_sequence = get_chara_antardasha_sequence(sign, years)
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
        'lagna_longitude': lagna_longitude
    }

def get_current_chara_dasha(dasha_periods: Dict[str, Any], date: Optional[datetime] = None) -> Optional[Dict[str, Any]]:
    """
    Get the current operating Chara Dasha period

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
    Get the balance of the first Chara Dasha (major period) at birth for a chart.

    Args:
        chart (Chart): The chart object containing birth details.

    Returns:
        float: The balance of the first Chara Dasha in years.

    Raises:
        ValueError: If the Ascendant is not found in the chart.
    """
    asc = chart.getAngle(const.ASC)
    if asc is None:
        raise ValueError("Ascendant not found in the chart.")
    
    _, balance = calculate_chara_dasha_balance(asc.lon)
    return balance

def get_current_dasha(chart: Chart, date: Optional[Datetime] = None) -> Optional[Dict[str, Any]]:
    """
    Get the current operating Chara Dasha for a chart at a specific date.

    Args:
        chart (Chart): The chart object containing birth details.
        date (Datetime, optional): The date to calculate for. 
                                   Defaults to the chart's date if None.

    Returns:
        dict or None: A dictionary containing the current 'mahadasha' and
                      'antardasha' signs and their periods, or None if calculation fails.

    Raises:
        ValueError: If the Ascendant or birth date is not found in the chart.
    """
    asc = chart.getAngle(const.ASC)
    if asc is None:
        raise ValueError("Ascendant not found in the chart.")
    
    if chart.date is None:
         raise ValueError("Birth date not found in the chart.")

    target_date = date if date else chart.date

    # Calculate all dasha periods starting from birth
    all_periods = calculate_chara_dasha_periods(chart.date.to_datetime(), asc.lon)
    
    # Find the specific dasha for the target date
    current_dasha_info = get_current_chara_dasha(all_periods, target_date.to_datetime())

    return current_dasha_info

def get_mahadasha(chart: Chart, date: Optional[Datetime] = None) -> Optional[Dict[str, Any]]:
    """
    Get the current Chara Mahadasha (major period) for a chart at a specific date.

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
    Get the current Chara Antardasha (sub-period) for a chart at a specific date.

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

def get_dasha_sign(dasha_info: Optional[Dict[str, Any]]) -> Optional[str]:
    """
    Get the ruling sign from a Dasha information dictionary.

    Args:
        dasha_info (dict or None): The Dasha dictionary containing a 'sign' key.

    Returns:
        str or None: The sign of the Dasha, or None if input is invalid.
    """
    return dasha_info.get('sign') if isinstance(dasha_info, dict) else None

def get_antardasha_sign(antardasha_info: Optional[Dict[str, Any]]) -> Optional[str]:
    """
    Get the ruling sign from an Antardasha information dictionary.

    Args:
        antardasha_info (dict or None): The Antardasha dictionary containing a 'sign' key.

    Returns:
        str or None: The sign of the Antardasha, or None if input is invalid.
    """
    return get_dasha_sign(antardasha_info)

def get_dasha(chart: Chart, date: Optional[Datetime] = None) -> Optional[Dict[str, Any]]:
    """
    Alias for get_mahadasha.
    Get the current Chara Mahadasha (major period) for a chart at a specific date.

    Args:
        chart (Chart): The chart object containing birth details.
        date (Datetime, optional): The date to calculate for. 
                                   Defaults to the chart's date if None.

    Returns:
        dict or None: Dictionary with current Mahadasha information, or None if not found.
    """
    return get_mahadasha(chart, date)
