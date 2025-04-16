#!/usr/bin/env python3
"""
Minimal API Example

This is a minimal example of using the Vedic API in astrovedic.
"""

import sys
import os

# Add the parent directory to the path so we can import astrovedic
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from astrovedic import const
    from astrovedic.vedic.api import create_vedic_chart, create_kp_chart
    
    print("Creating Vedic chart...")
    
    # Create a Vedic chart with default configuration
    vedic_chart = create_vedic_chart(
        '2025/04/09', '20:51',
        12.9716, 77.5946,
        '+05:30'
    )
    
    print("Vedic chart created successfully.")
    print(f"Ayanamsa: {vedic_chart.chart.mode}")
    print(f"House System: {vedic_chart.chart.hsys}")
    
    # Print some basic information from the chart
    sun = vedic_chart.chart.getObject(const.SUN)
    moon = vedic_chart.chart.getObject(const.MOON)
    asc = vedic_chart.chart.getAngle(const.ASC)
    
    print(f"Sun: {sun.sign} {sun.signlon:.2f}°")
    print(f"Moon: {moon.sign} {moon.signlon:.2f}°")
    print(f"Ascendant: {asc.sign} {asc.signlon:.2f}°")
    
    print("\nCreating KP chart...")
    
    # Create a KP chart with default KP configuration
    kp_chart = create_kp_chart(
        '2025/04/09', '20:51',
        12.9716, 77.5946,
        '+05:30'
    )
    
    print("KP chart created successfully.")
    print(f"Ayanamsa: {kp_chart.chart.mode}")
    print(f"House System: {kp_chart.chart.hsys}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
