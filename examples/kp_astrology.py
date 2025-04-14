#!/usr/bin/env python3
"""
KP Astrology Example

This script demonstrates how to use flatlib for KP (Krishnamurti Paddhati) astrology calculations.
It includes:
- Accurate KP sublord and sub-sublord calculations using the KP_SL_Divisions.csv file
- Placidus house system with Krishnamurti ayanamsa
- Proper house assignments for planets
- KP pointers in the format: Sign Lord-Star Lord-Sub Lord-Sub Sub Lord

Usage:
  python kp_astrology.py                   # Generate chart for current time
  python kp_astrology.py YYYY/MM/DD HH:MM  # Generate chart for specific date and time
  python kp_astrology.py -h, --help        # Show help message
"""

import os
import sys
import csv
import datetime
import logging
from tabulate import tabulate

from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic import const
from astrovedic import angle
from astrovedic.object import GenericObject

# Configure logging to suppress warnings
logger = logging.getLogger("flatlib")
logger.setLevel(logging.ERROR)

# Define Rahu and Ketu for KP astrology
const.RAHU = const.NORTH_NODE
const.KETU = const.SOUTH_NODE

# Nakshatra data (27 nakshatras)
NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu",
    "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta",
    "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula",
    "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

# Nakshatra lords (KP system) - in order of the 27 nakshatras
NAKSHATRA_LORDS = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",  # 1-9
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",  # 10-18
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"   # 19-27
]

# Vimshottari dasha periods (in years)
VIMSHOTTARI_PERIODS = {
    "Ketu": 7,
    "Venus": 20,
    "Sun": 6,
    "Moon": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Mercury": 17
}

# Total of Vimshottari periods (120 years)
TOTAL_VIMSHOTTARI_YEARS = sum(VIMSHOTTARI_PERIODS.values())

# Sign lords (rulers) in order of the 12 signs
SIGN_LORDS = [
    "Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",  # Aries to Virgo
    "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"  # Libra to Pisces
]

# Planet abbreviations for KP pointer format
PLANET_ABBR = {
    "Sun": "Sun",
    "Moon": "Mon",
    "Mercury": "Mer",
    "Venus": "Ven",
    "Mars": "Mar",
    "Jupiter": "Jup",
    "Saturn": "Sat",
    "Rahu": "Rah",
    "Ketu": "Ket",
    "North Node": "Rah",
    "South Node": "Ket"
}

# Path to the KP_SL_Divisions.csv file
CSV_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                            "kpDashboard/astro_engine/data/KP_SL_Divisions.csv")

# Cache for the KP sublord divisions data
KP_SL_DIVISIONS = None

def dms_to_decimal(dms_str):
    """Convert a DMS string (degrees:minutes:seconds) to decimal degrees"""
    # Handle malformed entries in the CSV
    dms_str = dms_str.strip()
    if dms_str.endswith(':'):
        dms_str = dms_str[:-1]
    
    parts = dms_str.split(':')
    if len(parts) != 3:
        raise ValueError(f"Invalid DMS format: {dms_str}")
    
    degrees = int(parts[0])
    minutes = int(parts[1])
    seconds = int(parts[2])
    
    return degrees + minutes/60 + seconds/3600

