#!/usr/bin/env python3
"""
Divisional Charts (Vargas) Example

This script demonstrates how to use flatlib for Vedic divisional chart calculations.
It includes:
- Creating divisional charts (D1 through D60)
- Analyzing planetary positions in divisional charts
- Calculating Varga Visesha (special divisional chart strengths)

Usage:
  python divisional_charts.py                   # Generate charts for current time
  python divisional_charts.py YYYY/MM/DD HH:MM  # Generate charts for specific date and time
  python divisional_charts.py -h, --help        # Show help message
"""

import sys
import argparse
from tabulate import tabulate

from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib.vedic.vargas import (
    D1, D2, D3, D4, D7, D9, D10, D12, 
    D16, D20, D24, D27, D30, D40, D45, D60,
    get_varga_chart, get_varga_name, get_varga_description
)
from flatlib.vedic.vargas.analysis import get_varga_visesha

# Default location: Bangalore, India
DEFAULT_LAT = 12.9716
DEFAULT_LON = 77.5946
DEFAULT_LOCATION = "Bangalore, India"

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Generate Vedic divisional charts')
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
        chart (Chart): Flatlib Chart object
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
    print(f"Planetary Positions (D1 - Rashi Chart)")
    print(f"{'=' * 60}")
    
    headers = ["Planet", "Sign", "Longitude", "Nakshatra"]
    rows = []
    
    for planet_id in const.LIST_OBJECTS_VEDIC:
        planet = chart.getObject(planet_id)
        
        # Get nakshatra information
        from flatlib.vedic.nakshatras import get_nakshatra
        nakshatra_info = get_nakshatra(planet.lon)
        
        rows.append([
            planet.id,
            f"{planet.sign}",
            f"{planet.signlon:.2f}°",
            f"{nakshatra_info['name']} {nakshatra_info['pada']}"
        ])
    
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def print_divisional_chart(chart, varga_type):
    """
    Print planetary positions in a divisional chart
    
    Args:
        chart (Chart): Flatlib Chart object
        varga_type (str): The type of divisional chart (e.g., D9, D10)
    """
    # Get the divisional chart
    varga_chart = get_varga_chart(chart, varga_type)
    
    # Get the Sanskrit name and description
    varga_name = get_varga_name(varga_type)
    varga_desc = get_varga_description(varga_type)
    
    print(f"\n{'=' * 60}")
    print(f"{varga_type} - {varga_name} Chart ({varga_desc})")
    print(f"{'=' * 60}")
    
    headers = ["Planet", "Sign", "Longitude"]
    rows = []
    
    for planet_id in const.LIST_OBJECTS_VEDIC:
        planet = varga_chart.getObject(planet_id)
        rows.append([
            planet.id,
            f"{planet.sign}",
            f"{planet.signlon:.2f}°"
        ])
    
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def print_varga_visesha(chart):
    """
    Print Varga Visesha (special divisional chart strengths) for all planets
    
    Args:
        chart (Chart): Flatlib Chart object
    """
    print(f"\n{'=' * 60}")
    print(f"Varga Visesha (Special Divisional Chart Strengths)")
    print(f"{'=' * 60}")
    
    headers = ["Planet", "Highest Varga Visesha", "Details"]
    rows = []
    
    for planet_id in const.LIST_OBJECTS_VEDIC:
        visesha = get_varga_visesha(chart, planet_id)
        
        # Create details string
        details = []
        if visesha['parijatamsha']:
            details.append("Parijatamsha (D1=D9)")
        if visesha['uttamamsha']:
            details.append("Uttamamsha (D1=D2=D9)")
        if visesha['gopuramsha']:
            details.append("Gopuramsha (D1=D2=D3=D9)")
        if visesha['simhasanamsha']:
            details.append("Simhasanamsha (D1=D2=D3=D9=D12)")
        if visesha['paravatamsha']:
            details.append("Paravatamsha (D1=D2=D3=D9=D12=D30)")
        if visesha['devalokamsha']:
            details.append("Devalokamsha (D1=D2=D3=D4=D9=D12=D30)")
        if visesha['brahmalokamsha']:
            details.append("Brahmalokamsha (D1=D2=D3=D4=D9=D12=D16=D30)")
        
        details_str = ", ".join(details) if details else "None"
        
        rows.append([
            planet_id,
            visesha['highest'] or "None",
            details_str
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
    
    # Print divisional charts
    for varga_type in [D1, D2, D3, D4, D7, D9, D10, D12, D16, D20, D24, D27, D30, D40, D45, D60]:
        print_divisional_chart(chart, varga_type)
    
    # Print Varga Visesha
    print_varga_visesha(chart)

if __name__ == "__main__":
    main()
