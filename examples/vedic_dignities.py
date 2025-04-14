#!/usr/bin/env python3
"""
    Vedic Dignities Example
    
    This example demonstrates how to use the Vedic dignities module
    to analyze planetary dignities in Vedic astrology.
"""

from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic import const
from astrovedic.vedic import dignities as vedic_dignities
from prettytable import PrettyTable


def print_section_header(title):
    """Print a section header"""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80)


def main():
    """Main function"""
    # Create a chart for the reference date
    date = Datetime('2025/04/09', '20:51', '+05:30')
    pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
    
    # Create a chart with Whole Sign houses and Lahiri ayanamsa
    chart = Chart(date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
    
    print_section_header("CHART INFORMATION")
    print(f"Date: {date.date} {date.time} {date.utcoffset}")
    print(f"Location: {pos.lat}°N, {pos.lon}°E (Bangalore, India)")
    print(f"House System: {chart.hsys}")
    print(f"Ayanamsa: {chart.mode}")
    
    # Print planet positions and dignities
    print_section_header("PLANET POSITIONS AND DIGNITIES")
    
    # Create a table for planet positions and dignities
    table = PrettyTable()
    table.field_names = ["Planet", "Sign", "Degree", "Dignity", "Score", "Rulership", "Exaltation", "Debilitation", "Moolatrikona"]
    
    # Add planets to the table
    for planet_id in const.LIST_OBJECTS_VEDIC:
        planet = chart.getObject(planet_id)
        sign = planet.sign
        degree = planet.signlon
        
        # Get dignity information
        dignity_score = vedic_dignities.get_dignity_score(planet_id, sign, degree)
        dignity_name = vedic_dignities.get_dignity_name(planet_id, sign, degree)
        
        # Get rulership information
        ruled_signs = vedic_dignities.get_ruled_signs(planet_id)
        rulership = ", ".join(ruled_signs) if ruled_signs else "None"
        
        # Get exaltation information
        exaltation = vedic_dignities.get_exaltation(planet_id)
        exalt_str = f"{exaltation[0]} {exaltation[1]}°" if exaltation else "None"
        
        # Get debilitation information
        debilitation = vedic_dignities.get_debilitation(planet_id)
        debil_str = f"{debilitation[0]} {debilitation[1]}°" if debilitation else "None"
        
        # Get Moolatrikona information
        moolatrikona = vedic_dignities.get_moolatrikona(planet_id)
        mt_str = f"{moolatrikona[0]} {moolatrikona[1]}-{moolatrikona[2]}°" if moolatrikona else "None"
        
        # Add the row to the table
        table.add_row([
            planet_id,
            sign,
            f"{degree:.2f}°",
            dignity_name,
            dignity_score['score'],
            rulership,
            exalt_str,
            debil_str,
            mt_str
        ])
    
    print(table)
    
    # Print natural friendships
    print_section_header("NATURAL FRIENDSHIPS")
    
    # Create a table for natural friendships
    table = PrettyTable()
    table.field_names = [""] + const.LIST_SEVEN_PLANETS
    
    # Add planets to the table
    for planet1_id in const.LIST_SEVEN_PLANETS:
        row = [planet1_id]
        for planet2_id in const.LIST_SEVEN_PLANETS:
            friendship = vedic_dignities.get_natural_friendship(planet1_id, planet2_id)
            if friendship == vedic_dignities.FRIENDSHIP_LEVELS['GREAT_FRIEND']:
                row.append("G+")
            elif friendship == vedic_dignities.FRIENDSHIP_LEVELS['FRIEND']:
                row.append("F")
            elif friendship == vedic_dignities.FRIENDSHIP_LEVELS['NEUTRAL']:
                row.append("N")
            elif friendship == vedic_dignities.FRIENDSHIP_LEVELS['ENEMY']:
                row.append("E")
            else:  # GREAT_ENEMY
                row.append("G-")
        table.add_row(row)
    
    print(table)
    
    # Print combined friendships
    print_section_header("COMBINED FRIENDSHIPS")
    
    # Create a table for combined friendships
    table = PrettyTable()
    table.field_names = [""] + const.LIST_SEVEN_PLANETS
    
    # Add planets to the table
    for planet1_id in const.LIST_SEVEN_PLANETS:
        row = [planet1_id]
        for planet2_id in const.LIST_SEVEN_PLANETS:
            friendship = vedic_dignities.calculate_combined_friendship(chart, planet1_id, planet2_id)
            if friendship == 'GREAT_FRIEND':
                row.append("G+")
            elif friendship == 'FRIEND':
                row.append("F")
            elif friendship == 'NEUTRAL':
                row.append("N")
            elif friendship == 'ENEMY':
                row.append("E")
            else:  # GREAT_ENEMY
                row.append("G-")
        table.add_row(row)
    
    print(table)


if __name__ == '__main__':
    main()
