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
print(f"Date: {chart.date}")
print(f"Location: {chart.pos}")
print(f"House System: {chart.houses.name}")
print(f"Ayanamsa: {chart.mode}")
print()

# Get the D1 chart (Rashi chart - same as birth chart)
d1_chart = vedic_chart.get_varga_chart(D1)
print("D1 Chart (Rashi - Birth Chart):")
for planet_id in const.LIST_PLANETS:
    planet = d1_chart.getObject(planet_id)
    print(f"{planet.id}: {planet.sign} {planet.lon:.2f}° (House {planet.house})")
print()

# Get the D9 chart (Navamsha chart)
d9_chart = vedic_chart.get_varga_chart(D9)
print("D9 Chart (Navamsha - Marriage and General Life Path):")
for planet_id in const.LIST_PLANETS:
    planet = d9_chart.getObject(planet_id)
    print(f"{planet.id}: {planet.sign} {planet.lon:.2f}° (House {planet.house})")
print()

# Get the D10 chart (Dashamsha chart)
d10_chart = vedic_chart.get_varga_chart(D10)
print("D10 Chart (Dashamsha - Career and Profession):")
for planet_id in const.LIST_PLANETS:
    planet = d10_chart.getObject(planet_id)
    print(f"{planet.id}: {planet.sign} {planet.lon:.2f}° (House {planet.house})")
print()

# Get planet positions in different vargas
sun_positions = vedic_chart.get_varga_positions(const.SUN)
print("Sun Positions in Different Vargas:")
for varga, position in sun_positions.items():
    print(f"{varga}: {position['sign']} {position['longitude']:.2f}°")
print()

moon_positions = vedic_chart.get_varga_positions(const.MOON)
print("Moon Positions in Different Vargas:")
for varga, position in moon_positions.items():
    print(f"{varga}: {position['sign']} {position['longitude']:.2f}°")
print()

# Analyze vargas
varga_analysis = vedic_chart.analyze_vargas()
print("Varga Analysis:")
print(f"Average Vimshopaka Bala: {varga_analysis['overall_strength']['average_vimshopaka']:.2f}/20")
print()

print("Planet Vimshopaka Bala:")
for planet_id, analysis in varga_analysis['planet_analysis'].items():
    if 'vimshopaka_bala' in analysis:
        print(f"{planet_id}: {analysis['vimshopaka_bala']['total']:.2f}/20")
print()

print("Varga Visesha (Special Combinations):")
for planet_id, analysis in varga_analysis['planet_analysis'].items():
    if 'varga_visesha' in analysis and analysis['varga_visesha']['has_visesha']:
        print(f"{planet_id}: {analysis['varga_visesha']['highest_visesha']}")
print()

# Print a summary
print("Varga Summary:")
print(f"Overall Vimshopaka Bala: {varga_analysis['overall_strength']['average_vimshopaka']:.2f}/20")
print(f"Strongest Planet in Vargas: {varga_analysis['strongest_planet']}")
print(f"Weakest Planet in Vargas: {varga_analysis['weakest_planet']}")
