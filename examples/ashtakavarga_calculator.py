#!/usr/bin/env python3
"""
Ashtakavarga Calculator Example

This script demonstrates how to use flatlib for Ashtakavarga (eight-source strength)
calculations in Vedic astrology. It includes:
- Calculating Bhinnashtakavarga (individual ashtakavarga) for each planet
- Calculating Sarvashtakavarga (combined ashtakavarga)
- Analyzing Kaksha Bala (zodiacal strength)
- Generating transit predictions using Ashtakavarga

Usage:
  python ashtakavarga_calculator.py                   # Generate calculations for current time
  python ashtakavarga_calculator.py YYYY/MM/DD HH:MM  # Generate calculations for specific date and time
  python ashtakavarga_calculator.py -h, --help        # Show help message
"""

import sys
import argparse
from tabulate import tabulate

from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib.vedic.ashtakavarga import (
    get_bhinnashtakavarga, get_sarvashtakavarga, get_all_ashtakavarga,
    get_kaksha_bala, get_transit_ashtakavarga, LIST_ASHTAKAVARGA_PLANETS
)
from flatlib.vedic.ashtakavarga.analysis import (
    get_ashtakavarga_predictions, get_ashtakavarga_strength_in_house
)

# Default location: Bangalore, India
DEFAULT_LAT = 12.9716
DEFAULT_LON = 77.5946
DEFAULT_LOCATION = "Bangalore, India"

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Calculate Ashtakavarga (eight-source strength)')
    parser.add_argument('date', nargs='?', help='Date in YYYY/MM/DD format')
    parser.add_argument('time', nargs='?', help='Time in HH:MM format')
    parser.add_argument('--lat', type=float, default=DEFAULT_LAT, help='Latitude')
    parser.add_argument('--lon', type=float, default=DEFAULT_LON, help='Longitude')
    parser.add_argument('--location', default=DEFAULT_LOCATION, help='Location name')
    parser.add_argument('--ayanamsa', default=const.AY_LAHIRI, help='Ayanamsa to use')
    parser.add_argument('--transit-date', help='Transit date in YYYY/MM/DD format')
    parser.add_argument('--transit-time', help='Transit time in HH:MM format')
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

def print_bhinnashtakavarga(bhinna):
    """
    Print Bhinnashtakavarga (individual ashtakavarga) information
    
    Args:
        bhinna (dict): Dictionary with Bhinnashtakavarga information
    """
    print(f"\n{'=' * 60}")
    print(f"Bhinnashtakavarga for {bhinna['planet']}")
    print(f"{'=' * 60}")
    
    # Print the total bindus
    print(f"Total Bindus: {bhinna['total_bindus']} out of 56")
    
    # Print the bindus in each sign
    print(f"\nBindus in Each Sign:")
    
    headers = ["Sign", "Bindus"]
    rows = []
    
    signs = [
        const.ARIES, const.TAURUS, const.GEMINI, const.CANCER,
        const.LEO, const.VIRGO, const.LIBRA, const.SCORPIO,
        const.SAGITTARIUS, const.CAPRICORN, const.AQUARIUS, const.PISCES
    ]
    
    for i, sign in enumerate(signs):
        rows.append([sign, bhinna['points'][i]])
    
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    
    # Print the contributors
    print(f"\nContributions from Each Planet:")
    
    headers = ["Contributor"] + signs
    rows = []
    
    contributors = [const.SUN, const.MOON, const.MARS, const.MERCURY,
                   const.JUPITER, const.VENUS, const.SATURN, const.ASC]
    
    for contributor in contributors:
        row = [contributor]
        for i in range(12):
            row.append(bhinna['contributors'][contributor][i])
        rows.append(row)
    
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def print_sarvashtakavarga(sarva):
    """
    Print Sarvashtakavarga (combined ashtakavarga) information
    
    Args:
        sarva (dict): Dictionary with Sarvashtakavarga information
    """
    print(f"\n{'=' * 60}")
    print(f"Sarvashtakavarga")
    print(f"{'=' * 60}")
    
    # Print the total bindus
    print(f"Total Bindus: {sarva['total_bindus']} out of 337")
    
    # Print the bindus in each sign
    print(f"\nBindus in Each Sign:")
    
    headers = ["Sign", "Bindus"]
    rows = []
    
    signs = [
        const.ARIES, const.TAURUS, const.GEMINI, const.CANCER,
        const.LEO, const.VIRGO, const.LIBRA, const.SCORPIO,
        const.SAGITTARIUS, const.CAPRICORN, const.AQUARIUS, const.PISCES
    ]
    
    for i, sign in enumerate(signs):
        rows.append([sign, sarva['points'][i]])
    
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    
    # Print the bindus in each house
    print(f"\nBindus in Each House:")
    
    headers = ["House", "Bindus"]
    rows = []
    
    for i, bindus in enumerate(sarva['bindus_in_houses']):
        rows.append([i + 1, bindus])
    
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    
    # Print the Sodhita Sarvashtakavarga
    print(f"\nSodhita Sarvashtakavarga (after reductions):")
    
    headers = ["Sign", "Original", "Trikona Sodhana", "Sodhita"]
    rows = []
    
    for i, sign in enumerate(signs):
        rows.append([
            sign,
            sarva['points'][i],
            sarva['trikona_sodhana'][i],
            sarva['sodhita_sarvashtakavarga'][i]
        ])
    
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def print_kaksha_bala(chart):
    """
    Print Kaksha Bala (zodiacal strength) information
    
    Args:
        chart (Chart): Flatlib Chart object
    """
    print(f"\n{'=' * 60}")
    print(f"Kaksha Bala (Zodiacal Strength)")
    print(f"{'=' * 60}")
    
    headers = ["Planet", "Sign", "Kaksha Bala", "Percentage", "Category"]
    rows = []
    
    for planet_id in LIST_ASHTAKAVARGA_PLANETS:
        kaksha = get_kaksha_bala(chart, planet_id)
        rows.append([
            planet_id,
            kaksha['sign'],
            kaksha['kaksha_bala'],
            f"{kaksha['percentage']:.2f}%",
            kaksha['category']
        ])
    
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def print_house_strengths(chart):
    """
    Print Ashtakavarga strength for each house
    
    Args:
        chart (Chart): Flatlib Chart object
    """
    print(f"\n{'=' * 60}")
    print(f"Ashtakavarga Strength for Each House")
    print(f"{'=' * 60}")
    
    headers = ["House", "Sign", "Total Bindus", "Percentage", "Category"]
    rows = []
    
    for house_num in range(1, 13):
        strength = get_ashtakavarga_strength_in_house(chart, house_num)
        rows.append([
            house_num,
            strength['sign'],
            strength['total_bindus'],
            f"{strength['percentage']:.2f}%",
            strength['category']
        ])
    
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def print_transit_predictions(birth_chart, transit_chart):
    """
    Print transit predictions based on Ashtakavarga
    
    Args:
        birth_chart (Chart): The birth chart
        transit_chart (Chart): The transit chart
    """
    print(f"\n{'=' * 60}")
    print(f"Transit Predictions using Ashtakavarga")
    print(f"{'=' * 60}")
    
    headers = ["Planet", "Transit Sign", "Bindus", "Category", "Description"]
    rows = []
    
    for planet_id in LIST_ASHTAKAVARGA_PLANETS:
        transit = get_transit_ashtakavarga(birth_chart, transit_chart, planet_id)
        rows.append([
            planet_id,
            transit['transit_sign'],
            transit['transit_strength']['bindus'],
            transit['transit_strength']['category'],
            transit['transit_strength']['description']
        ])
    
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    
    # Print best transit positions for each planet
    print(f"\nBest Transit Positions:")
    
    for planet_id in LIST_ASHTAKAVARGA_PLANETS:
        transit = get_transit_ashtakavarga(birth_chart, transit_chart, planet_id)
        best_positions = transit['best_positions']
        
        # Convert sign numbers to sign names
        signs = [
            const.ARIES, const.TAURUS, const.GEMINI, const.CANCER,
            const.LEO, const.VIRGO, const.LIBRA, const.SCORPIO,
            const.SAGITTARIUS, const.CAPRICORN, const.AQUARIUS, const.PISCES
        ]
        
        best_signs = [signs[pos] for pos in best_positions[:3]]
        
        print(f"{planet_id}: {', '.join(best_signs)}")

