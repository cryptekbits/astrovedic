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
    *   [x] No immediate tasks required for the core Varga position calculation, but ensure underlying planetary position calculations are accurate (relies on Swiss Ephemeris, seems okay).
    *   [x] Verify the specific calculation logic within each individual Varga module (e.g., `navamsha.py`, `hora.py`) against standard definitions if deeper accuracy checks are needed.

## 8. Vedic Object Representation

*   **Finding:** While `flatlib.object.VedicBody` exists, the base `Object` class and overall representation are geared towards Western astrology. Specific Vedic attributes or calculation results (like detailed Shadbala components, nuanced dignities) may not be easily accessible properties of the objects.
*   **Category:** `Astrology`, `API`
*   **Tasks:**
    *   [x] Evaluate if enhancing `VedicBody` or related classes to store and provide easy access to calculated Vedic-specific data (Shadbala breakdowns, detailed dignities, aspect info) would improve the API usability.
    *   [x] Consider adding methods to `VedicBody` for common Vedic queries.

## 9. Graha Drishti Strength Values for Drig Bala

*   **Finding:** The function `flatlib.vedic.aspects.get_graha_drishti_strength` assigns percentage-based strengths (1.0, 0.75, 0.5, 0.25) based on aspect type. While these might be useful for general aspect interpretation, they do not directly map to the standard Virupa point system required for Drig Bala calculations (e.g., 60 points for full aspect, 45 for 3/4, 30 for 1/2, 15 for 1/4, with variations for benefic/malefic aspects). This will lead to incorrect Drig Bala scores.
*   **Category:** `Astrology`, `Math`, `Shadbala`
*   **Tasks:**
    *   [x] Create a new function or modify `get_graha_drishti_strength` (or preferably create a dedicated function in the `drig_bala` module) to return the correct Virupa points for an aspect based on the aspecting planet, the aspected planet (benefic/malefic status), and the aspect type/distance, according to standard Drig Bala rules (e.g., BPHS).
    *   [x] Ensure the Drig Bala calculation function uses these correct Virupa points.

## 10. Non-Standard Drig Bala Calculation Logic

*   **Finding:** The main `flatlib.vedic.shadbala.drig_bala.calculate_drig_bala` function calculates the final score by subtracting the value derived from aspects *cast* by the planet from the value derived from aspects *received* by the planet (`net_value = aspects_received['value'] - aspects_cast['value']`). Standard Drig Bala calculation methodology typically focuses only on the net sum of Virupa points from aspects *received* (positive for benefic aspects, negative for malefic aspects).
*   **Category:** `Astrology`, `Math`, `Shadbala`
*   **Tasks:**
    *   [x] Modify `calculate_drig_bala` to compute the final score based solely on the sum of Virupa points from aspects received, applying the correct positive/negative sign based on the aspecting planet's benefic/malefic nature.
    *   [x] Remove or refactor the `calculate_aspects_cast` function within `drig_bala.py` as it's not standard for this specific Shadbala component.

## 11. Missing Moolatrikona Dignity Data

*   **Finding:** The primary dignity table (`flatlib.dignities.tables.ESSENTIAL_DIGNITIES`) completely lacks definitions for Moolatrikona signs and their specific degree ranges for each planet. Moolatrikona is a crucial dignity in Vedic astrology, especially for Shadbala (Saptavarga Bala).
*   **Category:** `Astrology`, `Data`, `Shadbala`
*   **Tasks:**
    *   [x] Create a comprehensive data structure (potentially in a new `flatlib/vedic/tables.py` or within `const.py`) defining the Moolatrikona sign and exact degree range for each of the 7 traditional planets according to authoritative Vedic sources.
    *   [x] Update dignity assessment functions (like `calculate_sign_strength`) to correctly identify when a planet falls within its Moolatrikona range.

## 12. Incorrect Vedic Exaltation/Fall Degrees

