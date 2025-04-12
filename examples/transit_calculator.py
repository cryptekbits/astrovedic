#!/usr/bin/env python3
"""
Transit Calculator Example

This script demonstrates how to use flatlib for transit analysis
in Vedic astrology. It includes:
- Calculating transit positions and aspects
- Analyzing Gochara (planetary transits)
- Generating transit predictions
- Creating transit timelines

Usage:
  python transit_calculator.py                   # Generate calculations for current time
  python transit_calculator.py YYYY/MM/DD HH:MM  # Generate calculations for specific date and time
  python transit_calculator.py -h, --help        # Show help message
"""

import sys
import argparse
from datetime import datetime, timedelta
from tabulate import tabulate

from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib.vedic.transits import (
    get_transits, get_transit_predictions_for_date,
    get_transit_timeline_for_period, analyze_transit_period,
    get_transit_chart, get_transit_planets, get_transit_aspects,
    get_transit_houses, get_transit_quality, get_gochara_effects,
    get_transit_ashtakavarga, get_transit_dasha_effects
    # Removed get_transit_analysis as it's not available and seemingly unused
)

# Default location: Bangalore, India
DEFAULT_LAT = 12.9716
DEFAULT_LON = 77.5946
DEFAULT_LOCATION = "Bangalore, India"

# Default birth date: January 1, 1990, 12:00 PM
DEFAULT_BIRTH_DATE = "1990/01/01"
DEFAULT_BIRTH_TIME = "12:00"

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Calculate transits in Vedic astrology')
    parser.add_argument('date', nargs='?', help='Transit date in YYYY/MM/DD format')
    parser.add_argument('time', nargs='?', help='Transit time in HH:MM format')
    parser.add_argument('--birth-date', default=DEFAULT_BIRTH_DATE, help='Birth date in YYYY/MM/DD format')
    parser.add_argument('--birth-time', default=DEFAULT_BIRTH_TIME, help='Birth time in HH:MM format')
    parser.add_argument('--lat', type=float, default=DEFAULT_LAT, help='Latitude')
    parser.add_argument('--lon', type=float, default=DEFAULT_LON, help='Longitude')
    parser.add_argument('--location', default=DEFAULT_LOCATION, help='Location name')
    parser.add_argument('--ayanamsa', default=const.AY_LAHIRI, help='Ayanamsa to use')
    parser.add_argument('--days', type=int, default=30, help='Number of days for timeline')
    return parser.parse_args()

def create_natal_chart(birth_date, birth_time, lat, lon, ayanamsa):
    """
    Create a natal chart
    
    Args:
        birth_date (str): Birth date in YYYY/MM/DD format
        birth_time (str): Birth time in HH:MM format
        lat (float): Latitude
        lon (float): Longitude
        ayanamsa (str): Ayanamsa to use
    
    Returns:
        Chart: The natal chart
    """
    # Create date and location objects
    date = Datetime(birth_date, birth_time, '+05:30')  # Indian Standard Time
    pos = GeoPos(lat, lon)
    
    # Create chart with specified ayanamsa and Whole Sign houses
    chart = Chart(date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=ayanamsa)
    
    return chart

def create_transit_chart(transit_date, transit_time, lat, lon, ayanamsa):
    """
    Create a transit chart
    
    Args:
        transit_date (str): Transit date in YYYY/MM/DD format
        transit_time (str): Transit time in HH:MM format
        lat (float): Latitude
        lon (float): Longitude
        ayanamsa (str): Ayanamsa to use
    
    Returns:
        tuple: (chart, date)
    """
    from datetime import datetime
    
    # Use current date and time if not provided
    if transit_date is None or transit_time is None:
        now = datetime.now()
        transit_date = now.strftime("%Y/%m/%d")
        transit_time = now.strftime("%H:%M")
    
    # Create date and location objects
    date = Datetime(transit_date, transit_time, '+05:30')  # Indian Standard Time
    pos = GeoPos(lat, lon)
    
    # Create chart with specified ayanamsa and Whole Sign houses
    chart = Chart(date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=ayanamsa)
    
    return chart, date

