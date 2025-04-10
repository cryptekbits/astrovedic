#!/usr/bin/env python3
"""
Vedic API Example

This script demonstrates how to use the unified Vedic API in flatlib.
It shows how to create a VedicChart and access various Vedic astrology features.

Usage:
  python vedic_api_example.py                  # Use default birth data
  python vedic_api_example.py YYYY/MM/DD HH:MM # Use custom birth data
  python vedic_api_example.py -h, --help       # Show help message
"""

import sys
import argparse
from tabulate import tabulate

from flatlib import const
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib.vedic.api import VedicChart, create_vedic_chart, create_kp_chart


# Default location: Bangalore, India
DEFAULT_LAT = 12.9716
DEFAULT_LON = 77.5946
DEFAULT_LOCATION = "Bangalore, India"

# Default birth data
DEFAULT_BIRTH_DATE = "2025/04/09"
DEFAULT_BIRTH_TIME = "20:51"


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Vedic API Example")
    
    parser.add_argument("birth_date", nargs="?", default=DEFAULT_BIRTH_DATE,
                        help="Birth date in YYYY/MM/DD format")
    parser.add_argument("birth_time", nargs="?", default=DEFAULT_BIRTH_TIME,
                        help="Birth time in HH:MM format")
    parser.add_argument("--lat", type=float, default=DEFAULT_LAT,
                        help="Latitude")
    parser.add_argument("--lon", type=float, default=DEFAULT_LON,
                        help="Longitude")
    parser.add_argument("--location", default=DEFAULT_LOCATION,
                        help="Location name")
    parser.add_argument("--timezone", default="+05:30",
                        help="Timezone in +/-HH:MM format")
    parser.add_argument("--ayanamsa", default=const.AY_LAHIRI,
                        help="Ayanamsa to use")
    parser.add_argument("--hsys", default=const.HOUSES_WHOLE_SIGN,
                        help="House system to use")
    
    return parser.parse_args()


def print_chart_info(chart):
    """Print basic chart information"""
    print(f"\n{'=' * 60}")
    print(f"Chart Information")
    print(f"{'=' * 60}")
    
    # Get the chart date and location
    date = chart.chart.date
    pos = chart.chart.pos
    
    print(f"Date: {date.date} {date.time} {date.timezone}")
    print(f"Location: {args.location} ({pos.lat}, {pos.lon})")
    print(f"Ayanamsa: {chart.ayanamsa}")
    print(f"House System: {chart.chart.houses.name}")
    
    # Print the ascendant
    asc = chart.get_ascendant()
    print(f"Ascendant: {asc.sign} {asc.signlon:.2f}°")
    
    # Print the nakshatra of the ascendant
    asc_nakshatra = chart.get_nakshatra(const.ASC)
    print(f"Ascendant Nakshatra: {asc_nakshatra['name']} (Pada {asc_nakshatra['pada']})")
    
    # Print the panchang
    panchang = chart.get_panchang()
    print(f"Tithi: {panchang['tithi']['name']} ({panchang['tithi']['phase']})")
    print(f"Nakshatra: {panchang['nakshatra']['name']}")
    print(f"Yoga: {panchang['yoga']['name']}")
    print(f"Karana: {panchang['karana']['name']}")
    print(f"Vara: {panchang['vara']['name']}")


def print_planet_positions(chart):
    """Print planet positions"""
    print(f"\n{'=' * 60}")
    print(f"Planet Positions")
    print(f"{'=' * 60}")
    
    # Create a table
    headers = ["Planet", "Sign", "Longitude", "Nakshatra", "House", "Retrograde"]
    rows = []
    
    # Add planets to the table
    for planet_id in const.LIST_OBJECTS_VEDIC:
        planet = chart.get_planet(planet_id)
        nakshatra = chart.get_nakshatra(planet_id)
        
        rows.append([
            planet.name,
            f"{planet.sign}",
            f"{planet.lon:.2f}°",
            f"{nakshatra['name']} (Pada {nakshatra['pada']})",
            f"{planet.house}",
            "Yes" if planet.isRetrograde() else "No"
        ])
    
    # Print the table
    print(tabulate(rows, headers=headers, tablefmt="grid"))


def print_house_positions(chart):
    """Print house positions"""
    print(f"\n{'=' * 60}")
    print(f"House Positions")
    print(f"{'=' * 60}")
    
    # Create a table
    headers = ["House", "Sign", "Cusp", "Lord"]
    rows = []
    
    # Add houses to the table
    for house_num in range(1, 13):
        house = chart.get_house(house_num)
        
        rows.append([
            house_num,
            house.sign,
            f"{house.lon:.2f}°",
            chart.chart.getObject(house.signRuler).name
        ])
    
    # Print the table
    print(tabulate(rows, headers=headers, tablefmt="grid"))


