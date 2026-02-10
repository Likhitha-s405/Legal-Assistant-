"""
Helper functions for document detection and type identification
"""

from .preprocessor import Preprocessor


def detect_document_type(file_path):
    """
    Detect if uploaded document is judgement, bail, or other legal document
    Returns: 'judgement', 'bail', or 'unknown'
    """
    try:
        preprocessor = Preprocessor()
        text = preprocessor.extract_text_from_file(file_path)

        if not text:
            return "unknown"

        text_lower = text.lower()

        # Bail keywords (higher priority)
        bail_keywords = [
            'bail application', 'regular bail', 'anticipatory bail',
            'interim bail', 'bail petition', 'bail under section',
            'grant of bail', 'prayer for bail'
        ]

        for keyword in bail_keywords:
            if keyword in text_lower:
                return "bail"

        # Judgement keywords
        judgement_keywords = [
            'judgement', 'judgment', 'verdict', 'court order',
            'in the matter of', 'case no.', 'crl.a.', 'criminal appeal',
            'civil appeal', 'writ petition'
        ]

        for keyword in judgement_keywords:
            if keyword in text_lower:
                return "judgement"

        return "unknown"

    except Exception as e:
        print(f"Error detecting document type: {e}")
        return "unknown"


def get_file_extension(file_path):
    """Get file extension from path"""
    import os
    return os.path.splitext(file_path)[1].lower()
