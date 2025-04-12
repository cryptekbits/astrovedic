#!/usr/bin/env python3
"""
Test Reference Date

This script tests the planetary positions for the reference date:
April 9, 2025 at 20:51 in Bangalore, India.

It outputs the positions using different ayanamsas and house systems
for comparison with reference data.
"""

from tabulate import tabulate

from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib.vedic.nakshatras import get_nakshatra
from flatlib.vedic.kp import get_kp_lords

# Reference date and location
REFERENCE_DATE = "2025/04/09"
REFERENCE_TIME = "20:51"
REFERENCE_LOCATION = "Bangalore, India"
BANGALORE_LAT = 12.9716
BANGALORE_LON = 77.5946

def get_chart(ayanamsa, hsys):
    """
    Create a chart for the reference date with the specified ayanamsa and house system
    
    Args:
        ayanamsa (str): Ayanamsa constant
        hsys (str): House system constant
    
    Returns:
        Chart: Flatlib Chart object
    """
    # Create date and location objects
    date = Datetime(REFERENCE_DATE, REFERENCE_TIME, '+05:30')  # Indian Standard Time
    pos = GeoPos(BANGALORE_LAT, BANGALORE_LON)
    
    # Create chart
    chart = Chart(date, pos, hsys=hsys, mode=ayanamsa)
    
    return chart

def print_planetary_positions(chart, title):
    """
    Print the planetary positions for the given chart
    
    Args:
        chart (Chart): Flatlib Chart object
        title (str): Title for the output
    """
    # List of planets to display
    planets = [
        const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS,
        const.JUPITER, const.SATURN, const.RAHU, const.KETU
    ]
    
    # Print header
    print(f"\n{'=' * 80}")
    print(f"{title}")
    print(f"Reference Date: {REFERENCE_DATE} {REFERENCE_TIME} ({REFERENCE_LOCATION})")
    print(f"Ayanamsa: {chart.mode}, House System: {chart.hsys}")
    print(f"{'=' * 80}\n")
    
    # Prepare data for table
    planet_data = []
    for planet_id in planets:
        planet = chart.getObject(planet_id)
        
        # Find which house contains the planet
        house = chart.houses.getHouseByLon(planet.lon)
        
        # Get nakshatra information
        nakshatra_info = get_nakshatra(planet.lon)
        
        # Get KP information
        kp_info = get_kp_lords(planet.lon)
        
        # Format position
        position = f"{planet.sign} {planet.signlon:.2f}°"
        
        # Format nakshatra
        nakshatra = f"{nakshatra_info['name']} (Pada {nakshatra_info['pada']})"
        
        # Use the house number
        house_num = house.num() if house else 0
        
        planet_data.append([
            planet.id,
            position,
            f"House {house_num}",
            nakshatra,
            kp_info['kp_pointer']
        ])
    
    # Print table
    print(tabulate(planet_data, headers=["Planet", "Position", "House", "Nakshatra", "KP Pointer"], tablefmt="grid"))
    print()

def main():
    """Main function"""
    # Test North Indian style (Lahiri ayanamsa with Whole Sign houses)
    north_indian_chart = get_chart(const.AY_LAHIRI, const.HOUSES_WHOLE_SIGN)
    print_planetary_positions(north_indian_chart, "NORTH INDIAN STYLE")
    
    # Test South Indian style (KP) (Krishnamurti ayanamsa with Placidus houses)
    kp_chart = get_chart(const.AY_KRISHNAMURTI, const.HOUSES_PLACIDUS)
    print_planetary_positions(kp_chart, "SOUTH INDIAN STYLE (KP)")
    
    # Test Tropical (no ayanamsa with Placidus houses)
    tropical_chart = get_chart(None, const.HOUSES_PLACIDUS)
    print_planetary_positions(tropical_chart, "TROPICAL (WESTERN)")

if __name__ == "__main__":
    main()
