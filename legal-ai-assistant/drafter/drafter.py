# drafter/drafter.py

from .planner import Planner
from .input_collector import InputCollector
from .clause_selector import ClauseSelector
from .formatter import Formatter
from num2words import num2words



class Drafter:
    """Main orchestrator for drafting legal agreements."""
    
    def __init__(self):
        self.planner = Planner()
        self.collector = InputCollector()
        self.selector = ClauseSelector()
        self.formatter = Formatter()

    def _enrich_inputs(self, inputs):
        # Add amount in words
        if 'rent_amount' in inputs and inputs['rent_amount']:
            try:
                inputs['rent_amount_in_words'] = num2words(float(inputs['rent_amount']), lang='en_IN').title() + ' Rupees'
            except:
                inputs['rent_amount_in_words'] = inputs['rent_amount']
        # Calculate end_date from start_date + term_months
        if 'start_date' in inputs and 'term_months' in inputs:
            try:
                from datetime import datetime
                from dateutil.relativedelta import relativedelta
                start = datetime.strptime(inputs['start_date'], '%d %B %Y')
                end = start + relativedelta(months=int(inputs['term_months']))
                inputs['end_date'] = end.strftime('%d %B %Y')
            except:
                inputs['end_date'] = '[end_date]'
        # Set default date if missing
        if 'date' not in inputs:
            from datetime import datetime
            inputs['date'] = datetime.now().strftime('%d %B %Y')
        return inputs
    
    def draft(self, user_request=None):
        """
        user_request: optional dict with initial data (agreement_type, etc.)
        Returns dict with success, pdf_bytes, etc.
        """
        if user_request is None:
            user_request = {}
        
        # Step 1: Planning
        plan = self.planner.plan(user_request)
        
        # Step 2: Input collection (CLI prompts if missing)
        inputs = self.collector.collect(plan, user_request)
        inputs = self._enrich_inputs(inputs)
        # Step 3: Clause selection and filling
        clauses = self.selector.select_clauses(plan['required_clauses'], inputs)
        
        # Step 4: Render HTML
        html = self.formatter.render_html(plan['agreement_type'], clauses, inputs)
        
        # Step 5: Generate PDF
        pdf_bytes = self.formatter.generate_pdf(html)
        
        return {
            'success': True,
            'pdf': pdf_bytes,
            'clauses': clauses,
            'plan': plan,
            'inputs': inputs
        }