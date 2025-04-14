"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Sarvatobhadra Chakra construction
    for Vedic astrology.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos


def create_chakra(janma_nakshatra):
    """
    Create the Sarvatobhadra Chakra based on the birth nakshatra
    
    Args:
        janma_nakshatra (int): The birth nakshatra number (1-27)
    
    Returns:
        dict: Dictionary with Sarvatobhadra Chakra information
    """
    # Initialize the 9x9 grid
    grid = [[0 for _ in range(9)] for _ in range(9)]
    
    # Fill the grid with nakshatras
    grid = fill_chakra_grid(grid, janma_nakshatra)
    
    # Create the chakra dictionary
    chakra = {
        'janma_nakshatra': janma_nakshatra,
        'grid': grid
    }
    
    return chakra


def fill_chakra_grid(grid, janma_nakshatra):
    """
    Fill the Sarvatobhadra Chakra grid with nakshatras
    
    Args:
        grid (list): The 9x9 grid
        janma_nakshatra (int): The birth nakshatra number (1-27)
    
    Returns:
        list: The filled 9x9 grid
    """
    # The Sarvatobhadra Chakra is filled in a specific pattern
    # Starting from the center (4, 4) with the birth nakshatra
    
    # Define the filling pattern
    pattern = [
        (4, 4), (4, 5), (3, 5), (3, 4), (3, 3), (4, 3), (5, 3), (5, 4), (5, 5),
        (5, 6), (4, 6), (3, 6), (2, 6), (2, 5), (2, 4), (2, 3), (2, 2), (3, 2),
        (4, 2), (5, 2), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (5, 7),
        (4, 7), (3, 7), (2, 7), (1, 7), (1, 6), (1, 5), (1, 4), (1, 3), (1, 2),
        (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (7, 2), (7, 3),
        (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (6, 8), (5, 8), (4, 8), (3, 8),
        (2, 8), (1, 8), (0, 8), (0, 7), (0, 6), (0, 5), (0, 4), (0, 3), (0, 2),
        (0, 1), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
        (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8)
    ]
    
    # Fill the grid according to the pattern
    for i, (row, col) in enumerate(pattern):
        # Calculate the nakshatra for this position
        nakshatra = ((janma_nakshatra - 1 + i) % 27) + 1
        
        # Fill the grid
        grid[row][col] = nakshatra
    
    return grid


def get_chakra_cell(chakra, row, col):
    """
    Get the nakshatra in a specific cell of the Sarvatobhadra Chakra
    
    Args:
        chakra (dict): The Sarvatobhadra Chakra
        row (int): The row in the chakra (0-8)
        col (int): The column in the chakra (0-8)
    
    Returns:
        int: The nakshatra number (1-27) in the cell
    """
    # Check if the row and column are valid
    if 0 <= row <= 8 and 0 <= col <= 8:
        return chakra['grid'][row][col]
    
    return None


def get_chakra_row(chakra, row):
    """
    Get a row from the Sarvatobhadra Chakra
    
    Args:
        chakra (dict): The Sarvatobhadra Chakra
        row (int): The row in the chakra (0-8)
    
    Returns:
        list: The nakshatras in the row
    """
    # Check if the row is valid
    if 0 <= row <= 8:
        return chakra['grid'][row]
    
    return None


def get_chakra_column(chakra, col):
    """
    Get a column from the Sarvatobhadra Chakra
    
    Args:
        chakra (dict): The Sarvatobhadra Chakra
        col (int): The column in the chakra (0-8)
    
    Returns:
        list: The nakshatras in the column
    """
    # Check if the column is valid
    if 0 <= col <= 8:
        return [chakra['grid'][row][col] for row in range(9)]
    
    return None


def get_chakra_diagonal(chakra, diagonal_type):
    """
    Get a diagonal from the Sarvatobhadra Chakra
    
    Args:
        chakra (dict): The Sarvatobhadra Chakra
        diagonal_type (str): The type of diagonal ('main' or 'anti')
    
    Returns:
        list: The nakshatras in the diagonal
    """
    if diagonal_type == 'main':
        # Main diagonal (top-left to bottom-right)
        return [chakra['grid'][i][i] for i in range(9)]
    elif diagonal_type == 'anti':
        # Anti-diagonal (top-right to bottom-left)
        return [chakra['grid'][i][8-i] for i in range(9)]
    
    return None


def get_direction_cells(chakra, direction):
    """
    Get the cells in a specific direction of the Sarvatobhadra Chakra
    
    Args:
        chakra (dict): The Sarvatobhadra Chakra
        direction (str): The direction ('North', 'Northeast', etc.)
    
    Returns:
        list: The cells in the direction
    """
    # Define the cells for each direction
    direction_cells = {
        'North': [(0, 4), (1, 4), (2, 4), (3, 4)],
        'Northeast': [(0, 8), (1, 7), (2, 6), (3, 5)],
        'East': [(4, 8), (4, 7), (4, 6), (4, 5)],
        'Southeast': [(8, 8), (7, 7), (6, 6), (5, 5)],
        'South': [(8, 4), (7, 4), (6, 4), (5, 4)],
        'Southwest': [(8, 0), (7, 1), (6, 2), (5, 3)],
        'West': [(4, 0), (4, 1), (4, 2), (4, 3)],
        'Northwest': [(0, 0), (1, 1), (2, 2), (3, 3)],
        'Center': [(4, 4)]
    }
    
    # Return the cells for the specified direction
    return direction_cells.get(direction, [])


def get_nakshatras_in_direction(chakra, direction):
    """
    Get the nakshatras in a specific direction of the Sarvatobhadra Chakra
    
    Args:
        chakra (dict): The Sarvatobhadra Chakra
        direction (str): The direction ('North', 'Northeast', etc.)
    
    Returns:
        list: The nakshatras in the direction
    """
    # Get the cells in the direction
    cells = get_direction_cells(chakra, direction)
    
    # Get the nakshatras in the cells
    nakshatras = [get_chakra_cell(chakra, row, col) for row, col in cells]
    
    return nakshatras


def get_planets_in_direction(chakra, direction):
    """
    Get the planets in a specific direction of the Sarvatobhadra Chakra
    
    Args:
        chakra (dict): The Sarvatobhadra Chakra
        direction (str): The direction ('North', 'Northeast', etc.)
    
    Returns:
        list: The planets in the direction
    """
    # Get the cells in the direction
    cells = get_direction_cells(chakra, direction)
    
    # Get the planets in the cells
    planets = []
    for planet_id, planet_info in chakra['planets'].items():
        position = planet_info['position']
        if position and position in cells:
            planets.append(planet_id)
    
    return planets


def get_nakshatra_name(nakshatra_num):
    """
    Get the name of a nakshatra
    
    Args:
        nakshatra_num (int): The nakshatra number (1-27)
    
    Returns:
        str: The name of the nakshatra
    """
    nakshatra_names = {
        1: 'Ashwini',
        2: 'Bharani',
        3: 'Krittika',
        4: 'Rohini',
        5: 'Mrigashira',
        6: 'Ardra',
        7: 'Punarvasu',
        8: 'Pushya',
        9: 'Ashlesha',
        10: 'Magha',
        11: 'Purva Phalguni',
        12: 'Uttara Phalguni',
        13: 'Hasta',
        14: 'Chitra',
        15: 'Swati',
        16: 'Vishakha',
        17: 'Anuradha',
        18: 'Jyeshtha',
        19: 'Moola',
        20: 'Purva Ashadha',
        21: 'Uttara Ashadha',
        22: 'Shravana',
        23: 'Dhanishta',
        24: 'Shatabhisha',
        25: 'Purva Bhadrapada',
        26: 'Uttara Bhadrapada',
        27: 'Revati'
    }
    
    return nakshatra_names.get(nakshatra_num, '')


def get_nakshatra_lord(nakshatra_num):
    """
    Get the lord of a nakshatra
    
    Args:
        nakshatra_num (int): The nakshatra number (1-27)
    
    Returns:
        str: The lord of the nakshatra
    """
    nakshatra_lords = {
        1: 'Ketu',
        2: 'Venus',
        3: 'Sun',
        4: 'Moon',
        5: 'Mars',
        6: 'Rahu',
        7: 'Jupiter',
        8: 'Saturn',
        9: 'Mercury',
        10: 'Ketu',
        11: 'Venus',
        12: 'Sun',
        13: 'Moon',
        14: 'Mars',
        15: 'Rahu',
        16: 'Jupiter',
        17: 'Saturn',
        18: 'Mercury',
        19: 'Ketu',
        20: 'Venus',
        21: 'Sun',
        22: 'Moon',
        23: 'Mars',
        24: 'Rahu',
        25: 'Jupiter',
        26: 'Saturn',
        27: 'Mercury'
    }
    
    return nakshatra_lords.get(nakshatra_num, '')
