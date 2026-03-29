# drafter/drafter.py
from .formatter import Formatter

class Drafter:
    def __init__(self):
        self.formatter = Formatter()
    
    def draft(self, user_request):
        """Generate a draft document based on user request"""
        agreement_type = user_request.get('agreement_type', 'residential_lease')
        
        # Generate clauses based on agreement type
        clauses = self.generate_clauses(agreement_type, user_request)
        
        try:
            # Generate HTML and PDF
            html = self.formatter.render_html(agreement_type, clauses, user_request)
            pdf = self.formatter.generate_pdf(html)
            
            return {
                'success': True,
                'pdf': pdf,
                'clauses': clauses,
                'inputs': user_request
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'clauses': clauses,
                'inputs': user_request
            }
    
    def generate_clauses(self, agreement_type, user_request):
        """Generate clauses based on agreement type"""
        clauses = []
        
        if agreement_type == 'residential_lease':
            clauses = [
                {'title': 'Parties', 'text': f"This Residential Lease Agreement is made between {user_request.get('lessee_name', 'Tenant')} (Tenant) and {user_request.get('lessor_name', 'Landlord')} (Landlord)."},
                {'title': 'Property', 'text': f"The property located at {user_request.get('property_address', 'Address not specified')} is leased to the Tenant."},
                {'title': 'Term', 'text': f"The term of this lease shall be for {user_request.get('lease_term', '12')} months."},
                {'title': 'Rent', 'text': f"The monthly rent shall be ${user_request.get('rent_amount', '0')} payable on the first day of each month."}
            ]
            if user_request.get('special_terms'):
                clauses.append({'title': 'Special Terms', 'text': user_request['special_terms']})
        
        elif agreement_type == 'commercial_lease':
            clauses = [
                {'title': 'Parties', 'text': f"This Commercial Lease Agreement is made between {user_request.get('lessee_name', 'Tenant')} (Tenant) and {user_request.get('lessor_name', 'Landlord')} (Landlord)."},
                {'title': 'Premises', 'text': f"The commercial premises located at {user_request.get('property_address', 'Address not specified')}."},
                {'title': 'Use', 'text': f"The premises shall be used for commercial business purposes."}
            ]
        
        elif agreement_type == 'nda':
            clauses = [
                {'title': 'Parties', 'text': f"This Non-Disclosure Agreement is between {user_request.get('disclosing_party', 'Disclosing Party')} and {user_request.get('receiving_party', 'Receiving Party')}."},
                {'title': 'Confidential Information', 'text': f"Confidential information includes all proprietary information shared between the parties."},
                {'title': 'Term', 'text': f"This agreement shall remain in effect for {user_request.get('term_years', '2')} years."}
            ]
        
        return clauses