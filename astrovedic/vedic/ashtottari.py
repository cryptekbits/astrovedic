"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Ashtottari Dasha calculations for Vedic astrology.
    Ashtottari Dasha is a 108-year cycle based on the Moon's Nakshatra.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.vedic.nakshatras import get_nakshatra
from datetime import datetime, timedelta
from typing import Dict, Optional, Any, List, Tuple

# Ashtottari Dasha periods (in years)
ASHTOTTARI_PERIODS = {
    const.SUN: 6,
    const.MOON: 15,
    const.MARS: 8,
    const.MERCURY: 17,
    const.SATURN: 10,
    const.JUPITER: 19,
    const.RAHU: 12,
    const.VENUS: 21
}

# Total years in Ashtottari Dasha cycle
TOTAL_ASHTOTTARI_YEARS = sum(ASHTOTTARI_PERIODS.values())  # 108 years

# Ashtottari Dasha sequence
ASHTOTTARI_SEQUENCE = [
    const.SUN, const.MOON, const.MARS, const.MERCURY,
    const.SATURN, const.JUPITER, const.RAHU, const.VENUS
]

# Nakshatra to Ashtottari starting planet mapping (1-based nakshatra index to planet)
NAKSHATRA_TO_ASHTOTTARI = {
    1: const.VENUS,    # Ashwini
    2: const.SUN,      # Bharani
    3: const.MOON,     # Krittika
    4: const.MARS,     # Rohini
    5: const.MERCURY,  # Mrigashira
    6: const.SATURN,   # Ardra
    7: const.JUPITER,  # Punarvasu
    8: const.RAHU,     # Pushya
    9: const.VENUS,    # Ashlesha
    10: const.SUN,     # Magha
    11: const.MOON,    # Purva Phalguni
    12: const.MARS,    # Uttara Phalguni
    13: const.MERCURY, # Hasta
    14: const.SATURN,  # Chitra
    15: const.JUPITER, # Swati
    16: const.RAHU,    # Vishakha
    17: const.VENUS,   # Anuradha
    18: const.SUN,     # Jyeshtha
    19: const.MOON,    # Mula
    20: const.MARS,    # Purva Ashadha
    21: const.MERCURY, # Uttara Ashadha
    22: const.SATURN,  # Shravana
    23: const.JUPITER, # Dhanishta
    24: const.RAHU,    # Shatabhisha
    25: const.VENUS,   # Purva Bhadrapada
    26: const.SUN,     # Uttara Bhadrapada
    27: const.MOON     # Revati
}

def calculate_ashtottari_dasha_balance(moon_longitude: float) -> float:
    """
    Calculate the balance of the current Ashtottari Dasha at birth

    Args:
        moon_longitude (float): The Moon's longitude in degrees (0-360)

    Returns:
        float: The balance of the current Ashtottari Dasha in years
    """
    # Get nakshatra information
    nakshatra_info = get_nakshatra(moon_longitude)
    nakshatra_index = nakshatra_info['index'] + 1  # Convert to 1-based index
    
    # Get the Ashtottari planet for this nakshatra
    ashtottari_planet = NAKSHATRA_TO_ASHTOTTARI[nakshatra_index]
    
    # Calculate position within nakshatra (0-13.33333 degrees)
    pos_in_nakshatra = nakshatra_info['percentage'] / 100
    
    # Calculate the balance of the current Ashtottari Dasha
    years_of_dasha = ASHTOTTARI_PERIODS[ashtottari_planet]
    balance = years_of_dasha * (1 - pos_in_nakshatra)
    
    return balance

def get_ashtottari_sequence(moon_longitude: float) -> List[Dict[str, Any]]:
    """
    Get the sequence of Ashtottari Dashas starting from birth

    Args:
        moon_longitude (float): The Moon's longitude in degrees (0-360)

    Returns:
        list: List of dictionaries with Ashtottari Dasha information
    """
    # Get nakshatra information
    nakshatra_info = get_nakshatra(moon_longitude)
    nakshatra_index = nakshatra_info['index'] + 1  # Convert to 1-based index
    
    # Get the Ashtottari planet for this nakshatra
    ashtottari_planet = NAKSHATRA_TO_ASHTOTTARI[nakshatra_index]
    
    # Calculate the balance of the current Ashtottari Dasha
    balance = calculate_ashtottari_dasha_balance(moon_longitude)
    
    # Find the starting index in the Ashtottari sequence
    start_idx = ASHTOTTARI_SEQUENCE.index(ashtottari_planet)
    
    # Create the sequence of Ashtottari Dashas
    ashtottari_sequence = []
    
    # Add the current Ashtottari Dasha with its balance
    ashtottari_sequence.append({
        'planet': ashtottari_planet,
        'years': balance
    })
    
    # Add the remaining Ashtottari Dashas in sequence
    for i in range(1, 8):
        idx = (start_idx + i) % 8
        planet = ASHTOTTARI_SEQUENCE[idx]
        ashtottari_sequence.append({
            'planet': planet,
            'years': ASHTOTTARI_PERIODS[planet]
        })
    
    return ashtottari_sequence

