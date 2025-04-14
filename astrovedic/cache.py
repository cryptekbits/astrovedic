"""
    This file is part of astrovedic - (C) FlatAngle

    This module implements caching functionality for astrovedic.
    It provides decorators and utilities for caching different
    types of calculations to improve performance.
"""

import functools
from typing import Dict, Any, Callable, Optional, TypeVar, cast, List

# Type variables for better type hints
F = TypeVar('F', bound=Callable[..., Any])

# Cache categories
CACHE_REFERENCE = 'reference_data'  # Unchanging reference data
CACHE_CALCULATION = 'calculations'  # Expensive calculations
CACHE_EPHEMERIS = 'ephemeris'       # Ephemeris lookups

# Registry of cached functions
_CACHED_FUNCTIONS: Dict[str, List[Any]] = {
    CACHE_REFERENCE: [],
    CACHE_CALCULATION: [],
    CACHE_EPHEMERIS: []
}

class CacheConfig:
    """Configuration for flatlib caching behavior."""

    # Default values
    enabled = True
    maxsize = {
        CACHE_REFERENCE: 512,   # Medium-large cache for reference data (rarely changes)
        CACHE_CALCULATION: 256,  # Medium cache for calculations (moderate reuse)
        CACHE_EPHEMERIS: 128     # Small-medium cache for ephemeris lookups (high value per cache hit)
    }

    @classmethod
    def disable_all(cls) -> None:
        """Disable all caching."""
        cls.enabled = False
        clear_all_caches()

    @classmethod
    def enable_all(cls) -> None:
        """Enable all caching."""
        cls.enabled = True

    @classmethod
    def set_cache_size(cls, category: str, size: int) -> None:
        """Set cache size for a specific category."""
        if category in cls.maxsize:
            cls.maxsize[category] = size
            # Clear existing cache for this category
            clear_category_cache(category)

    @classmethod
    def get_cache_info(cls) -> Dict[str, Any]:
        """Get information about all caches."""
        info = {}
        for category, funcs in _CACHED_FUNCTIONS.items():
            category_info = []
            for func in funcs:
                if hasattr(func, 'cache_info'):
                    cache_info = func.cache_info()
                    category_info.append({
                        'function': func.__name__,
                        'hits': cache_info.hits,
                        'misses': cache_info.misses,
                        'maxsize': cache_info.maxsize,
                        'currsize': cache_info.currsize
                    })
            info[category] = category_info
        return info

def clear_category_cache(category: str) -> None:
    """Clear cache for all functions in a category."""
    if category in _CACHED_FUNCTIONS:
        for func in _CACHED_FUNCTIONS[category]:
            if hasattr(func, 'cache_clear'):
                func.cache_clear()

def clear_all_caches() -> None:
    """Clear all caches."""
    for category in _CACHED_FUNCTIONS:
        clear_category_cache(category)

def reference_cache(maxsize: Optional[int] = None) -> Callable[[F], F]:
    """
    Decorator for caching reference data.

    This is for data that doesn't change, like nakshatra lords,
    sign lords, etc.

    Args:
        maxsize: Maximum size of the cache. If None, uses the default
                 size from CacheConfig.

    Returns:
        A decorator function.
    """
    def decorator(func: F) -> F:
        if not CacheConfig.enabled:
            return func

        size = maxsize if maxsize is not None else CacheConfig.maxsize[CACHE_REFERENCE]
        cached_func = functools.lru_cache(maxsize=size)(func)
        _CACHED_FUNCTIONS[CACHE_REFERENCE].append(cached_func)

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return cached_func(*args, **kwargs)

        wrapper.cache_info = cached_func.cache_info  # type: ignore
        wrapper.cache_clear = cached_func.cache_clear  # type: ignore

        return cast(F, wrapper)
    return decorator

def calculation_cache(maxsize: Optional[int] = None) -> Callable[[F], F]:
    """
    Decorator for caching expensive calculations.

    This is for pure functions that perform mathematical transformations,
    like divisional chart calculations.

    Args:
        maxsize: Maximum size of the cache. If None, uses the default
                 size from CacheConfig.

    Returns:
        A decorator function.
    """
    def decorator(func: F) -> F:
        if not CacheConfig.enabled:
            return func

        size = maxsize if maxsize is not None else CacheConfig.maxsize[CACHE_CALCULATION]
        cached_func = functools.lru_cache(maxsize=size)(func)
        _CACHED_FUNCTIONS[CACHE_CALCULATION].append(cached_func)

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return cached_func(*args, **kwargs)

        wrapper.cache_info = cached_func.cache_info  # type: ignore
        wrapper.cache_clear = cached_func.cache_clear  # type: ignore

        return cast(F, wrapper)
    return decorator

def ephemeris_cache(maxsize: Optional[int] = None) -> Callable[[F], F]:
    """
    Decorator for caching ephemeris lookups.

    This is for functions that look up planetary positions,
    house cusps, etc.

    Args:
        maxsize: Maximum size of the cache. If None, uses the default
                 size from CacheConfig.

    Returns:
        A decorator function.
    """
    def decorator(func: F) -> F:
        if not CacheConfig.enabled:
            return func

        size = maxsize if maxsize is not None else CacheConfig.maxsize[CACHE_EPHEMERIS]
        cached_func = functools.lru_cache(maxsize=size)(func)
        _CACHED_FUNCTIONS[CACHE_EPHEMERIS].append(cached_func)

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return cached_func(*args, **kwargs)

        wrapper.cache_info = cached_func.cache_info  # type: ignore
        wrapper.cache_clear = cached_func.cache_clear  # type: ignore

        return cast(F, wrapper)
    return decorator
