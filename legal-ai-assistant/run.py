#!/usr/bin/env python3
"""
Simple runner for the Legal AI Assistant
"""

from main import LegalAIAssistant
import sys
import os

def run_with_custom_file():
    """Run assistant with a custom file provided by user"""
    assistant = LegalAIAssistant()
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if os.path.exists(file_path):
            print(f"\nProcessing custom file: {file_path}")
            assistant.process_document(file_path)
        else:
            print(f"File not found: {file_path}")
    else:
        print("Usage: python run.py <path_to_legal_document>")
        print("\nExample: python run.py my_judgement.txt")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_with_custom_file()
    else:
        # Run with sample files
        from main import main
        main()