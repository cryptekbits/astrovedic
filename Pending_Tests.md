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

## Additional Areas Needing Test Coverage

### Traditional Protocols
- `flatlib/protocols/almutem.py` - Tests for Almutem calculations
- `flatlib/protocols/behavior.py` - Tests for behavior analysis
- `flatlib/protocols/temperament.py` - Tests for temperament analysis

### Vedic Compatibility Subsystems
- `flatlib/vedic/compatibility/dasha/` - Tests for compatibility dasha analysis
- `flatlib/vedic/compatibility/dosha/` - Tests for dosha analysis in compatibility
- `flatlib/vedic/compatibility/navamsa/` - Tests for navamsa compatibility analysis

### Ashtakavarga Detailed Analysis
- `flatlib/vedic/ashtakavarga/bhinna.py` - Tests for Bhinna Ashtakavarga
- `flatlib/vedic/ashtakavarga/kaksha.py` - Tests for Kaksha Ashtakavarga
- `flatlib/vedic/ashtakavarga/sarva.py` - Tests for Sarva Ashtakavarga
- `flatlib/vedic/ashtakavarga/transits.py` - Tests for Ashtakavarga transit analysis

### Jaimini Astrology
- More comprehensive tests for `flatlib/vedic/jaimini/` modules

### Specific Varga Charts
- Individual tests for each divisional chart calculation (D-1 through D-60)
- Tests for special varga calculations like Khavedamsha and Akshavedamsha

### Muhurta Specific Activities
- `flatlib/vedic/muhurta/activities.py` - Tests for specific activity timing
- `flatlib/vedic/muhurta/events.py` - Tests for event timing
- `flatlib/vedic/muhurta/timing.py` - Tests for general timing calculations

### Specific Yoga Types
- `flatlib/vedic/yogas/chandra.py` - Tests for Moon-based yogas
- `flatlib/vedic/yogas/dhana.py` - Tests for wealth yogas
- `flatlib/vedic/yogas/dosha.py` - Tests for inauspicious yogas
- `flatlib/vedic/yogas/mahapurusha.py` - Tests for Mahapurusha yogas
- `flatlib/vedic/yogas/nabhasa.py` - Tests for Nabhasa yogas
- `flatlib/vedic/yogas/raja.py` - Tests for Raja yogas

### Shadbala Components
- More detailed tests for individual Shadbala components
- Tests for Shadbala analysis and interpretation

### Performance Tests
- Benchmark tests for critical calculations
- Memory usage tests for large chart sets
- Optimization tests for cached vs. non-cached operations
