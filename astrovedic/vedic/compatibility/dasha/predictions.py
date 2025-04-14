"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Dasha-based predictions for compatibility
    in Vedic astrology.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from datetime import timedelta

from astrovedic.vedic.compatibility.dasha.helpers import (
    get_dasha, get_antardasha, get_dasha_lord, get_antardasha_lord
)

# Helper functions for dasha start and end dates
def get_dasha_start(chart, date):
    """Get the start date of the current Dasha"""
    return date  # Placeholder implementation

def get_dasha_end(chart, date):
    """Get the end date of the current Dasha"""
    return date  # Placeholder implementation

def get_antardasha_start(chart, date):
    """Get the start date of the current Antardasha"""
    return date  # Placeholder implementation

def get_antardasha_end(chart, date):
    """Get the end date of the current Antardasha"""
    return date  # Placeholder implementation

from astrovedic.vedic.compatibility.dasha.compatibility import (
    calculate_planet_compatibility
)


def get_dasha_predictions(chart1, chart2):
    """
    Get Dasha-based predictions for the compatibility between two charts

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with Dasha-based predictions
    """
    # Get the current date
    from datetime import datetime
    current_date = Datetime.fromDatetime(datetime.now())

    # Get the current Dasha and Antardasha for each chart
    dasha1 = get_dasha(chart1, current_date)
    dasha2 = get_dasha(chart2, current_date)
    antardasha1 = get_antardasha(chart1, current_date)
    antardasha2 = get_antardasha(chart2, current_date)

    # Get the Dasha and Antardasha lords
    dasha_lord1 = get_dasha_lord(dasha1)
    dasha_lord2 = get_dasha_lord(dasha2)
    antardasha_lord1 = get_antardasha_lord(antardasha1)
    antardasha_lord2 = get_antardasha_lord(antardasha2)

    # Get the Dasha and Antardasha periods
    dasha_start1 = get_dasha_start(chart1, current_date)
    dasha_end1 = get_dasha_end(chart1, current_date)
    dasha_start2 = get_dasha_start(chart2, current_date)
    dasha_end2 = get_dasha_end(chart2, current_date)
    antardasha_start1 = get_antardasha_start(chart1, current_date)
    antardasha_end1 = get_antardasha_end(chart1, current_date)
    antardasha_start2 = get_antardasha_start(chart2, current_date)
    antardasha_end2 = get_antardasha_end(chart2, current_date)

    # Calculate the compatibility between the Dasha lords
    dasha_compatibility = calculate_planet_compatibility(dasha_lord1, dasha_lord2)

    # Calculate the compatibility between the Antardasha lords
    antardasha_compatibility = calculate_planet_compatibility(antardasha_lord1, antardasha_lord2)

    # Generate the current period prediction
    current_period_prediction = generate_current_period_prediction(
        dasha_lord1, dasha_lord2, antardasha_lord1, antardasha_lord2,
        dasha_compatibility, antardasha_compatibility
    )

    # Generate the upcoming periods prediction
    upcoming_periods_prediction = generate_upcoming_periods_prediction(
        chart1, chart2, current_date,
        dasha_end1, dasha_end2, antardasha_end1, antardasha_end2
    )

    # Generate the favorable periods prediction
    favorable_periods_prediction = generate_favorable_periods_prediction(
        chart1, chart2, current_date
    )

    # Generate the challenging periods prediction
    challenging_periods_prediction = generate_challenging_periods_prediction(
        chart1, chart2, current_date
    )

    # Combine all predictions into a single dictionary
    predictions = {
        'current_period': current_period_prediction,
        'upcoming_periods': upcoming_periods_prediction,
        'favorable_periods': favorable_periods_prediction,
        'challenging_periods': challenging_periods_prediction
    }

    # Create a timeline of events for the next 2 years
    timeline = []

    # Calculate JD values for future dates
    current_jd = current_date.jd
    one_year_later_jd = current_jd + 365.25/365.25  # Adding 1 year in JD units
    two_years_later_jd = current_jd + 2 * 365.25/365.25  # Adding 2 years in JD units

    # Add current period to timeline
    timeline.append({
        'date': current_date.date.date(),
        'event': f"Current period: {dasha_lord1} Dasha / {antardasha_lord1} Antardasha for Person 1, {dasha_lord2} Dasha / {antardasha_lord2} Antardasha for Person 2",
        'type': 'current'
    })

    # Add upcoming period changes to timeline
    if antardasha_end1 and antardasha_end1.jd < one_year_later_jd:
        timeline.append({
            'date': antardasha_end1.date.date(),
            'event': f"Person 1 enters new Antardasha",
            'type': 'antardasha_change'
        })

    if antardasha_end2 and antardasha_end2.jd < one_year_later_jd:
        timeline.append({
            'date': antardasha_end2.date.date(),
            'event': f"Person 2 enters new Antardasha",
            'type': 'antardasha_change'
        })

    if dasha_end1 and dasha_end1.jd < two_years_later_jd:
        timeline.append({
            'date': dasha_end1.date.date(),
            'event': f"Person 1 enters new Dasha",
            'type': 'dasha_change'
        })

    if dasha_end2 and dasha_end2.jd < two_years_later_jd:
        timeline.append({
            'date': dasha_end2.date.date(),
            'event': f"Person 2 enters new Dasha",
            'type': 'dasha_change'
        })

    # Create a summary description
    description = f"Person 1 is currently in {dasha_lord1} Dasha and {antardasha_lord1} Antardasha. "
    description += f"Person 2 is currently in {dasha_lord2} Dasha and {antardasha_lord2} Antardasha. "

    if dasha_compatibility['score'] >= 7:
        description += "The Dasha lords are highly compatible, creating a harmonious period. "
    elif dasha_compatibility['score'] <= 3:
        description += "The Dasha lords have poor compatibility, creating challenges. "
    else:
        description += "The Dasha lords have moderate compatibility. "

    if antardasha_compatibility['score'] >= 7:
        description += "The Antardasha lords are highly compatible, enhancing the relationship. "
    elif antardasha_compatibility['score'] <= 3:
        description += "The Antardasha lords have poor compatibility, adding stress. "
    else:
        description += "The Antardasha lords have moderate compatibility. "

    # Check if there are favorable periods in the timeline
    has_favorable_periods = False
    has_challenging_periods = False

    # Check the timeline for favorable and challenging periods
    for event in timeline:
        if 'type' in event and event['type'] in ['dasha_change', 'antardasha_change']:
            # Consider period changes as potentially favorable or challenging
            if dasha_compatibility['score'] >= 7 or antardasha_compatibility['score'] >= 7:
                has_favorable_periods = True
            if dasha_compatibility['score'] <= 3 or antardasha_compatibility['score'] <= 3:
                has_challenging_periods = True

    if has_favorable_periods:
        description += "There are favorable periods ahead that will strengthen the relationship. "
    else:
        description += "No highly favorable periods were identified in the near future. "

    if has_challenging_periods:
        description += "There are challenging periods ahead that will require patience and understanding."
    else:
        description += "No highly challenging periods were identified in the near future."

    return {
        'current_period_prediction': current_period_prediction,
        'upcoming_periods_prediction': upcoming_periods_prediction,
        'favorable_periods_prediction': favorable_periods_prediction,
        'challenging_periods_prediction': challenging_periods_prediction,
        'predictions': predictions,
        'timeline': timeline,
        'description': description
    }


