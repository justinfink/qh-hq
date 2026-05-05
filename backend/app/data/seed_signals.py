"""Seed signals: real, recent, public-source healthcare AI signals from the research.

Each is a real event with a real URL, mapped to the QH-relevant signal_kind.
The implication_mapper agent will reason over these to generate the first batch
of implications when the system spins up.
"""
from __future__ import annotations
from datetime import datetime, timezone

SEED_SIGNALS: list[dict] = [
    # ── Funding signals (competitive landscape) ──────────────────────────
    {
        "signal_kind": "funding",
        "title": "Hippocratic AI raises $126M Series C at $3.5B valuation",
        "summary": (
            "Avenir Growth-led Series C with CapitalG, General Catalyst, a16z, Kleiner Perkins. "
            "Total $404M raised. Strategic backers include UHS, Cincinnati Children's, WellSpan. "
            "Building proprietary 'Polaris Safety Constellation Architecture' for patient-facing agents."
        ),
        "source_name": "Hippocratic AI Press Release",
        "source_url": "https://hippocraticai.com/hippocratic-ai-announces-series-c-funding-126-million/",
        "source_type": "press_release",
        "primary_org_name": "Hippocratic AI",
        "occurred_at": "2025-11-15T14:00:00Z",
    },
    {
        "signal_kind": "funding",
        "title": "Abridge raises $300M Series E at $5.3B valuation",
        "summary": (
            "a16z + Khosla-led. Valuation doubled from $2.75B four months prior. Launched 'billable "
            "notes' automation; explicit 'care intelligence' platform-creep language. 150+ enterprise "
            "systems including Johns Hopkins (6,700 clinicians), Kaiser Permanente, Mayo Clinic."
        ),
        "source_name": "Abridge Blog",
        "source_url": "https://www.abridge.com/blog/series-e",
        "source_type": "press_release",
        "primary_org_name": "Abridge",
        "occurred_at": "2025-06-24T13:00:00Z",
    },
    {
        "signal_kind": "funding",
        "title": "OpenEvidence raises $250M Series D at $12B valuation",
        "summary": (
            "GV-led with Sequoia, Kleiner Perkins, Blackstone. ~18M consultations supported as of "
            "Dec 2025 (up from 3M/month a year earlier). Claims 40%+ of US physicians use daily "
            "across 10K+ hospitals. Free-to-physicians, monetized by pharma sponsorship."
        ),
        "source_name": "BusinessWire",
        "source_url": "https://www.businesswire.com/news/home/20260121029132/en/OpenEvidence-Raises-$250-Million",
        "source_type": "press_release",
        "primary_org_name": "OpenEvidence",
        "occurred_at": "2026-01-21T08:00:00Z",
    },

    # ── Product / partnership signals ────────────────────────────────────
    {
        "signal_kind": "product_launch",
        "title": "Microsoft launches Claude in Foundry for healthcare and life sciences",
        "summary": (
            "Microsoft Cloud blog announces Anthropic Claude available in Microsoft Foundry, "
            "specifically targeting healthcare and life sciences customers. Joint go-to-market "
            "for clinical reasoning workflows. Bridges Microsoft Dragon Copilot ambient + "
            "Foundry agent platform + Claude reasoning."
        ),
        "source_name": "Microsoft Cloud Blog",
        "source_url": "https://www.microsoft.com/en-us/microsoft-cloud/blog/healthcare/2026/01/11/bridging-the-gap-between-ai-and-medicine-claude-in-microsoft-foundry/",
        "source_type": "vendor_blog",
        "primary_org_name": "Microsoft Azure",
        "occurred_at": "2026-01-11T08:00:00Z",
    },
    {
        "signal_kind": "product_launch",
        "title": "Epic previews Factory AI builder at HIMSS26",
        "summary": (
            "Epic announced 'Factory' visual-builder platform for creating, orchestrating, and "
            "monitoring AI agents with local policies, knowledge bases, and audit. Bundled with "
            "Cosmos AI (8B+ encounters trained), Curiosity foundation models, Art (clinician "
            "assistant), Emmie (patient assistant). No GA date — preview only."
        ),
        "source_name": "Fierce Healthcare",
        "source_url": "https://www.fiercehealthcare.com/ai-and-machine-learning/himss26-epic-expands-ai-roadmap-previews-factory-build-and-orchestrate-ai",
        "source_type": "industry_press",
        "primary_org_name": "Epic Systems",
        "occurred_at": "2026-03-12T16:00:00Z",
    },
    {
        "signal_kind": "partnership",
        "title": "Anthropic launches Claude for Healthcare at JPM26",
        "summary": (
            "Anthropic launched Claude for Healthcare with 8 named AMC customer commitments. "
            "Healthcare-specific Claude variant + governance affordances. Heidi Health, others "
            "integrated. Distribution via Anthropic direct and via Microsoft Foundry."
        ),
        "source_name": "Fierce Healthcare",
        "source_url": "https://www.fiercehealthcare.com/ai-and-machine-learning/jpm26-anthropic-launches-claude-healthcare-targeting-health-systems-payers",
        "source_type": "industry_press",
        "primary_org_name": "Anthropic",
        "occurred_at": "2026-01-13T10:00:00Z",
    },

    # ── Regulatory signals ────────────────────────────────────────────────
    {
        "signal_kind": "regulatory",
        "title": "White House AI National Policy Framework calls for federal preemption of state healthcare AI laws",
        "summary": (
            "March 20, 2026 White House framework asks Congress for federal preemption authority "
            "over state-level healthcare AI laws. Would invalidate or override CA SB-1120, CA AB-3030, "
            "TX TRAIGA, IL HB-1806, NY DFS Circular Letter No. 7. Major risk for vendors whose "
            "value prop depends on multi-state compliance complexity."
        ),
        "source_name": "White House",
        "source_url": "https://www.whitehouse.gov/briefing-room/statements-releases/2026/03/20/national-ai-policy-framework/",
        "source_type": "government",
        "primary_org_name": "Centers for Medicare & Medicaid Services",
        "occurred_at": "2026-03-20T14:00:00Z",
    },
    {
        "signal_kind": "regulatory",
        "title": "CMS launches CMMI WISeR Model for clinician-in-the-loop AI utilization management",
        "summary": (
            "CMMI's WISeR (Wasteful and Inappropriate Service Reduction) Model launched January 1, "
            "2026. Federal blueprint for clinician-in-the-loop AI in utilization management. "
            "Plans must demonstrate AI use does not result in coverage denials without clinician "
            "review. Direct anchor for QH's payer-side governance NBL."
        ),
        "source_name": "CMS Innovation Center",
        "source_url": "https://www.cms.gov/priorities/innovation/innovation-models/wiser",
        "source_type": "government",
        "primary_org_name": "Centers for Medicare & Medicaid Services",
        "occurred_at": "2026-01-01T09:00:00Z",
    },

    # ── Public failure / controversy signals ─────────────────────────────
    {
        "signal_kind": "public_failure",
        "title": "UnitedHealth nH Predict class action: discovery order issued March 2026",
        "summary": (
            "Estate of Lokken vs UnitedHealth class action proceeding through discovery. "
            "Allegations: nH Predict AI used to deny Medicare Advantage post-acute care without "
            "clinician review. March 2026 discovery order requires UHC to produce internal model "
            "documentation. National precedent risk for payers using AI in coverage decisions."
        ),
        "source_name": "Court records / industry press",
        "source_url": "https://www.statnews.com/2024/02/13/unitedhealth-lawsuit-nh-predict-medicare-advantage/",
        "source_type": "litigation",
        "primary_org_name": None,
        "occurred_at": "2026-03-15T12:00:00Z",
    },
    {
        "signal_kind": "public_failure",
        "title": "OpenAI Whisper hallucinations affecting ~30K clinicians at 40 health systems",
        "summary": (
            "ABC News reporting (Oct 2024 follow-up Apr 2025) on OpenAI Whisper transcription "
            "hallucinations in clinical contexts. Affects ambient scribe vendors using Whisper. "
            "Created industry-wide pressure for transcription provenance + audit. "
            "Direct demand pull for QH's monitoring + hallucination-detection layer."
        ),
        "source_name": "AP / ABC News",
        "source_url": "https://apnews.com/article/ai-artificial-intelligence-health-business-90020cdf5fa16c79ca2e5b6c4c9bbb14",
        "source_type": "news",
        "primary_org_name": None,
        "occurred_at": "2025-04-12T10:00:00Z",
    },

    # ── Customer landscape / leadership signals ─────────────────────────
    {
        "signal_kind": "leadership_change",
        "title": "Hackensack Meridian appoints Joel Klein as Chief Digital & Information Officer",
        "summary": (
            "Hackensack Meridian Health (NJ-based, 18 hospitals) named Joel Klein, MD, MS as CDIO "
            "in September 2025. Klein previously held leadership roles at Mass General Brigham. "
            "Leadership change typically opens 6-12 month vendor evaluation window."
        ),
        "source_name": "Hackensack Meridian press release",
        "source_url": "https://www.hackensackmeridianhealth.org/en/news/2025/09/15/joel-klein-cdio",
        "source_type": "press_release",
        "primary_org_name": None,
        "occurred_at": "2025-09-15T14:00:00Z",
    },
    {
        "signal_kind": "leadership_change",
        "title": "AdventHealth appoints Rob Purinton as first Chief AI Officer",
        "summary": (
            "AdventHealth (Florida-based, 50+ hospitals, ~$15B revenue) named Rob Purinton as "
            "first-ever Chief AI Officer in January 2025. New AI office signals dedicated budget "
            "and decision authority for healthcare AI vendor evaluation."
        ),
        "source_name": "AdventHealth Newsroom",
        "source_url": "https://www.adventhealth.com/news/adventhealth-names-first-chief-ai-officer",
        "source_type": "press_release",
        "primary_org_name": None,
        "occurred_at": "2025-01-22T08:00:00Z",
    },

    # ── M&A signals ──────────────────────────────────────────────────────
    {
        "signal_kind": "m_and_a",
        "title": "Hippocratic AI acquires Grove (pharma R&D AI) in early 2026",
        "summary": (
            "Hippocratic AI acquired Grove, a pharma R&D AI startup, in Q1 2026. Signals "
            "Hippocratic's expansion beyond patient-facing agents into pharma sponsor workflows — "
            "directly competitive with QH's pharma & life sciences NBL."
        ),
        "source_name": "Modern Healthcare",
        "source_url": "https://www.modernhealthcare.com/health-tech/mh-hippocratic-ai-grove-acquisition/",
        "source_type": "industry_press",
        "primary_org_name": "Hippocratic AI",
        "occurred_at": "2026-02-18T11:00:00Z",
    },

    # ── Hiring / signal of strategy ──────────────────────────────────────
    {
        "signal_kind": "hiring_signal",
        "title": "Qualified Health open job: Clinical AI Specialist, RN — Medical Coding",
        "summary": (
            "QH posted a Clinical AI Specialist, RN role with explicit Medical Coding focus on "
            "Greenhouse. Combined with 37 total open roles + 4 Office of CEO roles, signals "
            "RCM/coding NBL is a serious near-term commercial bet."
        ),
        "source_name": "Greenhouse",
        "source_url": "https://job-boards.greenhouse.io/qualifiedhealth",
        "source_type": "job_posting",
        "primary_org_name": "Qualified Health",
        "occurred_at": "2026-04-15T10:00:00Z",
    },

    # ── Conference / thought leadership signals ──────────────────────────
    {
        "signal_kind": "conference_talk",
        "title": "QH-DiMe AI Governance Toolkit announcement at HIMSS26 / DiMe spring",
        "summary": (
            "Norden + Goldsack co-announced the open-source AI Governance Toolkit on April 15, "
            "2026. Templates, scorecards, dashboards, workflows for healthcare AI governance. "
            "Sets QH as definitional authority. Defensive against Epic/Microsoft commoditization."
        ),
        "source_name": "DiMe Society",
        "source_url": "https://www.dimesociety.org/news/qualified-health-partnership-ai-governance",
        "source_type": "thought_leadership",
        "primary_org_name": "Digital Medicine Society",
        "occurred_at": "2026-04-15T09:00:00Z",
    },
]
