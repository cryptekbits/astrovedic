# Flatlib Vedic Astrology Review Summary & Task List

This document summarizes the findings from a review of the `flatlib` codebase for its suitability and accuracy regarding Vedic Astrology principles. Tasks required to address the identified issues are listed below each finding. For each task below, we have to maintain backwards compatibility with existing features and tests, and ensure that our changes are well-documented and tested.

---

## Development Workflow Guidelines

### Initial Setup
1. Before starting work on a new feature:
   - Run the test suite: `./run_tests.py`
   - Verify all tests pass before proceeding
   - Check for uncommitted Python code and commit using the format below
   - Only then begin new development

### Development Process
1. Follow an iterative development approach:
   - Break down features into smaller, manageable tasks
   - Implement one component at a time
   - Test each component as you build it
   - Refactor and optimize before moving to the next component

2. When reaching a critical/major development stage:
   - Write comprehensive tests following docs/test_creation_guidelines.md
   - Include proper test metadata in tests/test_metadata.json
   - Run the test suite to verify everything passes
   - Update README.md and other documentation as needed
   - Commit your changes using the format below

### Code Organization
1. Keep files concise and focused:
   - No file should exceed 600-700 lines of code
   - Split large implementations into multiple files
   - Create dedicated directories/packages for complex functionality

2. Plan ahead for complex features:
   - Before implementation, design a logical class structure
   - Organize related functionality into cohesive classes
   - Place related classes in a dedicated package/directory
   - Use clear naming conventions for better maintainability

### Commit Message Format
When committing code changes, follow this changelog-style format:

1. Use a structured header: type(scope): concise title
   - Types: feat, fix, docs, style, refactor, test, chore
   - Scope: area affected (e.g., core, testing, vedic)

2. Follow with a bulleted list of specific changes:
   - Each bullet should start with an action verb
   - Be specific about what was changed
   - Group related changes in the same commit
   - Include implementation details when relevant

Example:
feat(testing): implement comprehensive test suite infrastructure
- Create robust test suite framework in scripts/test.py
- Add run_tests.py wrapper script for easy test execution
- Implement detailed HTML report generation with charts
- Support command-line options for flexible test execution

### Testing Requirements
1. All new features must include tests
2. Tests must follow the structure in docs/test_creation_guidelines.md
3. Add test metadata to tests/test_metadata.json
4. Run the full test suite before committing: `./run_tests.py`
5. Fix any failing tests before proceeding

### Documentation Requirements
1. Update README.md with any user-facing changes
2. Document new features, APIs, and configuration options
3. Include examples for significant new functionality
4. Update any affected existing documentation

---

## Overview
This document summarizes the findings of a review of the `flatlib` codebase concerning its implementation of Vedic Astrology principles. The goal was to identify areas requiring correction or implementation to align with standard practices.

## Identified Issues and Tasks

### 1. Implement Chara Karakas
- **Concern:** Calculation of Jaimini Chara Karakas (Atmakaraka, etc.).
- **File(s):** N/A (New implementation needed).
- **Finding:** This functionality is currently missing from the library.
- **Status:** **Completed.**
- **Tasks:**
    - [x] Implement Chara Karaka calculation based on planetary degrees (longitude), handling exceptions like tied degrees according to standard Jaimini rules.

### 2. Correct Ishta/Kashta Bala Calculation
- **Concern:** Accuracy of Ishta/Kashta Phala calculation.
- **File(s):** `flatlib/vedic/shadbala/advanced.py`
- **Finding:** Uses a non-standard method relying on total Shadbala score and a non-standard 'position factor', instead of the standard method based on exaltation strength (Uchcha Bala) and Cheshta Bala.
- **Status:** **Completed.**
- **Tasks:**
    - [x] Refactor `calculate_ishta_phala` and `calculate_kashta_phala` to use the standard method based primarily on Uchcha Bala and Cheshta Bala.
    - [x] Remove the dependency on total Shadbala and the non-standard `calculate_position_factor`.

### 3. Correct Bhava Bala Calculation
- **Concern:** Accuracy of Bhava Bala (house strength) components.
- **File(s):** `flatlib/vedic/bhava_bala.py`
- **Finding:** Major components deviate from standard methods:
    - **Bhava Digbala:** Uses fixed values instead of cusp's distance from its direction.
    - **Bhava Drishti Bala:** Uses only planetary aspects, ignoring required Rashi Drishti (sign aspects).
    - **Bhava Sthana Bala:** Implements a non-standard component based on house type (Kendra, etc.).
- **Status:** **Completed.**
- **Tasks:**
    - [x] Correct `calculate_bhava_digbala` to use the standard method (distance from directional strength point).
    - [ ] Modify `calculate_bhava_drishti_bala` to include Rashi Drishti.
    - [x] Remove the non-standard `calculate_bhava_sthana_bala` component.

