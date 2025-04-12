# Flatlib Vedic Astrology Review Summary & Task List

This document summarizes the findings from a review of the `flatlib` codebase for its suitability and accuracy regarding Vedic Astrology principles. Tasks required to address the identified issues are listed below each finding. For each task below, we have to maintain backwards compatibility with existing features and tests, and ensure that our changes are well-documented and tested.

---

## 1. House System Defaults and Availability

*   **Finding:** The library defaults to the Placidus house system (`flatlib.chart.Chart`, `flatlib.const.py`), which is not standard for most Vedic traditions. Whole Sign houses are available but not the default. When using Lahiri ayanamsa, Whole Sign is the standard, and when using Krishnamurti, Placidus is the standard.
*   **Category:** `Astrology`, `API`
*   **Tasks:**
    *   [x] Change the default house system in `flatlib.const.py` to `HOUSE_SYS_WHOLE_SIGN` or provide a clear mechanism/configuration for users to set a Vedic default.
    *   [x] Update relevant examples and documentation to reflect Whole Sign as the recommended system for Vedic charts.
    *   [x] Ensure `flatlib.chart.Chart` correctly uses the default or user-specified house system.

## 2. Vedic Aspect Implementation

*   **Finding:** The library only implements Western/Hellenistic degree-based aspects (`flatlib.aspects.py`). It completely lacks definitions and calculation logic for Vedic aspects (Graha Drishti and Rashi Drishti). This significantly impacts chart interpretation and calculations like Drig Bala. Western aspects are good for finding conjuctions, oppositions, and trines, but not for the specific Vedic aspects that are crucial for Graha Drishti and Drig Bala. So we need support for both types of aspects depending on context while maintaining compatibility with existing Western-based functions.
*   **Category:** `Astrology`
*   **Tasks:**
    *   [x] Define constants for Vedic aspects (planet-to-planet Graha Drishti rules, sign-to-sign Rashi Drishti rules) potentially in `flatlib.const.py`.
    *   [x] Implement functions in `flatlib.aspects.py` (or a new `flatlib.vedic.aspects.py`) to calculate Graha Drishti between planets based on Vedic rules.
    *   [x] Implement functions to calculate Rashi Drishti between signs.
    *   [x] Integrate Vedic aspect calculations into relevant analysis functions (e.g., chart interpretation utilities).
    *   [x] (**Dependency for Shadbala**) Ensure Drig Bala calculation uses the newly implemented Vedic aspects.

## 3. Planetary Dignities (Rulership, Exaltation, Moolatrikona)

*   **Finding:** Dignity definitions (`flatlib.dignities.tables.py`) are primarily Western/Hellenistic. Moolatrikona signs and specific degrees are missing. Some exaltation degrees may differ slightly from standard Vedic points (though Uchcha Bala calculation seemed to use correct points internally). Modern rulerships might be mixed in.
*   **Category:** `Astrology`
*   **Tasks:**
    *   [x] Create a reliable, centralized source for Vedic dignities (Moolatrikona sign/degrees, Rulership, Exaltation sign/degree, Debilitation sign/degree). This could be a new data structure or enhancements to `const.py` or a dedicated `vedic/tables.py`.
    *   [x] Define Moolatrikona ranges accurately for all planets.
    *   [x] Verify and correct exaltation/debilitation degrees to match Vedic standards consistently.
    *   [x] Ensure only traditional Vedic rulerships are used for Vedic calculations.
    *   [x] Update all functions relying on dignities (especially Shadbala/Saptavarga) to use this corrected Vedic dignity source.

## 4. Planetary Friendships (Natural and Temporal)

*   **Finding:** The dignity assessment used in Saptavarga Bala (`flatlib.vedic.vargas.analysis.calculate_sign_strength`) uses a simplified Friend/Enemy model. It lacks the necessary calculation of combined Natural and Temporal friendships required for the 5-level relationship status (Great Friend, Friend, Neutral, Enemy, Great Enemy).
*   **Category:** `Astrology`
*   **Tasks:**
    *   [x] Define Natural Friendship rules between planets in a suitable constant/data structure.
    *   [x] Implement logic to calculate Temporal Friendship based on planetary placements in a given chart.
    *   [x] Implement logic to combine Natural and Temporal friendships to determine the 5-level relationship status between two planets in a chart.
    *   [x] Update Saptavarga Bala (and any other relevant calculations) to use this 5-level relationship status for assigning points.

