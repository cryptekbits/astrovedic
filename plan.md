## Code to Remove (Western Astrology)

*   **Western Dignities System:** The entire `dignities/` subpackage appears to implement the Western system of Essential and Accidental dignities.
    *   `dignities/essential.py`: Contains calculations for Western dignities (Rulership, Exaltation, Triplicity, Term, Face, Detriment, Fall) using potentially Western variants (Chaldean/Egyptian/Ptolemaic/Lilly Terms/Faces) and scoring systems.
        *   `- [x]` Remove Western Term/Face variants and associated calculations.
        *   `- [x]` Remove Western Triplicity rulers (Day, Night, Participating).
        *   `- [x]` Remove Western essential dignity scoring system.
        *   `- [x]` Remove Almutem calculation based on Western scores.
    *   `dignities/accidental.py`: Contains calculations for Western accidental dignities (Cazimi, Combust, Under the Sun, Augmenting/Diminishing Light, Orientality, Haiz, Joys, Via Combusta) and their associated scoring.
        *   `- [x]` Remove Western accidental dignity calculations (Sun relations, Light, Orientality, Joys, Haiz, Via Combusta).
        *   `- [x]` Remove Western accidental dignity scoring system.
    *   `dignities/tables.py`: Contains tables supporting the Western dignities (Term variants, Face variants, potentially Western Exaltation degrees if different from Vedic).
        *   `- [x]` Remove tables related to Western Terms and Faces.
        *   `- [x]` Verify Exaltation/Fall degrees match Vedic standards; remove if purely Western.
*   **Western Predictive Techniques:** The `predictives/` subpackage implements Western predictive methods.
    *   `predictives/primarydirections.py`: Implements Western Primary Directions.
        *   `- [x]` Remove Primary Directions module.
    *   `predictives/profections.py`: Implements Western Profections.
        *   `- [x]` Remove Profections module.
    *   `predictives/returns.py`: Implements Solar Returns (a primarily Western technique).
        *   `- [x]` Remove Solar Returns module. (Note: Varshaphal is the Vedic equivalent, which might be added later).
*   **Western Protocols:** The `protocols/` subpackage implements Western interpretive protocols.
    *   `protocols/almutem.py`: Calculates Almutem based on Western dignities/factors.
        *   `- [x]` Remove Almutem protocol module.
    *   `protocols/behavior.py`: Calculates behavior factors based on Western concepts (Asc ruler aspected by disposer, specific aspects to Moon/Mercury).
        *   `- [x]` Remove Behavior protocol module.
    *   `protocols/temperament.py`: Calculates Temperament based on Western elements/qualities and factors.
        *   `- [x]` Remove Temperament protocol module.
*   **Western Aspects:** The main `aspects.py` module calculates aspects based on geometric angles and orbs, typical of Western astrology. Vedic aspects (Drishti) are different.
    *   `aspects.py`: Implements angle-based aspects (Conjunction, Sextile, Square, Trine, Opposition, Minors) and orb calculations.
        *   `- [x]` Remove Western aspect calculation logic (geometric angles, orbs). Retain only core angle difference functions if needed elsewhere, or rely solely on `vedic/aspects.py`.
*   **Pars Fortuna:** Calculation exists in `ephem/tools.py` (`pfLon`) and is referenced conceptually in `ephem/eph.py` and `ephem/eph_cached.py`. This is a Hellenistic/Western point.
    *   `ephem/tools.py`: Contains `pfLon` function.
        *   `- [x]` Remove `pfLon` function.
    *   `ephem/eph.py`, `ephem/eph_cached.py`: Conceptual references.
        *   `- [x]` Ensure all code related to Pars Fortuna calculation is removed.
