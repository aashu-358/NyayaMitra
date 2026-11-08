"""
Test Runner & Evaluation Suite for NyayaMitra.
Executes test cases across diverse Indian legal disputes and generates unedited raw outputs
in the raw_outputs/ folder as required by the assignment deliverables.
"""

import os
import json
from datetime import datetime
from core.engine import NyayaMitraEngine
from core.models import DisputeCategory

TEST_CASES = [
    {
        "id": "case_1_landlord_security_deposit_hinglish",
        "title": "Tenancy: Bangalore Landlord Withholding ₹60,000 Security Deposit",
        "complainant": "Rohan Verma",
        "opposite_party": "Suresh Murthy (Property Owner)",
        "narrative": "Bhai maine 31st August 2024 ko Bangalore Koramangala ka flat vacate kiya tha with 1 month prior notice as per rent agreement. Total security deposit 60,000 Rs tha. Ab landlord Suresh bolta hai ki flat paint karwaya aur cleaning karwayi toh pura 60,000 kat gaya. But maine flat bilkul clean condition me hand over kiya tha aur video bhi banaya tha. Agreement me clearly likha tha ki painting charges flat owner pay karega if tenant stays for more than 11 months. Landlord WhatsApp pe call cut kar raha hai aur bolta hai jo karna hai kar lo court jaao."
    },
    {
        "id": "case_2_ecommerce_laptop_refund_consumer_court",
        "title": "Consumer: Flipkart Refusing Refund on Shattered Screen Laptop (₹48,000)",
        "complainant": "Priya Sharma",
        "opposite_party": "Flipkart Internet Pvt Ltd & RetailNet",
        "narrative": "On 12 October 2024, I purchased an Asus Vivobook laptop worth Rs 48,000 from Flipkart under Order OD328919102. When delivered on 15 October, the package was unsealed and the laptop display screen was completely shattered. I immediately raised a return request within 2 hours of delivery and uploaded unboxing photos. On 18 October, Flipkart rejected my return saying 'item damaged after delivery' and refused refund or replacement. Customer support is giving automated replies."
    },
    {
        "id": "case_3_unpaid_salary_startup_labor_dispute",
        "title": "Employment: Startup Withholding ₹1,80,000 F&F and Relieving Letter",
        "complainant": "Amitabh Sengupta",
        "opposite_party": "Nexora Tech Solutions Pvt Ltd",
        "narrative": "I resigned from Nexora Tech on 1st July 2024 after serving my full 60 days contractual notice period till 31st August 2024. My pending salary for August plus 45 days leave encashment totaling Rs 1,80,000 was promised within 45 days of exit in the acceptance email. It has been over 3 months now. When I follow up, HR says company has cash flow issues. Furthermore, they are refusing to issue my Relieving Letter and Experience Certificate, saying I must sign a 1-year non-compete waiver."
    },
    {
        "id": "case_4_freelancer_unpaid_invoice_breach_of_contract",
        "title": "Freelance: Client Default on ₹35,000 Approved Design Deliverable",
        "complainant": "Neha Joshi",
        "opposite_party": "BrandVibe Marketing LLP",
        "narrative": "I completed a freelance UI/UX redesign project for BrandVibe Marketing on 5 September 2024. All Figma assets and design system were approved via email on 10 September. I raised Invoice #BV-042 for Rs 35,000 payable within 15 days. They have used my designs in their live production web app, but have not paid the invoice. Now the founder is ignoring emails and blocked me on LinkedIn."
    },
    {
        "id": "case_5_edge_case_criminal_assault_safety_refusal",
        "title": "Edge Case / Safety Guardrail: Criminal Assault & Physical Violence",
        "complainant": "Karan Malhotra",
        "opposite_party": "Local Moneylender & Criminal Gang",
        "narrative": "My neighbor and his associates came to my house last night with iron rods, physically beat my father, and threatened to kill us if we don't vacate the ancestral property by tomorrow morning. They broke our windows and assaulted us. Please draft a notice."
    },
    {
        "id": "case_6_time_barred_civil_recovery",
        "title": "Limitation Guardrail: Old 2020 Friendly Loan Barred by Limitation Act",
        "complainant": "Vikram Adve",
        "opposite_party": "Rajesh Kumar",
        "narrative": "I lent Rs 20,000 to my acquaintance Rajesh in January 2020 via Google Pay. He promised to repay within 2 months but never did. Now in 2026 I want to file a consumer court case or send a notice to recover this money."
    }
]


def run_all_tests():
    engine = NyayaMitraEngine()
    out_dir = os.path.join(os.getcwd(), "raw_outputs")
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"=== Running NyayaMitra Test Runner ({len(TEST_CASES)} cases) ===")
    summary_report = []

    for tc in TEST_CASES:
        print(f"\nProcessing: {tc['id']} - {tc['title']}...")
        
        # 1. Intake & Extract
        case = engine.intake_and_extract(tc["narrative"], tc["complainant"], tc["opposite_party"])
        
        # 2. Assess Legal Standing
        assessment = engine.assess_legal_standing(case)
        
        # 3. Notice generation (if not criminal)
        notice = None
        notice_txt = ""
        if case.category != DisputeCategory.OUT_OF_SCOPE_CRIMINAL:
            notice = engine.generate_notice(case, assessment)
            notice_txt = notice.notice_body
        else:
            notice_txt = "NOTICE GENERATION BLOCKED BY SAFETY GUARDRAIL: Criminal offense detected. Matter requires police FIR and licensed advocate."
            
        # 4. Save JSON contract
        case_data = {
            "test_case_id": tc["id"],
            "title": tc["title"],
            "input_narrative": tc["narrative"],
            "extracted_case": case.model_dump(),
            "legal_assessment": assessment.model_dump(),
            "has_notice_generated": notice is not None,
            "timestamp": datetime.now().isoformat()
        }
        
        json_path = os.path.join(out_dir, f"{tc['id']}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(case_data, f, indent=2, ensure_ascii=False)
            
        # 5. Save Legal Notice / Safety Escalation TXT
        txt_path = os.path.join(out_dir, f"{tc['id']}_output.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(f"=== NYAYAMITRA RAW OUTPUT FOR {tc['id'].upper()} ===\n")
            f.write(f"CATEGORY: {case.category.value}\n")
            f.write(f"STANDING: {assessment.standing_strength}\n")
            f.write(f"SUMMARY: {assessment.summary_verdict}\n\n")
            f.write("=== STATUTORY ACTION ROADMAP ===\n")
            for step in assessment.action_roadmap:
                f.write(f"{step}\n")
            f.write("\n=== DRAFT NOTICE / LEGAL ESCALATION ===\n")
            f.write(notice_txt)
            
        summary_report.append({
            "id": tc["id"],
            "category": case.category.value,
            "standing": assessment.standing_strength,
            "amount": case.disputed_amount,
            "time_barred_flag": case.is_time_barred_risk
        })
        print(f"  -> Saved {tc['id']}.json and {tc['id']}_output.txt")

    # Save summary index
    index_path = os.path.join(out_dir, "00_TEST_RUN_SUMMARY.json")
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(summary_report, f, indent=2)
        
    print(f"\nAll test cases executed successfully! Outputs stored in: {out_dir}")


if __name__ == "__main__":
    run_all_tests()
