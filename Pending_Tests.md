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
✅ Tests implemented in `tests/test_primary_directions.py`, `tests/test_profections.py`, and `tests/test_returns.py`

### Tool Functions
✅ Tests implemented in `tests/test_chart_dynamics.py` and `tests/test_planetary_time.py`

### Cache System
✅ Tests implemented in `tests/test_cache_comprehensive.py`, `tests/test_cache_configuration.py`, and `tests/test_cache_performance.py`

### API Functions
✅ Tests implemented in `tests/test_api_functions.py`

## Error Handling and Edge Cases

✅ Tests implemented in `tests/test_error_handling.py` and `tests/test_edge_cases.py`

## Integration Tests

✅ Tests implemented in `tests/test_integration.py`

## Additional Areas Needing Technical Test Coverage

### Calculation Modules

#### Traditional Protocol Calculations
- `flatlib/protocols/almutem.py` - Tests for mathematical correctness of Almutem calculations
- `flatlib/protocols/behavior.py` - Tests for consistent behavior score calculations
- `flatlib/protocols/temperament.py` - Tests for temperament score calculations

#### Ashtakavarga Calculation Modules
- `flatlib/vedic/ashtakavarga/bhinna.py` - Tests for Bhinna Ashtakavarga point calculations
- `flatlib/vedic/ashtakavarga/kaksha.py` - Tests for Kaksha Ashtakavarga subdivision calculations
- `flatlib/vedic/ashtakavarga/sarva.py` - Tests for Sarva Ashtakavarga summation calculations

#### Jaimini System Calculations
- `flatlib/vedic/jaimini/karakas.py` - Tests for Chara Karaka calculations and assignments

#### Divisional Chart Calculations
- Tests for mathematical accuracy of divisional chart calculations (D-1 through D-60)
- Tests for special varga calculation algorithms like Khavedamsha and Akshavedamsha

### API Consistency Tests

#### Compatibility Module APIs
- `flatlib/vedic/compatibility/dasha/` - Tests for API consistency and parameter validation
- `flatlib/vedic/compatibility/dosha/` - Tests for consistent return types and error handling
- `flatlib/vedic/compatibility/navamsa/` - Tests for proper function signatures and return values

#### Muhurta Module APIs
- `flatlib/vedic/muhurta/activities.py` - Tests for API consistency and parameter validation
- `flatlib/vedic/muhurta/events.py` - Tests for consistent return types and error handling
- `flatlib/vedic/muhurta/timing.py` - Tests for proper function signatures and return values

#### Yoga Module APIs
- Tests for consistent API patterns across all yoga calculation modules
- Tests for proper error handling and edge cases in yoga detection functions

#### Shadbala Module APIs
- Tests for consistent API patterns across all strength calculation components
- Tests for proper parameter validation and error handling

### Performance and Optimization Tests

#### Benchmark Tests
- Benchmark tests for critical and computationally intensive calculations
- Comparative performance tests for alternative calculation methods

#### Memory Usage Tests
- Memory profiling for large chart sets and extensive calculations
- Tests for memory leaks in long-running operations

#### Caching Effectiveness Tests
- Optimization tests for cached vs. non-cached operations
- Tests for cache invalidation scenarios
- Tests for cache hit/miss ratios under various workloads
