#!/usr/bin/env python3
"""
Test Cache Configuration

This script tests the cache configuration in flatlib.
"""

import unittest
import time
import sys
from flatlib import const
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib.cache import (
    CacheConfig, clear_all_caches, clear_category_cache,
    reference_cache, calculation_cache, ephemeris_cache,
    CACHE_REFERENCE, CACHE_CALCULATION, CACHE_EPHEMERIS
)


# Define test functions for each cache type with custom maxsize
@reference_cache(maxsize=10)
def test_reference_cache_custom_size(value):
    """Test function for reference cache with custom size."""
    # Simulate some work
    time.sleep(0.001)
    return f"Reference: {value}"


@calculation_cache(maxsize=20)
def test_calculation_cache_custom_size(value):
    """Test function for calculation cache with custom size."""
    # Simulate some work
    time.sleep(0.001)
    return f"Calculation: {value}"


@ephemeris_cache(maxsize=30)
def test_ephemeris_cache_custom_size(value):
    """Test function for ephemeris cache with custom size."""
    # Simulate some work
    time.sleep(0.001)
    return f"Ephemeris: {value}"


class TestCacheCustomSize(unittest.TestCase):
    """Test case for cache with custom size"""
    
    def setUp(self):
        """Set up test case"""
        # Clear all caches before each test
        clear_all_caches()
        
        # Ensure caching is enabled
        CacheConfig.enable_all()
    
    def test_custom_cache_size(self):
        """Test custom cache size"""
        # Check that the cache sizes were set correctly
        self.assertEqual(test_reference_cache_custom_size.cache_info().maxsize, 10)
        self.assertEqual(test_calculation_cache_custom_size.cache_info().maxsize, 20)
        self.assertEqual(test_ephemeris_cache_custom_size.cache_info().maxsize, 30)
        
        # Print the cache sizes for reference
        print(f"Custom Cache Sizes:")
        print(f"  Reference: {test_reference_cache_custom_size.cache_info().maxsize}")
        print(f"  Calculation: {test_calculation_cache_custom_size.cache_info().maxsize}")
        print(f"  Ephemeris: {test_ephemeris_cache_custom_size.cache_info().maxsize}")
    
    def test_cache_size_limit(self):
        """Test cache size limit"""
        # Call the function with more unique values than the cache size
        for i in range(15):
            test_reference_cache_custom_size(i)
        
        # Check that the cache size is limited to the max size
        cache_info = test_reference_cache_custom_size.cache_info()
        self.assertLessEqual(cache_info.currsize, 10)
        
        # Print the cache info for reference
        print(f"Cache Size Limit Test:")
        print(f"  Max Size: {cache_info.maxsize}")
        print(f"  Current Size: {cache_info.currsize}")
        print(f"  Hits: {cache_info.hits}")
        print(f"  Misses: {cache_info.misses}")


class TestCacheConfigOverride(unittest.TestCase):
    """Test case for CacheConfig override"""
    
    def setUp(self):
        """Set up test case"""
        # Clear all caches before each test
        clear_all_caches()
        
        # Ensure caching is enabled
        CacheConfig.enable_all()
        
        # Save the original cache sizes
        self.original_reference_size = CacheConfig.maxsize[CACHE_REFERENCE]
        self.original_calculation_size = CacheConfig.maxsize[CACHE_CALCULATION]
        self.original_ephemeris_size = CacheConfig.maxsize[CACHE_EPHEMERIS]
    
    def tearDown(self):
        """Tear down test case"""
        # Restore the original cache sizes
        CacheConfig.maxsize[CACHE_REFERENCE] = self.original_reference_size
        CacheConfig.maxsize[CACHE_CALCULATION] = self.original_calculation_size
        CacheConfig.maxsize[CACHE_EPHEMERIS] = self.original_ephemeris_size
    
    def test_config_override(self):
        """Test CacheConfig override"""
        # Set new cache sizes
        CacheConfig.set_cache_size(CACHE_REFERENCE, 100)
        CacheConfig.set_cache_size(CACHE_CALCULATION, 200)
        CacheConfig.set_cache_size(CACHE_EPHEMERIS, 300)
        
        # Check that the cache sizes were set correctly
        self.assertEqual(CacheConfig.maxsize[CACHE_REFERENCE], 100)
        self.assertEqual(CacheConfig.maxsize[CACHE_CALCULATION], 200)
        self.assertEqual(CacheConfig.maxsize[CACHE_EPHEMERIS], 300)
        
        # Create new functions with the default cache sizes
        @reference_cache()
        def test_reference_cache_default_size(value):
            return f"Reference: {value}"
        
        @calculation_cache()
        def test_calculation_cache_default_size(value):
            return f"Calculation: {value}"
        
        @ephemeris_cache()
        def test_ephemeris_cache_default_size(value):
            return f"Ephemeris: {value}"
        
        # Check that the new functions use the updated default cache sizes
        self.assertEqual(test_reference_cache_default_size.cache_info().maxsize, 100)
        self.assertEqual(test_calculation_cache_default_size.cache_info().maxsize, 200)
        self.assertEqual(test_ephemeris_cache_default_size.cache_info().maxsize, 300)
        
        # Print the cache sizes for reference
        print(f"Updated Default Cache Sizes:")
        print(f"  Reference: {test_reference_cache_default_size.cache_info().maxsize}")
        print(f"  Calculation: {test_calculation_cache_default_size.cache_info().maxsize}")
        print(f"  Ephemeris: {test_ephemeris_cache_default_size.cache_info().maxsize}")
    
    def test_disable_caching(self):
        """Test disabling caching"""
        # Disable caching
        CacheConfig.disable_all()
        
        # Create new functions with caching disabled
        @reference_cache()
        def test_reference_cache_disabled(value):
            # Simulate some work
            time.sleep(0.001)
            return f"Reference: {value}"
        
        # Call the function multiple times with the same value
        value = "test"
        
        # First call
        start_time = time.time()
        result1 = test_reference_cache_disabled(value)
        first_call_time = time.time() - start_time
        
        # Second call
        start_time = time.time()
        result2 = test_reference_cache_disabled(value)
        second_call_time = time.time() - start_time
        
        # Check that the results are the same
        self.assertEqual(result1, result2)
        
        # Check that the second call was not significantly faster
        # (caching is disabled, so both calls should take similar time)
        # Note: This test might be flaky due to system load, etc.
        # We use a very small threshold to account for this
        self.assertGreater(second_call_time, first_call_time * 0.5)
        
        # Print the call times for reference
        print(f"Disabled Caching Call Times:")
        print(f"  First Call: {first_call_time:.6f}s")
        print(f"  Second Call: {second_call_time:.6f}s")
        print(f"  Ratio: {second_call_time/first_call_time:.2f}x")


