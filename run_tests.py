"""Simple test runner script."""
import pytest
import sys

if __name__ == "__main__":
    # Run pytest programmatically
    exit_code = pytest.main(["tests/test_simple.py", "-v"])
    sys.exit(exit_code)
