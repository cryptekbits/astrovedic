"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module provides a unified API for accessing Vedic astrology features.
    It serves as a high-level interface to all the Vedic modules in astrovedic.
"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from datetime import datetime, timezone, timedelta

# Import from Vedic modules
from astrovedic.vedic import (
    DEFAULT_AYANAMSA, DEFAULT_HOUSE_SYSTEM,
    DEFAULT_KP_AYANAMSA, DEFAULT_KP_HOUSE_SYSTEM
)

# Import from Nakshatra module
from astrovedic.vedic.nakshatras import (
    get_nakshatra, get_nakshatra_lord, get_nakshatra_pada,
    get_nakshatra_degree, get_nakshatra_qualities
)

# Import from Panchang module
from astrovedic.vedic.panchang import (
    get_tithi, get_karana, get_yoga, get_vara,
    get_panchang, get_hora
)

# Import from Upagrah module
from astrovedic.vedic.upagrah import (
    get_upagrah, get_gulika, get_mandi, get_upagrah_positions
)

# Import from Vimshottari module
from astrovedic.vedic.vimshottari import (
    get_dasha_balance, get_mahadasha, get_antardasha,
    get_pratyantardasha, get_current_dasha
)

# Import from KP module
from astrovedic.vedic.kp import (
    get_kp_planets, get_kp_houses, get_kp_significators,
    get_kp_cusps, get_kp_sublords, get_kp_ruling_planets
)

# Import from Vargas module
from astrovedic.vedic.vargas import (
    get_varga_chart, get_varga_positions, analyze_varga_charts,
    get_basic_varga_analysis
)

# Note: For detailed analysis, use the astroved_extension package

# Import from Shadbala module
from astrovedic.vedic.shadbala import get_shadbala

# Note: For detailed analysis, use the astroved_extension package

# Import from Ashtakavarga module
from astrovedic.vedic.ashtakavarga import (
    get_bhinnashtakavarga, get_sarvashtakavarga, get_all_ashtakavarga,
    get_basic_ashtakavarga_analysis
)

# Note: For detailed analysis, use the astroved_extension package

# Import from Yogas module
from astrovedic.vedic.yogas import (
    get_yogas, get_basic_yoga_analysis
)

# Note: For detailed analysis, use the astroved_extension package

# Import from Muhurta module
from astrovedic.vedic.muhurta import (
    get_muhurta_for_date, get_best_muhurta_for_activity,
    get_basic_muhurta_analysis
)

# Note: For detailed analysis, use the astroved_extension package

# Import from Sarvatobhadra module
from astrovedic.vedic.sarvatobhadra import (
    get_sarvatobhadra_for_date, get_best_direction_for_activity,
    get_tara_bala_for_date, get_basic_sarvatobhadra_analysis
)

# Note: For detailed analysis, use the astroved_extension package

# Import from Transits module
from astrovedic.vedic.transits import (
    get_transits, get_transit_predictions_for_date,
    get_transit_timeline_for_period, get_basic_transit_analysis
)

# Note: For detailed analysis, use the astroved_extension package

# Import from Compatibility module
from astrovedic.vedic.compatibility import (
    get_compatibility, get_basic_compatibility_analysis
)

# Note: For detailed analysis, use the astroved_extension package


