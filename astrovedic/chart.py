"""
    This file is part of astrovedic - (C) FlatAngle
    Author: João Ventura (flatangleweb@gmail.com)
    Modified for Vedic Astrology


    This module implements a class to represent an
    astrology Chart. It provides methods to handle
    the chart, as well as three relevant properties:

    - objects: a list with the chart's objects
    - houses: a list with the chart's houses
    - angles: a list with the chart's angles

    Since houses 1 and 10 may not match the Asc and
    MC in some house systems, the Chart class
    includes the list of angles. The angles should be
    used when you want to deal with angle's longitudes.

    There are also methods to access fixed stars.

"""

from . import angle
from . import const
from . import utils
from .ephem import ephem
from .datetime import Datetime
from .vedic.ayanamsa import AyanamsaManager
from .vedic.houses import HouseSystemManager
from .vedic.config import ChartConfiguration


# ------------------ #
#    Chart Class     #
# ------------------ #

class Chart:
    """ This class represents an astrology chart. """

    def __init__(self, date, pos, **kwargs):
        """ Creates an astrology chart for a given
        date and location.

        Optional arguments are:
        - hsys: house system
        - ayanamsa: ayanamsa for sidereal zodiac (replaces mode)
        - mode: deprecated, use ayanamsa instead
        - IDs: list of objects to include
        - houses_offset: Offset for including objects in calculed houses.
        - orbs: alternative dict of orbs for using dynamic orbs instead of the default const.LIST_ORBS
        - is_kp: whether this is a KP chart

        """
        # Handle optional arguments
        is_kp = kwargs.get('is_kp', False)

        # Get ayanamsa from kwargs, with backward compatibility for 'mode'
        ayanamsa = kwargs.get('ayanamsa', None)
        if ayanamsa is None and 'mode' in kwargs:
            ayanamsa = kwargs.get('mode')

        # Create and validate configuration
        config = ChartConfiguration(ayanamsa, kwargs.get('hsys'), is_kp)
        config.validate()

        # Get object IDs based on whether we're using an ayanamsa (sidereal zodiac)
        if config.ayanamsa is not None:
            IDs = kwargs.get('IDs', const.LIST_OBJECTS_VEDIC)
        else:
            IDs = kwargs.get('IDs', const.LIST_OBJECTS_TRADITIONAL)

        houses_offset = kwargs.get('houses_offset', const.MODERN_HOUSE_OFFSET)
        orbs = kwargs.get('orbs', const.LIST_ORBS)

        self.date = date
        self.pos = pos
        self.hsys = config.house_system
        self.orbs = orbs
        self.ayanamsa = config.ayanamsa
        # Keep mode for backward compatibility
        self.mode = config.ayanamsa
        self.houses_offset = houses_offset

        if config.ayanamsa:
            self.objects = ephem.get_objects(IDs, date, pos, mode=config.ayanamsa)
            self.houses, self.angles = ephem.get_houses(date, pos, config.house_system, houses_offset, mode=config.ayanamsa)
        else:
            self.objects = ephem.getObjectList(IDs, date, pos)
            self.houses, self.angles = ephem.getHouses(date, pos, config.house_system, houses_offset)

        self.update_objects_orbs()

    def copy(self):
        """ Returns a deep copy of this chart. """
        chart = Chart.__new__(Chart)
        chart.date = self.date
        chart.pos = self.pos
        chart.hsys = self.hsys
        chart.orbs = self.orbs
        chart.ayanamsa = self.ayanamsa if hasattr(self, 'ayanamsa') else None
        chart.mode = self.mode if hasattr(self, 'mode') else None
        chart.houses_offset = self.houses_offset
        chart.objects = self.objects.copy()
        chart.houses = self.houses.copy()
        chart.angles = self.angles.copy()
        return chart

    def move(self, offset):
        """ Moves all items of the chart by an offset. """
        for obj in self.objects:
            obj.relocate(obj.lon + offset)
        for obj in self.houses:
            obj.relocate(obj.lon + offset)
        for obj in self.angles:
            obj.relocate(obj.lon + offset)

    def to_sidereal_zodiac(self, ayanamsa):
        """
        Returns a copy of this chart on the sidereal zodiac.

        Args:
            ayanamsa (str): The ayanamsa to use for the sidereal zodiac.

        Returns:
            Chart: A new chart with positions adjusted for the specified ayanamsa.
        """
        from astrovedic.ephem import swe
        chart = self.copy()
        offset = swe.get_ayanamsa(chart.date.jd, ayanamsa)
        chart.move(-offset)
        chart.ayanamsa = ayanamsa
        chart.mode = ayanamsa  # For backward compatibility
        return chart

    def update_objects_orbs(self):
        """Update the objects orbs if needed"""
        if self.orbs == const.LIST_ORBS:
            return
        for obj in self.objects:
            obj.orbs = self.orbs


    # === Properties === #

    def getObject(self, ID):
        """ Returns an object from the chart. """
        return self.objects.get(ID)

    def getHouse(self, ID):
        """ Returns an house from the chart. """
        return self.houses.get(ID)

    def getAngle(self, ID):
        """ Returns an angle from the chart. """
        return self.angles.get(ID)

    def get(self, ID):
        """ Returns an object, house or angle
        from the chart.

        """
        if ID.startswith('House'):
            return self.getHouse(ID)
        elif ID in const.LIST_ANGLES:
            return self.getAngle(ID)
        else:
            return self.getObject(ID)

    # === Fixed stars === #

    # The computation of fixed stars is inefficient,
    # so the access must be made directly to the
    # ephemeris only when needed.

    def getFixedStar(self, ID):
        """ Returns a fixed star from the ephemeris. """
        return ephem.getFixedStar(ID, self.date)

    def getFixedStars(self):
        """ Returns a list with all fixed stars. """
        IDs = const.LIST_FIXED_STARS
        return ephem.getFixedStarList(IDs, self.date)

    # === Houses and angles === #

    def isHouse1Asc(self):
        """ Returns true if House1 is the same as the Asc. """
        house1 = self.getHouse(const.HOUSE1)
        asc = self.getAngle(const.ASC)
        dist = angle.closestdistance(house1.lon, asc.lon)
        return abs(dist) < 0.0003  # 1 arc-second

    def isHouse10MC(self):
        """ Returns true if House10 is the same as the MC. """
        house10 = self.getHouse(const.HOUSE10)
        mc = self.getAngle(const.MC)
        dist = angle.closestdistance(house10.lon, mc.lon)
        return abs(dist) < 0.0003  # 1 arc-second

    # === Other properties === #

    # Western methods removed (isDiurnal, getMoonPhase, solarReturn)
