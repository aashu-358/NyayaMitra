"""
Core Pydantic data schemas for NyayaMitra AI Lawyer.
Ensures deterministic data contracts between conversational LLMs and document generators.
"""

from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field


class DisputeCategory(str, Enum):
    TENANCY = "tenancy_security_deposit"
    CONSUMER = "consumer_protection_refund_deficiency"
    EMPLOYMENT = "unpaid_salary_f_and_f_settlement"
    FREELANCE = "freelance_unpaid_invoices_contract"
    CYBER_FRAUD = "cyber_financial_fraud"
    GENERAL_CIVIL = "general_civil_contract"
    OUT_OF_SCOPE_CRIMINAL = "out_of_scope_criminal_or_emergency"


class CaseParty(BaseModel):
    name: str = Field(..., description="Name of the party (person or company)")
    role: str = Field(..., description="Complainant / Tenant / Buyer / Employee / Landlord / Seller / Employer")
    contact: Optional[str] = Field(None, description="Phone, email, or address if known")
    address: Optional[str] = Field(None, description="Physical address or city if known")


class TimelineEvent(BaseModel):
    approx_date: str = Field(..., description="Approximate date or timeframe (e.g. '15 May 2024')")
    event: str = Field(..., description="What transpired on this date")
    evidence_available: Optional[str] = Field(None, description="Proof (e.g. WhatsApp chat, Bank UTR, Invoice, Email)")


class ExtractedCase(BaseModel):
    case_title: str = Field(..., description="Short descriptive title of the dispute")
    category: DisputeCategory = Field(..., description="Primary category of the dispute")
    complainant: CaseParty = Field(..., description="The user seeking help")
    opposite_party: CaseParty = Field(..., description="The person/entity denying rights/payment")
    disputed_amount: Optional[str] = Field(None, description="Total monetary claim in INR (e.g. ₹45,000)")
    key_facts: List[str] = Field(default_factory=list, description="Bulleted summary of what happened")
    timeline: List[TimelineEvent] = Field(default_factory=list, description="Chronological sequence of events")
    evidence_held: List[str] = Field(default_factory=list, description="Evidence the user currently possesses")
    evidence_gaps: List[str] = Field(default_factory=list, description="Critical proof or documents missing that user should gather")
    jurisdiction_city: Optional[str] = Field(None, description="City / State where dispute arose")
    is_time_barred_risk: bool = Field(False, description="Flagged if cause of action is near or beyond limitation (2-3 years)")
    urgency_level: str = Field("NORMAL", description="LOW, NORMAL, HIGH, or CRITICAL_CRIMINAL")


class VerifiedStatute(BaseModel):
    act_name: str
    section: str
    official_title: str
    plain_meaning: str
    maximum_penalty_or_relief: str


class LegalAssessment(BaseModel):
    summary_verdict: str = Field(..., description="Plain-language 2-sentence summary of user's legal standing")
    standing_strength: str = Field(..., description="STRONG, MODERATE, WEAK, or OUT_OF_SCOPE")
    applicable_statutes: List[VerifiedStatute] = Field(default_factory=list, description="Strictly validated Indian statutes")
    action_roadmap: List[str] = Field(..., description="Step 1, Step 2, Step 3 concrete sequence of actions")
    realistic_outcome: str = Field(..., description="Expected timeline and likelihood of recovery without litigation")
    risks_and_caveats: List[str] = Field(default_factory=list, description="Potential counter-claims or weak spots")
    needs_human_lawyer: bool = Field(False, description="True if dispute exceeds small claims or involves litigation")
    legal_aid_option: Optional[str] = Field(None, description="Info on free legal aid (NALSA/DLSA) if applicable")


class LegalNoticeDraft(BaseModel):
    date_of_issuance: str
    sender_details: str
    recipient_details: str
    subject_line: str
    notice_body: str
    statutory_demands: List[str]
    cure_period_days: int = 15
    consequences_of_non_compliance: str
    dispatch_instructions: str


class OpponentSimulationTurn(BaseModel):
    opponent_response: str = Field(..., description="In-character response from the landlord/employer/seller")
    underlying_tactic: str = Field(..., description="Psychological/legal tactic being used (e.g. stall, bluff, intimidate)")
    user_coaching_tip: str = Field(..., description="What the user should say or reply with next to stand firm")
    relevant_fact_to_cite: str = Field(..., description="Specific evidence or clause the user should mention")
