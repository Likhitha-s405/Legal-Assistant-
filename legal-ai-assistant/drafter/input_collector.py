# drafter/input_collector.py

class InputCollector:
    """Collects required input from user via CLI prompts."""
    
    def collect(self, plan, existing=None):
        """Prompt user for all required fields based on agreement type."""
        inputs = existing or {}
        
        # Define required fields per agreement type
        fields_map = {
            'residential_lease': [
                'lessor_name', 'lessee_name',
                'property_address',
                'north_boundary', 'south_boundary', 'east_boundary', 'west_boundary',  # for schedule
                'term_months', 'start_date',  
                'rent_amount', 'rent_due_day', 'grace_period', 'late_interest_rate',
                'deposit_amount',
                'renewal_notice_days',
                'repair_response_days',
                'default_days', 'cure_days',
                'abandonment_days',
                'negotiation_days', 'arbitration_city', 'jurisdiction_city',
                'city', 'day', 'month', 'year'
            ],
            'commercial_lease': [
                'lessor_name', 'lessee_name', 'property_address',
                'rent_amount', 'deposit_amount', 'term_months',
                'rent_due_day', 'permitted_use', 'city', 'state'
            ],
            'nda': [
                'disclosing_party', 'receiving_party', 'purpose',
                'confidential_info_description', 'term_years'
            ]
        }
        
        fields = fields_map.get(plan['agreement_type'], [])
        print(f"\n--- Enter details for {plan['agreement_type']} ---")
        for field in fields:
            if field not in inputs:
                value = input(f"{field.replace('_', ' ').title()}: ")
                inputs[field] = value
        return inputs