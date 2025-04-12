#!/usr/bin/env python3
"""
    Vedic Aspects Example

    This example demonstrates how to use the Vedic aspects (Drishti) module
    to calculate and analyze aspects in Vedic astrology.
"""

from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib.vedic import aspects as vedic_aspects
# No need to import VedicChart for this example


def print_section_header(title):
    """Print a section header"""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80)


def print_aspect_info(aspect_info):
    """Print aspect information"""
    if aspect_info['has_aspect']:
        print(f"  - Aspect Type: {aspect_info['type']}")
        print(f"  - Strength: {aspect_info['strength'] * 100:.0f}%")
    else:
        print("  - No aspect")


def main():
    """Main function"""
    # Create a chart for the reference date
    date = Datetime('2025/04/09', '20:51', '+05:30')
    pos = GeoPos(12.9716, 77.5946)  # Bangalore, India

    # Create a chart with Whole Sign houses and Lahiri ayanamsa
    chart = Chart(date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)

    # No need to create a Vedic chart wrapper for this example

    print_section_header("CHART INFORMATION")
    print(f"Date: {date.date} {date.time} {date.utcoffset}")
    print(f"Location: {pos.lat}°N, {pos.lon}°E (Bangalore, India)")
    print(f"House System: {chart.hsys}")
    print(f"Ayanamsa: {chart.mode}")

    # Print planet positions
    print_section_header("PLANET POSITIONS")
    for planet_id in const.LIST_OBJECTS_VEDIC:
        planet = chart.getObject(planet_id)
        print(f"{planet_id}: {planet.sign} {planet.signlon:.2f}°")

    # Demonstrate Graha Drishti (Planetary Aspects)
    print_section_header("GRAHA DRISHTI (PLANETARY ASPECTS)")

    # Check aspects from Mars
    mars = chart.getObject(const.MARS)
    print(f"Aspects cast by Mars (at {mars.lon:.2f}°):")

    # Check aspects to each planet
    for other_id in const.LIST_OBJECTS_VEDIC:
        if other_id != const.MARS:
            other = chart.getObject(other_id)
            print(f"\nMars -> {other_id} (at {other.lon:.2f}°):")

            # Calculate the aspect strength
            aspect_info = vedic_aspects.get_graha_drishti_strength(const.MARS, mars.lon, other.lon)
            print_aspect_info(aspect_info)

    # Demonstrate Rashi Drishti (Sign Aspects)
    print_section_header("RASHI DRISHTI (SIGN ASPECTS)")

    # Check aspects from Aries
    print(f"Aspects cast by Aries:")

    # Check aspects to each sign
    for sign in const.LIST_SIGNS:
        if sign != const.ARIES:
            print(f"\nAries -> {sign}:")

            # Calculate the aspect strength
            aspect_info = vedic_aspects.get_rashi_drishti_strength(const.ARIES, sign)
            print_aspect_info(aspect_info)

    # Get all aspects in the chart
    print_section_header("ALL ASPECTS IN THE CHART")
    all_aspects = vedic_aspects.get_all_aspects(chart)

    # Print aspects cast by each planet
    print("\nPlanetary Aspects Cast:")
    for planet_id in const.LIST_OBJECTS_VEDIC:
        aspects_cast = all_aspects['planet_aspects'][planet_id]['aspects_cast']
        if aspects_cast:
            print(f"\n{planet_id} aspects:")
            for aspect in aspects_cast:
                print(f"  - {aspect['to_planet']} ({aspect['type']}, {aspect['strength'] * 100:.0f}% strength)")
        else:
            print(f"\n{planet_id} has no aspects")

    # Print aspects received by each planet
    print("\nPlanetary Aspects Received:")
    for planet_id in const.LIST_OBJECTS_VEDIC:
        aspects_received = all_aspects['planet_aspects'][planet_id]['aspects_received']
        if aspects_received:
            print(f"\n{planet_id} is aspected by:")
            for aspect in aspects_received:
                print(f"  - {aspect['from_planet']} ({aspect['type']}, {aspect['strength'] * 100:.0f}% strength)")
        else:
            print(f"\n{planet_id} receives no aspects")


if __name__ == '__main__':
    main()