def print_dasha_info(chart):
    """Print dasha information"""
    print(f"\n{'=' * 60}")
    print(f"Dasha Information")
    print(f"{'=' * 60}")
    
    # Get the dasha balance at birth
    dasha_balance = chart.get_dasha_balance()
    print(f"Dasha Balance at Birth: {dasha_balance['years']} years, {dasha_balance['months']} months, {dasha_balance['days']} days")
    
    # Get the current dasha
    current_dasha = chart.get_current_dasha()
    print(f"\nCurrent Mahadasha: {current_dasha['mahadasha']['planet']}")
    print(f"  Start: {current_dasha['mahadasha']['start']}")
    print(f"  End: {current_dasha['mahadasha']['end']}")
    
    print(f"\nCurrent Antardasha: {current_dasha['antardasha']['planet']}")
    print(f"  Start: {current_dasha['antardasha']['start']}")
    print(f"  End: {current_dasha['antardasha']['end']}")
    
    print(f"\nCurrent Pratyantardasha: {current_dasha['pratyantardasha']['planet']}")
    print(f"  Start: {current_dasha['pratyantardasha']['start']}")
    print(f"  End: {current_dasha['pratyantardasha']['end']}")


def print_varga_info(chart):
    """Print varga information"""
    print(f"\n{'=' * 60}")
    print(f"Varga Information")
    print(f"{'=' * 60}")
    
    # Get the navamsa positions
    navamsa_positions = chart.get_varga_positions('D9')
    
    # Create a table
    headers = ["Planet", "Rashi (D1)", "Navamsa (D9)"]
    rows = []
    
    # Add planets to the table
    for planet_id in const.LIST_OBJECTS_VEDIC:
        planet = chart.get_planet(planet_id)
        
        rows.append([
            planet.name,
            planet.sign,
            navamsa_positions[planet_id]['sign']
        ])
    
    # Print the table
    print(tabulate(rows, headers=headers, tablefmt="grid"))


def print_shadbala_info(chart):
    """Print shadbala information"""
    print(f"\n{'=' * 60}")
    print(f"Shadbala Information")
    print(f"{'=' * 60}")
    
    # Get the shadbala
    shadbala = chart.get_shadbala()
    
    # Create a table
    headers = ["Planet", "Sthana Bala", "Dig Bala", "Kala Bala", "Cheshta Bala", "Naisargika Bala", "Drig Bala", "Total"]
    rows = []
    
    # Add planets to the table
    for planet_id in const.LIST_PLANETS:
        if planet_id in shadbala:
            planet_shadbala = shadbala[planet_id]
            
            rows.append([
                chart.get_planet(planet_id).name,
                f"{planet_shadbala['sthana_bala']:.2f}",
                f"{planet_shadbala['dig_bala']:.2f}",
                f"{planet_shadbala['kala_bala']:.2f}",
                f"{planet_shadbala['cheshta_bala']:.2f}",
                f"{planet_shadbala['naisargika_bala']:.2f}",
                f"{planet_shadbala['drig_bala']:.2f}",
                f"{planet_shadbala['total']:.2f}"
            ])
    
    # Print the table
    print(tabulate(rows, headers=headers, tablefmt="grid"))


def print_ashtakavarga_info(chart):
    """Print ashtakavarga information"""
    print(f"\n{'=' * 60}")
    print(f"Ashtakavarga Information")
    print(f"{'=' * 60}")
    
    # Get the sarvashtakavarga
    sarva = chart.get_sarvashtakavarga()
    
    # Create a table
    headers = ["Sign", "Bindus"]
    rows = []
    
    # Add signs to the table
    for sign, bindus in sarva['bindus_in_signs'].items():
        rows.append([
            sign,
            bindus
        ])
    
    # Print the table
    print(tabulate(rows, headers=headers, tablefmt="grid"))


def print_yoga_info(chart):
    """Print yoga information"""
    print(f"\n{'=' * 60}")
    print(f"Yoga Information")
    print(f"{'=' * 60}")
    
    # Get the yogas
    yogas = chart.get_yogas()
    
    # Print Raja Yogas
    print("Raja Yogas:")
    for yoga in yogas['raja_yogas']:
        print(f"- {yoga['name']}: {yoga['description']}")
    
    # Print Dhana Yogas
    print("\nDhana Yogas:")
    for yoga in yogas['dhana_yogas']:
        print(f"- {yoga['name']}: {yoga['description']}")
    
    # Print Dosha Yogas
    print("\nDosha Yogas:")
    for yoga in yogas['dosha_yogas']:
        print(f"- {yoga['name']}: {yoga['description']}")


def main():
    """Main function"""
    global args
    args = parse_args()
    
    # Create a VedicChart
    chart = create_vedic_chart(
        args.birth_date, args.birth_time, args.lat, args.lon,
        args.timezone, args.hsys, args.ayanamsa
    )
    
    # Print chart information
    print_chart_info(chart)
    
    # Print planet positions
    print_planet_positions(chart)
    
    # Print house positions
    print_house_positions(chart)
    
    # Print dasha information
    print_dasha_info(chart)
    
    # Print varga information
    print_varga_info(chart)
    
    # Print shadbala information
    print_shadbala_info(chart)
    
    # Print ashtakavarga information
    print_ashtakavarga_info(chart)
    
    # Print yoga information
    print_yoga_info(chart)


if __name__ == "__main__":
    main()
