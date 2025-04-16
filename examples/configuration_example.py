#!/usr/bin/env python3
"""
Configuration System Example

This script demonstrates how to use the configuration system in astrovedic.
It shows how to:
1. Use the ChartConfiguration class
2. Work with AyanamsaManager and HouseSystemManager
3. Create charts with different configurations
4. Validate configurations and get warnings
5. Use recommended combinations

Usage:
  python configuration_example.py
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
from astrovedic.vedic.ayanamsa import AyanamsaManager
from astrovedic.vedic.houses import HouseSystemManager
from astrovedic.vedic.config import ChartConfiguration
from astrovedic.vedic.api import VedicChart, create_vedic_chart, create_kp_chart


def print_section_header(title):
    """Print a section header."""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80)


def demonstrate_ayanamsa_manager():
    """Demonstrate the AyanamsaManager class."""
    print_section_header("AYANAMSA MANAGER")

    # Get default ayanamsa
    default_ayanamsa = AyanamsaManager.get_default()
    print(f"Default Ayanamsa: {default_ayanamsa}")

    # Get default KP ayanamsa
    default_kp_ayanamsa = AyanamsaManager.get_kp_default()
    print(f"Default KP Ayanamsa: {default_kp_ayanamsa}")

    # Get all supported ayanamsas
    supported_ayanamsas = AyanamsaManager.get_all_ayanamsas()
    print(f"\nSupported Ayanamsas ({len(supported_ayanamsas)}):")

    # Create a table of ayanamsas
    ayanamsa_data = []
    for ayanamsa in supported_ayanamsas:
        info = AyanamsaManager.get_ayanamsa_info(ayanamsa)
        recommended_house_systems = AyanamsaManager.get_recommended_house_systems(ayanamsa)
        recommended_str = ", ".join([HouseSystemManager.get_house_system_info(hs)['name']
                                    for hs in recommended_house_systems])

        ayanamsa_data.append([
            ayanamsa,
            info['name'],
            info['category'],
            recommended_str
        ])

    print(tabulate(ayanamsa_data,
                  headers=["Ayanamsa ID", "Name", "Category", "Recommended House Systems"],
                  tablefmt="grid"))

    # Set a custom default ayanamsa
    print("\nSetting custom default ayanamsa...")
    original_default = AyanamsaManager.get_default()
    AyanamsaManager.set_default(const.AY_RAMAN)
    print(f"New default ayanamsa: {AyanamsaManager.get_default()}")

    # Restore original default
    AyanamsaManager.set_default(original_default)
    print(f"Restored default ayanamsa: {AyanamsaManager.get_default()}")


def demonstrate_house_system_manager():
    """Demonstrate the HouseSystemManager class."""
    print_section_header("HOUSE SYSTEM MANAGER")

    # Get default house system
    default_house_system = HouseSystemManager.get_default()
    print(f"Default House System: {default_house_system}")

    # Get default KP house system
    default_kp_house_system = HouseSystemManager.get_kp_default()
    print(f"Default KP House System: {default_kp_house_system}")

    # Get all supported house systems
    supported_house_systems = HouseSystemManager.get_all_house_systems()
    print(f"\nSupported House Systems ({len(supported_house_systems)}):")

    # Create a table of house systems
    house_system_data = []
    for house_system in supported_house_systems:
        info = HouseSystemManager.get_house_system_info(house_system)
        recommended_ayanamsas = HouseSystemManager.get_recommended_ayanamsas(house_system)
        recommended_str = ", ".join([AyanamsaManager.get_ayanamsa_info(ay)['name']
                                    for ay in recommended_ayanamsas])

        house_system_data.append([
            house_system,
            info['name'],
            info['category'],
            recommended_str
        ])

    print(tabulate(house_system_data,
                  headers=["House System ID", "Name", "Category", "Recommended Ayanamsas"],
                  tablefmt="grid"))

    # Set a custom default house system
    print("\nSetting custom default house system...")
    original_default = HouseSystemManager.get_default()
    HouseSystemManager.set_default(const.HOUSES_EQUAL)
    print(f"New default house system: {HouseSystemManager.get_default()}")

    # Restore original default
    HouseSystemManager.set_default(original_default)
    print(f"Restored default house system: {HouseSystemManager.get_default()}")


def demonstrate_chart_configuration():
    """Demonstrate the ChartConfiguration class."""
    print_section_header("CHART CONFIGURATION")

    # Create a default configuration
    default_config = ChartConfiguration()
    print("Default Configuration:")
    print(f"  Ayanamsa: {default_config.ayanamsa}")
    print(f"  House System: {default_config.house_system}")

    # Create a KP configuration
    kp_config = ChartConfiguration(is_kp=True)
    print("\nKP Configuration:")
    print(f"  Ayanamsa: {kp_config.ayanamsa}")
    print(f"  House System: {kp_config.house_system}")

    # Create a custom configuration
    custom_config = ChartConfiguration(const.AY_RAMAN, const.HOUSES_EQUAL)
    print("\nCustom Configuration:")
    print(f"  Ayanamsa: {custom_config.ayanamsa}")
    print(f"  House System: {custom_config.house_system}")

    # Validate configurations
    print("\nValidating configurations...")
    try:
        default_config.validate()
        print("Default configuration is valid.")
    except ValueError as e:
        print(f"Default configuration is invalid: {e}")

    try:
        kp_config.validate()
        print("KP configuration is valid.")
    except ValueError as e:
        print(f"KP configuration is invalid: {e}")

    try:
        custom_config.validate()
        print("Custom configuration is valid.")
    except ValueError as e:
        print(f"Custom configuration is invalid: {e}")

    # Check if configurations are recommended
    print("\nChecking if configurations are recommended...")
    print(f"Default configuration is recommended: {default_config.is_recommended_combination()}")
    print(f"KP configuration is recommended: {kp_config.is_recommended_combination()}")
    print(f"Custom configuration is recommended: {custom_config.is_recommended_combination()}")

    # Get warnings for configurations
    print("\nGetting warnings for configurations...")
    default_warnings = default_config.get_warnings()
    kp_warnings = kp_config.get_warnings()
    custom_warnings = custom_config.get_warnings()

    print(f"Default configuration warnings: {default_warnings if default_warnings else 'None'}")
    print(f"KP configuration warnings: {kp_warnings if kp_warnings else 'None'}")
    print(f"Custom configuration warnings: {custom_warnings if custom_warnings else 'None'}")

    # Create a non-recommended configuration
    non_recommended_config = ChartConfiguration(const.AY_KRISHNAMURTI, const.HOUSES_WHOLE_SIGN)
    print("\nNon-recommended Configuration:")
    print(f"  Ayanamsa: {non_recommended_config.ayanamsa}")
    print(f"  House System: {non_recommended_config.house_system}")
    print(f"  Is recommended: {non_recommended_config.is_recommended_combination()}")

    non_recommended_warnings = non_recommended_config.get_warnings()
    print(f"  Warnings: {non_recommended_warnings if non_recommended_warnings else 'None'}")


def demonstrate_chart_creation_with_configuration():
    """Demonstrate chart creation with different configurations."""
    print_section_header("CHART CREATION WITH CONFIGURATION")

    # Create a sample date and location
    date = Datetime('2025/04/09', '20:51', '+05:30')
    pos = GeoPos(12.9716, 77.5946)  # Bangalore, India

    print(f"Date: {date}")
    print(f"Location: {pos}")

    # Create a chart with default configuration
    default_config = ChartConfiguration()
    default_chart = Chart(date, pos, hsys=default_config.house_system, ayanamsa=default_config.ayanamsa)

    print("\nChart with Default Configuration:")
    print(f"  Ayanamsa: {default_chart.mode}")
    print(f"  House System: {default_chart.hsys}")

    # Create a chart with KP configuration
    kp_config = ChartConfiguration(is_kp=True)
    kp_chart = Chart(date, pos, hsys=kp_config.house_system, ayanamsa=kp_config.ayanamsa)

    print("\nChart with KP Configuration:")
    print(f"  Ayanamsa: {kp_chart.mode}")
    print(f"  House System: {kp_chart.hsys}")

    # Create a chart with custom configuration
    custom_config = ChartConfiguration(const.AY_RAMAN, const.HOUSES_EQUAL)
    custom_chart = Chart(date, pos, hsys=custom_config.house_system, ayanamsa=custom_config.ayanamsa)

    print("\nChart with Custom Configuration:")
    print(f"  Ayanamsa: {custom_chart.mode}")
    print(f"  House System: {custom_chart.hsys}")

    # Compare Sun positions in different charts
    sun_default = default_chart.getObject(const.SUN)
    sun_kp = kp_chart.getObject(const.SUN)
    sun_custom = custom_chart.getObject(const.SUN)

    print("\nSun Position Comparison:")
    print(f"  Default: {sun_default.sign} {sun_default.signlon:.2f}°")
    print(f"  KP: {sun_kp.sign} {sun_kp.signlon:.2f}°")
    print(f"  Custom: {sun_custom.sign} {sun_custom.signlon:.2f}°")


def demonstrate_vedic_chart_api():
    """Demonstrate the VedicChart API with different configurations."""
    print_section_header("VEDIC CHART API WITH CONFIGURATION")

    # Create a sample date and location
    date = Datetime('2025/04/09', '20:51', '+05:30')
    pos = GeoPos(12.9716, 77.5946)  # Bangalore, India

    print(f"Date: {date}")
    print(f"Location: {pos}")

    # Create a VedicChart with default configuration
    # The API expects string parameters, not Datetime and GeoPos objects
    default_vedic_chart = create_vedic_chart(
        '2025/04/09', '20:51',
        12.9716, 77.5946,
        '+05:30'
    )

    print("\nVedicChart with Default Configuration:")
    print(f"  Ayanamsa: {default_vedic_chart.chart.mode}")
    print(f"  House System: {default_vedic_chart.chart.hsys}")

    # Create a VedicChart with KP configuration
    kp_vedic_chart = create_kp_chart(
        '2025/04/09', '20:51',
        12.9716, 77.5946,
        '+05:30'
    )

    print("\nVedicChart with KP Configuration:")
    print(f"  Ayanamsa: {kp_vedic_chart.chart.mode}")
    print(f"  House System: {kp_vedic_chart.chart.hsys}")

    # Create a VedicChart with custom configuration
    custom_vedic_chart = create_vedic_chart(
        '2025/04/09', '20:51',
        12.9716, 77.5946,
        '+05:30',
        ayanamsa=const.AY_RAMAN,
        hsys=const.HOUSES_EQUAL
    )

    print("\nVedicChart with Custom Configuration:")
    print(f"  Ayanamsa: {custom_vedic_chart.chart.mode}")
    print(f"  House System: {custom_vedic_chart.chart.hsys}")

    # Compare Moon Nakshatra in different charts
    moon_nakshatra_default = default_vedic_chart.get_nakshatra(const.MOON)
    moon_nakshatra_kp = kp_vedic_chart.get_nakshatra(const.MOON)
    moon_nakshatra_custom = custom_vedic_chart.get_nakshatra(const.MOON)

    print("\nMoon Nakshatra Comparison:")
    print(f"  Default: {moon_nakshatra_default['name']} (Lord: {moon_nakshatra_default['lord']})")
    print(f"  KP: {moon_nakshatra_kp['name']} (Lord: {moon_nakshatra_kp['lord']})")
    print(f"  Custom: {moon_nakshatra_custom['name']} (Lord: {moon_nakshatra_custom['lord']})")


def main():
    """Main function."""
    print("ASTROVEDIC CONFIGURATION SYSTEM EXAMPLE")
    print("This example demonstrates how to use the configuration system in astrovedic.")

    # Demonstrate AyanamsaManager
    demonstrate_ayanamsa_manager()

    # Demonstrate HouseSystemManager
    demonstrate_house_system_manager()

    # Demonstrate ChartConfiguration
    demonstrate_chart_configuration()

    # Demonstrate chart creation with configuration
    demonstrate_chart_creation_with_configuration()

    # Demonstrate VedicChart API with configuration
    demonstrate_vedic_chart_api()


if __name__ == "__main__":
    main()