def print_chart_info(chart, chart_type, location, ayanamsa):
    """
    Print basic chart information
    
    Args:
        chart (Chart): Flatlib Chart object
        chart_type (str): Type of chart ('Natal' or 'Transit')
        location (str): Location name
        ayanamsa (str): Ayanamsa used
    """
    print(f"\n{'=' * 60}")
    print(f"{chart_type} Chart Information")
    print(f"{'=' * 60}")
    print(f"Date: {chart.date}")
    print(f"Location: {location} ({chart.pos.lat:.4f}, {chart.pos.lon:.4f})")
    print(f"Ayanamsa: {ayanamsa}")
    print(f"House System: {chart.hsys}")
    
    # Print ascendant
    asc = chart.getAngle(const.ASC)
    print(f"Ascendant: {asc.sign} {asc.signlon:.2f}°")
    
    # Print planets
    print("\nPlanetary Positions:")
    for planet_id in const.LIST_OBJECTS_VEDIC:
        planet = chart.getObject(planet_id)
        retrograde_status = ''
        if hasattr(planet, 'isRetrograde') and planet.isRetrograde():
            retrograde_status = ' (R)'
        print(f"  {planet_id}: {planet.sign} {planet.signlon:.2f}°{retrograde_status}")

def print_transit_planets(transit_planets):
    """
    Print transit planet information
    
    Args:
        transit_planets (dict): Transit planet information
    """
    print(f"\n{'=' * 60}")
    print(f"Transit Planets")
    print(f"{'=' * 60}")
    
    # Create a table
    headers = ["Planet", "Natal Sign", "Transit Sign", "House", "Distance", "Retrograde"]
    rows = []
    
    for planet_id, planet_info in transit_planets.items():
        rows.append([
            planet_id,
            planet_info['natal_sign'],
            planet_info['transit_sign'],
            planet_info['house'],
            f"{planet_info['distance']:.2f}°",
            "Yes" if planet_info['is_retrograde'] else "No"
        ])
    
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def print_transit_aspects(transit_aspects):
    """
    Print transit aspect information
    
    Args:
        transit_aspects (list): Transit aspect information
    """
    print(f"\n{'=' * 60}")
    print(f"Transit Aspects")
    print(f"{'=' * 60}")
    
    if not transit_aspects:
        print("No significant transit aspects found.")
        return
    
    # Create a table
    headers = ["Transit Planet", "Aspect", "Natal Planet", "Orb", "Applying"]
    rows = []
    
    for aspect in transit_aspects:
        rows.append([
            aspect['transit_planet'],
            aspect['aspect'],
            aspect['natal_planet'],
            f"{aspect['orb']:.2f}°",
            "Yes" if aspect['applying'] else "No"
        ])
    
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def print_transit_houses(transit_houses):
    """
    Print transit house information
    
    Args:
        transit_houses (dict): Transit house information
    """
    print(f"\n{'=' * 60}")
    print(f"Transit Houses")
    print(f"{'=' * 60}")
    
    # Create a table
    headers = ["House", "Sign", "Transit Planets"]
    rows = []
    
    for house_num, house_info in transit_houses.items():
        rows.append([
            house_num,
            house_info['sign'],
            ", ".join(house_info['planets']) if house_info['planets'] else "None"
        ])
    
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def print_transit_quality(transit_quality):
    """
    Print transit quality information
    
    Args:
        transit_quality (dict): Transit quality information
    """
    print(f"\n{'=' * 60}")
    print(f"Transit Quality")
    print(f"{'=' * 60}")
    print(f"Quality: {transit_quality['quality']}")
    print(f"Score: {transit_quality['score']}")
    
    print("\nFactors:")
    for factor in transit_quality['factors']:
        print(f"  - {factor}")

