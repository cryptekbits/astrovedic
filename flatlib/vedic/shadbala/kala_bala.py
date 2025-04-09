"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Kala Bala (temporal strength) calculations
    for Shadbala in Vedic astrology.
"""

from flatlib import const
from flatlib import angle
from flatlib.datetime import Datetime
from datetime import datetime


def calculate_kala_bala(chart, planet_id):
    """
    Calculate Kala Bala (temporal strength) for a planet
    
    Kala Bala includes:
    1. Nathonnatha Bala (day/night strength)
    2. Paksha Bala (lunar phase strength)
    3. Tribhaga Bala (three-part day/night strength)
    4. Abda Bala (yearly strength)
    5. Masa Bala (monthly strength)
    6. Vara Bala (weekday strength)
    7. Hora Bala (hourly strength)
    8. Ayana Bala (solstice strength)
    9. Yuddha Bala (planetary war strength)
    
    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet to analyze
    
    Returns:
        dict: Dictionary with Kala Bala information
    """
    # Get the planet from the chart
    planet = chart.getObject(planet_id)
    
    # Calculate each component of Kala Bala
    nathonnatha_bala = calculate_nathonnatha_bala(chart, planet_id)
    paksha_bala = calculate_paksha_bala(chart, planet_id)
    tribhaga_bala = calculate_tribhaga_bala(chart, planet_id)
    abda_bala = calculate_abda_bala(chart, planet_id)
    masa_bala = calculate_masa_bala(chart, planet_id)
    vara_bala = calculate_vara_bala(chart, planet_id)
    hora_bala = calculate_hora_bala(chart, planet_id)
    ayana_bala = calculate_ayana_bala(chart, planet_id)
    yuddha_bala = calculate_yuddha_bala(chart, planet_id)
    
    # Calculate total Kala Bala
    total = (nathonnatha_bala['value'] + paksha_bala['value'] + 
             tribhaga_bala['value'] + abda_bala['value'] + 
             masa_bala['value'] + vara_bala['value'] + 
             hora_bala['value'] + ayana_bala['value'] + 
             yuddha_bala['value'])
    
    return {
        'planet': planet_id,
        'nathonnatha_bala': nathonnatha_bala,
        'paksha_bala': paksha_bala,
        'tribhaga_bala': tribhaga_bala,
        'abda_bala': abda_bala,
        'masa_bala': masa_bala,
        'vara_bala': vara_bala,
        'hora_bala': hora_bala,
        'ayana_bala': ayana_bala,
        'yuddha_bala': yuddha_bala,
        'total': total
    }


def calculate_nathonnatha_bala(chart, planet_id):
    """
    Calculate Nathonnatha Bala (day/night strength) for a planet
    
    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet
    
    Returns:
        dict: Dictionary with Nathonnatha Bala information
    """
    # Determine if the chart is diurnal or nocturnal
    is_diurnal = chart.isDiurnal()
    
    # Diurnal planets (Sun, Jupiter, Saturn)
    diurnal_planets = [const.SUN, const.JUPITER, const.SATURN]
    
    # Nocturnal planets (Moon, Venus, Mars)
    nocturnal_planets = [const.MOON, const.VENUS, const.MARS]
    
    # Mercury is both diurnal and nocturnal
    
    # Maximum value (in Virupas)
    max_value = 60.0
    
    # Calculate Nathonnatha Bala
    if planet_id in diurnal_planets and is_diurnal:
        value = max_value
        description = 'Diurnal planet in day'
    elif planet_id in nocturnal_planets and not is_diurnal:
        value = max_value
        description = 'Nocturnal planet in night'
    elif planet_id == const.MERCURY:
        value = max_value
        description = 'Mercury is both diurnal and nocturnal'
    elif planet_id in [const.RAHU, const.KETU]:
        value = max_value / 2.0
        description = 'Nodes have half strength'
    else:
        value = 0.0
        description = 'Planet in unfavorable time'
    
    return {'value': value, 'description': description}


def calculate_paksha_bala(chart, planet_id):
    """
    Calculate Paksha Bala (lunar phase strength) for a planet
    
    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet
    
    Returns:
        dict: Dictionary with Paksha Bala information
    """
    # Get the Sun and Moon
    sun = chart.getObject(const.SUN)
    moon = chart.getObject(const.MOON)
    
    # Calculate the distance from Sun to Moon
    sun_moon_distance = angle.distance(sun.lon, moon.lon)
    
    # Determine if it's Shukla Paksha (waxing) or Krishna Paksha (waning)
    is_shukla_paksha = sun_moon_distance <= 180
    
    # Maximum value (in Virupas)
    max_value = 60.0
    
    # Calculate the phase of the Moon (0-1)
    if is_shukla_paksha:
        phase = sun_moon_distance / 180.0
    else:
        phase = 1.0 - ((sun_moon_distance - 180.0) / 180.0)
    
    # Benefic planets (Jupiter, Venus, Mercury, Moon)
    benefic_planets = [const.JUPITER, const.VENUS, const.MERCURY, const.MOON]
    
    # Malefic planets (Sun, Mars, Saturn, Rahu, Ketu)
    malefic_planets = [const.SUN, const.MARS, const.SATURN, const.RAHU, const.KETU]
    
    # Calculate Paksha Bala
    if planet_id in benefic_planets:
        if is_shukla_paksha:
            # Benefics gain strength in Shukla Paksha
            value = max_value * phase
            description = 'Benefic in Shukla Paksha'
        else:
            # Benefics lose strength in Krishna Paksha
            value = max_value * phase
            description = 'Benefic in Krishna Paksha'
    elif planet_id in malefic_planets:
        if is_shukla_paksha:
            # Malefics lose strength in Shukla Paksha
            value = max_value * (1.0 - phase)
            description = 'Malefic in Shukla Paksha'
        else:
            # Malefics gain strength in Krishna Paksha
            value = max_value * (1.0 - phase)
            description = 'Malefic in Krishna Paksha'
    else:
        value = max_value / 2.0
        description = 'Neutral'
    
    return {'value': value, 'description': description}


def calculate_tribhaga_bala(chart, planet_id):
    """
    Calculate Tribhaga Bala (three-part day/night strength) for a planet
    
    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet
    
    Returns:
        dict: Dictionary with Tribhaga Bala information
    """
    # For simplicity, we'll use a fixed value for now
    # In a full implementation, we would calculate the exact part of the day/night
    
    # Maximum value (in Virupas)
    max_value = 60.0
    
    # Fixed value for now
    value = max_value / 2.0
    description = 'Fixed value for Tribhaga Bala'
    
    return {'value': value, 'description': description}


def calculate_abda_bala(chart, planet_id):
    """
    Calculate Abda Bala (yearly strength) for a planet
    
    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet
    
    Returns:
        dict: Dictionary with Abda Bala information
    """
    # Get the year of the chart
    year = int(chart.date.date.split('/')[0])
    
    # Each planet rules a specific year in a 7-year cycle
    year_rulers = {
        0: const.SUN,     # Sun rules years divisible by 7
        1: const.VENUS,   # Venus rules years with remainder 1
        2: const.MARS,    # Mars rules years with remainder 2
        3: const.MERCURY, # Mercury rules years with remainder 3
        4: const.JUPITER, # Jupiter rules years with remainder 4
        5: const.SATURN,  # Saturn rules years with remainder 5
        6: const.MOON     # Moon rules years with remainder 6
    }
    
    # Maximum value (in Virupas)
    max_value = 15.0
    
    # Calculate the year ruler
    year_ruler = year_rulers[year % 7]
    
    # Calculate Abda Bala
    if planet_id == year_ruler:
        value = max_value
        description = 'Ruler of the year'
    else:
        value = 0.0
        description = 'Not ruler of the year'
    
    return {'value': value, 'description': description}


def calculate_masa_bala(chart, planet_id):
    """
    Calculate Masa Bala (monthly strength) for a planet
    
    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet
    
    Returns:
        dict: Dictionary with Masa Bala information
    """
    # Get the month of the chart
    month = int(chart.date.date.split('/')[1])
    
    # Each planet rules a specific month in a 12-month cycle
    month_rulers = {
        1: const.SUN,     # Sun rules January
        2: const.VENUS,   # Venus rules February
        3: const.MARS,    # Mars rules March
        4: const.MERCURY, # Mercury rules April
        5: const.JUPITER, # Jupiter rules May
        6: const.SATURN,  # Saturn rules June
        7: const.MOON,    # Moon rules July
        8: const.SUN,     # Sun rules August
        9: const.VENUS,   # Venus rules September
        10: const.MARS,   # Mars rules October
        11: const.MERCURY, # Mercury rules November
        12: const.JUPITER  # Jupiter rules December
    }
    
    # Maximum value (in Virupas)
    max_value = 30.0
    
    # Calculate the month ruler
    month_ruler = month_rulers[month]
    
    # Calculate Masa Bala
    if planet_id == month_ruler:
        value = max_value
        description = 'Ruler of the month'
    else:
        value = 0.0
        description = 'Not ruler of the month'
    
    return {'value': value, 'description': description}


def calculate_vara_bala(chart, planet_id):
    """
    Calculate Vara Bala (weekday strength) for a planet
    
    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet
    
    Returns:
        dict: Dictionary with Vara Bala information
    """
    # Get the date from the chart
    date_str = chart.date.date
    time_str = chart.date.time
    utc_offset = chart.date.utcoffset
    
    # Convert to Python datetime
    dt = datetime.strptime(f"{date_str} {time_str}", "%Y/%m/%d %H:%M")
    
    # Get the day of the week (0 = Monday, 6 = Sunday)
    day_of_week = dt.weekday()
    
    # Adjust to traditional week (0 = Sunday, 6 = Saturday)
    day_of_week = (day_of_week + 1) % 7
    
    # Each planet rules a specific day of the week
    day_rulers = {
        0: const.SUN,     # Sun rules Sunday
        1: const.MOON,    # Moon rules Monday
        2: const.MARS,    # Mars rules Tuesday
        3: const.MERCURY, # Mercury rules Wednesday
        4: const.JUPITER, # Jupiter rules Thursday
        5: const.VENUS,   # Venus rules Friday
        6: const.SATURN   # Saturn rules Saturday
    }
    
    # Maximum value (in Virupas)
    max_value = 45.0
    
    # Calculate the day ruler
    day_ruler = day_rulers[day_of_week]
    
    # Calculate Vara Bala
    if planet_id == day_ruler:
        value = max_value
        description = 'Ruler of the day'
    else:
        value = 0.0
        description = 'Not ruler of the day'
    
    return {'value': value, 'description': description}


def calculate_hora_bala(chart, planet_id):
    """
    Calculate Hora Bala (hourly strength) for a planet
    
    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet
    
    Returns:
        dict: Dictionary with Hora Bala information
    """
    # Get the date and time from the chart
    date_str = chart.date.date
    time_str = chart.date.time
    
    # Convert to Python datetime
    dt = datetime.strptime(f"{date_str} {time_str}", "%Y/%m/%d %H:%M")
    
    # Get the hour of the day (0-23)
    hour = dt.hour
    
    # Determine if it's day or night
    is_diurnal = chart.isDiurnal()
    
    # Each planet rules a specific hour in a 7-hour cycle
    # The order is different for day and night
    if is_diurnal:
        hour_rulers = {
            0: const.SUN,     # Sun rules the 1st hour of the day
            1: const.VENUS,   # Venus rules the 2nd hour of the day
            2: const.MERCURY, # Mercury rules the 3rd hour of the day
            3: const.MOON,    # Moon rules the 4th hour of the day
            4: const.SATURN,  # Saturn rules the 5th hour of the day
            5: const.JUPITER, # Jupiter rules the 6th hour of the day
            6: const.MARS     # Mars rules the 7th hour of the day
        }
    else:
        hour_rulers = {
            0: const.MOON,    # Moon rules the 1st hour of the night
            1: const.SATURN,  # Saturn rules the 2nd hour of the night
            2: const.JUPITER, # Jupiter rules the 3rd hour of the night
            3: const.MARS,    # Mars rules the 4th hour of the night
            4: const.SUN,     # Sun rules the 5th hour of the night
            5: const.VENUS,   # Venus rules the 6th hour of the night
            6: const.MERCURY  # Mercury rules the 7th hour of the night
        }
    
    # Maximum value (in Virupas)
    max_value = 60.0
    
    # Calculate the hour ruler
    hour_ruler = hour_rulers[hour % 7]
    
    # Calculate Hora Bala
    if planet_id == hour_ruler:
        value = max_value
        description = 'Ruler of the hour'
    else:
        value = 0.0
        description = 'Not ruler of the hour'
    
    return {'value': value, 'description': description}


def calculate_ayana_bala(chart, planet_id):
    """
    Calculate Ayana Bala (solstice strength) for a planet
    
    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet
    
    Returns:
        dict: Dictionary with Ayana Bala information
    """
    # Get the Sun's longitude
    sun = chart.getObject(const.SUN)
    sun_lon = sun.lon
    
    # Determine if it's Uttarayana (Sun in Capricorn to Gemini) or
    # Dakshinayana (Sun in Cancer to Sagittarius)
    is_uttarayana = (sun_lon >= 270 or sun_lon < 90)
    
    # Maximum value (in Virupas)
    max_value = 30.0
    
    # Benefic planets (Jupiter, Venus, Mercury, Moon)
    benefic_planets = [const.JUPITER, const.VENUS, const.MERCURY, const.MOON]
    
    # Malefic planets (Sun, Mars, Saturn, Rahu, Ketu)
    malefic_planets = [const.SUN, const.MARS, const.SATURN, const.RAHU, const.KETU]
    
    # Calculate Ayana Bala
    if planet_id in benefic_planets:
        if is_uttarayana:
            # Benefics gain strength in Uttarayana
            value = max_value
            description = 'Benefic in Uttarayana'
        else:
            # Benefics lose strength in Dakshinayana
            value = 0.0
            description = 'Benefic in Dakshinayana'
    elif planet_id in malefic_planets:
        if is_uttarayana:
            # Malefics lose strength in Uttarayana
            value = 0.0
            description = 'Malefic in Uttarayana'
        else:
            # Malefics gain strength in Dakshinayana
            value = max_value
            description = 'Malefic in Dakshinayana'
    else:
        value = max_value / 2.0
        description = 'Neutral'
    
    return {'value': value, 'description': description}


def calculate_yuddha_bala(chart, planet_id):
    """
    Calculate Yuddha Bala (planetary war strength) for a planet
    
    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet
    
    Returns:
        dict: Dictionary with Yuddha Bala information
    """
    # Get the planet from the chart
    planet = chart.getObject(planet_id)
    
    # Maximum value (in Virupas)
    max_value = 30.0
    
    # Check if the planet is in a planetary war
    in_war = False
    winner = False
    
    # A planetary war occurs when two planets are within 1 degree of each other
    for other_id in const.LIST_OBJECTS_VEDIC:
        if other_id != planet_id:
            other = chart.getObject(other_id)
            dist = abs(angle.closestdistance(planet.lon, other.lon))
            
            if dist <= 1.0:
                in_war = True
                
                # The winner is determined by brightness, but for simplicity,
                # we'll use a fixed order: Jupiter > Venus > Mercury > Saturn > Mars > Sun > Moon
                planet_order = {
                    const.JUPITER: 1,
                    const.VENUS: 2,
                    const.MERCURY: 3,
                    const.SATURN: 4,
                    const.MARS: 5,
                    const.SUN: 6,
                    const.MOON: 7,
                    const.RAHU: 8,
                    const.KETU: 9
                }
                
                if planet_order.get(planet_id, 10) < planet_order.get(other_id, 10):
                    winner = True
                
                break
    
    # Calculate Yuddha Bala
    if not in_war:
        value = max_value
        description = 'Not in planetary war'
    elif winner:
        value = max_value
        description = 'Winner in planetary war'
    else:
        value = 0.0
        description = 'Loser in planetary war'
    
    return {'value': value, 'description': description}
