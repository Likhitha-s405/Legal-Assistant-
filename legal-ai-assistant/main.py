import os
from agents.planner import Planner
from agents.preprocessor import Preprocessor
from agents.summarizer import Summarizer  # NEW
from dotenv import load_dotenv  # NEW

class LegalAIAssistant:
    """
    Main orchestrator for the Legal AI Assistant
    Now includes Summarizer Agent
    """
    
    def __init__(self):
        # Load environment variables
        load_dotenv()  # NEW
        
        # Initialize agents
        self.planner = Planner()
        self.preprocessor = Preprocessor()
        self.summarizer = Summarizer()  # NEW
        
        print("=" * 60)
        print("LEGAL AI ASSISTANT - WITH SUMMARIZER")
        print("=" * 60)
        print("Using LLaMA-3 via Groq for summarization")
        print("=" * 60)
    
    def process_document(self, file_path: str):
        """
        Main pipeline to process a legal document
        """
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            return
        
        print(f"\nProcessing document: {os.path.basename(file_path)}")
        print("-" * 40)
        
        # Step 1: Planning
        print("\n[STEP 1] PLANNING")
        print("-" * 20)
        plan = self.planner.plan(file_path)
        
        if not plan.get("success"):
            print(f"Planning failed: {plan.get('error')}")
            return plan
        
        print(f"✓ Document type: {plan['document_type']}")
        print(f"✓ Agent sequence: {' → '.join(plan['agent_sequence'])}")
        print(f"✓ Next agent: {plan['next_agent']}")
        
        # Initialize results dictionary
        results = {
            "plan": plan,
            "preprocessing": None,
            "summarization": None
        }
        
        # Step 2: Execute based on plan
        print(f"\n[STEP 2] EXECUTION")
        print("-" * 20)
        
        # Track what document text we have for summarization
        document_text_for_summary = ""
        extracted_info_for_summary = {}
        
        # Check if we need preprocessor
        if plan['next_agent'] == 'preprocessor':
            print("Running Preprocessor...")
            preprocess_result = self.preprocessor.process(file_path)
            results["preprocessing"] = preprocess_result
            
            if preprocess_result.get("success"):
                print("✓ Preprocessing completed successfully!")
                
                # Extract text for summarization
                document_text_for_summary = preprocess_result.get("original_text", "")
                extracted_info_for_summary = preprocess_result.get("extracted_info", {})
                
                print(f"\nExtracted Information:")
                print("-" * 30)
                info = extracted_info_for_summary
                print(f"Case Number: {info.get('case_number', 'N/A')}")
                print(f"Court: {info.get('court_name', 'N/A')}")
                print(f"Judge: {info.get('judge_name', 'N/A')}")
                print(f"Date: {info.get('date', 'N/A')}")
                print(f"Legal Sections: {', '.join(info.get('sections_mentioned', [])[:3])}")
                
                print(f"\nDocument Statistics:")
                print(f"Word Count: {preprocess_result.get('word_count', 0)}")
                
                print(f"\nReady for next agent: SUMMARIZER")
            else:
                print(f"✗ Preprocessing failed: {preprocess_result.get('error')}")
                return results
        
        elif plan['next_agent'] == 'summarizer':
            print(f"Document type '{plan['document_type']}' detected.")
            print("Skipping preprocessor, reading document directly...")
            
            # Read document directly for summarization
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    document_text_for_summary = f.read()
                print(f"✓ Read document directly ({len(document_text_for_summary)} chars)")
            except Exception as e:
                print(f"✗ Error reading document: {e}")
                return results
        
        # Step 3: Summarization (if we have text)
        if document_text_for_summary:
            print(f"\n[STEP 3] SUMMARIZATION")
            print("-" * 20)
            print("Generating summary using LLaMA-3 via Groq...")
            
            # Prepare data for summarizer
            summarizer_data = {
                "document_type": plan['document_type'],
                "text": document_text_for_summary,
                "extracted_info": extracted_info_for_summary
            }
            
            # Call summarizer
            summary_result = self.summarizer.summarize(summarizer_data)
            results["summarization"] = summary_result
            
            if summary_result.get("success"):
                print("✓ Summarization completed successfully!")
                print(f"\nSUMMARY:")
                print("=" * 60)
                print(summary_result.get("summary", "No summary generated"))
                print("=" * 60)
                
                # Show summary statistics
                print(f"\nSummary Statistics:")
                print(f"Original length: {summary_result.get('original_length', 0)} chars")
                print(f"Summary length: {summary_result.get('summary_length', 0)} chars")
                print(f"Compression ratio: {summary_result.get('compression_ratio', 'N/A')}")
                print(f"Model used: {summary_result.get('model_used', 'N/A')}")
                
                # Show simple explanation if available
                structured = summary_result.get('structured_summary', {})
                if structured.get('simple_explanation'):
                    print(f"\nSimple Explanation:")
                    print(f"{structured['simple_explanation']}")
                
                print(f"\nReady for next agent: FORMATTER")
            else:
                print(f"✗ Summarization failed: {summary_result.get('error')}")
        
        return results


