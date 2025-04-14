"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Yogas (planetary combinations) calculations
    for Vedic astrology. It includes functions to identify and analyze
    various types of Yogas in a chart.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.vedic.yogas.core import (
    get_yoga_summary, get_yoga_strength,
    get_yoga_effects, get_strongest_yoga
)

# Import specific yoga calculation functions
from astrovedic.vedic.yogas.mahapurusha import (
    get_mahapurusha_yogas, has_ruchaka_yoga,
    has_bhadra_yoga, has_hamsa_yoga,
    has_malavya_yoga, has_sasa_yoga
)
from astrovedic.vedic.yogas.raja import (
    get_raja_yogas, has_dharmakarmaadhipati_yoga,
    has_gajakesari_yoga, has_amala_yoga,
    has_sreenatha_yoga, has_chandra_mangala_yoga
)
from astrovedic.vedic.yogas.dhana import (
    get_dhana_yogas, has_lakshmi_yoga,
    has_kubera_yoga, has_kalanidhi_yoga,
    has_vasumati_yoga, has_mridanga_yoga
)
from astrovedic.vedic.yogas.nabhasa import (
    get_nabhasa_yogas, has_rajju_yoga,
    has_musala_yoga, has_nala_yoga,
    has_mala_yoga, has_sarpa_yoga
)
from astrovedic.vedic.yogas.dosha import (
    get_dosha_yogas, has_kemadruma_yoga,
    has_daridra_yoga, has_shakat_yoga,
    has_kalasarpa_yoga, has_graha_yuddha
)
from astrovedic.vedic.yogas.chandra import (
    get_chandra_yogas, has_adhi_yoga,
    has_sunapha_yoga, has_anapha_yoga,
    has_durudhura_yoga, has_kemadruma_yoga
)
from astrovedic.vedic.yogas.surya import (
    get_surya_yogas, has_vasi_yoga,
    has_vesi_yoga, has_ubhayachari_yoga,
    has_budha_aditya_yoga, has_sun_parivartana_yoga
)
from astrovedic.vedic.yogas.basic_analysis import (
    get_basic_yoga_analysis
)

# Note: For detailed analysis, use the astroved_extension package

# Constants for Yoga types
MAHAPURUSHA_YOGA = 'Mahapurusha Yoga'
RAJA_YOGA = 'Raja Yoga'
DHANA_YOGA = 'Dhana Yoga'
NABHASA_YOGA = 'Nabhasa Yoga'
DOSHA_YOGA = 'Dosha Yoga'
CHANDRA_YOGA = 'Chandra Yoga'
SURYA_YOGA = 'Surya Yoga'

# List of all Yoga types
LIST_YOGA_TYPES = [
    MAHAPURUSHA_YOGA, RAJA_YOGA, DHANA_YOGA,
    NABHASA_YOGA, DOSHA_YOGA, CHANDRA_YOGA,
    SURYA_YOGA
]


def get_all_yogas(chart):
    """
    Identify all Yogas in a chart

    Args:
        chart (Chart): The birth chart

    Returns:
        dict: Dictionary with all Yoga information
    """
    # Initialize the result
    result = {
        'mahapurusha_yogas': get_mahapurusha_yogas(chart),
        'raja_yogas': get_raja_yogas(chart),
        'dhana_yogas': get_dhana_yogas(chart),
        'nabhasa_yogas': get_nabhasa_yogas(chart),
        'dosha_yogas': get_dosha_yogas(chart),
        'chandra_yogas': get_chandra_yogas(chart),
        'surya_yogas': get_surya_yogas(chart),
        'summary': None
    }

    # Generate summary information
    result['summary'] = get_yoga_summary(result)

    return result


def get_yoga_analysis(chart):
    """
    Analyze the Yogas in a chart
    Note: For detailed analysis, use the astroved_extension package

    Args:
        chart (Chart): The birth chart

    Returns:
        dict: Dictionary with basic Yoga analysis
    """
    # Get all Yogas
    yogas = get_all_yogas(chart)

    # Get basic analysis
    analysis = get_basic_yoga_analysis(chart, yogas)

    return analysis


def has_yoga(chart, yoga_name):
    """
    Check if a chart has a specific Yoga

    Args:
        chart (Chart): The birth chart
        yoga_name (str): The name of the Yoga to check

    Returns:
        bool: True if the chart has the Yoga, False otherwise
    """
    # Get all Yogas
    yogas = get_all_yogas(chart)

    # Check each type of Yoga
    for yoga_type, yoga_list in yogas.items():
        if yoga_type != 'summary':
            for yoga in yoga_list:
                if yoga['name'] == yoga_name:
                    return True

    return False


def get_yoga_predictions(chart):
    """
    Generate predictions based on Yogas in a chart
    Note: This function is deprecated. Use astroved_extension for detailed predictions.

    Args:
        chart (Chart): The birth chart

    Returns:
        dict: Dictionary with basic Yoga analysis
    """
    # Get all Yogas
    yogas = get_all_yogas(chart)

    # Return basic analysis instead of predictions
    return get_basic_yoga_analysis(chart, yogas)


def get_yogas(chart):
    """
    Get all Yogas in a chart (alias for get_all_yogas)

    Args:
        chart (Chart): The birth chart

    Returns:
        dict: Dictionary with all Yoga information
    """
    return get_all_yogas(chart)
