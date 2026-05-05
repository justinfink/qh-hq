"""Real-world organizations grounded in QH research. Used to seed the DB.

Each entry uses publicly-disclosed information only. Executives are named where
they are public. Volumes/revenues are sourced from the company's own announcements,
audited reports, or named in industry coverage.
"""
from __future__ import annotations

# Format: dict matching organizations table columns

QH_FOCAL = {
    "name": "Qualified Health",
    "short_name": "QH",
    "org_type": "ai_vendor",
    "relationship": "ecosystem",  # this row IS QH; we model it for completeness
    "hq_city": "Palo Alto",
    "hq_state": "CA",
    "region": "Bay Area",
    "size_label": "92 employees, 37 open roles",
    "size_metric": "employees",
    "size_value": 92,
    "description": (
        "Healthcare-native enterprise AI platform / 'operating layer' sold to large U.S. "
        "health systems. PBC. Founded 2024. Series B $125M (Mar 2026, NEA-led). Six-layer "
        "platform: data integration, curated solution library, agent/workflow builder, "
        "unified governance, workforce enablement, outcomes tracking. Powered by Claude. "
        "Listed on Microsoft Azure Marketplace."
    ),
    "homepage_url": "https://www.qualifiedhealthai.com",
    "metadata": {
        "is_focal": True,
        "funding_total_usd": 155_000_000,
        "valuation_low_usd": 500_000_000,
        "valuation_high_usd": 1_000_000_000,
        "headcount": 92,
        "open_roles": 37,
        "patients_served_m": 40,
        "users_served": 500_000,
        "us_hospital_revenue_pct": 7.0,
    },
}


# CUSTOMERS — publicly named health systems
CUSTOMERS: list[dict] = [
    {
        "name": "University of Texas System",
        "short_name": "UT System",
        "org_type": "idn",
        "relationship": "customer",
        "hq_city": "Austin",
        "hq_state": "TX",
        "region": "Texas",
        "size_label": "8 institutions, ~$20B+ revenue, 15K+ active QH users",
        "size_metric": "annual_revenue_usd_b",
        "size_value": 20.0,
        "description": (
            "Eight UT health institutions deploying QH enterprise-wide: UTMB, UT Health Houston, "
            "UT Southwestern, UT Health San Antonio, MD Anderson, UT Health Tyler, UT Rio Grande "
            "Valley, Dell Medical School. UTMB is QH's flagship: $15M run-rate impact in 6 "
            "months; first academic system to deploy HIPAA-compliant real-time AI web search."
        ),
        "homepage_url": "https://www.utsystem.edu",
        "metadata": {
            "deployment_users": 15000,
            "deployment_velocity_days": 30,
            "annual_value_realized_usd_m": 15,
            "anchor_executive": "Peter McCaffrey, MD (Chief AI & Digital Officer, UTMB)",
            "institutions": [
                "UT Medical Branch (UTMB)", "UT Health Houston", "UT Southwestern Medical Center",
                "UT Health San Antonio", "MD Anderson Cancer Center", "UT Health Tyler",
                "UT Rio Grande Valley", "Dell Medical School at UT Austin",
            ],
        },
    },
    {
        "name": "Emory Healthcare",
        "short_name": "Emory",
        "org_type": "amc",
        "relationship": "customer",
        "hq_city": "Atlanta",
        "hq_state": "GA",
        "region": "Southeast",
        "size_label": "11 hospitals, ~$6B revenue",
        "size_metric": "annual_revenue_usd_b",
        "size_value": 6.0,
        "description": "Emory University Health Sciences Center. Named QH customer per Series B PR.",
        "homepage_url": "https://www.emoryhealthcare.org",
        "metadata": {"hospitals": 11},
    },
    {
        "name": "Jefferson Health",
        "short_name": "Jefferson",
        "org_type": "idn",
        "relationship": "customer",
        "hq_city": "Philadelphia",
        "hq_state": "PA",
        "region": "Mid-Atlantic",
        "size_label": "32 hospitals, ~$10B revenue",
        "size_metric": "annual_revenue_usd_b",
        "size_value": 10.0,
        "description": (
            "Jefferson Health (Thomas Jefferson University Hospitals). Use cases: quality "
            "registries automated from days to minutes, care-gap surfacing, admin automation. "
            "Standalone PR Mar 25, 2026."
        ),
        "homepage_url": "https://www.jeffersonhealth.org",
        "metadata": {"hospitals": 32},
    },
    {
        "name": "Mercy",
        "short_name": "Mercy",
        "org_type": "idn",
        "relationship": "customer",
        "hq_city": "Chesterfield",
        "hq_state": "MO",
        "region": "Midwest",
        "size_label": "50+ hospitals, ~$10B revenue",
        "size_metric": "annual_revenue_usd_b",
        "size_value": 10.0,
        "description": (
            "Mercy Health (St. Louis-headquartered Catholic system). Use case: end-to-end "
            "workflow redesign with QH. Quoted: Byron Yount."
        ),
        "homepage_url": "https://www.mercy.net",
        "metadata": {"anchor_executive": "Byron Yount"},
    },
    {
        "name": "University of Rochester Medicine",
        "short_name": "URMC",
        "org_type": "amc",
        "relationship": "customer",
        "hq_city": "Rochester",
        "hq_state": "NY",
        "region": "Northeast",
        "size_label": "7 hospitals, ~$5B revenue",
        "size_metric": "annual_revenue_usd_b",
        "size_value": 5.0,
        "description": "University of Rochester Medical Center. Named QH customer per Series B PR.",
        "homepage_url": "https://www.urmc.rochester.edu",
        "metadata": {"hospitals": 7},
    },
    {
        "name": "NYC Health + Hospitals",
        "short_name": "NYC H+H",
        "org_type": "idn",
        "relationship": "customer",
        "hq_city": "New York",
        "hq_state": "NY",
        "region": "Northeast",
        "size_label": "11 hospitals, ~$11B revenue, largest US public system",
        "size_metric": "annual_revenue_usd_b",
        "size_value": 11.0,
        "description": (
            "NYC Health + Hospitals — largest U.S. public health system. Surfaced as a QH "
            "deployment in OnHealthcare.tech analyst coverage."
        ),
        "homepage_url": "https://www.nychealthandhospitals.org",
        "metadata": {"hospitals": 11, "is_public_system": True},
    },
]


