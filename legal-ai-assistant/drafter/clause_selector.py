# drafter/clause_selector.py

import json
import os

class ClauseSelector:
    """Loads clause templates from a JSON database and fills placeholders."""
    
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.path.join(os.path.dirname(__file__), 'clause_db.json')
        with open(db_path, 'r', encoding='utf-8') as f:
            self.db = json.load(f)
    
    def select_clauses(self, required_clauses, user_inputs):
        """Return list of filled clause texts in order."""
        filled = []
        for clause_id in required_clauses:
            template = self.db.get(clause_id)
            if not template:
                continue
            text = template['text']
            # Replace placeholders like [lessor_name]
            for key, value in user_inputs.items():
                placeholder = f'[{key}]'
                if placeholder in text:
                    text = text.replace(placeholder, str(value))
            filled.append({
                'id': clause_id,
                'title': template.get('title', ''),
                'text': text
            })
        return filled