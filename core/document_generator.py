"""
Document Generator for NyayaMitra.
Produces legally formatted Indian Draft Legal Notices, e-Daakhil Consumer Complaints,
and generates ready-to-print PDFs using ReportLab.
"""

import os
from typing import Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from core.models import ExtractedCase, LegalAssessment, LegalNoticeDraft, DisputeCategory


def generate_legal_notice_text(case: ExtractedCase, assessment: LegalAssessment) -> LegalNoticeDraft:
    """
    Generates a structured, professional Indian Legal Notice text according to standard advocate convention.
    """
    sender_name = case.complainant.name or "Complainant / Aggrieved Party"
    sender_addr = case.complainant.address or "Address on Record"
    sender_contact = case.complainant.contact or "Contact on Record"
    
    recipient_name = case.opposite_party.name or "Opposite Party"
    recipient_addr = case.opposite_party.address or "Address on Record"
    
    amount_str = case.disputed_amount or "the outstanding statutory amount"
    
    subject = f"LEGAL NOTICE DEMANDING IMMEDIATE REFUND / PAYMENT OF {amount_str.upper()} WITH ACCRUED INTEREST"
    
    # Compile facts
    facts_paragraphs = []
    for idx, fact in enumerate(case.key_facts, start=1):
        facts_paragraphs.append(f"{idx}. {fact}")
    facts_text = "\n\n".join(facts_paragraphs) if facts_paragraphs else "1. The parties entered into a binding contractual arrangement as documented on record."
    
    # Statutory grounds
    statute_grounds = []
    for s in assessment.applicable_statutes:
        statute_grounds.append(f"• Violation of {s.act_name} [{s.section} - {s.official_title}]: {s.plain_meaning}")
    statute_grounds_text = "\n".join(statute_grounds) if statute_grounds else "• Violation of Section 73 of the Indian Contract Act, 1872 for breach of contractual obligations."
    
    demands = [
        f"Immediately pay and remit the sum of {amount_str} along with interest @ 18% per annum from the date of default until the date of actual realization.",
        "Furnish a written confirmation and statement of account acknowledging full settlement of all claims.",
        "Cease and desist from any further unlawful withholding of funds, security deposits, or earned dues."
    ]
    
    notice_body = f"""UNDER INSTRUCTIONS FROM MY CLIENT / ISSUED ON BEHALF OF:
{sender_name}, residing at {sender_addr} (hereinafter referred to as 'My Client / Undersigned').

TO:
{recipient_name}, having address/office at {recipient_addr} (hereinafter referred to as 'You / Addressee').

SUBJECT: {subject}

Sir/Madam,

Under instructions and on behalf of the Undersigned, this Legal Notice is hereby served upon you for immediate compliance:

1. STATEMENT OF FACTS & CHRONOLOGY:
{facts_text}

2. STATUTORY VIOLATIONS & LEGAL GROUNDS:
Your aforesaid act of arbitrarily and unilaterally withholding the legitimate dues of the Undersigned is illegal, fraudulent, and amounts to actionable default under the laws of India, including:
{statute_grounds_text}

3. PEREMPTORY DEMAND:
You are hereby called upon to pay and remit the entire legitimate claim of {amount_str} along with interest @ 18% per annum within a period of 15 (FIFTEEN) DAYS from the date of receipt of this notice, into the bank account details provided hereunder or via demand draft.

4. CONSEQUENCES OF NON-COMPLIANCE:
Please take note that if you fail, neglect, or refuse to comply with the above demands within the stipulated 15-day cure period, the Undersigned shall be constrained to initiate appropriate civil proceedings, including filing a statutory complaint before the competent Consumer Disputes Redressal Commission (via e-Daakhil) / competent Court of Small Causes / Rent Authority, entirely at your risk, cost, and consequence. 

In such event, you shall be held liable not only for the principal claim and enhanced interest, but also for comprehensive damages for mental agony, harassment, and all legal costs incurred.

A copy of this Legal Notice is retained on record for production before the Court as documentary proof of pre-litigation demand.

Yours sincerely,

___________________________
{sender_name}
(Aggrieved Party / Complainant)
Contact: {sender_contact}
"""

    return LegalNoticeDraft(
        date_of_issuance="November 2026",
        sender_details=f"{sender_name}\n{sender_addr}\n{sender_contact}",
        recipient_details=f"{recipient_name}\n{recipient_addr}",
        subject_line=subject,
        notice_body=notice_body,
        statutory_demands=demands,
        cure_period_days=15,
        consequences_of_non_compliance="Institution of formal proceedings before the competent Forum/Court with claims for 18% interest, damages, and litigation expenses.",
        dispatch_instructions="Send via Indian Speed Post with Acknowledgement Due (RPAD) and keep the postal receipt and tracking slip. Also email a PDF copy to the addressee's official email address."
    )


def export_legal_notice_pdf(notice: LegalNoticeDraft, output_path: str) -> str:
    """
    Compiles a clean, printable PDF of the Legal Notice using ReportLab.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    header_style = ParagraphStyle(
        'LegalHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        alignment=1, # Center
        textColor=colors.HexColor('#8B0000'),
        spaceAfter=6
    )
    
    sub_header = ParagraphStyle(
        'SubHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        alignment=1,
        textColor=colors.HexColor('#1A237E'),
        spaceAfter=12
    )
    
    body_style = ParagraphStyle(
        'LegalBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        spaceAfter=8
    )
    
    bold_body = ParagraphStyle(
        'BoldBody',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        spaceAfter=6
    )
    
    story = []
    
    # Top banner
    story.append(Paragraph("BY SPEED POST WITH ACKNOWLEDGEMENT DUE / REGISTERED EMAIL", header_style))
    story.append(Paragraph("PRE-LITIGATION STATUTORY DEMAND NOTICE (UNDER LAWS OF INDIA)", sub_header))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1A237E'), spaceAfter=10))
    
    # Sender / Recipient Table
    party_data = [
        [Paragraph(f"<b>FROM (SENDER):</b><br/>{notice.sender_details.replace(chr(10), '<br/>')}", body_style),
         Paragraph(f"<b>TO (ADDRESSEE):</b><br/>{notice.recipient_details.replace(chr(10), '<br/>')}", body_style)]
    ]
    t = Table(party_data, colWidths=[260, 260])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8F9FA')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#EEEEEE')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))
    
    # Subject Line Box
    subj_data = [[Paragraph(f"<b>SUBJECT:</b> {notice.subject_line}", bold_body)]]
    subj_table = Table(subj_data, colWidths=[520])
    subj_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFF3E0')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#E65100')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(subj_table)
    story.append(Spacer(1, 10))
    
    # Body Paragraphs
    for line in notice.notice_body.split("\n\n"):
        clean_line = line.strip().replace("\n", "<br/>")
        if clean_line:
            story.append(Paragraph(clean_line, body_style))
            story.append(Spacer(1, 4))
            
    # Dispatch box
    dispatch_data = [[
        Paragraph(f"<b>DISPATCH & PROOF INSTRUCTIONS:</b><br/>{notice.dispatch_instructions}", body_style)
    ]]
    dt = Table(dispatch_data, colWidths=[520])
    dt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#E8F5E9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#2E7D32')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(Spacer(1, 10))
    story.append(dt)
    
    doc.build(story)
    return output_path