def print_gochara_effects(gochara_effects):
    """
    Print Gochara (transit) effects
    
    Args:
        gochara_effects (dict): Gochara effect information
    """
    print(f"\n{'=' * 60}")
    print(f"Gochara (Transit) Effects")
    print(f"{'=' * 60}")
    
    # Create a table
    headers = ["Planet", "House", "Moon House", "Effect", "Strength"]
    rows = []
    
    for planet_id, effect in gochara_effects.items():
        rows.append([
            planet_id,
            effect['house'],
            effect['moon_house'],
            effect['effect']['effect'],
            effect['strength']['strength']
        ])
    
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    
    # Print detailed effects
    print("\nDetailed Gochara Effects:")
    for planet_id, effect in gochara_effects.items():
        print(f"\n{planet_id}:")
        print(f"  House: {effect['house']}")
        print(f"  Moon House: {effect['moon_house']}")
        print(f"  Effect: {effect['effect']['effect']}")
        print(f"  Description: {effect['effect']['description']}")
        print(f"  Strength: {effect['strength']['strength']} (Score: {effect['strength']['score']:.2f})")
        
        # Print Vedha effects
        if effect['vedha_effects']:
            print("  Vedha (Obstruction) Effects:")
            for vedha in effect['vedha_effects']:
                print(f"    - {vedha['description']}")
        
        # Print Argala effects
        if effect['argala_effects']:
            print("  Argala (Intervention) Effects:")
            for argala in effect['argala_effects']:
                print(f"    - {argala['description']}")

def print_transit_ashtakavarga(transit_ashtakavarga):
    """
    Print transit Ashtakavarga information
    
    Args:
        transit_ashtakavarga (dict): Transit Ashtakavarga information
    """
    print(f"\n{'=' * 60}")
    print(f"Transit Ashtakavarga")
    print(f"{'=' * 60}")
    
    # Create a table
    headers = ["Planet", "Sign", "House", "Bindus", "Strength"]
    rows = []
    
    for planet_id, transit in transit_ashtakavarga.items():
        if planet_id != 'sarvashtakavarga':
            rows.append([
                planet_id,
                transit['sign'],
                transit['house'],
                transit['bindus'],
                transit['strength']['strength']
            ])
    
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    
    # Print Sarvashtakavarga
    print("\nSarvashtakavarga Transit:")
    for planet_id, transit in transit_ashtakavarga['sarvashtakavarga'].items():
        print(f"  {planet_id}: {transit['sign']} (House {transit['house']}) - {transit['bindus']} bindus, {transit['strength']['strength']}")

def print_transit_dasha_effects(transit_dasha_effects):
    """
    Print transit Dasha effects
    
    Args:
        transit_dasha_effects (dict): Transit Dasha effect information
    """
    print(f"\n{'=' * 60}")
    print(f"Transit Dasha Effects")
    print(f"{'=' * 60}")
    print(f"Current Dasha: {transit_dasha_effects['dasha_lord']} Maha Dasha")
    print(f"Current Antardasha: {transit_dasha_effects['antardasha_lord']} Antardasha")
    print(f"Current Pratyantardasha: {transit_dasha_effects['pratyantardasha_lord']} Pratyantardasha")
    
    # Print Dasha lord effects
    print(f"\nEffects on Dasha Lord ({transit_dasha_effects['dasha_lord']}):")
    for effect in transit_dasha_effects['dasha_effects']:
        if 'aspect' in effect:
            print(f"  - {effect['transit_planet']} {effect['aspect']} {transit_dasha_effects['dasha_lord']} (Orb: {effect['orb']:.2f}°, {'Applying' if effect['applying'] else 'Separating'})")
            print(f"    Effect: {effect['effect']['effect']} - {effect['effect']['description']}")
        elif 'house' in effect:
            print(f"  - {effect['transit_planet']} in house {effect['house']} of {transit_dasha_effects['dasha_lord']}")
            print(f"    Effect: {effect['effect']['effect']} - {effect['effect']['description']}")
    
    # Print Antardasha lord effects
    print(f"\nEffects on Antardasha Lord ({transit_dasha_effects['antardasha_lord']}):")
    for effect in transit_dasha_effects['antardasha_effects']:
        if 'aspect' in effect:
            print(f"  - {effect['transit_planet']} {effect['aspect']} {transit_dasha_effects['antardasha_lord']} (Orb: {effect['orb']:.2f}°, {'Applying' if effect['applying'] else 'Separating'})")
            print(f"    Effect: {effect['effect']['effect']} - {effect['effect']['description']}")
        elif 'house' in effect:
            print(f"  - {effect['transit_planet']} in house {effect['house']} of {transit_dasha_effects['antardasha_lord']}")
            print(f"    Effect: {effect['effect']['effect']} - {effect['effect']['description']}")

