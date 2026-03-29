# drafter/input_collector.py
from datetime import datetime

class InputCollector:
    """Collects user inputs for required fields."""

    # Default values for common fields
    DEFAULTS = {
        "day": lambda: datetime.now().strftime("%d"),
        "month": lambda: datetime.now().strftime("%B"),
        "year": lambda: datetime.now().strftime("%Y"),
        "date": lambda: datetime.now().strftime("%d %B %Y"),
        "rent_due_day": "5",
        "grace_period": "5",
        "late_interest_rate": "18",
        "default_days": "10",
        "cure_days": "15",
        "abandonment_days": "30",
        "negotiation_days": "30",
        "arbitration_city": "Bangalore",
        "jurisdiction_city": "Bangalore",
    }

    def collect(self, plan, existing_inputs=None):
        """Collect inputs for the plan, merging with existing inputs."""
        if existing_inputs is None:
            existing_inputs = {}
        
        inputs = dict(existing_inputs)
        agreement_type = plan.get("agreement_type", "residential_lease")
        
        # Set default values for missing fields
        for key, default_value in self.DEFAULTS.items():
            if key not in inputs:
                if callable(default_value):
                    inputs[key] = default_value()
                else:
                    inputs[key] = default_value
        
        # Set agreement type
        inputs["agreement_type"] = agreement_type
        
        return inputs