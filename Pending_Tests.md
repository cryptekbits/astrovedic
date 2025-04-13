# Pending Tests for Flatlib

This document lists functionalities in the flatlib library that currently lack corresponding tests. These represent areas that should be prioritized for test coverage to ensure stability and correctness of the codebase.

## Vedic Astrology Functions

### Upagrah (Shadow Planets)
✅ Tests implemented in `tests/test_upagrah.py`

### KP Astrology
✅ Tests implemented in `tests/test_kp.py`

### Muhurta (Electional Astrology)
✅ Tests implemented in `tests/test_muhurta_core.py`

### Sarvatobhadra Chakra
✅ Tests implemented in `tests/test_sarvatobhadra_core.py`

### Compatibility Analysis
✅ Tests implemented in `tests/test_compatibility_core.py`

### Kuta Analysis
✅ Tests implemented in `tests/test_kuta.py`

### Transit Analysis
✅ Tests implemented in `tests/test_transit_core.py` and `tests/test_transit_predictions.py`

### Yogas (Planetary Combinations)
✅ Tests implemented in `tests/test_yoga_core.py` and `tests/test_yoga_types.py`

### Vargas (Divisional Charts)
✅ Tests implemented in `tests/test_higher_vargas.py` and `tests/test_vimshopaka_bala.py`

## Core Library Functions

### Predictive Techniques
- `primarydirections.py` - Primary directions calculations
- `profections.py` - Annual profections technique
- `returns.py` - Solar and lunar returns

### Tool Functions
- `chartdynamics.py` - Chart dynamics calculations
- `planetarytime.py` - Planetary hours and days

### Cache System
- `cache.py` - Comprehensive caching system tests
- Cache invalidation tests
- Cache size and configuration tests
- Performance benchmarks for caching

### API Functions
- VedicChart class API methods
- create_vedic_chart function
- create_kp_chart function

## Error Handling and Edge Cases

- Testing with invalid inputs
- Testing with edge case birth data (polar regions, date line crossing)
- Testing with extreme planetary positions
- Testing error handling in calculations with potential division by zero
- Testing timezone handling in various edge cases

## Integration Tests

- Full system integration tests with real-world charts
- Integration between core library and Vedic extensions
- Integration between different Vedic modules
