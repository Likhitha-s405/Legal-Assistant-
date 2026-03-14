# minimal_test.py
import sys
import os

print("="*60)
print("MINIMAL TEST FOR LAWYER FINDER")
print("="*60)

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print(f"Current directory: {current_dir}")
print(f"Files in directory: {[f for f in os.listdir('.') if f.endswith('.py')]}")
print()

# Try different import methods
try:
    # Method 1: Import from current directory
    from __init__ import LegalCaseAnalyzer
    print("✓ Method 1: Imported from __init__.py")
except ImportError as e1:
    print(f"✗ Method 1 failed: {e1}")
    
    try:
        # Method 2: Import specific file
        import importlib.util
        spec = importlib.util.spec_from_file_location("core", os.path.join(current_dir, "__init__.py"))
        core = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(core)
        LegalCaseAnalyzer = core.LegalCaseAnalyzer
        print("✓ Method 2: Dynamic import successful")
    except Exception as e2:
        print(f"✗ Method 2 failed: {e2}")
        
        try:
            # Method 3: Direct file import
            from lawyer_finder import LegalCaseAnalyzer
            print("✓ Method 3: Imported from lawyer_finder.py")
        except ImportError as e3:
            print(f"✗ Method 3 failed: {e3}")
            sys.exit(1)

# Now test the functionality
print("\n" + "-"*40)
print("TESTING FUNCTIONALITY")
print("-"*40)

try:
    # Create analyzer
    print("Creating analyzer instance...")
    analyzer = LegalCaseAnalyzer()
    print("✓ Analyzer created")
    
    # Add sample data
    print("\nAdding sample lawyers...")
    analyzer.lawyer_finder.add_sample_data()
    print("✓ Sample lawyers added")
    
    # Create a test case
    test_file = "test.txt"
    with open(test_file, 'w') as f:
        f.write("""
CASE: Smith Divorce
LOCATION: New York, NY
This is a divorce case with child custody issues.
        """)
    
    # Analyze
    print("\nAnalyzing case file...")
    result = analyzer.analyze_case_file(test_file)
    
    if result['success']:
        print("✓ Analysis successful")
        print(f"  Case type: {result['case_info']['case_type']}")
        print(f"  Location: {result['case_info']['location']}")
        print(f"  Lawyers found: {result['results']['total_found']}")
        
        if result['results'].get('lawyers'):
            print("\nLawyers:")
            for lawyer in result['results']['lawyers'][:3]:
                print(f"  • {lawyer['name']} - {lawyer['distance_km']}km")
    else:
        print(f"✗ Analysis failed: {result.get('error')}")
    
    # Clean up
    os.remove(test_file)
    print("\n✓ Test completed")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()