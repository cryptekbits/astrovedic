#!/usr/bin/env python3
"""
Sarvatobhadra Chakra Calculator Example

This script demonstrates how to use flatlib for Sarvatobhadra Chakra
calculations in Vedic astrology. It includes:
- Creating and displaying the Sarvatobhadra Chakra
- Finding auspicious directions
- Analyzing Tara Bala (lunar strength)
- Generating predictions based on Sarvatobhadra Chakra

Usage:
  python sarvatobhadra_calculator.py                   # Generate calculations for current time
  python sarvatobhadra_calculator.py YYYY/MM/DD HH:MM  # Generate calculations for specific date and time
  python sarvatobhadra_calculator.py -h, --help        # Show help message
"""

import sys
import argparse
from tabulate import tabulate

from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic import const
from astrovedic.vedic.sarvatobhadra import (
    get_sarvatobhadra_chakra, get_chakra_quality,
    get_auspicious_directions, get_inauspicious_directions,
    get_best_direction, get_direction_for_activity,
    get_tara_bala, get_basic_sarvatobhadra_analysis
)

# Default location: Bangalore, India
DEFAULT_LAT = 12.9716
DEFAULT_LON = 77.5946
DEFAULT_LOCATION = "Bangalore, India"

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Calculate Sarvatobhadra Chakra')
    parser.add_argument('date', nargs='?', help='Date in YYYY/MM/DD format')
    parser.add_argument('time', nargs='?', help='Time in HH:MM format')
    parser.add_argument('--lat', type=float, default=DEFAULT_LAT, help='Latitude')
    parser.add_argument('--lon', type=float, default=DEFAULT_LON, help='Longitude')
    parser.add_argument('--location', default=DEFAULT_LOCATION, help='Location name')
    parser.add_argument('--ayanamsa', default=const.AY_LAHIRI, help='Ayanamsa to use')
    parser.add_argument('--activity', help='Activity to find auspicious direction for')
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
    print(f"Chart Information")
    print(f"{'=' * 60}")
    print(f"Date: {chart.date}")
    print(f"Location: {location} ({chart.pos.lat:.4f}, {chart.pos.lon:.4f})")
    print(f"Ayanamsa: {ayanamsa}")
    print(f"House System: {chart.hsys}")
    
    # Print ascendant
    asc = chart.getAngle(const.ASC)
    print(f"Ascendant: {asc.sign} {asc.signlon:.2f}°")

def print_sarvatobhadra_chakra(chakra):
    """
    Print the Sarvatobhadra Chakra
    
    Args:
        chakra (dict): The Sarvatobhadra Chakra
    """
    print(f"\n{'=' * 60}")
    print(f"Sarvatobhadra Chakra")
    print(f"{'=' * 60}")
    print(f"Birth Nakshatra (Janma Tara): {chakra['janma_nakshatra']}")
    
    # Print the chakra grid
    grid = chakra['grid']
    
    # Create a formatted grid for display
    formatted_grid = []
    for row in grid:
        formatted_row = []
        for cell in row:
            # Check if any planet is in this cell
            planets_in_cell = []
            for planet_id, planet_info in chakra['planets'].items():
                position = planet_info['position']
                if position and position[0] == grid.index(row) and position[1] == row.index(cell):
                    planets_in_cell.append(planet_id)
            
            # Format the cell
            if planets_in_cell:
                formatted_row.append(f"{cell} ({', '.join(planets_in_cell)})")
            else:
                formatted_row.append(str(cell))
        
        formatted_grid.append(formatted_row)
    
    # Print the grid
    print("\nSarvatobhadra Chakra Grid:")
    print(tabulate(formatted_grid, tablefmt="grid"))

def print_chakra_quality(chakra):
    """
    Print the quality of the Sarvatobhadra Chakra
    
    Args:
        chakra (dict): The Sarvatobhadra Chakra
    """
    # Get the chakra quality
    quality = get_chakra_quality(chakra)
    
    print(f"\n{'=' * 60}")
    print(f"Chakra Quality")
    print(f"{'=' * 60}")
    print(f"Quality: {quality['quality']}")
    print(f"Score: {quality['score']}")
    
    print("\nFactors:")
    for factor in quality['factors']:
        print(f"  - {factor}")

def print_auspicious_directions(chakra):
    """
    Print the auspicious directions
    
    Args:
        chakra (dict): The Sarvatobhadra Chakra
    """
    # Get the auspicious directions
    auspicious_directions = get_auspicious_directions(chakra)
    
    print(f"\n{'=' * 60}")
    print(f"Auspicious Directions")
    print(f"{'=' * 60}")
    
    if not auspicious_directions:
        print("No auspicious directions found.")
        return
    
    for direction in auspicious_directions:
        print(f"\n{direction['direction']} ({direction['quality']})")
        print(f"Score: {direction['score']}")
        
        print("Factors:")
        for factor in direction['factors']:
            print(f"  - {factor}")

def print_inauspicious_directions(chakra):
    """
    Print the inauspicious directions
    
    Args:
        chakra (dict): The Sarvatobhadra Chakra
    """
    # Get the inauspicious directions
    inauspicious_directions = get_inauspicious_directions(chakra)
    
    print(f"\n{'=' * 60}")
    print(f"Inauspicious Directions")
    print(f"{'=' * 60}")
    
    if not inauspicious_directions:
        print("No inauspicious directions found.")
        return
    
    for direction in inauspicious_directions:
        print(f"\n{direction['direction']} ({direction['quality']})")
        print(f"Score: {direction['score']}")
        
        print("Factors:")
        for factor in direction['factors']:
            print(f"  - {factor}")

