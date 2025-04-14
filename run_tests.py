#!/usr/bin/env python3
"""
Run Astrovedic Test Suite

This script provides a simple interface for running the Astrovedic test suite.
"""

import sys
import os
import importlib.util

# Import the main function directly from the file
script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts', 'test.py')
spec = importlib.util.spec_from_file_location('test_module', script_path)
test_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(test_module)
main = test_module.main

if __name__ == '__main__':
    sys.exit(main())
