# drafter/planner.py

class Planner:
    """Determines agreement type and required clauses based on user request."""
    
    def plan(self, user_request):
        agreement_type = user_request.get('agreement_type', 'unknown')
        
        # Map agreement types to ordered list of clause IDs
        clause_mapping = {
            'residential_lease': [
                'parties',
                'property_description',
                'schedule',               
                'term',
                'rent',
                'deposit',
                'use_of_premises',
                'utilities',
                'maintenance_lessee',
                'maintenance_lessor',
                'quiet_enjoyment',
                'insurance',
                'indemnity',
                'default',
                'surrender',
                'dispute_resolution',
                'governing_law',
                'signatures'
            ],
            'commercial_lease': [
                'parties',
                'property_description',
                'schedule',
                'term',
                'rent',
                'deposit',
                'use_of_premises',
                'utilities',
                'maintenance_lessee',
                'maintenance_lessor',
                'quiet_enjoyment',
                'insurance',
                'sublease',
                'default',
                'surrender',
                'dispute_resolution',
                'governing_law',
                'signatures'
            ],
            'nda': [
                'parties',
                'confidential_info',
                'obligations',
                'exclusions',
                'term',
                'return_of_materials',
                'dispute_resolution',
                'governing_law',
                'signatures'
            ],
        }
        
        required_clauses = clause_mapping.get(agreement_type, [])
        return {
            'agreement_type': agreement_type,
            'required_clauses': required_clauses,
            'next_agent': 'input_collector'
        }