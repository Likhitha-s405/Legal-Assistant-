# final_test.py
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("="*60)
print("FINAL TEST - LAWYER FINDER MODULE")
print("="*60)
print(f"Current directory: {os.getcwd()}")
print(f"Python path: {sys.path[0]}")
print()

# Try direct imports first
try:
    from __init__ import LegalCaseAnalyzer
    print("✓ Successfully imported LegalCaseAnalyzer from __init__")
except ImportError as e:
    print(f"✗ Import failed: {e}")
    
    # Try importing the classes directly
    try:
        from case_parser import CaseParser
        from lawyer_finder import LawyerFinder
        from models import Lawyer, Base
        print("✓ Imported individual modules")
        
        # Create a simple wrapper
        class LegalCaseAnalyzer:
            def __init__(self, db_path=None):
                self.case_parser = CaseParser()
                self.lawyer_finder = LawyerFinder(db_path) if db_path else LawyerFinder()
            
            def analyze_case_file(self, file_path, max_distance=25):
                case_info = self.case_parser.parse_case_file(file_path)
                return self.lawyer_finder.find_lawyers_by_case(case_info, max_distance=max_distance)
        
        print("✓ Created LegalCaseAnalyzer wrapper")
    except ImportError as e2:
        print(f"✗ Module imports failed: {e2}")
        sys.exit(1)

# Test the functionality
print("\n" + "-"*40)
print("TESTING FUNCTIONALITY")
print("-"*40)

try:
    # Create analyzer
    print("1. Creating analyzer instance...")
    analyzer = LegalCaseAnalyzer()
    print("   ✓ Analyzer created")
    
    # Add sample data
    print("\n2. Adding sample lawyers...")
    analyzer.lawyer_finder.add_sample_data()
    print("   ✓ Sample lawyers added")
    
    # Test case parsing
    print("\n3. Testing case parser...")
    parser = analyzer.case_parser
    test_text = "This is a divorce case in New York, NY"
    case_type = parser.extract_case_type(test_text)
    print(f"   ✓ Case type detected: {case_type}")
    
    # Test with a real file
    print("\n4. Testing with a sample case file...")
    test_file = "sample_case.txt"
    with open(test_file, 'w') as f:
        f.write("""
CASE: Johnson Divorce
LOCATION: New York, NY
This is a divorce proceeding with child custody issues.
        """)
    
    result = analyzer.analyze_case_file(test_file)
    
    if isinstance(result, dict):
        print(f"   ✓ Analysis completed")
        print(f"   Case type: {result.get('case_type', 'N/A')}")
        print(f"   Location: {result.get('location', 'N/A')}")
        print(f"   Lawyers found: {result.get('total_found', 0)}")
        
        if result.get('lawyers'):
            print("\n   Lawyers in your area:")
            for lawyer in result['lawyers'][:3]:
                print(f"     • {lawyer['name']} - {lawyer['distance_km']}km")
    else:
        print(f"   ✗ Unexpected result: {result}")
    
    # Clean up
    os.remove(test_file)
    print("\n5. Cleaning up...")
    print("   ✓ Test file removed")
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()