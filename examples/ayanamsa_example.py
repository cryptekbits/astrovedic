#!/usr/bin/env python3
"""
    Example script to demonstrate the use of different ayanamsas in flatlib.

    This script calculates the position of the Sun using different ayanamsas
    and displays the results.
"""

import sys
import os

# Add the parent directory to the path so we can import flatlib
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const

# Create a sample date and location
date = Datetime('2023/05/15', '12:00', '+00:00')
pos = GeoPos('38n32', '8w54')

# List of ayanamsas to test
ayanamsas = [
    const.AY_FAGAN_BRADLEY,
    const.AY_LAHIRI,
    const.AY_DELUCE,
    const.AY_RAMAN,
    const.AY_KRISHNAMURTI,
    const.AY_SASSANIAN,
    const.AY_YUKTESHWAR,
    const.AY_JN_BHASIN,
    const.AY_SURYASIDDHANTA,
    const.AY_ARYABHATA,
    const.AY_TRUE_CITRA,
    const.AY_TRUE_REVATI,
    const.AY_TRUE_PUSHYA,
    const.AY_TRUE_MULA,
    const.AY_TRUE_SHEORAN
]

# Print header
print(f"Sun position on {date.date} at {date.time} UTC")
print("-" * 60)
print(f"{'Ayanamsa':<30} {'Tropical':<15} {'Sidereal':<15}")
print("-" * 60)

# Create a tropical chart
tropical_chart = Chart(date, pos)
sun_tropical = tropical_chart.getObject(const.SUN)

# Calculate and display Sun position for each ayanamsa
for ayanamsa in ayanamsas:
    # Create a sidereal chart with the current ayanamsa
    sidereal_chart = Chart(date, pos, mode=ayanamsa)
    sun_sidereal = sidereal_chart.getObject(const.SUN)

    # Format the ayanamsa name
    ayanamsa_name = ayanamsa.replace('Ayanamsa ', '')

    # Print the results
    print(f"{ayanamsa_name:<30} {sun_tropical.sign} {sun_tropical.signlon:>6.2f}° {sun_sidereal.sign} {sun_sidereal.signlon:>6.2f}°")