# PROSPECTS — publicly known IDNs likely in QH's expansion path
PROSPECTS: list[dict] = [
    {
        "name": "Cleveland Clinic",
        "short_name": "Cleveland Clinic",
        "org_type": "amc",
        "relationship": "prospect",
        "hq_city": "Cleveland", "hq_state": "OH", "region": "Midwest",
        "size_label": "~$15B revenue, 22 hospitals",
        "size_metric": "annual_revenue_usd_b", "size_value": 15.0,
        "description": "Active deployment of Bayesian Health (sepsis) + Hippocratic AI agents. Strong adjacent vendor footprint creates governance demand.",
        "homepage_url": "https://my.clevelandclinic.org",
        "metadata": {"competing_ai_vendors": ["Bayesian Health", "Hippocratic AI"]},
    },
    {
        "name": "Mayo Clinic",
        "short_name": "Mayo",
        "org_type": "amc",
        "relationship": "prospect",
        "hq_city": "Rochester", "hq_state": "MN", "region": "Midwest",
        "size_label": "~$17B revenue, 23 hospitals",
        "size_metric": "annual_revenue_usd_b", "size_value": 17.0,
        "description": "Abridge enterprise customer (2,000+ physicians + nursing pilots). Abridge platform-creep into care intelligence creates QH wedge for cross-vendor governance.",
        "homepage_url": "https://www.mayoclinic.org",
        "metadata": {"competing_ai_vendors": ["Abridge"]},
    },
    {
        "name": "HCA Healthcare",
        "short_name": "HCA",
        "org_type": "idn",
        "relationship": "prospect",
        "hq_city": "Nashville", "hq_state": "TN", "region": "Southeast",
        "size_label": "~$70B revenue, 188 hospitals (largest for-profit US system)",
        "size_metric": "annual_revenue_usd_b", "size_value": 70.0,
        "description": "Multi-vendor AI footprint: Commure ambient, Google MedLM ED documentation pilot, Augmedix legacy contracts. Multi-EHR exposure is QH's strongest counter to Epic Factory.",
        "homepage_url": "https://hcahealthcare.com",
        "metadata": {"competing_ai_vendors": ["Commure", "Google MedLM", "Augmedix"]},
    },
    {
        "name": "Kaiser Permanente",
        "short_name": "Kaiser",
        "org_type": "idn",
        "relationship": "prospect",
        "hq_city": "Oakland", "hq_state": "CA", "region": "West",
        "size_label": "~$100B revenue, integrated payer-provider, 12.5M members",
        "size_metric": "annual_revenue_usd_b", "size_value": 100.0,
        "description": "Abridge enterprise customer (24,600 physicians, 40 hospitals). Co-founder Nirav R. Shah is former Kaiser SoCal COO — warm intro path.",
        "homepage_url": "https://about.kaiserpermanente.org",
        "metadata": {"competing_ai_vendors": ["Abridge"], "warm_intro_path": "Nirav Shah (QH co-founder)"},
    },
    {
        "name": "CommonSpirit Health",
        "short_name": "CommonSpirit",
        "org_type": "idn",
        "relationship": "prospect",
        "hq_city": "Chicago", "hq_state": "IL", "region": "Multi-region",
        "size_label": "~$35B revenue, 140+ hospitals, multi-EHR (Epic + Cerner)",
        "size_metric": "annual_revenue_usd_b", "size_value": 35.0,
        "description": "Multi-EHR footprint (Epic + Oracle Cerner) — cannot governance through Epic Factory alone. Highest-fit prospect for QH's multi-EHR thesis.",
        "homepage_url": "https://www.commonspirit.org",
        "metadata": {"ehrs": ["Epic", "Oracle Cerner"], "fit_score": "high"},
    },
    {
        "name": "Northwell Health",
        "short_name": "Northwell",
        "org_type": "idn",
        "relationship": "prospect",
        "hq_city": "New Hyde Park", "hq_state": "NY", "region": "Northeast",
        "size_label": "~$18B revenue, 21 hospitals",
        "size_metric": "annual_revenue_usd_b", "size_value": 18.0,
        "description": "Largest healthcare provider in NY State. Active AI program; Aegis Ventures NYC connection.",
        "homepage_url": "https://www.northwell.edu",
        "metadata": {},
    },
]


