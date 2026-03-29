from .preprocessor import Preprocessor


def detect_document_type(file_path):
    try:
        preprocessor = Preprocessor()
        text = preprocessor.extract_text_from_file(file_path)

        # 1. Immediate rejection for short/empty files
        if not text or len(text.strip()) < 300: # Threshold increased for better accuracy
            return "non-legal"

        text_lower = text.lower()
        
        # 2. Scoring system instead of immediate return
        bail_keywords = ['bail','bail application', 'regular bail', 'anticipatory bail', 'interim bail', 'bail order', 'bail hearing', 'bail petition']
        judgement_keywords = ['judgement', 'judgment', 'verdict', 'court order', 'crl.a.']

        bail_score = sum(1 for k in bail_keywords if k in text_lower)
        judgement_score = sum(1 for k in judgement_keywords if k in text_lower)

        # 3. Decision logic
        if bail_score > 0 and bail_score >= judgement_score:
            return "bail"
        if judgement_score > 0:
            return "judgement"
            
        return "non-legal" # If no legal markers are found, it's non-legal

    except Exception as e:
        print(f"Error: {e}")
        return "non-legal"