def print_transit_predictions(predictions):
    """
    Print transit predictions
    
    Args:
        predictions (dict): Transit prediction information
    """
    print(f"\n{'=' * 60}")
    print(f"Transit Predictions")
    print(f"{'=' * 60}")
    
    # Print general predictions
    print("General Predictions:")
    for prediction in predictions['general']:
        print(f"  - {prediction}")
    
    # Print planet-specific predictions
    print("\nPlanet Predictions:")
    for planet_id, prediction in predictions['planets'].items():
        print(f"\n{planet_id}:")
        for line in prediction['description']:
            print(f"  - {line}")
    
    # Print house-specific predictions
    print("\nHouse Predictions:")
    for house_num, prediction in predictions['houses'].items():
        print(f"\nHouse {house_num}:")
        for line in prediction['description']:
            print(f"  - {line}")
    
    # Print Dasha-related predictions
    print("\nDasha Predictions:")
    for prediction in predictions['dashas']:
        print(f"  - {prediction}")

def print_transit_timeline(timeline):
    """
    Print transit timeline
    
    Args:
        timeline (list): Transit timeline information
    """
    print(f"\n{'=' * 60}")
    print(f"Transit Timeline")
    print(f"{'=' * 60}")
    
    if not timeline:
        print("No significant transit events found in the specified period.")
        return
    
    # Create a table
    headers = ["Date", "Event Type", "Description"]
    rows = []
    
    for event in timeline:
        rows.append([
            event['date'],
            event['type'],
            event['description']
        ])
    
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def main():
    """Main function"""
    args = parse_args()
    
    # Create natal chart
    natal_chart = create_natal_chart(
        args.birth_date, args.birth_time, args.lat, args.lon, args.ayanamsa
    )
    
    # Create transit chart
    transit_chart, transit_date = create_transit_chart(
        args.date, args.time, args.lat, args.lon, args.ayanamsa
    )
    
    # Print chart information
    print_chart_info(natal_chart, "Natal", args.location, args.ayanamsa)
    print_chart_info(transit_chart, "Transit", args.location, args.ayanamsa)
    
    # Get transits
    transits = get_transits(natal_chart, transit_date)
    
    # Print transit planets
    print_transit_planets(transits['transit_planets'])
    
    # Print transit aspects
    print_transit_aspects(transits['transit_aspects'])
    
    # Print transit houses
    print_transit_houses(transits['transit_houses'])
    
    # Print transit quality
    print_transit_quality(transits['transit_quality'])
    
    # Print Gochara effects
    print_gochara_effects(transits['gochara_effects'])
    
    # Print Ashtakavarga analysis
    print_transit_ashtakavarga(transits['ashtakavarga_analysis']) # Use the correct key
    
    # Example: Analyze transit period (replace with desired start/end dates)
    #start_date = Datetime('2024/01/01', '00:00', '+00:00')
    
    # Print transit Dasha effects (Data not available in get_basic_transit_analysis)
    # print_transit_dasha_effects(transits['transit_dasha_effects'])

if __name__ == "__main__":
    main()