# COMPETITORS / ADJACENT AI VENDORS
COMPETITORS: list[dict] = [
    {
        "name": "Hippocratic AI",
        "short_name": "Hippocratic",
        "org_type": "ai_vendor",
        "relationship": "competitor",
        "hq_city": "Palo Alto", "hq_state": "CA", "region": "Bay Area",
        "size_label": "$404M raised, $3.5B val (Series C Nov 2025)",
        "size_metric": "valuation_usd_b", "size_value": 3.5,
        "description": (
            "Vertically integrated patient-facing clinical agents. Polaris Safety Constellation "
            "Architecture is explicit safety/governance moat at the model layer — direct "
            "competitive framing with QH. 50+ health systems, 115M+ patient interactions."
        ),
        "homepage_url": "https://hippocraticai.com",
        "metadata": {
            "funding_total_usd_m": 404, "latest_round": "Series C Nov 2025 ($126M, Avenir Growth)",
            "named_customers": ["Cleveland Clinic", "Northwestern Medicine", "Ochsner Health",
                                "Moffitt Cancer Center", "University Hospitals", "Advocate Health",
                                "Cincinnati Children's", "Sanford Health", "OhioHealth", "Memorial Hermann"],
            "threat_level": "highest_among_agent_vendors",
        },
    },
    {
        "name": "Abridge",
        "short_name": "Abridge",
        "org_type": "ai_vendor",
        "relationship": "competitor",
        "hq_city": "Pittsburgh", "hq_state": "PA", "region": "Northeast",
        "size_label": "$300M Series E, $5.3B val (June 2025)",
        "size_metric": "valuation_usd_b", "size_value": 5.3,
        "description": (
            "Ambient scribe expanding into 'care intelligence' — explicit platform-creep "
            "language that signals ambitions beyond documentation. 150+ enterprise systems."
        ),
        "homepage_url": "https://www.abridge.com",
        "metadata": {
            "funding_total_usd_m": 600, "latest_round": "Series E June 2025 ($300M, a16z + Khosla)",
            "named_customers": ["Johns Hopkins", "Kaiser Permanente", "Mayo Clinic", "Duke Health",
                                "UPMC", "Yale New Haven"],
            "threat_level": "medium_high_platform_creep",
        },
    },
    {
        "name": "Commure",
        "short_name": "Commure",
        "org_type": "ai_vendor",
        "relationship": "competitor",
        "hq_city": "San Francisco", "hq_state": "CA", "region": "Bay Area",
        "size_label": "$6B val, $200M GC financing (June 2025)",
        "size_metric": "valuation_usd_b", "size_value": 6.0,
        "description": (
            "Self-described 'Healthcare AI Operating System' — direct platform overlap with QH. "
            "Multi-product wedge via Athelas (RCM/RPM), Augmedix (ambient), Memora Health "
            "(patient engagement). 130+ health systems including HCA."
        ),
        "homepage_url": "https://www.commure.com",
        "metadata": {
            "valuation_usd_b": 6.0, "named_customers": ["HCA Healthcare"],
            "threat_level": "highest_ambient_adjacent",
            "acquisitions": ["Augmedix (Oct 2024, $139M)", "Memora Health (Dec 2024)", "Athelas (2023)"],
        },
    },
    {
        "name": "Microsoft Dragon Copilot",
        "short_name": "Dragon Copilot",
        "org_type": "ai_vendor",
        "relationship": "competitor",
        "hq_city": "Redmond", "hq_state": "WA", "region": "Pacific NW",
        "size_label": "200+ health systems, 10K+ clinicians",
        "size_metric": "customers", "size_value": 200,
        "description": (
            "Microsoft Nuance + DAX Copilot merged March 2025. Embedded in Epic. Anthropic "
            "Claude available via Microsoft Foundry as of Jan 2026 specifically for healthcare. "
            "Cloud-incumbent existential threat at the platform level."
        ),
        "homepage_url": "https://www.microsoft.com/en-us/health-solutions/clinical-workflow/dragon-copilot",
        "metadata": {
            "parent": "Microsoft (Nuance acquired 2022, ~$19.7B)",
            "threat_level": "highest_platform_level",
        },
    },
    {
        "name": "Suki AI",
        "short_name": "Suki",
        "org_type": "ai_vendor",
        "relationship": "competitor",
        "hq_city": "Redwood City", "hq_state": "CA", "region": "Bay Area",
        "size_label": "$165M raised, Series D (2024)",
        "size_metric": "funding_total_usd_m", "size_value": 165,
        "description": (
            "Ambient scribe with growing developer-platform positioning (Suki Platform as "
            "infrastructure for other vendors). MEDITECH Expanse + athenahealth integrations."
        ),
        "homepage_url": "https://www.suki.ai",
        "metadata": {"named_customers": ["MedStar Health", "FMOL Health", "McLeod", "Rush"]},
    },
    {
        "name": "OpenEvidence",
        "short_name": "OpenEvidence",
        "org_type": "ai_vendor",
        "relationship": "regulator_watch",  # shadow-AI inventory target
        "hq_city": "Cambridge", "hq_state": "MA", "region": "Northeast",
        "size_label": "$12B val, Series D Jan 2026 ($250M)",
        "size_metric": "valuation_usd_b", "size_value": 12.0,
        "description": (
            "'Medical superintelligence' — point-of-care evidence answers. Free-to-physicians, "
            "monetized by pharma. ~18M consultations, ~40% of US physicians use daily. "
            "Classic 'shadow AI' target for QH governance inventory."
        ),
        "homepage_url": "https://www.openevidence.com",
        "metadata": {"physicians_using_pct": 40, "monthly_consultations_m": 1.5},
    },
    {
        "name": "Tempus AI",
        "short_name": "Tempus",
        "org_type": "ai_vendor",
        "relationship": "ecosystem",
        "hq_city": "Chicago", "hq_state": "IL", "region": "Midwest",
        "size_label": "NASDAQ: TEM, $955M 2025 revenue",
        "size_metric": "annual_revenue_usd_m", "size_value": 955,
        "description": "Multi-modal precision medicine; Tempus One generative AI assistant for oncologists. Possible QH partner (governance for Tempus One in oncology workflows).",
        "homepage_url": "https://www.tempus.com",
        "metadata": {"ticker": "TEM", "guidance_2026_revenue_usd_b": 1.59},
    },
    {
        "name": "Aidoc",
        "short_name": "Aidoc",
        "org_type": "ai_vendor",
        "relationship": "ecosystem",
        "hq_city": "Tel Aviv", "hq_state": "IL", "region": "International",
        "size_label": "$500M+ raised, Series E $150M (2026)",
        "size_metric": "funding_total_usd_m", "size_value": 500,
        "description": "Imaging AI orchestration ('aiOS'). 30+ FDA approvals. ~2,000 hospitals. Adjacency: imaging governance overlap.",
        "homepage_url": "https://www.aidoc.com",
        "metadata": {"fda_approvals": 30, "hospitals": 2000},
    },
    {
        "name": "Health Catalyst",
        "short_name": "Health Catalyst",
        "org_type": "governance_competitor",
        "relationship": "competitor",
        "hq_city": "South Jordan", "hq_state": "UT", "region": "Mountain West",
        "size_label": "NASDAQ: HCAT, ~$400-500M market cap",
        "size_metric": "market_cap_usd_m", "size_value": 450,
        "description": (
            "Public incumbent (300+ health system install base). Launched 'Healthcare.AI' "
            "governance offering on top of analytics platform. Path-of-least-resistance threat "
            "for CIOs already on Catalyst."
        ),
        "homepage_url": "https://www.healthcatalyst.com",
        "metadata": {"ticker": "HCAT", "install_base": 300},
    },
    {
        "name": "Cohere Health",
        "short_name": "Cohere Health",
        "org_type": "ai_vendor",
        "relationship": "competitor",
        "hq_city": "Boston", "hq_state": "MA", "region": "Northeast",
        "size_label": "$200M raised, Series C $90M May 2025",
        "size_metric": "funding_total_usd_m", "size_value": 200,
        "description": (
            "Payer-side prior auth & utilization management AI. 94% provider satisfaction; "
            "85% real-time auth approvals. Direct fit to QH's payer-side NBL thesis."
        ),
        "homepage_url": "https://www.coherehealth.com",
        "metadata": {"acquisitions": ["ZignaAI (Sep 2025, payment integrity)"]},
    },
    {
        "name": "Bayesian Health",
        "short_name": "Bayesian",
        "org_type": "ai_vendor",
        "relationship": "ecosystem",
        "hq_city": "Baltimore", "hq_state": "MD", "region": "Mid-Atlantic",
        "size_label": "Seed-stage, NSF + a16z + Khosla",
        "size_metric": "customers", "size_value": 13,
        "description": "Sepsis detection (TREWS algorithm). 13 Cleveland Clinic hospitals. Spinout from Johns Hopkins (Suchi Saria).",
        "homepage_url": "https://www.bayesianhealth.com",
        "metadata": {},
    },
]


