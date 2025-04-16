#!/usr/bin/env python3
"""
    Example script to demonstrate the use of different Vedic ayanamsas in astrovedic.

    This script calculates the position of the Sun using different Vedic ayanamsas
    and displays the results. The astrovedic library focuses on Vedic astrology
    calculations without any predictive analysis.
"""

import sys
import os

# Add the parent directory to the path so we can import astrovedic
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic import const

# Create a sample date and location
date = Datetime('2023/05/15', '12:00', '+00:00')
pos = GeoPos('38n32', '8w54')

# List of Vedic ayanamsas to test
ayanamsas = [
    # Primary Vedic Ayanamsas
    const.AY_LAHIRI,        # Official ayanamsa of the Indian government
    const.AY_RAMAN,         # B.V. Raman's ayanamsa
    const.AY_KRISHNAMURTI,  # K.S. Krishnamurti's ayanamsa for KP system

    # Additional Vedic Ayanamsas
    const.AY_YUKTESHWAR,    # Based on Sri Yukteshwar's book "The Holy Science"
    const.AY_JN_BHASIN,     # J.N. Bhasin's ayanamsa
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
print("-" * 70)
print(f"{'Ayanamsa':<20} {'Tropical':<15} {'Sidereal':<15} {'Difference':<10}")
print("-" * 70)

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

    # Calculate the ayanamsa value (difference between tropical and sidereal)
    from astrovedic.ephem import swe
    ayanamsa_value = swe.get_ayanamsa(date.jd, ayanamsa)

    # Print the results
    print(f"{ayanamsa_name:<20} {sun_tropical.sign} {sun_tropical.signlon:>6.2f}° {sun_sidereal.sign} {sun_sidereal.signlon:>6.2f}° {ayanamsa_value:>9.2f}°")

print("\nNote: The 'Difference' column shows the ayanamsa value in degrees (the precession offset)")
print("      This is the angular difference between the tropical and sidereal zodiacs.")
