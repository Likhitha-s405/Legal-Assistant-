# test_location.py - Test location parsing
from case_parser import CaseParser

parser = CaseParser()

# Test cases
test_inputs = [
    "New York, NY",
    "Los Angeles, CA",
    "in Chicago, IL",
    "at Houston, TX",
    "injury of jumana from cet,new york",  # Your input
    "Divorce case in Miami, Florida",
]

for test in test_inputs:
    print(f"\nTesting: '{test}'")
    lat, lng, location = parser.extract_location(test)
    if location:
        print(f"  ✓ Found: {location}")
        if lat and lng:
            print(f"  ✓ Coordinates: {lat}, {lng}")
        else:
            print(f"  ⚠️  Location name found but geocoding failed")
    else:
        print(f"  ✗ No location found")