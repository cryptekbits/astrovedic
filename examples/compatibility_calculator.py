#!/usr/bin/env python3
"""
Compatibility Calculator Example

This script demonstrates how to use flatlib for compatibility analysis
in Vedic astrology. It includes:
- Calculating Kuta (compatibility) factors
- Analyzing Dosha (affliction)
- Generating compatibility reports
- Creating compatibility timelines

Usage:
  python compatibility_calculator.py                                   # Use default birth data
  python compatibility_calculator.py YYYY/MM/DD HH:MM YYYY/MM/DD HH:MM # Use custom birth data
  python compatibility_calculator.py -h, --help                        # Show help message
"""

import sys
import argparse
from datetime import datetime, timedelta
from tabulate import tabulate

from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic import const
from astrovedic.vedic.compatibility import (
    get_compatibility, get_detailed_compatibility_report,
    get_compatibility_timeline, analyze_charts_compatibility
)
from astrovedic.vedic.compatibility.kuta import (
    get_varna_kuta, get_vashya_kuta, get_tara_kuta,
    get_yoni_kuta, get_graha_maitri_kuta, get_gana_kuta,
    get_bhakoot_kuta, get_nadi_kuta, get_total_kuta_score
)
from astrovedic.vedic.compatibility.dosha import (
    get_mangal_dosha, get_kuja_dosha, get_shani_dosha,
    get_grahan_dosha, get_dosha_cancellation, get_dosha_remedies
)
from astrovedic.vedic.compatibility.dasha import (
    get_dasha_compatibility, get_antardasha_compatibility,
    get_dasha_periods_compatibility, get_dasha_predictions
)
from astrovedic.vedic.compatibility.navamsa import (
    get_navamsa_compatibility, get_navamsa_positions,
    get_navamsa_aspects, get_navamsa_strength
)

# Default location: Bangalore, India
DEFAULT_LAT = 12.9716
DEFAULT_LON = 77.5946
DEFAULT_LOCATION = "Bangalore, India"

# Default birth data
DEFAULT_BIRTH_DATE1 = "1990/01/01"
DEFAULT_BIRTH_TIME1 = "12:00"
DEFAULT_BIRTH_DATE2 = "1995/01/01"
DEFAULT_BIRTH_TIME2 = "12:00"


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Calculate compatibility in Vedic astrology')
    parser.add_argument('birth_date1', nargs='?', default=DEFAULT_BIRTH_DATE1, help='Birth date 1 in YYYY/MM/DD format')
    parser.add_argument('birth_time1', nargs='?', default=DEFAULT_BIRTH_TIME1, help='Birth time 1 in HH:MM format')
    parser.add_argument('birth_date2', nargs='?', default=DEFAULT_BIRTH_DATE2, help='Birth date 2 in YYYY/MM/DD format')
    parser.add_argument('birth_time2', nargs='?', default=DEFAULT_BIRTH_TIME2, help='Birth time 2 in HH:MM format')
    parser.add_argument('--lat1', type=float, default=DEFAULT_LAT, help='Latitude for birth 1')
    parser.add_argument('--lon1', type=float, default=DEFAULT_LON, help='Longitude for birth 1')
    parser.add_argument('--lat2', type=float, default=DEFAULT_LAT, help='Latitude for birth 2')
    parser.add_argument('--lon2', type=float, default=DEFAULT_LON, help='Longitude for birth 2')
    parser.add_argument('--location1', default=DEFAULT_LOCATION, help='Location name for birth 1')
    parser.add_argument('--location2', default=DEFAULT_LOCATION, help='Location name for birth 2')
    parser.add_argument('--ayanamsa', default=const.AY_LAHIRI, help='Ayanamsa to use')
    parser.add_argument('--timeline-days', type=int, default=365, help='Number of days for timeline')
    return parser.parse_args()


def create_chart(birth_date, birth_time, lat, lon, ayanamsa):
    """
    Create a chart
    
    Args:
        birth_date (str): Birth date in YYYY/MM/DD format
        birth_time (str): Birth time in HH:MM format
        lat (float): Latitude
        lon (float): Longitude
        ayanamsa (str): Ayanamsa to use
    
    Returns:
        Chart: The chart
    """
    # Create date and location objects
    date = Datetime(birth_date, birth_time, '+05:30')  # Indian Standard Time
    pos = GeoPos(lat, lon)
    
    # Create chart with specified ayanamsa and Whole Sign houses
    chart = Chart(date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=ayanamsa)
    
    return chart