def generate_current_period_prediction(
    dasha_lord1, dasha_lord2, antardasha_lord1, antardasha_lord2,
    dasha_compatibility, antardasha_compatibility
):
    """
    Generate a prediction for the current Dasha period

    Args:
        dasha_lord1 (str): The Dasha lord of the first person
        dasha_lord2 (str): The Dasha lord of the second person
        antardasha_lord1 (str): The Antardasha lord of the first person
        antardasha_lord2 (str): The Antardasha lord of the second person
        dasha_compatibility (dict): The Dasha compatibility information
        antardasha_compatibility (dict): The Antardasha compatibility information

    Returns:
        str: The current period prediction
    """
    # Define the planet qualities
    planet_qualities = {
        const.SUN: {
            'positive': 'leadership, authority, and vitality',
            'negative': 'ego, domination, and pride'
        },
        const.MOON: {
            'positive': 'emotions, nurturing, and adaptability',
            'negative': 'moodiness, dependency, and insecurity'
        },
        const.MARS: {
            'positive': 'energy, courage, and assertiveness',
            'negative': 'aggression, impatience, and anger'
        },
        const.MERCURY: {
            'positive': 'communication, intellect, and adaptability',
            'negative': 'nervousness, overthinking, and indecision'
        },
        const.JUPITER: {
            'positive': 'wisdom, expansion, and optimism',
            'negative': 'excess, overindulgence, and overconfidence'
        },
        const.VENUS: {
            'positive': 'love, harmony, and pleasure',
            'negative': 'indulgence, vanity, and attachment'
        },
        const.SATURN: {
            'positive': 'discipline, responsibility, and endurance',
            'negative': 'restriction, delay, and pessimism'
        },
        const.RAHU: {
            'positive': 'ambition, innovation, and worldly success',
            'negative': 'obsession, confusion, and illusion'
        },
        const.KETU: {
            'positive': 'spirituality, detachment, and liberation',
            'negative': 'isolation, confusion, and escapism'
        }
    }

    # Get the qualities
    positive1 = planet_qualities.get(dasha_lord1, {}).get('positive', 'unknown qualities')
    negative1 = planet_qualities.get(dasha_lord1, {}).get('negative', 'unknown qualities')
    positive2 = planet_qualities.get(dasha_lord2, {}).get('positive', 'unknown qualities')
    negative2 = planet_qualities.get(dasha_lord2, {}).get('negative', 'unknown qualities')

    # Generate the prediction
    prediction = f"Person 1 is currently in {dasha_lord1} Dasha and {antardasha_lord1} Antardasha, experiencing {positive1} but potentially also {negative1}. "
    prediction += f"Person 2 is in {dasha_lord2} Dasha and {antardasha_lord2} Antardasha, experiencing {positive2} but potentially also {negative2}. "

    # Add compatibility assessment
    if dasha_compatibility['friendship'] == 'Friend' and antardasha_compatibility['friendship'] == 'Friend':
        prediction += "Both the main periods and sub-periods are highly compatible, creating a harmonious and supportive relationship during this time. "
        prediction += "This is an excellent period for deepening the relationship and working together on shared goals."
    elif dasha_compatibility['friendship'] == 'Friend' and antardasha_compatibility['friendship'] == 'Neutral':
        prediction += "The main periods are highly compatible, but the sub-periods are moderately compatible, creating a generally positive relationship with occasional indifference. "
        prediction += "This is a good period for the relationship, but minor adjustments may be needed in day-to-day interactions."
    elif dasha_compatibility['friendship'] == 'Friend' and antardasha_compatibility['friendship'] == 'Enemy':
        prediction += "The main periods are highly compatible, but the sub-periods are challenging, creating a mixed relationship with both harmony and conflict. "
        prediction += "The long-term outlook is positive, but short-term challenges need to be addressed with patience and understanding."
    elif dasha_compatibility['friendship'] == 'Neutral' and antardasha_compatibility['friendship'] == 'Friend':
        prediction += "The main periods are moderately compatible, but the sub-periods are highly compatible, creating a relationship that improves in day-to-day interactions. "
        prediction += "This is a period of growing harmony, especially in immediate experiences and interactions."
    elif dasha_compatibility['friendship'] == 'Neutral' and antardasha_compatibility['friendship'] == 'Neutral':
        prediction += "Both the main periods and sub-periods are moderately compatible, creating a balanced but sometimes indifferent relationship. "
        prediction += "This is a period of stability, but effort is needed to maintain excitement and engagement in the relationship."
    elif dasha_compatibility['friendship'] == 'Neutral' and antardasha_compatibility['friendship'] == 'Enemy':
        prediction += "The main periods are moderately compatible, but the sub-periods are challenging, creating a relationship with underlying stability but frequent conflicts. "
        prediction += "This is a period that requires patience and compromise, especially in day-to-day interactions."
    elif dasha_compatibility['friendship'] == 'Enemy' and antardasha_compatibility['friendship'] == 'Friend':
        prediction += "The main periods are challenging, but the sub-periods are highly compatible, creating a relationship with long-term challenges but immediate harmony. "
        prediction += "This is a period where day-to-day interactions may be pleasant, but underlying issues need to be addressed for long-term success."
    elif dasha_compatibility['friendship'] == 'Enemy' and antardasha_compatibility['friendship'] == 'Neutral':
        prediction += "The main periods are challenging, and the sub-periods are moderately compatible, creating a relationship with significant obstacles and occasional indifference. "
        prediction += "This is a period that requires substantial effort and understanding to navigate successfully."
    else:  # Both Enemy
        prediction += "Both the main periods and sub-periods are challenging, creating a relationship with significant conflicts and misunderstandings. "
        prediction += "This is a difficult period that requires exceptional patience, communication, and compromise."

    return prediction


