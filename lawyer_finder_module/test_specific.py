# test_specific.py - Test with your specific input
from __init__ import LegalCaseAnalyzer

analyzer = LegalCaseAnalyzer()
analyzer.lawyer_finder.add_sample_data()

# Your specific case text
case_text = """
injury of jumana from cet, new york
"""

print("="*60)
print("TESTING WITH YOUR INPUT")
print("="*60)
print(f"Input text: {case_text}")

# Create temp file
with open('temp_test.txt', 'w') as f:
    f.write(case_text)

# Analyze
result = analyzer.analyze_case_file('temp_test.txt')

print("\nRESULTS:")
print(f"Success: {result['success']}")
print(f"Case Type: {result['case_info']['case_type']}")
print(f"Location: {result['case_info']['location']}")

# Show what the parser extracted
from case_parser import CaseParser
parser = CaseParser()
lat, lng, location = parser.extract_location(case_text)
print(f"\nParser extracted location: {location}")

# Clean up
import os
os.remove('temp_test.txt')