# PARTNERS, INVESTORS, ECOSYSTEM
PARTNERS: list[dict] = [
    {
        "name": "Anthropic",
        "short_name": "Anthropic",
        "org_type": "ai_vendor",
        "relationship": "partner",
        "hq_city": "San Francisco", "hq_state": "CA", "region": "Bay Area",
        "size_label": "Strategic Series B investor",
        "size_metric": "strategic_relationship", "size_value": 1,
        "description": (
            "Strategic investor on QH Series B. Anthology Fund (Menlo Ventures' Anthropic-"
            "affiliated AI fund) also participated. Claude powers QH's clinical and admin "
            "workflows on UT System. Launched 'Claude for Healthcare' Jan 2026 at JPM."
        ),
        "homepage_url": "https://www.anthropic.com",
        "metadata": {"relationship_strength": "structural"},
    },
    {
        "name": "Digital Medicine Society",
        "short_name": "DiMe",
        "org_type": "thought_leadership",
        "relationship": "partner",
        "hq_city": "Boston", "hq_state": "MA", "region": "Northeast",
        "size_label": "Non-profit thought leadership org",
        "size_metric": "membership", "size_value": 0,
        "description": (
            "Co-developing AI Governance Toolkit (open source). Templates, scorecards, "
            "dashboards, workflows for operationalizing healthcare AI governance. "
            "Co-authored by Norden + Jennifer Goldsack (DiMe CEO)."
        ),
        "homepage_url": "https://www.dimesociety.org",
        "metadata": {"anchor_executive": "Jennifer Goldsack (CEO)"},
    },
    {
        "name": "New Enterprise Associates",
        "short_name": "NEA",
        "org_type": "investor",
        "relationship": "investor",
        "hq_city": "Chevy Chase", "hq_state": "MD", "region": "Mid-Atlantic",
        "size_label": "Series B lead, $125M (Mar 2026)",
        "size_metric": "investment_usd_m", "size_value": 125,
        "description": "Series B lead investor. Mohamad Makhzoumi (Co-CEO/Managing GP) joined QH board.",
        "homepage_url": "https://www.nea.com",
        "metadata": {"board_member": "Mohamad Makhzoumi"},
    },
    {
        "name": "Microsoft Azure",
        "short_name": "Microsoft Azure",
        "org_type": "cloud_provider",
        "relationship": "partner",
        "hq_city": "Redmond", "hq_state": "WA", "region": "Pacific NW",
        "size_label": "Marketplace listing live",
        "size_metric": "channel", "size_value": 1,
        "description": "QH listed on Microsoft Azure Marketplace (SaaS product ID qualifiedhealth.deecd82d-cd6b-437b-9bae-f463301907be). Implies Azure deployment + Microsoft cloud-marketplace transactability.",
        "homepage_url": "https://azuremarketplace.microsoft.com",
        "metadata": {},
    },
    {
        "name": "Epic Systems",
        "short_name": "Epic",
        "org_type": "ehr_vendor",
        "relationship": "competitor",  # Epic Factory is the existential threat
        "hq_city": "Verona", "hq_state": "WI", "region": "Midwest",
        "size_label": "~40% US acute-care market share",
        "size_metric": "market_share_pct", "size_value": 40,
        "description": (
            "Epic Factory (visual builder for AI agents with audit/policy/local-knowledge) is "
            "QH's single largest existential threat. Epic-only governance creates QH wedge for "
            "multi-EHR systems. HIMSS26 'preview', no GA date."
        ),
        "homepage_url": "https://www.epic.com",
        "metadata": {"products": ["Art", "Emmie", "Cosmos AI", "Curiosity", "Epic Factory"]},
    },
    {
        "name": "Oracle Health",
        "short_name": "Oracle Health",
        "org_type": "ehr_vendor",
        "relationship": "ecosystem",
        "hq_city": "Austin", "hq_state": "TX", "region": "Texas",
        "size_label": "~25% US acute-care market share (post-Cerner)",
        "size_metric": "market_share_pct", "size_value": 25,
        "description": "AI-first EHR launched late 2025. Explicitly designed for third-party model integration. Probable partner channel for QH at non-Epic systems.",
        "homepage_url": "https://www.oracle.com/health",
        "metadata": {"openness": "high"},
    },
]


