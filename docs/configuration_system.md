# Astrovedic Configuration System

This document explains the configuration system in the Astrovedic library, which allows you to customize ayanamsa and house system settings for Vedic astrology calculations.

## Overview

The configuration system in Astrovedic consists of three main components:

1. **AyanamsaManager**: Manages ayanamsa selection and configuration
2. **HouseSystemManager**: Manages house system selection and configuration
3. **ChartConfiguration**: Combines ayanamsa and house system settings into a unified configuration

This system follows the desired flow of:
- Ayanamsa Selection → House System Selection → Chart Creation

Where chart creation is dynamic based on selections, and all other features (dashas, balas, yogas) are derived from that chart.

## Ayanamsa Manager

The `AyanamsaManager` class provides methods for working with ayanamsas (the offset between the tropical and sidereal zodiacs).

### Supported Ayanamsas

Astrovedic supports the following ayanamsas:

| Ayanamsa ID | Name | Description | Category |
|-------------|------|-------------|----------|
| AY_LAHIRI | Lahiri | Official ayanamsa of the Indian government | primary |
| AY_RAMAN | Raman | B.V. Raman's ayanamsa, a variant of Lahiri | primary |
| AY_KRISHNAMURTI | Krishnamurti | K.S. Krishnamurti's ayanamsa for KP system | kp |
| AY_YUKTESHWAR | Yukteshwar | Based on Sri Yukteshwar's book "The Holy Science" | traditional |
| AY_JN_BHASIN | JN Bhasin | J.N. Bhasin's ayanamsa | alternative |
| AY_SURYASIDDHANTA | Surya Siddhanta | Based on the ancient Surya Siddhanta text | traditional |
| AY_TRUE_CITRA | True Citra | True Citra ayanamsa with Spica at 0° Libra | traditional |
| AY_TRUE_REVATI | True Revati | True Revati ayanamsa with Revati at 0° Aries | traditional |

### Default Ayanamsas

- Default Vedic ayanamsa: `AY_LAHIRI` (Lahiri)
- Default KP ayanamsa: `AY_KRISHNAMURTI` (Krishnamurti)

### Key Methods

```python
# Get the default ayanamsa
default_ayanamsa = AyanamsaManager.get_default()

# Set the default ayanamsa
AyanamsaManager.set_default(const.AY_RAMAN)

# Get the default KP ayanamsa
default_kp_ayanamsa = AyanamsaManager.get_kp_default()

# Set the default KP ayanamsa
AyanamsaManager.set_kp_default(const.AY_KRISHNAMURTI)

# Get all supported ayanamsas
all_ayanamsas = AyanamsaManager.get_all_ayanamsas()

# Get information about an ayanamsa
ayanamsa_info = AyanamsaManager.get_ayanamsa_info(const.AY_LAHIRI)

# Check if an ayanamsa is supported
is_supported = AyanamsaManager.is_supported(const.AY_LAHIRI)

# Get recommended house systems for an ayanamsa
recommended_house_systems = AyanamsaManager.get_recommended_house_systems(const.AY_LAHIRI)
```

## House System Manager

The `HouseSystemManager` class provides methods for working with house systems (methods of dividing the ecliptic into houses).

### Supported House Systems

Astrovedic supports the following house systems:

| House System ID | Name | Description | Category |
|-----------------|------|-------------|----------|
| HOUSES_WHOLE_SIGN | Whole Sign | Traditional Vedic house system | vedic |
| HOUSES_EQUAL | Equal | Equal house system | vedic |
| HOUSES_PLACIDUS | Placidus | Preferred house system for KP astrology | kp |
| HOUSES_KOCH | Koch | Koch house system | alternative |
| HOUSES_REGIOMONTANUS | Regiomontanus | Regiomontanus house system | alternative |
| HOUSES_CAMPANUS | Campanus | Campanus house system | alternative |
| HOUSES_PORPHYRIUS | Porphyrius | Porphyrius house system | alternative |
| HOUSES_MORINUS | Morinus | Morinus house system | alternative |

### Default House Systems

- Default Vedic house system: `HOUSES_WHOLE_SIGN` (Whole Sign)
- Default KP house system: `HOUSES_PLACIDUS` (Placidus)

### Key Methods

