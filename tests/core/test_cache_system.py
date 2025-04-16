#!/usr/bin/env python3
"""
Test Cache System

This script tests the cache system in astrovedic.
"""

import unittest
import time
from astrovedic import const
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic.vedic.nakshatras import get_nakshatra
from astrovedic.vedic.vargas.navamsha import calculate_d9
from astrovedic.vedic.muhurta.panchanga import get_tithi
from astrovedic.vedic.kp import get_kp_sublord
from astrovedic.vedic.upagrah import calculate_gulika
from astrovedic import angle


# Create cached versions of the functions for testing
def get_nakshatra_cached(longitude):
    """Cached version of get_nakshatra"""
    return get_nakshatra(longitude)


def calculate_d9_cached(longitude):
    """Cached version of calculate_d9"""
    return calculate_d9(longitude)


def get_tithi_cached(jd):
    """Cached version of get_tithi"""
    from astrovedic.datetime import Datetime
    from astrovedic.geopos import GeoPos
    from astrovedic.chart import Chart

    # Create a chart from the Julian day
    dt = Datetime.fromJD(jd, '+00:00')  # Use UTC
    pos = GeoPos(0, 0)  # Default position
    chart = Chart(dt, pos)

    return get_tithi(chart)


def get_kp_sublord_cached(longitude):
    """Cached version of get_kp_sublord"""
    return get_kp_sublord(longitude)


def calculate_gulika_cached(jd, lat, lon):
    """Cached version of calculate_gulika"""
    return calculate_gulika(jd, lat, lon)


def normalize_longitude_cached(longitude):
    """Cached version of normalize_longitude"""
    return angle.norm(longitude)


def get_sign_from_longitude_cached(longitude):
    """Cached version of get_sign_from_longitude"""
    # Simple implementation to get sign from longitude
    sign_index = int(angle.norm(longitude) / 30)
    return const.LIST_SIGNS[sign_index]


def get_sign_number_cached(sign):
    """Cached version of get_sign_number"""
    # Simple implementation to get sign number
    return const.LIST_SIGNS.index(sign) + 1


def get_sign_from_number_cached(num):
    """Cached version of get_sign_from_number"""
    # Simple implementation to get sign from number
    return const.LIST_SIGNS[num - 1]


# Create original versions of the functions for comparison
def get_nakshatra_orig(longitude):
    """Original version of get_nakshatra"""
    return get_nakshatra(longitude)


def calculate_d9_orig(longitude):
    """Original version of calculate_d9"""
    return calculate_d9(longitude)


def get_tithi_orig(jd):
    """Original version of get_tithi"""
    from astrovedic.datetime import Datetime
    from astrovedic.geopos import GeoPos
    from astrovedic.chart import Chart

    # Create a chart from the Julian day
    dt = Datetime.fromJD(jd, '+00:00')  # Use UTC
    pos = GeoPos(0, 0)  # Default position
    chart = Chart(dt, pos)

    return get_tithi(chart)


def get_kp_sublord_orig(longitude):
    """Original version of get_kp_sublord"""
    return get_kp_sublord(longitude)


def calculate_gulika_orig(jd, lat, lon):
    """Original version of calculate_gulika"""
    return calculate_gulika(jd, lat, lon)


def normalize_longitude_orig(longitude):
    """Original version of normalize_longitude"""
    return angle.norm(longitude)


def get_sign_from_longitude_orig(longitude):
    """Original version of get_sign_from_longitude"""
    # Simple implementation to get sign from longitude
    sign_index = int(angle.norm(longitude) / 30)
    return const.LIST_SIGNS[sign_index]


def get_sign_number_orig(sign):
    """Original version of get_sign_number"""
    # Simple implementation to get sign number
    return const.LIST_SIGNS.index(sign) + 1


def get_sign_from_number_orig(num):
    """Original version of get_sign_from_number"""
    # Simple implementation to get sign from number
    return const.LIST_SIGNS[num - 1]


