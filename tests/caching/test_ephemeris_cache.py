#!/usr/bin/env python3
"""
Simple test script for ephemeris caching functionality
"""

import time
from astrovedic import const
from astrovedic.cache import clear_all_caches, CacheConfig

# Import original functions
from astrovedic.ephem.swe import sweObject as sweObject_orig
from astrovedic.ephem.swe import sweHouses as sweHouses_orig
from astrovedic.ephem.swe import sweFixedStar as sweFixedStar_orig
from astrovedic.ephem.eph import getObject as getObject_orig
from astrovedic.ephem.eph import getHouses as getHouses_orig

# Import cached functions
from astrovedic.ephem.swe_cached import sweObject as sweObject_cached
from astrovedic.ephem.swe_cached import sweHouses as sweHouses_cached
from astrovedic.ephem.swe_cached import sweFixedStar as sweFixedStar_cached
from astrovedic.ephem.eph_cached import getObject as getObject_cached
from astrovedic.ephem.eph_cached import getHouses as getHouses_cached

def test_correctness():
    """Test that cached functions produce the same results as original functions."""
    print("Testing correctness...")

    # Test sweObject
    jd = 2460000.5  # Example Julian day
    for planet in [const.SUN, const.MOON, const.JUPITER, const.SATURN]:
        orig = sweObject_orig(planet, jd)
        cached = sweObject_cached(planet, jd)
        if orig['lon'] != cached['lon'] or orig['lat'] != cached['lat']:
            print(f"Error: sweObject({planet}, {jd}) - Original: {orig['lon']}, {orig['lat']}, Cached: {cached['lon']}, {cached['lat']}")
        else:
            print(f"sweObject({planet}, {jd}) - OK")

    # Test sweHouses
    lat, lon = 12.9716, 77.5946  # Bangalore
    hsys = const.HOUSES_PLACIDUS
    orig_houses, orig_angles = sweHouses_orig(jd, lat, lon, hsys)
    cached_houses, cached_angles = sweHouses_cached(jd, lat, lon, hsys)

    # Check first house and Ascendant
    if orig_houses[0]['lon'] != cached_houses[0]['lon']:
        print(f"Error: sweHouses({jd}, {lat}, {lon}, {hsys}) - Original House1: {orig_houses[0]['lon']}, Cached House1: {cached_houses[0]['lon']}")
    else:
        print(f"sweHouses({jd}, {lat}, {lon}, {hsys}) House1 - OK")

    if orig_angles[0]['lon'] != cached_angles[0]['lon']:
        print(f"Error: sweHouses({jd}, {lat}, {lon}, {hsys}) - Original ASC: {orig_angles[0]['lon']}, Cached ASC: {cached_angles[0]['lon']}")
    else:
        print(f"sweHouses({jd}, {lat}, {lon}, {hsys}) ASC - OK")

    # Test sweFixedStar
    star = "Spica"
    orig = sweFixedStar_orig(star, jd)
    cached = sweFixedStar_cached(star, jd)
    if orig['lon'] != cached['lon'] or orig['lat'] != cached['lat']:
        print(f"Error: sweFixedStar({star}, {jd}) - Original: {orig['lon']}, {orig['lat']}, Cached: {cached['lon']}, {cached['lat']}")
    else:
        print(f"sweFixedStar({star}, {jd}) - OK")

    # Test getObject
    lat, lon = 12.9716, 77.5946  # Bangalore
    for planet in [const.SUN, const.MOON, const.JUPITER, const.SATURN]:
        orig = getObject_orig(planet, jd, lat, lon)
        cached = getObject_cached(planet, jd, lat, lon)
        if orig['lon'] != cached['lon'] or orig['sign'] != cached['sign']:
            print(f"Error: getObject({planet}, {jd}, {lat}, {lon}) - Original: {orig['lon']} {orig['sign']}, Cached: {cached['lon']} {cached['sign']}")
        else:
            print(f"getObject({planet}, {jd}, {lat}, {lon}) - OK")

    # Test getHouses
    orig_houses, orig_angles = getHouses_orig(jd, lat, lon, hsys)
    cached_houses, cached_angles = getHouses_cached(jd, lat, lon, hsys)

    # Check first house and Ascendant
    if orig_houses[0]['lon'] != cached_houses[0]['lon'] or orig_houses[0]['sign'] != cached_houses[0]['sign']:
        print(f"Error: getHouses({jd}, {lat}, {lon}, {hsys}) - Original House1: {orig_houses[0]['lon']} {orig_houses[0]['sign']}, Cached House1: {cached_houses[0]['lon']} {cached_houses[0]['sign']}")
    else:
        print(f"getHouses({jd}, {lat}, {lon}, {hsys}) House1 - OK")

    if orig_angles[0]['lon'] != cached_angles[0]['lon'] or orig_angles[0]['sign'] != cached_angles[0]['sign']:
        print(f"Error: getHouses({jd}, {lat}, {lon}, {hsys}) - Original ASC: {orig_angles[0]['lon']} {orig_angles[0]['sign']}, Cached ASC: {cached_angles[0]['lon']} {cached_angles[0]['sign']}")
    else:
        print(f"getHouses({jd}, {lat}, {lon}, {hsys}) ASC - OK")

