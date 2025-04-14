"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Vimshottari Dasha calculations for Vedic astrology.
    It includes functions to calculate main periods (Mahadashas), sub-periods
    (Antardashas), and sub-sub-periods (Pratyantardashas).
"""

from datetime import datetime, timedelta
from astrovedic import const
from astrovedic.datetime import Datetime
from astrovedic.vedic.nakshatras import (
    get_nakshatra, VIMSHOTTARI_PERIODS, TOTAL_VIMSHOTTARI_YEARS,
    NAKSHATRA_SPAN
)

# Vimshottari Dasha planet sequence
VIMSHOTTARI_SEQUENCE = [
    const.KETU, const.VENUS, const.SUN, const.MOON, const.MARS,
    const.RAHU, const.JUPITER, const.SATURN, const.MERCURY
]

def calculate_dasha_balance(moon_longitude):
    """
    Calculate the balance of the current Mahadasha at birth

    Args:
        moon_longitude (float): The Moon's longitude in degrees (0-360)

    Returns:
        float: The balance of the current Mahadasha in years
    """
    # Get nakshatra information
    nakshatra_info = get_nakshatra(moon_longitude)
    nakshatra_lord = nakshatra_info['lord']

    # Calculate position within nakshatra (0-13.33333 degrees)
    pos_in_nakshatra = moon_longitude % NAKSHATRA_SPAN

    # Calculate the percentage of nakshatra traversed
    percentage_traversed = pos_in_nakshatra / NAKSHATRA_SPAN

    # Calculate the balance of the current Mahadasha
    years_of_dasha = VIMSHOTTARI_PERIODS[nakshatra_lord]
    balance = years_of_dasha * (1 - percentage_traversed)

    return balance

def get_mahadasha_sequence(moon_longitude):
    """
    Get the sequence of Mahadashas starting from birth

    Args:
        moon_longitude (float): The Moon's longitude in degrees (0-360)

    Returns:
        list: List of dictionaries with Mahadasha information
    """
    # Get nakshatra information
    nakshatra_info = get_nakshatra(moon_longitude)
    nakshatra_lord = nakshatra_info['lord']

    # Calculate the balance of the current Mahadasha
    balance = calculate_dasha_balance(moon_longitude)

    # Find the starting index in the Vimshottari sequence
    start_idx = VIMSHOTTARI_SEQUENCE.index(nakshatra_lord)

    # Create the sequence of Mahadashas
    mahadasha_sequence = []

    # Add the current Mahadasha with its balance
    mahadasha_sequence.append({
        'planet': nakshatra_lord,
        'years': balance
    })

    # Add the remaining Mahadashas in sequence
    for i in range(1, 9):
        idx = (start_idx + i) % 9
        planet = VIMSHOTTARI_SEQUENCE[idx]
        mahadasha_sequence.append({
            'planet': planet,
            'years': VIMSHOTTARI_PERIODS[planet]
        })

    return mahadasha_sequence

def get_antardasha_sequence(mahadasha_planet, mahadasha_years):
    """
    Get the sequence of Antardashas (sub-periods) for a given Mahadasha

    Args:
        mahadasha_planet (str): The planet ruling the Mahadasha
        mahadasha_years (float): The duration of the Mahadasha in years

    Returns:
        list: List of dictionaries with Antardasha information
    """
    # Find the starting index in the Vimshottari sequence
    start_idx = VIMSHOTTARI_SEQUENCE.index(mahadasha_planet)

    # Create the sequence of Antardashas
    antardasha_sequence = []

    # Add all Antardashas in sequence
    for i in range(9):
        idx = (start_idx + i) % 9
        planet = VIMSHOTTARI_SEQUENCE[idx]

        # Calculate the duration of the Antardasha
        years = (VIMSHOTTARI_PERIODS[planet] / TOTAL_VIMSHOTTARI_YEARS) * mahadasha_years

        antardasha_sequence.append({
            'planet': planet,
            'years': years
        })

    return antardasha_sequence

def get_pratyantardasha_sequence(antardasha_planet, antardasha_years):
    """
    Get the sequence of Pratyantardashas (sub-sub-periods) for a given Antardasha

    Args:
        antardasha_planet (str): The planet ruling the Antardasha
        antardasha_years (float): The duration of the Antardasha in years

    Returns:
        list: List of dictionaries with Pratyantardasha information
    """
    # Find the starting index in the Vimshottari sequence
    start_idx = VIMSHOTTARI_SEQUENCE.index(antardasha_planet)

    # Create the sequence of Pratyantardashas
    pratyantardasha_sequence = []

    # Add all Pratyantardashas in sequence
    for i in range(9):
        idx = (start_idx + i) % 9
        planet = VIMSHOTTARI_SEQUENCE[idx]

        # Calculate the duration of the Pratyantardasha
        years = (VIMSHOTTARI_PERIODS[planet] / TOTAL_VIMSHOTTARI_YEARS) * antardasha_years

        pratyantardasha_sequence.append({
            'planet': planet,
            'years': years
        })

    return pratyantardasha_sequence

def years_to_days(years):
    """
    Convert years to days

    Args:
        years (float): Number of years

    Returns:
        float: Number of days
    """
    return years * 365.25

def add_years_to_date(date, years):
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

def calculate_dasha_periods(birth_date, moon_longitude):
    """
    Calculate all Vimshottari Dasha periods from birth

    Args:
        birth_date (Datetime): The birth date
        moon_longitude (float): The Moon's longitude in degrees (0-360)

    Returns:
        dict: Dictionary with Mahadasha, Antardasha, and Pratyantardasha information
    """
    # Convert flatlib Datetime to Python datetime
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

    # Get the Mahadasha sequence
    mahadasha_sequence = get_mahadasha_sequence(moon_longitude)

    # Calculate start and end dates for each Mahadasha
    current_date = birth_dt
    mahadashas = []

    for mahadasha in mahadasha_sequence:
        planet = mahadasha['planet']
        years = mahadasha['years']

        start_date = current_date
        end_date = add_years_to_date(start_date, years)

        # Get Antardashas for this Mahadasha
        antardasha_sequence = get_antardasha_sequence(planet, years)
        antardashas = []

        # Calculate start and end dates for each Antardasha
        antardasha_date = start_date

        for antardasha in antardasha_sequence:
            ad_planet = antardasha['planet']
            ad_years = antardasha['years']

            ad_start_date = antardasha_date
            ad_end_date = add_years_to_date(ad_start_date, ad_years)

            # Get Pratyantardashas for this Antardasha
            pratyantardasha_sequence = get_pratyantardasha_sequence(ad_planet, ad_years)
            pratyantardashas = []

            # Calculate start and end dates for each Pratyantardasha
            pratyantardasha_date = ad_start_date

            for pratyantardasha in pratyantardasha_sequence:
                pad_planet = pratyantardasha['planet']
                pad_years = pratyantardasha['years']

                pad_start_date = pratyantardasha_date
                pad_end_date = add_years_to_date(pad_start_date, pad_years)

                pratyantardashas.append({
                    'planet': pad_planet,
                    'start_date': pad_start_date,
                    'end_date': pad_end_date,
                    'years': pad_years
                })

                pratyantardasha_date = pad_end_date

            antardashas.append({
                'planet': ad_planet,
                'start_date': ad_start_date,
                'end_date': ad_end_date,
                'years': ad_years,
                'pratyantardashas': pratyantardashas
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

def get_current_dasha(dasha_periods, date=None):
    """
    Get the current operating Dasha period

    Args:
        dasha_periods (dict): Dictionary with Dasha periods
        date (datetime, optional): The date to check. Defaults to current date.

    Returns:
        dict: Dictionary with current Mahadasha, Antardasha, and Pratyantardasha
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
            'mahadasha': current_mahadasha['planet'],
            'antardasha': None,
            'pratyantardasha': None
        }

    # Find the current Pratyantardasha
    current_pratyantardasha = None
    for pratyantardasha in current_antardasha['pratyantardashas']:
        if pratyantardasha['start_date'] <= date < pratyantardasha['end_date']:
            current_pratyantardasha = pratyantardasha
            break

    if not current_pratyantardasha:
        return {
            'mahadasha': current_mahadasha['planet'],
            'antardasha': current_antardasha['planet'],
            'pratyantardasha': None
        }

    return {
        'mahadasha': current_mahadasha['planet'],
        'antardasha': current_antardasha['planet'],
        'pratyantardasha': current_pratyantardasha['planet'],
        'mahadasha_start': current_mahadasha['start_date'],
        'mahadasha_end': current_mahadasha['end_date'],
        'antardasha_start': current_antardasha['start_date'],
        'antardasha_end': current_antardasha['end_date'],
        'pratyantardasha_start': current_pratyantardasha['start_date'],
        'pratyantardasha_end': current_pratyantardasha['end_date']
    }

