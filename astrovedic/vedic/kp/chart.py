"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module implements a KP-specific chart wrapper that adds support
    for numeric house keys, which are required by the KP module.
"""

from astrovedic.chart import Chart
from astrovedic.lists import HouseList, GenericList


class KPHouseList(HouseList):
    """A wrapper around HouseList that adds support for numeric keys."""

    def __init__(self, house_list):
        """Initialize from an existing HouseList."""
        self.content = house_list.content.copy()
        
        # Add numeric keys for houses
        for house in self:
            if house.id.startswith('House'):
                try:
                    # Extract the house number from the ID (e.g., 'House1' -> 1)
                    house_num = int(house.id[5:])
                    self.content[house_num] = house
                except (ValueError, IndexError):
                    pass


class KPChart:
    """A wrapper around Chart that adds KP-specific functionality."""

    def __init__(self, chart):
        """Initialize from an existing Chart."""
        self.chart = chart
        self.date = chart.date
        self.pos = chart.pos
        self.hsys = chart.hsys
        self.orbs = chart.orbs
        self.mode = chart.mode
        self.houses_offset = chart.houses_offset
        
        # Wrap the houses list with KPHouseList
        self.houses = KPHouseList(chart.houses)
        
        # Keep references to the original objects and angles
        self.objects = chart.objects
        self.angles = chart.angles

    def getObject(self, ID):
        """Returns an object from the chart."""
        return self.chart.getObject(ID)

    def getHouse(self, ID):
        """Returns a house from the chart."""
        return self.houses.get(ID)

    def getAngle(self, ID):
        """Returns an angle from the chart."""
        return self.chart.getAngle(ID)

    def get(self, ID):
        """Returns an object, house or angle from the chart."""
        return self.chart.get(ID)


def create_kp_chart(date, pos, **kwargs):
    """Create a KP-compatible chart."""
    chart = Chart(date, pos, **kwargs)
    return KPChart(chart)
