# test_cases.py - Test different case types
from __init__ import LegalCaseAnalyzer

def test_case(analyzer, case_text, case_name):
    print(f"\n{'='*50}")
    print(f"TESTING: {case_name}")
    print('='*50)
    
    # Create a temporary file
    filename = f"temp_{case_name.lower().replace(' ', '_')}.txt"
    with open(filename, 'w') as f:
        f.write(case_text)
    
    # Analyze
    result = analyzer.analyze_case_file(filename)
    
    if result['success']:
        print(f"✓ Case Type Detected: {result['case_info']['case_type']}")
        print(f"✓ Location Detected: {result['case_info']['location']}")
        print(f"✓ Lawyers Found: {result['results']['total_found']}")
        
        if result['results'].get('lawyers'):
            print("\nTop 3 lawyers:")
            for i, lawyer in enumerate(result['results']['lawyers'][:3], 1):
                print(f"  {i}. {lawyer['name']} - {lawyer['specialization']} - {lawyer['distance_km']}km")
    else:
        print(f"✗ Error: {result.get('error')}")
    
    # Clean up
    import os
    os.remove(filename)

# Initialize analyzer
print("Initializing Legal Case Analyzer...")
analyzer = LegalCaseAnalyzer()

# Add sample data
print("Adding sample lawyers...")
analyzer.lawyer_finder.add_sample_data()

# Test Case 1: Divorce
test_case(analyzer, """
CASE: Johnson vs Smith
COURT: Family Court
LOCATION: New York, NY

This is a divorce proceeding. The parties were married for 10 years 
and have two minor children. Issues include child custody and support.
""", "Divorce Case")

# Test Case 2: Personal Injury
test_case(analyzer, """
CASE: Martinez vs City Bus Company
COURT: Superior Court
LOCATION: Los Angeles, CA

Personal injury claim arising from a bus accident. Plaintiff suffered 
broken leg and medical expenses. Seeking compensation for damages.
""", "Personal Injury")

# Test Case 3: Criminal Defense
test_case(analyzer, """
CASE: State vs Williams
COURT: Criminal Court
LOCATION: Chicago, IL

Defendant charged with theft and assault. Seeking criminal defense 
representation for trial.
""", "Criminal Defense")

# Test Case 4: Immigration
test_case(analyzer, """
CASE: Patel Green Card Application
LOCATION: Houston, TX

Client seeking immigration assistance for green card application 
based on employment. Need help with visa processing.
""", "Immigration")

print("\n✅ All tests completed!")