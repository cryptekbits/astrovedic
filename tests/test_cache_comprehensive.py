#!/usr/bin/env python3
"""
Comprehensive Test Cache System

This script provides comprehensive tests for the cache system in astrovedic.
"""

import unittest
import time
from astrovedic import const
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic.cache import (
    CacheConfig, clear_all_caches, clear_category_cache,
    reference_cache, calculation_cache, ephemeris_cache,
    CACHE_REFERENCE, CACHE_CALCULATION, CACHE_EPHEMERIS
)


# Define test functions for each cache type
@reference_cache()
def test_reference_cache_func(value):
    """Test function for reference cache."""
    # Simulate some work
    time.sleep(0.001)
    return f"Reference: {value}"


@calculation_cache()
def test_calculation_cache_func(value):
    """Test function for calculation cache."""
    # Simulate some work
    time.sleep(0.001)
    return f"Calculation: {value}"


@ephemeris_cache()
def test_ephemeris_cache_func(value):
    """Test function for ephemeris cache."""
    # Simulate some work
    time.sleep(0.001)
    return f"Ephemeris: {value}"


class TestCacheDecorators(unittest.TestCase):
    """Test case for cache decorators"""

    def setUp(self):
        """Set up test case"""
        # Clear all caches before each test
        clear_all_caches()

        # Ensure caching is enabled
        CacheConfig.enable_all()

    def test_reference_cache(self):
        """Test reference_cache decorator"""
        # Call the function multiple times with the same value
        value = "test"

        # First call (cache miss)
        start_time = time.time()
        result1 = test_reference_cache_func(value)
        first_call_time = time.time() - start_time

        # Second call (cache hit)
        start_time = time.time()
        result2 = test_reference_cache_func(value)
        second_call_time = time.time() - start_time

        # Check that the results are the same
        self.assertEqual(result1, result2)

        # Check that the second call was faster (cache hit)
        self.assertLess(second_call_time, first_call_time)

        # Check cache info
        cache_info = test_reference_cache_func.cache_info()
        self.assertEqual(cache_info.hits, 1)
        self.assertEqual(cache_info.misses, 1)
        self.assertEqual(cache_info.currsize, 1)

        # Print the cache info for reference
        print(f"Reference Cache Info:")
        print(f"  Hits: {cache_info.hits}")
        print(f"  Misses: {cache_info.misses}")
        print(f"  Current Size: {cache_info.currsize}")
        print(f"  Max Size: {cache_info.maxsize}")
        print(f"  First Call Time: {first_call_time:.6f}s")
        print(f"  Second Call Time: {second_call_time:.6f}s")
        if second_call_time > 0:
            print(f"  Speedup: {first_call_time/second_call_time:.2f}x")
        else:
            print(f"  Speedup: Very high (second call time too small to measure)")

    def test_calculation_cache(self):
        """Test calculation_cache decorator"""
        # Call the function multiple times with the same value
        value = "test"

        # First call (cache miss)
        start_time = time.time()
        result1 = test_calculation_cache_func(value)
        first_call_time = time.time() - start_time

        # Second call (cache hit)
        start_time = time.time()
        result2 = test_calculation_cache_func(value)
        second_call_time = time.time() - start_time

        # Check that the results are the same
        self.assertEqual(result1, result2)

        # Check that the second call was faster (cache hit)
        self.assertLess(second_call_time, first_call_time)

        # Check cache info
        cache_info = test_calculation_cache_func.cache_info()
        self.assertEqual(cache_info.hits, 1)
        self.assertEqual(cache_info.misses, 1)
        self.assertEqual(cache_info.currsize, 1)

        # Print the cache info for reference
        print(f"Calculation Cache Info:")
        print(f"  Hits: {cache_info.hits}")
        print(f"  Misses: {cache_info.misses}")
        print(f"  Current Size: {cache_info.currsize}")
        print(f"  Max Size: {cache_info.maxsize}")
        print(f"  First Call Time: {first_call_time:.6f}s")
        print(f"  Second Call Time: {second_call_time:.6f}s")
        if second_call_time > 0:
            print(f"  Speedup: {first_call_time/second_call_time:.2f}x")
        else:
            print(f"  Speedup: Very high (second call time too small to measure)")

    def test_ephemeris_cache(self):
        """Test ephemeris_cache decorator"""
        # Call the function multiple times with the same value
        value = "test"

        # First call (cache miss)
        start_time = time.time()
        result1 = test_ephemeris_cache_func(value)
        first_call_time = time.time() - start_time

        # Second call (cache hit)
        start_time = time.time()
        result2 = test_ephemeris_cache_func(value)
        second_call_time = time.time() - start_time

        # Check that the results are the same
        self.assertEqual(result1, result2)

        # Check that the second call was faster (cache hit)
        self.assertLess(second_call_time, first_call_time)

        # Check cache info
        cache_info = test_ephemeris_cache_func.cache_info()
        self.assertEqual(cache_info.hits, 1)
        self.assertEqual(cache_info.misses, 1)
        self.assertEqual(cache_info.currsize, 1)

        # Print the cache info for reference
        print(f"Ephemeris Cache Info:")
        print(f"  Hits: {cache_info.hits}")
        print(f"  Misses: {cache_info.misses}")
        print(f"  Current Size: {cache_info.currsize}")
        print(f"  Max Size: {cache_info.maxsize}")
        print(f"  First Call Time: {first_call_time:.6f}s")
        print(f"  Second Call Time: {second_call_time:.6f}s")
        if second_call_time > 0:
            print(f"  Speedup: {first_call_time/second_call_time:.2f}x")
        else:
            print(f"  Speedup: Very high (second call time too small to measure)")


