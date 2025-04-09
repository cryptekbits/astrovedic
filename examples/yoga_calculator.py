#!/usr/bin/env python3
"""
Yoga Calculator Example

This script demonstrates how to use flatlib for Yoga (planetary combinations)
calculations in Vedic astrology. It includes:
- Identifying Pancha Mahapurusha Yogas
- Identifying Raja Yogas (combinations for power and authority)
- Identifying Dhana Yogas (combinations for wealth)
- Identifying Nabhasa Yogas (special planetary patterns)
- Identifying Dosha Yogas (combinations indicating difficulties)
- Identifying Chandra Yogas (Moon combinations)
- Analyzing the strength and effects of Yogas

Usage:
  python yoga_calculator.py                   # Generate calculations for current time
  python yoga_calculator.py YYYY/MM/DD HH:MM  # Generate calculations for specific date and time
  python yoga_calculator.py -h, --help        # Show help message
"""

import sys
import argparse
from tabulate import tabulate

from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib.vedic.yogas import (
    get_all_yogas, get_yoga_analysis, get_yoga_predictions,
    MAHAPURUSHA_YOGA, RAJA_YOGA, DHANA_YOGA,
    NABHASA_YOGA, DOSHA_YOGA, CHANDRA_YOGA
)

# Default location: Bangalore, India
DEFAULT_LAT = 12.9716
DEFAULT_LON = 77.5946
DEFAULT_LOCATION = "Bangalore, India"

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Calculate Yogas (planetary combinations)')
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
    print(f"Planetary Positions")
    print(f"{'=' * 60}")
    
    headers = ["Planet", "Sign", "Longitude", "House"]
    rows = []
    
    for planet_id in const.LIST_OBJECTS_VEDIC:
        planet = chart.getObject(planet_id)
        
        # Get the house number
        from flatlib.vedic.yogas.core import get_house_number
        house_num = get_house_number(chart, planet_id)
        
        rows.append([
            planet.id,
            f"{planet.sign}",
            f"{planet.signlon:.2f}°",
            f"{house_num}"
        ])
    
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def print_yoga_summary(yogas):
    """
    Print a summary of Yogas in a chart
    
    Args:
        yogas (dict): Dictionary with Yoga information
    """
    print(f"\n{'=' * 60}")
    print(f"Yoga Summary")
    print(f"{'=' * 60}")
    
    # Print summary information
    summary = yogas['summary']
    print(f"Total Yogas: {summary['total_yogas']}")
    print(f"Beneficial Yogas: {summary['beneficial_yogas']}")
    print(f"Harmful Yogas: {summary['harmful_yogas']}")
    
    # Print the strongest Yoga
    strongest_yoga = summary['strongest_yoga']
    if strongest_yoga:
        print(f"\nStrongest Yoga: {strongest_yoga['name']} ({strongest_yoga['type']})")
        print(f"Strength: {strongest_yoga['strength']:.2f}")
        print(f"Description: {strongest_yoga['description']}")
    
    # Print the number of Yogas of each type
    print(f"\nYoga Types:")
    for yoga_type, count in summary['yoga_types'].items():
        print(f"- {yoga_type}: {count}")

def print_mahapurusha_yogas(yogas):
    """
    Print Pancha Mahapurusha Yogas in a chart
    
    Args:
        yogas (dict): Dictionary with Yoga information
    """
    print(f"\n{'=' * 60}")
    print(f"Pancha Mahapurusha Yogas")
    print(f"{'=' * 60}")
    
    # Check if there are any Mahapurusha Yogas
    if not yogas['mahapurusha_yogas']:
        print("No Mahapurusha Yogas found in the chart.")
        return
    
    # Print each Mahapurusha Yoga
    for yoga in yogas['mahapurusha_yogas']:
        print(f"\n{yoga['name']}")
        print(f"Strength: {yoga['strength']:.2f}")
        print(f"Description: {yoga['description']}")
        print(f"Planets: {', '.join(yoga['planets'])}")
        print(f"Houses: {', '.join(str(house) for house in yoga['houses'])}")

def print_raja_yogas(yogas):
    """
    Print Raja Yogas in a chart
    
    Args:
        yogas (dict): Dictionary with Yoga information
    """
    print(f"\n{'=' * 60}")
    print(f"Raja Yogas (Combinations for Power and Authority)")
    print(f"{'=' * 60}")
    
    # Check if there are any Raja Yogas
    if not yogas['raja_yogas']:
        print("No Raja Yogas found in the chart.")
        return
    
    # Print each Raja Yoga
    for yoga in yogas['raja_yogas']:
        print(f"\n{yoga['name']}")
        print(f"Strength: {yoga['strength']:.2f}")
        print(f"Description: {yoga['description']}")
        print(f"Planets: {', '.join(yoga['planets'])}")
        print(f"Houses: {', '.join(str(house) for house in yoga['houses'])}")

def print_dhana_yogas(yogas):
    """
    Print Dhana Yogas in a chart
    
    Args:
        yogas (dict): Dictionary with Yoga information
    """
    print(f"\n{'=' * 60}")
    print(f"Dhana Yogas (Combinations for Wealth)")
    print(f"{'=' * 60}")
    
    # Check if there are any Dhana Yogas
    if not yogas['dhana_yogas']:
        print("No Dhana Yogas found in the chart.")
        return
    
    # Print each Dhana Yoga
    for yoga in yogas['dhana_yogas']:
        print(f"\n{yoga['name']}")
        print(f"Strength: {yoga['strength']:.2f}")
        print(f"Description: {yoga['description']}")
        print(f"Planets: {', '.join(yoga['planets'])}")
        print(f"Houses: {', '.join(str(house) for house in yoga['houses'])}")

