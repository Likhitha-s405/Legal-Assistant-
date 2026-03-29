from typing import Dict, Any
from . import detect_document_type

class Planner:
    """
    Simple planner that decides which agents to run based on document type.
    Rejects non‑legal files with an error.
    """
    
    def __init__(self):
        self.name = "Planner"
        self.agent_sequence = {
            "judgement": ["preprocessor", "summarizer", "formatter"],
            "bail": ["preprocessor","summarizer", "formatter"],   
            "unknown": ["preprocessor", "summarizer", "formatter"]  
        }
    
    def plan(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze the document and create execution plan.
        Returns a dict with success flag, agent sequence, or error.
        """
        print(f"[Planner] Analyzing document: {file_path}")
        
        try:
            # Step 1: Detect document type
            doc_type = detect_document_type(file_path)
            print(f"[Planner] Detected document type: {doc_type}")
            
            # Step 2: Reject non‑legal files
            if doc_type == "non-legal":
                return {
                    "success": False,
                    "error": "The uploaded file does not appear to be a legal document. Please upload a valid judgement or bail application.",
                    "file_path": file_path,
                    "document_type": doc_type,
                    "agent_sequence": [],
                    "next_agent": None
                }
            
            # Step 3: Determine agent sequence
            sequence = self.agent_sequence.get(doc_type, self.agent_sequence["unknown"])
            
            # Step 4: Create plan
            plan = {
                "success": True,
                "file_path": file_path,
                "document_type": doc_type,
                "agent_sequence": sequence,
                "next_agent": sequence[0] if sequence else None,
                "notes": self._get_notes_for_doc_type(doc_type)
            }
            
            print(f"[Planner] Plan created: {plan}")
            return plan
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Planning error: {str(e)}",
                "file_path": file_path,
                "document_type": "unknown",
                "agent_sequence": [],
                "next_agent": None
            }
    
    def _get_notes_for_doc_type(self, doc_type: str) -> str:
        """Get processing notes for the document type"""
        notes = {
            "judgement": "Judgement detected. Will run full preprocessing, summarization, and formatting.",
            "bail": "Bail document detected. Will run preprocessing, summarization, and formatting.",
            "unknown": "Document type not fully recognized. Will attempt preprocessing and summarization.",
            "non-legal": "Document rejected because it does not contain legal content."
        }
        return notes.get(doc_type, "No specific notes.")