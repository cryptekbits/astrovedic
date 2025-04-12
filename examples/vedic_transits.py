#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Example script demonstrating how to use the Vedic transit calculator.
"""

from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const
from flatlib.ephem import eph
from flatlib.vedic.transits import calculator


def main():
    """Main function demonstrating Vedic transit calculations."""

    # Create a datetime and location
    dt = Datetime('2025/04/09', '20:51', '+05:30')  # April 9, 2025 at 20:51 in Bangalore
    pos = GeoPos('12n58', '77e35')  # Bangalore

    print("Reference date:", dt)
    print("Location:", pos)
    print("\n" + "=" * 50 + "\n")

    # Calculate when Sun will enter Taurus
    sun_taurus = calculator.next_sign_transit(const.SUN, dt, const.TAURUS, const.AY_LAHIRI)
    print(f"Sun enters Taurus on: {sun_taurus}")

    # Calculate when Moon will enter next nakshatra
    moon_data = calculator.next_nakshatra_transit(const.MOON, dt, 'Krittika', const.AY_LAHIRI)
    print(f"Moon enters Krittika nakshatra on: {moon_data}")

    # Calculate when Sun will reach a specific degree (Mercury's position + 10°)
    mercury_data = eph.get_object(const.MERCURY, dt.jd, mode=const.AY_LAHIRI)
    mercury_lon = mercury_data['lon']
    target_lon = (mercury_lon + 10) % 360  # 10 degrees ahead of Mercury
    sun_transit = calculator.next_degree_transit(const.SUN, dt, target_lon, const.AY_LAHIRI)
    print(f"Sun reaches {target_lon:.2f}° (Mercury's position + 10°) on: {sun_transit}")

    # Calculate when Mercury will station (turn retrograde or direct)
    mercury_station_dt, station_type = calculator.next_station(const.MERCURY, dt, const.AY_LAHIRI)
    station_type_name = "retrograde" if station_type == 'R' else "direct"
    print(f"Mercury turns {station_type_name} on: {mercury_station_dt}")

    # Calculate when Sun will reach a specific degree
    sun_degree = calculator.next_degree_transit(const.SUN, dt, 15, const.AY_LAHIRI)
    print(f"Sun reaches 15° on: {sun_degree}")

    print("\n" + "=" * 50 + "\n")
    print("Transit calculations complete!")


if __name__ == "__main__":
    main()
