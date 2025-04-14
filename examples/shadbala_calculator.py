#!/usr/bin/env python3
"""
Shadbala Calculator Example

This script demonstrates how to use flatlib for Shadbala (six-fold planetary strength)
calculations in Vedic astrology. It includes:
- Calculating all six sources of planetary strength
- Analyzing the total Shadbala for each planet
- Calculating Ishta and Kashta Phala (beneficial and harmful effects)
- Calculating Bhava Bala (house strength)

Usage:
  python shadbala_calculator.py                   # Generate calculations for current time
  python shadbala_calculator.py YYYY/MM/DD HH:MM  # Generate calculations for specific date and time
  python shadbala_calculator.py -h, --help        # Show help message
"""

import sys
import argparse
from tabulate import tabulate
from prettytable import PrettyTable

from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic import const
from astrovedic.vedic.shadbala import (
    get_shadbala, get_all_shadbala, get_bhava_bala,
    STHANA_BALA, DIG_BALA, KALA_BALA, 
    CHESHTA_BALA, NAISARGIKA_BALA, DRIG_BALA,
    MINIMUM_SHADBALA
)

# Default location: Bangalore, India
DEFAULT_LAT = 12.9716
DEFAULT_LON = 77.5946
DEFAULT_LOCATION = "Bangalore, India"

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Calculate Shadbala (six-fold planetary strength)')
    parser.add_argument('date', nargs='?', help='Date in YYYY/MM/DD format')
    parser.add_argument('time', nargs='?', help='Time in HH:MM format')
    parser.add_argument('--lat', type=float, default=DEFAULT_LAT, help='Latitude')
    parser.add_argument('--lon', type=float, default=DEFAULT_LON, help='Longitude')
    parser.add_argument('--location', default=DEFAULT_LOCATION, help='Location name')
    parser.add_argument('--ayanamsa', default=const.AY_LAHIRI, help='Ayanamsa to use')
    return parser.parse_args()

def create_chart(date_str=None, time_str=None, lat=DEFAULT_LAT, lon=DEFAULT_LON, ayanamsa=const.AY_LAHIRI):
    """
    Create a chart for the given date, time, and location
    
    Args:
        date_str (str, optional): Date in YYYY/MM/DD format
        time_str (str, optional): Time in HH:MM format
        lat (float, optional): Latitude
        lon (float, optional): Longitude
        ayanamsa (str, optional): Ayanamsa to use
    
    Returns:
        tuple: (chart, date)
    """
    from datetime import datetime
    
    # Use current date and time if not provided
    if date_str is None or time_str is None:
        now = datetime.now()
        date_str = now.strftime("%Y/%m/%d")
        time_str = now.strftime("%H:%M")
    
    # Create date and location objects
    date = Datetime(date_str, time_str, '+05:30')  # Indian Standard Time
    pos = GeoPos(lat, lon)
    
    # Create chart with specified ayanamsa and Whole Sign houses
    chart = Chart(date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=ayanamsa)
    
    return chart, date

def print_chart_info(chart, location, ayanamsa):
    """
    Print basic chart information
    
    Args:
        chart (Chart): Astrovedic Chart object
        location (str): Location name
        ayanamsa (str): Ayanamsa used
    """
    print(f"\n{'=' * 60}")
    print(f"Birth Chart Information")
    print(f"{'=' * 60}")
    print(f"Date: {chart.date}")
    print(f"Location: {location} ({chart.pos.lat:.4f}, {chart.pos.lon:.4f})")
    print(f"Ayanamsa: {ayanamsa}")
    print(f"House System: {chart.hsys}")
    
    # Print ascendant
    asc = chart.getAngle(const.ASC)
    print(f"Ascendant: {asc.sign} {asc.signlon:.2f}°")
    
    # Print planetary positions
    print(f"\n{'=' * 60}")
    print(f"Planetary Positions")
    print(f"{'=' * 60}")
    
    table = PrettyTable()
    table.field_names = ["Planet", "Position", "Motion", "Retrograde"]
    table.align["Planet"] = "l"
    table.align["Position"] = "r"
    table.align["Motion"] = "l"
    table.align["Retrograde"] = "l"

    # Populate the table
    for planet in chart.objects:
        # Check if the object is a planet or node and has the isRetrograde method
        retrograde_status = "N/A" # Default for nodes or objects without the method
        if hasattr(planet, 'isRetrograde'):
            retrograde_status = "Yes" if planet.isRetrograde() else "No"
            
        # Check for motion status
        motion_status = "N/A"
        if hasattr(planet, 'motion'):
            motion_status = planet.motion
            
        table.add_row([
            planet.id,
            f"{planet.sign} {planet.signlon:.2f}°",
            motion_status, # Use checked motion status
            retrograde_status
        ])

    print(table)
    print("\n")

