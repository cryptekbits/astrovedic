#!/usr/bin/env python3
"""
    Basic Chart Creation Example
    
    This example demonstrates how to create a basic Vedic astrology chart
    using the flatlib library and access its basic properties.
"""

from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib.vedic.api import VedicChart

# Define date, time, and location
date = Datetime('2025/04/09', '20:51', '+05:30')
location = GeoPos(12.9716, 77.5946)  # Bangalore, India

# Create a chart using Whole Sign houses and Lahiri ayanamsa
chart = Chart(date, location, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)

# Create a Vedic chart from the basic chart
vedic_chart = VedicChart(chart)

# Print basic chart information
print("Basic Chart Information:")
print(f"Date: {chart.date}")
print(f"Location: {chart.pos}")
print(f"House System: {chart.hsys}")
print(f"Ayanamsa: {chart.mode}")
print()

# Print planet positions
print("Planet Positions:")
for planet_id in const.LIST_OBJECTS_VEDIC:
    planet = chart.getObject(planet_id)
    print(f"{planet.id}: {planet.sign} {planet.lon:.2f}° (House {chart.houses.getObjectHouse(planet).num()})")
print()

# Print house cusps
print("House Cusps:")
for house in chart.houses: 
    print(f"House {house.num()}: {house.sign} {house.lon:.2f}°") 
print()

# Get nakshatra information
print("Nakshatra Information:")
for planet_id in const.LIST_OBJECTS_VEDIC:
    planet = chart.getObject(planet_id)
    nakshatra = vedic_chart.get_nakshatra(planet_id)
    print(f"{planet.id}: {nakshatra['name']} (Pada {nakshatra['pada']})")
print()

# Get panchanga information
panchanga = vedic_chart.get_panchang() 
print("Panchanga Information:")
# print(panchanga) 
print(f"Tithi: {panchanga['tithi']['name']} ({panchanga['tithi']['paksha']})") 
print(f"Karana: {panchanga['karana']['name']}") 
print(f"Yoga: {panchanga['yoga']['name']}") 
print(f"Vara: {panchanga['vara']['name']}") 
print()

# Get basic yoga information
yogas = vedic_chart.get_yogas()
print("Yoga Information:")
# print(yogas) 
print(f"Total Yogas: {yogas['summary']['total_yogas']}") 
# for yoga in yogas['yogas'][:5]:  
#     print(f"- {yoga['name']}: {yoga['description']}") 
print()

# Get basic varga information
vargas = vedic_chart.analyze_vargas()
print("Varga Information:")
print(f"Average Vimshopaka Bala: {vargas['overall_strength']['average_vimshopaka']:.2f}/20")
print()

# Get basic muhurta information
muhurta = vedic_chart.get_muhurta()
print("Muhurta Information:")
print(f"Quality: {muhurta['quality']}")
print()

# Get basic sarvatobhadra information
sarvatobhadra = vedic_chart.get_sarvatobhadra()
print("Sarvatobhadra Information:")
print(f"Quality: {sarvatobhadra['quality']}")
print(f"Best Direction: {sarvatobhadra['best_direction']['direction']} ({sarvatobhadra['best_direction']['quality']})")
print()

# Get basic transit information
transits = vedic_chart.get_transits()
print("Transit Information:")
print(f"Transit Quality: {transits['transit_quality']}")
print()

# Print a summary
print("Chart Summary:")
for first_house in chart.houses: # Iterate to get the first house
    print(f"Lagna (Ascendant): {first_house.sign}") 
    break # Only need the first one
# print(f"Lagna Lord: {vedic_chart.get_lagna_lord()['lord']}")
# print(f"Strongest House: House {vedic_chart.get_strongest_house()['house']} ({vedic_chart.get_strongest_house()['strength']:.2f})")
# print(f"Weakest House: House {vedic_chart.get_weakest_house()['house']} ({vedic_chart.get_weakest_house()['strength']:.2f})")
