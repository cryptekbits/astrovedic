#!/usr/bin/env python3
"""
    Compatibility Analysis Example
    
    This example demonstrates how to analyze compatibility between two charts
    using the flatlib library.
"""

from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic import const
from astrovedic.vedic.api import VedicChart
import json

# Define date, time, and location for the first person
date1 = Datetime('2025/04/09', '20:51', '+05:30')
location1 = GeoPos(12.9716, 77.5946)  # Bangalore, India

# Create a chart for the first person
chart1 = Chart(date1, location1, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
vedic_chart1 = VedicChart(chart1)

# Define date, time, and location for the second person
date2 = Datetime('2025/05/15', '14:30', '+05:30')
location2 = GeoPos(12.9716, 77.5946)  # Bangalore, India

# Create a chart for the second person
chart2 = Chart(date2, location2, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
vedic_chart2 = VedicChart(chart2)

# Print basic chart information for both people
print("Person 1 Chart Information:")
print(f"Date: {date1}")
print(f"Location: {location1}")
for first_house1 in chart1.houses:
    print(f"Lagna (Ascendant): {first_house1.sign}")
    break
print(f"Moon Sign: {chart1.getObject(const.MOON).sign}")
print(f"Sun Sign: {chart1.getObject(const.SUN).sign}")
print()

print("Person 2 Chart Information:")
print(f"Date: {date2}")
print(f"Location: {location2}")
for first_house2 in chart2.houses:
    print(f"Lagna (Ascendant): {first_house2.sign}")
    break
print(f"Moon Sign: {chart2.getObject(const.MOON).sign}")
print(f"Sun Sign: {chart2.getObject(const.SUN).sign}")
print()

# Get basic compatibility information
compatibility = vedic_chart1.get_compatibility(vedic_chart2)
print("Basic Compatibility Information:")
print(f"Overall Score: {compatibility['overall_score']}/100")
print(f"Moon Compatibility: {compatibility['moon_compatibility']['score']}/100")
print(f"Sun Compatibility: {compatibility['sun_compatibility']['score']}/100")
print(f"Ascendant Compatibility: {compatibility['ascendant_compatibility']['score']}/100")
print()

# Get detailed compatibility analysis
compatibility_analysis = vedic_chart1.get_compatibility_analysis(vedic_chart2)
print("\nCompatibility Analysis:")

# Kuta Score
print(f"Kuta Score: {compatibility_analysis['kuta_scores']['total_kuta_score']['total_score']}/{compatibility_analysis['kuta_scores']['total_kuta_score']['max_total_score']}")
print()

# Kuta Details 
print("Kuta Details:") 
for kuta, details in compatibility_analysis['kuta_scores']['kuta_scores'].items():
    print(f"- {kuta}: {details['score']}/{details['max_score']} - {details['description']}")
print()

# Key 'strengths' not found in compatibility_analysis
# print("Compatibility Strengths:")
# for strength in compatibility_analysis['strengths'][:3]:  # Print top 3 strengths
#     print(f"- {strength}")
# print()

# Key 'challenges' not found in compatibility_analysis
# print("Compatibility Challenges:")
# for challenge in compatibility_analysis['challenges'][:3]:  # Print top 3 challenges
#     print(f"- {challenge}")
# print()

# Key 'recommendations' not found in compatibility_analysis
# print("Compatibility Recommendations:")
# for recommendation in compatibility_analysis['recommendations'][:3]:  # Print top 3 recommendations
#     print(f"- {recommendation}")
# print()

# Print a summary
print("Compatibility Summary:")
# Overall Compatibility Level
print(f"Overall Compatibility: {compatibility_analysis['level']}")
# Key 'recommendation' not found in compatibility_analysis
# print(f"Recommendation: {compatibility_analysis['recommendation']}")