def print_chart_info(chart, chart_type, location, ayanamsa):
    """
    Print basic chart information
    
    Args:
        chart (Chart): Astrovedic Chart object
        chart_type (str): Type of chart ('Person 1' or 'Person 2')
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
        retrograde_str = ''
        if hasattr(planet, 'isRetrograde') and planet.isRetrograde():
            retrograde_str = ' (R)'
        print(f"  {planet_id}: {planet.sign} {planet.signlon:.2f}°{retrograde_str}")


def print_kuta_scores(kuta_scores):
    """
    Print Kuta scores
    
    Args:
        kuta_scores (dict): Dictionary with Kuta scores
    """
    print(f"\n{'=' * 60}")
    print(f"Kuta (Compatibility) Scores")
    print(f"{'=' * 60}")
    
    # Create a table
    headers = ["Kuta Factor", "Score", "Max Score", "Description"]
    rows = []
    
    for kuta_name, kuta_info in kuta_scores.items():
        rows.append([
            kuta_name,
            kuta_info['score'],
            kuta_info['max_score'],
            kuta_info['description']
        ])
    
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    
    # Print the total score
    total_kuta_score = get_total_kuta_score(kuta_scores)
    print(f"\nTotal Kuta Score: {total_kuta_score['total_score']}/{total_kuta_score['max_total_score']} ({total_kuta_score['percentage']:.1f}%)")
    print(f"Compatibility Level: {total_kuta_score['level']}")
    print(f"Description: {total_kuta_score['description']}")


def print_dosha_analysis(dosha_analysis, dosha_cancellation):
    """
    Print Dosha analysis
    
    Args:
        dosha_analysis (dict): Dictionary with Dosha analysis
        dosha_cancellation (dict): Dictionary with Dosha cancellation information
    """
    print(f"\n{'=' * 60}")
    print(f"Dosha (Affliction) Analysis")
    print(f"{'=' * 60}")
    
    # Print Mangal Dosha
    print("\nMangal Dosha:")
    print(f"  Person 1: {'Yes' if dosha_analysis['Mangal Dosha']['chart1']['has_dosha'] else 'No'}")
    print(f"  Description: {dosha_analysis['Mangal Dosha']['chart1']['description']}")
    print(f"  Person 2: {'Yes' if dosha_analysis['Mangal Dosha']['chart2']['has_dosha'] else 'No'}")
    print(f"  Description: {dosha_analysis['Mangal Dosha']['chart2']['description']}")
    
    # Print Kuja Dosha
    print("\nKuja Dosha:")
    print(f"  Person 1: {'Yes' if dosha_analysis['Kuja Dosha']['chart1']['has_dosha'] else 'No'}")
    print(f"  Description: {dosha_analysis['Kuja Dosha']['chart1']['description']}")
    print(f"  Person 2: {'Yes' if dosha_analysis['Kuja Dosha']['chart2']['has_dosha'] else 'No'}")
    print(f"  Description: {dosha_analysis['Kuja Dosha']['chart2']['description']}")
    
    # Print Shani Dosha
    print("\nShani Dosha:")
    print(f"  Person 1: {'Yes' if dosha_analysis['Shani Dosha']['chart1']['has_dosha'] else 'No'}")
    print(f"  Description: {dosha_analysis['Shani Dosha']['chart1']['description']}")
    print(f"  Person 2: {'Yes' if dosha_analysis['Shani Dosha']['chart2']['has_dosha'] else 'No'}")
    print(f"  Description: {dosha_analysis['Shani Dosha']['chart2']['description']}")
    
    # Print Grahan Dosha
    print("\nGrahan Dosha:")
    print(f"  Person 1: {'Yes' if dosha_analysis['Grahan Dosha']['chart1']['has_dosha'] else 'No'}")
    print(f"  Description: {dosha_analysis['Grahan Dosha']['chart1']['description']}")
    print(f"  Person 2: {'Yes' if dosha_analysis['Grahan Dosha']['chart2']['has_dosha'] else 'No'}")
    print(f"  Description: {dosha_analysis['Grahan Dosha']['chart2']['description']}")
    
    # Print Dosha cancellation
    print("\nDosha Cancellation:")
    print(f"  Is Cancelled: {'Yes' if dosha_cancellation['is_cancelled'] else 'No'}")
    print(f"  Description: {dosha_cancellation['description']}")


def print_dosha_remedies(dosha_remedies):
    """
    Print Dosha remedies
    
    Args:
        dosha_remedies (dict): Dictionary with Dosha remedies
    """
    print(f"\n{'=' * 60}")
    print(f"Dosha Remedies")
    print(f"{'=' * 60}")
    
    if not dosha_remedies:
        print("No remedies are needed as no significant Doshas are present.")
        return
    
    for dosha_name, remedies in dosha_remedies.items():
        print(f"\n{dosha_name}:")
        for i, remedy in enumerate(remedies, 1):
            print(f"  {i}. {remedy}")


def print_dasha_compatibility(dasha_compatibility):
    """
    Print Dasha compatibility
    
    Args:
        dasha_compatibility (dict): Dictionary with Dasha compatibility information
    """
    print(f"\n{'=' * 60}")
    print(f"Dasha Compatibility")
    print(f"{'=' * 60}")
    
    print(f"Person 1 Dasha: {dasha_compatibility['dasha_lord1']}")
    print(f"Person 2 Dasha: {dasha_compatibility['dasha_lord2']}")
    print(f"Compatibility: {dasha_compatibility['compatibility']['friendship']}")
    print(f"Score: {dasha_compatibility['score']}/10")
    print(f"Description: {dasha_compatibility['description']}")


def print_dasha_predictions(dasha_predictions):
    """
    Print Dasha predictions
    
    Args:
        dasha_predictions (dict): Dictionary with Dasha predictions
    """
    print(f"\n{'=' * 60}")
    print(f"Dasha Predictions")
    print(f"{'=' * 60}")
    
    print("\nCurrent Period Prediction:")
    print(dasha_predictions['current_period_prediction'])
    
    print("\nUpcoming Periods Prediction:")
    print(dasha_predictions['upcoming_periods_prediction'])
    
    print("\nFavorable Periods Prediction:")
    print(dasha_predictions['favorable_periods_prediction'])
    
    print("\nChallenging Periods Prediction:")
    print(dasha_predictions['challenging_periods_prediction'])


def print_navamsa_compatibility(navamsa_compatibility):
    """
    Print Navamsa compatibility
    
    Args:
        navamsa_compatibility (dict): Dictionary with Navamsa compatibility information
    """
    print(f"\n{'=' * 60}")
    print(f"Navamsa Compatibility")
    print(f"{'=' * 60}")
    
    print(f"Score: {navamsa_compatibility['score']:.1f}/10")
    print(f"Description: {navamsa_compatibility['description']}")
    
    # Print aspects
    print("\nKey Aspects:")
    for aspect in navamsa_compatibility['aspects'][:5]:  # Show top 5 aspects
        print(f"  {aspect['planet1']} {aspect['aspect']} {aspect['planet2']} (Orb: {aspect['orb']:.1f}°)")


def print_compatibility_timeline(timeline):
    """
    Print compatibility timeline
    
    Args:
        timeline (list): List of compatibility events
    """
    print(f"\n{'=' * 60}")
    print(f"Compatibility Timeline")
    print(f"{'=' * 60}")
    
    # Create a table
    headers = ["Date", "Person 1", "Person 2", "Score", "Level"]
    rows = []
    
    # Check if 'events' key exists and is a list before iterating
    if 'events' in timeline and isinstance(timeline['events'], list):
        for event in timeline['events']:
            # Format the date
            # Assuming event['date'] is a flatlib Datetime object
            # We need a way to format it. Let's use its __str__ representation for now.
            # date_str = event['date'].strftime("%B %Y") # Original line causes error if event['date'] is not datetime
            date_str = str(event.get('date', 'N/A')) # Use get for safety and convert to string
            
            # Format the Dasha information
            person1 = f"{event.get('dasha_lord1', 'N/A')} / {event.get('antardasha_lord1', 'N/A')}"
            person2 = f"{event.get('dasha_lord2', 'N/A')} / {event.get('antardasha_lord2', 'N/A')}"
            
            # Get the compatibility level
            score = event.get('score', 0) # Default to 0 if score is missing
            level = get_compatibility_level(score * 10)
            
            rows.append([
                date_str,
                person1,
                person2,
                f"{score:.1f}/10",
                level
            ])
    else:
        print("  No timeline events found or timeline format is incorrect.")

    if rows:
        print(tabulate(rows, headers=headers, tablefmt="grid"))


def get_compatibility_level(score):
    """
    Get the compatibility level based on the score
    
    Args:
        score (float): The compatibility score (0-100)
    
    Returns:
        str: The compatibility level
    """
    if score >= 80:
        return 'Excellent'
    elif score >= 60:
        return 'Good'
    elif score >= 40:
        return 'Average'
    elif score >= 20:
        return 'Challenging'
    else:
        return 'Difficult'


def print_overall_compatibility(compatibility):
    """
    Print overall compatibility summary
    
    Args:
        compatibility (dict): Dictionary with overall compatibility information
    """
    print(f"\n{'=' * 60}")
    print(f"Overall Compatibility")
    print(f"{'=' * 60}")
    
    # Check if 'overall_score' key exists
    if 'overall_score' in compatibility:
        score = compatibility['overall_score']
        level = get_compatibility_level(score)
        print(f"Score: {score:.1f}/100")
        print(f"Level: {level}")
    else:
        print("  Overall score not found.")
    
    # You might want to print other details from the compatibility dict here
    # e.g., factors, moon_compatibility, etc.


def main():
    """Main function"""
    args = parse_args()
    
    # Create charts
    chart1 = create_chart(
        args.birth_date1, args.birth_time1, args.lat1, args.lon1, args.ayanamsa
    )
    
    chart2 = create_chart(
        args.birth_date2, args.birth_time2, args.lat2, args.lon2, args.ayanamsa
    )
    
    # Print chart information
    print_chart_info(chart1, "Person 1", args.location1, args.ayanamsa)
    print_chart_info(chart2, "Person 2", args.location2, args.ayanamsa)
    
    # Get Kuta scores
    kuta_scores = {}
    kuta_scores['Varna Kuta'] = get_varna_kuta(chart1, chart2)
    kuta_scores['Vashya Kuta'] = get_vashya_kuta(chart1, chart2)
    kuta_scores['Tara Kuta'] = get_tara_kuta(chart1, chart2)
    kuta_scores['Yoni Kuta'] = get_yoni_kuta(chart1, chart2)
    kuta_scores['Graha Maitri Kuta'] = get_graha_maitri_kuta(chart1, chart2)
    kuta_scores['Gana Kuta'] = get_gana_kuta(chart1, chart2)
    kuta_scores['Bhakoot Kuta'] = get_bhakoot_kuta(chart1, chart2)
    kuta_scores['Nadi Kuta'] = get_nadi_kuta(chart1, chart2)
    
    # Print Kuta scores
    print_kuta_scores(kuta_scores)
    
    # Get Dosha analysis
    dosha_analysis = {}
    dosha_analysis['Mangal Dosha'] = {
        'chart1': get_mangal_dosha(chart1),
        'chart2': get_mangal_dosha(chart2)
    }
    dosha_analysis['Kuja Dosha'] = {
        'chart1': get_kuja_dosha(chart1),
        'chart2': get_kuja_dosha(chart2)
    }
    dosha_analysis['Shani Dosha'] = {
        'chart1': get_shani_dosha(chart1),
        'chart2': get_shani_dosha(chart2)
    }
    dosha_analysis['Grahan Dosha'] = {
        'chart1': get_grahan_dosha(chart1),
        'chart2': get_grahan_dosha(chart2)
    }
    
    # Get Dosha cancellation
    dosha_cancellation = get_dosha_cancellation(chart1, chart2)
    
    # Print Dosha analysis
    print_dosha_analysis(dosha_analysis, dosha_cancellation)
    
    # Get Dosha remedies
    dosha_remedies = get_dosha_remedies(chart1, chart2)
    
    # Print Dosha remedies
    print_dosha_remedies(dosha_remedies)
    
    # Get Dasha compatibility
    dasha_compatibility = get_dasha_compatibility(chart1, chart2)
    
    # Print Dasha compatibility
    print_dasha_compatibility(dasha_compatibility)
    
    # Get Dasha predictions
    dasha_predictions = get_dasha_predictions(chart1, chart2)
    
    # Print Dasha predictions
    print_dasha_predictions(dasha_predictions)
    
    # Get Navamsa compatibility
    navamsa_compatibility = get_navamsa_compatibility(chart1, chart2)
    
    # Print Navamsa compatibility
    print_navamsa_compatibility(navamsa_compatibility)
    
    # Get compatibility timeline
    current_date = Datetime.fromDatetime(datetime.now())
    end_jd = current_date.jd + args.timeline_days
    end_date = Datetime.fromJD(end_jd, current_date.utcoffset)
    timeline = get_compatibility_timeline(chart1, chart2, current_date, end_date)
    
    # Print compatibility timeline
    print_compatibility_timeline(timeline)
    
    # Get overall compatibility
    compatibility = get_compatibility(chart1, chart2)
    
    # Print overall compatibility
    print_overall_compatibility(compatibility)


if __name__ == "__main__":
    main()