def print_best_direction(chakra):
    """
    Print the best direction
    
    Args:
        chakra (dict): The Sarvatobhadra Chakra
    """
    # Get the best direction
    best_direction = get_best_direction(chakra)
    
    print(f"\n{'=' * 60}")
    print(f"Best Direction")
    print(f"{'=' * 60}")
    print(f"Direction: {best_direction['direction']}")
    print(f"Quality: {best_direction['quality']}")
    print(f"Score: {best_direction['score']}")
    
    print("\nFactors:")
    for factor in best_direction['factors']:
        print(f"  - {factor}")

def print_tara_bala(chakra):
    """
    Print the Tara Bala (lunar strength)
    
    Args:
        chakra (dict): The Sarvatobhadra Chakra
    """
    # Get the Tara Bala
    tara_bala = chakra['tara_bala']
    
    print(f"\n{'=' * 60}")
    print(f"Tara Bala (Lunar Strength)")
    print(f"{'=' * 60}")
    print(f"Current Tara: {tara_bala['current_tara']}")
    print(f"Score: {tara_bala['score']}")
    
    print("\nTara Positions:")
    print(f"  Janma Tara (Birth Star): {tara_bala['janma_tara']}")
    print(f"  Sampath Tara (Wealth Star): {tara_bala['sampath_tara']}")
    print(f"  Vipat Tara (Danger Star): {tara_bala['vipat_tara']}")
    print(f"  Kshema Tara (Well-being Star): {tara_bala['kshema_tara']}")
    print(f"  Pratyak Tara (Obstacle Star): {tara_bala['pratyak_tara']}")
    print(f"  Sadhaka Tara (Accomplishment Star): {tara_bala['sadhaka_tara']}")
    print(f"  Vadha Tara (Obstruction Star): {tara_bala['vadha_tara']}")
    print(f"  Mitra Tara (Friendly Star): {tara_bala['mitra_tara']}")
    print(f"  Ati Mitra Tara (Very Friendly Star): {tara_bala['ati_mitra_tara']}")

def print_direction_for_activity(chakra, activity):
    """
    Print the best direction for a specific activity
    
    Args:
        chakra (dict): The Sarvatobhadra Chakra
        activity (str): The type of activity
    """
    # Get the best direction for the activity
    direction = get_direction_for_activity(chakra, activity)
    
    print(f"\n{'=' * 60}")
    print(f"Best Direction for {activity.capitalize()}")
    print(f"{'=' * 60}")
    print(f"Direction: {direction['direction']}")
    print(f"Quality: {direction['quality']}")
    print(f"Score: {direction['score']}")
    
    print("\nFactors:")
    for factor in direction['factors']:
        print(f"  - {factor}")

def print_basic_sarvatobhadra_analysis(chart):
    """
    Print basic analysis based on Sarvatobhadra Chakra
    
    Args:
        chart (Chart): The chart
    """
    # Get the basic analysis
    analysis = get_basic_sarvatobhadra_analysis(chart)
    
    print(f"\n{'=' * 60}")
    print(f"Sarvatobhadra Chakra Basic Analysis")
    print(f"{'=' * 60}")
    
    # Print chakra quality
    print(f"Chakra Quality: {analysis['quality']}")
    
    # Print auspicious directions
    print("\nAuspicious Directions:")
    if analysis['auspicious_directions']:
        for direction_info in analysis['auspicious_directions']:
            print(f"  - {direction_info['direction']} ({direction_info['quality']}, Score: {direction_info['score']})")
    else:
        print("  - None")

    # Print inauspicious directions
    print("\nInauspicious Directions:")
    if analysis['inauspicious_directions']:
        for direction_info in analysis['inauspicious_directions']:
            print(f"  - {direction_info['direction']} ({direction_info['quality']}, Score: {direction_info['score']})")
    else:
        print("  - None")

    # Print best direction
    print(f"\nBest Direction: {analysis['best_direction']}")

    # Print Tara Bala
    print("\nTara Bala:")
    if isinstance(analysis['tara_bala'], dict):
        print(f"  - Quality: {analysis['tara_bala'].get('quality', 'N/A')}")
        print(f"  - Tara: {analysis['tara_bala'].get('tara', 'N/A')}")
    else:
        print(f"  - {analysis['tara_bala']}")

def main():
    """Main function"""
    args = parse_args()
    
    # Create chart
    chart, date = create_chart(
        args.date, args.time, args.lat, args.lon, args.ayanamsa
    )
    
    # Print chart information
    print_chart_info(chart, args.location, args.ayanamsa)
    
    # Get the Sarvatobhadra Chakra
    chakra = get_sarvatobhadra_chakra(chart)
    
    # Print the Sarvatobhadra Chakra
    print_sarvatobhadra_chakra(chakra)
    
    # Print the chakra quality
    print_chakra_quality(chakra)
    
    # Print the auspicious directions
    print_auspicious_directions(chakra)
    
    # Print the inauspicious directions
    print_inauspicious_directions(chakra)
    
    # Print the best direction
    print_best_direction(chakra)
    
    # Print the Tara Bala
    print_tara_bala(chakra)
    
    # Print the best direction for a specific activity if requested
    if args.activity:
        print_direction_for_activity(chakra, args.activity)
    
    # Print the Sarvatobhadra Chakra basic analysis
    print_basic_sarvatobhadra_analysis(chart)

if __name__ == "__main__":
    main()
