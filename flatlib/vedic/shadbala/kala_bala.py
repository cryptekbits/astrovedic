"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Kala Bala (temporal strength) calculations
    for Shadbala in Vedic astrology.
"""

from flatlib import const
from flatlib import angle
from flatlib.datetime import Datetime, Date, Time, jdnDate
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

    According to standard Vedic rules, Nathonnatha Bala is based on the planet's
    preference for day or night and the birth time's proximity to midday or midnight.
    Strength is maximum (60 Virupas) at the peak time (midday for diurnal planets,
    midnight for nocturnal planets) and decreases linearly to 0 at the nadir.

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet

    Returns:
        dict: Dictionary with Nathonnatha Bala information
    """
    # Get date and time components from the chart
    date_list = jdnDate(chart.date.date.jdn)
    year, month, day = date_list[0], date_list[1], date_list[2]

    time_list = chart.date.time.time()
    hour, minute, second = time_list[0], time_list[1], int(time_list[2])

    # Format string correctly for datetime
    datetime_str = f"{year}/{month:02d}/{day:02d} {hour:02d}:{minute:02d}:{second:02d}"

    try:
        # Parse the datetime
        dt = datetime.strptime(datetime_str, "%Y/%m/%d %H:%M:%S")

        # Calculate time from midnight (in hours, 0-24)
        time_from_midnight = dt.hour + dt.minute/60.0 + dt.second/3600.0

        # Calculate time from midday (in hours, 0-12)
        if time_from_midnight < 12:
            time_from_midday = 12 - time_from_midnight
        else:
            time_from_midday = time_from_midnight - 12

        # Normalize to 0-1 range (0 = midday/midnight, 1 = nadir)
        midday_factor = time_from_midday / 12.0  # 0 at midday, 1 at midnight
        midnight_factor = 1.0 - midday_factor     # 0 at midnight, 1 at midday
    except ValueError as e:
        # Handle datetime parsing error
        print(f"Error parsing date/time: {datetime_str} with format %Y/%m/%d %H:%M:%S")
        print(e)
        # Use a default value
        midday_factor = 0.5
        midnight_factor = 0.5

    # Correct planet classifications according to standard Vedic rules
    # Diurnal planets (Sun, Jupiter, Venus)
    diurnal_planets = [const.SUN, const.JUPITER, const.VENUS]

    # Nocturnal planets (Moon, Mars, Saturn)
    nocturnal_planets = [const.MOON, const.MARS, const.SATURN]

    # Mercury is both diurnal and nocturnal

    # Maximum value (in Virupas)
    max_value = 60.0

    # Calculate Nathonnatha Bala using linear interpolation
    if planet_id in diurnal_planets:
        # Diurnal planets are strongest at midday (midday_factor = 0)
        # and weakest at midnight (midday_factor = 1)
        value = max_value * (1.0 - midday_factor)
        if midday_factor < 0.25:
            description = 'Diurnal planet near midday (strong)'
        elif midday_factor < 0.5:
            description = 'Diurnal planet moderately distant from midday'
        else:
            description = 'Diurnal planet far from midday (weak)'
    elif planet_id in nocturnal_planets:
        # Nocturnal planets are strongest at midnight (midnight_factor = 0)
        # and weakest at midday (midnight_factor = 1)
        value = max_value * (1.0 - midnight_factor)
        if midnight_factor < 0.25:
            description = 'Nocturnal planet near midnight (strong)'
        elif midnight_factor < 0.5:
            description = 'Nocturnal planet moderately distant from midnight'
        else:
            description = 'Nocturnal planet far from midnight (weak)'
    elif planet_id == const.MERCURY:
        # Mercury gets the better of day or night strength
        value = max_value * max(1.0 - midday_factor, 1.0 - midnight_factor)
        description = 'Mercury (benefits from both day and night)'
    elif planet_id in [const.RAHU, const.KETU]:
        # Rahu and Ketu are excluded from Nathonnatha Bala
        value = 0.0
        description = 'Nodes are excluded from Nathonnatha Bala'
    else:
        value = 0.0
        description = 'Unknown planet'

    # Add additional information for debugging/analysis
    return {
        'value': value,
        'description': description,
        'midday_factor': midday_factor,
        'midnight_factor': midnight_factor,
        'time_from_midnight': time_from_midnight,
        'time_from_midday': time_from_midday
    }


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

    In Vedic astrology, Tribhaga Bala is based on dividing the day and night into
    three equal parts each, with different planetary rulers for each part.

    Day parts rulers:
    - 1st part: Mercury
    - 2nd part: Sun
    - 3rd part: Saturn

    Night parts rulers:
    - 1st part: Moon
    - 2nd part: Venus
    - 3rd part: Mars

    Jupiter always gets full strength regardless of the part.

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet

    Returns:
        dict: Dictionary with Tribhaga Bala information
    """
    from flatlib.ephem import ephem
    from flatlib.datetime import Datetime

    # Maximum value (in Virupas)
    max_value = 60.0

    # Special case for Jupiter (always gets full strength)
    if planet_id == const.JUPITER:
        return {
            'value': max_value,
            'description': 'Jupiter always gets full strength in Tribhaga Bala',
            'part': None,
            'is_day': None
        }

    # Get the chart date and location
    date = chart.date
    location = chart.pos

    # Get sunrise and sunset times
    sunrise = ephem.lastSunrise(date, location)
    sunset = ephem.nextSunset(date, location)

    # Check if the birth time is during day or night
    is_day = sunrise.jd <= date.jd < sunset.jd

    if is_day:
        # Day time calculation
        day_duration = sunset.jd - sunrise.jd
        part_duration = day_duration / 3.0

        # Determine which part of the day the birth time falls into
        elapsed_time = date.jd - sunrise.jd
        part = int(elapsed_time / part_duration) + 1  # 1, 2, or 3

        # Day parts rulers
        day_rulers = {
            1: const.MERCURY,  # 1st part: Mercury
            2: const.SUN,      # 2nd part: Sun
            3: const.SATURN    # 3rd part: Saturn
        }

        # Get the ruler of this part
        part_ruler = day_rulers[part]

        # Calculate Tribhaga Bala
        if planet_id == part_ruler:
            value = max_value
            # Use correct ordinal suffix
            if part == 1:
                suffix = 'st'
            elif part == 2:
                suffix = 'nd'
            else:  # part == 3
                suffix = 'rd'
            description = f'Ruler of the {part}{suffix} part of the day'
        else:
            value = 0.0
            # Use correct ordinal suffix
            if part == 1:
                suffix = 'st'
            elif part == 2:
                suffix = 'nd'
            else:  # part == 3
                suffix = 'rd'
            description = f'Not ruler of the {part}{suffix} part of the day'
    else:
        # Night time calculation
        # For night, we need to handle the case where the birth time might be
        # after midnight but before sunrise of the next day

        # Get the next day's sunrise
        next_sunrise = ephem.nextSunrise(date, location)

        # Calculate night duration
        night_duration = next_sunrise.jd - sunset.jd
        part_duration = night_duration / 3.0

        # Determine which part of the night the birth time falls into
        if date.jd >= sunset.jd:
            # After sunset on the same day
            elapsed_time = date.jd - sunset.jd
        else:
            # After midnight but before sunrise
            prev_sunset = ephem.lastSunset(date, location)
            elapsed_time = date.jd - prev_sunset.jd

        part = int(elapsed_time / part_duration) + 1  # 1, 2, or 3

        # Night parts rulers
        night_rulers = {
            1: const.MOON,    # 1st part: Moon
            2: const.VENUS,   # 2nd part: Venus
            3: const.MARS     # 3rd part: Mars
        }

        # Get the ruler of this part
        part_ruler = night_rulers[part]

        # Calculate Tribhaga Bala
        if planet_id == part_ruler:
            value = max_value
            # Use correct ordinal suffix
            if part == 1:
                suffix = 'st'
            elif part == 2:
                suffix = 'nd'
            else:  # part == 3
                suffix = 'rd'
            description = f'Ruler of the {part}{suffix} part of the night'
        else:
            value = 0.0
            # Use correct ordinal suffix
            if part == 1:
                suffix = 'st'
            elif part == 2:
                suffix = 'nd'
            else:  # part == 3
                suffix = 'rd'
            description = f'Not ruler of the {part}{suffix} part of the night'

    # Return the result with additional information for debugging
    return {
        'value': value,
        'description': description,
        'part': part,
        'is_day': is_day
    }


def calculate_mesha_sankranti(year, utcoffset='+00:00'):
    """
    Calculate the Mesha Sankranti (solar ingress into Aries) for a given year

    Args:
        year (int): The year to calculate Mesha Sankranti for
        utcoffset (str): UTC offset string (default: '+00:00')

    Returns:
        Datetime: The date and time of Mesha Sankranti
    """
    from flatlib.ephem import eph
    from flatlib.datetime import Datetime
    from flatlib.vedic.transits import calculator

    # Create a date near the expected Mesha Sankranti (around April 14)
    # This is just an approximation to start the search
    start_date = Datetime(f'{year}/04/14', '12:00', utcoffset)

    # Calculate when the Sun enters Aries (sign 1)
    # For Vedic/sidereal calculations, we need to use the appropriate ayanamsa
    try:
        # Use the transit calculator from the vedic.transits module
        mesha_sankranti = calculator.next_sign_transit(const.SUN, start_date, const.ARIES, const.AY_LAHIRI)

        # If the transit is more than 30 days away, it means we're past this year's
        # Mesha Sankranti, so we need to look for the previous one
        if mesha_sankranti.jd - start_date.jd > 30:
            # Try a date from the previous month
            start_date = Datetime(f'{year}/03/14', '12:00', utcoffset)
            mesha_sankranti = calculator.next_sign_transit(const.SUN, start_date, const.ARIES, const.AY_LAHIRI)

        return mesha_sankranti
    except Exception as e:
        # Fallback method if the transit calculator fails
        print(f"Error calculating Mesha Sankranti: {e}")

        # Return a fixed date (April 14) as a fallback
        return Datetime(f'{year}/04/14', '12:00', utcoffset)


def get_weekday_ruler(weekday):
    """
    Get the planetary ruler of a weekday

    Args:
        weekday (int): Day of week (0=Sunday, 1=Monday, ..., 6=Saturday)

    Returns:
        str: Planet ID of the ruler
    """
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

    return day_rulers[weekday]


def calculate_abda_bala(chart, planet_id):
    """
    Calculate Abda Bala (Year Lord Strength)

    In Vedic astrology, the year lord (Abda Pati) is determined by the
    weekday on which the solar year begins (Mesha Sankranti, when the Sun
    enters Aries in the sidereal zodiac). The lord of that weekday becomes
    the lord of the year.

    Args:
        chart (Chart): The chart
        planet_id (str): The ID of the planet

    Returns:
        dict: Dictionary with Abda Bala information (15 Rupas if the planet is the year lord)
    """
    # Get the year from the chart date
    date_list = jdnDate(chart.date.date.jdn)
    year = date_list[0]

    # Get the UTC offset from the chart
    utcoffset = chart.date.utcoffset.toString()

    # Calculate Mesha Sankranti for the year
    mesha_sankranti = calculate_mesha_sankranti(year, utcoffset)

    # Determine the weekday of Mesha Sankranti (0=Sunday, 1=Monday, ..., 6=Saturday)
    weekday = mesha_sankranti.date.dayofweek()

    # Get the planetary ruler of that weekday
    abda_pati = get_weekday_ruler(weekday)

    # Maximum value (in Virupas)
    max_value = 15.0

    # Calculate Abda Bala
    if planet_id == abda_pati:
        value = max_value
        description = f'Ruler of the year (lord of Mesha Sankranti weekday: {weekday})'
    else:
        value = 0.0
        description = f'Not ruler of the year (Mesha Sankranti weekday: {weekday})'

    # Add additional information for debugging/analysis
    return {
        'value': value,
        'description': description,
        'mesha_sankranti': str(mesha_sankranti),
        'weekday': weekday,
        'abda_pati': abda_pati
    }


def calculate_sankranti(chart, sign):
    """
    Calculate the Sankranti (solar ingress) for a given sign

    Args:
        chart (Chart): The birth chart
        sign (str or int): The sign to calculate Sankranti for

    Returns:
        Datetime: The date and time of the Sankranti
    """
    from flatlib.vedic.transits import calculator

    # Get the date and UTC offset from the chart
    date = chart.date

    # Create a date object for the calculation
    # We'll start from the chart date and look for the next Sankranti
    start_date = date

    try:
        # Calculate when the Sun enters the specified sign
        sankranti = calculator.next_sign_transit(const.SUN, start_date, sign, const.AY_LAHIRI)

        # If the Sankranti is more than 30 days away, it means we're looking for
        # the current solar month, so we need to find the previous Sankranti
        if sankranti.jd - start_date.jd > 30:
            # Try to find the last sign transit
            try:
                sankranti = calculator.last_sign_transit(const.SUN, start_date, sign, const.AY_LAHIRI)
            except Exception as e:
                # If that fails, use a fallback method
                print(f"Error calculating last Sankranti: {e}")
                # Fallback: use a date 30 days before and look for the next Sankranti
                from flatlib.datetime import Datetime
                fallback_date = Datetime.fromJD(start_date.jd - 30, start_date.utcoffset.toString())
                sankranti = calculator.next_sign_transit(const.SUN, fallback_date, sign, const.AY_LAHIRI)

        return sankranti
    except Exception as e:
        # If the transit calculator fails, return a fallback date
        print(f"Error calculating Sankranti: {e}")
        # Fallback: return the chart date as a placeholder
        return date


def calculate_masa_bala(chart, planet_id):
    """
    Calculate Masa Bala (monthly strength) for a planet

    In Vedic astrology, the month lord (Masa Pati) is determined by the
    weekday on which the solar month begins (Sankranti, when the Sun
    enters a new sign). The lord of that weekday becomes the lord of the month.

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet

    Returns:
        dict: Dictionary with Masa Bala information
    """
    # Get the Sun's sign from the chart
    sun = chart.getObject(const.SUN)
    sun_sign = sun.sign

    # Calculate the Sankranti for the current solar month
    sankranti = calculate_sankranti(chart, sun_sign)

    # Determine the weekday of the Sankranti (0=Sunday, 1=Monday, ..., 6=Saturday)
    weekday = sankranti.date.dayofweek()

    # Get the planetary ruler of that weekday
    masa_pati = get_weekday_ruler(weekday)

    # Maximum value (in Virupas)
    max_value = 30.0

    # Calculate Masa Bala
    if planet_id == masa_pati:
        value = max_value
        description = f'Ruler of the month (lord of Sankranti weekday: {weekday})'
    else:
        value = 0.0
        description = f'Not ruler of the month (Sankranti weekday: {weekday})'

    # Add additional information for debugging/analysis
    return {
        'value': value,
        'description': description,
        'sankranti': str(sankranti),
        'weekday': weekday,
        'masa_pati': masa_pati
    }


def calculate_vara_bala(chart, planet_id):
    """
    Calculate Vara Bala (weekday strength) for a planet

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet

    Returns:
        dict: Dictionary with Vara Bala information
    """
    # Get the day of the week (0=Sunday, 1=Monday, ..., 6=Saturday)
    day_of_week = chart.date.date.dayofweek()

    # Get date components
    date_list = jdnDate(chart.date.date.jdn)
    year, month, day = date_list[0], date_list[1], date_list[2]

    # Get time components
    time_list = chart.date.time.time()
    hour, minute, second = time_list[0], time_list[1], int(time_list[2]) # Ensure second is int

    # Format string correctly
    datetime_str = f"{year}/{month:02d}/{day:02d} {hour:02d}:{minute:02d}:{second:02d}"

    try:
        dt = datetime.strptime(datetime_str, "%Y/%m/%d %H:%M:%S")
        day_of_week = (dt.weekday() + 1) % 7  # Monday is 0, Sunday is 6 -> Sunday is 0
    except ValueError as e:
        print(f"Error parsing date/time: {datetime_str} with format %Y/%m/%d %H:%M:%S")
        print(e)
        # Handle error or return default/error value
        return {'value': 0.0, 'description': 'Error calculating Vara Bala'}

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

    In Vedic astrology, Hora (planetary hour) is calculated by dividing the day
    (sunrise to sunset) and night (sunset to sunrise) into 12 equal parts each.
    The first hora of the day is ruled by the lord of the weekday (Vara Lord),
    and subsequent horas follow the Chaldean order: Saturn, Jupiter, Mars, Sun,
    Venus, Mercury, Moon.

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet

    Returns:
        dict: Dictionary with Hora Bala information
    """
    from flatlib.ephem import ephem
    from flatlib.tools import planetarytime

    # Maximum value (in Virupas)
    max_value = 60.0

    try:
        # Get the date and location from the chart
        date = chart.date
        location = chart.pos

        # Get the planetary hour table
        hour_table = planetarytime.getHourTable(date, location)

        # Get the current hora ruler
        hora_ruler = hour_table.hourRuler()

        # Get additional information for debugging
        hora_info = hour_table.currInfo()

        # Calculate Hora Bala
        if planet_id == hora_ruler:
            value = max_value
            description = f'Ruler of the hora (hour {hora_info["hourNumber"]})'
        else:
            value = 0.0
            description = f'Not ruler of the hora (hour {hora_info["hourNumber"]}, ruler: {hora_ruler})'

        # Return the result with additional information for debugging
        return {
            'value': value,
            'description': description,
            'hora_ruler': hora_ruler,
            'hora_number': hora_info['hourNumber'],
            'hora_start': str(hora_info['start']),
            'hora_end': str(hora_info['end']),
            'day_ruler': hour_table.dayRuler(),
            'night_ruler': hour_table.nightRuler()
        }
    except Exception as e:
        # If there's an error, use a fallback method
        print(f"Error calculating Hora Bala: {e}")

        # Fallback method: Calculate the day of week and use a simplified approach
        try:
            # Get the day of the week (0=Sunday, 1=Monday, ..., 6=Saturday)
            day_of_week = chart.date.date.dayofweek()

            # Get the Vara Lord (weekday ruler)
            day_rulers = {
                0: const.SUN,     # Sun rules Sunday
                1: const.MOON,    # Moon rules Monday
                2: const.MARS,    # Mars rules Tuesday
                3: const.MERCURY, # Mercury rules Wednesday
                4: const.JUPITER, # Jupiter rules Thursday
                5: const.VENUS,   # Venus rules Friday
                6: const.SATURN   # Saturn rules Saturday
            }
            vara_lord = day_rulers[day_of_week]

            # Chaldean order of planets (used for hora sequence)
            chaldean_order = [
                const.SATURN,
                const.JUPITER,
                const.MARS,
                const.SUN,
                const.VENUS,
                const.MERCURY,
                const.MOON
            ]

            # Get the hour of the day (approximate)
            hour_of_day = chart.date.time.time()[0]

            # Determine if it's day or night (simplified)
            is_diurnal = chart.isDiurnal()

            # Find the index of the Vara Lord in the Chaldean order
            vara_lord_index = chaldean_order.index(vara_lord) if vara_lord in chaldean_order else 0

            # Calculate the hora index
            if is_diurnal:
                # Day hours start from the Vara Lord
                hora_index = (vara_lord_index + hour_of_day) % 7
            else:
                # Night hours start from the 12th hour after the Vara Lord
                hora_index = (vara_lord_index + 12 + hour_of_day) % 7

            # Get the hora ruler
            hora_ruler = chaldean_order[hora_index]

            # Calculate Hora Bala
            if planet_id == hora_ruler:
                value = max_value
                description = f'Ruler of the hora (fallback method)'
            else:
                value = 0.0
                description = f'Not ruler of the hora (fallback method, ruler: {hora_ruler})'

            # Return the result with limited information
            return {
                'value': value,
                'description': description,
                'hora_ruler': hora_ruler,
                'day_ruler': vara_lord
            }
        except Exception as e:
            # If even the fallback method fails, return a default value
            print(f"Error in fallback method for Hora Bala: {e}")
            return {'value': 0.0, 'description': 'Error calculating Hora Bala'}


