"""Simple test of GPS functionality."""

def test_gps_logic():
    """Test basic GPS logic functionality."""
    try:
        from gps_logic import GPSLogic
        
        # Initialize GPSLogic
        gps = GPSLogic()
        print("✓ GPSLogic initialized successfully")
        
        # Test adding a marker
        gps.add_marker("Test Location", 40.7128, -74.0060, "Test Description")
        markers = gps.get_markers()
        assert len(markers) > 0, "No markers were added"
        print("✓ Successfully added and retrieved marker")
        
        # Test map creation
        map_obj = gps.create_map(center=(40.7128, -74.0060))
        assert map_obj is not None, "Failed to create map"
        print("✓ Successfully created map with markers")
        
        print("\n✅ All tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_gps_logic()
