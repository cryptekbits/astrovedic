#!/usr/bin/env python3
"""
    Detailed Compatibility Analysis Example
    
    This example demonstrates how to perform detailed compatibility analysis
    using the AstroVed Extension.
"""

from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib.vedic.api import VedicChart
from astroved_extension.api import AstroVedChart, create_astroved_chart

# Create charts for two people
chart1 = create_astroved_chart(
    date_str='2025/04/09',
    time_str='20:51',
    lat=12.9716,
    lon=77.5946,
    timezone='+05:30',
    hsys=const.HOUSES_WHOLE_SIGN,
    ayanamsa=const.AY_LAHIRI
)

chart2 = create_astroved_chart(
    date_str='2025/05/15',
    time_str='14:30',
    lat=12.9716,
    lon=77.5946,
    timezone='+05:30',
    hsys=const.HOUSES_WHOLE_SIGN,
    ayanamsa=const.AY_LAHIRI
)

# Print basic chart information for both people
print("Person 1 Chart Information:")
print(f"Date: {chart1.chart.date}")
print(f"Lagna (Ascendant): {chart1.chart.getObject(const.ASC).sign}")
print(f"Moon Sign: {chart1.chart.getObject(const.MOON).sign}")
print(f"Sun Sign: {chart1.chart.getObject(const.SUN).sign}")
print()

print("Person 2 Chart Information:")
print(f"Date: {chart2.chart.date}")
print(f"Lagna (Ascendant): {chart2.chart.getObject(const.ASC).sign}")
print(f"Moon Sign: {chart2.chart.getObject(const.MOON).sign}")
print(f"Sun Sign: {chart2.chart.getObject(const.SUN).sign}")
print()

# Get detailed compatibility analysis
compatibility = chart1.get_detailed_compatibility(chart2)
print("Detailed Compatibility Analysis:")
print(f"Overall Score: {compatibility['overall_score']}/100")
print()

print("Compatibility Factors:")
for factor, score in compatibility['factor_scores'].items():
    print(f"- {factor}: {score}/100")
print()

# Get detailed compatibility report
report = chart1.get_compatibility_report(chart2)
print("Detailed Compatibility Report:")
print(f"Overall Compatibility: {report['overall_compatibility']}")
print(f"Compatibility Level: {report['compatibility_level']}")
print()

print("Kuta Analysis:")
for kuta, details in report['kutas'].items():
    print(f"- {kuta}: {details['score']}/{details['max_score']} - {details['description']}")
print()

print("Dasha Compatibility:")
print(f"Dasha Compatibility Score: {report['dasha_compatibility']['score']}/100")
print(f"Current Dasha Period: {report['dasha_compatibility']['current_dasha']}")
print()

print("Ashtakavarga Compatibility:")
print(f"Ashtakavarga Compatibility Score: {report['ashtakavarga_compatibility']['score']}/100")
print()

print("Varga Compatibility:")
print(f"Navamsha (D9) Compatibility: {report['varga_compatibility']['navamsha_compatibility']}/100")
print(f"Dashamsha (D10) Compatibility: {report['varga_compatibility']['dashamsha_compatibility']}/100")
print()

# Get compatibility timeline
timeline = chart1.get_compatibility_timeline(chart2)
print("Compatibility Timeline:")
print(f"Total Events: {len(timeline['events'])}")
print()

print("Upcoming Events:")
for event in timeline['events'][:5]:  # Print first 5 events
    print(f"- {event['date']}: {event['description']}")
print()

print("Favorable Periods:")
for period in timeline['favorable_periods'][:3]:  # Print first 3 favorable periods
    print(f"- {period['start_date']} to {period['end_date']}: {period['description']}")
print()

print("Challenging Periods:")
for period in timeline['challenging_periods'][:3]:  # Print first 3 challenging periods
    print(f"- {period['start_date']} to {period['end_date']}: {period['description']}")
print()

# Print compatibility strengths and challenges
print("Compatibility Strengths:")
for strength in report['strengths'][:5]:  # Print top 5 strengths
    print(f"- {strength}")
print()

print("Compatibility Challenges:")
for challenge in report['challenges'][:5]:  # Print top 5 challenges
    print(f"- {challenge}")
print()

# Print compatibility recommendations
print("Compatibility Recommendations:")
for recommendation in report['recommendations'][:5]:  # Print top 5 recommendations
    print(f"- {recommendation}")
print()

# Print a summary
print("Compatibility Summary:")
print(f"Overall Compatibility Score: {compatibility['overall_score']}/100")
print(f"Compatibility Level: {report['compatibility_level']}")
print(f"Recommendation: {report['recommendation']}")
