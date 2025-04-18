# Flatlib Vedic Astrology Module

This module extends flatlib to support Vedic astrology features.

## Features

### Nakshatras

The `nakshatras.py` module provides support for the 27 nakshatras (lunar mansions) used in Vedic astrology. It includes:

- Nakshatra calculations
- Pada (quarter) calculations
- Nakshatra lords based on the Vimshottari Dasha system
- Nakshatra elements and doshas

### KP Astrology

The `kp.py` module implements Krishnamurti Paddhati (KP) astrology features:

- Sublord calculations based on Vimshottari Dasha periods
- Sub-sublord calculations
- KP pointers in the format: Sign Lord-Star Lord-Sub Lord-Sub Sub Lord

### Panchang

The `panchang.py` module provides Vedic almanac calculations:

- Tithi (lunar day)
- Nakshatra (lunar mansion)
- Yoga (lunar-solar combination)
- Karana (half tithi)
- Vara (weekday)
- Rahukala (inauspicious period)
- Yamaganda (inauspicious period)
- Gulika Kala (inauspicious period)
- Abhijit Muhurta (auspicious period)

### Shadow Planets (Upagrah)

The `upagrah.py` module implements calculations for shadow planets:

- Gulika/Mandi (Son of Saturn)
- Dhuma (Smoky one)
- Vyatipata (Calamity)
- Parivesha (Halo)
- Indrachapa (Rainbow)
- Upaketu (Comet)

### Outer Planets

The library supports outer planets in Vedic calculations:

- Uranus
- Neptune
- Pluto

### Vimshottari Dasha

The `dashas.py` module implements Vimshottari Dasha calculations:

- Mahadasha (main period) calculations
- Antardasha (sub-period) calculations
- Pratyantardasha (sub-sub-period) calculations
- Dasha balance at birth
- Current operating period analysis
- Dasha Sandhi (junction points) detection

## Usage

```python
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib.vedic.nakshatras import get_nakshatra
from flatlib.vedic.panchang import get_panchang
from flatlib.vedic.kp import get_kp_lords
from flatlib.vedic.upagrah import get_upagrah

from flatlib.vedic.dashas import calculate_dasha_periods, get_current_dasha

# Create a chart with Lahiri ayanamsa and Whole Sign houses
date = Datetime('2025/04/09', '20:51', '+05:30')
pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
chart = Chart(date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)

# Get nakshatra information for the Moon
moon = chart.getObject(const.MOON)
nakshatra_info = get_nakshatra(moon.lon)
print(f"Moon is in {nakshatra_info['name']} nakshatra, pada {nakshatra_info['pada']}")

# Get panchang information
panchang = get_panchang(date.jd, pos.lat, pos.lon, chart.mode)
print(f"Tithi: {panchang['tithi']['name']} ({panchang['tithi']['paksha']})")
print(f"Yoga: {panchang['yoga']['name']}")
print(f"Karana: {panchang['karana']['name']}")

# Get KP information for the Sun
sun = chart.getObject(const.SUN)
kp_info = get_kp_lords(sun.lon)
print(f"Sun KP pointer: {kp_info['kp_pointer']}")

# Get shadow planet position
gulika = get_upagrah(const.GULIKA, date.jd, pos.lat, pos.lon)
print(f"Gulika is at {gulika['sign']} {gulika['signlon']:.2f}°")

# Get outer planet position
uranus = chart.getObject(const.URANUS)
print(f"Uranus is at {uranus.sign} {uranus.signlon:.2f}°")

# Calculate Vimshottari Dasha periods
moon = chart.getObject(const.MOON)
dasha_periods = calculate_dasha_periods(date, moon.lon)
current_dasha = get_current_dasha(dasha_periods)
print(f"Current Dasha: {current_dasha['mahadasha']}-{current_dasha['antardasha']}-{current_dasha['pratyantardasha']}")
```

## References

- Lahiri ayanamsa is the official ayanamsa of the Indian government
- Krishnamurti ayanamsa is used for KP astrology
- Placidus house system is recommended for KP astrology
- Whole Sign house system is commonly used in North Indian style charts