def generate_upcoming_periods_prediction(
    chart1, chart2, current_date,
    dasha_end1, dasha_end2, antardasha_end1, antardasha_end2
):
    """
    Generate a prediction for upcoming Dasha periods

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart
        current_date (Datetime): The current date
        dasha_end1 (Datetime): The end date of the current Dasha for the first person
        dasha_end2 (Datetime): The end date of the current Dasha for the second person
        antardasha_end1 (Datetime): The end date of the current Antardasha for the first person
        antardasha_end2 (Datetime): The end date of the current Antardasha for the second person

    Returns:
        str: The upcoming periods prediction
    """
    # Initialize the prediction
    prediction = "Upcoming period changes: "

    # Import datetime for comparison
    from datetime import datetime, timedelta

    # Convert to Python datetime objects for comparison
    # Since Datetime doesn't have a datetime() method, we'll use the jd property
    # and create a simple comparison based on JD values
    current_jd = current_date.jd
    one_year_later_jd = current_jd + 365.25/365.25  # Adding 1 year in JD units

    # Check for upcoming Antardasha changes
    if antardasha_end1 and antardasha_end1.jd < one_year_later_jd:
        next_antardasha_date = antardasha_end1
        next_antardasha = get_antardasha(chart1, next_antardasha_date)
        next_antardasha_lord = get_antardasha_lord(next_antardasha)

        prediction += f"Person 1 will enter {next_antardasha_lord} Antardasha on {next_antardasha_date}. "

    if antardasha_end2 and antardasha_end2.jd < one_year_later_jd:
        next_antardasha_date = antardasha_end2
        next_antardasha = get_antardasha(chart2, next_antardasha_date)
        next_antardasha_lord = get_antardasha_lord(next_antardasha)

        prediction += f"Person 2 will enter {next_antardasha_lord} Antardasha on {next_antardasha_date}. "

    # Check for upcoming Dasha changes
    # Calculate JD for 2 years later
    two_years_later_jd = current_jd + 2 * 365.25/365.25  # Adding 2 years in JD units

    if dasha_end1 and dasha_end1.jd < two_years_later_jd:
        next_dasha_date = dasha_end1
        next_dasha = get_dasha(chart1, next_dasha_date)
        next_dasha_lord = get_dasha_lord(next_dasha)

        prediction += f"Person 1 will enter {next_dasha_lord} Dasha on {next_dasha_date}. "

    if dasha_end2 and dasha_end2.jd < two_years_later_jd:
        next_dasha_date = dasha_end2
        next_dasha = get_dasha(chart2, next_dasha_date)
        next_dasha_lord = get_dasha_lord(next_dasha)

        prediction += f"Person 2 will enter {next_dasha_lord} Dasha on {next_dasha_date}. "

    # If no upcoming changes, indicate that
    if prediction == "Upcoming period changes: ":
        prediction += "No significant Dasha or Antardasha changes are expected in the next year."

    return prediction


