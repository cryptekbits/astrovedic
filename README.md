# flatlib - Vedic Astrology

Flatlib is a Python library for Vedic Astrology, extended from the original flatlib library. This version includes support for Vedic features such as nakshatras, panchang, KP astrology, shadow planets, and more.

```python
# Example of Vedic chart with Lahiri ayanamsa
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib.vedic.nakshatras import get_nakshatra

# Create a chart for Bangalore, India
date = Datetime('2025/04/09', '20:51', '+05:30')
pos = GeoPos(12.9716, 77.5946)  # Bangalore
chart = Chart(date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)

# Get Moon position and nakshatra
moon = chart.getObject(const.MOON)
nakshatra_info = get_nakshatra(moon.lon)

print(f"Moon: {moon.sign} {moon.signlon:.2f}°")
print(f"Nakshatra: {nakshatra_info['name']} (Pada {nakshatra_info['pada']})")
```

## Features

- **Vedic Ayanamsas**: Support for multiple Vedic ayanamsas including Lahiri, Krishnamurti, and more
- **Nakshatras**: Calculations for the 27 nakshatras (lunar mansions) and their padas (quarters)
- **Panchang**: Vedic almanac elements including tithi, yoga, karana, and more
- **KP Astrology**: Krishnamurti Paddhati features including sublord calculations
- **Shadow Planets**: Support for upagrah (shadow planets) like Gulika, Mandi, etc.
- **Additional Vedic Bodies**: Support for bodies like Arun, Varun, Yama

## Installation

Flatlib is a Python 3 package. Make sure you have Python 3 installed on your system.

```bash
# Clone the repository
git clone https://github.com/your-username/flatlib-vedic.git
cd flatlib-vedic

# Install the package
pip3 install -e .
```

## Documentation

See the `flatlib/vedic/README.md` file for detailed documentation on the Vedic features.

## Examples

Check the `examples/` directory for example scripts:

- `examples/vedic_chart.py`: Basic Vedic chart calculations
- `examples/dainik_panchang.py`: Daily panchang calculations
- `examples/test_reference_date.py`: Test script for the reference date

## Development

This is a fork of the original flatlib library, modified to focus on Vedic astrology features.