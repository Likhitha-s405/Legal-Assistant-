from typing import Dict, Any
from . import detect_document_type

class Planner:
    """
    Simple planner that decides which agents to run based on document type
    """
    
    def __init__(self):
        self.name = "Planner"
        self.agent_sequence = {
            "judgement": ["preprocessor", "summarizer", "formatter"],
            "bail": ["summarizer", "formatter"],  # Skip preprocessor for bail
            "unknown": ["preprocessor", "summarizer", "formatter"]  # Default
        }
    
    def plan(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze the document and create execution plan
        Returns: Plan with sequence of agents to run
        """
        print(f"[Planner] Analyzing document: {file_path}")
        
        try:
            # Step 1: Detect document type
            doc_type = detect_document_type(file_path)
            print(f"[Planner] Detected document type: {doc_type}")
            
            # Step 2: Determine agent sequence
            sequence = self.agent_sequence.get(doc_type, self.agent_sequence["unknown"])
            
            # Step 3: Create plan
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
        """Get notes about how to process this document type"""
        notes = {
            "judgement": "Judgement detected. Will preprocess to extract structure, then summarize.",
            "bail": "Bail document detected. Skipping preprocessing, going directly to summarization.",
            "unknown": "Document type not recognized. Will attempt preprocessing and summarization."
        }
        return notes.get(doc_type, "No specific notes.")