### 4. Correct Varga Chart Calculation (Navamsa Sign)
- **Concern:** Accuracy of calculating the sign for Varga charts, especially D9 (Navamsa).
- **File(s):** `flatlib/vedic/vargas/core.py`
- **Finding:** The generic `calculate_varga_longitude` function correctly calculates the position *within* a Varga, but incorrectly determines the Varga *sign*. It fails to apply the standard Parashari rules based on the Rashi sign's modality (Movable, Fixed, Dual) for Navamsa.
- **Status:** **Incorrect Implementation (Core Logic).**
- **Tasks:**
    - [ ] Refactor `calculate_varga_longitude` or create specific Varga sign functions (e.g., for D9) to correctly implement the standard sign determination rules based on Rashi modality.

### 5. Correct Combustion Calculation (Retrograde Orbs)
- **Concern:** Accuracy of planetary combustion (Asta) check.
- **File(s):** `flatlib/vedic/muhurta/events.py`
- **Finding:** The `is_combust` function uses standard fixed orbs but fails to apply the different, specific orbs required for *retrograde* planets.
- **Status:** **Incomplete Implementation.**
- **Tasks:**
    - [ ] Modify `is_combust` to check the planet's retrograde status and apply the appropriate combustion orb based on whether it's direct or retrograde.

### 6. Correct Cheshta Bala Calculation
- **Concern:** Accuracy of Cheshta Bala (motional strength) calculation.
- **File(s):** `flatlib/vedic/shadbala/cheshta_bala.py`
- **Finding:** The calculation is fundamentally flawed. It incorrectly uses angular distance from the Sun as a proxy for Cheshta Kendra (ignoring mean longitude) and employs non-standard formulae.
- **Status:** **Incorrect Implementation.**
- **Tasks:**
    - [ ] Completely refactor `calculate_cheshta_bala`.
    - [ ] Implement the standard method using mean longitude calculations to determine Cheshta Kendra.
    - [ ] Apply standard formulae for combining speed and Kendra factors to derive Cheshta Bala.

### 7. Ensure Consistent Retrogradation Handling
- **Concern:** Consistent and correct application of retrograde status across calculations.
- **File(s):** `muhurta/events.py`, `shadbala/cheshta_bala.py`, others potentially.
- **Finding:** Retrograde status is handled inconsistently: ignored in Combustion (Item 5), used within the flawed Cheshta Bala (Item 6).
- **Status:** **Inconsistent Handling / Dependent on other fixes.**
- **Tasks:**
    - [ ] Ensure the corrected Combustion calculation (Task for Item 5) properly uses retrograde status.
    - [ ] Ensure the refactored Cheshta Bala calculation (Task for Item 6) correctly incorporates retrograde motion according to standard rules.
    - [ ] Review other areas (e.g., aspects, other strengths) to ensure retrograde status is applied where necessary and according to standard Vedic principles.

### 8. Correct Sunrise/Sunset Calculation
- **Concern:** Accuracy of sunrise and sunset timings used in various calculations.
- **File(s):** `flatlib/vedic/muhurta/timing.py`
- **Finding:** Uses explicitly simplified/inaccurate astronomical formulae. Does not use the precise `swisseph` library, leading to inaccurate timings.
- **Status:** **Completed.**
- **Tasks:**
    - [x] Replace the simplified logic in `get_sunrise` and `get_sunset` with calls to `swisseph.rise_trans`.
    - [x] Ensure the correct arguments (Julian Day, `swisseph.SUN`, rise/set flags, geo-coordinates, default pressure/temp, ephemeris flags) are used as per the library's requirements.

### 9. Correct Ojha/Yugma Bala Calculation
- **Concern:** Accuracy of Ojha/Yugma Bala (strength from Odd/Even sign placement).
- **File(s):** `flatlib/vedic/shadbala/sthana_bala.py`
- **Finding:** Verified. The implementation in `calculate_ojha_yugma_bala` correctly checks both D1 and D9 signs, handles Mercury appropriately (strength in both odd/even), and assigns 0 points to Rahu/Ketu, aligning with standard Vedic rules.
- **Status:** **Verified - Correct Implementation.**
- **Tasks:**
    - [x] ~~Modify `calculate_ojha_yugma_bala` to check the sign type (Odd/Even) in both Rashi (D1) and Navamsa (D9).~~ (Verified: Already implemented correctly)
    - [x] ~~Correct the classification rules for Mercury.~~ (Verified: Already implemented correctly)
    - [x] ~~Apply standard rules or remove the simplified handling for Rahu/Ketu if appropriate for the intended scope.~~ (Verified: Standard handling implemented)

---
