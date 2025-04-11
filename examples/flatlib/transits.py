#!/usr/bin/env python3
"""
    Transit Analysis Example
    
    This example demonstrates how to analyze transits for a chart
    using the flatlib library.
"""

from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib.vedic.api import VedicChart

# Define date, time, and location for the natal chart
natal_date = Datetime('2025/04/09', '20:51', '+05:30')
location = GeoPos(12.9716, 77.5946)  # Bangalore, India

# Create the natal chart
natal_chart = Chart(natal_date, location, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
vedic_chart = VedicChart(natal_chart)

# Define the transit date
transit_date = Datetime.now()

# Print basic chart information
print("Natal Chart Information:")
print(f"Date: {natal_chart.date}")
print(f"Lagna (Ascendant): {natal_chart.getObject(const.ASC).sign}")
print(f"Moon Sign: {natal_chart.getObject(const.MOON).sign}")
print(f"Sun Sign: {natal_chart.getObject(const.SUN).sign}")
print()

print("Transit Date:")
print(f"{transit_date}")
print()

# Get basic transit information
transits = vedic_chart.get_transits(transit_date)
print("Transit Information:")
print(f"Transit Quality: {transits['transit_quality']}")
print()

# Print transit planet positions
print("Transit Planet Positions:")
for planet_id, planet_info in transits['transit_planets'].items():
    print(f"{planet_id}: {planet_info['sign']} (House {planet_info['house']})")
print()

# Print transit aspects
print("Transit Aspects:")
for aspect in transits['transit_aspects'][:5]:  # Print first 5 aspects
    print(f"{aspect['transit_planet']} aspects {aspect['natal_planet']} ({aspect['aspect_type']})")
print()

# Print gochara effects
print("Gochara (Transit) Effects:")
for planet_id, effect in transits['gochara_effects'].items():
    print(f"{planet_id}: {effect['effect']} ({effect['quality']})")
print()

# Get transit predictions
predictions = vedic_chart.get_transit_predictions(transit_date)
print("Transit Predictions:")
for planet_id, prediction in predictions['planet_predictions'].items():
    print(f"{planet_id}: {prediction}")
print()

# Get transit timeline
timeline = vedic_chart.get_transit_timeline(transit_date)
print("Transit Timeline:")
for event in timeline['events'][:5]:  # Print first 5 events
    print(f"{event['date']}: {event['description']}")
print()

# Print a summary
print("Transit Summary:")
print(f"Overall Transit Quality: {transits['transit_quality']}")
print(f"Most Favorable Planet: {predictions['most_favorable_planet']}")
print(f"Most Challenging Planet: {predictions['most_challenging_planet']}")
