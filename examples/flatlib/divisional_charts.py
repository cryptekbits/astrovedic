#!/usr/bin/env python3
"""
    Divisional Charts (Vargas) Example
    
    This example demonstrates how to work with divisional charts
    using the flatlib library.
"""

from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib.vedic.api import VedicChart
from flatlib.vedic.vargas import D1, D9, D10

# Define date, time, and location
date = Datetime('2025/04/09', '20:51', '+05:30')
location = GeoPos(12.9716, 77.5946)  # Bangalore, India

# Create a chart using Whole Sign houses and Lahiri ayanamsa
chart = Chart(date, location, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
vedic_chart = VedicChart(chart)

# Print basic chart information
print("Basic Chart Information:")
print(f"Date: {date}")
print(f"Location: {location}")
print(f"House System: {chart.hsys}")
print(f"Ayanamsa: {chart.mode}")
print()

# Get the D1 chart (Rashi chart - same as birth chart)
d1_chart = chart # D1 is the main chart
print("D1 Chart (Rashi - Birth Chart):")
for planet_id in const.LIST_OBJECTS_VEDIC:
    planet = d1_chart.getObject(planet_id)
    house_num = chart.houses.getObjectHouse(planet).num() # Get house number correctly
    print(f"{planet.id}: {planet.sign} {planet.lon:.2f}° (House {house_num})")
print()

# Get the D9 chart (Navamsha chart)
d9_chart = vedic_chart.get_varga_chart(D9)
print("D9 Chart (Navamsha - Marriage and General Life Path):")
if d9_chart:
    for planet_id in const.LIST_OBJECTS_VEDIC: 
        planet = d9_chart.getObject(planet_id)
        print(f"  {planet.id}: {planet.sign} {planet.lon:.2f}°") 
else:
    print("  Could not calculate D9 chart.")
print()

# Get the D10 chart (Dashamsha chart)
d10_chart = vedic_chart.get_varga_chart(D10)
print("D10 Chart (Dashamsha - Career and Profession):")
if d10_chart:
    for planet_id in const.LIST_OBJECTS_VEDIC: 
        planet = d10_chart.getObject(planet_id)
        print(f"  {planet.id}: {planet.sign} {planet.lon:.2f}°")
print()

# Commenting out due to incorrect function usage: 
# get_varga_positions expects a Varga ID, not a Planet ID.
# print("Sun's Position in Different Vargas:")
# sun_positions = vedic_chart.get_varga_positions(const.SUN) 
# for varga, position in sun_positions.items():
#     print(f"  {varga}: {position.sign} {position.lon:.2f}°")
# print()
# 
# print("Moon's Position in Different Vargas:")
# moon_positions = vedic_chart.get_varga_positions(const.MOON)
# for varga, position in moon_positions.items():
#     print(f"  {varga}: {position.sign} {position.lon:.2f}°")
# print()

# Analyze vargas
varga_analysis = vedic_chart.analyze_vargas() 
print("\nVarga Analysis Summary:")
if varga_analysis:
    # Keys 'strongest_vargas', 'weakest_vargas', 'vimshopaka_bala' not found in varga_analysis dict.
    # print(f"  Strongest Vargas: {varga_analysis['strongest_vargas']}") 
    # print(f"  Weakest Vargas: {varga_analysis['weakest_vargas']}")   
    # print(f"  Overall Vimshopaka Bala: {varga_analysis['vimshopaka_bala']:.2f}") 
    pass # Keep the if block structure, print average score below
else:
    print("  Could not perform Varga analysis.")

# Print a summary
print("\nVarga Summary:") # Add newline for better formatting
print(f"Overall Vimshopaka Bala: {varga_analysis['overall_strength']['average_vimshopaka']:.2f}/20") # Uncomment this line
# Keys 'strongest_planet', 'weakest_planet' not found in varga_analysis dict.
# print(f"Strongest Planet in Vargas: {varga_analysis['strongest_planet']}")
# print(f"Weakest Planet in Vargas: {varga_analysis['weakest_planet']}")
