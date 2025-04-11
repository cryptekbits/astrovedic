#!/usr/bin/env python3
"""
    Detailed Analysis Example
    
    This example demonstrates how to perform detailed analysis
    using the AstroVed Extension.
"""

from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib.vedic.api import VedicChart
from astroved_extension.api import AstroVedChart, create_astroved_chart

# Method 1: Create an AstroVedChart directly from date and location
chart = create_astroved_chart(
    date_str='2025/04/09',
    time_str='20:51',
    lat=12.9716,
    lon=77.5946,
    timezone='+05:30',
    hsys=const.HOUSES_WHOLE_SIGN,
    ayanamsa=const.AY_LAHIRI
)

# Method 2: Create a flatlib Chart and VedicChart first, then convert
date = Datetime('2025/04/09', '20:51', '+05:30')
location = GeoPos(12.9716, 77.5946)  # Bangalore, India
flatlib_chart = Chart(date, location, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
vedic_chart = VedicChart(flatlib_chart)
chart2 = AstroVedChart.from_vedic_chart(vedic_chart)

# Print basic chart information
print("Basic Chart Information:")
print(f"Date: {chart.chart.date}")
print(f"Location: {chart.chart.pos}")
print(f"House System: {chart.chart.houses.name}")
print(f"Ayanamsa: {chart.chart.mode}")
print()

# Perform detailed yoga analysis
yoga_analysis = chart.analyze_yogas()
print("Detailed Yoga Analysis:")
print(f"Total Yogas: {len(yoga_analysis['yogas'])}")
print(f"Raja Yogas: {len(yoga_analysis['raja_yogas'])}")
print(f"Dhana Yogas: {len(yoga_analysis['dhana_yogas'])}")
print(f"Dosha Yogas: {len(yoga_analysis['dosha_yogas'])}")
print()

print("Top 5 Yogas:")
for yoga in yoga_analysis['yogas'][:5]:
    print(f"- {yoga['name']}: {yoga['description']}")
print()

# Get yoga predictions
yoga_predictions = chart.get_yoga_predictions()
print("Yoga Predictions:")
print(f"Overall Strength: {yoga_predictions['overall_strength']}/100")
print()

print("Life Area Predictions:")
for area, prediction in yoga_predictions['life_areas'].items():
    print(f"- {area}: {prediction['prediction']}")
print()

# Perform detailed ashtakavarga analysis
ashtakavarga_analysis = chart.analyze_ashtakavarga()
print("Detailed Ashtakavarga Analysis:")
print(f"Total Bindus: {ashtakavarga_analysis['total_bindus']}")
print(f"Average Bindus per Sign: {ashtakavarga_analysis['average_bindus_per_sign']:.2f}")
print()

print("Planet Bindus:")
for planet_id, bindus in ashtakavarga_analysis['planet_bindus'].items():
    print(f"- {planet_id}: {bindus}")
print()

# Get ashtakavarga predictions
ashtakavarga_predictions = chart.get_ashtakavarga_predictions()
print("Ashtakavarga Predictions:")
for sign, prediction in ashtakavarga_predictions['sign_predictions'].items():
    print(f"- {sign}: {prediction}")
print()

# Perform detailed shadbala analysis
shadbala_analysis = chart.analyze_shadbala()
print("Detailed Shadbala Analysis:")
print(f"Strongest Planet: {shadbala_analysis['strongest_planet']}")
print(f"Weakest Planet: {shadbala_analysis['weakest_planet']}")
print()

print("Planet Shadbala:")
for planet_id, strength in shadbala_analysis['planet_strengths'].items():
    print(f"- {planet_id}: {strength['total']:.2f} (Minimum Required: {strength['minimum_required']:.2f})")
print()

# Get shadbala predictions
shadbala_predictions = chart.get_shadbala_predictions()
print("Shadbala Predictions:")
for planet_id, prediction in shadbala_predictions['planet_predictions'].items():
    print(f"- {planet_id}: {prediction}")
print()

# Perform detailed varga analysis
varga_analysis = chart.analyze_vargas()
print("Detailed Varga Analysis:")
print(f"Average Vimshopaka Bala: {varga_analysis['overall_strength']['average_vimshopaka']:.2f}/20")
print()

print("Planet Vimshopaka Bala:")
for planet_id, analysis in varga_analysis['planet_analysis'].items():
    if 'vimshopaka_bala' in analysis:
        print(f"- {planet_id}: {analysis['vimshopaka_bala']['total']:.2f}/20")
print()

# Get varga predictions
varga_predictions = chart.get_varga_predictions()
print("Varga Predictions:")
for prediction in varga_predictions['general']:
    print(f"- {prediction}")
print()

# Analyze transits
transit_analysis = chart.analyze_transits()
print("Detailed Transit Analysis:")
print(f"Transit Date: {transit_analysis['transit_date']}")
print(f"Transit Quality: {transit_analysis['transit_quality']}")
print()

print("Transit Aspects:")
for aspect in transit_analysis['transit_aspects'][:5]:  # Print first 5 aspects
    print(f"- {aspect['transit_planet']} aspects {aspect['natal_planet']} ({aspect['aspect_type']})")
print()

# Get transit predictions
transit_predictions = chart.get_transit_predictions()
print("Transit Predictions:")
for prediction in transit_predictions['general']:
    print(f"- {prediction}")
print()

# Print a summary
print("Chart Summary:")
print(f"Lagna (Ascendant): {chart.chart.getObject(const.ASC).sign}")
print(f"Moon Sign: {chart.chart.getObject(const.MOON).sign}")
print(f"Sun Sign: {chart.chart.getObject(const.SUN).sign}")
print(f"Overall Yoga Strength: {yoga_predictions['overall_strength']}/100")
print(f"Overall Shadbala Strength: {shadbala_analysis['overall_strength']}/100")
print(f"Overall Vimshopaka Bala: {varga_analysis['overall_strength']['average_vimshopaka']:.2f}/20")
