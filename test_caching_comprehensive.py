#!/usr/bin/env python3
"""
Comprehensive test script for caching functionality in flatlib
"""

import time
import unittest
from flatlib import const
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib.cache import clear_all_caches, CacheConfig

# Import original functions
from flatlib.vedic.utils import get_sign_lord as get_sign_lord_orig
from flatlib.vedic.nakshatras import get_nakshatra as get_nakshatra_orig
from flatlib.vedic.vargas.navamsha import calculate_d9 as calculate_d9_orig
from flatlib.vedic.panchang import get_tithi as get_tithi_orig
from flatlib.ephem.swe import sweObject as sweObject_orig
from flatlib.ephem.eph import getObject as getObject_orig

# Import cached functions
from flatlib.vedic.utils_cached import get_sign_lord as get_sign_lord_cached
from flatlib.vedic.nakshatras_cached import get_nakshatra as get_nakshatra_cached
from flatlib.vedic.vargas.cached import calculate_d9 as calculate_d9_cached
from flatlib.vedic.panchang_cached import get_tithi as get_tithi_cached
from flatlib.ephem.swe_cached import sweObject as sweObject_cached
from flatlib.ephem.eph_cached import getObject as getObject_cached


class TestCaching(unittest.TestCase):
    """Test the caching implementation."""

    def setUp(self):
        """Set up the test case."""
        # Clear all caches before each test
        clear_all_caches()
        
        # Enable caching
        CacheConfig.enable_all()
        
        # Set up test data
        self.jd = 2460000.5  # Example Julian day
        self.lat = 12.9716  # Bangalore latitude
        self.lon = 77.5946  # Bangalore longitude
        self.planets = [const.SUN, const.MOON, const.JUPITER, const.SATURN]
        self.signs = const.LIST_SIGNS
        self.longitudes = [0, 15, 30, 45, 60, 90, 180, 270, 359]
        self.iterations = 100  # Number of iterations for performance tests

    def test_reference_data_caching(self):
        """Test reference data caching."""
        print("\nTesting reference data caching...")
        
        # Test get_sign_lord
        for sign in self.signs:
            orig = get_sign_lord_orig(sign)
            cached = get_sign_lord_cached(sign)
            self.assertEqual(orig, cached)
        
        # Performance test
        start_time = time.time()
        for _ in range(self.iterations):
            for sign in self.signs:
                get_sign_lord_orig(sign)
        orig_time = time.time() - start_time
        
        start_time = time.time()
        for _ in range(self.iterations):
            for sign in self.signs:
                get_sign_lord_cached(sign)
        cached_time = time.time() - start_time
        
        print(f"get_sign_lord: Original: {orig_time:.6f}s, Cached: {cached_time:.6f}s, Speedup: {orig_time/cached_time:.2f}x")
        self.assertLess(cached_time, orig_time)

    def test_calculation_caching(self):
        """Test calculation caching."""
        print("\nTesting calculation caching...")
        
        # Test calculate_d9
        for lon in self.longitudes:
            orig = round(calculate_d9_orig(lon), 8)
            cached = calculate_d9_cached(lon)
            self.assertEqual(orig, cached)
        
        # Test get_tithi
        orig_result = get_tithi_orig(self.jd)
        cached_result = get_tithi_cached(self.jd)
        self.assertEqual(orig_result['name'], cached_result['name'])
        
        # Performance test
        start_time = time.time()
        for _ in range(self.iterations):
            for lon in self.longitudes:
                calculate_d9_orig(lon)
        orig_time = time.time() - start_time
        
        start_time = time.time()
        for _ in range(self.iterations):
            for lon in self.longitudes:
                calculate_d9_cached(lon)
        cached_time = time.time() - start_time
        
        print(f"calculate_d9: Original: {orig_time:.6f}s, Cached: {cached_time:.6f}s, Speedup: {orig_time/cached_time:.2f}x")
        self.assertLess(cached_time, orig_time)

    def test_ephemeris_caching(self):
        """Test ephemeris caching."""
        print("\nTesting ephemeris caching...")
        
        # Test sweObject
        for planet in self.planets:
            orig = sweObject_orig(planet, self.jd)
            cached = sweObject_cached(planet, self.jd)
            self.assertEqual(orig['lon'], cached['lon'])
            self.assertEqual(orig['lat'], cached['lat'])
        
        # Test getObject
        for planet in self.planets:
            orig = getObject_orig(planet, self.jd, self.lat, self.lon)
            cached = getObject_cached(planet, self.jd, self.lat, self.lon)
            self.assertEqual(orig['lon'], cached['lon'])
            self.assertEqual(orig['sign'], cached['sign'])
        
        # Performance test
        start_time = time.time()
        for _ in range(self.iterations):
            for planet in self.planets:
                sweObject_orig(planet, self.jd)
        orig_time = time.time() - start_time
        
        start_time = time.time()
        for _ in range(self.iterations):
            for planet in self.planets:
                sweObject_cached(planet, self.jd)
        cached_time = time.time() - start_time
        
        print(f"sweObject: Original: {orig_time:.6f}s, Cached: {cached_time:.6f}s, Speedup: {orig_time/cached_time:.2f}x")
        self.assertLess(cached_time, orig_time)

    def test_cache_config(self):
        """Test the CacheConfig class."""
        print("\nTesting CacheConfig...")
        
        # Test disabling caching
        CacheConfig.disable_all()
        self.assertFalse(CacheConfig.enabled)
        
        # Test enabling caching
        CacheConfig.enable_all()
        self.assertTrue(CacheConfig.enabled)
        
        # Test setting cache size
        CacheConfig.set_cache_size('reference_data', 500)
        self.assertEqual(CacheConfig.maxsize['reference_data'], 500)
        
        # Test getting cache info
        cache_info = CacheConfig.get_cache_info()
        self.assertIsInstance(cache_info, dict)
        self.assertIn('reference_data', cache_info)
        self.assertIn('calculations', cache_info)
        self.assertIn('ephemeris', cache_info)

    def test_cache_invalidation(self):
        """Test cache invalidation."""
        print("\nTesting cache invalidation...")
        
        # Fill the cache
        for sign in self.signs:
            get_sign_lord_cached(sign)
        
        # Get cache info before clearing
        cache_info_before = CacheConfig.get_cache_info()
        
        # Clear the cache
        clear_all_caches()
        
        # Get cache info after clearing
        cache_info_after = CacheConfig.get_cache_info()
        
        # Check that the cache was cleared
        for category in cache_info_after:
            for func_info in cache_info_after[category]:
                self.assertEqual(func_info['currsize'], 0)
        
        print("Cache invalidation working correctly")

    def test_real_world_scenario(self):
        """Test a real-world scenario with chart calculations."""
        print("\nTesting real-world scenario...")
        
        # Create a chart
        date = Datetime('2025/04/09', '20:51', '+05:30')
        pos = GeoPos(self.lat, self.lon)
        chart = Chart(date, pos, hsys=const.HOUSES_PLACIDUS)
        
        # Get nakshatra information for the Moon
        moon = chart.getObject(const.MOON)
        
        # Test with original function
        start_time = time.time()
        for _ in range(self.iterations):
            nakshatra_info_orig = get_nakshatra_orig(moon.lon)
        orig_time = time.time() - start_time
        
        # Test with cached function
        start_time = time.time()
        for _ in range(self.iterations):
            nakshatra_info_cached = get_nakshatra_cached(moon.lon)
        cached_time = time.time() - start_time
        
        print(f"Real-world nakshatra lookup: Original: {orig_time:.6f}s, Cached: {cached_time:.6f}s, Speedup: {orig_time/cached_time:.2f}x")
        self.assertLess(cached_time, orig_time)
        
        # Verify results are the same
        self.assertEqual(nakshatra_info_orig['name'], nakshatra_info_cached['name'])
        self.assertEqual(nakshatra_info_orig['lord'], nakshatra_info_cached['lord'])


if __name__ == '__main__':
    unittest.main()