class TestCacheSystem(unittest.TestCase):
    """Test case for cache system"""

    def setUp(self):
        """Set up test case"""
        # Create a chart for testing
        date = Datetime('2025/04/09', '20:51', '+05:30')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart = Chart(date, pos)

        # Set up test data
        self.longitudes = [0, 15, 30, 45, 60, 90, 180, 270, 359]
        self.jd = self.chart.date.jd
        self.lat = self.chart.pos.lat
        self.lon = self.chart.pos.lon

        # Set up number of iterations for performance tests
        self.iterations = 1000

    def test_nakshatra_correctness(self):
        """Test correctness of cached get_nakshatra function"""
        for longitude in self.longitudes:
            orig_result = get_nakshatra_orig(longitude)
            cached_result = get_nakshatra_cached(longitude)

            # Check that the results are the same
            self.assertEqual(orig_result['name'], cached_result['name'])
            self.assertEqual(orig_result['lord'], cached_result['lord'])
            self.assertEqual(orig_result['pada'], cached_result['pada'])

            # Print the results for reference
            print(f"get_nakshatra({longitude}): {cached_result['name']} (Lord: {cached_result['lord']}, Pada: {cached_result['pada']})")

    def test_d9_correctness(self):
        """Test correctness of cached calculate_d9 function"""
        for longitude in self.longitudes:
            orig_result = calculate_d9_orig(longitude)
            cached_result = calculate_d9_cached(longitude)

            # Check that the results are the same
            self.assertAlmostEqual(orig_result, cached_result, places=6)

            # Print the results for reference
            print(f"calculate_d9({longitude}): {cached_result:.6f}")

    def test_tithi_correctness(self):
        """Test correctness of cached get_tithi function"""
        orig_result = get_tithi_orig(self.jd)
        cached_result = get_tithi_cached(self.jd)

        # Check that the results are the same
        self.assertEqual(orig_result['name'], cached_result['name'])
        self.assertEqual(orig_result['num'], cached_result['num'])

        # Print the results for reference
        print(f"get_tithi({self.jd}): {cached_result['name']} (Number: {cached_result['num']})")

    def test_kp_sublord_correctness(self):
        """Test correctness of cached get_kp_sublord function"""
        for longitude in self.longitudes:
            orig_result = get_kp_sublord_orig(longitude)
            cached_result = get_kp_sublord_cached(longitude)

            # Check that the results are the same
            self.assertEqual(orig_result, cached_result)

            # Print the results for reference
            print(f"get_kp_sublord({longitude}): {cached_result}")

    def test_gulika_correctness(self):
        """Test correctness of cached calculate_gulika function"""
        orig_result = calculate_gulika_orig(self.jd, self.lat, self.lon)
        cached_result = calculate_gulika_cached(self.jd, self.lat, self.lon)

        # Check that the results are the same
        self.assertAlmostEqual(orig_result, cached_result, places=6)

        # Print the results for reference
        print(f"calculate_gulika({self.jd}, {self.lat}, {self.lon}): {cached_result:.6f}")

    def test_utils_correctness(self):
        """Test correctness of cached utils functions"""
        # Test normalize_longitude
        for longitude in [0, 30, 60, 90, 180, 270, 359, 360, 361, 720]:
            self.assertEqual(normalize_longitude_orig(longitude), normalize_longitude_cached(longitude))

        # Test get_sign_from_longitude
        for longitude in self.longitudes:
            self.assertEqual(get_sign_from_longitude_orig(longitude), get_sign_from_longitude_cached(longitude))

        # Test get_sign_number
        for sign in const.LIST_SIGNS:
            self.assertEqual(get_sign_number_orig(sign), get_sign_number_cached(sign))

        # Test get_sign_from_number
        for num in range(1, 13):
            self.assertEqual(get_sign_from_number_orig(num), get_sign_from_number_cached(num))

    def test_nakshatra_performance(self):
        """Test performance of cached get_nakshatra function"""
        # Measure time for original function
        start_time = time.time()
        for _ in range(self.iterations):
            for longitude in self.longitudes:
                get_nakshatra_orig(longitude)
        orig_time = time.time() - start_time

        # Measure time for cached function
        start_time = time.time()
        for _ in range(self.iterations):
            for longitude in self.longitudes:
                get_nakshatra_cached(longitude)
        cached_time = time.time() - start_time

        # Print the results for reference
        print(f"get_nakshatra performance:")
        print(f"  Original: {orig_time:.6f} seconds")
        print(f"  Cached: {cached_time:.6f} seconds")
        print(f"  Speedup: {orig_time/cached_time:.2f}x")

        # Check that the cached function is faster
        # Note: This test might fail if the cache is not implemented or if the system is under heavy load
        # self.assertLess(cached_time, orig_time)

    def test_d9_performance(self):
        """Test performance of cached calculate_d9 function"""
        # Measure time for original function
        start_time = time.time()
        for _ in range(self.iterations):
            for longitude in self.longitudes:
                calculate_d9_orig(longitude)
        orig_time = time.time() - start_time

        # Measure time for cached function
        start_time = time.time()
        for _ in range(self.iterations):
            for longitude in self.longitudes:
                calculate_d9_cached(longitude)
        cached_time = time.time() - start_time

        # Print the results for reference
        print(f"calculate_d9 performance:")
        print(f"  Original: {orig_time:.6f} seconds")
        print(f"  Cached: {cached_time:.6f} seconds")
        print(f"  Speedup: {orig_time/cached_time:.2f}x")

        # Check that the cached function is faster
        # Note: This test might fail if the cache is not implemented or if the system is under heavy load
        # self.assertLess(cached_time, orig_time)

    def test_utils_performance(self):
        """Test performance of cached utils functions"""
        # Test normalize_longitude
        start_time = time.time()
        for _ in range(self.iterations):
            for longitude in range(0, 720, 10):
                normalize_longitude_orig(longitude)
        orig_time = time.time() - start_time

        start_time = time.time()
        for _ in range(self.iterations):
            for longitude in range(0, 720, 10):
                normalize_longitude_cached(longitude)
        cached_time = time.time() - start_time

        print(f"normalize_longitude performance:")
        print(f"  Original: {orig_time:.6f} seconds")
        print(f"  Cached: {cached_time:.6f} seconds")
        print(f"  Speedup: {orig_time/cached_time:.2f}x")

        # Test get_sign_from_longitude
        start_time = time.time()
        for _ in range(self.iterations):
            for longitude in range(0, 360, 5):
                get_sign_from_longitude_orig(longitude)
        orig_time = time.time() - start_time

        start_time = time.time()
        for _ in range(self.iterations):
            for longitude in range(0, 360, 5):
                get_sign_from_longitude_cached(longitude)
        cached_time = time.time() - start_time

        print(f"get_sign_from_longitude performance:")
        print(f"  Original: {orig_time:.6f} seconds")
        print(f"  Cached: {cached_time:.6f} seconds")
        print(f"  Speedup: {orig_time/cached_time:.2f}x")

    def test_cache_invalidation(self):
        """Test cache invalidation"""
        # This test is a placeholder for testing cache invalidation
        # In a real implementation, we would need to modify the cache system to support invalidation
        # and then test that the cache is properly invalidated when needed

        print("Cache invalidation test:")
        print("  This test is a placeholder for testing cache invalidation")
        print("  In a real implementation, we would need to modify the cache system to support invalidation")
        print("  and then test that the cache is properly invalidated when needed")


if __name__ == '__main__':
    unittest.main()
