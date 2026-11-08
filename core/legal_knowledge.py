"""
Authoritative Indian Legal Statute & Ground Truth Knowledge Base.
This verified registry prevents LLM hallucination by restricting statutory citations
to verified, valid Indian legal sections and limitation periods.
"""

from typing import Dict, List, Optional
from core.models import VerifiedStatute, DisputeCategory

# Verified Statutes Dictionary
STATUTE_REGISTRY: Dict[str, VerifiedStatute] = {
    # Consumer Protection Act, 2019
    "CPA_2_11": VerifiedStatute(
        act_name="Consumer Protection Act, 2019",
        section="Section 2(11)",
        official_title="Deficiency of Service",
        plain_meaning="Any fault, imperfection, shortcoming or inadequacy in the quality, nature and manner of performance required by law or contract.",
        maximum_penalty_or_relief="Refund of amount paid, compensation for harassment/mental agony, and litigation costs."
    ),
    "CPA_2_47": VerifiedStatute(
        act_name="Consumer Protection Act, 2019",
        section="Section 2(47)",
        official_title="Unfair Trade Practice",
        plain_meaning="Deceptive practices including refusing refunds for defective goods, false guarantees, or charging above agreed price.",
        maximum_penalty_or_relief="Direction to discontinue unfair trade practice, issue full refund, and pay punitive damages."
    ),
    "CPA_35": VerifiedStatute(
        act_name="Consumer Protection Act, 2019",
        section="Section 35",
        official_title="Filing of Complaint before District Commission (e-Daakhil)",
        plain_meaning="Any consumer can file a complaint directly online via e-Daakhil for claims up to ₹50 Lakhs without needing to hire an advocate.",
        maximum_penalty_or_relief="Direct court order for full refund with interest and punitive compensation."
    ),

    # Tenancy / Security Deposit Law
    "TPA_108": VerifiedStatute(
        act_name="Transfer of Property Act, 1882",
        section="Section 108(m) & (q)",
        official_title="Rights and Liabilities of Lessor and Lessee",
        plain_meaning="Tenant must restore premises in reasonable condition (subject to normal wear and tear); landlord must return the security deposit after deducting only mutually agreed damages.",
        maximum_penalty_or_relief="Recovery of full security deposit with commercial interest (typically 6-18% p.a.)."
    ),
    "MTA_2021_DEPOSIT": VerifiedStatute(
        act_name="Model Tenancy Act, 2021 (and State Tenancy Rules)",
        section="Section 13",
        official_title="Security Deposit Cap and Refund Timeline",
        plain_meaning="Security deposit for residential premises is capped at maximum 2 months' rent and must be returned within 30 days of vacating after agreed deductions.",
        maximum_penalty_or_relief="Landlord liable for compound interest and penalties before Rent Authority."
    ),

    # Contract Law & Civil Recovery
    "ICA_73": VerifiedStatute(
        act_name="Indian Contract Act, 1872",
        section="Section 73",
        official_title="Compensation for Loss or Damage Caused by Breach of Contract",
        plain_meaning="When a contract is broken, the party who suffers is entitled to receive compensation for any loss or damage naturally arising from the breach.",
        maximum_penalty_or_relief="Full recovery of dues plus consequential damages and interest."
    ),
    "ICA_27": VerifiedStatute(
        act_name="Indian Contract Act, 1872",
        section="Section 27",
        official_title="Agreement in Restraint of Trade Void",
        plain_meaning="Any clause restraining an employee from exercising a lawful profession, trade or business is legally void. Employers cannot withhold relieving letters or salaries based on illegal non-competes.",
        maximum_penalty_or_relief="Clause struck down as unenforceable; employer ordered to release pending dues."
    ),

    # Employment & Wages
    "PWA_15": VerifiedStatute(
        act_name="Payment of Wages Act, 1936",
        section="Section 15",
        official_title="Claims Arising out of Deductions from Wages or Delay in Payment",
        plain_meaning="Employers cannot withhold earned wages without explicit statutory authorization. Applies to employees earning up to statutory wage limits.",
        maximum_penalty_or_relief="Direction to pay withheld wages plus compensation up to 10 times the deducted amount."
    ),
    "IDA_25F": VerifiedStatute(
        act_name="Industrial Disputes Act, 1947",
        section="Section 25F",
        official_title="Conditions Precedent to Retrenchment",
        plain_meaning="Requires 1 month notice or wages in lieu thereof, plus retrenchment compensation of 15 days average pay for each completed year of service.",
        maximum_penalty_or_relief="Reinstatement with full back wages or statutory retrenchment package."
    ),

    # MSME / Freelance
    "MSMED_15_16": VerifiedStatute(
        act_name="Micro, Small and Medium Enterprises Development Act, 2006",
        section="Sections 15 & 16",
        official_title="Mandatory Payment Period and Compound Interest for Delay",
        plain_meaning="Buyer must make payment within 45 days. Delayed payment attracts compound interest with monthly rests at 3 times the Bank Rate notified by RBI.",
        maximum_penalty_or_relief="Mandatory 3x RBI interest rate via MSME Samadhaan conciliation."
    ),

    # Negotiable Instruments (Cheque Bounce)
    "NIA_138": VerifiedStatute(
        act_name="Negotiable Instruments Act, 1881",
        section="Section 138",
        official_title="Dishonour of Cheque for Insufficiency of Funds",
        plain_meaning="Bouncing a cheque is a quasi-criminal offense. Holder must issue a statutory demand notice within 30 days of receiving the cheque return memo, giving 15 days to pay.",
        maximum_penalty_or_relief="Imprisonment up to 2 years and/or fine up to twice the cheque amount."
    ),

    # Limitation Act
    "LIMITATION_ACT": VerifiedStatute(
        act_name="Limitation Act, 1963",
        section="Article 113 / General Schedule",
        official_title="Statutory Period of Limitation for Recovery",
        plain_meaning="General civil recovery suits must be filed within 3 years from the date payment became due. Consumer complaints have a 2-year limitation (Section 69 CPA).",
        maximum_penalty_or_relief="Bar on judicial remedy if suit is not filed within the limitation period."
    )
}


