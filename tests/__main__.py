"""
Executable test runner for the tests package.
Run with:  python -m tests

This will discover all test_*.py files inside the tests/ directory,
execute them, and print a summary with PASS/FAIL markers.
"""

import sys

def main():
    try:
        import pytest
        # Run pytest on the tests/ directory
        exit_code = pytest.main(["-v", "tests"])
        if exit_code == 0:
            print("\n✅ ALL TESTS PASS")
        else:
            print("\n❌ SOME TESTS FAILED")
    except ImportError:
        import unittest
        loader = unittest.TestLoader()
        suite = loader.discover(start_dir="tests", pattern="test_*.py")
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)

        print("\n" + "="*40)
        print("TEST SUMMARY")
        print("="*40)

        total = result.testsRun
        failures = len(result.failures)
        errors = len(result.errors)
        passed = total - failures - errors

        print(f"Total tests run: {total}")
        print(f"Passed: {passed}")
        print(f"Failures: {failures}")
        print(f"Errors: {errors}")

        if failures == 0 and errors == 0:
            print("\n ALL TESTS PASS")
        else:
            print("\n SOME TESTS FAILED")

if __name__ == "__main__":
    main()