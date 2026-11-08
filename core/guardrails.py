"""
Safety Guardrails & Hallucination Mitigation Engine for NyayaMitra.
Enforces strict boundaries around criminal matters, prevents hallucinated legal citations,
and calculates limitation period risks under Indian law.
"""

import re
from typing import Dict, Any, Tuple, List, Optional
from datetime import datetime
from core.models import DisputeCategory, VerifiedStatute
from core.legal_knowledge import STATUTE_REGISTRY, EMERGENCY_RESOURCES


# Critical Out-of-Scope Criminal / Emergency Keywords
CRIMINAL_EMERGENCY_PATTERNS = [
    r"\b(murder|kill|assault|beat|stab|rape|molest|pocso|narcotics|drugs|dowry|domestic violence|acid attack)\b",
    r"\b(kidnap|abduct|extortion|blackmail|terror|custody torture|police brutality)\b",
    r"\b(suicide|kill myself|harm myself)\b",
    r"\b(bail petition|anticipatory bail|fir quashing|habeas corpus)\b"
]

# Keywords for triage classification
CATEGORY_TRIGGERS = {
    DisputeCategory.TENANCY: [
        "landlord", "tenant", "rent", "security deposit", "flat", "pg", "broker", "brokerage",
        "maintenance", "painting charge", "vacate", "eviction", "lease", "agreement"
    ],
    DisputeCategory.CONSUMER: [
        "flipkart", "amazon", "swiggy", "zomato", "myntra", "order", "refund", "defective",
        "warranty", "product", "seller", "replacement", "customer care", "e-commerce", "damaged"
    ],
    DisputeCategory.EMPLOYMENT: [
        "salary", "employer", "boss", "company", "hr", "resignation", "notice period",
        "relieving letter", "experience letter", "f&f", "full and final", "layoff", "fired", "unpaid"
    ],
    DisputeCategory.FREELANCE: [
        "client", "freelance", "invoice", "milestone", "contractor", "deliverable", "upwork",
        "fiverr", "scope creep", "retainer", "vendor"
    ],
    DisputeCategory.CYBER_FRAUD: [
        "upi", "otp", "phishing", "scam", "fraud", "hacked", "paytm", "gpay", "phonepe", "unauthorized transaction"
    ]
}


class LegalGuardrail:
    @staticmethod
    def detect_emergency_or_criminal(text: str) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Scans text for criminal offenses, violence, or emergencies.
        Returns: (is_critical, detected_keyword, emergency_guidance)
        """
        lower_text = text.lower()
        for pattern in CRIMINAL_EMERGENCY_PATTERNS:
            match = re.search(pattern, lower_text)
            if match:
                keyword = match.group(0)
                guidance = {
                    "alert": "CRIMINAL OR EMERGENCY MATTER DETECTED",
                    "reason": f"Your query contains references to '{keyword}', which falls under criminal law or emergency safety.",
                    "instruction": "An AI tool cannot and must not draft private criminal complaints or handle emergency safety threats. Please seek immediate help from law enforcement or a qualified advocate.",
                    "contacts": [
                        EMERGENCY_RESOURCES["police"],
                        EMERGENCY_RESOURCES["women_helpline"],
                        EMERGENCY_RESOURCES["nalsa_legal_aid"]
                    ]
                }
                return True, keyword, guidance
        return False, None, None

    @staticmethod
    def classify_dispute_category(text: str) -> DisputeCategory:
        """
        Deterministic keyword & heuristic classifier to route dispute into recognized Indian civil categories.
        """
        is_crit, _, _ = LegalGuardrail.detect_emergency_or_criminal(text)
        if is_crit:
            return DisputeCategory.OUT_OF_SCOPE_CRIMINAL

        lower_text = text.lower()
        scores: Dict[DisputeCategory, int] = {}
        for cat, keywords in CATEGORY_TRIGGERS.items():
            score = sum(1 for kw in keywords if kw in lower_text)
            scores[cat] = score

        best_category = max(scores, key=scores.get)
        if scores[best_category] > 0:
            return best_category
        return DisputeCategory.GENERAL_CIVIL

    @staticmethod
    def check_limitation_risk(text: str) -> Tuple[bool, str]:
        """
        Checks if the narrative mentions dates older than standard Indian civil limitation periods (2-3 years).
        """
        current_year = 2026
        # Find 4-digit years like 2020, 2021, 2022, 2023
        years = [int(y) for y in re.findall(r"\b(201\d|202[0-3])\b", text)]
        if years:
            oldest = min(years)
            diff = current_year - oldest
            if diff >= 3:
                return True, f"Cause of action mentions year {oldest} ({diff} years ago). General civil suits carry a 3-year limitation under the Limitation Act, 1963; this claim may face limitation objections unless acknowledgment of debt is shown."
            elif diff >= 2:
                return True, f"Cause of action mentions year {oldest} ({diff} years ago). Consumer forum complaints carry a strict 2-year limitation period under Section 69 of the Consumer Protection Act, 2019."
        return False, "Within standard limitation periods."

    @staticmethod
    def sanitize_statutory_citations(raw_statute_codes: List[str]) -> List[VerifiedStatute]:
        """
        Strips unverified or hallucinated statutes. Ensures only verified statutes in our registry are returned.
        """
        verified = []
        for code in raw_statute_codes:
            if code in STATUTE_REGISTRY:
                verified.append(STATUTE_REGISTRY[code])
        return verified

