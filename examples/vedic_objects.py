#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Example script demonstrating how to use Vedic objects.
"""

from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib.object import VedicBody
from flatlib.vedic.utils import to_vedic_object, to_vedic_chart


def main():
    """Main function demonstrating Vedic object usage."""

    # Create a datetime and location
    dt = Datetime('2025/04/09', '20:51', '+05:30')  # April 9, 2025 at 20:51 in Bangalore
    pos = GeoPos('12n58', '77e35')  # Bangalore

    print("Reference date:", dt)
    print("Location:", pos)
    print("\n" + "=" * 50 + "\n")

    # Create the birth chart
    birth_chart = Chart(dt, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)

    # Get a regular object from the chart
    sun = birth_chart.getObject(const.SUN)

    print("REGULAR OBJECT:")
    print(f"ID: {sun.id}")
    print(f"Longitude: {sun.lon:.2f}°")
    print(f"Sign: {sun.sign}")
    # Get the house of the object
    house_num = 0
    for i in range(1, 13):
        house_id = f"House{i}"
        house = birth_chart.getHouse(house_id)
        if house and house.sign == sun.sign:
            house_num = i
            break
    print(f"House: {house_num}")
    print(f"Retrograde: {sun.isRetrograde()}")

    print("\n" + "=" * 50 + "\n")

    # Convert the object to a VedicBody object
    vedic_sun = to_vedic_object(sun, birth_chart)

    print("VEDIC OBJECT:")
    print(f"ID: {vedic_sun.id}")
    print(f"Longitude: {vedic_sun.lon:.2f}°")
    print(f"Sign: {vedic_sun.sign}")
    # Get the house of the object
    house_num = 0
    for i in range(1, 13):
        house_id = f"House{i}"
        house = birth_chart.getHouse(house_id)
        if house and house.sign == vedic_sun.sign:
            house_num = i
            break
    print(f"House: {house_num}")
    print(f"Retrograde: {vedic_sun.isRetrograde()}")

    # Print Vedic-specific attributes
    print("\nVEDIC-SPECIFIC ATTRIBUTES:")
    print(f"Nakshatra: {vedic_sun.nakshatra}")
    print(f"Nakshatra Lord: {vedic_sun.nakshatra_lord}")
    print(f"Nakshatra Pada: {vedic_sun.nakshatra_pada}")
    print(f"Nakshatra Degree: {vedic_sun.nakshatra_degree:.2f}°")

    # Print Shadbala components if available
    if hasattr(vedic_sun, 'total_shadbala') and vedic_sun.total_shadbala > 0:
        print("\nSHADBALA COMPONENTS:")
        print(f"Sthana Bala: {vedic_sun.sthana_bala:.2f}")
        print(f"Dig Bala: {vedic_sun.dig_bala:.2f}")
        print(f"Kala Bala: {vedic_sun.kala_bala:.2f}")
        print(f"Cheshta Bala: {vedic_sun.cheshta_bala:.2f}")
        print(f"Naisargika Bala: {vedic_sun.naisargika_bala:.2f}")
        print(f"Drig Bala: {vedic_sun.drig_bala:.2f}")
        print(f"Total Shadbala: {vedic_sun.total_shadbala:.2f}")

    # Print Varga positions if available
    if hasattr(vedic_sun, 'varga_positions') and vedic_sun.varga_positions:
        print("\nVARGA POSITIONS:")
        for varga, longitude in vedic_sun.varga_positions.items():
            sign_num = int(longitude / 30) + 1
            sign_name = const.LIST_SIGNS[sign_num - 1]
            degrees = longitude % 30
            print(f"D{varga}: {sign_name} {degrees:.2f}°")

    print("\n" + "=" * 50 + "\n")

    # Convert the entire chart to a Vedic chart
    vedic_chart = to_vedic_chart(birth_chart)

    print("VEDIC CHART OBJECTS:")
    # Print the objects in the chart
    print("Objects in chart:")
    for obj in vedic_chart.objects:
        print(f"  {obj.id}")

    # Get the Sun object directly
    sun = vedic_chart.getObject(const.SUN)
    if sun:
        print(f"Sun: {sun.id}, {sun.sign}, {sun.lon:.2f}°")
        if hasattr(sun, 'nakshatra'):
            print(f"Sun Nakshatra: {sun.nakshatra}")

    # Try to get each object
    for obj_id in [const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS, const.JUPITER, const.SATURN, const.RAHU, const.KETU]:
        obj = vedic_chart.getObject(obj_id)
        if obj:
            print(f"{obj.id}: {obj.sign} {obj.lon % 30:.2f}°")
            if hasattr(obj, 'nakshatra'):
                print(f"  Nakshatra: {obj.nakshatra}")

    print("\n" + "=" * 50 + "\n")
    print("Vedic object demonstration complete!")


if __name__ == "__main__":
    main()