def format_dasha_period(dasha_period):
    """
    Format a Dasha period as a string

    Args:
        dasha_period (dict): Dictionary with Dasha period information

    Returns:
        str: Formatted string
    """
    if not dasha_period:
        return "No Dasha period found"

    mahadasha = dasha_period['mahadasha']
    antardasha = dasha_period.get('antardasha')
    pratyantardasha = dasha_period.get('pratyantardasha')

    if antardasha and pratyantardasha:
        return f"{mahadasha}-{antardasha}-{pratyantardasha}"
    elif antardasha:
        return f"{mahadasha}-{antardasha}"
    else:
        return mahadasha

def analyze_dasha_strength(chart, dasha_period):
    """
    Analyze the strength of the current Dasha lords

    Args:
        chart (Chart): The birth chart
        dasha_period (dict): Dictionary with current Dasha period

    Returns:
        dict: Dictionary with strength analysis
    """
    # This is a placeholder for more advanced analysis
    # In a real implementation, this would analyze the strength of the
    # Dasha lords based on their positions in the birth chart

    mahadasha = dasha_period['mahadasha']
    antardasha = dasha_period.get('antardasha')
    pratyantardasha = dasha_period.get('pratyantardasha')

    # Get the planets from the chart
    mahadasha_planet = chart.getObject(mahadasha) if mahadasha in chart.objects else None
    antardasha_planet = chart.getObject(antardasha) if antardasha in chart.objects else None
    pratyantardasha_planet = chart.getObject(pratyantardasha) if pratyantardasha in chart.objects else None

    # Simple analysis based on house position
    analysis = {}

    if mahadasha_planet:
        house = chart.houses.getHouseByLon(mahadasha_planet.lon)
        house_num = house.num() if house else 0
        analysis['mahadasha'] = {
            'planet': mahadasha,
            'house': house_num,
            'sign': mahadasha_planet.sign,
            'retrograde': mahadasha_planet.movement == const.RETROGRADE
        }

    if antardasha_planet:
        house = chart.houses.getHouseByLon(antardasha_planet.lon)
        house_num = house.num() if house else 0
        analysis['antardasha'] = {
            'planet': antardasha,
            'house': house_num,
            'sign': antardasha_planet.sign,
            'retrograde': antardasha_planet.movement == const.RETROGRADE
        }

    if pratyantardasha_planet:
        house = chart.houses.getHouseByLon(pratyantardasha_planet.lon)
        house_num = house.num() if house else 0
        analysis['pratyantardasha'] = {
            'planet': pratyantardasha,
            'house': house_num,
            'sign': pratyantardasha_planet.sign,
            'retrograde': pratyantardasha_planet.movement == const.RETROGRADE
        }

    return analysis

def is_dasha_sandhi(dasha_periods, date=None, threshold_days=15):
    """
    Check if the current date is in a Dasha Sandhi (junction point)

    Args:
        dasha_periods (dict): Dictionary with Dasha periods
        date (datetime, optional): The date to check. Defaults to current date.
        threshold_days (int, optional): Number of days to consider as junction. Defaults to 15.

    Returns:
        bool: True if in Dasha Sandhi, False otherwise
    """
    if date is None:
        date = datetime.now()

    # Check all Mahadasha end dates
    for mahadasha in dasha_periods['mahadashas']:
        if abs((mahadasha['end_date'] - date).days) <= threshold_days:
            return True

        # Check all Antardasha end dates
        for antardasha in mahadasha['antardashas']:
            if abs((antardasha['end_date'] - date).days) <= threshold_days:
                return True

    return False
