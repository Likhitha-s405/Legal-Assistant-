# drafter/planner.py

class Planner:
    """Determines agreement type and required clauses based on user request."""

    AGREEMENT_TYPES = {
        "residential_lease": {
            "required_clauses": [
                "parties", "recitals", "property_description", "schedule",
                "term", "rent", "deposit", "use_of_premises", "utilities",
                "maintenance_lessee", "maintenance_lessor", "quiet_enjoyment",
                "insurance", "indemnity", "default", "surrender",
                "dispute_resolution", "governing_law", "signatures"
            ]
        },
        "commercial_lease": {
            "required_clauses": [
                "parties", "property_description", "term", "rent", "deposit",
                "permitted_use", "maintenance", "default", "dispute_resolution",
                "governing_law", "signatures"
            ]
        },
        "nda": {
            "required_clauses": [
                "parties", "recitals", "confidential_info", "term",
                "obligations", "exclusions", "return_of_info",
                "governing_law", "signatures"
            ]
        }
    }

    def plan(self, user_request):
        """Determine agreement type and required clauses."""
        agreement_type = user_request.get("agreement_type", "residential_lease")
        
        if agreement_type not in self.AGREEMENT_TYPES:
            return {
                "success": False,
                "agreement_type": "unknown",
                "required_clauses": [],
                "error": f"Unknown agreement type: {agreement_type}"
            }
        
        return {
            "success": True,
            "agreement_type": agreement_type,
            "required_clauses": self.AGREEMENT_TYPES[agreement_type]["required_clauses"]
        }