def load_kp_sl_divisions():
    """Load the KP sublord divisions from the CSV file"""
    global KP_SL_DIVISIONS
    
    if KP_SL_DIVISIONS is not None:
        return KP_SL_DIVISIONS
    
    KP_SL_DIVISIONS = []
    
    try:
        with open(CSV_FILE_PATH, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Convert DMS strings to decimal degrees
                try:
                    from_deg = dms_to_decimal(row['From_DMS'])
                    to_deg = dms_to_decimal(row['To_DMS'])
                    
                    # Add sign offset (0-330 degrees)
                    sign_offset = {
                        'Aries': 0, 'Taurus': 30, 'Gemini': 60, 'Cancer': 90,
                        'Leo': 120, 'Virgo': 150, 'Libra': 180, 'Scorpio': 210,
                        'Sagittarius': 240, 'Capricorn': 270, 'Aquarius': 300, 'Pisces': 330
                    }
                    
                    from_deg_abs = sign_offset[row['Sign']] + from_deg
                    to_deg_abs = sign_offset[row['Sign']] + to_deg
                    
                    KP_SL_DIVISIONS.append({
                        'sign': row['Sign'],
                        'nakshatra': row['Nakshatra'],
                        'from_deg': from_deg,
                        'to_deg': to_deg,
                        'from_deg_abs': from_deg_abs,
                        'to_deg_abs': to_deg_abs,
                        'rasi_lord': row['RasiLord'],
                        'nakshatra_lord': row['NakshatraLord'],
                        'sub_lord': row['SubLord']
                    })
                except ValueError as e:
                    print(f"Error processing row: {row} - {e}")
    except FileNotFoundError:
        print(f"Warning: KP_SL_Divisions.csv file not found at {CSV_FILE_PATH}")
        print("Falling back to algorithmic calculation for KP sublords")
        return None
    
    return KP_SL_DIVISIONS

def get_kp_sublord(longitude):
    """Get the KP sublord for a given longitude
    
    Args:
        longitude (float): The longitude in degrees (0-360)
    
    Returns:
        dict: A dictionary with the KP sublord information
    """
    divisions = load_kp_sl_divisions()
    
    # If CSV file not found, return None to trigger fallback
    if divisions is None:
        return None
    
    # Normalize longitude to 0-360
    longitude = longitude % 360
    
    # Get the sign and position within the sign
    sign_num = int(longitude / 30)
    sign_pos = longitude % 30
    
    # Find the matching division
    for div in divisions:
        if div['from_deg_abs'] <= longitude < div['to_deg_abs']:
            return {
                'sign': div['sign'],
                'nakshatra': div['nakshatra'],
                'rasi_lord': div['rasi_lord'],
                'nakshatra_lord': div['nakshatra_lord'],
                'sub_lord': div['sub_lord']
            }
    
    # If no match found (shouldn't happen), return None
    return None

def get_sub_sublord(longitude):
    """Calculate the sub-sublord for a given longitude
    
    This uses the same Vimshottari dasha periods as the sublord calculation,
    but applies it to the sub-division.
    
    Args:
        longitude (float): The longitude in degrees (0-360)
    
    Returns:
        str: The sub-sublord name
    """
    # Vimshottari dasha periods (in years)
    vimshottari_periods = VIMSHOTTARI_PERIODS
    
    # Total of Vimshottari periods (120 years)
    total_vimshottari_years = TOTAL_VIMSHOTTARI_YEARS
    
    # Lords sequence
    lords_sequence = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
    
    # Get the sublord information
    sublord_info = get_kp_sublord(longitude)
    if not sublord_info:
        return None
    
    # Get the sublord
    sub_lord = sublord_info['sub_lord']
    
    # Find the start index for the sub-sublord calculation
    start_idx = lords_sequence.index(sub_lord)
    
    # Find the exact position within the sub-division
    divisions = load_kp_sl_divisions()
    
    # Normalize longitude to 0-360
    longitude = longitude % 360
    
    # Find the matching division
    for div in divisions:
        if div['from_deg_abs'] <= longitude < div['to_deg_abs']:
            # Calculate position within the sub-division
            sub_div_length = div['to_deg_abs'] - div['from_deg_abs']
            pos_in_sub_div = (longitude - div['from_deg_abs']) / sub_div_length
            break
    else:
        # If no match found (shouldn't happen), return None
        return None
    
    # Calculate sub-sublord
    current_pos = 0
    
    for i in range(9):  # 9 planets in Vimshottari
        lord_idx = (start_idx + i) % 9
        current_lord = lords_sequence[lord_idx]
        
        # Calculate sub-sub length based on Vimshottari period
        sub_sub_length = vimshottari_periods[current_lord] / total_vimshottari_years
        
        if current_pos <= pos_in_sub_div < (current_pos + sub_sub_length):
            return current_lord
        
        current_pos += sub_sub_length
    
    # If no sub-sublord found (shouldn't happen), return the sublord
    return sub_lord

def get_kp_pointer(planet_id, longitude):
    """Get the KP pointer (Sign Lord-Star Lord-Sub Lord-Sub Sub Lord) for a planet
    
    Args:
        planet_id (str): The planet ID
        longitude (float): The longitude in degrees (0-360)
    
    Returns:
        str: The KP pointer string
    """
    # Get the KP lords information
    kp_info = get_kp_lords(longitude)
    
    # Format the KP pointer
    return kp_info['kp_pointer']

def get_kp_lords(longitude):
    """Get sign lord, star lord, sub lord, and sub-sub lord for KP astrology
    using the KP_SL_Divisions.csv file for accurate divisions"""
    # Get the sublord information from the CSV-based calculator
    sublord_info = get_kp_sublord(longitude)
    if not sublord_info:
        # Fallback to the old calculation if the CSV-based calculator fails
        return get_kp_lords_fallback(longitude)
    
    # Get the sub-sublord
    sub_sublord = get_sub_sublord(longitude)
    
    # Format the KP pointer
    sign_lord = sublord_info['rasi_lord']
    star_lord = sublord_info['nakshatra_lord']
    sub_lord = sublord_info['sub_lord']
    
    sign_abbr = PLANET_ABBR.get(sign_lord, sign_lord[:3])
    star_abbr = PLANET_ABBR.get(star_lord, star_lord[:3])
    sub_abbr = PLANET_ABBR.get(sub_lord, sub_lord[:3])
    sub_sub_abbr = PLANET_ABBR.get(sub_sublord, sub_sublord[:3])
    
    kp_pointer = f"{sign_abbr}-{star_abbr}-{sub_abbr}-{sub_sub_abbr}"
    
    return {
        'sign_lord': sign_lord,
        'star_lord': star_lord,
        'sub_lord': sub_lord,
        'sub_sub_lord': sub_sublord,
        'kp_pointer': kp_pointer
    }

def get_kp_lords_fallback(longitude):
    """Fallback method using the original calculation algorithm
    in case the CSV-based calculator fails"""
    # Calculate nakshatra (0-26)
    nakshatra_id = int(longitude / 13.33333) % 27

    # Get nakshatra (star) lord
    star_lord = NAKSHATRA_LORDS[nakshatra_id]

    # Calculate sign (0-11)
    sign_num = int(longitude / 30) % 12

    # Get sign lord based on sign number
    sign_lord = SIGN_LORDS[sign_num]

    # Calculate position within nakshatra (0-13.33333 degrees)
    pos_in_nakshatra = longitude % 13.33333

    # Calculate sub-divisions based on Vimshottari dasha periods
    nakshatra_length = 13.33333  # degrees

    # Start with the nakshatra lord and follow the Vimshottari sequence
    lords_sequence = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
    start_idx = lords_sequence.index(star_lord)

    # Calculate sub lord
    current_pos = 0
    sub_lord = None
    sub_lord_pos = 0
    sub_length_found = 0

    for i in range(9):  # 9 planets in Vimshottari
        lord_idx = (start_idx + i) % 9
        current_lord = lords_sequence[lord_idx]

        # Calculate sub length based on Vimshottari period
        sub_length = (VIMSHOTTARI_PERIODS[current_lord] / TOTAL_VIMSHOTTARI_YEARS) * nakshatra_length

        if current_pos <= pos_in_nakshatra < (current_pos + sub_length):
            sub_lord = current_lord
            sub_lord_pos = pos_in_nakshatra - current_pos
            sub_length_found = sub_length
            break

        current_pos += sub_length

    # If no sub lord found, use star lord
    if not sub_lord:
        sub_lord = star_lord
        sub_lord_pos = 0
        sub_length_found = nakshatra_length

    # Calculate sub-sub lord
    start_idx = lords_sequence.index(sub_lord)
    current_pos = 0
    sub_sub_lord = None

    for i in range(9):  # 9 planets in Vimshottari
        lord_idx = (start_idx + i) % 9
        current_lord = lords_sequence[lord_idx]

        # Calculate sub-sub length based on Vimshottari period
        sub_sub_length = (VIMSHOTTARI_PERIODS[current_lord] / TOTAL_VIMSHOTTARI_YEARS) * sub_length_found

        if current_pos <= sub_lord_pos < (current_pos + sub_sub_length):
            sub_sub_lord = current_lord
            break

        current_pos += sub_sub_length

    # If no sub-sub lord found, use sub lord
    if not sub_sub_lord:
        sub_sub_lord = sub_lord

    # Format the KP pointer as Sign-Star-Sub-SubSub
    sign_abbr = PLANET_ABBR.get(sign_lord, sign_lord[:3])
    star_abbr = PLANET_ABBR.get(star_lord, star_lord[:3])
    sub_abbr = PLANET_ABBR.get(sub_lord, sub_lord[:3])
    sub_sub_abbr = PLANET_ABBR.get(sub_sub_lord, sub_sub_lord[:3])

    # Format the KP pointer
    kp_pointer = f"{sign_abbr}-{star_abbr}-{sub_abbr}-{sub_sub_abbr}"

    return {
        'sign_lord': sign_lord,
        'star_lord': star_lord,
        'sub_lord': sub_lord,
        'sub_sub_lord': sub_sub_lord,
        'kp_pointer': kp_pointer
    }

def format_position(longitude):
    """Format longitude as sign, degrees, minutes, seconds"""
    # Calculate sign (0-11)
    sign_num = int(longitude / 30) % 12
    sign_names = ["Ari", "Tau", "Gem", "Can", "Leo", "Vir", "Lib", "Sco", "Sag", "Cap", "Aqu", "Pis"]
    sign = sign_names[sign_num]
    
    # Calculate position within sign
    pos_in_sign = longitude % 30
    degrees = int(pos_in_sign)
    minutes_float = (pos_in_sign - degrees) * 60
    minutes = int(minutes_float)
    seconds = int((minutes_float - minutes) * 60)
    
    return f"{degrees:02d}° {sign} {minutes:02d}' {seconds:02d}\""

def get_chart(custom_date=None, custom_time=None):
    """Get chart for specified time and location
    
    Args:
        custom_date (str, optional): Date in format 'YYYY/MM/DD'. Defaults to current date.
        custom_time (str, optional): Time in format 'HH:MM'. Defaults to current time.
    
    Returns:
        Chart: Astrovedic chart object
    """
    # Get current time in UTC if no custom date/time provided
    now = datetime.datetime.now()
    
    if custom_date and custom_time:
        # Use custom date and time
        date_str = custom_date
        time_str = custom_time
        offset_str = "+05:30"  # Indian Standard Time
    else:
        # Format current time for flatlib
        date_str = now.strftime("%Y/%m/%d")
        time_str = now.strftime("%H:%M")
        offset_str = "+05:30"  # Indian Standard Time
    
    # Create flatlib datetime
    date = Datetime(date_str, time_str, offset_str)
    
    # Use Bangalore, India as the location
    pos = GeoPos('12n58', '77e35')  # Bangalore coordinates
    
    # Use Placidus house system with Krishnamurti ayanamsa to match the reference
    return Chart(date, pos, hsys=const.HOUSES_PLACIDUS, houses_offset=const.MODERN_HOUSE_OFFSET, mode=const.AY_KRISHNAMURTI)

def main():
    """Main function"""
    # Check for help flag
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help"]:
        print("KP Astrology Chart Generator")
        print("Usage:")
        print("  python kp_astrology.py                   # Generate chart for current time")
        print("  python kp_astrology.py YYYY/MM/DD HH:MM  # Generate chart for specific date and time")
        print("  python kp_astrology.py -h, --help        # Show this help message")
        print("\nExample:")
        print("  python kp_astrology.py 2025/04/09 20:51")
        return
    
    # Check if custom date and time are provided as command line arguments
    if len(sys.argv) == 3:
        custom_date = sys.argv[1]  # Format: YYYY/MM/DD
        custom_time = sys.argv[2]  # Format: HH:MM
        try:
            chart = get_chart(custom_date, custom_time)
            print(f"Generating KP chart for {custom_date} {custom_time} in Bangalore, India\n")
        except Exception as e:
            print(f"Error: {e}")
            print("Please use the format: YYYY/MM/DD HH:MM (e.g., 2025/04/09 20:51)")
            return
    else:
        # Use current date and time
        chart = get_chart()
        print(f"Generating KP chart for current time in Bangalore, India\n")
    
    # List of planets to display
    planets = [
        const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS,
        const.JUPITER, const.SATURN, const.RAHU, const.KETU
    ]
    
    # First pass: collect all planet data
    planets_data = {}
    for planet_id in planets:
        planet = chart.getObject(planet_id)
        
        planets_data[planet_id] = {
            'lon': planet.lon,
            'lat': planet.lat,
            'sign': planet.sign,
            'signlon': planet.signlon
        }
    
    # Prepare data for table
    table_data = []
    
    for planet_id in planets:
        # Use the regular planet
        planet = chart.getObject(planet_id)
        
        # Find which house contains the planet
        house = chart.houses.getHouseByLon(planet.lon)
        
        # Get KP lords information (sign, star, sub, sub-sub)
        kp_info = get_kp_lords(planet.lon)
        
        # Format position like in the reference panchang
        position = f"{int(planet.signlon):02d}° {planet.sign[:3]} {int(planet.signlon % 1 * 60):02d}' {int(planet.signlon % 1 * 60 % 1 * 60):02d}\""
        
        # Use the house number from astrovedic's calculation
        house_num = house.num() if house else 0
        
        # Use the calculated KP pointer
        kp_pointer = kp_info['kp_pointer']
        
        # Add to table data
        table_data.append([
            planet.id,
            position,
            f"House {house_num}",
            kp_pointer
        ])
    
    # Print planet table
    headers = ["Planet", "Position", "House", "KP Pointer"]
    print("Planet Positions")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    # Add house positions
    house_data = []
    
    # Add Ascendant
    asc = chart.getAngle(const.ASC)
    asc_position = f"{int(asc.signlon):02d}° {asc.sign[:3]} {int(asc.signlon % 1 * 60):02d}' {int(asc.signlon % 1 * 60 % 1 * 60):02d}\""
    asc_kp_info = get_kp_lords(asc.lon)
    house_data.append(["Ascendant", asc_position, "House 1", asc_kp_info['kp_pointer']])
    
    # Add house cusps
    for i in range(1, 13):
        house_id = f'House{i}'
        house = chart.getHouse(house_id)
        house_position = f"{int(house.signlon):02d}° {house.sign[:3]} {int(house.signlon % 1 * 60):02d}' {int(house.signlon % 1 * 60 % 1 * 60):02d}\""
        house_kp_info = get_kp_lords(house.lon)
        house_data.append([f"House {i}", house_position, f"House {i}", house_kp_info['kp_pointer']])
    
    # Print house table
    print("\nHouse Positions")
    print(tabulate(house_data, headers=headers, tablefmt="grid"))
    
    # Print chart information
    print(f"\nChart Information:")
    print(f"Date and Time: {chart.date}")
    print(f"Location: Bangalore, India ({chart.pos})")
    print(f"Ayanamsa: Krishnamurti (KP System)")
    print(f"\nNote: This is a KP (Krishnamurti Paddhati) astrology chart with:")
    print(f"- Nakshatras divided into 27 equal parts of 13°20' each")
    print(f"- Each Nakshatra divided into 4 padas (quarters)")
    print(f"- Sub-divisions based on the KP system")
    print(f"- Placidus house system")

if __name__ == "__main__":
    main()