# Category-to-Statutes Mapping
CATEGORY_STATUTE_MAPPING: Dict[DisputeCategory, List[str]] = {
    DisputeCategory.TENANCY: ["TPA_108", "MTA_2021_DEPOSIT", "ICA_73", "LIMITATION_ACT"],
    DisputeCategory.CONSUMER: ["CPA_2_11", "CPA_2_47", "CPA_35", "LIMITATION_ACT"],
    DisputeCategory.EMPLOYMENT: ["PWA_15", "IDA_25F", "ICA_27", "ICA_73", "LIMITATION_ACT"],
    DisputeCategory.FREELANCE: ["ICA_73", "MSMED_15_16", "LIMITATION_ACT"],
    DisputeCategory.CYBER_FRAUD: ["CPA_2_11", "ICA_73"],
    DisputeCategory.GENERAL_CIVIL: ["ICA_73", "LIMITATION_ACT"],
    DisputeCategory.OUT_OF_SCOPE_CRIMINAL: []
}


# Emergency Contacts & Legal Aid Hotlines
EMERGENCY_RESOURCES = {
    "police": {"name": "National Emergency Police Response", "number": "112", "desc": "Immediate physical safety or crime reporting"},
    "cybercrime": {"name": "National Cyber Crime Reporting Helpline", "number": "1930", "portal": "https://cybercrime.gov.in", "desc": "Immediate reporting for financial UPI/banking fraud within golden hour"},
    "women_helpline": {"name": "Women in Distress National Helpline", "number": "1091 / 181", "desc": "Domestic violence, harassment, emergency legal aid"},
    "consumer_helpline": {"name": "National Consumer Helpline (NCH)", "number": "1915", "portal": "https://consumerhelpline.gov.in", "desc": "Toll-free pre-litigation conciliation with registered brands"},
    "nalsa_legal_aid": {"name": "National Legal Services Authority (NALSA)", "number": "15100", "portal": "https://nalsa.gov.in", "desc": "Free legal aid and lawyer assignment for eligible citizens (women, SC/ST, low income)"}
}


def get_verified_statutes_for_category(category: DisputeCategory) -> List[VerifiedStatute]:
    """Returns only authoritative, vetted statutes for a dispute category."""
    statute_keys = CATEGORY_STATUTE_MAPPING.get(category, [])
    return [STATUTE_REGISTRY[k] for k in statute_keys if k in STATUTE_REGISTRY]


def validate_legal_citation(statute_code: str) -> Optional[VerifiedStatute]:
    """Validates if a cited statute is within the verified Indian legal registry."""
    return STATUTE_REGISTRY.get(statute_code)

