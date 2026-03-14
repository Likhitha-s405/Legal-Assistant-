# test_auto_location.py - Test automatic location detection
from __init__ import LegalCaseAnalyzer
import time

def main():
    print("="*70)
    print("🤖 AUTO LOCATION DETECTION TEST")
    print("="*70)
    
    # Initialize
    analyzer = LegalCaseAnalyzer()
    
    # Add sample data if needed
    analyzer.lawyer_finder.add_sample_data()
    
    print("\n📡 Detecting your location...")
    time.sleep(1)
    
    # Test 1: Find lawyers near me (general)
    print("\n" + "-"*40)
    print("TEST 1: Find any lawyers near me")
    print("-"*40)
    
    result = analyzer.find_lawyers_near_me()
    
    if result.get('success', False):
        print(f"\n✅ Location detected: {result['case_info']['location']}")
        print(f"✅ Method: {result.get('detection_method', 'unknown')}")
        print(f"✅ Lawyers found within {result['max_distance_km']}km: {result['total_found']}")
        
        if result.get('lawyers'):
            print("\n📋 Nearby lawyers:")
            for i, lawyer in enumerate(result['lawyers'][:5], 1):
                print(f"  {i}. {lawyer['name']}")
                print(f"     Firm: {lawyer['firm_name']}")
                print(f"     Specialization: {lawyer['specialization']}")
                print(f"     Distance: {lawyer['distance_km']} km")
                print(f"     Phone: {lawyer['phone']}")
                print()
    else:
        print(f"\n❌ Error: {result.get('message', 'Unknown error')}")
        print("\nFalling back to manual location...")
        print("Please enter your city and state (e.g., 'New York, NY'):")
        location = input("> ")
        
        # You would handle manual input here
        print(f"\nSearching for lawyers near {location}...")
    
    # Test 2: Find specific case type near me
    print("\n" + "-"*40)
    print("TEST 2: Find divorce lawyers near me")
    print("-"*40)
    
    result = analyzer.find_lawyers_near_me(case_type="divorce")
    
    if result.get('success', False):
        print(f"\n✅ Location: {result['case_info']['location']}")
        
        # Count exact matches
        exact_matches = sum(1 for l in result.get('lawyers', []) if l.get('exact_match'))
        print(f"✅ Divorce specialists nearby: {exact_matches}")
        
        if result.get('lawyers'):
            print("\n📋 Divorce lawyers near you:")
            for lawyer in result['lawyers'][:3]:
                match_icon = "🎯" if lawyer.get('exact_match') else "  "
                print(f"  {match_icon} {lawyer['name']} - {lawyer['distance_km']}km")
                print(f"     {lawyer['specialization']}")
    else:
        print(f"\n❌ {result.get('message', 'Could not find lawyers')}")
    
    # Test 3: With custom case text (extracts location from text)
    print("\n" + "-"*40)
    print("TEST 3: Extract location from case text")
    print("-"*40)
    
    case_text = "I need a personal injury lawyer in Chicago, IL"
    print(f"Case text: '{case_text}'")
    
    # Create temp file with case text
    import os
    with open('temp_case.txt', 'w') as f:
        f.write(case_text)
    
    result = analyzer.analyze_case_file('temp_case.txt')
    os.remove('temp_case.txt')
    
    if result['success']:
        print(f"✅ Extracted location: {result['case_info']['location']}")
        print(f"✅ Case type: {result['case_info']['case_type']}")
        print(f"✅ Lawyers in Chicago: {result['results']['total_found']}")
    else:
        print(f"❌ Error: {result.get('error')}")

if __name__ == "__main__":
    main()