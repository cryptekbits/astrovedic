# Plan for Streamlining Ayanamsa and House System Selection in Astrovedic

## Overview

This document outlines a comprehensive plan to streamline and improve the ayanamsa (precession model) and house system selection in the Astrovedic library. The goal is to create a more intuitive, flexible, and maintainable system that follows the desired flow:

**Ayanamsa Selection → House System Selection → Chart Creation**

Where chart creation is dynamic based on selections, and all other features (dashas, balas, yogas) are derived from that chart.

## Current Implementation

### Ayanamsas

- Defined as string constants in `astrovedic/const.py`
- Mapped to Swiss Ephemeris values in `astrovedic/ephem/swe.py`
- Default ayanamsas defined in `astrovedic/vedic/__init__.py`:
  - `DEFAULT_AYANAMSA = const.AY_LAHIRI` (for Vedic)
  - `DEFAULT_KP_AYANAMSA = const.AY_KRISHNAMURTI` (for KP)

### House Systems

- Defined as string constants in `astrovedic/const.py`
- Mapped to Swiss Ephemeris values in `astrovedic/ephem/swe.py`
- Default house systems defined in `astrovedic/vedic/__init__.py`:
  - `DEFAULT_HOUSE_SYSTEM = const.HOUSES_WHOLE_SIGN` (for Vedic)
  - `DEFAULT_KP_HOUSE_SYSTEM = const.HOUSES_PLACIDUS` (for KP)

### Chart Creation

- `Chart` class in `astrovedic/chart.py` accepts `hsys` and `mode` parameters
- `VedicChart` class in `astrovedic/vedic/api.py` provides convenience methods
- Helper functions `create_vedic_chart()` and `create_kp_chart()` with default parameters

## Issues with Current Implementation

1. **Lack of Encapsulation**: Ayanamsa and house system selection are spread across multiple files
2. **Rigid Defaults**: Hard-coded defaults make it difficult to change preferences
3. **Inconsistent Naming**: `mode` parameter for ayanamsa is not intuitive
4. **Limited Validation**: No validation of compatible ayanamsa and house system combinations
5. **No Configuration System**: Users can't set global preferences easily

## Proposed Solution

### 1. Create an AyanamsaManager Class

```python
# astrovedic/vedic/ayanamsa.py
class AyanamsaManager:
    """Manages ayanamsa selection and configuration."""
    
    # Dictionary of supported ayanamsas with metadata
    SUPPORTED_AYANAMSAS = {
        const.AY_LAHIRI: {
            'name': 'Lahiri',
            'description': 'Official ayanamsa of the Indian government',
            'category': 'primary',
            'recommended_house_systems': [const.HOUSES_WHOLE_SIGN]
        },
        const.AY_RAMAN: {
            'name': 'Raman',
            'description': 'B.V. Raman\'s ayanamsa, a variant of Lahiri',
            'category': 'primary',
            'recommended_house_systems': [const.HOUSES_WHOLE_SIGN]
        },
        # ... other ayanamsas
    }
    
    # Default ayanamsa
    _default_ayanamsa = const.AY_LAHIRI
    
    @classmethod
    def get_default(cls):
        """Get the default ayanamsa."""
        return cls._default_ayanamsa
        
    @classmethod
    def set_default(cls, ayanamsa):
        """Set the default ayanamsa."""
        if ayanamsa not in cls.SUPPORTED_AYANAMSAS:
            raise ValueError(f"Unsupported ayanamsa: {ayanamsa}")
        cls._default_ayanamsa = ayanamsa
        
    @classmethod
    def get_recommended_house_systems(cls, ayanamsa):
        """Get recommended house systems for an ayanamsa."""
        if ayanamsa not in cls.SUPPORTED_AYANAMSAS:
            raise ValueError(f"Unsupported ayanamsa: {ayanamsa}")
        return cls.SUPPORTED_AYANAMSAS[ayanamsa]['recommended_house_systems']
        
    # ... other utility methods
```

### 2. Create a HouseSystemManager Class

```python
# astrovedic/vedic/houses.py
class HouseSystemManager:
    """Manages house system selection and configuration."""
    
    # Dictionary of supported house systems with metadata
    SUPPORTED_HOUSE_SYSTEMS = {
        const.HOUSES_WHOLE_SIGN: {
            'name': 'Whole Sign',
            'description': 'Traditional Vedic house system',
            'category': 'vedic',
            'recommended_ayanamsas': [const.AY_LAHIRI, const.AY_RAMAN]
        },
        const.HOUSES_PLACIDUS: {
            'name': 'Placidus',
            'description': 'Preferred house system for KP astrology',
            'category': 'kp',
            'recommended_ayanamsas': [const.AY_KRISHNAMURTI]
        },
        # ... other house systems
    }
    
    # Default house system
    _default_house_system = const.HOUSES_WHOLE_SIGN
    
    @classmethod
    def get_default(cls):
        """Get the default house system."""
        return cls._default_house_system
        
    @classmethod
    def set_default(cls, house_system):
        """Set the default house system."""
        if house_system not in cls.SUPPORTED_HOUSE_SYSTEMS:
            raise ValueError(f"Unsupported house system: {house_system}")
        cls._default_house_system = house_system
        
    @classmethod
    def get_recommended_ayanamsas(cls, house_system):
        """Get recommended ayanamsas for a house system."""
        if house_system not in cls.SUPPORTED_HOUSE_SYSTEMS:
            raise ValueError(f"Unsupported house system: {house_system}")
        return cls.SUPPORTED_HOUSE_SYSTEMS[house_system]['recommended_ayanamsas']
        
    # ... other utility methods
```

