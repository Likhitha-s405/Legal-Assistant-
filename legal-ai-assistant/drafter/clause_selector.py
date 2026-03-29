# drafter/clause_selector.py


class ClauseSelector:
    """Selects and fills clause templates based on required clause IDs and inputs."""

    CLAUSES = {
        "residential_lease": {
            "parties": {
                "title": "Parties",
                "template": (
                    "This Agreement for Residential Lease (hereinafter referred to as the "
                    "<b>'Agreement'</b>) is entered into on the <b>{day}</b> day of <b>{month}, {year}</b>, "
                    "by and between:<br><br>"
                    "<b>{lessor_name}</b> (hereinafter referred to as the <b>'Lessor'</b>),<br><br>"
                    "AND<br><br>"
                    "<b>{lessee_name}</b> (hereinafter referred to as the <b>'Lessee'</b>)."
                ),
            },
            "recitals": {
                "title": "Recitals",
                "template": (
                    "WHEREAS, the Lessor is the lawful owner and is in possession of the premises "
                    "described herein and desires to lease the same to the Lessee; and<br><br>"
                    "WHEREAS, the Lessee desires to take on lease the said premises from the Lessor "
                    "on the terms and conditions set forth in this Agreement."
                ),
            },
            "property_description": {
                "title": "Property Description",
                "template": (
                    "The Lessor agrees to lease to the Lessee the residential premises located at "
                    "<b>{property_address}</b> (hereinafter referred to as the <b>'Premises'</b>), "
                    "more particularly described in the Schedule annexed hereto."
                ),
            },
            "schedule": {
                "title": "Schedule — Description of Premises",
                "template": (
                    "<table style='width:100%; border-collapse:collapse;'>"
                    "<tr><td style='padding:4px 8px;'><b>Property Address:</b></td>"
                    "<td style='padding:4px 8px;'>{property_address}</td></tr>"
                    "<tr><td style='padding:4px 8px;'><b>North:</b></td><td style='padding:4px 8px;'>{north_boundary}</td></tr>"
                    "<tr><td style='padding:4px 8px;'><b>South:</b></td><td style='padding:4px 8px;'>{south_boundary}</td></tr>"
                    "<tr><td style='padding:4px 8px;'><b>East:</b></td><td style='padding:4px 8px;'>{east_boundary}</td></tr>"
                    "<tr><td style='padding:4px 8px;'><b>West:</b></td><td style='padding:4px 8px;'>{west_boundary}</td></tr>"
                    "</table>"
                ),
            },
            "term": {
                "title": "Term",
                "template": (
                    "The lease shall be for a period of <b>{term_months} months</b>, commencing on "
                    "<b>{start_date}</b> and ending on <b>{end_date}</b>, unless sooner terminated "
                    "in accordance with the provisions of this Agreement."
                ),
            },
            "rent": {
                "title": "Rent",
                "template": (
                    "The Lessee agrees to pay the Lessor a monthly rent of "
                    "<b>₹{rent_amount} ({rent_amount_in_words})</b>, payable on or before the "
                    "<b>{rent_due_day}th</b> day of each calendar month. "
                    "A grace period of <b>{grace_period} days</b> shall be allowed, after which "
                    "interest at <b>{late_interest_rate}% per annum</b> shall accrue on overdue amounts."
                ),
            },
            "deposit": {
                "title": "Security Deposit",
                "template": (
                    "The Lessee shall pay a refundable security deposit of <b>₹{deposit_amount}</b> "
                    "prior to taking possession of the Premises. The deposit shall be refunded within "
                    "30 days of the expiry or termination of this Agreement, after deduction of any "
                    "amounts due for unpaid rent or damages caused by the Lessee beyond normal wear and tear."
                ),
            },
            "use_of_premises": {
                "title": "Use of Premises",
                "template": (
                    "The Lessee shall use the Premises solely for residential purposes and shall not "
                    "carry on any trade, business, or commercial activity therein. The Lessee shall "
                    "not use the Premises or permit the same to be used for any illegal or immoral purpose."
                ),
            },
            "utilities": {
                "title": "Utilities",
                "template": (
                    "The Lessee shall be responsible for all utility charges including electricity, "
                    "water, gas, internet, and telephone services consumed at the Premises during the "
                    "lease term. The Lessor shall ensure that utility connections are available at the "
                    "commencement of the lease."
                ),
            },
            "maintenance_lessee": {
                "title": "Maintenance by Lessee",
                "template": (
                    "The Lessee shall maintain the Premises in good and tenantable condition, "
                    "keep it clean, and shall not make any structural alterations or additions without "
                    "prior written consent of the Lessor. Minor repairs not exceeding ₹500 shall be "
                    "the responsibility of the Lessee."
                ),
            },
            "maintenance_lessor": {
                "title": "Maintenance by Lessor",
                "template": (
                    "The Lessor shall be responsible for major structural repairs and shall attend to "
                    "reported defects within <b>{repair_response_days} days</b> of written notice from "
                    "the Lessee. The Lessor shall ensure the Premises are fit for habitation at the "
                    "commencement of the lease."
                ),
            },
            "quiet_enjoyment": {
                "title": "Quiet Enjoyment",
                "template": (
                    "The Lessor covenants that upon the Lessee paying rent and observing the terms "
                    "hereof, the Lessee shall peaceably hold and enjoy the Premises during the lease "
                    "term without any interruption or disturbance from the Lessor or any person claiming "
                    "under or through the Lessor."
                ),
            },
            "insurance": {
                "title": "Insurance",
                "template": (
                    "The Lessor shall maintain adequate insurance for the structure of the Premises. "
                    "The Lessee is advised to obtain renter's insurance to cover personal belongings "
                    "and any liability arising within the Premises. Neither party's insurance shall "
                    "be required to cover the other party's property."
                ),
            },
            "indemnity": {
                "title": "Indemnity",
                "template": (
                    "The Lessee shall indemnify and hold harmless the Lessor against any claims, "
                    "losses, or damages arising from the Lessee's use of the Premises or any breach "
                    "of this Agreement by the Lessee. The Lessor shall not be liable for any loss "
                    "or damage to the Lessee's belongings stored in the Premises."
                ),
            },
            "default": {
                "title": "Default",
                "template": (
                    "If the Lessee fails to pay rent within <b>{default_days} days</b> of its due date, "
                    "or breaches any provision of this Agreement and fails to remedy the breach within "
                    "<b>{cure_days} days</b> of written notice, the Lessor shall be entitled to terminate "
                    "this Agreement and recover possession of the Premises, without prejudice to any "
                    "other remedies available under law."
                ),
            },
            "surrender": {
                "title": "Surrender of Premises",
                "template": (
                    "Upon expiry or earlier termination of this Agreement, the Lessee shall vacate "
                    "and surrender the Premises to the Lessor in the same condition as at the "
                    "commencement of the lease, subject to fair wear and tear. The Lessee shall "
                    "return all keys and access devices to the Lessor upon vacation. "
                    "If the Lessee abandons the Premises for more than <b>{abandonment_days} days</b> "
                    "without notice, the Lessor may treat this as surrender."
                ),
            },
            "dispute_resolution": {
                "title": "Dispute Resolution",
                "template": (
                    "In the event of any dispute arising out of or in connection with this Agreement, "
                    "the parties shall first attempt to resolve the same amicably through negotiation "
                    "within <b>{negotiation_days} days</b> of the dispute arising. If unresolved, the "
                    "matter shall be referred to arbitration in <b>{arbitration_city}</b> in accordance "
                    "with the Arbitration and Conciliation Act, 1996, and the award shall be binding "
                    "on both parties."
                ),
            },
            "governing_law": {
                "title": "Governing Law",
                "template": (
                    "This Agreement shall be governed by and construed in accordance with the laws of "
                    "India. Any legal proceedings arising out of this Agreement shall be subject to "
                    "the exclusive jurisdiction of the courts in <b>{jurisdiction_city}</b>."
                ),
            },
            "signatures": {
                "title": "Signatures",
                "template": (
                    "<br><br>"
                    "IN WITNESS WHEREOF, the parties hereto have executed this Agreement on the date "
                    "first written above.<br><br>"
                    "<table style='width:100%; margin-top:40px;'>"
                    "<tr>"
                    "<td style='width:45%; vertical-align:top;'>"
                    "<b>LESSOR</b><br><br><br>"
                    "____________________________<br>"
                    "{lessor_name}<br>"
                    "Date: ___________________"
                    "</td>"
                    "<td style='width:10%;'></td>"
                    "<td style='width:45%; vertical-align:top;'>"
                    "<b>LESSEE</b><br><br><br>"
                    "____________________________<br>"
                    "{lessee_name}<br>"
                    "Date: ___________________"
                    "</td>"
                    "</tr>"
                    "</table><br><br>"
                    "<b>Witnesses:</b><br><br>"
                    "<table style='width:100%; margin-top:20px;'>"
                    "<tr>"
                    "<td style='width:45%; vertical-align:top;'>"
                    "1. ____________________________<br>"
                    "Name:<br>Address:"
                    "</td>"
                    "<td style='width:10%;'></td>"
                    "<td style='width:45%; vertical-align:top;'>"
                    "2. ____________________________<br>"
                    "Name:<br>Address:"
                    "</td>"
                    "</tr>"
                    "</table>"
                ),
            },
        }
    }

    def select_clauses(self, required_clause_ids, inputs):
        """
        Returns a list of clause dicts with id, title, text
        filled with inputs.
        """
        agreement_type = inputs.get("agreement_type", "residential_lease")

        # Try to detect agreement_type from inputs if not set
        # (Planner passes it in the plan, but not always in inputs)
        clauses_bank = self.CLAUSES.get(agreement_type) or self.CLAUSES.get("residential_lease")

        result = []
        for clause_id in required_clause_ids:
            clause_def = clauses_bank.get(clause_id)
            if not clause_def:
                continue

            try:
                filled_text = clause_def["template"].format_map(
                    _SafeDict(inputs)
                )
            except Exception as e:
                filled_text = clause_def["template"]  # fallback: unfilled

            result.append({
                "id": clause_id,
                "title": clause_def["title"],
                "text": filled_text,
            })

        return result


class _SafeDict(dict):
    """A dict subclass that returns a placeholder for missing keys instead of raising KeyError."""

    def __missing__(self, key):
        return f"[{key}]"