# Astrovedic Examples

This directory contains examples demonstrating how to use the astrovedic library for Vedic astrology calculations and analysis.

## Directory Structure

- `flatlib/`: Legacy examples using the core flatlib library (kept for reference)
- Other examples in the root directory demonstrate specific features and use cases of astrovedic

## Basic Examples

These examples demonstrate how to use the astrovedic library for basic Vedic astrology calculations:

1. **basic_chart.py**: Creating a basic chart and accessing its properties
2. **compatibility.py**: Basic compatibility analysis between two charts
3. **transits.py**: Basic transit analysis for a chart
4. **divisional_charts.py**: Working with divisional charts (vargas)
5. **vedic_api_example.py**: Using the unified Vedic API

## Feature-Specific Examples

These examples demonstrate specific features of astrovedic:

1. **compatibility_calculator.py**: Detailed compatibility analysis between two charts
2. **dainik_panchang.py**: Daily panchang (almanac) calculations
3. **muhurta_calculator.py**: Muhurta (electional astrology) analysis
4. **transit_calculator.py**: Transit analysis and predictions
5. **yoga_calculator.py**: Identification of yogas (planetary combinations)
6. **shadbala_calculator.py**: Calculation of planetary strengths
7. **sarvatobhadra_calculator.py**: Directional analysis
8. **ayanamsa_example.py**: Comparing different ayanamsas
9. **vedic_objects.py**: Working with Vedic objects
10. **vedic_aspects.py**: Vedic aspects and planetary relationships
11. **vedic_dignities.py**: Planetary dignities and strengths

## Configuration System Examples

These examples demonstrate how to use the configuration system in astrovedic:

1. **configuration_example.py**: Comprehensive demonstration of the configuration system
2. **simple_configuration.py**: Simple usage of the configuration system
3. **varga_configuration.py**: Using the configuration system with divisional charts

## Running the Examples

To run these examples, make sure you have astrovedic installed:

```bash
# Navigate to the examples directory
cd examples

# Run a basic example
python basic_chart.py

# Run a configuration example
python configuration_example.py

# Run a feature-specific example
python compatibility_calculator.py
```

## Notes

- The basic examples focus on fundamental calculations and data retrieval
- The feature-specific examples demonstrate more advanced functionality
- The configuration examples show how to customize ayanamsa and house system settings
- All examples use Bangalore, India as the default location and April 9, 2025 at 20:51 as the reference date
- By default, examples use the Whole Sign house system and Lahiri ayanamsa for Vedic calculations
- For KP (Krishnamurti Paddhati) calculations, examples use the Krishnamurti ayanamsa and Placidus house system
