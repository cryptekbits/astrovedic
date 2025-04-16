# Ayanamsas in Astrovedic

This document provides information about the different ayanamsas (sidereal zodiac systems) available in the Astrovedic library.

## What is an Ayanamsa?

An ayanamsa is the angular difference between the tropical zodiac (based on the vernal equinox) and the sidereal zodiac (based on fixed stars). This difference is caused by the precession of the equinoxes.

In Vedic astrology, the sidereal zodiac is used, which requires an ayanamsa to convert from the tropical positions calculated by modern ephemerides.

## Available Ayanamsas in Astrovedic

Astrovedic supports the following Vedic ayanamsas:

### Primary Vedic Ayanamsas

- **Lahiri** (`const.AY_LAHIRI`): Official ayanamsa of the Indian government.
- **Raman** (`const.AY_RAMAN`): B.V. Raman's ayanamsa, a variant of Lahiri.
- **Krishnamurti** (`const.AY_KRISHNAMURTI`): K.S. Krishnamurti's ayanamsa used in KP system.

### Additional Vedic Ayanamsas

- **Yukteshwar** (`const.AY_YUKTESHWAR`): Yukteshwar's ayanamsa based on his book "The Holy Science".
- **JN Bhasin** (`const.AY_JN_BHASIN`): J.N. Bhasin's ayanamsa.
- **Surya Siddhanta** (`const.AY_SURYASIDDHANTA`): Based on the ancient Surya Siddhanta text.
- **Surya Siddhanta (Mean Sun)** (`const.AY_SURYASIDDHANTA_MSUN`): Variant using mean solar position.
- **Aryabhata** (`const.AY_ARYABHATA`): Based on Aryabhata's work.
- **Aryabhata (Mean Sun)** (`const.AY_ARYABHATA_MSUN`): Variant using mean solar position.
- **SS Revati** (`const.AY_SS_REVATI`): Surya Siddhanta with Revati (Zeta Piscium) at 0° Aries.
- **SS Citra** (`const.AY_SS_CITRA`): Surya Siddhanta with Citra (Spica) at 0° Libra.
- **True Citra** (`const.AY_TRUE_CITRA`): True Citra ayanamsa with Spica at 0° Libra.
- **True Revati** (`const.AY_TRUE_REVATI`): True Revati ayanamsa with Revati at 0° Aries.
- **True Pushya** (`const.AY_TRUE_PUSHYA`): True Pushya ayanamsa.
- **True Mula** (`const.AY_TRUE_MULA`): True Mula ayanamsa.
- **Aryabhata 522** (`const.AY_ARYABHATA_522`): Aryabhata's ayanamsa for the year 522 CE.
- **True Sheoran** (`const.AY_TRUE_SHEORAN`): True Sheoran ayanamsa.

## Using Ayanamsas in Astrovedic

To create a chart with a specific ayanamsa:

```python
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.chart import Chart
from astrovedic import const

# Create a date and location
date = Datetime('2023/05/15', '12:00', '+00:00')
pos = GeoPos('38n32', '8w54')

# Create a chart with the Lahiri ayanamsa
chart = Chart(date, pos, mode=const.AY_LAHIRI)

# Get the Sun's position in the sidereal zodiac
sun = chart.getObject(const.SUN)
print(f"Sun in sidereal zodiac: {sun.sign} {sun.signlon:.2f}°")
```

## Default Ayanamsas

Astrovedic defines default ayanamsas for different systems:

- **Default for Vedic calculations**: Lahiri (`const.AY_DEFAULT_VEDIC = const.AY_LAHIRI`)
- **Default for KP calculations**: Krishnamurti (`const.AY_DEFAULT_KP = const.AY_KRISHNAMURTI`)

## Choosing an Ayanamsa

Different Vedic astrological traditions use different ayanamsas:

- Indian government calculations use Lahiri
- KP (Krishnamurti Paddhati) astrology uses Krishnamurti
- Traditional Jyotish practitioners may use True Citra or True Pushya
- Some Vedic astrologers prefer Yukteshwar's ayanamsa
- B.V. Raman's followers use the Raman ayanamsa

The choice of ayanamsa can shift planetary positions by several degrees, so it's important to be consistent in your practice.
