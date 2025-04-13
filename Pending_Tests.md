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
- `get_sarvatobhadra_chakra` - Testing chakra construction
- `get_chakra_quality` - Testing chakra quality assessment
- `get_auspicious_directions` - Testing auspicious direction identification
- `get_inauspicious_directions` - Testing inauspicious direction identification

### Compatibility Analysis
- `get_compatibility_score` - Testing compatibility score calculation
- `get_compatibility_factors` - Testing compatibility factors identification
- `get_compatibility_description` - Testing compatibility descriptions
- `get_compatibility_report` - Testing comprehensive compatibility reporting

### Kuta Analysis
- `get_varna_kuta` - Testing Varna compatibility
- `get_vashya_kuta` - Testing Vashya compatibility
- `get_tara_kuta` - Testing Tara compatibility
- `get_yoni_kuta` - Testing Yoni compatibility
- `get_graha_maitri_kuta` - Testing planetary friendship compatibility
- `get_gana_kuta` - Testing Gana compatibility
- `get_bhakoot_kuta` - Testing Bhakoot compatibility
- `get_nadi_kuta` - Testing Nadi compatibility

### Transit Analysis
- `get_transit_chart` - Testing transit chart creation
- `get_transit_planets` - Testing transit planet positions
- `get_transit_aspects` - Testing transit aspects calculation
- `get_transit_houses` - Testing transit house positions
- `get_transit_quality` - Testing transit quality assessment
- `get_transit_predictions` - Testing transit predictions
- `get_transit_timeline` - Testing transit timeline calculation
- `get_transit_events` - Testing transit event identification

### Yogas (Planetary Combinations)
- `get_yoga_strength` - Testing yoga strength calculation
- `get_yoga_effects` - Testing yoga effects assessment
- `get_strongest_yoga` - Testing strongest yoga identification
- `get_mahapurusha_yogas` - Testing Pancha Mahapurusha yoga identification
- `get_raja_yogas` - Testing Raja yoga identification
- `get_dhana_yogas` - Testing Dhana yoga identification

### Vargas (Divisional Charts)
- `calculate_d20` - Testing D20 (Vimshamsha) chart calculations
- `calculate_d24` - Testing D24 (Chaturvimshamsha) chart calculations
- `calculate_d27` - Testing D27 (Saptavimshamsha) chart calculations
- `calculate_d30` - Testing D30 (Trimshamsha) chart calculations
- `calculate_d40` - Testing D40 (Khavedamsha) chart calculations
- `calculate_d45` - Testing D45 (Akshavedamsha) chart calculations
- `calculate_d60` - Testing D60 (Shashtiamsha) chart calculations
- `get_vimshopaka_bala` - Testing Vimshopaka Bala calculation

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