*   **Finding:** The exaltation and corresponding fall degrees listed in `flatlib.dignities.tables.ESSENTIAL_DIGNITIES` contain inaccuracies compared to standard Vedic astrology values for several planets:
    *   Sun: Exaltation listed as Aries 19° (Vedic standard is 10°)
    *   Jupiter: Exaltation listed as Cancer 15° (Vedic standard is 5°)
    *   Saturn: Exaltation listed as Libra 21° (Vedic standard is 20°)
*   **Category:** `Astrology`, `Data`, `Shadbala`
*   **Tasks:**
    *   [x] Correct the exaltation/fall degree values in the primary dignity source used for Vedic calculations to match standard Vedic degrees.
    *   [x] Verify the source being used (e.g., `ESSENTIAL_DIGNITIES` or a potential new Vedic table) is consistently applied.

## 13. Incorrect/Incomplete Natural Friendship Implementation

*   **Finding:** The functions `get_friendly_signs` and `get_enemy_signs` in `flatlib.vedic.vargas.analysis` attempt to define Natural Friendships but have issues:
    *   **Incorrect Data:** The Moon is incorrectly listed as having Saturn as a Natural Enemy.
    *   **Incorrect Logic:** The functions return lists of *signs ruled by* friends/enemies, instead of determining the Natural Friendship status between a planet and the lord of a sign it occupies, which is the standard requirement for Shadbala calculations.
