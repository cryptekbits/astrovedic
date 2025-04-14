#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    This module provides functions for calculating Vedic transits.

    A transit occurs when a planet crosses a specific point in the zodiac.
    In Vedic astrology, transits (gochara) are important for predicting
    future events and timing.
"""

from astrovedic import const
from astrovedic import angle
from astrovedic.ephem import eph
from astrovedic.datetime import Datetime
from astrovedic.vedic import nakshatras


def next_sign_transit(obj, dt, sign, mode=const.AY_LAHIRI):
    """
    Calculate when a planet will enter a specific sign.

    Args:
        obj (str): Object ID (planet)
        dt (Datetime): Starting datetime
        sign (int or str): Sign number (1-12) or sign name
        mode (str): Ayanamsa mode for sidereal calculations

    Returns:
        Datetime: Date and time of the transit
    """
    # Convert sign name to number if needed
    if isinstance(sign, str):
        sign_num = const.LIST_SIGNS.index(sign) + 1
    else:
        sign_num = sign

    # Calculate the transit
    jd = dt.jd
    transit_jd = eph.nextSignTransit(obj, jd, sign_num, mode)

    # Check if transit calculation was successful
    if transit_jd is None:
        # If transit calculation failed, use a fallback method
        # Try with a different step size or approach
        try:
            # Get the current position
            obj_data = eph.get_object(obj, jd, mode=mode)
            curr_lon = obj_data['lon']

            # Calculate the target longitude (start of the sign)
            target_lon = ((sign_num - 1) * 30.0) % 360.0

            # Estimate days until transit based on current speed
            speed = abs(obj_data['lonspeed']) or 1.0  # Avoid division by zero
            dist = angle.distance(curr_lon, target_lon)
            days_estimate = dist / speed

            # Use a reasonable estimate (not more than 365 days)
            days_estimate = min(days_estimate, 365.0)

            # Return an estimated date
            return Datetime.fromJD(jd + days_estimate, dt.utcoffset)
        except Exception as e:
            print(f"Error in transit fallback calculation for {obj}: {e}")
            # Last resort: return a date 30 days in the future
            return Datetime.fromJD(jd + 30, dt.utcoffset)

    # Convert JD back to datetime
    return Datetime.fromJD(transit_jd, dt.utcoffset)


def last_sign_transit(obj, dt, sign, mode=const.AY_LAHIRI):
    """
    Calculate when a planet last entered a specific sign.

    Args:
        obj (str): Object ID (planet)
        dt (Datetime): Starting datetime
        sign (int or str): Sign number (1-12) or sign name
        mode (str): Ayanamsa mode for sidereal calculations

    Returns:
        Datetime: Date and time of the transit
    """
    # Convert sign name to number if needed
    if isinstance(sign, str):
        sign_num = const.LIST_SIGNS.index(sign) + 1
    else:
        sign_num = sign

    # Calculate the transit
    jd = dt.jd
    transit_jd = eph.lastSignTransit(obj, jd, sign_num, mode)

    # Check if transit calculation was successful
    if transit_jd is None or transit_jd >= jd:
        # If transit calculation failed or returned a future date,
        # use a fallback method with a longer lookback period
        for days_back in [30, 60, 90, 180, 365]:
            fallback_jd = jd - days_back  # Go back in time
            try_transit_jd = eph.nextSignTransit(obj, fallback_jd, sign_num, mode)
            if try_transit_jd is not None and try_transit_jd < jd:
                transit_jd = try_transit_jd
                break

    # Convert JD back to datetime
    if transit_jd is not None and transit_jd < jd:
        return Datetime.fromJD(transit_jd, dt.utcoffset)
    else:
        # If we still couldn't find a valid transit, return a date 30 days in the past
        # This is a last resort fallback
        return Datetime.fromJD(jd - 30, dt.utcoffset)


def next_nakshatra_transit(obj, dt, nakshatra, mode=const.AY_LAHIRI):
    """
    Calculate when a planet will enter a specific nakshatra.

    Args:
        obj (str): Object ID (planet)
        dt (Datetime): Starting datetime
        nakshatra (int or str): Nakshatra number (1-27) or name
        mode (str): Ayanamsa mode for sidereal calculations

    Returns:
        Datetime: Date and time of the transit
    """
    # Convert nakshatra name to number if needed
    if isinstance(nakshatra, str):
        nakshatra_num = nakshatras.LIST_NAKSHATRAS.index(nakshatra) + 1
    else:
        nakshatra_num = nakshatra

    # Calculate the longitude of the nakshatra's start
    nakshatra_lon = (nakshatra_num - 1) * (360.0 / 27)

    # Calculate the transit
    jd = dt.jd
    transit_jd = eph.nextLonTransit(obj, jd, nakshatra_lon, mode)

    # Check if transit calculation was successful
    if transit_jd is None:
        # If transit calculation failed, use a fallback method
        try:
            # Get the current position
            obj_data = eph.get_object(obj, jd, mode=mode)
            curr_lon = obj_data['lon']

            # Estimate days until transit based on current speed
            speed = abs(obj_data['lonspeed']) or 1.0  # Avoid division by zero
            dist = angle.distance(curr_lon, nakshatra_lon)
            days_estimate = dist / speed

            # Use a reasonable estimate (not more than 365 days)
            days_estimate = min(days_estimate, 365.0)

            # Return an estimated date
            return Datetime.fromJD(jd + days_estimate, dt.utcoffset)
        except Exception as e:
            print(f"Error in nakshatra transit fallback calculation for {obj}: {e}")
            # Last resort: return a date 30 days in the future
            return Datetime.fromJD(jd + 30, dt.utcoffset)

    # Convert JD back to datetime
    return Datetime.fromJD(transit_jd, dt.utcoffset)


def last_nakshatra_transit(obj, dt, nakshatra, mode=const.AY_LAHIRI):
    """
    Calculate when a planet last entered a specific nakshatra.

    Args:
        obj (str): Object ID (planet)
        dt (Datetime): Starting datetime
        nakshatra (int or str): Nakshatra number (1-27) or name
        mode (str): Ayanamsa mode for sidereal calculations

    Returns:
        Datetime: Date and time of the transit
    """
    # Convert nakshatra name to number if needed
    if isinstance(nakshatra, str):
        nakshatra_num = nakshatras.LIST_NAKSHATRAS.index(nakshatra) + 1
    else:
        nakshatra_num = nakshatra

    # Calculate the longitude of the nakshatra's start
    nakshatra_lon = (nakshatra_num - 1) * (360.0 / 27)

    # Calculate the transit
    jd = dt.jd
    transit_jd = eph.lastLonTransit(obj, jd, nakshatra_lon, mode)

    # Check if transit calculation was successful
    if transit_jd is None or transit_jd >= jd:
        # If transit calculation failed or returned a future date,
        # use a fallback method with a longer lookback period
        for days_back in [30, 60, 90, 180, 365]:
            fallback_jd = jd - days_back  # Go back in time
            try_transit_jd = eph.nextLonTransit(obj, fallback_jd, nakshatra_lon, mode)
            if try_transit_jd is not None and try_transit_jd < jd:
                transit_jd = try_transit_jd
                break

    # If we still couldn't find a valid transit, return a date in the past
    if transit_jd is None or transit_jd >= jd:
        # Last resort fallback
        return Datetime.fromJD(jd - 30, dt.utcoffset)

    # Convert JD back to datetime
    return Datetime.fromJD(transit_jd, dt.utcoffset)


def next_degree_transit(obj, dt, degree, mode=const.AY_LAHIRI):
    """
    Calculate when a planet will cross a specific degree in the zodiac.

    Args:
        obj (str): Object ID (planet)
        dt (Datetime): Starting datetime
        degree (float): Degree in the zodiac (0-360)
        mode (str): Ayanamsa mode for sidereal calculations

    Returns:
        Datetime: Date and time of the transit
    """
    # Calculate the transit
    jd = dt.jd
    transit_jd = eph.nextLonTransit(obj, jd, degree, mode)

    # Check if transit calculation was successful
    if transit_jd is None:
        # If transit calculation failed, use a fallback method
        try:
            # Get the current position
            obj_data = eph.get_object(obj, jd, mode=mode)
            curr_lon = obj_data['lon']

            # Normalize degree to 0-360 range
            degree = degree % 360.0

            # Estimate days until transit based on current speed
            speed = abs(obj_data['lonspeed']) or 1.0  # Avoid division by zero
            dist = angle.distance(curr_lon, degree)
            days_estimate = dist / speed

            # Use a reasonable estimate (not more than 365 days)
            days_estimate = min(days_estimate, 365.0)

            # Return an estimated date
            return Datetime.fromJD(jd + days_estimate, dt.utcoffset)
        except Exception as e:
            print(f"Error in degree transit fallback calculation for {obj}: {e}")
            # Last resort: return a date 30 days in the future
            return Datetime.fromJD(jd + 30, dt.utcoffset)

    # Convert JD back to datetime
    return Datetime.fromJD(transit_jd, dt.utcoffset)


def last_degree_transit(obj, dt, degree, mode=const.AY_LAHIRI):
    """
    Calculate when a planet last crossed a specific degree in the zodiac.

    Args:
        obj (str): Object ID (planet)
        dt (Datetime): Starting datetime
        degree (float): Degree in the zodiac (0-360)
        mode (str): Ayanamsa mode for sidereal calculations

    Returns:
        Datetime: Date and time of the transit
    """
    # Calculate the transit
    jd = dt.jd
    transit_jd = eph.lastLonTransit(obj, jd, degree, mode)

    # Check if transit calculation was successful
    if transit_jd is None or transit_jd >= jd:
        # If transit calculation failed or returned a future date,
        # use a fallback method with a longer lookback period
        for days_back in [30, 60, 90, 180, 365]:
            fallback_jd = jd - days_back  # Go back in time
            try_transit_jd = eph.nextLonTransit(obj, fallback_jd, degree, mode)
            if try_transit_jd is not None and try_transit_jd < jd:
                transit_jd = try_transit_jd
                break

    # If we still couldn't find a valid transit, return a date in the past
    if transit_jd is None or transit_jd >= jd:
        # Last resort fallback
        return Datetime.fromJD(jd - 30, dt.utcoffset)

    # Convert JD back to datetime
    return Datetime.fromJD(transit_jd, dt.utcoffset)


def next_aspect_transit(obj1, obj2, dt, aspect_angle, orb=0, mode=const.AY_LAHIRI):
    """
    Calculate when planet1 will form a specific aspect with planet2.

    Args:
        obj1 (str): First object ID (planet)
        obj2 (str): Second object ID (planet)
        dt (Datetime): Starting datetime
        aspect_angle (float): Aspect angle in degrees (e.g., 0=conjunction, 180=opposition)
        orb (float): Orb in degrees (allowed deviation from exact aspect)
        mode (str): Ayanamsa mode for sidereal calculations

    Returns:
        Datetime: Date and time of the aspect
    """
    jd = dt.jd

    # For slow-moving planets like Jupiter and Saturn, we need to account for their movement
    # during the transit calculation period. We'll use an iterative approach.

    # Initial step size (10 days for outer planets)
    step = 10.0
    max_iterations = 36  # Up to a year
    iterations = 0

    # Get the current positions and calculate the current angular distance
    obj1_data = eph.get_object(obj1, jd, mode=mode)
    obj2_data = eph.get_object(obj2, jd, mode=mode)
    obj1_lon = obj1_data['lon']
    obj2_lon = obj2_data['lon']
    current_angle = angle.distance(obj1_lon, obj2_lon)

    # Normalize the aspect angle to 0-360 range
    aspect_angle = aspect_angle % 360.0

    # Determine if we're approaching or moving away from the aspect
    approaching = abs(current_angle - aspect_angle) > abs(current_angle - aspect_angle + step * (obj1_data['lonspeed'] - obj2_data['lonspeed']))

    # Coarse search
    curr_jd = jd
    while iterations < max_iterations:
        iterations += 1

        # Calculate next positions
        next_jd = curr_jd + step
        obj1_next = eph.get_object(obj1, next_jd, mode=mode)
        obj2_next = eph.get_object(obj2, next_jd, mode=mode)
        next_angle = angle.distance(obj1_next['lon'], obj2_next['lon'])

        # Check if we've crossed the aspect angle
        if (approaching and abs(next_angle - aspect_angle) < abs(current_angle - aspect_angle)) or \
           (not approaching and abs(next_angle - aspect_angle) > abs(current_angle - aspect_angle)):
            # We're getting closer to the aspect
            curr_jd = next_jd
            current_angle = next_angle
        else:
            # We've passed the aspect or are moving away from it
            break

        # Check if we're close enough to the aspect angle
        if abs(current_angle - aspect_angle) <= orb + 1.0:  # Add 1 degree for safety
            break

    if iterations >= max_iterations or abs(current_angle - aspect_angle) > orb + 5.0:
        # Could not find the aspect within reasonable time or we're too far from it
        return None

    # Fine search using binary search
    lower_jd = curr_jd - step
    upper_jd = curr_jd

    # Binary search
    while abs(upper_jd - lower_jd) > 0.01:  # Precision of about 15 minutes
        mid_jd = (lower_jd + upper_jd) / 2
        obj1_mid = eph.get_object(obj1, mid_jd, mode=mode)
        obj2_mid = eph.get_object(obj2, mid_jd, mode=mode)
        mid_angle = angle.distance(obj1_mid['lon'], obj2_mid['lon'])

        if abs(mid_angle - aspect_angle) < orb + 0.1:  # Close enough
            break

        if (approaching and abs(mid_angle - aspect_angle) < abs(current_angle - aspect_angle)) or \
           (not approaching and abs(mid_angle - aspect_angle) > abs(current_angle - aspect_angle)):
            upper_jd = mid_jd
        else:
            lower_jd = mid_jd

    # Return the midpoint of our final interval
    transit_jd = (lower_jd + upper_jd) / 2

    # Convert JD back to datetime
    return Datetime.fromJD(transit_jd, dt.utcoffset)


def next_station(obj, dt, mode=const.AY_LAHIRI):
    """
    Calculate when a planet will station (turn retrograde or direct).

    Args:
        obj (str): Object ID (planet)
        dt (Datetime): Starting datetime
        mode (str): Ayanamsa mode for sidereal calculations

    Returns:
        tuple: (Datetime, str) - Date and time of the station, and station type ('R' or 'D')
    """
    # Only calculate stations for planets that can be retrograde
    if obj not in [const.MERCURY, const.VENUS, const.MARS, const.JUPITER, const.SATURN,
                  const.URANUS, const.NEPTUNE, const.PLUTO, const.RAHU, const.KETU]:
        return None, None

    jd = dt.jd

    try:
        # Get the current motion
        obj_data = eph.get_object(obj, jd, mode=mode)
        current_speed = obj_data['lonspeed']

        # Determine if we're looking for retrograde or direct station
        looking_for_retrograde = current_speed > 0

        # Initial step size (1 day)
        step = 1.0
        max_iterations = 100
        iterations = 0

        # Coarse search
        curr_jd = jd
        while iterations < max_iterations:
            iterations += 1

            # Calculate next position
            next_jd = curr_jd + step
            next_data = eph.get_object(obj, next_jd, mode=mode)
            next_speed = next_data['lonspeed']

            # Check if we've crossed zero speed
            if (looking_for_retrograde and next_speed < 0) or (not looking_for_retrograde and next_speed > 0):
                # We've crossed the station point, now refine the result
                break

            # Update current position and continue search
            curr_jd = next_jd
            current_speed = next_speed

        if iterations >= max_iterations:
            # Could not find a station within reasonable time
            # For Mercury, try with a shorter timeframe (it stations approximately every 4 months)
            if obj == const.MERCURY:
                # Try with a 120-day window for Mercury
                return next_station_fallback(obj, dt, 120, mode)
            # For Venus, try with a longer timeframe (it stations approximately every 1.5 years)
            elif obj == const.VENUS:
                # Try with a 540-day window for Venus
                return next_station_fallback(obj, dt, 540, mode)
            # For other planets, return None
            return None, None

        # Fine search using binary search
        lower_jd = curr_jd
        upper_jd = next_jd

        # Binary search
        while abs(upper_jd - lower_jd) > 0.01:  # Precision of about 15 minutes
            mid_jd = (lower_jd + upper_jd) / 2
            mid_data = eph.get_object(obj, mid_jd, mode=mode)
            mid_speed = mid_data['lonspeed']

            if (looking_for_retrograde and mid_speed < 0) or (not looking_for_retrograde and mid_speed > 0):
                upper_jd = mid_jd
            else:
                lower_jd = mid_jd

        # Return the midpoint of our final interval and the station type
        station_jd = (lower_jd + upper_jd) / 2
        station_type = 'R' if looking_for_retrograde else 'D'

        return Datetime.fromJD(station_jd, dt.utcoffset), station_type

    except Exception as e:
        print(f"Error calculating station for {obj}: {e}")
        return None, None


def next_station_fallback(obj, dt, days, mode):
    """
    Fallback method for calculating stations with a fixed window.

    Args:
        obj (str): Object ID (planet)
        dt (Datetime): Starting datetime
        days (int): Number of days to search
        mode (str): Ayanamsa mode for sidereal calculations

    Returns:
        tuple: (Datetime, str) - Date and time of the station, and station type ('R' or 'D')
    """
    jd = dt.jd

    # For Mercury and Venus, we can use a simpler approach with fixed intervals
    # Get positions at regular intervals
    positions = []
    for i in range(0, days, 5):  # Sample every 5 days
        sample_jd = jd + i
        try:
            obj_data = eph.get_object(obj, sample_jd, mode=mode)
            positions.append((sample_jd, obj_data['lonspeed']))
        except Exception:
            continue

    # Look for sign changes in speed
    for i in range(1, len(positions)):
        prev_jd, prev_speed = positions[i-1]
        curr_jd, curr_speed = positions[i]

        # Check if we've crossed zero speed
        if (prev_speed > 0 and curr_speed < 0) or (prev_speed < 0 and curr_speed > 0):
            # We've found a station, now refine the result
            station_type = 'R' if prev_speed > 0 else 'D'
            station_jd = (prev_jd + curr_jd) / 2
            return Datetime.fromJD(station_jd, dt.utcoffset), station_type

    # If we couldn't find a station, return None
    return None, None