class VedicChart:
    """
    A class that provides a unified interface for Vedic astrology calculations.
    It wraps a flatlib Chart object and provides methods for all Vedic features.
    """

    def __init__(self, chart, ayanamsa=DEFAULT_AYANAMSA):
        """
        Initialize a VedicChart object.

        Args:
            chart (Chart): A flatlib Chart object
            ayanamsa (str, optional): The ayanamsa to use. Defaults to DEFAULT_AYANAMSA.
        """
        self.chart = chart
        self.ayanamsa = ayanamsa

    @classmethod
    def from_data(cls, date, pos, hsys=DEFAULT_HOUSE_SYSTEM, ayanamsa=DEFAULT_AYANAMSA):
        """
        Create a VedicChart from date and position data.

        Args:
            date (Datetime): A flatlib Datetime object
            pos (GeoPos): A flatlib GeoPos object
            hsys (str, optional): The house system to use. Defaults to DEFAULT_HOUSE_SYSTEM.
            ayanamsa (str, optional): The ayanamsa to use. Defaults to DEFAULT_AYANAMSA.

        Returns:
            VedicChart: A VedicChart object
        """
        chart = Chart(date, pos, hsys=hsys, mode=ayanamsa)
        return cls(chart, ayanamsa)

    @classmethod
    def from_date_place(cls, date_str, time_str, lat, lon, timezone="+00:00",
                        hsys=DEFAULT_HOUSE_SYSTEM, ayanamsa=DEFAULT_AYANAMSA):
        """
        Create a VedicChart from date, time, and location.

        Args:
            date_str (str): Date in format 'YYYY/MM/DD'
            time_str (str): Time in format 'HH:MM'
            lat (float): Latitude
            lon (float): Longitude
            timezone (str, optional): Timezone in format '+/-HH:MM'. Defaults to "+00:00".
            hsys (str, optional): The house system to use. Defaults to DEFAULT_HOUSE_SYSTEM.
            ayanamsa (str, optional): The ayanamsa to use. Defaults to DEFAULT_AYANAMSA.

        Returns:
            VedicChart: A VedicChart object
        """
        date = Datetime(date_str, time_str, timezone)
        pos = GeoPos(lat, lon)
        return cls.from_data(date, pos, hsys, ayanamsa)

    @classmethod
    def kp_chart(cls, date, pos, hsys=DEFAULT_KP_HOUSE_SYSTEM, ayanamsa=DEFAULT_KP_AYANAMSA):
        """
        Create a KP (Krishnamurti Paddhati) chart.

        Args:
            date (Datetime): A flatlib Datetime object
            pos (GeoPos): A flatlib GeoPos object
            hsys (str, optional): The house system to use. Defaults to DEFAULT_KP_HOUSE_SYSTEM.
            ayanamsa (str, optional): The ayanamsa to use. Defaults to DEFAULT_KP_AYANAMSA.

        Returns:
            VedicChart: A VedicChart object configured for KP
        """
        chart = Chart(date, pos, hsys=hsys, mode=ayanamsa)
        return cls(chart, ayanamsa)

    # Basic chart information methods
    def get_planet(self, planet_id):
        """
        Get a planet from the chart.

        Args:
            planet_id (str): The ID of the planet

        Returns:
            Object: The planet object
        """
        return self.chart.getObject(planet_id)

    def get_house(self, house_num):
        """
        Get a house from the chart.

        Args:
            house_num (int): The house number (1-12)

        Returns:
            Object: The house object
        """
        return self.chart.getHouse(house_num)

    def get_ascendant(self):
        """
        Get the ascendant from the chart.

        Returns:
            Object: The ascendant object
        """
        return self.chart.getAngle(const.ASC)

    # Nakshatra methods
    def get_nakshatra(self, planet_id):
        """
        Get the nakshatra of a planet.

        Args:
            planet_id (str): The ID of the planet

        Returns:
            dict: Dictionary with nakshatra information
        """
        if planet_id in const.LIST_ANGLES:
            # Handle angles like Ascendant
            astro_object = self.chart.getAngle(planet_id)
        else:
            # Handle planets and other objects
            astro_object = self.get_planet(planet_id)
            
        if astro_object is None:
            # Or raise an error, depending on desired behavior
            return None
            
        return get_nakshatra(astro_object.lon)

    def get_nakshatra_lord(self, planet_id):
        """
        Get the nakshatra lord of a planet.

        Args:
            planet_id (str): The ID of the planet

        Returns:
            str: The nakshatra lord
        """
        planet = self.get_planet(planet_id)
        return get_nakshatra_lord(planet)

    def get_nakshatra_pada(self, planet_id):
        """
        Get the nakshatra pada of a planet.

        Args:
            planet_id (str): The ID of the planet

        Returns:
            int: The nakshatra pada (1-4)
        """
        planet = self.get_planet(planet_id)
        return get_nakshatra_pada(planet)

    # Panchang methods
    def get_panchang(self):
        """
        Calculate complete Panchang for the chart's date and location
        
        Returns:
            dict: Dictionary with complete Panchang information
        """
        return get_panchang(self.chart.date.jd, self.chart.pos.lat, self.chart.pos.lon, self.chart.date.utcoffset, ayanamsa=self.ayanamsa)

    def get_tithi(self):
        """
        Get the tithi for the chart date.

        Returns:
            dict: Dictionary with tithi information
        """
        return get_tithi(self.chart)

    def get_karana(self):
        """
        Get the karana for the chart date.

        Returns:
            dict: Dictionary with karana information
        """
        return get_karana(self.chart)

    def get_yoga(self):
        """
        Get the yoga for the chart date.

        Returns:
            dict: Dictionary with yoga information
        """
        return get_yoga(self.chart)

    def get_vara(self):
        """
        Get the vara (weekday) for the chart date.

        Returns:
            dict: Dictionary with vara information
        """
        return get_vara(self.chart)

    # Upagrah methods
    def get_upagrah_positions(self):
        """
        Get the positions of all upagrah (shadow planets).

        Returns:
            dict: Dictionary with upagrah positions
        """
        return get_upagrah_positions(self.chart)

    def get_gulika(self):
        """
        Get the position of Gulika.

        Returns:
            dict: Dictionary with Gulika information
        """
        return get_gulika(self.chart)

    def get_mandi(self):
        """
        Get the position of Mandi.

        Returns:
            dict: Dictionary with Mandi information
        """
        return get_mandi(self.chart)

    # Vimshottari Dasha methods
    def get_dasha_balance(self):
        """
        Get the dasha balance at birth.

        Returns:
            dict: Dictionary with dasha balance information
        """
        return get_dasha_balance(self.chart)

    def get_current_dasha(self, date=None):
        """
        Get the current dasha.

        Args:
            date (Datetime, optional): The date to calculate for. Defaults to None (current date).

        Returns:
            dict: Dictionary with current dasha information
        """
        return get_current_dasha(self.chart, date)

    def get_dasha_timeline(self, levels=3, start_date=None, end_date=None):
        """
        Get the dasha timeline.

        Args:
            levels (int, optional): The number of dasha levels to include. Defaults to 3.
            start_date (Datetime, optional): The start date. Defaults to None (birth date).
            end_date (Datetime, optional): The end date. Defaults to None (120 years from birth).

        Returns:
            list: List of dasha periods
        """
        if levels == 1:
            return get_mahadasha(self.chart, start_date, end_date)
        elif levels == 2:
            return get_antardasha(self.chart, start_date, end_date)
        elif levels == 3:
            return get_pratyantardasha(self.chart, start_date, end_date)
        else:
            raise ValueError("Invalid dasha levels. Must be 1, 2, or 3.")

    # KP methods
    def get_kp_planets(self):
        """
        Get KP planet information.

        Returns:
            dict: Dictionary with KP planet information
        """
        return get_kp_planets(self.chart)

    def get_kp_houses(self):
        """
        Get KP house information.

        Returns:
            dict: Dictionary with KP house information
        """
        return get_kp_houses(self.chart)

    def get_kp_significators(self, house_num):
        """
        Get KP significators for a house.

        Args:
            house_num (int): The house number (1-12)

        Returns:
            dict: Dictionary with KP significator information
        """
        return get_kp_significators(self.chart, house_num)

    def get_kp_ruling_planets(self):
        """
        Get KP ruling planets.

        Returns:
            dict: Dictionary with KP ruling planet information
        """
        return get_kp_ruling_planets(self.chart)

    # Varga methods
    def get_varga_chart(self, varga):
        """
        Get a divisional chart.

        Args:
            varga (str): The varga (divisional chart) to get

        Returns:
            Chart: The divisional chart
        """
        return get_varga_chart(self.chart, varga)

    def get_varga_positions(self, varga):
        """
        Get planet positions in a divisional chart.

        Args:
            varga (str): The varga (divisional chart) to get

        Returns:
            dict: Dictionary with planet positions in the divisional chart
        """
        return get_varga_positions(self.chart, varga)

    def analyze_vargas(self):
        """
        Analyze Varga charts (divisional charts).
        Note: For detailed analysis, use the astroved_extension package

        Returns:
            dict: Dictionary with basic Varga analysis
        """
        return analyze_varga_charts(self.chart)

    # Shadbala methods
    def get_shadbala(self, planet_id):
        """
        Get Shadbala (six-fold strength) for a specific planet.

        Args:
            planet_id (str): The ID of the planet (e.g., const.SUN).

        Returns:
            dict: Dictionary with Shadbala information for the specified planet.
        """
        return get_shadbala(self.chart, planet_id)

    def analyze_shadbala(self):
        """
        Analyze Shadbala (six-fold strength).
        Note: For detailed analysis, use the astroved_extension package

        Returns:
            dict: Dictionary with basic Shadbala analysis
        """
        return get_basic_shadbala_analysis(self.chart)

    def get_planet_strength(self, planet_id):
        """
        Get the strength of a planet.

        Args:
            planet_id (str): The ID of the planet

        Returns:
            dict: Dictionary with planet strength information
        """
        return get_planet_strength(self.chart, planet_id)

    def get_house_strength(self, house_num):
        """
        Get the strength of a house.

        Args:
            house_num (int): The house number (1-12)

        Returns:
            dict: Dictionary with house strength information
        """
        return get_house_strength(self.chart, house_num)

    # Ashtakavarga methods
    def get_ashtakavarga(self, planet_id=None):
        """
        Get Ashtakavarga information.

        Args:
            planet_id (str, optional): The ID of the planet. Defaults to None (all planets).

        Returns:
            dict: Dictionary with Ashtakavarga information
        """
        if planet_id:
            return get_bhinnashtakavarga(self.chart, planet_id)
        else:
            return get_all_ashtakavarga(self.chart)

    def get_sarvashtakavarga(self):
        """
        Get Sarvashtakavarga (combined Ashtakavarga) information.

        Returns:
            dict: Dictionary with Sarvashtakavarga information
        """
        return get_sarvashtakavarga(self.chart)

    def analyze_ashtakavarga(self):
        """
        Analyze Ashtakavarga.
        Note: For detailed analysis, use the astroved_extension package

        Returns:
            dict: Dictionary with basic Ashtakavarga analysis
        """
        return get_basic_ashtakavarga_analysis(self.chart)

    # Yoga methods
    def get_yogas(self):
        """
        Get all yogas (planetary combinations) in the chart.
        Note: For detailed analysis, use the astroved_extension package

        Returns:
            dict: Dictionary with basic yoga information
        """
        return get_yogas(self.chart)

    def get_yoga_analysis(self):
        """
        Get basic yoga analysis for the chart.
        Note: For detailed analysis, use the astroved_extension package

        Returns:
            dict: Dictionary with basic yoga analysis
        """
        return get_basic_yoga_analysis(self.chart)

    # Muhurta methods
    def get_muhurta(self, date=None):
        """
        Get Muhurta information for a specific date.
        Note: For detailed analysis, use the astroved_extension package

        Args:
            date (Datetime, optional): The date to check. Defaults to None (chart date).

        Returns:
            dict: Dictionary with basic Muhurta information
        """
        if date is None:
            date = self.chart.date

        return get_muhurta_for_date(date, self.chart.pos)

    def get_best_muhurta(self, activity, start_date=None, end_date=None):
        """
        Get the best Muhurta for a specific activity.
        Note: For detailed analysis, use the astroved_extension package

        Args:
            activity (str): The activity to check
            start_date (Datetime, optional): The start date. Defaults to None (chart date).
            end_date (Datetime, optional): The end date. Defaults to None (7 days from start).

        Returns:
            dict: Dictionary with best Muhurta information
        """
        if start_date is None:
            start_date = self.chart.date

        return get_best_muhurta_for_activity(start_date, end_date, self.chart.pos, activity)

    # Sarvatobhadra methods
    def get_sarvatobhadra(self, date=None):
        """
        Get Sarvatobhadra Chakra information for a specific date.
        Note: For detailed analysis, use the astroved_extension package

        Args:
            date (Datetime, optional): The date to check. Defaults to None (chart date).

        Returns:
            dict: Dictionary with basic Sarvatobhadra Chakra information
        """
        if date is None:
            date = self.chart.date

        return get_sarvatobhadra_for_date(date, self.chart.pos)

    def get_best_direction(self, activity, date=None):
        """
        Get the best direction for a specific activity.
        Note: For detailed analysis, use the astroved_extension package

        Args:
            activity (str): The activity to check
            date (Datetime, optional): The date to check. Defaults to None (chart date).

        Returns:
            dict: Dictionary with best direction information
        """
        if date is None:
            date = self.chart.date

        return get_best_direction_for_activity(date, self.chart.pos, activity)

    def get_tara_bala(self, date=None):
        """
        Get Tara Bala (lunar strength) information for a specific date.
        Note: For detailed analysis, use the astroved_extension package

        Args:
            date (Datetime, optional): The date to check. Defaults to None (chart date).

        Returns:
            dict: Dictionary with Tara Bala information
        """
        if date is None:
            date = self.chart.date

        return get_tara_bala_for_date(date, self.chart.pos)

    # Transit methods
    def get_transits(self, transit_date=None):
        """
        Get transit information for a specific date.
        Note: For detailed analysis, use the astroved_extension package

        Args:
            transit_date (Datetime, optional): The transit date. Defaults to None (current date).

        Returns:
            dict: Dictionary with basic transit information
        """
        if transit_date is None:
            now = datetime.now(timezone.utc)
            utc_offset_str = str(timedelta(seconds=now.utcoffset().total_seconds())).split('.')[0]
            transit_date = Datetime(now.strftime('%Y/%m/%d'), now.strftime('%H:%M:%S'), utc_offset_str)

        return get_transits(self.chart, transit_date)

    def get_transit_predictions(self, transit_date=None):
        """
        Get transit predictions for a specific date.
        Note: For detailed analysis, use the astroved_extension package

        Args:
            transit_date (Datetime, optional): The transit date. Defaults to None (current date).

        Returns:
            dict: Dictionary with basic transit predictions
        """
        if transit_date is None:
            now = datetime.now(timezone.utc)
            utc_offset_str = str(timedelta(seconds=now.utcoffset().total_seconds())).split('.')[0]
            transit_date = Datetime(now.strftime('%Y/%m/%d'), now.strftime('%H:%M:%S'), utc_offset_str)

        return get_transit_predictions_for_date(self.chart, transit_date)

    def get_transit_timeline(self, start_date=None, end_date=None):
        """
        Get transit timeline for a specific period.
        Note: For detailed analysis, use the astroved_extension package

        Args:
            start_date (Datetime, optional): The start date. Defaults to None (current date).
            end_date (Datetime, optional): The end date. Defaults to None (1 year from start).

        Returns:
            dict: Dictionary with basic transit timeline information
        """
        if start_date is None:
            now = datetime.now(timezone.utc)
            utc_offset_str = str(timedelta(seconds=now.utcoffset().total_seconds())).split('.')[0]
            start_date = Datetime(now.strftime('%Y/%m/%d'), now.strftime('%H:%M:%S'), utc_offset_str)

        return get_transit_timeline_for_period(self.chart, start_date, end_date)

    # Compatibility methods
    def get_compatibility(self, other_chart):
        """
        Get compatibility with another chart.
        Note: For detailed analysis, use the astroved_extension package

        Args:
            other_chart (Chart or VedicChart): The other chart

        Returns:
            dict: Dictionary with basic compatibility information
        """
        if isinstance(other_chart, VedicChart):
            other_chart = other_chart.chart
        return get_compatibility(self.chart, other_chart)

    def get_compatibility_analysis(self, other_chart):
        """
        Get basic compatibility analysis with another chart.
        Note: For detailed analysis, use the astroved_extension package

        Args:
            other_chart (Chart or VedicChart): The other chart

        Returns:
            dict: Dictionary with basic compatibility analysis
        """
        if isinstance(other_chart, VedicChart):
            other_chart = other_chart.chart
        return get_basic_compatibility_analysis(self.chart, other_chart)