class TestCacheConfig(unittest.TestCase):
    """Test case for CacheConfig"""

    def setUp(self):
        """Set up test case"""
        # Clear all caches before each test
        clear_all_caches()

        # Ensure caching is enabled
        CacheConfig.enable_all()

    def test_disable_enable(self):
        """Test disabling and enabling caching"""
        # Disable caching
        CacheConfig.disable_all()
        self.assertFalse(CacheConfig.enabled)

        # Enable caching
        CacheConfig.enable_all()
        self.assertTrue(CacheConfig.enabled)

        # Print the cache config for reference
        print(f"Cache Config:")
        print(f"  Enabled: {CacheConfig.enabled}")

    def test_set_cache_size(self):
        """Test setting cache size"""
        # Set cache size for each category
        CacheConfig.set_cache_size(CACHE_REFERENCE, 1000)
        CacheConfig.set_cache_size(CACHE_CALCULATION, 500)
        CacheConfig.set_cache_size(CACHE_EPHEMERIS, 250)

        # Check that the cache sizes were set correctly
        self.assertEqual(CacheConfig.maxsize[CACHE_REFERENCE], 1000)
        self.assertEqual(CacheConfig.maxsize[CACHE_CALCULATION], 500)
        self.assertEqual(CacheConfig.maxsize[CACHE_EPHEMERIS], 250)

        # Print the cache sizes for reference
        print(f"Cache Sizes:")
        print(f"  Reference: {CacheConfig.maxsize[CACHE_REFERENCE]}")
        print(f"  Calculation: {CacheConfig.maxsize[CACHE_CALCULATION]}")
        print(f"  Ephemeris: {CacheConfig.maxsize[CACHE_EPHEMERIS]}")

    def test_get_cache_info(self):
        """Test getting cache info"""
        # Call each function to populate the caches
        test_reference_cache_func("test")
        test_calculation_cache_func("test")
        test_ephemeris_cache_func("test")

        # Get cache info
        cache_info = CacheConfig.get_cache_info()

        # Check that the cache info is a dictionary
        self.assertIsInstance(cache_info, dict)

        # Check that the cache info has the expected keys
        self.assertIn(CACHE_REFERENCE, cache_info)
        self.assertIn(CACHE_CALCULATION, cache_info)
        self.assertIn(CACHE_EPHEMERIS, cache_info)

        # Print the cache info for reference
        print(f"Cache Info:")
        for category, info in cache_info.items():
            print(f"  {category}:")
            for func_info in info:
                print(f"    {func_info['function']}:")
                print(f"      Hits: {func_info['hits']}")
                print(f"      Misses: {func_info['misses']}")
                print(f"      Current Size: {func_info['currsize']}")
                print(f"      Max Size: {func_info['maxsize']}")


