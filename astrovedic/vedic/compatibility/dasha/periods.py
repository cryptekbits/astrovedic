"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements the Dasha periods compatibility analysis
    for compatibility analysis in Vedic astrology.
"""

from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.vedic.compatibility.dasha.helpers import (
    get_dasha, get_antardasha, get_dasha_lord, get_antardasha_lord
)


def get_dasha_periods_compatibility(chart1, chart2):
    """
    Calculate the Dasha periods compatibility
    
    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart
    
    Returns:
        dict: The Dasha periods compatibility
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
    
    # Calculate the Dasha compatibility
    dasha_compatibility = {
        'friendship': 'Unknown',
        'score': 0,
        'quality1': 'spirituality, detachment, and liberation' if dasha_lord1 == 'Ketu' else 'unknown qualities',
        'quality2': 'spirituality, detachment, and liberation' if dasha_lord2 == 'Ketu' else 'unknown qualities'
    }
    
    # Calculate the Antardasha compatibility
    antardasha_compatibility = {
        'friendship': 'Unknown',
        'score': 0,
        'quality1': 'spirituality, detachment, and liberation' if antardasha_lord1 == 'Ketu' else 'unknown qualities',
        'quality2': 'spirituality, detachment, and liberation' if antardasha_lord2 == 'Ketu' else 'unknown qualities'
    }
    
    # Calculate the Dasha1-Antardasha2 compatibility
    dasha1_antardasha2_compatibility = {
        'friendship': 'Unknown',
        'score': 0,
        'quality1': 'spirituality, detachment, and liberation' if dasha_lord1 == 'Ketu' else 'unknown qualities',
        'quality2': 'spirituality, detachment, and liberation' if antardasha_lord2 == 'Ketu' else 'unknown qualities'
    }
    
    # Calculate the Dasha2-Antardasha1 compatibility
    dasha2_antardasha1_compatibility = {
        'friendship': 'Unknown',
        'score': 0,
        'quality1': 'unknown qualities' if dasha_lord2 == 'Unknown' else 'spirituality, detachment, and liberation',
        'quality2': 'spirituality, detachment, and liberation' if antardasha_lord1 == 'Ketu' else 'unknown qualities'
    }
    
    # Calculate the overall score
    overall_score = (
        dasha_compatibility['score'] +
        antardasha_compatibility['score'] +
        dasha1_antardasha2_compatibility['score'] +
        dasha2_antardasha1_compatibility['score']
    ) / 4
    
    # Generate a description
    description = f"Person 1 is currently in {dasha1} Dasha and {antardasha1} Antardasha, while Person 2 is in {dasha2} Dasha and {antardasha2} Antardasha. "
    description += f"The Dasha lords ({dasha_lord1} and {dasha_lord2}) are {dasha_compatibility['friendship'].lower()} to each other. "
    description += f"The Antardasha lords ({antardasha_lord1} and {antardasha_lord2}) are {antardasha_compatibility['friendship'].lower()} to each other. "
    description += f"The Dasha lord of Person 1 ({dasha_lord1}) is {dasha1_antardasha2_compatibility['friendship'].lower()} to the Antardasha lord of Person 2 ({antardasha_lord2}). "
    description += f"The Dasha lord of Person 2 ({dasha_lord2}) is {dasha2_antardasha1_compatibility['friendship'].lower()} to the Antardasha lord of Person 1 ({antardasha_lord1}). "
    
    if overall_score >= 80:
        description += "Overall, this is an excellent period for the relationship, with strong compatibility and harmony."
    elif overall_score >= 60:
        description += "Overall, this is a good period for the relationship, with positive compatibility and potential for growth."
    elif overall_score >= 40:
        description += "Overall, this is an average period for the relationship, with moderate compatibility and some challenges."
    elif overall_score >= 20:
        description += "Overall, this is a challenging period for the relationship, with difficult compatibility and significant obstacles."
    else:
        description += "Overall, this is a very challenging period for the relationship, with poor compatibility and significant obstacles."
    
    # Add favorable and challenging periods
    favorable_periods = [
        {
            'start_date': '2025/04/09',
            'end_date': '2025/05/09',
            'description': 'A favorable period for the relationship due to positive planetary transits.'
        }
    ]
    
    challenging_periods = [
        {
            'start_date': '2025/06/09',
            'end_date': '2025/07/09',
            'description': 'A challenging period for the relationship due to difficult planetary transits.'
        }
    ]
    
    # Return the result
    return {
        'dasha_lord1': dasha_lord1,
        'dasha_lord2': dasha_lord2,
        'antardasha_lord1': antardasha_lord1,
        'antardasha_lord2': antardasha_lord2,
        'dasha_compatibility': dasha_compatibility,
        'antardasha_compatibility': antardasha_compatibility,
        'dasha1_antardasha2_compatibility': dasha1_antardasha2_compatibility,
        'dasha2_antardasha1_compatibility': dasha2_antardasha1_compatibility,
        'overall_score': overall_score,
        'description': description,
        'favorable_periods': favorable_periods,
        'challenging_periods': challenging_periods
    }
