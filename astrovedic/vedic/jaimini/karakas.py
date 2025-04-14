"""Jaimini Karaka calculations.

This module implements both Chara Karaka (temporary significators) and
Sthira Karaka (fixed significators) calculations for Jaimini astrology.
"""

from typing import Dict, List, Tuple

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.object import GenericObject


# Karaka names (standard abbreviations)
ATMAKARAKA = "AK"
AMATYAKARAKA = "AmK"
BHRATRIKARAKA = "BK"
MATRIKARAKA = "MK"
PUTRAKARAKA = "PK"
GNATIKARAKA = "GK"
DARAKARAKA = "DK"
STRIKAKARAKA = "SK" # Some traditions use 7 karakas, omitting this

# Full Karaka names
ATMAKARAKA_FULL = "Atma Karaka"
AMATYAKARAKA_FULL = "Amatya Karaka"
BHRATRIKARAKA_FULL = "Bhratri Karaka"
MATRIKARAKA_FULL = "Matri Karaka"
PUTRAKARAKA_FULL = "Putra Karaka"
GNATIKARAKA_FULL = "Gnati Karaka"
DARAKARAKA_FULL = "Dara Karaka"
STRIKAKARAKA_FULL = "Stri Karaka"


# List of planets considered for Chara Karakas
CHARA_KARAKA_PLANETS = [
    const.SUN, const.MOON, const.MARS, const.MERCURY,
    const.JUPITER, const.VENUS, const.SATURN, const.RAHU
]

# Sthira Karaka (fixed significator) assignments
STHIRA_KARAKAS = {
    ATMAKARAKA_FULL: const.SUN,      # Soul, self
    AMATYAKARAKA_FULL: const.JUPITER, # Career, minister
    BHRATRIKARAKA_FULL: const.MARS,   # Siblings, courage
    MATRIKARAKA_FULL: const.MOON,     # Mother, mind
    PUTRAKARAKA_FULL: const.JUPITER,  # Children, wisdom
    GNATIKARAKA_FULL: const.SATURN,   # Relatives, longevity
    DARAKARAKA_FULL: const.VENUS,     # Spouse, relationships
    STRIKAKARAKA_FULL: const.VENUS    # Alternate spouse significator
}

# Define Karaka sequence for assignment
# KARAKA_SEQUENCE = [
#     ATMAKARAKA, AMATYAKARAKA, BHRATRIKARAKA, MATRIKARAKA,
#     PUTRAKARAKA, GNATIKARAKA, DARAKARAKA, STRIKAKARAKA
# ]


def calculate_sthira_karakas() -> Dict[str, str]:
    """Returns the Jaimini Sthira Karakas (fixed significators).

    Sthira Karakas are fixed planetary significators in Jaimini astrology.
    Unlike Chara Karakas which change based on planetary positions,
    Sthira Karakas are always the same for every chart.

    Returns:
        Dict[str, str]: A dictionary where keys are the full Karaka names
        and values are the corresponding planet IDs.
    """
    return STHIRA_KARAKAS


def calculate_chara_karakas(chart: Chart) -> Dict[str, str]:
    """Calculates the Jaimini Chara Karakas (temporary significators) for a chart.

    This function determines the eight Chara Karakas (Atmakaraka, Amatyakaraka,
    Bhratrikaraka, Matrikaraka, Putrakaraka, Gnatikaraka, Darakaraka, and
    Strīkaraka/Alternate Darakaraka) based on the longitudes of the planets
    defined in `const.CHARA_KARAKA_PLANETS` (Sun, Moon, Mars, Mercury,
    Jupiter, Venus, Saturn, and Rahu).

    Calculation Logic:
    1. Planets are ranked based on their degree within their sign (longitude % 30),
       from highest to lowest.
    2. For Rahu, the longitude is calculated as 360 - original longitude, as per
       standard Jaimini rules, before determining the degree within the sign.
    3. Ties in degree within the sign are broken by comparing the full longitude
       (using the adjusted longitude for Rahu), with the higher longitude ranking
       higher. Ketu is not considered in standard 8-karaka schemes.
    4. The karakas are assigned in order based on `const.LIST_CHARA_KARAKAS`.

    Args:
        chart: A astrovedic.chart.Chart object containing planetary data.

    Returns:
        Dict[str, str]: A dictionary where keys are the full Karaka names
        (e.g., 'Atma Karaka' from `const.LIST_CHARA_KARAKAS`) and values
        are the corresponding planet IDs (e.g., 'Venus', 'Sun' from
        `const.PLANET_IDs`).
    """
    planet_degrees: List[Tuple[str, float, float]] = []

    for planet_id in const.CHARA_KARAKA_PLANETS:
        try:
            obj: GenericObject = chart.getObject(planet_id)
            longitude = obj.lon

            if planet_id == const.RAHU:
                # Jaimini rule for Rahu: 360 - longitude
                # Ensure longitude is positive before calculation
                adjusted_lon = 360.0 - (longitude % 360)
                deg_in_sign = adjusted_lon % 30.0
                sort_key = adjusted_lon # Use adjusted lon for tie-breaking
            else:
                deg_in_sign = longitude % 30.0
                sort_key = longitude # Use original lon for tie-breaking

            planet_degrees.append((planet_id, deg_in_sign, sort_key))

        except ValueError:
            # Handle cases where a planet might not be in the chart object
            # (should not happen with standard chart generation)
            print(f"Warning: Planet {planet_id} not found in chart for Chara Karaka calculation.")
            continue

    # Sort planets:
    # Primary sort key: Degree within the sign (descending)
    # Secondary sort key (for ties): Full longitude (adjusted for Rahu, descending)
    planet_degrees.sort(key=lambda x: (x[1], x[2]), reverse=True)

    # Assign Karakas based on sorted order
    chara_karakas: Dict[str, str] = {}
    num_karakas = min(len(planet_degrees), len(const.LIST_CHARA_KARAKAS))

    for i in range(num_karakas):
        karaka_name = const.LIST_CHARA_KARAKAS[i]
        planet_id = planet_degrees[i][0]
        chara_karakas[karaka_name] = planet_id

    # Handle potential ties explicitly based on standard rules (re-check if needed)
    # The current sort key handles ties by longitude value implicitly.
    # Further tie-breaking (e.g., latitude) is complex and less standard.

    return chara_karakas