*   **Category:** `Astrology`, `Logic`, `Shadbala`
*   **Tasks:**
    *   [x] Correct the Natural Friendship data (specifically for the Moon's enemies).
    *   [x] Refactor or create a new function to determine the correct Natural Friendship status (Friend, Enemy, Neutral) between two planets according to Vedic rules.

## 14. Missing Temporal and Combined Friendship Calculation

*   **Finding:** The library completely lacks the logic to calculate Temporal Friendships based on planetary placements relative to each other in a specific chart. Consequently, the essential 5-fold combined friendship status (Great Friend, Friend, Neutral, Enemy, Great Enemy), derived from combining Natural and Temporal friendships, cannot be determined.
*   **Category:** `Astrology`, `Logic`, `Shadbala`
*   **Tasks:**
    *   [x] Implement a function to calculate Temporal Friendship (Temporary Friend/Enemy) between two planets based on their house positions relative to each other in the D1 chart.
    *   [x] Implement a function to combine Natural and Temporal friendship statuses to derive the final 5-fold relationship.
    *   [x] Ensure that Shadbala components requiring this status (like Saptavarga Bala within `calculate_sign_strength`) utilize the correct 5-fold status.

## 15. Verification Needed for Saptavarga Bala Implementation

*   **Finding:** While `flatlib/vedic/dignities.py` appears to contain the correct data and functions for Vedic dignities (Exaltation, Moolatrikona) and combined friendships (Natural + Temporal), the implementation of `calculate_saptavarga_bala` within `sthana_bala.py` requires specific verification. It needs to be confirmed that this function correctly utilizes the combined friendship status and applies the standard Virupa point system for each dignity level (Exaltation, Moolatrikona, Own Sign, Great Friend, Friend, Neutral, Enemy, Great Enemy) across the seven Vargas (D1, D2, D3, D7, D9, D12, D30).
*   **Category:** `Astrology`, `Logic`, `Shadbala`
*   **Tasks:**
    *   [x] Review the code of `calculate_saptavarga_bala` in `sthana_bala.py`.
    *   [x] Confirm it fetches the Combined Friendship status using `vedic_dignities.calculate_combined_friendship` (or equivalent logic).
    *   [x] Confirm it assigns the correct Virupa points based on the planet's dignity (including Moolatrikona, Own Sign, and the 5 levels of friendship relative to the sign lord) in each of the 7 Vargas.
    *   [x] Refactor `calculate_saptavarga_bala` if it deviates from standard Vedic calculation methods or point systems.

## 16. Saptavarga Bala Implementation Errors

*   **Finding:** The `calculate_saptavarga_bala` function in `sthana_bala.py` contains multiple significant deviations from standard Vedic calculation methods:
    *   **Incorrect Friendship:** Uses only Natural Friendships, failing to incorporate required Temporal Friendships to get the Combined Friendship status.
    *   **Non-Standard Points:** Employs an arbitrary, simplified point scale for dignities instead of the standard Virupa system (e.g., Moolatrikona should yield ~45 Virupas, not 4.0).
    *   **Incorrect Dignity Scope:** Assigns points for Exaltation/Debilitation, which are typically handled only by Uchcha Bala, not Saptavarga Bala.
    *   **Non-Standard Weighting:** Applies weights to the contribution of each Varga, which is not standard practice for Saptavarga Bala within Shadbala.
    *   **Non-Standard Scaling:** Uses arbitrary maximums and double scaling for the final result, instead of a simple sum of Virupas obtained.
*   **Category:** `Astrology`, `Logic`, `Shadbala`
*   **Tasks:**
    *   [x] Refactor `calculate_saptavarga_bala` to use `vedic_dignities.calculate_combined_friendship` to determine the planet's relationship with the sign lord in each Varga.
    *   [x] Implement the standard Virupa point system for Moolatrikona (~45), Own Sign (~30), Great Friend (~22.5), Friend (~15), Neutral (~7.5), Enemy (~3.75), Great Enemy (~1.875).
    *   [x] Remove Exaltation/Debilitation checks from Saptavarga Bala point assignment.
    *   [x] Remove the non-standard Varga weighting.
    *   [x] Calculate the final Saptavarga Bala score as the simple sum of Virupas obtained across the 7 Vargas.

## 17. Ojha/Yugma Bala Implementation Errors

*   **Finding:** The `calculate_ojha_yugma_bala` function in `sthana_bala.py` is incorrectly implemented according to standard Vedic rules:
    *   **Missing Navamsha Check:** It only considers the planet's sign in the Rashi (D1) chart. Standard calculation requires checking the sign type (Odd/Even) in both the Rashi (D1) *and* the Navamsha (D9) charts. Points (typically 15 Virupas) are awarded only if the planet occupies a favorable sign type in *both* divisional charts.
    *   **Incorrect Mercury Classification:** Mercury is listed as preferring only Odd signs. Standard texts state Mercury gains strength in *both* Odd and Even signs.
    *   **Simplified Rahu/Ketu:** Rahu and Ketu are given a fixed half-strength (7.5 Virupas) regardless of sign placement, which is a non-standard simplification.
*   **Category:** `Astrology`, `Logic`, `Shadbala`
*   **Tasks:**
    *   [x] Modify `calculate_ojha_yugma_bala` to accept both the Rashi (D1) sign and Navamsha (D9) sign as input.
    *   [x] Implement the logic to check if the planet is in a favorable sign type (Odd/Even) in *both* D1 and D9.
    *   [x] Correct Mercury's classification to gain strength in both Odd and Even signs (or always award full points).
    *   [x] Review and implement a more standard handling for Rahu/Ketu (e.g., neutral, based on dispositor, etc.) or clarify the source of the current rule.

## 18. Dig Bala Implementation Errors

*   **Finding:** The `calculate_dig_bala` function in `dig_bala.py` uses the correct standard *method* for calculating strength based on house distance (0-60 Virupas, linear interpolation). However, it assigns planets to the **wrong houses/directions** of strength:
    *   Jupiter/Mercury: Assigned 10th House (North) instead of **1st House (East)**.
    *   Sun/Mars: Assigned 1st House (East) instead of **10th House (South)**.
    *   Moon/Venus: Assigned 4th House (correct) but direction labeled "South" instead of **North**.
    *   Saturn: Assigned 7th House (West) - **Correct**.
    *   Rahu/Ketu: Assigned 0 strength - **Correct/Standard**.
*   **Category:** `Astrology`, `Logic`, `Shadbala`
*   **Tasks:**
    *   [x] Correct the `preferred_house` assignments within `calculate_dig_bala` to match standard Vedic rules (Jup/Merc->1st, Sun/Mars->10th, Moon/Ven->4th, Sat->7th).
    *   [x] Correct the direction label associated with the 4th house to "North".

## 19. Nathonnatha Bala Implementation Errors

*   **Finding:** The `calculate_nathonnatha_bala` function in `kala_bala.py` is incorrectly implemented according to standard Vedic rules:
    *   **Incorrect Planet Classification:** Assigns Venus to the nocturnal group and Saturn to the diurnal group, contrary to standard rules (Venus=Diurnal, Saturn=Nocturnal).
    *   **Simplified Calculation:** Uses a basic day/night check (`chart.isDiurnal()`) and assigns full or zero strength. Standard calculation requires determining the birth time's interval from local midday/midnight and applying linear interpolation (max 60 Virupas at peak, min 0 at nadir). The current code lacks this interpolation.
    *   **Simplified Rahu/Ketu:** Assigns a non-standard flat half-strength.
*   **Category:** `Astrology`, `Logic`, `Shadbala`
*   **Tasks:**
    *   [x] Correct the diurnal/nocturnal planet classifications within `calculate_nathonnatha_bala`.
    *   [x] Replace the `chart.isDiurnal()` check with calculations involving local midday and midnight times (requires sunrise/sunset calculations).
    *   [x] Implement the standard linear interpolation formula to calculate strength based on the time interval from midday/midnight.
    *   [x] Review and implement standard handling for Rahu/Ketu (likely exclude them or assign 0).

## 20. Paksha Bala Implementation Review

*   **Finding:** The `calculate_paksha_bala` function appears to correctly implement the standard rules for Paksha Bala:
    *   Correctly identifies Shukla (waxing) and Krishna (waning) Paksha.
    *   Correctly classifies planets as benefic/malefic for this purpose.
    *   Correctly scales strength (0-60 Virupas) based on the calculated lunar phase (`phase`), where Benefics gain strength towards Full Moon and Malefics gain strength towards New Moon.
*   **Potential Issue:** The calculation's accuracy depends on `angle.distance(sun.lon, moon.lon)` returning the Moon's elongation from the Sun in the direction of zodiacal motion (0-360 degrees). If it returns the shortest angle (0-180), the phase calculation for Krishna Paksha might be inaccurate.
*   **Category:** `Astrology`, `Logic`, `Shadbala`, `Dependency`
*   **Tasks:**
    *   [x] Verify the behavior of `angle.distance(a, b)`. Ensure it returns `(b-a) % 360` or adjust the Paksha Bala calculation accordingly if it returns the shortest distance.

## 21. Tribhaga Bala Not Implemented

*   **Finding:** The `calculate_tribhaga_bala` function in `kala_bala.py` is currently a **placeholder**. It does not implement the standard Tribhaga Bala calculation. Instead, it returns a fixed value of 30 Virupas with the description "Fixed value for Tribhaga Bala".
*   **Missing Logic:** The function lacks the necessary calculations to:
    *   Determine sunrise and sunset times.
    *   Divide the day (sunrise-sunset) and night (sunset-sunrise) durations into three equal parts.
    *   Identify which part the birth time falls into.
    *   Assign strength (60 Virupas) based on the ruling planet for that part (Day: 1st-Merc, 2nd-Sun, 3rd-Sat; Night: 1st-Moon, 2nd-Ven, 3rd-Mars; Jupiter always gets 60).
*   **Category:** `Astrology`, `Logic`, `Shadbala`, `Missing Implementation`
*   **Tasks:**
    *   [x] Implement the full logic for Tribhaga Bala calculation in `calculate_tribhaga_bala`, including sunrise/sunset calculation, day/night division, and strength assignment based on planetary rulership of the parts.

## 22. Abda Bala Uses Non-Standard Simplification

*   **Finding:** The `calculate_abda_bala` function determines the Lord of the Year (Abda Pati) using a **non-standard simplification**. It relies on `Gregorian Year % 7` and assigns rulership based on a fixed cycle corresponding to the remainder.
*   **Standard Method:** The traditional method calculates the Abda Pati as the lord of the weekday on which the solar year begins (usually Mesha Sankranti). This requires accurate calculation of the Sankranti time and its corresponding weekday.
*   **Impact:** The current implementation awards the correct strength (15 Virupas) but assigns it based on a simplified rule, not to the actual astrological Lord of the Year.
*   **Category:** `Astrology`, `Logic`, `Shadbala`, `Simplification`, `Accuracy`
*   **Tasks:**
    *   [x] Replace the `year % 7` simplification with the standard calculation of the Abda Pati (weekday lord of the solar year's start). This will require integrating functionality to calculate Mesha Sankranti time accurately.

## 23. Masa Bala Uses Non-Standard Simplification

*   **Finding:** The `calculate_masa_bala` function determines the Lord of the Month (Masa Pati) using a **non-standard simplification**. It relies on the **Gregorian calendar month** of birth and assigns rulership based on a fixed, seemingly arbitrary mapping of planets to these months.
*   **Standard Method:** The traditional method calculates the Masa Pati as the lord of the weekday on which the **solar month begins** (the day of the Sun's ingress into a new sign, Sankranti).
*   **Impact:** The current implementation awards the correct strength (30 Virupas) but assigns it based on a simplified rule tied to the Gregorian calendar, not to the actual astrological Lord of the Month.
*   **Category:** `Astrology`, `Logic`, `Shadbala`, `Simplification`, `Accuracy`
*   **Tasks:**
    *   [x] Replace the Gregorian month simplification with the standard calculation of the Masa Pati (weekday lord of the solar month's start). This requires integrating functionality to calculate the precise times of all solar ingresses (Sankrantis).

## 24. Hora Bala Uses Non-Standard Simplification

*   **Finding:** The `calculate_hora_bala` function uses **non-standard simplifications** and is **incorrectly implemented**:
    *   It relies on standard **clock hours** (`datetime.hour`) instead of calculating variable-length planetary hours (Horas) based on day/night duration.
    *   It uses a simplified day/night check (`chart.isDiurnal()`) instead of precise sunrise/sunset calculations.
    *   The `hour_of_day % 7` logic and the fixed `hour_rulers` dictionaries do not correctly determine the ruler of the Hora, which should start with the Vara Lord (weekday lord) at sunrise and follow the standard planetary sequence.
*   **Standard Method:** Requires calculating sunrise/sunset, determining day/night duration, dividing each by 12 to find the length of daytime and nighttime Horas, identifying the first Hora lord (Vara Lord), following the correct planetary sequence, and finding the ruler of the specific Hora the birth time falls into.
*   **Impact:** The current implementation assigns Hora Bala based on incorrect assumptions and calculations, not reflecting the actual planetary hour rulership at birth.
*   **Category:** `Astrology`, `Logic`, `Shadbala`, `Simplification`, `Accuracy`
*   **Tasks:**
    *   [ ] Remove the simplified logic based on clock hours and `hour_of_day % 7`.
    *   [ ] Implement the standard Hora Bala calculation:
        *   Calculate sunrise and sunset times.
        *   Calculate daytime and nighttime Hora lengths.
        *   Determine the Vara Lord (weekday lord).
        *   Determine the Hora sequence starting from the Vara Lord at sunrise.
        *   Identify the specific Hora the birth time falls into.
        *   Assign 60 Virupas to the ruling planet of that Hora.

## 25. Ayana Bala Incorrectly Implemented

*   **Finding:** The `calculate_ayana_bala` function is **fundamentally incorrect** and does not calculate Ayana Bala according to standard Vedic principles:
    *   It **fails to calculate or use the declination** of the planet (`planet_id`), which is the basis of Ayana Bala.
    *   It incorrectly uses the Sun's path (Uttarayana/Dakshinayana) and a benefic/malefic classification as the primary factors, assigning a fixed strength (30 or 0 Virupas).
    *   The maximum value used (30 Virupas) is half the standard maximum (60 Virupas).
*   **Standard Method:** Requires calculating the specific planet's declination (`δ`) and often uses a formula like `Strength = (30 + (Declination / Obliquity) * 30)` adjusted for the planet's preferred hemisphere (North/South), scaling up to 60 Virupas.
*   **Impact:** The current implementation yields completely wrong results for Ayana Bala.
*   **Category:** `Astrology`, `Logic`, `Shadbala`, `Incorrect Implementation`, `Accuracy`
*   **Tasks:**
    *   [ ] Remove the existing incorrect logic based on the Sun's path.
    *   [ ] Implement the standard Ayana Bala calculation:
        *   Calculate the declination (`δ`) for the given `planet_id`.
        *   Obtain the obliquity of the ecliptic (`ε`).
        *   Apply the standard formula (e.g., `(30 + (δ / ε) * 30)`) incorporating adjustments for the planet's preferred declination direction (North/South) to scale strength from 0 to 60 Virupas.

## 26. Yuddha Bala Incorrectly Implemented

*   **Finding:** The `calculate_yuddha_bala` function is **significantly simplified and incorrectly implemented**:
    *   **Incorrect Participants:** Includes Sun, Moon, Rahu, and Ketu in planetary war (Graha Yuddha) checks. Standard rules only consider Mars, Mercury, Jupiter, Venus, Saturn.
    *   **Simplified Winner Logic:** Uses a fixed hierarchical order (`planet_order`) to determine the winner, ignoring standard factors like declination, brightness, speed, etc.
    *   **Incorrect Strength Value:** Assigns a fixed strength (30 Virupas) to the winner/non-participant and 0 to the loser. Standard Yuddha Bala strength is typically derived from the difference in the planets' other Shadbala strengths (e.g., `sqrt(|Shadbala1 - Shadbala2|)`).
    *   **Incorrect Integration:** Treats Yuddha Bala as a component added *within* Kala Bala. It's often calculated *after* other components are summed and acts as a final *correction* (added to winner, subtracted from loser).
*   **Impact:** The calculation provides inaccurate Yuddha Bala results and incorrectly affects the Kala Bala total.
*   **Category:** `Astrology`, `Logic`, `Shadbala`, `Simplification`, `Accuracy`
*   **Tasks:**
    *   [ ] Modify the function to only consider valid participants (Mars, Mercury, Jupiter, Venus, Saturn) for Yuddha checks.
    *   [ ] Implement a standard method for determining the winner (this can be complex, potentially starting with declination/latitude as a primary factor).
    *   [ ] Implement the standard strength calculation based on the difference in other Shadbala components.
    *   [ ] Move the Yuddha Bala calculation outside the main Kala Bala summation, likely to be applied as a final correction after summing the five main Shadbala components.

## 27. Cheshta Bala Incorrectly Implemented

*   **Finding:** The `calculate_cheshta_bala` function is **incorrectly implemented** for planets and incomplete for luminaries:
    *   **Sun/Moon:** Correctly excluded from the direct calculation but fails to incorporate their strength derived from Ayana Bala (Sun) and Paksha Bala (Moon) as required by many standard systems.
    *   **Planets (Mars-Saturn):** The calculation is fundamentally flawed:
        *   Uses fixed *maximum* speeds (`get_max_speed`) instead of standard *average* speeds.
        *   Fails to calculate or use the planet's *mean* speed.
        *   Ignores the planet's position relative to the Sun (synodic cycle) and the concept of `Cheshta Kendra`.
        *   Incorrectly *reduces* strength for retrograde motion, contrary to standard rules where retrograde motion (especially when slow) increases Chesta Bala.
        *   The logic based on `relative_speed` (current speed / max speed) is non-standard.
*   **Impact:** Provides inaccurate Cheshta Bala values for all objects.
*   **Category:** `Astrology`, `Logic`, `Shadbala`, `Incorrect Implementation`, `Accuracy`
*   **Tasks:**
    *   [ ] Modify the function to include calculations for Sun (based on Ayana Bala) and Moon (based on Paksha Bala), potentially dividing their respective Bala by 2 or following a specific authoritative source.
    *   [ ] For Mars-Saturn, replace the current logic with the standard calculation:
        *   Obtain mean and true longitudes for the planet and the Sun.
        *   Calculate the planet's mean speed and current speed.
        *   Calculate the `Cheshta Kendra` (Mean Longitude - True Longitude).
        *   Apply the standard formula based on speed deviation and `Cheshta Kendra` to scale strength from 0 to 60 Virupas, ensuring retrograde motion is appropriately awarded strength.

## 28. Naisargika Bala Implementation Errors

*   **Finding:** The `calculate_naisargika_bala` function contains errors in the assigned values:
    *   **Jupiter/Venus Swap:** The fixed Naisargika Bala values for Jupiter (~34.3) and Venus (~42.9) are incorrectly swapped in the `natural_strengths` dictionary. Jupiter is assigned 42.9, and Venus is assigned 34.3.
    *   **Rahu/Ketu:** These nodes are assigned a non-standard, arbitrary value of 30.0. Traditional methods usually exclude them or assign them Saturn's value (~8.6).
*   **Impact:** Provides incorrect Naisargika Bala values for Jupiter, Venus, Rahu, and Ketu.
*   **Category:** `Astrology`, `Data`, `Shadbala`, `Accuracy`
*   **Tasks:**
    *   [ ] Correct the values for Jupiter and Venus in the `natural_strengths` dictionary to match the standard hierarchy (Venus ~42.9, Jupiter ~34.3).
    *   [ ] Decide on a consistent handling for Rahu/Ketu: either remove them from the dictionary (assigning 0.0 by default) or assign them Saturn's standard value (~8.6). Update the associated comment.

## 29. Shadbala Aggregation Issues

*   **Finding:** The `calculate_total_shadbala` function in `core.py` exhibits several issues:
    *   **Fragile Value Extraction:** Relies on specific dictionary keys (`'total'` or `'value'`) from the component functions. This is prone to errors if the component functions change their output format.
    *   **Simplified Relative Strength:** Calculates `relative_strength` using a fixed, arbitrary maximum (`max_possible = 600.0`). Standard relative strength requires comparison to the *theoretical maximum achievable* Shadbala, which is variable and complex to calculate.
    *   **Missing Yuddha Bala:** Fails to incorporate the Yuddha Bala correction, which should be applied *after* summing the main six components according to standard methods.
*   **Impact:** The final Shadbala score may be inaccurate due to the missing Yuddha Bala correction, and the `relative_strength` metric is unreliable. The aggregation logic is vulnerable to changes in component function outputs.
*   **Category:** `Astrology`, `Logic`, `Shadbala`, `Accuracy`, `Integration`
*   **Tasks:**
    *   [ ] Standardize the output format (e.g., always use `'value'`) from all component Shadbala functions (`calculate_sthana_bala`, `calculate_kala_bala`, etc.) and update the extraction logic here accordingly.
    *   [ ] Either remove the simplified `relative_strength` calculation or replace it with a placeholder/comment indicating a more complex calculation is needed.
    *   [ ] Implement the Yuddha Bala calculation and apply its result as a correction *after* the initial summation of the six components within the main `get_shadbala` function (in `__init__.py`), not within this aggregation function.

---
