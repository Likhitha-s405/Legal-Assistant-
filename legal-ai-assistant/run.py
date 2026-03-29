#!/usr/bin/env python3
"""
Simple runner for the Legal AI Assistant
"""

from summarizer_main import LegalAIAssistant
import sys
import os

def run_with_custom_file():
    assistant = LegalAIAssistant()
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if os.path.exists(file_path):
            print(f"\nProcessing custom file: {file_path}")
            result = assistant.process_document(file_path)

            print("\n" + "=" * 60)
            print("RESULTS")
            print("=" * 60)

            if not result.get("success", True):
                print(f"❌ Error: {result.get('error')}")
                return

            # Print extracted info
            preprocessing = result.get("preprocessing", {})
            if preprocessing and preprocessing.get("success"):
                info = preprocessing.get("extracted_info", {})
                print(f"\n📋 DOCUMENT INFO:")
                for key, value in info.items():
                    print(f"  {key}: {value}")

            # Print summary
            summarization = result.get("summarization", {})
            if summarization and summarization.get("success"):
                print(f"\n📝 SUMMARY:")
                print(summarization.get("summary", "No summary generated"))
            else:
                print(f"\n❌ Summarization failed: {summarization.get('error') if summarization else 'No result'}")

        else:
            print(f"File not found: {file_path}")
    else:
        print("Usage: python run.py <path_to_legal_document>")

        
if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_with_custom_file()
    else:
        # Run with sample files
        from summarizer_main import main
        main()