def generate_favorable_periods_prediction(chart1, chart2, current_date):
    """
    Generate a prediction for favorable Dasha periods

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart
        current_date (Datetime): The current date

    Returns:
        str: The favorable periods prediction
    """
    # Initialize the prediction
    prediction = "Favorable periods in the next two years: "

    # Check the next two years
    favorable_periods = []

    # Import datetime for calculations
    from datetime import datetime, timedelta

    for months in range(0, 24, 3):
        # Calculate the date by adding months to the JD
        # 30 days per month, converted to JD units
        future_jd = current_date.jd + (30 * months) / 365.25
        future_datetime = Datetime.fromJD(future_jd, current_date.utcoffset)

        # Get the Dasha and Antardasha for each chart
        dasha1 = get_dasha(chart1, future_datetime)
        dasha2 = get_dasha(chart2, future_datetime)
        antardasha1 = get_antardasha(chart1, future_datetime)
        antardasha2 = get_antardasha(chart2, future_datetime)

        # Get the Dasha and Antardasha lords
        dasha_lord1 = get_dasha_lord(dasha1)
        dasha_lord2 = get_dasha_lord(dasha2)
        antardasha_lord1 = get_antardasha_lord(antardasha1)
        antardasha_lord2 = get_antardasha_lord(antardasha2)

        # Calculate the compatibility between the Dasha lords
        dasha_compatibility = calculate_planet_compatibility(dasha_lord1, dasha_lord2)

        # Calculate the compatibility between the Antardasha lords
        antardasha_compatibility = calculate_planet_compatibility(antardasha_lord1, antardasha_lord2)

        # Calculate the overall compatibility score
        overall_score = (dasha_compatibility['score'] * 0.6 + antardasha_compatibility['score'] * 0.4)

        # Check if this is a favorable period
        if overall_score >= 7:
            # Format the date - Datetime doesn't have strftime, so we'll create a simple string
            date = future_datetime.date.date()
            month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            month_name = month_names[date[1] - 1]  # date[1] is the month (1-12)
            year = date[0]
            date_str = f"{month_name} {year}"

            # Add to favorable periods
            favorable_periods.append({
                'date': date_str,
                'score': overall_score,
                'dasha_lord1': dasha_lord1,
                'dasha_lord2': dasha_lord2,
                'antardasha_lord1': antardasha_lord1,
                'antardasha_lord2': antardasha_lord2
            })

    # Add the favorable periods to the prediction
    if favorable_periods:
        for period in favorable_periods[:3]:  # Limit to top 3
            prediction += f"\n- {period['date']}: {period['dasha_lord1']} Dasha / {period['antardasha_lord1']} Antardasha for Person 1, {period['dasha_lord2']} Dasha / {period['antardasha_lord2']} Antardasha for Person 2."
    else:
        prediction += "No highly favorable periods were identified in the next two years."

    return prediction


