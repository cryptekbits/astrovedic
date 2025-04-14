#!/usr/bin/env python3
"""
Muhurta Calculator Example

This script demonstrates how to use flatlib for Muhurta (electional astrology)
calculations in Vedic astrology. It includes:
- Calculating Panchanga (five limbs of the day)
- Finding auspicious times for various activities
- Analyzing the quality of a Muhurta
- Generating predictions based on Muhurta

Usage:
  python muhurta_calculator.py                   # Generate calculations for current time
  python muhurta_calculator.py YYYY/MM/DD HH:MM  # Generate calculations for specific date and time
  python muhurta_calculator.py -h, --help        # Show help message
"""

import sys
import argparse
from datetime import datetime, timedelta
from tabulate import tabulate

from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic import const
from astrovedic.vedic.muhurta import (
    get_panchanga, get_muhurta_quality, get_abhijit_muhurta,
    get_brahma_muhurta, get_rahu_kala, get_yama_ghantaka,
    get_gulika_kala, get_activity_score, get_best_time_for_activity,
    get_basic_muhurta_analysis
)

# Default location: Bangalore, India
DEFAULT_LAT = 12.9716
DEFAULT_LON = 77.5946
DEFAULT_LOCATION = "Bangalore, India"

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Calculate Muhurta (electional astrology)')
    parser.add_argument('date', nargs='?', help='Date in YYYY/MM/DD format')
    parser.add_argument('time', nargs='?', help='Time in HH:MM format')
    parser.add_argument('--lat', type=float, default=DEFAULT_LAT, help='Latitude')
    parser.add_argument('--lon', type=float, default=DEFAULT_LON, help='Longitude')
    parser.add_argument('--location', default=DEFAULT_LOCATION, help='Location name')
    parser.add_argument('--ayanamsa', default=const.AY_LAHIRI, help='Ayanamsa to use')
    parser.add_argument('--activity', help='Activity to find auspicious time for')
    parser.add_argument('--days', type=int, default=1, help='Number of days to search for auspicious times')
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

def print_panchanga(chart):
    """
    Print Panchanga information
    
    Args:
        chart (Chart): Astrovedic Chart object
    """
    # Get the Panchanga
    panchanga = get_panchanga(chart)
    
    print(f"\n{'=' * 60}")
    print(f"Panchanga (Five Limbs of the Day)")
    print(f"{'=' * 60}")
    
    # Print Tithi
    tithi = panchanga['tithi']
    print(f"Tithi: {tithi['name']} ({tithi['num']})")
    print(f"  Paksha: {tithi['paksha']}")
    print(f"  Type: {tithi['type']}")
    print(f"  Elapsed: {tithi['elapsed'] * 100:.2f}%")
    
    # Print Nakshatra
    nakshatra = panchanga['nakshatra']
    print(f"\nNakshatra: {nakshatra['name']} ({nakshatra['num']})")
    print(f"  Pada: {nakshatra['pada']}")
    print(f"  Lord: {nakshatra['lord']}")
    print(f"  Type: {nakshatra['type']}")

    # Print Yoga
    yoga = panchanga['yoga']
    print(f"\nYoga: {yoga['name']} ({yoga['num']})")
    print(f"  Type: {yoga['type']}")
    print(f"  Elapsed: {yoga['elapsed'] * 100:.2f}%")
    
    # Print Karana
    karana = panchanga['karana']
    print(f"\nKarana: {karana['name']} ({karana['num']})")
    print(f"  Type: {karana['type']}")
    print(f"  Elapsed: {karana['elapsed'] * 100:.2f}%")
    
    # Print Vara
    vara = panchanga['vara']
    print(f"\nVara: {vara['name']} ({vara['num']})")
    print(f"  Lord: {vara['lord']}")

def print_muhurta_quality(chart):
    """
    Print Muhurta quality information
    
    Args:
        chart (Chart): Astrovedic Chart object
    """
    # Get the Muhurta quality
    quality = get_muhurta_quality(chart)
    
    print(f"\n{'=' * 60}")
    print(f"Muhurta Quality")
    print(f"{'=' * 60}")
    print(f"Quality: {quality['quality']}")
    print(f"Score: {quality['score']}")

def print_special_muhurtas(date, location):
    """
    Print special Muhurtas for the day
    
    Args:
        date (Datetime): The date
        location (GeoPos): The geographical location
    """
    print(f"\n{'=' * 60}")
    print(f"Special Muhurtas")
    print(f"{'=' * 60}")
    
    # Get Abhijit Muhurta
    abhijit = get_abhijit_muhurta(date, location)
    print(f"Abhijit Muhurta (Most Auspicious Time):")
    print(f"  Start: {abhijit['start']}")
    print(f"  End: {abhijit['end']}")
    print(f"  Duration: {abhijit['duration']:.0f} minutes")
    print(f"  Description: {abhijit['description']}")
    
    # Get Brahma Muhurta
    brahma = get_brahma_muhurta(date, location)
    print(f"\nBrahma Muhurta (Auspicious Time Before Sunrise):")
    print(f"  Start: {brahma['start']}")
    print(f"  End: {brahma['end']}")
    print(f"  Duration: {brahma['duration']:.0f} minutes")
    print(f"  Description: {brahma['description']}")