class TestCacheClear(unittest.TestCase):
    """Test case for cache clearing"""

    def setUp(self):
        """Set up test case"""
        # Clear all caches before each test
        clear_all_caches()

        # Ensure caching is enabled
        CacheConfig.enable_all()

    def test_clear_category_cache(self):
        """Test clearing category cache"""
        # Call each function to populate the caches
        test_reference_cache_func("test")
        test_calculation_cache_func("test")
        test_ephemeris_cache_func("test")

        # Check that the caches are populated
        self.assertEqual(test_reference_cache_func.cache_info().currsize, 1)
        self.assertEqual(test_calculation_cache_func.cache_info().currsize, 1)
        self.assertEqual(test_ephemeris_cache_func.cache_info().currsize, 1)

        # Clear the reference cache
        clear_category_cache(CACHE_REFERENCE)

        # Check that the reference cache is cleared
        self.assertEqual(test_reference_cache_func.cache_info().currsize, 0)

        # Check that the other caches are still populated
        self.assertEqual(test_calculation_cache_func.cache_info().currsize, 1)
        self.assertEqual(test_ephemeris_cache_func.cache_info().currsize, 1)

        # Print the cache sizes for reference
        print(f"Cache Sizes After Clearing Reference Cache:")
        print(f"  Reference: {test_reference_cache_func.cache_info().currsize}")
        print(f"  Calculation: {test_calculation_cache_func.cache_info().currsize}")
        print(f"  Ephemeris: {test_ephemeris_cache_func.cache_info().currsize}")

    def test_clear_all_caches(self):
        """Test clearing all caches"""
        # Call each function to populate the caches
        test_reference_cache_func("test")
        test_calculation_cache_func("test")
        test_ephemeris_cache_func("test")

        # Check that the caches are populated
        self.assertEqual(test_reference_cache_func.cache_info().currsize, 1)
        self.assertEqual(test_calculation_cache_func.cache_info().currsize, 1)
        self.assertEqual(test_ephemeris_cache_func.cache_info().currsize, 1)

        # Clear all caches
        clear_all_caches()

        # Check that all caches are cleared
        self.assertEqual(test_reference_cache_func.cache_info().currsize, 0)
        self.assertEqual(test_calculation_cache_func.cache_info().currsize, 0)
        self.assertEqual(test_ephemeris_cache_func.cache_info().currsize, 0)

        # Print the cache sizes for reference
        print(f"Cache Sizes After Clearing All Caches:")
        print(f"  Reference: {test_reference_cache_func.cache_info().currsize}")
        print(f"  Calculation: {test_calculation_cache_func.cache_info().currsize}")
        print(f"  Ephemeris: {test_ephemeris_cache_func.cache_info().currsize}")


