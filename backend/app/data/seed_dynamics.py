"""Relationship dynamics: explicit headwinds/tailwinds per organization-to-QH relationship.

This is the substrate that powers the semantic understanding the implication mapper
reasons against. Without this, the system would treat 'partner' and 'competitor' as
flat labels. With it, the agent can say: 'Anthropic is a partner today, but their
direct healthcare push creates disintermediation risk to QH's Claude-as-substrate
positioning — this signal accelerates that risk by 6 months.'

Each entry maps to an organization by name and is merged into that org's metadata
during seed.
"""
from __future__ import annotations

# Schema for each entry:
# {
#   "org_name": str,                  # exact match to seed_organizations
#   "relationship_strength": 1-10,    # current health
#   "trajectory": "improving" | "stable" | "deteriorating" | "volatile",
#   "strategic_value": "critical" | "high" | "medium" | "low",
#   "tailwinds": list[str],           # forces strengthening the relationship
#   "headwinds": list[str],           # forces weakening the relationship
#   "qh_leverage": list[str],         # what QH controls that helps
#   "qh_exposure": list[str],         # what QH is exposed to / can't control
#   "watch_signals": list[str],       # what to monitor for relationship change
# }

DYNAMICS: list[dict] = [
    # ── ANCHOR CUSTOMERS ─────────────────────────────────────────────────
    {
        "org_name": "University of Texas System",
        "relationship_strength": 9,
        "trajectory": "improving",
        "strategic_value": "critical",
        "tailwinds": [
            "Public $15M run-rate at UTMB validates ROI story for every other prospect",
            "Peter McCaffrey (Chief AI & Digital Officer) is publicly evangelizing QH",
            "Enterprise rollout across 8 institutions = compounding internal champion network",
            "First academic system to deploy HIPAA-compliant AI web search → defining 'first'",
        ],
        "headwinds": [
            "Single-system concentration risk: if UTMB pilot stalls, the public narrative breaks",
            "Texas state AI legislation (TRAIGA, eff 1/1/2026) adds compliance load to a flagship",
            "Anthropic-direct relationship may eventually let UT System bypass QH's substrate",
        ],
        "qh_leverage": [
            "FDE model has senior product leaders embedded inside UT — switching cost is high",
            "Outcomes data is owned in QH's audit layer, not the EHR",
        ],
        "qh_exposure": [
            "Reliance on McCaffrey as the public face — single point of failure if he leaves",
        ],
        "watch_signals": [
            "McCaffrey LinkedIn or job change",
            "UT System budget cycle (next decision: Sep 2026)",
            "TRAIGA compliance enforcement actions",
        ],
    },
    {
        "org_name": "Mercy",
        "relationship_strength": 7,
        "trajectory": "stable",
        "strategic_value": "high",
        "tailwinds": [
            "Byron Yount publicly quoted endorses 'simplify complex workflows, anticipate patient needs'",
            "Mercy's Catholic-system network creates referral path to Ascension, CommonSpirit",
            "End-to-end workflow redesign engagement = deep integration",
        ],
        "headwinds": [
            "Mercy financial pressure post-2024 margin compression may slow expansion",
            "Commure aggressive pricing in Catholic systems via shared GPO contracts",
        ],
        "qh_leverage": ["Mate's IHI lineage credibility with Catholic system quality leadership"],
        "qh_exposure": ["Limited public ROI numbers vs UTMB to use externally"],
        "watch_signals": ["Mercy CFO commentary on tech spend; Commure Catholic-system wins"],
    },
    {
        "org_name": "Jefferson Health",
        "relationship_strength": 8,
        "trajectory": "improving",
        "strategic_value": "high",
        "tailwinds": [
            "Standalone PR (3/25/2026) signals deep commitment from Jefferson side",
            "Quality registries automated days→minutes is a CFO-friendly metric",
            "Northeast academic anchor creates Penn Medicine, NYU, Mount Sinai referral path",
        ],
        "headwinds": [
            "Jefferson's Epic-heavy stack will see Epic Factory pitched aggressively",
            "Pennsylvania has not yet adopted state-level AI healthcare laws — less reg pull",
        ],
        "qh_leverage": ["Care-gap surfacing depends on cross-system data QH unifies, not Epic"],
        "qh_exposure": ["Epic Factory positioning calls in 2026"],
        "watch_signals": ["Jefferson CMIO public commentary; Epic Factory GA timing"],
    },
    {
        "org_name": "NYC Health + Hospitals",
        "relationship_strength": 6,
        "trajectory": "stable",
        "strategic_value": "high",
        "tailwinds": [
            "Largest US public system — political/credibility halo on each win",
            "Public mission alignment with QH's PBC structure",
            "OnHealthcare.tech analyst surfacing customer relationship implies quiet-confidence stage",
        ],
        "headwinds": [
            "Public-sector procurement is slow and politically exposed",
            "NY DFS Insurance Circular (7/11/2024) plus state AI activity = compliance burden on QH delivery",
            "Competing scrutiny: any AI failure at NYCHH becomes a national news cycle",
        ],
        "qh_leverage": [
            "Norgeot's ex-Elevance compliance fluency translates to NY regulator credibility",
        ],
        "qh_exposure": ["High blast radius if any audit finding goes public"],
        "watch_signals": ["NYC Mayor's Office AI policy moves; DFS enforcement"],
    },

    # ── PROSPECTS ─────────────────────────────────────────────────────────
    {
        "org_name": "Cleveland Clinic",
        "relationship_strength": 3,
        "trajectory": "stable",
        "strategic_value": "high",
        "tailwinds": [
            "Bayesian Health (sepsis) + Hippocratic AI deployments = governance demand pull",
            "Rohit Chandra (CDO) reorg creates window for new vendor evaluation",
            "Cleveland Clinic London + UAE expansion creates multi-jurisdiction governance need (EU AI Act)",
        ],
        "headwinds": [
            "Hippocratic Polaris narrative could foreclose QH's marketplace pitch",
            "Cleveland Clinic Innovations historically insources rather than partners",
            "Existing Bayesian relationship creates 'why a separate governance layer?' objection",
        ],
        "qh_leverage": [
            "Multi-vendor footprint is exactly QH's positioning sweet spot",
            "Hippocratic + Bayesian + ambient = perfect 'cross-vendor governance' demo",
        ],
        "qh_exposure": ["No public warm intro path; cold outbound disadvantage"],
        "watch_signals": [
            "Hippocratic enterprise expansion at Cleveland Clinic",
            "Cleveland Clinic CMS Innovation Center pilot announcements",
        ],
    },
    {
        "org_name": "Mayo Clinic",
        "relationship_strength": 2,
        "trajectory": "stable",
        "strategic_value": "high",
        "tailwinds": [
            "John Halamka (President, Mayo Platform) historically pro-platform partnerships",
            "Mayo Clinic Platform's own AI marketplace ambitions = peer recognition for QH",
            "Abridge enterprise creates governance demand at scribe layer",
        ],
        "headwinds": [
            "Mayo Platform itself competes for QH's positioning — partner OR competitor depending on framing",
            "Mayo's own Coral foundation model partnership narrows third-party need",
            "High switching cost from Abridge embedded in 2,000+ physicians",
        ],
        "qh_leverage": ["Norden's Stanford academic credibility opens academic-system doors"],
        "qh_exposure": ["Mayo Platform launching its own competitive products is the worst-case scenario"],
        "watch_signals": ["Mayo Platform AI marketplace announcements; Halamka public commentary"],
    },
    {
        "org_name": "HCA Healthcare",
        "relationship_strength": 2,
        "trajectory": "improving",
        "strategic_value": "critical",
        "tailwinds": [
            "Largest US for-profit IDN — single contract = market-shaking credibility",
            "Multi-EHR + multi-vendor footprint (Commure, Google MedLM, legacy Augmedix) = highest QH-fit",
            "HCA cost discipline favors a single horizontal layer over per-vendor governance",
            "Mike Schlosser (CTO) + Mangesh Patil (CAIO) — both new in role create vendor evaluation window",
        ],
        "headwinds": [
            "HCA-Commure existing relationship is multi-product (RCM, ambient, patient engagement)",
            "Google MedLM partnership is enterprise scope; Google Cloud could bundle governance",
            "HCA scale = procurement and security review process is 9-12 months minimum",
        ],
        "qh_leverage": [
            "Multi-EHR thesis is most compelling at HCA scale",
            "Patil is on record about needing a 'platform approach to AI ROI' — directly QH framing",
        ],
        "qh_exposure": [
            "If Commure expands to governance product, HCA defaults to existing vendor",
        ],
        "watch_signals": [
            "Patil/Schlosser conference talks or interviews",
            "HCA Q earnings tech-spend commentary",
            "Commure HCA expansion announcements",
        ],
    },
    {
        "org_name": "Kaiser Permanente",
        "relationship_strength": 4,
        "trajectory": "stable",
        "strategic_value": "high",
        "tailwinds": [
            "Co-founder Nirav Shah (former Kaiser SoCal COO) is structural warm-intro path",
            "Daniel Yang (VP AI) reports to CMO Andrew Bindman — clear decision tree",
            "Integrated payer-provider model means QH's payer NBL + provider product can pitch together",
            "Kaiser's vertically-integrated tech philosophy historically embraces platform plays",
        ],
        "headwinds": [
            "Abridge enterprise (24.6K physicians) is hard to dislodge",
            "Kaiser builds much of its own AI infra — third-party adoption requires uniquely defensible value",
            "Kaiser legal/compliance is among the most conservative in US healthcare",
        ],
        "qh_leverage": ["Shah warm intro is the strongest in QH's prospect set"],
        "qh_exposure": ["If Shah's involvement remains advisory rather than active, intro path weakens"],
        "watch_signals": [
            "Kaiser Permanente AI ethics board public guidance",
            "Daniel Yang or Andrew Bindman public commentary on third-party AI vendors",
        ],
    },
    {
        "org_name": "CommonSpirit Health",
        "relationship_strength": 2,
        "trajectory": "improving",
        "strategic_value": "critical",
        "tailwinds": [
            "Multi-EHR (Epic + Oracle Cerner) makes Epic Factory unviable — PERFECT QH fit",
            "Catholic-system network alignment with Mercy reference",
            "CommonSpirit financial recovery in 2025 unlocked tech budget for 2026",
        ],
        "headwinds": [
            "CommonSpirit IT consolidation post-merger still in flight = decision-making slow",
            "Daniel Barchi (CIO) historically prefers in-house builds",
        ],
        "qh_leverage": [
            "Multi-EHR governance is uniquely QH's wedge — no incumbent owns this",
            "Mercy reference is a Catholic-network credibility bridge",
        ],
        "qh_exposure": ["Long sales cycle for any large IDN at this stage of recovery"],
        "watch_signals": [
            "CommonSpirit IT spend public commentary",
            "Barchi conference talks on AI strategy",
        ],
    },

    # ── PARTNERS ──────────────────────────────────────────────────────────
    {
        "org_name": "Hackensack Meridian Health",
        "relationship_strength": 2,
        "trajectory": "improving",
        "strategic_value": "high",
        "tailwinds": [
            "New CDIO creates an executive evaluation window for AI governance vendors",
            "Northeast market adjacency lets QH reuse Jefferson and NYC H+H proof points",
            "Academic/community mix creates cross-setting governance complexity",
        ],
        "headwinds": [
            "No public QH warm-intro path yet",
            "Existing EHR and analytics vendors will frame governance as an add-on",
        ],
        "qh_leverage": ["Jefferson-style quality registry and care-gap examples are regionally credible"],
        "qh_exposure": ["Must establish executive sponsor before vendor list hardens"],
        "watch_signals": ["Joel Klein public roadmap", "AI governance hiring", "new ambient/clinical AI vendor announcements"],
    },
    {
        "org_name": "AdventHealth",
        "relationship_strength": 3,
        "trajectory": "improving",
        "strategic_value": "high",
        "tailwinds": [
            "First CAIO indicates dedicated AI budget and executive authority",
            "Faith-based system similarity makes Mercy reference unusually relevant",
            "RCM and workforce relief are CFO-friendly entry points",
        ],
        "headwinds": [
            "Large multi-state procurement can slow even high-intent AI programs",
            "New CAIO may prefer internal platform build before external governance layer",
        ],
        "qh_leverage": ["Mercy proof plus RCM coding agent maps directly to CFO/CAIO agenda"],
        "qh_exposure": ["CAIO agenda could be captured by cloud or EHR incumbents first"],
        "watch_signals": ["Rob Purinton talks", "AI center hiring", "finance transformation announcements"],
    },
    {
        "org_name": "Advocate Health",
        "relationship_strength": 2,
        "trajectory": "stable",
        "strategic_value": "high",
        "tailwinds": [
            "Very large nonprofit system creates strong enterprise-control-plane need",
            "Vendor sprawl across ambulatory, acute, and digital channels favors neutral governance",
        ],
        "headwinds": [
            "Scale creates complex stakeholder map and long cycle times",
            "Innovation office may prefer venture/partner build paths over external control plane",
        ],
        "qh_leverage": ["Emory/Mercy references fit large nonprofit operating realities"],
        "qh_exposure": ["Need a named executive pain point to avoid generic platform pitch"],
        "watch_signals": ["AI partnership announcements", "clinical automation pilots", "enterprise governance policy"],
    },
    {
        "org_name": "Mass General Brigham",
        "relationship_strength": 2,
        "trajectory": "stable",
        "strategic_value": "high",
        "tailwinds": [
            "AI-mature AMC can validate QH governance primitives with academic credibility",
            "Research workflows overlap with FDA, pharma, and model evaluation initiatives",
        ],
        "headwinds": [
            "Strong internal AI bench may resist external governance platform framing",
            "MGB may evaluate QH as a research collaborator before a buyer",
        ],
        "qh_leverage": ["Stanford/IHI/academic leadership credibility improves opener quality"],
        "qh_exposure": ["Must avoid being positioned as generic vendor instead of governance partner"],
        "watch_signals": ["new AI trial infrastructure", "model evaluation publications", "digital governance roles"],
    },
    {
        "org_name": "Providence",
        "relationship_strength": 2,
        "trajectory": "stable",
        "strategic_value": "high",
        "tailwinds": [
            "Large mission-driven footprint creates multi-state compliance and governance complexity",
            "Digital innovation history makes platform conversation credible",
        ],
        "headwinds": [
            "Providence has historically built and spun out internal digital assets",
            "Cloud incumbents may own first call on AI governance",
        ],
        "qh_leverage": ["Multi-state and workforce enablement narrative maps to Providence operating scale"],
        "qh_exposure": ["Need to differentiate from internal innovation platform efforts"],
        "watch_signals": ["AI vendor partnerships", "digital workforce programs", "state AI compliance updates"],
    },
    {
        "org_name": "Trinity Health",
        "relationship_strength": 2,
        "trajectory": "stable",
        "strategic_value": "high",
        "tailwinds": [
            "Large Catholic nonprofit system where Mercy can act as reference bridge",
            "Mission/safety framing aligns with QH's PBC and governance posture",
        ],
        "headwinds": [
            "Very large federated operating model can make enterprise standards slow to adopt",
            "Finance scrutiny may require hard ROI before broad platform sale",
        ],
        "qh_leverage": ["Mercy reference plus RCM/margin proof is the cleanest opener"],
        "qh_exposure": ["If no CFO/CEO pain is active, conversation drifts to innovation theater"],
        "watch_signals": ["workflow automation investments", "CIO changes", "system AI policy formation"],
    },
    {
        "org_name": "Anthropic",
        "relationship_strength": 9,
        "trajectory": "improving",
        "strategic_value": "critical",
        "tailwinds": [
            "Strategic Series B investor + Anthology Fund participation = aligned cap table",
            "Claude powers QH UT System workflows = production technical dependency both ways",
            "Anthropic-Anthology AI fund creates portfolio-company referral network",
            "Joint roadmap likely on healthcare-specific Claude features",
        ],
        "headwinds": [
            "Claude for Healthcare (Jan 2026 launch) signals Anthropic's healthcare-direct ambitions",
            "Microsoft Foundry partnership puts Claude in direct cloud distribution — potentially bypasses QH",
            "Anthropic-OpenAI competitive dynamics could pull priorities away from healthcare",
            "If Anthropic chooses one healthcare 'partner of record', not guaranteed QH wins",
        ],
        "qh_leverage": [
            "Anthology Fund creates structural protection — Anthropic invested in QH's success",
            "QH's healthcare-specific governance layer is non-Anthropic core",
        ],
        "qh_exposure": [
            "Disintermediation risk is real and growing through 2026-2027",
            "Model-layer pricing pressure from Anthropic could compress QH margins",
        ],
        "watch_signals": [
            "Claude for Healthcare named customer announcements",
            "Anthropic enterprise sales motion in healthcare",
            "Microsoft Foundry healthcare-specific roadmap",
        ],
    },
    {
        "org_name": "Digital Medicine Society",
        "relationship_strength": 8,
        "trajectory": "improving",
        "strategic_value": "high",
        "tailwinds": [
            "Co-authored AI Governance Toolkit announcement = definitional authority",
            "Goldsack + Norden public co-bylines compound thought leadership",
            "DiMe's FDA / regulator network is a credibility bridge for pharma NBL",
            "Open-source toolkit forces competitors to adopt QH-shaped primitives",
        ],
        "headwinds": [
            "Open-source = competitors get the basics for free; differentiation must be 'beyond toolkit'",
            "DiMe is non-profit with limited commercial leverage",
            "If DiMe partners with Epic or Microsoft, neutrality narrative weakens",
        ],
        "qh_leverage": ["Mate's IHI lineage parallels DiMe's mission orientation — cultural fit"],
        "qh_exposure": ["Toolkit governance shared with DiMe — single-source-of-truth not QH-owned"],
        "watch_signals": ["DiMe other vendor partnerships; toolkit v1 reception at HIMSS27"],
    },
    {
        "org_name": "Microsoft Azure",
        "relationship_strength": 5,
        "trajectory": "volatile",
        "strategic_value": "high",
        "tailwinds": [
            "Azure Marketplace listing live = transactional channel for Microsoft-cloud customers",
            "Microsoft healthcare GTM has 200+ system relationships = co-sell potential",
        ],
        "headwinds": [
            "Microsoft Foundry positions as the agentic governance platform = direct competitor",
            "Microsoft Dragon Copilot (200+ systems) embeds ambient — owns the documentation layer",
            "Microsoft owns Anthropic distribution via Foundry = could compress QH margin",
            "Microsoft can credibly bundle: Foundry + Dragon + Azure compliance + Claude",
        ],
        "qh_leverage": [
            "Multi-cloud positioning lets QH deflect Microsoft lock-in narrative",
        ],
        "qh_exposure": [
            "Microsoft strategic decision to make Foundry healthcare-specific would be bad for QH",
        ],
        "watch_signals": [
            "Microsoft Foundry healthcare announcements",
            "Microsoft-Epic partnership depth",
        ],
    },
    {
        "org_name": "New Enterprise Associates",
        "relationship_strength": 9,
        "trajectory": "stable",
        "strategic_value": "critical",
        "tailwinds": [
            "Mohamad Makhzoumi on board = top-tier VC pattern recognition",
            "NEA's healthcare track record (Optum, Watson Health, etc.) = network access",
            "Series B lead position = aligned through next round",
        ],
        "headwinds": [
            "Series B clock starts on Series C narrative pressure (~18-24 months)",
            "NEA portfolio conflict possible if they invest in adjacent vendor",
        ],
        "qh_leverage": ["Board seat is single-investor — no investor coalition friction"],
        "qh_exposure": ["Standard VC growth-rate pressure"],
        "watch_signals": ["NEA new healthcare AI portfolio additions; Makhzoumi public commentary"],
    },

    # ── COMPETITORS ───────────────────────────────────────────────────────
    {
        "org_name": "Epic Systems",
        "relationship_strength": 1,
        "trajectory": "deteriorating",
        "strategic_value": "critical",
        "tailwinds": [
            "Epic Factory still 'preview' at HIMSS26 — no GA date = QH first-mover window",
            "Epic-only governance creates real wedge for multi-EHR systems",
            "Health systems with Epic + Cerner + Meditech mix can't governance through Epic alone",
        ],
        "headwinds": [
            "Epic ~40% market share = path-of-least-resistance for half the addressable market",
            "Epic Factory leverages existing Epic relationship = no new procurement",
            "Epic's incumbent relationship with health system C-suite is decades-deep",
            "Epic's product velocity once they decide to ship is feared in industry",
        ],
        "qh_leverage": [
            "Epic doesn't govern third-party non-Epic vendors well",
            "Multi-EHR + non-EHR + shadow-AI inventory is QH's defensible territory",
        ],
        "qh_exposure": [
            "Epic Factory GA + Epic native ambient becoming the default forecloses 40% of TAM",
        ],
        "watch_signals": [
            "Epic Factory GA announcements",
            "Epic Healthcare AI Council guidance",
            "Health system multi-EHR consolidation moves",
        ],
    },
    {
        "org_name": "Hippocratic AI",
        "relationship_strength": 4,
        "trajectory": "volatile",
        "strategic_value": "high",
        "tailwinds": [
            "Hippocratic informally agreed to be marketplace design partner",
            "Vertically-integrated competitor framing creates 'multi-vendor neutral' QH positioning",
            "Hippocratic's $3.5B valuation makes them too large to acquire = stays a partner-or-competitor longer",
        ],
        "headwinds": [
            "Polaris Safety Constellation directly competes with QH's governance framing",
            "Hippocratic legal review at Week 3 — unresolved data residency + incident response ownership",
            "If marketplace partnership fails, Hippocratic becomes adversarial competitor with capital",
            "Patient-facing agent category gives Hippocratic native data + outcomes = strong governance moat",
        ],
        "qh_leverage": [
            "QH multi-vendor neutrality is exactly Hippocratic's vulnerability for non-Hippocratic AI",
        ],
        "qh_exposure": [
            "Hippocratic could decide to build its own marketplace = direct strategic conflict",
        ],
        "watch_signals": [
            "Hippocratic legal closure or breakdown by 5/9",
            "Hippocratic enterprise customer wins at QH prospect IDNs",
            "Hippocratic 'governance' product announcements",
        ],
    },
    {
        "org_name": "Commure",
        "relationship_strength": 1,
        "trajectory": "stable",
        "strategic_value": "high",
        "tailwinds": [
            "Commure RCM-led + Athelas + Memora wedge gives QH 'specialized governance, not RCM' positioning",
            "Commure's $6B valuation = at scale risks bureaucracy slowdown",
        ],
        "headwinds": [
            "Self-described 'Healthcare AI Operating System' = direct positional collision with QH",
            "General Catalyst funding + Customer Value Fund = patient capital advantage",
            "Multi-product wedge (Athelas RCM + Augmedix ambient + Memora engagement) = QH must partner-up to match",
        ],
        "qh_leverage": ["Governance-first positioning is more credible than RCM-first for compliance-conscious systems"],
        "qh_exposure": ["Direct competitive sales cycles will be common; price compression possible"],
        "watch_signals": ["Commure governance product announcements; HCA expansion"],
    },
    {
        "org_name": "Health Catalyst",
        "relationship_strength": 2,
        "trajectory": "stable",
        "strategic_value": "medium",
        "tailwinds": [
            "Health Catalyst is data-warehouse-shaped, not AI-runtime-shaped — adjacency, not full overlap",
            "300+ install base is also a 300+ source of AI deployments QH could govern",
        ],
        "headwinds": [
            "300+ existing health system relationships = 'they're already on Catalyst' procurement objection",
            "Public company = pricing flexibility for defensive positioning",
        ],
        "qh_leverage": ["Catalyst's analytics-first DNA limits ability to govern agentic AI well"],
        "qh_exposure": ["Catalyst could acquire smaller AI governance startups to fill the gap"],
        "watch_signals": ["Health Catalyst Healthcare.AI v2 announcements; Catalyst M&A"],
    },

    # ── REGULATORS ────────────────────────────────────────────────────────
    {
        "org_name": "Centers for Medicare & Medicaid Services",
        "relationship_strength": 5,
        "trajectory": "improving",
        "strategic_value": "critical",
        "tailwinds": [
            "Each new rule (CMS-4201-F, CMS-0057-F, CMMI WISeR) creates QH demand",
            "WISeR Model = federal blueprint that maps directly to QH's payer NBL",
            "Andy Slavitt (QH advisor) is ex-Acting CMS Administrator = senior network access",
            "Patrick Conway (QH advisor) is ex-CMMI Director = WISeR insider context",
        ],
        "headwinds": [
            "Federal preemption (3/20/2026 White House framework) would gut QH's state-tracking value",
            "CMS political turnover risk every administration cycle",
            "CMS rule-making timelines are slow and unpredictable",
        ],
        "qh_leverage": ["Slavitt + Conway advisory bench is unmatched in QH's competitive set"],
        "qh_exposure": ["Federal preemption is the single biggest external risk to QH thesis"],
        "watch_signals": [
            "Federal AI healthcare bill movement in Congress",
            "CMS RFI responses on CRUSH + Plan Finder",
            "WISeR Model first cohort announcements",
        ],
    },
    {
        "org_name": "Coalition for Health AI",
        "relationship_strength": 3,
        "trajectory": "deteriorating",
        "strategic_value": "high",
        "tailwinds": [
            "Joint Commission + CHAI partnership (June 2025) = 22K accredited orgs in funnel",
            "ARP designation becoming procurement-gating = strong demand-pull if certified",
        ],
        "headwinds": [
            "5 competitors already ARP-certified (Signal1, LensAI, ALIGNMT AI, Ferrum, ModelOp) = QH behind",
            "If ARP becomes a procurement filter and QH isn't on it, lost deals are silent",
            "CHAI's membership skews toward incumbents with whom QH is competitive",
        ],
        "qh_leverage": ["DiMe partnership creates parallel governance authority QH can leverage"],
        "qh_exposure": ["Falling further behind on ARP certification each quarter"],
        "watch_signals": ["CHAI ARP new certifications; Joint Commission AI standards finalization"],
    },
]


def merge_dynamics_into_orgs(orgs: list[dict]) -> list[dict]:
    """Merge dynamics metadata into the seed organizations by name."""
    by_name = {d["org_name"]: d for d in DYNAMICS}
    out = []
    for org in orgs:
        d = by_name.get(org["name"])
        if d:
            org["metadata"] = {
                **(org.get("metadata") or {}),
                "dynamics": {k: v for k, v in d.items() if k != "org_name"},
            }
        out.append(org)
    return out
