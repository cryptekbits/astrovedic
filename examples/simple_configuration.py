#!/usr/bin/env python3
"""
Simple Configuration Example

This script demonstrates the basic usage of the configuration system in astrovedic.
It shows how to create and use different chart configurations for Vedic astrology.

Usage:
  python simple_configuration.py
"""

import sys
import os

# Add the parent directory to the path so we can import astrovedic
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from astrovedic import const
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic.vedic.config import ChartConfiguration
from astrovedic.vedic.api import create_vedic_chart, create_kp_chart


def print_section(title):
    """Print a section title."""
    print(f"\n=== {title} ===")


def main():
    """Main function demonstrating simple configuration usage."""
    # Create a sample birth data
    birth_date = Datetime('2025/04/09', '20:51', '+05:30')
    birth_location = GeoPos(12.9716, 77.5946)  # Bangalore, India

    print("Birth Date:", birth_date)
    print("Birth Location:", birth_location)

    # Example 1: Default Vedic Configuration
    print_section("Default Vedic Configuration")

    # Create a default configuration (Lahiri ayanamsa with Whole Sign houses)
    default_config = ChartConfiguration()
    print(f"Ayanamsa: {default_config.ayanamsa}")
    print(f"House System: {default_config.house_system}")

    # Create a chart with this configuration
    chart1 = Chart(birth_date, birth_location,
                  hsys=default_config.house_system,
                  ayanamsa=default_config.ayanamsa)

    # Print some basic information from the chart
    sun1 = chart1.getObject(const.SUN)
    moon1 = chart1.getObject(const.MOON)
    asc1 = chart1.getAngle(const.ASC)

    print(f"Sun: {sun1.sign} {sun1.signlon:.2f}°")
    print(f"Moon: {moon1.sign} {moon1.signlon:.2f}°")
    print(f"Ascendant: {asc1.sign} {asc1.signlon:.2f}°")

    # Example 2: KP Configuration
    print_section("KP Configuration")

    # Create a KP configuration (Krishnamurti ayanamsa with Placidus houses)
    kp_config = ChartConfiguration(is_kp=True)
    print(f"Ayanamsa: {kp_config.ayanamsa}")
    print(f"House System: {kp_config.house_system}")

    # Create a chart with this configuration
    chart2 = Chart(birth_date, birth_location,
                  hsys=kp_config.house_system,
                  ayanamsa=kp_config.ayanamsa)

    # Print some basic information from the chart
    sun2 = chart2.getObject(const.SUN)
    moon2 = chart2.getObject(const.MOON)
    asc2 = chart2.getAngle(const.ASC)

    print(f"Sun: {sun2.sign} {sun2.signlon:.2f}°")
    print(f"Moon: {moon2.sign} {moon2.signlon:.2f}°")
    print(f"Ascendant: {asc2.sign} {asc2.signlon:.2f}°")

    # Example 3: Custom Configuration
    print_section("Custom Configuration")

    # Create a custom configuration (Raman ayanamsa with Equal houses)
    custom_config = ChartConfiguration(const.AY_RAMAN, const.HOUSES_EQUAL)
    print(f"Ayanamsa: {custom_config.ayanamsa}")
    print(f"House System: {custom_config.house_system}")

    # Check if this is a recommended combination
    is_recommended = custom_config.is_recommended_combination()
    print(f"Is recommended combination: {is_recommended}")

    # Get any warnings for this configuration
    warnings = custom_config.get_warnings()
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("No warnings for this configuration.")

    # Create a chart with this configuration
    chart3 = Chart(birth_date, birth_location,
                  hsys=custom_config.house_system,
                  ayanamsa=custom_config.ayanamsa)

    # Print some basic information from the chart
    sun3 = chart3.getObject(const.SUN)
    moon3 = chart3.getObject(const.MOON)
    asc3 = chart3.getAngle(const.ASC)

    print(f"Sun: {sun3.sign} {sun3.signlon:.2f}°")
    print(f"Moon: {moon3.sign} {moon3.signlon:.2f}°")
    print(f"Ascendant: {asc3.sign} {asc3.signlon:.2f}°")

    # Example 4: Using the Vedic API
    print_section("Using the Vedic API")

    # Create charts using the Vedic API
    # The API expects string parameters, not Datetime and GeoPos objects
    vedic_chart = create_vedic_chart(
        '2025/04/09', '20:51',
        12.9716, 77.5946,
        '+05:30'
    )

    kp_chart = create_kp_chart(
        '2025/04/09', '20:51',
        12.9716, 77.5946,
        '+05:30'
    )

    custom_chart = create_vedic_chart(
        '2025/04/09', '20:51',
        12.9716, 77.5946,
        '+05:30',
        ayanamsa=const.AY_RAMAN,
        hsys=const.HOUSES_EQUAL
    )

    print("Default Vedic Chart:")
    print(f"  Ayanamsa: {vedic_chart.chart.mode}")
    print(f"  House System: {vedic_chart.chart.hsys}")

    print("\nKP Chart:")
    print(f"  Ayanamsa: {kp_chart.chart.mode}")
    print(f"  House System: {kp_chart.chart.hsys}")

    print("\nCustom Chart:")
    print(f"  Ayanamsa: {custom_chart.chart.mode}")
    print(f"  House System: {custom_chart.chart.hsys}")


if __name__ == "__main__":
    print("Starting simple_configuration.py...")
    try:
        main()
        print("Finished simple_configuration.py.")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
