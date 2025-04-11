#!/usr/bin/env python3
"""
    Detailed Transit Analysis Example
    
    This example demonstrates how to perform detailed transit analysis
    using the AstroVed Extension.
"""

from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from astroved_extension.api import create_astroved_chart
from datetime import datetime, timedelta

# Create a natal chart
natal_chart = create_astroved_chart(
    date_str='2025/04/09',
    time_str='20:51',
    lat=12.9716,
    lon=77.5946,
    timezone='+05:30',
    hsys=const.HOUSES_WHOLE_SIGN,
    ayanamsa=const.AY_LAHIRI
)

# Define the transit date (current date)
transit_date = Datetime.now()

# Print basic chart information
print("Natal Chart Information:")
print(f"Date: {natal_chart.chart.date}")
print(f"Lagna (Ascendant): {natal_chart.chart.getObject(const.ASC).sign}")
print(f"Moon Sign: {natal_chart.chart.getObject(const.MOON).sign}")
print(f"Sun Sign: {natal_chart.chart.getObject(const.SUN).sign}")
print()

print("Transit Date:")
print(f"{transit_date}")
print()

# Analyze transits in detail
transit_analysis = natal_chart.analyze_transits(transit_date)
print("Detailed Transit Analysis:")
print(f"Transit Quality: {transit_analysis['transit_quality']}")
print()

print("Transit Planet Positions:")
for planet_id, planet_info in transit_analysis['transit_planets'].items():
    print(f"{planet_id}: {planet_info['sign']} (House {planet_info['house']})")
print()

print("Transit Aspects:")
for aspect in transit_analysis['transit_aspects'][:5]:  # Print first 5 aspects
    print(f"{aspect['transit_planet']} aspects {aspect['natal_planet']} ({aspect['aspect_type']})")
print()

print("Gochara (Transit) Effects:")
for planet_id, effect in transit_analysis['gochara_effects'].items():
    print(f"{planet_id}: {effect['effect']} ({effect['quality']})")
print()

print("Vedha Effects:")
for planet_id, effect in transit_analysis['vedha_effects'].items():
    print(f"{planet_id}: {effect['effect']} ({effect['quality']})")
print()

print("Argala Effects:")
for planet_id, effect in transit_analysis['argala_effects'].items():
    print(f"{planet_id}: {effect['effect']} ({effect['quality']})")
print()

print("Ashtakavarga Transit Analysis:")
for planet_id, analysis in transit_analysis['ashtakavarga_analysis'].items():
    print(f"{planet_id}: {analysis['bindus']} bindus ({analysis['quality']})")
print()

print("Dasha Transit Effects:")
dasha_effects = transit_analysis['dasha_effects']
print(f"Dasha Lord: {dasha_effects['dasha_lord']}")
print(f"Transit Effect: {dasha_effects['effect']} ({dasha_effects['quality']})")
print()

print("Antardasha Transit Effects:")
antardasha_effects = transit_analysis['antardasha_effects']
print(f"Antardasha Lord: {antardasha_effects['antardasha_lord']}")
print(f"Transit Effect: {antardasha_effects['effect']} ({antardasha_effects['quality']})")
print()

# Get detailed transit predictions
start_date = transit_date
end_date = Datetime(
    (datetime.strptime(start_date.date, '%Y/%m/%d') + timedelta(days=90)).strftime('%Y/%m/%d'),
    '23:59',
    start_date.timezone
)

transit_predictions = natal_chart.get_transit_predictions(start_date, end_date)
print("Detailed Transit Predictions:")
print()

print("General Predictions:")
for prediction in transit_predictions['general']:
    print(f"- {prediction}")
print()

print("Planet Predictions:")
for planet_id, predictions in transit_predictions['planets'].items():
    print(f"{planet_id}:")
    for prediction in predictions:
        print(f"- {prediction}")
    print()

print("House Predictions:")
for house_num, predictions in transit_predictions['houses'].items():
    print(f"House {house_num}:")
    for prediction in predictions:
        print(f"- {prediction}")
    print()

print("Transit Timeline:")
for event in transit_predictions['timeline']['events'][:10]:  # Print first 10 events
    print(f"- {event['date']}: {event['description']}")
print()

print("Favorable Periods:")
for period in transit_predictions['periods']['favorable_periods'][:5]:  # Print first 5 favorable periods
    print(f"- {period['start_date']} to {period['end_date']}: {period['description']}")
print()

print("Challenging Periods:")
for period in transit_predictions['periods']['challenging_periods'][:5]:  # Print first 5 challenging periods
    print(f"- {period['start_date']} to {period['end_date']}: {period['description']}")
print()

# Get transit compatibility
transit_compatibility = natal_chart.get_transit_compatibility(transit_date)
print("Transit Compatibility:")
print(f"Overall Score: {transit_compatibility['overall_score']}/100")
print()

print("Gochara Strength:")
for planet_id, strength in transit_compatibility['gochara_strength']['planet_scores'].items():
    print(f"{planet_id}: {strength}/10")
print()

print("Ashtakavarga Strength:")
for planet_id, strength in transit_compatibility['ashtakavarga_strength']['planet_scores'].items():
    print(f"{planet_id}: {strength}/10")
print()

print("Dasha Compatibility:")
dasha_compatibility = transit_compatibility['dasha_compatibility']
print(f"Dasha Lord: {dasha_compatibility['dasha_lord']}")
print(f"Transit Planet: {dasha_compatibility['transit_planet']}")
print(f"Compatibility: {dasha_compatibility['compatibility']} ({dasha_compatibility['score']}/10)")
print()

# Get transit strength score
transit_strength = natal_chart.get_transit_strength_score(transit_date)
print("Transit Strength Score:")
print(f"Overall Score: {transit_strength['overall_score']}/100")
print()

# Print a summary
print("Transit Summary:")
print(f"Overall Transit Quality: {transit_analysis['transit_quality']}")
print(f"Overall Transit Strength: {transit_strength['overall_score']}/100")
print(f"Overall Transit Compatibility: {transit_compatibility['overall_score']}/100")
print()

if transit_strength['overall_score'] >= 70:
    print("This is a highly favorable transit period.")
elif transit_strength['overall_score'] >= 50:
    print("This is a moderately favorable transit period.")
elif transit_strength['overall_score'] >= 30:
    print("This is a mixed transit period with both opportunities and challenges.")
else:
    print("This is a challenging transit period. Exercise caution and patience.")
