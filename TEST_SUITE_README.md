# Flatlib Test Suite

This directory contains a comprehensive test suite for the Flatlib library. The test suite is designed to run all existing tests and provide clean, detailed reporting.

## Quick Start

To run all tests with default settings:

```bash
python run_test_suite.py
```

This will run all tests except for known failing tests and example tests, and provide a detailed report in the console.

## Test Suite Options

The test suite provides several options for customizing the test run:

```bash
python run_test_suite.py --category core --html --output test_results.txt
```

### Available Options

- `--category`: Run tests from a specific category. Available categories:
  - `core`: Core functionality tests
  - `caching`: Caching-related tests
  - `vedic`: Vedic astrology tests
  - `examples`: Example tests
  - `compatibility`: Compatibility tests
  - `error_handling`: Error handling tests
  - `all`: All tests

- `--include-failing`: Include tests that are known to fail
- `--html`: Generate an HTML report (requires `html-testRunner` package)
- `--output`: Output file for test results
- `--verbosity`: Verbosity level (1-3)

## HTML Reports

To generate HTML reports, you need to install the `html-testRunner` package:

```bash
pip install html-testRunner
```

Then run the test suite with the `--html` option:

```bash
python run_test_suite.py --html
```

The HTML report will be generated in the `test_reports` directory.

## Advanced Usage

For more advanced usage, you can use the `run_tests.py` script directly:

```bash
python run_tests.py --dir tests --pattern "test_*.py" --verbosity 2 --output test_results.txt
```

### Available Options

- `--dir`: Directory to search for tests
- `--pattern`: Pattern to match test files
- `--verbosity`: Verbosity level (1-3)
- `--output`: Output file for test results
- `--modules`: Specific test modules to run
- `--exclude`: Test modules to exclude
- `--include-examples`: Include example tests

## Configuration

The test suite configuration is stored in `test_config.py`. You can modify this file to customize the test suite behavior:

- `EXCLUDED_TESTS`: List of test modules to exclude from the default test run
- `SLOW_TESTS`: List of test modules that are known to be slow
- `TEST_DIRECTORIES`: Default test directories
- `TEST_CATEGORIES`: Test categories and their corresponding modules

## Examples

### Run Core Tests Only

```bash
python run_test_suite.py --category core
```

### Run All Tests Including Known Failing Tests

```bash
python run_test_suite.py --category all --include-failing
```

### Generate HTML Report for Caching Tests

```bash
python run_test_suite.py --category caching --html
```

### Run Tests with High Verbosity and Save Output to File

```bash
python run_test_suite.py --verbosity 3 --output detailed_results.txt
```
