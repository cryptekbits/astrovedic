"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements transit-based predictions
    for Vedic astrology.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic import angle
from datetime import timedelta

# Import core functions
from astrovedic.vedic.transits.core import (
    get_transit_chart, get_transit_planets,
    get_transit_aspects, get_transit_houses,
    get_transit_quality
)

# Import Gochara functions
from astrovedic.vedic.transits.gochara import (
    get_gochara_effects, get_planet_gochara
)

# Import Ashtakavarga functions
from astrovedic.vedic.transits.ashtakavarga import (
    get_transit_ashtakavarga, get_transit_bindus
)

# Import Dasha functions
from astrovedic.vedic.transits.dashas import (
    get_transit_dasha_effects, get_dasha_transit_compatibility
)


def get_transit_effects(natal_chart, transits):
    """
    Get transit effects data

    Args:
        natal_chart (Chart): The natal chart
        transits (dict): The transit information

    Returns:
        dict: Dictionary with transit effects data
    """
    # Initialize the effects data
    effects = {
        'transit_quality': transits['transit_quality'],
        'planets': {},
        'houses': {},
        'dashas': {}
    }

    # Compile planet-specific effects
    for planet_id in const.LIST_OBJECTS_VEDIC:
        # Get the transit planet information
        transit_planet = transits['transit_planets'][planet_id]

        # Get the Gochara effects
        gochara_effect = transits['gochara_effects'][planet_id]

        # Get the Ashtakavarga transit
        ashtakavarga_transit = transits['transit_ashtakavarga'][planet_id]

        # Compile the planet effects data
        effects['planets'][planet_id] = {
            'planet': planet_id,
            'sign': transit_planet['transit_sign'],
            'house': transit_planet['house'],
            'is_retrograde': transit_planet['is_retrograde'],
            'gochara_effect': gochara_effect['effect'],
            'ashtakavarga_strength': ashtakavarga_transit['strength']['strength']
        }

    # Compile house-specific effects
    for house_num in range(1, 13):
        # Get the transit house information
        transit_house = transits['transit_houses'][house_num]

        # Compile the house effects data
        effects['houses'][house_num] = {
            'house': house_num,
            'sign': transit_house['sign'],
            'planets': transit_house['planets']
        }

    # Compile Dasha-related effects
    effects['dashas'] = {
        'dasha_effects': transits['transit_dasha_effects'],
        'dasha_compatibility': get_dasha_transit_compatibility(natal_chart, transits['transit_chart'])
    }

    return effects


def get_transit_timeline(natal_chart, start_date, end_date):
    """
    Generate a timeline of transit events for a specific period

    Args:
        natal_chart (Chart): The natal chart
        start_date (Datetime): The start date
        end_date (Datetime): The end date

    Returns:
        list: List of transit events
    """
    # Initialize the timeline
    timeline = []

    # Calculate the number of days in the period
    days = (end_date.datetime() - start_date.datetime()).days

    # Check each day in the period
    for day in range(days + 1):
        # Calculate the current date
        current_date = start_date.datetime() + timedelta(days=day)
        current_datetime = Datetime.fromDatetime(current_date)

        # Create a transit chart for the current date
        transit_chart = get_transit_chart(natal_chart, current_datetime)

        # Get the transit aspects
        transit_aspects = get_transit_aspects(natal_chart, transit_chart)

        # Check for exact aspects (orb < 1 degree)
        for aspect in transit_aspects:
            if aspect['orb'] < 1:
                # Add the aspect to the timeline
                timeline.append({
                    'date': current_datetime,
                    'type': 'aspect',
                    'transit_planet': aspect['transit_planet'],
                    'natal_planet': aspect['natal_planet'],
                    'aspect': aspect['aspect'],
                    'description': f"Transit {aspect['transit_planet']} {aspect['aspect'].lower()} natal {aspect['natal_planet']}"
                })

        # Check for sign changes
        if day > 0:
            # Get the previous date
            previous_date = start_date.datetime() + timedelta(days=day-1)
            previous_datetime = Datetime.fromDatetime(previous_date)

            # Create a transit chart for the previous date
            previous_transit_chart = get_transit_chart(natal_chart, previous_datetime)

            # Check each planet
            for planet_id in const.LIST_OBJECTS_VEDIC:
                # Get the current and previous transit planets
                current_transit_planet = transit_chart.getObject(planet_id)
                previous_transit_planet = previous_transit_chart.getObject(planet_id)

                # Check if the sign has changed
                if current_transit_planet.sign != previous_transit_planet.sign:
                    # Add the sign change to the timeline
                    timeline.append({
                        'date': current_datetime,
                        'type': 'sign_change',
                        'planet': planet_id,
                        'from_sign': previous_transit_planet.sign,
                        'to_sign': current_transit_planet.sign,
                        'description': f"Transit {planet_id} moves from {previous_transit_planet.sign} to {current_transit_planet.sign}"
                    })

        # Check for retrograde stations
        if day > 0:
            # Get the previous date
            previous_date = start_date.datetime() + timedelta(days=day-1)
            previous_datetime = Datetime.fromDatetime(previous_date)

            # Create a transit chart for the previous date
            previous_transit_chart = get_transit_chart(natal_chart, previous_datetime)

            # Check each planet
            for planet_id in [const.MERCURY, const.VENUS, const.MARS, const.JUPITER, const.SATURN]:
                # Get the current and previous transit planets
                current_transit_planet = transit_chart.getObject(planet_id)
                previous_transit_planet = previous_transit_chart.getObject(planet_id)

                # Check if the retrograde status has changed
                if current_transit_planet.isRetrograde() != previous_transit_planet.isRetrograde():
                    # Add the retrograde station to the timeline
                    if current_transit_planet.isRetrograde():
                        timeline.append({
                            'date': current_datetime,
                            'type': 'retrograde_station',
                            'planet': planet_id,
                            'status': 'retrograde',
                            'description': f"Transit {planet_id} stations retrograde at {current_transit_planet.sign} {current_transit_planet.signlon:.2f}°"
                        })
                    else:
                        timeline.append({
                            'date': current_datetime,
                            'type': 'direct_station',
                            'planet': planet_id,
                            'status': 'direct',
                            'description': f"Transit {planet_id} stations direct at {current_transit_planet.sign} {current_transit_planet.signlon:.2f}°"
                        })

    # Sort the timeline by date
    timeline.sort(key=lambda x: x['date'].datetime())

    return timeline