def print_ashtakavarga_predictions(chart):
    """
    Print predictions based on Ashtakavarga
    
    Args:
        chart (Chart): Flatlib Chart object
    """
    print(f"\n{'=' * 60}")
    print(f"Ashtakavarga Predictions")
    print(f"{'=' * 60}")
    
    # Calculate all Ashtakavarga data
    ashtakavarga_data = get_all_ashtakavarga(chart)
    
    # Generate predictions
    predictions = get_ashtakavarga_predictions(ashtakavarga_data)
    
    # Print general predictions
    print("General Predictions:")
    for prediction in predictions['general']:
        print(f"- {prediction}")
    
    # Print planet predictions
    print("\nPlanet Predictions:")
    for planet_id, prediction in predictions['planets'].items():
        print(f"{planet_id}: {prediction}")
    
    # Print house predictions
    print("\nHouse Predictions:")
    for house_num, prediction in predictions['houses'].items():
        print(f"House {house_num}: {prediction}")

def main():
    """Main function"""
    args = parse_args()
    
    # Create birth chart
    birth_chart, birth_date = create_chart(
        args.date, args.time, args.lat, args.lon, args.ayanamsa
    )
    
    # Print chart information
    print_chart_info(birth_chart, args.location, args.ayanamsa)
    
    # Calculate and print Bhinnashtakavarga for each planet
    for planet_id in LIST_ASHTAKAVARGA_PLANETS:
        bhinna = get_bhinnashtakavarga(birth_chart, planet_id)
        print_bhinnashtakavarga(bhinna)
    
    # Calculate and print Sarvashtakavarga
    sarva = get_sarvashtakavarga(birth_chart)
    print_sarvashtakavarga(sarva)
    
    # Calculate and print Kaksha Bala
    print_kaksha_bala(birth_chart)
    
    # Calculate and print house strengths
    print_house_strengths(birth_chart)
    
    # Generate and print predictions
    print_ashtakavarga_predictions(birth_chart)
    
    # If transit date and time are provided, calculate transit predictions
    if args.transit_date and args.transit_time:
        # Create transit chart
        transit_chart, transit_date = create_chart(
            args.transit_date, args.transit_time, args.lat, args.lon, args.ayanamsa
        )
        
        # Print transit predictions
        print_transit_predictions(birth_chart, transit_chart)

if __name__ == "__main__":
    main()
