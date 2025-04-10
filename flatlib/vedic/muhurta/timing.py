"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements timing calculations for Muhurta (electional astrology)
    in Vedic astrology.
"""

from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from datetime import timedelta, datetime
import math

# Import Panchanga functions
from flatlib.vedic.muhurta.panchanga import get_vara


def get_abhijit_muhurta(date, location):
    """
    Calculate the Abhijit Muhurta (most auspicious time of the day)
    
    Abhijit Muhurta is the 8th muhurta of the day, which occurs during midday.
    It lasts for 48 minutes (2 ghatis) and is considered highly auspicious.
    
    Args:
        date (Datetime): The date
        location (GeoPos): The geographical location
    
    Returns:
        dict: Dictionary with Abhijit Muhurta information
    """
    # Get the sunrise and sunset times
    sunrise = get_sunrise(date, location)
    sunset = get_sunset(date, location)
    
    # Calculate the duration of the day
    day_duration = (sunset.datetime() - sunrise.datetime()).total_seconds()
    
    # Calculate the midday
    midday = sunrise.datetime() + timedelta(seconds=day_duration / 2)
    
    # Calculate the duration of Abhijit Muhurta (48 minutes)
    abhijit_duration = 48 * 60  # in seconds
    
    # Calculate the start and end times of Abhijit Muhurta
    abhijit_start = midday - timedelta(seconds=abhijit_duration / 2)
    abhijit_end = midday + timedelta(seconds=abhijit_duration / 2)
    
    return {
        'start': Datetime.fromDatetime(abhijit_start),
        'end': Datetime.fromDatetime(abhijit_end),
        'duration': abhijit_duration / 60,  # in minutes
        'description': 'Most auspicious time of the day'
    }


def get_brahma_muhurta(date, location):
    """
    Calculate the Brahma Muhurta (auspicious time before sunrise)
    
    Brahma Muhurta is the time approximately 1.5 hours before sunrise,
    lasting for 48 minutes (2 ghatis). It is considered auspicious for
    spiritual practices.
    
    Args:
        date (Datetime): The date
        location (GeoPos): The geographical location
    
    Returns:
        dict: Dictionary with Brahma Muhurta information
    """
    # Get the sunrise time
    sunrise = get_sunrise(date, location)
    
    # Calculate the duration of Brahma Muhurta (48 minutes)
    brahma_duration = 48 * 60  # in seconds
    
    # Calculate the start and end times of Brahma Muhurta
    brahma_end = sunrise.datetime() - timedelta(minutes=24)
    brahma_start = brahma_end - timedelta(seconds=brahma_duration)
    
    return {
        'start': Datetime.fromDatetime(brahma_start),
        'end': Datetime.fromDatetime(brahma_end),
        'duration': brahma_duration / 60,  # in minutes
        'description': 'Auspicious time before sunrise for spiritual practices'
    }


def get_rahu_kala(date, location):
    """
    Calculate the Rahu Kala (inauspicious time of the day)
    
    Rahu Kala is an inauspicious time that occurs during different parts
    of the day depending on the weekday. It lasts for 1.5 hours (3 horas).
    
    Args:
        date (Datetime): The date
        location (GeoPos): The geographical location
    
    Returns:
        dict: Dictionary with Rahu Kala information
    """
    # Get the sunrise and sunset times
    sunrise = get_sunrise(date, location)
    sunset = get_sunset(date, location)
    
    # Calculate the duration of the day
    day_duration = (sunset.datetime() - sunrise.datetime()).total_seconds()
    
    # Calculate the duration of one hora (1/8 of the day)
    hora_duration = day_duration / 8
    
    # Get the weekday
    chart = Chart(date, location, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
    vara = get_vara(chart)
    weekday = vara['num']
    
    # Determine the hora for Rahu Kala based on the weekday
    # Sunday: 8th hora, Monday: 2nd hora, Tuesday: 7th hora,
    # Wednesday: 5th hora, Thursday: 6th hora, Friday: 4th hora, Saturday: 3rd hora
    rahu_horas = {1: 8, 2: 2, 3: 7, 4: 5, 5: 6, 6: 4, 7: 3}
    rahu_hora = rahu_horas.get(weekday, 1)
    
    # Calculate the start and end times of Rahu Kala
    rahu_start = sunrise.datetime() + timedelta(seconds=(rahu_hora - 1) * hora_duration)
    rahu_end = rahu_start + timedelta(seconds=hora_duration * 1.5)
    
    return {
        'start': Datetime.fromDatetime(rahu_start),
        'end': Datetime.fromDatetime(rahu_end),
        'duration': hora_duration * 1.5 / 60,  # in minutes
        'description': 'Inauspicious time ruled by Rahu'
    }


def get_yama_ghantaka(date, location):
    """
    Calculate the Yama Ghantaka (inauspicious time of the day)
    
    Yama Ghantaka is an inauspicious time that occurs during different parts
    of the day depending on the weekday. It lasts for 1.5 hours (3 horas).
    
    Args:
        date (Datetime): The date
        location (GeoPos): The geographical location
    
    Returns:
        dict: Dictionary with Yama Ghantaka information
    """
    # Get the sunrise and sunset times
    sunrise = get_sunrise(date, location)
    sunset = get_sunset(date, location)
    
    # Calculate the duration of the day
    day_duration = (sunset.datetime() - sunrise.datetime()).total_seconds()
    
    # Calculate the duration of one hora (1/8 of the day)
    hora_duration = day_duration / 8
    
    # Get the weekday
    chart = Chart(date, location, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
    vara = get_vara(chart)
    weekday = vara['num']
    
    # Determine the hora for Yama Ghantaka based on the weekday
    # Sunday: 4th hora, Monday: 7th hora, Tuesday: 3rd hora,
    # Wednesday: 6th hora, Thursday: 2nd hora, Friday: 5th hora, Saturday: 8th hora
    yama_horas = {1: 4, 2: 7, 3: 3, 4: 6, 5: 2, 6: 5, 7: 8}
    yama_hora = yama_horas.get(weekday, 1)
    
    # Calculate the start and end times of Yama Ghantaka
    yama_start = sunrise.datetime() + timedelta(seconds=(yama_hora - 1) * hora_duration)
    yama_end = yama_start + timedelta(seconds=hora_duration * 1.5)
    
    return {
        'start': Datetime.fromDatetime(yama_start),
        'end': Datetime.fromDatetime(yama_end),
        'duration': hora_duration * 1.5 / 60,  # in minutes
        'description': 'Inauspicious time ruled by Yama'
    }


def get_gulika_kala(date, location):
    """
    Calculate the Gulika Kala (inauspicious time of the day)
    
    Gulika Kala is an inauspicious time that occurs during different parts
    of the day depending on the weekday. It lasts for 1.5 hours (3 horas).
    
    Args:
        date (Datetime): The date
        location (GeoPos): The geographical location
    
    Returns:
        dict: Dictionary with Gulika Kala information
    """
    # Get the sunrise and sunset times
    sunrise = get_sunrise(date, location)
    sunset = get_sunset(date, location)
    
    # Calculate the duration of the day
    day_duration = (sunset.datetime() - sunrise.datetime()).total_seconds()
    
    # Calculate the duration of one hora (1/8 of the day)
    hora_duration = day_duration / 8
    
    # Get the weekday
    chart = Chart(date, location, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
    vara = get_vara(chart)
    weekday = vara['num']
    
    # Determine the hora for Gulika Kala based on the weekday
    # Sunday: 6th hora, Monday: 5th hora, Tuesday: 4th hora,
    # Wednesday: 3rd hora, Thursday: 2nd hora, Friday: 1st hora, Saturday: 7th hora
    gulika_horas = {1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1, 7: 7}
    gulika_hora = gulika_horas.get(weekday, 1)
    
    # Calculate the start and end times of Gulika Kala
    gulika_start = sunrise.datetime() + timedelta(seconds=(gulika_hora - 1) * hora_duration)
    gulika_end = gulika_start + timedelta(seconds=hora_duration * 1.5)
    
    return {
        'start': Datetime.fromDatetime(gulika_start),
        'end': Datetime.fromDatetime(gulika_end),
        'duration': hora_duration * 1.5 / 60,  # in minutes
        'description': 'Inauspicious time ruled by Gulika'
    }


def get_hora(date, location):
    """
    Calculate the Hora (planetary hour) for a given time
    
    Hora is a division of the day into 24 equal parts, each ruled by a planet.
    The ruling planets follow the Chaldean order: Saturn, Jupiter, Mars, Sun,
    Venus, Mercury, Moon.
    
    Args:
        date (Datetime): The date and time
        location (GeoPos): The geographical location
    
    Returns:
        dict: Dictionary with Hora information
    """
    # Get the sunrise and sunset times
    sunrise = get_sunrise(date, location)
    sunset = get_sunset(date, location)
    
    # Calculate the duration of the day and night
    day_duration = (sunset.datetime() - sunrise.datetime()).total_seconds()
    night_duration = 24 * 60 * 60 - day_duration
    
    # Calculate the duration of one day hora and one night hora
    day_hora_duration = day_duration / 12
    night_hora_duration = night_duration / 12
    
    # Get the weekday
    chart = Chart(date, location, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
    vara = get_vara(chart)
    weekday = vara['num']
    
    # Determine the ruling planet of the first hora of the day based on the weekday
    # Sunday: Sun, Monday: Moon, Tuesday: Mars, Wednesday: Mercury,
    # Thursday: Jupiter, Friday: Venus, Saturday: Saturn
    first_hora_lords = {1: 'Sun', 2: 'Moon', 3: 'Mars', 4: 'Mercury', 5: 'Jupiter', 6: 'Venus', 7: 'Saturn'}
    first_hora_lord = first_hora_lords.get(weekday, 'Sun')
    
    # Chaldean order of planets
    chaldean_order = ['Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon']
    
    # Find the index of the first hora lord in the Chaldean order
    first_hora_index = chaldean_order.index(first_hora_lord)
    
    # Check if the given time is during the day or night
    is_day = sunrise.datetime() <= date.datetime() < sunset.datetime()
    
    # Calculate the elapsed time since sunrise or sunset
    if is_day:
        elapsed_time = (date.datetime() - sunrise.datetime()).total_seconds()
        hora_duration = day_hora_duration
    else:
        if date.datetime() < sunrise.datetime():
            # Previous day's sunset
            prev_day = date.datetime() - timedelta(days=1)
            prev_date = Datetime.fromDatetime(prev_day)
            prev_sunset = get_sunset(prev_date, location)
            elapsed_time = (date.datetime() - prev_sunset.datetime()).total_seconds()
        else:
            elapsed_time = (date.datetime() - sunset.datetime()).total_seconds()
        hora_duration = night_hora_duration
    
    # Calculate the current hora number (0-11)
    hora_num = int(elapsed_time / hora_duration)
    
    # Calculate the elapsed portion of the current hora
    elapsed = (elapsed_time % hora_duration) / hora_duration
    
    # Calculate the ruling planet of the current hora
    hora_index = (first_hora_index + hora_num) % 7
    hora_lord = chaldean_order[hora_index]
    
    # Calculate the start and end times of the current hora
    if is_day:
        hora_start = sunrise.datetime() + timedelta(seconds=hora_num * hora_duration)
        hora_end = hora_start + timedelta(seconds=hora_duration)
    else:
        if date.datetime() < sunrise.datetime():
            # Previous day's sunset
            prev_day = date.datetime() - timedelta(days=1)
            prev_date = Datetime.fromDatetime(prev_day)
            prev_sunset = get_sunset(prev_date, location)
            hora_start = prev_sunset.datetime() + timedelta(seconds=hora_num * hora_duration)
        else:
            hora_start = sunset.datetime() + timedelta(seconds=hora_num * hora_duration)
        hora_end = hora_start + timedelta(seconds=hora_duration)
    
    return {
        'lord': hora_lord,
        'start': Datetime.fromDatetime(hora_start),
        'end': Datetime.fromDatetime(hora_end),
        'duration': hora_duration / 60,  # in minutes
        'elapsed': elapsed,
        'is_day': is_day
    }


def get_kaala(date, location):
    """
    Calculate the Kaala (division of the day) for a given time
    
    Kaala is a division of the day into 8 equal parts, each with a specific name.
    
    Args:
        date (Datetime): The date and time
        location (GeoPos): The geographical location
    
    Returns:
        dict: Dictionary with Kaala information
    """
    # Get the sunrise and sunset times
    sunrise = get_sunrise(date, location)
    sunset = get_sunset(date, location)
    
    # Calculate the duration of the day
    day_duration = (sunset.datetime() - sunrise.datetime()).total_seconds()
    
    # Calculate the duration of one kaala (1/8 of the day)
    kaala_duration = day_duration / 8
    
    # Check if the given time is during the day
    is_day = sunrise.datetime() <= date.datetime() < sunset.datetime()
    
    # If the time is not during the day, return None
    if not is_day:
        return None
    
    # Calculate the elapsed time since sunrise
    elapsed_time = (date.datetime() - sunrise.datetime()).total_seconds()
    
    # Calculate the current kaala number (0-7)
    kaala_num = int(elapsed_time / kaala_duration)
    
    # Calculate the elapsed portion of the current kaala
    elapsed = (elapsed_time % kaala_duration) / kaala_duration
    
    # Get the name of the current kaala
    kaala_names = [
        'Rudra', 'Ahi', 'Mitra', 'Pitri',
        'Vasu', 'Vara', 'Vishvedeva', 'Brahma'
    ]
    kaala_name = kaala_names[kaala_num]
    
    # Calculate the start and end times of the current kaala
    kaala_start = sunrise.datetime() + timedelta(seconds=kaala_num * kaala_duration)
    kaala_end = kaala_start + timedelta(seconds=kaala_duration)
    
    return {
        'name': kaala_name,
        'start': Datetime.fromDatetime(kaala_start),
        'end': Datetime.fromDatetime(kaala_end),
        'duration': kaala_duration / 60,  # in minutes
        'elapsed': elapsed
    }


def get_amrita_yoga(chart):
    """
    Check if Amrita Yoga is present in a chart
    
    Amrita Yoga is formed when the Moon is in a Kendra house (1, 4, 7, 10)
    and aspected by Jupiter.
    
    Args:
        chart (Chart): The chart
    
    Returns:
        bool: True if Amrita Yoga is present, False otherwise
    """
    # Get the Moon and Jupiter
    moon = chart.getObject(const.MOON)
    jupiter = chart.getObject(const.JUPITER)
    
    # Get the house number of the Moon
    moon_house = get_house_number(chart, const.MOON)
    
    # Check if the Moon is in a Kendra house
    is_moon_in_kendra = moon_house in [1, 4, 7, 10]
    
    # Check if the Moon is aspected by Jupiter
    is_aspected_by_jupiter = is_aspected(chart, const.MOON, const.JUPITER)
    
    # Check if Amrita Yoga is formed
    return is_moon_in_kendra and is_aspected_by_jupiter


def get_siddha_yoga(chart):
    """
    Check if Siddha Yoga is present in a chart
    
    Siddha Yoga is formed when the Moon is in a Trikona house (1, 5, 9)
    and aspected by Mercury.
    
    Args:
        chart (Chart): The chart
    
    Returns:
        bool: True if Siddha Yoga is present, False otherwise
    """
    # Get the Moon and Mercury
    moon = chart.getObject(const.MOON)
    mercury = chart.getObject(const.MERCURY)
    
    # Get the house number of the Moon
    moon_house = get_house_number(chart, const.MOON)
    
    # Check if the Moon is in a Trikona house
    is_moon_in_trikona = moon_house in [1, 5, 9]
    
    # Check if the Moon is aspected by Mercury
    is_aspected_by_mercury = is_aspected(chart, const.MOON, const.MERCURY)
    
    # Check if Siddha Yoga is formed
    return is_moon_in_trikona and is_aspected_by_mercury


def get_amrita_siddha_yoga(chart):
    """
    Check if Amrita-Siddha Yoga is present in a chart
    
    Amrita-Siddha Yoga is formed when both Amrita Yoga and Siddha Yoga
    are present in the chart.
    
    Args:
        chart (Chart): The chart
    
    Returns:
        bool: True if Amrita-Siddha Yoga is present, False otherwise
    """
    # Check if both Amrita Yoga and Siddha Yoga are present
    return get_amrita_yoga(chart) and get_siddha_yoga(chart)


def get_sunrise(date, location):
    """
    Calculate the sunrise time for a given date and location
    
    Args:
        date (Datetime): The date
        location (GeoPos): The geographical location
    
    Returns:
        Datetime: The sunrise time
    """
    # This is a simplified calculation for demonstration purposes
    # In a real implementation, you would use a more accurate algorithm
    
    # Get the date components
    dt = date.datetime()
    year = dt.year
    month = dt.month
    day = dt.day
    
    # Get the location components
    lat = location.lat
    lon = location.lon
    
    # Calculate the day of the year
    day_of_year = dt.timetuple().tm_yday
    
    # Calculate the solar declination
    declination = 23.45 * math.sin(math.radians(360 / 365 * (day_of_year - 81)))
    
    # Calculate the sunrise hour angle
    hour_angle = math.degrees(math.acos(-math.tan(math.radians(lat)) * math.tan(math.radians(declination))))
    
    # Calculate the sunrise time in hours
    sunrise_hours = 12 - hour_angle / 15
    
    # Adjust for longitude
    sunrise_hours -= lon / 15
    
    # Convert to hours and minutes
    sunrise_hour = int(sunrise_hours)
    sunrise_minute = int((sunrise_hours - sunrise_hour) * 60)
    
    # Create a datetime object for the sunrise time
    sunrise_dt = datetime(year, month, day, sunrise_hour, sunrise_minute)
    
    # Convert to Datetime object
    return Datetime.fromDatetime(sunrise_dt)


def get_sunset(date, location):
    """
    Calculate the sunset time for a given date and location
    
    Args:
        date (Datetime): The date
        location (GeoPos): The geographical location
    
    Returns:
        Datetime: The sunset time
    """
    # This is a simplified calculation for demonstration purposes
    # In a real implementation, you would use a more accurate algorithm
    
    # Get the date components
    dt = date.datetime()
    year = dt.year
    month = dt.month
    day = dt.day
    
    # Get the location components
    lat = location.lat
    lon = location.lon
    
    # Calculate the day of the year
    day_of_year = dt.timetuple().tm_yday
    
    # Calculate the solar declination
    declination = 23.45 * math.sin(math.radians(360 / 365 * (day_of_year - 81)))
    
    # Calculate the sunset hour angle
    hour_angle = math.degrees(math.acos(-math.tan(math.radians(lat)) * math.tan(math.radians(declination))))
    
    # Calculate the sunset time in hours
    sunset_hours = 12 + hour_angle / 15
    
    # Adjust for longitude
    sunset_hours -= lon / 15
    
    # Convert to hours and minutes
    sunset_hour = int(sunset_hours)
    sunset_minute = int((sunset_hours - sunset_hour) * 60)
    
    # Create a datetime object for the sunset time
    sunset_dt = datetime(year, month, day, sunset_hour, sunset_minute)
    
    # Convert to Datetime object
    return Datetime.fromDatetime(sunset_dt)


def get_house_number(chart, planet_id):
    """
    Get the house number of a planet
    
    Args:
        chart (Chart): The chart
        planet_id (str): The ID of the planet
    
    Returns:
        int: The house number (1-12) of the planet
    """
    # Get the planet
    planet = chart.getObject(planet_id)
    
    # Get the Ascendant
    asc = chart.getAngle(const.ASC)
    
    # Calculate the house number
    from flatlib import angle
    house_num = 1 + int(angle.distance(planet.lon, asc.lon) / 30) % 12
    
    # Adjust for 0-based indexing
    if house_num == 0:
        house_num = 12
    
    return house_num


def is_aspected(chart, planet1_id, planet2_id):
    """
    Check if a planet is aspected by another planet
    
    Args:
        chart (Chart): The chart
        planet1_id (str): The ID of the planet being aspected
        planet2_id (str): The ID of the planet casting the aspect
    
    Returns:
        bool: True if planet1 is aspected by planet2, False otherwise
    """
    # Get the planets
    planet1 = chart.getObject(planet1_id)
    planet2 = chart.getObject(planet2_id)
    
    # Calculate the orb for different aspects
    from flatlib import angle
    
    # Check for conjunction (0 degrees)
    conj_orb = abs(angle.closestdistance(planet1.lon, planet2.lon))
    if conj_orb <= 10:  # 10 degrees orb
        return True
    
    # Check for opposition (180 degrees)
    opp_orb = abs(angle.closestdistance(planet1.lon, planet2.lon + 180))
    if opp_orb <= 10:  # 10 degrees orb
        return True
    
    # Check for trine (120 degrees)
    trine1_orb = abs(angle.closestdistance(planet1.lon, planet2.lon + 120))
    trine2_orb = abs(angle.closestdistance(planet1.lon, planet2.lon - 120))
    if trine1_orb <= 10 or trine2_orb <= 10:  # 10 degrees orb
        return True
    
    # Check for square (90 degrees)
    square1_orb = abs(angle.closestdistance(planet1.lon, planet2.lon + 90))
    square2_orb = abs(angle.closestdistance(planet1.lon, planet2.lon - 90))
    if square1_orb <= 10 or square2_orb <= 10:  # 10 degrees orb
        return True
    
    # Check for sextile (60 degrees)
    sextile1_orb = abs(angle.closestdistance(planet1.lon, planet2.lon + 60))
    sextile2_orb = abs(angle.closestdistance(planet1.lon, planet2.lon - 60))
    if sextile1_orb <= 10 or sextile2_orb <= 10:  # 10 degrees orb
        return True
    
    return False