def get_ashtottari_antardasha_sequence(mahadasha_planet: str, mahadasha_years: float) -> List[Dict[str, Any]]:
    """
    Get the sequence of Ashtottari Antardashas (sub-periods) for a given Mahadasha

    Args:
        mahadasha_planet (str): The planet ruling the Mahadasha
        mahadasha_years (float): The duration of the Mahadasha in years

    Returns:
        list: List of dictionaries with Antardasha information
    """
    # Find the starting index in the Ashtottari sequence
    start_idx = ASHTOTTARI_SEQUENCE.index(mahadasha_planet)
    
    # Create the sequence of Antardashas
    antardasha_sequence = []
    
    # Add all Antardashas in sequence
    for i in range(8):
        idx = (start_idx + i) % 8
        planet = ASHTOTTARI_SEQUENCE[idx]
        
        # Calculate the duration of the Antardasha
        years = (ASHTOTTARI_PERIODS[planet] / TOTAL_ASHTOTTARI_YEARS) * mahadasha_years
        
        antardasha_sequence.append({
            'planet': planet,
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

def calculate_ashtottari_dasha_periods(birth_date: datetime, moon_longitude: float) -> Dict[str, Any]:
    """
    Calculate all Ashtottari Dasha periods from birth

    Args:
        birth_date (datetime): The birth date
        moon_longitude (float): The Moon's longitude in degrees (0-360)

    Returns:
        dict: Dictionary with Mahadasha and Antardasha information
    """
    # Convert flatlib Datetime to Python datetime if needed
    if isinstance(birth_date, Datetime):
        birth_dt = birth_date.to_datetime()
    else:
        birth_dt = birth_date
    
    # Get the Ashtottari Dasha sequence
    ashtottari_sequence = get_ashtottari_sequence(moon_longitude)
    
    # Calculate start and end dates for each Mahadasha
    current_date = birth_dt
    mahadashas = []
    
    for mahadasha in ashtottari_sequence:
        planet = mahadasha['planet']
        years = mahadasha['years']
        
        start_date = current_date
        end_date = add_years_to_date(start_date, years)
        
        # Get Antardashas for this Mahadasha
        antardasha_sequence = get_ashtottari_antardasha_sequence(planet, years)
        antardashas = []
        
        # Calculate start and end dates for each Antardasha
        antardasha_date = start_date
        
        for antardasha in antardasha_sequence:
            ad_planet = antardasha['planet']
            ad_years = antardasha['years']
            
            ad_start_date = antardasha_date
            ad_end_date = add_years_to_date(ad_start_date, ad_years)
            
            antardashas.append({
                'planet': ad_planet,
                'start_date': ad_start_date,
                'end_date': ad_end_date,
                'years': ad_years
            })
            
            antardasha_date = ad_end_date
        
        mahadashas.append({
            'planet': planet,
            'start_date': start_date,
            'end_date': end_date,
            'years': years,
            'antardashas': antardashas
        })
        
        current_date = end_date
    
    return {
        'mahadashas': mahadashas,
        'birth_date': birth_dt,
        'moon_longitude': moon_longitude
    }

def get_current_ashtottari_dasha(dasha_periods: Dict[str, Any], date: Optional[datetime] = None) -> Optional[Dict[str, Any]]:
    """
    Get the current operating Ashtottari Dasha period

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
    Get the balance of the first Ashtottari Dasha (major period) at birth for a chart.

    Args:
        chart (Chart): The chart object containing birth details.

    Returns:
        float: The balance of the first Ashtottari Dasha in years.

    Raises:
        ValueError: If the Moon object is not found in the chart.
    """
    moon = chart.getObject(const.MOON)
    if moon is None:
        raise ValueError("Moon object not found in the chart.")
    
    return calculate_ashtottari_dasha_balance(moon.lon)

def get_current_dasha(chart: Chart, date: Optional[Datetime] = None) -> Optional[Dict[str, Any]]:
    """
    Get the current operating Ashtottari Dasha for a chart at a specific date.

    Args:
        chart (Chart): The chart object containing birth details.
        date (Datetime, optional): The date to calculate for. 
                                   Defaults to the chart's date if None.

    Returns:
        dict or None: A dictionary containing the current 'mahadasha' and
                      'antardasha' lords and their periods, or None if calculation fails.

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
    all_periods = calculate_ashtottari_dasha_periods(chart.date.to_datetime(), moon.lon)
    
    # Find the specific dasha for the target date
    current_dasha_info = get_current_ashtottari_dasha(all_periods, target_date.to_datetime())

    return current_dasha_info

def get_mahadasha(chart: Chart, date: Optional[Datetime] = None) -> Optional[Dict[str, Any]]:
    """
    Get the current Ashtottari Mahadasha (major period) for a chart at a specific date.

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
    Get the current Ashtottari Antardasha (sub-period) for a chart at a specific date.

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

def get_dasha_lord(dasha_info: Optional[Dict[str, Any]]) -> Optional[str]:
    """
    Get the ruling planet (lord) from a Dasha information dictionary.

    Args:
        dasha_info (dict or None): The Dasha dictionary containing a 'planet' key.

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

def get_dasha(chart: Chart, date: Optional[Datetime] = None) -> Optional[Dict[str, Any]]:
    """
    Alias for get_mahadasha.
    Get the current Ashtottari Mahadasha (major period) for a chart at a specific date.

    Args:
        chart (Chart): The chart object containing birth details.
        date (Datetime, optional): The date to calculate for. 
                                   Defaults to the chart's date if None.

    Returns:
        dict or None: Dictionary with current Mahadasha information, or None if not found.
    """
    return get_mahadasha(chart, date)