def generate_challenging_periods_prediction(chart1, chart2, current_date):
    """
    Generate a prediction for challenging Dasha periods

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart
        current_date (Datetime): The current date

    Returns:
        str: The challenging periods prediction
    """
    # Initialize the prediction
    prediction = "Challenging periods in the next two years: "

    # Check the next two years
    challenging_periods = []

    # Import datetime for calculations
    from datetime import datetime, timedelta

    for months in range(0, 24, 3):
        # Calculate the date by adding months to the JD
        # 30 days per month, converted to JD units
        future_jd = current_date.jd + (30 * months) / 365.25
        future_datetime = Datetime.fromJD(future_jd, current_date.utcoffset)

        # Get the Dasha and Antardasha for each chart
        dasha1 = get_dasha(chart1, future_datetime)
        dasha2 = get_dasha(chart2, future_datetime)
        antardasha1 = get_antardasha(chart1, future_datetime)
        antardasha2 = get_antardasha(chart2, future_datetime)

        # Get the Dasha and Antardasha lords
        dasha_lord1 = get_dasha_lord(dasha1)
        dasha_lord2 = get_dasha_lord(dasha2)
        antardasha_lord1 = get_antardasha_lord(antardasha1)
        antardasha_lord2 = get_antardasha_lord(antardasha2)

        # Calculate the compatibility between the Dasha lords
        dasha_compatibility = calculate_planet_compatibility(dasha_lord1, dasha_lord2)

        # Calculate the compatibility between the Antardasha lords
        antardasha_compatibility = calculate_planet_compatibility(antardasha_lord1, antardasha_lord2)

        # Calculate the overall compatibility score
        overall_score = (dasha_compatibility['score'] * 0.6 + antardasha_compatibility['score'] * 0.4)

        # Check if this is a challenging period
        if overall_score <= 3:
            # Format the date - Datetime doesn't have strftime, so we'll create a simple string
            date = future_datetime.date.date()
            month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            month_name = month_names[date[1] - 1]  # date[1] is the month (1-12)
            year = date[0]
            date_str = f"{month_name} {year}"

            # Add to challenging periods
            challenging_periods.append({
                'date': date_str,
                'score': overall_score,
                'dasha_lord1': dasha_lord1,
                'dasha_lord2': dasha_lord2,
                'antardasha_lord1': antardasha_lord1,
                'antardasha_lord2': antardasha_lord2
            })

    # Add the challenging periods to the prediction
    if challenging_periods:
        for period in challenging_periods[:3]:  # Limit to top 3
            prediction += f"\n- {period['date']}: {period['dasha_lord1']} Dasha / {period['antardasha_lord1']} Antardasha for Person 1, {period['dasha_lord2']} Dasha / {period['antardasha_lord2']} Antardasha for Person 2."
    else:
        prediction += "No highly challenging periods were identified in the next two years."

    return prediction
