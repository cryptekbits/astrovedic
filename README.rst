astrovedic
=========

A Python 3 library for Vedic and Traditional Astrology.

This project was originally forked from flatlib and has been significantly enhanced with Vedic astrology features. It has been renamed to astrovedic to reflect its focus on Vedic astrology while maintaining compatibility with Western/Traditional astrology features.


Installation
------------

You can install astrovedic using pip::

    pip install astrovedic

Or directly from the repository::

    pip install git+https://github.com/cryptekbits/astrovedic.git


Examples
--------

Western Astrology Example::

    >>> from astrovedic.datetime import Datetime
    >>> from astrovedic.geopos import GeoPos
    >>> from astrovedic.chart import Chart
    >>> from astrovedic import const

    >>> date = Datetime('2015/03/10', '14:00', '+00:00')
    >>> pos = GeoPos('38n32', '8w54')
    >>> chart = Chart(date, pos)

    >>> sun = chart.get(const.SUN)
    >>> print(sun)
    <Sun Pisces +19:40:13 +00:59:57>

Vedic Astrology Example::

    >>> from astrovedic.datetime import Datetime
    >>> from astrovedic.geopos import GeoPos
    >>> from astrovedic.chart import Chart
    >>> from astrovedic import const
    >>> from astrovedic.vedic.nakshatras import get_nakshatra

    >>> date = Datetime('2015/03/10', '14:00', '+00:00')
    >>> pos = GeoPos('38n32', '8w54')
    >>> chart = Chart(date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)

    >>> moon = chart.get(const.MOON)
    >>> nakshatra_info = get_nakshatra(moon.lon)
    >>> print(f"Moon in {nakshatra_info['name']} Nakshatra, Pada {nakshatra_info['pada']}")
    Moon in Uttara Phalguni Nakshatra, Pada 2


Features
--------

* **Western Astrology**
    - Chart calculations with Swiss Ephemeris
    - Essential and accidental dignities
    - Aspects and orbs
    - Predictive techniques (profections, solar returns, primary directions)
    - Protocols (almutem, temperament, behavior)
    - Fixed stars and Arabic parts

* **Vedic Astrology**
    - Multiple ayanamsa options (Lahiri, Raman, KP, etc.)
    - Nakshatra calculations
    - Divisional charts (Vargas) - D1 to D60
    - Vimshottari Dasha calculations
    - Shadbala (planetary strength)
    - Ashtakavarga system
    - Yogas (planetary combinations)
    - Compatibility analysis (Kuta matching)
    - Muhurta (electional astrology)
    - Transit analysis (Gochara)
    - KP (Krishnamurti Paddhati) astrology

* **Performance Optimizations**
    - Caching system for ephemeris calculations
    - Optimized algorithms for divisional charts
    - Efficient memory usage


Changelog
---------

* 0.3.0 (released 2025-04-14)
    - Renamed project from flatlib to astrovedic
    - Extensive additions for Vedic astrology
    - Improved caching system
    - Enhanced API for Vedic calculations

* 0.2.1 (released 06-05-2016)
    - Added Pars Horsemanship
    - Return accidental dignities that score more than zero
    - Added chartdynamics.disposits to return dignities where planet A disposes a planet B
    - Includes new Triplicity Faces

* 0.2.0 (released 08-04-2015)
    - Many new features:
        - Planetary time
        - Arabic Parts
        - Chart Dynamics
        - Accidental dignities
        - Predictives (Profections, Solar Returns and Primary Directions)
        - Protocols (Almutem, Temperament and Behavior calculations)
    - Bug fixes

* 0.1.1 (released 18-03-2015)
    - Changed threshold for stationary (1 arc-second)
    - Implementation of essential dignities
    - Added essential dignities recipe

* 0.1.0 (released 14-03-2015)
    - Initial release
    - Implementation of core modules
