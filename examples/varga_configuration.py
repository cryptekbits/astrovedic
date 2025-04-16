#!/usr/bin/env python3
"""
Varga Configuration Example

This script demonstrates how to use the configuration system with divisional charts (vargas)
in Vedic astrology. It shows how different ayanamsas and house systems affect varga calculations.

Usage:
  python varga_configuration.py
"""

import sys
import os
from tabulate import tabulate

# Add the parent directory to the path so we can import astrovedic
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from astrovedic import const
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic.vedic.config import ChartConfiguration
from astrovedic.vedic.api import VedicChart, create_vedic_chart, create_kp_chart
from astrovedic.vedic.vargas.constants import D1, D9, D10


def print_section_header(title):
    """Print a section header."""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80)


def print_planet_positions(chart, title):
    """Print planet positions in a chart."""
    print(f"\n{title}:")

    # Create a table of planet positions
    planet_data = []
    for planet_id in const.LIST_OBJECTS_VEDIC:
        try:
            planet = chart.getObject(planet_id)
            planet_data.append([
                planet.id,
                planet.sign,
                f"{planet.signlon:.2f}°",
                "R" if planet.retrograde else ""
            ])
        except Exception:
            # Skip planets that might not be available
            pass

    print(tabulate(planet_data,
                  headers=["Planet", "Sign", "Longitude", "Retro"],
                  tablefmt="simple"))


