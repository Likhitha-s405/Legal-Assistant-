#!/usr/bin/env python3
"""
Test script for the Summarizer Agent
"""

import os
from dotenv import load_dotenv
from agents.summarizer import Summarizer

def test_summarizer():
    """Test the summarizer with sample text"""
    
    # Load environment
    load_dotenv()
    
    # Check if API key is available
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("ERROR: GROQ_API_KEY not found in .env file")
        print("Please create a .env file with: GROQ_API_KEY=your_key_here")
        return
    
    print("Testing Summarizer Agent...")
    print(f"API Key found: {'*' * 10}{api_key[-4:]}")
    
    # Create summarizer
    try:
        summarizer = Summarizer()
        print("Summarizer initialized successfully!")
    except Exception as e:
        print(f"Failed to initialize summarizer: {e}")
        return
    
    # Test with sample text
    sample_text = """
    IN THE SUPREME COURT OF INDIA
    Criminal Appeal No. 123 of 2023
    
    The appellant was convicted under Section 302 IPC for murder and sentenced to life imprisonment.
    The High Court upheld the conviction. The appellant appeals to the Supreme Court claiming 
    the evidence is purely circumstantial. The prosecution argues that the chain of circumstances 
    conclusively proves guilt. After examining the evidence, this Court finds that while most 
    circumstances are proven, one critical link in the chain is missing. Therefore, benefit of 
    doubt must be given to the appellant.
    
    HELD: The appeal is allowed. The conviction is set aside. The appellant is acquitted of all 
    charges and directed to be released forthwith if not required in any other case.
    """
    
    print("\n" + "=" * 60)
    print("TESTING WITH SAMPLE JUDGEMENT TEXT")
    print("=" * 60)
    
    try:
        result = summarizer.summarize({
            "document_type": "judgement",
            "text": sample_text,
            "extracted_info": {
                "case_number": "Criminal Appeal No. 123/2023",
                "court_name": "Supreme Court of India",
                "judge_name": "Not specified",
                "date": "Not specified"
            }
        })
        
        if result["success"]:
            print("\n✓ SUMMARY GENERATED SUCCESSFULLY")
            print("=" * 60)
            print(result["summary"])
            print("=" * 60)
            print(f"\nStatistics:")
            print(f"Original length: {result['original_length']} chars")
            print(f"Summary length: {result['summary_length']} chars")
            print(f"Compression: {result['compression_ratio']}")
        else:
            print(f"\n✗ FAILED: {result.get('error')}")
            
    except Exception as e:
        print(f"\n✗ EXCEPTION: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_summarizer()