def test_performance():
    """Test the performance improvement of cached functions."""
    print("\nTesting performance...")

    # Clear all caches
    clear_all_caches()

    # Number of iterations
    iterations = 100

    # Test sweObject
    jd = 2460000.5  # Example Julian day
    start_time = time.time()
    for _ in range(iterations):
        for planet in [const.SUN, const.MOON, const.JUPITER, const.SATURN]:
            sweObject_orig(planet, jd)
    orig_time = time.time() - start_time

    start_time = time.time()
    for _ in range(iterations):
        for planet in [const.SUN, const.MOON, const.JUPITER, const.SATURN]:
            sweObject_cached(planet, jd)
    cached_time = time.time() - start_time

    print(f"sweObject: Original: {orig_time:.6f}s, Cached: {cached_time:.6f}s, Speedup: {orig_time/cached_time:.2f}x")

    # Test sweHouses
    lat, lon = 12.9716, 77.5946  # Bangalore
    hsys = const.HOUSES_PLACIDUS
    start_time = time.time()
    for _ in range(iterations):
        sweHouses_orig(jd, lat, lon, hsys)
    orig_time = time.time() - start_time

    start_time = time.time()
    for _ in range(iterations):
        sweHouses_cached(jd, lat, lon, hsys)
    cached_time = time.time() - start_time

    print(f"sweHouses: Original: {orig_time:.6f}s, Cached: {cached_time:.6f}s, Speedup: {orig_time/cached_time:.2f}x")

    # Test getObject
    lat, lon = 12.9716, 77.5946  # Bangalore
    start_time = time.time()
    for _ in range(iterations):
        for planet in [const.SUN, const.MOON, const.JUPITER, const.SATURN]:
            getObject_orig(planet, jd, lat, lon)
    orig_time = time.time() - start_time

    start_time = time.time()
    for _ in range(iterations):
        for planet in [const.SUN, const.MOON, const.JUPITER, const.SATURN]:
            getObject_cached(planet, jd, lat, lon)
    cached_time = time.time() - start_time

    print(f"getObject: Original: {orig_time:.6f}s, Cached: {cached_time:.6f}s, Speedup: {orig_time/cached_time:.2f}x")

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
    CacheConfig.set_cache_size('ephemeris', 100)
    print(f"CacheConfig.maxsize['ephemeris'] = {CacheConfig.maxsize['ephemeris']}")

    # Test getting cache info
    cache_info = CacheConfig.get_cache_info()
    print(f"CacheConfig.get_cache_info()['ephemeris'] = {cache_info['ephemeris']}")

if __name__ == '__main__':
    test_correctness()
    test_performance()
    test_cache_config()