def main():
    """Main function demonstrating varga configuration usage."""
    # Create a sample birth data
    birth_date = Datetime('2025/04/09', '20:51', '+05:30')
    birth_location = GeoPos(12.9716, 77.5946)  # Bangalore, India

    print_section_header("VARGA CONFIGURATION EXAMPLE")
    print(f"Birth Date: {birth_date}")
    print(f"Birth Location: {birth_location}")

    # Example 1: Default Vedic Configuration
    print_section_header("DEFAULT VEDIC CONFIGURATION")

    # Create a default configuration (Lahiri ayanamsa with Whole Sign houses)
    default_config = ChartConfiguration()
    print(f"Ayanamsa: {default_config.ayanamsa}")
    print(f"House System: {default_config.house_system}")

    # Create a VedicChart with this configuration
    # The API expects string parameters, not Datetime and GeoPos objects
    vedic_chart = create_vedic_chart(
        '2025/04/09', '20:51',
        12.9716, 77.5946,
        '+05:30'
    )

    # Print planet positions in the birth chart (D1)
    print_planet_positions(vedic_chart.chart, "Birth Chart (D1)")

    # Get and print Navamsa chart (D9)
    navamsa_chart = vedic_chart.get_varga_chart(D9)
    print_planet_positions(navamsa_chart, "Navamsa Chart (D9)")

    # Get and print Dashamsha chart (D10)
    dashamsha_chart = vedic_chart.get_varga_chart(D10)
    print_planet_positions(dashamsha_chart, "Dashamsha Chart (D10)")

    # Example 2: KP Configuration
    print_section_header("KP CONFIGURATION")

    # Create a KP configuration (Krishnamurti ayanamsa with Placidus houses)
    kp_config = ChartConfiguration(is_kp=True)
    print(f"Ayanamsa: {kp_config.ayanamsa}")
    print(f"House System: {kp_config.house_system}")

    # Create a chart with this configuration
    kp_chart = Chart(birth_date, birth_location,
                    hsys=kp_config.house_system,
                    ayanamsa=kp_config.ayanamsa)

    # Create a VedicChart wrapper
    kp_vedic_chart = VedicChart(kp_chart)

    # Print planet positions in the birth chart (D1)
    print_planet_positions(kp_vedic_chart.chart, "KP Birth Chart (D1)")

    # Get and print Navamsa chart (D9)
    kp_navamsa_chart = kp_vedic_chart.get_varga_chart(D9)
    print_planet_positions(kp_navamsa_chart, "KP Navamsa Chart (D9)")

    # Get and print Dashamsha chart (D10)
    kp_dashamsha_chart = kp_vedic_chart.get_varga_chart(D10)
    print_planet_positions(kp_dashamsha_chart, "KP Dashamsha Chart (D10)")

    # Example 3: Custom Configuration
    print_section_header("CUSTOM CONFIGURATION")

    # Create a custom configuration (Raman ayanamsa with Equal houses)
    custom_config = ChartConfiguration(const.AY_RAMAN, const.HOUSES_EQUAL)
    print(f"Ayanamsa: {custom_config.ayanamsa}")
    print(f"House System: {custom_config.house_system}")

    # Create a chart with this configuration
    custom_chart = Chart(birth_date, birth_location,
                        hsys=custom_config.house_system,
                        ayanamsa=custom_config.ayanamsa)

    # Create a VedicChart wrapper
    custom_vedic_chart = VedicChart(custom_chart)

    # Print planet positions in the birth chart (D1)
    print_planet_positions(custom_vedic_chart.chart, "Custom Birth Chart (D1)")

    # Get and print Navamsa chart (D9)
    custom_navamsa_chart = custom_vedic_chart.get_varga_chart(D9)
    print_planet_positions(custom_navamsa_chart, "Custom Navamsa Chart (D9)")

    # Get and print Dashamsha chart (D10)
    custom_dashamsha_chart = custom_vedic_chart.get_varga_chart(D10)
    print_planet_positions(custom_dashamsha_chart, "Custom Dashamsha Chart (D10)")

    # Compare planet positions in different configurations
    print_section_header("COMPARISON OF CONFIGURATIONS")

    # Get Sun position in D1, D9, and D10 for each configuration
    sun_default_d1 = vedic_chart.chart.getObject(const.SUN)
    sun_default_d9 = navamsa_chart.getObject(const.SUN)
    sun_default_d10 = dashamsha_chart.getObject(const.SUN)

    sun_kp_d1 = kp_vedic_chart.chart.getObject(const.SUN)
    sun_kp_d9 = kp_navamsa_chart.getObject(const.SUN)
    sun_kp_d10 = kp_dashamsha_chart.getObject(const.SUN)

    sun_custom_d1 = custom_vedic_chart.chart.getObject(const.SUN)
    sun_custom_d9 = custom_navamsa_chart.getObject(const.SUN)
    sun_custom_d10 = custom_dashamsha_chart.getObject(const.SUN)

    # Create a comparison table
    comparison_data = [
        ["Default (Lahiri/Whole Sign)",
         f"{sun_default_d1.sign} {sun_default_d1.signlon:.2f}°",
         f"{sun_default_d9.sign} {sun_default_d9.signlon:.2f}°",
         f"{sun_default_d10.sign} {sun_default_d10.signlon:.2f}°"],
        ["KP (Krishnamurti/Placidus)",
         f"{sun_kp_d1.sign} {sun_kp_d1.signlon:.2f}°",
         f"{sun_kp_d9.sign} {sun_kp_d9.signlon:.2f}°",
         f"{sun_kp_d10.sign} {sun_kp_d10.signlon:.2f}°"],
        ["Custom (Raman/Equal)",
         f"{sun_custom_d1.sign} {sun_custom_d1.signlon:.2f}°",
         f"{sun_custom_d9.sign} {sun_custom_d9.signlon:.2f}°",
         f"{sun_custom_d10.sign} {sun_custom_d10.signlon:.2f}°"]
    ]

    print("Sun Position Comparison:")
    print(tabulate(comparison_data,
                  headers=["Configuration", "D1 (Birth)", "D9 (Navamsa)", "D10 (Dashamsha)"],
                  tablefmt="grid"))

    # Demonstrate how configuration affects varga analysis
    print_section_header("VARGA ANALYSIS WITH DIFFERENT CONFIGURATIONS")

    # Get varga analysis for each configuration
    default_analysis = vedic_chart.analyze_varga_charts()
    kp_analysis = kp_vedic_chart.analyze_varga_charts()
    custom_analysis = custom_vedic_chart.analyze_varga_charts()

    # Print a summary of the analysis
    print("Varga Analysis Summary:")
    print("\nDefault Configuration:")
    print(f"  Status: {default_analysis.get('status', 'N/A')}")

    print("\nKP Configuration:")
    print(f"  Status: {kp_analysis.get('status', 'N/A')}")

    print("\nCustom Configuration:")
    print(f"  Status: {custom_analysis.get('status', 'N/A')}")

    print("\nNote: The differences in varga positions and analysis demonstrate")
    print("how the choice of ayanamsa and house system affects chart interpretation.")


if __name__ == "__main__":
    main()