def calculate_ayana_bala(chart, planet_id):
    """
    Calculate Ayana Bala (declination strength) for a planet

    In Vedic astrology, Ayana Bala is based on the planet's declination (distance
    from the celestial equator). Planets gain strength when they are in their
    preferred hemisphere: northern declination for Sun, Mars, Jupiter, and Mercury;
    southern declination for Moon, Venus, and Saturn.

    The standard formula is:
    Strength = (30 + (Declination / Obliquity) * 30) Virupas

    This is adjusted based on the planet's preferred hemisphere.

    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet

    Returns:
        dict: Dictionary with Ayana Bala information
    """
    from flatlib import utils

    # Get the planet from the chart
    planet = chart.getObject(planet_id)

    # Maximum value (in Virupas)
    max_value = 60.0

    # Standard obliquity of the ecliptic (in degrees)
    obliquity = 23.44

    # Calculate the declination of the planet
    _, declination = utils.eqCoords(planet.lon, planet.lat)

    # Determine the preferred hemisphere for each planet
    # Northern declination (positive) is preferred for Sun, Mars, Jupiter, Mercury
    # Southern declination (negative) is preferred for Moon, Venus, Saturn
    northern_preference = [const.SUN, const.MARS, const.JUPITER, const.MERCURY]
    southern_preference = [const.MOON, const.VENUS, const.SATURN]

    # For Rahu and Ketu, we'll use the same preference as Saturn (southern)
    if planet_id in [const.RAHU, const.KETU]:
        preferred_hemisphere = 'south'
    elif planet_id in northern_preference:
        preferred_hemisphere = 'north'
    elif planet_id in southern_preference:
        preferred_hemisphere = 'south'
    else:
        # For any other object, default to northern
        preferred_hemisphere = 'north'

    # Calculate the absolute declination (0 to 23.44 degrees)
    abs_declination = abs(declination)

    # Calculate the relative strength based on declination (0 to 1)
    relative_strength = abs_declination / obliquity

    # Adjust the strength based on the preferred hemisphere
    if (preferred_hemisphere == 'north' and declination >= 0) or \
       (preferred_hemisphere == 'south' and declination <= 0):
        # Planet is in its preferred hemisphere
        strength_factor = relative_strength
        hemisphere_status = 'preferred'
    else:
        # Planet is in its non-preferred hemisphere
        strength_factor = 1 - relative_strength
        hemisphere_status = 'non-preferred'

    # Calculate the final Ayana Bala value (0 to 60 Virupas)
    value = 30.0 + (strength_factor * 30.0)

    # Create a descriptive message
    if hemisphere_status == 'preferred':
        description = f'In preferred hemisphere ({preferred_hemisphere}) with declination {declination:.2f}°'
    else:
        description = f'In non-preferred hemisphere ({preferred_hemisphere} preferred) with declination {declination:.2f}°'

    # Return the result with additional information for debugging
    return {
        'value': value,
        'description': description,
        'declination': declination,
        'preferred_hemisphere': preferred_hemisphere,
        'hemisphere_status': hemisphere_status,
        'relative_strength': relative_strength,
        'strength_factor': strength_factor
    }


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