class TestCacheInvalidation(unittest.TestCase):
    """Test case for cache invalidation"""
    
    def setUp(self):
        """Set up test case"""
        # Clear all caches before each test
        clear_all_caches()
        
        # Ensure caching is enabled
        CacheConfig.enable_all()
    
    def test_manual_invalidation(self):
        """Test manual cache invalidation"""
        # Call the function to populate the cache
        test_reference_cache_custom_size("test")
        
        # Check that the cache is populated
        self.assertEqual(test_reference_cache_custom_size.cache_info().currsize, 1)
        
        # Clear the cache
        test_reference_cache_custom_size.cache_clear()
        
        # Check that the cache is cleared
        self.assertEqual(test_reference_cache_custom_size.cache_info().currsize, 0)
        
        # Print the cache info for reference
        print(f"Manual Invalidation Test:")
        print(f"  Current Size: {test_reference_cache_custom_size.cache_info().currsize}")
        print(f"  Hits: {test_reference_cache_custom_size.cache_info().hits}")
        print(f"  Misses: {test_reference_cache_custom_size.cache_info().misses}")
    
    def test_category_invalidation(self):
        """Test category cache invalidation"""
        # Call functions from different categories to populate the caches
        test_reference_cache_custom_size("test")
        test_calculation_cache_custom_size("test")
        test_ephemeris_cache_custom_size("test")
        
        # Check that the caches are populated
        self.assertEqual(test_reference_cache_custom_size.cache_info().currsize, 1)
        self.assertEqual(test_calculation_cache_custom_size.cache_info().currsize, 1)
        self.assertEqual(test_ephemeris_cache_custom_size.cache_info().currsize, 1)
        
        # Clear the reference cache
        clear_category_cache(CACHE_REFERENCE)
        
        # Check that the reference cache is cleared
        self.assertEqual(test_reference_cache_custom_size.cache_info().currsize, 0)
        
        # Check that the other caches are still populated
        self.assertEqual(test_calculation_cache_custom_size.cache_info().currsize, 1)
        self.assertEqual(test_ephemeris_cache_custom_size.cache_info().currsize, 1)
        
        # Print the cache sizes for reference
        print(f"Category Invalidation Test:")
        print(f"  Reference: {test_reference_cache_custom_size.cache_info().currsize}")
        print(f"  Calculation: {test_calculation_cache_custom_size.cache_info().currsize}")
        print(f"  Ephemeris: {test_ephemeris_cache_custom_size.cache_info().currsize}")
    
    def test_all_invalidation(self):
        """Test all cache invalidation"""
        # Call functions from different categories to populate the caches
        test_reference_cache_custom_size("test")
        test_calculation_cache_custom_size("test")
        test_ephemeris_cache_custom_size("test")
        
        # Check that the caches are populated
        self.assertEqual(test_reference_cache_custom_size.cache_info().currsize, 1)
        self.assertEqual(test_calculation_cache_custom_size.cache_info().currsize, 1)
        self.assertEqual(test_ephemeris_cache_custom_size.cache_info().currsize, 1)
        
        # Clear all caches
        clear_all_caches()
        
        # Check that all caches are cleared
        self.assertEqual(test_reference_cache_custom_size.cache_info().currsize, 0)
        self.assertEqual(test_calculation_cache_custom_size.cache_info().currsize, 0)
        self.assertEqual(test_ephemeris_cache_custom_size.cache_info().currsize, 0)
        
        # Print the cache sizes for reference
        print(f"All Invalidation Test:")
        print(f"  Reference: {test_reference_cache_custom_size.cache_info().currsize}")
        print(f"  Calculation: {test_calculation_cache_custom_size.cache_info().currsize}")
        print(f"  Ephemeris: {test_ephemeris_cache_custom_size.cache_info().currsize}")


if __name__ == '__main__':
    unittest.main()
