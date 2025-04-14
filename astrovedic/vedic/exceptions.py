"""
    This file is part of astrovedic - (C) FlatAngle
    Modified for Vedic Astrology

    This module defines custom exceptions for Vedic astrology calculations.
"""


class VedicError(Exception):
    """Base class for all Vedic astrology exceptions."""
    pass


class InputError(VedicError):
    """Exception raised for errors in the input."""
    def __init__(self, message="Invalid input"):
        self.message = message
        super().__init__(self.message)


class CalculationError(VedicError):
    """Exception raised for errors during calculations."""
    def __init__(self, message="Error in calculation"):
        self.message = message
        super().__init__(self.message)


class ValidationError(VedicError):
    """Exception raised for validation errors."""
    def __init__(self, message="Validation failed"):
        self.message = message
        super().__init__(self.message)


class ConfigurationError(VedicError):
    """Exception raised for configuration errors."""
    def __init__(self, message="Invalid configuration"):
        self.message = message
        super().__init__(self.message)


class DataError(VedicError):
    """Exception raised for data errors."""
    def __init__(self, message="Invalid data"):
        self.message = message
        super().__init__(self.message)


class NotSupportedError(VedicError):
    """Exception raised when a feature is not supported."""
    def __init__(self, message="Feature not supported"):
        self.message = message
        super().__init__(self.message)


class AyanamsaError(ConfigurationError):
    """Exception raised for ayanamsa-related errors."""
    def __init__(self, message="Invalid ayanamsa"):
        self.message = message
        super().__init__(self.message)


class HouseSystemError(ConfigurationError):
    """Exception raised for house system-related errors."""
    def __init__(self, message="Invalid house system"):
        self.message = message
        super().__init__(self.message)


class PlanetNotFoundError(DataError):
    """Exception raised when a planet is not found."""
    def __init__(self, planet_id=None):
        self.planet_id = planet_id
        message = f"Planet not found: {planet_id}" if planet_id else "Planet not found"
        super().__init__(message)


class HouseNotFoundError(DataError):
    """Exception raised when a house is not found."""
    def __init__(self, house_num=None):
        self.house_num = house_num
        message = f"House not found: {house_num}" if house_num else "House not found"
        super().__init__(message)


class NakshatraError(CalculationError):
    """Exception raised for nakshatra-related errors."""
    def __init__(self, message="Error in nakshatra calculation"):
        self.message = message
        super().__init__(self.message)


class DashaError(CalculationError):
    """Exception raised for dasha-related errors."""
    def __init__(self, message="Error in dasha calculation"):
        self.message = message
        super().__init__(self.message)


class VargaError(CalculationError):
    """Exception raised for varga-related errors."""
    def __init__(self, message="Error in varga calculation"):
        self.message = message
        super().__init__(self.message)


class YogaError(CalculationError):
    """Exception raised for yoga-related errors."""
    def __init__(self, message="Error in yoga calculation"):
        self.message = message
        super().__init__(self.message)


class AshtakavargaError(CalculationError):
    """Exception raised for ashtakavarga-related errors."""
    def __init__(self, message="Error in ashtakavarga calculation"):
        self.message = message
        super().__init__(self.message)


class ShadbalaError(CalculationError):
    """Exception raised for shadbala-related errors."""
    def __init__(self, message="Error in shadbala calculation"):
        self.message = message
        super().__init__(self.message)


class MuhurtaError(CalculationError):
    """Exception raised for muhurta-related errors."""
    def __init__(self, message="Error in muhurta calculation"):
        self.message = message
        super().__init__(self.message)


class TransitError(CalculationError):
    """Exception raised for transit-related errors."""
    def __init__(self, message="Error in transit calculation"):
        self.message = message
        super().__init__(self.message)


class CompatibilityError(CalculationError):
    """Exception raised for compatibility-related errors."""
    def __init__(self, message="Error in compatibility calculation"):
        self.message = message
        super().__init__(self.message)


class KPError(CalculationError):
    """Exception raised for KP-related errors."""
    def __init__(self, message="Error in KP calculation"):
        self.message = message
        super().__init__(self.message)
