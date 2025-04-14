#!/usr/bin/env python3
"""
    Transit Analysis Example
    
    This example demonstrates how to analyze transits for a chart
    using the flatlib library.
"""

from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic import const
from astrovedic.vedic.api import VedicChart

# Define date, time, and location for the natal chart
natal_date = Datetime('2025/04/09', '20:51', '+05:30')
location = GeoPos(12.9716, 77.5946)  # Bangalore, India

# Create the natal chart
natal_chart = Chart(natal_date, location, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
vedic_chart = VedicChart(natal_chart)

try:
    from datetime import datetime
    # Get current local time and timezone
    now = datetime.now()
    tz_str = now.strftime('%z')
    if len(tz_str) == 5: # Format timezone offset like +05:30
        tz_str = tz_str[:3] + ":" + tz_str[3:]
    elif len(tz_str) == 0: # Handle cases where timezone might be naive
        # Attempt to get local offset, or default to UTC if difficult
        # This part can be complex; using a fixed default like UTC might be safer
        # For now, let's assume system provides offset or default to UTC ('+00:00')
        # A more robust solution might involve 'pytz' or 'dateutil'
        try:
            import time
            # Get local offset in seconds, convert to HH:MM format
            offset_seconds = time.localtime().tm_gmtoff
            offset_hours = abs(offset_seconds) // 3600
            offset_minutes = (abs(offset_seconds) % 3600) // 60
            sign = '+' if offset_seconds >= 0 else '-'
            tz_str = f"{sign}{offset_hours:02d}:{offset_minutes:02d}"
        except (ImportError, AttributeError):
             tz_str = '+00:00' # Default to UTC if local offset fails

    transit_date = Datetime(now.strftime('%Y/%m/%d'), now.strftime('%H:%M'), tz_str)
except ImportError:
    print("Python's standard 'datetime' module not found. Using a fixed date for transit.")
    # Option 2: Use a fixed date if datetime is not available or for testing

# Print basic chart information
print("Natal Chart Information:")
print(f"Date: {natal_date}")
print(f"Location: {location}")
for first_house in natal_chart.houses: # Iterate to get Ascendant sign
    print(f"Lagna (Ascendant): {first_house.sign}")
    break
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

# Create transit chart and print positions relative to natal houses
print("\nTransit Planet Positions (Relative to Natal Houses):")
transit_chart = Chart(transit_date, location, hsys=natal_chart.hsys, mode=natal_chart.mode)
for planet_id in const.LIST_OBJECTS_VEDIC:
    transit_planet = transit_chart.getObject(planet_id)
    # Find which natal house the transiting planet is in
    try:
        natal_house_num = natal_chart.houses.getObjectHouse(transit_planet).num()
        print(f"  {transit_planet.id}: {transit_planet.sign} {transit_planet.signlon:.2f}° (Natal House {natal_house_num})")
    except Exception as e:
        # Handle cases where house calculation might fail for some objects/configurations
        print(f"  {transit_planet.id}: {transit_planet.sign} {transit_planet.signlon:.2f}° (Natal House calculation error: {e})")
print()

# Print transit aspects
print("\nTransit Aspects:")
for aspect in transits['transit_aspects'][:5]:  # Print first 5 aspects
    print(f"{aspect['transit_planet']} aspects {aspect['natal_planet']} ({aspect['aspect']})")
print()

# Print gochara effects
print("Gochara (Transit) Effects:")
for planet_id, effect in transits['gochara_effects'].items():
    print(f"{planet_id}: {effect['effect']} ({effect['strength']})")
print()

# Get transit predictions
predictions = vedic_chart.get_transit_predictions(transit_date)
print("\nTransit Predictions:")
# The key 'planet_predictions' does not seem to exist in the 'predictions' dict.
# Commenting out the loop below based on debug output.
# for planet_id, prediction in predictions['planet_predictions'].items():
#     print(f"{planet_id}: {prediction}")
print()

# Example: Find next Saturn return

# Print a summary
print("\nTransit Summary:")
print(f"Overall Quality: {predictions['transit_quality']['quality']}")
print(f"Overall Score: {predictions['transit_quality']['score']}")
# The keys 'most_favorable_planet' and 'most_challenging_planet' do not exist.
# Commenting out the lines below.
# print(f"Most Favorable Planet: {predictions['most_favorable_planet']}")
# print(f"Most Challenging Planet: {predictions['most_challenging_planet']}")