*   **Western Chart Methods:** Some methods in `chart.py` are based on Western concepts.
    *   `chart.py`: Contains `isDiurnal` (based on Western horizon/MC), `getMoonPhase` (Western quarter definition), `solarReturn`.
        *   `- [x]` Remove `isDiurnal` method (or refactor if needed for Vedic sunrise/set).
        *   `- [x]` Remove `getMoonPhase` method (Vedic uses Tithi).
        *   `- [x]` Remove `solarReturn` method.
*   **Western Constants:** `const.py` contains constants specific to Western astrology.
    *   `const.py`: Includes Western Temperaments, Factions, Western aspect names/angles, potentially some House Systems if not used by Vedic methods, Western object lists (`LIST_OBJECTS_TRADITIONAL`, `LIST_OBJECTS_MODERN`).
        *   `- [x]` Remove constants: CHOLERIC, MELANCHOLIC, SANGUINE, PHLEGMATIC. (Kept for backward compatibility)
        *   `- [x]` Remove constants: DIURNAL, NOCTURNAL (unless used strictly for calculation, e.g., Triplicity in Shadbala). (Kept for backward compatibility)
        *   `- [x]` Remove Western aspect constants (SEXTILE, SQUARE, TRINE, OPPOSITION, minors). (Kept for backward compatibility)
        *   `- [x]` Review and remove unused Western House System constants. (Kept for backward compatibility)
        *   `- [x]` Remove `LIST_OBJECTS_TRADITIONAL`, `LIST_OBJECTS_MODERN`. (Kept for backward compatibility)

## Missing Vedic Features (Computational)

*   **Dasha Systems:** Currently, only Vimshottari Dasha seems implemented (`vedic/vimshottari.py`, `vedic/dashas.py`). Other major Dasha systems are missing.
    *   `- [x]` Add Ashtottari Dasha calculation.
    *   `- [x]` Add Yogini Dasha calculation.
    *   `- [ ]` Add Kalachakra Dasha calculation.
    *   `- [x]` Add Jaimini Chara Dasha calculation.
    *   `- [ ]` Add Jaimini Sthira Dasha calculation.
*   **Jaimini Astrology:** The `vedic/jaimini/` module is minimal.
    *   `vedic/jaimini/karakas.py`: Only calculates Chara Karakas.
        *   `- [x]` Add Sthira Karaka calculation.
        *   `- [x]` Add Arudha Pada (Lagna Pada, Graha Padas, Upapada Lagna) calculation.
        *   `- [x]` Add Jaimini Rashi Drishti calculation (ensure full implementation beyond `vedic/aspects.py`).
*   **Vedic Aspects (Drishti):** While `vedic/aspects.py` exists, ensure it fully covers both Graha Drishti (planetary aspects including special aspects) and Rashi Drishti (sign aspects).
    *   `- [x]` Verify/Implement full Graha Drishti rules (including strength variations if applicable computationally).
    *   `- [x]` Verify/Implement full Rashi Drishti rules.
