import sys
import os
from pathlib import Path

# Add parent directory to path (though not needed if running from current dir)
sys.path.insert(0, str(Path(__file__).parent))

# Import from the current module (folder name)
from lawyer_finder_module import LegalCaseAnalyzer

def test_module():
    print("="*60)
    print("TESTING LAWYER FINDER MODULE")
    print("="*60)
    print(f"Current directory: {os.getcwd()}")
    
    # Initialize
    print("\n1. Initializing analyzer...")
    analyzer = LegalCaseAnalyzer()
    
    # Add sample data
    print("2. Adding sample lawyers...")
    analyzer.lawyer_finder.add_sample_data()
    
    # Create a sample case file
    print("3. Creating sample case file...")
    test_file = os.path.join(os.path.dirname(__file__), 'test_case.txt')
    with open(test_file, 'w') as f:
        f.write("""
CASE FILE: Johnson Divorce Case
DATE: January 15, 2024
LOCATION: New York, NY

This is a divorce proceeding filed in New York, NY. The petitioner
is seeking dissolution of marriage on grounds of irreconcilable differences.
The parties have been married for 10 years and have two minor children.
Issues include child custody, child support, and division of marital assets.
        """)
    
    # Test the module
    print("4. Analyzing case file...")
    result = analyzer.analyze_case_file(test_file)
    
    if result['success']:
        print("\n✅ ANALYSIS RESULTS:")
        print(f"   Case Type: {result['case_info']['case_type']}")
        print(f"   Location: {result['case_info']['location']}")
        print(f"   Lawyers Found: {result['results']['total_found']}")
        
        print("\n📋 RECOMMENDED LAWYERS:")
        for i, lawyer in enumerate(result['results']['lawyers'], 1):
            match = "🎯 EXACT MATCH" if lawyer.get('exact_match') else ""
            print(f"\n{i}. {lawyer['name']} {match}")
            print(f"   Firm: {lawyer['firm_name']}")
            print(f"   Specialization: {lawyer['specialization']}")
            print(f"   Distance: {lawyer['distance_km']} km")
            print(f"   Phone: {lawyer['phone']}")
    else:
        print(f"\n❌ ERROR: {result.get('error')}")
    
    # Clean up
    print("\n5. Cleaning up...")
    if os.path.exists(test_file):
        os.remove(test_file)
    
    print("\n✅ Test completed!")

if __name__ == "__main__":
    test_module()