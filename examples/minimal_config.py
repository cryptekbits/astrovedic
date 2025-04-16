#!/usr/bin/env python3
"""
Minimal Configuration Example

This is a minimal example of using the configuration system in astrovedic.
"""

import sys
import os

# Add the parent directory to the path so we can import astrovedic
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from astrovedic import const
    from astrovedic.datetime import Datetime
    from astrovedic.geopos import GeoPos
    from astrovedic.chart import Chart
    from astrovedic.vedic.config import ChartConfiguration
    
    # Create a sample birth data
    birth_date = Datetime('2025/04/09', '20:51', '+05:30')
    birth_location = GeoPos(12.9716, 77.5946)  # Bangalore, India
    
    print("Birth Date:", birth_date)
    print("Birth Location:", birth_location)
    
    # Create a default configuration (Lahiri ayanamsa with Whole Sign houses)
    default_config = ChartConfiguration()
    print(f"Ayanamsa: {default_config.ayanamsa}")
    print(f"House System: {default_config.house_system}")
    
    # Create a chart with this configuration
    chart = Chart(birth_date, birth_location,
                 hsys=default_config.house_system,
                 ayanamsa=default_config.ayanamsa)
    
    # Print some basic information from the chart
    sun = chart.getObject(const.SUN)
    moon = chart.getObject(const.MOON)
    asc = chart.getAngle(const.ASC)
    
    print(f"Sun: {sun.sign} {sun.signlon:.2f}°")
    print(f"Moon: {moon.sign} {moon.signlon:.2f}°")
    print(f"Ascendant: {asc.sign} {asc.signlon:.2f}°")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
