#!/usr/bin/env python3
"""
    Muhurta Analysis Example
    
    This example demonstrates how to perform detailed muhurta analysis
    using the AstroVed Extension.
"""

from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from astroved_extension.api import create_astroved_chart
from datetime import datetime, timedelta

# Define location
location = GeoPos(12.9716, 77.5946)  # Bangalore, India

# Create a chart for the current date and time
current_date = Datetime.now()
chart = create_astroved_chart(
    date_str=current_date.date,
    time_str=current_date.time,
    lat=location.lat,
    lon=location.lon,
    timezone=current_date.timezone
)

# Print basic information
print("Current Date and Time:")
print(f"{current_date}")
print(f"Location: Bangalore, India (Lat: {location.lat}, Lon: {location.lon})")
print()

# Analyze muhurta for the current date
muhurta = chart.analyze_muhurta()
print("Muhurta Analysis for Current Date:")
print(f"Overall Quality: {muhurta['quality']}")
print()

print("Panchanga:")
panchanga = muhurta['panchanga']
print(f"Tithi: {panchanga['tithi']['tithi']} ({panchanga['tithi']['paksha']})")
print(f"Karana: {panchanga['karana']['karana']}")
print(f"Yoga: {panchanga['yoga']['yoga']}")
print(f"Vara: {panchanga['vara']['vara']}")
print(f"Nakshatra: {panchanga['nakshatra']['nakshatra']}")
print()

print("Special Muhurtas:")
special_muhurtas = muhurta['special_muhurtas']
for name, details in special_muhurtas.items():
    if details['is_active']:
        print(f"- {name}: Active from {details['start_time']} to {details['end_time']}")
print()

print("Inauspicious Periods:")
inauspicious_periods = muhurta['inauspicious_periods']
for name, details in inauspicious_periods.items():
    print(f"- {name}: {details['start_time']} to {details['end_time']}")
print()

print("Auspicious Yogas:")
auspicious_yogas = muhurta['auspicious_yogas']
for name, is_active in auspicious_yogas.items():
    if is_active:
        print(f"- {name}: Active")
print()

# Get muhurta predictions
predictions = chart.get_muhurta_predictions()
print("Muhurta Predictions:")
for prediction in predictions['general']:
    print(f"- {prediction}")
print()

print("Activity Recommendations:")
for activity, recommendation in predictions['activities'].items():
    print(f"- {activity}: {recommendation}")
print()

# Define a date range for finding the best muhurta
start_date = Datetime.now()
end_date = Datetime(
    (datetime.strptime(start_date.date, '%Y/%m/%d') + timedelta(days=7)).strftime('%Y/%m/%d'),
    '23:59',
    start_date.timezone
)

# Find the best muhurta for different activities
activities = ['marriage', 'travel', 'business', 'education', 'medical', 'spiritual']

print("Best Muhurtas for Activities (Next 7 Days):")
for activity in activities:
    best_muhurta = chart.analyze_muhurta_for_activity(activity, start_date, end_date)
    print(f"Best Muhurta for {activity.capitalize()}:")
    print(f"- Date: {best_muhurta['date']}")
    print(f"- Time: {best_muhurta['time']}")
    print(f"- Quality: {best_muhurta['quality']}")
    print(f"- Reason: {best_muhurta['reason']}")
    print()

# Print a summary
print("Muhurta Summary:")
print(f"Current Muhurta Quality: {muhurta['quality']}")
if muhurta['quality'] in ['Excellent', 'Good']:
    print("This is a favorable time for most activities.")
elif muhurta['quality'] == 'Neutral':
    print("This is a neutral time. Consider the specific activity recommendations.")
else:
    print("This is an unfavorable time. It's recommended to postpone important activities if possible.")
