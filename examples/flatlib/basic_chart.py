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
print(f"House System: {chart.houses.name}")
print(f"Ayanamsa: {chart.mode}")
print()

# Print planet positions
print("Planet Positions:")
for planet_id in const.LIST_PLANETS:
    planet = chart.getObject(planet_id)
    print(f"{planet.id}: {planet.sign} {planet.lon:.2f}° (House {planet.house})")
print()

# Print house cusps
print("House Cusps:")
for house_num in range(1, 13):
    house = chart.houses.getHouse(house_num)
    print(f"House {house.num}: {house.sign} {house.lon:.2f}°")
print()

# Get nakshatra information
print("Nakshatra Information:")
for planet_id in const.LIST_PLANETS:
    planet = chart.getObject(planet_id)
    nakshatra = vedic_chart.get_nakshatra(planet_id)
    print(f"{planet.id}: {nakshatra['nakshatra']} (Pada {nakshatra['pada']})")
print()

# Get panchanga information
panchanga = vedic_chart.get_panchanga()
print("Panchanga Information:")
print(f"Tithi: {panchanga['tithi']['tithi']} ({panchanga['tithi']['paksha']})")
print(f"Karana: {panchanga['karana']['karana']}")
print(f"Yoga: {panchanga['yoga']['yoga']}")
print(f"Vara: {panchanga['vara']['vara']}")
print()

# Get basic yoga information
yogas = vedic_chart.get_yogas()
print("Yoga Information:")
print(f"Total Yogas: {len(yogas['yogas'])}")
for yoga in yogas['yogas'][:5]:  # Print first 5 yogas
    print(f"- {yoga['name']}: {yoga['description']}")
print()

# Get basic ashtakavarga information
ashtakavarga = vedic_chart.analyze_ashtakavarga()
print("Ashtakavarga Information:")
print(f"Total Bindus: {ashtakavarga['total_bindus']}")
print(f"Average Bindus per Sign: {ashtakavarga['average_bindus_per_sign']:.2f}")
print()

# Get basic shadbala information
shadbala = vedic_chart.analyze_shadbala()
print("Shadbala Information:")
print(f"Strongest Planet: {shadbala['strongest_planet']}")
print(f"Weakest Planet: {shadbala['weakest_planet']}")
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
print(f"Lagna (Ascendant): {chart.getObject(const.ASC).sign}")
print(f"Moon Sign: {chart.getObject(const.MOON).sign}")
print(f"Sun Sign: {chart.getObject(const.SUN).sign}")
