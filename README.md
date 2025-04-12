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
- **Outer Planets**: Support for Uranus, Neptune, and Pluto in Vedic calculations
- **Core Calculations**: Focus on accurate astrological calculations with minimal interpretation

## Architecture

Flatlib is designed with a clear separation between core calculations and detailed analysis/reporting:

- **Core Library (flatlib)**: Focuses on accurate astrological calculations and core functionality
- **AstroVed Extension**: Contains detailed analysis, interpretations, and reporting functionality

This separation allows flatlib to remain focused and efficient while providing a path for more detailed analysis through the extension.

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

## Testing

Flatlib includes a comprehensive test suite to ensure accuracy and reliability of calculations.

### Running Tests

```bash
# Run all tests
./run_tests.py

# Run tests in a specific category
./run_tests.py --category vedic

# Generate HTML report
./run_tests.py --html

# Include tests that are known to fail
./run_tests.py --include-failing
```

Test reports are generated in the `reports` directory and include detailed information about each test.

### Adding Tests

See `docs/test_creation_guidelines.md` for detailed information on creating and maintaining tests.

## Development

This is a fork of the original flatlib library, modified to focus on Vedic astrology features.

### Commit Message Format

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification for commit messages:

```
feat(vedic): implement Vimshottari Dasha system

- Create core dasha calculations based on Moon's nakshatra
- Implement main periods (Mahadashas) with precise dates
- Add sub-period (Antardasha/Bhukti) calculations
- Include utility functions for finding current period
```

Common types include:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `refactor`: Code changes that neither fix bugs nor add features
- `test`: Adding or updating tests
- `chore`: Changes to build process or auxiliary tools