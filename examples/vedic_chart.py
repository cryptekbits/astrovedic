#!/usr/bin/env python3
"""
Vedic Chart Example

This script demonstrates how to use flatlib for Vedic astrology calculations.
It includes:
- Planetary positions with Lahiri ayanamsa
- Nakshatra positions
- Shadow planets (upagrah)
- Additional Vedic bodies

Usage:
  python vedic_chart.py                   # Generate chart for current time
  python vedic_chart.py YYYY/MM/DD HH:MM  # Generate chart for specific date and time
  python vedic_chart.py -h, --help        # Show help message
"""

import sys
import datetime
from tabulate import tabulate

from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib.vedic.nakshatras import get_nakshatra
from flatlib.vedic.upagrah import get_upagrah
# Removed import of get_vedic_body

# Default location: Bangalore, India
DEFAULT_LAT = 12.9716
DEFAULT_LON = 77.5946
DEFAULT_LOCATION = "Bangalore, India"

def get_chart(date_str=None, time_str=None, lat=DEFAULT_LAT, lon=DEFAULT_LON):
    """
    Create a chart for the given date, time, and location

    Args:
        date_str (str, optional): Date in format YYYY/MM/DD
        time_str (str, optional): Time in format HH:MM
        lat (float, optional): Latitude in degrees
        lon (float, optional): Longitude in degrees

    Returns:
        Chart: Flatlib Chart object
    """
    # If no date is provided, use current date
    if not date_str:
        now = datetime.datetime.now()
        date_str = now.strftime("%Y/%m/%d")
        time_str = now.strftime("%H:%M")
    elif not time_str:
        time_str = "12:00"

    # Create date and location objects
    date = Datetime(date_str, time_str, '+05:30')  # Indian Standard Time
    pos = GeoPos(lat, lon)

    # Create chart with Lahiri ayanamsa and Whole Sign houses
    chart = Chart(date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)

    return chart

def print_vedic_chart(chart):
    """
    Print the Vedic chart for the given chart

    Args:
        chart (Chart): Flatlib Chart object
    """
    # Get date and location
    date = chart.date
    pos = chart.pos

    # Print header
    print(f"\n{'=' * 60}")
    print(f"VEDIC CHART FOR {date.date} {date.time} ({DEFAULT_LOCATION})")
    print(f"Ayanamsa: {chart.mode}, House System: {chart.hsys}")
    print(f"{'=' * 60}\n")

    # Print planetary positions
    planets = [
        const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS,
        const.JUPITER, const.SATURN, const.RAHU, const.KETU
    ]

    planet_data = []
    for planet_id in planets:
        planet = chart.getObject(planet_id)
        nakshatra_info = get_nakshatra(planet.lon)

        # Format position
        position = f"{planet.sign} {planet.signlon:.2f}°"

        # Format nakshatra
        nakshatra = f"{nakshatra_info['name']} (Pada {nakshatra_info['pada']})"

        # Get house
        house = chart.houses.getHouseByLon(planet.lon)
        house_num = house.num() if house else 0

        planet_data.append([
            planet.id,
            position,
            f"House {house_num}",
            nakshatra,
            nakshatra_info['lord'],
            nakshatra_info['element']
        ])

    print("PLANETARY POSITIONS:")
    print(tabulate(planet_data, headers=["Planet", "Position", "House", "Nakshatra", "Nakshatra Lord", "Element"], tablefmt="grid"))
    print()

    # Print shadow planets (upagrah)
    shadow_planets = [
        const.GULIKA, const.MANDI, const.DHUMA, const.VYATIPATA,
        const.PARIVESHA, const.INDRACHAPA, const.UPAKETU
    ]

    shadow_data = []
    for upagrah_id in shadow_planets:
        try:
            if upagrah_id in [const.GULIKA, const.MANDI]:
                upagrah = get_upagrah(upagrah_id, date.jd, pos.lat, pos.lon)
            else:
                upagrah = get_upagrah(upagrah_id, date.jd)

            position = f"{upagrah['sign']} {upagrah['signlon']:.2f}°"
            nakshatra_info = get_nakshatra(upagrah['lon'])
            nakshatra = f"{nakshatra_info['name']} (Pada {nakshatra_info['pada']})"

            # Get house
            house = chart.houses.getHouseByLon(upagrah['lon'])
            house_num = house.num() if house else 0

            shadow_data.append([
                upagrah_id,
                position,
                f"House {house_num}",
                nakshatra
            ])
        except Exception as e:
            shadow_data.append([
                upagrah_id,
                f"Error: {e}",
                "",
                ""
            ])

    print("SHADOW PLANETS (UPAGRAH):")
    print(tabulate(shadow_data, headers=["Upagrah", "Position", "House", "Nakshatra"], tablefmt="grid"))
    print()

    # Print outer planets
    outer_planets = [
        const.URANUS, const.NEPTUNE, const.PLUTO
    ]

    outer_planets_data = []
    for planet_id in outer_planets:
        try:
            planet = chart.getObject(planet_id)
            position = f"{planet.sign} {planet.signlon:.2f}°"
            nakshatra_info = get_nakshatra(planet.lon)
            nakshatra = f"{nakshatra_info['name']} (Pada {nakshatra_info['pada']})"

            # Get house
            house = chart.houses.getHouseByLon(planet.lon)
            house_num = house.num() if house else 0

            outer_planets_data.append([
                planet_id,
                position,
                f"House {house_num}",
                nakshatra
            ])
        except Exception as e:
            outer_planets_data.append([
                planet_id,
                f"Error: {e}",
                "",
                ""
            ])

    print("OUTER PLANETS:")
    print(tabulate(outer_planets_data, headers=["Planet", "Position", "House", "Nakshatra"], tablefmt="grid"))
    print()

def main():
    """Main function"""
    # Check if date is provided as command line argument
    if len(sys.argv) >= 2:
        if sys.argv[1] in ['-h', '--help']:
            print(__doc__)
            return

        date_str = sys.argv[1]
        time_str = sys.argv[2] if len(sys.argv) >= 3 else None

        try:
            chart = get_chart(date_str, time_str)
            print(f"Generating Vedic chart for {date_str} {time_str or '12:00'} in {DEFAULT_LOCATION}")
        except Exception as e:
            print(f"Error: {e}")
            print("Please use the format: YYYY/MM/DD HH:MM (e.g., 2025/04/09 20:51)")
            return
    else:
        # Use current date
        chart = get_chart()
        print(f"Generating Vedic chart for current time in {DEFAULT_LOCATION}")

    # Print Vedic chart
    print_vedic_chart(chart)

if __name__ == "__main__":
    main()