def create_sample_files():
    """Create sample legal documents for testing"""
    samples_dir = "sample_docs"
    os.makedirs(samples_dir, exist_ok=True)
    
    # Sample judgement document (more detailed)
    judgement_text = """IN THE HIGH COURT OF DELHI AT NEW DELHI

CRL.A. 1234/2023

APPELLANT: SHRI RAJESH KUMAR
VERSUS
RESPONDENT: STATE OF NCT OF DELHI

JUDGEMENT

Date: 15-12-2023

HON'BLE MR. JUSTICE A. K. SHARMA

1. The present appeal has been filed under Section 374 of the Code of Criminal Procedure, 1973 against the judgement dated 15.03.2023 passed by the Additional Sessions Judge, Delhi.

FACTS OF THE CASE:
The appellant was accused of committing offenses under Sections 420 and 468 of the Indian Penal Code, 1860. The trial court convicted the appellant and sentenced him to 3 years rigorous imprisonment with a fine of ₹50,000. The prosecution alleged that the appellant fraudulently obtained money from multiple investors by promising high returns on a real estate investment scheme.

ISSUES FOR CONSIDERATION:
1. Whether the trial court erred in appreciating the evidence?
2. Whether the conviction under Sections 420 and 468 IPC is sustainable?
3. Whether the sentence imposed is excessive?

ARGUMENTS:
Learned counsel for the appellant argued that the evidence was circumstantial and the prosecution failed to prove fraudulent intent beyond reasonable doubt. The appellant contended that it was a business failure, not fraud.

Learned APP for the State argued that the appellant knowingly made false promises to investors and misappropriated funds for personal use.

ANALYSIS:
After perusing the evidence and records, this Court finds that while the prosecution established fraudulent intent under Section 420 IPC, the evidence for forgery under Section 468 IPC is insufficient. The appellant's conduct shows clear intention to deceive investors.

DECISION:
For the reasons stated above, the appeal is partly allowed.

ORDER:
1. The conviction under Section 468 IPC is set aside.
2. The conviction under Section 420 IPC is upheld.
3. The sentence is modified to 1 year rigorous imprisonment.
4. The fine of ₹50,000 is maintained.
5. The appellant shall surrender within 4 weeks to serve the sentence.

Pronounced in open court on this 15th day of December, 2023."""
    
    # Sample bail document
    bail_text = """IN THE COURT OF THE ADDITIONAL SESSIONS JUDGE, DELHI

BAIL APPLICATION NO. 456/2023

APPLICANT: MR. AMIT SHARMA
VERSUS
STATE: NCT OF DELHI

APPLICATION FOR GRANT OF REGULAR BAIL

The applicant respectfully submits:

1. That the applicant has been falsely implicated in FIR No. 789/2023 registered at Police Station Dwarka, Delhi under Sections 406 and 420 IPC.

2. That the applicant is a law-abiding citizen with no criminal antecedents and has deep roots in society.

3. That the investigation is complete and chargesheet has been filed.

4. That the applicant is not a flight risk and will cooperate with the trial.

5. That the applicant is ready to abide by any conditions imposed by this Hon'ble Court.

GROUNDS FOR BAIL:
a) The offense alleged is triable by Magistrate and not punishable with death or life imprisonment.
b) The applicant has permanent residence and family in Delhi.
c) Custodial interrogation is not required as investigation is complete.
d) The applicant is willing to furnish surety.

LEGAL PROVISIONS:
The application is filed under Section 439 of the Code of Criminal Procedure, 1973.

PRAYER:
In view of the above, it is prayed that regular bail may be granted to the applicant on suitable terms and conditions.

VERIFICATION:
I, Amit Sharma, s/o Sh. Ramesh Sharma, do hereby verify that the contents of paragraphs 1 to 5 are true to my knowledge and I believe no part of it is false."""
    
    # Write sample files
    judgement_path = os.path.join(samples_dir, "sample_judgement.txt")
    bail_path = os.path.join(samples_dir, "sample_bail.txt")
    
    with open(judgement_path, 'w', encoding='utf-8') as f:
        f.write(judgement_text)
    
    with open(bail_path, 'w', encoding='utf-8') as f:
        f.write(bail_text)
    
    print(f"Sample files created in '{samples_dir}' folder:")
    print(f"  - {judgement_path}")
    print(f"  - {bail_path}")
    
    return [judgement_path, bail_path]


def main():
    """Main function to run the assistant"""
    assistant = LegalAIAssistant()
    
    # Create sample documents for testing
    sample_files = create_sample_files()
    
    # Test with sample documents
    for file_path in sample_files:
        print("\n" + "=" * 60)
        print(f"PROCESSING: {os.path.basename(file_path)}")
        print("=" * 60)
        
        result = assistant.process_document(file_path)
        
        # Wait for user to continue
        if file_path != sample_files[-1]:
            input("\nPress Enter to process next document...")


if __name__ == "__main__":
    main()