def print_shadbala_summary(shadbala_results):
    """
    Print a summary of Shadbala results
    
    Args:
        shadbala_results (dict): Dictionary with Shadbala results
    """
    print(f"\n{'=' * 60}")
    print(f"Shadbala Summary")
    print(f"{'=' * 60}")
    
    # Print summary information
    summary = shadbala_results['summary']
    print(f"Average Shadbala: {summary['average_rupas']:.2f} Rupas")
    print(f"Planets with sufficient strength: {summary['sufficient_count']} out of {summary['total_planets']}")
    
    # Print strongest and weakest planets
    strongest = shadbala_results['strongest']
    weakest = shadbala_results['weakest']
    
    print(f"Strongest planet: {strongest} ({shadbala_results[strongest]['total_shadbala']['total_rupas']:.2f} Rupas)")
    print(f"Weakest planet: {weakest} ({shadbala_results[weakest]['total_shadbala']['total_rupas']:.2f} Rupas)")
    
    # Print Shadbala for each planet
    print(f"\n{'=' * 60}")
    print(f"Shadbala for Each Planet")
    print(f"{'=' * 60}")
    
    headers = ["Planet", "Total Shadbala", "Minimum Required", "Sufficient?"]
    rows = []
    
    for planet_id in const.LIST_OBJECTS_VEDIC:
        result = shadbala_results[planet_id]
        rows.append([
            planet_id,
            f"{result['total_shadbala']['total_rupas']:.2f} Rupas",
            f"{result['minimum_required']:.2f} Rupas",
            "Yes" if result['is_sufficient'] else "No"
        ])
    
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def print_shadbala_components(shadbala_results):
    """
    Print the components of Shadbala for each planet
    
    Args:
        shadbala_results (dict): Dictionary with Shadbala results
    """
    print(f"\n{'=' * 60}")
    print(f"Shadbala Components")
    print(f"{'=' * 60}")
    
    headers = ["Planet", STHANA_BALA, DIG_BALA, KALA_BALA, CHESHTA_BALA, NAISARGIKA_BALA, DRIG_BALA]
    rows = []
    
    for planet_id in const.LIST_OBJECTS_VEDIC:
        result = shadbala_results[planet_id]
        rows.append([
            planet_id,
            f"{result['sthana_bala']:.2f}",
            f"{result['dig_bala']:.2f}",
            f"{result['kala_bala']:.2f}",
            f"{result['cheshta_bala']:.2f}",
            f"{result['naisargika_bala']:.2f}",
            f"{result['drig_bala']:.2f}"
        ])
    
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def print_ishta_kashta_phala(shadbala_results):
    """
    Print Ishta and Kashta Phala for each planet
    
    Args:
        shadbala_results (dict): Dictionary with Shadbala results
    """
    print(f"\n{'=' * 60}")
    print(f"Ishta and Kashta Phala")
    print(f"{'=' * 60}")
    
    headers = ["Planet", "Ishta Phala", "Description", "Kashta Phala", "Description"]
    rows = []
    
    for planet_id in const.LIST_OBJECTS_VEDIC:
        result = shadbala_results[planet_id]
        rows.append([
            planet_id,
            f"{result['ishta_phala']['value']:.2f}",
            result['ishta_phala']['description'],
            f"{result['kashta_phala']['value']:.2f}",
            result['kashta_phala']['description']
        ])
    
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def print_bhava_bala(chart):
    """
    Print Bhava Bala for each house
    
    Args:
        chart (Chart): Astrovedic Chart object
    """
    print(f"\n{'=' * 60}")
    print(f"Bhava Bala (House Strength)")
    print(f"{'=' * 60}")
    
    headers = ["House", "Total Bala", "Description"]
    rows = []
    
    for house_num in range(1, 13):
        house_id = f"House{house_num}"
        result = get_bhava_bala(chart, house_id)
        rows.append([
            house_id,
            f"{result['total']:.2f}",
            result['description']
        ])
    
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def main():
    """Main function"""
    args = parse_args()
    
    # Create chart
    chart, date = create_chart(
        args.date, args.time, args.lat, args.lon, args.ayanamsa
    )
    
    # Print chart information
    print_chart_info(chart, args.location, args.ayanamsa)
    
    # Calculate Shadbala for all planets
    shadbala_results = get_all_shadbala(chart)
    
    # Print Shadbala summary
    print_shadbala_summary(shadbala_results)
    
    # Print Shadbala components
    print_shadbala_components(shadbala_results)
    
    # Print Ishta and Kashta Phala
    print_ishta_kashta_phala(shadbala_results)
    
    # Print Bhava Bala
    print_bhava_bala(chart)

if __name__ == "__main__":
    main()
