#!/usr/bin/env python3
"""
Simple test script for caching functionality
"""

import time
from astrovedic import const
from astrovedic.cache import clear_all_caches, CacheConfig

# Import original functions
from astrovedic.vedic.utils import get_sign_lord as get_sign_lord_orig
from astrovedic.vedic.nakshatras import get_nakshatra as get_nakshatra_orig

# Import cached functions
from astrovedic.vedic.utils_cached import get_sign_lord as get_sign_lord_cached
from astrovedic.vedic.nakshatras_cached import get_nakshatra as get_nakshatra_cached

def test_correctness():
    """Test that cached functions produce the same results as original functions."""
    print("Testing correctness...")
    
    # Test get_sign_lord
    for sign in const.LIST_SIGNS:
        orig = get_sign_lord_orig(sign)
        cached = get_sign_lord_cached(sign)
        if orig != cached:
            print(f"Error: get_sign_lord({sign}) - Original: {orig}, Cached: {cached}")
        else:
            print(f"get_sign_lord({sign}) - OK")
    
    # Test get_nakshatra
    for lon in [0, 15, 30, 45, 60, 90, 180, 270, 359]:
        orig_result = get_nakshatra_orig(lon)
        cached_result = get_nakshatra_cached(lon)
        if orig_result['name'] != cached_result['name']:
            print(f"Error: get_nakshatra({lon}) - Original: {orig_result['name']}, Cached: {cached_result['name']}")
        else:
            print(f"get_nakshatra({lon}) - OK")

def test_performance():
    """Test the performance improvement of cached functions."""
    print("\nTesting performance...")
    
    # Clear all caches
    clear_all_caches()
    
    # Number of iterations
    iterations = 10000
    
    # Test get_sign_lord
    start_time = time.time()
    for _ in range(iterations):
        get_sign_lord_orig(const.ARIES)
    orig_time = time.time() - start_time
    
    start_time = time.time()
    for _ in range(iterations):
        get_sign_lord_cached(const.ARIES)
    cached_time = time.time() - start_time
    
    print(f"get_sign_lord: Original: {orig_time:.6f}s, Cached: {cached_time:.6f}s, Speedup: {orig_time/cached_time:.2f}x")
    
    # Test get_nakshatra
    start_time = time.time()
    for i in range(iterations):
        get_nakshatra_orig(i % 360)
    orig_time = time.time() - start_time
    
    start_time = time.time()
    for i in range(iterations):
        get_nakshatra_cached(i % 360)
    cached_time = time.time() - start_time
    
    print(f"get_nakshatra: Original: {orig_time:.6f}s, Cached: {cached_time:.6f}s, Speedup: {orig_time/cached_time:.2f}x")

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
    CacheConfig.set_cache_size('reference_data', 500)
    print(f"CacheConfig.maxsize['reference_data'] = {CacheConfig.maxsize['reference_data']}")
    
    # Test getting cache info
    cache_info = CacheConfig.get_cache_info()
    print(f"CacheConfig.get_cache_info() = {cache_info}")

if __name__ == '__main__':
    test_correctness()
    test_performance()
    test_cache_config()
