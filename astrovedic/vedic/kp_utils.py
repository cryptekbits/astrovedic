"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module provides utility functions for KP (Krishnamurti Paddhati) astrology.
    It includes wrapper functions that avoid circular imports.
"""

from astrovedic.chart import Chart
from astrovedic.lists import HouseList
from astrovedic.vedic.kp import (
    get_kp_sublord, get_kp_sub_sublord, get_kp_pointer, get_kp_lords,
    get_kp_planets, get_kp_houses, get_kp_significators, get_kp_ruling_planets
)


class KPHouseList(HouseList):
    """A wrapper around HouseList that adds support for numeric keys."""

    def __init__(self, house_list):
        """Initialize from an existing HouseList."""
        self.content = house_list.content.copy()
        
        # Add numeric keys for houses
        houses_to_add = {}
        for house in list(self):
            if house.id.startswith('House'):
                try:
                    # Extract the house number from the ID (e.g., 'House1' -> 1)
                    house_num = int(house.id[5:])
                    houses_to_add[house_num] = house
                except (ValueError, IndexError):
                    pass
                    
        # Update the content with numeric keys
        self.content.update(houses_to_add)


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


# Wrapper functions for KP calculations that use the KPChart
def get_kp_sublord_wrapper(longitude):
    """Wrapper for get_kp_sublord."""
    return get_kp_sublord(longitude)


def get_kp_sub_sublord_wrapper(longitude):
    """Wrapper for get_kp_sub_sublord."""
    return get_kp_sub_sublord(longitude)


def get_kp_pointer_wrapper(longitude):
    """Wrapper for get_kp_pointer."""
    return get_kp_pointer(longitude)


def get_kp_lords_wrapper(longitude):
    """Wrapper for get_kp_lords."""
    return get_kp_lords(longitude)


def get_kp_planets_wrapper(chart):
    """Wrapper for get_kp_planets."""
    if isinstance(chart, KPChart):
        return get_kp_planets(chart)
    else:
        kp_chart = create_kp_chart(chart.date, chart.pos, hsys=chart.hsys, mode=chart.mode)
        return get_kp_planets(kp_chart)


def get_kp_houses_wrapper(chart):
    """Wrapper for get_kp_houses."""
    if isinstance(chart, KPChart):
        return get_kp_houses(chart)
    else:
        kp_chart = create_kp_chart(chart.date, chart.pos, hsys=chart.hsys, mode=chart.mode)
        return get_kp_houses(kp_chart)


def get_kp_significators_wrapper(chart, house_num):
    """Wrapper for get_kp_significators."""
    if isinstance(chart, KPChart):
        return get_kp_significators(chart, house_num)
    else:
        kp_chart = create_kp_chart(chart.date, chart.pos, hsys=chart.hsys, mode=chart.mode)
        return get_kp_significators(kp_chart, house_num)


def get_kp_ruling_planets_wrapper(chart):
    """Wrapper for get_kp_ruling_planets."""
    if isinstance(chart, KPChart):
        return get_kp_ruling_planets(chart)
    else:
        kp_chart = create_kp_chart(chart.date, chart.pos, hsys=chart.hsys, mode=chart.mode)
        return get_kp_ruling_planets(kp_chart)