def print_inauspicious_periods(date, location):
    """
    Print inauspicious periods for the day
    
    Args:
        date (Datetime): The date
        location (GeoPos): The geographical location
    """
    print(f"\n{'=' * 60}")
    print(f"Inauspicious Periods")
    print(f"{'=' * 60}")
    
    # Get Rahu Kala
    rahu_kala = get_rahu_kala(date, location)
    print(f"Rahu Kala:")
    print(f"  Start: {rahu_kala['start']}")
    print(f"  End: {rahu_kala['end']}")
    print(f"  Duration: {rahu_kala['duration']:.0f} minutes")
    print(f"  Description: {rahu_kala['description']}")
    
    # Get Yama Ghantaka
    yama_ghantaka = get_yama_ghantaka(date, location)
    print(f"\nYama Ghantaka:")
    print(f"  Start: {yama_ghantaka['start']}")
    print(f"  End: {yama_ghantaka['end']}")
    print(f"  Duration: {yama_ghantaka['duration']:.0f} minutes")
    print(f"  Description: {yama_ghantaka['description']}")
    
    # Get Gulika Kala
    gulika_kala = get_gulika_kala(date, location)
    print(f"\nGulika Kala:")
    print(f"  Start: {gulika_kala['start']}")
    print(f"  End: {gulika_kala['end']}")
    print(f"  Duration: {gulika_kala['duration']:.0f} minutes")
    print(f"  Description: {gulika_kala['description']}")

def print_activity_scores(date, location):
    """
    Print activity scores for the current time
    
    Args:
        date (Datetime): The date and time
        location (GeoPos): The geographical location
    """
    print(f"\n{'=' * 60}")
    print(f"Activity Scores")
    print(f"{'=' * 60}")
    
    # List of activities
    activities = ['general', 'marriage', 'travel', 'business', 'education', 'medical', 'house_construction']
    
    # Calculate scores for each activity
    headers = ["Activity", "Quality", "Score", "Top Factors"]
    rows = []
    
    for activity in activities:
        score = get_activity_score(date, location, activity)
        
        rows.append([
            activity.capitalize(),
            score['quality'],
            f"{score['percentage']:.2f}%",
            ", ".join(score['factors'][:2])
        ])
    
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def find_auspicious_times(start_date, end_date, location, activity):
    """
    Find auspicious times for a specific activity
    
    Args:
        start_date (Datetime): The start date and time
        end_date (Datetime): The end date and time
        location (GeoPos): The geographical location
        activity (str): The type of activity
    """
    print(f"\n{'=' * 60}")
    print(f"Auspicious Times for {activity.capitalize()}")
    print(f"{'=' * 60}")
    print(f"Searching from {start_date} to {end_date}...")
    
    # Get the best time for the activity
    best_time = get_best_time_for_activity(start_date, end_date, location, activity)
    
    if best_time:
        print(f"\nBest Time Found:")
        print(f"  Start: {best_time['start']}")
        print(f"  End: {best_time['end']}")
        print(f"  Duration: {best_time['duration']:.0f} minutes")
        print(f"  Quality: {best_time['score']['quality']}")
        print(f"  Score: {best_time['score']['percentage']:.2f}%")
        print(f"\nFactors:")
        for factor in best_time['score']['factors']:
            print(f"  - {factor}")
    else:
        print(f"\nNo auspicious times found for {activity} in the specified date range.")

def print_muhurta_predictions(date, location):
    """
    Print predictions based on Muhurta
    
    Args:
        date (Datetime): The date and time
        location (GeoPos): The geographical location
    """
    # Get the basic analysis
    analysis_result = get_basic_muhurta_analysis(date, location)

    print(f"\n{'=' * 60}")
    print(f"Muhurta Analysis (Basic)")
    print(f"{'=' * 60}")

    # Create a copy to modify for printing
    analysis_print = analysis_result.copy()
    # Convert the Datetime object to its string representation
    if 'date' in analysis_print and isinstance(analysis_print['date'], Datetime):
        analysis_print['date'] = str(analysis_print['date'])

    # Print the modified analysis result with a formatted date
    # Use pprint for better readability of the dictionary
    import pprint
    pprint.pprint(analysis_print)

    # Commented out original prediction processing due to unknown structure
    # # Print general predictions
    # print("General Predictions:")
    # for prediction in predictions['general']:
    #     print(f"  - {prediction}")
    #
    # # Print activity-specific predictions
    # print("\nActivity Predictions:")
    # for activity, prediction in predictions['activities'].items():
    #     print(f"  - {activity.capitalize()}: {prediction}")
    #
    # # Print timing predictions
    # print("\nTiming Predictions:")
    # for prediction in predictions['timing']:
    #     print(f"  - {prediction}")

def main():
    """Main function"""
    args = parse_args()
    
    # Create chart
    chart, date = create_chart(
        args.date, args.time, args.lat, args.lon, args.ayanamsa
    )
    
    # Create location object
    location = GeoPos(args.lat, args.lon)
    
    # Print chart information
    print_chart_info(chart, args.location, args.ayanamsa)
    
    # Print Panchanga
    print_panchanga(chart)
    
    # Print Muhurta quality
    print_muhurta_quality(chart)
    
    # Print special Muhurtas
    print_special_muhurtas(date, location)
    
    # Print inauspicious periods
    print_inauspicious_periods(date, location)
    
    # Print activity scores
    print_activity_scores(date, location)
    
    # Print Muhurta predictions
    print_muhurta_predictions(date, location)
    
    # Find auspicious times for a specific activity if requested
    if args.activity:
        # Calculate the end date
        end_dt = date.datetime() + timedelta(days=args.days)
        end_date = Datetime.fromDatetime(end_dt)
        
        # Find auspicious times
        find_auspicious_times(date, end_date, location, args.activity)

if __name__ == "__main__":
    main()
