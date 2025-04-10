"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements transit-based predictions
    for Vedic astrology.
"""

from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import angle
from datetime import timedelta

# Import core functions
from flatlib.vedic.transits.core import (
    get_transit_chart, get_transit_planets,
    get_transit_aspects, get_transit_houses,
    get_transit_quality
)

# Import Gochara functions
from flatlib.vedic.transits.gochara import (
    get_gochara_effects, get_planet_gochara
)

# Import Ashtakavarga functions
from flatlib.vedic.transits.ashtakavarga import (
    get_transit_ashtakavarga, get_transit_bindus
)

# Import Dasha functions
from flatlib.vedic.transits.dashas import (
    get_transit_dasha_effects, get_dasha_transit_compatibility
)


def get_transit_predictions(natal_chart, transits):
    """
    Generate predictions based on transits
    
    Args:
        natal_chart (Chart): The natal chart
        transits (dict): The transit information
    
    Returns:
        dict: Dictionary with transit predictions
    """
    # Initialize the predictions
    predictions = {
        'general': [],
        'planets': {},
        'houses': {},
        'dashas': []
    }
    
    # Generate general predictions
    transit_quality = transits['transit_quality']
    
    if transit_quality['quality'] == 'Excellent':
        predictions['general'].append("This is an excellent transit period. The planetary influences are highly favorable for most activities.")
    elif transit_quality['quality'] == 'Good':
        predictions['general'].append("This is a good transit period. The planetary influences are generally favorable for most activities.")
    elif transit_quality['quality'] == 'Neutral':
        predictions['general'].append("This is a neutral transit period. The planetary influences are mixed, with both favorable and challenging aspects.")
    elif transit_quality['quality'] == 'Challenging':
        predictions['general'].append("This is a challenging transit period. The planetary influences may bring obstacles and difficulties.")
    elif transit_quality['quality'] == 'Difficult':
        predictions['general'].append("This is a difficult transit period. The planetary influences are likely to bring significant challenges and obstacles.")
    
    # Add the main factors
    for factor in transit_quality['factors'][:3]:
        predictions['general'].append(factor)
    
    # Generate planet-specific predictions
    for planet_id in const.LIST_OBJECTS_VEDIC:
        # Get the transit planet information
        transit_planet = transits['transit_planets'][planet_id]
        
        # Get the Gochara effects
        gochara_effect = transits['gochara_effects'][planet_id]
        
        # Get the Ashtakavarga transit
        ashtakavarga_transit = transits['transit_ashtakavarga'][planet_id]
        
        # Generate the prediction
        planet_prediction = generate_planet_prediction(planet_id, transit_planet, gochara_effect, ashtakavarga_transit)
        
        # Add to the predictions
        predictions['planets'][planet_id] = planet_prediction
    
    # Generate house-specific predictions
    for house_num in range(1, 13):
        # Get the transit house information
        transit_house = transits['transit_houses'][house_num]
        
        # Generate the prediction
        house_prediction = generate_house_prediction(house_num, transit_house)
        
        # Add to the predictions
        predictions['houses'][house_num] = house_prediction
    
    # Generate Dasha-related predictions
    dasha_effects = transits['transit_dasha_effects']
    
    # Get the Dasha compatibility
    dasha_compatibility = get_dasha_transit_compatibility(natal_chart, transits['transit_chart'])
    
    # Generate the Dasha prediction
    dasha_prediction = generate_dasha_prediction(dasha_effects, dasha_compatibility)
    
    # Add to the predictions
    predictions['dashas'] = dasha_prediction
    
    return predictions


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


def generate_planet_prediction(planet_id, transit_planet, gochara_effect, ashtakavarga_transit):
    """
    Generate a prediction for a transit planet
    
    Args:
        planet_id (str): The ID of the planet
        transit_planet (dict): The transit planet information
        gochara_effect (dict): The Gochara effect information
        ashtakavarga_transit (dict): The Ashtakavarga transit information
    
    Returns:
        dict: Dictionary with planet prediction
    """
    # Initialize the prediction
    prediction = {
        'planet': planet_id,
        'sign': transit_planet['transit_sign'],
        'house': transit_planet['house'],
        'is_retrograde': transit_planet['is_retrograde'],
        'gochara_effect': gochara_effect['effect'],
        'ashtakavarga_strength': ashtakavarga_transit['strength']['strength'],
        'description': []
    }
    
    # Generate the description
    
    # Basic transit information
    prediction['description'].append(f"Transit {planet_id} is in {transit_planet['transit_sign']} in the {transit_planet['house']}th house.")
    
    # Retrograde status
    if transit_planet['is_retrograde']:
        prediction['description'].append(f"{planet_id} is retrograde, indicating a period of reflection and internalization.")
    
    # Gochara effect
    prediction['description'].append(f"From the Moon, {planet_id} is in the {gochara_effect['moon_house']}th house, which is {gochara_effect['effect']['effect'].lower()}. {gochara_effect['effect']['description']}.")
    
    # Ashtakavarga strength
    prediction['description'].append(f"The Ashtakavarga strength is {ashtakavarga_transit['strength']['strength'].lower()} with {ashtakavarga_transit['bindus']} bindus. {ashtakavarga_transit['strength']['description']}.")
    
    # Overall effect
    if gochara_effect['strength']['strength'] == 'Strong Favorable' and ashtakavarga_transit['strength']['strength'] in ['Excellent', 'Good']:
        prediction['description'].append(f"Overall, transit {planet_id} is highly favorable during this period.")
    elif gochara_effect['strength']['strength'] in ['Strong Favorable', 'Moderate Favorable'] and ashtakavarga_transit['strength']['strength'] in ['Excellent', 'Good', 'Neutral']:
        prediction['description'].append(f"Overall, transit {planet_id} is favorable during this period.")
    elif gochara_effect['strength']['strength'] == 'Neutral' and ashtakavarga_transit['strength']['strength'] == 'Neutral':
        prediction['description'].append(f"Overall, transit {planet_id} has a mixed influence during this period.")
    elif gochara_effect['strength']['strength'] in ['Moderate Unfavorable', 'Strong Unfavorable'] or ashtakavarga_transit['strength']['strength'] in ['Challenging', 'Difficult']:
        prediction['description'].append(f"Overall, transit {planet_id} may bring challenges during this period.")
    
    return prediction


def generate_house_prediction(house_num, transit_house):
    """
    Generate a prediction for a transit house
    
    Args:
        house_num (int): The house number
        transit_house (dict): The transit house information
    
    Returns:
        dict: Dictionary with house prediction
    """
    # Initialize the prediction
    prediction = {
        'house': house_num,
        'sign': transit_house['sign'],
        'planets': transit_house['planets'],
        'description': []
    }
    
    # Generate the description
    
    # Basic house information
    prediction['description'].append(f"The {house_num}th house is in {transit_house['sign']}.")
    
    # Planets in the house
    if transit_house['planets']:
        planets_str = ', '.join(transit_house['planets'])
        prediction['description'].append(f"Transit planets in this house: {planets_str}.")
        
        # House-specific predictions
        house_meanings = {
            1: "focus on self, identity, physical appearance, and new beginnings",
            2: "financial matters, possessions, values, and self-worth",
            3: "communication, short journeys, siblings, and learning",
            4: "home, family, emotional foundation, and real estate",
            5: "creativity, romance, children, and pleasure",
            6: "health, work, service, and daily routines",
            7: "partnerships, marriage, contracts, and open enemies",
            8: "transformation, shared resources, sexuality, and occult matters",
            9: "higher education, philosophy, travel, and spirituality",
            10: "career, public image, authority, and achievements",
            11: "friends, groups, hopes, and wishes",
            12: "spirituality, isolation, hidden matters, and self-undoing"
        }
        
        # Add house-specific prediction
        if house_num in house_meanings:
            prediction['description'].append(f"This indicates a focus on {house_meanings[house_num]} during this transit period.")
        
        # Check for benefic and malefic planets
        benefics = [planet for planet in transit_house['planets'] if planet in [const.MOON, const.MERCURY, const.JUPITER, const.VENUS]]
        malefics = [planet for planet in transit_house['planets'] if planet in [const.SUN, const.MARS, const.SATURN, const.RAHU, const.KETU]]
        
        if benefics and not malefics:
            prediction['description'].append(f"The presence of benefic planets ({', '.join(benefics)}) suggests favorable developments in these areas.")
        elif malefics and not benefics:
            prediction['description'].append(f"The presence of malefic planets ({', '.join(malefics)}) suggests challenges or transformations in these areas.")
        elif benefics and malefics:
            prediction['description'].append(f"The mix of benefic ({', '.join(benefics)}) and malefic ({', '.join(malefics)}) planets suggests both opportunities and challenges in these areas.")
    else:
        prediction['description'].append("No transit planets are currently in this house.")
    
    return prediction


def generate_dasha_prediction(dasha_effects, dasha_compatibility):
    """
    Generate a prediction for Dasha-transit interactions
    
    Args:
        dasha_effects (dict): The Dasha effects information
        dasha_compatibility (dict): The Dasha-transit compatibility information
    
    Returns:
        list: List of Dasha predictions
    """
    # Initialize the predictions
    predictions = []
    
    # Add the Dasha information
    predictions.append(f"Current Dasha: {dasha_effects['dasha_lord']} Maha Dasha")
    predictions.append(f"Current Antardasha: {dasha_effects['antardasha_lord']} Antardasha")
    predictions.append(f"Current Pratyantardasha: {dasha_effects['pratyantardasha_lord']} Pratyantardasha")
    
    # Add the compatibility information
    predictions.append(f"Dasha-Transit Compatibility: {dasha_compatibility['compatibility']}")
    predictions.append(dasha_compatibility['description'])
    
    # Add the main factors
    for factor in dasha_compatibility['factors'][:3]:
        predictions.append(factor)
    
    return predictions
