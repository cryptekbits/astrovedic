"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements basic analysis tools for Varga (divisional chart) calculations
    in Vedic astrology. For detailed analysis and reporting,
    use the astroved_extension package.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.vedic.vargas.constants import (
    D1, D2, D3, D4, D7, D9, D10, D12,
    D16, D20, D24, D27, D30, D40, D45, D60,
    LIST_VARGAS
)
from astrovedic.vedic.vargas import get_varga_chart

from astrovedic.vedic.vargas.analysis import (
    get_varga_visesha, get_varga_strength,
    get_vimshopaka_bala
)


def get_basic_varga_analysis(chart):
    """
    Get basic analysis of Vargas (divisional charts) for a chart.
    For detailed analysis, use the astroved_extension package.

    Args:
        chart (Chart): The chart

    Returns:
        dict: Dictionary with basic Vargas analysis
    """
    # Initialize the result
    result = {
        'planet_analysis': {},
        'overall_strength': {}
    }

    # Get all planets
    planets = [
        const.SUN, const.MOON, const.MARS, const.MERCURY,
        const.JUPITER, const.VENUS, const.SATURN,
        const.URANUS, const.NEPTUNE, const.PLUTO
    ]

    # Analyze each planet
    for planet_id in planets:
        try:
            # Get the planet from the birth chart
            planet = chart.getObject(planet_id)

            # Get Varga Visesha
            varga_visesha = get_varga_visesha(chart, planet_id)

            # Get Varga Strength
            varga_strength = get_varga_strength(chart, planet_id)

            # Get Vimshopaka Bala
            vimshopaka_bala = get_vimshopaka_bala(chart, planet_id)

            # Store the analysis
            result['planet_analysis'][planet_id] = {
                'varga_visesha': varga_visesha,
                'varga_strength': varga_strength,
                'vimshopaka_bala': vimshopaka_bala
            }
        except:
            # Planet not found in chart
            pass

    # Calculate overall strength
    total_vimshopaka = 0
    total_planets = 0

    for planet_id, analysis in result['planet_analysis'].items():
        if 'vimshopaka_bala' in analysis:
            total_vimshopaka += analysis['vimshopaka_bala']['vimshopaka_bala']
            total_planets += 1

    if total_planets > 0:
        result['overall_strength']['average_vimshopaka'] = total_vimshopaka / total_planets
    else:
        result['overall_strength']['average_vimshopaka'] = 0

    return result
