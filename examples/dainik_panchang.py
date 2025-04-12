#!/usr/bin/env python3
"""
Dainik Panchang Example

This script generates a daily Panchang (Vedic almanac) for a given date and location.
It includes tithi, nakshatra, yoga, karana, and various auspicious and inauspicious periods.

Usage:
  python dainik_panchang.py                   # Generate panchang for current date in Bangalore
  python dainik_panchang.py YYYY/MM/DD        # Generate panchang for specific date in Bangalore
  python dainik_panchang.py -h, --help        # Show help message
"""

import sys
import datetime
from tabulate import tabulate

from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib.vedic.panchang import get_panchang
from flatlib.vedic.nakshatras import get_nakshatra
from flatlib.vedic.upagrah import get_upagrah
from flatlib.vedic.kp import get_kp_lords

# Default location: Bangalore, India
DEFAULT_LAT = 12.9716
DEFAULT_LON = 77.5946
DEFAULT_LOCATION = "Bangalore, India"

def get_chart(date_str=None, time_str="00:00", lat=DEFAULT_LAT, lon=DEFAULT_LON):
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
    
    # Create date and location objects
    date = Datetime(date_str, time_str, '+05:30')  # Indian Standard Time
    pos = GeoPos(lat, lon)
    
    # Create chart with Lahiri ayanamsa and Whole Sign houses
    chart = Chart(date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
    
    return chart

def format_time(dt):
    """Format datetime object as HH:MM"""
    return dt.time

def print_panchang(chart):
    """
    Print the panchang for the given chart
    
    Args:
        chart (Chart): Flatlib Chart object
    """
    # Get date and location
    date = chart.date
    pos = chart.pos
    
    # Get panchang information
    panchang = get_panchang(date.jd, pos.lat, pos.lon, date.utcoffset, chart.mode)
    
    # Print header
    print(f"\n{'=' * 60}")
    print(f"DAINIK PANCHANG FOR {date.date} ({DEFAULT_LOCATION})")
    print(f"{'=' * 60}\n")
    
    # Print basic panchang elements
    basic_data = [
        ["Date", date.date],
        ["Day", panchang['vara']['name']],
        ["Tithi", f"{panchang['tithi']['name']} ({panchang['tithi']['paksha']})"],
        ["Nakshatra", f"{panchang['nakshatra']['name']} (Pada {panchang['nakshatra']['pada']})"],
        ["Yoga", panchang['yoga']['name']],
        ["Karana", panchang['karana']['name']]
    ]
    
    print(tabulate(basic_data, tablefmt="grid"))
    print()
    
    # Print auspicious and inauspicious periods
    periods_data = [
        ["Rahukala", f"{format_time(panchang['rahukala']['start'])} - {format_time(panchang['rahukala']['end'])}"],
        ["Yamaganda", f"{format_time(panchang['yamaganda']['start'])} - {format_time(panchang['yamaganda']['end'])}"],
        ["Gulika Kala", f"{format_time(panchang['gulika_kala']['start'])} - {format_time(panchang['gulika_kala']['end'])}"],
        ["Abhijit Muhurta", f"{format_time(panchang['abhijit_muhurta']['start'])} - {format_time(panchang['abhijit_muhurta']['end'])}"]
    ]
    
    print("AUSPICIOUS AND INAUSPICIOUS PERIODS:")
    print(tabulate(periods_data, tablefmt="grid"))
    print()
    
    # Print planetary positions
    planets = [
        const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS,
        const.JUPITER, const.SATURN, const.RAHU, const.KETU
    ]
    
    planet_data = []
    for planet_id in planets:
        planet = chart.getObject(planet_id)
        nakshatra_info = get_nakshatra(planet.lon)
        
        # Format position
        position = f"{planet.sign} {planet.signlon:.2f}°"
        
        # Format nakshatra
        nakshatra = f"{nakshatra_info['name']} (Pada {nakshatra_info['pada']})"
        
        # Get KP information
        kp_info = get_kp_lords(planet.lon)
        
        planet_data.append([
            planet.id,
            position,
            nakshatra,
            kp_info['kp_pointer']
        ])
    
    print("PLANETARY POSITIONS:")
    print(tabulate(planet_data, headers=["Planet", "Position", "Nakshatra", "KP Pointer"], tablefmt="grid"))
    print()
    
    # Print shadow planets (upagrah)
    shadow_planets = [
        const.GULIKA, const.MANDI, const.DHUMA, const.VYATIPATA,
        const.PARIVESHA, const.INDRACHAPA, const.UPAKETU
    ]
    
    shadow_data = []
    for upagrah_id in shadow_planets:
        try:
            if upagrah_id in [const.GULIKA, const.MANDI]:
                upagrah = get_upagrah(upagrah_id, date.jd, pos.lat, pos.lon)
            else:
                upagrah = get_upagrah(upagrah_id, date.jd)
                
            position = f"{upagrah['sign']} {upagrah['signlon']:.2f}°"
            nakshatra_info = get_nakshatra(upagrah['lon'])
            nakshatra = f"{nakshatra_info['name']} (Pada {nakshatra_info['pada']})"
            
            shadow_data.append([
                upagrah_id,
                position,
                nakshatra
            ])
        except Exception as e:
            shadow_data.append([
                upagrah_id,
                f"Error: {e}",
                ""
            ])
    
    print("SHADOW PLANETS (UPAGRAH):")
    print(tabulate(shadow_data, headers=["Upagrah", "Position", "Nakshatra"], tablefmt="grid"))
    print()

def main():
    """Main function"""
    # Check if date is provided as command line argument
    if len(sys.argv) == 2:
        if sys.argv[1] in ['-h', '--help']:
            print(__doc__)
            return
        
        date_str = sys.argv[1]
        try:
            chart = get_chart(date_str)
            print(f"Generating Panchang for {date_str} in {DEFAULT_LOCATION}")
        except Exception as e:
            print(f"Error: {e}")
            print("Please use the format: YYYY/MM/DD (e.g., 2025/04/09)")
            return
    else:
        # Use current date
        chart = get_chart()
        print(f"Generating Panchang for today in {DEFAULT_LOCATION}")
    
    # Print panchang
    print_panchang(chart)

if __name__ == "__main__":
    main()
