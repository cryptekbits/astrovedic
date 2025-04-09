#!/usr/bin/env python3
"""
Vimshottari Dasha Example

This script demonstrates how to use flatlib for Vimshottari Dasha calculations.
It includes:
- Calculation of Mahadashas (main periods)
- Calculation of Antardashas (sub-periods)
- Calculation of Pratyantardashas (sub-sub-periods)
- Finding the current operating Dasha period
- Analysis of Dasha lord strengths

Usage:
  python vimshottari_dasha.py                   # Generate dashas for current time
  python vimshottari_dasha.py YYYY/MM/DD HH:MM  # Generate dashas for specific date and time
  python vimshottari_dasha.py -h, --help        # Show help message
"""

import sys
import datetime
from tabulate import tabulate

from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib.vedic.nakshatras import get_nakshatra
from flatlib.vedic.dashas import (
    calculate_dasha_balance, calculate_dasha_periods,
    get_current_dasha, format_dasha_period, analyze_dasha_strength,
    is_dasha_sandhi
)

# Default location: Bangalore, India
DEFAULT_LAT = 12.9716
DEFAULT_LON = 77.5946
DEFAULT_LOCATION = "Bangalore, India"

def get_chart(date_str=None, time_str=None, lat=DEFAULT_LAT, lon=DEFAULT_LON):
    """
    Create a chart for the given date, time, and location
    
    Args:
        date_str (str, optional): Date in format YYYY/MM/DD
        time_str (str, optional): Time in format HH:MM
        lat (float, optional): Latitude in degrees
        lon (float, optional): Longitude in degrees
    
    Returns:
        Chart: Flatlib Chart object
    """
    # If no date is provided, use current date
    if not date_str:
        now = datetime.datetime.now()
        date_str = now.strftime("%Y/%m/%d")
        time_str = now.strftime("%H:%M")
    elif not time_str:
        time_str = "12:00"
    
    # Create date and location objects
    date = Datetime(date_str, time_str, '+05:30')  # Indian Standard Time
    pos = GeoPos(lat, lon)
    
    # Create chart with Lahiri ayanamsa and Whole Sign houses
    chart = Chart(date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
    
    return chart, date

def format_date(dt):
    """Format datetime object as YYYY-MM-DD"""
    if isinstance(dt, datetime.datetime):
        return dt.strftime("%Y-%m-%d")
    return str(dt)

def print_dasha_periods(chart, date):
    """
    Print the Vimshottari Dasha periods for the given chart
    
    Args:
        chart (Chart): Flatlib Chart object
        date (Datetime): Birth date
    """
    # Get the Moon's longitude
    moon = chart.getObject(const.MOON)
    moon_longitude = moon.lon
    
    # Get nakshatra information
    nakshatra_info = get_nakshatra(moon_longitude)
    
    # Calculate dasha balance
    dasha_balance = calculate_dasha_balance(moon_longitude)
    
    # Calculate all dasha periods
    dasha_periods = calculate_dasha_periods(date, moon_longitude)
    
    # Get current dasha
    current_dasha = get_current_dasha(dasha_periods)
    
    # Check if in dasha sandhi
    in_sandhi = is_dasha_sandhi(dasha_periods)
    
    # Analyze dasha strength
    dasha_strength = analyze_dasha_strength(chart, current_dasha)
    
    # Print header
    print(f"\n{'=' * 60}")
    print(f"VIMSHOTTARI DASHA CALCULATIONS FOR {date.date} {date.time} ({DEFAULT_LOCATION})")
    print(f"{'=' * 60}\n")
    
    # Print Moon and nakshatra information
    print(f"Moon Position: {moon.sign} {moon.signlon:.2f}° (Total: {moon_longitude:.2f}°)")
    print(f"Moon Nakshatra: {nakshatra_info['name']} (Pada {nakshatra_info['pada']})")
    print(f"Nakshatra Lord: {nakshatra_info['lord']}")
    print(f"Dasha Balance at Birth: {dasha_balance:.2f} years\n")
    
    # Print current dasha
    print(f"CURRENT DASHA PERIOD: {format_dasha_period(current_dasha)}")
    if in_sandhi:
        print("NOTE: Currently in Dasha Sandhi (junction period)")
    print()
    
    # Print dasha lord analysis
    if dasha_strength:
        print("DASHA LORD ANALYSIS:")
        for level, info in dasha_strength.items():
            print(f"  {level.capitalize()}: {info['planet']} in {info['sign']} (House {info['house']})")
            if info.get('retrograde'):
                print(f"    Retrograde: Yes")
        print()
    
    # Print Mahadasha sequence
    print("MAHADASHA SEQUENCE:")
    mahadasha_data = []
    
    for mahadasha in dasha_periods['mahadashas']:
        # Highlight current mahadasha
        is_current = (current_dasha and mahadasha['planet'] == current_dasha['mahadasha'] and
                     mahadasha['start_date'] <= datetime.datetime.now() < mahadasha['end_date'])
        
        planet = f"* {mahadasha['planet']} *" if is_current else mahadasha['planet']
        
        mahadasha_data.append([
            planet,
            format_date(mahadasha['start_date']),
            format_date(mahadasha['end_date']),
            f"{mahadasha['years']:.2f} years"
        ])
    
    print(tabulate(mahadasha_data, headers=["Planet", "Start Date", "End Date", "Duration"], tablefmt="grid"))
    print()
    
    # Print Antardasha sequence for current Mahadasha
    if current_dasha:
        current_mahadasha = None
        for mahadasha in dasha_periods['mahadashas']:
            if mahadasha['planet'] == current_dasha['mahadasha']:
                current_mahadasha = mahadasha
                break
        
        if current_mahadasha:
            print(f"ANTARDASHAS FOR CURRENT {current_mahadasha['planet']} MAHADASHA:")
            antardasha_data = []
            
            for antardasha in current_mahadasha['antardashas']:
                # Highlight current antardasha
                is_current = (current_dasha.get('antardasha') == antardasha['planet'] and
                             antardasha['start_date'] <= datetime.datetime.now() < antardasha['end_date'])
                
                planet = f"* {antardasha['planet']} *" if is_current else antardasha['planet']
                
                antardasha_data.append([
                    planet,
                    format_date(antardasha['start_date']),
                    format_date(antardasha['end_date']),
                    f"{antardasha['years']:.2f} years"
                ])
            
            print(tabulate(antardasha_data, headers=["Planet", "Start Date", "End Date", "Duration"], tablefmt="grid"))
            print()
            
            # Print Pratyantardasha sequence for current Antardasha
            if current_dasha.get('antardasha'):
                current_antardasha = None
                for antardasha in current_mahadasha['antardashas']:
                    if antardasha['planet'] == current_dasha['antardasha']:
                        current_antardasha = antardasha
                        break
                
                if current_antardasha:
                    print(f"PRATYANTARDASHAS FOR CURRENT {current_antardasha['planet']} ANTARDASHA:")
                    pratyantardasha_data = []
                    
                    for pratyantardasha in current_antardasha['pratyantardashas']:
                        # Highlight current pratyantardasha
                        is_current = (current_dasha.get('pratyantardasha') == pratyantardasha['planet'] and
                                     pratyantardasha['start_date'] <= datetime.datetime.now() < pratyantardasha['end_date'])
                        
                        planet = f"* {pratyantardasha['planet']} *" if is_current else pratyantardasha['planet']
                        
                        pratyantardasha_data.append([
                            planet,
                            format_date(pratyantardasha['start_date']),
                            format_date(pratyantardasha['end_date']),
                            f"{pratyantardasha['years']:.2f} years"
                        ])
                    
                    print(tabulate(pratyantardasha_data, headers=["Planet", "Start Date", "End Date", "Duration"], tablefmt="grid"))
                    print()

def main():
    """Main function"""
    # Check if date is provided as command line argument
    if len(sys.argv) >= 2:
        if sys.argv[1] in ['-h', '--help']:
            print(__doc__)
            return
        
        date_str = sys.argv[1]
        time_str = sys.argv[2] if len(sys.argv) >= 3 else None
        
        try:
            chart, date = get_chart(date_str, time_str)
            print(f"Generating Vimshottari Dasha calculations for {date_str} {time_str or '12:00'} in {DEFAULT_LOCATION}")
        except Exception as e:
            print(f"Error: {e}")
            print("Please use the format: YYYY/MM/DD HH:MM (e.g., 2025/04/09 20:51)")
            return
    else:
        # Use current date
        chart, date = get_chart()
        print(f"Generating Vimshottari Dasha calculations for current time in {DEFAULT_LOCATION}")
    
    # Print Vimshottari Dasha periods
    print_dasha_periods(chart, date)

if __name__ == "__main__":
    main()
