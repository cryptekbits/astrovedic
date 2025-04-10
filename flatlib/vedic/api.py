"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology

    This module provides a unified API for accessing Vedic astrology features.
    It serves as a high-level interface to all the Vedic modules in flatlib.
"""

from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

# Import from Vedic modules
from flatlib.vedic import (
    DEFAULT_AYANAMSA, DEFAULT_HOUSE_SYSTEM,
    DEFAULT_KP_AYANAMSA, DEFAULT_KP_HOUSE_SYSTEM
)

# Import from Nakshatra module
from flatlib.vedic.nakshatras import (
    get_nakshatra, get_nakshatra_lord, get_nakshatra_pada,
    get_nakshatra_degree, get_nakshatra_qualities
)

# Import from Panchang module
from flatlib.vedic.panchang import (
    get_tithi, get_karana, get_yoga, get_vara,
    get_panchang, get_muhurta, get_hora
)

# Import from Upagrah module
from flatlib.vedic.upagrah import (
    get_upagrah, get_gulika, get_mandi, get_upagrah_positions
)

# Import from Vimshottari module
from flatlib.vedic.vimshottari import (
    get_dasha_balance, get_mahadasha, get_antardasha,
    get_pratyantardasha, get_current_dasha
)

# Import from KP module
from flatlib.vedic.kp import (
    get_kp_planets, get_kp_houses, get_kp_significators,
    get_kp_cusps, get_kp_sublords, get_kp_ruling_planets
)

# Import from Vargas module
from flatlib.vedic.vargas import (
    get_varga_chart, get_varga_positions, get_varga_strengths,
    get_varga_analysis, get_all_vargas
)

# Import from Shadbala module
from flatlib.vedic.shadbala import (
    get_shadbala, get_planet_strength, get_house_strength,
    get_ishta_kashta_phala, get_vimsopaka_bala
)

# Import from Ashtakavarga module
from flatlib.vedic.ashtakavarga import (
    get_bhinnashtakavarga, get_sarvashtakavarga, get_all_ashtakavarga,
    get_kaksha_bala, get_transit_ashtakavarga
)

# Import from Yogas module
from flatlib.vedic.yogas import (
    get_yogas, get_raja_yogas, get_dhana_yogas, get_dosha_yogas,
    get_yoga_analysis, get_yoga_strength
)

# Import from Muhurta module
from flatlib.vedic.muhurta import (
    get_auspicious_time, get_inauspicious_time, get_muhurta_quality,
    get_panchanga_shuddhi, get_activity_muhurta
)

# Import from Sarvatobhadra module
from flatlib.vedic.sarvatobhadra import (
    get_sarvatobhadra_chakra, get_auspicious_directions,
    get_tara_bala, get_direction_quality
)

# Import from Transits module
from flatlib.vedic.transits import (
    get_transit_analysis, get_transit_effects, get_transit_timeline,
    get_dasha_transit_analysis, get_transit_predictions
)

# Import from Compatibility module
from flatlib.vedic.compatibility import (
    get_compatibility, get_compatibility_level, get_detailed_compatibility_report,
    get_compatibility_timeline, analyze_charts_compatibility
)


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
        planet = self.get_planet(planet_id)
        return get_nakshatra(planet)

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
        Get the panchang for the chart date.

        Returns:
            dict: Dictionary with panchang information
        """
        return get_panchang(self.chart)

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

    def get_all_vargas(self):
        """
        Get all divisional charts.

        Returns:
            dict: Dictionary with all divisional charts
        """
        return get_all_vargas(self.chart)

    # Shadbala methods
    def get_shadbala(self):
        """
        Get Shadbala (six-fold strength) for all planets.

        Returns:
            dict: Dictionary with Shadbala information
        """
        return get_shadbala(self.chart)

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

    # Yoga methods
    def get_yogas(self):
        """
        Get all yogas (planetary combinations) in the chart.

        Returns:
            dict: Dictionary with yoga information
        """
        return get_yogas(self.chart)

    def get_raja_yogas(self):
        """
        Get Raja Yogas (combinations for power and authority) in the chart.

        Returns:
            dict: Dictionary with Raja Yoga information
        """
        return get_raja_yogas(self.chart)

    def get_dhana_yogas(self):
        """
        Get Dhana Yogas (combinations for wealth) in the chart.

        Returns:
            dict: Dictionary with Dhana Yoga information
        """
        return get_dhana_yogas(self.chart)

    def get_dosha_yogas(self):
        """
        Get Dosha Yogas (combinations indicating difficulties) in the chart.

        Returns:
            dict: Dictionary with Dosha Yoga information
        """
        return get_dosha_yogas(self.chart)

    # Muhurta methods
    def get_muhurta_quality(self, activity=None):
        """
        Get the quality of the current time for a specific activity.

        Args:
            activity (str, optional): The activity to check. Defaults to None (general quality).

        Returns:
            dict: Dictionary with muhurta quality information
        """
        return get_muhurta_quality(self.chart, activity)

    def get_auspicious_time(self, activity, start_date=None, end_date=None):
        """
        Get auspicious times for a specific activity.

        Args:
            activity (str): The activity to check
            start_date (Datetime, optional): The start date. Defaults to None (current date).
            end_date (Datetime, optional): The end date. Defaults to None (7 days from start).

        Returns:
            list: List of auspicious times
        """
        return get_auspicious_time(self.chart, activity, start_date, end_date)

    def get_inauspicious_time(self, start_date=None, end_date=None):
        """
        Get inauspicious times.

        Args:
            start_date (Datetime, optional): The start date. Defaults to None (current date).
            end_date (Datetime, optional): The end date. Defaults to None (7 days from start).

        Returns:
            list: List of inauspicious times
        """
        return get_inauspicious_time(self.chart, start_date, end_date)

    # Sarvatobhadra methods
    def get_sarvatobhadra_chakra(self):
        """
        Get the Sarvatobhadra Chakra.

        Returns:
            dict: Dictionary with Sarvatobhadra Chakra information
        """
        return get_sarvatobhadra_chakra(self.chart)

    def get_auspicious_directions(self, activity=None):
        """
        Get auspicious directions.

        Args:
            activity (str, optional): The activity to check. Defaults to None (general directions).

        Returns:
            dict: Dictionary with auspicious direction information
        """
        return get_auspicious_directions(self.chart, activity)

    # Transit methods
    def get_transit_analysis(self, transit_chart):
        """
        Get transit analysis.

        Args:
            transit_chart (Chart): The transit chart

        Returns:
            dict: Dictionary with transit analysis information
        """
        return get_transit_analysis(self.chart, transit_chart)

    def get_transit_timeline(self, start_date=None, end_date=None):
        """
        Get transit timeline.

        Args:
            start_date (Datetime, optional): The start date. Defaults to None (current date).
            end_date (Datetime, optional): The end date. Defaults to None (1 year from start).

        Returns:
            list: List of transit events
        """
        return get_transit_timeline(self.chart, start_date, end_date)

    def get_dasha_transit_analysis(self, transit_chart):
        """
        Get combined Dasha-Transit analysis.

        Args:
            transit_chart (Chart): The transit chart

        Returns:
            dict: Dictionary with Dasha-Transit analysis information
        """
        return get_dasha_transit_analysis(self.chart, transit_chart)

    # Compatibility methods
    def get_compatibility(self, other_chart):
        """
        Get compatibility with another chart.

        Args:
            other_chart (Chart or VedicChart): The other chart

        Returns:
            dict: Dictionary with compatibility information
        """
        if isinstance(other_chart, VedicChart):
            other_chart = other_chart.chart
        return get_compatibility(self.chart, other_chart)

    def get_detailed_compatibility(self, other_chart):
        """
        Get detailed compatibility with another chart.

        Args:
            other_chart (Chart or VedicChart): The other chart

        Returns:
            dict: Dictionary with detailed compatibility information
        """
        if isinstance(other_chart, VedicChart):
            other_chart = other_chart.chart
        return get_detailed_compatibility_report(self.chart, other_chart)

    def get_compatibility_timeline(self, other_chart, start_date=None, end_date=None):
        """
        Get compatibility timeline with another chart.

        Args:
            other_chart (Chart or VedicChart): The other chart
            start_date (Datetime, optional): The start date. Defaults to None (current date).
            end_date (Datetime, optional): The end date. Defaults to None (1 year from start).

        Returns:
            list: List of compatibility events
        """
        if isinstance(other_chart, VedicChart):
            other_chart = other_chart.chart
        return get_compatibility_timeline(self.chart, other_chart, start_date, end_date)


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