def get_transit_events(natal_chart, start_date, end_date):
    """
    Get significant transit events for a specific period

    Args:
        natal_chart (Chart): The natal chart
        start_date (Datetime): The start date
        end_date (Datetime): The end date

    Returns:
        list: List of significant transit events
    """
    # Get the transit timeline
    timeline = get_transit_timeline(natal_chart, start_date, end_date)

    # Filter for significant events
    significant_events = []

    for event in timeline:
        # Check if the event is significant
        is_significant = False

        if event['type'] == 'aspect':
            # Conjunctions, oppositions, and squares to Sun, Moon, Ascendant, or chart ruler are significant
            if event['aspect'] in ['Conjunction', 'Opposition', 'Square'] and \
               event['natal_planet'] in [const.SUN, const.MOON, const.ASC]:
                is_significant = True

            # Any aspect from Jupiter or Saturn is significant
            if event['transit_planet'] in [const.JUPITER, const.SATURN]:
                is_significant = True

        elif event['type'] in ['sign_change', 'retrograde_station', 'direct_station']:
            # All sign changes and stations are significant
            is_significant = True

        # Add significant events to the result
        if is_significant:
            significant_events.append(event)

    return significant_events


def get_transit_periods(natal_chart, start_date, end_date):
    """
    Get transit periods with similar qualities

    Args:
        natal_chart (Chart): The natal chart
        start_date (Datetime): The start date
        end_date (Datetime): The end date

    Returns:
        list: List of transit periods
    """
    # Initialize the periods
    periods = []

    # Get the transit events
    events = get_transit_events(natal_chart, start_date, end_date)

    # If there are no events, return a single period
    if not events:
        # Create a transit chart for the start date
        transit_chart = get_transit_chart(natal_chart, start_date)

        # Get the transit quality
        transit_quality = get_transit_quality(natal_chart, transit_chart)

        # Add the period
        periods.append({
            'start_date': start_date,
            'end_date': end_date,
            'quality': transit_quality['quality'],
            'description': f"Transit period from {start_date} to {end_date}: {transit_quality['quality']}"
        })

        return periods

    # Add the start date as the first event
    events.insert(0, {
        'date': start_date,
        'type': 'period_start',
        'description': 'Start of transit period'
    })

    # Add the end date as the last event
    events.append({
        'date': end_date,
        'type': 'period_end',
        'description': 'End of transit period'
    })

    # Create periods between events
    for i in range(len(events) - 1):
        # Get the current and next events
        current_event = events[i]
        next_event = events[i + 1]

        # Create a transit chart for the middle of the period
        mid_date = current_event['date'].datetime() + (next_event['date'].datetime() - current_event['date'].datetime()) / 2
        mid_datetime = Datetime.fromDatetime(mid_date)

        transit_chart = get_transit_chart(natal_chart, mid_datetime)

        # Get the transit quality
        transit_quality = get_transit_quality(natal_chart, transit_chart)

        # Add the period
        periods.append({
            'start_date': current_event['date'],
            'end_date': next_event['date'],
            'quality': transit_quality['quality'],
            'description': f"Transit period from {current_event['date']} to {next_event['date']}: {transit_quality['quality']}"
        })

    return periods









