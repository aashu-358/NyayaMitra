# 3-Minute Walkthrough Video Script (Problem 2: Build an AI Lawyer)
**Candidate:** Aashanvit Kumarchand Janbandhu (Roll No: 23125002, B.Tech DSAI, IIT Roorkee)  
**App:** NyayaMitra — AI Legal Co-Pilot for Everyday Indians  
**Target Duration:** Exactly 2 minutes 45 seconds to 3 minutes.

---

### [0:00 - 0:30] Introduction & The Problem
> *"Hi everyone, my name is Aashanvit Janbandhu, a 3rd-year Data Science and AI student at IIT Roorkee. This is my submission for Problem 2 of the Kuku AI Generalist Assignment: building an AI lawyer for everyday Indians.*
>
> *In India, over 85% of people facing common disputes—like a landlord withholding a ₹60,000 security deposit, or Flipkart refusing a refund for a damaged laptop—never consult a lawyer. Lawyer consultation fees of ₹2,000 to ₹10,000 exceed the disputed amount, and people find the paperwork intimidating.*
>
> *I built **NyayaMitra**: a conversational legal co-pilot that turns messy stories into enforceable legal notices, checks limitation periods, prevents hallucinations, and lets users practise negotiating against an AI opponent."*

---

### [0:30 - 1:15] Demo 1: Conversational Intake & Case Builder (Hinglish Support)
> *(Action: Open the Streamlit web app. Select preset 1: 'Bangalore Landlord Withholding ₹60,000 Deposit' in Hinglish. Click 'Analyze & Build Legal Case'.)*
>
> *"Let's look at a real scenario: a tenant in Bangalore speaking in conversational Hinglish: 'Bhai 60,000 deposit tha, landlord bolta hai painting ka kategi...' The user hasn't quoted any legal sections.*
>
> *When we click 'Analyze & Build Legal Case', NyayaMitra instantly breaks this down into:*
> 1. *Dispute Category: Tenancy Security Deposit.*
> 2. *Exact Claim: ₹60,000.*
> 3. *Structured Chronology: The move-out date, notice date, and handover video.*
> 4. *Evidence Checklist: It notes they have the agreement and video, but flags that they need to demand the landlord's actual painting invoices."*

---

### [1:15 - 1:55] Demo 2: Anti-Hallucination Legal Standing & Court-Ready Notice
> *(Action: Switch to Tab 2 'Legal Standing' then Tab 3 'Draft Legal Notice'.)*
>
> *"In Tab 2, we explain where the citizen stands in plain language. The ground rule of the brief was: 'AI models confidently invent laws and sections—tell us how yours avoids that.'*
>
> *Notice that every statute shown here—Section 108 of the Transfer of Property Act and the Model Tenancy Act—comes from a strictly verified, deterministic legal registry. The LLM is never allowed to hallucinate nonexistent sections.*
>
> *In Tab 3, NyayaMitra generates a court-standard, 15-day Pre-Litigation Legal Notice demanding the principal plus 18% statutory interest. With one click, the citizen can download a professionally styled PDF ready to be dispatched via Indian Speed Post with Acknowledgement Due. In India, over 65% of small civil disputes get settled right at this step."*

---

### [1:55 - 2:30] Demo 3: Opponent Simulator & Safety Guardrail
> *(Action: Switch to Tab 4 'Opponent Simulator', then load Preset 5 'Criminal Assault' in Tab 1 to show the safety circuit breaker.)*
>
> *"In Tab 4, we have the Opponent Simulator. Here, the AI plays the difficult landlord, trying out common bluffs like: 'Walls had marks, it cost ₹25,000, take 50% or go to court.'*
> *Underneath, NyayaMitra exposes the tactic and gives the user coaching tips on what legal clauses to quote to stand firm.*
>
> *Finally, what happens if someone brings a criminal matter or physical assault? If I load Preset 5—where a moneylender threatens violence—the system's deterministic safety circuit breaker immediately halts notice generation, flags it as a criminal emergency, and provides direct hotlines for Police 112 and NALSA free legal aid at 15100."*

---

### [2:30 - 3:00] Conclusion & Scalability
> *"Architecture-wise: We keep natural language empathy in the LLM, but keep statutes, limitations, and safety strictly in deterministic code. At production scale, this costs less than ₹0.35 per case, meaning 100,000 cases cost less than $400 a month.*
>
> *All 13 unedited test outputs, the full test runner, and the 2-page solution PDF are included in the repository. Thank you for your time!"*