### 3. Create a ChartConfiguration Class

```python
# astrovedic/vedic/config.py
class ChartConfiguration:
    """Manages chart configuration settings."""
    
    def __init__(self, ayanamsa=None, house_system=None):
        """Initialize chart configuration."""
        self.ayanamsa = ayanamsa or AyanamsaManager.get_default()
        self.house_system = house_system or HouseSystemManager.get_default()
        
    def validate(self):
        """Validate the configuration."""
        if self.ayanamsa not in AyanamsaManager.SUPPORTED_AYANAMSAS:
            raise ValueError(f"Unsupported ayanamsa: {self.ayanamsa}")
        if self.house_system not in HouseSystemManager.SUPPORTED_HOUSE_SYSTEMS:
            raise ValueError(f"Unsupported house system: {self.house_system}")
        
    def is_recommended_combination(self):
        """Check if the ayanamsa and house system combination is recommended."""
        return (
            self.house_system in AyanamsaManager.get_recommended_house_systems(self.ayanamsa) or
            self.ayanamsa in HouseSystemManager.get_recommended_ayanamsas(self.house_system)
        )
        
    # ... other utility methods
```

### 4. Update the Chart Class

```python
# astrovedic/chart.py (modified)
class Chart:
    """This class represents an astrology chart."""
    
    def __init__(self, date, pos, **kwargs):
        """Creates an astrology chart for a given date and location."""
        # Handle optional arguments
        hsys = kwargs.get('hsys', HouseSystemManager.get_default())
        ayanamsa = kwargs.get('ayanamsa', AyanamsaManager.get_default())
        
        # For backward compatibility
        if 'mode' in kwargs and kwargs['mode'] is not None:
            ayanamsa = kwargs['mode']
            
        # Create and validate configuration
        config = ChartConfiguration(ayanamsa, hsys)
        config.validate()
        
        # Store configuration
        self.ayanamsa = ayanamsa
        self.hsys = hsys
        
        # ... rest of initialization
```

### 5. Update the VedicChart Class

```python
# astrovedic/vedic/api.py (modified)
class VedicChart:
    """High-level class for Vedic astrology charts."""
    
    @classmethod
    def from_data(cls, date, pos, hsys=None, ayanamsa=None):
        """Create a VedicChart from date and position data."""
        config = ChartConfiguration(ayanamsa, hsys)
        chart = Chart(date, pos, hsys=config.house_system, ayanamsa=config.ayanamsa)
        return cls(chart, config.ayanamsa)
        
    @classmethod
    def kp_chart(cls, date, pos, hsys=None, ayanamsa=None):
        """Create a KP (Krishnamurti Paddhati) chart."""
        # Set KP defaults if not specified
        if ayanamsa is None:
            ayanamsa = const.AY_KRISHNAMURTI
        if hsys is None:
            hsys = const.HOUSES_PLACIDUS
            
        config = ChartConfiguration(ayanamsa, hsys)
        chart = Chart(date, pos, hsys=config.house_system, ayanamsa=config.ayanamsa)
        return cls(chart, config.ayanamsa)
```

## Implementation Tasks

### Phase 1: Core Infrastructure

1. **Create Base Classes**
   - Implement `AyanamsaManager` class
   - Implement `HouseSystemManager` class
   - Implement `ChartConfiguration` class

2. **Update Constants**
   - Reorganize ayanamsa constants in `const.py`
   - Reorganize house system constants in `const.py`
   - Add metadata for each ayanamsa and house system

3. **Update Documentation**
   - Create new documentation for ayanamsa selection
   - Create new documentation for house system selection
   - Update existing documentation to reflect new approach

### Phase 2: Integration

4. **Update Chart Class**
   - Modify `Chart` class to use the new configuration system
   - Add backward compatibility for existing code
   - Add validation for ayanamsa and house system combinations

5. **Update VedicChart Class**
   - Modify `VedicChart` class to use the new configuration system
   - Update factory methods to use the new configuration system
   - Add convenience methods for common configurations

6. **Update Helper Functions**
   - Update `create_vedic_chart()` function
   - Update `create_kp_chart()` function
   - Add new helper functions for common configurations

### Phase 3: Testing and Refinement

7. **Update Tests**
   - Add tests for the new configuration system
   - Update existing tests to use the new configuration system
   - Add tests for validation and error handling

8. **Create Examples**
   - Create examples for using the new configuration system
   - Update existing examples to use the new configuration system
   - Add examples for common configurations

9. **Performance Optimization**
   - Profile the new configuration system
   - Optimize for performance
   - Add caching where appropriate

## Benefits

1. **Improved Usability**: More intuitive API for selecting ayanamsas and house systems
2. **Better Validation**: Validation of compatible combinations
3. **Flexibility**: Easy to add new ayanamsas and house systems
4. **Maintainability**: Centralized configuration system
5. **Documentation**: Better documentation for ayanamsa and house system selection
6. **Backward Compatibility**: Maintains compatibility with existing code

## Timeline

- **Phase 1**: 1-2 weeks
- **Phase 2**: 2-3 weeks
- **Phase 3**: 1-2 weeks

Total estimated time: 4-7 weeks

## Conclusion

This plan provides a comprehensive approach to streamlining ayanamsa and house system selection in the Astrovedic library. By implementing a centralized configuration system with proper validation and documentation, we can improve the usability and maintainability of the library while maintaining backward compatibility.

The proposed solution follows the desired flow of Ayanamsa Selection → House System Selection → Chart Creation, where chart creation is dynamic based on selections, and all other features (dashas, balas, yogas) are derived from that chart.