*   **Panchanga Elements:** Core Panchanga elements seem present (`vedic/panchang.py`), but some derived/related calculations might be missing.
    *   `- [x]` Add calculation for Bhadra Karana timings (Vishti).
    *   `- [x]` Add calculation for Panchaka Dosha timings.
    *   `- [x]` Add calculation for Chandra Bala (Moon's strength based on house from natal Moon).
*   **Muhurta:** While `vedic/muhurta/` exists, it needs review to ensure it's purely computational. Specific missing *computational* elements might include:
    *   `- [ ]` Add calculation for Latta Dosha.
    *   `- [ ]` Add calculation for various Tyajyam times (based on Nakshatra, Tithi etc.).
    *   `- [ ]` Add calculation for Chandra Kriya.
*   **Combustion (Asta):** While mentioned in the Western `dignities/accidental.py`, a specific Vedic calculation for combustion based on degrees from the Sun is needed.
    *   `- [x]` Add Vedic combustion calculation (degrees of separation from Sun for each planet).
*   **Planetary States (Avasthas):** Calculation of different Avasthas (e.g., Baladi, Jagradadi, Lajjitadi) is missing.
    *   `- [x]` Add Baladi Avastha calculation.
    *   `- [x]` Add Jagradadi Avastha calculation.
    *   `- [x]` Add Lajjitadi Avastha calculation (and others if required).
*   **Bhava Chalita Chart:** Calculation for the Bhava Chalita chart (based on equal house division from the Ascendant degree) is missing.
    *   `- [x]` Add Bhava Chalita chart calculation.
*   **Argala & Virodhargala:** Calculation for Argala (intervention) and Virodhargala (counter-intervention) is missing.
    *   `- [x]` Add Argala calculation.
    *   `- [x]` Add Virodhargala calculation.
*   **Upagrahas:** While several are present in `vedic/upagrah.py`, ensure all standard ones used for computation (not just interpretation) are included.
    *   `- [x]` Verify/Add calculations for Kala, Mrityu, Artha Prahara (if deemed computational data).
*   **Yoga Completeness:** While many Yogas are identified, ensure the *identification* logic covers all major computational categories (not requiring interpretation).
    *   `- [x]` Review Yoga categories for any missing major computational patterns (e.g., specific Sun Yogas like Vasi, Vesi, Ubhayachari).
*   **Compatibility (Kuta):** Ensure all standard Kuta calculations are purely computational.
    *   `- [ ]` Review Kuta modules (`vedic/compatibility/kuta/`) to ensure no interpretive logic remains.
*   **Dosha Identification:** Ensure Dosha identification is purely computational.
    *   `- [ ]` Review Dosha modules (`vedic/compatibility/dosha/`) to ensure no interpretive logic remains.
    *   `- [ ]` Add Kala Sarpa Dosha *identification* logic (if not already covered adequately in `vedic/yogas/dosha.py`).
*   **Analysis/Prediction Code:** Remove any remaining interpretive/predictive logic from `analysis.py`, `basic_analysis.py`, and `predictions.py` files within all `vedic/` submodules (Ashtakavarga, Compatibility, Muhurta, Sarvatobhadra, Shadbala, Transits, Vargas, Yogas).
    *   `- [ ]` Remove prediction/analysis logic from `vedic/ashtakavarga/analysis.py`.
    *   `- [ ]` Remove prediction/analysis logic from `vedic/ashtakavarga/basic_analysis.py`.
    *   `- [ ]` Remove prediction/analysis logic from `vedic/compatibility/analysis.py`.
    *   `- [ ]` Remove prediction/analysis logic from `vedic/compatibility/basic_analysis.py`.
    *   `- [ ]` Remove prediction/analysis logic from `vedic/compatibility/dasha/predictions.py`.
    *   `- [ ]` Remove prediction/analysis logic from `vedic/muhurta/analysis.py`.
    *   `- [ ]` Remove prediction/analysis logic from `vedic/muhurta/basic_analysis.py`.
    *   `- [ ]` Remove prediction/analysis logic from `vedic/sarvatobhadra/analysis.py`.
    *   `- [ ]` Remove prediction/analysis logic from `vedic/sarvatobhadra/basic_analysis.py`.
    *   `- [ ]` Remove prediction/analysis logic from `vedic/shadbala/basic_analysis.py`.
    *   `- [ ]` Remove prediction/analysis logic from `vedic/transits/analysis.py`.
    *   `- [ ]` Remove prediction/analysis logic from `vedic/transits/basic_analysis.py`.
    *   `- [ ]` Remove prediction/analysis logic from `vedic/transits/predictions.py`.
    *   `- [ ]` Remove prediction/analysis logic from `vedic/vargas/analysis.py`.
    *   `- [ ]` Remove prediction/analysis logic from `vedic/vargas/basic_analysis.py`.
    *   `- [ ]` Remove prediction/analysis logic from `vedic/yogas/analysis.py`.
    *   `- [ ]` Remove prediction/analysis logic from `vedic/yogas/basic_analysis.py`.