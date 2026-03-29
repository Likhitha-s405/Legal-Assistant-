import os
import tempfile
import base64
import asyncio
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from summarizer.planner import Planner
from summarizer.preprocessor import Preprocessor
from summarizer.summarizer import Summarizer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to import drafter
try:
    from drafter.drafter import Drafter
    drafter = Drafter()
    print("✓ Drafter module loaded successfully")
except Exception as e:
    print(f"⚠️ Drafter module failed to load: {e}")
    drafter = None

# Create FastAPI app
app = FastAPI(title="Legal AI Assistant")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


# ===================================================
# API ENDPOINTS
# ===================================================

@app.get("/")
def health():
    """Health check endpoint"""
    return {"status": "Legal AI Assistant running"}


@app.get("/test")
def test():
    """Simple test endpoint to verify API is working"""
    return {"message": "API is working!", "status": "online"}


@app.get("/api/health")
def api_health():
    """Detailed health check for frontend"""
    return {
        "status": "healthy",
        "summarizer_loaded": True,
        "version": "1.0.0"
    }


@app.get("/api/case-types")
def get_case_types():
    """Return available case types for lawyer search"""
    return {
        "case_types": [
            {"id": "divorce", "name": "Divorce / Family Law"},
            {"id": "personal_injury", "name": "Personal Injury"},
            {"id": "criminal", "name": "Criminal Defense"},
            {"id": "immigration", "name": "Immigration"},
            {"id": "business", "name": "Business Law"},
            {"id": "contract", "name": "Contract Dispute"},
            {"id": "general", "name": "General Legal"}
        ]
    }


@app.post("/api/summarize")
async def summarize_document(file: UploadFile = File(...)):
    """
    API endpoint for frontend to upload file and get summary
    """
    # Save uploaded file temporarily
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, file.filename)
    
    try:
        # Save file
        content = await file.read()
        with open(temp_path, 'wb') as f:
            f.write(content)
        
        # Process with your existing assistant
        result = await asyncio.to_thread(assistant.process_document, temp_path)
        
        # Clean up
        os.remove(temp_path)
        
        # Return formatted response for frontend
        if result.get("success") is False:
            return {"success": False, "error": result.get("error")}
        
        # Extract summary from result
        summary = ""
        if result.get("summarization") and result["summarization"].get("success"):
            summary = result["summarization"].get("summary", "")
        elif result.get("summarization"):
            summary = result["summarization"].get("summary", "Summary generated")
        
        return {
            "success": True,
            "summary": summary,
            "document_type": result.get("plan", {}).get("document_type", "Unknown"),
            "processing_time": result.get("summarization", {}).get("processing_time", 0)
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}


@app.post("/api/draft")
async def draft_document(
    agreement_type: str = "residential_lease",
    lessor_name: str = "",
    lessee_name: str = "",
    property_address: str = "",
    city: str = "",
    term_months: str = "11",
    start_date: str = "01 January 2025",
    rent_amount: str = "10000",
    rent_due_day: str = "5",
    grace_period: str = "5",
    late_interest_rate: str = "18",
    deposit_amount: str = "50000",
    north_boundary: str = "",
    south_boundary: str = "",
    east_boundary: str = "",
    west_boundary: str = "",
    default_days: str = "10",
    cure_days: str = "15",
    abandonment_days: str = "30",
    negotiation_days: str = "30",
    arbitration_city: str = "Bangalore",
    jurisdiction_city: str = "Bangalore",
    special_terms: str = ""
):
    """
    Draft a legal document using the drafter module
    """
    import base64
    
    # Build user request for drafter
    user_request = {
        'agreement_type': agreement_type,
        'lessor_name': lessor_name,
        'lessee_name': lessee_name,
        'property_address': property_address,
        'city': city,
        'term_months': term_months,
        'start_date': start_date,
        'rent_amount': rent_amount,
        'rent_due_day': rent_due_day,
        'grace_period': grace_period,
        'late_interest_rate': late_interest_rate,
        'deposit_amount': deposit_amount,
        'north_boundary': north_boundary,
        'south_boundary': south_boundary,
        'east_boundary': east_boundary,
        'west_boundary': west_boundary,
        'default_days': default_days,
        'cure_days': cure_days,
        'abandonment_days': abandonment_days,
        'negotiation_days': negotiation_days,
        'arbitration_city': arbitration_city,
        'jurisdiction_city': jurisdiction_city,
        'special_terms': special_terms
    }
    
    try:
        if drafter is None:
            return {"success": False, "error": "Drafter module not available"}
        
        result = drafter.draft(user_request)
        
        if result['success']:
            pdf_base64 = base64.b64encode(result['pdf']).decode('utf-8')
            
            # Create text preview
            text_preview = "\n\n".join([
                f"{clause['title']}\n{clause['text'][:500]}..." 
                for clause in result.get('clauses', [])[:5]
            ])
            
            return {
                "success": True,
                "draft": text_preview,
                "pdf_base64": pdf_base64,
                "filename": f"{agreement_type}_{lessee_name}.pdf",
                "clauses_count": len(result.get('clauses', [])),
                "message": "Draft generated successfully"
            }
        else:
            return {"success": False, "error": result.get('error', 'Drafting failed')}
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}

@app.post("/process")
def process_document_api(file_path: str):
    """
    Original API endpoint to process a legal document by file path
    """
    result = assistant.process_document(file_path)
    return result