```python
# Get the default house system
default_house_system = HouseSystemManager.get_default()

# Set the default house system
HouseSystemManager.set_default(const.HOUSES_EQUAL)

# Get the default KP house system
default_kp_house_system = HouseSystemManager.get_kp_default()

# Set the default KP house system
HouseSystemManager.set_kp_default(const.HOUSES_PLACIDUS)

# Get all supported house systems
all_house_systems = HouseSystemManager.get_all_house_systems()

# Get information about a house system
house_system_info = HouseSystemManager.get_house_system_info(const.HOUSES_WHOLE_SIGN)

# Check if a house system is supported
is_supported = HouseSystemManager.is_supported(const.HOUSES_WHOLE_SIGN)

# Get recommended ayanamsas for a house system
recommended_ayanamsas = HouseSystemManager.get_recommended_ayanamsas(const.HOUSES_WHOLE_SIGN)
```

## Chart Configuration

The `ChartConfiguration` class combines ayanamsa and house system settings into a unified configuration.

### Creating a Configuration

```python
# Create a default configuration (Lahiri ayanamsa with Whole Sign houses)
default_config = ChartConfiguration()

# Create a KP configuration (Krishnamurti ayanamsa with Placidus houses)
kp_config = ChartConfiguration(is_kp=True)

# Create a custom configuration
custom_config = ChartConfiguration(const.AY_RAMAN, const.HOUSES_EQUAL)
```

### Key Methods

```python
# Validate the configuration
config.validate()

# Check if the configuration is a recommended combination
is_recommended = config.is_recommended_combination()

# Get warnings for the configuration
warnings = config.get_warnings()
```

## Using the Configuration System

### Creating a Chart with a Configuration

```python
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic.vedic.config import ChartConfiguration

# Create a date and location
date = Datetime('2025/04/09', '20:51', '+05:30')
pos = GeoPos(12.9716, 77.5946)  # Bangalore, India

# Create a configuration
config = ChartConfiguration(const.AY_LAHIRI, const.HOUSES_WHOLE_SIGN)

# Create a chart with this configuration
chart = Chart(date, pos, hsys=config.house_system, ayanamsa=config.ayanamsa)
```

### Using the Vedic API with a Configuration

```python
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.vedic.api import create_vedic_chart, create_kp_chart

# Create a date and location
date = Datetime('2025/04/09', '20:51', '+05:30')
pos = GeoPos(12.9716, 77.5946)  # Bangalore, India

# Create a Vedic chart with default configuration (Lahiri/Whole Sign)
vedic_chart = create_vedic_chart(date, pos)

# Create a KP chart with default KP configuration (Krishnamurti/Placidus)
kp_chart = create_kp_chart(date, pos)

# Create a Vedic chart with custom configuration
custom_chart = create_vedic_chart(
    date, pos,
    ayanamsa=const.AY_RAMAN,
    house_system=const.HOUSES_EQUAL
)
```

## Recommended Combinations

Astrovedic recommends certain combinations of ayanamsas and house systems for optimal results:

| Ayanamsa | Recommended House Systems |
|----------|---------------------------|
| Lahiri | Whole Sign, Equal |
| Raman | Whole Sign, Equal |
| Krishnamurti | Placidus |
| Yukteshwar | Whole Sign |
| True Citra | Whole Sign |
| True Revati | Whole Sign |

| House System | Recommended Ayanamsas |
|--------------|------------------------|
| Whole Sign | Lahiri, Raman, Yukteshwar, True Citra, True Revati |
| Equal | Lahiri, Raman |
| Placidus | Krishnamurti |

Using non-recommended combinations will generate warnings but will still work.

## Examples

For complete examples of using the configuration system, see:

1. **examples/configuration_example.py**: Comprehensive demonstration of the configuration system
2. **examples/simple_configuration.py**: Simple usage of the configuration system
3. **examples/varga_configuration.py**: Using the configuration system with divisional charts

## Best Practices

1. **Use the ChartConfiguration class** instead of directly specifying ayanamsa and house system parameters
2. **Validate your configuration** using the `validate()` method
3. **Check for warnings** using the `get_warnings()` method
4. **Use recommended combinations** when possible
5. **Use the Vedic API** for a simplified interface to chart creation with configuration

## Conclusion

The configuration system in Astrovedic provides a flexible and robust way to customize ayanamsa and house system settings for Vedic astrology calculations. By using this system, you can ensure that your calculations are accurate and consistent with your preferred astrological tradition.
