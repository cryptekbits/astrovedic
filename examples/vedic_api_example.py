#!/usr/bin/env python3
"""
Vedic API Example

This script demonstrates how to use the unified Vedic API in astrovedic.
It shows how to create a VedicChart and access various Vedic astrology features.

Usage:
  python vedic_api_example.py                  # Use default birth data
  python vedic_api_example.py YYYY/MM/DD HH:MM # Use custom birth data
  python vedic_api_example.py -h, --help       # Show help message
"""

import sys
import argparse
from tabulate import tabulate
from prettytable import PrettyTable

from astrovedic import const
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic.vedic.api import VedicChart, create_vedic_chart
from astrovedic.vedic.vimshottari import get_dasha_balance, get_current_dasha
from astrovedic.dignities.essential import EssentialInfo
from astrovedic.dignities import essential

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
    
    print(f"Date: {date.date.toString()} {date.time.toString()} {date.utcoffset.toString()}")
    print(f"Location: {args.location} ({pos.lat}, {pos.lon})")
    print(f"Ayanamsa: {chart.ayanamsa}")
    print(f"House System: {chart.chart.hsys}")
    
    # Print the ascendant
    asc = chart.get_ascendant()
    print(f"Ascendant: {asc.sign} {asc.signlon:.2f}°")
    
    # Print the nakshatra of the ascendant
    asc_nakshatra = chart.get_nakshatra(const.ASC)
    print(f"Ascendant Nakshatra: {asc_nakshatra['name']} (Pada {asc_nakshatra['pada']})")
    
    # Get Panchang details
    panchang = chart.get_panchang()
    print(f"Tithi: {panchang['tithi']['name']} ({panchang['tithi']['paksha']}) - {panchang['tithi']['completion']:.2f}% complete")
    print(f"Nakshatra: {panchang['nakshatra']['name']} - {panchang['nakshatra']['percentage']:.2f}% complete")
    print(f"Yoga: {panchang['yoga']['name']} - {panchang['yoga']['completion']:.2f}% complete")
    print(f"Karana: {panchang['karana']['name']} - {panchang['karana']['completion']:.2f}% complete")
    print(f"Vara: {panchang['vara']['name']}")


def print_planet_positions(chart):
    """
    Print detailed planet positions, including dignity and rulership.
    
    Args:
        chart (VedicChart): The VedicChart object
    """
    print("\n" + "=" * 60)
    print("Planet Positions".center(60))
    print("=" * 60 + "\n")
    
    table = PrettyTable()
    table.field_names = ["Planet", "Position", "House", "Rulerships", "Nakshatra (Pada)", "Dignity"]
    
    # Iterate through standard Vedic objects
    for pid in const.LIST_OBJECTS_VEDIC:
        planet = chart.get_planet(pid)
        if planet is None:
            # Skip if planet data is not available (e.g., Nodes in certain ephem settings)
            continue
            
        # Get house position using the HouseList method
        house_obj = chart.chart.houses.getObjectHouse(planet)
        house_num = 'N/A'
        if house_obj:
            try:
                # Extract number from ID like 'House1', 'House10', etc.
                house_num = int(house_obj.id.replace('House', '')) 
            except (ValueError, AttributeError):
                house_num = 'Error' # Should not happen if ID is valid

        # Get rulerships by checking all signs
        ruled_signs = []
        for sign in const.LIST_SIGNS:
            if essential.ruler(sign) == pid:
                ruled_signs.append(sign)
        rulerships_str = ", ".join(ruled_signs) if ruled_signs else "None"
        
        # Get nakshatra details
        nakshatra = chart.get_nakshatra(pid)
        nak_str = f"{nakshatra['name']} (Pada {nakshatra['pada']})"
        
        # Dignity info using EssentialInfo
        dignity_str = "None"
        if planet:
            essential_info = EssentialInfo(planet)
            dignities_list = essential_info.getDignities()
            dignity_str = ", ".join(dignities_list) if dignities_list else "None"

        table.add_row([
            pid, 
            f"{planet.sign} {planet.signlon:.2f}°",
            house_num,
            rulerships_str,
            nak_str,
            dignity_str
        ])
        
    print(table)


def print_house_positions(chart):
    """Print house positions"""
    print(f"\n{'=' * 60}")
    print(f"House Positions")
    print(f"{'=' * 60}")
    
    # Create a table
    table = PrettyTable()
    table.field_names = ["House", "Sign", "Longitude"]

    for house_num in range(1, 13):
        # Construct the string ID (e.g., 'House1')
        house_id_str = f"House{house_num}"
        house = chart.get_house(house_id_str)
        
        if house:
            table.add_row([
                house_num,
                house.sign,
                f"{house.lon:.2f}°"
            ])
    
    # Print the table
    print(table)


def print_dasha_info(chart):
    """Print dasha information"""
    print(f"\n{'=' * 60}")
    print(f"Dasha Information")
    print(f"{'=' * 60}")
    
    # Get the dasha balance at birth using the imported function
    # Pass the base chart object (chart.chart)
    dasha_balance = get_dasha_balance(chart.chart)
    print(f"Dasha Balance at Birth: {dasha_balance:.2f} years") # Format float
    
    # Get the current dasha using the imported function
    # Pass the base chart object (chart.chart)
    current_dasha = get_current_dasha(chart.chart)
    print(f"\nCurrent Mahadasha: {current_dasha['mahadasha']['planet']}")
    print(f"  Start: {current_dasha['mahadasha']['start_date']}")
    print(f"  End: {current_dasha['mahadasha']['end_date']}")
    
    print(f"\nCurrent Antardasha: {current_dasha['antardasha']['planet']}")
    print(f"  Start: {current_dasha['antardasha']['start_date']}")
    print(f"  End: {current_dasha['antardasha']['end_date']}")
    
    print(f"\nCurrent Pratyantardasha: {current_dasha['pratyantardasha']['planet']}")
    print(f"  Start: {current_dasha['pratyantardasha']['start_date']}")
    print(f"  End: {current_dasha['pratyantardasha']['end_date']}")


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
            planet_id,
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
    
    # Create a table
    headers = ["Planet", "Sthana Bala", "Dig Bala", "Kala Bala", "Cheshta Bala", "Naisargika Bala", "Drig Bala", "Total"]
    rows = []
    
    # Add planets to the table, iterating over LIST_OBJECTS_VEDIC
    for planet_id in const.LIST_OBJECTS_VEDIC:
        # Check if the object is a planet typically used in Shadbala
        # (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn)
        if planet_id in const.LIST_SEVEN_PLANETS: # Use LIST_SEVEN_PLANETS
            # Call get_shadbala for each planet
            planet_shadbala = chart.get_shadbala(planet_id)
            
            # Check if shadbala data was returned (might be None if calculation fails)
            if planet_shadbala:
                rows.append([
                    planet_id, # Use planet_id directly as name
                    f"{planet_shadbala.get('sthana_bala', 0):.2f}", 
                    f"{planet_shadbala.get('dig_bala', 0):.2f}",    
                    f"{planet_shadbala.get('kala_bala', 0):.2f}",    
                    f"{planet_shadbala.get('cheshta_bala', 0):.2f}", 
                    f"{planet_shadbala.get('naisargika_bala', 0):.2f}", 
                    f"{planet_shadbala.get('drig_bala', 0):.2f}",    
                    f"{planet_shadbala.get('total_shadbala', {}).get('total_rupas', 0):.2f}" 
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
