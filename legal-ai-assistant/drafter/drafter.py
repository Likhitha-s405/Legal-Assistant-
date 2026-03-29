# drafter/drafter.py
from .formatter import Formatter


class Drafter:
    def __init__(self):
        self.formatter = Formatter()
        print("✅ Drafter initialized")

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
            print(f"❌ Error in draft: {e}")
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
                {'title': 'Parties', 'text': f"This Residential Lease Agreement is made between {user_request.get('lessor_name', 'Landlord')} (Landlord) and {user_request.get('lessee_name', 'Tenant')} (Tenant)."},
                {'title': 'Property', 'text': f"The property located at {user_request.get('property_address', 'Address not specified')}."},
                {'title': 'Term', 'text': f"The term of this lease shall be for {user_request.get('term_months', '11')} months, starting from {user_request.get('start_date', 'the start date')}."},
                {'title': 'Rent', 'text': f"The monthly rent shall be ₹{user_request.get('rent_amount', '0')}, payable on the {user_request.get('rent_due_day', '5th')} day of each month."},
                {'title': 'Security Deposit', 'text': f"A security deposit of ₹{user_request.get('deposit_amount', '0')} is paid by the Tenant to the Landlord."},
                {'title': 'Property Boundaries', 'text': f"North: {user_request.get('north_boundary', 'N/A')}, South: {user_request.get('south_boundary', 'N/A')}, East: {user_request.get('east_boundary', 'N/A')}, West: {user_request.get('west_boundary', 'N/A')}."},
                {'title': 'Default', 'text': f"If rent is not paid within {user_request.get('default_days', '10')} days of due date, the Landlord may terminate this agreement."},
                {'title': 'Jurisdiction', 'text': f"Any disputes shall be subject to the courts in {user_request.get('jurisdiction_city', 'Bangalore')}."}
            ]
            if user_request.get('special_terms'):
                clauses.append({'title': 'Special Terms', 'text': user_request['special_terms']})

        elif agreement_type == 'commercial_lease':
            clauses = [
                {'title': 'Parties', 'text': f"This Commercial Lease Agreement is made between {user_request.get('lessor_name', 'Landlord')} (Landlord) and {user_request.get('lessee_name', 'Tenant')} (Tenant)."},
                {'title': 'Premises', 'text': f"The commercial premises located at {user_request.get('property_address', 'Address not specified')}."},
                {'title': 'Term', 'text': f"The term of this lease shall be for {user_request.get('term_months', '36')} months."},
                {'title': 'Rent', 'text': f"The monthly rent shall be <span class='rupee'>₹</span>{user_request.get('rent_amount', '0')}, payable on the {user_request.get('rent_due_day', '5th')} day of each month."}
            ]

        elif agreement_type == 'nda':
            clauses = [
                {'title': 'Parties', 'text': f"This Non-Disclosure Agreement is between {user_request.get('disclosing_party', 'Disclosing Party')} and {user_request.get('receiving_party', 'Receiving Party')}."},
                {'title': 'Purpose', 'text': f"The purpose of this agreement is {user_request.get('purpose', 'confidential information sharing')}."},
                {'title': 'Term', 'text': f"This agreement shall remain in effect for {user_request.get('term_years', '2')} years."}
            ]

        return clauses