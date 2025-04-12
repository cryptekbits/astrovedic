# Flatlib Test Creation Guidelines

This document provides guidelines for creating and maintaining tests for the Flatlib library.

## Table of Contents

1. [Test Structure](#test-structure)
2. [Test Categories](#test-categories)
3. [Naming Conventions](#naming-conventions)
4. [Test Metadata](#test-metadata)
5. [Writing Effective Tests](#writing-effective-tests)
6. [Running Tests](#running-tests)
7. [Test Reports](#test-reports)

## Test Structure

All tests should be placed in the `tests` directory, organized by category or functionality:

```
tests/
├── __init__.py
├── test_chart.py
├── test_factory.py
├── test_compatibility.py
├── caching/
│   ├── __init__.py
│   ├── test_comprehensive.py
│   ├── test_calculation_cache.py
│   └── test_ephemeris_cache.py
└── examples/
    ├── __init__.py
    └── test_reference_date.py
```

Each test file should:
- Start with `test_` prefix
- Use unittest framework
- Include detailed docstrings explaining the purpose of the tests
- Group related tests in test classes

## Test Categories

Tests are organized into the following categories:

| Category | Description |
|----------|-------------|
| core | Core functionality tests (chart creation, factory methods, etc.) |
| caching | Tests for caching functionality |
| vedic | Tests for Vedic astrology features |
| compatibility | Tests for compatibility calculations |
| error_handling | Tests for error handling and edge cases |
| examples | Example tests and reference data validation |

## Naming Conventions

- **Test Files**: `test_<module_name>.py`
- **Test Classes**: `Test<ModuleName>` or `<ModuleName>Tests`
- **Test Methods**: `test_<functionality_being_tested>`

Example:
```python
# test_chart.py
class ChartTests(unittest.TestCase):
    def test_solar_return_hsys(self):
        """Solar return charts must maintain original house system."""
        # Test implementation
```

## Test Metadata

Each test should have associated metadata in the `tests/test_metadata.json` file with the following information:

- **name**: A human-readable name for the test (e.g., "Solar Return House System")
- **description**: A brief description of what the test verifies
- **category**: The test category (core, caching, vedic, etc.)

Example metadata entry:
```json
{
    "tests.test_chart.ChartTests.test_solar_return_hsys": {
        "name": "Solar Return House System",
        "description": "Tests that solar return charts maintain the original house system",
        "category": "core"
    }
}
```

## Writing Effective Tests

### Test Structure

Each test should follow this structure:
1. **Arrange**: Set up the test data and environment
2. **Act**: Perform the action being tested
3. **Assert**: Verify the expected outcome

Example:
```python
def test_solar_return_hsys(self):
    """Solar return charts must maintain original house system."""
    # Arrange
    date = Datetime('2015/03/13', '17:00', '+00:00')
    pos = GeoPos('38n32', '8w54')
    chart = Chart(date, pos, hsys=const.HOUSES_MORINUS)
    
    # Act
    sr_chart = chart.solarReturn(2018)
    
    # Assert
    self.assertEqual(chart.hsys, sr_chart.hsys)
```

### Test Documentation

Include detailed docstrings for each test method explaining:
- What functionality is being tested
- Expected behavior
- Any special conditions or edge cases
- If the test is expected to generate warnings or errors

### Test Data

- Use consistent test data when possible
- For reference data, use the standard reference date: April 9, 2025 at 20:51 in Bangalore
- Document the source of reference data for validation tests

## Running Tests

Tests can be run using the test suite:

```bash
# Run all tests
python -m scripts.test

# Run tests in a specific category
python -m scripts.test --category vedic

# Generate HTML report
python -m scripts.test --html

# Include tests that are known to fail
python -m scripts.test --include-failing
```

## Test Reports

Test reports are generated in the `reports` directory and include:

- Summary of test results (pass/fail/error/skip)
- Detailed information for each test
- Test name, description, and category
- Duration of each test
- Error messages and tracebacks for failed tests

HTML reports provide a visual representation of test results and can be used to track test coverage and performance over time.

---

## Adding a New Test

1. Create a new test file in the appropriate directory
2. Implement test cases using the unittest framework
3. Add metadata for the tests in `tests/test_metadata.json`
4. Run the tests to verify they work correctly
5. Update documentation if necessary

Example of a new test file:

```python
#!/usr/bin/env python3
"""
Test New Feature

This script tests the new feature in flatlib.
"""

import unittest
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const

class TestNewFeature(unittest.TestCase):
    """Test case for new feature"""
    
    def setUp(self):
        """Set up test case"""
        # Create a chart for the reference date
        date = Datetime('2025/04/09', '20:51', '+05:30')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart = Chart(date, pos, hsys=const.HOUSES_WHOLE_SIGN, mode=const.AY_LAHIRI)
    
    def test_new_feature(self):
        """Test the new feature functionality."""
        # Test implementation
        result = some_function(self.chart)
        self.assertEqual(result, expected_value)

if __name__ == '__main__':
    unittest.main()
```

Example metadata entry for the new test:

```json
{
    "tests.test_new_feature.TestNewFeature.test_new_feature": {
        "name": "New Feature Test",
        "description": "Tests the functionality of the new feature",
        "category": "core"
    }
}
```
