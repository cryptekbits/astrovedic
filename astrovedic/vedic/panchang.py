"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Panchang (Vedic almanac) calculations.
    It includes tithi, nakshatra, yoga, karana, and other
    Vedic time elements.
"""

from astrovedic import const
from astrovedic import angle
from astrovedic.datetime import Datetime
from astrovedic.ephem import swe, ephem
from astrovedic.geopos import GeoPos

# Tithi (lunar day) names
TITHI_NAMES = [
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima",
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Amavasya"
]

# Paksha (lunar fortnight) names
SHUKLA_PAKSHA = "Shukla Paksha"  # Bright half (waxing moon)
KRISHNA_PAKSHA = "Krishna Paksha"  # Dark half (waning moon)

# Karana (half tithi) names
KARANA_NAMES = [
    "Bava", "Balava", "Kaulava", "Taitila", "Garija",
    "Vanija", "Vishti", "Bava", "Balava", "Kaulava",
    "Taitila", "Garija", "Vanija", "Vishti", "Bava",
    "Balava", "Kaulava", "Taitila", "Garija", "Vanija",
    "Vishti", "Bava", "Balava", "Kaulava", "Taitila",
    "Garija", "Vanija", "Vishti", "Bava", "Balava",
    "Kaulava", "Taitila", "Garija", "Vanija", "Vishti",
    "Bava", "Balava", "Kaulava", "Taitila", "Garija",
    "Vanija", "Vishti", "Bava", "Balava", "Kaulava",
    "Taitila", "Garija", "Vanija", "Vishti", "Bava",
    "Balava", "Kaulava", "Taitila", "Garija", "Vanija",
    "Vishti", "Shakuni", "Chatushpada", "Naga", "Kimstughna"
]

# Yoga (lunar-solar combination) names
YOGA_NAMES = [
    "Vishkumbha", "Preeti", "Ayushman", "Saubhagya", "Shobhana",
    "Atiganda", "Sukarma", "Dhriti", "Shoola", "Ganda",
    "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra",
    "Siddhi", "Vyatipata", "Variyana", "Parigha", "Shiva",
    "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma",
    "Indra", "Vaidhriti"
]

# Vara (weekday) names
VARA_NAMES = [
    "Ravivara",    # Sunday
    "Somavara",    # Monday
    "Mangalavara", # Tuesday
    "Budhavara",   # Wednesday
    "Guruvara",    # Thursday
    "Shukravara",  # Friday
    "Shanivara"    # Saturday
]

# Hora (planetary hour) rulers
HORA_RULERS = [
    const.SUN, const.VENUS, const.MERCURY, const.MOON, const.SATURN,
    const.JUPITER, const.MARS
]


def get_tithi(jd, ayanamsa=None):
    """
    Calculate tithi (lunar day) for a given Julian day

    Args:
        jd (float): Julian day
        ayanamsa (str, optional): Ayanamsa to use for sidereal calculations

    Returns:
        dict: Dictionary with tithi information
    """
    # Get Sun and Moon longitudes
    sun_lon = swe.sweObjectLon(const.SUN, jd)
    moon_lon = swe.sweObjectLon(const.MOON, jd)

    # If ayanamsa is provided, convert to sidereal
    if ayanamsa:
        ayanamsa_val = swe.get_ayanamsa(jd, ayanamsa)
        sun_lon = angle.norm(sun_lon - ayanamsa_val)
        moon_lon = angle.norm(moon_lon - ayanamsa_val)

    # Calculate lunar phase angle
    phase_angle = angle.norm(moon_lon - sun_lon)

    # Calculate tithi (0-29)
    tithi_index = int(phase_angle / 12)

    # Get tithi name
    tithi_name = TITHI_NAMES[tithi_index]

    # Determine paksha (lunar fortnight)
    paksha = SHUKLA_PAKSHA if tithi_index < 15 else KRISHNA_PAKSHA

    # Calculate completion percentage
    completion = (phase_angle % 12) / 12 * 100

    # Check for Purnima and Amavasya
    is_purnima = (tithi_index == 14)
    is_amavasya = (tithi_index == 29)

    return {
        'index': tithi_index,
        'name': tithi_name,
        'paksha': paksha,
        'completion': completion,
        'is_purnima': is_purnima,
        'is_amavasya': is_amavasya
    }


def get_karana(jd, ayanamsa=None):
    """
    Calculate karana (half tithi) for a given Julian day

    Args:
        jd (float): Julian day
        ayanamsa (str, optional): Ayanamsa to use for sidereal calculations (not used directly in this function)

    Returns:
        dict: Dictionary with karana information
    """
    # Calculate karana index (0-59)
    phase_angle = angle.norm(swe.sweObjectLon(const.MOON, jd) - swe.sweObjectLon(const.SUN, jd))
    karana_index = int(phase_angle / 6)

    # Get karana name
    karana_name = KARANA_NAMES[karana_index]

    # Calculate completion percentage
    completion = (phase_angle % 6) / 6 * 100

    return {
        'index': karana_index,
        'name': karana_name,
        'completion': completion
    }


def get_yoga(jd, ayanamsa=None):
    """
    Calculate yoga for a given Julian day

    Yoga is the sum of the longitudes of the Sun and Moon
    divided into 27 parts.

    Args:
        jd (float): Julian day
        ayanamsa (str, optional): Ayanamsa to use for sidereal calculations

    Returns:
        dict: Dictionary with yoga information
    """
    # Get Sun and Moon longitudes
    sun_lon = swe.sweObjectLon(const.SUN, jd)
    moon_lon = swe.sweObjectLon(const.MOON, jd)

    # If ayanamsa is provided, convert to sidereal
    if ayanamsa:
        ayanamsa_val = swe.get_ayanamsa(jd, ayanamsa)
        sun_lon = angle.norm(sun_lon - ayanamsa_val)
        moon_lon = angle.norm(moon_lon - ayanamsa_val)

    # Calculate yoga angle (sum of Sun and Moon longitudes)
    yoga_angle = angle.norm(sun_lon + moon_lon)

    # Calculate yoga index (0-26)
    yoga_index = int(yoga_angle / (360 / 27))

    # Get yoga name
    yoga_name = YOGA_NAMES[yoga_index]

    # Calculate completion percentage
    completion = (yoga_angle % (360 / 27)) / (360 / 27) * 100

    return {
        'index': yoga_index,
        'name': yoga_name,
        'completion': completion
    }


def get_vara(jd):
    """
    Calculate vara (weekday) for a given Julian day

    Args:
        jd (float): Julian day

    Returns:
        dict: Dictionary with vara information
    """
    # Calculate day of week (0 = Sunday, 1 = Monday, etc.)
    day_of_week = int((jd + 1.5) % 7)

    # Get vara name
    vara_name = VARA_NAMES[day_of_week]

    return {
        'index': day_of_week,
        'name': vara_name
    }


def get_hora(jd, lat, lon):
    """
    Calculate hora (planetary hour) for a given Julian day

    Args:
        jd (float): Julian day
        lat (float): Latitude in degrees
        lon (float): Longitude in degrees

    Returns:
        dict: Dictionary with hora information
    """
    from astrovedic.ephem import ephem

    # Get date from Julian day
    date = Datetime.fromJD(jd)

    # Find the previous sunrise
    prev_sunrise = ephem.lastSunrise(date, GeoPos(lat, lon))

    # Find the next sunset
    next_sunset = ephem.nextSunset(date, GeoPos(lat, lon))

    # Find the next sunrise
    next_sunrise = ephem.nextSunrise(date, GeoPos(lat, lon))

    # Determine if it's day or night
    is_day = prev_sunrise.jd <= jd < next_sunset.jd

    # Get day of week (0 = Sunday, 1 = Monday, etc.)
    day_of_week = date.date.weekday()

    if is_day:
        # Day time calculation
        day_duration = next_sunset.jd - prev_sunrise.jd
        hora_duration = day_duration / 12
        hora_index = int((jd - prev_sunrise.jd) / hora_duration)
    else:
        # Night time calculation
        night_duration = next_sunrise.jd - next_sunset.jd
        hora_duration = night_duration / 12
        hora_index = int((jd - next_sunset.jd) / hora_duration)

    # The first hora of the day is ruled by the planet of the day
    # The sequence follows: Sun, Venus, Mercury, Moon, Saturn, Jupiter, Mars
    hora_ruler_index = (day_of_week + hora_index) % 7
    hora_ruler = HORA_RULERS[hora_ruler_index]

    return {
        'index': hora_index,
        'ruler': hora_ruler,
        'is_day': is_day
    }


def get_rahukala(jd, lat, lon, utcoffset):
    """
    Calculate Rahu Kala for a given Julian day and location

    Args:
        jd (float): Julian day
        lat (float): Latitude in degrees
        lon (float): Longitude in degrees
        utcoffset (Time): UTC offset

    Returns:
        dict: Dictionary with Rahu Kala start and end times
    """
    # Get date and weekday
    date = Datetime.fromJD(jd, utcoffset)
    # Convert flatlib dayofweek (Sun=0) to Python weekday (Mon=0)
    weekday = (date.date.dayofweek() - 1 + 7) % 7

    # Find the previous sunrise and next sunset using ephem
    prev_sunrise = ephem.lastSunrise(date, GeoPos(lat, lon))
    next_sunset = ephem.nextSunset(date, GeoPos(lat, lon))

    # Calculate day duration in JD
    day_duration = next_sunset.jd - prev_sunrise.jd

    # Rahu Kala sequence (Mon=0 to Sun=6)
    # Original flatlib sequence: [7, 1, 6, 4, 5, 3, 2] for Sun=0 index
    # Adjusted for Mon=0 index: [1, 6, 4, 5, 3, 2, 7]
    rahukala_sequence = [1, 6, 4, 5, 3, 2, 7]
    rahukala_part = rahukala_sequence[weekday]

    # Calculate Rahu Kala start and end Julian Days
    # Note: Sequence parts are 1-based for calculation (1st part to 8th part)
    rahukala_start_jd = prev_sunrise.jd + ((rahukala_part - 1) * day_duration / 8)
    rahukala_end_jd = prev_sunrise.jd + (rahukala_part * day_duration / 8)

    # Convert back to Datetime objects with the correct utcoffset
    rahukala_start = Datetime.fromJD(rahukala_start_jd, utcoffset)
    rahukala_end = Datetime.fromJD(rahukala_end_jd, utcoffset)

    return {
        'start': rahukala_start,
        'end': rahukala_end
    }


def get_yamaganda(jd, lat, lon, utcoffset):
    """
    Calculate Yamaganda Kalam for a given Julian day and location

    Args:
        jd (float): Julian day
        lat (float): Latitude in degrees
        lon (float): Longitude in degrees
        utcoffset (Time): UTC offset

    Returns:
        dict: Dictionary with Yamaganda Kalam start and end times
    """
    # Get date and weekday
    date = Datetime.fromJD(jd, utcoffset)
    # Convert flatlib dayofweek (Sun=0) to Python weekday (Mon=0)
    weekday = (date.date.dayofweek() - 1 + 7) % 7

    # Find the previous sunrise and next sunset using ephem
    prev_sunrise = ephem.lastSunrise(date, GeoPos(lat, lon))
    next_sunset = ephem.nextSunset(date, GeoPos(lat, lon))

    # Calculate day duration in JD
    day_duration = next_sunset.jd - prev_sunrise.jd

    # Yamaganda sequence (Mon=0 to Sun=6)
    # Original flatlib sequence: [1, 5, 3, 4, 2, 6, 7] for Sun=0 index
    # Adjusted for Mon=0 index: [5, 3, 4, 2, 6, 7, 1]
    yamaganda_sequence = [5, 3, 4, 2, 6, 7, 1]
    yamaganda_part = yamaganda_sequence[weekday]

    # Calculate Yamaganda start and end Julian Days
    yamaganda_start_jd = prev_sunrise.jd + ((yamaganda_part - 1) * day_duration / 8)
    yamaganda_end_jd = prev_sunrise.jd + (yamaganda_part * day_duration / 8)

    # Convert back to Datetime objects with the correct utcoffset
    yamaganda_start = Datetime.fromJD(yamaganda_start_jd, utcoffset)
    yamaganda_end = Datetime.fromJD(yamaganda_end_jd, utcoffset)

    return {
        'start': yamaganda_start,
        'end': yamaganda_end
    }


def get_gulika_kala(jd, lat, lon, utcoffset):
    """
    Calculate Gulika Kalam for a given Julian day and location

    Args:
        jd (float): Julian day
        lat (float): Latitude in degrees
        lon (float): Longitude in degrees
        utcoffset (Time): UTC offset

    Returns:
        dict: Dictionary with Gulika Kalam start and end times
    """
    # Get date and weekday
    date = Datetime.fromJD(jd, utcoffset)
    # Convert flatlib dayofweek (Sun=0) to Python weekday (Mon=0)
    weekday = (date.date.dayofweek() - 1 + 7) % 7

    # Find the previous sunrise and next sunset using ephem
    prev_sunrise = ephem.lastSunrise(date, GeoPos(lat, lon))
    next_sunset = ephem.nextSunset(date, GeoPos(lat, lon))

    # Calculate day duration in JD
    day_duration = next_sunset.jd - prev_sunrise.jd

    # Gulika sequence (Mon=0 to Sun=6)
    # Original flatlib sequence: [6, 5, 4, 3, 2, 1, 0] for Sun=0 index --> [6, 5, 4, 3, 2, 1, 7] 1-based
    # Adjusted for Mon=0 index: [5, 4, 3, 2, 1, 7, 6]
    gulika_sequence = [5, 4, 3, 2, 1, 7, 6]
    gulika_part = gulika_sequence[weekday]

    # Calculate Gulika start and end Julian Days
    gulika_start_jd = prev_sunrise.jd + ((gulika_part - 1) * day_duration / 8)
    gulika_end_jd = prev_sunrise.jd + (gulika_part * day_duration / 8)

    # Convert back to Datetime objects with the correct utcoffset
    gulika_start = Datetime.fromJD(gulika_start_jd, utcoffset)
    gulika_end = Datetime.fromJD(gulika_end_jd, utcoffset)

    return {
        'start': gulika_start,
        'end': gulika_end
    }


def get_abhijit_muhurta(jd, lat, lon, utcoffset):
    """
    Calculate Abhijit Muhurta for a given Julian day and location

    Args:
        jd (float): Julian day
        lat (float): Latitude in degrees
        lon (float): Longitude in degrees
        utcoffset (Time): UTC offset

    Returns:
        dict: Dictionary with Abhijit Muhurta start and end times
    """
    # Get date object
    date = Datetime.fromJD(jd, utcoffset)

    # Find the previous sunrise and next sunset using ephem
    prev_sunrise = ephem.lastSunrise(date, GeoPos(lat, lon))
    next_sunset = ephem.nextSunset(date, GeoPos(lat, lon))

    # Calculate day duration in JD
    day_duration = next_sunset.jd - prev_sunrise.jd

    # Calculate Abhijit Muhurta (8th muhurta of the day)
    # There are 15 muhurtas in a day, so the 8th starts after 7/15 and ends after 8/15
    abhijit_start_jd = prev_sunrise.jd + (7 * day_duration / 15)
    abhijit_end_jd = prev_sunrise.jd + (8 * day_duration / 15)

    # Convert back to Datetime objects with the correct utcoffset
    abhijit_start = Datetime.fromJD(abhijit_start_jd, utcoffset)
    abhijit_end = Datetime.fromJD(abhijit_end_jd, utcoffset)

    return {
        'start': abhijit_start,
        'end': abhijit_end
    }


def get_bhadra_karana(jd, utcoffset, ayanamsa=None):
    """
    Calculate Bhadra Karana (Vishti) timings for a given Julian day

    Vishti Karana is considered inauspicious for starting new ventures.
    It occurs 8 times in a lunar month (4 times in each paksha).

    Args:
        jd (float): Julian day
        utcoffset (Time): UTC offset
        ayanamsa (str, optional): Ayanamsa to use for sidereal calculations

    Returns:
        dict: Dictionary with Bhadra Karana information
    """
    # Get karana information for the current time
    karana_info = get_karana(jd, ayanamsa)

    # Check if current karana is Vishti (Bhadra)
    is_vishti = (karana_info['name'] == 'Vishti')

    # If not Vishti, find the next Vishti karana
    if not is_vishti:
        # Start searching from current time
        search_jd = jd
        max_iterations = 60  # Maximum number of karanas to check
        iterations = 0

        while iterations < max_iterations:
            # Add 1/60th of a day (24 minutes) to search for next karana
            search_jd += 0.016666667  # 1/60 of a day
            temp_karana = get_karana(search_jd, ayanamsa)

            if temp_karana['name'] == 'Vishti':
                # Found the next Vishti karana
                karana_info = temp_karana
                is_vishti = True
                break

            iterations += 1

    # If we found Vishti, calculate its start and end times
    if is_vishti:
        # Get the phase angle at the current time
        phase_angle = angle.norm(swe.sweObjectLon(const.MOON, jd) - swe.sweObjectLon(const.SUN, jd))

        # Calculate the karana index (0-59)
        karana_index = int(phase_angle / 6)

        # Calculate the start of the current karana
        karana_start_angle = karana_index * 6

        # Find the Julian day when the phase angle was at the start of the karana
        # Use binary search to find the exact time
        start_jd = jd - (phase_angle - karana_start_angle) * 0.0175  # Approximate conversion

        # Refine the start time using binary search
        lower_jd = start_jd - 0.1
        upper_jd = start_jd + 0.1

        for _ in range(10):  # 10 iterations should be enough for precision
            mid_jd = (lower_jd + upper_jd) / 2
            mid_angle = angle.norm(swe.sweObjectLon(const.MOON, mid_jd) - swe.sweObjectLon(const.SUN, mid_jd))

            if mid_angle < karana_start_angle:
                lower_jd = mid_jd
            else:
                upper_jd = mid_jd

        karana_start_jd = upper_jd

        # Calculate the end of the current karana (start + 6 degrees)
        karana_end_angle = karana_start_angle + 6

        # Find the Julian day when the phase angle will be at the end of the karana
        end_jd = jd + (karana_end_angle - phase_angle) * 0.0175  # Approximate conversion

        # Refine the end time using binary search
        lower_jd = end_jd - 0.1
        upper_jd = end_jd + 0.1

        for _ in range(10):  # 10 iterations should be enough for precision
            mid_jd = (lower_jd + upper_jd) / 2
            mid_angle = angle.norm(swe.sweObjectLon(const.MOON, mid_jd) - swe.sweObjectLon(const.SUN, mid_jd))

            if mid_angle < karana_end_angle:
                lower_jd = mid_jd
            else:
                upper_jd = mid_jd

        karana_end_jd = upper_jd

        # Convert to Datetime objects
        karana_start = Datetime.fromJD(karana_start_jd, utcoffset)
        karana_end = Datetime.fromJD(karana_end_jd, utcoffset)

        return {
            'is_vishti': True,
            'start': karana_start,
            'end': karana_end,
            'karana_index': karana_index
        }
    else:
        # Couldn't find Vishti karana in the search range
        return {
            'is_vishti': False,
            'karana_index': karana_info['index']
        }


def get_panchaka_dosha(jd, ayanamsa=None):
    """
    Calculate Panchaka Dosha for a given Julian day

    Panchaka Dosha is considered inauspicious for certain activities.
    It is based on the Nakshatra of the Moon.

    Args:
        jd (float): Julian day
        ayanamsa (str, optional): Ayanamsa to use for sidereal calculations

    Returns:
        dict: Dictionary with Panchaka Dosha information
    """
    # Get nakshatra information
    nakshatra_info = get_nakshatra(jd, ayanamsa)
    nakshatra_index = nakshatra_info['index']

    # Panchaka Dosha occurs in the following nakshatras (0-based index):
    # Dhanishta (23), Shatabhisha (24), Purva Bhadrapada (25), Uttara Bhadrapada (26), Revati (27)
    panchaka_nakshatras = [23, 24, 25, 26, 27]

    # Check if current nakshatra is in the Panchaka Dosha list
    is_panchaka_dosha = nakshatra_index in panchaka_nakshatras

    # Determine the type of Panchaka Dosha
    panchaka_type = None
    if is_panchaka_dosha:
        # Mrityu (Death) - Dhanishta
        if nakshatra_index == 23:
            panchaka_type = "Mrityu Panchaka"
        # Agni (Fire) - Shatabhisha
        elif nakshatra_index == 24:
            panchaka_type = "Agni Panchaka"
        # Raja (King) - Purva Bhadrapada
        elif nakshatra_index == 25:
            panchaka_type = "Raja Panchaka"
        # Chora (Thief) - Uttara Bhadrapada
        elif nakshatra_index == 26:
            panchaka_type = "Chora Panchaka"
        # Roga (Disease) - Revati
        elif nakshatra_index == 27:
            panchaka_type = "Roga Panchaka"

    return {
        'is_panchaka_dosha': is_panchaka_dosha,
        'type': panchaka_type,
        'nakshatra': nakshatra_info['name'] if is_panchaka_dosha else None
    }


def get_chandra_bala(jd, natal_moon_house, ayanamsa=None):
    """
    Calculate Chandra Bala (Moon's strength) for a given Julian day

    Chandra Bala is the strength of the Moon based on its position
    relative to the natal Moon's house.

    Args:
        jd (float): Julian day
        natal_moon_house (int): The house (1-12) of the natal Moon
        ayanamsa (str, optional): Ayanamsa to use for sidereal calculations

    Returns:
        dict: Dictionary with Chandra Bala information
    """
    # Get current Moon longitude
    moon_lon = swe.sweObjectLon(const.MOON, jd)

    # If ayanamsa is provided, convert to sidereal
    if ayanamsa:
        ayanamsa_val = swe.get_ayanamsa(jd, ayanamsa)
        moon_lon = angle.norm(moon_lon - ayanamsa_val)

    # Calculate the current house of the Moon (1-12)
    current_moon_house = (int(moon_lon / 30) + 1)

    # Calculate the distance from natal Moon's house (1-12)
    house_distance = ((current_moon_house - natal_moon_house) % 12) + 1

    # Determine the strength of Chandra Bala
    # Houses 3, 6, 10, 11 from natal Moon are considered strong
    # Houses 1, 2, 4, 5, 7, 8, 9, 12 from natal Moon are considered weak
    strong_houses = [3, 6, 10, 11]
    is_strong = house_distance in strong_houses

    # Calculate the strength percentage (subjective scale)
    if house_distance in [3, 11]:
        strength = 100  # Very strong
    elif house_distance in [6, 10]:
        strength = 75   # Strong
    elif house_distance in [2, 5, 9]:
        strength = 50   # Moderate
    elif house_distance in [1, 7]:
        strength = 25   # Weak
    else:  # 4, 8, 12
        strength = 0    # Very weak

    return {
        'natal_moon_house': natal_moon_house,
        'current_moon_house': current_moon_house,
        'house_distance': house_distance,
        'is_strong': is_strong,
        'strength': strength
    }


def get_panchang(jd, lat, lon, utcoffset, ayanamsa=None):
    """
    Calculate complete Panchang for a given Julian day

    Args:
        jd (float): Julian day
        lat (float): Latitude in degrees
        lon (float): Longitude in degrees
        utcoffset (Time): UTC offset
        ayanamsa (str, optional): Ayanamsa to use for sidereal calculations

    Returns:
        dict: Dictionary with complete Panchang information
    """
    # Get date from Julian day
    date = Datetime.fromJD(jd, utcoffset)

    # Calculate all Panchang elements
    tithi_info = get_tithi(jd, ayanamsa)
    nakshatra_info = get_nakshatra(jd, ayanamsa)
    yoga_info = get_yoga(jd, ayanamsa)
    karana_info = get_karana(jd, ayanamsa)
    vara_info = get_vara(jd)

    # Calculate inauspicious periods
    rahukala_info = get_rahukala(jd, lat, lon, utcoffset)
    yamaganda_info = get_yamaganda(jd, lat, lon, utcoffset)
    gulika_kala_info = get_gulika_kala(jd, lat, lon, utcoffset)
    bhadra_karana_info = get_bhadra_karana(jd, utcoffset, ayanamsa)
    panchaka_dosha_info = get_panchaka_dosha(jd, ayanamsa)

    # Calculate auspicious periods
    abhijit_muhurta_info = get_abhijit_muhurta(jd, lat, lon, utcoffset)

    return {
        'date': date,
        'tithi': tithi_info,
        'nakshatra': nakshatra_info,
        'yoga': yoga_info,
        'karana': karana_info,
        'vara': vara_info,
        'rahukala': rahukala_info,
        'yamaganda': yamaganda_info,
        'gulika_kala': gulika_kala_info,
        'bhadra_karana': bhadra_karana_info,
        'panchaka_dosha': panchaka_dosha_info,
        'abhijit_muhurta': abhijit_muhurta_info
    }


def get_nakshatra(jd, ayanamsa=None):
    """
    Calculate nakshatra for a given Julian day

    Args:
        jd (float): Julian day
        ayanamsa (str, optional): Ayanamsa to use for sidereal calculations

    Returns:
        dict: Dictionary with nakshatra information
    """
    from astrovedic.vedic.nakshatras import get_nakshatra as get_nak

    # Get Moon longitude
    moon_lon = swe.sweObjectLon(const.MOON, jd)

    # If ayanamsa is provided, convert to sidereal
    if ayanamsa:
        ayanamsa_val = swe.get_ayanamsa(jd, ayanamsa)
        moon_lon = angle.norm(moon_lon - ayanamsa_val)

    # Get nakshatra information
    nakshatra_info = get_nak(moon_lon)

    return nakshatra_info
