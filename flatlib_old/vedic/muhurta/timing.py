"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements timing calculations for Muhurta (electional astrology)
    in Vedic astrology.
"""

from flatlib import const
from flatlib.chart import Chart
from flatlib.geopos import GeoPos
from flatlib.datetime import Datetime, Time, Date, dateJDN, GREGORIAN
from datetime import datetime
import math
from datetime import timedelta

# Import swisseph for precise calculations
import swisseph as swe

# Import Panchanga functions
from flatlib.vedic.muhurta.panchanga import get_vara

# Standard atmospheric pressure (mbar) and temperature (Celsius)
ATMOS_PRES = 1013.25
ATMOS_TEMP = 15

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
    
    # Calculate the duration of the day in days using Julian Day
    day_duration_days = sunset.jd - sunrise.jd
    
    # Calculate the midday Julian Day
    midday_jd = sunrise.jd + day_duration_days / 2
    
    # Calculate the duration of Abhijit Muhurta (48 minutes)
    abhijit_duration_minutes = 48
    abhijit_duration_seconds = abhijit_duration_minutes * 60
    # Convert half duration (24 minutes) to fraction of a day
    half_duration_days = (abhijit_duration_seconds / 2) / (24 * 60 * 60)
    
    # Calculate the start and end times of Abhijit Muhurta in JD
    abhijit_start_jd = midday_jd - half_duration_days
    abhijit_end_jd = midday_jd + half_duration_days
    
    # Convert start and end JDs back to Datetime objects
    # Use the original date's utcoffset
    abhijit_start_dt = Datetime.fromJD(abhijit_start_jd, date.utcoffset)
    abhijit_end_dt = Datetime.fromJD(abhijit_end_jd, date.utcoffset)

    return {
        'start': abhijit_start_dt, # Use the calculated Datetime objects
        'end': abhijit_end_dt,     # Use the calculated Datetime objects
        'duration': abhijit_duration_minutes,  # in minutes
        'description': 'Most auspicious time of the day'
    }


def get_brahma_muhurta(date, location):
    """
    Calculate the Brahma Muhurta (auspicious time before sunrise)
    
    Brahma Muhurta starts 96 minutes before sunrise and ends 48 minutes
    before sunrise (lasting 48 minutes). It is considered auspicious for
    spiritual practices.
    
    Args:
        date (Datetime): The date
        location (GeoPos): The geographical location
    
    Returns:
        dict: Dictionary with Brahma Muhurta information
    """
    # Get the sunrise time
    sunrise = get_sunrise(date, location)
    sunrise_jd = sunrise.jd # Get Julian Day
    
    # Calculate the duration of Brahma Muhurta (48 minutes)
    brahma_duration_minutes = 48
    
    # Calculate offsets in minutes before sunrise
    start_offset_minutes = 96
    end_offset_minutes = 48
    
    # Convert offsets to fractions of a day
    start_offset_days = (start_offset_minutes * 60) / (24 * 60 * 60)
    end_offset_days = (end_offset_minutes * 60) / (24 * 60 * 60)
    
    # Calculate the start and end times in JD
    brahma_start_jd = sunrise_jd - start_offset_days
    brahma_end_jd = sunrise_jd - end_offset_days
    
    # Convert JDs back to Datetime objects
    brahma_start_dt = Datetime.fromJD(brahma_start_jd, date.utcoffset)
    brahma_end_dt = Datetime.fromJD(brahma_end_jd, date.utcoffset)
    
    return {
        'start': brahma_start_dt,
        'end': brahma_end_dt,
        'duration': brahma_duration_minutes, # Duration remains 48 minutes
        'description': 'Auspicious time before sunrise for spiritual practices'
    }


def get_rahu_kala(date, location):
    """
    Calculate the Rahu Kala (inauspicious time of the day)
    
    Rahu Kala is an inauspicious time that occurs during different parts
    of the day depending on the weekday. It lasts for 1.5 horas (where a hora
    is 1/8th of the daylight duration).
    
    Args:
        date (Datetime): The date
        location (GeoPos): The geographical location
    
    Returns:
        dict: Dictionary with Rahu Kala information
    """
    # Get the sunrise and sunset times
    sunrise = get_sunrise(date, location)
    sunset = get_sunset(date, location)
    
    # Calculate the duration of the day in days using Julian Day
    day_duration_days = sunset.jd - sunrise.jd
    
    # Calculate the duration of one hora in days
    hora_duration_days = day_duration_days / 8
    
    # Get the weekday
    # Note: Creating a chart just to get the weekday might be inefficient
    # if called repeatedly. Consider passing weekday if already known.
    chart = Chart(date, location, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
    vara = get_vara(chart)
    weekday = vara['num'] # Weekday 1=Sunday, ..., 7=Saturday
    
    # Determine the starting hora number (1-8) for Rahu Kala based on the weekday
    # Sun: 8th, Mon: 2nd, Tue: 7th, Wed: 5th, Thu: 6th, Fri: 4th, Sat: 3rd
    # Using 1-based indexing for horas (1st hora starts at sunrise)
    rahu_horas = {1: 8, 2: 2, 3: 7, 4: 5, 5: 6, 6: 4, 7: 3}
    rahu_hora_start_num = rahu_horas.get(weekday, 1) # Default to 1 (Sunday's value) if error
    
    # Calculate the start and end times of Rahu Kala in JD
    rahu_start_jd = sunrise.jd + (rahu_hora_start_num - 1) * hora_duration_days
    # Rahu Kala duration is 1.5 horas
    rahu_duration_days = hora_duration_days * 1.5
    rahu_end_jd = rahu_start_jd + rahu_duration_days

    # Convert JDs back to Datetime objects
    rahu_start_dt = Datetime.fromJD(rahu_start_jd, date.utcoffset)
    rahu_end_dt = Datetime.fromJD(rahu_end_jd, date.utcoffset)

    # Calculate duration in minutes for the return dict
    rahu_duration_minutes = rahu_duration_days * 24 * 60
    
    return {
        'start': rahu_start_dt,
        'end': rahu_end_dt,
        'duration': rahu_duration_minutes,  # in minutes
        'description': 'Inauspicious time ruled by Rahu'
    }


def get_yama_ghantaka(date, location):
    """
    Calculate the Yama Ghantaka (inauspicious time of the day)
    
    Yama Ghantaka is an inauspicious time that occurs during different parts
    of the day depending on the weekday. It lasts for 1.5 horas (where a hora
    is 1/8th of the daylight duration).
    
    Args:
        date (Datetime): The date
        location (GeoPos): The geographical location
    
    Returns:
        dict: Dictionary with Yama Ghantaka information
    """
    # Get the sunrise and sunset times
    sunrise = get_sunrise(date, location)
    sunset = get_sunset(date, location)
    
    # Calculate the duration of the day in days using Julian Day
    day_duration_days = sunset.jd - sunrise.jd
    
    # Calculate the duration of one hora in days
    hora_duration_days = day_duration_days / 8
    
    # Get the weekday
    chart = Chart(date, location, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
    vara = get_vara(chart)
    weekday = vara['num'] # Weekday 1=Sunday, ..., 7=Saturday
    
    # Determine the starting hora number (1-8) for Yama Ghantaka based on the weekday
    # Sun: 4th, Mon: 7th, Tue: 3rd, Wed: 6th, Thu: 2nd, Fri: 5th, Sat: 8th
    yama_horas = {1: 4, 2: 7, 3: 3, 4: 6, 5: 2, 6: 5, 7: 8}
    yama_hora_start_num = yama_horas.get(weekday, 1) # Default to 1 if error
    
    # Calculate the start and end times of Yama Ghantaka in JD
    yama_start_jd = sunrise.jd + (yama_hora_start_num - 1) * hora_duration_days
    # Yama Ghantaka duration is 1.5 horas
    yama_duration_days = hora_duration_days * 1.5
    yama_end_jd = yama_start_jd + yama_duration_days

    # Convert JDs back to Datetime objects
    yama_start_dt = Datetime.fromJD(yama_start_jd, date.utcoffset)
    yama_end_dt = Datetime.fromJD(yama_end_jd, date.utcoffset)

    # Calculate duration in minutes for the return dict
    yama_duration_minutes = yama_duration_days * 24 * 60
    
    return {
        'start': yama_start_dt,
        'end': yama_end_dt,
        'duration': yama_duration_minutes,  # in minutes
        'description': 'Inauspicious time ruled by Yama'
    }


def get_gulika_kala(date, location):
    """
    Calculate the Gulika Kala (inauspicious time of the day)
    
    Gulika Kala is an inauspicious time that occurs during different parts
    of the day depending on the weekday. It lasts for 1.5 horas (where a hora
    is 1/8th of the daylight duration).
    
    Args:
        date (Datetime): The date
        location (GeoPos): The geographical location
    
    Returns:
        dict: Dictionary with Gulika Kala information
    """
    # Get the sunrise and sunset times
    sunrise = get_sunrise(date, location)
    sunset = get_sunset(date, location)
    
    # Calculate the duration of the day in days using Julian Day
    day_duration_days = sunset.jd - sunrise.jd
    
    # Calculate the duration of one hora in days
    hora_duration_days = day_duration_days / 8
    
    # Get the weekday
    chart = Chart(date, location, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
    vara = get_vara(chart)
    weekday = vara['num'] # Weekday 1=Sunday, ..., 7=Saturday
    
    # Determine the starting hora number (1-8) for Gulika Kala based on the weekday
    # Sun: 6th, Mon: 5th, Tue: 4th, Wed: 3rd, Thu: 2nd, Fri: 1st, Sat: 7th
    gulika_horas = {1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1, 7: 7}
    gulika_hora_start_num = gulika_horas.get(weekday, 1) # Default to 1 if error
    
    # Calculate the start and end times of Gulika Kala in JD
    gulika_start_jd = sunrise.jd + (gulika_hora_start_num - 1) * hora_duration_days
    # Gulika Kala duration is 1.5 horas
    gulika_duration_days = hora_duration_days * 1.5
    gulika_end_jd = gulika_start_jd + gulika_duration_days

    # Convert JDs back to Datetime objects
    gulika_start_dt = Datetime.fromJD(gulika_start_jd, date.utcoffset)
    gulika_end_dt = Datetime.fromJD(gulika_end_jd, date.utcoffset)

    # Calculate duration in minutes for the return dict
    gulika_duration_minutes = gulika_duration_days * 24 * 60
    
    return {
        'start': gulika_start_dt,
        'end': gulika_end_dt,
        'duration': gulika_duration_minutes,  # in minutes
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


def get_sunrise(date: Datetime, location: GeoPos) -> Datetime:
    """
    Calculate the sunrise time for a given date and location using swisseph.
    
    Args:
        date (Datetime): The date (UT is derived from this).
        location (GeoPos): The geographical location.
    
    Returns:
        Datetime: The sunrise time in the original date's timezone.
        
    Raises:
        RuntimeError: If swisseph calculation fails.
    """
    # Get Julian Day UT from input Datetime
    jd_ut = date.jd
    
    # Get geographic coordinates
    lon = location.lon
    lat = location.lat
    alt = location.alt # Use altitude if available, default 0
    
    # Prepare arguments for swisseph
    ipl = swe.SUN
    starname = ''
    epheflag = swe.FLG_SWIEPH # Use Swiss Ephemeris
    # Calculate sunrise (apparent rise of the disc center)
    risetrans_flag = swe.RISE_TRANS | swe.BIT_DISC_CENTER
    geopos = (lon, lat, alt)
    atpress = ATMOS_PRES
    attemp = ATMOS_TEMP
    
    # Call swisseph
    try:
        ret, jd_et, err = swe.rise_trans(jd_ut, ipl, starname, epheflag, risetrans_flag, geopos, atpress, attemp)
    except Exception as e:
        raise RuntimeError(f"Swisseph error during sunrise calculation: {e}") from e

    if ret < 0:
        raise RuntimeError(f"Swisseph calculation failed for sunrise: {err}")

    # Convert result JD ET back to Datetime, preserving original timezone
    # Note: rise_trans returns JD ET (Ephemeris Time), which is close enough to UT for this purpose
    # without complex Delta T corrections for historical dates.
    # Use the original date's utcoffset for conversion.
    sunrise_dt = Datetime.fromJD(jd_et, date.utcoffset)
    
    return sunrise_dt


def get_sunset(date: Datetime, location: GeoPos) -> Datetime:
    """
    Calculate the sunset time for a given date and location using swisseph.
    
    Args:
        date (Datetime): The date (UT is derived from this).
        location (GeoPos): The geographical location.
    
    Returns:
        Datetime: The sunset time in the original date's timezone.
        
    Raises:
        RuntimeError: If swisseph calculation fails.
    """
    # Get Julian Day UT from input Datetime
    jd_ut = date.jd
    
    # Get geographic coordinates
    lon = location.lon
    lat = location.lat
    alt = location.alt # Use altitude if available, default 0
    
    # Prepare arguments for swisseph
    ipl = swe.SUN
    starname = ''
    epheflag = swe.FLG_SWIEPH # Use Swiss Ephemeris
    # Calculate sunset (apparent set of the disc center)
    risetrans_flag = swe.SET_TRANS | swe.BIT_DISC_CENTER 
    geopos = (lon, lat, alt)
    atpress = ATMOS_PRES
    attemp = ATMOS_TEMP
    
    # Call swisseph
    try:
        ret, jd_et, err = swe.rise_trans(jd_ut, ipl, starname, epheflag, risetrans_flag, geopos, atpress, attemp)
    except Exception as e:
        raise RuntimeError(f"Swisseph error during sunset calculation: {e}") from e

    if ret < 0:
        raise RuntimeError(f"Swisseph calculation failed for sunset: {err}")

    # Convert result JD ET back to Datetime, preserving original timezone
    sunset_dt = Datetime.fromJD(jd_et, date.utcoffset)
    
    return sunset_dt


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
