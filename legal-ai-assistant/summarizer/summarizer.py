from email.mime import text

from .summarizer_service import LongDocSummarizer
import asyncio

class Summarizer:
    """
    Main Agent that coordinates with Module A and Module C.
    """
    def __init__(self):
        self.processor = LongDocSummarizer()

    def summarize(self, document_data: dict):
        text = document_data.get('text') or document_data.get('original_text')
    # Retrieve the doc_type from the planner's output
        doc_type = document_data.get('document_type', 'judgement') 
    
        if not text:
            return {"success": False, "error": "No text provided"}

        print(f"[Summarizer] Starting {doc_type} processing...")
    
        try:
            summary = asyncio.run(self.processor.summarize(text, doc_type))
        except Exception as e:
            print(f"[Summarizer] Error during summarization: {e}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": str(e)}


        return {
            "success": True,
            "summary": summary,
            "model_used": "Fine-Tuned Llama-3 (via Colab)"
        }