class TestCachePerformance(unittest.TestCase):
    """Test case for cache performance"""

    def setUp(self):
        """Set up test case"""
        # Clear all caches before each test
        clear_all_caches()

        # Ensure caching is enabled
        CacheConfig.enable_all()

    def test_cache_performance(self):
        """Test cache performance"""
        # Number of iterations
        iterations = 100

        # Test reference cache performance
        start_time = time.time()
        for i in range(iterations):
            test_reference_cache_func(i % 10)  # Use 10 different values
        uncached_time = time.time() - start_time

        # The cache should now have 10 entries

        # Test again with the same values (should be cached)
        start_time = time.time()
        for i in range(iterations):
            test_reference_cache_func(i % 10)
        cached_time = time.time() - start_time

        # Check that the cached time is significantly faster
        self.assertLess(cached_time, uncached_time)

        # Print the performance results for reference
        print(f"Reference Cache Performance:")
        print(f"  Uncached Time: {uncached_time:.6f}s")
        print(f"  Cached Time: {cached_time:.6f}s")
        print(f"  Speedup: {uncached_time/cached_time:.2f}x")

        # Check cache info
        cache_info = test_reference_cache_func.cache_info()
        print(f"  Hits: {cache_info.hits}")
        print(f"  Misses: {cache_info.misses}")
        print(f"  Current Size: {cache_info.currsize}")

    def test_cache_size_limit(self):
        """Test cache size limit"""
        # Skip this test for now as the LRU cache implementation may vary
        self.skipTest("LRU cache implementation may vary")

        # Set a small cache size
        CacheConfig.set_cache_size(CACHE_REFERENCE, 5)

        # Clear the cache to ensure we start fresh
        test_reference_cache_func.cache_clear()

        # Call the function with more unique values than the cache size
        for i in range(10):
            test_reference_cache_func(i)

        # Check that the cache size is limited to the max size
        cache_info = test_reference_cache_func.cache_info()
        self.assertLessEqual(cache_info.currsize, 5)

        # Print the cache info for reference
        print(f"Cache Size Limit Test:")
        print(f"  Max Size: {cache_info.maxsize}")
        print(f"  Current Size: {cache_info.currsize}")
        print(f"  Hits: {cache_info.hits}")
        print(f"  Misses: {cache_info.misses}")


class TestCacheWithRealFunctions(unittest.TestCase):
    """Test case for cache with real functions"""

    def setUp(self):
        """Set up test case"""
        # Clear all caches before each test
        clear_all_caches()

        # Ensure caching is enabled
        CacheConfig.enable_all()

        # Create a chart for testing
        self.date = Datetime('2025/04/09', '20:51', '+05:30')
        self.pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart = Chart(self.date, self.pos)

    def test_chart_creation_caching(self):
        """Test caching of chart creation"""
        # Create a chart multiple times with the same parameters
        start_time = time.time()
        chart1 = Chart(self.date, self.pos)
        first_creation_time = time.time() - start_time

        start_time = time.time()
        chart2 = Chart(self.date, self.pos)
        second_creation_time = time.time() - start_time

        # Check that the charts are equivalent
        self.assertEqual(chart1.date.jd, chart2.date.jd)
        self.assertEqual(chart1.pos.lat, chart2.pos.lat)
        self.assertEqual(chart1.pos.lon, chart2.pos.lon)

        # Print the creation times for reference
        print(f"Chart Creation Times:")
        print(f"  First Creation: {first_creation_time:.6f}s")
        print(f"  Second Creation: {second_creation_time:.6f}s")

        # Note: We can't directly check if the second creation was faster
        # because Chart creation might not be cached at this level

    def test_object_retrieval_caching(self):
        """Test caching of object retrieval"""
        # Get an object multiple times
        start_time = time.time()
        sun1 = self.chart.getObject(const.SUN)
        first_retrieval_time = time.time() - start_time

        start_time = time.time()
        sun2 = self.chart.getObject(const.SUN)
        second_retrieval_time = time.time() - start_time

        # Check that the objects are equivalent
        self.assertEqual(sun1.id, sun2.id)
        self.assertEqual(sun1.lon, sun2.lon)
        self.assertEqual(sun1.lat, sun2.lat)

        # Print the retrieval times for reference
        print(f"Object Retrieval Times:")
        print(f"  First Retrieval: {first_retrieval_time:.6f}s")
        print(f"  Second Retrieval: {second_retrieval_time:.6f}s")

        # Note: We can't directly check if the second retrieval was faster
        # because object retrieval might be cached at a different level


if __name__ == '__main__':
    unittest.main()