def print_nabhasa_yogas(yogas):
    """
    Print Nabhasa Yogas in a chart
    
    Args:
        yogas (dict): Dictionary with Yoga information
    """
    print(f"\n{'=' * 60}")
    print(f"Nabhasa Yogas (Special Planetary Patterns)")
    print(f"{'=' * 60}")
    
    # Check if there are any Nabhasa Yogas
    if not yogas['nabhasa_yogas']:
        print("No Nabhasa Yogas found in the chart.")
        return
    
    # Print each Nabhasa Yoga
    for yoga in yogas['nabhasa_yogas']:
        print(f"\n{yoga['name']}")
        print(f"Strength: {yoga['strength']:.2f}")
        print(f"Description: {yoga['description']}")
        print(f"Planets: {', '.join(yoga['planets'])}")
        if yoga['houses']:
            print(f"Houses: {', '.join(str(house) for house in yoga['houses'])}")

def print_dosha_yogas(yogas):
    """
    Print Dosha Yogas in a chart
    
    Args:
        yogas (dict): Dictionary with Yoga information
    """
    print(f"\n{'=' * 60}")
    print(f"Dosha Yogas (Combinations Indicating Difficulties)")
    print(f"{'=' * 60}")
    
    # Check if there are any Dosha Yogas
    if not yogas['dosha_yogas']:
        print("No Dosha Yogas found in the chart.")
        return
    
    # Print each Dosha Yoga
    for yoga in yogas['dosha_yogas']:
        print(f"\n{yoga['name']}")
        print(f"Strength: {yoga['strength']:.2f}")
        print(f"Description: {yoga['description']}")
        print(f"Planets: {', '.join(yoga['planets'])}")
        print(f"Houses: {', '.join(str(house) for house in yoga['houses'])}")

def print_chandra_yogas(yogas):
    """
    Print Chandra Yogas in a chart
    
    Args:
        yogas (dict): Dictionary with Yoga information
    """
    print(f"\n{'=' * 60}")
    print(f"Chandra Yogas (Moon Combinations)")
    print(f"{'=' * 60}")
    
    # Check if there are any Chandra Yogas
    if not yogas['chandra_yogas']:
        print("No Chandra Yogas found in the chart.")
        return
    
    # Print each Chandra Yoga
    for yoga in yogas['chandra_yogas']:
        print(f"\n{yoga['name']}")
        print(f"Strength: {yoga['strength']:.2f}")
        print(f"Description: {yoga['description']}")
        print(f"Planets: {', '.join(yoga['planets'])}")
        print(f"Houses: {', '.join(str(house) for house in yoga['houses'])}")

def print_yoga_effects(chart, yogas):
    """
    Print the effects of Yogas in a chart
    
    Args:
        chart (Chart): Flatlib Chart object
        yogas (dict): Dictionary with Yoga information
    """
    print(f"\n{'=' * 60}")
    print(f"Yoga Effects")
    print(f"{'=' * 60}")
    
    # Get the Yoga analysis
    analysis = get_yoga_analysis(chart)
    
    # Print the effects of each Yoga
    for effect in analysis['effects']:
        print(f"\n{effect['name']} ({effect['type']})")
        for e in effect['effects']:
            print(f"- {e}")

def print_yoga_predictions(chart):
    """
    Print predictions based on Yogas in a chart
    
    Args:
        chart (Chart): Flatlib Chart object
    """
    print(f"\n{'=' * 60}")
    print(f"Yoga Predictions")
    print(f"{'=' * 60}")
    
    # Get the Yoga predictions
    predictions = get_yoga_predictions(chart)
    
    # Print general predictions
    print("\nGeneral:")
    for prediction in predictions['general']:
        print(f"- {prediction}")
    
    # Print personality predictions
    if predictions['personality']:
        print("\nPersonality:")
        for prediction in predictions['personality']:
            print(f"- {prediction}")
    
    # Print career predictions
    if predictions['career']:
        print("\nCareer:")
        for prediction in predictions['career']:
            print(f"- {prediction}")
    
    # Print wealth predictions
    if predictions['wealth']:
        print("\nWealth:")
        for prediction in predictions['wealth']:
            print(f"- {prediction}")
    
    # Print relationship predictions
    if predictions['relationships']:
        print("\nRelationships:")
        for prediction in predictions['relationships']:
            print(f"- {prediction}")
    
    # Print health predictions
    if predictions['health']:
        print("\nHealth:")
        for prediction in predictions['health']:
            print(f"- {prediction}")
    
    # Print challenge predictions
    if predictions['challenges']:
        print("\nChallenges:")
        for prediction in predictions['challenges']:
            print(f"- {prediction}")

def main():
    """Main function"""
    args = parse_args()
    
    # Create chart
    chart, date = create_chart(
        args.date, args.time, args.lat, args.lon, args.ayanamsa
    )
    
    # Print chart information
    print_chart_info(chart, args.location, args.ayanamsa)
    
    # Calculate all Yogas
    yogas = get_all_yogas(chart)
    
    # Print Yoga summary
    print_yoga_summary(yogas)
    
    # Print each type of Yoga
    print_mahapurusha_yogas(yogas)
    print_raja_yogas(yogas)
    print_dhana_yogas(yogas)
    print_nabhasa_yogas(yogas)
    print_dosha_yogas(yogas)
    print_chandra_yogas(yogas)
    
    # Print Yoga effects
    print_yoga_effects(chart, yogas)
    
    # Print Yoga predictions
    print_yoga_predictions(chart)

if __name__ == "__main__":
    main()