## 5. Shadbala Calculation Accuracy

*   **Finding:** The Shadbala module (`flatlib.vedic.shadbala`) is structurally well-organized, but the Saptavarga Bala component is critically flawed.
    *   **Saptavarga Bala Method:** Uses a non-standard weighting/scaling approach instead of summing Virupa points based on dignity.
    *   **Saptavarga Dignity Assessment:** Relies on `calculate_sign_strength`, which ignores Moolatrikona and uses simplified friendships (See Findings 3 & 4).
    *   **Drig Bala:** Likely uses incorrect Western aspects due to Finding 2. Needs verification.
*   **Category:** `Astrology`, `Math`
*   **Tasks:**
    *   [x] Rewrite `flatlib.vedic.shadbala.sthana_bala.calculate_saptavarga_bala` to:
        *   Correctly determine the 5-level relationship status (using results from Task List 4) and Moolatrikona status (using results from Task List 3) for the planet in each of the 7 Vargas (D1, D2, D3, D7, D9, D12, D30).
        *   Assign the standard Virupa points for each dignity level achieved (Moolatrikona, Own House, Great Friend, Friend, Neutral, Enemy, Great Enemy, Debilitation, etc.) in each Varga.
        *   Sum the Virupa points from all 7 Vargas to get the final Saptavarga Bala score.
    *   [x] Review and correct `flatlib.vedic.shadbala.drig_bala.calculate_drig_bala` to use Vedic aspects (Graha Drishti) and assign points according to standard rules.
    *   [x] Briefly review other Shadbala components (`dig_bala`, `kala_bala`, `cheshta_bala`, `naisargika_bala`) for adherence to standard Vedic formulas.

## 6. Transit Calculations

*   **Finding:** The `sweNextTransit` function in `flatlib.ephem.swe.py` does not appear to explicitly set the sidereal flag (`FLG_SIDEREAL`) when calling `swisseph.rise_trans`, potentially leading to inaccurate transit times if the global ephemeris setting is not already sidereal.
*   **Category:** `Astrology`, `Math`
*   **Tasks:**
    *   [x] Modify `sweNextTransit` to explicitly include `swisseph.FLG_SIDEREAL` in the `ephe_flag` argument passed to `swisseph.rise_trans` when performing calculations for a sidereal chart context.
    *   [x] Add tests to verify sidereal transit calculation accuracy against known examples.

## 7. Varga Implementation

*   **Finding:** The calculation of Varga chart *positions* seems structurally sound and comprehensive (`flatlib.vedic.vargas`). The issue lies in the *interpretation* of these positions for dignity/strength (addressed in Shadbala/Saptavarga findings).
*   **Category:** `Core`, `Math`
*   **Tasks:**
    *   [ ] No immediate tasks required for the core Varga position calculation, but ensure underlying planetary position calculations are accurate (relies on Swiss Ephemeris, seems okay).
    *   [ ] Verify the specific calculation logic within each individual Varga module (e.g., `navamsha.py`, `hora.py`) against standard definitions if deeper accuracy checks are needed.

## 8. Vedic Object Representation

*   **Finding:** While `flatlib.object.VedicBody` exists, the base `Object` class and overall representation are geared towards Western astrology. Specific Vedic attributes or calculation results (like detailed Shadbala components, nuanced dignities) may not be easily accessible properties of the objects.
*   **Category:** `Astrology`, `API`
*   **Tasks:**
    *   [ ] Evaluate if enhancing `VedicBody` or related classes to store and provide easy access to calculated Vedic-specific data (Shadbala breakdowns, detailed dignities, aspect info) would improve the API usability.
    *   [ ] Consider adding methods to `VedicBody` for common Vedic queries.

---
