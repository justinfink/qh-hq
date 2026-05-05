"""Initiatives and workstreams. Sourced from QH research signals:
- Open job postings (e.g. "Clinical AI Specialist, RN — Medical Coding")
- Public NBL hints from leadership content
- Strategic moves implied by Series B positioning
- DiMe partnership scope
- Competitive whitespace from regulatory + competitive analysis
"""
from __future__ import annotations
from datetime import date

INITIATIVES: list[dict] = [
    {
        "code": "NBL-RCM",
        "name": "Medical Coding & RCM Automation",
        "kind": "nbl",
        "thesis": (
            "Native medical coding agent embedded in QH governance layer. Open RN coding role "
            "+ Suki/Abridge moves into E&M coding signal market shift. RCM is the cleanest "
            "ROI story for health system CFOs and the most defensible NBL against Commure's "
            "RCM-led OS positioning."
        ),
        "stage": "pilot",
        "confidence": "high",
        "velocity": "accelerating",
        "primary_owner": "Shantanu Phatakwala (CCO)",
        "exec_sponsor": "Justin Norden (CEO)",
        "fte_allocated": 4.5,
        "spend_quarterly_usd": 850_000,
        "target_revenue_year_one_usd": 8_000_000,
        "target_design_partners": 3,
        "current_design_partners": 1,
        "top_blocker": "Need 2 more named design partners by end of Q3 2026 to validate value-based pricing model.",
        "next_milestone": "UTMB coding pilot Phase 2 results readout",
        "next_milestone_date": date(2026, 6, 12),
        "metadata": {
            "evidence": ["Greenhouse: Clinical AI Specialist RN (Medical Coding)", "Suki KLAS validation on E&M coding"],
            "competitive_overlap": ["Commure (RCM lead)", "Suki (E&M coding)"],
        },
    },
    {
        "code": "NBL-PAYER",
        "name": "Payer-Side AI Audit & UM Governance",
        "kind": "nbl",
        "thesis": (
            "Build the regulator-ready audit layer for payers running AI on prior auth and "
            "utilization mgmt. Anchor on CMMI WISeR Model (eff. Jan 1, 2026) as the federal "
            "blueprint for clinician-in-the-loop AI UM. Norgeot's Elevance VP-AI lineage opens "
            "the natural pilot doors. UnitedHealth nH Predict + Cigna PXDX class actions create "
            "demand pull from compliance leadership across the top-7 national plans."
        ),
        "stage": "greenlight",
        "confidence": "high",
        "velocity": "accelerating",
        "primary_owner": "Beau Norgeot (Chief AI Officer)",
        "exec_sponsor": "Justin Norden (CEO)",
        "fte_allocated": 2.0,
        "spend_quarterly_usd": 400_000,
        "target_revenue_year_one_usd": 5_000_000,
        "target_design_partners": 2,
        "current_design_partners": 0,
        "top_blocker": "Strategic positioning — lead with CMMI WISeR compliance OR with operational defensibility for IRO appeals. Each implies a different first-customer profile.",
        "next_milestone": "Anthem (Elevance) compliance leadership intro by Norgeot",
        "next_milestone_date": date(2026, 5, 22),
        "metadata": {
            "evidence": ["CMS-4201-F", "CMMI WISeR launch Jan 2026", "Estate of Lokken vs UHC", "Cigna PXDX class action"],
            "competitive_overlap": ["Cohere Health (payer lead)"],
            "warm_intro": "Norgeot ex-VP AI Elevance",
        },
    },
    {
        "code": "NBL-PHARMA",
        "name": "Pharma & Life-Sciences Clinical AI Governance",
        "kind": "nbl",
        "thesis": (
            "Pharma sponsors deploying LLMs in patient-facing trial recruitment, eligibility "
            "screening, protocol search. Need defensible governance against FDA AI guidance + "
            "21 CFR Part 11 audit + IRB scrutiny. Higher contract values, longer cycles than "
            "provider side. DIA partnership + DiMe bridge are natural channels. Mate's IHI "
            "lineage provides quality framework credibility."
        ),
        "stage": "greenlight",
        "confidence": "high",
        "velocity": "accelerating",
        "primary_owner": "Kedar Mate, MD (CMO)",
        "exec_sponsor": "Justin Norden (CEO)",
        "fte_allocated": 1.5,
        "spend_quarterly_usd": 300_000,
        "target_revenue_year_one_usd": 6_000_000,
        "target_design_partners": 2,
        "current_design_partners": 0,
        "top_blocker": "Need 2 named design partners (target: Pfizer + AstraZeneca) before scaling spend.",
        "next_milestone": "Pfizer CMIO Lidia Fonseca intro via DiMe contact — 1-pager due 5/8",
        "next_milestone_date": date(2026, 5, 8),
        "metadata": {
            "evidence": ["FDA PCCP", "21 CFR Part 11", "DIA Annual abstract pending"],
            "named_targets": ["Pfizer (Lidia Fonseca, CDTO)", "AstraZeneca (Jim Weatherall)", "Lilly (Thomas Fuchs, first CAIO)"],
        },
    },
    {
        "code": "NBL-MARKETPLACE",
        "name": "Governed Model Marketplace",
        "kind": "nbl",
        "thesis": (
            "Third-party clinical AI vendors (ambient scribe, prior auth, sepsis prediction, "
            "etc.) want to ship to health systems but each system's procurement and security "
            "review is a 6-month slog. QH's governed runtime + audit infra = 'App Store with "
            "the security review pre-baked.' Vendor revenue share + system-side seat license. "
            "Direct counter-positioning to Epic Factory (Epic-only) and Commure (RCM-first)."
        ),
        "stage": "greenlight",
        "confidence": "medium",
        "velocity": "slipping",
        "primary_owner": "Beau Norgeot (Chief AI Officer)",
        "exec_sponsor": "Justin Norden (CEO)",
        "fte_allocated": 3.0,
        "spend_quarterly_usd": 600_000,
        "target_revenue_year_one_usd": 4_000_000,
        "target_design_partners": 5,
        "current_design_partners": 0,
        "top_blocker": "Anchor vendor partnership structure with Hippocratic in legal review week 3 — data residency + incident response ownership unresolved. Need exec sponsor by 5/9.",
        "next_milestone": "Hippocratic legal tie-break decision",
        "next_milestone_date": date(2026, 5, 9),
        "metadata": {
            "evidence": ["Hippocratic, Abridge, Suki informal design partner signal"],
            "competitive_overlap": ["Epic Factory (incumbent path)", "Commure (multi-product wedge)"],
        },
    },
    {
        "code": "NBL-ASC",
        "name": "Ambulatory Surgery Center Vertical",
        "kind": "nbl",
        "thesis": (
            "Lighter IT than IDNs, simpler procurement, rising AI scribe + pre-op workflow "
            "adoption. Underpenetrated. Big-5 ASC operators (USPI, Surgery Partners, SCA "
            "Health, AmSurg, HCA-affiliated) are natural anchors. Lower ACV but faster "
            "deployment cycle compensates."
        ),
        "stage": "pilot",
        "confidence": "medium",
        "velocity": "accelerating",
        "primary_owner": "Shantanu Phatakwala (CCO)",
        "exec_sponsor": "Justin Norden (CEO)",
        "fte_allocated": 1.5,
        "spend_quarterly_usd": 200_000,
        "target_revenue_year_one_usd": 2_500_000,
        "target_design_partners": 3,
        "current_design_partners": 1,
        "top_blocker": "Pricing model not yet validated for sub-$50M-revenue ASC groups; current IDN list price is a non-starter.",
        "next_milestone": "Surgery Partners pilot scoping call",
        "next_milestone_date": date(2026, 5, 14),
        "metadata": {},
    },
    {
        "code": "NBL-SPECIALTY",
        "name": "Specialty Practice MSOs (Oncology, Cardiology)",
        "kind": "nbl",
        "thesis": (
            "PE-rolled specialty MSOs are deploying scribes + CDS without enterprise governance. "
            "Single-procurement, 30+ clinic deploy. Anchor on oncology first via Tempus + ASCO "
            "data standards rather than build proprietary mapping."
        ),
        "stage": "greenlight",
        "confidence": "medium",
        "velocity": "accelerating",
        "primary_owner": "Shantanu Phatakwala (CCO)",
        "exec_sponsor": "Justin Norden (CEO)",
        "fte_allocated": 1.0,
        "spend_quarterly_usd": 150_000,
        "target_revenue_year_one_usd": 1_500_000,
        "target_design_partners": 2,
        "current_design_partners": 0,
        "top_blocker": "GTM motion debate — direct to specialty groups vs. via PE-owned MSOs. Two inbound MSO inquiries this week shifted the debate.",
        "next_milestone": "Leadership decision on MSO-led vs. direct",
        "next_milestone_date": date(2026, 5, 12),
        "metadata": {},
    },
    {
        "code": "PARTNER-DIME",
        "name": "DiMe AI Governance Toolkit (Open Source)",
        "kind": "partnership",
        "thesis": (
            "Co-author the open-source AI governance toolkit with DiMe — templates, scorecards, "
            "dashboards, workflows. Sets QH as definitional authority for healthcare AI "
            "governance. Bridges to FDA submission support and CHAI ARP designation. "
            "Defensible against Epic/Microsoft commoditization by being the open standard."
        ),
        "stage": "scaling",
        "confidence": "high",
        "velocity": "accelerating",
        "primary_owner": "Justin Norden (CEO)",
        "exec_sponsor": "Justin Norden (CEO)",
        "fte_allocated": 0.5,
        "spend_quarterly_usd": 75_000,
        "target_revenue_year_one_usd": 0,  # ecosystem play, not direct revenue
        "target_design_partners": 1,
        "current_design_partners": 1,
        "top_blocker": "None — partnership announced 4/15; toolkit v1 in active co-development.",
        "next_milestone": "Toolkit v1 public release",
        "next_milestone_date": date(2026, 7, 1),
        "metadata": {"counter_positioning": ["Epic Factory", "Microsoft Foundry"]},
    },
    {
        "code": "STRAT-CHAI",
        "name": "CHAI Assurance Lab (ARP) Designation",
        "kind": "strategic_project",
        "thesis": (
            "CHAI ARP designation is becoming procurement-gating credential (Signal1, LensAI, "
            "ALIGNMT AI, Ferrum, ModelOp already certified). Joint Commission + CHAI partnership "
            "(June 2025) brings 22K+ accredited orgs into compliance funnel. Defensive priority — "
            "QH must achieve ARP before competitors use it as procurement objection."
        ),
        "stage": "discovery",
        "confidence": "high",
        "velocity": "holding",
        "primary_owner": "Beau Norgeot (Chief AI Officer)",
        "exec_sponsor": "Justin Norden (CEO)",
        "fte_allocated": 0.75,
        "spend_quarterly_usd": 150_000,
        "target_revenue_year_one_usd": 0,
        "target_design_partners": 0,
        "current_design_partners": 0,
        "top_blocker": "Need to confirm scope/cost/timeline of ARP audit. No public pricing.",
        "next_milestone": "CHAI scoping call",
        "next_milestone_date": date(2026, 5, 30),
        "metadata": {
            "competitors_already_certified": ["Signal1", "LensAI", "ALIGNMT AI", "Ferrum", "ModelOp"],
        },
    },
    {
        "code": "STRAT-EPIC",
        "name": "Multi-EHR Counter-Positioning vs Epic Factory",
        "kind": "strategic_project",
        "thesis": (
            "Epic Factory (HIMSS26 preview, no GA) is the single largest existential threat. "
            "QH's wedge: multi-EHR systems (CommonSpirit, HCA, Northwell), non-EHR sources, and "
            "third-party vendor governance Epic won't touch. Build the comparison narrative + "
            "case studies + positioning content before Epic Factory GAs."
        ),
        "stage": "greenlight",
        "confidence": "high",
        "velocity": "accelerating",
        "primary_owner": "Justin Norden (CEO)",
        "exec_sponsor": "Justin Norden (CEO)",
        "fte_allocated": 1.0,
        "spend_quarterly_usd": 200_000,
        "target_revenue_year_one_usd": 0,
        "target_design_partners": 0,
        "current_design_partners": 0,
        "top_blocker": "Need a public CommonSpirit-style multi-EHR reference customer (Epic + Cerner) to make the narrative concrete.",
        "next_milestone": "Multi-EHR reference deal in pipeline",
        "next_milestone_date": date(2026, 7, 15),
        "metadata": {},
    },
]


