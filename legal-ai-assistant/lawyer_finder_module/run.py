import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Now try to import
try:
    from __init__ import LegalCaseAnalyzer
    print("✓ Imported from __init__")
except ImportError:
    try:
        from lawyer_finder_module import LegalCaseAnalyzer
        print("✓ Imported from lawyer_finder_module")
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        print(f"Files in directory: {os.listdir('.')}")
        sys.exit(1)

# Run the test
print("="*60)
print("TESTING LAWYER FINDER MODULE")
print("="*60)

# Initialize
print("\n1. Initializing analyzer...")
analyzer = LegalCaseAnalyzer()

# Add sample data
print("2. Adding sample lawyers...")
analyzer.lawyer_finder.add_sample_data()

# Create a sample case file
print("3. Creating sample case file...")
with open('test_case.txt', 'w') as f:
    f.write("""
CASE FILE: Johnson Divorce Case
LOCATION: New York, NY
This is a divorce case.
    """)

# Test the module
print("4. Analyzing case file...")
result = analyzer.analyze_case_file('test_case.txt')

if result['success']:
    print("\n✅ SUCCESS!")
    print(f"   Case Type: {result['case_info']['case_type']}")
    print(f"   Location: {result['case_info']['location']}")
    print(f"   Lawyers Found: {result['results']['total_found']}")
else:
    print(f"\n❌ ERROR: {result.get('error')}")

# Clean up
os.remove('test_case.txt')
print("\n✅ Test completed!")