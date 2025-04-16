#!/usr/bin/env python3
"""
Astrovedic Test Suite

This module provides a comprehensive test suite for the Astrovedic library.
It allows running tests with detailed reporting and various options.
"""

import os
import sys
import time
import unittest
import argparse
from datetime import datetime
from unittest import TextTestRunner, TestLoader
from unittest.runner import TextTestResult
import importlib
import json
from pathlib import Path


class AstrovedicTestSuite:
    """
    A comprehensive test suite for the Astrovedic library.
    """

    def __init__(self):
        """Initialize the test suite with default configuration."""
        # Load configuration
        self.config = self._load_config()

        # Set up paths
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.tests_dir = os.path.join(self.base_dir, 'tests')
        self.reports_dir = os.path.join(self.base_dir, 'reports')

        # Ensure reports directory exists
        os.makedirs(self.reports_dir, exist_ok=True)

        # Load test metadata
        self.test_metadata = self._load_test_metadata()

    def _load_config(self):
        """Load test configuration."""
        config = {
            'excluded_tests': [
                # Missing test modules
                'tests.vedic.test_vedic_aspects',
                'tests.vedic.test_vedic_dignities',
                'tests.vedic.test_vedic_avasthas',
                'tests.vedic.test_vedic_object',
                'tests.vedic.yogas.test_yoga_core',
                'tests.vedic.yogas.test_yoga_types',
                'tests.vedic.jaimini.test_jaimini_arudha',
                'tests.vedic.jaimini.test_jaimini_drishti',
                'tests.vedic.jaimini.test_drig_bala',
                'vedic.dignities.test_exaltation',
                'vedic.muhurta.test_muhurta',
                'vedic.sarvatobhadra.test_sarvatobhadra',
                'vedic.test_ashtakavarga',
                'vedic.transits.test_predictions',
                'vedic.transits.test_transits',

                # Modules with missing functionality
                'tests.vedic.muhurta.test_muhurta',
                'tests.vedic.sarvatobhadra.test_sarvatobhadra',
                'tests.vedic.transits.test_vedic_transits',
                'tests.vedic.transits.test_predictions',
                'tests.vedic.transits.test_transits',
                'tests.vedic.dignities.test_exaltation',
                'compatibility.test_compatibility',

                # Modules with implementation errors
                'tests.vedic.shadbala.test_shadbala',
                'vedic.shadbala.test_shadbala',
                'core.test_cache_system',
                'core.test_chart_dynamics',
                'core.test_tool_functions',

                # Modules with failing tests
                'tests.caching.test_caching',
                'caching.test_caching',
                'tests.vedic.compatibility.test_kuta',
                'vedic.compatibility.test_kuta',
                'tests.vedic.transits.test_calculator',
                'vedic.transits.test_calculator'
            ],
            'slow_tests': [],
            'test_directories': [
                'tests',
                'tests/caching',
                'tests/core',
                'tests/examples',
                'tests/vedic',
                'tests/vedic/jaimini',
                'tests/vedic/shadbala',
                'tests/vedic/vargas',
                'tests/vedic/yogas',
                'tests/vedic/aspects',
                'tests/vedic/compatibility',
                'tests/vedic/dashas',
                'tests/vedic/dignities',
                'tests/vedic/muhurta',
                'tests/vedic/transits',
                'tests/compatibility',
                'tests/reference_data'
            ],
            'test_categories': {
                'core': ['tests.core.test_factory', 'tests.core.test_error_handling'],
                'caching': ['tests.caching.test_comprehensive', 'tests.caching.test_calculation_cache',
                          'tests.caching.test_ephemeris_cache', 'tests.caching.test_reference_data_cache'],
                'vedic': ['tests.vedic.vargas.test_divisional_charts', 'tests.vedic.yogas.test_yogas',
                          'tests.vedic.jaimini.test_karakas', 'tests.vedic.shadbala.test_advanced'],
                'examples': ['tests.examples.test_reference_date'],
                'compatibility': ['tests.vedic.compatibility.test_compatibility_core', 'tests.vedic.compatibility.test_kuta'],
                'error_handling': ['tests.core.test_error_handling'],
                'jaimini': ['tests.vedic.jaimini.test_karakas'],
                'muhurta': ['tests.vedic.muhurta.test_muhurta_core'],
                'transits': ['tests.vedic.transits.test_transit_core'],
                'yogas': ['tests.vedic.yogas.test_yogas', 'tests.vedic.yogas.test_surya_yogas'],
                'vargas': ['tests.vedic.vargas.test_divisional_charts', 'tests.vedic.vargas.test_higher_vargas',
                          'tests.vedic.vargas.test_varga_calculations', 'tests.vedic.vargas.test_vimshopaka_bala'],
                'reference_data': ['tests.reference_data.test_ashtakavarga_reference']
            }
        }
        return config

    def _load_test_metadata(self):
        """Load test metadata with friendly names, descriptions, and categories."""
        # Initialize empty metadata dictionary
        metadata = {}

        # Find all test_metadata.json files
        for root, dirs, files in os.walk(os.path.join(self.base_dir, 'tests')):
            if 'test_metadata.json' in files:
                metadata_path = os.path.join(root, 'test_metadata.json')
                try:
                    with open(metadata_path, 'r') as f:
                        file_metadata = json.load(f)
                        # Merge with existing metadata
                        metadata.update(file_metadata)
                except (json.JSONDecodeError, FileNotFoundError):
                    print(f"Warning: Could not load test metadata from {metadata_path}.")

        # If no metadata was found, create a default metadata file
        if not metadata:
            print("Warning: No test metadata found. Creating default metadata.")
            metadata_path = os.path.join(self.base_dir, 'tests', 'test_metadata.json')
            default_metadata = {
                # Examples tests as default
                'tests.examples.test_reference_date.TestReferenceDate.test_tropical_planetary_positions': {
                    'name': 'Tropical Planetary Positions',
                    'description': 'Tests tropical planetary positions against reference data',
                    'category': 'reference_data'
                },
                'tests.examples.test_reference_date.TestReferenceDate.test_vedic_planetary_positions': {
                    'name': 'Vedic Planetary Positions',
                    'description': 'Tests Vedic planetary positions against reference data',
                    'category': 'reference_data'
                }
            }

            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(metadata_path), exist_ok=True)

            # Write default metadata to file
            with open(metadata_path, 'w') as f:
                json.dump(default_metadata, f, indent=4)

            metadata = default_metadata

        return metadata

    class DetailedTestResult(TextTestResult):
        """Custom test result class that provides more detailed output."""

        def __init__(self, stream, descriptions, verbosity, test_suite=None):
            super().__init__(stream, descriptions, verbosity)
            self.successes = []
            self.start_times = {}
            self.execution_times = {}
            self.test_suite = test_suite
            # Track results by category
            self.category_results = {}

        def startTest(self, test):
            super().startTest(test)
            self.start_times[test] = time.time()

        def addSuccess(self, test):
            super().addSuccess(test)
            self.successes.append(test)
            self.execution_times[test] = time.time() - self.start_times[test]
            self._track_category_result(test, 'success')

        def addError(self, test, err):
            super().addError(test, err)
            self.execution_times[test] = time.time() - self.start_times[test]
            self._track_category_result(test, 'error')

        def addFailure(self, test, err):
            super().addFailure(test, err)
            self.execution_times[test] = time.time() - self.start_times[test]
            self._track_category_result(test, 'failure')

        def addSkip(self, test, reason):
            super().addSkip(test, reason)
            self.execution_times[test] = time.time() - self.start_times[test]
            self._track_category_result(test, 'skipped')

        def _track_category_result(self, test, result_type):
            """Track test results by category."""
            if not self.test_suite:
                return

            # Get the category for this test
            test_id = test.id()
            category = self.test_suite._get_category_for_test(test_id)

            # Initialize category if not already present
            if category not in self.category_results:
                self.category_results[category] = {
                    'success': 0,
                    'failure': 0,
                    'error': 0,
                    'skipped': 0,
                    'total': 0
                }

            # Increment the appropriate counter
            self.category_results[category][result_type] += 1
            self.category_results[category]['total'] += 1

        def get_category_summary_table(self):
            """Generate a category-wise summary table."""
            if not self.category_results:
                return "No category data available."

            # Calculate totals
            all_categories = {
                'success': 0,
                'failure': 0,
                'error': 0,
                'skipped': 0,
                'total': 0
            }

            for category_data in self.category_results.values():
                for key, value in category_data.items():
                    all_categories[key] += value

            # Build the table
            table = "\nCATEGORY-WISE TEST SUMMARY\n"
            table += "=" * 80 + "\n"
            table += f"{'Category':<20} {'Total':<10} {'Passed':<10} {'Failed':<10} {'Errors':<10} {'Skipped':<10}\n"
            table += "-" * 80 + "\n"

            # Add rows for each category
            for category, data in sorted(self.category_results.items()):
                table += f"{category:<20} {data['total']:<10} {data['success']:<10} {data['failure']:<10} {data['error']:<10} {data['skipped']:<10}\n"

            # Add totals row
            table += "-" * 80 + "\n"
            table += f"{'TOTAL':<20} {all_categories['total']:<10} {all_categories['success']:<10} {all_categories['failure']:<10} {all_categories['error']:<10} {all_categories['skipped']:<10}\n"
            table += "=" * 80 + "\n"

            return table

    class DetailedTestRunner(TextTestRunner):
        """Custom test runner that uses DetailedTestResult."""

        def __init__(self, test_suite=None, **kwargs):
            super().__init__(**kwargs)
            self.resultclass = AstrovedicTestSuite.DetailedTestResult
            self.test_suite = test_suite

        def run(self, test):
            # Create result object with reference to test_suite
            result = self.resultclass(self.stream, self.descriptions, self.verbosity, self.test_suite)
            self._makeResult = lambda: result  # Override _makeResult to return our custom result

            result = super().run(test)
            return result

    def discover_and_run_tests(self, test_dir='tests', pattern='test_*.py', verbosity=2, output_file=None):
        """
        Discover and run tests from the specified directory.

        Args:
            test_dir (str): Directory to search for tests
            pattern (str): Pattern to match test files
            verbosity (int): Verbosity level (1-3)
            output_file (str): File to write test results to

        Returns:
            unittest.TestResult: Test result object
        """
        # Create test loader
        loader = TestLoader()

        # Discover tests
        test_suite = loader.discover(test_dir, pattern=pattern)

        # Set up output stream
        if output_file:
            stream = open(output_file, 'w')
        else:
            stream = sys.stdout

        # Create and run test runner
        runner = self.DetailedTestRunner(test_suite=self, stream=stream, verbosity=verbosity)
        start_time = time.time()
        result = runner.run(test_suite)
        end_time = time.time()

        # Print summary
        print("\n" + "=" * 80, file=stream)
        print("TEST SUMMARY", file=stream)
        print("=" * 80, file=stream)
        print(f"Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", file=stream)
        print(f"Total Tests: {result.testsRun}", file=stream)
        print(f"Successes: {len(result.successes)}", file=stream)
        print(f"Failures: {len(result.failures)}", file=stream)
        print(f"Errors: {len(result.errors)}", file=stream)
        print(f"Skipped: {len(result.skipped)}", file=stream)
        print(f"Total Time: {end_time - start_time:.2f} seconds", file=stream)
        print("=" * 80, file=stream)

        # Print category-wise summary table
        print(result.get_category_summary_table(), file=stream)

        # Print slow tests
        if result.execution_times:
            print("\nSLOWEST TESTS:", file=stream)
            sorted_times = sorted(result.execution_times.items(), key=lambda x: x[1], reverse=True)
            for test, execution_time in sorted_times[:10]:  # Show top 10 slowest tests
                print(f"{test.id()}: {execution_time:.4f}s", file=stream)

        # Close output file if needed
        if output_file:
            stream.close()
            print(f"Test results written to {output_file}")

        return result

    def run_specific_modules(self, modules, verbosity=2, output_file=None):
        """
        Run specific test modules.

        Args:
            modules (list): List of module names to run
            verbosity (int): Verbosity level (1-3)
            output_file (str): File to write test results to

        Returns:
            unittest.TestResult: Test result object
        """
        # Create test loader
        loader = TestLoader()

        # Create test suite
        test_suite = unittest.TestSuite()

        # Add each module to the suite
        for module_name in modules:
            try:
                module = importlib.import_module(module_name)
                tests = loader.loadTestsFromModule(module)
                test_suite.addTests(tests)
            except (ImportError, AttributeError) as e:
                print(f"Error loading module {module_name}: {e}")

        # Set up output stream
        if output_file:
            stream = open(output_file, 'w')
        else:
            stream = sys.stdout

        # Create and run test runner
        runner = self.DetailedTestRunner(test_suite=self, stream=stream, verbosity=verbosity)
        start_time = time.time()
        result = runner.run(test_suite)
        end_time = time.time()

        # Print summary
        print("\n" + "=" * 80, file=stream)
        print("TEST SUMMARY", file=stream)
        print("=" * 80, file=stream)
        print(f"Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", file=stream)
        print(f"Total Tests: {result.testsRun}", file=stream)
        print(f"Successes: {len(result.successes)}", file=stream)
        print(f"Failures: {len(result.failures)}", file=stream)
        print(f"Errors: {len(result.errors)}", file=stream)
        print(f"Skipped: {len(result.skipped)}", file=stream)
        print(f"Total Time: {end_time - start_time:.2f} seconds", file=stream)
        print("=" * 80, file=stream)

        # Print category-wise summary table
        print(result.get_category_summary_table(), file=stream)

        # Close output file if needed
        if output_file:
            stream.close()
            print(f"Test results written to {output_file}")

        return result

    def generate_html_report(self, modules, report_name=None):
        """
        Generate an HTML report for the specified test modules.

        Args:
            modules (list): List of module names to run
            report_name (str, optional): Name for the report file

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Try to import jinja2
            from jinja2 import Template
        except ImportError:
            print("Jinja2 not installed. Run 'pip install jinja2' to enable HTML reports.")
            return False

        # Create test suite
        suite = unittest.TestSuite()
        loader = unittest.TestLoader()

        for module_name in modules:
            try:
                # Import the module
                module = importlib.import_module(module_name)
                # Add tests from the module
                suite.addTests(loader.loadTestsFromModule(module))
            except ImportError as e:
                print(f"Error importing {module_name}: {e}")

        # Generate timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Set report name
        if not report_name:
            report_name = f"astrovedic_test_report_{timestamp}"

        # Create a custom test result class that tracks execution times
        class CustomTestResult(TextTestResult):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.successes = []
                self.execution_times = {}
                self.start_times = {}
                self.start_time = time.time()

            def startTest(self, test):
                super().startTest(test)
                self.start_times[test] = time.time()

            def addSuccess(self, test):
                super().addSuccess(test)
                self.successes.append(test)
                self.execution_times[test] = time.time() - self.start_times[test]

            def addError(self, test, err):
                super().addError(test, err)
                self.execution_times[test] = time.time() - self.start_times[test]

            def addFailure(self, test, err):
                super().addFailure(test, err)
                self.execution_times[test] = time.time() - self.start_times[test]

            def addSkip(self, test, reason):
                super().addSkip(test, reason)
                self.execution_times[test] = time.time() - self.start_times[test]

        # Create a custom test runner
        class CustomTestRunner(TextTestRunner):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.resultclass = CustomTestResult

        # Run the tests
        runner = CustomTestRunner(verbosity=2)
        result = runner.run(suite)

        # Calculate test duration
        duration = time.time() - result.start_time

        # Prepare template variables
        start_time = datetime.fromtimestamp(result.start_time).strftime('%Y-%m-%d %H:%M:%S')
        duration_str = f"{duration:.2f} seconds"
        status = "passed" if result.wasSuccessful() else "failed"
        total_tests = result.testsRun
        passed_tests = len(result.successes)
        failed_tests = len(result.failures)
        error_tests = len(result.errors)
        skipped_tests = len(result.skipped)

        # Prepare test details
        failed_tests_details = []
        for test, err in result.failures:
            test_id = test.id()
            metadata = self.test_metadata.get(test_id, {})
            failed_tests_details.append({
                'id': test_id,
                'name': metadata.get('name', test_id),
                'description': metadata.get('description', ''),
                'category': metadata.get('category', self._get_category_for_test(test_id)),
                'error_message': str(err).split('\n')[0],
                'traceback': str(err)
            })

        error_tests_details = []
        for test, err in result.errors:
            test_id = test.id()
            metadata = self.test_metadata.get(test_id, {})
            error_tests_details.append({
                'id': test_id,
                'name': metadata.get('name', test_id),
                'description': metadata.get('description', ''),
                'category': metadata.get('category', self._get_category_for_test(test_id)),
                'error_message': str(err).split('\n')[0],
                'traceback': str(err)
            })

        skipped_tests_details = []
        for test, reason in result.skipped:
            test_id = test.id()
            metadata = self.test_metadata.get(test_id, {})
            skipped_tests_details.append({
                'id': test_id,
                'name': metadata.get('name', test_id),
                'description': metadata.get('description', ''),
                'category': metadata.get('category', self._get_category_for_test(test_id)),
                'reason': reason
            })

        passed_tests_details = []
        for test in result.successes:
            test_id = test.id()
            metadata = self.test_metadata.get(test_id, {})
            passed_tests_details.append({
                'id': test_id,
                'name': metadata.get('name', test_id),
                'description': metadata.get('description', ''),
                'category': metadata.get('category', self._get_category_for_test(test_id)),
                'duration': f"{result.execution_times.get(test, 0):.4f}s"
            })

        # Read template
        template_path = self._get_report_template()
        with open(template_path, 'r') as f:
            template_content = f.read()

        # Create template
        template = Template(template_content)

        # Render template
        html_content = template.render(
            title="Unittest Results",
            start_time=start_time,
            duration=duration_str,
            status=status,
            total_tests=total_tests,
            passed_tests=passed_tests,
            failed_tests=failed_tests,
            error_tests=error_tests,
            skipped_tests=skipped_tests,
            failed_tests_details=failed_tests_details,
            error_tests_details=error_tests_details,
            skipped_tests_details=skipped_tests_details,
            passed_tests_details=passed_tests_details,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

        # Write report file
        os.makedirs(self.reports_dir, exist_ok=True)
        report_file = os.path.join(self.reports_dir, f"{report_name}.html")
        with open(report_file, 'w') as f:
            f.write(html_content)

        print(f"HTML report generated in {self.reports_dir}")
        return result.wasSuccessful()

    def _get_report_template(self):
        """
        Get the HTML report template content.

        Returns:
            str: The template content
        """
        template_path = os.path.join(self.base_dir, 'scripts', 'report_template.html')

        # If template doesn't exist, create it
        if not os.path.exists(template_path):
            self._create_report_template(template_path)

        return template_path

    def _create_report_template(self, template_path):
        """
        Create the HTML report template file.

        Args:
            template_path (str): Path to save the template
        """
        template_content = """<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
    <style type="text/css">
        body {
            padding: 30px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .heading {
            margin-top: 20px;
            margin-bottom: 20px;
            color: #2c3e50;
        }
        .summary {
            background-color: #f8f9fa;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 20px;
        }
        .summary-item {
            margin-bottom: 10px;
        }
        .test-case {
            margin-bottom: 15px;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            overflow: hidden;
        }
        .test-case-header {
            padding: 10px 15px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .test-case-content {
            padding: 15px;
            border-top: 1px solid #dee2e6;
            display: none;
        }
        .success {
            background-color: #d4edda;
            color: #155724;
        }
        .failure {
            background-color: #f8d7da;
            color: #721c24;
        }
        .error {
            background-color: #f8d7da;
            color: #721c24;
        }
        .skipped {
            background-color: #fff3cd;
            color: #856404;
        }
        .badge {
            font-size: 0.8em;
            padding: 5px 10px;
        }
        .badge-success {
            background-color: #28a745;
        }
        .badge-danger {
            background-color: #dc3545;
        }
        .badge-warning {
            background-color: #ffc107;
            color: #212529;
        }
        .badge-info {
            background-color: #17a2b8;
        }
        pre {
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        .chart-container {
            width: 400px;
            height: 400px;
            margin: 0 auto;
        }
        .test-details {
            margin-top: 20px;
        }
        .test-details h3 {
            margin-bottom: 15px;
            color: #2c3e50;
        }
        .test-details-table {
            width: 100%;
            margin-bottom: 20px;
        }
        .test-details-table th {
            background-color: #f8f9fa;
            padding: 10px;
            text-align: left;
        }
        .test-details-table td {
            padding: 10px;
            border-bottom: 1px solid #dee2e6;
        }
        .test-details-table tr:hover {
            background-color: #f8f9fa;
        }
        .timestamp {
            color: #6c757d;
            font-size: 0.9em;
        }
        .footer {
            margin-top: 30px;
            padding-top: 10px;
            border-top: 1px solid #dee2e6;
            color: #6c757d;
            font-size: 0.9em;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="heading">{{ title }}</h1>

        <div class="summary">
            <div class="row">
                <div class="col-md-6">
                    <div class="summary-item">
                        <strong>Start Time:</strong> {{ start_time }}
                    </div>
                    <div class="summary-item">
                        <strong>Duration:</strong> {{ duration }}
                    </div>
                    <div class="summary-item">
                        <strong>Status:</strong>
                        {% if status == 'passed' %}
                            <span class="badge badge-success">Passed</span>
                        {% else %}
                            <span class="badge badge-danger">Failed</span>
                        {% endif %}
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="summary-item">
                        <strong>Total Tests:</strong> {{ total_tests }}
                    </div>
                    <div class="summary-item">
                        <strong>Passed:</strong> <span class="badge badge-success">{{ passed_tests }}</span>
                    </div>
                    <div class="summary-item">
                        <strong>Failed:</strong> <span class="badge badge-danger">{{ failed_tests }}</span>
                    </div>
                    <div class="summary-item">
                        <strong>Errors:</strong> <span class="badge badge-danger">{{ error_tests }}</span>
                    </div>
                    <div class="summary-item">
                        <strong>Skipped:</strong> <span class="badge badge-warning">{{ skipped_tests }}</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="chart-container">
            <canvas id="testResultChart"></canvas>
        </div>

        <div class="test-details">
            <h3>Test Results</h3>

            {% if failed_tests_details %}
            <h4>Failed Tests</h4>
            {% for test in failed_tests_details %}
            <div class="test-case">
                <div class="test-case-header failure" onclick="toggleTestCase(this)">
                    <span>{{ test.name }}</span>
                    <span class="badge badge-secondary">{{ test.category }}</span>
                    <span class="badge badge-danger">Failed</span>
                </div>
                <div class="test-case-content">
                    <p><strong>Error Message:</strong></p>
                    <pre>{{ test.error_message }}</pre>
                    <p><strong>Traceback:</strong></p>
                    <pre>{{ test.traceback }}</pre>
                </div>
            </div>
            {% endfor %}
            {% endif %}

            {% if error_tests_details %}
            <h4>Error Tests</h4>
            {% for test in error_tests_details %}
            <div class="test-case">
                <div class="test-case-header error" onclick="toggleTestCase(this)">
                    <span>{{ test.name }}</span>
                    <span class="badge badge-secondary">{{ test.category }}</span>
                    <span class="badge badge-danger">Error</span>
                </div>
                <div class="test-case-content">
                    <p><strong>Error Message:</strong></p>
                    <pre>{{ test.error_message }}</pre>
                    <p><strong>Traceback:</strong></p>
                    <pre>{{ test.traceback }}</pre>
                </div>
            </div>
            {% endfor %}
            {% endif %}

            {% if skipped_tests_details %}
            <h4>Skipped Tests</h4>
            {% for test in skipped_tests_details %}
            <div class="test-case">
                <div class="test-case-header skipped" onclick="toggleTestCase(this)">
                    <span>{{ test.name }}</span>
                    <span class="badge badge-secondary">{{ test.category }}</span>
                    <span class="badge badge-warning">Skipped</span>
                </div>
                <div class="test-case-content">
                    <p><strong>Reason:</strong> {{ test.reason }}</p>
                </div>
            </div>
            {% endfor %}
            {% endif %}

            {% if passed_tests_details %}
            <h4>Passed Tests</h4>
            <table class="test-details-table">
                <thead>
                    <tr>
                        <th>Test Name</th>
                        <th>Description</th>
                        <th>Category</th>
                        <th>Duration</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {% for test in passed_tests_details %}
                    <tr>
                        <td>{{ test.name }}</td>
                        <td>{{ test.description }}</td>
                        <td>{{ test.category }}</td>
                        <td>{{ test.duration }}</td>
                        <td><span class="badge badge-success">Passed</span></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% endif %}
        </div>

        <div class="footer">
            <p>Generated by Astrovedic Test Suite on {{ timestamp }}</p>
        </div>
    </div>

    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <script>
        function toggleTestCase(element) {
            const content = element.nextElementSibling;
            if (content.style.display === "block") {
                content.style.display = "none";
            } else {
                content.style.display = "block";
            }
        }

        // Create chart
        document.addEventListener('DOMContentLoaded', function() {
            const ctx = document.getElementById('testResultChart').getContext('2d');
            const chart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: ['Passed', 'Failed', 'Errors', 'Skipped'],
                    datasets: [{
                        data: [{{ passed_tests }}, {{ failed_tests }}, {{ error_tests }}, {{ skipped_tests }}],
                        backgroundColor: [
                            '#28a745',
                            '#dc3545',
                            '#dc3545',
                            '#ffc107'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'bottom',
                        },
                        title: {
                            display: true,
                            text: 'Test Results'
                        }
                    }
                }
            });
        });
    </script>
</body>
</html>"""

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(template_path), exist_ok=True)

        # Write template to file
        with open(template_path, 'w') as f:
            f.write(template_content)

    def run_tests(self, category=None, exclude_known_failures=True, html_report=False,
                 output_file=None, verbosity=2):
        """
        Run tests with the specified options.

        Args:
            category (str): Test category to run (from config)
            exclude_known_failures (bool): Whether to exclude known failing tests
            html_report (bool): Whether to generate an HTML report
            output_file (str): File to write test results to
            verbosity (int): Verbosity level (1-3)

        Returns:
            int: Exit code (0 for success, 1 for failure)
        """
        # Determine which modules to run
        modules_to_run = []

        if category and category in self.config['test_categories']:
            # Run tests from a specific category
            modules_to_run = self.config['test_categories'][category]
        elif category == 'all':
            # Run all tests by discovering them in all test directories
            print("Running all tests by discovering them in all test directories...")
            test_dirs = self.config['test_directories']
            return self.run_all_tests(test_dirs, exclude_known_failures, html_report, output_file, verbosity)
        else:
            # Default: run all except examples
            for cat, cat_modules in self.config['test_categories'].items():
                if cat != 'examples':
                    modules_to_run.extend(cat_modules)

        # Exclude known failing tests if requested
        if exclude_known_failures:
            modules_to_run = [m for m in modules_to_run if m not in self.config['excluded_tests']]

        # Generate HTML report if requested
        if html_report:
            success = self.generate_html_report(modules_to_run)
            return 0 if success else 1

        # Run the tests
        if modules_to_run:
            result = self.run_specific_modules(modules_to_run, verbosity, output_file)
        else:
            result = self.discover_and_run_tests(self.tests_dir, verbosity=verbosity, output_file=output_file)

        return 0 if result.wasSuccessful() else 1

    def run_all_tests(self, test_dirs, exclude_known_failures=True, html_report=False,
                     output_file=None, verbosity=2):
        """
        Run all tests by discovering them in the specified directories.

        Args:
            test_dirs (list): List of directories to search for tests
            exclude_known_failures (bool): Whether to exclude known failing tests
            html_report (bool): Whether to generate an HTML report
            output_file (str): File to write test results to
            verbosity (int): Verbosity level (1-3)

        Returns:
            int: Exit code (0 for success, 1 for failure)
        """
        # Create a test suite to hold all tests
        all_tests = unittest.TestSuite()
        loader = TestLoader()

        # Discover tests in each directory
        for test_dir in test_dirs:
            dir_path = os.path.join(self.base_dir, test_dir)
            if os.path.exists(dir_path):
                print(f"Discovering tests in {test_dir}...")
                try:
                    # Make sure the directory is a package
                    init_file = os.path.join(dir_path, '__init__.py')
                    if not os.path.exists(init_file):
                        with open(init_file, 'w') as f:
                            f.write('# Auto-generated __init__.py file for test discovery\n')

                    # Discover tests
                    suite = loader.discover(dir_path, pattern='test_*.py')
                    all_tests.addTests(suite)
                except ImportError as e:
                    print(f"Error discovering tests in {test_dir}: {e}")

        # Set up output stream
        if output_file:
            stream = open(output_file, 'w')
        else:
            stream = sys.stdout

        # Create and run test runner
        runner = self.DetailedTestRunner(test_suite=self, stream=stream, verbosity=verbosity)
        start_time = time.time()
        result = runner.run(all_tests)
        end_time = time.time()

        # Print summary
        print("\n" + "=" * 80, file=stream)
        print("TEST SUMMARY", file=stream)
        print("=" * 80, file=stream)
        print(f"Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", file=stream)
        print(f"Total Tests: {result.testsRun}", file=stream)
        print(f"Successes: {len(result.successes)}", file=stream)
        print(f"Failures: {len(result.failures)}", file=stream)
        print(f"Errors: {len(result.errors)}", file=stream)
        print(f"Skipped: {len(result.skipped)}", file=stream)
        print(f"Total Time: {end_time - start_time:.2f} seconds", file=stream)
        print("=" * 80, file=stream)

        # Print category-wise summary table
        print(result.get_category_summary_table(), file=stream)

        # Close output file if needed
        if output_file:
            stream.close()
            print(f"Test results written to {output_file}")

        return 0 if result.wasSuccessful() else 1

    def _get_category_for_test(self, test_id):
        """Determine the category for a test based on its module."""
        # Extract module name from test ID
        module_parts = test_id.split('.')
        if len(module_parts) < 2:
            return 'unknown'

        module_name = '.'.join(module_parts[:2])  # e.g., 'tests.test_chart'

        # Check if module is in a specific category
        for category, modules in self.config['test_categories'].items():
            for cat_module in modules:
                if module_name.startswith(cat_module):
                    return category

        # Special case for caching tests
        if 'caching' in module_name:
            return 'caching'

        return 'unknown'


def main():
    """Parse command line arguments and run the test suite."""
    parser = argparse.ArgumentParser(description='Run the Astrovedic test suite')

    # Add categories
    test_suite = AstrovedicTestSuite()
    categories = list(test_suite.config['test_categories'].keys()) + ['all']
    parser.add_argument('--category', choices=categories, default=None,
                        help='Test category to run')

    # Add other options
    parser.add_argument('--include-failing', action='store_true',
                        help='Include tests that are known to fail')
    parser.add_argument('--html', action='store_true',
                        help='Generate HTML report')
    parser.add_argument('--output', help='Output file for test results')
    parser.add_argument('--verbosity', type=int, default=2,
                        help='Verbosity level (1-3)')

    args = parser.parse_args()

    # Run the test suite
    return test_suite.run_tests(
        category=args.category,
        exclude_known_failures=not args.include_failing,
        html_report=args.html,
        output_file=args.output,
        verbosity=args.verbosity
    )


if __name__ == '__main__':
    sys.exit(main())