WORKSTREAMS: list[dict] = [
    # NBL-RCM
    {
        "initiative_code": "NBL-RCM", "kind": "product",
        "status": "Coding agent v1 live at UTMB; Phase 2 expansion to UT Houston scoping",
        "owner": "B. Norgeot",
        "summary": "Native E&M coding agent + governance audit trail. Phase 1 live, Phase 2 scoping.",
        "next_action": "Phase 2 scope freeze + UT Health Houston onboarding plan",
        "next_action_due": date(2026, 6, 1),
        "last_movement_at": "2026-05-02T15:00:00Z",
    },
    {
        "initiative_code": "NBL-RCM", "kind": "gtm",
        "status": "1 design partner live (UTMB); 2 more needed by Q3",
        "owner": "S. Phatakwala",
        "summary": "Active conversations: Mercy, Jefferson. Need value-based pricing model.",
        "next_action": "Pricing v1 + Mercy/Jefferson scoping calls",
        "next_action_due": date(2026, 5, 20),
        "last_movement_at": "2026-04-29T10:00:00Z",
    },
    {
        "initiative_code": "NBL-RCM", "kind": "regulatory",
        "status": "Mapping coding agent to OIG compliance + CMS billing audit guidance",
        "owner": "B. Norgeot",
        "summary": "Coding agents need defensible OIG-friendly audit trail. Scoping with outside counsel.",
        "next_action": "Outside counsel review of audit trail spec",
        "next_action_due": date(2026, 5, 30),
        "last_movement_at": "2026-04-25T14:00:00Z",
    },

    # NBL-PAYER
    {
        "initiative_code": "NBL-PAYER", "kind": "product",
        "status": "Reg-mapping for CMMI WISeR + CMS-4201-F. Not started — on hold pending positioning decision.",
        "owner": "B. Norgeot",
        "summary": "Two distinct PMs needed depending on positioning (state-reg vs IRO-defensibility).",
        "next_action": "Positioning decision + PM assignment",
        "next_action_due": date(2026, 5, 22),
        "last_movement_at": "2026-04-22T11:00:00Z",
    },
    {
        "initiative_code": "NBL-PAYER", "kind": "gtm",
        "status": "Anthem innovation group passed initial intro to compliance leadership. Compliance side has not responded in 12 days.",
        "owner": "B. Norgeot",
        "summary": "Anthem (Elevance) compliance silence. Norgeot has alternate warm-intro path via ex-Elevance network.",
        "next_action": "Re-engage Anthem compliance with positioning brief",
        "next_action_due": date(2026, 5, 16),
        "last_movement_at": "2026-04-25T09:00:00Z",
    },

    # NBL-PHARMA
    {
        "initiative_code": "NBL-PHARMA", "kind": "product",
        "status": "Compliance mapping for FDA draft AI/ML guidance + 21 CFR Part 11. Scoping.",
        "owner": "K. Mate",
        "summary": "2-week internal scope to map QH audit trail to Part 11 e-records. Mostly schema-level.",
        "next_action": "Internal scope readout",
        "next_action_due": date(2026, 5, 16),
        "last_movement_at": "2026-04-28T13:00:00Z",
    },
    {
        "initiative_code": "NBL-PHARMA", "kind": "gtm",
        "status": "Pfizer CMIO Lidia Fonseca open to 30-min intro via DiMe. AstraZeneca clinical innovation flagged interest at HIMSS.",
        "owner": "K. Mate",
        "summary": "Top-20 pharma BD. Lidia Fonseca needs 1-pager by 5/8 to confirm.",
        "next_action": "1-pager for Pfizer + AstraZeneca",
        "next_action_due": date(2026, 5, 8),
        "last_movement_at": "2026-05-01T09:30:00Z",
    },
    {
        "initiative_code": "NBL-PHARMA", "kind": "partnerships",
        "status": "DIA Annual June — abstract submitted for governance panel. Decision pending by 5/12.",
        "owner": "K. Mate",
        "summary": "DIA accreditation gives QH a credibility wedge for pharma sponsors.",
        "next_action": "DIA decision",
        "next_action_due": date(2026, 5, 12),
        "last_movement_at": "2026-04-29T16:00:00Z",
    },

    # NBL-MARKETPLACE
    {
        "initiative_code": "NBL-MARKETPLACE", "kind": "product",
        "status": "Vendor SDK v0 spec ready for internal review. Hippocratic / Abridge / Suki gave informal design partner signal.",
        "owner": "B. Norgeot",
        "summary": "SDK: auth, audit-log emission, model-card schema. v0 in review.",
        "next_action": "Internal SDK review + Hippocratic feedback session",
        "next_action_due": date(2026, 5, 16),
        "last_movement_at": "2026-05-01T11:00:00Z",
    },
    {
        "initiative_code": "NBL-MARKETPLACE", "kind": "gtm",
        "status": "Holding all outbound until partnership structure unblocks. Don't want to commit a partnership we can't honor.",
        "owner": "S. Phatakwala",
        "summary": "Vendor signups paused.",
        "next_action": "Resume outbound after Hippocratic legal closes",
        "next_action_due": date(2026, 5, 9),
        "last_movement_at": "2026-04-24T10:00:00Z",
    },
    {
        "initiative_code": "NBL-MARKETPLACE", "kind": "partnerships",
        "status": "Hippocratic legal review entering week 3. Sticking points: data residency + incident response ownership.",
        "owner": "J. Norden (escalated)",
        "summary": "Need exec sponsor to break tie by 5/9.",
        "next_action": "Norden + Hippocratic CEO 1:1 to break tie",
        "next_action_due": date(2026, 5, 9),
        "last_movement_at": "2026-04-14T14:00:00Z",
    },

    # NBL-ASC
    {
        "initiative_code": "NBL-ASC", "kind": "product",
        "status": "Lightweight onboarding playbook (target: 2-week deploy vs 8-week IDN). In build.",
        "owner": "S. Phatakwala",
        "summary": "Reduced compliance config from 47 fields to 11 by hardcoding ASC-typical workflows. Need security review by 5/9.",
        "next_action": "Security review",
        "next_action_due": date(2026, 5, 9),
        "last_movement_at": "2026-05-02T15:00:00Z",
    },
    {
        "initiative_code": "NBL-ASC", "kind": "gtm",
        "status": "3 ASC group prospects in early conversations: Surgery Partners, USPI, HCA-affiliated.",
        "owner": "S. Phatakwala",
        "summary": "Surgery Partners pilot scoping call set 5/14. Need pricing v1.",
        "next_action": "Pricing v1 by 5/14",
        "next_action_due": date(2026, 5, 14),
        "last_movement_at": "2026-04-30T10:00:00Z",
    },

    # NBL-SPECIALTY
    {
        "initiative_code": "NBL-SPECIALTY", "kind": "gtm",
        "status": "Two inbound MSO inquiries this week (one cardiology PE-owned, one oncology). Switching working hypothesis to MSO-led.",
        "owner": "S. Phatakwala",
        "summary": "Need leadership decision on motion design.",
        "next_action": "Leadership decision on MSO-led vs direct",
        "next_action_due": date(2026, 5, 12),
        "last_movement_at": "2026-05-03T16:00:00Z",
    },
    {
        "initiative_code": "NBL-SPECIALTY", "kind": "product",
        "status": "Oncology workflow scope decision: lean on Flatiron + ASCO data standards rather than build proprietary mapping.",
        "owner": "K. Mate",
        "summary": "Specialty workflow templates (oncology first; treatment planning, tumor board, MRD).",
        "next_action": "Spec readout",
        "next_action_due": date(2026, 5, 23),
        "last_movement_at": "2026-04-30T13:00:00Z",
    },

    # PARTNER-DIME
    {
        "initiative_code": "PARTNER-DIME", "kind": "partnerships",
        "status": "Toolkit v1 in co-development with Goldsack team. Public preview at HIMSS26 was well-received.",
        "owner": "J. Norden",
        "summary": "Open-source AI governance toolkit. Templates + scorecards + dashboards.",
        "next_action": "Toolkit v1 public release",
        "next_action_due": date(2026, 7, 1),
        "last_movement_at": "2026-04-15T09:00:00Z",
    },

    # STRAT-CHAI
    {
        "initiative_code": "STRAT-CHAI", "kind": "regulatory",
        "status": "ARP designation analysis. 5 competitors already certified. Need to scope cost/timeline.",
        "owner": "B. Norgeot",
        "summary": "CHAI ARP designation scope and timeline TBD.",
        "next_action": "CHAI scoping call",
        "next_action_due": date(2026, 5, 30),
        "last_movement_at": "2026-04-20T10:00:00Z",
    },

    # STRAT-EPIC
    {
        "initiative_code": "STRAT-EPIC", "kind": "product",
        "status": "Comparison narrative + case studies in development. Need a multi-EHR reference customer.",
        "owner": "J. Norden",
        "summary": "Multi-EHR + non-EHR + third-party governance is the wedge against Epic Factory.",
        "next_action": "Sign multi-EHR reference customer (CommonSpirit / HCA / Northwell)",
        "next_action_due": date(2026, 7, 15),
        "last_movement_at": "2026-04-22T15:00:00Z",
    },
]
