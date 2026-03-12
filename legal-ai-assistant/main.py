import os
from fastapi import FastAPI
from summarizer.planner import Planner
from summarizer.preprocessor import Preprocessor
from summarizer.summarizer import Summarizer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(title="Legal AI Assistant")

class LegalAIAssistant:
    """
    Main orchestrator for the Legal AI Assistant
    """

    def __init__(self):

        # Initialize agents
        self.planner = Planner()
        self.preprocessor = Preprocessor()
        self.summarizer = Summarizer()

        print("=" * 60)
        print("LEGAL AI ASSISTANT - WITH SUMMARIZER")
        print("=" * 60)
        print("Fine-Tuned Llama-3 (10k+ Data) via Colab API")
        print("=" * 60)

    def process_document(self, file_path: str):

        if not os.path.exists(file_path):
            return {"success": False, "error": "File not found"}

        # STEP 1: Planning
        plan = self.planner.plan(file_path)

        if not plan.get("success"):
            return {"success": False, "error": plan.get("error")}

        results = {
            "plan": plan,
            "preprocessing": None,
            "summarization": None
        }

        document_text_for_summary = ""
        extracted_info_for_summary = {}

        # STEP 2: Preprocessing
        if plan['next_agent'] == 'preprocessor':

            preprocess_result = self.preprocessor.process(file_path)
            results["preprocessing"] = preprocess_result

            if preprocess_result.get("success"):
                document_text_for_summary = preprocess_result.get("original_text", "")
                extracted_info_for_summary = preprocess_result.get("extracted_info", {})
            else:
                return results

        elif plan['next_agent'] == 'summarizer':

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    document_text_for_summary = f.read()
            except Exception as e:
                return {"success": False, "error": str(e)}

        # STEP 3: Summarization
        if document_text_for_summary:

            summarizer_data = {
                "document_type": plan['document_type'],
                "text": document_text_for_summary,
                "extracted_info": extracted_info_for_summary
            }

            summary_result = self.summarizer.summarize(summarizer_data)
            results["summarization"] = summary_result

        return results


# Initialize assistant
assistant = LegalAIAssistant()


# ---------------------------------------------------
# Health check endpoint (REQUIRED for Render)
# ---------------------------------------------------

@app.get("/")
def health():
    return {"status": "Legal AI Assistant running"}


# ---------------------------------------------------
# API endpoint to process a document
# ---------------------------------------------------

@app.post("/process")
def process_document_api(file_path: str):
    """
    API endpoint to process a legal document
    """
    result = assistant.process_document(file_path)
    return result