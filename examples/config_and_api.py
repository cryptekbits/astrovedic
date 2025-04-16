#!/usr/bin/env python3
"""
Configuration and API Example

This example demonstrates how to use both the configuration system and the Vedic API in astrovedic.
"""

import sys
import os

# Add the parent directory to the path so we can import astrovedic
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from astrovedic import const
    from astrovedic.datetime import Datetime
    from astrovedic.geopos import GeoPos
    from astrovedic.chart import Chart
    from astrovedic.vedic.config import ChartConfiguration
    from astrovedic.vedic.ayanamsa import AyanamsaManager
    from astrovedic.vedic.houses import HouseSystemManager
    from astrovedic.vedic.api import create_vedic_chart, create_kp_chart

    def print_section(title):
        """Print a section title."""
        print(f"\n=== {title} ===")

    # Part 1: Using the Configuration System
    print_section("CONFIGURATION SYSTEM")

    # Create a sample birth data
    birth_date = Datetime('2025/04/09', '20:51', '+05:30')
    birth_location = GeoPos(12.9716, 77.5946)  # Bangalore, India

    print("Birth Date:", birth_date)
    print("Birth Location:", birth_location)

    # Create a default configuration (Lahiri ayanamsa with Whole Sign houses)
    default_config = ChartConfiguration()
    print(f"Default Configuration:")
    print(f"  Ayanamsa: {default_config.ayanamsa}")
    print(f"  House System: {default_config.house_system}")

    # Create a KP configuration (Krishnamurti ayanamsa with Placidus houses)
    kp_config = ChartConfiguration(is_kp=True)
    print(f"\nKP Configuration:")
    print(f"  Ayanamsa: {kp_config.ayanamsa}")
    print(f"  House System: {kp_config.house_system}")

    # Create a custom configuration (Raman ayanamsa with Equal houses)
    custom_config = ChartConfiguration(const.AY_RAMAN, const.HOUSES_EQUAL)
    print(f"\nCustom Configuration:")
    print(f"  Ayanamsa: {custom_config.ayanamsa}")
    print(f"  House System: {custom_config.house_system}")

    # Check if the custom configuration is recommended
    is_recommended = custom_config.is_recommended_combination()
    print(f"  Is recommended: {is_recommended}")

    # Get warnings for the custom configuration
    warnings = custom_config.get_warnings()
    if warnings:
        print("  Warnings:")
        for warning in warnings:
            print(f"    - {warning}")
    else:
        print("  No warnings.")

    # Part 2: Creating Charts with Configuration
    print_section("CREATING CHARTS WITH CONFIGURATION")

    # Create a chart with default configuration
    chart1 = Chart(birth_date, birth_location,
                  hsys=default_config.house_system,
                  ayanamsa=default_config.ayanamsa)

    # Print some basic information from the chart
    sun1 = chart1.getObject(const.SUN)
    moon1 = chart1.getObject(const.MOON)
    asc1 = chart1.getAngle(const.ASC)

    print("Chart with Default Configuration:")
    print(f"  Sun: {sun1.sign} {sun1.signlon:.2f}°")
    print(f"  Moon: {moon1.sign} {moon1.signlon:.2f}°")
    print(f"  Ascendant: {asc1.sign} {asc1.signlon:.2f}°")

    # Create a chart with KP configuration
    chart2 = Chart(birth_date, birth_location,
                  hsys=kp_config.house_system,
                  ayanamsa=kp_config.ayanamsa)

    # Print some basic information from the chart
    sun2 = chart2.getObject(const.SUN)
    moon2 = chart2.getObject(const.MOON)
    asc2 = chart2.getAngle(const.ASC)

    print("\nChart with KP Configuration:")
    print(f"  Sun: {sun2.sign} {sun2.signlon:.2f}°")
    print(f"  Moon: {moon2.sign} {moon2.signlon:.2f}°")
    print(f"  Ascendant: {asc2.sign} {asc2.signlon:.2f}°")

    # Create a chart with custom configuration
    chart3 = Chart(birth_date, birth_location,
                  hsys=custom_config.house_system,
                  ayanamsa=custom_config.ayanamsa)

    # Print some basic information from the chart
    sun3 = chart3.getObject(const.SUN)
    moon3 = chart3.getObject(const.MOON)
    asc3 = chart3.getAngle(const.ASC)

    print("\nChart with Custom Configuration:")
    print(f"  Sun: {sun3.sign} {sun3.signlon:.2f}°")
    print(f"  Moon: {moon3.sign} {moon3.signlon:.2f}°")
    print(f"  Ascendant: {asc3.sign} {asc3.signlon:.2f}°")

    # Part 3: Using the Vedic API
    print_section("USING THE VEDIC API")

    # Create a Vedic chart with default configuration
    vedic_chart = create_vedic_chart(
        '2025/04/09', '20:51',
        12.9716, 77.5946,
        '+05:30'
    )

    print("Vedic Chart with Default Configuration:")
    print(f"  Ayanamsa: {vedic_chart.chart.mode}")
    print(f"  House System: {vedic_chart.chart.hsys}")

    # Print some basic information from the chart
    sun_v = vedic_chart.chart.getObject(const.SUN)
    moon_v = vedic_chart.chart.getObject(const.MOON)
    asc_v = vedic_chart.chart.getAngle(const.ASC)

    print(f"  Sun: {sun_v.sign} {sun_v.signlon:.2f}°")
    print(f"  Moon: {moon_v.sign} {moon_v.signlon:.2f}°")
    print(f"  Ascendant: {asc_v.sign} {asc_v.signlon:.2f}°")

    # Create a KP chart with default KP configuration
    kp_chart = create_kp_chart(
        '2025/04/09', '20:51',
        12.9716, 77.5946,
        '+05:30'
    )

    print("\nKP Chart with Default KP Configuration:")
    print(f"  Ayanamsa: {kp_chart.chart.mode}")
    print(f"  House System: {kp_chart.chart.hsys}")

    # Print some basic information from the chart
    sun_kp = kp_chart.chart.getObject(const.SUN)
    moon_kp = kp_chart.chart.getObject(const.MOON)
    asc_kp = kp_chart.chart.getAngle(const.ASC)

    print(f"  Sun: {sun_kp.sign} {sun_kp.signlon:.2f}°")
    print(f"  Moon: {moon_kp.sign} {moon_kp.signlon:.2f}°")
    print(f"  Ascendant: {asc_kp.sign} {asc_kp.signlon:.2f}°")

    # Create a Vedic chart with custom configuration
    custom_vedic_chart = create_vedic_chart(
        '2025/04/09', '20:51',
        12.9716, 77.5946,
        '+05:30',
        ayanamsa=const.AY_RAMAN,
        hsys=const.HOUSES_EQUAL
    )

    print("\nVedic Chart with Custom Configuration:")
    print(f"  Ayanamsa: {custom_vedic_chart.chart.mode}")
    print(f"  House System: {custom_vedic_chart.chart.hsys}")

    # Print some basic information from the chart
    sun_cv = custom_vedic_chart.chart.getObject(const.SUN)
    moon_cv = custom_vedic_chart.chart.getObject(const.MOON)
    asc_cv = custom_vedic_chart.chart.getAngle(const.ASC)

    print(f"  Sun: {sun_cv.sign} {sun_cv.signlon:.2f}°")
    print(f"  Moon: {moon_cv.sign} {moon_cv.signlon:.2f}°")
    print(f"  Ascendant: {asc_cv.sign} {asc_cv.signlon:.2f}°")

    # Part 4: Accessing Nakshatra Information
    print_section("ACCESSING NAKSHATRA INFORMATION")

    # Get Moon nakshatra using the Vedic API
    moon_nakshatra = vedic_chart.get_nakshatra(const.MOON)

    print("Moon Nakshatra Information:")
    print(f"  Name: {moon_nakshatra['name']}")
    print(f"  Lord: {moon_nakshatra['lord']}")
    print(f"  Pada: {moon_nakshatra['pada']}")
    # Note: The nakshatra information doesn't have a 'degree' key
    # We can calculate it from the longitude if needed
    moon_lon = vedic_chart.chart.getObject(const.MOON).lon
    print(f"  Longitude: {moon_lon:.2f}°")

    # Part 5: Changing Default Settings
    print_section("CHANGING DEFAULT SETTINGS")

    # Get current default ayanamsa
    original_ayanamsa = AyanamsaManager.get_default()
    print(f"Original Default Ayanamsa: {original_ayanamsa}")

    # Change default ayanamsa
    AyanamsaManager.set_default(const.AY_RAMAN)
    print(f"New Default Ayanamsa: {AyanamsaManager.get_default()}")

    # Create a chart with the new default
    new_config = ChartConfiguration()
    print(f"New Default Configuration:")
    print(f"  Ayanamsa: {new_config.ayanamsa}")
    print(f"  House System: {new_config.house_system}")

    # Restore original default
    AyanamsaManager.set_default(original_ayanamsa)
    print(f"Restored Default Ayanamsa: {AyanamsaManager.get_default()}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
