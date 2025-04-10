"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements Dosha (affliction) analysis
    for Vedic astrology.
"""

from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

from flatlib.vedic.compatibility.dosha.mangal import get_mangal_dosha
from flatlib.vedic.compatibility.dosha.kuja import get_kuja_dosha
from flatlib.vedic.compatibility.dosha.shani import get_shani_dosha
from flatlib.vedic.compatibility.dosha.grahan import get_grahan_dosha


def get_dosha_cancellation(chart1, chart2):
    """
    Check if Doshas are cancelled between two charts

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with Dosha cancellation information
    """
    # Get the Doshas for each chart
    mangal_dosha1 = get_mangal_dosha(chart1)
    mangal_dosha2 = get_mangal_dosha(chart2)
    kuja_dosha1 = get_kuja_dosha(chart1)
    kuja_dosha2 = get_kuja_dosha(chart2)

    # Check if both have the same Dosha
    both_have_mangal = mangal_dosha1['has_dosha'] and mangal_dosha2['has_dosha']
    both_have_kuja = kuja_dosha1['has_dosha'] and kuja_dosha2['has_dosha']

    # Check for cancellation
    is_cancelled = both_have_mangal or both_have_kuja

    # Generate the description
    if both_have_mangal and both_have_kuja:
        description = "Both individuals have Mangal Dosha and Kuja Dosha, which cancels out the negative effects."
    elif both_have_mangal:
        description = "Both individuals have Mangal Dosha, which cancels out the negative effects."
    elif both_have_kuja:
        description = "Both individuals have Kuja Dosha, which cancels out the negative effects."
    else:
        description = "No Dosha cancellation is present."

    return {
        'is_cancelled': is_cancelled,
        'both_have_mangal': both_have_mangal,
        'both_have_kuja': both_have_kuja,
        'description': description
    }


def get_dosha_remedies(chart1, chart2):
    """
    Get remedies for Doshas

    Args:
        chart1 (Chart): The first chart
        chart2 (Chart): The second chart

    Returns:
        dict: Dictionary with Dosha remedies
    """
    # Get the Doshas for each chart
    mangal_dosha1 = get_mangal_dosha(chart1)
    mangal_dosha2 = get_mangal_dosha(chart2)
    kuja_dosha1 = get_kuja_dosha(chart1)
    kuja_dosha2 = get_kuja_dosha(chart2)
    shani_dosha1 = get_shani_dosha(chart1)
    shani_dosha2 = get_shani_dosha(chart2)
    grahan_dosha1 = get_grahan_dosha(chart1)
    grahan_dosha2 = get_grahan_dosha(chart2)

    # Initialize the remedies with default empty lists for all possible doshas
    remedies = {
        'Mangal Dosha (Person 1)': [],
        'Mangal Dosha (Person 2)': [],
        'Kuja Dosha (Person 1)': [],
        'Kuja Dosha (Person 2)': [],
        'Shani Dosha (Person 1)': [],
        'Shani Dosha (Person 2)': [],
        'Grahan Dosha (Person 1)': [],
        'Grahan Dosha (Person 2)': []
    }

    # Add remedies for Mangal Dosha
    if mangal_dosha1['has_dosha']:
        remedies['Mangal Dosha (Person 1)'] = [
            "Wear a red coral gemstone set in gold or copper.",
            "Recite the Hanuman Chalisa daily.",
            "Perform Mars-related rituals on Tuesdays.",
            "Donate red items like red lentils, red cloth, or copper items.",
            "Worship Lord Hanuman or Lord Kartikeya."
        ]

    if mangal_dosha2['has_dosha']:
        remedies['Mangal Dosha (Person 2)'] = [
            "Wear a red coral gemstone set in gold or copper.",
            "Recite the Hanuman Chalisa daily.",
            "Perform Mars-related rituals on Tuesdays.",
            "Donate red items like red lentils, red cloth, or copper items.",
            "Worship Lord Hanuman or Lord Kartikeya."
        ]

    # Add remedies for Kuja Dosha
    if kuja_dosha1['has_dosha']:
        remedies['Kuja Dosha (Person 1)'] = [
            "Perform Kuja Dosha Nivarana Puja.",
            "Recite the Mangal Gayatri Mantra 108 times daily.",
            "Donate copper vessels filled with jaggery and ghee.",
            "Worship Lord Subramanya on Tuesdays.",
            "Perform charity to unmarried girls."
        ]

    if kuja_dosha2['has_dosha']:
        remedies['Kuja Dosha (Person 2)'] = [
            "Perform Kuja Dosha Nivarana Puja.",
            "Recite the Mangal Gayatri Mantra 108 times daily.",
            "Donate copper vessels filled with jaggery and ghee.",
            "Worship Lord Subramanya on Tuesdays.",
            "Perform charity to unmarried girls."
        ]

    # Add remedies for Shani Dosha
    if shani_dosha1['has_dosha']:
        remedies['Shani Dosha (Person 1)'] = [
            "Wear a blue sapphire or amethyst gemstone.",
            "Recite the Shani Stotra or Shani Chalisa on Saturdays.",
            "Offer mustard oil to Lord Shani on Saturdays.",
            "Feed crows and dogs on Saturdays.",
            "Donate black items like sesame seeds, iron, or black cloth."
        ]

    if shani_dosha2['has_dosha']:
        remedies['Shani Dosha (Person 2)'] = [
            "Wear a blue sapphire or amethyst gemstone.",
            "Recite the Shani Stotra or Shani Chalisa on Saturdays.",
            "Offer mustard oil to Lord Shani on Saturdays.",
            "Feed crows and dogs on Saturdays.",
            "Donate black items like sesame seeds, iron, or black cloth."
        ]

    # Add remedies for Grahan Dosha
    if grahan_dosha1['has_dosha']:
        remedies['Grahan Dosha (Person 1)'] = [
            "Perform Grahan Dosha Nivarana Puja.",
            "Recite the Surya Gayatri Mantra and Chandra Gayatri Mantra.",
            "Donate according to the afflicted planet (Sun or Moon).",
            "Perform charity during solar or lunar eclipses.",
            "Wear a ruby (for Sun) or pearl (for Moon) gemstone."
        ]

    if grahan_dosha2['has_dosha']:
        remedies['Grahan Dosha (Person 2)'] = [
            "Perform Grahan Dosha Nivarana Puja.",
            "Recite the Surya Gayatri Mantra and Chandra Gayatri Mantra.",
            "Donate according to the afflicted planet (Sun or Moon).",
            "Perform charity during solar or lunar eclipses.",
            "Wear a ruby (for Sun) or pearl (for Moon) gemstone."
        ]

    return remedies
