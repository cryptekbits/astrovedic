"""
    This module implements the ChartConfiguration class for managing chart configuration
    settings in Vedic astrology calculations.
"""

from astrovedic.vedic.ayanamsa import AyanamsaManager
from astrovedic.vedic.houses import HouseSystemManager

class ChartConfiguration:
    """Manages chart configuration settings."""
    
    def __init__(self, ayanamsa=None, house_system=None, is_kp=False):
        """
        Initialize chart configuration.
        
        Args:
            ayanamsa (str, optional): The ayanamsa to use. If None, uses the default.
            house_system (str, optional): The house system to use. If None, uses the default.
            is_kp (bool, optional): Whether this is a KP chart. Defaults to False.
        """
        if is_kp:
            self.ayanamsa = ayanamsa or AyanamsaManager.get_kp_default()
            self.house_system = house_system or HouseSystemManager.get_kp_default()
        else:
            self.ayanamsa = ayanamsa or AyanamsaManager.get_default()
            self.house_system = house_system or HouseSystemManager.get_default()
        
    def validate(self):
        """
        Validate the configuration.
        
        Raises:
            ValueError: If the ayanamsa or house system is not supported.
        """
        if not AyanamsaManager.is_supported(self.ayanamsa):
            raise ValueError(f"Unsupported ayanamsa: {self.ayanamsa}")
        if not HouseSystemManager.is_supported(self.house_system):
            raise ValueError(f"Unsupported house system: {self.house_system}")
    
    def is_recommended_combination(self):
        """
        Check if the ayanamsa and house system combination is recommended.
        
        Returns:
            bool: True if the combination is recommended, False otherwise.
        """
        return (
            self.house_system in AyanamsaManager.get_recommended_house_systems(self.ayanamsa) or
            self.ayanamsa in HouseSystemManager.get_recommended_ayanamsas(self.house_system)
        )
    
    def get_warnings(self):
        """
        Get warnings for the configuration.
        
        Returns:
            list: A list of warning messages.
        """
        warnings = []
        
        if not self.is_recommended_combination():
            warnings.append(
                f"The combination of {AyanamsaManager.get_ayanamsa_info(self.ayanamsa)['name']} "
                f"ayanamsa and {HouseSystemManager.get_house_system_info(self.house_system)['name']} "
                f"house system is not recommended."
            )
        
        return warnings
