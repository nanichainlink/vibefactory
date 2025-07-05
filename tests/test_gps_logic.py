"""
Tests for the GPS Logic module.
"""
import pytest
from gps_logic import GPSLogic

def test_gps_logic_initialization():
    """Test that GPSLogic initializes correctly."""
    gps = GPSLogic()
    assert gps is not None

def test_add_and_get_markers():
    """Test adding and retrieving markers."""
    gps = GPSLogic()
    
    # Test adding a marker
    gps.add_marker("Test Location", 40.7128, -74.0060, "Test Description")
    markers = gps.get_markers()
    
    # Verify marker was added
    assert len(markers) > 0
    assert markers[-1]["name"] == "Test Location"
    assert markers[-1]["latitude"] == 40.7128
    assert markers[-1]["longitude"] == -74.0060
    assert markers[-1]["description"] == "Test Description"

def test_create_map():
    """Test map creation with markers."""
    gps = GPSLogic()
    
    # Add a test marker
    gps.add_marker("Test Location", 40.7128, -74.0060, "Test Description")
    
    # Create a map
    map_obj = gps.create_map(center=(40.7128, -74.0060))
    
    # Verify map was created
    assert map_obj is not None
    assert "folium.folium.Map" in str(type(map_obj))