# REGULATORS
REGULATORS: list[dict] = [
    {
        "name": "Centers for Medicare & Medicaid Services",
        "short_name": "CMS",
        "org_type": "regulator",
        "relationship": "regulator_watch",
        "hq_city": "Baltimore", "hq_state": "MD", "region": "Mid-Atlantic",
        "size_label": "Federal payer regulator",
        "size_metric": "is_federal", "size_value": 1,
        "description": (
            "CMS-4201-F (2024 MA Final Rule) bars AI as sole basis for coverage denials. "
            "CMS-0057-F (FHIR API mandate effective 2026). CMMI WISeR Model launched Jan 2026 "
            "for clinician-in-the-loop AI utilization mgmt — federal blueprint for QH's payer NBL."
        ),
        "homepage_url": "https://www.cms.gov",
        "metadata": {"key_rules": ["CMS-4201-F", "CMS-0057-F", "CMMI WISeR"]},
    },
    {
        "name": "Office of the National Coordinator for Health IT",
        "short_name": "ONC / ASTP",
        "org_type": "regulator",
        "relationship": "regulator_watch",
        "hq_city": "Washington", "hq_state": "DC", "region": "Mid-Atlantic",
        "size_label": "Federal HIT regulator",
        "size_metric": "is_federal", "size_value": 1,
        "description": (
            "HTI-1 final rule (FR 1/9/2024, DSI compliance 1/1/2025). DSI source attributes "
            "(31 attributes / 9 categories) is the single most product-shaping regulation for "
            "QH's home-turf governance product. HTI-2 + 12/2025 Clinical AI RFI in flight."
        ),
        "homepage_url": "https://www.healthit.gov",
        "metadata": {"key_rules": ["HTI-1 DSI", "HTI-2", "Clinical AI RFI"]},
    },
    {
        "name": "Food and Drug Administration",
        "short_name": "FDA",
        "org_type": "regulator",
        "relationship": "regulator_watch",
        "hq_city": "Silver Spring", "hq_state": "MD", "region": "Mid-Atlantic",
        "size_label": "Federal medical device regulator",
        "size_metric": "is_federal", "size_value": 1,
        "description": (
            "PCCP final guidance (Dec 2024 / Aug 2025 expansion). AI Lifecycle Management "
            "draft (Jan 2025). GMLP Guiding Principles (2021 + Jan 2025 IMDRF update). "
            "Transparency Principles (June 2024)."
        ),
        "homepage_url": "https://www.fda.gov",
        "metadata": {"key_rules": ["PCCP", "AI Lifecycle Mgmt", "GMLP", "Transparency"]},
    },
    {
        "name": "Coalition for Health AI",
        "short_name": "CHAI",
        "org_type": "thought_leadership",
        "relationship": "regulator_watch",
        "hq_city": "Boston", "hq_state": "MA", "region": "Northeast",
        "size_label": "Industry coalition (22K+ accredited orgs reach via JC)",
        "size_metric": "is_certifying_body", "size_value": 1,
        "description": (
            "CHAI ARP designation becoming procurement-gating credential. Joint Commission "
            "+ CHAI partnership (June 2025). Already certified: Signal1, LensAI, ALIGNMT AI, "
            "Ferrum, ModelOp. QH should evaluate ARP path."
        ),
        "homepage_url": "https://chai.org",
        "metadata": {"already_certified_competitors": ["Signal1", "LensAI", "ALIGNMT AI", "Ferrum", "ModelOp"]},
    },
    {
        "name": "The Joint Commission",
        "short_name": "Joint Commission",
        "org_type": "thought_leadership",
        "relationship": "regulator_watch",
        "hq_city": "Oakbrook Terrace", "hq_state": "IL", "region": "Midwest",
        "size_label": "22,000+ accredited healthcare organizations",
        "size_metric": "accredited_orgs", "size_value": 22000,
        "description": (
            "Responsible Use of Health Data (RUHD) Certification (eff. 1/1/2024). "
            "JC + CHAI partnership June 2025; AI guidance Sep 17, 2025. Anticipated "
            "AI certification in 2026."
        ),
        "homepage_url": "https://www.jointcommission.org",
        "metadata": {"key_credentials": ["RUHD", "Anticipated AI certification"]},
    },
]
