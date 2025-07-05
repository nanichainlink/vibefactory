"""
Pytest configuration and fixtures for the VibeFactory test suite.
"""
import os
import sys
from pathlib import Path
from typing import Generator, Any

import pytest
from fastapi.testclient import TestClient

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from vibefactory.api.main import app  # noqa: E402


@pytest.fixture(scope="module")
def test_client() -> Generator[TestClient, Any, None]:
    """Create a test client for the FastAPI application."""
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def sample_project_data() -> dict:
    """Sample project data for testing."""
    return {
        "description": "A test project for VibeFactory",
        "project_type": "web",
        "config": {
            "framework": "fastapi",
            "database": "sqlite",
            "auth": True
        }
    }
