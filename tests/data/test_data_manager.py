#!/usr/bin/env python3
"""
Test Data Manager

This module provides a class for managing test data for the flatlib library.
It loads reference data from JSON files and provides methods for accessing it.
"""

import os
import json
from datetime import datetime
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic import const

class TestDataManager:
    """
    Class for managing test data for the flatlib library.

    This class loads reference data from JSON files and provides methods for accessing it.
    It also provides methods for creating charts with the reference data.
    """

    # Reference date and location
    REFERENCE_DATE = "2025/04/09"
    REFERENCE_TIME = "20:51"
    REFERENCE_TIMEZONE = "+05:30"
    REFERENCE_LOCATION = "Bangalore, India"
    REFERENCE_LAT = 12.9716
    REFERENCE_LON = 77.5946

    def __init__(self):
        """Initialize the test data manager"""
        self.data_dir = os.path.dirname(os.path.abspath(__file__))
        self.reference_charts_dir = os.path.join(self.data_dir, "reference_charts")
        self.reference_data = {}
        self._load_reference_data()

    def _load_reference_data(self):
        """Load all reference data from JSON files"""
        # Load reference data from all JSON files in the reference_charts directory
        for filename in os.listdir(self.reference_charts_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(self.reference_charts_dir, filename)
                with open(file_path, "r") as f:
                    data = json.load(f)
                    # Use the filename (without extension) as the key
                    key = os.path.splitext(filename)[0]
                    self.reference_data[key] = data

    def get_reference_data(self, key):
        """
        Get reference data by key

        Args:
            key (str): The key for the reference data

        Returns:
            dict: The reference data
        """
        return self.reference_data.get(key, {})

    def get_reference_chart(self, ayanamsa=const.AY_LAHIRI, hsys=const.HOUSES_PLACIDUS):
        """
        Create a chart for the reference date with the specified ayanamsa and house system

        Args:
            ayanamsa (str): Ayanamsa constant
            hsys (str): House system constant

        Returns:
            Chart: Flatlib Chart object
        """
        # Create date and location objects
        date = Datetime(self.REFERENCE_DATE, self.REFERENCE_TIME, self.REFERENCE_TIMEZONE)
        pos = GeoPos(self.REFERENCE_LAT, self.REFERENCE_LON)

        # Create chart
        chart = Chart(date, pos, hsys=hsys, ayanamsa=ayanamsa)

        return chart

    def save_reference_data(self, key, data):
        """
        Save reference data to a JSON file

        Args:
            key (str): The key for the reference data
            data (dict): The reference data to save
        """
        # Add metadata
        data["_metadata"] = {
            "created": datetime.now().isoformat(),
            "reference_date": self.REFERENCE_DATE,
            "reference_time": self.REFERENCE_TIME,
            "reference_timezone": self.REFERENCE_TIMEZONE,
            "reference_location": self.REFERENCE_LOCATION,
            "reference_lat": self.REFERENCE_LAT,
            "reference_lon": self.REFERENCE_LON
        }

        # Save to file
        file_path = os.path.join(self.reference_charts_dir, f"{key}.json")
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

        # Update in-memory data
        self.reference_data[key] = data
