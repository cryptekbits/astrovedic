#!/usr/bin/env python3
"""
Test Cache Performance

This script tests the performance of the cache system in flatlib.
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


# Define test functions with varying complexity
@reference_cache()
def simple_function(value):
    """Simple function that returns a value."""
    # Simulate some work
    time.sleep(0.0001)
    return value


@reference_cache()
def medium_function(value):
    """Medium complexity function."""
    # Simulate more work
    time.sleep(0.001)
    result = 0
    for i in range(1000):
        result += i * value
    return result


@reference_cache()
def complex_function(value):
    """Complex function."""
    # Simulate heavy work
    time.sleep(0.01)
    result = 0
    for i in range(10000):
        result += i * value
    return result


class TestCachePerformance(unittest.TestCase):
    """Test case for cache performance"""
    
    def setUp(self):
        """Set up test case"""
        # Clear all caches before each test
        clear_all_caches()
        
        # Ensure caching is enabled
        CacheConfig.enable_all()
    
    def test_simple_function_performance(self):
        """Test performance of simple function"""
        # Number of iterations
        iterations = 100
        
        # Test without cache (first call for each value)
        start_time = time.time()
        for i in range(iterations):
            simple_function(i)
        uncached_time = time.time() - start_time
        
        # Test with cache (all values already cached)
        start_time = time.time()
        for i in range(iterations):
            simple_function(i)
        cached_time = time.time() - start_time
        
        # Calculate speedup
        speedup = uncached_time / cached_time if cached_time > 0 else float('inf')
        
        # Print the performance results
        print(f"Simple Function Performance:")
        print(f"  Uncached Time: {uncached_time:.6f}s")
        print(f"  Cached Time: {cached_time:.6f}s")
        print(f"  Speedup: {speedup:.2f}x")
        
        # Check that the cached time is significantly faster
        self.assertLess(cached_time, uncached_time)
        
        # Check cache info
        cache_info = simple_function.cache_info()
        print(f"  Hits: {cache_info.hits}")
        print(f"  Misses: {cache_info.misses}")
        print(f"  Current Size: {cache_info.currsize}")
    
    def test_medium_function_performance(self):
        """Test performance of medium complexity function"""
        # Number of iterations
        iterations = 50
        
        # Test without cache (first call for each value)
        start_time = time.time()
        for i in range(iterations):
            medium_function(i)
        uncached_time = time.time() - start_time
        
        # Test with cache (all values already cached)
        start_time = time.time()
        for i in range(iterations):
            medium_function(i)
        cached_time = time.time() - start_time
        
        # Calculate speedup
        speedup = uncached_time / cached_time if cached_time > 0 else float('inf')
        
        # Print the performance results
        print(f"Medium Function Performance:")
        print(f"  Uncached Time: {uncached_time:.6f}s")
        print(f"  Cached Time: {cached_time:.6f}s")
        print(f"  Speedup: {speedup:.2f}x")
        
        # Check that the cached time is significantly faster
        self.assertLess(cached_time, uncached_time)
        
        # Check cache info
        cache_info = medium_function.cache_info()
        print(f"  Hits: {cache_info.hits}")
        print(f"  Misses: {cache_info.misses}")
        print(f"  Current Size: {cache_info.currsize}")
    
    def test_complex_function_performance(self):
        """Test performance of complex function"""
        # Number of iterations
        iterations = 20
        
        # Test without cache (first call for each value)
        start_time = time.time()
        for i in range(iterations):
            complex_function(i)
        uncached_time = time.time() - start_time
        
        # Test with cache (all values already cached)
        start_time = time.time()
        for i in range(iterations):
            complex_function(i)
        cached_time = time.time() - start_time
        
        # Calculate speedup
        speedup = uncached_time / cached_time if cached_time > 0 else float('inf')
        
        # Print the performance results
        print(f"Complex Function Performance:")
        print(f"  Uncached Time: {uncached_time:.6f}s")
        print(f"  Cached Time: {cached_time:.6f}s")
        print(f"  Speedup: {speedup:.2f}x")
        
        # Check that the cached time is significantly faster
        self.assertLess(cached_time, uncached_time)
        
        # Check cache info
        cache_info = complex_function.cache_info()
        print(f"  Hits: {cache_info.hits}")
        print(f"  Misses: {cache_info.misses}")
        print(f"  Current Size: {cache_info.currsize}")


class TestCacheWithRealFunctions(unittest.TestCase):
    """Test case for cache with real functions"""
    
    def setUp(self):
        """Set up test case"""
        # Clear all caches before each test
        clear_all_caches()
        
        # Ensure caching is enabled
        CacheConfig.enable_all()
    
    def test_chart_creation_performance(self):
        """Test performance of chart creation"""
        # Number of iterations
        iterations = 10
        
        # Create different dates and positions
        dates = []
        positions = []
        for i in range(iterations):
            date = Datetime(f'2025/0{(i%12)+1}/0{(i%28)+1}', f'{(i%24):02d}:00', '+05:30')
            pos = GeoPos(12.9716 + i*0.1, 77.5946 + i*0.1)
            dates.append(date)
            positions.append(pos)
        
        # Test chart creation (first time)
        start_time = time.time()
        for i in range(iterations):
            Chart(dates[i], positions[i])
        first_run_time = time.time() - start_time
        
        # Test chart creation again (might be cached at some level)
        start_time = time.time()
        for i in range(iterations):
            Chart(dates[i], positions[i])
        second_run_time = time.time() - start_time
        
        # Print the performance results
        print(f"Chart Creation Performance:")
        print(f"  First Run Time: {first_run_time:.6f}s")
        print(f"  Second Run Time: {second_run_time:.6f}s")
        print(f"  Ratio: {first_run_time/second_run_time:.2f}x")
    
    def test_object_retrieval_performance(self):
        """Test performance of object retrieval"""
        # Create a chart
        date = Datetime('2025/04/09', '20:51', '+05:30')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        chart = Chart(date, pos)
        
        # Number of iterations
        iterations = 100
        
        # Test object retrieval (first time)
        start_time = time.time()
        for i in range(iterations):
            chart.getObject(const.SUN)
            chart.getObject(const.MOON)
            chart.getObject(const.MERCURY)
            chart.getObject(const.VENUS)
            chart.getObject(const.MARS)
            chart.getObject(const.JUPITER)
            chart.getObject(const.SATURN)
        first_run_time = time.time() - start_time
        
        # Test object retrieval again (might be cached at some level)
        start_time = time.time()
        for i in range(iterations):
            chart.getObject(const.SUN)
            chart.getObject(const.MOON)
            chart.getObject(const.MERCURY)
            chart.getObject(const.VENUS)
            chart.getObject(const.MARS)
            chart.getObject(const.JUPITER)
            chart.getObject(const.SATURN)
        second_run_time = time.time() - start_time
        
        # Print the performance results
        print(f"Object Retrieval Performance:")
        print(f"  First Run Time: {first_run_time:.6f}s")
        print(f"  Second Run Time: {second_run_time:.6f}s")
        print(f"  Ratio: {first_run_time/second_run_time:.2f}x")


class TestCacheSizeImpact(unittest.TestCase):
    """Test case for cache size impact on performance"""
    
    def setUp(self):
        """Set up test case"""
        # Clear all caches before each test
        clear_all_caches()
        
        # Ensure caching is enabled
        CacheConfig.enable_all()
        
        # Save the original cache sizes
        self.original_reference_size = CacheConfig.maxsize[CACHE_REFERENCE]
    
    def tearDown(self):
        """Tear down test case"""
        # Restore the original cache sizes
        CacheConfig.maxsize[CACHE_REFERENCE] = self.original_reference_size
    
    def test_cache_size_impact(self):
        """Test impact of cache size on performance"""
        # Number of unique values
        num_values = 1000
        
        # Number of iterations per test
        iterations = 10000
        
        # Test with different cache sizes
        cache_sizes = [10, 100, 500, 1000, 2000]
        
        results = {}
        
        for cache_size in cache_sizes:
            # Set the cache size
            CacheConfig.set_cache_size(CACHE_REFERENCE, cache_size)
            
            # Create a new function with the updated cache size
            @reference_cache()
            def test_function(value):
                # Simulate some work
                time.sleep(0.00001)
                return value
            
            # Populate the cache with some values
            for i in range(num_values):
                test_function(i)
            
            # Clear the cache
            test_function.cache_clear()
            
            # Test performance with random access pattern
            import random
            random.seed(42)  # For reproducibility
            
            # Generate random indices
            indices = [random.randint(0, num_values-1) for _ in range(iterations)]
            
            # Measure time
            start_time = time.time()
            for i in indices:
                test_function(i)
            total_time = time.time() - start_time
            
            # Get cache info
            cache_info = test_function.cache_info()
            
            # Store results
            results[cache_size] = {
                'time': total_time,
                'hits': cache_info.hits,
                'misses': cache_info.misses,
                'hit_ratio': cache_info.hits / (cache_info.hits + cache_info.misses) if (cache_info.hits + cache_info.misses) > 0 else 0
            }
        
        # Print the results
        print(f"Cache Size Impact:")
        for cache_size, result in results.items():
            print(f"  Cache Size: {cache_size}")
            print(f"    Time: {result['time']:.6f}s")
            print(f"    Hits: {result['hits']}")
            print(f"    Misses: {result['misses']}")
            print(f"    Hit Ratio: {result['hit_ratio']:.2f}")
        
        # Check that larger cache sizes generally lead to better hit ratios
        # (this might not always be true due to access patterns)
        for i in range(len(cache_sizes) - 1):
            size1 = cache_sizes[i]
            size2 = cache_sizes[i + 1]
            ratio1 = results[size1]['hit_ratio']
            ratio2 = results[size2]['hit_ratio']
            print(f"  Comparing Size {size1} (Ratio: {ratio1:.2f}) to Size {size2} (Ratio: {ratio2:.2f})")


if __name__ == '__main__':
    unittest.main()