def create_vedic_chart(date_str, time_str, lat, lon, timezone="+00:00",
                      hsys=DEFAULT_HOUSE_SYSTEM, ayanamsa=DEFAULT_AYANAMSA):
    """
    Create a VedicChart from date, time, and location.

    Args:
        date_str (str): Date in format 'YYYY/MM/DD'
        time_str (str): Time in format 'HH:MM'
        lat (float): Latitude
        lon (float): Longitude
        timezone (str, optional): Timezone in format '+/-HH:MM'. Defaults to "+00:00".
        hsys (str, optional): The house system to use. Defaults to DEFAULT_HOUSE_SYSTEM.
        ayanamsa (str, optional): The ayanamsa to use. Defaults to DEFAULT_AYANAMSA.

    Returns:
        VedicChart: A VedicChart object
    """
    return VedicChart.from_date_place(date_str, time_str, lat, lon, timezone, hsys, ayanamsa)


def create_kp_chart(date_str, time_str, lat, lon, timezone="+00:00",
                   hsys=DEFAULT_KP_HOUSE_SYSTEM, ayanamsa=DEFAULT_KP_AYANAMSA):
    """
    Create a KP (Krishnamurti Paddhati) chart from date, time, and location.

    Args:
        date_str (str): Date in format 'YYYY/MM/DD'
        time_str (str): Time in format 'HH:MM'
        lat (float): Latitude
        lon (float): Longitude
        timezone (str, optional): Timezone in format '+/-HH:MM'. Defaults to "+00:00".
        hsys (str, optional): The house system to use. Defaults to DEFAULT_KP_HOUSE_SYSTEM.
        ayanamsa (str, optional): The ayanamsa to use. Defaults to DEFAULT_KP_AYANAMSA.

    Returns:
        VedicChart: A VedicChart object configured for KP
    """
    date = Datetime(date_str, time_str, timezone)
    pos = GeoPos(lat, lon)
    return VedicChart.kp_chart(date, pos, hsys, ayanamsa)
