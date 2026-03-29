#!/usr/bin/env python3
# drafter_cli.py

import os
import sys
from drafter.drafter import Drafter

def main():
    # If you want to accept agreement type as command line argument
    agreement_type = input("Enter agreement type (residential_lease/commercial_lease/nda): ").strip()
    
    # Initial request
    user_request = {'agreement_type': agreement_type}
    
    drafter = Drafter()
    result = drafter.draft(user_request)
    
    if result['success']:
        # Save PDF to file
        filename = f"{agreement_type}_{result['inputs'].get('lessee_name', 'output')}.pdf"
        with open(filename, 'wb') as f:
            f.write(result['pdf'])
        print(f"\n✅ PDF generated: {filename}")
        
        # Optionally print preview of clauses
        print("\n--- Clauses Generated ---")
        for clause in result['clauses']:
            print(f"{clause['title']}: {clause['text'][:80]}...")
    else:
        print("❌ Drafting failed.")

if __name__ == "__main__":
    main()