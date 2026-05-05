"""Seed implications. Hand-crafted reasoning that maps each seed signal to its
QH-specific implication, severity, and recommended action — using the relationship
dynamics layer as substrate. These are what news_scout + implication_mapper would
produce when actually run; we seed them so the terminal lights up before agent runs.

Each implication is grounded in research-backed facts, not inventions.
"""
from __future__ import annotations

# Indexed by signal source_url for lookup at seed-time
SEED_IMPLICATIONS: list[dict] = [
    # Hippocratic AI Series C
    {
        "signal_source_url": "https://hippocraticai.com/hippocratic-ai-announces-series-c-funding-126-million/",
        "initiative_code": "NBL-MARKETPLACE",
        "customer_org_name": None,
        "severity": "high",
        "confidence_score": 0.85,
        "headline": "Hippocratic's $126M war chest accelerates the Polaris-as-governance threat to QH's marketplace pitch",
        "reasoning": (
            "Hippocratic doubled its capital base just as QH's anchor partnership negotiation enters Week 3 of legal "
            "review. Polaris Safety Constellation Architecture is explicitly competitive framing with QH's governance "
            "layer. The strategic bet behind the marketplace NBL — that vendors prefer multi-system distribution via "
            "QH over building their own governance — gets harder when a $3.5B-valuation competitor has the patient "
            "capital to vertically integrate. Marketplace partnership probability declines if Hippocratic chooses to "
            "build their own platform instead of partnering."
        ),
        "recommended_action": (
            "Norden + Munjal Shah 1:1 by 5/9 to break the legal tie or formally exit the partnership. "
            "Continued silence costs us optionality on every other anchor vendor."
        ),
        "recommended_owner": "CEO",
        "recommended_by_date": "2026-05-09",
    },
    # Abridge Series E
    {
        "signal_source_url": "https://www.abridge.com/blog/series-e",
        "initiative_code": "NBL-MARKETPLACE",
        "customer_org_name": "Mayo Clinic",
        "severity": "high",
        "confidence_score": 0.8,
        "headline": "Abridge 'care intelligence' framing is the platform-creep we modeled — Mayo and Kaiser exposure",
        "reasoning": (
            "Abridge's explicit pivot from documentation to 'care intelligence' is the platform-creep pattern we flagged. "
            "Mayo Clinic (2,000+ physicians + nursing pilots) and Kaiser (24,600 physicians) are both Abridge enterprise "
            "customers AND on QH's prospect list. If Abridge ships embedded governance/audit features, our 'cross-vendor "
            "governance' pitch loses force at exactly these accounts. The MARKETPLACE NBL design partner narrative gets "
            "harder if the dominant ambient vendor is pulling governance in-house."
        ),
        "recommended_action": (
            "Mate to schedule call with John Halamka (Mayo Platform) by 5/20. Frame: 'Abridge owns the documentation "
            "layer; you need a separate governance backbone for the rest of your AI portfolio.' Use the multi-vendor "
            "thesis as the explicit hook."
        ),
        "recommended_owner": "CMO",
        "recommended_by_date": "2026-05-20",
    },
    # OpenEvidence Series D
    {
        "signal_source_url": "https://www.businesswire.com/news/home/20260121029132/en/OpenEvidence-Raises-$250-Million",
        "initiative_code": "STRAT-EPIC",
        "customer_org_name": None,
        "severity": "medium",
        "confidence_score": 0.75,
        "headline": "OpenEvidence at $12B is the canonical 'shadow AI' problem QH governance solves — concrete demo",
        "reasoning": (
            "40%+ of US physicians using OpenEvidence daily on personal devices is THE archetypal shadow-AI problem "
            "for hospital CIOs: a clinical tool with $12B of capital behind it, unmanaged, used in patient-facing "
            "decisions, with no audit trail visible to compliance. This is a near-perfect concrete example for the "
            "Epic counter-positioning: Epic Factory cannot govern OpenEvidence (it's not Epic-native). QH's shadow-AI "
            "inventory + governance layer is the only credible answer."
        ),
        "recommended_action": (
            "Norden to draft 1-page positioning brief: 'OpenEvidence and the shadow-AI inventory case' for "
            "multi-EHR target conversations (CommonSpirit, HCA, Northwell). Ready by 5/15 for Q3 outbound."
        ),
        "recommended_owner": "CEO",
        "recommended_by_date": "2026-05-15",
    },
    # Microsoft Foundry + Claude
    {
        "signal_source_url": "https://www.microsoft.com/en-us/microsoft-cloud/blog/healthcare/2026/01/11/bridging-the-gap-between-ai-and-medicine-claude-in-microsoft-foundry/",
        "initiative_code": "NBL-MARKETPLACE",
        "customer_org_name": "Microsoft Azure",
        "severity": "critical",
        "confidence_score": 0.85,
        "headline": "Microsoft Foundry + Claude direct distribution risks disintermediating QH's healthcare-Anthropic stack",
        "reasoning": (
            "Microsoft now distributes Claude directly to healthcare customers via Foundry. This is the headwind we "
            "flagged on the Anthropic relationship — model-layer disintermediation through a cloud channel. If a CIO's "
            "default path becomes 'Foundry + Dragon Copilot + Claude,' QH's healthcare-native governance has to win "
            "against Microsoft bundling. Anthology Fund alignment provides structural protection but does not block "
            "this distribution path. Multi-cloud + healthcare-specificity become the only credible counter-positioning."
        ),
        "recommended_action": (
            "Norden to escalate with Anthropic exec sponsor (use Anthology Fund relationship): clarify joint "
            "GTM motion on healthcare to ensure QH is the named governance layer in Foundry healthcare deals."
        ),
        "recommended_owner": "CEO",
        "recommended_by_date": "2026-05-12",
    },
    # Epic Factory
    {
        "signal_source_url": "https://www.fiercehealthcare.com/ai-and-machine-learning/himss26-epic-expands-ai-roadmap-previews-factory-build-and-orchestrate-ai",
        "initiative_code": "STRAT-EPIC",
        "customer_org_name": "Epic Systems",
        "severity": "critical",
        "confidence_score": 0.9,
        "headline": "Epic Factory at HIMSS26 is preview-only — first-mover window is now until GA (estimated 2026 Q4)",
        "reasoning": (
            "Epic Factory's HIMSS26 unveiling targets exactly QH's positioning — visual builder for AI agents with "
            "audit + policy + local-knowledge layers. The good news: still preview, no GA date. The bad news: once "
            "Epic ships, the path-of-least-resistance for ~40% of acute care will close. The CommonSpirit-style "
            "multi-EHR play is the only durable wedge. Need a public multi-EHR reference customer signed before "
            "Epic Factory GA to make the differentiator real, not theoretical."
        ),
        "recommended_action": (
            "Phatakwala + Norden joint push on CommonSpirit (Daniel Barchi). Goal: signed pilot agreement by 7/15 to "
            "publish ahead of Epic Factory GA. Use Mercy reference as Catholic-network credibility bridge."
        ),
        "recommended_owner": "CCO + CEO",
        "recommended_by_date": "2026-07-15",
    },
    # Anthropic Claude for Healthcare
    {
        "signal_source_url": "https://www.fiercehealthcare.com/ai-and-machine-learning/jpm26-anthropic-launches-claude-healthcare-targeting-health-systems-payers",
        "initiative_code": "NBL-PHARMA",
        "customer_org_name": "Anthropic",
        "severity": "high",
        "confidence_score": 0.8,
        "headline": "Anthropic's Claude for Healthcare — partner-or-competitor depends on which vertical lanes Anthropic owns",
        "reasoning": (
            "Anthropic launching healthcare-direct with 8 named AMC commitments is the dual-use signal we modeled. "
            "Tailwind: deeper joint roadmap; QH's UT System work becomes a reference. Headwind: Anthropic could pick "
            "preferred 'partner of record' per vertical, and we are not yet that named partner for pharma — exactly "
            "the NBL-PHARMA territory we are entering. Need to lock joint pharma sponsorship messaging before "
            "Anthropic establishes their own pharma account team without us."
        ),
        "recommended_action": (
            "Mate to broker a 30-min Norden + Anthropic healthcare lead call by 5/18. Goal: explicit alignment that "
            "QH is the governance partner for any pharma sponsor evaluating Claude for trial workflows."
        ),
        "recommended_owner": "CMO",
        "recommended_by_date": "2026-05-18",
    },
    # White House preemption framework — CRITICAL
    {
        "signal_source_url": "https://www.whitehouse.gov/briefing-room/statements-releases/2026/03/20/national-ai-policy-framework/",
        "initiative_code": "NBL-PAYER",
        "customer_org_name": "Centers for Medicare & Medicaid Services",
        "severity": "critical",
        "confidence_score": 0.9,
        "headline": "Federal preemption framework would gut QH's state-tracking compliance value prop — single biggest external risk",
        "reasoning": (
            "The 3/20 White House framework asks Congress for federal preemption authority over state healthcare AI laws. "
            "Today, QH's compliance product derives meaningful value from cross-walking 47-state-bill complexity — that "
            "story collapses if federal preemption passes. The good news: Congress is unlikely to act before Q4 2026, "
            "giving 6+ months. The harder read: even the THREAT of preemption changes how CIOs evaluate state-compliance "
            "ROI. Strategic implication: shift positioning emphasis from state-by-state cross-walks to HTI-1 + CHAI ARP "
            "+ Joint Commission RUHD primitives, which are federally durable regardless of preemption outcome."
        ),
        "recommended_action": (
            "Norgeot + Slavitt (advisor, ex-CMS) to assess preemption likelihood by 5/20. Norden to commission strategic "
            "messaging refresh for federal-durable positioning by 6/1."
        ),
        "recommended_owner": "Chief AI Officer + CEO",
        "recommended_by_date": "2026-06-01",
    },
    # CMMI WISeR Model
    {
        "signal_source_url": "https://www.cms.gov/priorities/innovation/innovation-models/wiser",
        "initiative_code": "NBL-PAYER",
        "customer_org_name": "Centers for Medicare & Medicaid Services",
        "severity": "high",
        "confidence_score": 0.85,
        "headline": "CMMI WISeR is the federal blueprint that anchors NBL-PAYER positioning — first-mover credibility window",
        "reasoning": (
            "WISeR's clinician-in-the-loop AI utilization mgmt requirements are essentially a federal spec for what QH's "
            "payer-side governance product should be. Patrick Conway (advisor, ex-CMMI Director) gives us insider context "
            "on first-cohort health plans. Strategic positioning resolution: lead WITH WISeR compliance (not IRO appeal "
            "defensibility) — federal anchor is more durable than state-by-state."
        ),
        "recommended_action": (
            "Norgeot to formalize WISeR-anchored positioning by 5/22 (resolves the blocker on NBL-PAYER product roadmap). "
            "Conway-mediated intro to first-cohort plans."
        ),
        "recommended_owner": "Chief AI Officer",
        "recommended_by_date": "2026-05-22",
    },
    # UnitedHealth nH Predict lawsuit
    {
        "signal_source_url": "https://www.statnews.com/2024/02/13/unitedhealth-lawsuit-nh-predict-medicare-advantage/",
        "initiative_code": "NBL-PAYER",
        "customer_org_name": None,
        "severity": "high",
        "confidence_score": 0.8,
        "headline": "UHC nH Predict discovery order is the demand-pull catalyst for compliance-led NBL-PAYER outreach",
        "reasoning": (
            "March 2026 discovery order forces UHC to produce internal AI documentation. Every other top-7 payer is "
            "watching to assess their own exposure. This is the procurement catalyst: compliance leadership at "
            "Anthem, Humana, Cigna, Aetna will be asked by their boards in the next 90 days 'do we have defensible "
            "audit trails for our utilization mgmt AI?' QH's payer-side product is the answer if positioned now."
        ),
        "recommended_action": (
            "Norgeot to send breach-readiness one-pager to compliance leadership at top-7 plans by 5/15. Use "
            "Norgeot's ex-Elevance lineage for Anthem warm intro to compliance leadership (currently 12-day silence)."
        ),
        "recommended_owner": "Chief AI Officer",
        "recommended_by_date": "2026-05-15",
    },
    # OpenAI Whisper hallucinations
    {
        "signal_source_url": "https://apnews.com/article/ai-artificial-intelligence-health-business-90020cdf5fa16c79ca2e5b6c4c9bbb14",
        "initiative_code": "NBL-MARKETPLACE",
        "customer_org_name": None,
        "severity": "medium",
        "confidence_score": 0.75,
        "headline": "Whisper hallucinations across 30K clinicians at 40 systems = direct demand pull for QH monitoring layer",
        "reasoning": (
            "Whisper hallucinations affecting clinicians using ambient scribe products is the most concrete example of "
            "why the marketplace + monitoring product matters. Use as content marketing wedge for the NBL-MARKETPLACE "
            "positioning: 'when a foundation-model failure hits the clinical workflow, you need provenance + monitoring "
            "across vendors, not single-vendor assurance.'"
        ),
        "recommended_action": (
            "Norgeot to publish 'Whisper hallucinations and the case for cross-vendor monitoring' blog post by 5/29. "
            "Coordinate with DiMe co-distribution."
        ),
        "recommended_owner": "Chief AI Officer",
        "recommended_by_date": "2026-05-29",
    },
    # Hackensack Meridian Joel Klein hire
    {
        "signal_source_url": "https://www.hackensackmeridianhealth.org/en/news/2025/09/15/joel-klein-cdio",
        "initiative_code": "STRAT-EPIC",
        "customer_org_name": None,
        "severity": "medium",
        "confidence_score": 0.7,
        "headline": "Hackensack Meridian's new CDIO opens a vendor evaluation window — Tier-1 prospect activation moment",
        "reasoning": (
            "Joel Klein joining as CDIO (from Mass General Brigham) opens the typical 6-12 month vendor evaluation "
            "window. Hackensack Meridian (18 hospitals, NJ) is exactly the multi-EHR mid-large system QH's wedge "
            "addresses. Klein's MGB lineage suggests AI-native procurement instincts."
        ),
        "recommended_action": (
            "Phatakwala to send positioning email to Joel Klein by 5/20. Use Mate's MGB academic network for warm "
            "intro path."
        ),
        "recommended_owner": "CCO",
        "recommended_by_date": "2026-05-20",
    },
    # AdventHealth first CAIO
    {
        "signal_source_url": "https://www.adventhealth.com/news/adventhealth-names-first-chief-ai-officer",
        "initiative_code": "NBL-RCM",
        "customer_org_name": None,
        "severity": "medium",
        "confidence_score": 0.7,
        "headline": "AdventHealth's first CAIO Rob Purinton = budget unlock for AI governance procurement",
        "reasoning": (
            "First-ever CAIO at a $15B system means dedicated AI budget, decision authority, and a brief from "
            "leadership to evaluate vendors. Adventist health systems align with QH's PBC mission. "
            "RCM-led entry with the new CAIO has the highest CFO-friendly ROI story for first conversation."
        ),
        "recommended_action": (
            "Phatakwala to add AdventHealth (Rob Purinton) to Q3 prospect list. RCM coding agent demo as opener."
        ),
        "recommended_owner": "CCO",
        "recommended_by_date": "2026-06-15",
    },
    # Hippocratic acquires Grove
    {
        "signal_source_url": "https://www.modernhealthcare.com/health-tech/mh-hippocratic-ai-grove-acquisition/",
        "initiative_code": "NBL-PHARMA",
        "customer_org_name": "Hippocratic AI",
        "severity": "high",
        "confidence_score": 0.8,
        "headline": "Hippocratic's Grove acquisition = direct expansion into NBL-PHARMA territory before QH design partners locked",
        "reasoning": (
            "Grove (pharma R&D AI) acquisition signals Hippocratic moving into pharma sponsor workflows — the same "
            "territory NBL-PHARMA targets. Critical that we lock Pfizer or AstraZeneca as design partner before "
            "Hippocratic's pharma motion crystallizes. Mate's Lidia Fonseca intro path becomes more time-sensitive."
        ),
        "recommended_action": (
            "Mate to expedite Pfizer 1-pager to 5/8 (already on critical path). Add explicit competitive context "
            "to the brief: 'Hippocratic acquired Grove; QH is the cross-vendor governance answer for pharma AI.'"
        ),
        "recommended_owner": "CMO",
        "recommended_by_date": "2026-05-08",
    },
    # QH RN Coding hiring signal
    {
        "signal_source_url": "https://job-boards.greenhouse.io/qualifiedhealth",
        "initiative_code": "NBL-RCM",
        "customer_org_name": "Qualified Health",
        "severity": "low",
        "confidence_score": 0.6,
        "headline": "Internal RCM coding role posting validates NBL-RCM as a real near-term commercial bet",
        "reasoning": (
            "37 open roles + Clinical AI Specialist RN (Medical Coding) + 4 Office of CEO roles is a coordinated "
            "signal that NBL-RCM has executive air cover and dedicated headcount. Confidence on RCM thesis upgraded."
        ),
        "recommended_action": "Continue to track Greenhouse for additional NBL-coded roles as forward-looking commercial signal.",
        "recommended_owner": "Office of CEO",
        "recommended_by_date": None,
    },
    # DiMe Toolkit
    {
        "signal_source_url": "https://www.dimesociety.org/news/qualified-health-partnership-ai-governance",
        "initiative_code": "PARTNER-DIME",
        "customer_org_name": "Digital Medicine Society",
        "severity": "medium",
        "confidence_score": 0.75,
        "headline": "DiMe co-authored toolkit announcement is the definitional-authority play landed — sets QH up for 2027 ARP",
        "reasoning": (
            "Norden + Goldsack co-byline establishes QH as definitional authority for healthcare AI governance. "
            "Strategic implication: this is the credibility runway for the CHAI ARP submission — without DiMe-shaped "
            "primitives publicly attributed to QH, the ARP application is harder to differentiate from Signal1, LensAI, "
            "ALIGNMT AI, Ferrum, ModelOp."
        ),
        "recommended_action": (
            "Norgeot to start CHAI ARP scoping conversation by 5/30. Use DiMe toolkit as differentiator for "
            "submission narrative."
        ),
        "recommended_owner": "Chief AI Officer",
        "recommended_by_date": "2026-05-30",
    },
]
