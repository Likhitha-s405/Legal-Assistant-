# interactive_test.py - Interactive testing with proper error handling
from __init__ import LegalCaseAnalyzer
import os

def main():
    print("="*60)
    print("INTERACTIVE LAWYER FINDER TEST")
    print("="*60)
    
    # Initialize
    analyzer = LegalCaseAnalyzer()
    analyzer.lawyer_finder.add_sample_data()
    
    while True:
        print("\n" + "-"*40)
        print("1. Test with sample case")
        print("2. Enter custom case text")
        print("3. Test with a file")
        print("4. Search lawyers by specialization")
        print("5. Exit")
        print("-"*40)
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            # Sample case
            case_text = """
CASE: Johnson Divorce
LOCATION: New York, NY
This is a divorce case with child custody issues.
            """
            filename = "interactive_test.txt"
            with open(filename, 'w') as f:
                f.write(case_text)
            
            result = analyzer.analyze_case_file(filename)
            os.remove(filename)
            
            display_results(result)
            
        elif choice == '2':
            # Custom text
            print("\nEnter your case text (type 'END' on a new line to finish):")
            lines = []
            while True:
                line = input()
                if line == 'END':
                    break
                lines.append(line)
            
            case_text = "\n".join(lines)
            if not case_text.strip():
                print("No text entered. Returning to menu.")
                continue
                
            filename = "custom_test.txt"
            with open(filename, 'w') as f:
                f.write(case_text)
            
            result = analyzer.analyze_case_file(filename)
            os.remove(filename)
            
            display_results(result)
            
        elif choice == '3':
            # Test with file
            filepath = input("Enter file path: ").strip()
            if os.path.exists(filepath):
                result = analyzer.analyze_case_file(filepath)
                display_results(result)
            else:
                print(f"File not found: {filepath}")
                
        elif choice == '4':
            # Search by specialization
            spec = input("Enter specialization (e.g., divorce, criminal, etc.): ").strip()
            lawyers = analyzer.search_lawyers(specialization=spec)
            if lawyers:
                print(f"\nFound {len(lawyers)} lawyers specializing in {spec}:")
                for lawyer in lawyers[:5]:
                    print(f"  • {lawyer['name']} - {lawyer['firm_name']} - {lawyer['city']}, {lawyer['state']}")
            else:
                print(f"No lawyers found with specialization: {spec}")
                
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def display_results(result):
    """Display results with proper handling of different response formats"""
    
    if not result.get('success', False):
        print(f"\n❌ ERROR: {result.get('error', 'Unknown error')}")
        return
    
    print("\n✅ ANALYSIS RESULTS:")
    print(f"   Case Type: {result['case_info']['case_type']}")
    print(f"   Location: {result['case_info']['location']}")
    
    # Handle different response structures
    results_data = result.get('results', {})
    
    if isinstance(results_data, dict):
        # Check if it's the location_not_found response
        if results_data.get('status') == 'location_not_found':
            print(f"   ⚠️  {results_data.get('message', 'Location not found')}")
            recommendations = results_data.get('recommendations', [])
            if recommendations:
                print(f"\n📋 RECOMMENDED LAWYERS (by specialization):")
                for i, lawyer in enumerate(recommendations[:5], 1):
                    print(f"\n{i}. {lawyer['name']}")
                    print(f"   Firm: {lawyer['firm_name']}")
                    print(f"   Specialization: {lawyer['specialization']}")
                    print(f"   Location: {lawyer['city']}, {lawyer['state']}")
                    print(f"   Phone: {lawyer['phone']}")
            return
        
        # Regular success response
        lawyers_found = results_data.get('total_found', 0)
        print(f"   Lawyers Found: {lawyers_found}")
        
        lawyers = results_data.get('lawyers', [])
        if lawyers:
            print("\n📋 RECOMMENDED LAWYERS:")
            for i, lawyer in enumerate(lawyers, 1):
                match = "🎯 EXACT MATCH" if lawyer.get('exact_match') else ""
                print(f"\n{i}. {lawyer['name']} {match}")
                print(f"   Firm: {lawyer['firm_name']}")
                print(f"   Specialization: {lawyer['specialization']}")
                print(f"   Distance: {lawyer.get('distance_km', 'N/A')} km")
                print(f"   Phone: {lawyer.get('phone', 'N/A')}")
                print(f"   Email: {lawyer.get('email', 'N/A')}")
        else:
            print("\n   No lawyers found in this area.")
    else:
        print(f"   Unexpected result format: {results_data}")

if __name__ == "__main__":
    main()