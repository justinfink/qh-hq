"""Named executives, customer leaders, and partners. Sourced from research dossiers.
All publicly available via LinkedIn, press releases, or org websites.
"""
from __future__ import annotations

# Format: (org_name, name, title, role_category, linkedin_url, notes)
CONTACTS: list[dict] = [
    # QH leadership
    {"org": "Qualified Health", "name": "Justin Norden, MD MBA MPhil", "title": "Co-founder & CEO",
     "role_category": "ceo",
     "linkedin": "https://www.linkedin.com/in/justin-norden",
     "notes": "Stanford MD/MBA. Adjunct Stanford Medicine. Prior: Trustworthy AI (acq Waymo), GSR Ventures partner, Apple Health."},
    {"org": "Qualified Health", "name": "Kedar Mate, MD", "title": "Co-founder & Chief Medical Officer",
     "role_category": "cmo",
     "linkedin": "https://www.linkedin.com/in/kedarmatemd",
     "notes": "Former President & CEO of Institute for Healthcare Improvement (IHI). Weill Cornell faculty."},
    {"org": "Qualified Health", "name": "Shantanu Phatakwala", "title": "Co-founder & Chief Commercial Officer",
     "role_category": "cco",
     "linkedin": None,
     "notes": "Prior: Haven Chief Data Science Officer; Evolent VP R&D; Resolution Health (acq Anthem)."},
    {"org": "Qualified Health", "name": "Beau Norgeot, PhD", "title": "Co-founder & Chief AI Officer",
     "role_category": "cto",
     "linkedin": None,
     "notes": "Prior: VP of AI at Elevance Health (NYSE: ELV). UCSF PhD, AI/ML & personalized medicine."},
    {"org": "Qualified Health", "name": "Nirav R. Shah, MD MPH", "title": "Co-founder",
     "role_category": "advisor",
     "linkedin": None,
     "notes": "Former COO Kaiser Permanente Southern California. Former NY State Health Commissioner. Stanford Medicine faculty."},
    {"org": "Qualified Health", "name": "Nicholas Chedid, MD MBA", "title": "Associate Chief Medical Officer",
     "role_category": "leadership",
     "linkedin": None, "notes": "Visible via UC Berkeley Haas recruiting."},
    {"org": "Qualified Health", "name": "Matthew Lungren, MD MPH", "title": "GM Technical Advisor / Office of CTO",
     "role_category": "advisor",
     "linkedin": None,
     "notes": "Formerly Chief Scientific Officer, Microsoft Health & Life Sciences."},

    # Customers — UTMB
    {"org": "University of Texas System", "name": "Peter McCaffrey, MD", "title": "Chief AI & Digital Officer, UTMB",
     "role_category": "caio",
     "linkedin": None,
     "notes": "Quoted: 'The ROI has already exceeded expectations.' UTMB anchor exec for QH."},

    # Customers — Mercy
    {"org": "Mercy", "name": "Byron Yount", "title": "Mercy Health (operations)",
     "role_category": "operations",
     "linkedin": None,
     "notes": "Quoted on QH partnership: 'AI allows us to simplify complex workflows, anticipate patient needs earlier.'"},

    # Prospects — Cleveland Clinic
    {"org": "Cleveland Clinic", "name": "Rohit Chandra", "title": "Chief Digital Officer",
     "role_category": "cdo",
     "linkedin": None, "notes": "Active deployment of Bayesian Health (sepsis) + Hippocratic AI agents."},

    # Prospects — Mayo
    {"org": "Mayo Clinic", "name": "John Halamka, MD MS", "title": "President, Mayo Clinic Platform",
     "role_category": "platform_president",
     "linkedin": None, "notes": "Mayo Clinic Platform President. Drives Mayo's external AI program. Abridge enterprise customer."},

    # Prospects — HCA
    {"org": "HCA Healthcare", "name": "Mike Schlosser", "title": "Chief Technology Officer",
     "role_category": "cto",
     "linkedin": None, "notes": "HCA CTO. Multi-vendor AI footprint (Commure ambient, Google MedLM ED pilot)."},
    {"org": "HCA Healthcare", "name": "Mangesh Patil", "title": "Chief AI Officer",
     "role_category": "caio",
     "linkedin": None, "notes": "HCA's first CAIO. Multi-EHR enterprise — fits QH multi-EHR thesis."},

    # Prospects — Kaiser
    {"org": "Kaiser Permanente", "name": "Daniel Yang, MD", "title": "VP, AI / Augmented Intelligence in Medicine",
     "role_category": "vp_ai",
     "linkedin": None, "notes": "Reports to CMO Andrew Bindman. Abridge enterprise deployment."},
    {"org": "Kaiser Permanente", "name": "Andrew Bindman, MD", "title": "Chief Medical Officer",
     "role_category": "cmo",
     "linkedin": None, "notes": "Kaiser CMO. Warm intro path via QH co-founder Nirav Shah (former Kaiser SoCal COO)."},

    # Prospects — Northwell
    {"org": "Northwell Health", "name": "Tom Manning", "title": "Chairman, Ascertain (Northwell AI venture)",
     "role_category": "ai_executive",
     "linkedin": None, "notes": "Aegis Ventures + Northwell collaboration. Active healthcare AI investor."},

    # Prospects — CommonSpirit
    {"org": "CommonSpirit Health", "name": "Daniel Barchi", "title": "Chief Information Officer",
     "role_category": "cio",
     "linkedin": None, "notes": "CommonSpirit CIO. Multi-EHR (Epic + Cerner) — highest-fit for QH multi-EHR thesis."},

    # Pharma — Pfizer
    {"org": "Pfizer", "name": "Lidia Fonseca", "title": "Chief Digital & Technology Officer",
     "role_category": "cdto",
     "linkedin": None, "notes": "Pfizer CDTO. Open to 30-min intro via DiMe contact."},
    {"org": "Pfizer", "name": "Berta Rodriguez-Hervas, PhD", "title": "Chief AI & Analytics Officer",
     "role_category": "caio",
     "linkedin": None, "notes": "Pfizer CAIO. Direct counterpart for governance discussions."},

    # Pharma — Lilly
    {"org": "Eli Lilly", "name": "Thomas Fuchs, PhD", "title": "Chief AI Officer",
     "role_category": "caio",
     "linkedin": None, "notes": "Lilly's first CAIO (appointed Oct 2024). High-priority pharma target."},

    # Pharma — AstraZeneca
    {"org": "AstraZeneca", "name": "Jim Weatherall, PhD", "title": "Chief Data Scientist",
     "role_category": "cds",
     "linkedin": None, "notes": "AstraZeneca clinical innovation flagged interest at HIMSS26."},

    # Partner — DiMe
    {"org": "Digital Medicine Society", "name": "Jennifer Goldsack", "title": "Co-founder & CEO",
     "role_category": "ceo",
     "linkedin": None, "notes": "Co-author of QH-DiMe AI Governance Toolkit announcement (4/15/2026)."},

    # Investor — NEA
    {"org": "New Enterprise Associates", "name": "Mohamad Makhzoumi", "title": "Co-CEO / Managing GP",
     "role_category": "investor",
     "linkedin": None, "notes": "Joined QH board on Series B."},

    # Competitor — Hippocratic
    {"org": "Hippocratic AI", "name": "Munjal Shah", "title": "Co-founder & CEO",
     "role_category": "ceo",
     "linkedin": None, "notes": "Polaris Safety Constellation Architecture is competitive framing vs QH."},
]
