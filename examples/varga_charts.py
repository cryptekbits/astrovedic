#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Example script demonstrating how to use Varga (divisional) charts.
"""

from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic import const
from astrovedic.vedic.vargas import (
    D1, D2, D3, D4, D7, D9, D10, D12,
    D16, D20, D24, D27, D30, D40, D45, D60,
    get_varga_chart, get_varga_longitude
)


def main():
    """Main function demonstrating Varga chart calculations."""

    # Create a datetime and location
    dt = Datetime('2025/04/09', '20:51', '+05:30')  # April 9, 2025 at 20:51 in Bangalore
    pos = GeoPos('12n58', '77e35')  # Bangalore

    print("Reference date:", dt)
    print("Location:", pos)
    print("\n" + "=" * 50 + "\n")

    # Create the birth chart (D1)
    birth_chart = Chart(dt, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)

    # Get the planets we want to analyze
    planets = [
        birth_chart.getObject(const.SUN),
        birth_chart.getObject(const.MOON),
        birth_chart.getObject(const.MERCURY),
        birth_chart.getObject(const.VENUS),
        birth_chart.getObject(const.MARS),
        birth_chart.getObject(const.JUPITER),
        birth_chart.getObject(const.SATURN),
        birth_chart.getObject(const.RAHU),
        birth_chart.getObject(const.KETU)
    ]

    # Print the birth chart positions
    print("BIRTH CHART (D1) POSITIONS:")
    for planet in planets:
        sign_num = int(planet.lon / 30) + 1
        sign_name = const.LIST_SIGNS[sign_num - 1]
        degrees = planet.lon % 30
        print(f"{planet.id}: {sign_name} {degrees:.2f}°")

    print("\n" + "=" * 50 + "\n")

    # Create and print the Navamsha (D9) chart
    print("NAVAMSHA CHART (D9) POSITIONS:")
    navamsha_chart = get_varga_chart(birth_chart, D9)

    for planet in planets:
        # Get the corresponding planet in the Navamsha chart
        d9_planet = navamsha_chart.getObject(planet.id)
        sign_num = int(d9_planet.lon / 30) + 1
        sign_name = const.LIST_SIGNS[sign_num - 1]
        degrees = d9_planet.lon % 30
        print(f"{d9_planet.id}: {sign_name} {degrees:.2f}°")

    print("\n" + "=" * 50 + "\n")

    # Create and print the Dashamsha (D10) chart
    print("DASHAMSHA CHART (D10) POSITIONS:")
    dashamsha_chart = get_varga_chart(birth_chart, D10)

    for planet in planets:
        # Get the corresponding planet in the Dashamsha chart
        d10_planet = dashamsha_chart.getObject(planet.id)
        sign_num = int(d10_planet.lon / 30) + 1
        sign_name = const.LIST_SIGNS[sign_num - 1]
        degrees = d10_planet.lon % 30
        print(f"{d10_planet.id}: {sign_name} {degrees:.2f}°")

    print("\n" + "=" * 50 + "\n")

    # Create and print the Trimshamsha (D30) chart
    print("TRIMSHAMSHA CHART (D30) POSITIONS:")
    trimshamsha_chart = get_varga_chart(birth_chart, D30)

    for planet in planets:
        # Get the corresponding planet in the Trimshamsha chart
        d30_planet = trimshamsha_chart.getObject(planet.id)
        sign_num = int(d30_planet.lon / 30) + 1
        sign_name = const.LIST_SIGNS[sign_num - 1]
        degrees = d30_planet.lon % 30
        print(f"{d30_planet.id}: {sign_name} {degrees:.2f}°")

    print("\n" + "=" * 50 + "\n")
    print("Varga chart calculations complete!")


if __name__ == "__main__":
    main()
