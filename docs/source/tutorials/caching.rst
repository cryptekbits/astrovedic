Caching in Flatlib
=================

Flatlib uses caching to improve performance for frequently used calculations. This document explains how caching works and how you can control it.

Cache Categories
---------------

Flatlib uses three categories of caches:

1. **Reference Data**: Unchanging data like nakshatra lords, sign lords, etc.
2. **Calculations**: Mathematical transformations like divisional chart calculations
3. **Ephemeris**: Planetary position lookups

Controlling Cache Behavior
-------------------------

You can control caching behavior using the ``CacheConfig`` class::

    from flatlib.cache import CacheConfig

    # Disable all caching
    CacheConfig.disable_all()

    # Enable all caching
    CacheConfig.enable_all()

    # Set cache size for a specific category
    CacheConfig.set_cache_size('calculations', 256)

    # Get cache statistics
    cache_info = CacheConfig.get_cache_info()
    print(cache_info)

    # Clear all caches
    from flatlib.cache import clear_all_caches
    clear_all_caches()

    # Clear a specific category
    from flatlib.cache import clear_category_cache
    clear_category_cache('ephemeris')

Memory Usage
-----------

Caching improves performance but increases memory usage. The default cache sizes are:

- Reference Data: 1024 entries
- Calculations: 128 entries
- Ephemeris: 64 entries

If you're working with limited memory, you can reduce these sizes or disable caching entirely.

Cached Functions
--------------

The following functions in flatlib are cached:

Reference Data Functions:
    - ``get_nakshatra_lord``
    - ``get_sign_lord``
    - ``get_planet_friendship``
    - ``get_element``
    - ``get_quality``
    - ``get_gender``
    - ``get_planet_nature``
    - ``get_planet_element``
    - ``get_planet_abbreviation``

Calculation Functions:
    - Divisional chart calculations (``calculate_d1``, ``calculate_d2``, etc.)
    - ``get_ashtakavarga_points``
    - ``get_sarvashtakavarga``
    - ``get_nakshatra``
    - ``get_nakshatra_pada``
    - ``normalize_longitude``
    - ``get_sign_from_longitude``
    - ``get_sign_number``

Ephemeris Functions:
    - ``get_planet_position``
    - ``get_house_cusps``
    - ``get_fixed_star_position``

Thread Safety
------------

The caching system in flatlib is thread-safe, so you can use it in multi-threaded applications without issues.
