#!/usr/bin/env python3
"""
Simple test script for calculation caching functionality
"""

import time
from astrovedic import const
from astrovedic.cache import clear_all_caches, CacheConfig

# Import original functions
from astrovedic.vedic.vargas.navamsha import calculate_d9 as calculate_d9_orig
from astrovedic.vedic.panchang import get_tithi as get_tithi_orig

# Import cached functions
from astrovedic.vedic.vargas.cached import calculate_d9 as calculate_d9_cached
from astrovedic.vedic.panchang_cached import get_tithi as get_tithi_cached

def test_correctness():
    """Test that cached functions produce the same results as original functions."""
    print("Testing correctness...")

    # Test calculate_d9
    for lon in [0, 15, 30, 45, 60, 90, 180, 270, 359]:
        orig = round(calculate_d9_orig(lon), 8)  # Round to avoid floating point issues
        cached = calculate_d9_cached(lon)
        if orig != cached:
            print(f"Error: calculate_d9({lon}) - Original: {orig}, Cached: {cached}")
        else:
            print(f"calculate_d9({lon}) - OK")

    # Test get_tithi
    jd = 2460000.5  # Example Julian day
    orig_result = get_tithi_orig(jd)
    cached_result = get_tithi_cached(jd)
    if orig_result['name'] != cached_result['name']:
        print(f"Error: get_tithi({jd}) - Original: {orig_result['name']}, Cached: {cached_result['name']}")
    else:
        print(f"get_tithi({jd}) - OK")

def test_performance():
    """Test the performance improvement of cached functions."""
    print("\nTesting performance...")

    # Clear all caches
    clear_all_caches()

    # Number of iterations
    iterations = 10000

    # Test calculate_d9
    start_time = time.time()
    for i in range(iterations):
        calculate_d9_orig(i % 360)
    orig_time = time.time() - start_time

    start_time = time.time()
    for i in range(iterations):
        calculate_d9_cached(i % 360)
    cached_time = time.time() - start_time

    print(f"calculate_d9: Original: {orig_time:.6f}s, Cached: {cached_time:.6f}s, Speedup: {orig_time/cached_time:.2f}x")

    # Test get_tithi
    jd_base = 2460000.5
    start_time = time.time()
    for i in range(iterations):
        get_tithi_orig(jd_base + i/1000)
    orig_time = time.time() - start_time

    start_time = time.time()
    for i in range(iterations):
        get_tithi_cached(jd_base + i/1000)
    cached_time = time.time() - start_time

    print(f"get_tithi: Original: {orig_time:.6f}s, Cached: {cached_time:.6f}s, Speedup: {orig_time/cached_time:.2f}x")

def test_cache_config():
    """Test the CacheConfig class."""
    print("\nTesting CacheConfig...")

    # Test disabling caching
    CacheConfig.disable_all()
    print(f"CacheConfig.enabled = {CacheConfig.enabled}")

    # Test enabling caching
    CacheConfig.enable_all()
    print(f"CacheConfig.enabled = {CacheConfig.enabled}")

    # Test setting cache size
    CacheConfig.set_cache_size('calculations', 500)
    print(f"CacheConfig.maxsize['calculations'] = {CacheConfig.maxsize['calculations']}")

    # Test getting cache info
    cache_info = CacheConfig.get_cache_info()
    print(f"CacheConfig.get_cache_info() = {cache_info}")

if __name__ == '__main__':
    test_correctness()
    test_performance()
    test_cache_config()
